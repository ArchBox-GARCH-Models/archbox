---
title: "Jarque-Bera Test"
description: "Jarque-Bera normality test for standardized residuals of GARCH models: skewness, kurtosis, and distributional adequacy"
---

# Jarque-Bera Test

!!! info "Quick Reference"
    **Function:** `scipy.stats.jarque_bera` (used in `archbox.diagnostics.full_diagnostics`)
    **$H_0$:** Residuals are normally distributed ($S = 0$, $K = 3$)
    **$H_1$:** Residuals are not normally distributed
    **Statistic:** $JB = \frac{T}{6}\left[S^2 + \frac{(K-3)^2}{4}\right] \sim \chi^2(2)$
    **Key insight:** Rejection suggests using Student-$t$, Skewed-$t$, or GED distribution

---

## 1. What It Tests

The Jarque-Bera test checks whether the **standardized residuals** $z_t$ from a GARCH model follow a normal distribution by examining two key moments:

- **Skewness** ($S$): measures asymmetry. Normal distribution has $S = 0$.
- **Kurtosis** ($K$): measures tail heaviness. Normal distribution has $K = 3$.

Financial return residuals almost always exhibit **excess kurtosis** ($K > 3$) even after GARCH filtering. The Jarque-Bera test quantifies this departure from normality.

!!! tip "Practical Significance"
    Rejecting normality is **expected** with financial data. The test's value is not in surprising you, but in confirming that a non-normal distribution (Student-$t$, Skewed-$t$, GED) should be used for inference, confidence intervals, and risk measures like VaR and ES.

---

## 2. Mathematical Formulation

### Skewness and Kurtosis

For a sample $\{z_t\}_{t=1}^{T}$ with mean $\bar{z}$ and standard deviation $s$:

$$
S = \frac{1}{T} \sum_{t=1}^{T} \left(\frac{z_t - \bar{z}}{s}\right)^3
$$

$$
K = \frac{1}{T} \sum_{t=1}^{T} \left(\frac{z_t - \bar{z}}{s}\right)^4
$$

### Hypotheses

$$
H_0: S = 0 \text{ and } K = 3 \quad \text{(normal distribution)}
$$

$$
H_1: S \neq 0 \text{ or } K \neq 3
$$

### Test Statistic

$$
\boxed{JB = \frac{T}{6}\left[S^2 + \frac{(K-3)^2}{4}\right]}
$$

### Asymptotic Distribution

Under $H_0$:

$$
JB \xrightarrow{d} \chi^2(2)
$$

The two degrees of freedom correspond to the two moment conditions being tested (skewness and excess kurtosis).

??? note "Derivation"
    Under normality, the sample skewness and excess kurtosis are asymptotically independent:

    $$\sqrt{T} \cdot S \xrightarrow{d} N(0, 6)$$

    $$\sqrt{T} \cdot (K - 3) \xrightarrow{d} N(0, 24)$$

    The JB statistic is the sum of two squared standard normals:

    $$JB = \frac{(\sqrt{T} \cdot S)^2}{6} + \frac{(\sqrt{T} \cdot (K-3))^2}{24} \sim \chi^2(2)$$

---

## 3. Interpreting the Components

The JB statistic is the sum of two components. Decomposing it reveals **why** normality is rejected:

| Component | Formula | Measures | Financial interpretation |
|-----------|---------|----------|--------------------------|
| Skewness term | $\frac{T}{6} S^2$ | Asymmetry | Negative skew → more extreme losses than gains |
| Kurtosis term | $\frac{T}{6} \cdot \frac{(K-3)^2}{4}$ | Tail heaviness | Excess kurtosis → more extreme events than Normal predicts |

!!! warning "Kurtosis Dominates in Finance"
    For financial returns, the kurtosis term almost always dominates the JB statistic. Typical standardized GARCH residuals have $K$ between 4 and 8 even after filtering, while skewness is often close to zero. This means the rejection is driven by **fat tails**, not asymmetry.

---

## 4. Quick Example

```python
from archbox.models import GARCH
from archbox.diagnostics import full_diagnostics
from scipy.stats import jarque_bera, skew, kurtosis
import numpy as np

# Simulate or load return data
np.random.seed(42)
returns = np.random.standard_t(5, size=2000) * 0.01

# Fit GARCH(1,1) with Normal distribution
model = GARCH(returns, p=1, q=1)
result = model.fit()

# Jarque-Bera on standardized residuals
z_t = result.std_resids
jb_stat, jb_pval = jarque_bera(z_t)

print(f"Skewness:    {skew(z_t):.4f}")
print(f"Kurtosis:    {kurtosis(z_t, fisher=False):.4f}")
print(f"JB stat:     {jb_stat:.4f}")
print(f"JB p-value:  {jb_pval:.6f}")
```

