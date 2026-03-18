"""Results container for fitted volatility models."""

from __future__ import annotations

import pickle
from pathlib import Path
from typing import TYPE_CHECKING, Any

import numpy as np
import pandas as pd
from numpy.typing import NDArray
from scipy import stats

if TYPE_CHECKING:
    from archbox.core.volatility_model import VolatilityModel
from collections.abc import Callable
from typing import Annotated, ClassVar

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


class ArchResults:
    """Container for fitted ARCH/GARCH model results.

    Parameters
    ----------
    model : VolatilityModel
        The fitted model instance.
    params : ndarray
        Estimated parameters.
    loglike : float
        Log-likelihood at optimum.
    sigma2 : ndarray
        Conditional variance series sigma^2_t.
    se_robust : ndarray
        Robust (Bollerslev-Wooldridge) standard errors.
    se_nonrobust : ndarray
        Non-robust (inverse Hessian) standard errors.
    convergence : bool
        Whether optimization converged.
    """

    def __init__(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        args = [model, params, loglike, sigma2, se_robust, se_nonrobust, convergence]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁArchResultsǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁArchResultsǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁArchResultsǁ__init____mutmut_orig(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_1(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = None
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_2(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = None
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_3(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = None
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_4(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = None
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_5(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = None
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_6(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = None

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_7(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = None
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_8(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = None
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_9(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = None  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_10(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = None
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_11(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params * self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_12(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = None

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_13(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 / (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_14(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 3.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_15(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 + stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_16(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (2.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_17(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(None))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_18(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(None)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_19(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = None
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_20(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(None)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_21(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = None
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_22(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = None  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_23(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog * self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_24(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = None
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_25(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = None
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_26(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = None
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_27(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike - 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_28(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 / loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_29(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = +2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_30(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -3.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_31(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 / k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_32(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 3.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_33(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = None
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_34(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike - k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_35(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 / loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_36(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = +2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_37(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -3.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_38(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k / np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_39(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(None)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_40(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = None

    def xǁArchResultsǁ__init____mutmut_41(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike - 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_42(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 / loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_43(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = +2.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_44(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -3.0 * loglike + 2.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_45(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k / np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_46(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 / k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_47(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 3.0 * k * np.log(np.log(n))

    def xǁArchResultsǁ__init____mutmut_48(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(None)

    def xǁArchResultsǁ__init____mutmut_49(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        loglike: float,
        sigma2: NDArray[np.float64],
        se_robust: NDArray[np.float64],
        se_nonrobust: NDArray[np.float64],
        convergence: bool,
    ) -> None:
        """Initialize ArchResults with fitted model outputs."""
        self._model = model
        self.params = params
        self.param_names = model.param_names
        self.loglike = loglike
        self.nobs = model.nobs
        self.convergence = convergence

        # Standard errors (default to robust)
        self.se_robust = se_robust
        self.se_nonrobust = se_nonrobust
        self.se = se_robust  # default

        # t-statistics and p-values
        self.tvalues = params / self.se
        self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.tvalues)))

        # Conditional volatility and residuals
        self.conditional_volatility = np.sqrt(sigma2)
        self._sigma2 = sigma2
        self.resid = model.endog / self.conditional_volatility  # standardized residuals

        # Information criteria
        k = len(params)
        n = self.nobs
        self.aic = -2.0 * loglike + 2.0 * k
        self.bic = -2.0 * loglike + k * np.log(n)
        self.hqic = -2.0 * loglike + 2.0 * k * np.log(np.log(None))

    xǁArchResultsǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁArchResultsǁ__init____mutmut_1": xǁArchResultsǁ__init____mutmut_1,
        "xǁArchResultsǁ__init____mutmut_2": xǁArchResultsǁ__init____mutmut_2,
        "xǁArchResultsǁ__init____mutmut_3": xǁArchResultsǁ__init____mutmut_3,
        "xǁArchResultsǁ__init____mutmut_4": xǁArchResultsǁ__init____mutmut_4,
        "xǁArchResultsǁ__init____mutmut_5": xǁArchResultsǁ__init____mutmut_5,
        "xǁArchResultsǁ__init____mutmut_6": xǁArchResultsǁ__init____mutmut_6,
        "xǁArchResultsǁ__init____mutmut_7": xǁArchResultsǁ__init____mutmut_7,
        "xǁArchResultsǁ__init____mutmut_8": xǁArchResultsǁ__init____mutmut_8,
        "xǁArchResultsǁ__init____mutmut_9": xǁArchResultsǁ__init____mutmut_9,
        "xǁArchResultsǁ__init____mutmut_10": xǁArchResultsǁ__init____mutmut_10,
        "xǁArchResultsǁ__init____mutmut_11": xǁArchResultsǁ__init____mutmut_11,
        "xǁArchResultsǁ__init____mutmut_12": xǁArchResultsǁ__init____mutmut_12,
        "xǁArchResultsǁ__init____mutmut_13": xǁArchResultsǁ__init____mutmut_13,
        "xǁArchResultsǁ__init____mutmut_14": xǁArchResultsǁ__init____mutmut_14,
        "xǁArchResultsǁ__init____mutmut_15": xǁArchResultsǁ__init____mutmut_15,
        "xǁArchResultsǁ__init____mutmut_16": xǁArchResultsǁ__init____mutmut_16,
        "xǁArchResultsǁ__init____mutmut_17": xǁArchResultsǁ__init____mutmut_17,
        "xǁArchResultsǁ__init____mutmut_18": xǁArchResultsǁ__init____mutmut_18,
        "xǁArchResultsǁ__init____mutmut_19": xǁArchResultsǁ__init____mutmut_19,
        "xǁArchResultsǁ__init____mutmut_20": xǁArchResultsǁ__init____mutmut_20,
        "xǁArchResultsǁ__init____mutmut_21": xǁArchResultsǁ__init____mutmut_21,
        "xǁArchResultsǁ__init____mutmut_22": xǁArchResultsǁ__init____mutmut_22,
        "xǁArchResultsǁ__init____mutmut_23": xǁArchResultsǁ__init____mutmut_23,
        "xǁArchResultsǁ__init____mutmut_24": xǁArchResultsǁ__init____mutmut_24,
        "xǁArchResultsǁ__init____mutmut_25": xǁArchResultsǁ__init____mutmut_25,
        "xǁArchResultsǁ__init____mutmut_26": xǁArchResultsǁ__init____mutmut_26,
        "xǁArchResultsǁ__init____mutmut_27": xǁArchResultsǁ__init____mutmut_27,
        "xǁArchResultsǁ__init____mutmut_28": xǁArchResultsǁ__init____mutmut_28,
        "xǁArchResultsǁ__init____mutmut_29": xǁArchResultsǁ__init____mutmut_29,
        "xǁArchResultsǁ__init____mutmut_30": xǁArchResultsǁ__init____mutmut_30,
        "xǁArchResultsǁ__init____mutmut_31": xǁArchResultsǁ__init____mutmut_31,
        "xǁArchResultsǁ__init____mutmut_32": xǁArchResultsǁ__init____mutmut_32,
        "xǁArchResultsǁ__init____mutmut_33": xǁArchResultsǁ__init____mutmut_33,
        "xǁArchResultsǁ__init____mutmut_34": xǁArchResultsǁ__init____mutmut_34,
        "xǁArchResultsǁ__init____mutmut_35": xǁArchResultsǁ__init____mutmut_35,
        "xǁArchResultsǁ__init____mutmut_36": xǁArchResultsǁ__init____mutmut_36,
        "xǁArchResultsǁ__init____mutmut_37": xǁArchResultsǁ__init____mutmut_37,
        "xǁArchResultsǁ__init____mutmut_38": xǁArchResultsǁ__init____mutmut_38,
        "xǁArchResultsǁ__init____mutmut_39": xǁArchResultsǁ__init____mutmut_39,
        "xǁArchResultsǁ__init____mutmut_40": xǁArchResultsǁ__init____mutmut_40,
        "xǁArchResultsǁ__init____mutmut_41": xǁArchResultsǁ__init____mutmut_41,
        "xǁArchResultsǁ__init____mutmut_42": xǁArchResultsǁ__init____mutmut_42,
        "xǁArchResultsǁ__init____mutmut_43": xǁArchResultsǁ__init____mutmut_43,
        "xǁArchResultsǁ__init____mutmut_44": xǁArchResultsǁ__init____mutmut_44,
        "xǁArchResultsǁ__init____mutmut_45": xǁArchResultsǁ__init____mutmut_45,
        "xǁArchResultsǁ__init____mutmut_46": xǁArchResultsǁ__init____mutmut_46,
        "xǁArchResultsǁ__init____mutmut_47": xǁArchResultsǁ__init____mutmut_47,
        "xǁArchResultsǁ__init____mutmut_48": xǁArchResultsǁ__init____mutmut_48,
        "xǁArchResultsǁ__init____mutmut_49": xǁArchResultsǁ__init____mutmut_49,
    }
    xǁArchResultsǁ__init____mutmut_orig.__name__ = "xǁArchResultsǁ__init__"

    def persistence(self) -> float:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁArchResultsǁpersistence__mutmut_orig"),
            object.__getattribute__(self, "xǁArchResultsǁpersistence__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁArchResultsǁpersistence__mutmut_orig(self) -> float:
        """Compute persistence: sum(alpha_i) + sum(beta_j).

        Returns
        -------
        float
            Persistence value. Must be < 1 for stationarity.
        """
        # params = [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        return float(np.sum(self.params[1:]))

    def xǁArchResultsǁpersistence__mutmut_1(self) -> float:
        """Compute persistence: sum(alpha_i) + sum(beta_j).

        Returns
        -------
        float
            Persistence value. Must be < 1 for stationarity.
        """
        # params = [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        return float(None)

    def xǁArchResultsǁpersistence__mutmut_2(self) -> float:
        """Compute persistence: sum(alpha_i) + sum(beta_j).

        Returns
        -------
        float
            Persistence value. Must be < 1 for stationarity.
        """
        # params = [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        return float(np.sum(None))

    def xǁArchResultsǁpersistence__mutmut_3(self) -> float:
        """Compute persistence: sum(alpha_i) + sum(beta_j).

        Returns
        -------
        float
            Persistence value. Must be < 1 for stationarity.
        """
        # params = [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        return float(np.sum(self.params[2:]))

    xǁArchResultsǁpersistence__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁArchResultsǁpersistence__mutmut_1": xǁArchResultsǁpersistence__mutmut_1,
        "xǁArchResultsǁpersistence__mutmut_2": xǁArchResultsǁpersistence__mutmut_2,
        "xǁArchResultsǁpersistence__mutmut_3": xǁArchResultsǁpersistence__mutmut_3,
    }
    xǁArchResultsǁpersistence__mutmut_orig.__name__ = "xǁArchResultsǁpersistence"

    def half_life(self) -> float:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁArchResultsǁhalf_life__mutmut_orig"),
            object.__getattribute__(self, "xǁArchResultsǁhalf_life__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁArchResultsǁhalf_life__mutmut_orig(self) -> float:
        """Compute half-life of volatility shocks.

        Returns
        -------
        float
            Number of periods for a shock to decay by half.
        """
        p = self.persistence()
        if p <= 0 or p >= 1:
            return float("inf")
        return float(np.log(0.5) / np.log(p))

    def xǁArchResultsǁhalf_life__mutmut_1(self) -> float:
        """Compute half-life of volatility shocks.

        Returns
        -------
        float
            Number of periods for a shock to decay by half.
        """
        p = None
        if p <= 0 or p >= 1:
            return float("inf")
        return float(np.log(0.5) / np.log(p))

    def xǁArchResultsǁhalf_life__mutmut_2(self) -> float:
        """Compute half-life of volatility shocks.

        Returns
        -------
        float
            Number of periods for a shock to decay by half.
        """
        p = self.persistence()
        if p <= 0 and p >= 1:
            return float("inf")
        return float(np.log(0.5) / np.log(p))

    def xǁArchResultsǁhalf_life__mutmut_3(self) -> float:
        """Compute half-life of volatility shocks.

        Returns
        -------
        float
            Number of periods for a shock to decay by half.
        """
        p = self.persistence()
        if p < 0 or p >= 1:
            return float("inf")
        return float(np.log(0.5) / np.log(p))

    def xǁArchResultsǁhalf_life__mutmut_4(self) -> float:
        """Compute half-life of volatility shocks.

        Returns
        -------
        float
            Number of periods for a shock to decay by half.
        """
        p = self.persistence()
        if p <= 1 or p >= 1:
            return float("inf")
        return float(np.log(0.5) / np.log(p))

    def xǁArchResultsǁhalf_life__mutmut_5(self) -> float:
        """Compute half-life of volatility shocks.

        Returns
        -------
        float
            Number of periods for a shock to decay by half.
        """
        p = self.persistence()
        if p <= 0 or p > 1:
            return float("inf")
        return float(np.log(0.5) / np.log(p))

    def xǁArchResultsǁhalf_life__mutmut_6(self) -> float:
        """Compute half-life of volatility shocks.

        Returns
        -------
        float
            Number of periods for a shock to decay by half.
        """
        p = self.persistence()
        if p <= 0 or p >= 2:
            return float("inf")
        return float(np.log(0.5) / np.log(p))

    def xǁArchResultsǁhalf_life__mutmut_7(self) -> float:
        """Compute half-life of volatility shocks.

        Returns
        -------
        float
            Number of periods for a shock to decay by half.
        """
        p = self.persistence()
        if p <= 0 or p >= 1:
            return float(None)
        return float(np.log(0.5) / np.log(p))

    def xǁArchResultsǁhalf_life__mutmut_8(self) -> float:
        """Compute half-life of volatility shocks.

        Returns
        -------
        float
            Number of periods for a shock to decay by half.
        """
        p = self.persistence()
        if p <= 0 or p >= 1:
            return float("XXinfXX")
        return float(np.log(0.5) / np.log(p))

    def xǁArchResultsǁhalf_life__mutmut_9(self) -> float:
        """Compute half-life of volatility shocks.

        Returns
        -------
        float
            Number of periods for a shock to decay by half.
        """
        p = self.persistence()
        if p <= 0 or p >= 1:
            return float("INF")
        return float(np.log(0.5) / np.log(p))

    def xǁArchResultsǁhalf_life__mutmut_10(self) -> float:
        """Compute half-life of volatility shocks.

        Returns
        -------
        float
            Number of periods for a shock to decay by half.
        """
        p = self.persistence()
        if p <= 0 or p >= 1:
            return float("inf")
        return float(None)

    def xǁArchResultsǁhalf_life__mutmut_11(self) -> float:
        """Compute half-life of volatility shocks.

        Returns
        -------
        float
            Number of periods for a shock to decay by half.
        """
        p = self.persistence()
        if p <= 0 or p >= 1:
            return float("inf")
        return float(np.log(0.5) * np.log(p))

    def xǁArchResultsǁhalf_life__mutmut_12(self) -> float:
        """Compute half-life of volatility shocks.

        Returns
        -------
        float
            Number of periods for a shock to decay by half.
        """
        p = self.persistence()
        if p <= 0 or p >= 1:
            return float("inf")
        return float(np.log(None) / np.log(p))

    def xǁArchResultsǁhalf_life__mutmut_13(self) -> float:
        """Compute half-life of volatility shocks.

        Returns
        -------
        float
            Number of periods for a shock to decay by half.
        """
        p = self.persistence()
        if p <= 0 or p >= 1:
            return float("inf")
        return float(np.log(1.5) / np.log(p))

    def xǁArchResultsǁhalf_life__mutmut_14(self) -> float:
        """Compute half-life of volatility shocks.

        Returns
        -------
        float
            Number of periods for a shock to decay by half.
        """
        p = self.persistence()
        if p <= 0 or p >= 1:
            return float("inf")
        return float(np.log(0.5) / np.log(None))

    xǁArchResultsǁhalf_life__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁArchResultsǁhalf_life__mutmut_1": xǁArchResultsǁhalf_life__mutmut_1,
        "xǁArchResultsǁhalf_life__mutmut_2": xǁArchResultsǁhalf_life__mutmut_2,
        "xǁArchResultsǁhalf_life__mutmut_3": xǁArchResultsǁhalf_life__mutmut_3,
        "xǁArchResultsǁhalf_life__mutmut_4": xǁArchResultsǁhalf_life__mutmut_4,
        "xǁArchResultsǁhalf_life__mutmut_5": xǁArchResultsǁhalf_life__mutmut_5,
        "xǁArchResultsǁhalf_life__mutmut_6": xǁArchResultsǁhalf_life__mutmut_6,
        "xǁArchResultsǁhalf_life__mutmut_7": xǁArchResultsǁhalf_life__mutmut_7,
        "xǁArchResultsǁhalf_life__mutmut_8": xǁArchResultsǁhalf_life__mutmut_8,
        "xǁArchResultsǁhalf_life__mutmut_9": xǁArchResultsǁhalf_life__mutmut_9,
        "xǁArchResultsǁhalf_life__mutmut_10": xǁArchResultsǁhalf_life__mutmut_10,
        "xǁArchResultsǁhalf_life__mutmut_11": xǁArchResultsǁhalf_life__mutmut_11,
        "xǁArchResultsǁhalf_life__mutmut_12": xǁArchResultsǁhalf_life__mutmut_12,
        "xǁArchResultsǁhalf_life__mutmut_13": xǁArchResultsǁhalf_life__mutmut_13,
        "xǁArchResultsǁhalf_life__mutmut_14": xǁArchResultsǁhalf_life__mutmut_14,
    }
    xǁArchResultsǁhalf_life__mutmut_orig.__name__ = "xǁArchResultsǁhalf_life"

    def unconditional_variance(self) -> float:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁArchResultsǁunconditional_variance__mutmut_orig"),
            object.__getattribute__(self, "xǁArchResultsǁunconditional_variance__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁArchResultsǁunconditional_variance__mutmut_orig(self) -> float:
        """Compute unconditional (long-run) variance.

        Returns
        -------
        float
            omega / (1 - persistence).
        """
        p = self.persistence()
        if p >= 1:
            return float("inf")
        return float(self.params[0] / (1.0 - p))

    def xǁArchResultsǁunconditional_variance__mutmut_1(self) -> float:
        """Compute unconditional (long-run) variance.

        Returns
        -------
        float
            omega / (1 - persistence).
        """
        p = None
        if p >= 1:
            return float("inf")
        return float(self.params[0] / (1.0 - p))

    def xǁArchResultsǁunconditional_variance__mutmut_2(self) -> float:
        """Compute unconditional (long-run) variance.

        Returns
        -------
        float
            omega / (1 - persistence).
        """
        p = self.persistence()
        if p > 1:
            return float("inf")
        return float(self.params[0] / (1.0 - p))

    def xǁArchResultsǁunconditional_variance__mutmut_3(self) -> float:
        """Compute unconditional (long-run) variance.

        Returns
        -------
        float
            omega / (1 - persistence).
        """
        p = self.persistence()
        if p >= 2:
            return float("inf")
        return float(self.params[0] / (1.0 - p))

    def xǁArchResultsǁunconditional_variance__mutmut_4(self) -> float:
        """Compute unconditional (long-run) variance.

        Returns
        -------
        float
            omega / (1 - persistence).
        """
        p = self.persistence()
        if p >= 1:
            return float(None)
        return float(self.params[0] / (1.0 - p))

    def xǁArchResultsǁunconditional_variance__mutmut_5(self) -> float:
        """Compute unconditional (long-run) variance.

        Returns
        -------
        float
            omega / (1 - persistence).
        """
        p = self.persistence()
        if p >= 1:
            return float("XXinfXX")
        return float(self.params[0] / (1.0 - p))

    def xǁArchResultsǁunconditional_variance__mutmut_6(self) -> float:
        """Compute unconditional (long-run) variance.

        Returns
        -------
        float
            omega / (1 - persistence).
        """
        p = self.persistence()
        if p >= 1:
            return float("INF")
        return float(self.params[0] / (1.0 - p))

    def xǁArchResultsǁunconditional_variance__mutmut_7(self) -> float:
        """Compute unconditional (long-run) variance.

        Returns
        -------
        float
            omega / (1 - persistence).
        """
        p = self.persistence()
        if p >= 1:
            return float("inf")
        return float(None)

    def xǁArchResultsǁunconditional_variance__mutmut_8(self) -> float:
        """Compute unconditional (long-run) variance.

        Returns
        -------
        float
            omega / (1 - persistence).
        """
        p = self.persistence()
        if p >= 1:
            return float("inf")
        return float(self.params[0] * (1.0 - p))

    def xǁArchResultsǁunconditional_variance__mutmut_9(self) -> float:
        """Compute unconditional (long-run) variance.

        Returns
        -------
        float
            omega / (1 - persistence).
        """
        p = self.persistence()
        if p >= 1:
            return float("inf")
        return float(self.params[1] / (1.0 - p))

    def xǁArchResultsǁunconditional_variance__mutmut_10(self) -> float:
        """Compute unconditional (long-run) variance.

        Returns
        -------
        float
            omega / (1 - persistence).
        """
        p = self.persistence()
        if p >= 1:
            return float("inf")
        return float(self.params[0] / (1.0 + p))

    def xǁArchResultsǁunconditional_variance__mutmut_11(self) -> float:
        """Compute unconditional (long-run) variance.

        Returns
        -------
        float
            omega / (1 - persistence).
        """
        p = self.persistence()
        if p >= 1:
            return float("inf")
        return float(self.params[0] / (2.0 - p))

    xǁArchResultsǁunconditional_variance__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁArchResultsǁunconditional_variance__mutmut_1": xǁArchResultsǁunconditional_variance__mutmut_1,
        "xǁArchResultsǁunconditional_variance__mutmut_2": xǁArchResultsǁunconditional_variance__mutmut_2,
        "xǁArchResultsǁunconditional_variance__mutmut_3": xǁArchResultsǁunconditional_variance__mutmut_3,
        "xǁArchResultsǁunconditional_variance__mutmut_4": xǁArchResultsǁunconditional_variance__mutmut_4,
        "xǁArchResultsǁunconditional_variance__mutmut_5": xǁArchResultsǁunconditional_variance__mutmut_5,
        "xǁArchResultsǁunconditional_variance__mutmut_6": xǁArchResultsǁunconditional_variance__mutmut_6,
        "xǁArchResultsǁunconditional_variance__mutmut_7": xǁArchResultsǁunconditional_variance__mutmut_7,
        "xǁArchResultsǁunconditional_variance__mutmut_8": xǁArchResultsǁunconditional_variance__mutmut_8,
        "xǁArchResultsǁunconditional_variance__mutmut_9": xǁArchResultsǁunconditional_variance__mutmut_9,
        "xǁArchResultsǁunconditional_variance__mutmut_10": xǁArchResultsǁunconditional_variance__mutmut_10,
        "xǁArchResultsǁunconditional_variance__mutmut_11": xǁArchResultsǁunconditional_variance__mutmut_11,
    }
    xǁArchResultsǁunconditional_variance__mutmut_orig.__name__ = (
        "xǁArchResultsǁunconditional_variance"
    )

    def forecast(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        args = [horizon, method]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁArchResultsǁforecast__mutmut_orig"),
            object.__getattribute__(self, "xǁArchResultsǁforecast__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁArchResultsǁforecast__mutmut_orig(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_1(
        self,
        horizon: int = 2,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_2(
        self,
        horizon: int = 1,
        method: str = "XXanalyticXX",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_3(
        self,
        horizon: int = 1,
        method: str = "ANALYTIC",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_4(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = None
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_5(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[1]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_6(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = None
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_7(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = None

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_8(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = None
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_9(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] * 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_10(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[+1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_11(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-2] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_12(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 3
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_13(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = None

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_14(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[+1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_15(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-2]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_16(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = None
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_17(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[2 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_18(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 - getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_19(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 2 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_20(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(None, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_21(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, None, 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_22(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", None)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_23(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr("q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_24(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_25(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + self._model.q]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_26(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "XXqXX", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_27(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "Q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_28(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 2)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_29(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = None

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_30(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 - getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_31(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[2 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_32(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(None, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_33(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, None, 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_34(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", None) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_35(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr("q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_36(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_37(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + self._model.q :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_38(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "XXqXX", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_39(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "Q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_40(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 2) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_41(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = None

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_42(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 - np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_43(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega - np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_44(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) / last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_45(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(None) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_46(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) / last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_47(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(None) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_48(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = None
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_49(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(None)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_50(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(None):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_51(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence > 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_52(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 2.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_53(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = None
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_54(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = None

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_55(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf - persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_56(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h / (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_57(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence * h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_58(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next + sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_59(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "XXvarianceXX": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_60(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "VARIANCE": variance,
            "volatility": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_61(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "XXvolatilityXX": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_62(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "VOLATILITY": np.sqrt(variance),
        }

    def xǁArchResultsǁforecast__mutmut_63(
        self,
        horizon: int = 1,
        method: str = "analytic",
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast conditional variance h steps ahead.

        For GARCH(1,1):
            E[sigma^2_{T+h}] = sigma^2_inf + (alpha+beta)^{h-1} * (sigma^2_{T+1} - sigma^2_inf)

        Parameters
        ----------
        horizon : int
            Number of steps ahead.
        method : str
            Forecast method: 'analytic'.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'variance': Forecasted variance, shape (horizon,)
            - 'volatility': Forecasted volatility (sqrt), shape (horizon,)
        """
        omega = self.params[0]
        persistence = self.persistence()
        sigma2_inf = self.unconditional_variance()

        # One-step-ahead: use last observation
        last_resid2 = self._model.endog[-1] ** 2
        last_sigma2 = self._sigma2[-1]

        alphas = self.params[1 : 1 + getattr(self._model, "q", 1)]
        betas = self.params[1 + getattr(self._model, "q", 1) :]

        sigma2_next = omega + np.sum(alphas) * last_resid2 + np.sum(betas) * last_sigma2

        variance = np.empty(horizon)
        for h in range(horizon):
            if persistence >= 1.0:
                variance[h] = sigma2_next
            else:
                variance[h] = sigma2_inf + persistence**h * (sigma2_next - sigma2_inf)

        return {
            "variance": variance,
            "volatility": np.sqrt(None),
        }

    xǁArchResultsǁforecast__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁArchResultsǁforecast__mutmut_1": xǁArchResultsǁforecast__mutmut_1,
        "xǁArchResultsǁforecast__mutmut_2": xǁArchResultsǁforecast__mutmut_2,
        "xǁArchResultsǁforecast__mutmut_3": xǁArchResultsǁforecast__mutmut_3,
        "xǁArchResultsǁforecast__mutmut_4": xǁArchResultsǁforecast__mutmut_4,
        "xǁArchResultsǁforecast__mutmut_5": xǁArchResultsǁforecast__mutmut_5,
        "xǁArchResultsǁforecast__mutmut_6": xǁArchResultsǁforecast__mutmut_6,
        "xǁArchResultsǁforecast__mutmut_7": xǁArchResultsǁforecast__mutmut_7,
        "xǁArchResultsǁforecast__mutmut_8": xǁArchResultsǁforecast__mutmut_8,
        "xǁArchResultsǁforecast__mutmut_9": xǁArchResultsǁforecast__mutmut_9,
        "xǁArchResultsǁforecast__mutmut_10": xǁArchResultsǁforecast__mutmut_10,
        "xǁArchResultsǁforecast__mutmut_11": xǁArchResultsǁforecast__mutmut_11,
        "xǁArchResultsǁforecast__mutmut_12": xǁArchResultsǁforecast__mutmut_12,
        "xǁArchResultsǁforecast__mutmut_13": xǁArchResultsǁforecast__mutmut_13,
        "xǁArchResultsǁforecast__mutmut_14": xǁArchResultsǁforecast__mutmut_14,
        "xǁArchResultsǁforecast__mutmut_15": xǁArchResultsǁforecast__mutmut_15,
        "xǁArchResultsǁforecast__mutmut_16": xǁArchResultsǁforecast__mutmut_16,
        "xǁArchResultsǁforecast__mutmut_17": xǁArchResultsǁforecast__mutmut_17,
        "xǁArchResultsǁforecast__mutmut_18": xǁArchResultsǁforecast__mutmut_18,
        "xǁArchResultsǁforecast__mutmut_19": xǁArchResultsǁforecast__mutmut_19,
        "xǁArchResultsǁforecast__mutmut_20": xǁArchResultsǁforecast__mutmut_20,
        "xǁArchResultsǁforecast__mutmut_21": xǁArchResultsǁforecast__mutmut_21,
        "xǁArchResultsǁforecast__mutmut_22": xǁArchResultsǁforecast__mutmut_22,
        "xǁArchResultsǁforecast__mutmut_23": xǁArchResultsǁforecast__mutmut_23,
        "xǁArchResultsǁforecast__mutmut_24": xǁArchResultsǁforecast__mutmut_24,
        "xǁArchResultsǁforecast__mutmut_25": xǁArchResultsǁforecast__mutmut_25,
        "xǁArchResultsǁforecast__mutmut_26": xǁArchResultsǁforecast__mutmut_26,
        "xǁArchResultsǁforecast__mutmut_27": xǁArchResultsǁforecast__mutmut_27,
        "xǁArchResultsǁforecast__mutmut_28": xǁArchResultsǁforecast__mutmut_28,
        "xǁArchResultsǁforecast__mutmut_29": xǁArchResultsǁforecast__mutmut_29,
        "xǁArchResultsǁforecast__mutmut_30": xǁArchResultsǁforecast__mutmut_30,
        "xǁArchResultsǁforecast__mutmut_31": xǁArchResultsǁforecast__mutmut_31,
        "xǁArchResultsǁforecast__mutmut_32": xǁArchResultsǁforecast__mutmut_32,
        "xǁArchResultsǁforecast__mutmut_33": xǁArchResultsǁforecast__mutmut_33,
        "xǁArchResultsǁforecast__mutmut_34": xǁArchResultsǁforecast__mutmut_34,
        "xǁArchResultsǁforecast__mutmut_35": xǁArchResultsǁforecast__mutmut_35,
        "xǁArchResultsǁforecast__mutmut_36": xǁArchResultsǁforecast__mutmut_36,
        "xǁArchResultsǁforecast__mutmut_37": xǁArchResultsǁforecast__mutmut_37,
        "xǁArchResultsǁforecast__mutmut_38": xǁArchResultsǁforecast__mutmut_38,
        "xǁArchResultsǁforecast__mutmut_39": xǁArchResultsǁforecast__mutmut_39,
        "xǁArchResultsǁforecast__mutmut_40": xǁArchResultsǁforecast__mutmut_40,
        "xǁArchResultsǁforecast__mutmut_41": xǁArchResultsǁforecast__mutmut_41,
        "xǁArchResultsǁforecast__mutmut_42": xǁArchResultsǁforecast__mutmut_42,
        "xǁArchResultsǁforecast__mutmut_43": xǁArchResultsǁforecast__mutmut_43,
        "xǁArchResultsǁforecast__mutmut_44": xǁArchResultsǁforecast__mutmut_44,
        "xǁArchResultsǁforecast__mutmut_45": xǁArchResultsǁforecast__mutmut_45,
        "xǁArchResultsǁforecast__mutmut_46": xǁArchResultsǁforecast__mutmut_46,
        "xǁArchResultsǁforecast__mutmut_47": xǁArchResultsǁforecast__mutmut_47,
        "xǁArchResultsǁforecast__mutmut_48": xǁArchResultsǁforecast__mutmut_48,
        "xǁArchResultsǁforecast__mutmut_49": xǁArchResultsǁforecast__mutmut_49,
        "xǁArchResultsǁforecast__mutmut_50": xǁArchResultsǁforecast__mutmut_50,
        "xǁArchResultsǁforecast__mutmut_51": xǁArchResultsǁforecast__mutmut_51,
        "xǁArchResultsǁforecast__mutmut_52": xǁArchResultsǁforecast__mutmut_52,
        "xǁArchResultsǁforecast__mutmut_53": xǁArchResultsǁforecast__mutmut_53,
        "xǁArchResultsǁforecast__mutmut_54": xǁArchResultsǁforecast__mutmut_54,
        "xǁArchResultsǁforecast__mutmut_55": xǁArchResultsǁforecast__mutmut_55,
        "xǁArchResultsǁforecast__mutmut_56": xǁArchResultsǁforecast__mutmut_56,
        "xǁArchResultsǁforecast__mutmut_57": xǁArchResultsǁforecast__mutmut_57,
        "xǁArchResultsǁforecast__mutmut_58": xǁArchResultsǁforecast__mutmut_58,
        "xǁArchResultsǁforecast__mutmut_59": xǁArchResultsǁforecast__mutmut_59,
        "xǁArchResultsǁforecast__mutmut_60": xǁArchResultsǁforecast__mutmut_60,
        "xǁArchResultsǁforecast__mutmut_61": xǁArchResultsǁforecast__mutmut_61,
        "xǁArchResultsǁforecast__mutmut_62": xǁArchResultsǁforecast__mutmut_62,
        "xǁArchResultsǁforecast__mutmut_63": xǁArchResultsǁforecast__mutmut_63,
    }
    xǁArchResultsǁforecast__mutmut_orig.__name__ = "xǁArchResultsǁforecast"

    def summary(self) -> str:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁArchResultsǁsummary__mutmut_orig"),
            object.__getattribute__(self, "xǁArchResultsǁsummary__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁArchResultsǁsummary__mutmut_orig(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_1(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = None
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_2(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append(None)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_3(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" / 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_4(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("XX=XX" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_5(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 71)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_6(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(None)
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_7(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'XXVolatility Model ResultsXX':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_8(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'volatility model results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_9(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'VOLATILITY MODEL RESULTS':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_10(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append(None)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_11(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" / 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_12(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("XX=XX" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_13(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 71)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_14(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(None)
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_15(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(None)
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_16(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(None)
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_17(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(None)
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_18(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(None)
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_19(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(None)
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_20(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(None)
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_21(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append(None)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_22(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" / 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_23(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("XX-XX" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_24(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 71)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_25(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(None)
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_26(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'XXParameterXX':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_27(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_28(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'PARAMETER':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_29(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'XXEstimateXX':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_30(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_31(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'ESTIMATE':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_32(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'XXStd ErrXX':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_33(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'std err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_34(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'STD ERR':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_35(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'XXt-valueXX':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_36(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'T-VALUE':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_37(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'XXp-valueXX':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_38(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'P-VALUE':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_39(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append(None)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_40(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" / 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_41(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("XX-XX" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_42(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 71)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_43(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            None,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_44(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            None,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_45(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            None,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_46(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            None,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_47(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            None,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_48(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=None,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_49(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_50(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_51(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_52(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_53(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_54(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=False,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_55(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=False,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_56(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(None)
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_57(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append(None)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_58(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" / 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_59(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("XX-XX" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_60(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 71)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_61(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(None)
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_62(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(None)
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_63(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(None)
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_64(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(None)
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_65(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(None):.6e}")
        lines.append("=" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_66(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append(None)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_67(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" / 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_68(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("XX=XX" * 70)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_69(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 71)
        return "\n".join(lines)

    def xǁArchResultsǁsummary__mutmut_70(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "\n".join(None)

    def xǁArchResultsǁsummary__mutmut_71(self) -> str:
        """Generate formatted summary table.

        Returns
        -------
        str
            Formatted summary with parameters, SE, t-values, p-values,
            log-likelihood, AIC/BIC, persistence, and half-life.
        """
        lines: list[str] = []
        lines.append("=" * 70)
        lines.append(f"{'Volatility Model Results':^70}")
        lines.append("=" * 70)
        lines.append(f"Model:            {self._model.volatility_process}")
        lines.append(f"Distribution:     {self._model.dist.name}")
        lines.append(f"Observations:     {self.nobs}")
        lines.append(f"Log-Likelihood:   {self.loglike:.4f}")
        lines.append(f"AIC:              {self.aic:.4f}")
        lines.append(f"BIC:              {self.bic:.4f}")
        lines.append(f"Converged:        {self.convergence}")
        lines.append("-" * 70)
        lines.append(
            f"{'Parameter':<15} {'Estimate':>12} {'Std Err':>12} {'t-value':>12} {'p-value':>12}"
        )
        lines.append("-" * 70)
        for name, param, se, tv, pv in zip(
            self.param_names,
            self.params,
            self.se,
            self.tvalues,
            self.pvalues,
            strict=True,
        ):
            lines.append(f"{name:<15} {param:>12.6f} {se:>12.6f} {tv:>12.4f} {pv:>12.4f}")
        lines.append("-" * 70)
        lines.append(f"Persistence:      {self.persistence():.6f}")
        lines.append(f"Half-life:        {self.half_life():.2f} periods")
        lines.append(f"Uncond. Variance: {self.unconditional_variance():.6e}")
        lines.append(f"Uncond. Vol:      {np.sqrt(self.unconditional_variance()):.6e}")
        lines.append("=" * 70)
        return "XX\nXX".join(lines)

    xǁArchResultsǁsummary__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁArchResultsǁsummary__mutmut_1": xǁArchResultsǁsummary__mutmut_1,
        "xǁArchResultsǁsummary__mutmut_2": xǁArchResultsǁsummary__mutmut_2,
        "xǁArchResultsǁsummary__mutmut_3": xǁArchResultsǁsummary__mutmut_3,
        "xǁArchResultsǁsummary__mutmut_4": xǁArchResultsǁsummary__mutmut_4,
        "xǁArchResultsǁsummary__mutmut_5": xǁArchResultsǁsummary__mutmut_5,
        "xǁArchResultsǁsummary__mutmut_6": xǁArchResultsǁsummary__mutmut_6,
        "xǁArchResultsǁsummary__mutmut_7": xǁArchResultsǁsummary__mutmut_7,
        "xǁArchResultsǁsummary__mutmut_8": xǁArchResultsǁsummary__mutmut_8,
        "xǁArchResultsǁsummary__mutmut_9": xǁArchResultsǁsummary__mutmut_9,
        "xǁArchResultsǁsummary__mutmut_10": xǁArchResultsǁsummary__mutmut_10,
        "xǁArchResultsǁsummary__mutmut_11": xǁArchResultsǁsummary__mutmut_11,
        "xǁArchResultsǁsummary__mutmut_12": xǁArchResultsǁsummary__mutmut_12,
        "xǁArchResultsǁsummary__mutmut_13": xǁArchResultsǁsummary__mutmut_13,
        "xǁArchResultsǁsummary__mutmut_14": xǁArchResultsǁsummary__mutmut_14,
        "xǁArchResultsǁsummary__mutmut_15": xǁArchResultsǁsummary__mutmut_15,
        "xǁArchResultsǁsummary__mutmut_16": xǁArchResultsǁsummary__mutmut_16,
        "xǁArchResultsǁsummary__mutmut_17": xǁArchResultsǁsummary__mutmut_17,
        "xǁArchResultsǁsummary__mutmut_18": xǁArchResultsǁsummary__mutmut_18,
        "xǁArchResultsǁsummary__mutmut_19": xǁArchResultsǁsummary__mutmut_19,
        "xǁArchResultsǁsummary__mutmut_20": xǁArchResultsǁsummary__mutmut_20,
        "xǁArchResultsǁsummary__mutmut_21": xǁArchResultsǁsummary__mutmut_21,
        "xǁArchResultsǁsummary__mutmut_22": xǁArchResultsǁsummary__mutmut_22,
        "xǁArchResultsǁsummary__mutmut_23": xǁArchResultsǁsummary__mutmut_23,
        "xǁArchResultsǁsummary__mutmut_24": xǁArchResultsǁsummary__mutmut_24,
        "xǁArchResultsǁsummary__mutmut_25": xǁArchResultsǁsummary__mutmut_25,
        "xǁArchResultsǁsummary__mutmut_26": xǁArchResultsǁsummary__mutmut_26,
        "xǁArchResultsǁsummary__mutmut_27": xǁArchResultsǁsummary__mutmut_27,
        "xǁArchResultsǁsummary__mutmut_28": xǁArchResultsǁsummary__mutmut_28,
        "xǁArchResultsǁsummary__mutmut_29": xǁArchResultsǁsummary__mutmut_29,
        "xǁArchResultsǁsummary__mutmut_30": xǁArchResultsǁsummary__mutmut_30,
        "xǁArchResultsǁsummary__mutmut_31": xǁArchResultsǁsummary__mutmut_31,
        "xǁArchResultsǁsummary__mutmut_32": xǁArchResultsǁsummary__mutmut_32,
        "xǁArchResultsǁsummary__mutmut_33": xǁArchResultsǁsummary__mutmut_33,
        "xǁArchResultsǁsummary__mutmut_34": xǁArchResultsǁsummary__mutmut_34,
        "xǁArchResultsǁsummary__mutmut_35": xǁArchResultsǁsummary__mutmut_35,
        "xǁArchResultsǁsummary__mutmut_36": xǁArchResultsǁsummary__mutmut_36,
        "xǁArchResultsǁsummary__mutmut_37": xǁArchResultsǁsummary__mutmut_37,
        "xǁArchResultsǁsummary__mutmut_38": xǁArchResultsǁsummary__mutmut_38,
        "xǁArchResultsǁsummary__mutmut_39": xǁArchResultsǁsummary__mutmut_39,
        "xǁArchResultsǁsummary__mutmut_40": xǁArchResultsǁsummary__mutmut_40,
        "xǁArchResultsǁsummary__mutmut_41": xǁArchResultsǁsummary__mutmut_41,
        "xǁArchResultsǁsummary__mutmut_42": xǁArchResultsǁsummary__mutmut_42,
        "xǁArchResultsǁsummary__mutmut_43": xǁArchResultsǁsummary__mutmut_43,
        "xǁArchResultsǁsummary__mutmut_44": xǁArchResultsǁsummary__mutmut_44,
        "xǁArchResultsǁsummary__mutmut_45": xǁArchResultsǁsummary__mutmut_45,
        "xǁArchResultsǁsummary__mutmut_46": xǁArchResultsǁsummary__mutmut_46,
        "xǁArchResultsǁsummary__mutmut_47": xǁArchResultsǁsummary__mutmut_47,
        "xǁArchResultsǁsummary__mutmut_48": xǁArchResultsǁsummary__mutmut_48,
        "xǁArchResultsǁsummary__mutmut_49": xǁArchResultsǁsummary__mutmut_49,
        "xǁArchResultsǁsummary__mutmut_50": xǁArchResultsǁsummary__mutmut_50,
        "xǁArchResultsǁsummary__mutmut_51": xǁArchResultsǁsummary__mutmut_51,
        "xǁArchResultsǁsummary__mutmut_52": xǁArchResultsǁsummary__mutmut_52,
        "xǁArchResultsǁsummary__mutmut_53": xǁArchResultsǁsummary__mutmut_53,
        "xǁArchResultsǁsummary__mutmut_54": xǁArchResultsǁsummary__mutmut_54,
        "xǁArchResultsǁsummary__mutmut_55": xǁArchResultsǁsummary__mutmut_55,
        "xǁArchResultsǁsummary__mutmut_56": xǁArchResultsǁsummary__mutmut_56,
        "xǁArchResultsǁsummary__mutmut_57": xǁArchResultsǁsummary__mutmut_57,
        "xǁArchResultsǁsummary__mutmut_58": xǁArchResultsǁsummary__mutmut_58,
        "xǁArchResultsǁsummary__mutmut_59": xǁArchResultsǁsummary__mutmut_59,
        "xǁArchResultsǁsummary__mutmut_60": xǁArchResultsǁsummary__mutmut_60,
        "xǁArchResultsǁsummary__mutmut_61": xǁArchResultsǁsummary__mutmut_61,
        "xǁArchResultsǁsummary__mutmut_62": xǁArchResultsǁsummary__mutmut_62,
        "xǁArchResultsǁsummary__mutmut_63": xǁArchResultsǁsummary__mutmut_63,
        "xǁArchResultsǁsummary__mutmut_64": xǁArchResultsǁsummary__mutmut_64,
        "xǁArchResultsǁsummary__mutmut_65": xǁArchResultsǁsummary__mutmut_65,
        "xǁArchResultsǁsummary__mutmut_66": xǁArchResultsǁsummary__mutmut_66,
        "xǁArchResultsǁsummary__mutmut_67": xǁArchResultsǁsummary__mutmut_67,
        "xǁArchResultsǁsummary__mutmut_68": xǁArchResultsǁsummary__mutmut_68,
        "xǁArchResultsǁsummary__mutmut_69": xǁArchResultsǁsummary__mutmut_69,
        "xǁArchResultsǁsummary__mutmut_70": xǁArchResultsǁsummary__mutmut_70,
        "xǁArchResultsǁsummary__mutmut_71": xǁArchResultsǁsummary__mutmut_71,
    }
    xǁArchResultsǁsummary__mutmut_orig.__name__ = "xǁArchResultsǁsummary"

    def plot(self, which: str = "volatility") -> Any:
        args = [which]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁArchResultsǁplot__mutmut_orig"),
            object.__getattribute__(self, "xǁArchResultsǁplot__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁArchResultsǁplot__mutmut_orig(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_1(self, which: str = "XXvolatilityXX") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_2(self, which: str = "VOLATILITY") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_3(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which != "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_4(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "XXvolatilityXX":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_5(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "VOLATILITY":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_6(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = None
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_7(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(None, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_8(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, None, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_9(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=None, sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_10(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=None)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_11(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_12(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_13(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_14(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(
                2,
                1,
                figsize=(12, 8),
            )
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_15(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_16(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_17(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(13, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_18(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 9), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_19(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=False)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_20(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = None

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_21(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(None, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_22(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color=None, alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_23(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=None, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_24(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=None)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_25(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_26(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_27(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_28(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(
                self._model.endog,
                color="steelblue",
                alpha=0.7,
            )
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_29(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="XXsteelblueXX", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_30(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="STEELBLUE", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_31(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=1.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_32(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=1.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_33(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title(None)
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_34(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("XXReturnsXX")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_35(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_36(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("RETURNS")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_37(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel(None)

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_38(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("XXReturnXX")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_39(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_40(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("RETURN")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_41(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(None, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_42(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color=None, linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_43(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=None)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_44(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_45(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_46(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(
                self.conditional_volatility,
                color="darkred",
            )
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_47(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="XXdarkredXX", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_48(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="DARKRED", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_49(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=2.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_50(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title(None)
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_51(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("XXConditional VolatilityXX")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_52(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("conditional volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_53(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("CONDITIONAL VOLATILITY")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_54(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel(None)
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_55(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("XXVolatility (sigma_t)XX")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_56(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_57(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("VOLATILITY (SIGMA_T)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_58(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel(None)

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_59(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("XXObservationXX")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_60(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_61(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("OBSERVATION")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_62(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which != "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_63(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "XXresidualsXX":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_64(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "RESIDUALS":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_65(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = None
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_66(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(None, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_67(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, None, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_68(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=None)
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_69(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_70(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_71(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(
                2,
                1,
            )
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_72(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(3, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_73(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 2, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_74(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(13, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_75(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 9))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_76(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = None

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_77(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(None, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_78(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color=None, alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_79(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=None, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_80(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=None)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_81(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_82(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_83(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_84(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(
                self.resid,
                color="steelblue",
                alpha=0.7,
            )
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_85(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="XXsteelblueXX", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_86(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="STEELBLUE", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_87(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=1.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_88(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=1.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_89(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=None, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_90(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color=None, linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_91(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=None)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_92(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_93(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_94(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(
                y=0,
                color="black",
            )
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_95(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=1, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_96(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="XXblackXX", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_97(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="BLACK", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_98(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=1.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_99(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title(None)
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_100(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("XXStandardized ResidualsXX")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_101(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("standardized residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_102(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("STANDARDIZED RESIDUALS")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_103(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel(None)

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_104(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("XXz_tXX")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_105(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("Z_T")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_106(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(None, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_107(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=None, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_108(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=None, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_109(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=None, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_110(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color=None)
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_111(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_112(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_113(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_114(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_115(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(
                self.resid,
                bins=50,
                density=True,
                alpha=0.7,
            )
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_116(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=51, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_117(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=False, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_118(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=1.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_119(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="XXsteelblueXX")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_120(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="STEELBLUE")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_121(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = None
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_122(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(None, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_123(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, None, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_124(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, None)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_125(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_126(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_127(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(
                -4,
                4,
            )
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_128(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(+4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_129(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-5, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_130(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 5, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_131(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 201)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_132(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(None, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_133(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, None, "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_134(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), None, linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_135(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=None, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_136(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label=None)
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_137(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_138(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_139(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_140(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_141(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(
                x,
                stats.norm.pdf(x),
                "r-",
                linewidth=2,
            )
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_142(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(None), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_143(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "XXr-XX", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_144(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "R-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_145(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=3, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_146(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="XXN(0,1)XX")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_147(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="n(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_148(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title(None)
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_149(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("XXHistogram of Standardized ResidualsXX")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_150(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("histogram of standardized residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_151(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("HISTOGRAM OF STANDARDIZED RESIDUALS")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_152(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = None
        raise ValueError(msg)

    def xǁArchResultsǁplot__mutmut_153(self, which: str = "volatility") -> Any:
        """Plot conditional volatility or diagnostics.

        Parameters
        ----------
        which : str
            Plot type: 'volatility', 'residuals'.

        Returns
        -------
        matplotlib.figure.Figure
            The figure object.
        """
        import matplotlib.pyplot as plt

        if which == "volatility":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            ax1, ax2 = axes

            ax1.plot(self._model.endog, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.set_title("Returns")
            ax1.set_ylabel("Return")

            ax2.plot(self.conditional_volatility, color="darkred", linewidth=1.0)
            ax2.set_title("Conditional Volatility")
            ax2.set_ylabel("Volatility (sigma_t)")
            ax2.set_xlabel("Observation")

            fig.tight_layout()
            return fig

        elif which == "residuals":
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            ax1, ax2 = axes

            ax1.plot(self.resid, color="steelblue", alpha=0.7, linewidth=0.5)
            ax1.axhline(y=0, color="black", linewidth=0.5)
            ax1.set_title("Standardized Residuals")
            ax1.set_ylabel("z_t")

            ax2.hist(self.resid, bins=50, density=True, alpha=0.7, color="steelblue")
            x = np.linspace(-4, 4, 200)
            ax2.plot(x, stats.norm.pdf(x), "r-", linewidth=2, label="N(0,1)")
            ax2.set_title("Histogram of Standardized Residuals")
            ax2.legend()

            fig.tight_layout()
            return fig

        msg = f"Unknown plot type: {which}. Use 'volatility' or 'residuals'."
        raise ValueError(None)

    xǁArchResultsǁplot__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁArchResultsǁplot__mutmut_1": xǁArchResultsǁplot__mutmut_1,
        "xǁArchResultsǁplot__mutmut_2": xǁArchResultsǁplot__mutmut_2,
        "xǁArchResultsǁplot__mutmut_3": xǁArchResultsǁplot__mutmut_3,
        "xǁArchResultsǁplot__mutmut_4": xǁArchResultsǁplot__mutmut_4,
        "xǁArchResultsǁplot__mutmut_5": xǁArchResultsǁplot__mutmut_5,
        "xǁArchResultsǁplot__mutmut_6": xǁArchResultsǁplot__mutmut_6,
        "xǁArchResultsǁplot__mutmut_7": xǁArchResultsǁplot__mutmut_7,
        "xǁArchResultsǁplot__mutmut_8": xǁArchResultsǁplot__mutmut_8,
        "xǁArchResultsǁplot__mutmut_9": xǁArchResultsǁplot__mutmut_9,
        "xǁArchResultsǁplot__mutmut_10": xǁArchResultsǁplot__mutmut_10,
        "xǁArchResultsǁplot__mutmut_11": xǁArchResultsǁplot__mutmut_11,
        "xǁArchResultsǁplot__mutmut_12": xǁArchResultsǁplot__mutmut_12,
        "xǁArchResultsǁplot__mutmut_13": xǁArchResultsǁplot__mutmut_13,
        "xǁArchResultsǁplot__mutmut_14": xǁArchResultsǁplot__mutmut_14,
        "xǁArchResultsǁplot__mutmut_15": xǁArchResultsǁplot__mutmut_15,
        "xǁArchResultsǁplot__mutmut_16": xǁArchResultsǁplot__mutmut_16,
        "xǁArchResultsǁplot__mutmut_17": xǁArchResultsǁplot__mutmut_17,
        "xǁArchResultsǁplot__mutmut_18": xǁArchResultsǁplot__mutmut_18,
        "xǁArchResultsǁplot__mutmut_19": xǁArchResultsǁplot__mutmut_19,
        "xǁArchResultsǁplot__mutmut_20": xǁArchResultsǁplot__mutmut_20,
        "xǁArchResultsǁplot__mutmut_21": xǁArchResultsǁplot__mutmut_21,
        "xǁArchResultsǁplot__mutmut_22": xǁArchResultsǁplot__mutmut_22,
        "xǁArchResultsǁplot__mutmut_23": xǁArchResultsǁplot__mutmut_23,
        "xǁArchResultsǁplot__mutmut_24": xǁArchResultsǁplot__mutmut_24,
        "xǁArchResultsǁplot__mutmut_25": xǁArchResultsǁplot__mutmut_25,
        "xǁArchResultsǁplot__mutmut_26": xǁArchResultsǁplot__mutmut_26,
        "xǁArchResultsǁplot__mutmut_27": xǁArchResultsǁplot__mutmut_27,
        "xǁArchResultsǁplot__mutmut_28": xǁArchResultsǁplot__mutmut_28,
        "xǁArchResultsǁplot__mutmut_29": xǁArchResultsǁplot__mutmut_29,
        "xǁArchResultsǁplot__mutmut_30": xǁArchResultsǁplot__mutmut_30,
        "xǁArchResultsǁplot__mutmut_31": xǁArchResultsǁplot__mutmut_31,
        "xǁArchResultsǁplot__mutmut_32": xǁArchResultsǁplot__mutmut_32,
        "xǁArchResultsǁplot__mutmut_33": xǁArchResultsǁplot__mutmut_33,
        "xǁArchResultsǁplot__mutmut_34": xǁArchResultsǁplot__mutmut_34,
        "xǁArchResultsǁplot__mutmut_35": xǁArchResultsǁplot__mutmut_35,
        "xǁArchResultsǁplot__mutmut_36": xǁArchResultsǁplot__mutmut_36,
        "xǁArchResultsǁplot__mutmut_37": xǁArchResultsǁplot__mutmut_37,
        "xǁArchResultsǁplot__mutmut_38": xǁArchResultsǁplot__mutmut_38,
        "xǁArchResultsǁplot__mutmut_39": xǁArchResultsǁplot__mutmut_39,
        "xǁArchResultsǁplot__mutmut_40": xǁArchResultsǁplot__mutmut_40,
        "xǁArchResultsǁplot__mutmut_41": xǁArchResultsǁplot__mutmut_41,
        "xǁArchResultsǁplot__mutmut_42": xǁArchResultsǁplot__mutmut_42,
        "xǁArchResultsǁplot__mutmut_43": xǁArchResultsǁplot__mutmut_43,
        "xǁArchResultsǁplot__mutmut_44": xǁArchResultsǁplot__mutmut_44,
        "xǁArchResultsǁplot__mutmut_45": xǁArchResultsǁplot__mutmut_45,
        "xǁArchResultsǁplot__mutmut_46": xǁArchResultsǁplot__mutmut_46,
        "xǁArchResultsǁplot__mutmut_47": xǁArchResultsǁplot__mutmut_47,
        "xǁArchResultsǁplot__mutmut_48": xǁArchResultsǁplot__mutmut_48,
        "xǁArchResultsǁplot__mutmut_49": xǁArchResultsǁplot__mutmut_49,
        "xǁArchResultsǁplot__mutmut_50": xǁArchResultsǁplot__mutmut_50,
        "xǁArchResultsǁplot__mutmut_51": xǁArchResultsǁplot__mutmut_51,
        "xǁArchResultsǁplot__mutmut_52": xǁArchResultsǁplot__mutmut_52,
        "xǁArchResultsǁplot__mutmut_53": xǁArchResultsǁplot__mutmut_53,
        "xǁArchResultsǁplot__mutmut_54": xǁArchResultsǁplot__mutmut_54,
        "xǁArchResultsǁplot__mutmut_55": xǁArchResultsǁplot__mutmut_55,
        "xǁArchResultsǁplot__mutmut_56": xǁArchResultsǁplot__mutmut_56,
        "xǁArchResultsǁplot__mutmut_57": xǁArchResultsǁplot__mutmut_57,
        "xǁArchResultsǁplot__mutmut_58": xǁArchResultsǁplot__mutmut_58,
        "xǁArchResultsǁplot__mutmut_59": xǁArchResultsǁplot__mutmut_59,
        "xǁArchResultsǁplot__mutmut_60": xǁArchResultsǁplot__mutmut_60,
        "xǁArchResultsǁplot__mutmut_61": xǁArchResultsǁplot__mutmut_61,
        "xǁArchResultsǁplot__mutmut_62": xǁArchResultsǁplot__mutmut_62,
        "xǁArchResultsǁplot__mutmut_63": xǁArchResultsǁplot__mutmut_63,
        "xǁArchResultsǁplot__mutmut_64": xǁArchResultsǁplot__mutmut_64,
        "xǁArchResultsǁplot__mutmut_65": xǁArchResultsǁplot__mutmut_65,
        "xǁArchResultsǁplot__mutmut_66": xǁArchResultsǁplot__mutmut_66,
        "xǁArchResultsǁplot__mutmut_67": xǁArchResultsǁplot__mutmut_67,
        "xǁArchResultsǁplot__mutmut_68": xǁArchResultsǁplot__mutmut_68,
        "xǁArchResultsǁplot__mutmut_69": xǁArchResultsǁplot__mutmut_69,
        "xǁArchResultsǁplot__mutmut_70": xǁArchResultsǁplot__mutmut_70,
        "xǁArchResultsǁplot__mutmut_71": xǁArchResultsǁplot__mutmut_71,
        "xǁArchResultsǁplot__mutmut_72": xǁArchResultsǁplot__mutmut_72,
        "xǁArchResultsǁplot__mutmut_73": xǁArchResultsǁplot__mutmut_73,
        "xǁArchResultsǁplot__mutmut_74": xǁArchResultsǁplot__mutmut_74,
        "xǁArchResultsǁplot__mutmut_75": xǁArchResultsǁplot__mutmut_75,
        "xǁArchResultsǁplot__mutmut_76": xǁArchResultsǁplot__mutmut_76,
        "xǁArchResultsǁplot__mutmut_77": xǁArchResultsǁplot__mutmut_77,
        "xǁArchResultsǁplot__mutmut_78": xǁArchResultsǁplot__mutmut_78,
        "xǁArchResultsǁplot__mutmut_79": xǁArchResultsǁplot__mutmut_79,
        "xǁArchResultsǁplot__mutmut_80": xǁArchResultsǁplot__mutmut_80,
        "xǁArchResultsǁplot__mutmut_81": xǁArchResultsǁplot__mutmut_81,
        "xǁArchResultsǁplot__mutmut_82": xǁArchResultsǁplot__mutmut_82,
        "xǁArchResultsǁplot__mutmut_83": xǁArchResultsǁplot__mutmut_83,
        "xǁArchResultsǁplot__mutmut_84": xǁArchResultsǁplot__mutmut_84,
        "xǁArchResultsǁplot__mutmut_85": xǁArchResultsǁplot__mutmut_85,
        "xǁArchResultsǁplot__mutmut_86": xǁArchResultsǁplot__mutmut_86,
        "xǁArchResultsǁplot__mutmut_87": xǁArchResultsǁplot__mutmut_87,
        "xǁArchResultsǁplot__mutmut_88": xǁArchResultsǁplot__mutmut_88,
        "xǁArchResultsǁplot__mutmut_89": xǁArchResultsǁplot__mutmut_89,
        "xǁArchResultsǁplot__mutmut_90": xǁArchResultsǁplot__mutmut_90,
        "xǁArchResultsǁplot__mutmut_91": xǁArchResultsǁplot__mutmut_91,
        "xǁArchResultsǁplot__mutmut_92": xǁArchResultsǁplot__mutmut_92,
        "xǁArchResultsǁplot__mutmut_93": xǁArchResultsǁplot__mutmut_93,
        "xǁArchResultsǁplot__mutmut_94": xǁArchResultsǁplot__mutmut_94,
        "xǁArchResultsǁplot__mutmut_95": xǁArchResultsǁplot__mutmut_95,
        "xǁArchResultsǁplot__mutmut_96": xǁArchResultsǁplot__mutmut_96,
        "xǁArchResultsǁplot__mutmut_97": xǁArchResultsǁplot__mutmut_97,
        "xǁArchResultsǁplot__mutmut_98": xǁArchResultsǁplot__mutmut_98,
        "xǁArchResultsǁplot__mutmut_99": xǁArchResultsǁplot__mutmut_99,
        "xǁArchResultsǁplot__mutmut_100": xǁArchResultsǁplot__mutmut_100,
        "xǁArchResultsǁplot__mutmut_101": xǁArchResultsǁplot__mutmut_101,
        "xǁArchResultsǁplot__mutmut_102": xǁArchResultsǁplot__mutmut_102,
        "xǁArchResultsǁplot__mutmut_103": xǁArchResultsǁplot__mutmut_103,
        "xǁArchResultsǁplot__mutmut_104": xǁArchResultsǁplot__mutmut_104,
        "xǁArchResultsǁplot__mutmut_105": xǁArchResultsǁplot__mutmut_105,
        "xǁArchResultsǁplot__mutmut_106": xǁArchResultsǁplot__mutmut_106,
        "xǁArchResultsǁplot__mutmut_107": xǁArchResultsǁplot__mutmut_107,
        "xǁArchResultsǁplot__mutmut_108": xǁArchResultsǁplot__mutmut_108,
        "xǁArchResultsǁplot__mutmut_109": xǁArchResultsǁplot__mutmut_109,
        "xǁArchResultsǁplot__mutmut_110": xǁArchResultsǁplot__mutmut_110,
        "xǁArchResultsǁplot__mutmut_111": xǁArchResultsǁplot__mutmut_111,
        "xǁArchResultsǁplot__mutmut_112": xǁArchResultsǁplot__mutmut_112,
        "xǁArchResultsǁplot__mutmut_113": xǁArchResultsǁplot__mutmut_113,
        "xǁArchResultsǁplot__mutmut_114": xǁArchResultsǁplot__mutmut_114,
        "xǁArchResultsǁplot__mutmut_115": xǁArchResultsǁplot__mutmut_115,
        "xǁArchResultsǁplot__mutmut_116": xǁArchResultsǁplot__mutmut_116,
        "xǁArchResultsǁplot__mutmut_117": xǁArchResultsǁplot__mutmut_117,
        "xǁArchResultsǁplot__mutmut_118": xǁArchResultsǁplot__mutmut_118,
        "xǁArchResultsǁplot__mutmut_119": xǁArchResultsǁplot__mutmut_119,
        "xǁArchResultsǁplot__mutmut_120": xǁArchResultsǁplot__mutmut_120,
        "xǁArchResultsǁplot__mutmut_121": xǁArchResultsǁplot__mutmut_121,
        "xǁArchResultsǁplot__mutmut_122": xǁArchResultsǁplot__mutmut_122,
        "xǁArchResultsǁplot__mutmut_123": xǁArchResultsǁplot__mutmut_123,
        "xǁArchResultsǁplot__mutmut_124": xǁArchResultsǁplot__mutmut_124,
        "xǁArchResultsǁplot__mutmut_125": xǁArchResultsǁplot__mutmut_125,
        "xǁArchResultsǁplot__mutmut_126": xǁArchResultsǁplot__mutmut_126,
        "xǁArchResultsǁplot__mutmut_127": xǁArchResultsǁplot__mutmut_127,
        "xǁArchResultsǁplot__mutmut_128": xǁArchResultsǁplot__mutmut_128,
        "xǁArchResultsǁplot__mutmut_129": xǁArchResultsǁplot__mutmut_129,
        "xǁArchResultsǁplot__mutmut_130": xǁArchResultsǁplot__mutmut_130,
        "xǁArchResultsǁplot__mutmut_131": xǁArchResultsǁplot__mutmut_131,
        "xǁArchResultsǁplot__mutmut_132": xǁArchResultsǁplot__mutmut_132,
        "xǁArchResultsǁplot__mutmut_133": xǁArchResultsǁplot__mutmut_133,
        "xǁArchResultsǁplot__mutmut_134": xǁArchResultsǁplot__mutmut_134,
        "xǁArchResultsǁplot__mutmut_135": xǁArchResultsǁplot__mutmut_135,
        "xǁArchResultsǁplot__mutmut_136": xǁArchResultsǁplot__mutmut_136,
        "xǁArchResultsǁplot__mutmut_137": xǁArchResultsǁplot__mutmut_137,
        "xǁArchResultsǁplot__mutmut_138": xǁArchResultsǁplot__mutmut_138,
        "xǁArchResultsǁplot__mutmut_139": xǁArchResultsǁplot__mutmut_139,
        "xǁArchResultsǁplot__mutmut_140": xǁArchResultsǁplot__mutmut_140,
        "xǁArchResultsǁplot__mutmut_141": xǁArchResultsǁplot__mutmut_141,
        "xǁArchResultsǁplot__mutmut_142": xǁArchResultsǁplot__mutmut_142,
        "xǁArchResultsǁplot__mutmut_143": xǁArchResultsǁplot__mutmut_143,
        "xǁArchResultsǁplot__mutmut_144": xǁArchResultsǁplot__mutmut_144,
        "xǁArchResultsǁplot__mutmut_145": xǁArchResultsǁplot__mutmut_145,
        "xǁArchResultsǁplot__mutmut_146": xǁArchResultsǁplot__mutmut_146,
        "xǁArchResultsǁplot__mutmut_147": xǁArchResultsǁplot__mutmut_147,
        "xǁArchResultsǁplot__mutmut_148": xǁArchResultsǁplot__mutmut_148,
        "xǁArchResultsǁplot__mutmut_149": xǁArchResultsǁplot__mutmut_149,
        "xǁArchResultsǁplot__mutmut_150": xǁArchResultsǁplot__mutmut_150,
        "xǁArchResultsǁplot__mutmut_151": xǁArchResultsǁplot__mutmut_151,
        "xǁArchResultsǁplot__mutmut_152": xǁArchResultsǁplot__mutmut_152,
        "xǁArchResultsǁplot__mutmut_153": xǁArchResultsǁplot__mutmut_153,
    }
    xǁArchResultsǁplot__mutmut_orig.__name__ = "xǁArchResultsǁplot"

    def to_dataframe(self) -> pd.DataFrame:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁArchResultsǁto_dataframe__mutmut_orig"),
            object.__getattribute__(self, "xǁArchResultsǁto_dataframe__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁArchResultsǁto_dataframe__mutmut_orig(self) -> pd.DataFrame:
        """Export parameter estimates as DataFrame.

        Returns
        -------
        pd.DataFrame
            DataFrame with columns: estimate, std_err, t_value, p_value.
        """
        return pd.DataFrame(
            {
                "estimate": self.params,
                "std_err": self.se,
                "t_value": self.tvalues,
                "p_value": self.pvalues,
            },
            index=self.param_names,
        )

    def xǁArchResultsǁto_dataframe__mutmut_1(self) -> pd.DataFrame:
        """Export parameter estimates as DataFrame.

        Returns
        -------
        pd.DataFrame
            DataFrame with columns: estimate, std_err, t_value, p_value.
        """
        return pd.DataFrame(
            None,
            index=self.param_names,
        )

    def xǁArchResultsǁto_dataframe__mutmut_2(self) -> pd.DataFrame:
        """Export parameter estimates as DataFrame.

        Returns
        -------
        pd.DataFrame
            DataFrame with columns: estimate, std_err, t_value, p_value.
        """
        return pd.DataFrame(
            {
                "estimate": self.params,
                "std_err": self.se,
                "t_value": self.tvalues,
                "p_value": self.pvalues,
            },
            index=None,
        )

    def xǁArchResultsǁto_dataframe__mutmut_3(self) -> pd.DataFrame:
        """Export parameter estimates as DataFrame.

        Returns
        -------
        pd.DataFrame
            DataFrame with columns: estimate, std_err, t_value, p_value.
        """
        return pd.DataFrame(
            index=self.param_names,
        )

    def xǁArchResultsǁto_dataframe__mutmut_4(self) -> pd.DataFrame:
        """Export parameter estimates as DataFrame.

        Returns
        -------
        pd.DataFrame
            DataFrame with columns: estimate, std_err, t_value, p_value.
        """
        return pd.DataFrame(
            {
                "estimate": self.params,
                "std_err": self.se,
                "t_value": self.tvalues,
                "p_value": self.pvalues,
            },
        )

    def xǁArchResultsǁto_dataframe__mutmut_5(self) -> pd.DataFrame:
        """Export parameter estimates as DataFrame.

        Returns
        -------
        pd.DataFrame
            DataFrame with columns: estimate, std_err, t_value, p_value.
        """
        return pd.DataFrame(
            {
                "XXestimateXX": self.params,
                "std_err": self.se,
                "t_value": self.tvalues,
                "p_value": self.pvalues,
            },
            index=self.param_names,
        )

    def xǁArchResultsǁto_dataframe__mutmut_6(self) -> pd.DataFrame:
        """Export parameter estimates as DataFrame.

        Returns
        -------
        pd.DataFrame
            DataFrame with columns: estimate, std_err, t_value, p_value.
        """
        return pd.DataFrame(
            {
                "ESTIMATE": self.params,
                "std_err": self.se,
                "t_value": self.tvalues,
                "p_value": self.pvalues,
            },
            index=self.param_names,
        )

    def xǁArchResultsǁto_dataframe__mutmut_7(self) -> pd.DataFrame:
        """Export parameter estimates as DataFrame.

        Returns
        -------
        pd.DataFrame
            DataFrame with columns: estimate, std_err, t_value, p_value.
        """
        return pd.DataFrame(
            {
                "estimate": self.params,
                "XXstd_errXX": self.se,
                "t_value": self.tvalues,
                "p_value": self.pvalues,
            },
            index=self.param_names,
        )

    def xǁArchResultsǁto_dataframe__mutmut_8(self) -> pd.DataFrame:
        """Export parameter estimates as DataFrame.

        Returns
        -------
        pd.DataFrame
            DataFrame with columns: estimate, std_err, t_value, p_value.
        """
        return pd.DataFrame(
            {
                "estimate": self.params,
                "STD_ERR": self.se,
                "t_value": self.tvalues,
                "p_value": self.pvalues,
            },
            index=self.param_names,
        )

    def xǁArchResultsǁto_dataframe__mutmut_9(self) -> pd.DataFrame:
        """Export parameter estimates as DataFrame.

        Returns
        -------
        pd.DataFrame
            DataFrame with columns: estimate, std_err, t_value, p_value.
        """
        return pd.DataFrame(
            {
                "estimate": self.params,
                "std_err": self.se,
                "XXt_valueXX": self.tvalues,
                "p_value": self.pvalues,
            },
            index=self.param_names,
        )

    def xǁArchResultsǁto_dataframe__mutmut_10(self) -> pd.DataFrame:
        """Export parameter estimates as DataFrame.

        Returns
        -------
        pd.DataFrame
            DataFrame with columns: estimate, std_err, t_value, p_value.
        """
        return pd.DataFrame(
            {
                "estimate": self.params,
                "std_err": self.se,
                "T_VALUE": self.tvalues,
                "p_value": self.pvalues,
            },
            index=self.param_names,
        )

    def xǁArchResultsǁto_dataframe__mutmut_11(self) -> pd.DataFrame:
        """Export parameter estimates as DataFrame.

        Returns
        -------
        pd.DataFrame
            DataFrame with columns: estimate, std_err, t_value, p_value.
        """
        return pd.DataFrame(
            {
                "estimate": self.params,
                "std_err": self.se,
                "t_value": self.tvalues,
                "XXp_valueXX": self.pvalues,
            },
            index=self.param_names,
        )

    def xǁArchResultsǁto_dataframe__mutmut_12(self) -> pd.DataFrame:
        """Export parameter estimates as DataFrame.

        Returns
        -------
        pd.DataFrame
            DataFrame with columns: estimate, std_err, t_value, p_value.
        """
        return pd.DataFrame(
            {
                "estimate": self.params,
                "std_err": self.se,
                "t_value": self.tvalues,
                "P_VALUE": self.pvalues,
            },
            index=self.param_names,
        )

    xǁArchResultsǁto_dataframe__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁArchResultsǁto_dataframe__mutmut_1": xǁArchResultsǁto_dataframe__mutmut_1,
        "xǁArchResultsǁto_dataframe__mutmut_2": xǁArchResultsǁto_dataframe__mutmut_2,
        "xǁArchResultsǁto_dataframe__mutmut_3": xǁArchResultsǁto_dataframe__mutmut_3,
        "xǁArchResultsǁto_dataframe__mutmut_4": xǁArchResultsǁto_dataframe__mutmut_4,
        "xǁArchResultsǁto_dataframe__mutmut_5": xǁArchResultsǁto_dataframe__mutmut_5,
        "xǁArchResultsǁto_dataframe__mutmut_6": xǁArchResultsǁto_dataframe__mutmut_6,
        "xǁArchResultsǁto_dataframe__mutmut_7": xǁArchResultsǁto_dataframe__mutmut_7,
        "xǁArchResultsǁto_dataframe__mutmut_8": xǁArchResultsǁto_dataframe__mutmut_8,
        "xǁArchResultsǁto_dataframe__mutmut_9": xǁArchResultsǁto_dataframe__mutmut_9,
        "xǁArchResultsǁto_dataframe__mutmut_10": xǁArchResultsǁto_dataframe__mutmut_10,
        "xǁArchResultsǁto_dataframe__mutmut_11": xǁArchResultsǁto_dataframe__mutmut_11,
        "xǁArchResultsǁto_dataframe__mutmut_12": xǁArchResultsǁto_dataframe__mutmut_12,
    }
    xǁArchResultsǁto_dataframe__mutmut_orig.__name__ = "xǁArchResultsǁto_dataframe"

    def save(self, path: str | Path) -> None:
        args = [path]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁArchResultsǁsave__mutmut_orig"),
            object.__getattribute__(self, "xǁArchResultsǁsave__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁArchResultsǁsave__mutmut_orig(self, path: str | Path) -> None:
        """Save results to pickle file.

        Parameters
        ----------
        path : str or Path
            Output file path.
        """
        with open(path, "wb") as f:
            pickle.dump(self, f)

    def xǁArchResultsǁsave__mutmut_1(self, path: str | Path) -> None:
        """Save results to pickle file.

        Parameters
        ----------
        path : str or Path
            Output file path.
        """
        with open(None, "wb") as f:
            pickle.dump(self, f)

    def xǁArchResultsǁsave__mutmut_2(self, path: str | Path) -> None:
        """Save results to pickle file.

        Parameters
        ----------
        path : str or Path
            Output file path.
        """
        with open(path, None) as f:
            pickle.dump(self, f)

    def xǁArchResultsǁsave__mutmut_3(self, path: str | Path) -> None:
        """Save results to pickle file.

        Parameters
        ----------
        path : str or Path
            Output file path.
        """
        with open("wb") as f:
            pickle.dump(self, f)

    def xǁArchResultsǁsave__mutmut_4(self, path: str | Path) -> None:
        """Save results to pickle file.

        Parameters
        ----------
        path : str or Path
            Output file path.
        """
        with open(
            path,
        ) as f:
            pickle.dump(self, f)

    def xǁArchResultsǁsave__mutmut_5(self, path: str | Path) -> None:
        """Save results to pickle file.

        Parameters
        ----------
        path : str or Path
            Output file path.
        """
        with open(path, "XXwbXX") as f:
            pickle.dump(self, f)

    def xǁArchResultsǁsave__mutmut_6(self, path: str | Path) -> None:
        """Save results to pickle file.

        Parameters
        ----------
        path : str or Path
            Output file path.
        """
        with open(path, "WB") as f:
            pickle.dump(self, f)

    def xǁArchResultsǁsave__mutmut_7(self, path: str | Path) -> None:
        """Save results to pickle file.

        Parameters
        ----------
        path : str or Path
            Output file path.
        """
        with open(path, "wb") as f:
            pickle.dump(None, f)

    def xǁArchResultsǁsave__mutmut_8(self, path: str | Path) -> None:
        """Save results to pickle file.

        Parameters
        ----------
        path : str or Path
            Output file path.
        """
        with open(path, "wb") as f:
            pickle.dump(self, None)

    def xǁArchResultsǁsave__mutmut_9(self, path: str | Path) -> None:
        """Save results to pickle file.

        Parameters
        ----------
        path : str or Path
            Output file path.
        """
        with open(path, "wb") as f:
            pickle.dump(f)

    def xǁArchResultsǁsave__mutmut_10(self, path: str | Path) -> None:
        """Save results to pickle file.

        Parameters
        ----------
        path : str or Path
            Output file path.
        """
        with open(path, "wb") as f:
            pickle.dump(
                self,
            )

    xǁArchResultsǁsave__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁArchResultsǁsave__mutmut_1": xǁArchResultsǁsave__mutmut_1,
        "xǁArchResultsǁsave__mutmut_2": xǁArchResultsǁsave__mutmut_2,
        "xǁArchResultsǁsave__mutmut_3": xǁArchResultsǁsave__mutmut_3,
        "xǁArchResultsǁsave__mutmut_4": xǁArchResultsǁsave__mutmut_4,
        "xǁArchResultsǁsave__mutmut_5": xǁArchResultsǁsave__mutmut_5,
        "xǁArchResultsǁsave__mutmut_6": xǁArchResultsǁsave__mutmut_6,
        "xǁArchResultsǁsave__mutmut_7": xǁArchResultsǁsave__mutmut_7,
        "xǁArchResultsǁsave__mutmut_8": xǁArchResultsǁsave__mutmut_8,
        "xǁArchResultsǁsave__mutmut_9": xǁArchResultsǁsave__mutmut_9,
        "xǁArchResultsǁsave__mutmut_10": xǁArchResultsǁsave__mutmut_10,
    }
    xǁArchResultsǁsave__mutmut_orig.__name__ = "xǁArchResultsǁsave"

    @staticmethod
    def load(path: str | Path) -> ArchResults:
        """Load results from pickle file.

        Parameters
        ----------
        path : str or Path
            Input file path.

        Returns
        -------
        ArchResults
            Loaded results.
        """
        with open(path, "rb") as f:
            return pickle.load(f)  # noqa: S301  # nosec B301

    def __repr__(self) -> str:
        """Return string representation of ArchResults."""
        return (
            f"ArchResults(model={self._model.volatility_process}, "
            f"nobs={self.nobs}, loglike={self.loglike:.4f})"
        )
