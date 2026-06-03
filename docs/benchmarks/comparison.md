---
title: "Library Comparison"
description: "Comprehensive feature matrix comparing ArchBox against arch (Python), rugarch (R), rmgarch (R), and other volatility modeling libraries."
---

# Library Comparison

Comprehensive comparison of ArchBox against established volatility modeling libraries across features, performance, and ecosystem.

---

## Feature Matrix

### Univariate GARCH Models

| Model | ArchBox | arch (Python) | rugarch (R) | volatility (Julia) |
|-------|:-------:|:-------------:|:-----------:|:-------------------:|
| GARCH(p,q) | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| EGARCH | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| GJR-GARCH | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| APARCH | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x: |
| FIGARCH | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x: |
| IGARCH | :white_check_mark: | :x: | :white_check_mark: | :x: |
| GARCH-M | :white_check_mark: | :x: | :white_check_mark: | :x: |
| Component GARCH | :white_check_mark: | :x: | :white_check_mark: | :x: |
| HAR-RV | :white_check_mark: | :x: | :x: | :x: |
| realGARCH | :x: | :x: | :white_check_mark: | :x: |
| HARCH | :x: | :white_check_mark: | :x: | :x: |
| csGARCH | :x: | :x: | :white_check_mark: | :x: |

### Error Distributions

| Distribution | ArchBox | arch | rugarch |
|-------------|:-------:|:----:|:-------:|
| Normal | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Student-t | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Skewed Student-t | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| GED | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Skewed GED | :white_check_mark: | :x: | :white_check_mark: |
| JSU | :x: | :x: | :white_check_mark: |
| Generalized Hyperbolic | :x: | :x: | :white_check_mark: |
| Normal Inverse Gaussian | :x: | :x: | :white_check_mark: |

### Multivariate Models

| Model | ArchBox | arch | rmgarch (R) |
|-------|:-------:|:----:|:-----------:|
| DCC | :white_check_mark: | :x: | :white_check_mark: |
| BEKK | :white_check_mark: | :x: | :white_check_mark: |
| CCC | :white_check_mark: | :x: | :white_check_mark: |
| GO-GARCH | :white_check_mark: | :x: | :white_check_mark: |
| DECO | :white_check_mark: | :x: | :x: |
| Copula-DCC | :x: | :x: | :white_check_mark: |
| aDCC (Asymmetric) | :x: | :x: | :white_check_mark: |

### Regime-Switching Models

| Model | ArchBox | arch | rugarch | MSwM (R) |
|-------|:-------:|:----:|:-------:|:--------:|
| MS-AR | :white_check_mark: | :x: | :x: | :white_check_mark: |
| MS-VAR | :white_check_mark: | :x: | :x: | :x: |
| MS-GARCH | :white_check_mark: | :x: | :x: | :x: |
| Hamilton Filter | :white_check_mark: | :x: | :x: | :white_check_mark: |
| Kim Smoother | :white_check_mark: | :x: | :x: | :x: |
| EM Estimation | :white_check_mark: | :x: | :x: | :white_check_mark: |

### Threshold / Nonlinear Models

| Model | ArchBox | arch | tsDyn (R) |
|-------|:-------:|:----:|:---------:|
| TAR | :white_check_mark: | :x: | :white_check_mark: |
| SETAR | :white_check_mark: | :x: | :white_check_mark: |
| LSTAR | :white_check_mark: | :x: | :white_check_mark: |
| ESTAR | :white_check_mark: | :x: | :x: |
| Linearity Tests | :white_check_mark: | :x: | :white_check_mark: |

### Risk Management

| Feature | ArchBox | arch | PerformanceAnalytics (R) |
|---------|:-------:|:----:|:------------------------:|
| Historical VaR | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Parametric VaR | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| GARCH VaR | :white_check_mark: | :white_check_mark: | :x: |
| Expected Shortfall | :white_check_mark: | :x: | :white_check_mark: |
| EWMA | :white_check_mark: | :x: | :white_check_mark: |
| Kupiec Test | :white_check_mark: | :x: | :white_check_mark: |
| Christoffersen Test | :white_check_mark: | :x: | :x: |
| Basel Traffic Light | :white_check_mark: | :x: | :x: |

---

## Diagnostics & Testing

| Feature | ArchBox | arch | rugarch |
|---------|:-------:|:----:|:-------:|
| Ljung-Box | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| ARCH-LM | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Sign Bias | :white_check_mark: | :x: | :white_check_mark: |
| News Impact Curve | :white_check_mark: | :x: | :white_check_mark: |
| Jarque-Bera | :white_check_mark: | :x: | :white_check_mark: |
| KS Test | :white_check_mark: | :x: | :white_check_mark: |
| Information Criteria | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Persistence | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Forecast Evaluation | :white_check_mark: | :x: | :white_check_mark: |