```text
Skewness:    -0.0523
Kurtosis:     4.8712
JB stat:      287.4521
JB p-value:   0.000000
```

!!! tip "Reading the Output"
    The JB statistic is highly significant ($p \approx 0$), driven by excess kurtosis ($K = 4.87$ vs. the Normal's $K = 3$). Skewness is negligible ($S \approx -0.05$). This confirms that the Normal distribution is inadequate --- we should re-estimate with a Student-$t$ distribution.

---

## 5. Relationship to Distributional Choice

The Jarque-Bera test is most useful when the model is estimated under **normality**. If you already use a non-normal distribution, a different approach is needed:

=== "Normal Distribution"

    Use Jarque-Bera directly. Rejection means switch to a heavier-tailed distribution.

    ```python
    # If JB rejects, re-estimate with Student-t
    model_t = GARCH(returns, p=1, q=1, dist="t")
    result_t = model_t.fit()
    ```

=== "Student-t Distribution"

    Jarque-Bera tests against Normal, not Student-$t$. Instead, check whether the estimated degrees of freedom $\nu$ is consistent with the empirical kurtosis:

    $$K_{\text{theoretical}} = 3 + \frac{6}{\nu - 4} \quad (\nu > 4)$$

    Or use the [Kolmogorov-Smirnov test](kolmogorov-smirnov.md) with the fitted Student-$t$ CDF.

=== "Skewed-t Distribution"

    For skewed distributions, use the [Kolmogorov-Smirnov test](kolmogorov-smirnov.md) or PIT-based uniformity tests to verify distributional adequacy.

!!! note "JB After Non-Normal Estimation"
    If you fit a GARCH model with Student-$t$ errors, the standardized residuals should follow a Student-$t$, **not** a Normal. Running Jarque-Bera will reject (correctly), but this is not a model failure --- it simply confirms that the residuals are non-normal. Use KS or PIT tests instead.

---

## 6. Interpretation Table

| p-value | Decision | Action |
|---------|----------|--------|
| < 0.01 | Strong rejection | Use Student-$t$, Skewed-$t$, or GED |
| 0.01 -- 0.05 | Rejection | Non-normal distribution recommended |
| 0.05 -- 0.10 | Borderline | Normal may be acceptable; check kurtosis |
| > 0.10 | Fail to reject | Normal distribution is adequate |

---

## 7. Configuration Options

The Jarque-Bera test is accessed via `scipy.stats.jarque_bera` or through `full_diagnostics`:

```python
from archbox.diagnostics import full_diagnostics

report = full_diagnostics(result)
jb_stat, jb_pval = report.jarque_bera
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `x` | `array-like` | — | Sample data (standardized residuals) |

### Result Fields

| Field | Type | Description |
|-------|------|-------------|
| `statistic` | `float` | JB test statistic |
| `pvalue` | `float` | p-value from $\chi^2(2)$ |

---

## 8. Common Pitfalls

!!! warning "Common Pitfalls"
    1. **Expecting normality with financial data**: Financial returns almost never pass JB even after GARCH filtering. A rejection is information, not a failure --- it guides your distributional choice.
    2. **Applying JB after non-normal estimation**: If the model uses Student-$t$ errors, JB will reject because the true distribution is not Normal. Use KS or PIT instead.
    3. **Ignoring skewness**: If both $S$ and $K$ contribute to the JB statistic, consider a Skewed-$t$ distribution rather than a symmetric Student-$t$.
    4. **Small samples**: The $\chi^2(2)$ approximation is poor for $T < 50$. With small samples, use bootstrap-based tests or Shapiro-Wilk.
    5. **Confusing kurtosis conventions**: Some software reports **excess kurtosis** ($K - 3$), others report **raw kurtosis** ($K$). The JB formula uses raw kurtosis with the $-3$ built in.

---

## See Also

- [Kolmogorov-Smirnov Test](kolmogorov-smirnov.md) — general distributional goodness-of-fit
- [Diagnostics Overview](index.md) — complete diagnostic pipeline
- [Distributions Theory](../theory/distributions-theory.md) — available distributional assumptions

---

## References

- Jarque, C. M. & Bera, A. K. (1980). "Efficient Tests for Normality, Homoscedasticity, and Serial Independence of Regression Residuals." *Economics Letters*, 6(3), 255–259.
- Jarque, C. M. & Bera, A. K. (1987). "A Test for Normality of Observations and Regression Residuals." *International Statistical Review*, 55(2), 163–172.
- Bai, J. & Ng, S. (2005). "Tests for Skewness, Kurtosis, and Normality for Time Series Data." *Journal of Business & Economic Statistics*, 23(1), 49–60.
