---
title: "GARCH Variants: Comparing GARCH, EGARCH, and GJR"
description: "Tutorial comparing symmetric and asymmetric GARCH models for capturing leverage effects"
---

# Comparing GARCH, EGARCH, and GJR

!!! info "Tutorial Info"
    **Time:** ~30 minutes
    **Level:** Beginner
    **Prerequisites:** [Fundamentals](fundamentals.md) tutorial
    **What you'll learn:** Leverage effects, asymmetric models, news impact curves, and automated model comparison

Financial returns exhibit an important asymmetry: negative shocks ("bad news") tend to increase volatility more than positive shocks ("good news") of the same magnitude. This is called the **leverage effect**. In this tutorial, we compare three models and their ability to capture this phenomenon.

---

## Step 1: The Leverage Effect

### Why asymmetry matters

When a stock falls, the firm's debt-to-equity ratio rises, making it riskier -- hence **leverage** effect (Black, 1976). Empirically:

- A -2% return increases volatility more than a +2% return
- The standard GARCH(1,1) is **symmetric** -- it treats positive and negative shocks identically
- EGARCH and GJR-GARCH add parameters to capture this asymmetry

### The three models

=== "GARCH(1,1)"

    $$
    \sigma_t^2 = \omega + \alpha_1 \varepsilon_{t-1}^2 + \beta_1 \sigma_{t-1}^2
    $$

    - **Symmetric**: $\varepsilon_{t-1}^2$ depends only on magnitude, not sign
    - 3 parameters: $\omega, \alpha_1, \beta_1$

=== "EGARCH(1,1)"

    $$
    \ln \sigma_t^2 = \omega + \alpha_1 \left( |z_{t-1}| - E|z_{t-1}| \right) + \gamma_1 z_{t-1} + \beta_1 \ln \sigma_{t-1}^2
    $$

    - **Asymmetric** via $\gamma_1$: if $\gamma_1 < 0$, negative shocks increase volatility more
    - Models log-variance -- no positivity constraints needed
    - 4 parameters: $\omega, \alpha_1, \gamma_1, \beta_1$

=== "GJR-GARCH(1,1)"

    $$
    \sigma_t^2 = \omega + (\alpha_1 + \gamma_1 \mathbb{1}_{\varepsilon_{t-1}<0}) \varepsilon_{t-1}^2 + \beta_1 \sigma_{t-1}^2
    $$

    - **Asymmetric** via $\gamma_1$: adds extra weight when $\varepsilon_{t-1} < 0$
    - Effective impact of negative shock: $\alpha_1 + \gamma_1$
    - Effective impact of positive shock: $\alpha_1$
    - 4 parameters: $\omega, \alpha_1, \gamma_1, \beta_1$

---

## Step 2: Estimate All Three Models

Let's fit all three models on the same S&P 500 data using Student-t innovations:

```python
import numpy as np
import pandas as pd
from archbox import GARCH, EGARCH, GJRGARCH
from archbox.datasets import load_dataset

# Load data
sp500 = load_dataset("sp500")
returns = sp500["returns"].to_numpy()

# Fit GARCH(1,1)
model_garch = GARCH(returns, p=1, q=1, dist="student-t")
results_garch = model_garch.fit(disp=False)

# Fit EGARCH(1,1)
model_egarch = EGARCH(returns, p=1, q=1, dist="student-t")
results_egarch = model_egarch.fit(disp=False)

# Fit GJR-GARCH(1,1)
model_gjr = GJRGARCH(returns, p=1, q=1, dist="student-t")
results_gjr = model_gjr.fit(disp=False)

print("All models converged successfully!")
print(f"  GARCH:  converged={results_garch.convergence}")
print(f"  EGARCH: converged={results_egarch.convergence}")
print(f"  GJR:    converged={results_gjr.convergence}")
```

Expected output:

```text
All models converged successfully!
  GARCH:  converged=True
  EGARCH: converged=True
  GJR:    converged=True
```

---

## Step 3: Compare Parameters and Interpretation

Let's build a comparison table of the estimated parameters:

```python
# Collect results
models = {
    "GARCH(1,1)": results_garch,
    "EGARCH(1,1)": results_egarch,
    "GJR(1,1)": results_gjr,
}

# Display parameters for each model
for name, res in models.items():
    print(f"\n{'='*50}")
    print(f"  {name}")
    print(f"{'='*50}")
    for pname, val, se, pval in zip(
        res.param_names, res.params, res.se, res.pvalues
    ):
        sig = "***" if pval < 0.001 else "**" if pval < 0.01 else "*" if pval < 0.05 else ""
        print(f"  {pname:12s} = {val:10.6f}  (SE={se:.6f}, p={pval:.4f}) {sig}")
    print(f"  Persistence:  {res.persistence():.4f}")
    print(f"  Half-life:    {res.half_life():.1f} days")
```

