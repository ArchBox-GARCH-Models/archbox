---
title: "Kolmogorov-Smirnov Test"
description: "Kolmogorov-Smirnov goodness-of-fit test and Probability Integral Transform for GARCH model residuals"
---

# Kolmogorov-Smirnov Test

!!! info "Quick Reference"
    **Function:** `scipy.stats.kstest`
    **$H_0$:** Residuals follow the specified distribution
    **$H_1$:** Residuals do not follow the specified distribution
    **Statistic:** $D_n = \sup_x |F_n(x) - F(x)|$
    **Key technique:** Probability Integral Transform (PIT) for any distributional assumption

---

## 1. What It Tests

The Kolmogorov-Smirnov (KS) test measures the maximum distance between the **empirical distribution function** (EDF) of the standardized residuals and a **theoretical reference distribution**. Unlike the Jarque-Bera test (which only checks normality), the KS test can verify adherence to **any** continuous distribution --- Normal, Student-$t$, Skewed-$t$, GED, or mixtures.

This makes the KS test the primary tool for verifying that the distributional assumption used in GARCH estimation is consistent with the observed residuals.

!!! tip "When to Use KS Instead of Jarque-Bera"
    - **Jarque-Bera**: only tests normality ($S = 0$, $K = 3$). Use when the model assumes Normal errors.
    - **Kolmogorov-Smirnov**: tests any distribution. Use when the model assumes Student-$t$, Skewed-$t$, GED, or any non-normal distribution.

---

## 2. Mathematical Formulation

### Empirical Distribution Function

For an ordered sample $z_{(1)} \leq z_{(2)} \leq \cdots \leq z_{(T)}$, the EDF is:

$$
F_n(x) = \frac{1}{T} \sum_{t=1}^{T} \mathbf{1}(z_{(t)} \leq x)
$$

### Test Statistic

$$
\boxed{D_n = \sup_x |F_n(x) - F(x)|}
$$

where $F(x)$ is the CDF of the hypothesized distribution.

In practice, the supremum is computed at the sample points:

$$
D_n = \max_{1 \leq t \leq T} \left\{ \max\left(\left|\frac{t}{T} - F(z_{(t)})\right|, \left|F(z_{(t)}) - \frac{t-1}{T}\right|\right) \right\}
$$

### Asymptotic Distribution

Under $H_0$, the scaled statistic $\sqrt{T} \cdot D_n$ converges to the **Kolmogorov distribution**:

$$
P(\sqrt{T} \cdot D_n \leq x) \to K(x) = 1 - 2\sum_{k=1}^{\infty} (-1)^{k-1} e^{-2k^2 x^2}
$$

!!! note "Parameters Estimated from Data"
    When the reference distribution's parameters are estimated from the same data (as in GARCH models), the standard KS critical values are **too conservative**. The Lilliefors correction addresses this for the normal case; for general distributions, bootstrap-based p-values or the PIT approach (Section 4) is preferred.

---

## 3. Application to GARCH Residuals

### Direct KS Test

After fitting a GARCH model with a specific distributional assumption, test whether the standardized residuals follow that distribution:

=== "Normal"

    ```python
    from scipy.stats import kstest

    z_t = result.std_resids
    stat, pval = kstest(z_t, 'norm')
    print(f"KS stat: {stat:.4f}, p-value: {pval:.4f}")
    ```

=== "Student-t"

    ```python
    from scipy.stats import kstest, t as t_dist

    z_t = result.std_resids
    nu = result.params['nu']  # estimated degrees of freedom

    # Standardized t: zero mean, unit variance
    scale = np.sqrt((nu - 2) / nu)
    stat, pval = kstest(z_t, lambda x: t_dist.cdf(x / scale, df=nu))
    print(f"KS stat: {stat:.4f}, p-value: {pval:.4f}")
    ```

=== "GED"

    ```python
    from scipy.stats import kstest, gennorm

    z_t = result.std_resids
    shape = result.params['shape']  # GED shape parameter
    stat, pval = kstest(z_t, lambda x: gennorm.cdf(x, beta=shape))
    print(f"KS stat: {stat:.4f}, p-value: {pval:.4f}")
    ```

