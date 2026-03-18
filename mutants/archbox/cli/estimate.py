"""CLI estimate command implementation."""

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


def _load_data(data_path: str, column: str) -> np.ndarray:
    args = [data_path, column]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x__load_data__mutmut_orig, x__load_data__mutmut_mutants, args, kwargs, None
    )


def x__load_data__mutmut_orig(data_path: str, column: str) -> np.ndarray:
    """Load returns data from CSV file.

    Parameters
    ----------
    data_path : str
        Path to CSV file.
    column : str
        Column name containing returns.

    Returns
    -------
    np.ndarray
        Returns array.
    """
    df = pd.read_csv(data_path)
    if column not in df.columns:
        msg = f"Column '{column}' not found in {data_path}. Available: {list(df.columns)}"
        raise ValueError(msg)
    return df[column].dropna().to_numpy(dtype=np.float64)


def x__load_data__mutmut_1(data_path: str, column: str) -> np.ndarray:
    """Load returns data from CSV file.

    Parameters
    ----------
    data_path : str
        Path to CSV file.
    column : str
        Column name containing returns.

    Returns
    -------
    np.ndarray
        Returns array.
    """
    df = None
    if column not in df.columns:
        msg = f"Column '{column}' not found in {data_path}. Available: {list(df.columns)}"
        raise ValueError(msg)
    return df[column].dropna().to_numpy(dtype=np.float64)


def x__load_data__mutmut_2(data_path: str, column: str) -> np.ndarray:
    """Load returns data from CSV file.

    Parameters
    ----------
    data_path : str
        Path to CSV file.
    column : str
        Column name containing returns.

    Returns
    -------
    np.ndarray
        Returns array.
    """
    df = pd.read_csv(None)
    if column not in df.columns:
        msg = f"Column '{column}' not found in {data_path}. Available: {list(df.columns)}"
        raise ValueError(msg)
    return df[column].dropna().to_numpy(dtype=np.float64)


def x__load_data__mutmut_3(data_path: str, column: str) -> np.ndarray:
    """Load returns data from CSV file.

    Parameters
    ----------
    data_path : str
        Path to CSV file.
    column : str
        Column name containing returns.

    Returns
    -------
    np.ndarray
        Returns array.
    """
    df = pd.read_csv(data_path)
    if column in df.columns:
        msg = f"Column '{column}' not found in {data_path}. Available: {list(df.columns)}"
        raise ValueError(msg)
    return df[column].dropna().to_numpy(dtype=np.float64)


def x__load_data__mutmut_4(data_path: str, column: str) -> np.ndarray:
    """Load returns data from CSV file.

    Parameters
    ----------
    data_path : str
        Path to CSV file.
    column : str
        Column name containing returns.

    Returns
    -------
    np.ndarray
        Returns array.
    """
    df = pd.read_csv(data_path)
    if column not in df.columns:
        msg = None
        raise ValueError(msg)
    return df[column].dropna().to_numpy(dtype=np.float64)


def x__load_data__mutmut_5(data_path: str, column: str) -> np.ndarray:
    """Load returns data from CSV file.

    Parameters
    ----------
    data_path : str
        Path to CSV file.
    column : str
        Column name containing returns.

    Returns
    -------
    np.ndarray
        Returns array.
    """
    df = pd.read_csv(data_path)
    if column not in df.columns:
        msg = f"Column '{column}' not found in {data_path}. Available: {list(None)}"
        raise ValueError(msg)
    return df[column].dropna().to_numpy(dtype=np.float64)


def x__load_data__mutmut_6(data_path: str, column: str) -> np.ndarray:
    """Load returns data from CSV file.

    Parameters
    ----------
    data_path : str
        Path to CSV file.
    column : str
        Column name containing returns.

    Returns
    -------
    np.ndarray
        Returns array.
    """
    df = pd.read_csv(data_path)
    if column not in df.columns:
        msg = f"Column '{column}' not found in {data_path}. Available: {list(df.columns)}"
        raise ValueError(None)
    return df[column].dropna().to_numpy(dtype=np.float64)


def x__load_data__mutmut_7(data_path: str, column: str) -> np.ndarray:
    """Load returns data from CSV file.

    Parameters
    ----------
    data_path : str
        Path to CSV file.
    column : str
        Column name containing returns.

    Returns
    -------
    np.ndarray
        Returns array.
    """
    df = pd.read_csv(data_path)
    if column not in df.columns:
        msg = f"Column '{column}' not found in {data_path}. Available: {list(df.columns)}"
        raise ValueError(msg)
    return df[column].dropna().to_numpy(dtype=None)


