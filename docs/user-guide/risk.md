# Risk Management

## Value at Risk (VaR)

```python
from archbox import GARCH
from archbox.risk import ValueAtRisk
from archbox.datasets import load_dataset

sp500 = load_dataset('sp500')
model = GARCH(sp500['returns'], p=1, q=1)
results = model.fit()

var = ValueAtRisk(results, alpha=0.05)

# Methods
var_param = var.parametric()
var_hist = var.historical()
var_fhs = var.filtered_historical()
var_mc = var.monte_carlo(n_sims=10000)
```

## Expected Shortfall (ES)

```python
from archbox.risk import ExpectedShortfall

es = ExpectedShortfall(results, alpha=0.05)
es_series = es.compute(method='parametric')
```

## Backtesting

```python
from archbox.risk import VaRBacktest

bt = VaRBacktest(returns[-500:], var_param[-500:], alpha=0.05)
print(f"Violation ratio: {bt.violation_ratio():.4f}")
print(f"Kupiec p-value: {bt.kupiec_test().pvalue:.4f}")
print(f"Traffic light: {bt.traffic_light()}")
```
