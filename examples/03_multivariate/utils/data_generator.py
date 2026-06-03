"""
Data generators for multivariate GARCH examples.

Generates synthetic datasets:
- fx_majors.csv: DCC-simulated returns for EUR/USD, GBP/USD, JPY/USD, CHF/USD
- sector_indices.csv: Correlated returns for Technology, Finance, Healthcare, Energy, Consumer
"""

import numpy as np
import pandas as pd


def generate_dcc_returns(n: int = 2000, k: int = 4, seed: int = 50) -> pd.DataFrame:
    """
    Simulate DCC-GARCH(1,1) returns for 4 FX pairs.

    The DCC model (Engle 2002) generates time-varying correlations via:
        Q_t = (1 - a - b) * Q_bar + a * (e_{t-1} e_{t-1}') + b * Q_{t-1}
        R_t = diag(Q_t)^{-1/2} Q_t diag(Q_t)^{-1/2}

    Each marginal series follows GARCH(1,1):
        sigma^2_t = omega + alpha * eps^2_{t-1} + beta * sigma^2_{t-1}

    Parameters
    ----------
    n : int
        Number of observations (default 2000).
    k : int
        Number of series (default 4, should be 4 for FX).
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: date, eurusd, gbpusd, jpyusd, chfusd
    """
    rng = np.random.default_rng(seed)

    # Unconditional correlation matrix calibrated to real FX pairs
    # EUR/USD and CHF/USD are highly correlated (~0.85)
    # EUR/USD and GBP/USD moderately correlated (~0.60)
    # JPY/USD has lower correlation with European currencies
    Q_bar = np.array(
        [
            [1.00, 0.60, 0.25, 0.85],  # EUR/USD
            [0.60, 1.00, 0.20, 0.50],  # GBP/USD
            [0.25, 0.20, 1.00, 0.30],  # JPY/USD
            [0.85, 0.50, 0.30, 1.00],  # CHF/USD
        ]
    )

    # DCC parameters
    a = 0.02
    b = 0.95

    # GARCH(1,1) parameters for each series
    # omega, alpha, beta
    garch_params = np.array(
        [
            [0.00001, 0.06, 0.92],  # EUR/USD
            [0.00001, 0.07, 0.91],  # GBP/USD
            [0.00002, 0.08, 0.90],  # JPY/USD
            [0.00001, 0.05, 0.93],  # CHF/USD
        ]
    )

    # Initialize
    sigma2 = np.zeros((n, k))  # conditional variances
    eps = np.zeros((n, k))  # returns
    e = np.zeros((n, k))  # standardized residuals

    # Initial variances (unconditional)
    for i in range(k):
        omega, alpha, beta = garch_params[i]
        sigma2[0, i] = omega / (1.0 - alpha - beta)

    # Initialize Q
    Q_t = Q_bar.copy()

    for t in range(n):
        # Compute R_t from Q_t
        d = np.sqrt(np.diag(Q_t))
        d_inv = np.diag(1.0 / d)
        R_t = d_inv @ Q_t @ d_inv

        # Ensure R_t is valid correlation matrix
        np.fill_diagonal(R_t, 1.0)

        # Cholesky decomposition of R_t
        try:
            L = np.linalg.cholesky(R_t)
        except np.linalg.LinAlgError:
            # Fallback: use unconditional correlation
            L = np.linalg.cholesky(Q_bar)

        # Generate correlated standard normal innovations
        z = rng.standard_normal(k)
        e[t] = L @ z

        # Scale by conditional standard deviations
        eps[t] = e[t] * np.sqrt(sigma2[t])

        # Update GARCH variances for next period
        if t < n - 1:
            for i in range(k):
                omega, alpha, beta = garch_params[i]
                sigma2[t + 1, i] = omega + alpha * eps[t, i] ** 2 + beta * sigma2[t, i]

        # Update DCC Q for next period
        if t < n - 1:
            Q_t = (1 - a - b) * Q_bar + a * np.outer(e[t], e[t]) + b * Q_t

    # Create date index (business days)
    dates = pd.bdate_range(start="2016-01-04", periods=n)

    df = pd.DataFrame(
        eps,
        columns=["eurusd", "gbpusd", "jpyusd", "chfusd"],
    )
    df.insert(0, "date", dates.strftime("%Y-%m-%d"))

    return df


def generate_sector_returns(n: int = 2000, k: int = 5, seed: int = 51) -> pd.DataFrame:
    """
    Simulate correlated sector index returns with heterogeneous volatility.

    Uses a DCC-like process with sector-specific volatility levels:
    - Technology: high volatility
    - Finance: medium-high volatility
    - Healthcare: medium volatility
    - Energy: high volatility
    - Consumer: low volatility

    Correlations are higher between related sectors (e.g., Tech-Finance)
    and lower between unrelated ones (e.g., Healthcare-Energy).

    Parameters
    ----------
    n : int
        Number of observations (default 2000).
    k : int
        Number of series (default 5).
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: date, technology, finance, healthcare, energy, consumer
    """
    rng = np.random.default_rng(seed)

    # Unconditional correlation matrix for sectors
    Q_bar = np.array(
        [
            [1.00, 0.65, 0.35, 0.30, 0.45],  # Technology
            [0.65, 1.00, 0.40, 0.50, 0.55],  # Finance
            [0.35, 0.40, 1.00, 0.20, 0.50],  # Healthcare
            [0.30, 0.50, 0.20, 1.00, 0.35],  # Energy
            [0.45, 0.55, 0.50, 0.35, 1.00],  # Consumer
        ]
    )

    # DCC parameters
    a = 0.03
    b = 0.94

    # GARCH(1,1) parameters: omega, alpha, beta
    # Different volatility levels per sector
    garch_params = np.array(
        [
            [0.000015, 0.08, 0.90],  # Technology (high vol)
            [0.000012, 0.07, 0.91],  # Finance (medium-high)
            [0.000008, 0.05, 0.93],  # Healthcare (medium)
            [0.000018, 0.09, 0.89],  # Energy (high vol)
            [0.000006, 0.04, 0.94],  # Consumer (low vol)
        ]
    )

    # Initialize
    sigma2 = np.zeros((n, k))
    eps = np.zeros((n, k))
    e = np.zeros((n, k))

    for i in range(k):
        omega, alpha, beta = garch_params[i]
        sigma2[0, i] = omega / (1.0 - alpha - beta)

    Q_t = Q_bar.copy()

    for t in range(n):
        d = np.sqrt(np.diag(Q_t))
        d_inv = np.diag(1.0 / d)
        R_t = d_inv @ Q_t @ d_inv
        np.fill_diagonal(R_t, 1.0)

        try:
            L = np.linalg.cholesky(R_t)
        except np.linalg.LinAlgError:
            L = np.linalg.cholesky(Q_bar)

        z = rng.standard_normal(k)
        e[t] = L @ z
        eps[t] = e[t] * np.sqrt(sigma2[t])

        if t < n - 1:
            for i in range(k):
                omega, alpha, beta = garch_params[i]
                sigma2[t + 1, i] = omega + alpha * eps[t, i] ** 2 + beta * sigma2[t, i]
            Q_t = (1 - a - b) * Q_bar + a * np.outer(e[t], e[t]) + b * Q_t

    dates = pd.bdate_range(start="2016-01-04", periods=n)

    df = pd.DataFrame(
        eps,
        columns=["technology", "finance", "healthcare", "energy", "consumer"],
    )
    df.insert(0, "date", dates.strftime("%Y-%m-%d"))

    return df
