"""
Data generators for Threshold and STAR model examples.

Generates synthetic time series with known threshold/smooth transition dynamics:
- SETAR(2,1,1): Self-Exciting Threshold AR with 2 regimes
- LSTAR: Logistic Smooth Transition AR
- ESTAR: Exponential Smooth Transition AR

All generators use fixed seeds for reproducibility.
"""

import numpy as np
import pandas as pd


def generate_setar_data(n=500, seed=60):
    """
    Simulate a SETAR(2,1,1) process.

    Model:
        Regime 1 (y_{t-1} <= c): y_t = phi_1 * y_{t-1} + sigma_1 * e_t
        Regime 2 (y_{t-1} > c):  y_t = phi_2 * y_{t-1} + sigma_2 * e_t

    Parameters
    ----------
    n : int
        Number of observations (default: 500).
    seed : int
        Random seed for reproducibility (default: 60).

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: date, y, true_regime.

    True parameters:
        phi_1 = 0.5, sigma_1 = 0.8 (regime 1, y_{t-1} <= 0)
        phi_2 = -0.3, sigma_2 = 1.5 (regime 2, y_{t-1} > 0)
        threshold c = 0, delay d = 1
    """
    rng = np.random.default_rng(seed)

    phi_1, sigma_1 = 0.5, 0.8
    phi_2, sigma_2 = -0.3, 1.5
    c = 0.0  # threshold

    burn = 100
    total = n + burn

    y = np.zeros(total)
    regimes = np.zeros(total, dtype=int)

    y[0] = rng.normal(0, 1)

    for t in range(1, total):
        e = rng.normal(0, 1)
        if y[t - 1] <= c:
            y[t] = phi_1 * y[t - 1] + sigma_1 * e
            regimes[t] = 1
        else:
            y[t] = phi_2 * y[t - 1] + sigma_2 * e
            regimes[t] = 2

    y = y[burn:]
    regimes = regimes[burn:]

    dates = pd.date_range(start="2000-01-01", periods=n, freq="QE")

    return pd.DataFrame(
        {
            "date": dates,
            "y": y,
            "true_regime": regimes,
        }
    )


def generate_lstar_data(n=500, seed=61):
    """
    Simulate a Logistic STAR (LSTAR) process.

    Model:
        y_t = phi_1 * y_{t-1} * (1 - G) + phi_2 * y_{t-1} * G + sigma * e_t
        G(y_{t-1}; gamma, c) = 1 / (1 + exp(-gamma * (y_{t-1} - c)))

    Parameters
    ----------
    n : int
        Number of observations (default: 500).
    seed : int
        Random seed for reproducibility (default: 61).

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: date, y, transition_function.

    True parameters:
        phi_1 = 0.8, phi_2 = -0.5, sigma = 1.0
        gamma = 3.0, c = 0.0
    """
    rng = np.random.default_rng(seed)

    phi_1, phi_2 = 0.8, -0.5
    sigma = 1.0
    gamma, c = 3.0, 0.0

    burn = 100
    total = n + burn

    y = np.zeros(total)
    G = np.zeros(total)

    y[0] = rng.normal(0, 1)

    for t in range(1, total):
        e = rng.normal(0, 1)
        G[t] = 1.0 / (1.0 + np.exp(-gamma * (y[t - 1] - c)))
        y[t] = phi_1 * y[t - 1] * (1 - G[t]) + phi_2 * y[t - 1] * G[t] + sigma * e

    y = y[burn:]
    G = G[burn:]

    dates = pd.date_range(start="2000-01-01", periods=n, freq="B")

    return pd.DataFrame(
        {
            "date": dates,
            "y": y,
            "transition_function": G,
        }
    )


def generate_estar_data(n=500, seed=62):
    """
    Simulate an Exponential STAR (ESTAR) process.

    Model:
        y_t = phi_1 * y_{t-1} * (1 - G) + phi_2 * y_{t-1} * G + sigma * e_t
        G(y_{t-1}; gamma, c) = 1 - exp(-gamma * (y_{t-1} - c)^2)

    Parameters
    ----------
    n : int
        Number of observations (default: 500).
    seed : int
        Random seed for reproducibility (default: 62).

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: date, y, transition_function.

    True parameters:
        phi_1 = 0.8, phi_2 = -0.5, sigma = 1.0
        gamma = 2.0, c = 0.0
    """
    rng = np.random.default_rng(seed)

    phi_1, phi_2 = 0.8, -0.5
    sigma = 1.0
    gamma, c = 2.0, 0.0

    burn = 100
    total = n + burn

    y = np.zeros(total)
    G = np.zeros(total)

    y[0] = rng.normal(0, 1)

    for t in range(1, total):
        e = rng.normal(0, 1)
        G[t] = 1.0 - np.exp(-gamma * (y[t - 1] - c) ** 2)
        y[t] = phi_1 * y[t - 1] * (1 - G[t]) + phi_2 * y[t - 1] * G[t] + sigma * e

    y = y[burn:]
    G = G[burn:]

    dates = pd.date_range(start="2000-01-01", periods=n, freq="B")

    return pd.DataFrame(
        {
            "date": dates,
            "y": y,
            "transition_function": G,
        }
    )