x__load_data__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x__load_data__mutmut_1": x__load_data__mutmut_1,
    "x__load_data__mutmut_2": x__load_data__mutmut_2,
    "x__load_data__mutmut_3": x__load_data__mutmut_3,
    "x__load_data__mutmut_4": x__load_data__mutmut_4,
    "x__load_data__mutmut_5": x__load_data__mutmut_5,
    "x__load_data__mutmut_6": x__load_data__mutmut_6,
    "x__load_data__mutmut_7": x__load_data__mutmut_7,
}
x__load_data__mutmut_orig.__name__ = "x__load_data"


def _get_dist_name(dist: str) -> str:
    args = [dist]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x__get_dist_name__mutmut_orig, x__get_dist_name__mutmut_mutants, args, kwargs, None
    )


def x__get_dist_name__mutmut_orig(dist: str) -> str:
    """Map CLI distribution name to archbox distribution name.

    Parameters
    ----------
    dist : str
        CLI distribution name.

    Returns
    -------
    str
        archbox distribution name.
    """
    mapping = {
        "normal": "normal",
        "student-t": "studentt",
        "skewed-t": "skewt",
        "ged": "ged",
    }
    return mapping.get(dist, dist)


def x__get_dist_name__mutmut_1(dist: str) -> str:
    """Map CLI distribution name to archbox distribution name.

    Parameters
    ----------
    dist : str
        CLI distribution name.

    Returns
    -------
    str
        archbox distribution name.
    """
    mapping = None
    return mapping.get(dist, dist)


def x__get_dist_name__mutmut_2(dist: str) -> str:
    """Map CLI distribution name to archbox distribution name.

    Parameters
    ----------
    dist : str
        CLI distribution name.

    Returns
    -------
    str
        archbox distribution name.
    """
    mapping = {
        "XXnormalXX": "normal",
        "student-t": "studentt",
        "skewed-t": "skewt",
        "ged": "ged",
    }
    return mapping.get(dist, dist)


def x__get_dist_name__mutmut_3(dist: str) -> str:
    """Map CLI distribution name to archbox distribution name.

    Parameters
    ----------
    dist : str
        CLI distribution name.

    Returns
    -------
    str
        archbox distribution name.
    """
    mapping = {
        "NORMAL": "normal",
        "student-t": "studentt",
        "skewed-t": "skewt",
        "ged": "ged",
    }
    return mapping.get(dist, dist)


def x__get_dist_name__mutmut_4(dist: str) -> str:
    """Map CLI distribution name to archbox distribution name.

    Parameters
    ----------
    dist : str
        CLI distribution name.

    Returns
    -------
    str
        archbox distribution name.
    """
    mapping = {
        "normal": "XXnormalXX",
        "student-t": "studentt",
        "skewed-t": "skewt",
        "ged": "ged",
    }
    return mapping.get(dist, dist)


def x__get_dist_name__mutmut_5(dist: str) -> str:
    """Map CLI distribution name to archbox distribution name.

    Parameters
    ----------
    dist : str
        CLI distribution name.

    Returns
    -------
    str
        archbox distribution name.
    """
    mapping = {
        "normal": "NORMAL",
        "student-t": "studentt",
        "skewed-t": "skewt",
        "ged": "ged",
    }
    return mapping.get(dist, dist)


def x__get_dist_name__mutmut_6(dist: str) -> str:
    """Map CLI distribution name to archbox distribution name.

    Parameters
    ----------
    dist : str
        CLI distribution name.

    Returns
    -------
    str
        archbox distribution name.
    """
    mapping = {
        "normal": "normal",
        "XXstudent-tXX": "studentt",
        "skewed-t": "skewt",
        "ged": "ged",
    }
    return mapping.get(dist, dist)


def x__get_dist_name__mutmut_7(dist: str) -> str:
    """Map CLI distribution name to archbox distribution name.

    Parameters
    ----------
    dist : str
        CLI distribution name.

    Returns
    -------
    str
        archbox distribution name.
    """
    mapping = {
        "normal": "normal",
        "STUDENT-T": "studentt",
        "skewed-t": "skewt",
        "ged": "ged",
    }
    return mapping.get(dist, dist)


def x__get_dist_name__mutmut_8(dist: str) -> str:
    """Map CLI distribution name to archbox distribution name.

    Parameters
    ----------
    dist : str
        CLI distribution name.

    Returns
    -------
    str
        archbox distribution name.
    """
    mapping = {
        "normal": "normal",
        "student-t": "XXstudenttXX",
        "skewed-t": "skewt",
        "ged": "ged",
    }
    return mapping.get(dist, dist)


