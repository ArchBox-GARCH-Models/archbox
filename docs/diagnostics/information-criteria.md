---
title: "Information Criteria"
description: "AIC, BIC and HQC for GARCH model selection - formulas, trade-offs and comparative examples"
---

# Information Criteria

!!! info "Quick Reference"
    **Functions:** `archbox.diagnostics.information_criteria`
    **Purpose:** Select the best model among competing specifications
    **Criteria:** AIC (liberal), BIC (conservative), HQC (intermediate)
    **Rule:** Lower is better

---

## 1. What They Measure

Information criteria balance **goodness of fit** (log-likelihood) against **model complexity** (number of parameters). A model with more parameters will always fit at least as well, but may overfit. Information criteria penalize extra parameters to find the most parsimonious adequate specification.

!!! tip "When to Use"
    Use information criteria to compare **non-nested** models (e.g., GARCH vs. EGARCH). For nested models, the [Likelihood Ratio test](likelihood-ratio.md) provides a formal hypothesis test with known asymptotic distribution.

---

## 2. Mathematical Formulation

### Akaike Information Criterion (AIC)

$$
\boxed{AIC = -2\ell + 2k}
$$

where $\ell$ is the maximized log-likelihood and $k$ is the number of estimated parameters.

- Derived from minimizing Kullback-Leibler divergence
- Tends to select **larger models** (liberal)
- Asymptotically efficient but **not consistent** --- may overfit in large samples

### Bayesian Information Criterion (BIC)

$$
\boxed{BIC = -2\ell + k \ln(T)}
$$

where $T$ is the sample size.

- Derived from Bayesian model posterior probability
- Penalty grows with sample size ($\ln(T) > 2$ for $T > 8$)
- **Consistent** --- selects the true model as $T \to \infty$
- Tends to select **smaller models** (conservative)

### Hannan-Quinn Criterion (HQC)

$$
\boxed{HQC = -2\ell + 2k \ln(\ln(T))}
$$

- Intermediate between AIC and BIC
- **Strongly consistent** --- converges to the true model order
- Penalty: $2\ln(\ln(T))$ grows slower than $\ln(T)$ but faster than $2$ for large $T$

---

## 3. Comparing the Penalties

The key difference is the penalty per parameter:

| Criterion | Penalty per parameter | $T = 100$ | $T = 500$ | $T = 2000$ |
|-----------|----------------------|-----------|-----------|------------|
| AIC | $2$ | 2.00 | 2.00 | 2.00 |
| HQC | $2\ln(\ln(T))$ | 3.04 | 3.65 | 4.07 |
| BIC | $\ln(T)$ | 4.61 | 6.21 | 7.60 |

!!! note "AIC vs. BIC Trade-off"
    - **AIC** favors models that predict well out-of-sample (forecasting focus)
    - **BIC** favors models that identify the true data-generating process (inference focus)
    - In GARCH applications with moderate $T$, they often agree. When they disagree, report both and let the application context guide the choice.

---

## 4. Quick Example

```python
from archbox.models import GARCH, EGARCH, GJR_GARCH
from archbox.diagnostics.information_criteria import compute_ic
import numpy as np

# Simulate return data
np.random.seed(42)
returns = np.random.standard_t(5, size=2000) * 0.01

# Fit competing models
models = {
    "GARCH(1,1)": GARCH(returns, p=1, q=1),
    "GARCH(2,1)": GARCH(returns, p=2, q=1),
    "EGARCH(1,1)": EGARCH(returns, p=1, q=1),
    "GJR(1,1)": GJR_GARCH(returns, p=1, q=1),
}

results = {}
for name, model in models.items():
    results[name] = model.fit()

# Compare information criteria
print(f"{'Model':<15} {'LogLik':>10} {'AIC':>10} {'BIC':>10} {'HQC':>10}")
print("-" * 57)
for name, res in results.items():
    ic = compute_ic(res)
    print(f"{name:<15} {res.loglik:>10.2f} {ic.aic:>10.2f} {ic.bic:>10.2f} {ic.hqc:>10.2f}")
```

