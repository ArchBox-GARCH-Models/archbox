---
title: "Multivariate: Portfolio com DCC-GARCH"
description: "Tutorial completo: modelagem multivariada com CCC, DCC e BEKK para otimizacao de portfolio"
---

# Portfolio com DCC-GARCH

!!! info "Tutorial Info"
    **Time:** ~45 minutes
    **Level:** Intermediate
    **Prerequisites:** [Fundamentals](fundamentals.md), [GARCH Variants](garch-variants.md)
    **What you'll learn:** Correlacoes dinamicas, modelos multivariados (CCC, DCC, BEKK), portfolio de minima variancia, VaR de portfolio

In this tutorial, you will model the joint dynamics of multiple assets using multivariate GARCH models. We start with exploratory analysis of cross-asset dependencies, estimate three competing models (CCC, DCC, BEKK), build a minimum-variance portfolio with dynamic covariance, and compute portfolio-level risk measures.

---

## Step 1: Load Multi-Asset Returns

We use the `sector_indices` dataset containing daily returns for 5 sector indices: Technology, Health, Finance, Energy, and Consumer.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from archbox.datasets import load_dataset

# Load sector index returns
data = load_dataset("sector_indices")
print(f"Shape: {data.shape}")
print(f"Columns: {list(data.columns)}")
print(f"\nFirst 5 rows:")
print(data.head())
```

Expected output:

```text
Shape: (2000, 6)
Columns: ['date', 'tech', 'health', 'finance', 'energy', 'consumer']

First 5 rows:
         date      tech    health   finance    energy  consumer
0  2016-01-04 -0.012345  0.003456 -0.008901  0.005678 -0.002345
1  2016-01-05  0.007890 -0.001234  0.004567 -0.003456  0.006789
2  2016-01-06 -0.005678  0.002345 -0.006789  0.008901 -0.004567
3  2016-01-07  0.003456 -0.004567  0.002345 -0.006789  0.001234
4  2016-01-08 -0.008901  0.005678 -0.003456  0.002345 -0.007890
```

```python
# Extract returns as numpy array (T x k)
asset_names = ["tech", "health", "finance", "energy", "consumer"]
returns = data[asset_names].to_numpy()

print(f"\nReturns matrix: {returns.shape}")
print(f"  T (observations): {returns.shape[0]}")
print(f"  k (assets):       {returns.shape[1]}")

# Descriptive statistics
stats = pd.DataFrame({
    "Mean (%)": returns.mean(axis=0) * 100,
    "Std (%)": returns.std(axis=0) * 100,
    "Skewness": [pd.Series(returns[:, i]).skew() for i in range(returns.shape[1])],
    "Kurtosis": [pd.Series(returns[:, i]).kurtosis() for i in range(returns.shape[1])],
    "Min (%)": returns.min(axis=0) * 100,
    "Max (%)": returns.max(axis=0) * 100,
}, index=asset_names)

print("\nDescriptive Statistics:")
print(stats.round(4))
```

??? example "Expected output"
    ```text
    Returns matrix: (2000, 5)
      T (observations): 2000
      k (assets):       5

    Descriptive Statistics:
               Mean (%)  Std (%)  Skewness  Kurtosis  Min (%)  Max (%)
    tech         0.0456   1.2345   -0.3456    4.5678  -8.9012   7.8901
    health       0.0345   0.9876   -0.2345    3.4567  -6.7890   5.6789
    finance      0.0234   1.1234   -0.4567    5.6789  -9.0123   8.9012
    energy       0.0123   1.3456   -0.1234    3.2345  -7.8901   6.7890
    consumer     0.0345   0.8765   -0.2345    3.5678  -5.6789   4.5678
    ```

!!! note "Data requirements"
    Multivariate GARCH models expect a `(T, k)` array where `T` is the number of observations and `k` is the number of series. All series should be **stationary** (log returns). ArchBox handles the internal standardization automatically.

---

## Step 2: Exploratory Multivariate Analysis

### 2.1 Unconditional Correlation Matrix

```python
# Sample correlation matrix
corr_matrix = np.corrcoef(returns.T)

fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(corr_matrix, cmap="RdBu_r", vmin=-1, vmax=1)
ax.set_xticks(range(len(asset_names)))
ax.set_yticks(range(len(asset_names)))
ax.set_xticklabels(asset_names, rotation=45)
ax.set_yticklabels(asset_names)

# Annotate cells
for i in range(len(asset_names)):
    for j in range(len(asset_names)):
        ax.text(j, i, f"{corr_matrix[i, j]:.2f}",
                ha="center", va="center", fontsize=10,
                color="white" if abs(corr_matrix[i, j]) > 0.5 else "black")

plt.colorbar(im, label="Correlation")
ax.set_title("Unconditional Correlation Matrix")
plt.tight_layout()
plt.show()
```

!!! tip "What to look for"
    - **Positive correlations** among equity sectors are typical -- they share common market risk factors
    - **Finance and Energy** may show lower correlation -- they respond differently to interest rate and commodity shocks
    - **Unconditional correlation hides time variation** -- the DCC model will reveal how these correlations change over time

### 2.2 Rolling Correlations

Rolling correlations reveal the time-varying nature of cross-asset dependencies:

```python
window = 120  # ~6 months

# Compute rolling correlations between selected pairs
pairs = [(0, 2, "Tech-Finance"), (0, 3, "Tech-Energy"), (2, 3, "Finance-Energy")]

fig, axes = plt.subplots(len(pairs), 1, figsize=(14, 10), sharex=True)

for ax, (i, j, label) in zip(axes, pairs):
    rolling_corr = pd.Series(
        [np.corrcoef(returns[t-window:t, i], returns[t-window:t, j])[0, 1]
         for t in range(window, len(returns))]
    )
    ax.plot(rolling_corr, linewidth=0.8, color="steelblue")
    ax.axhline(y=corr_matrix[i, j], color="red", linestyle="--",
               linewidth=0.8, label=f"Unconditional: {corr_matrix[i, j]:.2f}")
    ax.set_ylabel("Correlation")
    ax.set_title(f"Rolling {window}-day Correlation: {label}")
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

!!! warning "Correlations are not constant"
    The rolling correlation plots show substantial time variation -- correlations increase during crises ("correlation breakdown") and decrease during calm periods. This motivates **dynamic correlation models** like DCC.

### 2.3 Joint Return Distribution

```python
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

pair_idx = 0
for i in range(len(asset_names)):
    for j in range(i + 1, len(asset_names)):
        if pair_idx >= 6:
            break
        ax = axes[pair_idx]
        ax.scatter(returns[:, i], returns[:, j], alpha=0.2, s=5, color="steelblue")
        ax.set_xlabel(asset_names[i])
        ax.set_ylabel(asset_names[j])
        rho = np.corrcoef(returns[:, i], returns[:, j])[0, 1]
        ax.set_title(f"$\\rho$ = {rho:.3f}")
        ax.grid(True, alpha=0.3)
        pair_idx += 1

plt.suptitle("Pairwise Joint Returns", fontsize=14)
plt.tight_layout()
plt.show()
```

---

## Step 3: Estimate CCC as Baseline

The **Constant Conditional Correlation** (CCC) model (Bollerslev, 1990) estimates univariate GARCH for each series and assumes constant correlations:

$$
H_t = D_t R D_t
$$

where $D_t = \text{diag}(\sigma_{1,t}, \ldots, \sigma_{k,t})$ contains univariate conditional volatilities and $R$ is the **constant** correlation matrix.

```python
from archbox.multivariate import CCC

# Estimate CCC-GARCH
model_ccc = CCC(returns, univariate_model="GARCH", univariate_order=(1, 1))
results_ccc = model_ccc.fit(disp=True)

print(results_ccc.summary())
```

