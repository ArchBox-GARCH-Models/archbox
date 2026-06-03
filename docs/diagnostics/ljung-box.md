---
title: "Ljung-Box Test"
description: "Ljung-Box portmanteau test for autocorrelation in standardized residuals and squared residuals of GARCH models"
---

# Ljung-Box Test

!!! info "Quick Reference"
    **Function:** `archbox.diagnostics.ljung_box.ljung_box_squared`
    **$H_0$:** No autocorrelation up to lag $m$
    **$H_1$:** At least one autocorrelation $\rho_k \neq 0$ for $k \leq m$
    **Statistic:** $Q(m) = T(T+2) \sum_{k=1}^{m} \frac{\hat{\rho}_k^2}{T-k} \sim \chi^2(m)$
    **Apply to:** $z_t$ (mean adequacy) and $z_t^2$ (variance adequacy)

---

## 1. What It Tests

The Ljung-Box test is a **portmanteau test** for autocorrelation. In the context of GARCH models, it serves two distinct purposes depending on which series is tested:

| Series | Tests for | If rejected |
|--------|-----------|-------------|
| $z_t$ (standardized residuals) | Serial correlation in the mean | Mean equation is misspecified |
| $z_t^2$ (squared standardized residuals) | Remaining ARCH effects | Variance equation is misspecified |

If the GARCH model is correctly specified, $z_t$ should be i.i.d. with zero mean and unit variance. This means both $z_t$ and $z_t^2$ should exhibit **no autocorrelation** at any lag.

!!! tip "Two Tests, Two Questions"
    Always run Ljung-Box on **both** $z_t$ and $z_t^2$. Rejection on $z_t$ indicates the conditional mean is wrong (e.g., missing AR terms). Rejection on $z_t^2$ indicates the conditional variance is wrong (e.g., insufficient GARCH lags or missing asymmetry).

---

## 2. Mathematical Formulation

### Hypotheses

$$
H_0: \rho_1 = \rho_2 = \cdots = \rho_m = 0 \quad \text{(no autocorrelation up to lag } m\text{)}
$$

$$
H_1: \exists \, k \leq m \text{ such that } \rho_k \neq 0
$$

### Test Statistic

The Ljung-Box $Q$-statistic is:

$$
\boxed{Q(m) = T(T+2) \sum_{k=1}^{m} \frac{\hat{\rho}_k^2}{T-k}}
$$

where:

- $T$ is the sample size
- $\hat{\rho}_k$ is the sample autocorrelation at lag $k$
- $m$ is the maximum lag tested

### Asymptotic Distribution

Under $H_0$:

$$
Q(m) \xrightarrow{d} \chi^2(m)
$$

!!! note "Degrees of Freedom Adjustment"
    When testing residuals from an ARMA($p$, $q$)-GARCH model, some references suggest adjusting degrees of freedom to $\chi^2(m - p - q)$ to account for estimated mean parameters. The ArchBox implementation uses $\chi^2(m)$ (unadjusted), which is **conservative** --- it may slightly over-reject but is safer than under-rejecting.

### Sample Autocorrelation

The sample autocorrelation of a series $\{x_t\}$ at lag $k$ is:

$$
\hat{\rho}_k = \frac{\sum_{t=k+1}^{T}(x_t - \bar{x})(x_{t-k} - \bar{x})}{\sum_{t=1}^{T}(x_t - \bar{x})^2}
$$

---

## 3. Application to GARCH Residuals

### Testing the Mean Equation ($z_t$)

After estimating a GARCH model, extract the standardized residuals and compute the $Q$-statistic:

$$
z_t = \frac{\varepsilon_t}{\sigma_t}, \qquad Q_z(m) = T(T+2) \sum_{k=1}^{m} \frac{\hat{\rho}_k^2(z)}{T-k}
$$

**Rejection** indicates that $z_t$ is autocorrelated, meaning the conditional mean specification is inadequate. Possible remedies:

- Add AR or MA terms to the mean equation
- Include additional exogenous regressors

### Testing the Variance Equation ($z_t^2$)

$$
Q_{z^2}(m) = T(T+2) \sum_{k=1}^{m} \frac{\hat{\rho}_k^2(z^2)}{T-k}
$$

**Rejection** indicates remaining ARCH effects in $z_t^2$, meaning the variance specification is inadequate. Possible remedies:

- Increase the GARCH order ($p$ or $q$)
- Switch to an asymmetric model (EGARCH, GJR-GARCH)
- Consider a different distributional assumption

