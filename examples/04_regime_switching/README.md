# Module 4: Regime-Switching Models

This module covers **Markov-Switching (MS)** models for financial time series,
where model parameters change according to an unobserved discrete state (regime)
that follows a Markov chain.

## Models Covered

### MS-AR: Markov-Switching Autoregressive (Hamilton, 1989)

The MS-AR model allows the intercept, AR coefficients, and variance of an
autoregressive process to switch between regimes:

```
y_t = mu(s_t) + phi(s_t) * y_{t-1} + sigma(s_t) * e_t
```

where `s_t in {1, 2, ..., K}` follows a first-order Markov chain with
transition probability matrix `P`. This is the foundational regime-switching
model, originally applied to US GDP growth to identify business cycle phases
(expansion vs. recession).

**Key references:**
- Hamilton, J.D. (1989). "A New Approach to the Economic Analysis of
  Nonstationary Time Series and the Business Cycle." *Econometrica*, 57(2), 357-384.
- Hamilton, J.D. (1994). *Time Series Analysis*. Princeton University Press, Ch. 22.

### MS-VAR: Markov-Switching Vector Autoregression

The MS-VAR extends the MS-AR framework to multivariate settings:

```
Y_t = mu(s_t) + A(s_t) * Y_{t-1} + Sigma(s_t)^{1/2} * e_t
```

where `Y_t` is a vector of variables. This allows regime-dependent dynamics
across multiple time series simultaneously, capturing changes in both
individual dynamics and cross-variable relationships.

**Key references:**
- Krolzig, H.-M. (1997). *Markov-Switching Vector Autoregressions*. Springer.
- Krolzig, H.-M. (1998). "Econometric Modelling of Markov-Switching Vector
  Autoregressions Using MSVAR for Ox." IES Working Paper.

### MS-GARCH: Markov-Switching GARCH

The MS-GARCH model combines regime-switching with GARCH volatility dynamics:

```
r_t = sigma_t * e_t
sigma_t^2 = omega(s_t) + alpha(s_t) * r_{t-1}^2 + beta(s_t) * sigma_{t-1}^2
```

This captures the observation that financial volatility exhibits distinct
regimes (e.g., calm vs. crisis periods) with different GARCH parameters.

**Key references:**
- Gray, S.F. (1996). "Modeling the Conditional Distribution of Interest Rates
  as a Regime-Switching Process." *Journal of Financial Economics*, 42(1), 27-62.
- Haas, M., Mittnik, S. & Paolella, M.S. (2004). "A New Approach to
  Markov-Switching GARCH Models." *Journal of Financial Econometrics*, 2(4), 493-530.
- Ardia, D., Bluteau, K., Boudt, K. & Catania, L. (2018). "Forecasting Risk
  with Markov-Switching GARCH Models." *Journal of Applied Econometrics*, 33(7), 1080-1100.

## Datasets

| File | Description | Obs | Frequency |
|------|-------------|-----|-----------|
| `data/us_gdp_growth.csv` | Simulated US GDP quarterly growth with expansion/recession regimes | 250 | Quarterly |
| `data/sp500_returns.csv` | Simulated S&P 500 returns with calm/turbulent volatility regimes | 2500 | Daily |

All datasets use fixed random seeds for full reproducibility.

## Directory Structure

```
04_regime_switching/
├── README.md              # This file
├── notebooks/             # Jupyter notebook exercises
├── solutions/             # Completed notebook solutions
├── R/                     # R validation scripts (MSwM, rugarch)
├── Stata/                 # Stata validation scripts (mswitch)
├── data/                  # Synthetic datasets
├── utils/                 # Data generators and plot helpers
│   ├── __init__.py
│   ├── data_generator.py  # MS-AR, MS-GARCH, MS-VAR generators
│   ├── generate_datasets.py  # Script to regenerate CSVs
│   └── plot_helpers.py    # Regime-switching visualization functions
└── outputs/               # Saved figures and results
```

## Estimation Methods

The notebooks cover:

1. **EM Algorithm** - Expectation-Maximization for ML estimation of MS models
2. **Hamilton Filter** - Forward filtering for regime probabilities
3. **Kim Smoother** - Smoothed regime probabilities using backward recursion
4. **Maximum Likelihood** - Direct numerical optimization of the log-likelihood

## Software References

- **Python**: `archbox` (this library)
- **R**: `MSwM`, `rugarch` (for MS-GARCH), `MTS` (for MS-VAR)
- **Stata**: `mswitch` (built-in since Stata 14)