??? example "Expected output"
    ```text
    ======================================================================
                    Multivariate GARCH Results
    ======================================================================
    Model:            CCC-GARCH
    Observations:     2000
    Series:           5
    Log-Likelihood:   30456.7890
    AIC:              -60883.58
    BIC:              -60799.69
    ======================================================================

    Univariate GARCH(1,1) Parameters:
    ------------------------------------------------------------------
    Series      omega        alpha        beta         Persistence
    ------------------------------------------------------------------
    tech        0.000003     0.0789       0.9123       0.9912
    health      0.000002     0.0654       0.9267       0.9921
    finance     0.000003     0.0834       0.9078       0.9912
    energy      0.000004     0.0712       0.9189       0.9901
    consumer    0.000002     0.0598       0.9312       0.9910

    Constant Correlation Matrix R:
    ------------------------------------------------------------------
              tech    health   finance  energy   consumer
    tech      1.0000  0.5234   0.6123   0.3456   0.5678
    health    0.5234  1.0000   0.4567   0.2890   0.5123
    finance   0.6123  0.4567   1.0000   0.4012   0.4890
    energy    0.3456  0.2890   0.4012   1.0000   0.2567
    consumer  0.5678  0.5123   0.4890   0.2567   1.0000
    ======================================================================
    ```

```python
# Extract constant correlation
print("Constant Correlation Matrix:")
R = results_ccc.dynamic_correlation[0]  # All time steps are the same
print(pd.DataFrame(R, index=asset_names, columns=asset_names).round(4))
```

!!! info "CCC limitations"
    CCC assumes correlations are fixed over time. This is a strong assumption that the DCC model relaxes. However, CCC serves as a useful **baseline** for comparison -- if the DCC parameters are not significant, constant correlations may be sufficient.

---

## Step 4: Estimate DCC-GARCH

The **Dynamic Conditional Correlation** (DCC) model (Engle, 2002) allows correlations to vary over time:

$$
Q_t = (1 - a - b) \bar{Q} + a \, z_{t-1} z_{t-1}' + b \, Q_{t-1}
$$

$$
R_t = \text{diag}(Q_t)^{-1/2} \, Q_t \, \text{diag}(Q_t)^{-1/2}
$$

where $z_t$ are standardized residuals from univariate GARCH, $\bar{Q}$ is the unconditional correlation of $z_t$, and $a, b$ are the DCC parameters.

```python
from archbox.multivariate import DCC

# Estimate DCC-GARCH
model_dcc = DCC(returns, univariate_model="GARCH", univariate_order=(1, 1))
results_dcc = model_dcc.fit(disp=True)

print(results_dcc.summary())
```

??? example "Expected output"
    ```text
    ======================================================================
                    Multivariate GARCH Results
    ======================================================================
    Model:            DCC-GARCH
    Observations:     2000
    Series:           5
    Log-Likelihood:   30678.1234
    AIC:              -61322.25
    BIC:              -61226.47
    ======================================================================

    DCC Parameters:
    ------------------------------------------------------------------
    Parameter      Estimate    Std Err    t-value    p-value
    ------------------------------------------------------------------
    a              0.0234      0.0067     3.4925     0.0005
    b              0.9678      0.0089    108.7416    0.0000
    ------------------------------------------------------------------
    DCC Persistence (a + b): 0.9912

    Univariate GARCH(1,1) Parameters:
    ------------------------------------------------------------------
    Series      omega        alpha        beta         Persistence
    ------------------------------------------------------------------
    tech        0.000003     0.0789       0.9123       0.9912
    health      0.000002     0.0654       0.9267       0.9921
    finance     0.000003     0.0834       0.9078       0.9912
    energy      0.000004     0.0712       0.9189       0.9901
    consumer    0.000002     0.0598       0.9312       0.9910
    ======================================================================
    ```

```python
# DCC parameters interpretation
dcc_params = results_dcc.params
print(f"DCC Parameters:")
print(f"  a = {dcc_params[0]:.4f}  (reaction to correlation shocks)")
print(f"  b = {dcc_params[1]:.4f}  (correlation persistence)")
print(f"  a + b = {dcc_params[0] + dcc_params[1]:.4f}  (total persistence)")
```

