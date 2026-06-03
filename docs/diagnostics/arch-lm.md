---
title: "ARCH-LM Test"
description: "Engle's ARCH-LM test for residual conditional heteroskedasticity in GARCH models"
---

# ARCH-LM Test

!!! info "Quick Reference"
    **Function:** `archbox.diagnostics.arch_lm.arch_lm_test`
    **$H_0$:** No ARCH effects (homoskedastic residuals)
    **$H_1$:** ARCH effects present ($\exists \, \alpha_i \neq 0$)
    **Statistic:** $LM = T \cdot R^2 \sim \chi^2(q)$
    **Based on:** Auxiliary regression of $z_t^2$ on its own lags

---

## 1. What It Tests

The ARCH-LM test (Engle, 1982) checks whether the **squared standardized residuals** from a GARCH model still exhibit conditional heteroskedasticity. If the variance equation is correctly specified, $z_t^2$ should have no predictable structure --- its lagged values should not help predict its current value.

This test is the canonical diagnostic for verifying that a GARCH model has adequately captured all volatility dynamics. A significant result means the model has **not fully absorbed** the time-varying variance in the data.

!!! tip "ARCH-LM vs. Ljung-Box on $z_t^2$"
    Both tests detect remaining ARCH effects, but they work differently. Ljung-Box checks for autocorrelation in $z_t^2$ via the portmanteau $Q$-statistic, while ARCH-LM uses an explicit auxiliary regression. In practice, they usually agree, but ARCH-LM has better power against specific ARCH alternatives because it directly tests the ARCH structure.

---

## 2. Mathematical Formulation

### Auxiliary Regression

Given standardized residuals $z_t$, compute $z_t^2$ and estimate the auxiliary OLS regression:

$$
\boxed{z_t^2 = \alpha_0 + \sum_{i=1}^{q} \alpha_i z_{t-i}^2 + v_t}
$$

where $q$ is the number of lags being tested.

### Hypotheses

$$
H_0: \alpha_1 = \alpha_2 = \cdots = \alpha_q = 0 \quad \text{(no ARCH effects)}
$$

$$
H_1: \exists \, i \leq q \text{ such that } \alpha_i \neq 0
$$

### LM Statistic

The Lagrange Multiplier statistic is:

$$
\boxed{LM = T \cdot R^2 \sim \chi^2(q)}
$$

where:

- $T$ is the number of observations in the auxiliary regression ($T_{\text{total}} - q$)
- $R^2$ is the coefficient of determination from the auxiliary regression
- $q$ is the number of lags (degrees of freedom)

### Why It Works

Under $H_0$ (no ARCH effects), the lagged squared residuals have no explanatory power for $z_t^2$, so $R^2 \approx 0$ and $LM \approx 0$. Under the alternative, $R^2 > 0$ and $LM$ grows with the sample size, leading to rejection.

??? note "Derivation"
    The test can be derived as a score (Lagrange Multiplier) test from the ARCH($q$) model:

    $$\sigma_t^2 = \omega + \sum_{i=1}^{q} \alpha_i \varepsilon_{t-i}^2$$

    Under $H_0: \alpha_1 = \cdots = \alpha_q = 0$, the score vector has the form:

    $$\frac{\partial \ell}{\partial \alpha} \bigg|_{H_0} \propto \sum_t (z_t^2 - 1) z_{t-i}^2$$

    The LM statistic based on the outer product of the score simplifies to $T \cdot R^2$ from the auxiliary regression above.

---

## 3. Choosing the Number of Lags

The choice of $q$ determines what ARCH structure the test can detect:

| Lags $q$ | Detects | Typical use |
|-----------|---------|-------------|
| 1 | ARCH(1) effects | Quick check |
| 5 | Weekly patterns (daily data) | Standard |
| 10 | Two-week patterns | Extended check |
| 20 | Monthly patterns | Thorough |

!!! tip "Multi-Lag Strategy"
    Always test multiple values of $q$. A model might pass at $q = 5$ but fail at $q = 10$ if there are longer-memory volatility patterns. The standard practice is to report results for $q \in \{1, 5, 10\}$.

---

## 4. Quick Example

```python
from archbox.models import GARCH
from archbox.diagnostics.arch_lm import arch_lm_test
import numpy as np

# Simulate or load return data
np.random.seed(42)
returns = np.random.standard_t(5, size=2000) * 0.01

# Fit GARCH(1,1)
model = GARCH(returns, p=1, q=1)
result = model.fit()

# Test for remaining ARCH effects at multiple lags
z_t = result.std_resids

print("Lag | LM Stat  | p-value  | Decision")
print("----|----------|----------|----------")
for q in [1, 5, 10]:
    test = arch_lm_test(z_t, lags=q)
    decision = "FAIL" if test.pvalue < 0.05 else "PASS"
    print(f"  {q:2d} | {test.statistic:8.4f} | {test.pvalue:8.4f} | {decision}")
```

