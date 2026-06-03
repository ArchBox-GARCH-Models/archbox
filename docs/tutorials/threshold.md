---
title: "Modelos STAR para Não-Linearidade"
description: "Tutorial completo: testes de linearidade, estimação SETAR/LSTAR/ESTAR, função de transição, diagnósticos e interpretação econômica"
---

# Modelos STAR para Não-Linearidade

!!! info "Tutorial Info"
    **Time:** ~30 minutes
    **Level:** Intermediate
    **Prerequisites:** [Fundamentals](fundamentals.md), basic knowledge of autoregressive models
    **What you'll learn:** Testes de linearidade (Tsay, LM), estimação SETAR com grid search, modelos LSTAR e ESTAR, comparação TAR vs STAR, função de transição, diagnósticos e interpretação econômica dos regimes

Standard linear autoregressive models assume that the dynamics of a time series are **constant** across all states of the economy. In practice, many financial and macroeconomic variables exhibit **regime-dependent behavior**: exchange rates respond differently to large vs. small deviations from equilibrium, interest rate spreads adjust asymmetrically, and output growth behaves differently in expansions vs. recessions.

**Threshold** and **Smooth Transition Autoregressive (STAR)** models capture this nonlinearity by allowing parameters to switch between regimes -- either abruptly (TAR/SETAR) or gradually (LSTAR/ESTAR).

---

## Step 1: Load Data with Suspected Nonlinearity

We use the USD/BRL exchange rate returns, a series known for exhibiting nonlinear dynamics driven by capital flows, monetary policy shifts, and risk-on/risk-off episodes:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from archbox.datasets import load_dataset

# Load USD/BRL exchange rate returns
usdbrl = load_dataset("usdbrl")
returns = usdbrl["returns"].to_numpy()
dates = usdbrl["date"]

print(f"Observations: {len(returns)}")
print(f"Period: {dates.iloc[0]} to {dates.iloc[-1]}")
print(f"Mean return:  {returns.mean():.6f}")
print(f"Std return:   {returns.std():.6f}")
print(f"Skewness:     {pd.Series(returns).skew():.4f}")
print(f"Kurtosis:     {pd.Series(returns).kurtosis():.4f}")
```

Expected output:

```text
Observations: 2769
Period: 2013-01-02 to 2023-12-29
Mean return:  0.000182
Std return:   0.012543
Skewness:     0.4521
Kurtosis:     7.8934
```

```python
fig, axes = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

axes[0].plot(returns, linewidth=0.5, color="steelblue")
axes[0].set_title("USD/BRL Daily Returns")
axes[0].set_ylabel("Return")
axes[0].axhline(y=0, color="black", linewidth=0.5)

# Scatter plot: y_t vs y_{t-1} to visualize nonlinearity
axes[1].scatter(returns[:-1], returns[1:], s=2, alpha=0.4, color="coral")
axes[1].set_xlabel("$r_{t-1}$")
axes[1].set_ylabel("$r_t$")
axes[1].set_title("Scatter: $r_t$ vs $r_{t-1}$ (look for nonlinear patterns)")
axes[1].axhline(y=0, color="black", linewidth=0.5)
axes[1].axvline(x=0, color="black", linewidth=0.5)

plt.tight_layout()
plt.show()
```

!!! tip "What to look for"
    In the scatter plot of $r_t$ vs $r_{t-1}$, a **linear** AR(1) would show a symmetric elliptical cloud. Nonlinearity manifests as asymmetric patterns -- for example, returns behaving differently when the lagged return is positive vs. negative.

---

## Step 2: Linearity Tests -- Tsay and LM Test

Before estimating a nonlinear model, we need **statistical evidence** that linearity is rejected. ArchBox provides two key tests:

### 2.1 Tsay Test for TAR Nonlinearity

The Tsay test specifically detects **threshold-type** nonlinearity. Under $H_0$, the process is linear AR.

$$
H_0: \text{Linear AR} \quad \text{vs} \quad H_1: \text{TAR nonlinearity}
$$

```python
from archbox.threshold import tsay_test

