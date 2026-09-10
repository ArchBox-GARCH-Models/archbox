"""Shared test fixtures for multivariate GARCH tests."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from archbox.datasets import load_dataset


def simulate_dcc_returns(
    n: int,
    r_bar: np.ndarray,
    a: float,
    b: float,
    seed: int = 0,
    scale: float = 0.01,
    burn: int = 500,
) -> np.ndarray:
    """Simulate returns from a DCC data-generating process.

    The conditional correlation genuinely moves over time, which is what the
    DCC/DECO estimators are supposed to pick up (a sample drawn from a fixed
    correlation matrix has none, and both models correctly collapse to CCC).

    Parameters
    ----------
    n : int
        Number of observations to return.
    r_bar : ndarray
        Long-run correlation matrix (k, k).
    a, b : float
        DCC parameters (a + b < 1).
    seed : int
        Seed of the random generator.
    scale : float
        Constant volatility applied to each series (realistic return scale).
    burn : int
        Burn-in draws discarded before the sample.

    Returns
    -------
    ndarray
        Simulated returns (n, k).
    """
    rng = np.random.default_rng(seed)
    q_bar = np.asarray(r_bar, dtype=np.float64)
    k = q_bar.shape[0]
    q = q_bar.copy()
    z_prev = np.zeros(k)
    out = np.zeros((n, k))
    for t in range(n + burn):
        q = (1.0 - a - b) * q_bar + a * np.outer(z_prev, z_prev) + b * q
        d = np.sqrt(np.diag(q))
        corr = q / np.outer(d, d)
        z = np.linalg.cholesky(corr) @ rng.standard_normal(k)
        z_prev = z
        if t >= burn:
            out[t - burn] = z * scale
    return out


def simulate_bekk_returns(
    n: int,
    c_mat: np.ndarray,
    a_mat: np.ndarray,
    b_mat: np.ndarray,
    seed: int = 0,
    burn: int = 300,
) -> np.ndarray:
    """Simulate returns from a diagonal/full BEKK process.

    Parameters
    ----------
    n : int
        Number of observations to return.
    c_mat : ndarray
        Lower-triangular constant matrix (k, k).
    a_mat, b_mat : ndarray
        ARCH and GARCH parameter matrices (k, k).
    seed : int
        Seed of the random generator.
    burn : int
        Burn-in draws discarded before the sample.

    Returns
    -------
    ndarray
        Simulated returns (n, k).
    """
    rng = np.random.default_rng(seed)
    k = c_mat.shape[0]
    cc = c_mat @ c_mat.T
    h = cc / max(1.0 - float(np.max(np.diag(a_mat)) ** 2 + np.max(np.diag(b_mat)) ** 2), 1e-3)
    eps = np.zeros(k)
    out = np.zeros((n, k))
    for t in range(n + burn):
        h = cc + a_mat.T @ np.outer(eps, eps) @ a_mat + b_mat.T @ h @ b_mat
        h = 0.5 * (h + h.T)
        eps = np.linalg.cholesky(h) @ rng.standard_normal(k)
        if t >= burn:
            out[t - burn] = eps
    return out


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
def fx_frame(fx_data: pd.DataFrame) -> pd.DataFrame:
    """FX majors returns as a DataFrame with named columns (no date column)."""
    cols = [c for c in fx_data.columns if c != "date"]
    return fx_data[cols].astype(np.float64)


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
    """Generate synthetic returns with a *constant* correlation (500, 3)."""
    n, k = 500, 3
    R = np.array([[1.0, 0.5, -0.3], [0.5, 1.0, 0.1], [-0.3, 0.1, 1.0]])
    L = np.linalg.cholesky(R)
    z = rng.standard_normal((n, k))
    returns = (z @ L.T) * 0.01
    return returns


@pytest.fixture(scope="module")
def dcc_returns() -> np.ndarray:
    """Returns from a DCC process with genuinely time-varying correlation."""
    k = 3
    r_bar = np.full((k, k), 0.4) + 0.6 * np.eye(k)
    return simulate_dcc_returns(1200, r_bar, a=0.05, b=0.90, seed=7)


@pytest.fixture(scope="module")
def bekk_sim_returns() -> np.ndarray:
    """Returns from a diagonal BEKK process (2 series)."""
    c_mat = np.linalg.cholesky(np.array([[1.0, 0.5], [0.5, 1.0]]) * 5e-6)
    return simulate_bekk_returns(800, c_mat, np.diag([0.25, 0.25]), np.diag([0.90, 0.90]), seed=3)


@pytest.fixture
def bekk_returns(rng: np.random.Generator) -> np.ndarray:
    """Returns suitable for BEKK (2 series, 300 obs, constant correlation)."""
    n, k = 300, 2
    R = np.array([[1.0, 0.5], [0.5, 1.0]])
    L = np.linalg.cholesky(R)
    z = rng.standard_normal((n, k))
    return (z @ L.T) * 0.01
