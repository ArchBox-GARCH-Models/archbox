"""Consolidated data loader for complete workflow examples.

Loads datasets from other example modules or generates them on the fly.
Falls back to local copies in the data/ directory if module datasets
are not available.
"""

import contextlib
from pathlib import Path

import pandas as pd

EXAMPLES_DIR = Path(__file__).parent.parent.parent
LOCAL_DATA_DIR = Path(__file__).parent.parent / "data"


def _load_csv(primary: Path, fallback: Path) -> pd.DataFrame:
    """Load CSV from primary path, falling back to local copy."""
    path = primary if primary.exists() else fallback
    df = pd.read_csv(path)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date", inplace=True)
    return df


def load_sp500() -> pd.DataFrame:
    """Load SP500 returns from FASE1 data."""
    return _load_csv(
        EXAMPLES_DIR / "01_garch_univariate/data/sp500_returns.csv",
        LOCAL_DATA_DIR / "sp500_returns.csv",
    )


def load_ibovespa() -> pd.DataFrame:
    """Load Ibovespa returns from FASE1 data."""
    return _load_csv(
        EXAMPLES_DIR / "01_garch_univariate/data/ibovespa_returns.csv",
        LOCAL_DATA_DIR / "ibovespa_returns.csv",
    )


def load_bitcoin() -> pd.DataFrame:
    """Load Bitcoin returns from FASE1 data."""
    return _load_csv(
        EXAMPLES_DIR / "01_garch_univariate/data/bitcoin_returns.csv",
        LOCAL_DATA_DIR / "bitcoin_returns.csv",
    )


def load_fx_majors() -> pd.DataFrame:
    """Load FX majors returns from FASE3 data."""
    return _load_csv(
        EXAMPLES_DIR / "03_multivariate/data/fx_majors.csv",
        LOCAL_DATA_DIR / "fx_majors.csv",
    )


def load_sector_indices() -> pd.DataFrame:
    """Load sector indices returns from FASE3 data."""
    return _load_csv(
        EXAMPLES_DIR / "03_multivariate/data/sector_indices.csv",
        LOCAL_DATA_DIR / "sector_indices.csv",
    )


def load_realized_volatility() -> pd.DataFrame:
    """Load realized volatility from FASE2 data."""
    return _load_csv(
        EXAMPLES_DIR / "02_garch_advanced/data/realized_volatility.csv",
        LOCAL_DATA_DIR / "realized_volatility.csv",
    )


def load_all_datasets() -> dict:
    """Load all available datasets as a dictionary."""
    loaders = {
        "sp500": load_sp500,
        "ibovespa": load_ibovespa,
        "bitcoin": load_bitcoin,
        "fx_majors": load_fx_majors,
        "sector_indices": load_sector_indices,
        "realized_volatility": load_realized_volatility,
    }
    datasets = {}
    for name, loader in loaders.items():
        with contextlib.suppress(FileNotFoundError):
            datasets[name] = loader()
    return datasets
