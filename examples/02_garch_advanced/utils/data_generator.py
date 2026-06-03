"""Data generators for advanced GARCH examples.

Generates synthetic financial return series for FIGARCH, GARCH-M, and
realized volatility models. All generators use fixed seeds for perfect
reproducibility.
"""

import numpy as np
import pandas as pd


def generate_figarch_returns(
    n: int = 2500,
    d: float = 0.4,
    omega: float = 1e-6,
    beta: float = 0.3,
    phi: float = 0.2,
    seed: int = 45,
    start_date: str = "2014-01-02",
) -> pd.DataFrame:
    """Generate returns from a FIGARCH(1,d,1) process.

    The FIGARCH model of Baillie, Bollerslev and Mikkelsen (1996) captures
    long memory in the conditional variance. The fractional differencing
    parameter d controls the rate of hyperbolic decay of the autocorrelation
    of squared returns.

    The conditional variance follows:
        sigma2_t = omega / (1 - beta) + [1 - (1-beta*L)^{-1} * (1-phi*L) * (1-L)^d] * eps2_t

    We approximate the infinite-order fractional difference filter using
    truncated binomial coefficients.

    Parameters
    ----------
    n : int
        Number of observations.
    d : float
        Fractional integration parameter (0 < d < 1). Higher d means
        stronger long memory.
    omega : float
        Constant in the variance equation.
    beta : float
        GARCH coefficient.
    phi : float
        ARCH coefficient in the FIGARCH parameterization.
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

    # Truncation length for the fractional difference filter
    trunclag = min(1000, n)

    # Compute fractional difference coefficients: (1-L)^d
    # delta_k are the coefficients of (1-L)^d = sum_{k=0}^{inf} delta_k * L^k
    # delta_0 = 1, delta_k = delta_{k-1} * (k - 1 - d) / k
    delta = np.zeros(trunclag)
    delta[0] = 1.0
    for k in range(1, trunclag):
        delta[k] = delta[k - 1] * (k - 1 - d) / k

    # Compute the lambda coefficients for the FIGARCH filter
    # lambda(L) = 1 - (1-beta*L)^{-1} * (1-phi*L) * (1-L)^d
    # We compute lambda_k recursively
    lam = np.zeros(trunclag)
    # First compute pi_k = coefficients of (1-phi*L)*(1-L)^d
    pi_coeff = np.zeros(trunclag)
    pi_coeff[0] = delta[0]  # = 1
    for k in range(1, trunclag):
        pi_coeff[k] = delta[k] - phi * delta[k - 1]

    # Now lambda_k = 1 - (1-beta*L)^{-1} * pi(L)
    # Let gamma(L) = (1-beta*L)^{-1} * pi(L), then gamma_k = pi_k + beta*gamma_{k-1}
    gamma = np.zeros(trunclag)
    gamma[0] = pi_coeff[0]  # = 1
    for k in range(1, trunclag):
        gamma[k] = pi_coeff[k] + beta * gamma[k - 1]

    # lambda_0 = 1 - gamma_0 = 0 (by construction)
    # lambda_k = -gamma_k for k >= 1
    lam[0] = 0.0
    for k in range(1, trunclag):
        lam[k] = -gamma[k]

    # Note: in the FIGARCH variance equation:
    # sigma2_t = omega/(1-beta) + sum_{k=1}^{trunclag} lambda_k * eps2_{t-k}
    # The lambda_k should be positive for valid variance

    # Simulate
    burn = 500
    total = n + burn
    eps2 = np.zeros(total)
    sigma2 = np.zeros(total)
    returns = np.zeros(total)

    unconditional_var = omega / (1 - beta)
    sigma2[0] = unconditional_var

    z = rng.standard_normal(total)

    for t in range(total):
        if t > 0:
            sigma2[t] = omega / (1 - beta)
            for k in range(1, min(t, trunclag)):
                sigma2[t] += lam[k] * eps2[t - k]
            # Ensure positivity
            sigma2[t] = max(sigma2[t], 1e-10)
        returns[t] = np.sqrt(sigma2[t]) * z[t]
        eps2[t] = returns[t] ** 2

    # Remove burn-in
    returns = returns[burn:]
    sigma2 = sigma2[burn:]

    dates = pd.bdate_range(start_date, periods=n)
    return pd.DataFrame(
        {
            "date": dates.strftime("%Y-%m-%d"),
            "returns": np.round(returns, 8),
            "true_volatility": np.round(np.sqrt(sigma2), 8),
        }
    )


def generate_garchm_returns(
    n: int = 2500,
    omega: float = 1.5e-6,
    alpha: float = 0.08,
    beta: float = 0.91,
    lambda_m: float = 0.01,
    seed: int = 46,
    start_date: str = "2014-01-02",
) -> pd.DataFrame:
    """Generate returns from a GARCH-in-Mean process.

    The GARCH-M model of Engle, Lilien and Robins (1987) allows the
    conditional variance (or standard deviation) to enter the mean equation,
    capturing the risk-return tradeoff:

        r_t = lambda * sigma_t + eps_t
        eps_t = sigma_t * z_t
        sigma2_t = omega + alpha * eps2_{t-1} + beta * sigma2_{t-1}

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
    lambda_m : float
        Risk premium parameter (coefficient on sigma_t in mean equation).
    seed : int
        Random seed for reproducibility.
    start_date : str
        Start date for the business-day index.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: date, returns, true_volatility, risk_premium.
    """
    rng = np.random.default_rng(seed)

    burn = 500
    total = n + burn

    sigma2 = np.zeros(total)
    eps = np.zeros(total)
    returns = np.zeros(total)

    unconditional_var = omega / (1 - alpha - beta)
    sigma2[0] = unconditional_var

    z = rng.standard_normal(total)

    for t in range(total):
        if t > 0:
            sigma2[t] = omega + alpha * eps[t - 1] ** 2 + beta * sigma2[t - 1]
        sigma_t = np.sqrt(sigma2[t])
        eps[t] = sigma_t * z[t]
        returns[t] = lambda_m * sigma_t + eps[t]

    # Remove burn-in
    returns = returns[burn:]
    sigma2 = sigma2[burn:]
    sigma = np.sqrt(sigma2)

    dates = pd.bdate_range(start_date, periods=n)
    return pd.DataFrame(
        {
            "date": dates.strftime("%Y-%m-%d"),
            "returns": np.round(returns, 8),
            "true_volatility": np.round(sigma, 8),
            "risk_premium": np.round(lambda_m * sigma, 8),
        }
    )


def generate_realized_volatility(
    n: int = 2500,
    seed: int = 47,
    start_date: str = "2014-01-02",
) -> pd.DataFrame:
    """Generate synthetic realized volatility data.

    Simulates daily realized volatility computed from 78 intraday 5-minute
    returns (6.5 hours trading day). The DGP uses a HAR-type structure to
    ensure the realized volatility exhibits long memory (slowly decaying ACF).

    The underlying process for log(RV) follows:
        log(rv_t) = c + beta_d * log(rv_{t-1}) + beta_w * log(rv_w_{t-1})
                     + beta_m * log(rv_m_{t-1}) + eps_t

    with parameters calibrated to empirical values from Corsi (2009).

    Parameters
    ----------
    n : int
        Number of observations.
    seed : int
        Random seed for reproducibility.
    start_date : str
        Start date for the business-day index.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: date, rv_daily, rv_weekly, rv_monthly,
        close_return.
    """
    rng = np.random.default_rng(seed)

    # HAR parameters calibrated to empirical S&P 500 values (Corsi 2009)
    # Higher persistence ensures long memory (slowly decaying ACF)
    c = -0.05  # intercept in log-RV space
    beta_d = 0.40  # daily component
    beta_w = 0.32  # weekly component
    beta_m = 0.22  # monthly component (sum ~0.94 for high persistence)
    sigma_eps = 0.25  # innovation std in log-RV

    n_intraday = 78  # 5-min intervals in 6.5 hour trading day

    burn = 500
    total = n + burn

    log_rv = np.zeros(total)
    rv_daily = np.zeros(total)
    close_return = np.zeros(total)

    # Initialize with unconditional mean
    unconditional_log_rv = c / (1 - beta_d - beta_w - beta_m)
    log_rv[:22] = unconditional_log_rv + rng.normal(0, sigma_eps, 22)
    rv_daily[:22] = np.exp(log_rv[:22])

    # Generate initial close returns
    for t in range(22):
        intraday_returns = rng.normal(0, np.sqrt(rv_daily[t] / n_intraday), n_intraday)
        close_return[t] = np.sum(intraday_returns)

    eps = rng.normal(0, sigma_eps, total)

    for t in range(22, total):
        # Weekly RV: average of last 5 days
        rv_w = np.mean(rv_daily[t - 5 : t])
        # Monthly RV: average of last 22 days
        rv_m = np.mean(rv_daily[t - 22 : t])

        log_rv[t] = (
            c
            + beta_d * log_rv[t - 1]
            + beta_w * np.log(rv_w + 1e-12)
            + beta_m * np.log(rv_m + 1e-12)
            + eps[t]
        )
        rv_daily[t] = np.exp(log_rv[t])

        # Generate intraday returns and compute close return
        intraday_returns = rng.normal(0, np.sqrt(rv_daily[t] / n_intraday), n_intraday)
        close_return[t] = np.sum(intraday_returns)

    # Remove burn-in
    rv_daily = rv_daily[burn:]
    close_return = close_return[burn:]

    # Compute rolling weekly and monthly RV
    rv_weekly = np.array([np.mean(rv_daily[max(0, t - 4) : t + 1]) for t in range(n)])
    rv_monthly = np.array([np.mean(rv_daily[max(0, t - 21) : t + 1]) for t in range(n)])

    dates = pd.bdate_range(start_date, periods=n)
    return pd.DataFrame(
        {
            "date": dates.strftime("%Y-%m-%d"),
            "rv_daily": np.round(rv_daily, 10),
            "rv_weekly": np.round(rv_weekly, 10),
            "rv_monthly": np.round(rv_monthly, 10),
            "close_return": np.round(close_return, 8),
        }
    )


def generate_sp500_returns(
    n: int = 2500,
    omega: float = 1.5e-6,
    alpha: float = 0.08,
    beta: float = 0.91,
    mu: float = 0.0004,
    seed: int = 42,
    start_date: str = "2014-01-02",
) -> pd.DataFrame:
    """Generate synthetic S&P 500-like returns from a GARCH(1,1) process.

    Reuses the same seed=42 as FASE1 for consistency.

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
