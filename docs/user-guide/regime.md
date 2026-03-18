# Regime-Switching Models

## MS-AR (Markov-Switching Autoregressive)

```python
from archbox.regime.ms_ar import MSAR
from archbox.datasets import load_dataset

gdp = load_dataset('us_gdp')
data = gdp['growth'].dropna().to_numpy()

model = MSAR(data, k_regimes=2, order=4)
results = model.fit(method='em')
print(results.summary())

# Smoothed probabilities
probs = results.smoothed_probabilities()

# Regime classification
regimes = results.classify_regimes()

# Transition matrix
P = results.transition_matrix
```

## Interpretation

- Regime 0: typically expansion (higher mean growth)
- Regime 1: typically recession (lower or negative mean growth)
- Transition probabilities indicate regime persistence