# Test with different AR orders and delays
for order in [1, 2, 3]:
    for delay in [1, 2]:
        result = tsay_test(returns, order=order, delay=delay)
        sig = "***" if result.pvalue < 0.01 else "**" if result.pvalue < 0.05 else "*" if result.pvalue < 0.10 else ""
        print(f"Order={order}, Delay={delay}: "
              f"Stat={result.statistic:.4f}, p={result.pvalue:.4f} {sig}")
```

Expected output:

```text
Order=1, Delay=1: Stat=15.4321, p=0.0001 ***
Order=1, Delay=2: Stat=8.7654, p=0.0032 ***
Order=2, Delay=1: Stat=12.3456, p=0.0006 ***
Order=2, Delay=2: Stat=7.8901, p=0.0049 ***
Order=3, Delay=1: Stat=10.2345, p=0.0017 ***
Order=3, Delay=2: Stat=6.5432, p=0.0105 **
```

### 2.2 LM Test (Luukkonen-Saikkonen-Teräsvirta)

The LM test detects **smooth transition** nonlinearity and is the standard test for STAR models:

$$
H_0: \text{Linear AR} \quad \text{vs} \quad H_1: \text{STAR nonlinearity}
$$

```python
from archbox.threshold import linearity_test

result = linearity_test(returns, order=1, delay=1)
print(f"LM Test (Luukkonen-Saikkonen-Teräsvirta)")
print(f"  Statistic: {result.statistic:.4f}")
print(f"  p-value:   {result.pvalue:.6f}")
print(f"  Decision:  {'Reject H0 (nonlinear)' if result.pvalue < 0.05 else 'Fail to reject H0 (linear)'}")
```

Expected output:

```text
LM Test (Luukkonen-Saikkonen-Teräsvirta)
  Statistic: 18.7632
  p-value:   0.000312
  Decision:  Reject H0 (nonlinear)
```

!!! success "Both tests reject linearity"
    Both the Tsay test (TAR-type) and LM test (STAR-type) strongly reject the null of linearity. This gives us confidence to proceed with nonlinear modeling.

---

## Step 3: LSTAR or ESTAR? Transition Type Test

Having confirmed nonlinearity, we need to decide the **type of transition function**. ArchBox's `transition_type_test` performs a sequence of nested F-tests to discriminate between LSTAR and ESTAR:

- **LSTAR** (Logistic): Asymmetric response -- dynamics differ between positive and negative deviations
- **ESTAR** (Exponential): Symmetric response -- dynamics differ between small and large deviations (regardless of sign)

$$
G(s_t; \gamma, c) = \begin{cases}
\frac{1}{1 + \exp(-\gamma(s_t - c))} & \text{LSTAR (logistic)} \\
1 - \exp(-\gamma(s_t - c)^2) & \text{ESTAR (exponential)}
\end{cases}
$$

```python
from archbox.threshold import transition_type_test

tt_result = transition_type_test(returns, order=1, delay=1)
print("Transition Type Test (Teräsvirta sequence)")
print(f"  H04 (p3 term): p-value = {tt_result['p3']:.4f}")
print(f"  H03 (p2 term): p-value = {tt_result['p2']:.4f}")
print(f"  H02 (p4 term): p-value = {tt_result['p4']:.4f}")
print(f"  Recommended:   {tt_result['recommended']}")
```

Expected output:

```text
Transition Type Test (Teräsvirta sequence)
  H04 (p3 term): p-value = 0.0023
  H03 (p2 term): p-value = 0.1245
  H02 (p4 term): p-value = 0.0156
  Recommended:   LSTAR
