"""ArchExperiment - orchestrator for volatility analysis workflows."""

from __future__ import annotations

from collections.abc import Callable
from typing import Annotated, Any, ClassVar

import numpy as np
from numpy.typing import NDArray

from archbox.experiment.comparison import ComparisonResult
from archbox.experiment.risk_analysis import RiskAnalysisResult
from archbox.experiment.validation import ValidationResult

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


class ArchExperiment:
    """Orchestrator for volatility analysis experiments.

    Provides a high-level API for fitting multiple models, comparing them,
    validating out-of-sample, and generating risk analysis reports.

    Parameters
    ----------
    returns : array-like
        Time series of returns.
    mean : str
        Mean model: 'constant' or 'zero'.

    Examples
    --------
    >>> from archbox.experiment import ArchExperiment
    >>> from archbox.datasets import load_dataset
    >>> sp500 = load_dataset('sp500')
    >>> exp = ArchExperiment(sp500['returns'])
    >>> exp.fit_all_models([
    ...     ('GARCH', {'p': 1, 'q': 1}),
    ...     ('EGARCH', {'p': 1, 'q': 1}),
    ... ])
    >>> comparison = exp.compare_models()
    >>> print(comparison.best_model())
    """

    def __init__(
        self,
        returns: Any,
        mean: str = "constant",
    ) -> None:
        args = [returns, mean]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁArchExperimentǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁArchExperimentǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁArchExperimentǁ__init____mutmut_orig(
        self,
        returns: Any,
        mean: str = "constant",
    ) -> None:
        """Initialize experiment with return data and mean model."""
        self.returns = np.asarray(returns, dtype=np.float64)
        self.mean = mean
        self.fitted_models: dict[str, Any] = {}
        self.model_specs: dict[str, tuple[str, dict[str, Any]]] = {}

    def xǁArchExperimentǁ__init____mutmut_1(
        self,
        returns: Any,
        mean: str = "XXconstantXX",
    ) -> None:
        """Initialize experiment with return data and mean model."""
        self.returns = np.asarray(returns, dtype=np.float64)
        self.mean = mean
        self.fitted_models: dict[str, Any] = {}
        self.model_specs: dict[str, tuple[str, dict[str, Any]]] = {}

    def xǁArchExperimentǁ__init____mutmut_2(
        self,
        returns: Any,
        mean: str = "CONSTANT",
    ) -> None:
        """Initialize experiment with return data and mean model."""
        self.returns = np.asarray(returns, dtype=np.float64)
        self.mean = mean
        self.fitted_models: dict[str, Any] = {}
        self.model_specs: dict[str, tuple[str, dict[str, Any]]] = {}

    def xǁArchExperimentǁ__init____mutmut_3(
        self,
        returns: Any,
        mean: str = "constant",
    ) -> None:
        """Initialize experiment with return data and mean model."""
        self.returns = None
        self.mean = mean
        self.fitted_models: dict[str, Any] = {}
        self.model_specs: dict[str, tuple[str, dict[str, Any]]] = {}

    def xǁArchExperimentǁ__init____mutmut_4(
        self,
        returns: Any,
        mean: str = "constant",
    ) -> None:
        """Initialize experiment with return data and mean model."""
        self.returns = np.asarray(None, dtype=np.float64)
        self.mean = mean
        self.fitted_models: dict[str, Any] = {}
        self.model_specs: dict[str, tuple[str, dict[str, Any]]] = {}

    def xǁArchExperimentǁ__init____mutmut_5(
        self,
        returns: Any,
        mean: str = "constant",
    ) -> None:
        """Initialize experiment with return data and mean model."""
        self.returns = np.asarray(returns, dtype=None)
        self.mean = mean
        self.fitted_models: dict[str, Any] = {}
        self.model_specs: dict[str, tuple[str, dict[str, Any]]] = {}

    def xǁArchExperimentǁ__init____mutmut_6(
        self,
        returns: Any,
        mean: str = "constant",
    ) -> None:
        """Initialize experiment with return data and mean model."""
        self.returns = np.asarray(dtype=np.float64)
        self.mean = mean
        self.fitted_models: dict[str, Any] = {}
        self.model_specs: dict[str, tuple[str, dict[str, Any]]] = {}

    def xǁArchExperimentǁ__init____mutmut_7(
        self,
        returns: Any,
        mean: str = "constant",
    ) -> None:
        """Initialize experiment with return data and mean model."""
        self.returns = np.asarray(
            returns,
        )
        self.mean = mean
        self.fitted_models: dict[str, Any] = {}
        self.model_specs: dict[str, tuple[str, dict[str, Any]]] = {}

    def xǁArchExperimentǁ__init____mutmut_8(
        self,
        returns: Any,
        mean: str = "constant",
    ) -> None:
        """Initialize experiment with return data and mean model."""
        self.returns = np.asarray(returns, dtype=np.float64)
        self.mean = None
        self.fitted_models: dict[str, Any] = {}
        self.model_specs: dict[str, tuple[str, dict[str, Any]]] = {}

    def xǁArchExperimentǁ__init____mutmut_9(
        self,
        returns: Any,
        mean: str = "constant",
    ) -> None:
        """Initialize experiment with return data and mean model."""
        self.returns = np.asarray(returns, dtype=np.float64)
        self.mean = mean
        self.fitted_models: dict[str, Any] = None
        self.model_specs: dict[str, tuple[str, dict[str, Any]]] = {}

    def xǁArchExperimentǁ__init____mutmut_10(
        self,
        returns: Any,
        mean: str = "constant",
    ) -> None:
        """Initialize experiment with return data and mean model."""
        self.returns = np.asarray(returns, dtype=np.float64)
        self.mean = mean
        self.fitted_models: dict[str, Any] = {}
        self.model_specs: dict[str, tuple[str, dict[str, Any]]] = None

    xǁArchExperimentǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁArchExperimentǁ__init____mutmut_1": xǁArchExperimentǁ__init____mutmut_1,
        "xǁArchExperimentǁ__init____mutmut_2": xǁArchExperimentǁ__init____mutmut_2,
        "xǁArchExperimentǁ__init____mutmut_3": xǁArchExperimentǁ__init____mutmut_3,
        "xǁArchExperimentǁ__init____mutmut_4": xǁArchExperimentǁ__init____mutmut_4,
        "xǁArchExperimentǁ__init____mutmut_5": xǁArchExperimentǁ__init____mutmut_5,
        "xǁArchExperimentǁ__init____mutmut_6": xǁArchExperimentǁ__init____mutmut_6,
        "xǁArchExperimentǁ__init____mutmut_7": xǁArchExperimentǁ__init____mutmut_7,
        "xǁArchExperimentǁ__init____mutmut_8": xǁArchExperimentǁ__init____mutmut_8,
        "xǁArchExperimentǁ__init____mutmut_9": xǁArchExperimentǁ__init____mutmut_9,
        "xǁArchExperimentǁ__init____mutmut_10": xǁArchExperimentǁ__init____mutmut_10,
    }
    xǁArchExperimentǁ__init____mutmut_orig.__name__ = "xǁArchExperimentǁ__init__"

    def _build_model(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        args = [model_type, returns, kwargs]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁArchExperimentǁ_build_model__mutmut_orig"),
            object.__getattribute__(self, "xǁArchExperimentǁ_build_model__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁArchExperimentǁ_build_model__mutmut_orig(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_1(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = None
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_2(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop(None, self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_3(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", None)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_4(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop(self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_5(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop(
            "mean",
        )
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_6(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("XXmeanXX", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_7(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("MEAN", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_8(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = None

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_9(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop(None, "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_10(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", None)

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_11(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_12(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop(
            "dist",
        )

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_13(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("XXdistXX", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_14(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("DIST", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_15(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "XXnormalXX")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_16(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "NORMAL")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_17(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = None
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_18(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = None

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_19(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.lower()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_20(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key != "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_21(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "XXGARCHXX":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_22(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "garch":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_23(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            model_map["GARCH"] = None
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_24(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["XXGARCHXX"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_25(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["garch"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_26(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key != "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_27(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "XXEGARCHXX":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_28(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "egarch":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_29(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            model_map["EGARCH"] = None
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_30(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["XXEGARCHXX"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_31(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["egarch"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_32(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key != "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_33(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "XXGJRXX":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_34(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "gjr":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_35(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            model_map["GJR"] = None
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_36(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["XXGJRXX"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_37(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["gjr"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_38(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key != "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_39(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "XXAPARCHXX":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_40(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "aparch":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_41(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            model_map["APARCH"] = None
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_42(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["XXAPARCHXX"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_43(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["aparch"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_44(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key != "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_45(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "XXCOMPONENTXX":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_46(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "component":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_47(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            model_map["COMPONENT"] = None
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_48(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["XXCOMPONENTXX"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_49(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["component"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_50(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key != "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_51(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "XXFIGARCHXX":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_52(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "figarch":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_53(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            model_map["FIGARCH"] = None
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_54(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["XXFIGARCHXX"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_55(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["figarch"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_56(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key != "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_57(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "XXIGARCHXX":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_58(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "igarch":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_59(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            model_map["IGARCH"] = None
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_60(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["XXIGARCHXX"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_61(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["igarch"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_62(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key != "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_63(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "XXGARCH-MXX":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_64(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "garch-m":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_65(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            model_map["GARCH-M"] = None

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_66(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["XXGARCH-MXX"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_67(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["garch-m"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_68(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = None
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_69(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(None)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_70(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is not None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_71(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = None
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_72(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(None)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_73(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(None, dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_74(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=None, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_75(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=None, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_76(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(dist=dist, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_77(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, mean=mean, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_78(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, **kwargs)

    def xǁArchExperimentǁ_build_model__mutmut_79(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(
            returns,
            dist=dist,
            mean=mean,
        )

    xǁArchExperimentǁ_build_model__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁArchExperimentǁ_build_model__mutmut_1": xǁArchExperimentǁ_build_model__mutmut_1,
        "xǁArchExperimentǁ_build_model__mutmut_2": xǁArchExperimentǁ_build_model__mutmut_2,
        "xǁArchExperimentǁ_build_model__mutmut_3": xǁArchExperimentǁ_build_model__mutmut_3,
        "xǁArchExperimentǁ_build_model__mutmut_4": xǁArchExperimentǁ_build_model__mutmut_4,
        "xǁArchExperimentǁ_build_model__mutmut_5": xǁArchExperimentǁ_build_model__mutmut_5,
        "xǁArchExperimentǁ_build_model__mutmut_6": xǁArchExperimentǁ_build_model__mutmut_6,
        "xǁArchExperimentǁ_build_model__mutmut_7": xǁArchExperimentǁ_build_model__mutmut_7,
        "xǁArchExperimentǁ_build_model__mutmut_8": xǁArchExperimentǁ_build_model__mutmut_8,
        "xǁArchExperimentǁ_build_model__mutmut_9": xǁArchExperimentǁ_build_model__mutmut_9,
        "xǁArchExperimentǁ_build_model__mutmut_10": xǁArchExperimentǁ_build_model__mutmut_10,
        "xǁArchExperimentǁ_build_model__mutmut_11": xǁArchExperimentǁ_build_model__mutmut_11,
        "xǁArchExperimentǁ_build_model__mutmut_12": xǁArchExperimentǁ_build_model__mutmut_12,
        "xǁArchExperimentǁ_build_model__mutmut_13": xǁArchExperimentǁ_build_model__mutmut_13,
        "xǁArchExperimentǁ_build_model__mutmut_14": xǁArchExperimentǁ_build_model__mutmut_14,
        "xǁArchExperimentǁ_build_model__mutmut_15": xǁArchExperimentǁ_build_model__mutmut_15,
        "xǁArchExperimentǁ_build_model__mutmut_16": xǁArchExperimentǁ_build_model__mutmut_16,
        "xǁArchExperimentǁ_build_model__mutmut_17": xǁArchExperimentǁ_build_model__mutmut_17,
        "xǁArchExperimentǁ_build_model__mutmut_18": xǁArchExperimentǁ_build_model__mutmut_18,
        "xǁArchExperimentǁ_build_model__mutmut_19": xǁArchExperimentǁ_build_model__mutmut_19,
        "xǁArchExperimentǁ_build_model__mutmut_20": xǁArchExperimentǁ_build_model__mutmut_20,
        "xǁArchExperimentǁ_build_model__mutmut_21": xǁArchExperimentǁ_build_model__mutmut_21,
        "xǁArchExperimentǁ_build_model__mutmut_22": xǁArchExperimentǁ_build_model__mutmut_22,
        "xǁArchExperimentǁ_build_model__mutmut_23": xǁArchExperimentǁ_build_model__mutmut_23,
        "xǁArchExperimentǁ_build_model__mutmut_24": xǁArchExperimentǁ_build_model__mutmut_24,
        "xǁArchExperimentǁ_build_model__mutmut_25": xǁArchExperimentǁ_build_model__mutmut_25,
        "xǁArchExperimentǁ_build_model__mutmut_26": xǁArchExperimentǁ_build_model__mutmut_26,
        "xǁArchExperimentǁ_build_model__mutmut_27": xǁArchExperimentǁ_build_model__mutmut_27,
        "xǁArchExperimentǁ_build_model__mutmut_28": xǁArchExperimentǁ_build_model__mutmut_28,
        "xǁArchExperimentǁ_build_model__mutmut_29": xǁArchExperimentǁ_build_model__mutmut_29,
        "xǁArchExperimentǁ_build_model__mutmut_30": xǁArchExperimentǁ_build_model__mutmut_30,
        "xǁArchExperimentǁ_build_model__mutmut_31": xǁArchExperimentǁ_build_model__mutmut_31,
        "xǁArchExperimentǁ_build_model__mutmut_32": xǁArchExperimentǁ_build_model__mutmut_32,
        "xǁArchExperimentǁ_build_model__mutmut_33": xǁArchExperimentǁ_build_model__mutmut_33,
        "xǁArchExperimentǁ_build_model__mutmut_34": xǁArchExperimentǁ_build_model__mutmut_34,
        "xǁArchExperimentǁ_build_model__mutmut_35": xǁArchExperimentǁ_build_model__mutmut_35,
        "xǁArchExperimentǁ_build_model__mutmut_36": xǁArchExperimentǁ_build_model__mutmut_36,
        "xǁArchExperimentǁ_build_model__mutmut_37": xǁArchExperimentǁ_build_model__mutmut_37,
        "xǁArchExperimentǁ_build_model__mutmut_38": xǁArchExperimentǁ_build_model__mutmut_38,
        "xǁArchExperimentǁ_build_model__mutmut_39": xǁArchExperimentǁ_build_model__mutmut_39,
        "xǁArchExperimentǁ_build_model__mutmut_40": xǁArchExperimentǁ_build_model__mutmut_40,
        "xǁArchExperimentǁ_build_model__mutmut_41": xǁArchExperimentǁ_build_model__mutmut_41,
        "xǁArchExperimentǁ_build_model__mutmut_42": xǁArchExperimentǁ_build_model__mutmut_42,
        "xǁArchExperimentǁ_build_model__mutmut_43": xǁArchExperimentǁ_build_model__mutmut_43,
        "xǁArchExperimentǁ_build_model__mutmut_44": xǁArchExperimentǁ_build_model__mutmut_44,
        "xǁArchExperimentǁ_build_model__mutmut_45": xǁArchExperimentǁ_build_model__mutmut_45,
        "xǁArchExperimentǁ_build_model__mutmut_46": xǁArchExperimentǁ_build_model__mutmut_46,
        "xǁArchExperimentǁ_build_model__mutmut_47": xǁArchExperimentǁ_build_model__mutmut_47,
        "xǁArchExperimentǁ_build_model__mutmut_48": xǁArchExperimentǁ_build_model__mutmut_48,
        "xǁArchExperimentǁ_build_model__mutmut_49": xǁArchExperimentǁ_build_model__mutmut_49,
        "xǁArchExperimentǁ_build_model__mutmut_50": xǁArchExperimentǁ_build_model__mutmut_50,
        "xǁArchExperimentǁ_build_model__mutmut_51": xǁArchExperimentǁ_build_model__mutmut_51,
        "xǁArchExperimentǁ_build_model__mutmut_52": xǁArchExperimentǁ_build_model__mutmut_52,
        "xǁArchExperimentǁ_build_model__mutmut_53": xǁArchExperimentǁ_build_model__mutmut_53,
        "xǁArchExperimentǁ_build_model__mutmut_54": xǁArchExperimentǁ_build_model__mutmut_54,
        "xǁArchExperimentǁ_build_model__mutmut_55": xǁArchExperimentǁ_build_model__mutmut_55,
        "xǁArchExperimentǁ_build_model__mutmut_56": xǁArchExperimentǁ_build_model__mutmut_56,
        "xǁArchExperimentǁ_build_model__mutmut_57": xǁArchExperimentǁ_build_model__mutmut_57,
        "xǁArchExperimentǁ_build_model__mutmut_58": xǁArchExperimentǁ_build_model__mutmut_58,
        "xǁArchExperimentǁ_build_model__mutmut_59": xǁArchExperimentǁ_build_model__mutmut_59,
        "xǁArchExperimentǁ_build_model__mutmut_60": xǁArchExperimentǁ_build_model__mutmut_60,
        "xǁArchExperimentǁ_build_model__mutmut_61": xǁArchExperimentǁ_build_model__mutmut_61,
        "xǁArchExperimentǁ_build_model__mutmut_62": xǁArchExperimentǁ_build_model__mutmut_62,
        "xǁArchExperimentǁ_build_model__mutmut_63": xǁArchExperimentǁ_build_model__mutmut_63,
        "xǁArchExperimentǁ_build_model__mutmut_64": xǁArchExperimentǁ_build_model__mutmut_64,
        "xǁArchExperimentǁ_build_model__mutmut_65": xǁArchExperimentǁ_build_model__mutmut_65,
        "xǁArchExperimentǁ_build_model__mutmut_66": xǁArchExperimentǁ_build_model__mutmut_66,
        "xǁArchExperimentǁ_build_model__mutmut_67": xǁArchExperimentǁ_build_model__mutmut_67,
        "xǁArchExperimentǁ_build_model__mutmut_68": xǁArchExperimentǁ_build_model__mutmut_68,
        "xǁArchExperimentǁ_build_model__mutmut_69": xǁArchExperimentǁ_build_model__mutmut_69,
        "xǁArchExperimentǁ_build_model__mutmut_70": xǁArchExperimentǁ_build_model__mutmut_70,
        "xǁArchExperimentǁ_build_model__mutmut_71": xǁArchExperimentǁ_build_model__mutmut_71,
        "xǁArchExperimentǁ_build_model__mutmut_72": xǁArchExperimentǁ_build_model__mutmut_72,
        "xǁArchExperimentǁ_build_model__mutmut_73": xǁArchExperimentǁ_build_model__mutmut_73,
        "xǁArchExperimentǁ_build_model__mutmut_74": xǁArchExperimentǁ_build_model__mutmut_74,
        "xǁArchExperimentǁ_build_model__mutmut_75": xǁArchExperimentǁ_build_model__mutmut_75,
        "xǁArchExperimentǁ_build_model__mutmut_76": xǁArchExperimentǁ_build_model__mutmut_76,
        "xǁArchExperimentǁ_build_model__mutmut_77": xǁArchExperimentǁ_build_model__mutmut_77,
        "xǁArchExperimentǁ_build_model__mutmut_78": xǁArchExperimentǁ_build_model__mutmut_78,
        "xǁArchExperimentǁ_build_model__mutmut_79": xǁArchExperimentǁ_build_model__mutmut_79,
    }
    xǁArchExperimentǁ_build_model__mutmut_orig.__name__ = "xǁArchExperimentǁ_build_model"

    def fit_all_models(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        args = [model_specs, disp]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁArchExperimentǁfit_all_models__mutmut_orig"),
            object.__getattribute__(self, "xǁArchExperimentǁfit_all_models__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁArchExperimentǁfit_all_models__mutmut_orig(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("dist", "normal")
            p = kwargs_copy.get("p", 1)
            q = kwargs_copy.get("q", 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, self.returns, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_1(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = True,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("dist", "normal")
            p = kwargs_copy.get("p", 1)
            q = kwargs_copy.get("q", 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, self.returns, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_2(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = None
            dist = kwargs_copy.get("dist", "normal")
            p = kwargs_copy.get("p", 1)
            q = kwargs_copy.get("q", 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, self.returns, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_3(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = None
            p = kwargs_copy.get("p", 1)
            q = kwargs_copy.get("q", 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, self.returns, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_4(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get(None, "normal")
            p = kwargs_copy.get("p", 1)
            q = kwargs_copy.get("q", 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, self.returns, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_5(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("dist", None)
            p = kwargs_copy.get("p", 1)
            q = kwargs_copy.get("q", 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, self.returns, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_6(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("normal")
            p = kwargs_copy.get("p", 1)
            q = kwargs_copy.get("q", 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, self.returns, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_7(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get(
                "dist",
            )
            p = kwargs_copy.get("p", 1)
            q = kwargs_copy.get("q", 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, self.returns, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_8(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("XXdistXX", "normal")
            p = kwargs_copy.get("p", 1)
            q = kwargs_copy.get("q", 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, self.returns, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_9(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("DIST", "normal")
            p = kwargs_copy.get("p", 1)
            q = kwargs_copy.get("q", 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, self.returns, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_10(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("dist", "XXnormalXX")
            p = kwargs_copy.get("p", 1)
            q = kwargs_copy.get("q", 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, self.returns, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_11(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("dist", "NORMAL")
            p = kwargs_copy.get("p", 1)
            q = kwargs_copy.get("q", 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, self.returns, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_12(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("dist", "normal")
            p = None
            q = kwargs_copy.get("q", 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, self.returns, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_13(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("dist", "normal")
            p = kwargs_copy.get(None, 1)
            q = kwargs_copy.get("q", 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, self.returns, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_14(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("dist", "normal")
            p = kwargs_copy.get("p", None)
            q = kwargs_copy.get("q", 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, self.returns, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_15(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("dist", "normal")
            p = kwargs_copy.get(1)
            q = kwargs_copy.get("q", 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, self.returns, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_16(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("dist", "normal")
            p = kwargs_copy.get(
                "p",
            )
            q = kwargs_copy.get("q", 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, self.returns, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_17(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("dist", "normal")
            p = kwargs_copy.get("XXpXX", 1)
            q = kwargs_copy.get("q", 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, self.returns, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_18(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("dist", "normal")
            p = kwargs_copy.get("P", 1)
            q = kwargs_copy.get("q", 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, self.returns, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_19(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("dist", "normal")
            p = kwargs_copy.get("p", 2)
            q = kwargs_copy.get("q", 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, self.returns, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_20(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("dist", "normal")
            p = kwargs_copy.get("p", 1)
            q = None
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, self.returns, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_21(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("dist", "normal")
            p = kwargs_copy.get("p", 1)
            q = kwargs_copy.get(None, 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, self.returns, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_22(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("dist", "normal")
            p = kwargs_copy.get("p", 1)
            q = kwargs_copy.get("q", None)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, self.returns, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_23(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("dist", "normal")
            p = kwargs_copy.get("p", 1)
            q = kwargs_copy.get(1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, self.returns, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_24(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("dist", "normal")
            p = kwargs_copy.get("p", 1)
            q = kwargs_copy.get(
                "q",
            )
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, self.returns, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_25(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("dist", "normal")
            p = kwargs_copy.get("p", 1)
            q = kwargs_copy.get("XXqXX", 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, self.returns, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_26(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("dist", "normal")
            p = kwargs_copy.get("p", 1)
            q = kwargs_copy.get("Q", 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, self.returns, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_27(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("dist", "normal")
            p = kwargs_copy.get("p", 1)
            q = kwargs_copy.get("q", 2)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, self.returns, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_28(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("dist", "normal")
            p = kwargs_copy.get("p", 1)
            q = kwargs_copy.get("q", 1)
            name = None

            model = self._build_model(model_type, self.returns, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_29(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("dist", "normal")
            p = kwargs_copy.get("p", 1)
            q = kwargs_copy.get("q", 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = None
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_30(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("dist", "normal")
            p = kwargs_copy.get("p", 1)
            q = kwargs_copy.get("q", 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(None, self.returns, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_31(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("dist", "normal")
            p = kwargs_copy.get("p", 1)
            q = kwargs_copy.get("q", 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, None, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_32(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("dist", "normal")
            p = kwargs_copy.get("p", 1)
            q = kwargs_copy.get("q", 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, self.returns, None)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_33(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("dist", "normal")
            p = kwargs_copy.get("p", 1)
            q = kwargs_copy.get("q", 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(self.returns, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_34(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("dist", "normal")
            p = kwargs_copy.get("p", 1)
            q = kwargs_copy.get("q", 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_35(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("dist", "normal")
            p = kwargs_copy.get("p", 1)
            q = kwargs_copy.get("q", 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(
                model_type,
                self.returns,
            )
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_36(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("dist", "normal")
            p = kwargs_copy.get("p", 1)
            q = kwargs_copy.get("q", 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, self.returns, kwargs_copy)
            results = None
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_37(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("dist", "normal")
            p = kwargs_copy.get("p", 1)
            q = kwargs_copy.get("q", 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, self.returns, kwargs_copy)
            results = model.fit(disp=None)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_38(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("dist", "normal")
            p = kwargs_copy.get("p", 1)
            q = kwargs_copy.get("q", 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, self.returns, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = None
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def xǁArchExperimentǁfit_all_models__mutmut_39(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("dist", "normal")
            p = kwargs_copy.get("p", 1)
            q = kwargs_copy.get("q", 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, self.returns, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = None

        return self.fitted_models

    xǁArchExperimentǁfit_all_models__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁArchExperimentǁfit_all_models__mutmut_1": xǁArchExperimentǁfit_all_models__mutmut_1,
        "xǁArchExperimentǁfit_all_models__mutmut_2": xǁArchExperimentǁfit_all_models__mutmut_2,
        "xǁArchExperimentǁfit_all_models__mutmut_3": xǁArchExperimentǁfit_all_models__mutmut_3,
        "xǁArchExperimentǁfit_all_models__mutmut_4": xǁArchExperimentǁfit_all_models__mutmut_4,
        "xǁArchExperimentǁfit_all_models__mutmut_5": xǁArchExperimentǁfit_all_models__mutmut_5,
        "xǁArchExperimentǁfit_all_models__mutmut_6": xǁArchExperimentǁfit_all_models__mutmut_6,
        "xǁArchExperimentǁfit_all_models__mutmut_7": xǁArchExperimentǁfit_all_models__mutmut_7,
        "xǁArchExperimentǁfit_all_models__mutmut_8": xǁArchExperimentǁfit_all_models__mutmut_8,
        "xǁArchExperimentǁfit_all_models__mutmut_9": xǁArchExperimentǁfit_all_models__mutmut_9,
        "xǁArchExperimentǁfit_all_models__mutmut_10": xǁArchExperimentǁfit_all_models__mutmut_10,
        "xǁArchExperimentǁfit_all_models__mutmut_11": xǁArchExperimentǁfit_all_models__mutmut_11,
        "xǁArchExperimentǁfit_all_models__mutmut_12": xǁArchExperimentǁfit_all_models__mutmut_12,
        "xǁArchExperimentǁfit_all_models__mutmut_13": xǁArchExperimentǁfit_all_models__mutmut_13,
        "xǁArchExperimentǁfit_all_models__mutmut_14": xǁArchExperimentǁfit_all_models__mutmut_14,
        "xǁArchExperimentǁfit_all_models__mutmut_15": xǁArchExperimentǁfit_all_models__mutmut_15,
        "xǁArchExperimentǁfit_all_models__mutmut_16": xǁArchExperimentǁfit_all_models__mutmut_16,
        "xǁArchExperimentǁfit_all_models__mutmut_17": xǁArchExperimentǁfit_all_models__mutmut_17,
        "xǁArchExperimentǁfit_all_models__mutmut_18": xǁArchExperimentǁfit_all_models__mutmut_18,
        "xǁArchExperimentǁfit_all_models__mutmut_19": xǁArchExperimentǁfit_all_models__mutmut_19,
        "xǁArchExperimentǁfit_all_models__mutmut_20": xǁArchExperimentǁfit_all_models__mutmut_20,
        "xǁArchExperimentǁfit_all_models__mutmut_21": xǁArchExperimentǁfit_all_models__mutmut_21,
        "xǁArchExperimentǁfit_all_models__mutmut_22": xǁArchExperimentǁfit_all_models__mutmut_22,
        "xǁArchExperimentǁfit_all_models__mutmut_23": xǁArchExperimentǁfit_all_models__mutmut_23,
        "xǁArchExperimentǁfit_all_models__mutmut_24": xǁArchExperimentǁfit_all_models__mutmut_24,
        "xǁArchExperimentǁfit_all_models__mutmut_25": xǁArchExperimentǁfit_all_models__mutmut_25,
        "xǁArchExperimentǁfit_all_models__mutmut_26": xǁArchExperimentǁfit_all_models__mutmut_26,
        "xǁArchExperimentǁfit_all_models__mutmut_27": xǁArchExperimentǁfit_all_models__mutmut_27,
        "xǁArchExperimentǁfit_all_models__mutmut_28": xǁArchExperimentǁfit_all_models__mutmut_28,
        "xǁArchExperimentǁfit_all_models__mutmut_29": xǁArchExperimentǁfit_all_models__mutmut_29,
        "xǁArchExperimentǁfit_all_models__mutmut_30": xǁArchExperimentǁfit_all_models__mutmut_30,
        "xǁArchExperimentǁfit_all_models__mutmut_31": xǁArchExperimentǁfit_all_models__mutmut_31,
        "xǁArchExperimentǁfit_all_models__mutmut_32": xǁArchExperimentǁfit_all_models__mutmut_32,
        "xǁArchExperimentǁfit_all_models__mutmut_33": xǁArchExperimentǁfit_all_models__mutmut_33,
        "xǁArchExperimentǁfit_all_models__mutmut_34": xǁArchExperimentǁfit_all_models__mutmut_34,
        "xǁArchExperimentǁfit_all_models__mutmut_35": xǁArchExperimentǁfit_all_models__mutmut_35,
        "xǁArchExperimentǁfit_all_models__mutmut_36": xǁArchExperimentǁfit_all_models__mutmut_36,
        "xǁArchExperimentǁfit_all_models__mutmut_37": xǁArchExperimentǁfit_all_models__mutmut_37,
        "xǁArchExperimentǁfit_all_models__mutmut_38": xǁArchExperimentǁfit_all_models__mutmut_38,
        "xǁArchExperimentǁfit_all_models__mutmut_39": xǁArchExperimentǁfit_all_models__mutmut_39,
    }
    xǁArchExperimentǁfit_all_models__mutmut_orig.__name__ = "xǁArchExperimentǁfit_all_models"

    def compare_models(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        args = [criteria]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁArchExperimentǁcompare_models__mutmut_orig"),
            object.__getattribute__(self, "xǁArchExperimentǁcompare_models__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁArchExperimentǁcompare_models__mutmut_orig(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_1(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_2(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = None
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_3(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "XXNo models fitted. Call fit_all_models() first.XX"
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_4(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "no models fitted. call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_5(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "NO MODELS FITTED. CALL FIT_ALL_MODELS() FIRST."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_6(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(None)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_7(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is not None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_8(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = None

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_9(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["XXaicXX", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_10(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["AIC", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_11(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "XXbicXX", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_12(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "BIC", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_13(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "XXloglikeXX", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_14(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "LOGLIKE", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_15(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "XXpersistenceXX"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_16(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "PERSISTENCE"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_17(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = None
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_18(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(None)
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_19(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = None
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_20(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = None

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_21(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = None
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_22(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(None)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_23(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c != "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_24(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "XXaicXX":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_25(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "AIC":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_26(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(None)
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_27(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(None))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_28(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c != "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_29(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "XXbicXX":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_30(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "BIC":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_31(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(None)
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_32(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(None))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_33(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c != "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_34(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "XXloglikeXX":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_35(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "LOGLIKE":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_36(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(None)
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_37(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(None))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_38(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c != "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_39(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "XXpersistenceXX":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_40(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "PERSISTENCE":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_41(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(None)
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_42(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(None))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_43(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(None)

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_44(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(None))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_45(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(None, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_46(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, None, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_47(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, None)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_48(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_49(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_50(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(
                        float(
                            getattr(
                                result,
                                c,
                            )
                        )
                    )

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_51(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=None,
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_52(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=None,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_53(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=None,
        )

    def xǁArchExperimentǁcompare_models__mutmut_54(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            criteria=criteria_values,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_55(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            results=results_list,
        )

    def xǁArchExperimentǁcompare_models__mutmut_56(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
        )

    xǁArchExperimentǁcompare_models__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁArchExperimentǁcompare_models__mutmut_1": xǁArchExperimentǁcompare_models__mutmut_1,
        "xǁArchExperimentǁcompare_models__mutmut_2": xǁArchExperimentǁcompare_models__mutmut_2,
        "xǁArchExperimentǁcompare_models__mutmut_3": xǁArchExperimentǁcompare_models__mutmut_3,
        "xǁArchExperimentǁcompare_models__mutmut_4": xǁArchExperimentǁcompare_models__mutmut_4,
        "xǁArchExperimentǁcompare_models__mutmut_5": xǁArchExperimentǁcompare_models__mutmut_5,
        "xǁArchExperimentǁcompare_models__mutmut_6": xǁArchExperimentǁcompare_models__mutmut_6,
        "xǁArchExperimentǁcompare_models__mutmut_7": xǁArchExperimentǁcompare_models__mutmut_7,
        "xǁArchExperimentǁcompare_models__mutmut_8": xǁArchExperimentǁcompare_models__mutmut_8,
        "xǁArchExperimentǁcompare_models__mutmut_9": xǁArchExperimentǁcompare_models__mutmut_9,
        "xǁArchExperimentǁcompare_models__mutmut_10": xǁArchExperimentǁcompare_models__mutmut_10,
        "xǁArchExperimentǁcompare_models__mutmut_11": xǁArchExperimentǁcompare_models__mutmut_11,
        "xǁArchExperimentǁcompare_models__mutmut_12": xǁArchExperimentǁcompare_models__mutmut_12,
        "xǁArchExperimentǁcompare_models__mutmut_13": xǁArchExperimentǁcompare_models__mutmut_13,
        "xǁArchExperimentǁcompare_models__mutmut_14": xǁArchExperimentǁcompare_models__mutmut_14,
        "xǁArchExperimentǁcompare_models__mutmut_15": xǁArchExperimentǁcompare_models__mutmut_15,
        "xǁArchExperimentǁcompare_models__mutmut_16": xǁArchExperimentǁcompare_models__mutmut_16,
        "xǁArchExperimentǁcompare_models__mutmut_17": xǁArchExperimentǁcompare_models__mutmut_17,
        "xǁArchExperimentǁcompare_models__mutmut_18": xǁArchExperimentǁcompare_models__mutmut_18,
        "xǁArchExperimentǁcompare_models__mutmut_19": xǁArchExperimentǁcompare_models__mutmut_19,
        "xǁArchExperimentǁcompare_models__mutmut_20": xǁArchExperimentǁcompare_models__mutmut_20,
        "xǁArchExperimentǁcompare_models__mutmut_21": xǁArchExperimentǁcompare_models__mutmut_21,
        "xǁArchExperimentǁcompare_models__mutmut_22": xǁArchExperimentǁcompare_models__mutmut_22,
        "xǁArchExperimentǁcompare_models__mutmut_23": xǁArchExperimentǁcompare_models__mutmut_23,
        "xǁArchExperimentǁcompare_models__mutmut_24": xǁArchExperimentǁcompare_models__mutmut_24,
        "xǁArchExperimentǁcompare_models__mutmut_25": xǁArchExperimentǁcompare_models__mutmut_25,
        "xǁArchExperimentǁcompare_models__mutmut_26": xǁArchExperimentǁcompare_models__mutmut_26,
        "xǁArchExperimentǁcompare_models__mutmut_27": xǁArchExperimentǁcompare_models__mutmut_27,
        "xǁArchExperimentǁcompare_models__mutmut_28": xǁArchExperimentǁcompare_models__mutmut_28,
        "xǁArchExperimentǁcompare_models__mutmut_29": xǁArchExperimentǁcompare_models__mutmut_29,
        "xǁArchExperimentǁcompare_models__mutmut_30": xǁArchExperimentǁcompare_models__mutmut_30,
        "xǁArchExperimentǁcompare_models__mutmut_31": xǁArchExperimentǁcompare_models__mutmut_31,
        "xǁArchExperimentǁcompare_models__mutmut_32": xǁArchExperimentǁcompare_models__mutmut_32,
        "xǁArchExperimentǁcompare_models__mutmut_33": xǁArchExperimentǁcompare_models__mutmut_33,
        "xǁArchExperimentǁcompare_models__mutmut_34": xǁArchExperimentǁcompare_models__mutmut_34,
        "xǁArchExperimentǁcompare_models__mutmut_35": xǁArchExperimentǁcompare_models__mutmut_35,
        "xǁArchExperimentǁcompare_models__mutmut_36": xǁArchExperimentǁcompare_models__mutmut_36,
        "xǁArchExperimentǁcompare_models__mutmut_37": xǁArchExperimentǁcompare_models__mutmut_37,
        "xǁArchExperimentǁcompare_models__mutmut_38": xǁArchExperimentǁcompare_models__mutmut_38,
        "xǁArchExperimentǁcompare_models__mutmut_39": xǁArchExperimentǁcompare_models__mutmut_39,
        "xǁArchExperimentǁcompare_models__mutmut_40": xǁArchExperimentǁcompare_models__mutmut_40,
        "xǁArchExperimentǁcompare_models__mutmut_41": xǁArchExperimentǁcompare_models__mutmut_41,
        "xǁArchExperimentǁcompare_models__mutmut_42": xǁArchExperimentǁcompare_models__mutmut_42,
        "xǁArchExperimentǁcompare_models__mutmut_43": xǁArchExperimentǁcompare_models__mutmut_43,
        "xǁArchExperimentǁcompare_models__mutmut_44": xǁArchExperimentǁcompare_models__mutmut_44,
        "xǁArchExperimentǁcompare_models__mutmut_45": xǁArchExperimentǁcompare_models__mutmut_45,
        "xǁArchExperimentǁcompare_models__mutmut_46": xǁArchExperimentǁcompare_models__mutmut_46,
        "xǁArchExperimentǁcompare_models__mutmut_47": xǁArchExperimentǁcompare_models__mutmut_47,
        "xǁArchExperimentǁcompare_models__mutmut_48": xǁArchExperimentǁcompare_models__mutmut_48,
        "xǁArchExperimentǁcompare_models__mutmut_49": xǁArchExperimentǁcompare_models__mutmut_49,
        "xǁArchExperimentǁcompare_models__mutmut_50": xǁArchExperimentǁcompare_models__mutmut_50,
        "xǁArchExperimentǁcompare_models__mutmut_51": xǁArchExperimentǁcompare_models__mutmut_51,
        "xǁArchExperimentǁcompare_models__mutmut_52": xǁArchExperimentǁcompare_models__mutmut_52,
        "xǁArchExperimentǁcompare_models__mutmut_53": xǁArchExperimentǁcompare_models__mutmut_53,
        "xǁArchExperimentǁcompare_models__mutmut_54": xǁArchExperimentǁcompare_models__mutmut_54,
        "xǁArchExperimentǁcompare_models__mutmut_55": xǁArchExperimentǁcompare_models__mutmut_55,
        "xǁArchExperimentǁcompare_models__mutmut_56": xǁArchExperimentǁcompare_models__mutmut_56,
    }
    xǁArchExperimentǁcompare_models__mutmut_orig.__name__ = "xǁArchExperimentǁcompare_models"

    def validate_model(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        args = [model_name, test_size, horizon]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁArchExperimentǁvalidate_model__mutmut_orig"),
            object.__getattribute__(self, "xǁArchExperimentǁvalidate_model__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_orig(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_1(
        self,
        model_name: str | None = None,
        test_size: int = 501,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_2(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 2,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_3(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is not None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_4(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = None

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_5(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(None)

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_6(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(None))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_7(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_8(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = None
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_9(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(None)}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_10(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(None)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_11(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = None
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_12(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size > n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_13(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = None
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_14(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(None)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_15(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = None
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_16(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n + test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_17(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = None

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_18(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n + test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_19(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = None
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_20(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = None
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_21(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = None
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_22(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(None, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_23(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, None, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_24(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, None)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_25(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_26(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_27(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(
            model_type,
            train_returns,
        )
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_28(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = None

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_29(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=None)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_30(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=True)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_31(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = None
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_32(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=None)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_33(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) or "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_34(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "XXvarianceXX" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_35(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "VARIANCE" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_36(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" not in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_37(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = None
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_38(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(None)
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_39(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["XXvarianceXX"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_40(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["VARIANCE"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_41(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = None

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_42(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(None, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_43(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, None):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_44(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr("__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_45(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(
            forecast_vol,
        ):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_46(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "XX__len__XX"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_47(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__LEN__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_48(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = None
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_49(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(None, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_50(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=None)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_51(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_52(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(
                forecast_vol,
            )
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_53(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) >= test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_54(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = None
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_55(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) <= test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_56(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = None
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_57(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(None, forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_58(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), None)
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_59(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_60(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(
                    test_size - len(forecast_vol),
                )
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_61(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size + len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_62(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[+1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_63(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-2])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_64(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = None
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_65(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate(None)
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_66(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = None  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_67(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(None, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_68(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, None)  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_69(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_70(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(
                test_size,
            )  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_71(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(None))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_72(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=None,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_73(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=None,
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_74(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=None,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_75(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=None,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_76(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=None,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_77(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=None,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_78(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_79(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_80(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_81(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_82(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_squared_returns=test_returns**2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_83(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_84(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns * 2,
        )

    def xǁArchExperimentǁvalidate_model__mutmut_85(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**3,
        )

    xǁArchExperimentǁvalidate_model__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁArchExperimentǁvalidate_model__mutmut_1": xǁArchExperimentǁvalidate_model__mutmut_1,
        "xǁArchExperimentǁvalidate_model__mutmut_2": xǁArchExperimentǁvalidate_model__mutmut_2,
        "xǁArchExperimentǁvalidate_model__mutmut_3": xǁArchExperimentǁvalidate_model__mutmut_3,
        "xǁArchExperimentǁvalidate_model__mutmut_4": xǁArchExperimentǁvalidate_model__mutmut_4,
        "xǁArchExperimentǁvalidate_model__mutmut_5": xǁArchExperimentǁvalidate_model__mutmut_5,
        "xǁArchExperimentǁvalidate_model__mutmut_6": xǁArchExperimentǁvalidate_model__mutmut_6,
        "xǁArchExperimentǁvalidate_model__mutmut_7": xǁArchExperimentǁvalidate_model__mutmut_7,
        "xǁArchExperimentǁvalidate_model__mutmut_8": xǁArchExperimentǁvalidate_model__mutmut_8,
        "xǁArchExperimentǁvalidate_model__mutmut_9": xǁArchExperimentǁvalidate_model__mutmut_9,
        "xǁArchExperimentǁvalidate_model__mutmut_10": xǁArchExperimentǁvalidate_model__mutmut_10,
        "xǁArchExperimentǁvalidate_model__mutmut_11": xǁArchExperimentǁvalidate_model__mutmut_11,
        "xǁArchExperimentǁvalidate_model__mutmut_12": xǁArchExperimentǁvalidate_model__mutmut_12,
        "xǁArchExperimentǁvalidate_model__mutmut_13": xǁArchExperimentǁvalidate_model__mutmut_13,
        "xǁArchExperimentǁvalidate_model__mutmut_14": xǁArchExperimentǁvalidate_model__mutmut_14,
        "xǁArchExperimentǁvalidate_model__mutmut_15": xǁArchExperimentǁvalidate_model__mutmut_15,
        "xǁArchExperimentǁvalidate_model__mutmut_16": xǁArchExperimentǁvalidate_model__mutmut_16,
        "xǁArchExperimentǁvalidate_model__mutmut_17": xǁArchExperimentǁvalidate_model__mutmut_17,
        "xǁArchExperimentǁvalidate_model__mutmut_18": xǁArchExperimentǁvalidate_model__mutmut_18,
        "xǁArchExperimentǁvalidate_model__mutmut_19": xǁArchExperimentǁvalidate_model__mutmut_19,
        "xǁArchExperimentǁvalidate_model__mutmut_20": xǁArchExperimentǁvalidate_model__mutmut_20,
        "xǁArchExperimentǁvalidate_model__mutmut_21": xǁArchExperimentǁvalidate_model__mutmut_21,
        "xǁArchExperimentǁvalidate_model__mutmut_22": xǁArchExperimentǁvalidate_model__mutmut_22,
        "xǁArchExperimentǁvalidate_model__mutmut_23": xǁArchExperimentǁvalidate_model__mutmut_23,
        "xǁArchExperimentǁvalidate_model__mutmut_24": xǁArchExperimentǁvalidate_model__mutmut_24,
        "xǁArchExperimentǁvalidate_model__mutmut_25": xǁArchExperimentǁvalidate_model__mutmut_25,
        "xǁArchExperimentǁvalidate_model__mutmut_26": xǁArchExperimentǁvalidate_model__mutmut_26,
        "xǁArchExperimentǁvalidate_model__mutmut_27": xǁArchExperimentǁvalidate_model__mutmut_27,
        "xǁArchExperimentǁvalidate_model__mutmut_28": xǁArchExperimentǁvalidate_model__mutmut_28,
        "xǁArchExperimentǁvalidate_model__mutmut_29": xǁArchExperimentǁvalidate_model__mutmut_29,
        "xǁArchExperimentǁvalidate_model__mutmut_30": xǁArchExperimentǁvalidate_model__mutmut_30,
        "xǁArchExperimentǁvalidate_model__mutmut_31": xǁArchExperimentǁvalidate_model__mutmut_31,
        "xǁArchExperimentǁvalidate_model__mutmut_32": xǁArchExperimentǁvalidate_model__mutmut_32,
        "xǁArchExperimentǁvalidate_model__mutmut_33": xǁArchExperimentǁvalidate_model__mutmut_33,
        "xǁArchExperimentǁvalidate_model__mutmut_34": xǁArchExperimentǁvalidate_model__mutmut_34,
        "xǁArchExperimentǁvalidate_model__mutmut_35": xǁArchExperimentǁvalidate_model__mutmut_35,
        "xǁArchExperimentǁvalidate_model__mutmut_36": xǁArchExperimentǁvalidate_model__mutmut_36,
        "xǁArchExperimentǁvalidate_model__mutmut_37": xǁArchExperimentǁvalidate_model__mutmut_37,
        "xǁArchExperimentǁvalidate_model__mutmut_38": xǁArchExperimentǁvalidate_model__mutmut_38,
        "xǁArchExperimentǁvalidate_model__mutmut_39": xǁArchExperimentǁvalidate_model__mutmut_39,
        "xǁArchExperimentǁvalidate_model__mutmut_40": xǁArchExperimentǁvalidate_model__mutmut_40,
        "xǁArchExperimentǁvalidate_model__mutmut_41": xǁArchExperimentǁvalidate_model__mutmut_41,
        "xǁArchExperimentǁvalidate_model__mutmut_42": xǁArchExperimentǁvalidate_model__mutmut_42,
        "xǁArchExperimentǁvalidate_model__mutmut_43": xǁArchExperimentǁvalidate_model__mutmut_43,
        "xǁArchExperimentǁvalidate_model__mutmut_44": xǁArchExperimentǁvalidate_model__mutmut_44,
        "xǁArchExperimentǁvalidate_model__mutmut_45": xǁArchExperimentǁvalidate_model__mutmut_45,
        "xǁArchExperimentǁvalidate_model__mutmut_46": xǁArchExperimentǁvalidate_model__mutmut_46,
        "xǁArchExperimentǁvalidate_model__mutmut_47": xǁArchExperimentǁvalidate_model__mutmut_47,
        "xǁArchExperimentǁvalidate_model__mutmut_48": xǁArchExperimentǁvalidate_model__mutmut_48,
        "xǁArchExperimentǁvalidate_model__mutmut_49": xǁArchExperimentǁvalidate_model__mutmut_49,
        "xǁArchExperimentǁvalidate_model__mutmut_50": xǁArchExperimentǁvalidate_model__mutmut_50,
        "xǁArchExperimentǁvalidate_model__mutmut_51": xǁArchExperimentǁvalidate_model__mutmut_51,
        "xǁArchExperimentǁvalidate_model__mutmut_52": xǁArchExperimentǁvalidate_model__mutmut_52,
        "xǁArchExperimentǁvalidate_model__mutmut_53": xǁArchExperimentǁvalidate_model__mutmut_53,
        "xǁArchExperimentǁvalidate_model__mutmut_54": xǁArchExperimentǁvalidate_model__mutmut_54,
        "xǁArchExperimentǁvalidate_model__mutmut_55": xǁArchExperimentǁvalidate_model__mutmut_55,
        "xǁArchExperimentǁvalidate_model__mutmut_56": xǁArchExperimentǁvalidate_model__mutmut_56,
        "xǁArchExperimentǁvalidate_model__mutmut_57": xǁArchExperimentǁvalidate_model__mutmut_57,
        "xǁArchExperimentǁvalidate_model__mutmut_58": xǁArchExperimentǁvalidate_model__mutmut_58,
        "xǁArchExperimentǁvalidate_model__mutmut_59": xǁArchExperimentǁvalidate_model__mutmut_59,
        "xǁArchExperimentǁvalidate_model__mutmut_60": xǁArchExperimentǁvalidate_model__mutmut_60,
        "xǁArchExperimentǁvalidate_model__mutmut_61": xǁArchExperimentǁvalidate_model__mutmut_61,
        "xǁArchExperimentǁvalidate_model__mutmut_62": xǁArchExperimentǁvalidate_model__mutmut_62,
        "xǁArchExperimentǁvalidate_model__mutmut_63": xǁArchExperimentǁvalidate_model__mutmut_63,
        "xǁArchExperimentǁvalidate_model__mutmut_64": xǁArchExperimentǁvalidate_model__mutmut_64,
        "xǁArchExperimentǁvalidate_model__mutmut_65": xǁArchExperimentǁvalidate_model__mutmut_65,
        "xǁArchExperimentǁvalidate_model__mutmut_66": xǁArchExperimentǁvalidate_model__mutmut_66,
        "xǁArchExperimentǁvalidate_model__mutmut_67": xǁArchExperimentǁvalidate_model__mutmut_67,
        "xǁArchExperimentǁvalidate_model__mutmut_68": xǁArchExperimentǁvalidate_model__mutmut_68,
        "xǁArchExperimentǁvalidate_model__mutmut_69": xǁArchExperimentǁvalidate_model__mutmut_69,
        "xǁArchExperimentǁvalidate_model__mutmut_70": xǁArchExperimentǁvalidate_model__mutmut_70,
        "xǁArchExperimentǁvalidate_model__mutmut_71": xǁArchExperimentǁvalidate_model__mutmut_71,
        "xǁArchExperimentǁvalidate_model__mutmut_72": xǁArchExperimentǁvalidate_model__mutmut_72,
        "xǁArchExperimentǁvalidate_model__mutmut_73": xǁArchExperimentǁvalidate_model__mutmut_73,
        "xǁArchExperimentǁvalidate_model__mutmut_74": xǁArchExperimentǁvalidate_model__mutmut_74,
        "xǁArchExperimentǁvalidate_model__mutmut_75": xǁArchExperimentǁvalidate_model__mutmut_75,
        "xǁArchExperimentǁvalidate_model__mutmut_76": xǁArchExperimentǁvalidate_model__mutmut_76,
        "xǁArchExperimentǁvalidate_model__mutmut_77": xǁArchExperimentǁvalidate_model__mutmut_77,
        "xǁArchExperimentǁvalidate_model__mutmut_78": xǁArchExperimentǁvalidate_model__mutmut_78,
        "xǁArchExperimentǁvalidate_model__mutmut_79": xǁArchExperimentǁvalidate_model__mutmut_79,
        "xǁArchExperimentǁvalidate_model__mutmut_80": xǁArchExperimentǁvalidate_model__mutmut_80,
        "xǁArchExperimentǁvalidate_model__mutmut_81": xǁArchExperimentǁvalidate_model__mutmut_81,
        "xǁArchExperimentǁvalidate_model__mutmut_82": xǁArchExperimentǁvalidate_model__mutmut_82,
        "xǁArchExperimentǁvalidate_model__mutmut_83": xǁArchExperimentǁvalidate_model__mutmut_83,
        "xǁArchExperimentǁvalidate_model__mutmut_84": xǁArchExperimentǁvalidate_model__mutmut_84,
        "xǁArchExperimentǁvalidate_model__mutmut_85": xǁArchExperimentǁvalidate_model__mutmut_85,
    }
    xǁArchExperimentǁvalidate_model__mutmut_orig.__name__ = "xǁArchExperimentǁvalidate_model"

    def risk_analysis(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        args = [model, alpha, methods]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁArchExperimentǁrisk_analysis__mutmut_orig"),
            object.__getattribute__(self, "xǁArchExperimentǁrisk_analysis__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_orig(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_1(
        self,
        model: str | None = None,
        alpha: float = 1.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_2(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is not None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_3(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = None

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_4(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(None)

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_5(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(None))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_6(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_7(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = None
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_8(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(None)}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_9(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(None)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_10(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is not None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_11(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = None

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_12(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["XXparametricXX"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_13(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["PARAMETRIC"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_14(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = None

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_15(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall

        var_calc = None
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_16(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(None, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_17(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=None)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_18(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_19(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(
            result,
        )
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_20(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = None

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_21(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(None, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_22(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=None)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_23(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_24(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(
            result,
        )

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_25(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = None
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_26(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = None
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_27(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = None

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_28(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method != "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_29(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "XXparametricXX":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_30(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "PARAMETRIC":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_31(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = None
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_32(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = None
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_33(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method != "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_34(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "XXhistoricalXX":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_35(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "HISTORICAL":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_36(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = None
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_37(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = None
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_38(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method != "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_39(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "XXfiltered-hsXX":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_40(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "FILTERED-HS":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_41(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = None
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_42(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = None
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_43(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method != "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_44(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "XXmonte-carloXX":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_45(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "MONTE-CARLO":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_46(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = None

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_47(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = None
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_48(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[+len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_49(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = None
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_50(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(None, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_51(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, None, alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_52(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=None)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_53(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_54(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_55(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(
                test_returns,
                var_series[method],
            )
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_56(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = None

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_57(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=None,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_58(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=None,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_59(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=None,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_60(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=None,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_61(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=None,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_62(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_63(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_64(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_65(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            backtest_results=backtest_results,
        )

    def xǁArchExperimentǁrisk_analysis__mutmut_66(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
        )

    xǁArchExperimentǁrisk_analysis__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁArchExperimentǁrisk_analysis__mutmut_1": xǁArchExperimentǁrisk_analysis__mutmut_1,
        "xǁArchExperimentǁrisk_analysis__mutmut_2": xǁArchExperimentǁrisk_analysis__mutmut_2,
        "xǁArchExperimentǁrisk_analysis__mutmut_3": xǁArchExperimentǁrisk_analysis__mutmut_3,
        "xǁArchExperimentǁrisk_analysis__mutmut_4": xǁArchExperimentǁrisk_analysis__mutmut_4,
        "xǁArchExperimentǁrisk_analysis__mutmut_5": xǁArchExperimentǁrisk_analysis__mutmut_5,
        "xǁArchExperimentǁrisk_analysis__mutmut_6": xǁArchExperimentǁrisk_analysis__mutmut_6,
        "xǁArchExperimentǁrisk_analysis__mutmut_7": xǁArchExperimentǁrisk_analysis__mutmut_7,
        "xǁArchExperimentǁrisk_analysis__mutmut_8": xǁArchExperimentǁrisk_analysis__mutmut_8,
        "xǁArchExperimentǁrisk_analysis__mutmut_9": xǁArchExperimentǁrisk_analysis__mutmut_9,
        "xǁArchExperimentǁrisk_analysis__mutmut_10": xǁArchExperimentǁrisk_analysis__mutmut_10,
        "xǁArchExperimentǁrisk_analysis__mutmut_11": xǁArchExperimentǁrisk_analysis__mutmut_11,
        "xǁArchExperimentǁrisk_analysis__mutmut_12": xǁArchExperimentǁrisk_analysis__mutmut_12,
        "xǁArchExperimentǁrisk_analysis__mutmut_13": xǁArchExperimentǁrisk_analysis__mutmut_13,
        "xǁArchExperimentǁrisk_analysis__mutmut_14": xǁArchExperimentǁrisk_analysis__mutmut_14,
        "xǁArchExperimentǁrisk_analysis__mutmut_15": xǁArchExperimentǁrisk_analysis__mutmut_15,
        "xǁArchExperimentǁrisk_analysis__mutmut_16": xǁArchExperimentǁrisk_analysis__mutmut_16,
        "xǁArchExperimentǁrisk_analysis__mutmut_17": xǁArchExperimentǁrisk_analysis__mutmut_17,
        "xǁArchExperimentǁrisk_analysis__mutmut_18": xǁArchExperimentǁrisk_analysis__mutmut_18,
        "xǁArchExperimentǁrisk_analysis__mutmut_19": xǁArchExperimentǁrisk_analysis__mutmut_19,
        "xǁArchExperimentǁrisk_analysis__mutmut_20": xǁArchExperimentǁrisk_analysis__mutmut_20,
        "xǁArchExperimentǁrisk_analysis__mutmut_21": xǁArchExperimentǁrisk_analysis__mutmut_21,
        "xǁArchExperimentǁrisk_analysis__mutmut_22": xǁArchExperimentǁrisk_analysis__mutmut_22,
        "xǁArchExperimentǁrisk_analysis__mutmut_23": xǁArchExperimentǁrisk_analysis__mutmut_23,
        "xǁArchExperimentǁrisk_analysis__mutmut_24": xǁArchExperimentǁrisk_analysis__mutmut_24,
        "xǁArchExperimentǁrisk_analysis__mutmut_25": xǁArchExperimentǁrisk_analysis__mutmut_25,
        "xǁArchExperimentǁrisk_analysis__mutmut_26": xǁArchExperimentǁrisk_analysis__mutmut_26,
        "xǁArchExperimentǁrisk_analysis__mutmut_27": xǁArchExperimentǁrisk_analysis__mutmut_27,
        "xǁArchExperimentǁrisk_analysis__mutmut_28": xǁArchExperimentǁrisk_analysis__mutmut_28,
        "xǁArchExperimentǁrisk_analysis__mutmut_29": xǁArchExperimentǁrisk_analysis__mutmut_29,
        "xǁArchExperimentǁrisk_analysis__mutmut_30": xǁArchExperimentǁrisk_analysis__mutmut_30,
        "xǁArchExperimentǁrisk_analysis__mutmut_31": xǁArchExperimentǁrisk_analysis__mutmut_31,
        "xǁArchExperimentǁrisk_analysis__mutmut_32": xǁArchExperimentǁrisk_analysis__mutmut_32,
        "xǁArchExperimentǁrisk_analysis__mutmut_33": xǁArchExperimentǁrisk_analysis__mutmut_33,
        "xǁArchExperimentǁrisk_analysis__mutmut_34": xǁArchExperimentǁrisk_analysis__mutmut_34,
        "xǁArchExperimentǁrisk_analysis__mutmut_35": xǁArchExperimentǁrisk_analysis__mutmut_35,
        "xǁArchExperimentǁrisk_analysis__mutmut_36": xǁArchExperimentǁrisk_analysis__mutmut_36,
        "xǁArchExperimentǁrisk_analysis__mutmut_37": xǁArchExperimentǁrisk_analysis__mutmut_37,
        "xǁArchExperimentǁrisk_analysis__mutmut_38": xǁArchExperimentǁrisk_analysis__mutmut_38,
        "xǁArchExperimentǁrisk_analysis__mutmut_39": xǁArchExperimentǁrisk_analysis__mutmut_39,
        "xǁArchExperimentǁrisk_analysis__mutmut_40": xǁArchExperimentǁrisk_analysis__mutmut_40,
        "xǁArchExperimentǁrisk_analysis__mutmut_41": xǁArchExperimentǁrisk_analysis__mutmut_41,
        "xǁArchExperimentǁrisk_analysis__mutmut_42": xǁArchExperimentǁrisk_analysis__mutmut_42,
        "xǁArchExperimentǁrisk_analysis__mutmut_43": xǁArchExperimentǁrisk_analysis__mutmut_43,
        "xǁArchExperimentǁrisk_analysis__mutmut_44": xǁArchExperimentǁrisk_analysis__mutmut_44,
        "xǁArchExperimentǁrisk_analysis__mutmut_45": xǁArchExperimentǁrisk_analysis__mutmut_45,
        "xǁArchExperimentǁrisk_analysis__mutmut_46": xǁArchExperimentǁrisk_analysis__mutmut_46,
        "xǁArchExperimentǁrisk_analysis__mutmut_47": xǁArchExperimentǁrisk_analysis__mutmut_47,
        "xǁArchExperimentǁrisk_analysis__mutmut_48": xǁArchExperimentǁrisk_analysis__mutmut_48,
        "xǁArchExperimentǁrisk_analysis__mutmut_49": xǁArchExperimentǁrisk_analysis__mutmut_49,
        "xǁArchExperimentǁrisk_analysis__mutmut_50": xǁArchExperimentǁrisk_analysis__mutmut_50,
        "xǁArchExperimentǁrisk_analysis__mutmut_51": xǁArchExperimentǁrisk_analysis__mutmut_51,
        "xǁArchExperimentǁrisk_analysis__mutmut_52": xǁArchExperimentǁrisk_analysis__mutmut_52,
        "xǁArchExperimentǁrisk_analysis__mutmut_53": xǁArchExperimentǁrisk_analysis__mutmut_53,
        "xǁArchExperimentǁrisk_analysis__mutmut_54": xǁArchExperimentǁrisk_analysis__mutmut_54,
        "xǁArchExperimentǁrisk_analysis__mutmut_55": xǁArchExperimentǁrisk_analysis__mutmut_55,
        "xǁArchExperimentǁrisk_analysis__mutmut_56": xǁArchExperimentǁrisk_analysis__mutmut_56,
        "xǁArchExperimentǁrisk_analysis__mutmut_57": xǁArchExperimentǁrisk_analysis__mutmut_57,
        "xǁArchExperimentǁrisk_analysis__mutmut_58": xǁArchExperimentǁrisk_analysis__mutmut_58,
        "xǁArchExperimentǁrisk_analysis__mutmut_59": xǁArchExperimentǁrisk_analysis__mutmut_59,
        "xǁArchExperimentǁrisk_analysis__mutmut_60": xǁArchExperimentǁrisk_analysis__mutmut_60,
        "xǁArchExperimentǁrisk_analysis__mutmut_61": xǁArchExperimentǁrisk_analysis__mutmut_61,
        "xǁArchExperimentǁrisk_analysis__mutmut_62": xǁArchExperimentǁrisk_analysis__mutmut_62,
        "xǁArchExperimentǁrisk_analysis__mutmut_63": xǁArchExperimentǁrisk_analysis__mutmut_63,
        "xǁArchExperimentǁrisk_analysis__mutmut_64": xǁArchExperimentǁrisk_analysis__mutmut_64,
        "xǁArchExperimentǁrisk_analysis__mutmut_65": xǁArchExperimentǁrisk_analysis__mutmut_65,
        "xǁArchExperimentǁrisk_analysis__mutmut_66": xǁArchExperimentǁrisk_analysis__mutmut_66,
    }
    xǁArchExperimentǁrisk_analysis__mutmut_orig.__name__ = "xǁArchExperimentǁrisk_analysis"

    def save_master_report(
        self,
        path: str,
        theme: str = "professional",
    ) -> None:
        args = [path, theme]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁArchExperimentǁsave_master_report__mutmut_orig"),
            object.__getattribute__(self, "xǁArchExperimentǁsave_master_report__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁArchExperimentǁsave_master_report__mutmut_orig(
        self,
        path: str,
        theme: str = "professional",
    ) -> None:
        """Save a consolidated master report.

        Parameters
        ----------
        path : str
            Output file path (HTML).
        theme : str
            Report theme.
        """
        from archbox.report.report_manager import ReportManager

        manager = ReportManager()
        manager.generate(
            results=self.fitted_models,
            report_type="garch",
            fmt="html",
            theme=theme,
            output_path=path,
        )

    def xǁArchExperimentǁsave_master_report__mutmut_1(
        self,
        path: str,
        theme: str = "XXprofessionalXX",
    ) -> None:
        """Save a consolidated master report.

        Parameters
        ----------
        path : str
            Output file path (HTML).
        theme : str
            Report theme.
        """
        from archbox.report.report_manager import ReportManager

        manager = ReportManager()
        manager.generate(
            results=self.fitted_models,
            report_type="garch",
            fmt="html",
            theme=theme,
            output_path=path,
        )

    def xǁArchExperimentǁsave_master_report__mutmut_2(
        self,
        path: str,
        theme: str = "PROFESSIONAL",
    ) -> None:
        """Save a consolidated master report.

        Parameters
        ----------
        path : str
            Output file path (HTML).
        theme : str
            Report theme.
        """
        from archbox.report.report_manager import ReportManager

        manager = ReportManager()
        manager.generate(
            results=self.fitted_models,
            report_type="garch",
            fmt="html",
            theme=theme,
            output_path=path,
        )

    def xǁArchExperimentǁsave_master_report__mutmut_3(
        self,
        path: str,
        theme: str = "professional",
    ) -> None:
        """Save a consolidated master report.

        Parameters
        ----------
        path : str
            Output file path (HTML).
        theme : str
            Report theme.
        """

        manager = None
        manager.generate(
            results=self.fitted_models,
            report_type="garch",
            fmt="html",
            theme=theme,
            output_path=path,
        )

    def xǁArchExperimentǁsave_master_report__mutmut_4(
        self,
        path: str,
        theme: str = "professional",
    ) -> None:
        """Save a consolidated master report.

        Parameters
        ----------
        path : str
            Output file path (HTML).
        theme : str
            Report theme.
        """
        from archbox.report.report_manager import ReportManager

        manager = ReportManager()
        manager.generate(
            results=None,
            report_type="garch",
            fmt="html",
            theme=theme,
            output_path=path,
        )

    def xǁArchExperimentǁsave_master_report__mutmut_5(
        self,
        path: str,
        theme: str = "professional",
    ) -> None:
        """Save a consolidated master report.

        Parameters
        ----------
        path : str
            Output file path (HTML).
        theme : str
            Report theme.
        """
        from archbox.report.report_manager import ReportManager

        manager = ReportManager()
        manager.generate(
            results=self.fitted_models,
            report_type=None,
            fmt="html",
            theme=theme,
            output_path=path,
        )

    def xǁArchExperimentǁsave_master_report__mutmut_6(
        self,
        path: str,
        theme: str = "professional",
    ) -> None:
        """Save a consolidated master report.

        Parameters
        ----------
        path : str
            Output file path (HTML).
        theme : str
            Report theme.
        """
        from archbox.report.report_manager import ReportManager

        manager = ReportManager()
        manager.generate(
            results=self.fitted_models,
            report_type="garch",
            fmt=None,
            theme=theme,
            output_path=path,
        )

    def xǁArchExperimentǁsave_master_report__mutmut_7(
        self,
        path: str,
        theme: str = "professional",
    ) -> None:
        """Save a consolidated master report.

        Parameters
        ----------
        path : str
            Output file path (HTML).
        theme : str
            Report theme.
        """
        from archbox.report.report_manager import ReportManager

        manager = ReportManager()
        manager.generate(
            results=self.fitted_models,
            report_type="garch",
            fmt="html",
            theme=None,
            output_path=path,
        )

    def xǁArchExperimentǁsave_master_report__mutmut_8(
        self,
        path: str,
        theme: str = "professional",
    ) -> None:
        """Save a consolidated master report.

        Parameters
        ----------
        path : str
            Output file path (HTML).
        theme : str
            Report theme.
        """
        from archbox.report.report_manager import ReportManager

        manager = ReportManager()
        manager.generate(
            results=self.fitted_models,
            report_type="garch",
            fmt="html",
            theme=theme,
            output_path=None,
        )

    def xǁArchExperimentǁsave_master_report__mutmut_9(
        self,
        path: str,
        theme: str = "professional",
    ) -> None:
        """Save a consolidated master report.

        Parameters
        ----------
        path : str
            Output file path (HTML).
        theme : str
            Report theme.
        """
        from archbox.report.report_manager import ReportManager

        manager = ReportManager()
        manager.generate(
            report_type="garch",
            fmt="html",
            theme=theme,
            output_path=path,
        )

    def xǁArchExperimentǁsave_master_report__mutmut_10(
        self,
        path: str,
        theme: str = "professional",
    ) -> None:
        """Save a consolidated master report.

        Parameters
        ----------
        path : str
            Output file path (HTML).
        theme : str
            Report theme.
        """
        from archbox.report.report_manager import ReportManager

        manager = ReportManager()
        manager.generate(
            results=self.fitted_models,
            fmt="html",
            theme=theme,
            output_path=path,
        )

    def xǁArchExperimentǁsave_master_report__mutmut_11(
        self,
        path: str,
        theme: str = "professional",
    ) -> None:
        """Save a consolidated master report.

        Parameters
        ----------
        path : str
            Output file path (HTML).
        theme : str
            Report theme.
        """
        from archbox.report.report_manager import ReportManager

        manager = ReportManager()
        manager.generate(
            results=self.fitted_models,
            report_type="garch",
            theme=theme,
            output_path=path,
        )

    def xǁArchExperimentǁsave_master_report__mutmut_12(
        self,
        path: str,
        theme: str = "professional",
    ) -> None:
        """Save a consolidated master report.

        Parameters
        ----------
        path : str
            Output file path (HTML).
        theme : str
            Report theme.
        """
        from archbox.report.report_manager import ReportManager

        manager = ReportManager()
        manager.generate(
            results=self.fitted_models,
            report_type="garch",
            fmt="html",
            output_path=path,
        )

    def xǁArchExperimentǁsave_master_report__mutmut_13(
        self,
        path: str,
        theme: str = "professional",
    ) -> None:
        """Save a consolidated master report.

        Parameters
        ----------
        path : str
            Output file path (HTML).
        theme : str
            Report theme.
        """
        from archbox.report.report_manager import ReportManager

        manager = ReportManager()
        manager.generate(
            results=self.fitted_models,
            report_type="garch",
            fmt="html",
            theme=theme,
        )

    def xǁArchExperimentǁsave_master_report__mutmut_14(
        self,
        path: str,
        theme: str = "professional",
    ) -> None:
        """Save a consolidated master report.

        Parameters
        ----------
        path : str
            Output file path (HTML).
        theme : str
            Report theme.
        """
        from archbox.report.report_manager import ReportManager

        manager = ReportManager()
        manager.generate(
            results=self.fitted_models,
            report_type="XXgarchXX",
            fmt="html",
            theme=theme,
            output_path=path,
        )

    def xǁArchExperimentǁsave_master_report__mutmut_15(
        self,
        path: str,
        theme: str = "professional",
    ) -> None:
        """Save a consolidated master report.

        Parameters
        ----------
        path : str
            Output file path (HTML).
        theme : str
            Report theme.
        """
        from archbox.report.report_manager import ReportManager

        manager = ReportManager()
        manager.generate(
            results=self.fitted_models,
            report_type="GARCH",
            fmt="html",
            theme=theme,
            output_path=path,
        )

    def xǁArchExperimentǁsave_master_report__mutmut_16(
        self,
        path: str,
        theme: str = "professional",
    ) -> None:
        """Save a consolidated master report.

        Parameters
        ----------
        path : str
            Output file path (HTML).
        theme : str
            Report theme.
        """
        from archbox.report.report_manager import ReportManager

        manager = ReportManager()
        manager.generate(
            results=self.fitted_models,
            report_type="garch",
            fmt="XXhtmlXX",
            theme=theme,
            output_path=path,
        )

    def xǁArchExperimentǁsave_master_report__mutmut_17(
        self,
        path: str,
        theme: str = "professional",
    ) -> None:
        """Save a consolidated master report.

        Parameters
        ----------
        path : str
            Output file path (HTML).
        theme : str
            Report theme.
        """
        from archbox.report.report_manager import ReportManager

        manager = ReportManager()
        manager.generate(
            results=self.fitted_models,
            report_type="garch",
            fmt="HTML",
            theme=theme,
            output_path=path,
        )

    xǁArchExperimentǁsave_master_report__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁArchExperimentǁsave_master_report__mutmut_1": xǁArchExperimentǁsave_master_report__mutmut_1,
        "xǁArchExperimentǁsave_master_report__mutmut_2": xǁArchExperimentǁsave_master_report__mutmut_2,
        "xǁArchExperimentǁsave_master_report__mutmut_3": xǁArchExperimentǁsave_master_report__mutmut_3,
        "xǁArchExperimentǁsave_master_report__mutmut_4": xǁArchExperimentǁsave_master_report__mutmut_4,
        "xǁArchExperimentǁsave_master_report__mutmut_5": xǁArchExperimentǁsave_master_report__mutmut_5,
        "xǁArchExperimentǁsave_master_report__mutmut_6": xǁArchExperimentǁsave_master_report__mutmut_6,
        "xǁArchExperimentǁsave_master_report__mutmut_7": xǁArchExperimentǁsave_master_report__mutmut_7,
        "xǁArchExperimentǁsave_master_report__mutmut_8": xǁArchExperimentǁsave_master_report__mutmut_8,
        "xǁArchExperimentǁsave_master_report__mutmut_9": xǁArchExperimentǁsave_master_report__mutmut_9,
        "xǁArchExperimentǁsave_master_report__mutmut_10": xǁArchExperimentǁsave_master_report__mutmut_10,
        "xǁArchExperimentǁsave_master_report__mutmut_11": xǁArchExperimentǁsave_master_report__mutmut_11,
        "xǁArchExperimentǁsave_master_report__mutmut_12": xǁArchExperimentǁsave_master_report__mutmut_12,
        "xǁArchExperimentǁsave_master_report__mutmut_13": xǁArchExperimentǁsave_master_report__mutmut_13,
        "xǁArchExperimentǁsave_master_report__mutmut_14": xǁArchExperimentǁsave_master_report__mutmut_14,
        "xǁArchExperimentǁsave_master_report__mutmut_15": xǁArchExperimentǁsave_master_report__mutmut_15,
        "xǁArchExperimentǁsave_master_report__mutmut_16": xǁArchExperimentǁsave_master_report__mutmut_16,
        "xǁArchExperimentǁsave_master_report__mutmut_17": xǁArchExperimentǁsave_master_report__mutmut_17,
    }
    xǁArchExperimentǁsave_master_report__mutmut_orig.__name__ = (
        "xǁArchExperimentǁsave_master_report"
    )
