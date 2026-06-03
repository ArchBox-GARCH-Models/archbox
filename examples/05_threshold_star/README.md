# Module 05: Threshold and Smooth Transition AR Models

This module covers **Threshold Autoregressive (TAR/SETAR)** and **Smooth Transition AR (STAR)** models for modeling nonlinear dynamics in financial and macroeconomic time series.

## Models Covered

### TAR - Threshold Autoregressive (Tong, 1978)

The TAR model allows different AR dynamics depending on whether a threshold variable exceeds a critical value:

```
y_t = phi_1 * y_{t-1} + sigma_1 * e_t    if s_{t-d} <= c
y_t = phi_2 * y_{t-1} + sigma_2 * e_t    if s_{t-d} > c
```

where `s_{t-d}` is the threshold variable with delay `d`, and `c` is the threshold value.

### SETAR - Self-Exciting Threshold AR (Tong & Lim, 1980)

A special case of TAR where the threshold variable is the dependent variable itself (`s_{t-d} = y_{t-d}`):

```
y_t = phi_1 * y_{t-1} + sigma_1 * e_t    if y_{t-d} <= c
y_t = phi_2 * y_{t-1} + sigma_2 * e_t    if y_{t-d} > c
```

The SETAR(2,1,1) has 2 regimes, AR order 1 in each regime, and delay d=1.

### LSTAR - Logistic Smooth Transition AR (Terasvirta, 1994)

The LSTAR replaces the abrupt regime switch with a smooth logistic transition:

```
y_t = phi_1 * y_{t-1} * (1 - G) + phi_2 * y_{t-1} * G + sigma * e_t

G(s; gamma, c) = 1 / (1 + exp(-gamma * (s - c)))
```

where `gamma > 0` controls the smoothness of transition (larger gamma = sharper transition) and `c` is the location parameter.

### ESTAR - Exponential Smooth Transition AR (Terasvirta, 1994)

The ESTAR uses an exponential transition function, symmetric around `c`:

```
y_t = phi_1 * y_{t-1} * (1 - G) + phi_2 * y_{t-1} * G + sigma * e_t

G(s; gamma, c) = 1 - exp(-gamma * (s - c)^2)
```

The ESTAR transition is **symmetric**: deviations from `c` in either direction activate the second regime.

## Linearity Tests

Before fitting nonlinear models, linearity should be tested:

- **Tsay test**: Tests for threshold nonlinearity using arranged autoregression
- **Hansen test**: Sup-LM test for threshold with bootstrapped p-values
- **LM linearity test (Luukkonen et al., 1988)**: Tests STAR-type nonlinearity using auxiliary regression with Taylor expansion of the transition function

## Datasets

| File | Process | Parameters |
|------|---------|------------|
| `us_gdp_growth.csv` | SETAR(2,1,1) | phi_1=0.5, phi_2=-0.3, sigma_1=0.8, sigma_2=1.5, c=0, d=1 |
| `sp500_returns.csv` | LSTAR | phi_1=0.8, phi_2=-0.5, gamma=3.0, c=0.0, sigma=1.0 |

All datasets use fixed seeds for reproducibility (seeds 60 and 61 respectively).

## Directory Structure

```
05_threshold_star/
├── README.md              # This file
├── notebooks/             # Jupyter notebook tutorials
├── solutions/             # Completed notebook solutions
├── R/                     # R validation scripts (tsDyn, etc.)
├── Stata/                 # Stata validation scripts
├── data/                  # Synthetic datasets
│   ├── us_gdp_growth.csv  # SETAR process (500 obs)
│   └── sp500_returns.csv  # LSTAR process (500 obs)
├── utils/                 # Utility functions
│   ├── __init__.py
│   ├── data_generator.py  # SETAR, LSTAR, ESTAR generators
│   ├── generate_datasets.py
│   └── plot_helpers.py    # Visualization helpers
└── outputs/               # Generated figures and results
```

## Key References

- Tong, H. (1978). On a threshold model. Pattern Recognition and Signal Processing.
- Tong, H. & Lim, K. S. (1980). Threshold autoregression, limit cycles, and cyclical data.
- Terasvirta, T. (1994). Specification, estimation, and evaluation of smooth transition autoregressive models.
- Luukkonen, R., Saikkonen, P. & Terasvirta, T. (1988). Testing linearity against smooth transition autoregressive models.
- Hansen, B. E. (1996). Inference when a nuisance parameter is not identified under the null hypothesis.