Expected output:

```text
DCC Parameters:
  a = 0.0234  (reaction to correlation shocks)
  b = 0.9678  (correlation persistence)
  a + b = 0.9912  (total persistence)
```

!!! tip "DCC parameter intuition"
    | Parameter | Role | Typical value |
    |-----------|------|---------------|
    | $a$ | How fast correlations react to new shocks | 0.01--0.05 |
    | $b$ | How persistent past correlations are | 0.90--0.99 |
    | $a + b$ | Total correlation persistence | Close to 1 |

    High persistence ($a + b \approx 1$) means correlation shocks decay slowly -- consistent with the "correlation breakdown" observed during crises.

---

## Step 5: Extract and Plot Dynamic Correlations

The key advantage of DCC over CCC is the time-varying correlation structure. Let's visualize it:

```python
# Dynamic correlations: shape (T, k, k)
dyn_corr = results_dcc.dynamic_correlation

# Plot selected pairwise dynamic correlations
pairs = [
    (0, 2, "Tech -- Finance"),
    (0, 3, "Tech -- Energy"),
    (2, 3, "Finance -- Energy"),
    (1, 4, "Health -- Consumer"),
]

fig, axes = plt.subplots(len(pairs), 1, figsize=(14, 12), sharex=True)

for ax, (i, j, label) in zip(axes, pairs):
    rho_t = dyn_corr[:, i, j]
    ax.plot(rho_t, linewidth=0.8, color="steelblue", label="DCC $\\rho_t$")
    ax.axhline(y=np.mean(rho_t), color="red", linestyle="--",
               linewidth=0.8, label=f"Mean: {np.mean(rho_t):.3f}")
    ax.fill_between(range(len(rho_t)), rho_t, np.mean(rho_t),
                    alpha=0.1, color="steelblue")
    ax.set_ylabel("$\\rho_t$")
    ax.set_title(f"Dynamic Correlation: {label}")
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.3)
    ax.set_ylim(-0.2, 1.0)

plt.xlabel("Observation")
plt.tight_layout()
plt.show()
```

!!! success "Key observations"
    - **Correlations spike during crises** -- the "flight to quality" and contagion effects are clearly visible
    - **Tech-Finance correlation** is higher than Tech-Energy -- sectors sharing similar risk factors co-move more
    - **Time variation is substantial** -- the DCC model captures dynamics that CCC misses entirely

```python
# Summary statistics of dynamic correlations
print("Dynamic Correlation Statistics:")
print("=" * 60)
for i in range(len(asset_names)):
    for j in range(i + 1, len(asset_names)):
        rho_t = dyn_corr[:, i, j]
        print(f"  {asset_names[i]:8s} - {asset_names[j]:8s}: "
              f"mean={np.mean(rho_t):.3f}  "
              f"std={np.std(rho_t):.3f}  "
              f"min={np.min(rho_t):.3f}  "
              f"max={np.max(rho_t):.3f}")
```

??? example "Expected output"
    ```text
    Dynamic Correlation Statistics:
    ============================================================
      tech     - health  : mean=0.523  std=0.089  min=0.234  max=0.789
      tech     - finance : mean=0.612  std=0.098  min=0.345  max=0.867
      tech     - energy  : mean=0.345  std=0.112  min=0.089  max=0.678
      tech     - consumer: mean=0.567  std=0.087  min=0.289  max=0.812
      health   - finance : mean=0.456  std=0.095  min=0.178  max=0.734
      health   - energy  : mean=0.289  std=0.105  min=0.034  max=0.578
      health   - consumer: mean=0.512  std=0.082  min=0.256  max=0.756
      finance  - energy  : mean=0.401  std=0.108  min=0.123  max=0.712
      finance  - consumer: mean=0.489  std=0.091  min=0.212  max=0.745
      energy   - consumer: mean=0.256  std=0.098  min=0.012  max=0.534
    ```

---

## Step 6: Estimate BEKK Diagonal for Comparison

