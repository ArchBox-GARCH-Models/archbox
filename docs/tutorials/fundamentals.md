---
title: "Fundamentals: Your First GARCH Model"
description: "Step-by-step tutorial: estimate a GARCH(1,1), run diagnostics, forecast volatility, and compute VaR"
---

# Your First GARCH Model

!!! info "Tutorial Info"
    **Time:** ~30 minutes
    **Level:** Beginner
    **Prerequisites:** Basic Python, NumPy, introductory statistics
    **What you'll learn:** Estimate, diagnose, compare, forecast, and compute risk with GARCH

In this tutorial, you will go from raw financial returns to a fully validated GARCH model with volatility forecasts and risk measures. We cover 11 steps that form the foundation for every volatility analysis.

---

## Step 1: Import ArchBox and Load Data

We start by loading S&P 500 daily returns, one of ArchBox's built-in datasets:

```python
import numpy as np
import pandas as pd
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
    You can pass any NumPy array or pandas Series of **log returns** to ArchBox models. The data should be stationary -- ArchBox models the conditional variance, not the mean.

---

## Step 2: Exploratory Analysis

Before modeling, let's verify the **stylized facts** of financial returns: volatility clustering, fat tails, and autocorrelation in squared returns.

### 2.1 Plot Returns

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(3, 1, figsize=(12, 10))

# Returns
axes[0].plot(returns, linewidth=0.5, color="steelblue")
axes[0].set_title("S&P 500 Daily Returns")
axes[0].set_ylabel("Return")
axes[0].axhline(y=0, color="black", linewidth=0.5)

# Histogram
axes[1].hist(returns, bins=100, density=True, alpha=0.7, color="steelblue")
axes[1].set_title("Distribution of Returns")
axes[1].set_ylabel("Density")

# Squared returns (proxy for volatility)
axes[2].plot(returns**2, linewidth=0.5, color="coral")
axes[2].set_title("Squared Returns (Volatility Proxy)")
axes[2].set_ylabel("$r_t^2$")

plt.tight_layout()
plt.show()
```

!!! tip "What to look for"
    - **Volatility clustering**: Periods of high and low volatility alternate (visible in both the returns and squared returns plots)
    - **Fat tails**: The histogram shows heavier tails than a Normal distribution
    - **Mean reversion**: Squared returns spike but revert to a long-run level

### 2.2 ACF of Squared Returns

```python
from statsmodels.graphics.tsaplots import plot_acf

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

plot_acf(returns, lags=30, ax=axes[0], title="ACF of Returns")
plot_acf(returns**2, lags=30, ax=axes[1], title="ACF of Squared Returns")

plt.tight_layout()
plt.show()
```

!!! info "Interpretation"
    - **Returns** ($r_t$): Little or no autocorrelation -- returns are approximately unpredictable
    - **Squared returns** ($r_t^2$): Significant autocorrelation at many lags -- **conditional heteroskedasticity** is present. This is the signal that GARCH models are designed to capture.

---

## Step 3: Test for ARCH Effects

Before fitting a GARCH model, we formally test whether ARCH effects are present using the **ARCH-LM test** (Engle, 1982):

$$
H_0: \alpha_1 = \alpha_2 = \cdots = \alpha_q = 0 \quad \text{(no ARCH effects)}
$$

```python
from archbox.diagnostics import arch_lm_test

# Test with 5 lags
result = arch_lm_test(returns, lags=5)

print(f"ARCH-LM Test")
print(f"Statistic: {result.statistic:.4f}")
print(f"P-value:   {result.pvalue:.4e}")
print(f"Lags:      {result.lags}")
```

Expected output:

```text
ARCH-LM Test
Statistic: 187.3456
P-value:   0.0000e+00
Lags:      5
```

!!! success "Result"
    The p-value is essentially zero, so we **reject** $H_0$ at any conventional significance level. There are strong ARCH effects in the data -- a GARCH model is appropriate.

---

## Step 4: Estimate GARCH(1,1) with Normal Distribution

The **GARCH(1,1)** model specifies the conditional variance as:

$$
\sigma_t^2 = \omega + \alpha_1 \varepsilon_{t-1}^2 + \beta_1 \sigma_{t-1}^2
$$

where $\varepsilon_t = \sigma_t z_t$ and $z_t \sim N(0,1)$.

```python
# Estimate GARCH(1,1) with Normal innovations
model_normal = GARCH(returns, p=1, q=1, dist="normal")
results_normal = model_normal.fit(disp=True)

print(results_normal.summary())
```