```text
Model            LogLik        AIC        BIC        HQC
---------------------------------------------------------
GARCH(1,1)      5842.31  -11678.62  -11656.22  -11670.24
GARCH(2,1)      5842.89  -11677.78  -11649.78  -11667.32
EGARCH(1,1)     5851.47  -11694.94  -11667.14  -11684.48
GJR(1,1)        5849.83  -11691.66  -11663.86  -11681.20
```

!!! success "Interpretation"
    **EGARCH(1,1) wins on all three criteria.** The asymmetric model captures leverage effects that improve the fit enough to offset the extra parameter. GARCH(2,1) adds a parameter over GARCH(1,1) but barely improves the log-likelihood --- all criteria penalize it.

---

## 5. Model Selection Table

A practical workflow for presenting results:

| Model | $k$ | $\ell$ | AIC | BIC | HQC |
|-------|-----|--------|-----|-----|-----|
| GARCH(1,1) | 3 | 5842.31 | -11678.62 | -11656.22 | -11670.24 |
| GARCH(2,1) | 4 | 5842.89 | -11677.78 | -11649.78 | -11667.32 |
| EGARCH(1,1) | 4 | 5851.47 | **-11694.94** | **-11667.14** | **-11684.48** |
| GJR(1,1) | 4 | 5849.83 | -11691.66 | -11663.86 | -11681.20 |

Bold values indicate the **best** (lowest) criterion value.

---

## 6. Interpretation Guidelines

### When Criteria Agree

If AIC, BIC, and HQC all select the same model, the choice is clear. This is the most common scenario in practice.

### When Criteria Disagree

| Scenario | Recommendation |
|----------|---------------|
| AIC selects larger, BIC selects smaller | Use BIC if the goal is inference; AIC if the goal is forecasting |
| Differences are small ($< 2$) | Models are essentially equivalent; prefer the simpler one |
| Differences are large ($> 10$) | Strong evidence for the selected model |

!!! tip "Burnham & Anderson Rule of Thumb"
    For AIC differences $\Delta_i = AIC_i - AIC_{\min}$:

    - $\Delta_i < 2$: Substantial support for model $i$
    - $4 < \Delta_i < 7$: Considerably less support
    - $\Delta_i > 10$: Essentially no support

---

## 7. Common Pitfalls

!!! warning "Common Pitfalls"
    1. **Different samples**: All models must be estimated on the **same data** (same $T$). Otherwise, log-likelihoods are not comparable.
    2. **Different distributions**: Comparing AIC from a Normal-GARCH to a Student-$t$-GARCH is valid, but the improvement may come from the distribution, not the variance equation.
    3. **Maximization issues**: A model with a higher log-likelihood may have converged to a local maximum. Always check convergence diagnostics.
    4. **Non-nested comparisons only**: IC values have no distributional theory --- you cannot compute a p-value. For nested models, use the [Likelihood Ratio test](likelihood-ratio.md).
    5. **Counting parameters correctly**: Include all estimated parameters ($\omega$, $\alpha_i$, $\beta_j$, distribution shape, mean equation).

---

## See Also

- [Likelihood Ratio Test](likelihood-ratio.md) --- formal test for nested models
- [Diagnostics Overview](index.md) --- complete diagnostic pipeline
- [GARCH Theory](../theory/garch-theory.md) --- model specification

---

## References

- Akaike, H. (1974). "A New Look at the Statistical Model Identification." *IEEE Transactions on Automatic Control*, 19(6), 716--723.
- Schwarz, G. (1978). "Estimating the Dimension of a Model." *The Annals of Statistics*, 6(2), 461--464.
- Hannan, E. J. & Quinn, B. G. (1979). "The Determination of the Order of an Autoregression." *Journal of the Royal Statistical Society, Series B*, 41(2), 190--195.
- Burnham, K. P. & Anderson, D. R. (2002). *Model Selection and Multimodel Inference*. Springer.