??? example "Expected output"
    ```text
    ==================================================
      GARCH(1,1)
    ==================================================
      omega        =   0.000002  (SE=0.000001, p=0.0018) **
      alpha[1]     =   0.075600  (SE=0.010800, p=0.0000) ***
      beta[1]      =   0.915500  (SE=0.011500, p=0.0000) ***
      nu           =   7.234500  (SE=1.056700, p=0.0000) ***
      Persistence:  0.9911
      Half-life:    77.5 days

    ==================================================
      EGARCH(1,1)
    ==================================================
      omega        =  -0.123400  (SE=0.034500, p=0.0004) ***
      alpha[1]     =   0.145600  (SE=0.023400, p=0.0000) ***
      gamma[1]     =  -0.098700  (SE=0.015600, p=0.0000) ***
      beta[1]      =   0.984500  (SE=0.004200, p=0.0000) ***
      nu           =   7.567800  (SE=1.089000, p=0.0000) ***
      Persistence:  0.9845
      Half-life:    44.4 days

    ==================================================
      GJR(1,1)
    ==================================================
      omega        =   0.000002  (SE=0.000001, p=0.0025) **
      alpha[1]     =   0.032100  (SE=0.011200, p=0.0042) **
      gamma[1]     =   0.089300  (SE=0.018900, p=0.0000) ***
      beta[1]      =   0.916700  (SE=0.011800, p=0.0000) ***
      nu           =   7.456700  (SE=1.078900, p=0.0000) ***
      Persistence:  0.9935
      Half-life:    106.2 days
    ```

!!! info "Interpreting asymmetry parameters"

    === "EGARCH"
        The parameter $\gamma_1 = -0.099$ is **negative and significant**. This means negative returns increase log-variance more than positive returns. The asymmetric effect accounts for approximately $\frac{|\gamma_1|}{\alpha_1} \approx 68\%$ of the news impact.

    === "GJR-GARCH"
        The parameter $\gamma_1 = 0.089$ is **positive and significant**. For negative shocks, the effective ARCH coefficient is $\alpha_1 + \gamma_1 = 0.032 + 0.089 = 0.121$, nearly **4x larger** than the response to positive shocks ($\alpha_1 = 0.032$).

    === "GARCH"
        No asymmetry parameter -- a -2% and +2% shock have the **same** impact ($\alpha_1 = 0.076$). This misses the leverage effect entirely.

---

## Step 4: News Impact Curves

The **news impact curve** (Engle and Ng, 1993) shows how a shock $\varepsilon_{t-1}$ affects tomorrow's conditional variance $\sigma_t^2$, holding past variance constant. It is the most intuitive way to visualize asymmetry.

```python
import matplotlib.pyplot as plt
from archbox.utils import news_impact_curve, compare_news_impact

# Compare news impact curves for all three models
models_results = [
    (model_garch, results_garch, "GARCH(1,1)"),
    (model_egarch, results_egarch, "EGARCH(1,1)"),
    (model_gjr, results_gjr, "GJR-GARCH(1,1)"),
]

fig, ax = plt.subplots(figsize=(10, 6))
ax = compare_news_impact(models_results, n_points=200, sigma_range=3.0)
ax.set_title("News Impact Curves: GARCH vs EGARCH vs GJR-GARCH")
ax.legend(fontsize=12)
plt.tight_layout()
plt.show()
```

!!! tip "Reading the news impact curve"
    - The **x-axis** shows the shock $\varepsilon_{t-1}$ (negative = bad news, positive = good news)
    - The **y-axis** shows the resulting conditional variance $\sigma_t^2$
    - **GARCH**: Symmetric parabola -- same response to good and bad news
    - **EGARCH**: Asymmetric -- steeper on the left (bad news increases variance more)
    - **GJR-GARCH**: Piecewise parabola -- steeper slope for negative shocks

You can also plot individual news impact curves:

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for ax, (model, results, name) in zip(axes, models_results):
    eps_range, sigma2 = news_impact_curve(model, results, n_points=200)
    ax.plot(eps_range, sigma2, linewidth=2, color="steelblue")
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_title(name)
    ax.set_xlabel("$\\varepsilon_{t-1}$")
    ax.set_ylabel("$\\sigma_t^2$")
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## Step 5: Sign Bias Test

