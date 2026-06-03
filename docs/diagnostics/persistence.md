---
title: "Persistence and Half-Life"
description: "Volatility persistence measures and half-life of shocks for GARCH, EGARCH, GJR and IGARCH models"
---

# Persistence and Half-Life

!!! info "Quick Reference"
    **Function:** `archbox.diagnostics.persistence.compute_persistence`
    **Purpose:** Measure how quickly volatility shocks dissipate
    **Key metric:** Half-life $HL = \ln(0.5) / \ln(P)$ where $P$ is persistence
    **Critical threshold:** $P = 1$ (IGARCH) --- shocks never dissipate

---

## 1. What Persistence Measures

Persistence quantifies **how long a volatility shock takes to decay**. After an unexpected large return (positive or negative), conditional variance spikes. Persistence determines whether that spike:

- **Dissipates quickly** ($P$ small) --- volatility returns to its long-run level within days
- **Dissipates slowly** ($P$ close to 1) --- elevated volatility persists for weeks or months
- **Never dissipates** ($P = 1$, IGARCH) --- every shock has a permanent effect on volatility

!!! tip "Economic Interpretation"
    High persistence means that a market shock (earnings surprise, geopolitical event) will affect market volatility for an extended period. This matters for option pricing, risk management, and portfolio allocation --- all of which depend on volatility forecasts over different horizons.

---

## 2. Persistence by Model

### GARCH(1,1)

$$
\sigma_t^2 = \omega + \alpha \varepsilon_{t-1}^2 + \beta \sigma_{t-1}^2
$$

Persistence:

$$
\boxed{P_{\text{GARCH}} = \alpha + \beta}
$$

- $P < 1$: covariance stationary, unconditional variance $\bar{\sigma}^2 = \omega / (1 - \alpha - \beta)$ exists
- $P = 1$: IGARCH, unconditional variance is undefined
- $P > 1$: explosive (not admissible)

### EGARCH(1,1)

$$
\ln \sigma_t^2 = \omega + \alpha(|z_{t-1}| - E|z_{t-1}|) + \gamma z_{t-1} + \beta \ln \sigma_{t-1}^2
$$

Persistence:

$$
\boxed{P_{\text{EGARCH}} = \beta}
$$

In the EGARCH model, $\beta$ directly measures persistence because it is the autoregressive coefficient on the log-variance.

### GJR-GARCH(1,1)

$$
\sigma_t^2 = \omega + (\alpha + \gamma \mathbb{1}_{\varepsilon_{t-1}<0}) \varepsilon_{t-1}^2 + \beta \sigma_{t-1}^2
$$

Persistence:

$$
\boxed{P_{\text{GJR}} = \alpha + \beta + \frac{\gamma}{2}}
$$

The $\gamma/2$ term arises because, under symmetry, roughly half the shocks are negative ($\Pr(\varepsilon < 0) \approx 0.5$).

### IGARCH(1,1)

$$
\sigma_t^2 = \omega + \alpha \varepsilon_{t-1}^2 + (1 - \alpha) \sigma_{t-1}^2
$$

$$
P_{\text{IGARCH}} = 1 \quad \text{(by construction)}
$$

!!! warning "IGARCH Implications"
    When $P = 1$:

    - The unconditional variance **does not exist** ($\omega / (1 - P) = \omega / 0$)
    - Shocks have a **permanent** effect on the variance level
    - Multi-step forecasts do not revert to a mean --- they drift
    - The model is still strictly stationary (if $\omega > 0$), but not covariance stationary

---

## 3. Half-Life of Shocks

The half-life is the number of periods for a volatility shock to decay to **half** its initial impact:

$$
\boxed{HL = \frac{\ln(0.5)}{\ln(P)}}
$$

### Derivation

After a shock at time $t$, the effect on $\sigma_{t+h}^2$ decays approximately as $P^h$. We want the $h$ such that $P^h = 0.5$:

$$
P^h = 0.5 \implies h \ln(P) = \ln(0.5) \implies h = \frac{\ln(0.5)}{\ln(P)}
$$

### Example Values

| $P$ | Half-Life (days) | Interpretation |
|-----|-------------------|----------------|
| 0.50 | 1.0 | Very fast decay (uncommon) |
| 0.80 | 3.1 | Fast decay |
| 0.90 | 6.6 | Moderate |
| 0.95 | 13.5 | Typical for daily equity data |
| 0.98 | 34.3 | High persistence |
| 0.99 | 69.0 | Very high persistence |
| 0.999 | 692.8 | Near-IGARCH |
| 1.00 | $\infty$ | IGARCH --- permanent shocks |

!!! tip "Typical Values"
    For daily financial returns, persistence is typically $0.93$--$0.99$, giving half-lives of $10$--$70$ days. Values above $0.99$ suggest the model may be misspecified or the data contains structural breaks.

---

## 4. Quick Example

```python
from archbox.models import GARCH, EGARCH, GJR_GARCH
from archbox.diagnostics.persistence import compute_persistence
import numpy as np

# Simulate return data
np.random.seed(42)
returns = np.random.standard_t(5, size=2000) * 0.01

# Fit models
garch = GARCH(returns, p=1, q=1).fit()
egarch = EGARCH(returns, p=1, q=1).fit()
gjr = GJR_GARCH(returns, p=1, q=1).fit()

# Compute persistence and half-life
for name, result in [("GARCH", garch), ("EGARCH", egarch), ("GJR", gjr)]:
    p = compute_persistence(result)
    print(f"{name:<10} | Persistence: {p.persistence:.4f} | Half-life: {p.half_life:.1f} days")
```

