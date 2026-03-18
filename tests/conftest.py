"""Shared test fixtures for archbox."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from archbox.datasets import load_dataset


@pytest.fixture
def sp500_data() -> pd.DataFrame:
    """Load the SP500 dataset."""
    return load_dataset("sp500")


@pytest.fixture
def sp500_returns(sp500_data: pd.DataFrame) -> np.ndarray:
    """SP500 returns as numpy array."""
    return sp500_data["returns"].to_numpy(dtype=np.float64)


@pytest.fixture
def rng() -> np.random.Generator:
    """Seeded random number generator."""
    return np.random.default_rng(42)