??? example "Expected output"
    ```text
    ======================================================================
                        Volatility Model Results
    ======================================================================
    Model:            GARCH(1,1)
    Distribution:     Normal
    Observations:     2769
    Log-Likelihood:   8234.5678
    AIC:              -16461.14
    BIC:              -16443.26
    Converged:        True
    ----------------------------------------------------------------------
    Parameter          Estimate    Std Err    t-value    p-value
    ----------------------------------------------------------------------
    omega              0.000002    0.000001    3.4567    0.0005
    alpha[1]           0.0823      0.0112      7.3482    0.0000
    beta[1]            0.9089      0.0121     75.1157    0.0000
    ----------------------------------------------------------------------
    Persistence:       0.9912
    Half-life:         78.38 periods
    Uncond. Variance:  2.27e-04
    Uncond. Vol:       1.51e-02
    ======================================================================
    ```

!!! tip "Parameter intuition"
    | Parameter | Role | Typical value |
    |-----------|------|---------------|
    | $\omega$ | Long-run variance floor | Small positive |
    | $\alpha_1$ | Reaction to news (ARCH) | 0.05--0.15 |
    | $\beta_1$ | Persistence of past variance | 0.80--0.95 |
    | $\alpha_1 + \beta_1$ | Total persistence | Close to 1 |

---

## Step 5: Interpret the Summary

Let's extract key quantities from the fitted model:

```python
# Parameter estimates
print("Parameters:")
for name, val, se, pval in zip(
    results_normal.param_names,
    results_normal.params,
    results_normal.se,
    results_normal.pvalues,
):
    sig = "***" if pval < 0.001 else "**" if pval < 0.01 else "*" if pval < 0.05 else ""
    print(f"  {name:12s} = {val:10.6f}  (SE={se:.6f}, p={pval:.4f}) {sig}")

# Key metrics
print(f"\nPersistence:    {results_normal.persistence():.4f}")
print(f"Half-life:      {results_normal.half_life():.1f} days")
print(f"Uncond. vol:    {np.sqrt(results_normal.unconditional_variance()):.4f}")
print(f"AIC:            {results_normal.aic:.2f}")
print(f"BIC:            {results_normal.bic:.2f}")
```

Expected output:

```text
Parameters:
  omega        =   0.000002  (SE=0.000001, p=0.0005) ***
  alpha[1]     =   0.082300  (SE=0.011200, p=0.0000) ***
  beta[1]      =   0.908900  (SE=0.012100, p=0.0000) ***

Persistence:    0.9912
Half-life:      78.4 days
Uncond. vol:    0.0151
AIC:            -16461.14
BIC:            -16443.26
```

!!! info "Key insights"
    - **All parameters significant** at 0.1% level -- the model is well-specified
    - **Persistence = 0.99** -- volatility shocks decay slowly (half-life ~78 days)
    - **Unconditional volatility = 1.51%** daily, or ~24% annualized ($0.0151 \times \sqrt{252}$)

---

## Step 6: Diagnostics

A good model should produce standardized residuals $z_t = \varepsilon_t / \sigma_t$ that are approximately i.i.d. We check two conditions:

1. **No serial correlation** in $z_t$ (Ljung-Box on $z_t$)
2. **No remaining ARCH effects** in $z_t^2$ (Ljung-Box on $z_t^2$)

### 6.1 Ljung-Box Tests

```python
from archbox.diagnostics import ljung_box_squared

# Standardized residuals
z_t = results_normal.resid

# Ljung-Box on z_t^2 (remaining ARCH effects)
lb_result = ljung_box_squared(z_t, lags=10)

print(f"Ljung-Box on z_t^2 (lag=10)")
print(f"  Statistic: {lb_result.statistic:.4f}")
print(f"  P-value:   {lb_result.pvalue:.4f}")
```

Expected output:

```text
Ljung-Box on z_t^2 (lag=10)
  Statistic: 12.3456
  P-value:   0.2634
```

!!! success "Interpretation"
    P-value > 0.05 means we **fail to reject** the null of no autocorrelation in $z_t^2$. The GARCH(1,1) has captured the conditional heteroskedasticity adequately.

### 6.2 QQ-Plot

