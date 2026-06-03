---
title: "Likelihood Ratio Test"
description: "Likelihood Ratio test for comparing nested GARCH models with chi-squared asymptotics"
---

# Likelihood Ratio Test

!!! info "Quick Reference"
    **Function:** `archbox.diagnostics.likelihood_ratio.lr_test`
    **$H_0$:** Restricted model is adequate (restrictions are valid)
    **$H_1$:** Unrestricted model provides significantly better fit
    **Statistic:** $LR = 2(\ell_u - \ell_r) \sim \chi^2(r)$
    **Requirement:** Models must be **nested**

---

## 1. What It Tests

The Likelihood Ratio (LR) test compares two **nested** models --- the restricted model is a special case of the unrestricted model obtained by imposing $r$ parameter restrictions. The test asks: does the unrestricted model fit significantly better than the restricted one?

!!! tip "Nested vs. Non-Nested"
    Two models are **nested** if the restricted model can be obtained from the unrestricted model by setting some parameters to specific values. For example:

    - GARCH(1,1) is nested in GARCH(2,1) --- set $\alpha_2 = 0$
    - IGARCH is nested in GARCH --- impose $\alpha + \beta = 1$
    - GARCH is nested in GJR-GARCH --- set $\gamma = 0$

    For **non-nested** models (e.g., EGARCH vs. GJR), use [Information Criteria](information-criteria.md) instead.

---

## 2. Mathematical Formulation

### LR Statistic

Given an unrestricted model with log-likelihood $\ell_u$ and a restricted model with log-likelihood $\ell_r$:

$$
\boxed{LR = 2(\ell_u - \ell_r) \sim \chi^2(r)}
$$

where $r$ is the number of restrictions (difference in number of parameters).

### Properties

- $LR \geq 0$ always, since the unrestricted model fits at least as well
- Under $H_0$, $LR$ is asymptotically $\chi^2(r)$
- The test is one-sided: reject $H_0$ for large values of $LR$

??? note "Derivation"
    The LR statistic arises from the likelihood ratio:

    $$\Lambda = \frac{L_r}{L_u} = \frac{\max_{\theta \in \Theta_0} L(\theta)}{\max_{\theta \in \Theta} L(\theta)}$$

    where $\Theta_0 \subset \Theta$. By Wilks' theorem:

    $$-2 \ln \Lambda = 2(\ell_u - \ell_r) \xrightarrow{d} \chi^2(r)$$

    under standard regularity conditions (the restricted parameters are not on the boundary of the parameter space).

---

## 3. Testing Common Restrictions

### GARCH vs. IGARCH ($\alpha + \beta = 1$)

| Model | Restriction | $r$ |
|-------|-------------|-----|
| Unrestricted: GARCH(1,1) | None | --- |
| Restricted: IGARCH(1,1) | $\alpha_1 + \beta_1 = 1$ | 1 |

$$
H_0: \alpha_1 + \beta_1 = 1 \quad \text{(integrated GARCH)}
$$

!!! warning "Boundary Problem"
    When $\alpha + \beta = 1$ lies on the boundary of the parameter space, the standard $\chi^2$ distribution may not apply. In practice, the test is still used as an approximation, but be cautious with borderline results.

### GARCH vs. GJR-GARCH ($\gamma = 0$)

| Model | Restriction | $r$ |
|-------|-------------|-----|
| Unrestricted: GJR-GARCH(1,1) | None | --- |
| Restricted: GARCH(1,1) | $\gamma = 0$ | 1 |

$$
H_0: \gamma = 0 \quad \text{(no leverage effect)}
$$

### GARCH vs. GARCH-M ($\lambda = 0$)

| Model | Restriction | $r$ |
|-------|-------------|-----|
| Unrestricted: GARCH-M(1,1) | None | --- |
| Restricted: GARCH(1,1) | $\lambda = 0$ | 1 |

$$
H_0: \lambda = 0 \quad \text{(no risk premium in mean)}
$$

---

## 4. Quick Example

```python
from archbox.models import GARCH, GJR_GARCH
from archbox.diagnostics.likelihood_ratio import lr_test
import numpy as np

# Simulate return data
np.random.seed(42)
returns = np.random.standard_t(5, size=2000) * 0.01

# Fit restricted (GARCH) and unrestricted (GJR-GARCH) models
restricted = GARCH(returns, p=1, q=1).fit()
unrestricted = GJR_GARCH(returns, p=1, q=1).fit()

# Likelihood Ratio test: is the leverage parameter significant?
test = lr_test(unrestricted, restricted)

print(f"Log-likelihood (GARCH):     {restricted.loglik:.4f}")
print(f"Log-likelihood (GJR-GARCH): {unrestricted.loglik:.4f}")
print(f"LR statistic:               {test.statistic:.4f}")
print(f"Degrees of freedom:         {test.df}")
print(f"p-value:                    {test.pvalue:.4f}")
```