---

## 4. Quick Example

```python
from archbox.models import GARCH
from archbox.diagnostics.ljung_box import ljung_box_squared
import numpy as np

# Simulate or load return data
np.random.seed(42)
returns = np.random.standard_t(5, size=2000) * 0.01

# Fit GARCH(1,1)
model = GARCH(returns, p=1, q=1)
result = model.fit()

# Test squared residuals for remaining ARCH effects
z_t = result.std_resids

for m in [5, 10, 20]:
    lb = ljung_box_squared(z_t, lags=m)
    print(lb)
```

```text
Ljung-Box (z^2)(lags=5): statistic=3.2154, pvalue=0.6674
Ljung-Box (z^2)(lags=10): statistic=7.8912, pvalue=0.6393
Ljung-Box (z^2)(lags=20): statistic=15.2340, pvalue=0.7634
```

!!! tip "Reading the Output"
    All p-values are well above 0.05, so we **fail to reject** $H_0$ at the 5% level. The GARCH(1,1) model adequately captures the conditional variance dynamics --- no remaining ARCH effects in $z_t^2$.

---

## 5. Interpretation

| p-value | Decision | Interpretation |
|---------|----------|----------------|
| < 0.01 | Strong rejection | Clear evidence of autocorrelation --- model is misspecified |
| 0.01 -- 0.05 | Rejection | Autocorrelation present at the tested lag order |
| 0.05 -- 0.10 | Borderline | Weak evidence; inspect individual autocorrelations |
| > 0.10 | Fail to reject | No evidence of autocorrelation --- model passes |

---

## 6. Choosing the Number of Lags

!!! tip "Lag Selection Guidelines"
    - **Daily data**: test $m \in \{5, 10, 20\}$ (one week, two weeks, one month)
    - **Weekly data**: test $m \in \{4, 8, 12\}$ (one month, two months, one quarter)
    - **Monthly data**: test $m \in \{6, 12, 24\}$ (half year, one year, two years)
    - **General rule**: always test at least three different lag lengths to check robustness

The test has higher power against autocorrelation concentrated at specific lags when $m$ is small, but may miss higher-order patterns. Testing multiple lag lengths provides a more complete picture.

---

## 7. Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `std_resids` | `array-like` | — | Standardized residuals $z_t$ |
| `lags` | `int` | `10` | Number of lags $m$ |

### Result Fields

| Field | Type | Description |
|-------|------|-------------|
| `statistic` | `float` | $Q(m)$ test statistic |
| `pvalue` | `float` | p-value from $\chi^2(m)$ |
| `lags` | `int` | Number of lags tested |
| `test_name` | `str` | `"Ljung-Box (z^2)"` |

---

## 8. Common Pitfalls

!!! warning "Common Pitfalls"
    1. **Testing only $z_t^2$**: Always test $z_t$ as well. Autocorrelation in $z_t$ indicates mean misspecification, which can bias variance estimates.
    2. **Too few lags**: Testing only $m = 1$ may miss seasonal or higher-order patterns. Always use multiple values of $m$.
    3. **Too many lags**: With $m$ close to $T$, the test loses power. Keep $m \ll T$ (a common rule is $m \leq \sqrt{T}$).
    4. **Small samples**: The $\chi^2$ approximation requires $T \gg m$. For $T < 100$, consider using fewer lags or bootstrap-based alternatives.
    5. **Ignoring borderline results**: p-values between 0.05 and 0.10 deserve investigation. Plot the autocorrelation function to check for individual significant lags.

---

## See Also

- [ARCH-LM Test](arch-lm.md) — alternative test for residual ARCH effects
- [Diagnostics Overview](index.md) — complete diagnostic pipeline
- [GARCH Theory](../theory/garch-theory.md) — model specification

---

## References

- Ljung, G. M. & Box, G. E. P. (1978). "On a Measure of Lack of Fit in Time Series Models." *Biometrika*, 65(2), 297–303.
- Box, G. E. P. & Pierce, D. A. (1970). "Distribution of Residual Autocorrelations in Autoregressive-Integrated Moving Average Time Series Models." *Journal of the American Statistical Association*, 65(332), 1509–1526.
- Li, W. K. & Mak, T. K. (1994). "On the Squared Residual Autocorrelations in Non-Linear Time Series with Conditional Heteroskedasticity." *Journal of Time Series Analysis*, 15(6), 627–636.