---

## 4. Probability Integral Transform (PIT)

The PIT provides a **distribution-free** approach to checking any distributional assumption. The idea is simple: if $z_t \sim F$, then $u_t = F(z_t)$ should be uniformly distributed on $[0, 1]$.

### Theory

$$
\boxed{u_t = F(z_t; \hat{\theta}) \sim \text{Uniform}(0, 1) \quad \text{under } H_0}
$$

where $F(\cdot; \hat{\theta})$ is the CDF of the assumed distribution with estimated parameters $\hat{\theta}$.

### PIT Procedure

1. Compute standardized residuals $z_t$
2. Apply the estimated CDF: $u_t = F(z_t; \hat{\theta})$
3. Test $\{u_t\}$ for uniformity using KS test against $\text{Uniform}(0, 1)$

```python
from scipy.stats import kstest, t as t_dist
import numpy as np

z_t = result.std_resids
nu = result.params['nu']

# PIT: transform to uniform
scale = np.sqrt((nu - 2) / nu)
u_t = t_dist.cdf(z_t / scale, df=nu)

# Test uniformity
stat, pval = kstest(u_t, 'uniform')
print(f"PIT KS stat: {stat:.4f}, p-value: {pval:.4f}")
```

```text
PIT KS stat: 0.0187, p-value: 0.4823
```

!!! tip "Why PIT Is Preferred"
    The PIT approach reduces every distributional test to a test of uniformity. This is elegant because:

    1. The KS test for uniformity has exact critical values (no parameter estimation issue)
    2. It works for **any** distribution, including mixtures and skewed distributions
    3. Visual diagnostics (histogram of $u_t$) are easy to interpret

---

## 5. Visual Diagnostics: QQ-Plot

The QQ-plot complements the KS test by providing a **visual** assessment of distributional fit. Points should fall along the 45° line if the distributional assumption is correct.

```python
import matplotlib.pyplot as plt
from scipy.stats import probplot, t as t_dist
import numpy as np

z_t = result.std_resids
nu = result.params['nu']

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# QQ-plot against Normal
probplot(z_t, dist="norm", plot=axes[0])
axes[0].set_title("QQ-Plot vs. Normal")
axes[0].get_lines()[0].set_markerfacecolor('steelblue')

# QQ-plot against Student-t
probplot(z_t, dist=t_dist, sparams=(nu,), plot=axes[1])
axes[1].set_title(f"QQ-Plot vs. Student-t (ν={nu:.1f})")
axes[1].get_lines()[0].set_markerfacecolor('steelblue')

# PIT histogram
u_t = t_dist.cdf(z_t * np.sqrt((nu - 2) / nu), df=nu)
axes[2].hist(u_t, bins=30, density=True, color='steelblue', alpha=0.7,
             edgecolor='white')
axes[2].axhline(y=1.0, color='red', linestyle='--', label='Uniform(0,1)')
axes[2].set_title("PIT Histogram")
axes[2].set_xlabel("$u_t$")
axes[2].legend()

plt.tight_layout()
plt.show()
```

!!! tip "Reading QQ-Plots"
    - **S-shaped deviation**: tails are heavier (or lighter) than assumed → change distribution
    - **Deviation at one tail only**: skewness → consider Skewed-$t$
    - **Points on the line**: distributional assumption is adequate
    - **PIT histogram flat at 1.0**: correct distributional specification

---

## 6. Interpretation

| p-value | Decision | Interpretation |
|---------|----------|----------------|
| < 0.01 | Strong rejection | Distribution is clearly wrong; try alternatives |
| 0.01 -- 0.05 | Rejection | Distributional misspecification; consider heavier tails or asymmetry |
| 0.05 -- 0.10 | Borderline | Inspect QQ-plot for localized deviations |
| > 0.10 | Fail to reject | Distributional assumption is adequate |

---

