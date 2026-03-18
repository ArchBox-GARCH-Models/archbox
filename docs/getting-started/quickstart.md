# Quickstart

This guide walks through a complete volatility analysis workflow.

## 1. Load data

```python
from archbox.datasets import load_dataset

sp500 = load_dataset('sp500')
returns = sp500['returns'].to_numpy()
print(f"Observations: {len(returns)}")
print(f"Mean return: {returns.mean():.6f}")
print(f"Std return: {returns.std():.6f}")
```

## 2. Fit a GARCH model

```python
from archbox import GARCH

model = GARCH(returns, p=1, q=1)
results = model.fit()
print(results.summary())
```

## 3. Diagnostics

```python
from archbox.diagnostics import full_diagnostics

diag = full_diagnostics(results)
print(f"ARCH-LM p-value: {diag.arch_lm.pvalue:.4f}")
print(f"Ljung-Box p-value: {diag.ljung_box.pvalue:.4f}")
```

## 4. Forecast

```python
forecast = results.forecast(horizon=10)
print(forecast)
```

## 5. Risk measures

```python
from archbox.risk import ValueAtRisk, ExpectedShortfall

var = ValueAtRisk(results, alpha=0.05)
var_series = var.parametric()
print(f"Last VaR(5%): {var_series[-1]:.6f}")

es = ExpectedShortfall(results, alpha=0.05)
es_series = es.compute(method='parametric')
print(f"Last ES(5%): {es_series[-1]:.6f}")
```

## 6. Compare models

```python
from archbox.experiment import ArchExperiment

exp = ArchExperiment(returns)
exp.fit_all_models([
    ('GARCH', {'p': 1, 'q': 1}),
    ('EGARCH', {'p': 1, 'q': 1}),
    ('GJR', {'p': 1, 'q': 1}),
])
comparison = exp.compare_models()
print(comparison.ranking())
print(f"Best model: {comparison.best_model()}")
```

## 7. CLI

```bash
archbox estimate --model garch --data sp500.csv --p 1 --q 1 --output results.json
archbox risk --model garch --data sp500.csv --alpha 0.05
```