```text
Lag | LM Stat  | p-value  | Decision
----|----------|----------|----------
   1 |   0.2340 |   0.6287 | PASS
   5 |   2.1560 |   0.8272 | PASS
  10 |   5.4320 |   0.8607 | PASS
```

!!! tip "Reading the Output"
    All p-values exceed 0.05, so we **fail to reject** $H_0$ at every lag. The GARCH(1,1) model has successfully captured the conditional heteroskedasticity --- no remaining ARCH effects in the squared residuals.

---

## 5. Interpretation

| p-value | Decision | Interpretation |
|---------|----------|----------------|
| < 0.01 | Strong rejection | Strong residual ARCH effects --- model is inadequate |
| 0.01 -- 0.05 | Rejection | ARCH effects present; consider higher-order GARCH |
| 0.05 -- 0.10 | Borderline | Weak evidence; inspect auxiliary regression coefficients |
| > 0.10 | Fail to reject | No residual ARCH effects --- model passes |

### What to Do When the Test Fails

!!! warning "Remedies for Residual ARCH Effects"
    1. **Increase GARCH order**: Try GARCH(1,2) or GARCH(2,1)
    2. **Switch to asymmetric model**: EGARCH or GJR-GARCH may capture asymmetric volatility that standard GARCH misses
    3. **Change distribution**: Heavy-tailed distributions (Student-$t$, GED) can reduce spurious ARCH effects caused by distributional misspecification
    4. **Component models**: For long-memory volatility, consider FIGARCH or component GARCH
    5. **Check mean equation**: Missing mean dynamics can appear as ARCH effects in residuals

---

## 6. Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `resids` | `array-like` | — | Residual series (raw or standardized) |
| `lags` | `int` | `5` | Number of lags $q$ for the auxiliary regression |

### Result Fields

| Field | Type | Description |
|-------|------|-------------|
| `statistic` | `float` | $LM = T \cdot R^2$ |
| `pvalue` | `float` | p-value from $\chi^2(q)$ |
| `test_name` | `str` | `"ARCH-LM"` |
| `lags` | `int` | Number of lags tested |

---

## 7. Relationship to Other Tests

| Test | Method | Advantage |
|------|--------|-----------|
| **ARCH-LM** | Auxiliary regression | Direct test of ARCH structure; optimal power against ARCH alternatives |
| **Ljung-Box** ($z_t^2$) | Portmanteau | More general; detects any autocorrelation in $z_t^2$ |
| **McLeod-Li** | Ljung-Box on $z_t^2$ | Equivalent to Ljung-Box on squared residuals |

The ARCH-LM test is **locally most powerful** against ARCH alternatives, making it the preferred test when the alternative is specifically ARCH-type heteroskedasticity.

---

## 8. Common Pitfalls

!!! warning "Common Pitfalls"
    1. **Using raw residuals**: Apply the test to **standardized** residuals $z_t$ from the GARCH model, not the raw residuals $\varepsilon_t$. Testing raw residuals will detect the ARCH effects the model was designed to capture, giving a misleading rejection.
    2. **Too many lags**: With $q$ close to $T$, the auxiliary regression has too many parameters relative to observations. Keep $q \ll T$.
    3. **Ignoring the mean equation**: ARCH-LM on residuals from a misspecified mean equation may find spurious ARCH effects. Verify the mean equation first.
    4. **Single lag only**: Testing only $q = 1$ may miss higher-order structure. Always report multiple lag lengths.
    5. **Pre-estimation vs. post-estimation**: Before fitting a GARCH model, ARCH-LM on raw returns confirms that ARCH effects exist (justifying the model). After fitting, ARCH-LM on standardized residuals confirms the model captured them.

---

## See Also

- [Ljung-Box Test](ljung-box.md) — portmanteau test for autocorrelation
- [Diagnostics Overview](index.md) — complete diagnostic pipeline
- [GARCH Theory](../theory/garch-theory.md) — model specification

---

## References

- Engle, R. F. (1982). "Autoregressive Conditional Heteroscedasticity with Estimates of the Variance of United Kingdom Inflation." *Econometrica*, 50(4), 987–1007.
- Lee, J. H. & King, M. L. (1993). "A Locally Most Mean Powerful Based Score Test for ARCH and GARCH Regression Disturbances." *Journal of Business & Economic Statistics*, 11(1), 17–27.