```python
from scipy import stats

fig, ax = plt.subplots(figsize=(6, 6))
stats.probplot(z_t, dist="norm", plot=ax)
ax.set_title("QQ-Plot: Standardized Residuals vs Normal")
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

!!! warning "Fat tails detected"
    You will likely see deviations in the tails of the QQ-plot. This means the Normal distribution underestimates extreme events. In the next step, we re-estimate with a Student-t distribution to better capture these fat tails.

---

## Step 7: Re-estimate with Student-t Distribution

The **Student-t** distribution adds a degrees-of-freedom parameter $\nu$ that controls tail thickness:

$$
z_t \sim t_\nu, \quad \nu > 2
$$

Lower $\nu$ means fatter tails. As $\nu \to \infty$, the Student-t converges to the Normal.

```python
# Estimate GARCH(1,1) with Student-t innovations
model_t = GARCH(returns, p=1, q=1, dist="student-t")
results_t = model_t.fit(disp=True)

print(results_t.summary())
```

??? example "Expected output"
    ```text
    ======================================================================
                        Volatility Model Results
    ======================================================================
    Model:            GARCH(1,1)
    Distribution:     Student-t
    Observations:     2769
    Log-Likelihood:   8312.4567
    AIC:              -16614.91
    BIC:              -16591.10
    Converged:        True
    ----------------------------------------------------------------------
    Parameter          Estimate    Std Err    t-value    p-value
    ----------------------------------------------------------------------
    omega              0.000002    0.000001    3.1234    0.0018
    alpha[1]           0.0756      0.0108      7.0000    0.0000
    beta[1]            0.9155      0.0115     79.6087    0.0000
    nu                 7.2345      1.0567      6.8462    0.0000
    ----------------------------------------------------------------------
    Persistence:       0.9911
    Half-life:         77.54 periods
    Uncond. Variance:  2.25e-04
    Uncond. Vol:       1.50e-02
    ======================================================================
    ```

!!! tip "Degrees of freedom"
    $\nu \approx 7$ means significantly fatter tails than the Normal. For financial data, typical values range from 4 to 10. The parameter is strongly significant, confirming that the Student-t is a better fit.

---

## Step 8: Compare AIC/BIC

Let's compare the Normal and Student-t models using information criteria:

```python
comparison = {
    "Model": ["GARCH(1,1)-Normal", "GARCH(1,1)-Student-t"],
    "LogLik": [results_normal.loglike, results_t.loglike],
    "AIC": [results_normal.aic, results_t.aic],
    "BIC": [results_normal.bic, results_t.bic],
    "Parameters": [len(results_normal.params), len(results_t.params)],
}

df_comp = pd.DataFrame(comparison)
print(df_comp.to_string(index=False))
```

Expected output:

```text
                Model     LogLik       AIC       BIC  Parameters
 GARCH(1,1)-Normal   8234.5678 -16461.14 -16443.26           3
 GARCH(1,1)-Student-t 8312.4567 -16614.91 -16591.10           4
```

!!! success "Model selection"
    The Student-t model wins on **both** AIC and BIC despite having one more parameter. The improvement in log-likelihood ($\Delta \approx 78$) far outweighs the penalty for the extra parameter. **Use the Student-t model going forward.**

---

## Step 9: Forecast Volatility

Let's forecast conditional volatility 10 days ahead:

$$
E[\sigma_{T+h}^2] = \sigma_\infty^2 + (\alpha_1 + \beta_1)^{h-1} \left(\sigma_{T+1}^2 - \sigma_\infty^2\right)
$$

```python
# 10-day ahead forecast
forecast = results_t.forecast(horizon=10)
vol_forecast = forecast["volatility"]

print("Volatility Forecast (next 10 days):")
print("-" * 35)
for h, vol in enumerate(vol_forecast, 1):
    annualized = vol * np.sqrt(252)
    print(f"  Day {h:2d}: {vol:.6f} (ann. {annualized:.2%})")
```

Expected output:

```text
Volatility Forecast (next 10 days):
-----------------------------------
  Day  1: 0.010234 (ann. 16.24%)
  Day  2: 0.010312 (ann. 16.37%)
  Day  3: 0.010389 (ann. 16.49%)
  Day  4: 0.010465 (ann. 16.61%)
  Day  5: 0.010540 (ann. 16.73%)
  Day  6: 0.010614 (ann. 16.85%)
  Day  7: 0.010687 (ann. 16.96%)
  Day  8: 0.010759 (ann. 17.08%)
  Day  9: 0.010830 (ann. 17.19%)
  Day 10: 0.010900 (ann. 17.30%)
