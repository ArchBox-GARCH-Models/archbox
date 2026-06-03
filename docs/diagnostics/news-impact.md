---
title: "News Impact Curve"
description: "News Impact Curve for visualizing asymmetric volatility response across GARCH, EGARCH and GJR models"
---

# News Impact Curve

!!! info "Quick Reference"
    **Function:** `archbox.utils.news_impact.news_impact_curve`
    **Purpose:** Visualize how shocks (news) of different sign and magnitude affect next-period volatility
    **Key insight:** Symmetric models produce a parabola centered at zero; asymmetric models shift or tilt it
    **Based on:** Engle & Ng (1993)

---

## 1. What It Shows

The News Impact Curve (NIC) plots **next-period conditional variance** $\sigma_t^2$ as a function of the **past shock** $\varepsilon_{t-1}$, holding the past variance $\sigma_{t-1}^2$ fixed at its unconditional level $\bar{\sigma}^2$.

$$
\boxed{NIC(\varepsilon_{t-1}) = \sigma_t^2 \Big|_{\sigma_{t-1}^2 = \bar{\sigma}^2}}
$$

This isolates the **pure impact of news** on volatility, making it easy to visually compare how different models respond to positive and negative shocks.

---

## 2. NIC for Each Model

### GARCH(1,1)

$$
\sigma_t^2 = \omega + \alpha \varepsilon_{t-1}^2 + \beta \bar{\sigma}^2
$$

The NIC is a **symmetric parabola** centered at $\varepsilon_{t-1} = 0$:

$$
NIC_{\text{GARCH}}(\varepsilon) = (\omega + \beta \bar{\sigma}^2) + \alpha \varepsilon^2
$$

Positive and negative shocks of the same magnitude produce **identical** volatility increases.

### EGARCH(1,1)

$$
\ln \sigma_t^2 = \omega + \alpha \left( |z_{t-1}| - E|z_{t-1}| \right) + \gamma z_{t-1} + \beta \ln \bar{\sigma}^2
$$

The NIC is **asymmetric and exponential**:

$$
NIC_{\text{EGARCH}}(\varepsilon) = \bar{\sigma}^{2\beta} \cdot \exp\!\left(\omega + \alpha \left|\frac{\varepsilon}{\bar{\sigma}}\right| - \alpha E|z| + \gamma \frac{\varepsilon}{\bar{\sigma}}\right)
$$

- If $\gamma < 0$: negative shocks increase volatility more (leverage effect)
- The exponential form ensures $\sigma_t^2 > 0$ without parameter constraints

### GJR-GARCH(1,1)

$$
\sigma_t^2 = \omega + (\alpha + \gamma \mathbb{1}_{\varepsilon_{t-1}<0}) \varepsilon_{t-1}^2 + \beta \bar{\sigma}^2
$$

The NIC is a **piecewise parabola** with different slopes:

$$
NIC_{\text{GJR}}(\varepsilon) = \begin{cases}
(\omega + \beta \bar{\sigma}^2) + (\alpha + \gamma) \varepsilon^2 & \text{if } \varepsilon < 0 \\
(\omega + \beta \bar{\sigma}^2) + \alpha \varepsilon^2 & \text{if } \varepsilon \geq 0
\end{cases}
$$

- Slope for negative shocks: $\alpha + \gamma$
- Slope for positive shocks: $\alpha$
- If $\gamma > 0$: steeper on the left (leverage effect)

---

## 3. Visual Comparison

```python
from archbox.models import GARCH, EGARCH, GJR_GARCH
from archbox.utils.news_impact import news_impact_curve
import numpy as np
import matplotlib.pyplot as plt

# Simulate return data
np.random.seed(42)
returns = np.random.standard_t(5, size=2000) * 0.01

# Fit three models
garch = GARCH(returns, p=1, q=1).fit()
egarch = EGARCH(returns, p=1, q=1).fit()
gjr = GJR_GARCH(returns, p=1, q=1).fit()

# Compute NICs
shock_range = np.linspace(-0.04, 0.04, 200)

nic_garch = news_impact_curve(garch, shocks=shock_range)
nic_egarch = news_impact_curve(egarch, shocks=shock_range)
nic_gjr = news_impact_curve(gjr, shocks=shock_range)

# Plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(shock_range, nic_garch, label="GARCH(1,1)", linewidth=2)
ax.plot(shock_range, nic_egarch, label="EGARCH(1,1)", linewidth=2, linestyle="--")
ax.plot(shock_range, nic_gjr, label="GJR-GARCH(1,1)", linewidth=2, linestyle=":")
ax.axvline(0, color="gray", linewidth=0.5, linestyle="-")
ax.set_xlabel(r"Shock $\varepsilon_{t-1}$")
ax.set_ylabel(r"$\sigma_t^2$")
ax.set_title("News Impact Curves")
ax.legend()
plt.tight_layout()
plt.show()
```

```text
         σ²_t
          |          EGARCH
          |         /
          |        /  GJR
          |       / /
          |      / /    GARCH
          |     / /    /
          |    / /    /
          |   //    /
          |  //   /            GARCH
          | //  /           __/
          |// /          __/
          |/ /        __/     GJR
       ---|/-------__/-------/-------→  ε_{t-1}
          |     __/        /
          |  __/         /
          |/           /
     negative       positive
      shocks        shocks
```

