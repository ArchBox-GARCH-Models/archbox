---
title: "Benchmarks Overview"
description: "Performance benchmarks for ArchBox — methodology, hardware specifications, and overview of GARCH, multivariate, and risk model comparisons."
---

# Performance Benchmarks

ArchBox is designed for efficient estimation of volatility models, leveraging NumPy/SciPy vectorized operations and optimized BLAS/LAPACK backends. This section provides systematic benchmarks comparing ArchBox against established libraries.

!!! info "Benchmark Environment"
    All benchmarks were conducted on:

    - **CPU**: Intel i7-12700K (12 cores, 3.6 GHz)
    - **RAM**: 32 GB DDR4-3200
    - **OS**: Ubuntu 22.04 LTS
    - **Python**: 3.12 | **NumPy**: 2.0 (MKL) | **SciPy**: 1.14 | **pandas**: 2.2

    Results may vary depending on CPU, BLAS/LAPACK implementation (MKL vs OpenBLAS), data characteristics, and software versions.

---

## Performance at a Glance

| Model Family | Typical Size | ArchBox Time | Memory | Detail Page |
|-------------|-------------|-------------|--------|-------------|
| GARCH(1,1) | T=5,000 | ~0.3s | < 10 MB | [GARCH Benchmarks](garch.md) |
| EGARCH(1,1) | T=5,000 | ~0.5s | < 10 MB | [GARCH Benchmarks](garch.md) |
| DCC (N=5) | T=2,000 | ~2s | < 50 MB | [Multivariate Benchmarks](multivariate.md) |
| DCC (N=20) | T=2,000 | ~25s | ~200 MB | [Multivariate Benchmarks](multivariate.md) |
| VaR/ES | T=5,000 | < 0.5s | < 10 MB | [Risk Benchmarks](risk.md) |
| Feature comparison | — | — | — | [Comparison](comparison.md) |

!!! tip "Cross-Library Comparison"
    See [Comparison](comparison.md) for a feature matrix of ArchBox vs `arch` (Python), `rugarch`/`rmgarch` (R), and other tools.

---

## Methodology

### Data Generation

Benchmarks use **simulated data** from known DGPs (Data Generating Processes) to enable fair comparison across libraries:

- **Univariate**: simulated GARCH(1,1) with $\omega = 10^{-5}$, $\alpha = 0.08$, $\beta = 0.90$, Normal innovations
- **Multivariate**: simulated DCC with diagonal GARCH(1,1) marginals and constant initial correlation
- **Risk**: historical S&P 500 daily returns (1990–2023) for realistic VaR/ES evaluation

Sample sizes: **T = 1,000**, **5,000**, and **10,000** observations for scalability analysis.

### Timing

- Each benchmark is the **median of 10 runs** (after 2 warm-up runs)
- Timing includes estimation only (data loading and post-processing excluded)
- All libraries use default optimization settings unless otherwise noted

### Accuracy Metrics

- **Log-likelihood**: higher is better (closer to true DGP likelihood)
- **Parameter bias**: distance from true parameter values (simulated data only)
- **VaR coverage**: empirical violation rate vs. nominal level

### Reproducibility

All benchmark scripts are available in the repository:

```bash
# Run benchmarks locally
python benchmarks/run_garch.py
python benchmarks/run_multivariate.py
python benchmarks/run_risk.py
```

---

## Runtime Categories

### Fast (< 1 second)

- GARCH(1,1), EGARCH(1,1), GJR(1,1) with T < 5,000
- VaR and ES computation
- EWMA volatility
- Ljung-Box, ARCH-LM, and other diagnostic tests

### Medium (1–10 seconds)

- Higher-order GARCH (p > 1 or q > 1)
- DCC with N < 10 assets
- BEKK with N < 5 assets
- MS-GARCH with 2 regimes

### Slow (10–60 seconds)

- DCC with N > 10 assets
- BEKK with N > 5 assets
- GO-GARCH with N > 10 assets
- MS-GARCH with 3+ regimes

### Very Slow (> 60 seconds)

- DCC with N > 30 assets
- BEKK with N > 10 assets (not recommended)
- ArchExperiment with many model specifications

!!! warning "Scaling"
    Multivariate models scale poorly with the number of assets. See the [Multivariate Benchmarks](multivariate.md) for scaling analysis and recommendations.

---

## Hardware Impact

Performance varies significantly with hardware and BLAS backend:

| Configuration | Relative Speed |
|--------------|---------------|
| NumPy + MKL | 1.0x (baseline) |
| NumPy + OpenBLAS | 1.2–1.5x slower |
| Apple M1/M2 (Accelerate) | 0.8–1.0x |
| Older CPU (pre-2018) | 2–3x slower |

!!! tip
    To check your BLAS backend:

    ```python
    import numpy as np
    np.show_config()
    ```
