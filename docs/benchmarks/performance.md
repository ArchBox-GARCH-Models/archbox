# Performance Benchmarks

## Targets

| Scenario | Target | Backend |
|:---------|:-------|:--------|
| GARCH(1,1) T=1000 | < 100ms | Python |
| GARCH(1,1) T=1000 | < 10ms | Numba |
| GARCH(1,1) T=10000 | < 50ms | Numba |
| EGARCH(1,1) T=1000 | < 15ms | Numba |
| DCC (2 series) T=1000 | < 500ms | Auto |
| DCC (5 series) T=1000 | < 2s | Auto |
| MS-AR(2,4) T=500 EM | < 5s | Auto |
| Hamilton filter T=1000 k=2 | < 10ms | Numba |
| VaR Monte Carlo 10K sims | < 5s | Auto |

## Enabling Numba

```python
from archbox.utils.backend import set_backend
set_backend('numba')
```

## Running benchmarks

```bash
pytest tests/benchmarks/test_performance.py -v -s
pytest tests/benchmarks/test_scaling.py -v -s
```