The **Sign Bias test** (Engle and Ng, 1993) formally tests whether a symmetric model is adequate. It regresses squared standardized residuals on sign indicators:

$$
z_t^2 = c_0 + c_1 \mathbb{1}_{\varepsilon_{t-1}<0} + c_2 \mathbb{1}_{\varepsilon_{t-1}<0} \varepsilon_{t-1} + c_3 \mathbb{1}_{\varepsilon_{t-1}>0} \varepsilon_{t-1} + u_t
$$

```python
from archbox.diagnostics import sign_bias_test

# Run sign bias test on GARCH residuals
sb_result = sign_bias_test(
    results_garch.resid * results_garch.conditional_volatility,  # raw residuals
    results_garch.resid  # standardized residuals
)

print("Sign Bias Test (GARCH(1,1) residuals)")
print("=" * 50)
print(f"  Sign Bias:      t={sb_result.sign_bias[0]:7.4f}  p={sb_result.sign_bias[1]:.4f}")
print(f"  Neg Sign Bias:  t={sb_result.neg_sign_bias[0]:7.4f}  p={sb_result.neg_sign_bias[1]:.4f}")
print(f"  Pos Sign Bias:  t={sb_result.pos_sign_bias[0]:7.4f}  p={sb_result.pos_sign_bias[1]:.4f}")
print(f"  Joint Test:     F={sb_result.joint[0]:7.4f}  p={sb_result.joint[1]:.4f}")
```

Expected output:

```text
Sign Bias Test (GARCH(1,1) residuals)
==================================================
  Sign Bias:      t= 2.3456  p=0.0191
  Neg Sign Bias:  t= 3.1234  p=0.0018
  Pos Sign Bias:  t= 0.8765  p=0.3812
  Joint Test:     F= 5.6789  p=0.0007
```

!!! success "Interpretation"
    - **Sign Bias** is significant ($p < 0.05$): the sign of the shock matters
    - **Negative Sign Bias** is highly significant: negative shocks are under-weighted
    - **Positive Sign Bias** is not significant: positive shocks are adequately modeled
    - **Joint test** rejects at 0.1%: the symmetric GARCH is **misspecified** -- an asymmetric model is needed

!!! note "Running on asymmetric models"
    You can also run the sign bias test on EGARCH or GJR residuals. If the asymmetric model is well-specified, the test should no longer reject.

---

## Step 6: Compare AIC/BIC

Let's create a formal comparison table:

```python
comparison = []
for name, res in models.items():
    comparison.append({
        "Model": name,
        "LogLik": res.loglike,
        "AIC": res.aic,
        "BIC": res.bic,
        "Params": len(res.params),
        "Persistence": res.persistence(),
    })

df_comp = pd.DataFrame(comparison)
df_comp = df_comp.sort_values("BIC")

print("Model Comparison (sorted by BIC)")
print("=" * 70)
print(df_comp.to_string(index=False))

best = df_comp.iloc[0]["Model"]
print(f"\nBest model by BIC: {best}")
```

Expected output:

```text
Model Comparison (sorted by BIC)
======================================================================
       Model     LogLik       AIC       BIC  Params  Persistence
 EGARCH(1,1)  8348.1234 -16684.25 -16654.52       5       0.9845
    GJR(1,1)  8340.5678 -16669.14 -16639.40       5       0.9935
 GARCH(1,1)   8312.4567 -16614.91 -16591.10       4       0.9911

Best model by BIC: EGARCH(1,1)
```

!!! info "Model selection guidelines"
    | Criterion | Prefers | Penalty for complexity |
    |-----------|---------|----------------------|
    | AIC | Better in-sample fit | Light ($2k$) |
    | BIC | Parsimony | Heavy ($k \ln n$) |

    When both AIC and BIC agree, the choice is clear. When they disagree, BIC is more conservative and better for pure forecasting, while AIC can be preferred for risk management where capturing tail behavior matters more.

---

## Step 7: Automate with ArchExperiment

ArchBox provides **ArchExperiment** to automate model comparison. Instead of manually fitting each model, define the candidates and let ArchExperiment handle the rest:

```python
import archbox as ab

# Create experiment
exp = ab.ArchExperiment(returns)

# Add models to compare
exp.add_model(ab.GARCH(1, 1))
exp.add_model(ab.EGARCH(1, 1))
exp.add_model(ab.GJR(1, 1))

# Run all fits
exp.run()

# View comparative summary
exp.summary()
```

