"""CLI regime command implementation."""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable
from pathlib import Path
from typing import Annotated, Any, ClassVar

import numpy as np
import pandas as pd

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


def _build_regime_model(model_name: str, data: np.ndarray, args: argparse.Namespace) -> Any:
    args = [model_name, data, args]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x__build_regime_model__mutmut_orig,
        x__build_regime_model__mutmut_mutants,
        args,
        kwargs,
        None,
    )


def x__build_regime_model__mutmut_orig(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=k_regimes)
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_1(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = None
    order = args.order

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=k_regimes)
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_2(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = None

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=k_regimes)
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_3(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name != "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=k_regimes)
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_4(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "XXms-meanXX":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=k_regimes)
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_5(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "MS-MEAN":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=k_regimes)
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_6(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(None, k_regimes=k_regimes)
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_7(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=None)
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_8(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(k_regimes=k_regimes)
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_9(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(
            data,
        )
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_10(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=k_regimes)
    elif model_name != "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_11(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=k_regimes)
    elif model_name == "XXms-arXX":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_12(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=k_regimes)
    elif model_name == "MS-AR":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_13(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=k_regimes)
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(None, k_regimes=k_regimes, order=order)
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_14(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=k_regimes)
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, k_regimes=None, order=order)
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_15(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=k_regimes)
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, k_regimes=k_regimes, order=None)
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_16(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=k_regimes)
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(k_regimes=k_regimes, order=order)
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_17(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=k_regimes)
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, order=order)
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_18(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=k_regimes)
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(
            data,
            k_regimes=k_regimes,
        )
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_19(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=k_regimes)
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, k_regimes=k_regimes, order=order)
    elif model_name != "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_20(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=k_regimes)
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "XXms-varXX":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_21(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=k_regimes)
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "MS-VAR":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_22(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=k_regimes)
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(None, k_regimes=k_regimes, order=order)
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_23(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=k_regimes)
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, k_regimes=None, order=order)
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_24(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=k_regimes)
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, k_regimes=k_regimes, order=None)
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_25(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=k_regimes)
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(k_regimes=k_regimes, order=order)
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_26(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=k_regimes)
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, order=order)
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_27(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=k_regimes)
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(
            data,
            k_regimes=k_regimes,
        )
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_28(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=k_regimes)
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, k_regimes=k_regimes, order=order)
    elif model_name != "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_29(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=k_regimes)
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "XXms-garchXX":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_30(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=k_regimes)
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "MS-GARCH":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_31(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=k_regimes)
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(None, k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_32(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=k_regimes)
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=None)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_33(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=k_regimes)
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_34(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=k_regimes)
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(
            data,
        )
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def x__build_regime_model__mutmut_35(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=k_regimes)
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=k_regimes)
    else:
        msg = None
        raise ValueError(msg)


def x__build_regime_model__mutmut_36(
    model_name: str, data: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=k_regimes)
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(None)


x__build_regime_model__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x__build_regime_model__mutmut_1": x__build_regime_model__mutmut_1,
    "x__build_regime_model__mutmut_2": x__build_regime_model__mutmut_2,
    "x__build_regime_model__mutmut_3": x__build_regime_model__mutmut_3,
    "x__build_regime_model__mutmut_4": x__build_regime_model__mutmut_4,
    "x__build_regime_model__mutmut_5": x__build_regime_model__mutmut_5,
    "x__build_regime_model__mutmut_6": x__build_regime_model__mutmut_6,
    "x__build_regime_model__mutmut_7": x__build_regime_model__mutmut_7,
    "x__build_regime_model__mutmut_8": x__build_regime_model__mutmut_8,
    "x__build_regime_model__mutmut_9": x__build_regime_model__mutmut_9,
    "x__build_regime_model__mutmut_10": x__build_regime_model__mutmut_10,
    "x__build_regime_model__mutmut_11": x__build_regime_model__mutmut_11,
    "x__build_regime_model__mutmut_12": x__build_regime_model__mutmut_12,
    "x__build_regime_model__mutmut_13": x__build_regime_model__mutmut_13,
    "x__build_regime_model__mutmut_14": x__build_regime_model__mutmut_14,
    "x__build_regime_model__mutmut_15": x__build_regime_model__mutmut_15,
    "x__build_regime_model__mutmut_16": x__build_regime_model__mutmut_16,
    "x__build_regime_model__mutmut_17": x__build_regime_model__mutmut_17,
    "x__build_regime_model__mutmut_18": x__build_regime_model__mutmut_18,
    "x__build_regime_model__mutmut_19": x__build_regime_model__mutmut_19,
    "x__build_regime_model__mutmut_20": x__build_regime_model__mutmut_20,
    "x__build_regime_model__mutmut_21": x__build_regime_model__mutmut_21,
    "x__build_regime_model__mutmut_22": x__build_regime_model__mutmut_22,
    "x__build_regime_model__mutmut_23": x__build_regime_model__mutmut_23,
    "x__build_regime_model__mutmut_24": x__build_regime_model__mutmut_24,
    "x__build_regime_model__mutmut_25": x__build_regime_model__mutmut_25,
    "x__build_regime_model__mutmut_26": x__build_regime_model__mutmut_26,
    "x__build_regime_model__mutmut_27": x__build_regime_model__mutmut_27,
    "x__build_regime_model__mutmut_28": x__build_regime_model__mutmut_28,
    "x__build_regime_model__mutmut_29": x__build_regime_model__mutmut_29,
    "x__build_regime_model__mutmut_30": x__build_regime_model__mutmut_30,
    "x__build_regime_model__mutmut_31": x__build_regime_model__mutmut_31,
    "x__build_regime_model__mutmut_32": x__build_regime_model__mutmut_32,
    "x__build_regime_model__mutmut_33": x__build_regime_model__mutmut_33,
    "x__build_regime_model__mutmut_34": x__build_regime_model__mutmut_34,
    "x__build_regime_model__mutmut_35": x__build_regime_model__mutmut_35,
    "x__build_regime_model__mutmut_36": x__build_regime_model__mutmut_36,
}
x__build_regime_model__mutmut_orig.__name__ = "x__build_regime_model"


