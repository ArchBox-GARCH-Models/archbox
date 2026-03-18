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


def load_dataset(name: str) -> pd.DataFrame:
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


def list_datasets() -> list[str]:
    """List available dataset names.

    Returns
    -------
    list[str]
        Sorted list of dataset names.
    """
    return sorted(_DATASETS.keys())


def dataset_info(name: str) -> dict[str, Any]:
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
