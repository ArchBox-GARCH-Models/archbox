---
title: "Tutorials"
description: "Step-by-step tutorials for learning volatility modeling with ArchBox"
---

# Tutorials

ArchBox provides **8 tutorials** covering every aspect of volatility modeling -- from your first GARCH(1,1) to complete portfolio risk workflows. Each tutorial is self-contained with executable code and expected output.

!!! tip "Quick Start"
    New to ArchBox? Start with [Fundamentals](fundamentals.md) to estimate your first GARCH model,
    then explore [GARCH Variants](garch-variants.md) to learn about asymmetric models.

---

## Learning Paths

Choose a path based on your goals and experience level:

| Path | Level | Duration | Topics |
|------|-------|----------|--------|
| **Beginner** | :material-school: Beginner | 2--3 hours | Fundamentals, GARCH Variants, Risk Management |
| **Intermediate** | :material-flask: Intermediate | 4--6 hours | + Multivariate, Regime-Switching, Complete Workflow |
| **Advanced** | :material-trophy: Advanced | 8--10 hours | + Threshold/STAR, HAR-RV, Complete Workflow |

### :material-school: Beginner Path (2--3 hours)

For researchers and practitioners new to volatility modeling. Covers the core GARCH toolkit.

1. [Fundamentals](fundamentals.md) -- Estimate, diagnose, and forecast with GARCH(1,1) (30 min)
2. [GARCH Variants](garch-variants.md) -- Compare GARCH, EGARCH, and GJR for asymmetry (30 min)
3. [Risk Management](risk-management.md) -- VaR, Expected Shortfall, and backtesting (30 min)

### :material-flask: Intermediate Path (4--6 hours)

For researchers ready to model multivariate dependencies and regime changes.

1. Complete the **Beginner** path first
2. [Multivariate](multivariate.md) -- DCC, BEKK, and portfolio volatility (45 min)
3. [Regime-Switching](regime-switching.md) -- Markov-switching GARCH models (45 min)
4. [Complete Workflow](complete-workflow.md) -- End-to-end analysis pipeline (60 min)

### :material-trophy: Advanced Path (8--10 hours)

The complete ArchBox curriculum. Master every model family.

1. Complete the **Intermediate** path first
2. [Threshold/STAR](threshold.md) -- Nonlinear models with smooth transitions (45 min)
3. [HAR-RV](har-realized.md) -- Realized volatility and high-frequency data (45 min)
4. [Complete Workflow](complete-workflow.md) -- Full portfolio risk analysis (60 min)

---

## Tutorial Catalog

<div class="grid cards" markdown>

-   :material-school: **Fundamentals**

    ---

    Your first GARCH model: estimation, diagnostics, forecasting, and VaR

    **Time:** ~30 min | **Level:** Beginner

    **Prerequisites:** Basic Python, NumPy, introductory statistics

    [:octicons-arrow-right-24: Start Tutorial](fundamentals.md)

-   :material-chart-bell-curve-cumulative: **GARCH Variants**

    ---

    Compare GARCH, EGARCH, and GJR-GARCH for capturing leverage effects

    **Time:** ~30 min | **Level:** Beginner

    **Prerequisites:** [Fundamentals](fundamentals.md)

    [:octicons-arrow-right-24: Start Tutorial](garch-variants.md)

-   :material-shield-alert: **Risk Management**

    ---

    Value-at-Risk, Expected Shortfall, EWMA, and backtesting

    **Time:** ~30 min | **Level:** Beginner

    **Prerequisites:** [Fundamentals](fundamentals.md)

    [:octicons-arrow-right-24: Start Tutorial](risk-management.md)

-   :material-chart-scatter-plot: **Multivariate**

    ---

    DCC, BEKK, CCC, and portfolio covariance modeling

    **Time:** ~45 min | **Level:** Intermediate

    **Prerequisites:** [GARCH Variants](garch-variants.md)

    [:octicons-arrow-right-24: Start Tutorial](multivariate.md)

-   :material-swap-horizontal: **Regime-Switching**

    ---

    Markov-switching models for structural breaks and regime changes

    **Time:** ~45 min | **Level:** Intermediate

    **Prerequisites:** [Fundamentals](fundamentals.md)

    [:octicons-arrow-right-24: Start Tutorial](regime-switching.md)

-   :material-arrow-decision: **Threshold/STAR**

    ---

    TAR, SETAR, LSTAR, and ESTAR nonlinear models

    **Time:** ~45 min | **Level:** Advanced

    **Prerequisites:** [Regime-Switching](regime-switching.md)

    [:octicons-arrow-right-24: Start Tutorial](threshold.md)

-   :material-chart-areaspline: **HAR-RV**

    ---

    Realized volatility modeling with high-frequency data

    **Time:** ~45 min | **Level:** Advanced

    **Prerequisites:** [GARCH Variants](garch-variants.md)

    [:octicons-arrow-right-24: Start Tutorial](har-realized.md)

-   :material-rocket-launch: **Complete Workflow**

    ---

    End-to-end analysis: data to report with ArchExperiment

    **Time:** ~60 min | **Level:** Intermediate--Advanced

    **Prerequisites:** At least the Beginner path

    [:octicons-arrow-right-24: Start Tutorial](complete-workflow.md)

</div>

---

## Prerequisites

All tutorials assume:

- **Python 3.10+** with ArchBox installed (`pip install archbox`)
- **NumPy** and **pandas** basics (indexing, arrays, DataFrames)
- **Introductory statistics** (mean, variance, distributions, hypothesis testing)

For the theory behind the models, see the [Theory](../theory/garch-theory.md) section.

---

## Conventions

Throughout these tutorials, we follow these conventions:

| Convention | Meaning |
|------------|---------|
| `returns` | Log returns as a NumPy array |
| `results` | Fitted model results (`ArchResults` object) |
| `sigma_t` | Conditional volatility series |
| `z_t` | Standardized residuals ($z_t = \varepsilon_t / \sigma_t$) |
| Expected output | Approximate values -- your results may vary slightly |
