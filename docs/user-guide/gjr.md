# GJR-GARCH Models

## Overview

The GJR-GARCH model by Glosten, Jagannathan, and Runkle (1993) adds an
asymmetric term to capture leverage effects:

$$\sigma^2_t = \omega + (\alpha + \gamma I_{t-1}) \varepsilon^2_{t-1} + \beta \sigma^2_{t-1}$$

where $I_{t-1} = 1$ if $\varepsilon_{t-1} < 0$.

## Usage

```python
from archbox.models.gjr import GJR
from archbox.datasets import load_dataset

sp500 = load_dataset('sp500')
model = GJR(sp500['returns'], p=1, q=1)
results = model.fit()
print(results.summary())
```