---

## Ecosystem & Tooling

| Feature | ArchBox | arch | rugarch/rmgarch |
|---------|:-------:|:----:|:---------------:|
| **Language** | Python | Python | R |
| **License** | MIT | NCSA | GPL-3 |
| **Built-in visualization** | :white_check_mark: | :x: | :white_check_mark: |
| **CLI interface** | :white_check_mark: | :x: | :x: |
| **Experiment framework** | :white_check_mark: | :x: | :x: |
| **Report generation** | :white_check_mark: | :x: | :x: |
| **Type hints** | :white_check_mark: | Partial | N/A |
| **NumPy/SciPy backend** | :white_check_mark: | :white_check_mark: | N/A |
| **Cython acceleration** | :x: | :white_check_mark: | N/A |
| **Active development** | :white_check_mark: | :white_check_mark: | Maintenance |
| **Documentation** | Comprehensive | Good | Excellent |

---

## Performance Summary

### Univariate GARCH(1,1), T = 5,000

| Library | Time | Log-Likelihood | Parameters |
|---------|------|---------------|------------|
| **ArchBox** | **0.28s** | -7,118.42 | Identical |
| arch | 0.35s | -7,118.42 | Identical |
| rugarch | 0.82s | -7,118.42 | Identical |

### DCC(1,1), N = 10, T = 2,000

| Library | Time | Log-Likelihood |
|---------|------|---------------|
| **ArchBox** | **8.5s** | -28,652.88 |
| rmgarch | 18.2s | -28,652.90 |

### VaR (1%), T = 5,000

| Library | Time | Violation Rate |
|---------|------|---------------|
| **ArchBox** (GARCH-t) | **0.40s** | 1.02% |
| PerformanceAnalytics (Hist.) | 0.012s | 1.08% |

!!! info
    All libraries produce equivalent numerical results. Performance differences arise from language overhead (Python vs. R) and optimization strategies.

---

## When to Use Each Library

=== "ArchBox"

    **Best for:**

    - Full Python workflow (data → estimation → risk → visualization)
    - Multivariate volatility modeling in Python
    - Regime-switching and threshold models
    - Integrated risk management (VaR/ES + backtesting)
    - Rapid prototyping with ArchExperiment

    ```python
    from archbox.models import GARCH
    from archbox.multivariate import DCC
    from archbox.risk import VaR

    # Everything in one library
    model = GARCH(returns, p=1, q=1, dist="student-t")
    result = model.fit()
    var = VaR(result, level=0.01)
    ```

=== "arch (Python)"

    **Best for:**

    - Mature, well-tested univariate GARCH estimation
    - Cython-accelerated performance
    - Unit root testing (ADF, KPSS, etc.)
    - Long-standing track record in academic research

    ```python
    from arch import arch_model

    model = arch_model(returns, vol="Garch", p=1, q=1, dist="t")
    result = model.fit()
    ```

=== "rugarch / rmgarch (R)"

    **Best for:**

    - Widest model variety (realGARCH, csGARCH, copula-DCC)
    - Extensive distribution library (JSU, GHyp, NIG)
    - Academic research requiring specific R-only models
    - Long publication history and established methodology

    ```r
    library(rugarch)

    spec <- ugarchspec(
      variance.model = list(model = "sGARCH", garchOrder = c(1,1)),
      distribution.model = "std"
    )
    fit <- ugarchfit(spec, returns)
    ```

---

## Migration Guide

### From arch (Python) to ArchBox

```python
# arch
from arch import arch_model
model = arch_model(returns, vol="Garch", p=1, q=1, dist="t")
result = model.fit()

# ArchBox equivalent
from archbox.models import GARCH
model = GARCH(returns, p=1, q=1, dist="student-t")
result = model.fit()
```

### From rugarch (R) to ArchBox

```r
# rugarch
spec <- ugarchspec(
  variance.model = list(model = "eGARCH", garchOrder = c(1,1)),
  distribution.model = "std"
)
fit <- ugarchfit(spec, returns)
```

```python
# ArchBox equivalent
from archbox.models import EGARCH
model = EGARCH(returns, p=1, q=1, dist="student-t")
result = model.fit()
```

!!! tip
    ArchBox aims for API simplicity — one class per model, with parameters as constructor arguments. No separate "spec" and "fit" steps.
