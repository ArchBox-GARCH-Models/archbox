# ArchBox

**ARCH/GARCH volatility models for financial time series.**

ArchBox is a comprehensive Python library for estimating, diagnosing, and forecasting
volatility using ARCH/GARCH family models. It provides a unified API covering univariate
models (GARCH, EGARCH, GJR, APARCH), multivariate models (DCC, CCC, BEKK),
regime-switching models (MS-AR, MS-GARCH), threshold models (SETAR, LSTAR),
and risk management tools (VaR, ES, backtesting).

## Features

- **Univariate GARCH**: GARCH, EGARCH, GJR-GARCH, APARCH, FIGARCH, IGARCH, GARCH-M, Component
- **Multivariate**: DCC, CCC, BEKK, GO-GARCH, DECO
- **Regime-Switching**: MS-Mean, MS-AR, MS-VAR, MS-GARCH
- **Threshold**: SETAR, LSTAR, ESTAR
- **Risk**: VaR (parametric, historical, filtered HS, Monte Carlo), Expected Shortfall, backtesting
- **Distributions**: Normal, Student-t, Skewed-t, GED
- **Diagnostics**: ARCH-LM, Ljung-Box, Jarque-Bera, QQ-plots
- **CLI**: Command-line interface for quick analysis
- **Numba acceleration**: Optional JIT compilation for critical loops

## Quick Example

```python
from archbox import GARCH
from archbox.datasets import load_dataset

# Load data
sp500 = load_dataset('sp500')
returns = sp500['returns']

# Fit GARCH(1,1)
model = GARCH(returns, p=1, q=1)
results = model.fit()
print(results.summary())

# Forecast
forecast = results.forecast(horizon=10)

# Risk measures
from archbox.risk import ValueAtRisk
var = ValueAtRisk(results, alpha=0.05)
print(f"VaR(5%): {var.parametric()[-1]:.4f}")
```

## Installation

```bash
pip install archbox
```

For development:

```bash
pip install archbox[dev]
```

## License

MIT License - see [LICENSE](https://github.com/nodesecon/archbox/blob/main/LICENSE).