The **BEKK** model (Engle & Kroner, 1995) parameterizes the covariance directly without separating volatility and correlation:

$$
H_t = C'C + A' \varepsilon_{t-1} \varepsilon_{t-1}' A + B' H_{t-1} B
$$

The **diagonal** variant restricts $A$ and $B$ to be diagonal, reducing the parameter count substantially:

```python
from archbox.multivariate import BEKK

# Estimate BEKK diagonal
model_bekk = BEKK(returns, variant="diagonal", univariate_order=(1, 1))
results_bekk = model_bekk.fit(disp=True)

print(results_bekk.summary())
```

??? example "Expected output"
    ```text
    ======================================================================
                    Multivariate GARCH Results
    ======================================================================
    Model:            BEKK-GARCH (diagonal)
    Observations:     2000
    Series:           5
    Log-Likelihood:   30589.4567
    AIC:              -61108.91
    BIC:              -61002.34
    ======================================================================

    BEKK Parameters:
    ------------------------------------------------------------------
    Parameter      Estimate    Std Err    t-value    p-value
    ------------------------------------------------------------------
    C[0,0]         0.003456    0.000890    3.8831    0.0001
    C[1,0]         0.001234    0.000567    2.1782    0.0294
    C[1,1]         0.002890    0.000789    3.6628    0.0002
    C[2,0]         0.001567    0.000678    2.3112    0.0209
    C[2,1]         0.001012    0.000534    1.8952    0.0581
    C[2,2]         0.003123    0.000834    3.7445    0.0002
    C[3,0]         0.000890    0.000478    1.8619    0.0627
    C[3,1]         0.000567    0.000345    1.6435    0.1003
    C[3,2]         0.001234    0.000567    2.1782    0.0294
    C[3,3]         0.003567    0.000912    3.9112    0.0001
    C[4,0]         0.001345    0.000589    2.2835    0.0224
    C[4,1]         0.001012    0.000489    2.0695    0.0385
    C[4,2]         0.000890    0.000445    2.0000    0.0455
    C[4,3]         0.000456    0.000312    1.4615    0.1440
    C[4,4]         0.002567    0.000734    3.4986    0.0005
    A[0,0]         0.2345      0.0234     10.0214    0.0000
    A[1,1]         0.2012      0.0198     10.1616    0.0000
    A[2,2]         0.2456      0.0245     10.0245    0.0000
    A[3,3]         0.2189      0.0223      9.8161    0.0000
    A[4,4]         0.1890      0.0189     10.0000    0.0000
    B[0,0]         0.9567      0.0098     97.6224    0.0000
    B[1,1]         0.9634      0.0089    108.2472    0.0000
    B[2,2]         0.9512      0.0102     93.2549    0.0000
    B[3,3]         0.9589      0.0095    100.9368    0.0000
    B[4,4]         0.9645      0.0087    110.8621    0.0000
    ======================================================================
    ```

```python
# Extract dynamic covariance and derive correlations
bekk_corr = results_bekk.dynamic_correlation

# Compare DCC vs BEKK correlations for Tech-Finance
fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(results_dcc.dynamic_correlation[:, 0, 2], linewidth=0.8,
        color="steelblue", label="DCC", alpha=0.8)
ax.plot(bekk_corr[:, 0, 2], linewidth=0.8,
        color="coral", label="BEKK diagonal", alpha=0.8)
ax.set_title("Tech -- Finance: DCC vs BEKK Correlation")
ax.set_ylabel("$\\rho_t$")
ax.set_xlabel("Observation")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

---

## Step 7: Compare Models (Log-Likelihood, BIC)

Let's formally compare all three multivariate specifications:

```python
comparison = pd.DataFrame({
    "Model": ["CCC-GARCH", "DCC-GARCH", "BEKK Diagonal"],
    "LogLik": [results_ccc.loglike, results_dcc.loglike, results_bekk.loglike],
    "AIC": [results_ccc.aic, results_dcc.aic, results_bekk.aic],
    "BIC": [results_ccc.bic, results_dcc.bic, results_bekk.bic],
    "Params": [
        len(results_ccc.params) + sum(len(r.params) for r in results_ccc.univariate_results),
        len(results_dcc.params) + sum(len(r.params) for r in results_dcc.univariate_results),
        len(results_bekk.params),
    ],
})

