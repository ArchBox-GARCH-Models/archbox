"""Shared test fixtures for multivariate GARCH tests."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from archbox.datasets import load_dataset


@pytest.fixture
def fx_data() -> pd.DataFrame:
    """Load the FX majors dataset."""
    return load_dataset("fx_majors")


@pytest.fixture
def fx_returns(fx_data: pd.DataFrame) -> np.ndarray:
    """FX majors returns as numpy array (T, 3)."""
    cols = [c for c in fx_data.columns if c != "date"]
    return fx_data[cols].to_numpy(dtype=np.float64)


@pytest.fixture
def sector_data() -> pd.DataFrame:
    """Load the sector indices dataset."""
    return load_dataset("sector_indices")


@pytest.fixture
def sector_returns(sector_data: pd.DataFrame) -> np.ndarray:
    """Sector indices returns as numpy array (T, 5)."""
    cols = [c for c in sector_data.columns if c != "date"]
    return sector_data[cols].to_numpy(dtype=np.float64)


@pytest.fixture
def rng() -> np.random.Generator:
    """Seeded random number generator."""
    return np.random.default_rng(42)


@pytest.fixture
def synthetic_returns(rng: np.random.Generator) -> np.ndarray:
    """Generate synthetic correlated returns (500, 3)."""
    n, k = 500, 3
    R = np.array([[1.0, 0.5, -0.3], [0.5, 1.0, 0.1], [-0.3, 0.1, 1.0]])
    L = np.linalg.cholesky(R)
    z = rng.standard_normal((n, k))
    returns = (z @ L.T) * 0.01
    return returns
