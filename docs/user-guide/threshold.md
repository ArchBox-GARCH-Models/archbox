# Threshold and STAR Models

## SETAR (Self-Exciting Threshold Autoregressive)

```python
from archbox.threshold.setar import SETAR
from archbox.datasets import load_dataset

ip = load_dataset('industrial_production')
data = ip['growth'].dropna().to_numpy()

model = SETAR(data, order=2, n_regimes=2)
results = model.fit()
print(results.summary())
print(f"Threshold: {results.threshold}")
```

## LSTAR (Logistic Smooth Transition Autoregressive)

```python
from archbox.threshold.lstar import LSTAR

model = LSTAR(data, order=2)
results = model.fit()
transition = results.transition_function()
```
