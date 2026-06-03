"""Data generators for risk management examples.

Generates synthetic financial return series calibrated to real-world assets.
All generators use fixed seeds for perfect reproducibility.
Reuses the same GARCH(1,1) parameters from FASE1 (01_garch_univariate).
"""

import numpy as np
import pandas as pd


def _generate_garch11(
    n: int,
    omega: float,
    alpha: float,
    beta: float,
    mu: float,
    seed: int,
    start_date: str,
    df: float | None = None,
) -> pd.DataFrame:
    """Generate returns from a GARCH(1,1) process.

    Parameters
    ----------
    n : int
        Number of observations.
    omega : float
        Constant in variance equation.
    alpha : float
        ARCH coefficient.
    beta : float
        GARCH coefficient.
    mu : float
        Mean return.
    seed : int
        Random seed for reproducibility.
    start_date : str
        Start date for the business-day index.
    df : float or None
        Degrees of freedom for t-Student innovations. If None, uses normal.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: date, returns.
    """
    rng = np.random.default_rng(seed)
    sigma2 = np.empty(n)
    returns = np.empty(n)
    sigma2[0] = omega / (1 - alpha - beta)

    for t in range(n):
        if t > 0:
            sigma2[t] = omega + alpha * (returns[t - 1] - mu) ** 2 + beta * sigma2[t - 1]
        z = rng.standard_t(df) / np.sqrt(df / (df - 2)) if df is not None else rng.standard_normal()
        returns[t] = mu + np.sqrt(sigma2[t]) * z

    dates = pd.bdate_range(start_date, periods=n)
    return pd.DataFrame(
        {
            "date": dates.strftime("%Y-%m-%d"),
            "returns": np.round(returns, 8),
        }
    )


def generate_garch_returns(n: int = 2500, seed: int = 42) -> pd.DataFrame:
    """Generate synthetic S&P 500 daily returns.

    Calibrated to typical S&P 500 GARCH(1,1) parameters:
    omega=1.5e-6, alpha=0.08, beta=0.91, mu=0.0004.
    Same parameters as FASE1.

    Parameters
    ----------
    n : int
        Number of observations (default 2500).
    seed : int
        Random seed (default 42).

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: date, returns.
    """
    return _generate_garch11(
        n=n,
        omega=1.5e-6,
        alpha=0.08,
        beta=0.91,
        mu=0.0004,
        seed=seed,
        start_date="2014-01-02",
    )


def generate_ibov_returns(n: int = 2500, seed: int = 43) -> pd.DataFrame:
    """Generate synthetic Ibovespa daily returns.

    Calibrated to typical Ibovespa GARCH(1,1) parameters:
    omega=3.0e-6, alpha=0.10, beta=0.88, mu=0.0005.
    Same parameters as FASE1.

    Parameters
    ----------
    n : int
        Number of observations (default 2500).
    seed : int
        Random seed (default 43).

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: date, returns.
    """
    return _generate_garch11(
        n=n,
        omega=3.0e-6,
        alpha=0.10,
        beta=0.88,
        mu=0.0005,
        seed=seed,
        start_date="2014-01-02",
    )


def generate_fat_tail_returns(n: int = 2500, df: int = 5, seed: int = 65) -> pd.DataFrame:
    """Generate returns with fat tails using t-Student innovations.

    Uses GARCH(1,1) with t-Student innovations to demonstrate fat tails
    and the inadequacy of the normal distribution for VaR estimation.

    Parameters
    ----------
    n : int
        Number of observations (default 2500).
    df : int
        Degrees of freedom for t-Student (default 5).
    seed : int
        Random seed (default 65).

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: date, returns.
    """
    return _generate_garch11(
        n=n,
        omega=2.0e-6,
        alpha=0.09,
        beta=0.90,
        mu=0.0003,
        seed=seed,
        start_date="2014-01-02",
        df=df,
    )
