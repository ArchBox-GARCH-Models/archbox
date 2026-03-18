"""Script to generate all synthetic datasets for archbox.

Run once to generate all CSV files:
    python -m archbox.datasets.generate_datasets

All datasets are synthetic but calibrated with realistic parameters.
Seeds are fixed for reproducibility.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from numpy.typing import NDArray

DATA_DIR = Path(__file__).parent / "data"


def _simulate_garch(
    n: int,
    omega: float,
    alpha: float,
    beta: float,
    mu: float,
    seed: int,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Simulate GARCH(1,1) returns."""
    rng = np.random.default_rng(seed)
    sigma2 = np.empty(n)
    returns = np.empty(n)
    sigma2[0] = omega / (1 - alpha - beta)
    for t in range(n):
        if t > 0:
            sigma2[t] = omega + alpha * (returns[t - 1] - mu) ** 2 + beta * sigma2[t - 1]
        z = rng.standard_normal()
        returns[t] = mu + np.sqrt(sigma2[t]) * z
    return returns, sigma2


def generate_ftse100() -> None:
    """Generate FTSE100 synthetic daily returns."""
    n = 2500
    returns, _ = _simulate_garch(n, omega=1.2e-6, alpha=0.09, beta=0.90, mu=0.0003, seed=100)
    dates = pd.bdate_range("2014-01-02", periods=n)
    df = pd.DataFrame({"date": dates.strftime("%Y-%m-%d"), "returns": np.round(returns, 8)})
    df.to_csv(DATA_DIR / "financial" / "ftse100.csv", index=False)
    print(f"FTSE100: {len(df)} obs, mean={returns.mean():.6f}, std={returns.std():.6f}")


def generate_bitcoin() -> None:
    """Generate Bitcoin synthetic daily returns (heavy-tailed)."""
    rng = np.random.default_rng(200)
    n = 2000
    omega = 5e-5
    alpha = 0.15
    beta = 0.80
    mu = 0.001

    sigma2 = np.empty(n)
    returns = np.empty(n)
    sigma2[0] = omega / (1 - alpha - beta)

    for t in range(n):
        if t > 0:
            sigma2[t] = omega + alpha * (returns[t - 1] - mu) ** 2 + beta * sigma2[t - 1]
        # Student-t with df=5 for heavy tails
        z = rng.standard_t(df=5) / np.sqrt(5 / 3)
        returns[t] = mu + np.sqrt(sigma2[t]) * z

    dates = pd.bdate_range("2016-01-04", periods=n)
    df = pd.DataFrame({"date": dates.strftime("%Y-%m-%d"), "returns": np.round(returns, 8)})
    df.to_csv(DATA_DIR / "financial" / "bitcoin.csv", index=False)
    print(f"Bitcoin: {len(df)} obs, mean={returns.mean():.6f}, std={returns.std():.6f}")


def generate_fx_majors() -> None:
    """Generate FX majors synthetic returns (3 correlated series)."""
    rng = np.random.default_rng(300)
    n = 2000
    k = 3  # USD/EUR, USD/GBP, USD/JPY

    # Correlation structure
    corr = np.array(
        [
            [1.0, 0.6, 0.3],
            [0.6, 1.0, 0.4],
            [0.3, 0.4, 1.0],
        ]
    )
    chol = np.linalg.cholesky(corr)

    returns = np.empty((n, k))
    for t in range(n):
        z = chol @ rng.standard_normal(k)
        returns[t] = z * np.array([0.005, 0.006, 0.004])

    dates = pd.bdate_range("2016-01-04", periods=n)
    df = pd.DataFrame(
        {
            "date": dates.strftime("%Y-%m-%d"),
            "usd_eur": np.round(returns[:, 0], 8),
            "usd_gbp": np.round(returns[:, 1], 8),
            "usd_jpy": np.round(returns[:, 2], 8),
        }
    )
    df.to_csv(DATA_DIR / "financial" / "fx_majors.csv", index=False)
    print(f"FX Majors: {len(df)} obs, {k} series")


def generate_sector_indices() -> None:
    """Generate sector indices synthetic returns (5 correlated series)."""
    rng = np.random.default_rng(400)
    n = 2000
    k = 5  # Tech, Health, Finance, Energy, Consumer

    # Correlation structure (market-driven)
    base_corr = 0.4
    corr = np.full((k, k), base_corr)
    np.fill_diagonal(corr, 1.0)
    chol = np.linalg.cholesky(corr)

    returns = np.empty((n, k))
    vols = np.array([0.012, 0.010, 0.011, 0.015, 0.009])
    for t in range(n):
        z = chol @ rng.standard_normal(k)
        returns[t] = z * vols

    dates = pd.bdate_range("2016-01-04", periods=n)
    df = pd.DataFrame(
        {
            "date": dates.strftime("%Y-%m-%d"),
            "tech": np.round(returns[:, 0], 8),
            "health": np.round(returns[:, 1], 8),
            "finance": np.round(returns[:, 2], 8),
            "energy": np.round(returns[:, 3], 8),
            "consumer": np.round(returns[:, 4], 8),
        }
    )
    df.to_csv(DATA_DIR / "financial" / "sector_indices.csv", index=False)
    print(f"Sector Indices: {len(df)} obs, {k} series")