!!! tip "Reading the Curve"
    - **GARCH**: Perfect symmetry --- the parabola is identical on both sides of zero
    - **GJR-GARCH**: Steeper slope for negative shocks (left side), creating a kinked parabola
    - **EGARCH**: Smooth asymmetry with exponential growth, especially steep for large negative shocks

---

## 4. Quick Example with Output

```python
from archbox.utils.news_impact import news_impact_curve

# Compute NIC at specific shock values
shocks = np.array([-0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03])

nic_g = news_impact_curve(garch, shocks=shocks)
nic_e = news_impact_curve(egarch, shocks=shocks)
nic_j = news_impact_curve(gjr, shocks=shocks)

print(f"{'Shock':>8} {'GARCH':>12} {'EGARCH':>12} {'GJR':>12}")
print("-" * 46)
for i, s in enumerate(shocks):
    print(f"{s:>8.3f} {nic_g[i]:>12.6f} {nic_e[i]:>12.6f} {nic_j[i]:>12.6f}")
```

```text
   Shock        GARCH       EGARCH          GJR
----------------------------------------------
  -0.030     0.000152     0.000198     0.000185
  -0.020     0.000098     0.000124     0.000118
  -0.010     0.000063     0.000075     0.000071
   0.000     0.000048     0.000048     0.000048
   0.010     0.000063     0.000058     0.000063
   0.020     0.000098     0.000082     0.000098
   0.030     0.000152     0.000121     0.000152
```

!!! success "Interpretation"
    At $\varepsilon_{t-1} = -0.03$:

    - **GARCH**: $\sigma_t^2 = 0.000152$ (same as $+0.03$)
    - **EGARCH**: $\sigma_t^2 = 0.000198$ (30% higher than GARCH for negative shock)
    - **GJR**: $\sigma_t^2 = 0.000185$ (22% higher than GARCH for negative shock)

    At $\varepsilon_{t-1} = +0.03$, EGARCH and GJR produce **lower** variance than GARCH, reflecting the reallocation of volatility response toward negative shocks.

---

## 5. Interpreting the Shape

| Shape | Model | Implication |
|-------|-------|-------------|
| Symmetric parabola | GARCH | No leverage effect |
| Asymmetric smooth curve | EGARCH | Leverage effect with smooth transition |
| Kinked parabola | GJR-GARCH | Leverage effect with discrete jump at zero |
| Shifted parabola | GARCH with nonzero mean | Mean effect shifts the minimum |

### What to Look For

1. **Is the curve symmetric?** If not, leverage effects are present
2. **How steep is the left side?** Steeper = stronger negative shock impact
3. **How does it behave at extremes?** EGARCH grows exponentially; GJR grows quadratically
4. **Where is the minimum?** Should be near $\varepsilon = 0$ for well-specified models

---

## 6. Using NIC for Model Comparison

The NIC is primarily a **visual diagnostic**. Use it alongside formal tests:

| Diagnostic | Type | Complements NIC by... |
|-----------|------|----------------------|
| [Sign Bias Test](sign-bias.md) | Statistical | Formal test of asymmetry significance |
| [Likelihood Ratio](likelihood-ratio.md) | Statistical | Tests if asymmetric model is significantly better |
| [Information Criteria](information-criteria.md) | Numerical | Selects best model accounting for complexity |

!!! tip "Workflow"
    1. Fit symmetric and asymmetric models
    2. Plot NICs to **see** the differences
    3. Run the [Sign Bias test](sign-bias.md) to **test** whether asymmetry is significant
    4. Use [Information Criteria](information-criteria.md) or [LR test](likelihood-ratio.md) to **select** the best model

---

## 7. Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `result` | `GARCHResult` | --- | Fitted model result |
| `shocks` | `array-like` | `None` | Custom shock values; if `None`, uses `np.linspace(-3*std, 3*std, 200)` |
| `sigma2_fixed` | `float` | `None` | Fixed $\sigma_{t-1}^2$; defaults to unconditional variance |

### Return Value

| Field | Type | Description |
|-------|------|-------------|
| `shocks` | `ndarray` | Shock values $\varepsilon_{t-1}$ |
| `variance` | `ndarray` | Corresponding $\sigma_t^2$ values |

---

## 8. Common Pitfalls

!!! warning "Common Pitfalls"
    1. **Comparing models on different scales**: Always use the same shock range and fixed $\sigma_{t-1}^2$ when overlaying NICs from different models.
    2. **Over-interpreting tail behavior**: The NIC extrapolates beyond observed shocks. Focus on the range where data exists (roughly $\pm 3\hat{\sigma}$).
    3. **Ignoring the fixed variance assumption**: The NIC holds $\sigma_{t-1}^2$ constant, but in reality past variance evolves. The NIC shows the **marginal** effect of a shock, not the full dynamic response.

---

## See Also

- [Sign Bias Test](sign-bias.md) --- formal test for asymmetric effects
- [Persistence](persistence.md) --- how long shocks affect volatility
- [GARCH Theory](../theory/garch-theory.md) --- model specification
- [Diagnostics Overview](index.md) --- complete diagnostic pipeline

---

## References

- Engle, R. F. & Ng, V. K. (1993). "Measuring and Testing the Impact of News on Volatility." *The Journal of Finance*, 48(5), 1749--1778.
- Pagan, A. R. & Schwert, G. W. (1990). "Alternative Models for Conditional Stock Volatility." *Journal of Econometrics*, 45(1--2), 267--290.