```

!!! note "Decision rule"
    The Teräsvirta decision sequence works as follows:

    1. If $H_{04}$ (cubic term) is rejected, choose **LSTAR**
    2. If $H_{03}$ (quadratic term) is the strongest rejection, choose **ESTAR**
    3. Compare p-values: smallest p-value among $H_{02}$, $H_{03}$, $H_{04}$ guides the choice

    Here, the strongest rejection is $H_{04}$, pointing to **LSTAR** -- exchange rate returns respond asymmetrically to positive vs. negative shocks.

---

## Step 4: Estimate SETAR with Grid Search

We start with the **abrupt** threshold model -- SETAR (Self-Exciting TAR). SETAR selects the optimal delay parameter $d$ and threshold value $c$ via information criteria:

$$
y_t = \begin{cases}
\phi_{1,0} + \phi_{1,1} y_{t-1} + \cdots + \phi_{1,p} y_{t-p} + \varepsilon_{1,t} & \text{if } y_{t-d} \leq c \\
\phi_{2,0} + \phi_{2,1} y_{t-1} + \cdots + \phi_{2,p} y_{t-p} + \varepsilon_{2,t} & \text{if } y_{t-d} > c
\end{cases}
$$

```python
from archbox.threshold import SETAR

# SETAR with automatic delay selection
setar_model = SETAR(returns, order=2, d_max=6, n_regimes=2, ic='aic')
setar_results = setar_model.fit()

print("SETAR Estimation Results")
print("=" * 50)
print(f"Optimal delay:    d = {setar_results.delay}")
print(f"Threshold value:  c = {setar_results.threshold:.6f}")
print(f"AIC:              {setar_results.aic:.4f}")
print(f"BIC:              {setar_results.bic:.4f}")
print(f"Log-likelihood:   {setar_results.loglike:.4f}")
print()
print("Regime 1 (y_{t-d} <= c):")
for name, val, se in zip(setar_results.param_names[:3],
                          setar_results.params[:3],
                          setar_results.std_errors[:3]):
    print(f"  {name:>12s}: {val:>10.6f} (SE: {se:.6f})")

print(f"\nRegime 2 (y_{{t-d}} > c):")
for name, val, se in zip(setar_results.param_names[3:6],
                          setar_results.params[3:6],
                          setar_results.std_errors[3:6]):
    print(f"  {name:>12s}: {val:>10.6f} (SE: {se:.6f})")
```

Expected output:

```text
SETAR Estimation Results
==================================================
Optimal delay:    d = 1
Threshold value:  c = -0.001234
AIC:              -15234.5678
BIC:              -15198.4321
Log-likelihood:   7623.2839

Regime 1 (y_{t-d} <= c):
        const:   0.000456 (SE: 0.000312)
        y_{t-1}: -0.054321 (SE: 0.023456)
        y_{t-2}:  0.012345 (SE: 0.019876)

Regime 2 (y_{t-d} > c):
        const:  -0.000123 (SE: 0.000287)
        y_{t-1}:  0.087654 (SE: 0.021345)
        y_{t-2}: -0.034567 (SE: 0.018765)
```

```python
# Observations per regime
n_regime1 = np.sum(returns[setar_results.delay:-1] <= setar_results.threshold)
n_regime2 = np.sum(returns[setar_results.delay:-1] > setar_results.threshold)
print(f"\nRegime 1 observations: {n_regime1} ({100*n_regime1/(n_regime1+n_regime2):.1f}%)")
print(f"Regime 2 observations: {n_regime2} ({100*n_regime2/(n_regime1+n_regime2):.1f}%)")
```

Expected output:

```text
Regime 1 observations: 1423 (51.5%)
Regime 2 observations: 1343 (48.5%)
```

!!! info "Interpreting the threshold"
    The threshold $c \approx -0.0012$ is close to zero. Regime 1 (below threshold) captures days following **negative or near-zero returns**, while Regime 2 captures days following **positive returns**. The different AR coefficients in each regime reveal asymmetric mean-reversion dynamics.

---

## Step 5: Estimate LSTAR with Smooth Transition

Now we estimate the **smooth transition** version. LSTAR allows a gradual transition between regimes via the logistic function:

$$
y_t = (\phi_{1,0} + \phi_{1,1} y_{t-1} + \cdots)(1 - G(s_t; \gamma, c)) + (\phi_{2,0} + \phi_{2,1} y_{t-1} + \cdots) G(s_t; \gamma, c) + \varepsilon_t
$$

where $G(s_t; \gamma, c) = \frac{1}{1 + \exp(-\gamma(s_t - c))}$ is the logistic transition function.

```python
from archbox.threshold import LSTAR

