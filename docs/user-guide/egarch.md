# EGARCH Models

## Overview

The EGARCH (Exponential GARCH) model by Nelson (1991) models log-volatility,
naturally ensuring positive variance without parameter constraints.

$$\log(\sigma^2_t) = \omega + \alpha(|z_{t-1}| - E|z_{t-1}|) + \gamma z_{t-1} + \beta \log(\sigma^2_{t-1})$$

## Usage

```python
from archbox.models.egarch import EGARCH
from archbox.datasets import load_dataset

sp500 = load_dataset('sp500')
model = EGARCH(sp500['returns'], p=1, q=1)
results = model.fit()
print(results.summary())
```

## Leverage effect

The gamma parameter captures leverage: negative gamma means negative shocks
increase volatility more than positive shocks.
