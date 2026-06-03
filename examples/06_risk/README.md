# Module 06: Risk Management with GARCH Models

This module demonstrates the application of GARCH-family models to financial risk management.
It covers Value-at-Risk (VaR), Expected Shortfall (ES), EWMA volatility, and backtesting.

## Concepts

### Value-at-Risk (VaR)

Value-at-Risk is the maximum loss expected over a given time horizon at a specified confidence level.

For a confidence level $\alpha$ (e.g., 95%), the VaR is defined as:

$$\text{VaR}_\alpha = -\inf\{x : P(R \leq x) \leq 1 - \alpha\}$$

Or equivalently, VaR is the $\alpha$-quantile of the loss distribution:

$$P(R < -\text{VaR}_\alpha) = 1 - \alpha$$

**Parametric VaR (Normal):**

$$\text{VaR}_\alpha^t = \mu_t + \sigma_t \cdot \Phi^{-1}(1 - \alpha)$$

where $\sigma_t$ is the conditional volatility from a GARCH model and $\Phi^{-1}$ is the standard normal quantile.

**Parametric VaR (Student-t):**

$$\text{VaR}_\alpha^t = \mu_t + \sigma_t \cdot t_\nu^{-1}(1 - \alpha) \cdot \sqrt{\frac{\nu - 2}{\nu}}$$

where $t_\nu^{-1}$ is the quantile function of the Student-t distribution with $\nu$ degrees of freedom.

### Expected Shortfall (ES)

Expected Shortfall (also called CVaR - Conditional Value-at-Risk) is the expected loss
conditional on the loss exceeding VaR:

$$\text{ES}_\alpha = -E[R \mid R < -\text{VaR}_\alpha]$$

**ES under Normal distribution:**

$$\text{ES}_\alpha = \mu_t + \sigma_t \cdot \frac{\phi(\Phi^{-1}(1-\alpha))}{1-\alpha}$$

where $\phi$ is the standard normal density.

**ES under Student-t distribution:**

$$\text{ES}_\alpha = \mu_t + \sigma_t \cdot \frac{f_\nu(t_\nu^{-1}(1-\alpha))}{1-\alpha} \cdot \frac{\nu + (t_\nu^{-1}(1-\alpha))^2}{\nu - 1} \cdot \sqrt{\frac{\nu-2}{\nu}}$$

### EWMA (Exponentially Weighted Moving Average)

The RiskMetrics EWMA model estimates conditional variance as:

$$\sigma_t^2 = \lambda \sigma_{t-1}^2 + (1 - \lambda) r_{t-1}^2$$

where $\lambda$ is the decay factor. The standard RiskMetrics value is $\lambda = 0.94$ for daily data.

EWMA is equivalent to an IGARCH(1,1) model with $\omega = 0$:
- No intercept term means the unconditional variance is undefined
- Shocks persist indefinitely (integrated process)
- Simple, parameter-free (given $\lambda$) approach widely used in practice

### Backtesting

Backtesting validates risk model accuracy by comparing predicted VaR to realized losses.

**Kupiec's Unconditional Coverage Test:**

Tests whether the observed violation rate equals the expected rate.

$$LR_{UC} = -2\ln\left(\frac{(1-p)^{n-x} p^x}{(1-\hat{p})^{n-x} \hat{p}^x}\right) \sim \chi^2(1)$$

where $p$ is the expected violation rate, $\hat{p} = x/n$ is the observed rate, $x$ is the number of violations, and $n$ is the sample size.

**Christoffersen's Conditional Coverage Test:**

Tests both coverage and independence of violations:

$$LR_{CC} = LR_{UC} + LR_{IND} \sim \chi^2(2)$$

where $LR_{IND}$ tests whether violations are serially independent using a first-order Markov chain.

## Datasets

- **sp500_returns.csv**: 2500 synthetic S&P 500 daily returns (GARCH(1,1), seed=42)
- **ibovespa_returns.csv**: 2500 synthetic Ibovespa daily returns (GARCH(1,1), seed=43)

Both datasets are generated with fixed seeds for reproducibility. Returns exhibit
volatility clustering and fat tails typical of financial time series.

## Structure

```
06_risk/
├── README.md              # This file
├── notebooks/             # Jupyter tutorial notebooks
├── solutions/             # Complete solution notebooks
├── R/                     # R validation scripts
├── Stata/                 # Stata validation scripts
├── data/                  # CSV datasets
│   ├── sp500_returns.csv
│   └── ibovespa_returns.csv
├── utils/                 # Python utilities
│   ├── data_generator.py  # Synthetic data generators
│   ├── generate_datasets.py  # Script to regenerate CSVs
│   └── plot_helpers.py    # Visualization functions
└── outputs/               # Saved figures and results
```

## References

- Jorion, P. (2006). *Value at Risk: The New Benchmark for Managing Financial Risk*.
- McNeil, A.J., Frey, R., & Embrechts, P. (2015). *Quantitative Risk Management*.
- RiskMetrics Group (1996). *RiskMetrics Technical Document*.
- Christoffersen, P.F. (1998). Evaluating interval forecasts. *International Economic Review*.
- Kupiec, P. (1995). Techniques for verifying the accuracy of risk measurement models. *Journal of Derivatives*.
