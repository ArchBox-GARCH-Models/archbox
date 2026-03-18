# Multivariate Models

## DCC (Dynamic Conditional Correlation)

```python
from archbox.multivariate.dcc import DCC
from archbox.datasets import load_dataset

fx = load_dataset('fx_majors')
returns = fx[['usd_eur', 'usd_gbp']].dropna().to_numpy()

model = DCC(returns, p=1, q=1)
results = model.fit()

# Dynamic correlation
dyn_corr = results.dynamic_correlation()

# Portfolio variance
weights = [0.5, 0.5]
port_var = results.portfolio_variance(weights)
```

## CCC (Constant Conditional Correlation)

```python
from archbox.multivariate.ccc import CCC

model = CCC(returns)
results = model.fit()
R = results.constant_correlation
```