def x__get_dist_name__mutmut_9(dist: str) -> str:
    """Map CLI distribution name to archbox distribution name.

    Parameters
    ----------
    dist : str
        CLI distribution name.

    Returns
    -------
    str
        archbox distribution name.
    """
    mapping = {
        "normal": "normal",
        "student-t": "STUDENTT",
        "skewed-t": "skewt",
        "ged": "ged",
    }
    return mapping.get(dist, dist)


def x__get_dist_name__mutmut_10(dist: str) -> str:
    """Map CLI distribution name to archbox distribution name.

    Parameters
    ----------
    dist : str
        CLI distribution name.

    Returns
    -------
    str
        archbox distribution name.
    """
    mapping = {
        "normal": "normal",
        "student-t": "studentt",
        "XXskewed-tXX": "skewt",
        "ged": "ged",
    }
    return mapping.get(dist, dist)


def x__get_dist_name__mutmut_11(dist: str) -> str:
    """Map CLI distribution name to archbox distribution name.

    Parameters
    ----------
    dist : str
        CLI distribution name.

    Returns
    -------
    str
        archbox distribution name.
    """
    mapping = {
        "normal": "normal",
        "student-t": "studentt",
        "SKEWED-T": "skewt",
        "ged": "ged",
    }
    return mapping.get(dist, dist)


def x__get_dist_name__mutmut_12(dist: str) -> str:
    """Map CLI distribution name to archbox distribution name.

    Parameters
    ----------
    dist : str
        CLI distribution name.

    Returns
    -------
    str
        archbox distribution name.
    """
    mapping = {
        "normal": "normal",
        "student-t": "studentt",
        "skewed-t": "XXskewtXX",
        "ged": "ged",
    }
    return mapping.get(dist, dist)


def x__get_dist_name__mutmut_13(dist: str) -> str:
    """Map CLI distribution name to archbox distribution name.

    Parameters
    ----------
    dist : str
        CLI distribution name.

    Returns
    -------
    str
        archbox distribution name.
    """
    mapping = {
        "normal": "normal",
        "student-t": "studentt",
        "skewed-t": "SKEWT",
        "ged": "ged",
    }
    return mapping.get(dist, dist)


def x__get_dist_name__mutmut_14(dist: str) -> str:
    """Map CLI distribution name to archbox distribution name.

    Parameters
    ----------
    dist : str
        CLI distribution name.

    Returns
    -------
    str
        archbox distribution name.
    """
    mapping = {
        "normal": "normal",
        "student-t": "studentt",
        "skewed-t": "skewt",
        "XXgedXX": "ged",
    }
    return mapping.get(dist, dist)


def x__get_dist_name__mutmut_15(dist: str) -> str:
    """Map CLI distribution name to archbox distribution name.

    Parameters
    ----------
    dist : str
        CLI distribution name.

    Returns
    -------
    str
        archbox distribution name.
    """
    mapping = {
        "normal": "normal",
        "student-t": "studentt",
        "skewed-t": "skewt",
        "GED": "ged",
    }
    return mapping.get(dist, dist)


def x__get_dist_name__mutmut_16(dist: str) -> str:
    """Map CLI distribution name to archbox distribution name.

    Parameters
    ----------
    dist : str
        CLI distribution name.

    Returns
    -------
    str
        archbox distribution name.
    """
    mapping = {
        "normal": "normal",
        "student-t": "studentt",
        "skewed-t": "skewt",
        "ged": "XXgedXX",
    }
    return mapping.get(dist, dist)


def x__get_dist_name__mutmut_17(dist: str) -> str:
    """Map CLI distribution name to archbox distribution name.

    Parameters
    ----------
    dist : str
        CLI distribution name.

    Returns
    -------
    str
        archbox distribution name.
    """
    mapping = {
        "normal": "normal",
        "student-t": "studentt",
        "skewed-t": "skewt",
        "ged": "GED",
    }
    return mapping.get(dist, dist)


def x__get_dist_name__mutmut_18(dist: str) -> str:
    """Map CLI distribution name to archbox distribution name.

    Parameters
    ----------
    dist : str
        CLI distribution name.

    Returns
    -------
    str
        archbox distribution name.
    """
    mapping = {
        "normal": "normal",
        "student-t": "studentt",
        "skewed-t": "skewt",
        "ged": "ged",
    }
    return mapping.get(None, dist)


def x__get_dist_name__mutmut_19(dist: str) -> str:
    """Map CLI distribution name to archbox distribution name.

    Parameters
    ----------
    dist : str
        CLI distribution name.

    Returns
    -------
    str
        archbox distribution name.
    """
    mapping = {
        "normal": "normal",
        "student-t": "studentt",
        "skewed-t": "skewt",
        "ged": "ged",
    }
    return mapping.get(dist)


