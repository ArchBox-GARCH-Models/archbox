# GARCH Models

## GARCH(1,1)

The standard GARCH(1,1) model:

```python
from archbox import GARCH
from archbox.datasets import load_dataset

sp500 = load_dataset('sp500')
returns = sp500['returns']

model = GARCH(returns, p=1, q=1)
results = model.fit()
print(results.summary())
```

## Higher-order GARCH

```python
model = GARCH(returns, p=2, q=2)
results = model.fit()
```

## With Student-t distribution

```python
model = GARCH(returns, p=1, q=1, dist='studentt')
results = model.fit()
```

## Variance targeting

```python
model = GARCH(returns, p=1, q=1)
results = model.fit(variance_targeting=True)
```

## Forecasting

```python
forecast = results.forecast(horizon=10)
print(forecast)
```

## Simulation

```python
sim_returns, sim_vol = model.simulate(n=1000, params=results.params, seed=42)
```