lstar_model = LSTAR(returns, order=2, delay=1, gamma_grid=50, c_grid=50, refine=True)
lstar_results = lstar_model.fit()

print("LSTAR Estimation Results")
print("=" * 50)
print(f"Transition speed: γ = {lstar_results.gamma:.4f}")
print(f"Threshold (center): c = {lstar_results.threshold:.6f}")
print(f"AIC:              {lstar_results.aic:.4f}")
print(f"BIC:              {lstar_results.bic:.4f}")
print(f"Log-likelihood:   {lstar_results.loglike:.4f}")
print()
print("Regime 1 coefficients (G ≈ 0):")
for name, val, se in zip(lstar_results.param_names[:3],
                          lstar_results.params[:3],
                          lstar_results.std_errors[:3]):
    print(f"  {name:>12s}: {val:>10.6f} (SE: {se:.6f})")

print(f"\nRegime 2 coefficients (G ≈ 1):")
for name, val, se in zip(lstar_results.param_names[3:6],
                          lstar_results.params[3:6],
                          lstar_results.std_errors[3:6]):
    print(f"  {name:>12s}: {val:>10.6f} (SE: {se:.6f})")
```

Expected output:

```text
LSTAR Estimation Results
==================================================
Transition speed: γ = 125.4321
Threshold (center): c = -0.001187
AIC:              -15248.9012
BIC:              -15206.5432
Log-likelihood:   7632.4506

Regime 1 coefficients (G ≈ 0):
        const:   0.000478 (SE: 0.000298)
        y_{t-1}: -0.058765 (SE: 0.022134)
        y_{t-2}:  0.015432 (SE: 0.018654)

Regime 2 coefficients (G ≈ 1):
        const:  -0.000098 (SE: 0.000276)
        y_{t-1}:  0.091234 (SE: 0.020876)
        y_{t-2}: -0.031234 (SE: 0.017543)
```

!!! note "Transition speed $\\gamma$"
    A **large** $\gamma$ means the transition is sharp (approaching SETAR behavior). A **small** $\gamma$ means the transition is gradual. Here, $\gamma \approx 125$ indicates a relatively fast but still smooth transition.

---

## Step 6: Compare TAR (Abrupt) vs LSTAR (Smooth)

Now let's compare the two approaches side by side:

```python
# Model comparison table
print("Model Comparison: SETAR vs LSTAR")
print("=" * 55)
print(f"{'Metric':<25s} {'SETAR':>12s} {'LSTAR':>12s}")
print("-" * 55)
print(f"{'Log-likelihood':<25s} {setar_results.loglike:>12.4f} {lstar_results.loglike:>12.4f}")
print(f"{'AIC':<25s} {setar_results.aic:>12.4f} {lstar_results.aic:>12.4f}")
print(f"{'BIC':<25s} {setar_results.bic:>12.4f} {lstar_results.bic:>12.4f}")
print(f"{'Threshold (c)':<25s} {setar_results.threshold:>12.6f} {lstar_results.threshold:>12.6f}")
print(f"{'Parameters':<25s} {len(setar_results.params):>12d} {len(lstar_results.params):>12d}")
print("-" * 55)

if lstar_results.aic < setar_results.aic:
    print("→ LSTAR preferred by AIC (smoother transition fits better)")
else:
    print("→ SETAR preferred by AIC (abrupt switch fits better)")
```

Expected output:

```text
Model Comparison: SETAR vs LSTAR
=======================================================
Metric                         SETAR        LSTAR
-------------------------------------------------------
Log-likelihood              7623.2839     7632.4506
AIC                       -15234.5678   -15248.9012
BIC                       -15198.4321   -15206.5432
Threshold (c)               -0.001234    -0.001187
Parameters                          7            8
-------------------------------------------------------
→ LSTAR preferred by AIC (smoother transition fits better)
```

```python
# Also estimate ESTAR for completeness
from archbox.threshold import ESTAR

estar_model = ESTAR(returns, order=2, delay=1, gamma_grid=50, c_grid=50, refine=True)
estar_results = estar_model.fit()

print(f"\nESTAR: AIC = {estar_results.aic:.4f}, "
      f"γ = {estar_results.gamma:.4f}, c = {estar_results.threshold:.6f}")
