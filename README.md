# archbox

ARCH/GARCH volatility models for financial time series.

## Installation

```bash
pip install -e ".[dev]"
```

## Quick Start

```python
from archbox import GARCH
from archbox.datasets import load_dataset

sp500 = load_dataset('sp500')
returns = sp500['returns']

model = GARCH(returns, p=1, q=1)
results = model.fit()
print(results.summary())
forecast = results.forecast(horizon=10)
```

## License

MIT
