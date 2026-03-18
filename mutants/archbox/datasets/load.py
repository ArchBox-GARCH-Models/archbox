"""Dataset loading utilities."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

_DATA_DIR = Path(__file__).parent / "data"

_DATASETS: dict[str, dict[str, Any]] = {
    "sp500": {
        "path": "financial/sp500.csv",
        "description": "S&P 500 daily returns, synthetic calibrated (n=2500)",
    },
    "ftse100": {
        "path": "financial/ftse100.csv",
        "description": "FTSE 100 daily returns, synthetic calibrated (n=2500)",
    },
    "bitcoin": {
        "path": "financial/bitcoin.csv",
        "description": "Bitcoin daily returns, synthetic heavy-tailed (n=2000)",
    },
    "fx_majors": {
        "path": "financial/fx_majors.csv",
        "description": "FX majors (USD/EUR, USD/GBP, USD/JPY), synthetic correlated (n=2000)",
    },
    "sector_indices": {
        "path": "financial/sector_indices.csv",
        "description": "Sector indices (5 sectors), synthetic correlated (n=2000)",
    },
    "realized_vol": {
        "path": "financial/realized_vol.csv",
        "description": "Realized volatility (daily, weekly, monthly), synthetic HAR-RV (n=2000)",
    },
    "us_gdp": {
        "path": "macro/us_gdp_quarterly.csv",
        "description": "US GDP quarterly growth, synthetic regime-switching (n=200)",
    },
    "us_unemployment": {
        "path": "macro/us_unemployment.csv",
        "description": "US unemployment rate monthly, synthetic regime-switching (n=300)",
    },
    "industrial_production": {
        "path": "macro/industrial_production.csv",
        "description": "Industrial production growth monthly, synthetic SETAR (n=300)",
    },
    "ibovespa": {
        "path": "brazil/ibovespa.csv",
        "description": "IBOVESPA daily returns, synthetic calibrated (n=2500)",
    },
    "usdbrl": {
        "path": "brazil/usdbrl.csv",
        "description": "USD/BRL daily returns, synthetic calibrated (n=2500)",
    },
}
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


def load_dataset(name: str) -> pd.DataFrame:
    args = [name]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_load_dataset__mutmut_orig, x_load_dataset__mutmut_mutants, args, kwargs, None
    )


def x_load_dataset__mutmut_orig(name: str) -> pd.DataFrame:
    """Load a built-in dataset by name.

    Parameters
    ----------
    name : str
        Dataset name.

    Returns
    -------
    pd.DataFrame
        DataFrame with the dataset.

    Raises
    ------
    ValueError
        If dataset name is not recognized.
    """
    if name not in _DATASETS:
        available = ", ".join(sorted(_DATASETS.keys()))
        msg = f"Unknown dataset '{name}'. Available: {available}"
        raise ValueError(msg)

    info = _DATASETS[name]
    path = _DATA_DIR / info["path"]

    if not path.exists():
        msg = (
            f"Dataset file not found: {path}. "
            f"Run 'python -m archbox.datasets.generate_datasets' to generate datasets."
        )
        raise FileNotFoundError(msg)

    return pd.read_csv(path)


def x_load_dataset__mutmut_1(name: str) -> pd.DataFrame:
    """Load a built-in dataset by name.

    Parameters
    ----------
    name : str
        Dataset name.

    Returns
    -------
    pd.DataFrame
        DataFrame with the dataset.

    Raises
    ------
    ValueError
        If dataset name is not recognized.
    """
    if name in _DATASETS:
        available = ", ".join(sorted(_DATASETS.keys()))
        msg = f"Unknown dataset '{name}'. Available: {available}"
        raise ValueError(msg)

    info = _DATASETS[name]
    path = _DATA_DIR / info["path"]

    if not path.exists():
        msg = (
            f"Dataset file not found: {path}. "
            f"Run 'python -m archbox.datasets.generate_datasets' to generate datasets."
        )
        raise FileNotFoundError(msg)

    return pd.read_csv(path)


def x_load_dataset__mutmut_2(name: str) -> pd.DataFrame:
    """Load a built-in dataset by name.

    Parameters
    ----------
    name : str
        Dataset name.

    Returns
    -------
    pd.DataFrame
        DataFrame with the dataset.

    Raises
    ------
    ValueError
        If dataset name is not recognized.
    """
    if name not in _DATASETS:
        available = None
        msg = f"Unknown dataset '{name}'. Available: {available}"
        raise ValueError(msg)

    info = _DATASETS[name]
    path = _DATA_DIR / info["path"]

    if not path.exists():
        msg = (
            f"Dataset file not found: {path}. "
            f"Run 'python -m archbox.datasets.generate_datasets' to generate datasets."
        )
        raise FileNotFoundError(msg)

    return pd.read_csv(path)


def x_load_dataset__mutmut_3(name: str) -> pd.DataFrame:
    """Load a built-in dataset by name.

    Parameters
    ----------
    name : str
        Dataset name.

    Returns
    -------
    pd.DataFrame
        DataFrame with the dataset.

    Raises
    ------
    ValueError
        If dataset name is not recognized.
    """
    if name not in _DATASETS:
        available = ", ".join(None)
        msg = f"Unknown dataset '{name}'. Available: {available}"
        raise ValueError(msg)

    info = _DATASETS[name]
    path = _DATA_DIR / info["path"]

    if not path.exists():
        msg = (
            f"Dataset file not found: {path}. "
            f"Run 'python -m archbox.datasets.generate_datasets' to generate datasets."
        )
        raise FileNotFoundError(msg)

    return pd.read_csv(path)


def x_load_dataset__mutmut_4(name: str) -> pd.DataFrame:
    """Load a built-in dataset by name.

    Parameters
    ----------
    name : str
        Dataset name.

    Returns
    -------
    pd.DataFrame
        DataFrame with the dataset.

    Raises
    ------
    ValueError
        If dataset name is not recognized.
    """
    if name not in _DATASETS:
        available = "XX, XX".join(sorted(_DATASETS.keys()))
        msg = f"Unknown dataset '{name}'. Available: {available}"
        raise ValueError(msg)

    info = _DATASETS[name]
    path = _DATA_DIR / info["path"]

    if not path.exists():
        msg = (
            f"Dataset file not found: {path}. "
            f"Run 'python -m archbox.datasets.generate_datasets' to generate datasets."
        )
        raise FileNotFoundError(msg)

    return pd.read_csv(path)


def x_load_dataset__mutmut_5(name: str) -> pd.DataFrame:
    """Load a built-in dataset by name.

    Parameters
    ----------
    name : str
        Dataset name.

    Returns
    -------
    pd.DataFrame
        DataFrame with the dataset.

    Raises
    ------
    ValueError
        If dataset name is not recognized.
    """
    if name not in _DATASETS:
        available = ", ".join(sorted(None))
        msg = f"Unknown dataset '{name}'. Available: {available}"
        raise ValueError(msg)

    info = _DATASETS[name]
    path = _DATA_DIR / info["path"]

    if not path.exists():
        msg = (
            f"Dataset file not found: {path}. "
            f"Run 'python -m archbox.datasets.generate_datasets' to generate datasets."
        )
        raise FileNotFoundError(msg)

    return pd.read_csv(path)


def x_load_dataset__mutmut_6(name: str) -> pd.DataFrame:
    """Load a built-in dataset by name.

    Parameters
    ----------
    name : str
        Dataset name.

    Returns
    -------
    pd.DataFrame
        DataFrame with the dataset.

    Raises
    ------
    ValueError
        If dataset name is not recognized.
    """
    if name not in _DATASETS:
        available = ", ".join(sorted(_DATASETS.keys()))
        msg = None
        raise ValueError(msg)

    info = _DATASETS[name]
    path = _DATA_DIR / info["path"]

    if not path.exists():
        msg = (
            f"Dataset file not found: {path}. "
            f"Run 'python -m archbox.datasets.generate_datasets' to generate datasets."
        )
        raise FileNotFoundError(msg)

    return pd.read_csv(path)


def x_load_dataset__mutmut_7(name: str) -> pd.DataFrame:
    """Load a built-in dataset by name.

    Parameters
    ----------
    name : str
        Dataset name.

    Returns
    -------
    pd.DataFrame
        DataFrame with the dataset.

    Raises
    ------
    ValueError
        If dataset name is not recognized.
    """
    if name not in _DATASETS:
        available = ", ".join(sorted(_DATASETS.keys()))
        msg = f"Unknown dataset '{name}'. Available: {available}"
        raise ValueError(None)

    info = _DATASETS[name]
    path = _DATA_DIR / info["path"]

    if not path.exists():
        msg = (
            f"Dataset file not found: {path}. "
            f"Run 'python -m archbox.datasets.generate_datasets' to generate datasets."
        )
        raise FileNotFoundError(msg)

    return pd.read_csv(path)


def x_load_dataset__mutmut_8(name: str) -> pd.DataFrame:
    """Load a built-in dataset by name.

    Parameters
    ----------
    name : str
        Dataset name.

    Returns
    -------
    pd.DataFrame
        DataFrame with the dataset.

    Raises
    ------
    ValueError
        If dataset name is not recognized.
    """
    if name not in _DATASETS:
        available = ", ".join(sorted(_DATASETS.keys()))
        msg = f"Unknown dataset '{name}'. Available: {available}"
        raise ValueError(msg)

    info = None
    path = _DATA_DIR / info["path"]

    if not path.exists():
        msg = (
            f"Dataset file not found: {path}. "
            f"Run 'python -m archbox.datasets.generate_datasets' to generate datasets."
        )
        raise FileNotFoundError(msg)

    return pd.read_csv(path)


def x_load_dataset__mutmut_9(name: str) -> pd.DataFrame:
    """Load a built-in dataset by name.

    Parameters
    ----------
    name : str
        Dataset name.

    Returns
    -------
    pd.DataFrame
        DataFrame with the dataset.

    Raises
    ------
    ValueError
        If dataset name is not recognized.
    """
    if name not in _DATASETS:
        available = ", ".join(sorted(_DATASETS.keys()))
        msg = f"Unknown dataset '{name}'. Available: {available}"
        raise ValueError(msg)

    info = _DATASETS[name]
    path = None

    if not path.exists():
        msg = (
            f"Dataset file not found: {path}. "
            f"Run 'python -m archbox.datasets.generate_datasets' to generate datasets."
        )
        raise FileNotFoundError(msg)

    return pd.read_csv(path)


def x_load_dataset__mutmut_10(name: str) -> pd.DataFrame:
    """Load a built-in dataset by name.

    Parameters
    ----------
    name : str
        Dataset name.

    Returns
    -------
    pd.DataFrame
        DataFrame with the dataset.

    Raises
    ------
    ValueError
        If dataset name is not recognized.
    """
    if name not in _DATASETS:
        available = ", ".join(sorted(_DATASETS.keys()))
        msg = f"Unknown dataset '{name}'. Available: {available}"
        raise ValueError(msg)

    info = _DATASETS[name]
    path = _DATA_DIR * info["path"]

    if not path.exists():
        msg = (
            f"Dataset file not found: {path}. "
            f"Run 'python -m archbox.datasets.generate_datasets' to generate datasets."
        )
        raise FileNotFoundError(msg)

    return pd.read_csv(path)


def x_load_dataset__mutmut_11(name: str) -> pd.DataFrame:
    """Load a built-in dataset by name.

    Parameters
    ----------
    name : str
        Dataset name.

    Returns
    -------
    pd.DataFrame
        DataFrame with the dataset.

    Raises
    ------
    ValueError
        If dataset name is not recognized.
    """
    if name not in _DATASETS:
        available = ", ".join(sorted(_DATASETS.keys()))
        msg = f"Unknown dataset '{name}'. Available: {available}"
        raise ValueError(msg)

    info = _DATASETS[name]
    path = _DATA_DIR / info["XXpathXX"]

    if not path.exists():
        msg = (
            f"Dataset file not found: {path}. "
            f"Run 'python -m archbox.datasets.generate_datasets' to generate datasets."
        )
        raise FileNotFoundError(msg)

    return pd.read_csv(path)


def x_load_dataset__mutmut_12(name: str) -> pd.DataFrame:
    """Load a built-in dataset by name.

    Parameters
    ----------
    name : str
        Dataset name.

    Returns
    -------
    pd.DataFrame
        DataFrame with the dataset.

    Raises
    ------
    ValueError
        If dataset name is not recognized.
    """
    if name not in _DATASETS:
        available = ", ".join(sorted(_DATASETS.keys()))
        msg = f"Unknown dataset '{name}'. Available: {available}"
        raise ValueError(msg)

    info = _DATASETS[name]
    path = _DATA_DIR / info["PATH"]

    if not path.exists():
        msg = (
            f"Dataset file not found: {path}. "
            f"Run 'python -m archbox.datasets.generate_datasets' to generate datasets."
        )
        raise FileNotFoundError(msg)

    return pd.read_csv(path)


def x_load_dataset__mutmut_13(name: str) -> pd.DataFrame:
    """Load a built-in dataset by name.

    Parameters
    ----------
    name : str
        Dataset name.

    Returns
    -------
    pd.DataFrame
        DataFrame with the dataset.

    Raises
    ------
    ValueError
        If dataset name is not recognized.
    """
    if name not in _DATASETS:
        available = ", ".join(sorted(_DATASETS.keys()))
        msg = f"Unknown dataset '{name}'. Available: {available}"
        raise ValueError(msg)

    info = _DATASETS[name]
    path = _DATA_DIR / info["path"]

    if path.exists():
        msg = (
            f"Dataset file not found: {path}. "
            f"Run 'python -m archbox.datasets.generate_datasets' to generate datasets."
        )
        raise FileNotFoundError(msg)

    return pd.read_csv(path)


def x_load_dataset__mutmut_14(name: str) -> pd.DataFrame:
    """Load a built-in dataset by name.

    Parameters
    ----------
    name : str
        Dataset name.

    Returns
    -------
    pd.DataFrame
        DataFrame with the dataset.

    Raises
    ------
    ValueError
        If dataset name is not recognized.
    """
    if name not in _DATASETS:
        available = ", ".join(sorted(_DATASETS.keys()))
        msg = f"Unknown dataset '{name}'. Available: {available}"
        raise ValueError(msg)

    info = _DATASETS[name]
    path = _DATA_DIR / info["path"]

    if not path.exists():
        msg = None
        raise FileNotFoundError(msg)

    return pd.read_csv(path)


def x_load_dataset__mutmut_15(name: str) -> pd.DataFrame:
    """Load a built-in dataset by name.

    Parameters
    ----------
    name : str
        Dataset name.

    Returns
    -------
    pd.DataFrame
        DataFrame with the dataset.

    Raises
    ------
    ValueError
        If dataset name is not recognized.
    """
    if name not in _DATASETS:
        available = ", ".join(sorted(_DATASETS.keys()))
        msg = f"Unknown dataset '{name}'. Available: {available}"
        raise ValueError(msg)

    info = _DATASETS[name]
    path = _DATA_DIR / info["path"]

    if not path.exists():
        msg = (
            f"Dataset file not found: {path}. "
            f"Run 'python -m archbox.datasets.generate_datasets' to generate datasets."
        )
        raise FileNotFoundError(None)

    return pd.read_csv(path)


def x_load_dataset__mutmut_16(name: str) -> pd.DataFrame:
    """Load a built-in dataset by name.

    Parameters
    ----------
    name : str
        Dataset name.

    Returns
    -------
    pd.DataFrame
        DataFrame with the dataset.

    Raises
    ------
    ValueError
        If dataset name is not recognized.
    """
    if name not in _DATASETS:
        available = ", ".join(sorted(_DATASETS.keys()))
        msg = f"Unknown dataset '{name}'. Available: {available}"
        raise ValueError(msg)

    info = _DATASETS[name]
    path = _DATA_DIR / info["path"]

    if not path.exists():
        msg = (
            f"Dataset file not found: {path}. "
            f"Run 'python -m archbox.datasets.generate_datasets' to generate datasets."
        )
        raise FileNotFoundError(msg)

    return pd.read_csv(None)


x_load_dataset__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_load_dataset__mutmut_1": x_load_dataset__mutmut_1,
    "x_load_dataset__mutmut_2": x_load_dataset__mutmut_2,
    "x_load_dataset__mutmut_3": x_load_dataset__mutmut_3,
    "x_load_dataset__mutmut_4": x_load_dataset__mutmut_4,
    "x_load_dataset__mutmut_5": x_load_dataset__mutmut_5,
    "x_load_dataset__mutmut_6": x_load_dataset__mutmut_6,
    "x_load_dataset__mutmut_7": x_load_dataset__mutmut_7,
    "x_load_dataset__mutmut_8": x_load_dataset__mutmut_8,
    "x_load_dataset__mutmut_9": x_load_dataset__mutmut_9,
    "x_load_dataset__mutmut_10": x_load_dataset__mutmut_10,
    "x_load_dataset__mutmut_11": x_load_dataset__mutmut_11,
    "x_load_dataset__mutmut_12": x_load_dataset__mutmut_12,
    "x_load_dataset__mutmut_13": x_load_dataset__mutmut_13,
    "x_load_dataset__mutmut_14": x_load_dataset__mutmut_14,
    "x_load_dataset__mutmut_15": x_load_dataset__mutmut_15,
    "x_load_dataset__mutmut_16": x_load_dataset__mutmut_16,
}
x_load_dataset__mutmut_orig.__name__ = "x_load_dataset"


def list_datasets() -> list[str]:
    args = []  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_list_datasets__mutmut_orig, x_list_datasets__mutmut_mutants, args, kwargs, None
    )


def x_list_datasets__mutmut_orig() -> list[str]:
    """List available dataset names.

    Returns
    -------
    list[str]
        Sorted list of dataset names.
    """
    return sorted(_DATASETS.keys())


def x_list_datasets__mutmut_1() -> list[str]:
    """List available dataset names.

    Returns
    -------
    list[str]
        Sorted list of dataset names.
    """
    return sorted(None)


x_list_datasets__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_list_datasets__mutmut_1": x_list_datasets__mutmut_1
}
x_list_datasets__mutmut_orig.__name__ = "x_list_datasets"


def dataset_info(name: str) -> dict[str, Any]:
    args = [name]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_dataset_info__mutmut_orig, x_dataset_info__mutmut_mutants, args, kwargs, None
    )


def x_dataset_info__mutmut_orig(name: str) -> dict[str, Any]:
    """Get information about a dataset.

    Parameters
    ----------
    name : str
        Dataset name.

    Returns
    -------
    dict
        Dataset information including path and description.
    """
    if name not in _DATASETS:
        available = ", ".join(sorted(_DATASETS.keys()))
        msg = f"Unknown dataset '{name}'. Available: {available}"
        raise ValueError(msg)
    return _DATASETS[name].copy()


def x_dataset_info__mutmut_1(name: str) -> dict[str, Any]:
    """Get information about a dataset.

    Parameters
    ----------
    name : str
        Dataset name.

    Returns
    -------
    dict
        Dataset information including path and description.
    """
    if name in _DATASETS:
        available = ", ".join(sorted(_DATASETS.keys()))
        msg = f"Unknown dataset '{name}'. Available: {available}"
        raise ValueError(msg)
    return _DATASETS[name].copy()


def x_dataset_info__mutmut_2(name: str) -> dict[str, Any]:
    """Get information about a dataset.

    Parameters
    ----------
    name : str
        Dataset name.

    Returns
    -------
    dict
        Dataset information including path and description.
    """
    if name not in _DATASETS:
        available = None
        msg = f"Unknown dataset '{name}'. Available: {available}"
        raise ValueError(msg)
    return _DATASETS[name].copy()


def x_dataset_info__mutmut_3(name: str) -> dict[str, Any]:
    """Get information about a dataset.

    Parameters
    ----------
    name : str
        Dataset name.

    Returns
    -------
    dict
        Dataset information including path and description.
    """
    if name not in _DATASETS:
        available = ", ".join(None)
        msg = f"Unknown dataset '{name}'. Available: {available}"
        raise ValueError(msg)
    return _DATASETS[name].copy()


def x_dataset_info__mutmut_4(name: str) -> dict[str, Any]:
    """Get information about a dataset.

    Parameters
    ----------
    name : str
        Dataset name.

    Returns
    -------
    dict
        Dataset information including path and description.
    """
    if name not in _DATASETS:
        available = "XX, XX".join(sorted(_DATASETS.keys()))
        msg = f"Unknown dataset '{name}'. Available: {available}"
        raise ValueError(msg)
    return _DATASETS[name].copy()


def x_dataset_info__mutmut_5(name: str) -> dict[str, Any]:
    """Get information about a dataset.

    Parameters
    ----------
    name : str
        Dataset name.

    Returns
    -------
    dict
        Dataset information including path and description.
    """
    if name not in _DATASETS:
        available = ", ".join(sorted(None))
        msg = f"Unknown dataset '{name}'. Available: {available}"
        raise ValueError(msg)
    return _DATASETS[name].copy()


def x_dataset_info__mutmut_6(name: str) -> dict[str, Any]:
    """Get information about a dataset.

    Parameters
    ----------
    name : str
        Dataset name.

    Returns
    -------
    dict
        Dataset information including path and description.
    """
    if name not in _DATASETS:
        available = ", ".join(sorted(_DATASETS.keys()))
        msg = None
        raise ValueError(msg)
    return _DATASETS[name].copy()


def x_dataset_info__mutmut_7(name: str) -> dict[str, Any]:
    """Get information about a dataset.

    Parameters
    ----------
    name : str
        Dataset name.

    Returns
    -------
    dict
        Dataset information including path and description.
    """
    if name not in _DATASETS:
        available = ", ".join(sorted(_DATASETS.keys()))
        msg = f"Unknown dataset '{name}'. Available: {available}"
        raise ValueError(None)
    return _DATASETS[name].copy()


x_dataset_info__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_dataset_info__mutmut_1": x_dataset_info__mutmut_1,
    "x_dataset_info__mutmut_2": x_dataset_info__mutmut_2,
    "x_dataset_info__mutmut_3": x_dataset_info__mutmut_3,
    "x_dataset_info__mutmut_4": x_dataset_info__mutmut_4,
    "x_dataset_info__mutmut_5": x_dataset_info__mutmut_5,
    "x_dataset_info__mutmut_6": x_dataset_info__mutmut_6,
    "x_dataset_info__mutmut_7": x_dataset_info__mutmut_7,
}
x_dataset_info__mutmut_orig.__name__ = "x_dataset_info"