def run_regime(args: argparse.Namespace) -> None:
    args = [args]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_run_regime__mutmut_orig, x_run_regime__mutmut_mutants, args, kwargs, None
    )


def x_run_regime__mutmut_orig(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_1(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = None
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_2(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(None)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_3(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = None
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_4(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_5(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = None
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_6(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(None)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_7(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(None)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_8(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = None
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_9(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=None)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_10(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(None)

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_11(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = None
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_12(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(None, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_13(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, None, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_14(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, None)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_15(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_16(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_17(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(
        args.model,
        data,
    )
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_18(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(None)
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_19(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.lower()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_20(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = None

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_21(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=None)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_22(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(None)

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_23(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = None

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_24(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "XXmodelXX": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_25(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "MODEL": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_26(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "XXk_regimesXX": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_27(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "K_REGIMES": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_28(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "XXorderXX": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_29(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "ORDER": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_30(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "XXmethodXX": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_31(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "METHOD": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_32(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "XXnobsXX": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_33(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "NOBS": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_34(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(None),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_35(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "XXloglikelihoodXX": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_36(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "LOGLIKELIHOOD": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_37(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(None),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_38(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "XXaicXX": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_39(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "AIC": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_40(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(None),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_41(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "XXbicXX": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_42(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "BIC": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_43(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(None),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_44(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(None, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_45(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, None):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_46(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr("transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_47(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(
        results,
    ):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_48(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "XXtransition_matrixXX"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_49(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "TRANSITION_MATRIX"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_50(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = None
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_51(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["XXtransition_matrixXX"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_52(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["TRANSITION_MATRIX"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_53(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(None, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_54(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, None):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_55(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr("regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_56(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(
        results,
    ):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_57(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "XXregime_paramsXX"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_58(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "REGIME_PARAMS"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_59(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = None

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_60(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["XXregime_paramsXX"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_61(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["REGIME_PARAMS"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_62(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(None) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_63(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = None
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_64(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(None)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_65(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(None)
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_66(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(None, indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_67(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=None, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_68(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=None))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_69(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(indent=2, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_70(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_71(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(
        json.dumps(
            output,
            indent=2,
        )
    )
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_72(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=3, default=str))
    print(f"\nResults saved to {output_path}")


def x_run_regime__mutmut_73(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(None)


x_run_regime__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_run_regime__mutmut_1": x_run_regime__mutmut_1,
    "x_run_regime__mutmut_2": x_run_regime__mutmut_2,
    "x_run_regime__mutmut_3": x_run_regime__mutmut_3,
    "x_run_regime__mutmut_4": x_run_regime__mutmut_4,
    "x_run_regime__mutmut_5": x_run_regime__mutmut_5,
    "x_run_regime__mutmut_6": x_run_regime__mutmut_6,
    "x_run_regime__mutmut_7": x_run_regime__mutmut_7,
    "x_run_regime__mutmut_8": x_run_regime__mutmut_8,
    "x_run_regime__mutmut_9": x_run_regime__mutmut_9,
    "x_run_regime__mutmut_10": x_run_regime__mutmut_10,
    "x_run_regime__mutmut_11": x_run_regime__mutmut_11,
    "x_run_regime__mutmut_12": x_run_regime__mutmut_12,
    "x_run_regime__mutmut_13": x_run_regime__mutmut_13,
    "x_run_regime__mutmut_14": x_run_regime__mutmut_14,
    "x_run_regime__mutmut_15": x_run_regime__mutmut_15,
    "x_run_regime__mutmut_16": x_run_regime__mutmut_16,
    "x_run_regime__mutmut_17": x_run_regime__mutmut_17,
    "x_run_regime__mutmut_18": x_run_regime__mutmut_18,
    "x_run_regime__mutmut_19": x_run_regime__mutmut_19,
    "x_run_regime__mutmut_20": x_run_regime__mutmut_20,
    "x_run_regime__mutmut_21": x_run_regime__mutmut_21,
    "x_run_regime__mutmut_22": x_run_regime__mutmut_22,
    "x_run_regime__mutmut_23": x_run_regime__mutmut_23,
    "x_run_regime__mutmut_24": x_run_regime__mutmut_24,
    "x_run_regime__mutmut_25": x_run_regime__mutmut_25,
    "x_run_regime__mutmut_26": x_run_regime__mutmut_26,
    "x_run_regime__mutmut_27": x_run_regime__mutmut_27,
    "x_run_regime__mutmut_28": x_run_regime__mutmut_28,
    "x_run_regime__mutmut_29": x_run_regime__mutmut_29,
    "x_run_regime__mutmut_30": x_run_regime__mutmut_30,
    "x_run_regime__mutmut_31": x_run_regime__mutmut_31,
    "x_run_regime__mutmut_32": x_run_regime__mutmut_32,
    "x_run_regime__mutmut_33": x_run_regime__mutmut_33,
    "x_run_regime__mutmut_34": x_run_regime__mutmut_34,
    "x_run_regime__mutmut_35": x_run_regime__mutmut_35,
    "x_run_regime__mutmut_36": x_run_regime__mutmut_36,
    "x_run_regime__mutmut_37": x_run_regime__mutmut_37,
    "x_run_regime__mutmut_38": x_run_regime__mutmut_38,
    "x_run_regime__mutmut_39": x_run_regime__mutmut_39,
    "x_run_regime__mutmut_40": x_run_regime__mutmut_40,
    "x_run_regime__mutmut_41": x_run_regime__mutmut_41,
    "x_run_regime__mutmut_42": x_run_regime__mutmut_42,
    "x_run_regime__mutmut_43": x_run_regime__mutmut_43,
    "x_run_regime__mutmut_44": x_run_regime__mutmut_44,
    "x_run_regime__mutmut_45": x_run_regime__mutmut_45,
    "x_run_regime__mutmut_46": x_run_regime__mutmut_46,
    "x_run_regime__mutmut_47": x_run_regime__mutmut_47,
    "x_run_regime__mutmut_48": x_run_regime__mutmut_48,
    "x_run_regime__mutmut_49": x_run_regime__mutmut_49,
    "x_run_regime__mutmut_50": x_run_regime__mutmut_50,
    "x_run_regime__mutmut_51": x_run_regime__mutmut_51,
    "x_run_regime__mutmut_52": x_run_regime__mutmut_52,
    "x_run_regime__mutmut_53": x_run_regime__mutmut_53,
    "x_run_regime__mutmut_54": x_run_regime__mutmut_54,
    "x_run_regime__mutmut_55": x_run_regime__mutmut_55,
    "x_run_regime__mutmut_56": x_run_regime__mutmut_56,
    "x_run_regime__mutmut_57": x_run_regime__mutmut_57,
    "x_run_regime__mutmut_58": x_run_regime__mutmut_58,
    "x_run_regime__mutmut_59": x_run_regime__mutmut_59,
    "x_run_regime__mutmut_60": x_run_regime__mutmut_60,
    "x_run_regime__mutmut_61": x_run_regime__mutmut_61,
    "x_run_regime__mutmut_62": x_run_regime__mutmut_62,
    "x_run_regime__mutmut_63": x_run_regime__mutmut_63,
    "x_run_regime__mutmut_64": x_run_regime__mutmut_64,
    "x_run_regime__mutmut_65": x_run_regime__mutmut_65,
    "x_run_regime__mutmut_66": x_run_regime__mutmut_66,
    "x_run_regime__mutmut_67": x_run_regime__mutmut_67,
    "x_run_regime__mutmut_68": x_run_regime__mutmut_68,
    "x_run_regime__mutmut_69": x_run_regime__mutmut_69,
    "x_run_regime__mutmut_70": x_run_regime__mutmut_70,
    "x_run_regime__mutmut_71": x_run_regime__mutmut_71,
    "x_run_regime__mutmut_72": x_run_regime__mutmut_72,
    "x_run_regime__mutmut_73": x_run_regime__mutmut_73,
}
x_run_regime__mutmut_orig.__name__ = "x_run_regime"