```text
Log-likelihood (GARCH):     5842.3100
Log-likelihood (GJR-GARCH): 5849.8300
LR statistic:               15.0400
Degrees of freedom:         1
p-value:                    0.0001
```

!!! success "Interpretation"
    The LR statistic is 15.04 with $p < 0.001$. We **reject** $H_0: \gamma = 0$. The GJR-GARCH model provides a significantly better fit, indicating that leverage effects are present in the data. Negative shocks have a different impact on volatility than positive shocks of the same magnitude.

---

## 5. Multiple Comparisons Example

```python
from archbox.models import GARCH, EGARCH, GJR_GARCH, GARCH_M
from archbox.diagnostics.likelihood_ratio import lr_test

# Fit models
garch = GARCH(returns, p=1, q=1).fit()
garch21 = GARCH(returns, p=2, q=1).fit()
gjr = GJR_GARCH(returns, p=1, q=1).fit()

# Test 1: GARCH(1,1) vs GARCH(2,1) -- is alpha_2 needed?
test1 = lr_test(garch21, garch)

# Test 2: GARCH(1,1) vs GJR-GARCH(1,1) -- is leverage present?
test2 = lr_test(gjr, garch)

print(f"{'Test':<35} {'LR':>8} {'df':>4} {'p-value':>10} {'Decision':>10}")
print("-" * 70)
print(f"{'GARCH(1,1) vs GARCH(2,1)':<35} {test1.statistic:>8.4f} {test1.df:>4d} {test1.pvalue:>10.4f} {'Reject' if test1.pvalue < 0.05 else 'Fail':>10}")
print(f"{'GARCH(1,1) vs GJR-GARCH(1,1)':<35} {test2.statistic:>8.4f} {test2.df:>4d} {test2.pvalue:>10.4f} {'Reject' if test2.pvalue < 0.05 else 'Fail':>10}")
```

```text
Test                                      LR   df    p-value   Decision
----------------------------------------------------------------------
GARCH(1,1) vs GARCH(2,1)              1.1600    1     0.2815       Fail
GARCH(1,1) vs GJR-GARCH(1,1)         15.0400    1     0.0001     Reject
```

!!! tip "Reading the Results"
    - The extra $\alpha_2$ parameter in GARCH(2,1) does **not** significantly improve the fit ($p = 0.28$). Stick with GARCH(1,1).
    - The leverage parameter in GJR-GARCH **does** significantly improve the fit ($p < 0.001$). The asymmetric model is preferred.

---

## 6. Interpretation

| p-value | Decision | Interpretation |
|---------|----------|----------------|
| < 0.01 | Strong rejection | Unrestricted model is strongly preferred |
| 0.01 -- 0.05 | Rejection | Unrestricted model is preferred at 5% level |
| 0.05 -- 0.10 | Borderline | Weak evidence against restrictions |
| > 0.10 | Fail to reject | Restrictions are valid; prefer the simpler model |

---

## 7. Limitations

!!! warning "Limitations of the LR Test"
    1. **Nested models only**: Cannot compare EGARCH vs. GJR-GARCH (neither is a special case of the other). Use [Information Criteria](information-criteria.md) for non-nested comparisons.
    2. **Boundary parameters**: When $H_0$ places parameters on the boundary of the parameter space (e.g., $\alpha = 0$ in GARCH, where $\alpha \geq 0$), the $\chi^2$ approximation breaks down. The correct distribution is a mixture of $\chi^2$ distributions.
    3. **Same data required**: Both models must be estimated on exactly the same sample.
    4. **Convergence**: Both models must have converged to their global maximum. Local maxima will distort the test.
    5. **Same distribution**: Both models should use the same error distribution. Comparing Normal-GARCH to Student-$t$-GJR confounds the distribution and variance equation effects.

---

## 8. Configuration

| Parameter | Type | Description |
|-----------|------|-------------|
| `unrestricted` | `GARCHResult` | Fitted unrestricted (larger) model |
| `restricted` | `GARCHResult` | Fitted restricted (smaller) model |

### Result Fields

| Field | Type | Description |
|-------|------|-------------|
| `statistic` | `float` | $LR = 2(\ell_u - \ell_r)$ |
| `pvalue` | `float` | p-value from $\chi^2(r)$ |
| `df` | `int` | Degrees of freedom $r$ |
| `test_name` | `str` | `"Likelihood Ratio"` |

---

## See Also

- [Information Criteria](information-criteria.md) --- for non-nested model comparison
- [Sign Bias Test](sign-bias.md) --- test for asymmetric effects
- [Diagnostics Overview](index.md) --- complete diagnostic pipeline

---

## References

- Wilks, S. S. (1938). "The Large-Sample Distribution of the Likelihood Ratio for Testing Composite Hypotheses." *The Annals of Mathematical Statistics*, 9(1), 60--62.
- Vuong, Q. H. (1989). "Likelihood Ratio Tests for Model Selection and Non-Nested Hypotheses." *Econometrica*, 57(2), 307--333.