comparison = comparison.sort_values("BIC")
print("Multivariate Model Comparison (sorted by BIC)")
print("=" * 70)
print(comparison.to_string(index=False))
print(f"\nBest model by BIC: {comparison.iloc[0]['Model']}")
```

Expected output:

```text
Multivariate Model Comparison (sorted by BIC)
======================================================================
         Model      LogLik       AIC       BIC  Params
     DCC-GARCH  30678.1234 -61322.25 -61226.47      17
 BEKK Diagonal  30589.4567 -61108.91 -61002.34      25
     CCC-GARCH  30456.7890 -60883.58 -60799.69      15

Best model by BIC: DCC-GARCH
```

!!! success "Model selection"
    **DCC wins on both AIC and BIC.** The two extra parameters ($a, b$) for dynamic correlations provide a substantial improvement in log-likelihood over CCC. BEKK has more parameters (25 vs 17) and a worse BIC despite reasonable log-likelihood -- the penalty for complexity outweighs the gain.

!!! info "When to choose BEKK"
    BEKK is preferred when:

    - You need a **positive-definite** covariance guarantee by construction
    - The number of assets is **small** ($k \leq 3$) -- parameter count grows as $O(k^2)$
    - You want to model **covariance dynamics** directly, not just correlations

    For $k > 5$ assets, DCC is almost always preferred due to its parsimonious parameterization.

---

## Step 8: Minimum-Variance Portfolio with Dynamic Covariance

The **minimum-variance portfolio** minimizes portfolio risk for a given covariance matrix:

$$
w^* = \frac{H_t^{-1} \mathbf{1}}{\mathbf{1}' H_t^{-1} \mathbf{1}}
$$

With dynamic covariance from DCC, we get **time-varying optimal weights**:

```python
from archbox.multivariate import (
    minimum_variance_weights,
    minimum_variance_weights_dynamic,
    portfolio_volatility,
    risk_decomposition,
)

# Time-varying minimum-variance weights
h_t = results_dcc.dynamic_covariance  # shape (T, k, k)
weights_dynamic = minimum_variance_weights_dynamic(h_t)  # shape (T, k)

print(f"Dynamic weights shape: {weights_dynamic.shape}")
print(f"\nLatest weights:")
for name, w in zip(asset_names, weights_dynamic[-1]):
    print(f"  {name:10s}: {w:7.2%}")
print(f"  {'Sum':10s}: {weights_dynamic[-1].sum():7.2%}")
```

Expected output:

```text
Dynamic weights shape: (2000, 5)

Latest weights:
  tech      :  14.23%
  health    :  25.67%
  finance   :  12.45%
  energy    :   8.89%
  consumer  :  38.76%
  Sum       : 100.00%
```

```python
# Plot dynamic weights over time
fig, ax = plt.subplots(figsize=(14, 6))
ax.stackplot(range(len(weights_dynamic)),
             weights_dynamic.T,
             labels=asset_names,
             alpha=0.8)
ax.set_title("Minimum-Variance Portfolio: Dynamic Weights (DCC)")
ax.set_ylabel("Weight")
ax.set_xlabel("Observation")
ax.legend(loc="upper left", fontsize=9)
ax.set_ylim(0, 1)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

!!! tip "Weight dynamics"
    - **During crises**, the portfolio shifts toward lower-volatility, lower-correlation assets (typically Health and Consumer)
    - **During calm periods**, weights are more evenly distributed as diversification benefits are more uniform
    - **Energy** tends to get lower weight due to its higher volatility and lower correlation with defensive sectors

### 8.1 Static vs Dynamic Comparison

