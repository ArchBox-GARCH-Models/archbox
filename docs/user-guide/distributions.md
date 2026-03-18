# Distributions

## Available distributions

| Distribution | Parameter | Use case |
|:-------------|:----------|:---------|
| Normal | - | Default, baseline |
| Student-t | nu (degrees of freedom) | Heavy tails |
| Skewed-t | nu, lambda | Asymmetry + heavy tails |
| GED | nu (shape) | Flexible tail weight |

## Usage

```python
from archbox import GARCH

# Normal (default)
model = GARCH(returns, p=1, q=1, dist='normal')

# Student-t
model = GARCH(returns, p=1, q=1, dist='studentt')

# Skewed-t
model = GARCH(returns, p=1, q=1, dist='skewt')

# GED
model = GARCH(returns, p=1, q=1, dist='ged')
```