## 7. Complete Example

```python
from archbox.models import GARCH
from scipy.stats import kstest, jarque_bera, t as t_dist
import numpy as np

np.random.seed(42)
returns = np.random.standard_t(5, size=2000) * 0.01

# Fit with Normal distribution
model_n = GARCH(returns, p=1, q=1, dist="normal")
result_n = model_n.fit()
z_n = result_n.std_resids

# Fit with Student-t distribution
model_t = GARCH(returns, p=1, q=1, dist="student-t")
result_t = model_t.fit()
z_t = result_t.std_resids
nu = result_t.params['nu']

# Compare distributional fit
print("=== Normal GARCH(1,1) ===")
jb_stat, jb_pval = jarque_bera(z_n)
ks_stat, ks_pval = kstest(z_n, 'norm')
print(f"Jarque-Bera: stat={jb_stat:.2f}, p={jb_pval:.6f}")
print(f"KS (Normal): stat={ks_stat:.4f}, p={ks_pval:.4f}")

print(f"\n=== Student-t GARCH(1,1) (ν={nu:.2f}) ===")
scale = np.sqrt((nu - 2) / nu)
u_t = t_dist.cdf(z_t / scale, df=nu)
ks_pit, ks_pit_p = kstest(u_t, 'uniform')
print(f"KS (PIT):    stat={ks_pit:.4f}, p={ks_pit_p:.4f}")
```

```text
=== Normal GARCH(1,1) ===
Jarque-Bera: stat=287.45, p=0.000000
KS (Normal): stat=0.0456, p=0.0003

=== Student-t GARCH(1,1) (ν=5.23) ===
KS (PIT):    stat=0.0187, p=0.4823
```

!!! tip "Reading the Comparison"
    The Normal assumption fails both JB and KS tests decisively. After switching to Student-$t$, the PIT-based KS test shows no evidence of distributional misspecification ($p = 0.48$). The Student-$t$ with $\nu \approx 5.2$ correctly captures the heavy tails.

---

## 8. Common Pitfalls

!!! warning "Common Pitfalls"
    1. **Using standard KS with estimated parameters**: When parameters are estimated from the data, the standard KS test is conservative (p-values too large). Use PIT-based uniformity testing or bootstrap p-values.
    2. **Ignoring standardization**: For Student-$t$, residuals must be scaled to have unit variance. The standardized Student-$t$ has variance $\nu/(\nu-2)$, so divide by $\sqrt{\nu/(\nu-2)}$ before applying the CDF.
    3. **Discrete or tied data**: KS assumes a continuous distribution. If residuals have ties (identical values), the test may be unreliable.
    4. **Large samples overpower the test**: With $T > 5000$, KS detects even tiny, practically irrelevant deviations. Supplement with QQ-plots and effect size ($D_n$ value) rather than relying solely on the p-value.
    5. **Confusing one-sample and two-sample KS**: The one-sample KS test compares data against a theoretical distribution. The two-sample KS compares two empirical samples. For GARCH diagnostics, use the one-sample version.

---

## See Also

- [Jarque-Bera Test](jarque-bera.md) — normality-specific test
- [Diagnostics Overview](index.md) — complete diagnostic pipeline
- [Distributions Theory](../theory/distributions-theory.md) — available distributional assumptions

---

## References

- Kolmogorov, A. N. (1933). "Sulla determinazione empirica di una legge di distribuzione." *Giornale dell'Istituto Italiano degli Attuari*, 4, 83–91.
- Smirnov, N. V. (1948). "Table for Estimating the Goodness of Fit of Empirical Distributions." *Annals of Mathematical Statistics*, 19(2), 279–281.
- Diebold, F. X., Gunther, T. A. & Tay, A. S. (1998). "Evaluating Density Forecasts with Applications to Financial Risk Management." *International Economic Review*, 39(4), 863–883.
- Berkowitz, J. (2001). "Testing Density Forecasts, with Applications to Risk Management." *Journal of Business & Economic Statistics*, 19(4), 465–474.
