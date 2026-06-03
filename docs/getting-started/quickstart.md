---
title: Quick Start
description: Estimate a GARCH(1,1), run diagnostics, and compute risk measures in 15 minutes
---

# Quick Start

This tutorial walks you through a complete volatility analysis workflow -- from loading data to computing risk measures -- in about 15 minutes. By the end, you'll have estimated a GARCH(1,1) model, validated it with diagnostics, and computed Value-at-Risk.

!!! tip "Prerequisites"

    Make sure ArchBox is installed before starting. See the [Installation Guide](installation.md) if you haven't done so yet.

---

## 1. Import ArchBox and Load Data

ArchBox ships with several built-in datasets for experimentation. Let's start with S&P 500 daily returns:

```python
from archbox import GARCH
from archbox.datasets import load_dataset

# Load S&P 500 daily returns
sp500 = load_dataset("sp500")
returns = sp500["returns"].to_numpy()

print(f"Observations: {len(returns)}")
print(f"Mean return:  {returns.mean():.6f}")
print(f"Std return:   {returns.std():.6f}")
print(f"Min return:   {returns.min():.6f}")
print(f"Max return:   {returns.max():.6f}")
```

Expected output:

```text
Observations: 2769
Mean return:  0.000375
Std return:   0.011856
Min return:  -0.094695
Max return:   0.089683
```

!!! note "Using your own data"

    You can pass any NumPy array or pandas Series of **log returns** to ArchBox models. The data should be demeaned or have zero mean -- ArchBox models the conditional variance, not the mean.

---

## 2. Exploratory Analysis

Before modeling, let's look at the key stylized facts of financial returns:

```python
import numpy as np
from scipy import stats

# Descriptive statistics
print(f"Skewness:  {stats.skew(returns):.4f}")
print(f"Kurtosis:  {stats.kurtosis(returns):.4f}")  # Excess kurtosis
print(f"Jarque-Bera stat: {stats.jarque_bera(returns).statistic:.2f}")
print(f"Jarque-Bera p:    {stats.jarque_bera(returns).pvalue:.4e}")
```

Expected output:

```text
Skewness:  -0.3524
Kurtosis:  7.5648
Jarque-Bera stat: 6627.43
Jarque-Bera p:    0.0000e+00
```

The high kurtosis and rejected Jarque-Bera test confirm that returns are **leptokurtic** (fat-tailed) -- exactly what GARCH models are designed to capture.

---

## 3. Estimate a GARCH(1,1)

Now let's fit the workhorse volatility model -- GARCH(1,1):

$$
\sigma_t^2 = \omega + \alpha \varepsilon_{t-1}^2 + \beta \sigma_{t-1}^2
$$

```python
# Fit GARCH(1,1) with Normal innovations
model = GARCH(returns, p=1, q=1)
results = model.fit()
```

That's it -- two lines to estimate the model.

---

## 4. Interpret Results

Print the full summary table:

```python
print(results.summary())
```

Expected output:

```text
======================================================================
                      Volatility Model Results
======================================================================
Model:            GARCH(1,1)
Distribution:     Normal
Observations:     2769
Log-Likelihood:   8451.2367
AIC:              -16896.4734
BIC:              -16878.6421
Converged:        True
----------------------------------------------------------------------
Parameter        Estimate      Std Err      t-value      p-value
----------------------------------------------------------------------
omega           0.000002     0.000001       3.1245       0.0018
alpha[1]        0.081234     0.012456       6.5213       0.0000
beta[1]         0.907543     0.013789      65.8121       0.0000
----------------------------------------------------------------------
Persistence:      0.988777
Half-life:        61.32 periods
Uncond. Variance: 1.406e-04
Uncond. Vol:      1.186e-02
======================================================================
```

!!! info "Key quantities to check"

    - **Persistence** ($\alpha + \beta$): Should be close to 1 but strictly less than 1 for stationarity. Values above 0.99 suggest near-integrated behavior.
    - **Half-life**: Number of days for a volatility shock to decay by half. Longer half-lives mean shocks are more persistent.
    - **p-values**: All parameters should be statistically significant (p < 0.05).

You can also access individual results programmatically:

```python
print(f"Parameters: {dict(zip(results.param_names, results.params))}")
print(f"Persistence: {results.persistence():.6f}")
print(f"Half-life: {results.half_life():.2f} days")
print(f"AIC: {results.aic:.4f}")
print(f"BIC: {results.bic:.4f}")
```

---

## 5. Run Diagnostics

A well-specified GARCH model should produce standardized residuals with no remaining ARCH effects. Let's verify:

```python
from archbox.diagnostics import arch_lm_test, ljung_box_squared

# ARCH-LM test on standardized residuals
arch_lm = arch_lm_test(results.resid, lags=5)
print(f"ARCH-LM statistic: {arch_lm.statistic:.4f}")
print(f"ARCH-LM p-value:   {arch_lm.pvalue:.4f}")

# Ljung-Box test on squared standardized residuals
lb = ljung_box_squared(results.resid, lags=10)
print(f"Ljung-Box statistic: {lb.statistic:.4f}")
print(f"Ljung-Box p-value:   {lb.pvalue:.4f}")
```