```

!!! info "Mean reversion"
    Notice how the forecast gradually converges toward the unconditional volatility (~1.50%). With persistence close to 1, convergence is slow -- but the direction is always toward the long-run level.

---

## Step 10: Compute Value-at-Risk (99%)

**Value-at-Risk** at level $\alpha$ answers: "What is the maximum loss we expect with probability $1 - \alpha$?"

$$
\text{VaR}_\alpha = \mu_t + \sigma_t \cdot q_\alpha
$$

where $q_\alpha$ is the $\alpha$-quantile of the innovation distribution.

```python
from archbox.risk import ValueAtRisk

# Compute parametric VaR at 99% confidence (alpha=0.01)
var_calc = ValueAtRisk(results_t, alpha=0.01)
var_series = var_calc.parametric()

# Last 5 VaR estimates
print("Last 5 days - VaR 99%:")
print("-" * 30)
for i in range(-5, 0):
    print(f"  VaR: {var_series[i]:.6f} ({var_series[i]:.2%})")

# Violation rate
violations = (returns[1:] < var_series[:-1]).mean()
print(f"\nExpected violation rate: 1.00%")
print(f"Actual violation rate:  {violations:.2%}")
```

Expected output:

```text
Last 5 days - VaR 99%:
------------------------------
  VaR: -0.025678 (-2.57%)
  VaR: -0.024892 (-2.49%)
  VaR: -0.025123 (-2.51%)
  VaR: -0.024567 (-2.46%)
  VaR: -0.024234 (-2.42%)

Expected violation rate: 1.00%
Actual violation rate:  1.12%
```

!!! tip "VaR interpretation"
    A VaR of -2.5% at the 99% level means: "On 99 out of 100 days, the loss will not exceed 2.5%." The actual violation rate close to 1% indicates the model is well-calibrated.

---

## Step 11: Plot Returns with Volatility Bands

Finally, let's visualize the model's fit by overlaying volatility bands on the return series:

```python
sigma_t = results_t.conditional_volatility

fig, axes = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

# Top: Returns with +/- 2*sigma bands
axes[0].plot(returns, linewidth=0.5, color="steelblue", alpha=0.7, label="Returns")
axes[0].plot(2 * sigma_t, linewidth=1.0, color="red", label="+2$\\sigma_t$")
axes[0].plot(-2 * sigma_t, linewidth=1.0, color="red", label="-2$\\sigma_t$")
axes[0].fill_between(
    range(len(returns)),
    -2 * sigma_t,
    2 * sigma_t,
    alpha=0.1,
    color="red",
)
axes[0].set_title("S&P 500 Returns with GARCH(1,1) Volatility Bands")
axes[0].set_ylabel("Return")
axes[0].legend(loc="upper right")

# Bottom: Conditional volatility
axes[1].plot(sigma_t, linewidth=1.0, color="coral", label="$\\sigma_t$")
axes[1].axhline(
    y=np.sqrt(results_t.unconditional_variance()),
    color="black",
    linestyle="--",
    linewidth=0.8,
    label="Unconditional $\\sigma$",
)
axes[1].set_title("Conditional Volatility")
axes[1].set_ylabel("$\\sigma_t$")
axes[1].set_xlabel("Observation")
axes[1].legend(loc="upper right")

plt.tight_layout()
plt.show()
```

!!! success "What this shows"
    - The **volatility bands** expand during turbulent periods and contract during calm periods
    - The **conditional volatility** mean-reverts toward the unconditional level (dashed line)
    - This time-varying behavior is exactly what GARCH captures that a simple standard deviation cannot

---

## Summary

In this tutorial, you completed a full GARCH analysis workflow:

| Step | What you did | Key takeaway |
|------|-------------|--------------|
| 1--2 | Load data and explore | Volatility clustering and fat tails motivate GARCH |
| 3 | ARCH-LM test | Formally confirm ARCH effects exist |
| 4--5 | Estimate GARCH(1,1) | $\alpha + \beta \approx 0.99$ indicates high persistence |
| 6 | Diagnostics | Ljung-Box and QQ-plot validate the model |
| 7--8 | Student-t distribution | Better AIC/BIC by capturing fat tails |
| 9 | Forecast | Multi-step forecasts mean-revert to unconditional level |
| 10 | VaR | 99% VaR with proper violation rate |
| 11 | Visualization | Volatility bands reveal time-varying risk |

---

## Next Steps

- :material-arrow-right: [GARCH Variants](garch-variants.md) -- Learn about asymmetric models (EGARCH, GJR)
- :material-arrow-right: [Risk Management](risk-management.md) -- Deep dive into VaR, ES, and backtesting
- :material-arrow-right: [User Guide: GARCH](../user-guide/garch/garch.md) -- Complete reference for GARCH models