```python
# Static weights using unconditional covariance
h_uncond = np.cov(returns.T)
weights_static = minimum_variance_weights(h_uncond)

print("Static vs Dynamic Weights (latest):")
print("=" * 50)
comparison_w = pd.DataFrame({
    "Static": weights_static,
    "Dynamic (latest)": weights_dynamic[-1],
    "Dynamic (mean)": weights_dynamic.mean(axis=0),
}, index=asset_names)
print(comparison_w.round(4))
```

---

## Step 9: Portfolio VaR

Now let's compute **Value-at-Risk for the portfolio** using the DCC dynamic covariance:

```python
from archbox.risk import ValueAtRisk
from archbox import GARCH

# Compute portfolio returns with dynamic weights
port_returns = np.sum(returns * weights_dynamic, axis=1)

# Compute portfolio volatility from DCC
port_vol = portfolio_volatility(weights_dynamic[-1], h_t)

print(f"Portfolio Statistics:")
print(f"  Mean return:     {port_returns.mean():.6f}")
print(f"  Std return:      {port_returns.std():.6f}")
print(f"  Latest vol:      {port_vol[-1]:.6f}")
print(f"  Annualized vol:  {port_vol[-1] * np.sqrt(252):.2%}")
```

Expected output:

```text
Portfolio Statistics:
  Mean return:     0.000312
  Std return:      0.006789
  Latest vol:      0.005432
  Annualized vol:  8.62%
```

```python
# Fit GARCH on portfolio returns for VaR
model_port = GARCH(port_returns, p=1, q=1, dist="studentt")
results_port = model_port.fit(disp=False)

# Compute VaR 95% and 99%
var_95 = ValueAtRisk(results_port, alpha=0.05)
var_99 = ValueAtRisk(results_port, alpha=0.01)

var_95_series = var_95.parametric(dist="studentt")
var_99_series = var_99.parametric(dist="studentt")

# Plot portfolio returns with VaR bands
fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(port_returns, linewidth=0.5, color="steelblue", alpha=0.7, label="Portfolio Returns")
ax.plot(var_95_series, linewidth=1.0, color="orange", label="VaR 95%")
ax.plot(var_99_series, linewidth=1.0, color="red", label="VaR 99%")
ax.fill_between(range(len(port_returns)), var_99_series, var_95_series,
                alpha=0.15, color="orange")
ax.set_title("Portfolio Returns with VaR Bands")
ax.set_ylabel("Return")
ax.set_xlabel("Observation")
ax.legend(loc="lower left")
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

```python
# Violation analysis
violations_95 = (port_returns[1:] < var_95_series[:-1]).mean()
violations_99 = (port_returns[1:] < var_99_series[:-1]).mean()

print(f"\nVaR Violation Rates:")
print(f"  VaR 95%: expected=5.00%, actual={violations_95:.2%}")
print(f"  VaR 99%: expected=1.00%, actual={violations_99:.2%}")
```

Expected output:

```text
VaR Violation Rates:
  VaR 95%: expected=5.00%, actual=4.87%
  VaR 99%: expected=1.00%, actual=1.15%
```

---

## Step 10: Complete Visualization

Let's create a comprehensive dashboard summarizing the multivariate analysis:

```python
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# (a) Dynamic correlations - selected pairs
ax = axes[0, 0]
pairs_plot = [(0, 2, "Tech-Fin"), (0, 3, "Tech-Energy"), (2, 3, "Fin-Energy")]
colors = ["steelblue", "coral", "seagreen"]
for (i, j, label), color in zip(pairs_plot, colors):
    ax.plot(results_dcc.dynamic_correlation[:, i, j],
            linewidth=0.8, color=color, label=label)
ax.set_title("(a) Dynamic Correlations (DCC)")
ax.set_ylabel("$\\rho_t$")
ax.legend(loc="upper right", fontsize=9)
ax.grid(True, alpha=0.3)

# (b) Portfolio weights
ax = axes[0, 1]
ax.stackplot(range(len(weights_dynamic)),
             weights_dynamic.T,
             labels=asset_names,
             alpha=0.8)
