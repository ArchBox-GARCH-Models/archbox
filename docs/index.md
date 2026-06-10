---
title: ArchBox - Conditional Volatility Modeling for Python
description: Python library for ARCH/GARCH models, regime-switching, threshold/STAR, risk management (VaR/ES), and multivariate volatility
---

<div class="home-logo" markdown>
  ![ArchBox](assets/images/logo.svg)
</div>

**The complete Python toolkit for conditional volatility modeling.**

[![CI](https://github.com/NodesEcon/archbox/actions/workflows/tests.yml/badge.svg)](https://github.com/NodesEcon/archbox/actions/workflows/tests.yml)
[![PyPI](https://img.shields.io/pypi/v/garchbox)](https://pypi.org/project/garchbox/)
[![Python](https://img.shields.io/pypi/pyversions/garchbox)](https://pypi.org/project/garchbox/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Development Status](https://img.shields.io/badge/development%20status-alpha-orange)

9 univariate GARCH models | 5 multivariate models | Regime-switching | Threshold/STAR | VaR & ES | Numba-accelerated

---

## Quick Start

=== "GARCH + VaR (6 lines)"

    ```python
    import archbox as ab
    from archbox.datasets import load_dataset

    # Estimate GARCH(1,1) with Student-t innovations
    returns = load_dataset("sp500")["returns"]
    model = ab.GARCH(returns, p=1, q=1, dist="student-t")
    result = model.fit()

    # Compute 99% Value-at-Risk
    var = result.var(alpha=0.01)
    print(result.summary())
    ```

=== "EGARCH + Forecast (5 lines)"

    ```python
    from archbox import EGARCH
    from archbox.datasets import load_dataset

    returns = load_dataset("sp500")["returns"]
    model = EGARCH(returns, p=1, q=1)
    result = model.fit()
    forecast = result.forecast(horizon=10)
    print(forecast)
    ```

=== "DCC Multivariate (6 lines)"

    ```python
    from archbox.multivariate import DCC
    from archbox.datasets import load_dataset

    data = load_dataset("forex")
    model = DCC(data, p=1, q=1)
    result = model.fit()
    cov_matrix = result.conditional_covariance()
    print(result.summary())
    ```

---

## What's Inside

<div class="grid cards" markdown>

-   :material-chart-line: **GARCH Univariado**

    ---

    9 modelos: GARCH, EGARCH, GJR-GARCH, APARCH, FIGARCH, IGARCH, GARCH-M, Component GARCH, HAR-RV

    [:octicons-arrow-right-24: User Guide](user-guide/garch/index.md)

-   :material-chart-multiple: **GARCH Multivariado**

    ---

    DCC, BEKK, CCC, GO-GARCH, DECO -- correlacoes dinamicas e matrizes de covariancia condicionais

    [:octicons-arrow-right-24: User Guide](user-guide/multivariate/index.md)

-   :material-swap-horizontal: **Regime-Switching**

    ---

    MS-AR, MS-VAR, MS-GARCH -- modelos Markov-Switching com Hamilton Filter e Kim Smoother

    [:octicons-arrow-right-24: User Guide](user-guide/regime-switching/index.md)

-   :material-toggle-switch: **Threshold/STAR**

    ---

    TAR, SETAR, LSTAR, ESTAR -- modelos de limiar e transicao suave com testes de linearidade

    [:octicons-arrow-right-24: User Guide](user-guide/threshold/index.md)

-   :material-shield-check: **Gestao de Risco**

    ---

    VaR (parametrico, historico, Filtered HS, Monte Carlo), Expected Shortfall, EWMA, backtesting

    [:octicons-arrow-right-24: User Guide](user-guide/risk/index.md)

-   :material-chart-bar: **Visualizacao e Reports**

    ---

    Graficos de volatilidade, correlacao, regimes, risco e diagnosticos com temas customizaveis

    [:octicons-arrow-right-24: Visualization Guide](visualization/index.md)

</div>

---

## ArchBox vs. arch (Python) e rugarch (R)

| Feature | ArchBox | arch (Python) | rugarch (R) |
|:--------|:-------:|:-------------:|:-----------:|
| GARCH/EGARCH/GJR/APARCH | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| FIGARCH | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Component GARCH | :white_check_mark: | :x: | :white_check_mark: |
| HAR-RV | :white_check_mark: | :x: | :x: |
| DCC/CCC | :white_check_mark: | :x: | :white_check_mark: rmgarch |
| BEKK | :white_check_mark: | :x: | :white_check_mark: rmgarch |
| GO-GARCH | :white_check_mark: | :x: | :white_check_mark: rmgarch |
| DECO | :white_check_mark: | :x: | :x: |
| Regime-Switching (MS-AR/MS-GARCH) | :white_check_mark: | :x: | :x: |
| Threshold/STAR | :white_check_mark: | :x: | :x: |
| VaR/ES + Backtesting | :white_check_mark: | :x: | :white_check_mark: |
| Skewed-t / GED distributions | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Numba acceleration | :white_check_mark: | Cython | :x: |
| ArchExperiment pattern | :white_check_mark: | :x: | :x: |

---

## The NodesEcon Ecosystem

ArchBox is part of the **NodesEcon** ecosystem of Python libraries for quantitative economics and finance:

<div class="grid cards" markdown>

-   :material-table: **PanelBox**

    ---

    Panel data econometrics: 70+ models, GMM, spatial, stochastic frontier, quantile regression

-   :material-chart-bell-curve-cumulative: **ArchBox**

    ---

    Conditional volatility: GARCH family, regime-switching, threshold/STAR, VaR/ES

</div>

Each library follows the same design philosophy: **scikit-learn-inspired API**, comprehensive diagnostics, publication-ready output, and Numba-accelerated performance.

---

## Installation

```bash
pip install garchbox
```

> The PyPI distribution is named `garchbox`; the import name is `archbox`. Run `pip install garchbox`, then `import archbox`.

With optional extras:

```bash
pip install garchbox[dev]     # Development tools
pip install garchbox[docs]    # Documentation tools
pip install garchbox[test]    # Testing tools
```

See the [Installation Guide](getting-started/installation.md) for detailed instructions.

---

## Explore by Topic

<div class="grid cards" markdown>

-   :material-rocket-launch: **Getting Started**

    ---

    Install and estimate your first model in 5 minutes

    [:octicons-arrow-right-24: Quick Start](getting-started/quickstart.md)

-   :material-book-open-variant: **User Guide**

    ---

    Comprehensive guides for all model families

    [:octicons-arrow-right-24: User Guide](user-guide/index.md)

-   :material-test-tube: **Diagnostics**

    ---

    ARCH-LM, Ljung-Box, sign bias, news impact and more

    [:octicons-arrow-right-24: Diagnostics](diagnostics/index.md)

-   :material-notebook: **Tutorials**

    ---

    Step-by-step notebooks from fundamentals to advanced workflows

    [:octicons-arrow-right-24: Tutorials](tutorials/index.md)

-   :material-code-tags: **API Reference**

    ---

    Complete technical reference for all classes and functions

    [:octicons-arrow-right-24: API Reference](api/index.md)

-   :material-sigma: **Theory**

    ---

    Mathematical foundations: GARCH theory, multivariate models, risk measures

    [:octicons-arrow-right-24: Theory](theory/garch-theory.md)

</div>

---

## The GARCH(1,1) Model

At the core of ArchBox is the GARCH(1,1) model for conditional variance:

$$
\sigma_t^2 = \omega + \alpha \varepsilon_{t-1}^2 + \beta \sigma_{t-1}^2
$$

where $\omega > 0$, $\alpha \geq 0$, $\beta \geq 0$, and $\alpha + \beta < 1$ ensures stationarity. ArchBox extends this foundation with leverage effects (EGARCH, GJR), long memory (FIGARCH), multivariate dynamics (DCC, BEKK), and regime-dependent volatility (MS-GARCH).

---

## Citation

If you use ArchBox in academic research, please cite:

```bibtex
@software{archbox2026,
  title = {ArchBox: Conditional Volatility Modeling for Python},
  author = {NodesEcon Development Team},
  year = {2026},
  url = {https://github.com/NodesEcon/archbox},
  version = {0.1.0}
}
```

---

## Design Philosophy

ArchBox is built on four principles:

- **Ease of Use** -- A unified, scikit-learn-inspired API lets you go from returns to risk measures in a few lines of code.
- **Academic Rigor** -- Every estimator follows published econometrics papers and is cross-validated against rugarch (R) and arch (Python).
- **Performance** -- Numba-optimized critical paths deliver fast estimation even on large datasets.
- **Publication-Ready Output** -- LaTeX tables, interactive reports, and diagnostic visualizations are built in, not bolted on.
