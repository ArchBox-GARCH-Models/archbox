"""Data generators for GARCH univariate examples.

Generates synthetic financial return series calibrated to real-world assets.
All generators use fixed seeds for perfect reproducibility.
"""

import numpy as np
import pandas as pd


def generate_garch11_returns(
    n: int = 2500,
    omega: float = 1.5e-6,
    alpha: float = 0.08,
    beta: float = 0.91,
    mu: float = 0.0004,
    seed: int = 42,
    start_date: str = "2014-01-02",
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

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: date, returns, true_volatility.
    """
    rng = np.random.default_rng(seed)
    sigma2 = np.empty(n)
    returns = np.empty(n)
    sigma2[0] = omega / (1 - alpha - beta)

    for t in range(n):
        if t > 0:
            sigma2[t] = omega + alpha * (returns[t - 1] - mu) ** 2 + beta * sigma2[t - 1]
        z = rng.standard_normal()
        returns[t] = mu + np.sqrt(sigma2[t]) * z

    dates = pd.bdate_range(start_date, periods=n)
    return pd.DataFrame(
        {
            "date": dates.strftime("%Y-%m-%d"),
            "returns": np.round(returns, 8),
            "true_volatility": np.round(np.sqrt(sigma2), 8),
        }
    )


def generate_sp500_returns(seed: int = 42) -> pd.DataFrame:
    """Generate synthetic S&P 500 daily returns.

    Calibrated to typical S&P 500 parameters:
    omega=1.5e-6, alpha=0.08, beta=0.91, mu=0.0004.

    Parameters
    ----------
    seed : int
        Random seed (default 42).

    Returns
    -------
    pd.DataFrame
        2500 observations with columns: date, returns, true_volatility.
    """
    return generate_garch11_returns(
        n=2500,
        omega=1.5e-6,
        alpha=0.08,
        beta=0.91,
        mu=0.0004,
        seed=seed,
        start_date="2014-01-02",
    )


def generate_ibovespa_returns(seed: int = 43) -> pd.DataFrame:
    """Generate synthetic Ibovespa daily returns.

    Calibrated to typical Ibovespa parameters:
    omega=3.0e-6, alpha=0.10, beta=0.88, mu=0.0005.

    Parameters
    ----------
    seed : int
        Random seed (default 43).

    Returns
    -------
    pd.DataFrame
        2500 observations with columns: date, returns, true_volatility.
    """
    return generate_garch11_returns(
        n=2500,
        omega=3.0e-6,
        alpha=0.10,
        beta=0.88,
        mu=0.0005,
        seed=seed,
        start_date="2014-01-02",
    )


def generate_bitcoin_returns(seed: int = 44) -> pd.DataFrame:
    """Generate synthetic Bitcoin daily returns.

    Calibrated to typical Bitcoin parameters:
    omega=1.0e-5, alpha=0.15, beta=0.82, mu=0.001.

    Parameters
    ----------
    seed : int
        Random seed (default 44).

    Returns
    -------
    pd.DataFrame
        2000 observations with columns: date, returns, true_volatility.
    """
    return generate_garch11_returns(
        n=2000,
        omega=1.0e-5,
        alpha=0.15,
        beta=0.82,
        mu=0.001,
        seed=seed,
        start_date="2016-01-04",
    )