def generate_realized_vol() -> None:
    """Generate realized volatility synthetic data."""
    rng = np.random.default_rng(500)
    n = 2000
    # HAR-RV components
    rv_daily = np.empty(n)
    rv_daily[0] = 1e-4  # initial RV

    for t in range(1, n):
        # HAR: RV_t = c + b_d * RV_{t-1} + b_w * RV_w + b_m * RV_m + eps
        rv_w = np.mean(rv_daily[max(0, t - 5) : t]) if t >= 1 else rv_daily[0]
        rv_m = np.mean(rv_daily[max(0, t - 22) : t]) if t >= 1 else rv_daily[0]
        rv_daily[t] = (
            1e-5 + 0.3 * rv_daily[t - 1] + 0.3 * rv_w + 0.3 * rv_m + rng.standard_normal() * 2e-5
        )
        rv_daily[t] = max(rv_daily[t], 1e-8)

    dates = pd.bdate_range("2016-01-04", periods=n)
    df = pd.DataFrame(
        {
            "date": dates.strftime("%Y-%m-%d"),
            "rv_daily": np.round(rv_daily, 10),
            "rv_weekly": np.round(pd.Series(rv_daily).rolling(5).mean().fillna(rv_daily[0]), 10),
            "rv_monthly": np.round(pd.Series(rv_daily).rolling(22).mean().fillna(rv_daily[0]), 10),
        }
    )
    df.to_csv(DATA_DIR / "financial" / "realized_vol.csv", index=False)
    print(f"Realized Vol: {len(df)} obs")


def generate_us_unemployment() -> None:
    """Generate US unemployment rate synthetic data (monthly)."""
    rng = np.random.default_rng(600)
    n = 300  # 25 years monthly

    unemp = np.empty(n)
    unemp[0] = 5.0

    # Regime-switching: expansion (low, stable) and recession (high, volatile)
    regime = 0  # 0=expansion, 1=recession
    for t in range(1, n):
        if regime == 0:
            unemp[t] = max(3.0, unemp[t - 1] - 0.05 + rng.standard_normal() * 0.1)
            if rng.random() < 0.02:
                regime = 1
        else:
            unemp[t] = min(12.0, unemp[t - 1] + 0.15 + rng.standard_normal() * 0.2)
            if rng.random() < 0.05:
                regime = 0

    dates = pd.date_range("2000-01-01", periods=n, freq="MS")
    df = pd.DataFrame(
        {
            "date": dates.strftime("%Y-%m-%d"),
            "unemployment_rate": np.round(unemp, 2),
        }
    )
    df.to_csv(DATA_DIR / "macro" / "us_unemployment.csv", index=False)
    print(f"US Unemployment: {len(df)} obs")


def generate_industrial_production() -> None:
    """Generate industrial production growth synthetic data (monthly)."""
    rng = np.random.default_rng(700)
    n = 300

    growth = np.empty(n)
    growth[0] = 0.2

    for t in range(1, n):
        # SETAR-like: different dynamics above/below threshold
        if growth[t - 1] > 0:
            growth[t] = 0.1 + 0.3 * growth[t - 1] + rng.standard_normal() * 0.5
        else:
            growth[t] = -0.2 + 0.5 * growth[t - 1] + rng.standard_normal() * 0.8

    dates = pd.date_range("2000-01-01", periods=n, freq="MS")
    df = pd.DataFrame(
        {
            "date": dates.strftime("%Y-%m-%d"),
            "growth": np.round(growth, 4),
        }
    )
    df.to_csv(DATA_DIR / "macro" / "industrial_production.csv", index=False)
    print(f"Industrial Production: {len(df)} obs")


def generate_ibovespa() -> None:
    """Generate IBOVESPA synthetic daily returns."""
    n = 2500
    returns, _ = _simulate_garch(n, omega=3e-6, alpha=0.10, beta=0.88, mu=0.0005, seed=800)
    dates = pd.bdate_range("2014-01-02", periods=n)
    df = pd.DataFrame({"date": dates.strftime("%Y-%m-%d"), "returns": np.round(returns, 8)})
    df.to_csv(DATA_DIR / "brazil" / "ibovespa.csv", index=False)
    print(f"IBOVESPA: {len(df)} obs, mean={returns.mean():.6f}, std={returns.std():.6f}")


def generate_usdbrl() -> None:
    """Generate USD/BRL synthetic daily returns."""
    n = 2500
    returns, _ = _simulate_garch(n, omega=2e-6, alpha=0.12, beta=0.86, mu=0.0002, seed=900)
    dates = pd.bdate_range("2014-01-02", periods=n)
    df = pd.DataFrame({"date": dates.strftime("%Y-%m-%d"), "returns": np.round(returns, 8)})
    df.to_csv(DATA_DIR / "brazil" / "usdbrl.csv", index=False)
    print(f"USD/BRL: {len(df)} obs, mean={returns.mean():.6f}, std={returns.std():.6f}")


def generate_all() -> None:
    """Generate all datasets."""
    print("Generating all archbox datasets...")
    print("=" * 50)
    generate_ftse100()
    generate_bitcoin()
    generate_fx_majors()
    generate_sector_indices()
    generate_realized_vol()
    generate_us_unemployment()
    generate_industrial_production()
    generate_ibovespa()
    generate_usdbrl()
    print("=" * 50)
    print("All datasets generated successfully.")


if __name__ == "__main__":
    generate_all()