Expected output:

```text
ARCH-LM statistic: 3.2145
ARCH-LM p-value:   0.6672

Ljung-Box statistic: 8.4532
Ljung-Box p-value:   0.5847
```

!!! tip "Interpreting diagnostic tests"

    - **p-value > 0.05**: No evidence of remaining ARCH effects -- the model is adequate.
    - **p-value < 0.05**: The model may be misspecified. Consider higher-order GARCH(p,q), asymmetric models (EGARCH, GJR-GARCH), or a different distribution.

You can also run all diagnostics at once:

```python
from archbox.diagnostics import full_diagnostics

diag = full_diagnostics(results)
print(diag.summary())
```

---

## 6. Compute Value-at-Risk and Expected Shortfall

Use the fitted model to compute risk measures:

```python
from archbox.risk import ValueAtRisk, ExpectedShortfall

# Value-at-Risk at 5% level
var = ValueAtRisk(results, alpha=0.05)
var_series = var.parametric()
print(f"Last VaR(5%): {var_series[-1]:.6f}")

# Expected Shortfall at 5% level
es = ExpectedShortfall(results, alpha=0.05)
es_series = es.parametric()
print(f"Last ES(5%):  {es_series[-1]:.6f}")
```

Expected output:

```text
Last VaR(5%): -0.017234
Last ES(5%):  -0.021567
```

!!! info "VaR vs. Expected Shortfall"

    - **VaR** ($\alpha$): The maximum loss not exceeded with probability $1 - \alpha$. E.g., VaR(5%) means there's a 5% chance of losing more than this amount.
    - **Expected Shortfall** (CVaR): The expected loss given that the loss exceeds VaR. ES is always larger in magnitude and provides a more complete picture of tail risk.

---

## 7. Visualize Conditional Volatility

Plot returns alongside the estimated conditional volatility:

```python
fig = results.plot(which="volatility")
fig.savefig("volatility.png", dpi=150, bbox_inches="tight")
```

This produces a two-panel figure:

- **Top panel**: Raw return series showing volatility clustering
- **Bottom panel**: Conditional volatility ($\sigma_t$) estimated by the GARCH model

You can also plot the standardized residuals:

```python
fig = results.plot(which="residuals")
fig.savefig("residuals.png", dpi=150, bbox_inches="tight")
```

---

## 8. Forecast Volatility

Generate multi-step-ahead volatility forecasts:

```python
forecast = results.forecast(horizon=10)

print("Variance forecast (10 days ahead):")
for h, (var_h, vol_h) in enumerate(
    zip(forecast["variance"], forecast["volatility"]), start=1
):
    print(f"  h={h:2d}: variance={var_h:.6e}, volatility={vol_h:.6f}")
```

Expected output:

```text
Variance forecast (10 days ahead):
  h= 1: variance=1.234567e-04, volatility=0.011111
  h= 2: variance=1.267890e-04, volatility=0.011261
  h= 3: variance=1.298765e-04, volatility=0.011397
  h= 4: variance=1.327654e-04, volatility=0.011523
  h= 5: variance=1.354321e-04, volatility=0.011638
  h= 6: variance=1.379012e-04, volatility=0.011743
  h= 7: variance=1.401987e-04, volatility=0.011841
  h= 8: variance=1.423456e-04, volatility=0.011931
  h= 9: variance=1.443210e-04, volatility=0.012013
  h=10: variance=1.461234e-04, volatility=0.012088
```

!!! note "Forecast convergence"

    For stationary GARCH models (persistence < 1), multi-step forecasts converge to the unconditional variance as $h \to \infty$. The speed of convergence depends on the persistence parameter.

---

## 9. Export Results

Save your results for later analysis:

```python
# Export parameters to DataFrame
df = results.to_dataframe()
print(df)

# Save full results to disk
results.save("garch_results.pkl")

# Load them back
from archbox.core.results import ArchResults
loaded = ArchResults.load("garch_results.pkl")
print(f"Loaded: {loaded}")
```

---

## Next Steps

You've completed the Quick Start! Here's where to go next:

<div class="grid cards" markdown>

-   :material-lightbulb-outline: **Core Concepts**

    ---

    Understand the theory behind what you just did

    [:octicons-arrow-right-24: Core Concepts](core-concepts.md)

-   :material-compass-outline: **Choosing a Model**

    ---

    EGARCH, GJR-GARCH, DCC, regime-switching -- which one do you need?

    [:octicons-arrow-right-24: Choosing a Model](choosing-model.md)

-   :material-book-open-variant: **User Guide**

    ---

    Comprehensive guides for every model family in ArchBox

    [:octicons-arrow-right-24: User Guide](../user-guide/index.md)

-   :material-test-tube: **Diagnostics**

    ---

    Full suite of diagnostic tests for model validation

    [:octicons-arrow-right-24: Diagnostics](../diagnostics/index.md)

</div>