def x__get_dist_name__mutmut_20(dist: str) -> str:
    """Map CLI distribution name to archbox distribution name.

    Parameters
    ----------
    dist : str
        CLI distribution name.

    Returns
    -------
    str
        archbox distribution name.
    """
    mapping = {
        "normal": "normal",
        "student-t": "studentt",
        "skewed-t": "skewt",
        "ged": "ged",
    }
    return mapping.get(dist)


def x__get_dist_name__mutmut_21(dist: str) -> str:
    """Map CLI distribution name to archbox distribution name.

    Parameters
    ----------
    dist : str
        CLI distribution name.

    Returns
    -------
    str
        archbox distribution name.
    """
    mapping = {
        "normal": "normal",
        "student-t": "studentt",
        "skewed-t": "skewt",
        "ged": "ged",
    }
    return mapping.get(
        dist,
    )


x__get_dist_name__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x__get_dist_name__mutmut_1": x__get_dist_name__mutmut_1,
    "x__get_dist_name__mutmut_2": x__get_dist_name__mutmut_2,
    "x__get_dist_name__mutmut_3": x__get_dist_name__mutmut_3,
    "x__get_dist_name__mutmut_4": x__get_dist_name__mutmut_4,
    "x__get_dist_name__mutmut_5": x__get_dist_name__mutmut_5,
    "x__get_dist_name__mutmut_6": x__get_dist_name__mutmut_6,
    "x__get_dist_name__mutmut_7": x__get_dist_name__mutmut_7,
    "x__get_dist_name__mutmut_8": x__get_dist_name__mutmut_8,
    "x__get_dist_name__mutmut_9": x__get_dist_name__mutmut_9,
    "x__get_dist_name__mutmut_10": x__get_dist_name__mutmut_10,
    "x__get_dist_name__mutmut_11": x__get_dist_name__mutmut_11,
    "x__get_dist_name__mutmut_12": x__get_dist_name__mutmut_12,
    "x__get_dist_name__mutmut_13": x__get_dist_name__mutmut_13,
    "x__get_dist_name__mutmut_14": x__get_dist_name__mutmut_14,
    "x__get_dist_name__mutmut_15": x__get_dist_name__mutmut_15,
    "x__get_dist_name__mutmut_16": x__get_dist_name__mutmut_16,
    "x__get_dist_name__mutmut_17": x__get_dist_name__mutmut_17,
    "x__get_dist_name__mutmut_18": x__get_dist_name__mutmut_18,
    "x__get_dist_name__mutmut_19": x__get_dist_name__mutmut_19,
    "x__get_dist_name__mutmut_20": x__get_dist_name__mutmut_20,
    "x__get_dist_name__mutmut_21": x__get_dist_name__mutmut_21,
}
x__get_dist_name__mutmut_orig.__name__ = "x__get_dist_name"


def _build_model(model_name: str, returns: np.ndarray, args: argparse.Namespace) -> Any:
    args = [model_name, returns, args]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x__build_model__mutmut_orig, x__build_model__mutmut_mutants, args, kwargs, None
    )


