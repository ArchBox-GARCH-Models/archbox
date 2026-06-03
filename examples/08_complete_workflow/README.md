# Module 08 - Complete Workflow

End-to-end volatility modeling workflows that integrate all archbox modules.

## Overview

This module demonstrates production-ready pipelines that combine:

- **Data loading** - Consolidated datasets from all previous modules
- **Univariate GARCH** - GARCH, EGARCH, GJR-GARCH model estimation
- **Multivariate GARCH** - CCC, DCC for covariance modeling
- **Risk measures** - VaR, Expected Shortfall, backtesting
- **Diagnostics** - ARCH-LM, Ljung-Box, sign bias tests

## Workflows

### 1. Univariate Pipeline
`data -> exploratory analysis -> ARCH-LM test -> fit multiple models -> diagnostics -> model selection -> VaR/ES -> backtesting`

### 2. Multivariate + Risk Pipeline
`multivariate data -> DCC/CCC -> portfolio covariance -> VaR -> regime-switching -> backtesting`

## Prerequisites

This module builds on all previous example modules (FASE 1-7). The following
datasets must be available either in the source module directories or locally
in `data/`:

| Dataset | Source | Description |
|---------|--------|-------------|
| `sp500_returns.csv` | Module 01 | S&P 500 daily log returns |
| `ibovespa_returns.csv` | Module 01 | Ibovespa daily log returns |
| `bitcoin_returns.csv` | Module 01 | Bitcoin daily log returns |
| `fx_majors.csv` | Module 03 | FX major pairs (EUR, GBP, JPY, CHF vs USD) |
| `sector_indices.csv` | Module 03 | US sector index returns |
| `realized_volatility.csv` | Module 02 | Realized volatility series |

## Structure

```
08_complete_workflow/
├── README.md              # This file
├── notebooks/             # Jupyter tutorial notebooks
├── solutions/             # Completed notebook solutions
├── R/                     # R validation scripts
├── Stata/                 # Stata validation scripts
├── data/                  # Local copies of key datasets
│   ├── sp500_returns.csv
│   ├── fx_majors.csv
│   └── sector_indices.csv
├── utils/                 # Pipeline and helper functions
│   ├── __init__.py
│   ├── data_loader.py    # Consolidated data loading
│   └── workflow_helpers.py # Pipeline orchestration
└── outputs/               # Generated figures and tables
```

## Quick Start

```python
import sys
sys.path.insert(0, "..")

from utils import load_sp500, run_univariate_pipeline, generate_comparison_report

# Load data
sp500 = load_sp500()
returns = sp500["returns"].values

# Run full univariate pipeline
results = run_univariate_pipeline(returns)

# Compare models
report = generate_comparison_report(results)
print(report)
```

## Utility Functions

### data_loader.py
- `load_sp500()` - S&P 500 returns
- `load_ibovespa()` - Ibovespa returns
- `load_bitcoin()` - Bitcoin returns
- `load_fx_majors()` - FX majors multivariate returns
- `load_sector_indices()` - Sector index multivariate returns
- `load_realized_volatility()` - Realized volatility
- `load_all_datasets()` - Load all available datasets

### workflow_helpers.py
- `run_univariate_pipeline(returns, models, alpha)` - Full univariate pipeline
- `run_multivariate_pipeline(returns_matrix, models, alpha)` - Full multivariate pipeline
- `generate_comparison_report(results_dict)` - Model comparison DataFrame
- `run_backtesting_suite(returns, var_dict, alpha)` - VaR backtesting suite

## Cross-Validation

R and Stata scripts in `R/` and `Stata/` directories validate archbox results
against reference implementations:

- **R**: `rugarch`, `rmgarch`, `GAS` packages
- **Stata**: `arch`, `mgarch` commands