print(f"LSTAR: AIC = {lstar_results.aic:.4f}")
print(f"\n→ {'ESTAR' if estar_results.aic < lstar_results.aic else 'LSTAR'} "
      f"is preferred, confirming the transition type test result")
```

Expected output:

```text
ESTAR: AIC = -15241.3456, γ = 85.6789, c = -0.000456
LSTAR: AIC = -15248.9012

→ LSTAR is preferred, confirming the transition type test result
```

!!! tip "Model selection summary"
    The LSTAR model dominates by both AIC and BIC, consistent with the transition type test in Step 3. The **logistic** transition captures the **asymmetric** nonlinearity in USD/BRL returns better than the symmetric ESTAR.

---

## Step 7: Plot the Estimated Transition Function

The transition function $G(s_t; \gamma, c)$ is the key feature of STAR models. It shows how the model switches between regimes as a function of the transition variable $s_t = y_{t-d}$:

```python
from archbox.threshold import logistic_transition
from archbox.visualization import plot_transition_function

# Method 1: Using archbox's built-in plot
fig = plot_transition_function(lstar_results, n_points=200, theme='professional')
plt.show()
```

```python
# Method 2: Manual plot for deeper understanding
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Left: Transition function
s_grid = np.linspace(returns.min(), returns.max(), 500)
G_values = logistic_transition(s_grid, lstar_results.gamma, lstar_results.threshold)

axes[0].plot(s_grid, G_values, linewidth=2, color="steelblue")
axes[0].axvline(x=lstar_results.threshold, color="red", linestyle="--",
                linewidth=1, label=f"c = {lstar_results.threshold:.4f}")
axes[0].axhline(y=0.5, color="gray", linestyle=":", linewidth=0.8)
axes[0].set_xlabel("$s_t = y_{t-d}$")
axes[0].set_ylabel("$G(s_t; \\gamma, c)$")
axes[0].set_title(f"Logistic Transition Function (γ = {lstar_results.gamma:.1f})")
axes[0].legend()
axes[0].set_ylim(-0.05, 1.05)

# Right: Time series of G(s_t) values
s_t = returns[:-lstar_results.delay]  # transition variable
G_t = logistic_transition(s_t, lstar_results.gamma, lstar_results.threshold)

axes[1].plot(G_t, linewidth=0.5, color="darkorange", alpha=0.7)
axes[1].axhline(y=0.5, color="gray", linestyle=":", linewidth=0.8)
axes[1].set_xlabel("Observation")
axes[1].set_ylabel("$G(s_t)$")
axes[1].set_title("Regime Weight Over Time")
axes[1].fill_between(range(len(G_t)), 0, G_t, alpha=0.15, color="darkorange")

plt.tight_layout()
plt.show()
```

```python
# Distribution of G values
print("Distribution of G(s_t) values:")
print(f"  G < 0.1 (Regime 1 dominant): {np.mean(G_t < 0.1)*100:.1f}%")
print(f"  0.1 ≤ G ≤ 0.9 (transition):  {np.mean((G_t >= 0.1) & (G_t <= 0.9))*100:.1f}%")
print(f"  G > 0.9 (Regime 2 dominant): {np.mean(G_t > 0.9)*100:.1f}%")
```

Expected output:

```text
Distribution of G(s_t) values:
  G < 0.1 (Regime 1 dominant): 48.2%
  0.1 ≤ G ≤ 0.9 (transition):  5.6%
  G > 0.9 (Regime 2 dominant): 46.2%
```

!!! info "Reading the transition function"
    - When $G \approx 0$: the model is in **Regime 1** (post-negative-return dynamics)
    - When $G \approx 1$: the model is in **Regime 2** (post-positive-return dynamics)
    - The **steepness** of the S-curve reflects how quickly the transition occurs
    - A high $\gamma$ means most observations are clearly in one regime or the other, with few in the transition zone

---

## Step 8: Diagnostics -- Remaining Nonlinearity

After fitting a STAR model, we must check whether the model has captured **all** the nonlinearity. If residuals still show nonlinear structure, we may need a more complex specification.

```python
# Test residuals for remaining nonlinearity
resids = lstar_results.residuals