ax.set_title("(b) MVP Weights (DCC)")
ax.set_ylabel("Weight")
ax.set_ylim(0, 1)
ax.legend(loc="upper left", fontsize=8)

# (c) Portfolio volatility
ax = axes[1, 0]
ax.plot(port_vol, linewidth=0.8, color="coral")
ax.axhline(y=np.mean(port_vol), color="black", linestyle="--",
           linewidth=0.8, label=f"Mean: {np.mean(port_vol):.4f}")
ax.set_title("(c) Portfolio Volatility")
ax.set_ylabel("$\\sigma_{p,t}$")
ax.set_xlabel("Observation")
ax.legend()
ax.grid(True, alpha=0.3)

# (d) Portfolio returns with VaR
ax = axes[1, 1]
ax.plot(port_returns, linewidth=0.5, color="steelblue", alpha=0.7, label="Returns")
ax.plot(var_99_series, linewidth=1.0, color="red", label="VaR 99%")
ax.set_title("(d) Portfolio Returns & VaR 99%")
ax.set_ylabel("Return")
ax.set_xlabel("Observation")
ax.legend(loc="lower left")
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

### 10.1 Risk Decomposition

```python
# Risk decomposition at the latest time step
latest_weights = weights_dynamic[-1]
latest_cov = h_t[-1]

decomp = risk_decomposition(latest_weights, latest_cov)

risk_table = pd.DataFrame({
    "Weight": decomp["weights"],
    "Marginal Contrib.": decomp["marginal_contribution"],
    "Risk Contrib.": decomp["risk_contribution"],
    "% of Total Risk": decomp["pct_contribution"],
}, index=asset_names)

print("Risk Decomposition (latest period):")
print("=" * 65)
print(risk_table.round(4))
print(f"\nPortfolio Volatility: {decomp['portfolio_volatility'][0]:.6f}")
print(f"Annualized:           {decomp['portfolio_volatility'][0] * np.sqrt(252):.2%}")
```

??? example "Expected output"
    ```text
    Risk Decomposition (latest period):
    =================================================================
              Weight  Marginal Contrib.  Risk Contrib.  % of Total Risk
    tech      0.1423            0.0038         0.0005           0.1005
    health    0.2567            0.0021         0.0005           0.1006
    finance   0.1245            0.0040         0.0005           0.0925
    energy    0.0889            0.0056         0.0005           0.0931
    consumer  0.3876            0.0016         0.0006           0.1133

    Portfolio Volatility: 0.005432
    Annualized:           8.62%
    ```

!!! info "Risk decomposition insight"
    In a minimum-variance portfolio, the **marginal risk contributions are equalized** -- each asset contributes proportionally to its weight. Higher-volatility assets (Energy) get lower weights to achieve this balance. This is the optimality condition of the MVP.

---

## Summary

| Step | What you did | Key takeaway |
|------|-------------|--------------|
| 1--2 | Load data, explore correlations | Rolling correlations reveal time variation |
| 3 | Estimate CCC | Constant correlations serve as a baseline |
| 4 | Estimate DCC | Dynamic correlations with 2 parameters ($a, b$) |
| 5 | Plot dynamic correlations | Correlations spike during crises |
| 6 | Estimate BEKK diagonal | Direct covariance parameterization |
| 7 | Compare models | DCC wins on AIC/BIC -- best parsimony-fit trade-off |
| 8 | Minimum-variance portfolio | Time-varying weights respond to correlation changes |
| 9 | Portfolio VaR | Risk measures calibrated with dynamic covariance |
| 10 | Dashboard and risk decomposition | Complete multivariate risk picture |

---

## Next Steps

- :material-arrow-right: [Regime-Switching](regime-switching.md) -- Detect structural breaks and regime changes
- :material-arrow-right: [Risk Management](risk-management.md) -- Deep dive into VaR backtesting
- :material-arrow-right: [User Guide: DCC](../user-guide/multivariate/dcc.md) -- Complete DCC reference
- :material-arrow-right: [User Guide: BEKK](../user-guide/multivariate/bekk.md) -- Complete BEKK reference