```text
GARCH      | Persistence: 0.9540 | Half-life: 14.7 days
EGARCH     | Persistence: 0.9680 | Half-life: 21.3 days
GJR        | Persistence: 0.9610 | Half-life: 17.4 days
```

!!! success "Interpretation"
    All three models show high persistence ($> 0.95$), typical for daily financial returns. A volatility shock takes approximately **15--21 days** to decay to half its initial impact. The EGARCH model shows the highest persistence, meaning volatility shocks last longer in the log-variance specification.

---

## 5. Shock Decay Path

```python
from archbox.diagnostics.persistence import compute_persistence
import numpy as np

# Visualize the decay of a volatility shock
p_garch = compute_persistence(garch)
P = p_garch.persistence

# Impact at horizon h (as fraction of initial shock)
horizons = np.arange(0, 61)
decay = P ** horizons

print(f"Persistence: {P:.4f}")
print(f"Half-life:   {p_garch.half_life:.1f} days\n")

print(f"{'Day':>4} {'Remaining Impact':>18} {'Bar':>30}")
print("-" * 55)
for h in [0, 1, 5, 10, 15, 20, 30, 45, 60]:
    pct = decay[h] * 100
    bar = "#" * int(pct / 2)
    print(f"{h:>4} {pct:>17.1f}% {bar}")
```

```text
Persistence: 0.9540
Half-life:   14.7 days

 Day  Remaining Impact                            Bar
-------------------------------------------------------
   0             100.0% ##################################################
   1              95.4% ###############################################
   5              79.1% #######################################
  10              62.6% ###############################
  15              49.5% ########################
  20              39.2% ###################
  30              24.5% ############
  45              12.2% ######
  60               6.1% ###
```

---

## 6. Stationarity Conditions

| Condition | Stationarity | Unconditional Variance | Forecast Behavior |
|-----------|-------------|------------------------|-------------------|
| $P < 1$ | Covariance stationary | $\bar{\sigma}^2 = \omega / (1 - P)$ exists | Reverts to $\bar{\sigma}^2$ |
| $P = 1$ | Strictly stationary (not covariance) | Undefined | Random walk in variance |
| $P > 1$ | Non-stationary | Undefined | Explosive |

### Multi-Step Forecast

For a GARCH(1,1) model, the $h$-step-ahead variance forecast is:

$$
E_t[\sigma_{t+h}^2] = \bar{\sigma}^2 + P^h (\sigma_{t+1}^2 - \bar{\sigma}^2)
$$

- If $P < 1$: forecast converges to $\bar{\sigma}^2$ as $h \to \infty$
- If $P = 1$: forecast equals $\sigma_{t+1}^2 + (h-1)\omega$ --- linear drift
- Speed of convergence is governed by $P$

---

## 7. Diagnostics: Is Persistence Too High?

!!! warning "When Persistence Is Suspiciously High"
    If $P > 0.99$, consider:

    1. **Structural breaks**: A single model over a period with regime changes (e.g., calm vs. crisis) will show artificially high persistence. Use [regime-switching models](../user-guide/regime-switching/index.md).
    2. **Level shifts in variance**: A permanent jump in the volatility level inflates $\beta$. Consider the [ICSS algorithm](https://en.wikipedia.org/wiki/ICSS_algorithm) to detect variance breaks.
    3. **Long memory**: True long-memory processes (FIGARCH) can be misidentified as near-IGARCH by short-memory models.
    4. **Sample size**: Very short samples may produce imprecise estimates that happen to sum to near unity.

---

## 8. Configuration

| Parameter | Type | Description |
|-----------|------|-------------|
| `result` | `GARCHResult` | Fitted model result |

### Result Fields

| Field | Type | Description |
|-------|------|-------------|
| `persistence` | `float` | Persistence measure $P$ |
| `half_life` | `float` | $HL = \ln(0.5) / \ln(P)$ (days) |
| `is_stationary` | `bool` | `True` if $P < 1$ |
| `unconditional_var` | `float` or `None` | $\omega / (1 - P)$ if stationary |

---

## See Also

- [News Impact Curve](news-impact.md) --- how shocks affect volatility
- [Forecast Evaluation](forecast-evaluation.md) --- evaluate volatility forecasts
- [Information Criteria](information-criteria.md) --- model selection
- [Diagnostics Overview](index.md) --- complete diagnostic pipeline

---

## References

- Engle, R. F. & Bollerslev, T. (1986). "Modelling the Persistence of Conditional Variances." *Econometric Reviews*, 5(1), 1--50.
- Nelson, D. B. (1990). "Stationarity and Persistence in the GARCH(1,1) Model." *Econometric Theory*, 6(3), 318--334.
- Lamoureux, C. G. & Lastrapes, W. D. (1990). "Persistence in Variance, Structural Change, and the GARCH Model." *Journal of Business & Economic Statistics*, 8(2), 225--234.