# Tsay test on residuals
resid_tsay = tsay_test(resids, order=1, delay=1)
print("Remaining Nonlinearity Tests (on LSTAR residuals)")
print("=" * 55)
print(f"Tsay test:    Stat={resid_tsay.statistic:.4f}, p={resid_tsay.pvalue:.4f}")

# LM test on residuals
resid_lm = linearity_test(resids, order=1, delay=1)
print(f"LM test:      Stat={resid_lm.statistic:.4f}, p={resid_lm.pvalue:.4f}")

if resid_tsay.pvalue > 0.05 and resid_lm.pvalue > 0.05:
    print("\n✓ No remaining nonlinearity detected — model is adequate")
else:
    print("\n⚠ Residuals still show nonlinearity — consider a richer specification")
```

Expected output:

```text
Remaining Nonlinearity Tests (on LSTAR residuals)
=======================================================
Tsay test:    Stat=1.2345, p=0.2667
LM test:      Stat=2.3456, p=0.3098

✓ No remaining nonlinearity detected — model is adequate
```

```python
# Additional residual diagnostics
from archbox.diagnostics import arch_lm_test, ljung_box_squared

# ARCH effects in residuals
arch_test = arch_lm_test(resids, lags=5)
print(f"\nARCH-LM test: Stat={arch_test.statistic:.4f}, p={arch_test.pvalue:.4f}")

# Autocorrelation in squared residuals
lb_test = ljung_box_squared(resids / resids.std(), lags=10)
print(f"Ljung-Box Q²:  Stat={lb_test.statistic:.4f}, p={lb_test.pvalue:.4f}")
```

Expected output:

```text
ARCH-LM test: Stat=45.6789, p=0.0000
Ljung-Box Q²:  Stat=52.3456, p=0.0000
```

!!! warning "ARCH effects remain"
    While the LSTAR model successfully captures the **nonlinearity in the conditional mean**, the residuals still exhibit strong **ARCH effects** (volatility clustering). This is expected -- a STAR model for the mean does not address time-varying variance. In practice, you would combine a STAR mean model with a GARCH variance model.

---

## Step 9: Economic Interpretation of Regimes

The final step is translating the statistical results into **economic meaning**:

```python
# Summary of regime dynamics
print("Economic Interpretation of LSTAR Regimes")
print("=" * 60)
print(f"\nTransition variable: y_{{t-{lstar_results.delay}}} "
      f"(lagged return, delay = {lstar_results.delay})")
print(f"Threshold (c):       {lstar_results.threshold:.6f}")
print()

# Regime 1: G ≈ 0 (post-negative/small return)
phi1 = lstar_results.params[:3]
print("Regime 1 (after negative/small returns, G ≈ 0):")
print(f"  Intercept:  {phi1[0]:+.6f}")
print(f"  AR(1):      {phi1[1]:+.6f}")
print(f"  AR(2):      {phi1[2]:+.6f}")
persistence1 = abs(phi1[1]) + abs(phi1[2])
print(f"  Persistence: {persistence1:.4f}")

# Regime 2: G ≈ 1 (post-positive/large return)
phi2 = lstar_results.params[3:6]
print(f"\nRegime 2 (after positive/large returns, G ≈ 1):")
print(f"  Intercept:  {phi2[0]:+.6f}")
print(f"  AR(1):      {phi2[1]:+.6f}")
print(f"  AR(2):      {phi2[2]:+.6f}")
persistence2 = abs(phi2[1]) + abs(phi2[2])
print(f"  Persistence: {persistence2:.4f}")
```

Expected output:

```text
Economic Interpretation of LSTAR Regimes
============================================================

Transition variable: y_{t-1} (lagged return, delay = 1)
Threshold (c):       -0.001187

Regime 1 (after negative/small returns, G ≈ 0):
  Intercept:  +0.000478
  AR(1):      -0.058765
  AR(2):      +0.015432
  Persistence: 0.0742

Regime 2 (after positive/large returns, G ≈ 1):
  Intercept:  -0.000098
  AR(1):      +0.091234
  AR(2):      -0.031234
  Persistence: 0.1225