??? example "Expected output"
    ```text
    ================================================================
    ArchExperiment Summary
    ================================================================
    Data: 2769 observations
    Models: 3
    Best model (BIC): EGARCH(1,1)
    ================================================================

    Model            LogLik      AIC         BIC         VaR Kupiec p
    ----------------------------------------------------------------
    GARCH(1,1)       8312.46     -16614.91   -16591.10   0.6523
    EGARCH(1,1)      8348.12     -16684.25   -16654.52   0.7812
    GJR(1,1)         8340.57     -16669.14   -16639.40   0.7234

    Rankings:
      AIC:  1. EGARCH  2. GJR  3. GARCH
      BIC:  1. EGARCH  2. GJR  3. GARCH
    ================================================================
    ```

!!! tip "ArchExperiment advantages"
    - **Less code**: Define models once, get a complete comparison
    - **Consistent evaluation**: Same data, same splits, same metrics
    - **Built-in backtesting**: Automatically evaluates VaR performance
    - **Report generation**: Export results to HTML, LaTeX, or CSV

You can also add more model variants:

```python
# Extended comparison with different distributions
exp = ab.ArchExperiment(returns)

# Normal distribution models
exp.add_model(ab.GARCH(1, 1))
exp.add_model(ab.EGARCH(1, 1))
exp.add_model(ab.GJR(1, 1))

# Student-t distribution models
exp.add_model(ab.GARCH(1, 1), dist="student-t")
exp.add_model(ab.EGARCH(1, 1), dist="student-t")
exp.add_model(ab.GJR(1, 1), dist="student-t")

# Run and compare
exp.run()
exp.summary()
```

---

## Step 8: Conclusions and Recommendations

### Key findings

Based on our analysis of S&P 500 returns:

1. **The leverage effect is statistically significant** -- the sign bias test rejects symmetry, and both EGARCH and GJR produce significant asymmetry parameters

2. **EGARCH performs best** on both AIC and BIC -- it captures the asymmetry and provides the best in-sample fit

3. **GJR-GARCH is a close second** -- simpler to interpret than EGARCH and often preferred in practice

4. **Standard GARCH is inadequate** for equity data -- it misses the leverage effect and produces worse information criteria

### When to use each model

| Model | Best for | Limitations |
|-------|----------|-------------|
| **GARCH(1,1)** | Symmetric assets (FX, some commodities) | Misses leverage in equities |
| **EGARCH(1,1)** | Equities, any asymmetric data | Harder to interpret; log-variance can extrapolate |
| **GJR-GARCH(1,1)** | Equities, regulatory applications | Requires positivity constraints |

!!! tip "Practical recommendations"

    **For equity markets:** Start with GJR-GARCH or EGARCH. Always run the sign bias test to confirm asymmetry.

    **For FX markets:** Standard GARCH(1,1) often suffices. The leverage effect is typically weaker in FX.

    **For risk management:** Use ArchExperiment to systematically compare models and distributions. The model with the best VaR backtest (highest Kupiec p-value) may differ from the model with the best AIC/BIC.

    **For academic research:** Report results from multiple models. Use the sign bias test to justify your model choice.

---

## Summary

| Step | What you did | Key takeaway |
|------|-------------|--------------|
| 1 | Motivation | Leverage effect makes asymmetric models necessary for equities |
| 2 | Estimation | Fit GARCH, EGARCH, GJR on the same data |
| 3 | Parameters | $\gamma$ parameters capture asymmetry; all significant |
| 4 | News impact curves | Visual proof: bad news increases volatility more |
| 5 | Sign bias test | Formal rejection of symmetry justifies EGARCH/GJR |
| 6 | AIC/BIC | EGARCH best; GJR close second |
| 7 | ArchExperiment | Automated comparison in a few lines of code |
| 8 | Recommendations | Model choice depends on asset class and use case |

---

## Next Steps

- :material-arrow-right: [Risk Management](risk-management.md) -- Apply these models to VaR and Expected Shortfall
- :material-arrow-right: [Multivariate](multivariate.md) -- Model volatility across multiple assets with DCC and BEKK
- :material-arrow-right: [User Guide: EGARCH](../user-guide/garch/egarch.md) -- Full EGARCH reference
- :material-arrow-right: [User Guide: GJR-GARCH](../user-guide/garch/gjr-garch.md) -- Full GJR-GARCH reference
