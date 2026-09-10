---
title: "Local Performance Benchmarks"
description: "Wall-clock targets for the archbox benchmark suite and how to run it locally."
---

# Local Performance Benchmarks

This page documents the wall-clock suite shipped in `tests/benchmarks/`. For the
cross-library comparison see [Benchmarks Overview](index.md).

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

!!! warning "Targets are machine-dependent"
    The numbers above were measured on the reference machine described in
    [Benchmarks Overview](index.md). They are wall-clock assertions, so they can
    fail on a loaded CI runner or a slower CPU without anything being wrong with
    the library.

## Enabling Numba

Numba is an optional extra:

```bash
pip install "garchbox[numba]"
```

```python
from archbox.utils.backend import set_backend

set_backend("numba")   # 'auto' (default), 'numba', or 'python'
```

## Running the benchmarks

Benchmarks carry the `benchmark` pytest marker and are **deselected by default**
(`addopts` in `pyproject.toml` contains `-m "not benchmark"`), so a normal
`pytest` run never pays for them. Run them explicitly:

```bash
# The whole benchmark suite
pytest tests/benchmarks -m benchmark -v -s

# A single file
pytest tests/benchmarks/test_performance.py -m benchmark -v -s
pytest tests/benchmarks/test_scaling.py -m benchmark -v -s

# Everything, benchmarks included
pytest -m ""
```

`-s` is what lets the per-scenario timings reach your terminal.

!!! note "Backend isolation"
    Benchmarks that force a backend use the `restore_backend` fixture, so a
    failed timing assertion can no longer leave the process pinned to the
    pure-Python (or numba) backend for the rest of the session.