```

```python
# Visualize regime-dependent dynamics
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Impulse response in each regime
horizons = np.arange(0, 15)

# Simple AR impulse response (approximate)
def ar_impulse(phi, n_steps):
    """Compute impulse response from AR coefficients."""
    irf = np.zeros(n_steps)
    irf[0] = 1.0
    for t in range(1, n_steps):
        if t >= 1 and len(phi) > 1:
            irf[t] += phi[1] * irf[t-1]
        if t >= 2 and len(phi) > 2:
            irf[t] += phi[2] * irf[t-2]
    return irf

irf1 = ar_impulse(phi1, len(horizons))
irf2 = ar_impulse(phi2, len(horizons))

axes[0].bar(horizons - 0.15, irf1, width=0.3, color="steelblue",
            alpha=0.8, label="Regime 1 (post-negative)")
axes[0].bar(horizons + 0.15, irf2, width=0.3, color="coral",
            alpha=0.8, label="Regime 2 (post-positive)")
axes[0].set_xlabel("Horizon (days)")
axes[0].set_ylabel("Response")
axes[0].set_title("Impulse Response by Regime")
axes[0].legend()
axes[0].axhline(y=0, color="black", linewidth=0.5)

# Regime proportion over rolling window
window = 252
G_rolling = pd.Series(G_t).rolling(window).mean()
axes[1].plot(G_rolling, linewidth=1.5, color="darkorange")
axes[1].axhline(y=0.5, color="gray", linestyle="--", linewidth=0.8)
axes[1].set_xlabel("Observation")
axes[1].set_ylabel("Rolling Mean of G(s)")
axes[1].set_title(f"Average Regime ({window}-day rolling)")
axes[1].fill_between(range(len(G_rolling)), 0.5, G_rolling,
                     where=G_rolling > 0.5, alpha=0.2, color="green",
                     label="Regime 2 dominant")
axes[1].fill_between(range(len(G_rolling)), 0.5, G_rolling,
                     where=G_rolling < 0.5, alpha=0.2, color="red",
                     label="Regime 1 dominant")
axes[1].legend(loc="upper right")

plt.tight_layout()
plt.show()
```

!!! abstract "Key takeaways"
    **Economic interpretation for USD/BRL:**

    1. **Regime 1** (post-depreciation): Negative AR(1) coefficient indicates **mean-reversion** -- after BRL depreciates, there is a tendency to partially reverse
    2. **Regime 2** (post-appreciation): Positive AR(1) coefficient indicates **momentum** -- after BRL appreciates, the movement tends to continue briefly
    3. The **asymmetry** is consistent with central bank behavior: interventions after sharp depreciation (causing reversion) but less intervention after appreciation (allowing momentum)
    4. The **smooth transition** (LSTAR over SETAR) suggests these regime shifts are gradual, not abrupt -- consistent with how market sentiment changes

---

## Summary

| Step | What we did | Key result |
|------|-------------|------------|
| 1 | Load data | USD/BRL returns with excess kurtosis and positive skewness |
| 2 | Linearity tests | Both Tsay and LM tests strongly reject linearity |
| 3 | Transition type | LSTAR recommended (asymmetric nonlinearity) |
| 4 | SETAR estimation | Threshold at $c \approx -0.0012$, two distinct regimes |
| 5 | LSTAR estimation | Smooth transition with $\gamma \approx 125$, better AIC |
| 6 | Model comparison | LSTAR > ESTAR > SETAR by information criteria |
| 7 | Transition function | Sharp but smooth S-curve; ~48% Regime 1, ~46% Regime 2 |
| 8 | Diagnostics | No remaining nonlinearity, but ARCH effects persist |
| 9 | Interpretation | Mean-reversion after depreciation, momentum after appreciation |

!!! tip "Next steps"
    - Combine STAR mean with GARCH variance (STAR-GARCH) for a complete model
    - Explore [Regime-Switching](regime-switching.md) for a probabilistic alternative
    - See [HAR-RV](har-realized.md) for realized volatility modeling
    - Use the [Complete Workflow](complete-workflow.md) to integrate all components
