"""
Data generators for Markov-Switching regime examples.

Generates synthetic datasets with known regime structures for:
- MS(2)-AR(1): GDP growth with expansion/recession regimes
- MS(2)-GARCH(1,1): S&P 500 returns with calm/turbulent regimes
- MS(2)-VAR(1): Bivariate VAR with regime-dependent dynamics
"""

import numpy as np
import pandas as pd


def _simulate_markov_chain(n: int, p11: float, p22: float, rng: np.random.Generator) -> np.ndarray:
    """Simulate a 2-state Markov chain.

    Parameters
    ----------
    n : int
        Number of observations.
    p11 : float
        Probability of staying in regime 1.
    p22 : float
        Probability of staying in regime 2.
    rng : np.random.Generator
        Random number generator.

    Returns
    -------
    np.ndarray
        Array of regime indicators (1 or 2).
    """
    # Ergodic probabilities for initialization
    pi1 = (1 - p22) / (2 - p11 - p22)
    regimes = np.zeros(n, dtype=int)
    regimes[0] = 1 if rng.random() < pi1 else 2

    for t in range(1, n):
        u = rng.random()
        if regimes[t - 1] == 1:
            regimes[t] = 1 if u < p11 else 2
        else:
            regimes[t] = 2 if u < p22 else 1

    return regimes


def generate_ms_gdp(n: int = 250, seed: int = 55) -> pd.DataFrame:
    """Generate MS(2)-AR(1) data simulating US GDP quarterly growth.

    Regime 1 (expansion): mu=0.8, sigma=0.5, phi=0.3, P(stay)=0.95
    Regime 2 (recession): mu=-0.3, sigma=1.2, phi=0.1, P(stay)=0.85

    Parameters
    ----------
    n : int
        Number of quarterly observations (default 250, ~62 years).
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: date, gdp_growth, true_regime.
    """
    rng = np.random.default_rng(seed)

    # Regime parameters
    mu = {1: 0.8, 2: -0.3}
    sigma = {1: 0.5, 2: 1.2}
    phi = {1: 0.3, 2: 0.1}

    # Simulate Markov chain
    regimes = _simulate_markov_chain(n, p11=0.95, p22=0.85, rng=rng)

    # Simulate AR(1) with regime-switching parameters
    y = np.zeros(n)
    y[0] = mu[regimes[0]] + sigma[regimes[0]] * rng.standard_normal()

    for t in range(1, n):
        s = regimes[t]
        y[t] = mu[s] + phi[s] * y[t - 1] + sigma[s] * rng.standard_normal()

    # Create quarterly date index starting 1962-Q1
    dates = pd.date_range(start="1962-01-01", periods=n, freq="QS")

    return pd.DataFrame(
        {
            "date": dates,
            "gdp_growth": np.round(y, 6),
            "true_regime": regimes,
        }
    )


def generate_ms_returns(n: int = 2500, seed: int = 56) -> pd.DataFrame:
    """Generate MS(2)-GARCH(1,1) data simulating S&P 500 daily returns.

    Regime 1 (calm):      omega=1e-6, alpha=0.05, beta=0.93
    Regime 2 (turbulent): omega=5e-6, alpha=0.15, beta=0.80
    Transition: P(stay calm)=0.98, P(stay turbulent)=0.95

    Parameters
    ----------
    n : int
        Number of daily observations (default 2500, ~10 years).
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: date, returns, true_regime, true_volatility.
    """
    rng = np.random.default_rng(seed)

    # GARCH parameters per regime
    omega = {1: 1e-6, 2: 5e-6}
    alpha = {1: 0.05, 2: 0.15}
    beta = {1: 0.93, 2: 0.80}

    # Simulate Markov chain
    regimes = _simulate_markov_chain(n, p11=0.98, p22=0.95, rng=rng)

    # Simulate MS-GARCH
    returns = np.zeros(n)
    sigma2 = np.zeros(n)

    # Initialize variance at unconditional level of regime 1
    sigma2[0] = omega[1] / (1 - alpha[1] - beta[1])
    returns[0] = np.sqrt(sigma2[0]) * rng.standard_normal()

    for t in range(1, n):
        s = regimes[t]
        sigma2[t] = omega[s] + alpha[s] * returns[t - 1] ** 2 + beta[s] * sigma2[t - 1]
        returns[t] = np.sqrt(sigma2[t]) * rng.standard_normal()

    volatility = np.sqrt(sigma2)

    # Create daily date index (business days)
    dates = pd.bdate_range(start="2014-01-02", periods=n)

    return pd.DataFrame(
        {
            "date": dates,
            "returns": np.round(returns, 8),
            "true_regime": regimes,
            "true_volatility": np.round(volatility, 8),
        }
    )


def generate_ms_var(n: int = 250, k: int = 2, seed: int = 57) -> pd.DataFrame:
    """Generate MS(2)-VAR(1) bivariate data.

    Simulates a bivariate VAR(1) with 2 regimes:
    - Regime 1: stronger cross-variable dynamics, lower volatility
    - Regime 2: weaker cross-variable dynamics, higher volatility

    Parameters
    ----------
    n : int
        Number of observations.
    k : int
        Number of variables (fixed at 2).
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: date, y1, y2, true_regime.
    """
    rng = np.random.default_rng(seed)

    # VAR(1) coefficient matrices per regime
    # Regime 1: stronger cross-effects
    A1 = np.array([[0.5, 0.2], [0.15, 0.4]])
    mu1 = np.array([0.3, 0.2])
    Sigma1 = np.array([[0.5, 0.1], [0.1, 0.4]])

    # Regime 2: weaker cross-effects, higher volatility
    A2 = np.array([[0.3, 0.05], [0.05, 0.25]])
    mu2 = np.array([-0.1, -0.05])
    Sigma2 = np.array([[1.5, 0.3], [0.3, 1.2]])

    A = {1: A1, 2: A2}
    mu = {1: mu1, 2: mu2}
    Sigma = {1: Sigma1, 2: Sigma2}

    # Simulate Markov chain
    regimes = _simulate_markov_chain(n, p11=0.95, p22=0.90, rng=rng)

    # Simulate VAR(1)
    Y = np.zeros((n, k))
    Y[0] = mu[regimes[0]] + rng.multivariate_normal(np.zeros(k), Sigma[regimes[0]])

    for t in range(1, n):
        s = regimes[t]
        Y[t] = mu[s] + A[s] @ Y[t - 1] + rng.multivariate_normal(np.zeros(k), Sigma[s])

    dates = pd.date_range(start="1962-01-01", periods=n, freq="QS")

    return pd.DataFrame(
        {
            "date": dates,
            "y1": np.round(Y[:, 0], 6),
            "y2": np.round(Y[:, 1], 6),
            "true_regime": regimes,
        }
    )


if __name__ == "__main__":
    # Quick test
    gdp = generate_ms_gdp()
    print(f"GDP data: {gdp.shape}, regimes: {gdp['true_regime'].value_counts().to_dict()}")
    print(gdp.head())

    ret = generate_ms_returns()
    print(f"\nReturns data: {ret.shape}, regimes: {ret['true_regime'].value_counts().to_dict()}")
    print(ret.head())

    var = generate_ms_var()
    print(f"\nVAR data: {var.shape}, regimes: {var['true_regime'].value_counts().to_dict()}")
    print(var.head())
