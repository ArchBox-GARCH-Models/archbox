"""Markov-Switching Mean and Mean-Variance models.

Implements the simplest Markov-Switching models:
- MarkovSwitchingMean: only the mean switches between regimes
- MarkovSwitchingMeanVar: both mean and variance switch

These are simplified versions of Hamilton (1989) without AR dynamics.

References
----------
Hamilton, J.D. (1989). A New Approach to the Economic Analysis of
Nonstationary Time Series and the Business Cycle.
Econometrica, 57(2), 357-384.
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


class MarkovSwitchingMean(MarkovSwitchingModel):
    """Markov-Switching Mean model.

    Only the mean switches between regimes. The variance is constant
    across all regimes.

    y_t | S_t = s ~ N(mu_s, sigma^2)

    Parameters
    ----------
    endog : array-like
        Time series of observations, shape (T,).
    k_regimes : int
        Number of regimes. Default is 2.

    Examples
    --------
    >>> import numpy as np
    >>> from archbox.regime.ms_mean import MarkovSwitchingMean
    >>> y = np.random.randn(200)
    >>> model = MarkovSwitchingMean(y, k_regimes=2)
    >>> results = model.fit()
    >>> print(results.summary())
    """

    model_name: str = "MS-Mean"

    def __init__(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        args = [endog, k_regimes]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMarkovSwitchingMeanǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁMarkovSwitchingMeanǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMarkovSwitchingMeanǁ__init____mutmut_orig(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean model."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=0,
            switching_mean=True,
            switching_variance=False,
            switching_ar=False,
        )

    def xǁMarkovSwitchingMeanǁ__init____mutmut_1(
        self,
        endog: Any,
        k_regimes: int = 3,
    ) -> None:
        """Initialize Markov-Switching Mean model."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=0,
            switching_mean=True,
            switching_variance=False,
            switching_ar=False,
        )

    def xǁMarkovSwitchingMeanǁ__init____mutmut_2(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean model."""
        super().__init__(
            None,
            k_regimes=k_regimes,
            order=0,
            switching_mean=True,
            switching_variance=False,
            switching_ar=False,
        )

    def xǁMarkovSwitchingMeanǁ__init____mutmut_3(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean model."""
        super().__init__(
            endog,
            k_regimes=None,
            order=0,
            switching_mean=True,
            switching_variance=False,
            switching_ar=False,
        )

    def xǁMarkovSwitchingMeanǁ__init____mutmut_4(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean model."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=None,
            switching_mean=True,
            switching_variance=False,
            switching_ar=False,
        )

    def xǁMarkovSwitchingMeanǁ__init____mutmut_5(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean model."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=0,
            switching_mean=None,
            switching_variance=False,
            switching_ar=False,
        )

    def xǁMarkovSwitchingMeanǁ__init____mutmut_6(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean model."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=0,
            switching_mean=True,
            switching_variance=None,
            switching_ar=False,
        )

    def xǁMarkovSwitchingMeanǁ__init____mutmut_7(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean model."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=0,
            switching_mean=True,
            switching_variance=False,
            switching_ar=None,
        )

    def xǁMarkovSwitchingMeanǁ__init____mutmut_8(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean model."""
        super().__init__(
            k_regimes=k_regimes,
            order=0,
            switching_mean=True,
            switching_variance=False,
            switching_ar=False,
        )

    def xǁMarkovSwitchingMeanǁ__init____mutmut_9(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean model."""
        super().__init__(
            endog,
            order=0,
            switching_mean=True,
            switching_variance=False,
            switching_ar=False,
        )

    def xǁMarkovSwitchingMeanǁ__init____mutmut_10(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean model."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            switching_mean=True,
            switching_variance=False,
            switching_ar=False,
        )

    def xǁMarkovSwitchingMeanǁ__init____mutmut_11(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean model."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=0,
            switching_variance=False,
            switching_ar=False,
        )

    def xǁMarkovSwitchingMeanǁ__init____mutmut_12(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean model."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=0,
            switching_mean=True,
            switching_ar=False,
        )

    def xǁMarkovSwitchingMeanǁ__init____mutmut_13(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean model."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=0,
            switching_mean=True,
            switching_variance=False,
        )

    def xǁMarkovSwitchingMeanǁ__init____mutmut_14(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean model."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=1,
            switching_mean=True,
            switching_variance=False,
            switching_ar=False,
        )

    def xǁMarkovSwitchingMeanǁ__init____mutmut_15(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean model."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=0,
            switching_mean=False,
            switching_variance=False,
            switching_ar=False,
        )

    def xǁMarkovSwitchingMeanǁ__init____mutmut_16(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean model."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=0,
            switching_mean=True,
            switching_variance=True,
            switching_ar=False,
        )

    def xǁMarkovSwitchingMeanǁ__init____mutmut_17(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean model."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=0,
            switching_mean=True,
            switching_variance=False,
            switching_ar=True,
        )

    xǁMarkovSwitchingMeanǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingMeanǁ__init____mutmut_1": xǁMarkovSwitchingMeanǁ__init____mutmut_1,
        "xǁMarkovSwitchingMeanǁ__init____mutmut_2": xǁMarkovSwitchingMeanǁ__init____mutmut_2,
        "xǁMarkovSwitchingMeanǁ__init____mutmut_3": xǁMarkovSwitchingMeanǁ__init____mutmut_3,
        "xǁMarkovSwitchingMeanǁ__init____mutmut_4": xǁMarkovSwitchingMeanǁ__init____mutmut_4,
        "xǁMarkovSwitchingMeanǁ__init____mutmut_5": xǁMarkovSwitchingMeanǁ__init____mutmut_5,
        "xǁMarkovSwitchingMeanǁ__init____mutmut_6": xǁMarkovSwitchingMeanǁ__init____mutmut_6,
        "xǁMarkovSwitchingMeanǁ__init____mutmut_7": xǁMarkovSwitchingMeanǁ__init____mutmut_7,
        "xǁMarkovSwitchingMeanǁ__init____mutmut_8": xǁMarkovSwitchingMeanǁ__init____mutmut_8,
        "xǁMarkovSwitchingMeanǁ__init____mutmut_9": xǁMarkovSwitchingMeanǁ__init____mutmut_9,
        "xǁMarkovSwitchingMeanǁ__init____mutmut_10": xǁMarkovSwitchingMeanǁ__init____mutmut_10,
        "xǁMarkovSwitchingMeanǁ__init____mutmut_11": xǁMarkovSwitchingMeanǁ__init____mutmut_11,
        "xǁMarkovSwitchingMeanǁ__init____mutmut_12": xǁMarkovSwitchingMeanǁ__init____mutmut_12,
        "xǁMarkovSwitchingMeanǁ__init____mutmut_13": xǁMarkovSwitchingMeanǁ__init____mutmut_13,
        "xǁMarkovSwitchingMeanǁ__init____mutmut_14": xǁMarkovSwitchingMeanǁ__init____mutmut_14,
        "xǁMarkovSwitchingMeanǁ__init____mutmut_15": xǁMarkovSwitchingMeanǁ__init____mutmut_15,
        "xǁMarkovSwitchingMeanǁ__init____mutmut_16": xǁMarkovSwitchingMeanǁ__init____mutmut_16,
        "xǁMarkovSwitchingMeanǁ__init____mutmut_17": xǁMarkovSwitchingMeanǁ__init____mutmut_17,
    }
    xǁMarkovSwitchingMeanǁ__init____mutmut_orig.__name__ = "xǁMarkovSwitchingMeanǁ__init__"

    def _regime_loglike(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        args = [params, regime]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_orig"),
            object.__getattribute__(self, "xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_orig(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, mu_1, ..., mu_{k-1}, sigma, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k]), 1e-6)  # Single sigma after k means
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_1(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, mu_1, ..., mu_{k-1}, sigma, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = None
        mu = params[regime]
        sigma = max(abs(params[k]), 1e-6)  # Single sigma after k means
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_2(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, mu_1, ..., mu_{k-1}, sigma, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = None
        sigma = max(abs(params[k]), 1e-6)  # Single sigma after k means
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_3(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, mu_1, ..., mu_{k-1}, sigma, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = None  # Single sigma after k means
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_4(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, mu_1, ..., mu_{k-1}, sigma, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(None, 1e-6)  # Single sigma after k means
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_5(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, mu_1, ..., mu_{k-1}, sigma, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k]), None)  # Single sigma after k means
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_6(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, mu_1, ..., mu_{k-1}, sigma, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(1e-6)  # Single sigma after k means
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_7(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, mu_1, ..., mu_{k-1}, sigma, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(
            abs(params[k]),
        )  # Single sigma after k means
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_8(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, mu_1, ..., mu_{k-1}, sigma, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(None), 1e-6)  # Single sigma after k means
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_9(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, mu_1, ..., mu_{k-1}, sigma, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k]), 1.000001)  # Single sigma after k means
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_10(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, mu_1, ..., mu_{k-1}, sigma, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k]), 1e-6)  # Single sigma after k means
        y = None
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_11(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, mu_1, ..., mu_{k-1}, sigma, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k]), 1e-6)  # Single sigma after k means
        y = self.endog
        ll = None
        return ll

    def xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_12(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, mu_1, ..., mu_{k-1}, sigma, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k]), 1e-6)  # Single sigma after k means
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) + 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_13(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, mu_1, ..., mu_{k-1}, sigma, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k]), 1e-6)  # Single sigma after k means
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) + np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_14(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, mu_1, ..., mu_{k-1}, sigma, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k]), 1e-6)  # Single sigma after k means
        y = self.endog
        ll = -0.5 / np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_15(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, mu_1, ..., mu_{k-1}, sigma, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k]), 1e-6)  # Single sigma after k means
        y = self.endog
        ll = +0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_16(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, mu_1, ..., mu_{k-1}, sigma, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k]), 1e-6)  # Single sigma after k means
        y = self.endog
        ll = -1.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_17(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, mu_1, ..., mu_{k-1}, sigma, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k]), 1e-6)  # Single sigma after k means
        y = self.endog
        ll = -0.5 * np.log(None) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_18(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, mu_1, ..., mu_{k-1}, sigma, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k]), 1e-6)  # Single sigma after k means
        y = self.endog
        ll = -0.5 * np.log(2.0 / np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_19(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, mu_1, ..., mu_{k-1}, sigma, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k]), 1e-6)  # Single sigma after k means
        y = self.endog
        ll = -0.5 * np.log(3.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_20(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, mu_1, ..., mu_{k-1}, sigma, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k]), 1e-6)  # Single sigma after k means
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(None) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_21(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, mu_1, ..., mu_{k-1}, sigma, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k]), 1e-6)  # Single sigma after k means
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 / ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_22(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, mu_1, ..., mu_{k-1}, sigma, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k]), 1e-6)  # Single sigma after k means
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 1.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_23(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, mu_1, ..., mu_{k-1}, sigma, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k]), 1e-6)  # Single sigma after k means
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) * 2
        return ll

    def xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_24(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, mu_1, ..., mu_{k-1}, sigma, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k]), 1e-6)  # Single sigma after k means
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) * sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_25(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, mu_1, ..., mu_{k-1}, sigma, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k]), 1e-6)  # Single sigma after k means
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y + mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_26(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, mu_1, ..., mu_{k-1}, sigma, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k]), 1e-6)  # Single sigma after k means
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 3
        return ll

    xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_1": xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_1,
        "xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_2": xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_2,
        "xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_3": xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_3,
        "xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_4": xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_4,
        "xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_5": xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_5,
        "xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_6": xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_6,
        "xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_7": xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_7,
        "xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_8": xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_8,
        "xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_9": xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_9,
        "xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_10": xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_10,
        "xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_11": xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_11,
        "xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_12": xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_12,
        "xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_13": xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_13,
        "xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_14": xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_14,
        "xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_15": xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_15,
        "xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_16": xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_16,
        "xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_17": xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_17,
        "xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_18": xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_18,
        "xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_19": xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_19,
        "xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_20": xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_20,
        "xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_21": xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_21,
        "xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_22": xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_22,
        "xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_23": xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_23,
        "xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_24": xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_24,
        "xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_25": xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_25,
        "xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_26": xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_26,
    }
    xǁMarkovSwitchingMeanǁ_regime_loglike__mutmut_orig.__name__ = (
        "xǁMarkovSwitchingMeanǁ_regime_loglike"
    )

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values.

        Returns
        -------
        ndarray
            [mu_0, ..., mu_{k-1}, sigma, trans_params].
        """
        k = self.k_regimes
        y = self.endog

        # Initialize means using quantiles
        quantiles = np.linspace(0, 1, k + 2)[1:-1]
        mus = np.quantile(y, quantiles)

        # Single sigma
        sigma = np.array([np.std(y)])

        # Transition params (k*(k-1) logit values, initialized to 0 = p=0.5)
        trans = np.zeros(k * (k - 1))

        return np.concatenate([mus, sigma, trans])

    @property
    def param_names(self) -> list[str]:
        """Parameter names."""
        k = self.k_regimes
        names = [f"mu_{i}" for i in range(k)]
        names.append("sigma")
        names += [f"p_{i}{j}" for i in range(k) for j in range(k) if i != j]
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
            object.__getattribute__(self, "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_orig"),
            object.__getattribute__(self, "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_orig(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_1(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_2(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = None
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_3(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = None

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_4(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(None):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_5(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = None
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_6(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = None
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_7(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum >= 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_8(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1.000000000001:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_9(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = None

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_10(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) * w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_11(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(None) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_12(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights / y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_13(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = None
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_14(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 1.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_15(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = None
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_16(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 1.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_17(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(None):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_18(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = None
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_19(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = None
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_20(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum >= 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_21(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1.000000000001:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_22(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = None
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_23(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var = np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_24(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var -= np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_25(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(None)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_26(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights / (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_27(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) * 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_28(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y + mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_29(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 3)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_30(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight = w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_31(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight -= w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_32(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight >= 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_33(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1.000000000001:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_34(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = None

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_35(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(None, 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_36(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), None)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_37(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_38(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(
                np.sqrt(total_var / total_weight),
            )

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_39(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(None), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_40(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var * total_weight), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_41(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update single sigma (weighted across all regimes)
        total_var = 0.0
        total_weight = 0.0
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                total_var += np.sum(weights * (y - mu_s) ** 2)
                total_weight += w_sum

        if total_weight > 1e-12:
            new_params[k] = max(np.sqrt(total_var / total_weight), 1.000001)

        return new_params

    xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_1": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_1,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_2": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_2,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_3": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_3,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_4": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_4,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_5": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_5,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_6": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_6,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_7": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_7,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_8": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_8,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_9": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_9,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_10": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_10,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_11": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_11,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_12": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_12,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_13": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_13,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_14": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_14,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_15": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_15,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_16": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_16,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_17": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_17,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_18": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_18,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_19": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_19,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_20": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_20,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_21": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_21,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_22": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_22,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_23": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_23,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_24": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_24,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_25": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_25,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_26": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_26,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_27": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_27,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_28": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_28,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_29": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_29,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_30": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_30,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_31": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_31,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_32": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_32,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_33": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_33,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_34": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_34,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_35": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_35,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_36": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_36,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_37": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_37,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_38": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_38,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_39": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_39,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_40": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_40,
        "xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_41": xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_41,
    }
    xǁMarkovSwitchingMeanǁ_m_step_update__mutmut_orig.__name__ = (
        "xǁMarkovSwitchingMeanǁ_m_step_update"
    )

    def _extract_regime_params(self, params: NDArray[np.float64]) -> dict[int, dict[str, float]]:
        args = [params]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )

    def xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_orig(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime parameters."""
        k = self.k_regimes
        sigma = float(abs(params[k]))
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            regime_params[s] = {
                "mu": float(params[s]),
                "sigma": sigma,
            }
        return regime_params

    def xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_1(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime parameters."""
        k = None
        sigma = float(abs(params[k]))
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            regime_params[s] = {
                "mu": float(params[s]),
                "sigma": sigma,
            }
        return regime_params

    def xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_2(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime parameters."""
        k = self.k_regimes
        sigma = None
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            regime_params[s] = {
                "mu": float(params[s]),
                "sigma": sigma,
            }
        return regime_params

    def xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_3(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime parameters."""
        k = self.k_regimes
        sigma = float(None)
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            regime_params[s] = {
                "mu": float(params[s]),
                "sigma": sigma,
            }
        return regime_params

    def xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_4(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime parameters."""
        k = self.k_regimes
        sigma = float(abs(None))
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            regime_params[s] = {
                "mu": float(params[s]),
                "sigma": sigma,
            }
        return regime_params

    def xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_5(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime parameters."""
        k = self.k_regimes
        sigma = float(abs(params[k]))
        regime_params: dict[int, dict[str, float]] = None
        for s in range(k):
            regime_params[s] = {
                "mu": float(params[s]),
                "sigma": sigma,
            }
        return regime_params

    def xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_6(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime parameters."""
        k = self.k_regimes
        sigma = float(abs(params[k]))
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(None):
            regime_params[s] = {
                "mu": float(params[s]),
                "sigma": sigma,
            }
        return regime_params

    def xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_7(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime parameters."""
        k = self.k_regimes
        sigma = float(abs(params[k]))
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            regime_params[s] = None
        return regime_params

    def xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_8(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime parameters."""
        k = self.k_regimes
        sigma = float(abs(params[k]))
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            regime_params[s] = {
                "XXmuXX": float(params[s]),
                "sigma": sigma,
            }
        return regime_params

    def xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_9(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime parameters."""
        k = self.k_regimes
        sigma = float(abs(params[k]))
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            regime_params[s] = {
                "MU": float(params[s]),
                "sigma": sigma,
            }
        return regime_params

    def xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_10(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime parameters."""
        k = self.k_regimes
        sigma = float(abs(params[k]))
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            regime_params[s] = {
                "mu": float(None),
                "sigma": sigma,
            }
        return regime_params

    def xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_11(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime parameters."""
        k = self.k_regimes
        sigma = float(abs(params[k]))
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            regime_params[s] = {
                "mu": float(params[s]),
                "XXsigmaXX": sigma,
            }
        return regime_params

    def xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_12(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime parameters."""
        k = self.k_regimes
        sigma = float(abs(params[k]))
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            regime_params[s] = {
                "mu": float(params[s]),
                "SIGMA": sigma,
            }
        return regime_params

    xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_1": xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_1,
        "xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_2": xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_2,
        "xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_3": xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_3,
        "xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_4": xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_4,
        "xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_5": xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_5,
        "xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_6": xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_6,
        "xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_7": xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_7,
        "xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_8": xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_8,
        "xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_9": xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_9,
        "xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_10": xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_10,
        "xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_11": xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_11,
        "xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_12": xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_12,
    }
    xǁMarkovSwitchingMeanǁ_extract_regime_params__mutmut_orig.__name__ = (
        "xǁMarkovSwitchingMeanǁ_extract_regime_params"
    )


class MarkovSwitchingMeanVar(MarkovSwitchingModel):
    """Markov-Switching Mean-Variance model.

    Both mean and variance switch between regimes.

    y_t | S_t = s ~ N(mu_s, sigma_s^2)

    Parameters
    ----------
    endog : array-like
        Time series of observations, shape (T,).
    k_regimes : int
        Number of regimes. Default is 2.

    Examples
    --------
    >>> import numpy as np
    >>> from archbox.regime.ms_mean import MarkovSwitchingMeanVar
    >>> y = np.random.randn(200)
    >>> model = MarkovSwitchingMeanVar(y, k_regimes=2)
    >>> results = model.fit()
    >>> print(results.summary())
    """

    model_name: str = "MS-Mean-Var"

    def __init__(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        args = [endog, k_regimes]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMarkovSwitchingMeanVarǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁMarkovSwitchingMeanVarǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMarkovSwitchingMeanVarǁ__init____mutmut_orig(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean-Variance model."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=0,
            switching_mean=True,
            switching_variance=True,
            switching_ar=False,
        )

    def xǁMarkovSwitchingMeanVarǁ__init____mutmut_1(
        self,
        endog: Any,
        k_regimes: int = 3,
    ) -> None:
        """Initialize Markov-Switching Mean-Variance model."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=0,
            switching_mean=True,
            switching_variance=True,
            switching_ar=False,
        )

    def xǁMarkovSwitchingMeanVarǁ__init____mutmut_2(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean-Variance model."""
        super().__init__(
            None,
            k_regimes=k_regimes,
            order=0,
            switching_mean=True,
            switching_variance=True,
            switching_ar=False,
        )

    def xǁMarkovSwitchingMeanVarǁ__init____mutmut_3(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean-Variance model."""
        super().__init__(
            endog,
            k_regimes=None,
            order=0,
            switching_mean=True,
            switching_variance=True,
            switching_ar=False,
        )

    def xǁMarkovSwitchingMeanVarǁ__init____mutmut_4(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean-Variance model."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=None,
            switching_mean=True,
            switching_variance=True,
            switching_ar=False,
        )

    def xǁMarkovSwitchingMeanVarǁ__init____mutmut_5(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean-Variance model."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=0,
            switching_mean=None,
            switching_variance=True,
            switching_ar=False,
        )

    def xǁMarkovSwitchingMeanVarǁ__init____mutmut_6(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean-Variance model."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=0,
            switching_mean=True,
            switching_variance=None,
            switching_ar=False,
        )

    def xǁMarkovSwitchingMeanVarǁ__init____mutmut_7(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean-Variance model."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=0,
            switching_mean=True,
            switching_variance=True,
            switching_ar=None,
        )

    def xǁMarkovSwitchingMeanVarǁ__init____mutmut_8(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean-Variance model."""
        super().__init__(
            k_regimes=k_regimes,
            order=0,
            switching_mean=True,
            switching_variance=True,
            switching_ar=False,
        )

    def xǁMarkovSwitchingMeanVarǁ__init____mutmut_9(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean-Variance model."""
        super().__init__(
            endog,
            order=0,
            switching_mean=True,
            switching_variance=True,
            switching_ar=False,
        )

    def xǁMarkovSwitchingMeanVarǁ__init____mutmut_10(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean-Variance model."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            switching_mean=True,
            switching_variance=True,
            switching_ar=False,
        )

    def xǁMarkovSwitchingMeanVarǁ__init____mutmut_11(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean-Variance model."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=0,
            switching_variance=True,
            switching_ar=False,
        )

    def xǁMarkovSwitchingMeanVarǁ__init____mutmut_12(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean-Variance model."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=0,
            switching_mean=True,
            switching_ar=False,
        )

    def xǁMarkovSwitchingMeanVarǁ__init____mutmut_13(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean-Variance model."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=0,
            switching_mean=True,
            switching_variance=True,
        )

    def xǁMarkovSwitchingMeanVarǁ__init____mutmut_14(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean-Variance model."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=1,
            switching_mean=True,
            switching_variance=True,
            switching_ar=False,
        )

    def xǁMarkovSwitchingMeanVarǁ__init____mutmut_15(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean-Variance model."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=0,
            switching_mean=False,
            switching_variance=True,
            switching_ar=False,
        )

    def xǁMarkovSwitchingMeanVarǁ__init____mutmut_16(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean-Variance model."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=0,
            switching_mean=True,
            switching_variance=False,
            switching_ar=False,
        )

    def xǁMarkovSwitchingMeanVarǁ__init____mutmut_17(
        self,
        endog: Any,
        k_regimes: int = 2,
    ) -> None:
        """Initialize Markov-Switching Mean-Variance model."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=0,
            switching_mean=True,
            switching_variance=True,
            switching_ar=True,
        )

    xǁMarkovSwitchingMeanVarǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingMeanVarǁ__init____mutmut_1": xǁMarkovSwitchingMeanVarǁ__init____mutmut_1,
        "xǁMarkovSwitchingMeanVarǁ__init____mutmut_2": xǁMarkovSwitchingMeanVarǁ__init____mutmut_2,
        "xǁMarkovSwitchingMeanVarǁ__init____mutmut_3": xǁMarkovSwitchingMeanVarǁ__init____mutmut_3,
        "xǁMarkovSwitchingMeanVarǁ__init____mutmut_4": xǁMarkovSwitchingMeanVarǁ__init____mutmut_4,
        "xǁMarkovSwitchingMeanVarǁ__init____mutmut_5": xǁMarkovSwitchingMeanVarǁ__init____mutmut_5,
        "xǁMarkovSwitchingMeanVarǁ__init____mutmut_6": xǁMarkovSwitchingMeanVarǁ__init____mutmut_6,
        "xǁMarkovSwitchingMeanVarǁ__init____mutmut_7": xǁMarkovSwitchingMeanVarǁ__init____mutmut_7,
        "xǁMarkovSwitchingMeanVarǁ__init____mutmut_8": xǁMarkovSwitchingMeanVarǁ__init____mutmut_8,
        "xǁMarkovSwitchingMeanVarǁ__init____mutmut_9": xǁMarkovSwitchingMeanVarǁ__init____mutmut_9,
        "xǁMarkovSwitchingMeanVarǁ__init____mutmut_10": xǁMarkovSwitchingMeanVarǁ__init____mutmut_10,
        "xǁMarkovSwitchingMeanVarǁ__init____mutmut_11": xǁMarkovSwitchingMeanVarǁ__init____mutmut_11,
        "xǁMarkovSwitchingMeanVarǁ__init____mutmut_12": xǁMarkovSwitchingMeanVarǁ__init____mutmut_12,
        "xǁMarkovSwitchingMeanVarǁ__init____mutmut_13": xǁMarkovSwitchingMeanVarǁ__init____mutmut_13,
        "xǁMarkovSwitchingMeanVarǁ__init____mutmut_14": xǁMarkovSwitchingMeanVarǁ__init____mutmut_14,
        "xǁMarkovSwitchingMeanVarǁ__init____mutmut_15": xǁMarkovSwitchingMeanVarǁ__init____mutmut_15,
        "xǁMarkovSwitchingMeanVarǁ__init____mutmut_16": xǁMarkovSwitchingMeanVarǁ__init____mutmut_16,
        "xǁMarkovSwitchingMeanVarǁ__init____mutmut_17": xǁMarkovSwitchingMeanVarǁ__init____mutmut_17,
    }
    xǁMarkovSwitchingMeanVarǁ__init____mutmut_orig.__name__ = "xǁMarkovSwitchingMeanVarǁ__init__"

    def _regime_loglike(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        args = [params, regime]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_orig"),
            object.__getattribute__(
                self, "xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )

    def xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_orig(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, ..., mu_{k-1}, sigma_0, ..., sigma_{k-1}, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k + regime]), 1e-6)
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_1(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, ..., mu_{k-1}, sigma_0, ..., sigma_{k-1}, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = None
        mu = params[regime]
        sigma = max(abs(params[k + regime]), 1e-6)
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_2(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, ..., mu_{k-1}, sigma_0, ..., sigma_{k-1}, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = None
        sigma = max(abs(params[k + regime]), 1e-6)
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_3(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, ..., mu_{k-1}, sigma_0, ..., sigma_{k-1}, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = None
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_4(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, ..., mu_{k-1}, sigma_0, ..., sigma_{k-1}, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(None, 1e-6)
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_5(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, ..., mu_{k-1}, sigma_0, ..., sigma_{k-1}, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k + regime]), None)
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_6(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, ..., mu_{k-1}, sigma_0, ..., sigma_{k-1}, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(1e-6)
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_7(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, ..., mu_{k-1}, sigma_0, ..., sigma_{k-1}, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(
            abs(params[k + regime]),
        )
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_8(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, ..., mu_{k-1}, sigma_0, ..., sigma_{k-1}, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(None), 1e-6)
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_9(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, ..., mu_{k-1}, sigma_0, ..., sigma_{k-1}, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k - regime]), 1e-6)
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_10(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, ..., mu_{k-1}, sigma_0, ..., sigma_{k-1}, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k + regime]), 1.000001)
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_11(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, ..., mu_{k-1}, sigma_0, ..., sigma_{k-1}, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k + regime]), 1e-6)
        y = None
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_12(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, ..., mu_{k-1}, sigma_0, ..., sigma_{k-1}, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k + regime]), 1e-6)
        y = self.endog
        ll = None
        return ll

    def xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_13(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, ..., mu_{k-1}, sigma_0, ..., sigma_{k-1}, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k + regime]), 1e-6)
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) + 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_14(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, ..., mu_{k-1}, sigma_0, ..., sigma_{k-1}, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k + regime]), 1e-6)
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) + np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_15(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, ..., mu_{k-1}, sigma_0, ..., sigma_{k-1}, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k + regime]), 1e-6)
        y = self.endog
        ll = -0.5 / np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_16(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, ..., mu_{k-1}, sigma_0, ..., sigma_{k-1}, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k + regime]), 1e-6)
        y = self.endog
        ll = +0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_17(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, ..., mu_{k-1}, sigma_0, ..., sigma_{k-1}, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k + regime]), 1e-6)
        y = self.endog
        ll = -1.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_18(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, ..., mu_{k-1}, sigma_0, ..., sigma_{k-1}, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k + regime]), 1e-6)
        y = self.endog
        ll = -0.5 * np.log(None) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_19(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, ..., mu_{k-1}, sigma_0, ..., sigma_{k-1}, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k + regime]), 1e-6)
        y = self.endog
        ll = -0.5 * np.log(2.0 / np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_20(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, ..., mu_{k-1}, sigma_0, ..., sigma_{k-1}, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k + regime]), 1e-6)
        y = self.endog
        ll = -0.5 * np.log(3.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_21(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, ..., mu_{k-1}, sigma_0, ..., sigma_{k-1}, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k + regime]), 1e-6)
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(None) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_22(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, ..., mu_{k-1}, sigma_0, ..., sigma_{k-1}, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k + regime]), 1e-6)
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 / ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_23(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, ..., mu_{k-1}, sigma_0, ..., sigma_{k-1}, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k + regime]), 1e-6)
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 1.5 * ((y - mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_24(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, ..., mu_{k-1}, sigma_0, ..., sigma_{k-1}, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k + regime]), 1e-6)
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) * 2
        return ll

    def xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_25(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, ..., mu_{k-1}, sigma_0, ..., sigma_{k-1}, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k + regime]), 1e-6)
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) * sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_26(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, ..., mu_{k-1}, sigma_0, ..., sigma_{k-1}, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k + regime]), 1e-6)
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y + mu) / sigma) ** 2
        return ll

    def xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_27(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime) for all t.

        Parameters
        ----------
        params : ndarray
            [mu_0, ..., mu_{k-1}, sigma_0, ..., sigma_{k-1}, trans_params...].
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        mu = params[regime]
        sigma = max(abs(params[k + regime]), 1e-6)
        y = self.endog
        ll = -0.5 * np.log(2.0 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 3
        return ll

    xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_1": xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_1,
        "xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_2": xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_2,
        "xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_3": xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_3,
        "xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_4": xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_4,
        "xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_5": xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_5,
        "xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_6": xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_6,
        "xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_7": xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_7,
        "xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_8": xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_8,
        "xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_9": xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_9,
        "xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_10": xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_10,
        "xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_11": xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_11,
        "xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_12": xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_12,
        "xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_13": xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_13,
        "xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_14": xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_14,
        "xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_15": xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_15,
        "xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_16": xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_16,
        "xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_17": xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_17,
        "xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_18": xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_18,
        "xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_19": xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_19,
        "xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_20": xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_20,
        "xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_21": xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_21,
        "xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_22": xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_22,
        "xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_23": xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_23,
        "xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_24": xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_24,
        "xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_25": xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_25,
        "xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_26": xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_26,
        "xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_27": xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_27,
    }
    xǁMarkovSwitchingMeanVarǁ_regime_loglike__mutmut_orig.__name__ = (
        "xǁMarkovSwitchingMeanVarǁ_regime_loglike"
    )

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values.

        Returns
        -------
        ndarray
            [mu_0, ..., mu_{k-1}, sigma_0, ..., sigma_{k-1}, trans_params].
        """
        k = self.k_regimes
        y = self.endog

        # Initialize means using quantiles
        quantiles = np.linspace(0, 1, k + 2)[1:-1]
        mus = np.quantile(y, quantiles)

        # Initialize sigmas
        sigmas = np.full(k, np.std(y))

        # Transition params
        trans = np.zeros(k * (k - 1))

        return np.concatenate([mus, sigmas, trans])

    @property
    def param_names(self) -> list[str]:
        """Parameter names."""
        k = self.k_regimes
        names = [f"mu_{i}" for i in range(k)]
        names += [f"sigma_{i}" for i in range(k)]
        names += [f"p_{i}{j}" for i in range(k) for j in range(k) if i != j]
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
            object.__getattribute__(self, "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_orig"),
            object.__getattribute__(
                self, "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_orig(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update regime-specific sigmas
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                resid2 = (y - mu_s) ** 2
                var_s = np.sum(weights * resid2) / w_sum
                new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_1(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update regime-specific sigmas
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                resid2 = (y - mu_s) ** 2
                var_s = np.sum(weights * resid2) / w_sum
                new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_2(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = None
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update regime-specific sigmas
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                resid2 = (y - mu_s) ** 2
                var_s = np.sum(weights * resid2) / w_sum
                new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_3(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = self.endog
        new_params = None

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update regime-specific sigmas
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                resid2 = (y - mu_s) ** 2
                var_s = np.sum(weights * resid2) / w_sum
                new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_4(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(None):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update regime-specific sigmas
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                resid2 = (y - mu_s) ** 2
                var_s = np.sum(weights * resid2) / w_sum
                new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_5(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = None
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update regime-specific sigmas
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                resid2 = (y - mu_s) ** 2
                var_s = np.sum(weights * resid2) / w_sum
                new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_6(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = None
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update regime-specific sigmas
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                resid2 = (y - mu_s) ** 2
                var_s = np.sum(weights * resid2) / w_sum
                new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_7(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum >= 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update regime-specific sigmas
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                resid2 = (y - mu_s) ** 2
                var_s = np.sum(weights * resid2) / w_sum
                new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_8(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1.000000000001:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update regime-specific sigmas
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                resid2 = (y - mu_s) ** 2
                var_s = np.sum(weights * resid2) / w_sum
                new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_9(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = None

        # Update regime-specific sigmas
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                resid2 = (y - mu_s) ** 2
                var_s = np.sum(weights * resid2) / w_sum
                new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_10(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) * w_sum

        # Update regime-specific sigmas
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                resid2 = (y - mu_s) ** 2
                var_s = np.sum(weights * resid2) / w_sum
                new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_11(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(None) / w_sum

        # Update regime-specific sigmas
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                resid2 = (y - mu_s) ** 2
                var_s = np.sum(weights * resid2) / w_sum
                new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_12(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights / y) / w_sum

        # Update regime-specific sigmas
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                resid2 = (y - mu_s) ** 2
                var_s = np.sum(weights * resid2) / w_sum
                new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_13(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update regime-specific sigmas
        for s in range(None):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                resid2 = (y - mu_s) ** 2
                var_s = np.sum(weights * resid2) / w_sum
                new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_14(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update regime-specific sigmas
        for s in range(k):
            weights = None
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                resid2 = (y - mu_s) ** 2
                var_s = np.sum(weights * resid2) / w_sum
                new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_15(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update regime-specific sigmas
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = None
            if w_sum > 1e-12:
                mu_s = new_params[s]
                resid2 = (y - mu_s) ** 2
                var_s = np.sum(weights * resid2) / w_sum
                new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_16(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update regime-specific sigmas
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum >= 1e-12:
                mu_s = new_params[s]
                resid2 = (y - mu_s) ** 2
                var_s = np.sum(weights * resid2) / w_sum
                new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_17(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update regime-specific sigmas
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1.000000000001:
                mu_s = new_params[s]
                resid2 = (y - mu_s) ** 2
                var_s = np.sum(weights * resid2) / w_sum
                new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_18(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update regime-specific sigmas
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = None
                resid2 = (y - mu_s) ** 2
                var_s = np.sum(weights * resid2) / w_sum
                new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_19(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update regime-specific sigmas
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                resid2 = None
                var_s = np.sum(weights * resid2) / w_sum
                new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_20(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update regime-specific sigmas
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                resid2 = (y - mu_s) * 2
                var_s = np.sum(weights * resid2) / w_sum
                new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_21(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update regime-specific sigmas
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                resid2 = (y + mu_s) ** 2
                var_s = np.sum(weights * resid2) / w_sum
                new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_22(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update regime-specific sigmas
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                resid2 = (y - mu_s) ** 3
                var_s = np.sum(weights * resid2) / w_sum
                new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_23(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update regime-specific sigmas
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                resid2 = (y - mu_s) ** 2
                var_s = None
                new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_24(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update regime-specific sigmas
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                resid2 = (y - mu_s) ** 2
                var_s = np.sum(weights * resid2) * w_sum
                new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_25(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update regime-specific sigmas
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                resid2 = (y - mu_s) ** 2
                var_s = np.sum(None) / w_sum
                new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_26(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update regime-specific sigmas
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                resid2 = (y - mu_s) ** 2
                var_s = np.sum(weights / resid2) / w_sum
                new_params[k + s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_27(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update regime-specific sigmas
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                resid2 = (y - mu_s) ** 2
                var_s = np.sum(weights * resid2) / w_sum
                new_params[k + s] = None

        return new_params

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_28(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update regime-specific sigmas
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                resid2 = (y - mu_s) ** 2
                var_s = np.sum(weights * resid2) / w_sum
                new_params[k - s] = max(np.sqrt(var_s), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_29(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update regime-specific sigmas
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                resid2 = (y - mu_s) ** 2
                var_s = np.sum(weights * resid2) / w_sum
                new_params[k + s] = max(None, 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_30(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update regime-specific sigmas
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                resid2 = (y - mu_s) ** 2
                var_s = np.sum(weights * resid2) / w_sum
                new_params[k + s] = max(np.sqrt(var_s), None)

        return new_params

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_31(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update regime-specific sigmas
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                resid2 = (y - mu_s) ** 2
                var_s = np.sum(weights * resid2) / w_sum
                new_params[k + s] = max(1e-6)

        return new_params

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_32(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update regime-specific sigmas
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                resid2 = (y - mu_s) ** 2
                var_s = np.sum(weights * resid2) / w_sum
                new_params[k + s] = max(
                    np.sqrt(var_s),
                )

        return new_params

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_33(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update regime-specific sigmas
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                resid2 = (y - mu_s) ** 2
                var_s = np.sum(weights * resid2) / w_sum
                new_params[k + s] = max(np.sqrt(None), 1e-6)

        return new_params

    def xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_34(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-Mean-Var.

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
        y = self.endog
        new_params = params.copy()

        # Update means
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                new_params[s] = np.sum(weights * y) / w_sum

        # Update regime-specific sigmas
        for s in range(k):
            weights = smoothed[:, s]
            w_sum = weights.sum()
            if w_sum > 1e-12:
                mu_s = new_params[s]
                resid2 = (y - mu_s) ** 2
                var_s = np.sum(weights * resid2) / w_sum
                new_params[k + s] = max(np.sqrt(var_s), 1.000001)

        return new_params

    xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_1": xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_1,
        "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_2": xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_2,
        "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_3": xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_3,
        "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_4": xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_4,
        "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_5": xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_5,
        "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_6": xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_6,
        "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_7": xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_7,
        "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_8": xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_8,
        "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_9": xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_9,
        "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_10": xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_10,
        "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_11": xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_11,
        "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_12": xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_12,
        "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_13": xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_13,
        "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_14": xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_14,
        "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_15": xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_15,
        "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_16": xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_16,
        "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_17": xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_17,
        "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_18": xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_18,
        "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_19": xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_19,
        "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_20": xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_20,
        "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_21": xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_21,
        "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_22": xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_22,
        "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_23": xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_23,
        "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_24": xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_24,
        "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_25": xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_25,
        "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_26": xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_26,
        "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_27": xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_27,
        "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_28": xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_28,
        "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_29": xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_29,
        "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_30": xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_30,
        "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_31": xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_31,
        "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_32": xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_32,
        "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_33": xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_33,
        "xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_34": xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_34,
    }
    xǁMarkovSwitchingMeanVarǁ_m_step_update__mutmut_orig.__name__ = (
        "xǁMarkovSwitchingMeanVarǁ_m_step_update"
    )

    def _extract_regime_params(self, params: NDArray[np.float64]) -> dict[int, dict[str, float]]:
        args = [params]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )

    def xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_orig(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            regime_params[s] = {
                "mu": float(params[s]),
                "sigma": float(abs(params[k + s])),
            }
        return regime_params

    def xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_1(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime parameters."""
        k = None
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            regime_params[s] = {
                "mu": float(params[s]),
                "sigma": float(abs(params[k + s])),
            }
        return regime_params

    def xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_2(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, float]] = None
        for s in range(k):
            regime_params[s] = {
                "mu": float(params[s]),
                "sigma": float(abs(params[k + s])),
            }
        return regime_params

    def xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_3(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(None):
            regime_params[s] = {
                "mu": float(params[s]),
                "sigma": float(abs(params[k + s])),
            }
        return regime_params

    def xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_4(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            regime_params[s] = None
        return regime_params

    def xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_5(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            regime_params[s] = {
                "XXmuXX": float(params[s]),
                "sigma": float(abs(params[k + s])),
            }
        return regime_params

    def xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_6(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            regime_params[s] = {
                "MU": float(params[s]),
                "sigma": float(abs(params[k + s])),
            }
        return regime_params

    def xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_7(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            regime_params[s] = {
                "mu": float(None),
                "sigma": float(abs(params[k + s])),
            }
        return regime_params

    def xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_8(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            regime_params[s] = {
                "mu": float(params[s]),
                "XXsigmaXX": float(abs(params[k + s])),
            }
        return regime_params

    def xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_9(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            regime_params[s] = {
                "mu": float(params[s]),
                "SIGMA": float(abs(params[k + s])),
            }
        return regime_params

    def xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_10(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            regime_params[s] = {
                "mu": float(params[s]),
                "sigma": float(None),
            }
        return regime_params

    def xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_11(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            regime_params[s] = {
                "mu": float(params[s]),
                "sigma": float(abs(None)),
            }
        return regime_params

    def xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_12(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            regime_params[s] = {
                "mu": float(params[s]),
                "sigma": float(abs(params[k - s])),
            }
        return regime_params

    xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_1": xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_1,
        "xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_2": xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_2,
        "xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_3": xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_3,
        "xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_4": xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_4,
        "xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_5": xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_5,
        "xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_6": xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_6,
        "xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_7": xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_7,
        "xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_8": xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_8,
        "xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_9": xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_9,
        "xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_10": xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_10,
        "xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_11": xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_11,
        "xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_12": xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_12,
    }
    xǁMarkovSwitchingMeanVarǁ_extract_regime_params__mutmut_orig.__name__ = (
        "xǁMarkovSwitchingMeanVarǁ_extract_regime_params"
    )
