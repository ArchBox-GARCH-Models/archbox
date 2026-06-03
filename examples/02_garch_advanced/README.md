# Module 02 - Advanced GARCH Models

This module covers three advanced volatility models that extend the standard
GARCH framework: FIGARCH (long memory), GARCH-in-Mean (risk-return tradeoff),
and HAR-RV (realized volatility).

## Topics

### 1. FIGARCH - Fractionally Integrated GARCH

The FIGARCH(1,d,1) model of Baillie, Bollerslev and Mikkelsen (1996) captures
**long memory** in the conditional variance. Unlike standard GARCH where
volatility shocks decay exponentially, FIGARCH allows hyperbolic (slow) decay
controlled by the fractional integration parameter `d` (0 < d < 1).

- **Key parameter**: `d` — fractional differencing order
- **Use case**: modeling persistent volatility in equity indices, exchange rates
- **R validation**: `rugarch` package with `variance.model = list(model = "fiGARCH")`

### 2. GARCH-in-Mean (GARCH-M)

The GARCH-M model of Engle, Lilien and Robins (1987) incorporates the
conditional volatility directly into the **mean equation**, capturing the
theoretical risk-return tradeoff:

```
r_t = lambda * sigma_t + eps_t
sigma2_t = omega + alpha * eps2_{t-1} + beta * sigma2_{t-1}
```

- **Key parameter**: `lambda` — risk premium coefficient
- **Use case**: testing whether higher risk commands higher expected returns
- **R validation**: `rugarch` with `archm = TRUE`

### 3. HAR-RV - Heterogeneous Autoregressive Realized Volatility

The HAR-RV model of Corsi (2009) uses realized volatility computed from
high-frequency (intraday) data at three horizons:

```
RV_t = c + beta_d * RV_{t-1} + beta_w * RV_w_{t-1} + beta_m * RV_m_{t-1} + eps_t
```

- **Components**: daily (1-day), weekly (5-day avg), monthly (22-day avg)
- **Use case**: forecasting volatility using high-frequency data
- **R validation**: `HARModel` or manual OLS with lagged RV components

## Datasets

| File | Description | Observations | Seed |
|------|-------------|:------------:|:----:|
| `data/sp500_returns.csv` | Synthetic S&P 500 returns (GARCH(1,1) DGP) | 2500 | 42 |
| `data/realized_volatility.csv` | Synthetic realized volatility (HAR DGP) | 2500 | 47 |

### `sp500_returns.csv`

| Column | Description |
|--------|-------------|
| `date` | Business day date |
| `returns` | Daily log returns |
| `true_volatility` | True conditional volatility (sigma_t) |

### `realized_volatility.csv`

| Column | Description |
|--------|-------------|
| `date` | Business day date |
| `rv_daily` | Daily realized volatility (sum of 78 squared 5-min returns) |
| `rv_weekly` | Weekly RV (5-day rolling average) |
| `rv_monthly` | Monthly RV (22-day rolling average) |
| `close_return` | Daily close-to-close return |

## Notebooks

| # | Notebook | Topic |
|---|----------|-------|
| 1 | FIGARCH | Long memory in volatility, fractional integration |
| 2 | GARCH-M | Risk-return tradeoff, mean equation with volatility |
| 3 | HAR-RV | Realized volatility forecasting with heterogeneous components |

## Cross-Validation

- **R scripts** (`R/`): Validation against `rugarch`, `HARModel` packages
- **Stata scripts** (`Stata/`): Validation against native `arch` and regression commands

## Directory Structure

```
02_garch_advanced/
├── README.md
├── notebooks/          # Jupyter tutorial notebooks
├── solutions/          # Completed notebook solutions
├── R/                  # R validation scripts
├── Stata/              # Stata validation scripts
├── data/               # Generated datasets (CSV)
├── utils/              # Data generators, plot helpers
│   ├── __init__.py
│   ├── data_generator.py
│   ├── generate_datasets.py
│   └── plot_helpers.py
└── outputs/            # Saved figures and results
```

## Reproducing Datasets

```bash
cd examples/02_garch_advanced
python3 utils/generate_datasets.py
```

All generators use fixed seeds, so output is perfectly reproducible.

## References

- Baillie, R.T., Bollerslev, T., & Mikkelsen, H.O. (1996). Fractionally integrated
  generalized autoregressive conditional heteroskedasticity. *Journal of Econometrics*, 74(1), 3-30.
- Engle, R.F., Lilien, D.M., & Robins, R.P. (1987). Estimating time varying risk premia
  in the term structure: The ARCH-M model. *Econometrica*, 55(2), 391-407.
- Corsi, F. (2009). A simple approximate long-memory model of realized volatility.
  *Journal of Financial Econometrics*, 7(2), 174-196.
