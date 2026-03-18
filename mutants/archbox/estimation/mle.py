"""Maximum Likelihood Estimation for volatility models."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from scipy import optimize

from archbox._logging import get_logger
from archbox.core.results import ArchResults

if TYPE_CHECKING:
    from archbox.core.volatility_model import VolatilityModel

logger = get_logger("estimation.mle")
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


class MLEstimator:
    """Maximum Likelihood Estimator for ARCH/GARCH models.

    Minimizes the negative log-likelihood using scipy.optimize.minimize,
    then computes standard errors via numerical Hessian.
    """

    def fit(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "SLSQP",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        args = [model, starting_values, variance_targeting, optimizer, maxiter, disp]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMLEstimatorǁfit__mutmut_orig"),
            object.__getattribute__(self, "xǁMLEstimatorǁfit__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMLEstimatorǁfit__mutmut_orig(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "SLSQP",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(model.endog)

        if starting_values is not None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                model,
                x0_constrained,
                backcast,
                optimizer,
                maxiter,
                disp,
            )
        return self._fit_standard(
            model,
            x0_constrained,
            backcast,
            optimizer,
            maxiter,
            disp,
        )

    def xǁMLEstimatorǁfit__mutmut_1(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = True,
        optimizer: str = "SLSQP",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(model.endog)

        if starting_values is not None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                model,
                x0_constrained,
                backcast,
                optimizer,
                maxiter,
                disp,
            )
        return self._fit_standard(
            model,
            x0_constrained,
            backcast,
            optimizer,
            maxiter,
            disp,
        )

    def xǁMLEstimatorǁfit__mutmut_2(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "XXSLSQPXX",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(model.endog)

        if starting_values is not None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                model,
                x0_constrained,
                backcast,
                optimizer,
                maxiter,
                disp,
            )
        return self._fit_standard(
            model,
            x0_constrained,
            backcast,
            optimizer,
            maxiter,
            disp,
        )

    def xǁMLEstimatorǁfit__mutmut_3(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "slsqp",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(model.endog)

        if starting_values is not None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                model,
                x0_constrained,
                backcast,
                optimizer,
                maxiter,
                disp,
            )
        return self._fit_standard(
            model,
            x0_constrained,
            backcast,
            optimizer,
            maxiter,
            disp,
        )

    def xǁMLEstimatorǁfit__mutmut_4(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "SLSQP",
        maxiter: int = 501,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(model.endog)

        if starting_values is not None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                model,
                x0_constrained,
                backcast,
                optimizer,
                maxiter,
                disp,
            )
        return self._fit_standard(
            model,
            x0_constrained,
            backcast,
            optimizer,
            maxiter,
            disp,
        )

    def xǁMLEstimatorǁfit__mutmut_5(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "SLSQP",
        maxiter: int = 500,
        disp: bool = False,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(model.endog)

        if starting_values is not None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                model,
                x0_constrained,
                backcast,
                optimizer,
                maxiter,
                disp,
            )
        return self._fit_standard(
            model,
            x0_constrained,
            backcast,
            optimizer,
            maxiter,
            disp,
        )

    def xǁMLEstimatorǁfit__mutmut_6(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "SLSQP",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = None

        if starting_values is not None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                model,
                x0_constrained,
                backcast,
                optimizer,
                maxiter,
                disp,
            )
        return self._fit_standard(
            model,
            x0_constrained,
            backcast,
            optimizer,
            maxiter,
            disp,
        )

    def xǁMLEstimatorǁfit__mutmut_7(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "SLSQP",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(None)

        if starting_values is not None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                model,
                x0_constrained,
                backcast,
                optimizer,
                maxiter,
                disp,
            )
        return self._fit_standard(
            model,
            x0_constrained,
            backcast,
            optimizer,
            maxiter,
            disp,
        )

    def xǁMLEstimatorǁfit__mutmut_8(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "SLSQP",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(model.endog)

        if starting_values is None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                model,
                x0_constrained,
                backcast,
                optimizer,
                maxiter,
                disp,
            )
        return self._fit_standard(
            model,
            x0_constrained,
            backcast,
            optimizer,
            maxiter,
            disp,
        )

    def xǁMLEstimatorǁfit__mutmut_9(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "SLSQP",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(model.endog)

        if starting_values is not None:
            x0_constrained = None
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                model,
                x0_constrained,
                backcast,
                optimizer,
                maxiter,
                disp,
            )
        return self._fit_standard(
            model,
            x0_constrained,
            backcast,
            optimizer,
            maxiter,
            disp,
        )

    def xǁMLEstimatorǁfit__mutmut_10(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "SLSQP",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(model.endog)

        if starting_values is not None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = None

        if variance_targeting:
            return self._fit_with_targeting(
                model,
                x0_constrained,
                backcast,
                optimizer,
                maxiter,
                disp,
            )
        return self._fit_standard(
            model,
            x0_constrained,
            backcast,
            optimizer,
            maxiter,
            disp,
        )

    def xǁMLEstimatorǁfit__mutmut_11(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "SLSQP",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(model.endog)

        if starting_values is not None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                None,
                x0_constrained,
                backcast,
                optimizer,
                maxiter,
                disp,
            )
        return self._fit_standard(
            model,
            x0_constrained,
            backcast,
            optimizer,
            maxiter,
            disp,
        )

    def xǁMLEstimatorǁfit__mutmut_12(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "SLSQP",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(model.endog)

        if starting_values is not None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                model,
                None,
                backcast,
                optimizer,
                maxiter,
                disp,
            )
        return self._fit_standard(
            model,
            x0_constrained,
            backcast,
            optimizer,
            maxiter,
            disp,
        )

    def xǁMLEstimatorǁfit__mutmut_13(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "SLSQP",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(model.endog)

        if starting_values is not None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                model,
                x0_constrained,
                None,
                optimizer,
                maxiter,
                disp,
            )
        return self._fit_standard(
            model,
            x0_constrained,
            backcast,
            optimizer,
            maxiter,
            disp,
        )

    def xǁMLEstimatorǁfit__mutmut_14(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "SLSQP",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(model.endog)

        if starting_values is not None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                model,
                x0_constrained,
                backcast,
                None,
                maxiter,
                disp,
            )
        return self._fit_standard(
            model,
            x0_constrained,
            backcast,
            optimizer,
            maxiter,
            disp,
        )

    def xǁMLEstimatorǁfit__mutmut_15(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "SLSQP",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(model.endog)

        if starting_values is not None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                model,
                x0_constrained,
                backcast,
                optimizer,
                None,
                disp,
            )
        return self._fit_standard(
            model,
            x0_constrained,
            backcast,
            optimizer,
            maxiter,
            disp,
        )

    def xǁMLEstimatorǁfit__mutmut_16(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "SLSQP",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(model.endog)

        if starting_values is not None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                model,
                x0_constrained,
                backcast,
                optimizer,
                maxiter,
                None,
            )
        return self._fit_standard(
            model,
            x0_constrained,
            backcast,
            optimizer,
            maxiter,
            disp,
        )

    def xǁMLEstimatorǁfit__mutmut_17(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "SLSQP",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(model.endog)

        if starting_values is not None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                x0_constrained,
                backcast,
                optimizer,
                maxiter,
                disp,
            )
        return self._fit_standard(
            model,
            x0_constrained,
            backcast,
            optimizer,
            maxiter,
            disp,
        )

    def xǁMLEstimatorǁfit__mutmut_18(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "SLSQP",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(model.endog)

        if starting_values is not None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                model,
                backcast,
                optimizer,
                maxiter,
                disp,
            )
        return self._fit_standard(
            model,
            x0_constrained,
            backcast,
            optimizer,
            maxiter,
            disp,
        )

    def xǁMLEstimatorǁfit__mutmut_19(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "SLSQP",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(model.endog)

        if starting_values is not None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                model,
                x0_constrained,
                optimizer,
                maxiter,
                disp,
            )
        return self._fit_standard(
            model,
            x0_constrained,
            backcast,
            optimizer,
            maxiter,
            disp,
        )

    def xǁMLEstimatorǁfit__mutmut_20(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "SLSQP",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(model.endog)

        if starting_values is not None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                model,
                x0_constrained,
                backcast,
                maxiter,
                disp,
            )
        return self._fit_standard(
            model,
            x0_constrained,
            backcast,
            optimizer,
            maxiter,
            disp,
        )

    def xǁMLEstimatorǁfit__mutmut_21(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "SLSQP",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(model.endog)

        if starting_values is not None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                model,
                x0_constrained,
                backcast,
                optimizer,
                disp,
            )
        return self._fit_standard(
            model,
            x0_constrained,
            backcast,
            optimizer,
            maxiter,
            disp,
        )

    def xǁMLEstimatorǁfit__mutmut_22(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "SLSQP",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(model.endog)

        if starting_values is not None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                model,
                x0_constrained,
                backcast,
                optimizer,
                maxiter,
            )
        return self._fit_standard(
            model,
            x0_constrained,
            backcast,
            optimizer,
            maxiter,
            disp,
        )

    def xǁMLEstimatorǁfit__mutmut_23(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "SLSQP",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(model.endog)

        if starting_values is not None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                model,
                x0_constrained,
                backcast,
                optimizer,
                maxiter,
                disp,
            )
        return self._fit_standard(
            None,
            x0_constrained,
            backcast,
            optimizer,
            maxiter,
            disp,
        )

    def xǁMLEstimatorǁfit__mutmut_24(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "SLSQP",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(model.endog)

        if starting_values is not None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                model,
                x0_constrained,
                backcast,
                optimizer,
                maxiter,
                disp,
            )
        return self._fit_standard(
            model,
            None,
            backcast,
            optimizer,
            maxiter,
            disp,
        )

    def xǁMLEstimatorǁfit__mutmut_25(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "SLSQP",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(model.endog)

        if starting_values is not None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                model,
                x0_constrained,
                backcast,
                optimizer,
                maxiter,
                disp,
            )
        return self._fit_standard(
            model,
            x0_constrained,
            None,
            optimizer,
            maxiter,
            disp,
        )

    def xǁMLEstimatorǁfit__mutmut_26(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "SLSQP",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(model.endog)

        if starting_values is not None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                model,
                x0_constrained,
                backcast,
                optimizer,
                maxiter,
                disp,
            )
        return self._fit_standard(
            model,
            x0_constrained,
            backcast,
            None,
            maxiter,
            disp,
        )

    def xǁMLEstimatorǁfit__mutmut_27(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "SLSQP",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(model.endog)

        if starting_values is not None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                model,
                x0_constrained,
                backcast,
                optimizer,
                maxiter,
                disp,
            )
        return self._fit_standard(
            model,
            x0_constrained,
            backcast,
            optimizer,
            None,
            disp,
        )

    def xǁMLEstimatorǁfit__mutmut_28(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "SLSQP",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(model.endog)

        if starting_values is not None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                model,
                x0_constrained,
                backcast,
                optimizer,
                maxiter,
                disp,
            )
        return self._fit_standard(
            model,
            x0_constrained,
            backcast,
            optimizer,
            maxiter,
            None,
        )

    def xǁMLEstimatorǁfit__mutmut_29(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "SLSQP",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(model.endog)

        if starting_values is not None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                model,
                x0_constrained,
                backcast,
                optimizer,
                maxiter,
                disp,
            )
        return self._fit_standard(
            x0_constrained,
            backcast,
            optimizer,
            maxiter,
            disp,
        )

    def xǁMLEstimatorǁfit__mutmut_30(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "SLSQP",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(model.endog)

        if starting_values is not None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                model,
                x0_constrained,
                backcast,
                optimizer,
                maxiter,
                disp,
            )
        return self._fit_standard(
            model,
            backcast,
            optimizer,
            maxiter,
            disp,
        )

    def xǁMLEstimatorǁfit__mutmut_31(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "SLSQP",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(model.endog)

        if starting_values is not None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                model,
                x0_constrained,
                backcast,
                optimizer,
                maxiter,
                disp,
            )
        return self._fit_standard(
            model,
            x0_constrained,
            optimizer,
            maxiter,
            disp,
        )

    def xǁMLEstimatorǁfit__mutmut_32(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "SLSQP",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(model.endog)

        if starting_values is not None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                model,
                x0_constrained,
                backcast,
                optimizer,
                maxiter,
                disp,
            )
        return self._fit_standard(
            model,
            x0_constrained,
            backcast,
            maxiter,
            disp,
        )

    def xǁMLEstimatorǁfit__mutmut_33(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "SLSQP",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(model.endog)

        if starting_values is not None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                model,
                x0_constrained,
                backcast,
                optimizer,
                maxiter,
                disp,
            )
        return self._fit_standard(
            model,
            x0_constrained,
            backcast,
            optimizer,
            disp,
        )

    def xǁMLEstimatorǁfit__mutmut_34(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "SLSQP",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(model.endog)

        if starting_values is not None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                model,
                x0_constrained,
                backcast,
                optimizer,
                maxiter,
                disp,
            )
        return self._fit_standard(
            model,
            x0_constrained,
            backcast,
            optimizer,
            maxiter,
        )

    xǁMLEstimatorǁfit__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMLEstimatorǁfit__mutmut_1": xǁMLEstimatorǁfit__mutmut_1,
        "xǁMLEstimatorǁfit__mutmut_2": xǁMLEstimatorǁfit__mutmut_2,
        "xǁMLEstimatorǁfit__mutmut_3": xǁMLEstimatorǁfit__mutmut_3,
        "xǁMLEstimatorǁfit__mutmut_4": xǁMLEstimatorǁfit__mutmut_4,
        "xǁMLEstimatorǁfit__mutmut_5": xǁMLEstimatorǁfit__mutmut_5,
        "xǁMLEstimatorǁfit__mutmut_6": xǁMLEstimatorǁfit__mutmut_6,
        "xǁMLEstimatorǁfit__mutmut_7": xǁMLEstimatorǁfit__mutmut_7,
        "xǁMLEstimatorǁfit__mutmut_8": xǁMLEstimatorǁfit__mutmut_8,
        "xǁMLEstimatorǁfit__mutmut_9": xǁMLEstimatorǁfit__mutmut_9,
        "xǁMLEstimatorǁfit__mutmut_10": xǁMLEstimatorǁfit__mutmut_10,
        "xǁMLEstimatorǁfit__mutmut_11": xǁMLEstimatorǁfit__mutmut_11,
        "xǁMLEstimatorǁfit__mutmut_12": xǁMLEstimatorǁfit__mutmut_12,
        "xǁMLEstimatorǁfit__mutmut_13": xǁMLEstimatorǁfit__mutmut_13,
        "xǁMLEstimatorǁfit__mutmut_14": xǁMLEstimatorǁfit__mutmut_14,
        "xǁMLEstimatorǁfit__mutmut_15": xǁMLEstimatorǁfit__mutmut_15,
        "xǁMLEstimatorǁfit__mutmut_16": xǁMLEstimatorǁfit__mutmut_16,
        "xǁMLEstimatorǁfit__mutmut_17": xǁMLEstimatorǁfit__mutmut_17,
        "xǁMLEstimatorǁfit__mutmut_18": xǁMLEstimatorǁfit__mutmut_18,
        "xǁMLEstimatorǁfit__mutmut_19": xǁMLEstimatorǁfit__mutmut_19,
        "xǁMLEstimatorǁfit__mutmut_20": xǁMLEstimatorǁfit__mutmut_20,
        "xǁMLEstimatorǁfit__mutmut_21": xǁMLEstimatorǁfit__mutmut_21,
        "xǁMLEstimatorǁfit__mutmut_22": xǁMLEstimatorǁfit__mutmut_22,
        "xǁMLEstimatorǁfit__mutmut_23": xǁMLEstimatorǁfit__mutmut_23,
        "xǁMLEstimatorǁfit__mutmut_24": xǁMLEstimatorǁfit__mutmut_24,
        "xǁMLEstimatorǁfit__mutmut_25": xǁMLEstimatorǁfit__mutmut_25,
        "xǁMLEstimatorǁfit__mutmut_26": xǁMLEstimatorǁfit__mutmut_26,
        "xǁMLEstimatorǁfit__mutmut_27": xǁMLEstimatorǁfit__mutmut_27,
        "xǁMLEstimatorǁfit__mutmut_28": xǁMLEstimatorǁfit__mutmut_28,
        "xǁMLEstimatorǁfit__mutmut_29": xǁMLEstimatorǁfit__mutmut_29,
        "xǁMLEstimatorǁfit__mutmut_30": xǁMLEstimatorǁfit__mutmut_30,
        "xǁMLEstimatorǁfit__mutmut_31": xǁMLEstimatorǁfit__mutmut_31,
        "xǁMLEstimatorǁfit__mutmut_32": xǁMLEstimatorǁfit__mutmut_32,
        "xǁMLEstimatorǁfit__mutmut_33": xǁMLEstimatorǁfit__mutmut_33,
        "xǁMLEstimatorǁfit__mutmut_34": xǁMLEstimatorǁfit__mutmut_34,
    }
    xǁMLEstimatorǁfit__mutmut_orig.__name__ = "xǁMLEstimatorǁfit"

    def _fit_standard(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        args = [model, x0_constrained, backcast, optimizer, maxiter, disp]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMLEstimatorǁ_fit_standard__mutmut_orig"),
            object.__getattribute__(self, "xǁMLEstimatorǁ_fit_standard__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_orig(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_1(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = None

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_2(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(None)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_3(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = None
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_4(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(None)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_5(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = None
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_6(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(None, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_7(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, None)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_8(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_9(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(
                constrained,
            )
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_10(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return +ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_11(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = None

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_12(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            None,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_13(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            None,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_14(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=None,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_15(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options=None,
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_16(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_17(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_18(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_19(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_20(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"XXmaxiterXX": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_21(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"MAXITER": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_22(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "XXdispXX": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_23(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "DISP": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_24(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "XXftolXX": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_25(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "FTOL": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_26(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1.0000000001},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_27(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_28(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning(None, result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_29(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", None)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_30(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning(result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_31(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning(
                "Optimization did not converge: %s",
            )

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_32(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("XXOptimization did not converge: %sXX", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_33(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_34(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("OPTIMIZATION DID NOT CONVERGE: %S", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_35(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = None
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_36(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(None)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_37(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = None

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_38(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = +result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_39(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = None
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_40(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(None, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_41(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, None, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_42(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, None)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_43(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_44(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_45(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(
            params_opt,
            model.endog,
        )
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_46(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = None

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_47(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(None, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_48(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, None)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_49(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_50(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(
            sigma2,
        )

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_51(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1.000000000001)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_52(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = None

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_53(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            None,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_54(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            None,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_55(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            None,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_56(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_57(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_58(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_59(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=None,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_60(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=None,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_61(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=None,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_62(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=None,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_63(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=None,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_64(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=None,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_65(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=None,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_66(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_67(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_68(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_69(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_70(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_71(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_standard__mutmut_72(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
        )

    xǁMLEstimatorǁ_fit_standard__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMLEstimatorǁ_fit_standard__mutmut_1": xǁMLEstimatorǁ_fit_standard__mutmut_1,
        "xǁMLEstimatorǁ_fit_standard__mutmut_2": xǁMLEstimatorǁ_fit_standard__mutmut_2,
        "xǁMLEstimatorǁ_fit_standard__mutmut_3": xǁMLEstimatorǁ_fit_standard__mutmut_3,
        "xǁMLEstimatorǁ_fit_standard__mutmut_4": xǁMLEstimatorǁ_fit_standard__mutmut_4,
        "xǁMLEstimatorǁ_fit_standard__mutmut_5": xǁMLEstimatorǁ_fit_standard__mutmut_5,
        "xǁMLEstimatorǁ_fit_standard__mutmut_6": xǁMLEstimatorǁ_fit_standard__mutmut_6,
        "xǁMLEstimatorǁ_fit_standard__mutmut_7": xǁMLEstimatorǁ_fit_standard__mutmut_7,
        "xǁMLEstimatorǁ_fit_standard__mutmut_8": xǁMLEstimatorǁ_fit_standard__mutmut_8,
        "xǁMLEstimatorǁ_fit_standard__mutmut_9": xǁMLEstimatorǁ_fit_standard__mutmut_9,
        "xǁMLEstimatorǁ_fit_standard__mutmut_10": xǁMLEstimatorǁ_fit_standard__mutmut_10,
        "xǁMLEstimatorǁ_fit_standard__mutmut_11": xǁMLEstimatorǁ_fit_standard__mutmut_11,
        "xǁMLEstimatorǁ_fit_standard__mutmut_12": xǁMLEstimatorǁ_fit_standard__mutmut_12,
        "xǁMLEstimatorǁ_fit_standard__mutmut_13": xǁMLEstimatorǁ_fit_standard__mutmut_13,
        "xǁMLEstimatorǁ_fit_standard__mutmut_14": xǁMLEstimatorǁ_fit_standard__mutmut_14,
        "xǁMLEstimatorǁ_fit_standard__mutmut_15": xǁMLEstimatorǁ_fit_standard__mutmut_15,
        "xǁMLEstimatorǁ_fit_standard__mutmut_16": xǁMLEstimatorǁ_fit_standard__mutmut_16,
        "xǁMLEstimatorǁ_fit_standard__mutmut_17": xǁMLEstimatorǁ_fit_standard__mutmut_17,
        "xǁMLEstimatorǁ_fit_standard__mutmut_18": xǁMLEstimatorǁ_fit_standard__mutmut_18,
        "xǁMLEstimatorǁ_fit_standard__mutmut_19": xǁMLEstimatorǁ_fit_standard__mutmut_19,
        "xǁMLEstimatorǁ_fit_standard__mutmut_20": xǁMLEstimatorǁ_fit_standard__mutmut_20,
        "xǁMLEstimatorǁ_fit_standard__mutmut_21": xǁMLEstimatorǁ_fit_standard__mutmut_21,
        "xǁMLEstimatorǁ_fit_standard__mutmut_22": xǁMLEstimatorǁ_fit_standard__mutmut_22,
        "xǁMLEstimatorǁ_fit_standard__mutmut_23": xǁMLEstimatorǁ_fit_standard__mutmut_23,
        "xǁMLEstimatorǁ_fit_standard__mutmut_24": xǁMLEstimatorǁ_fit_standard__mutmut_24,
        "xǁMLEstimatorǁ_fit_standard__mutmut_25": xǁMLEstimatorǁ_fit_standard__mutmut_25,
        "xǁMLEstimatorǁ_fit_standard__mutmut_26": xǁMLEstimatorǁ_fit_standard__mutmut_26,
        "xǁMLEstimatorǁ_fit_standard__mutmut_27": xǁMLEstimatorǁ_fit_standard__mutmut_27,
        "xǁMLEstimatorǁ_fit_standard__mutmut_28": xǁMLEstimatorǁ_fit_standard__mutmut_28,
        "xǁMLEstimatorǁ_fit_standard__mutmut_29": xǁMLEstimatorǁ_fit_standard__mutmut_29,
        "xǁMLEstimatorǁ_fit_standard__mutmut_30": xǁMLEstimatorǁ_fit_standard__mutmut_30,
        "xǁMLEstimatorǁ_fit_standard__mutmut_31": xǁMLEstimatorǁ_fit_standard__mutmut_31,
        "xǁMLEstimatorǁ_fit_standard__mutmut_32": xǁMLEstimatorǁ_fit_standard__mutmut_32,
        "xǁMLEstimatorǁ_fit_standard__mutmut_33": xǁMLEstimatorǁ_fit_standard__mutmut_33,
        "xǁMLEstimatorǁ_fit_standard__mutmut_34": xǁMLEstimatorǁ_fit_standard__mutmut_34,
        "xǁMLEstimatorǁ_fit_standard__mutmut_35": xǁMLEstimatorǁ_fit_standard__mutmut_35,
        "xǁMLEstimatorǁ_fit_standard__mutmut_36": xǁMLEstimatorǁ_fit_standard__mutmut_36,
        "xǁMLEstimatorǁ_fit_standard__mutmut_37": xǁMLEstimatorǁ_fit_standard__mutmut_37,
        "xǁMLEstimatorǁ_fit_standard__mutmut_38": xǁMLEstimatorǁ_fit_standard__mutmut_38,
        "xǁMLEstimatorǁ_fit_standard__mutmut_39": xǁMLEstimatorǁ_fit_standard__mutmut_39,
        "xǁMLEstimatorǁ_fit_standard__mutmut_40": xǁMLEstimatorǁ_fit_standard__mutmut_40,
        "xǁMLEstimatorǁ_fit_standard__mutmut_41": xǁMLEstimatorǁ_fit_standard__mutmut_41,
        "xǁMLEstimatorǁ_fit_standard__mutmut_42": xǁMLEstimatorǁ_fit_standard__mutmut_42,
        "xǁMLEstimatorǁ_fit_standard__mutmut_43": xǁMLEstimatorǁ_fit_standard__mutmut_43,
        "xǁMLEstimatorǁ_fit_standard__mutmut_44": xǁMLEstimatorǁ_fit_standard__mutmut_44,
        "xǁMLEstimatorǁ_fit_standard__mutmut_45": xǁMLEstimatorǁ_fit_standard__mutmut_45,
        "xǁMLEstimatorǁ_fit_standard__mutmut_46": xǁMLEstimatorǁ_fit_standard__mutmut_46,
        "xǁMLEstimatorǁ_fit_standard__mutmut_47": xǁMLEstimatorǁ_fit_standard__mutmut_47,
        "xǁMLEstimatorǁ_fit_standard__mutmut_48": xǁMLEstimatorǁ_fit_standard__mutmut_48,
        "xǁMLEstimatorǁ_fit_standard__mutmut_49": xǁMLEstimatorǁ_fit_standard__mutmut_49,
        "xǁMLEstimatorǁ_fit_standard__mutmut_50": xǁMLEstimatorǁ_fit_standard__mutmut_50,
        "xǁMLEstimatorǁ_fit_standard__mutmut_51": xǁMLEstimatorǁ_fit_standard__mutmut_51,
        "xǁMLEstimatorǁ_fit_standard__mutmut_52": xǁMLEstimatorǁ_fit_standard__mutmut_52,
        "xǁMLEstimatorǁ_fit_standard__mutmut_53": xǁMLEstimatorǁ_fit_standard__mutmut_53,
        "xǁMLEstimatorǁ_fit_standard__mutmut_54": xǁMLEstimatorǁ_fit_standard__mutmut_54,
        "xǁMLEstimatorǁ_fit_standard__mutmut_55": xǁMLEstimatorǁ_fit_standard__mutmut_55,
        "xǁMLEstimatorǁ_fit_standard__mutmut_56": xǁMLEstimatorǁ_fit_standard__mutmut_56,
        "xǁMLEstimatorǁ_fit_standard__mutmut_57": xǁMLEstimatorǁ_fit_standard__mutmut_57,
        "xǁMLEstimatorǁ_fit_standard__mutmut_58": xǁMLEstimatorǁ_fit_standard__mutmut_58,
        "xǁMLEstimatorǁ_fit_standard__mutmut_59": xǁMLEstimatorǁ_fit_standard__mutmut_59,
        "xǁMLEstimatorǁ_fit_standard__mutmut_60": xǁMLEstimatorǁ_fit_standard__mutmut_60,
        "xǁMLEstimatorǁ_fit_standard__mutmut_61": xǁMLEstimatorǁ_fit_standard__mutmut_61,
        "xǁMLEstimatorǁ_fit_standard__mutmut_62": xǁMLEstimatorǁ_fit_standard__mutmut_62,
        "xǁMLEstimatorǁ_fit_standard__mutmut_63": xǁMLEstimatorǁ_fit_standard__mutmut_63,
        "xǁMLEstimatorǁ_fit_standard__mutmut_64": xǁMLEstimatorǁ_fit_standard__mutmut_64,
        "xǁMLEstimatorǁ_fit_standard__mutmut_65": xǁMLEstimatorǁ_fit_standard__mutmut_65,
        "xǁMLEstimatorǁ_fit_standard__mutmut_66": xǁMLEstimatorǁ_fit_standard__mutmut_66,
        "xǁMLEstimatorǁ_fit_standard__mutmut_67": xǁMLEstimatorǁ_fit_standard__mutmut_67,
        "xǁMLEstimatorǁ_fit_standard__mutmut_68": xǁMLEstimatorǁ_fit_standard__mutmut_68,
        "xǁMLEstimatorǁ_fit_standard__mutmut_69": xǁMLEstimatorǁ_fit_standard__mutmut_69,
        "xǁMLEstimatorǁ_fit_standard__mutmut_70": xǁMLEstimatorǁ_fit_standard__mutmut_70,
        "xǁMLEstimatorǁ_fit_standard__mutmut_71": xǁMLEstimatorǁ_fit_standard__mutmut_71,
        "xǁMLEstimatorǁ_fit_standard__mutmut_72": xǁMLEstimatorǁ_fit_standard__mutmut_72,
    }
    xǁMLEstimatorǁ_fit_standard__mutmut_orig.__name__ = "xǁMLEstimatorǁ_fit_standard"

    def _fit_with_targeting(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        args = [model, x0_constrained, backcast, optimizer, maxiter, disp]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMLEstimatorǁ_fit_with_targeting__mutmut_orig"),
            object.__getattribute__(self, "xǁMLEstimatorǁ_fit_with_targeting__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_orig(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_1(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = None

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_2(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(None)

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_3(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(None))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_4(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = None
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_5(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[2:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_6(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = None  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_7(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(None)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_8(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = None
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_9(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(None)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_10(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = None
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_11(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(None)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_12(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence > 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_13(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 1.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_14(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 10000000001.0
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_15(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = None
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_16(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var / (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_17(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 + persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_18(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (2.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_19(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega < 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_20(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 1:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_21(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 10000000001.0
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_22(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = None
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_23(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate(None)
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_24(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = None
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_25(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(None, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_26(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, None)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_27(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_28(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(
                full_params,
            )
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_29(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return +ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_30(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = None

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_31(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            None,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_32(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            None,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_33(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=None,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_34(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options=None,
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_35(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_36(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_37(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_38(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_39(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"XXmaxiterXX": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_40(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"MAXITER": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_41(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "XXdispXX": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_42(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "DISP": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_43(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "XXftolXX": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_44(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "FTOL": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_45(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1.0000000001},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_46(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_47(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning(None, result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_48(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", None)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_49(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning(result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_50(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning(
                "Optimization did not converge: %s",
            )

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_51(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("XXOptimization did not converge: %sXX", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_52(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_53(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("OPTIMIZATION DID NOT CONVERGE: %S", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_54(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = None
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_55(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(None)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_56(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = None
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_57(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(None)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_58(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = None
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_59(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var / (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_60(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 + persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_61(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (2.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_62(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = None
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_63(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate(None)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_64(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = None

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_65(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = +result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_66(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = None
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_67(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(None, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_68(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, None, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_69(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, None)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_70(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_71(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_72(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(
            params_opt,
            model.endog,
        )
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_73(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = None

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_74(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(None, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_75(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, None)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_76(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_77(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(
            sigma2,
        )

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_78(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1.000000000001)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_79(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = None

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_80(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            None,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_81(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            None,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_82(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            None,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_83(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_84(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_85(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_86(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=None,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_87(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=None,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_88(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=None,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_89(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=None,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_90(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=None,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_91(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=None,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_92(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=None,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_93(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_94(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_95(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_96(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_97(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_98(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            convergence=result.success,
        )

    def xǁMLEstimatorǁ_fit_with_targeting__mutmut_99(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
        )

    xǁMLEstimatorǁ_fit_with_targeting__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_1": xǁMLEstimatorǁ_fit_with_targeting__mutmut_1,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_2": xǁMLEstimatorǁ_fit_with_targeting__mutmut_2,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_3": xǁMLEstimatorǁ_fit_with_targeting__mutmut_3,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_4": xǁMLEstimatorǁ_fit_with_targeting__mutmut_4,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_5": xǁMLEstimatorǁ_fit_with_targeting__mutmut_5,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_6": xǁMLEstimatorǁ_fit_with_targeting__mutmut_6,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_7": xǁMLEstimatorǁ_fit_with_targeting__mutmut_7,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_8": xǁMLEstimatorǁ_fit_with_targeting__mutmut_8,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_9": xǁMLEstimatorǁ_fit_with_targeting__mutmut_9,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_10": xǁMLEstimatorǁ_fit_with_targeting__mutmut_10,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_11": xǁMLEstimatorǁ_fit_with_targeting__mutmut_11,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_12": xǁMLEstimatorǁ_fit_with_targeting__mutmut_12,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_13": xǁMLEstimatorǁ_fit_with_targeting__mutmut_13,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_14": xǁMLEstimatorǁ_fit_with_targeting__mutmut_14,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_15": xǁMLEstimatorǁ_fit_with_targeting__mutmut_15,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_16": xǁMLEstimatorǁ_fit_with_targeting__mutmut_16,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_17": xǁMLEstimatorǁ_fit_with_targeting__mutmut_17,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_18": xǁMLEstimatorǁ_fit_with_targeting__mutmut_18,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_19": xǁMLEstimatorǁ_fit_with_targeting__mutmut_19,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_20": xǁMLEstimatorǁ_fit_with_targeting__mutmut_20,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_21": xǁMLEstimatorǁ_fit_with_targeting__mutmut_21,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_22": xǁMLEstimatorǁ_fit_with_targeting__mutmut_22,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_23": xǁMLEstimatorǁ_fit_with_targeting__mutmut_23,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_24": xǁMLEstimatorǁ_fit_with_targeting__mutmut_24,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_25": xǁMLEstimatorǁ_fit_with_targeting__mutmut_25,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_26": xǁMLEstimatorǁ_fit_with_targeting__mutmut_26,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_27": xǁMLEstimatorǁ_fit_with_targeting__mutmut_27,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_28": xǁMLEstimatorǁ_fit_with_targeting__mutmut_28,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_29": xǁMLEstimatorǁ_fit_with_targeting__mutmut_29,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_30": xǁMLEstimatorǁ_fit_with_targeting__mutmut_30,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_31": xǁMLEstimatorǁ_fit_with_targeting__mutmut_31,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_32": xǁMLEstimatorǁ_fit_with_targeting__mutmut_32,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_33": xǁMLEstimatorǁ_fit_with_targeting__mutmut_33,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_34": xǁMLEstimatorǁ_fit_with_targeting__mutmut_34,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_35": xǁMLEstimatorǁ_fit_with_targeting__mutmut_35,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_36": xǁMLEstimatorǁ_fit_with_targeting__mutmut_36,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_37": xǁMLEstimatorǁ_fit_with_targeting__mutmut_37,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_38": xǁMLEstimatorǁ_fit_with_targeting__mutmut_38,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_39": xǁMLEstimatorǁ_fit_with_targeting__mutmut_39,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_40": xǁMLEstimatorǁ_fit_with_targeting__mutmut_40,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_41": xǁMLEstimatorǁ_fit_with_targeting__mutmut_41,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_42": xǁMLEstimatorǁ_fit_with_targeting__mutmut_42,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_43": xǁMLEstimatorǁ_fit_with_targeting__mutmut_43,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_44": xǁMLEstimatorǁ_fit_with_targeting__mutmut_44,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_45": xǁMLEstimatorǁ_fit_with_targeting__mutmut_45,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_46": xǁMLEstimatorǁ_fit_with_targeting__mutmut_46,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_47": xǁMLEstimatorǁ_fit_with_targeting__mutmut_47,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_48": xǁMLEstimatorǁ_fit_with_targeting__mutmut_48,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_49": xǁMLEstimatorǁ_fit_with_targeting__mutmut_49,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_50": xǁMLEstimatorǁ_fit_with_targeting__mutmut_50,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_51": xǁMLEstimatorǁ_fit_with_targeting__mutmut_51,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_52": xǁMLEstimatorǁ_fit_with_targeting__mutmut_52,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_53": xǁMLEstimatorǁ_fit_with_targeting__mutmut_53,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_54": xǁMLEstimatorǁ_fit_with_targeting__mutmut_54,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_55": xǁMLEstimatorǁ_fit_with_targeting__mutmut_55,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_56": xǁMLEstimatorǁ_fit_with_targeting__mutmut_56,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_57": xǁMLEstimatorǁ_fit_with_targeting__mutmut_57,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_58": xǁMLEstimatorǁ_fit_with_targeting__mutmut_58,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_59": xǁMLEstimatorǁ_fit_with_targeting__mutmut_59,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_60": xǁMLEstimatorǁ_fit_with_targeting__mutmut_60,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_61": xǁMLEstimatorǁ_fit_with_targeting__mutmut_61,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_62": xǁMLEstimatorǁ_fit_with_targeting__mutmut_62,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_63": xǁMLEstimatorǁ_fit_with_targeting__mutmut_63,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_64": xǁMLEstimatorǁ_fit_with_targeting__mutmut_64,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_65": xǁMLEstimatorǁ_fit_with_targeting__mutmut_65,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_66": xǁMLEstimatorǁ_fit_with_targeting__mutmut_66,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_67": xǁMLEstimatorǁ_fit_with_targeting__mutmut_67,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_68": xǁMLEstimatorǁ_fit_with_targeting__mutmut_68,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_69": xǁMLEstimatorǁ_fit_with_targeting__mutmut_69,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_70": xǁMLEstimatorǁ_fit_with_targeting__mutmut_70,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_71": xǁMLEstimatorǁ_fit_with_targeting__mutmut_71,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_72": xǁMLEstimatorǁ_fit_with_targeting__mutmut_72,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_73": xǁMLEstimatorǁ_fit_with_targeting__mutmut_73,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_74": xǁMLEstimatorǁ_fit_with_targeting__mutmut_74,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_75": xǁMLEstimatorǁ_fit_with_targeting__mutmut_75,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_76": xǁMLEstimatorǁ_fit_with_targeting__mutmut_76,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_77": xǁMLEstimatorǁ_fit_with_targeting__mutmut_77,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_78": xǁMLEstimatorǁ_fit_with_targeting__mutmut_78,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_79": xǁMLEstimatorǁ_fit_with_targeting__mutmut_79,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_80": xǁMLEstimatorǁ_fit_with_targeting__mutmut_80,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_81": xǁMLEstimatorǁ_fit_with_targeting__mutmut_81,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_82": xǁMLEstimatorǁ_fit_with_targeting__mutmut_82,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_83": xǁMLEstimatorǁ_fit_with_targeting__mutmut_83,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_84": xǁMLEstimatorǁ_fit_with_targeting__mutmut_84,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_85": xǁMLEstimatorǁ_fit_with_targeting__mutmut_85,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_86": xǁMLEstimatorǁ_fit_with_targeting__mutmut_86,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_87": xǁMLEstimatorǁ_fit_with_targeting__mutmut_87,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_88": xǁMLEstimatorǁ_fit_with_targeting__mutmut_88,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_89": xǁMLEstimatorǁ_fit_with_targeting__mutmut_89,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_90": xǁMLEstimatorǁ_fit_with_targeting__mutmut_90,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_91": xǁMLEstimatorǁ_fit_with_targeting__mutmut_91,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_92": xǁMLEstimatorǁ_fit_with_targeting__mutmut_92,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_93": xǁMLEstimatorǁ_fit_with_targeting__mutmut_93,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_94": xǁMLEstimatorǁ_fit_with_targeting__mutmut_94,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_95": xǁMLEstimatorǁ_fit_with_targeting__mutmut_95,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_96": xǁMLEstimatorǁ_fit_with_targeting__mutmut_96,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_97": xǁMLEstimatorǁ_fit_with_targeting__mutmut_97,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_98": xǁMLEstimatorǁ_fit_with_targeting__mutmut_98,
        "xǁMLEstimatorǁ_fit_with_targeting__mutmut_99": xǁMLEstimatorǁ_fit_with_targeting__mutmut_99,
    }
    xǁMLEstimatorǁ_fit_with_targeting__mutmut_orig.__name__ = "xǁMLEstimatorǁ_fit_with_targeting"

    def _compute_standard_errors(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        args = [model, params, backcast]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMLEstimatorǁ_compute_standard_errors__mutmut_orig"),
            object.__getattribute__(self, "xǁMLEstimatorǁ_compute_standard_errors__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_orig(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_1(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = None

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_2(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = None
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_3(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(None, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_4(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, None, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_5(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, None)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_6(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_7(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_8(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(
                model,
                params,
            )
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_9(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = None

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_10(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(None)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_11(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = None

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_12(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(None)

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_13(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(None))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_14(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(None)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_15(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = None
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_16(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(None, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_17(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, None, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_18(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, None)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_19(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_20(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_21(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(
                model,
                params,
            )
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_22(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = None
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_23(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = None

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_24(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(None)

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_25(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(None))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_26(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(None)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_27(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning(None)
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_28(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("XXFailed to compute standard errors, using fallbackXX")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_29(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_30(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("FAILED TO COMPUTE STANDARD ERRORS, USING FALLBACK")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_31(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = None
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_32(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(None, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_33(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, None)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_34(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_35(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(
                k,
            )
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_36(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = None

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_37(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(None, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_38(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, None)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_39(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_40(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(
                k,
            )

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_41(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = None
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_42(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(None, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_43(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, None)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_44(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_45(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(
            se_robust,
        )
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_46(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1.0)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_47(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = None

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_48(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(None, 1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_49(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, None)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_50(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(1e-20)

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_51(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(
            se_nonrobust,
        )

        return se_robust, se_nonrobust

    def xǁMLEstimatorǁ_compute_standard_errors__mutmut_52(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1.0)

        return se_robust, se_nonrobust

    xǁMLEstimatorǁ_compute_standard_errors__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_1": xǁMLEstimatorǁ_compute_standard_errors__mutmut_1,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_2": xǁMLEstimatorǁ_compute_standard_errors__mutmut_2,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_3": xǁMLEstimatorǁ_compute_standard_errors__mutmut_3,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_4": xǁMLEstimatorǁ_compute_standard_errors__mutmut_4,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_5": xǁMLEstimatorǁ_compute_standard_errors__mutmut_5,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_6": xǁMLEstimatorǁ_compute_standard_errors__mutmut_6,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_7": xǁMLEstimatorǁ_compute_standard_errors__mutmut_7,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_8": xǁMLEstimatorǁ_compute_standard_errors__mutmut_8,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_9": xǁMLEstimatorǁ_compute_standard_errors__mutmut_9,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_10": xǁMLEstimatorǁ_compute_standard_errors__mutmut_10,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_11": xǁMLEstimatorǁ_compute_standard_errors__mutmut_11,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_12": xǁMLEstimatorǁ_compute_standard_errors__mutmut_12,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_13": xǁMLEstimatorǁ_compute_standard_errors__mutmut_13,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_14": xǁMLEstimatorǁ_compute_standard_errors__mutmut_14,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_15": xǁMLEstimatorǁ_compute_standard_errors__mutmut_15,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_16": xǁMLEstimatorǁ_compute_standard_errors__mutmut_16,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_17": xǁMLEstimatorǁ_compute_standard_errors__mutmut_17,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_18": xǁMLEstimatorǁ_compute_standard_errors__mutmut_18,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_19": xǁMLEstimatorǁ_compute_standard_errors__mutmut_19,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_20": xǁMLEstimatorǁ_compute_standard_errors__mutmut_20,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_21": xǁMLEstimatorǁ_compute_standard_errors__mutmut_21,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_22": xǁMLEstimatorǁ_compute_standard_errors__mutmut_22,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_23": xǁMLEstimatorǁ_compute_standard_errors__mutmut_23,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_24": xǁMLEstimatorǁ_compute_standard_errors__mutmut_24,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_25": xǁMLEstimatorǁ_compute_standard_errors__mutmut_25,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_26": xǁMLEstimatorǁ_compute_standard_errors__mutmut_26,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_27": xǁMLEstimatorǁ_compute_standard_errors__mutmut_27,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_28": xǁMLEstimatorǁ_compute_standard_errors__mutmut_28,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_29": xǁMLEstimatorǁ_compute_standard_errors__mutmut_29,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_30": xǁMLEstimatorǁ_compute_standard_errors__mutmut_30,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_31": xǁMLEstimatorǁ_compute_standard_errors__mutmut_31,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_32": xǁMLEstimatorǁ_compute_standard_errors__mutmut_32,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_33": xǁMLEstimatorǁ_compute_standard_errors__mutmut_33,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_34": xǁMLEstimatorǁ_compute_standard_errors__mutmut_34,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_35": xǁMLEstimatorǁ_compute_standard_errors__mutmut_35,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_36": xǁMLEstimatorǁ_compute_standard_errors__mutmut_36,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_37": xǁMLEstimatorǁ_compute_standard_errors__mutmut_37,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_38": xǁMLEstimatorǁ_compute_standard_errors__mutmut_38,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_39": xǁMLEstimatorǁ_compute_standard_errors__mutmut_39,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_40": xǁMLEstimatorǁ_compute_standard_errors__mutmut_40,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_41": xǁMLEstimatorǁ_compute_standard_errors__mutmut_41,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_42": xǁMLEstimatorǁ_compute_standard_errors__mutmut_42,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_43": xǁMLEstimatorǁ_compute_standard_errors__mutmut_43,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_44": xǁMLEstimatorǁ_compute_standard_errors__mutmut_44,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_45": xǁMLEstimatorǁ_compute_standard_errors__mutmut_45,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_46": xǁMLEstimatorǁ_compute_standard_errors__mutmut_46,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_47": xǁMLEstimatorǁ_compute_standard_errors__mutmut_47,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_48": xǁMLEstimatorǁ_compute_standard_errors__mutmut_48,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_49": xǁMLEstimatorǁ_compute_standard_errors__mutmut_49,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_50": xǁMLEstimatorǁ_compute_standard_errors__mutmut_50,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_51": xǁMLEstimatorǁ_compute_standard_errors__mutmut_51,
        "xǁMLEstimatorǁ_compute_standard_errors__mutmut_52": xǁMLEstimatorǁ_compute_standard_errors__mutmut_52,
    }
    xǁMLEstimatorǁ_compute_standard_errors__mutmut_orig.__name__ = (
        "xǁMLEstimatorǁ_compute_standard_errors"
    )

    def _compute_hessian(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        args = [model, params, backcast]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMLEstimatorǁ_compute_hessian__mutmut_orig"),
            object.__getattribute__(self, "xǁMLEstimatorǁ_compute_hessian__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMLEstimatorǁ_compute_hessian__mutmut_orig(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_1(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = None
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_2(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = None

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_3(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1.00001

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_4(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return +model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_5(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(None, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_6(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, None)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_7(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_8(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(
                p,
            )

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_9(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = None

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_10(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros(None)

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_11(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(None):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_12(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(None, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_13(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, None):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_14(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_15(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(
                i,
            ):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_16(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = None
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_17(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(None)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_18(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = None
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_19(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(None)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_20(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = None
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_21(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps / max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_22(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(None, 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_23(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), None)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_24(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_25(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(
                    abs(params[i]),
                )
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_26(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(None), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_27(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1.00000001)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_28(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = None

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_29(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps / max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_30(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(None, 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_31(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), None)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_32(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_33(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(
                    abs(params[j]),
                )

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_34(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(None), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_35(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1.00000001)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_36(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = None
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_37(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(None)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_38(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei - ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_39(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params - ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_40(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = None
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_41(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(None)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_42(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei + ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_43(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params - ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_44(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = None
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_45(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(None)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_46(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei - ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_47(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params + ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_48(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = None

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_49(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(None)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_50(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei + ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_51(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params + ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_52(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = None
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_53(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) * (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_54(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp - fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_55(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm + fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_56(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp + fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_57(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] / ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_58(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 / ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_59(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (5.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def xǁMLEstimatorǁ_compute_hessian__mutmut_60(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = None

        return hessian

    xǁMLEstimatorǁ_compute_hessian__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMLEstimatorǁ_compute_hessian__mutmut_1": xǁMLEstimatorǁ_compute_hessian__mutmut_1,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_2": xǁMLEstimatorǁ_compute_hessian__mutmut_2,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_3": xǁMLEstimatorǁ_compute_hessian__mutmut_3,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_4": xǁMLEstimatorǁ_compute_hessian__mutmut_4,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_5": xǁMLEstimatorǁ_compute_hessian__mutmut_5,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_6": xǁMLEstimatorǁ_compute_hessian__mutmut_6,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_7": xǁMLEstimatorǁ_compute_hessian__mutmut_7,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_8": xǁMLEstimatorǁ_compute_hessian__mutmut_8,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_9": xǁMLEstimatorǁ_compute_hessian__mutmut_9,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_10": xǁMLEstimatorǁ_compute_hessian__mutmut_10,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_11": xǁMLEstimatorǁ_compute_hessian__mutmut_11,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_12": xǁMLEstimatorǁ_compute_hessian__mutmut_12,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_13": xǁMLEstimatorǁ_compute_hessian__mutmut_13,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_14": xǁMLEstimatorǁ_compute_hessian__mutmut_14,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_15": xǁMLEstimatorǁ_compute_hessian__mutmut_15,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_16": xǁMLEstimatorǁ_compute_hessian__mutmut_16,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_17": xǁMLEstimatorǁ_compute_hessian__mutmut_17,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_18": xǁMLEstimatorǁ_compute_hessian__mutmut_18,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_19": xǁMLEstimatorǁ_compute_hessian__mutmut_19,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_20": xǁMLEstimatorǁ_compute_hessian__mutmut_20,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_21": xǁMLEstimatorǁ_compute_hessian__mutmut_21,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_22": xǁMLEstimatorǁ_compute_hessian__mutmut_22,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_23": xǁMLEstimatorǁ_compute_hessian__mutmut_23,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_24": xǁMLEstimatorǁ_compute_hessian__mutmut_24,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_25": xǁMLEstimatorǁ_compute_hessian__mutmut_25,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_26": xǁMLEstimatorǁ_compute_hessian__mutmut_26,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_27": xǁMLEstimatorǁ_compute_hessian__mutmut_27,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_28": xǁMLEstimatorǁ_compute_hessian__mutmut_28,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_29": xǁMLEstimatorǁ_compute_hessian__mutmut_29,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_30": xǁMLEstimatorǁ_compute_hessian__mutmut_30,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_31": xǁMLEstimatorǁ_compute_hessian__mutmut_31,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_32": xǁMLEstimatorǁ_compute_hessian__mutmut_32,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_33": xǁMLEstimatorǁ_compute_hessian__mutmut_33,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_34": xǁMLEstimatorǁ_compute_hessian__mutmut_34,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_35": xǁMLEstimatorǁ_compute_hessian__mutmut_35,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_36": xǁMLEstimatorǁ_compute_hessian__mutmut_36,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_37": xǁMLEstimatorǁ_compute_hessian__mutmut_37,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_38": xǁMLEstimatorǁ_compute_hessian__mutmut_38,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_39": xǁMLEstimatorǁ_compute_hessian__mutmut_39,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_40": xǁMLEstimatorǁ_compute_hessian__mutmut_40,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_41": xǁMLEstimatorǁ_compute_hessian__mutmut_41,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_42": xǁMLEstimatorǁ_compute_hessian__mutmut_42,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_43": xǁMLEstimatorǁ_compute_hessian__mutmut_43,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_44": xǁMLEstimatorǁ_compute_hessian__mutmut_44,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_45": xǁMLEstimatorǁ_compute_hessian__mutmut_45,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_46": xǁMLEstimatorǁ_compute_hessian__mutmut_46,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_47": xǁMLEstimatorǁ_compute_hessian__mutmut_47,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_48": xǁMLEstimatorǁ_compute_hessian__mutmut_48,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_49": xǁMLEstimatorǁ_compute_hessian__mutmut_49,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_50": xǁMLEstimatorǁ_compute_hessian__mutmut_50,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_51": xǁMLEstimatorǁ_compute_hessian__mutmut_51,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_52": xǁMLEstimatorǁ_compute_hessian__mutmut_52,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_53": xǁMLEstimatorǁ_compute_hessian__mutmut_53,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_54": xǁMLEstimatorǁ_compute_hessian__mutmut_54,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_55": xǁMLEstimatorǁ_compute_hessian__mutmut_55,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_56": xǁMLEstimatorǁ_compute_hessian__mutmut_56,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_57": xǁMLEstimatorǁ_compute_hessian__mutmut_57,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_58": xǁMLEstimatorǁ_compute_hessian__mutmut_58,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_59": xǁMLEstimatorǁ_compute_hessian__mutmut_59,
        "xǁMLEstimatorǁ_compute_hessian__mutmut_60": xǁMLEstimatorǁ_compute_hessian__mutmut_60,
    }
    xǁMLEstimatorǁ_compute_hessian__mutmut_orig.__name__ = "xǁMLEstimatorǁ_compute_hessian"

    def _compute_opg(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        args = [model, params, backcast]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMLEstimatorǁ_compute_opg__mutmut_orig"),
            object.__getattribute__(self, "xǁMLEstimatorǁ_compute_opg__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMLEstimatorǁ_compute_opg__mutmut_orig(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(abs(params[j]), 1e-8)

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_1(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = None
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(abs(params[j]), 1e-8)

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_2(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = None

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(abs(params[j]), 1e-8)

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_3(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1.00001

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(abs(params[j]), 1e-8)

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_4(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = None
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(abs(params[j]), 1e-8)

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_5(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(None, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(abs(params[j]), 1e-8)

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_6(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, None)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(abs(params[j]), 1e-8)

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_7(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(abs(params[j]), 1e-8)

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_8(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(
            params,
        )
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(abs(params[j]), 1e-8)

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_9(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = None

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(abs(params[j]), 1e-8)

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_10(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = None
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(abs(params[j]), 1e-8)

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_11(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros(None)
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(abs(params[j]), 1e-8)

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_12(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(None):
            ej = np.zeros(k)
            ej[j] = eps * max(abs(params[j]), 1e-8)

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_13(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = None
            ej[j] = eps * max(abs(params[j]), 1e-8)

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_14(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(None)
            ej[j] = eps * max(abs(params[j]), 1e-8)

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_15(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = None

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_16(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps / max(abs(params[j]), 1e-8)

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_17(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(None, 1e-8)

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_18(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(abs(params[j]), None)

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_19(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(1e-8)

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_20(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(
                abs(params[j]),
            )

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_21(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(abs(None), 1e-8)

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_22(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(abs(params[j]), 1.00000001)

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_23(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(abs(params[j]), 1e-8)

            ll_plus = None
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_24(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(abs(params[j]), 1e-8)

            ll_plus = model.loglike_per_obs(None, backcast)
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_25(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(abs(params[j]), 1e-8)

            ll_plus = model.loglike_per_obs(params + ej, None)
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_26(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(abs(params[j]), 1e-8)

            ll_plus = model.loglike_per_obs(backcast)
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_27(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(abs(params[j]), 1e-8)

            ll_plus = model.loglike_per_obs(
                params + ej,
            )
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_28(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(abs(params[j]), 1e-8)

            ll_plus = model.loglike_per_obs(params - ej, backcast)
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_29(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(abs(params[j]), 1e-8)

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = None
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_30(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(abs(params[j]), 1e-8)

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(None, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_31(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(abs(params[j]), 1e-8)

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(params - ej, None)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_32(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(abs(params[j]), 1e-8)

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_33(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(abs(params[j]), 1e-8)

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(
                params - ej,
            )
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_34(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(abs(params[j]), 1e-8)

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(params + ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_35(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(abs(params[j]), 1e-8)

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = None

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_36(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(abs(params[j]), 1e-8)

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) * (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_37(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(abs(params[j]), 1e-8)

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus + ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_38(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(abs(params[j]), 1e-8)

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 / ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    def xǁMLEstimatorǁ_compute_opg__mutmut_39(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(abs(params[j]), 1e-8)

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (3.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients

    xǁMLEstimatorǁ_compute_opg__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMLEstimatorǁ_compute_opg__mutmut_1": xǁMLEstimatorǁ_compute_opg__mutmut_1,
        "xǁMLEstimatorǁ_compute_opg__mutmut_2": xǁMLEstimatorǁ_compute_opg__mutmut_2,
        "xǁMLEstimatorǁ_compute_opg__mutmut_3": xǁMLEstimatorǁ_compute_opg__mutmut_3,
        "xǁMLEstimatorǁ_compute_opg__mutmut_4": xǁMLEstimatorǁ_compute_opg__mutmut_4,
        "xǁMLEstimatorǁ_compute_opg__mutmut_5": xǁMLEstimatorǁ_compute_opg__mutmut_5,
        "xǁMLEstimatorǁ_compute_opg__mutmut_6": xǁMLEstimatorǁ_compute_opg__mutmut_6,
        "xǁMLEstimatorǁ_compute_opg__mutmut_7": xǁMLEstimatorǁ_compute_opg__mutmut_7,
        "xǁMLEstimatorǁ_compute_opg__mutmut_8": xǁMLEstimatorǁ_compute_opg__mutmut_8,
        "xǁMLEstimatorǁ_compute_opg__mutmut_9": xǁMLEstimatorǁ_compute_opg__mutmut_9,
        "xǁMLEstimatorǁ_compute_opg__mutmut_10": xǁMLEstimatorǁ_compute_opg__mutmut_10,
        "xǁMLEstimatorǁ_compute_opg__mutmut_11": xǁMLEstimatorǁ_compute_opg__mutmut_11,
        "xǁMLEstimatorǁ_compute_opg__mutmut_12": xǁMLEstimatorǁ_compute_opg__mutmut_12,
        "xǁMLEstimatorǁ_compute_opg__mutmut_13": xǁMLEstimatorǁ_compute_opg__mutmut_13,
        "xǁMLEstimatorǁ_compute_opg__mutmut_14": xǁMLEstimatorǁ_compute_opg__mutmut_14,
        "xǁMLEstimatorǁ_compute_opg__mutmut_15": xǁMLEstimatorǁ_compute_opg__mutmut_15,
        "xǁMLEstimatorǁ_compute_opg__mutmut_16": xǁMLEstimatorǁ_compute_opg__mutmut_16,
        "xǁMLEstimatorǁ_compute_opg__mutmut_17": xǁMLEstimatorǁ_compute_opg__mutmut_17,
        "xǁMLEstimatorǁ_compute_opg__mutmut_18": xǁMLEstimatorǁ_compute_opg__mutmut_18,
        "xǁMLEstimatorǁ_compute_opg__mutmut_19": xǁMLEstimatorǁ_compute_opg__mutmut_19,
        "xǁMLEstimatorǁ_compute_opg__mutmut_20": xǁMLEstimatorǁ_compute_opg__mutmut_20,
        "xǁMLEstimatorǁ_compute_opg__mutmut_21": xǁMLEstimatorǁ_compute_opg__mutmut_21,
        "xǁMLEstimatorǁ_compute_opg__mutmut_22": xǁMLEstimatorǁ_compute_opg__mutmut_22,
        "xǁMLEstimatorǁ_compute_opg__mutmut_23": xǁMLEstimatorǁ_compute_opg__mutmut_23,
        "xǁMLEstimatorǁ_compute_opg__mutmut_24": xǁMLEstimatorǁ_compute_opg__mutmut_24,
        "xǁMLEstimatorǁ_compute_opg__mutmut_25": xǁMLEstimatorǁ_compute_opg__mutmut_25,
        "xǁMLEstimatorǁ_compute_opg__mutmut_26": xǁMLEstimatorǁ_compute_opg__mutmut_26,
        "xǁMLEstimatorǁ_compute_opg__mutmut_27": xǁMLEstimatorǁ_compute_opg__mutmut_27,
        "xǁMLEstimatorǁ_compute_opg__mutmut_28": xǁMLEstimatorǁ_compute_opg__mutmut_28,
        "xǁMLEstimatorǁ_compute_opg__mutmut_29": xǁMLEstimatorǁ_compute_opg__mutmut_29,
        "xǁMLEstimatorǁ_compute_opg__mutmut_30": xǁMLEstimatorǁ_compute_opg__mutmut_30,
        "xǁMLEstimatorǁ_compute_opg__mutmut_31": xǁMLEstimatorǁ_compute_opg__mutmut_31,
        "xǁMLEstimatorǁ_compute_opg__mutmut_32": xǁMLEstimatorǁ_compute_opg__mutmut_32,
        "xǁMLEstimatorǁ_compute_opg__mutmut_33": xǁMLEstimatorǁ_compute_opg__mutmut_33,
        "xǁMLEstimatorǁ_compute_opg__mutmut_34": xǁMLEstimatorǁ_compute_opg__mutmut_34,
        "xǁMLEstimatorǁ_compute_opg__mutmut_35": xǁMLEstimatorǁ_compute_opg__mutmut_35,
        "xǁMLEstimatorǁ_compute_opg__mutmut_36": xǁMLEstimatorǁ_compute_opg__mutmut_36,
        "xǁMLEstimatorǁ_compute_opg__mutmut_37": xǁMLEstimatorǁ_compute_opg__mutmut_37,
        "xǁMLEstimatorǁ_compute_opg__mutmut_38": xǁMLEstimatorǁ_compute_opg__mutmut_38,
        "xǁMLEstimatorǁ_compute_opg__mutmut_39": xǁMLEstimatorǁ_compute_opg__mutmut_39,
    }
    xǁMLEstimatorǁ_compute_opg__mutmut_orig.__name__ = "xǁMLEstimatorǁ_compute_opg"