def x__build_model__mutmut_orig(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_1(model_name: str, returns: np.ndarray, args: argparse.Namespace) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = None
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_2(model_name: str, returns: np.ndarray, args: argparse.Namespace) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(None)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_3(model_name: str, returns: np.ndarray, args: argparse.Namespace) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = None

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_4(model_name: str, returns: np.ndarray, args: argparse.Namespace) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(None, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_5(model_name: str, returns: np.ndarray, args: argparse.Namespace) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, None, "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_6(model_name: str, returns: np.ndarray, args: argparse.Namespace) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", None)

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_7(model_name: str, returns: np.ndarray, args: argparse.Namespace) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = ("mean").constant

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_8(model_name: str, returns: np.ndarray, args: argparse.Namespace) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = args.constant

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_9(model_name: str, returns: np.ndarray, args: argparse.Namespace) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = args.mean

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_10(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "XXmeanXX", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_11(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "MEAN", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_12(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "XXconstantXX")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_13(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "CONSTANT")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_14(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name != "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_15(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "XXgarchXX":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_16(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "GARCH":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_17(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(None, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_18(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=None, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_19(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=None, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_20(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=None, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_21(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=None)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_22(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_23(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_24(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_25(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_26(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(
            returns,
            p=args.p,
            q=args.q,
            dist=dist,
        )
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_27(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name != "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_28(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "XXegarchXX":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_29(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "EGARCH":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_30(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(None, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_31(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=None, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_32(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=None, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_33(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=None, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_34(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=None)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_35(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_36(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_37(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_38(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_39(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(
            returns,
            p=args.p,
            q=args.q,
            dist=dist,
        )
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_40(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name != "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_41(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "XXgjrXX":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_42(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "GJR":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_43(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(None, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_44(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=None, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_45(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=None, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_46(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=None, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_47(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=None)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_48(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_49(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_50(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_51(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_52(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(
            returns,
            p=args.p,
            q=args.q,
            dist=dist,
        )
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_53(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name != "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_54(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "XXaparchXX":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_55(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "APARCH":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_56(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(None, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_57(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=None, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_58(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=None, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_59(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=None, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_60(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=None)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_61(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_62(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_63(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_64(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_65(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(
            returns,
            p=args.p,
            q=args.q,
            dist=dist,
        )
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_66(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name != "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_67(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "XXfigarchXX":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_68(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "FIGARCH":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_69(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(None, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_70(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=None, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_71(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=None)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_72(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_73(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_74(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(
            returns,
            dist=dist,
        )
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_75(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name != "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_76(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "XXigarchXX":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_77(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "IGARCH":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_78(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(None, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_79(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=None, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_80(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=None)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_81(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_82(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_83(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(
            returns,
            dist=dist,
        )
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_84(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name != "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_85(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "XXgarch-mXX":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_86(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "GARCH-M":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_87(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(None, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_88(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=None, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_89(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=None, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_90(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=None, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_91(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=None)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_92(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_93(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_94(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_95(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_96(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(
            returns,
            p=args.p,
            q=args.q,
            dist=dist,
        )
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_97(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name != "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_98(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "XXcomponentXX":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_99(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "COMPONENT":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_100(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(None, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_101(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=None, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_102(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=None)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_103(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_104(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_105(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(
            returns,
            dist=dist,
        )
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_106(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name != "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_107(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "XXhar-rvXX":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_108(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "HAR-RV":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_109(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(None)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def x__build_model__mutmut_110(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = None
        raise ValueError(msg)


def x__build_model__mutmut_111(
    model_name: str, returns: np.ndarray, args: argparse.Namespace
) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(None)


x__build_model__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x__build_model__mutmut_1": x__build_model__mutmut_1,
    "x__build_model__mutmut_2": x__build_model__mutmut_2,
    "x__build_model__mutmut_3": x__build_model__mutmut_3,
    "x__build_model__mutmut_4": x__build_model__mutmut_4,
    "x__build_model__mutmut_5": x__build_model__mutmut_5,
    "x__build_model__mutmut_6": x__build_model__mutmut_6,
    "x__build_model__mutmut_7": x__build_model__mutmut_7,
    "x__build_model__mutmut_8": x__build_model__mutmut_8,
    "x__build_model__mutmut_9": x__build_model__mutmut_9,
    "x__build_model__mutmut_10": x__build_model__mutmut_10,
    "x__build_model__mutmut_11": x__build_model__mutmut_11,
    "x__build_model__mutmut_12": x__build_model__mutmut_12,
    "x__build_model__mutmut_13": x__build_model__mutmut_13,
    "x__build_model__mutmut_14": x__build_model__mutmut_14,
    "x__build_model__mutmut_15": x__build_model__mutmut_15,
    "x__build_model__mutmut_16": x__build_model__mutmut_16,
    "x__build_model__mutmut_17": x__build_model__mutmut_17,
    "x__build_model__mutmut_18": x__build_model__mutmut_18,
    "x__build_model__mutmut_19": x__build_model__mutmut_19,
    "x__build_model__mutmut_20": x__build_model__mutmut_20,
    "x__build_model__mutmut_21": x__build_model__mutmut_21,
    "x__build_model__mutmut_22": x__build_model__mutmut_22,
    "x__build_model__mutmut_23": x__build_model__mutmut_23,
    "x__build_model__mutmut_24": x__build_model__mutmut_24,
    "x__build_model__mutmut_25": x__build_model__mutmut_25,
    "x__build_model__mutmut_26": x__build_model__mutmut_26,
    "x__build_model__mutmut_27": x__build_model__mutmut_27,
    "x__build_model__mutmut_28": x__build_model__mutmut_28,
    "x__build_model__mutmut_29": x__build_model__mutmut_29,
    "x__build_model__mutmut_30": x__build_model__mutmut_30,
    "x__build_model__mutmut_31": x__build_model__mutmut_31,
    "x__build_model__mutmut_32": x__build_model__mutmut_32,
    "x__build_model__mutmut_33": x__build_model__mutmut_33,
    "x__build_model__mutmut_34": x__build_model__mutmut_34,
    "x__build_model__mutmut_35": x__build_model__mutmut_35,
    "x__build_model__mutmut_36": x__build_model__mutmut_36,
    "x__build_model__mutmut_37": x__build_model__mutmut_37,
    "x__build_model__mutmut_38": x__build_model__mutmut_38,
    "x__build_model__mutmut_39": x__build_model__mutmut_39,
    "x__build_model__mutmut_40": x__build_model__mutmut_40,
    "x__build_model__mutmut_41": x__build_model__mutmut_41,
    "x__build_model__mutmut_42": x__build_model__mutmut_42,
    "x__build_model__mutmut_43": x__build_model__mutmut_43,
    "x__build_model__mutmut_44": x__build_model__mutmut_44,
    "x__build_model__mutmut_45": x__build_model__mutmut_45,
    "x__build_model__mutmut_46": x__build_model__mutmut_46,
    "x__build_model__mutmut_47": x__build_model__mutmut_47,
    "x__build_model__mutmut_48": x__build_model__mutmut_48,
    "x__build_model__mutmut_49": x__build_model__mutmut_49,
    "x__build_model__mutmut_50": x__build_model__mutmut_50,
    "x__build_model__mutmut_51": x__build_model__mutmut_51,
    "x__build_model__mutmut_52": x__build_model__mutmut_52,
    "x__build_model__mutmut_53": x__build_model__mutmut_53,
    "x__build_model__mutmut_54": x__build_model__mutmut_54,
    "x__build_model__mutmut_55": x__build_model__mutmut_55,
    "x__build_model__mutmut_56": x__build_model__mutmut_56,
    "x__build_model__mutmut_57": x__build_model__mutmut_57,
    "x__build_model__mutmut_58": x__build_model__mutmut_58,
    "x__build_model__mutmut_59": x__build_model__mutmut_59,
    "x__build_model__mutmut_60": x__build_model__mutmut_60,
    "x__build_model__mutmut_61": x__build_model__mutmut_61,
    "x__build_model__mutmut_62": x__build_model__mutmut_62,
    "x__build_model__mutmut_63": x__build_model__mutmut_63,
    "x__build_model__mutmut_64": x__build_model__mutmut_64,
    "x__build_model__mutmut_65": x__build_model__mutmut_65,
    "x__build_model__mutmut_66": x__build_model__mutmut_66,
    "x__build_model__mutmut_67": x__build_model__mutmut_67,
    "x__build_model__mutmut_68": x__build_model__mutmut_68,
    "x__build_model__mutmut_69": x__build_model__mutmut_69,
    "x__build_model__mutmut_70": x__build_model__mutmut_70,
    "x__build_model__mutmut_71": x__build_model__mutmut_71,
    "x__build_model__mutmut_72": x__build_model__mutmut_72,
    "x__build_model__mutmut_73": x__build_model__mutmut_73,
    "x__build_model__mutmut_74": x__build_model__mutmut_74,
    "x__build_model__mutmut_75": x__build_model__mutmut_75,
    "x__build_model__mutmut_76": x__build_model__mutmut_76,
    "x__build_model__mutmut_77": x__build_model__mutmut_77,
    "x__build_model__mutmut_78": x__build_model__mutmut_78,
    "x__build_model__mutmut_79": x__build_model__mutmut_79,
    "x__build_model__mutmut_80": x__build_model__mutmut_80,
    "x__build_model__mutmut_81": x__build_model__mutmut_81,
    "x__build_model__mutmut_82": x__build_model__mutmut_82,
    "x__build_model__mutmut_83": x__build_model__mutmut_83,
    "x__build_model__mutmut_84": x__build_model__mutmut_84,
    "x__build_model__mutmut_85": x__build_model__mutmut_85,
    "x__build_model__mutmut_86": x__build_model__mutmut_86,
    "x__build_model__mutmut_87": x__build_model__mutmut_87,
    "x__build_model__mutmut_88": x__build_model__mutmut_88,
    "x__build_model__mutmut_89": x__build_model__mutmut_89,
    "x__build_model__mutmut_90": x__build_model__mutmut_90,
    "x__build_model__mutmut_91": x__build_model__mutmut_91,
    "x__build_model__mutmut_92": x__build_model__mutmut_92,
    "x__build_model__mutmut_93": x__build_model__mutmut_93,
    "x__build_model__mutmut_94": x__build_model__mutmut_94,
    "x__build_model__mutmut_95": x__build_model__mutmut_95,
    "x__build_model__mutmut_96": x__build_model__mutmut_96,
    "x__build_model__mutmut_97": x__build_model__mutmut_97,
    "x__build_model__mutmut_98": x__build_model__mutmut_98,
    "x__build_model__mutmut_99": x__build_model__mutmut_99,
    "x__build_model__mutmut_100": x__build_model__mutmut_100,
    "x__build_model__mutmut_101": x__build_model__mutmut_101,
    "x__build_model__mutmut_102": x__build_model__mutmut_102,
    "x__build_model__mutmut_103": x__build_model__mutmut_103,
    "x__build_model__mutmut_104": x__build_model__mutmut_104,
    "x__build_model__mutmut_105": x__build_model__mutmut_105,
    "x__build_model__mutmut_106": x__build_model__mutmut_106,
    "x__build_model__mutmut_107": x__build_model__mutmut_107,
    "x__build_model__mutmut_108": x__build_model__mutmut_108,
    "x__build_model__mutmut_109": x__build_model__mutmut_109,
    "x__build_model__mutmut_110": x__build_model__mutmut_110,
    "x__build_model__mutmut_111": x__build_model__mutmut_111,
}
x__build_model__mutmut_orig.__name__ = "x__build_model"


def run_estimate(args: argparse.Namespace) -> None:
    args = [args]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_run_estimate__mutmut_orig, x_run_estimate__mutmut_mutants, args, kwargs, None
    )


def x_run_estimate__mutmut_orig(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_1(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = None
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_2(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(None, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_3(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, None)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_4(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_5(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(
        args.data,
    )
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_6(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(None)

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_7(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = None
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_8(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(None, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_9(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, None, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_10(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, None)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_11(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_12(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_13(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(
        args.model,
        returns,
    )
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_14(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = None

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_15(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(None, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_16(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, None, False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_17(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", None)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_18(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr("variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_19(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_20(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = args.variance_targeting

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_21(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "XXvariance_targetingXX", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_22(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "VARIANCE_TARGETING", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_23(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", True)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_24(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(None)
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_25(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.lower()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_26(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = None

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_27(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=None)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_28(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(None)

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_29(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = None

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_30(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "XXmodelXX": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_31(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "MODEL": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_32(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "XXpXX": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_33(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "P": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_34(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "XXqXX": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_35(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "Q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_36(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "XXdistributionXX": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_37(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "DISTRIBUTION": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_38(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "XXnobsXX": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_39(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "NOBS": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_40(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(None),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_41(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "XXparametersXX": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_42(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "PARAMETERS": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_43(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(None)
            for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_44(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {name: float(val) for name, val in zip(None, results.params, strict=False)},
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_45(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, None, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_46(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=None)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_47(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {name: float(val) for name, val in zip(results.params, strict=False)},
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_48(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {name: float(val) for name, val in zip(results.param_names, strict=False)},
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_49(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val)
            for name, val in zip(
                results.param_names,
                results.params,
                strict=False,
            )
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_50(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=True)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_51(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "XXloglikelihoodXX": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_52(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "LOGLIKELIHOOD": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_53(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(None),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_54(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "XXaicXX": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_55(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "AIC": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_56(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(None),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_57(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "XXbicXX": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_58(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "BIC": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_59(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(None),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_60(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "XXpersistenceXX": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_61(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "PERSISTENCE": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_62(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(None),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_63(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = None
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_64(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(None)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_65(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(None)
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_66(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(None, indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_67(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=None))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_68(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(indent=2))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_69(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(
        json.dumps(
            output,
        )
    )
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_70(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=3))
    print(f"\nResults saved to {output_path}")


def x_run_estimate__mutmut_71(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(None)


x_run_estimate__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_run_estimate__mutmut_1": x_run_estimate__mutmut_1,
    "x_run_estimate__mutmut_2": x_run_estimate__mutmut_2,
    "x_run_estimate__mutmut_3": x_run_estimate__mutmut_3,
    "x_run_estimate__mutmut_4": x_run_estimate__mutmut_4,
    "x_run_estimate__mutmut_5": x_run_estimate__mutmut_5,
    "x_run_estimate__mutmut_6": x_run_estimate__mutmut_6,
    "x_run_estimate__mutmut_7": x_run_estimate__mutmut_7,
    "x_run_estimate__mutmut_8": x_run_estimate__mutmut_8,
    "x_run_estimate__mutmut_9": x_run_estimate__mutmut_9,
    "x_run_estimate__mutmut_10": x_run_estimate__mutmut_10,
    "x_run_estimate__mutmut_11": x_run_estimate__mutmut_11,
    "x_run_estimate__mutmut_12": x_run_estimate__mutmut_12,
    "x_run_estimate__mutmut_13": x_run_estimate__mutmut_13,
    "x_run_estimate__mutmut_14": x_run_estimate__mutmut_14,
    "x_run_estimate__mutmut_15": x_run_estimate__mutmut_15,
    "x_run_estimate__mutmut_16": x_run_estimate__mutmut_16,
    "x_run_estimate__mutmut_17": x_run_estimate__mutmut_17,
    "x_run_estimate__mutmut_18": x_run_estimate__mutmut_18,
    "x_run_estimate__mutmut_19": x_run_estimate__mutmut_19,
    "x_run_estimate__mutmut_20": x_run_estimate__mutmut_20,
    "x_run_estimate__mutmut_21": x_run_estimate__mutmut_21,
    "x_run_estimate__mutmut_22": x_run_estimate__mutmut_22,
    "x_run_estimate__mutmut_23": x_run_estimate__mutmut_23,
    "x_run_estimate__mutmut_24": x_run_estimate__mutmut_24,
    "x_run_estimate__mutmut_25": x_run_estimate__mutmut_25,
    "x_run_estimate__mutmut_26": x_run_estimate__mutmut_26,
    "x_run_estimate__mutmut_27": x_run_estimate__mutmut_27,
    "x_run_estimate__mutmut_28": x_run_estimate__mutmut_28,
    "x_run_estimate__mutmut_29": x_run_estimate__mutmut_29,
    "x_run_estimate__mutmut_30": x_run_estimate__mutmut_30,
    "x_run_estimate__mutmut_31": x_run_estimate__mutmut_31,
    "x_run_estimate__mutmut_32": x_run_estimate__mutmut_32,
    "x_run_estimate__mutmut_33": x_run_estimate__mutmut_33,
    "x_run_estimate__mutmut_34": x_run_estimate__mutmut_34,
    "x_run_estimate__mutmut_35": x_run_estimate__mutmut_35,
    "x_run_estimate__mutmut_36": x_run_estimate__mutmut_36,
    "x_run_estimate__mutmut_37": x_run_estimate__mutmut_37,
    "x_run_estimate__mutmut_38": x_run_estimate__mutmut_38,
    "x_run_estimate__mutmut_39": x_run_estimate__mutmut_39,
    "x_run_estimate__mutmut_40": x_run_estimate__mutmut_40,
    "x_run_estimate__mutmut_41": x_run_estimate__mutmut_41,
    "x_run_estimate__mutmut_42": x_run_estimate__mutmut_42,
    "x_run_estimate__mutmut_43": x_run_estimate__mutmut_43,
    "x_run_estimate__mutmut_44": x_run_estimate__mutmut_44,
    "x_run_estimate__mutmut_45": x_run_estimate__mutmut_45,
    "x_run_estimate__mutmut_46": x_run_estimate__mutmut_46,
    "x_run_estimate__mutmut_47": x_run_estimate__mutmut_47,
    "x_run_estimate__mutmut_48": x_run_estimate__mutmut_48,
    "x_run_estimate__mutmut_49": x_run_estimate__mutmut_49,
    "x_run_estimate__mutmut_50": x_run_estimate__mutmut_50,
    "x_run_estimate__mutmut_51": x_run_estimate__mutmut_51,
    "x_run_estimate__mutmut_52": x_run_estimate__mutmut_52,
    "x_run_estimate__mutmut_53": x_run_estimate__mutmut_53,
    "x_run_estimate__mutmut_54": x_run_estimate__mutmut_54,
    "x_run_estimate__mutmut_55": x_run_estimate__mutmut_55,
    "x_run_estimate__mutmut_56": x_run_estimate__mutmut_56,
    "x_run_estimate__mutmut_57": x_run_estimate__mutmut_57,
    "x_run_estimate__mutmut_58": x_run_estimate__mutmut_58,
    "x_run_estimate__mutmut_59": x_run_estimate__mutmut_59,
    "x_run_estimate__mutmut_60": x_run_estimate__mutmut_60,
    "x_run_estimate__mutmut_61": x_run_estimate__mutmut_61,
    "x_run_estimate__mutmut_62": x_run_estimate__mutmut_62,
    "x_run_estimate__mutmut_63": x_run_estimate__mutmut_63,
    "x_run_estimate__mutmut_64": x_run_estimate__mutmut_64,
    "x_run_estimate__mutmut_65": x_run_estimate__mutmut_65,
    "x_run_estimate__mutmut_66": x_run_estimate__mutmut_66,
    "x_run_estimate__mutmut_67": x_run_estimate__mutmut_67,
    "x_run_estimate__mutmut_68": x_run_estimate__mutmut_68,
    "x_run_estimate__mutmut_69": x_run_estimate__mutmut_69,
    "x_run_estimate__mutmut_70": x_run_estimate__mutmut_70,
    "x_run_estimate__mutmut_71": x_run_estimate__mutmut_71,
}
x_run_estimate__mutmut_orig.__name__ = "x_run_estimate"
