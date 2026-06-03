---
title: "Risk Measures Theory"
description: "Mathematical foundations of Value-at-Risk, Expected Shortfall, coherent risk measures, backtesting methodology, and regulatory frameworks (Basel II/III, FRTB)"
---

# Risk Measures --- Theoretical Foundations

!!! abstract "Key Takeaway"
    Risk measurement in finance revolves around quantifying potential losses. **Value-at-Risk (VaR)** provides a single-number summary of downside risk but fails the subadditivity axiom, meaning diversification can appear to *increase* risk. **Expected Shortfall (ES)** remedies this by averaging over tail losses and satisfies all four axioms of **coherent risk measures** (Artzner et al., 1999). Rigorous **backtesting** procedures (Kupiec, Christoffersen, Berkowitz) are essential to validate any risk model. Modern regulation (Basel III, FRTB) has shifted from VaR to ES as the primary capital charge metric.

---

## Value-at-Risk: Formal Theory

### Definition

Let $L$ denote the loss of a portfolio over a given horizon (e.g., 1 day, 10 days). The **Value-at-Risk** at confidence level $\alpha \in (0,1)$ is the smallest loss threshold $x$ such that the probability of exceeding $x$ is at most $1 - \alpha$:

$$
\boxed{\text{VaR}_\alpha(L) = \inf\{x \in \mathbb{R} : P(L > x) \leq 1 - \alpha\} = F_L^{-1}(\alpha)}
$$

where $F_L^{-1}$ is the **generalized inverse** (quantile function) of the loss distribution.

!!! info "Sign Convention"
    Two conventions coexist in the literature. Under the **loss convention** used here, $L > 0$ represents a loss. Some authors define VaR on returns $r_t$, where $\text{VaR}_\alpha = -F_r^{-1}(1-\alpha)$. The archbox library uses the **return convention** internally: $\text{VaR}_\alpha = \mu_t + \sigma_t \cdot q_{1-\alpha}(D)$, where $q_{1-\alpha}(D)$ is the quantile of the standardized innovation distribution.

### Properties of VaR

VaR satisfies several desirable properties:

**Monotonicity.** If $L_1 \leq L_2$ almost surely, then $\text{VaR}_\alpha(L_1) \leq \text{VaR}_\alpha(L_2)$.

**Translation invariance.** For any constant $c \in \mathbb{R}$:

$$
\text{VaR}_\alpha(L + c) = \text{VaR}_\alpha(L) + c
$$

Adding a deterministic loss $c$ shifts VaR by exactly $c$.

**Positive homogeneity.** For any $\lambda > 0$:

$$
\text{VaR}_\alpha(\lambda L) = \lambda \cdot \text{VaR}_\alpha(L)
$$

Scaling a position scales risk proportionally.

### VaR is NOT Subadditive

!!! danger "Critical Limitation"
    VaR **violates subadditivity**: there exist portfolios $L_1, L_2$ such that

    $$
    \text{VaR}_\alpha(L_1 + L_2) > \text{VaR}_\alpha(L_1) + \text{VaR}_\alpha(L_2)
    $$

    This means VaR can penalize diversification --- a portfolio may appear riskier than the sum of its parts.

??? note "Counter-Example: Two Binary Default Bonds"
    Consider two independent bonds, each defaulting with probability $p = 0.04$. Loss on default is 1, otherwise 0.

    - Individual VaR at $\alpha = 0.95$: Since $P(L_i > 0) = 0.04 < 0.05$, we get $\text{VaR}_{0.95}(L_i) = 0$.
    - Portfolio loss $L = L_1 + L_2$ has $P(L > 0) = 1 - (1-p)^2 = 0.0784 > 0.05$, so $\text{VaR}_{0.95}(L) = 1$.

    Thus $\text{VaR}_{0.95}(L_1 + L_2) = 1 > 0 = \text{VaR}_{0.95}(L_1) + \text{VaR}_{0.95}(L_2)$. Diversification appears to *increase* risk under VaR.

!!! tip "When VaR is Subadditive"
    For **elliptical distributions** (Normal, Student-$t$), VaR *is* subadditive. The failure occurs primarily with discrete or highly skewed distributions.

### VaR Computation Methods

=== "Parametric (Delta-Normal)"

    Assuming $r_t | \mathcal{F}_{t-1} \sim N(\mu_t, \sigma_t^2)$:

    $$
    \text{VaR}_\alpha = -(\mu_t + \sigma_t \cdot \Phi^{-1}(1-\alpha))
    $$

    where $\Phi^{-1}$ is the standard normal quantile. Under a GARCH model, $\sigma_t$ is the conditional volatility forecast.

=== "Historical Simulation"

    Use the empirical quantile of past returns:

    $$
    \text{VaR}_\alpha = -\hat{Q}_{1-\alpha}(\{r_{t-1}, r_{t-2}, \ldots, r_{t-W}\})
    $$

    where $W$ is the rolling window size. Simple but assumes stationarity.

=== "Filtered Historical Simulation (FHS)"

    Combine GARCH with historical simulation:

    1. Fit a GARCH model to obtain standardized residuals $\hat{z}_t = \varepsilon_t / \hat{\sigma}_t$
    2. Compute the empirical quantile of the standardized residuals: $\hat{q}_{1-\alpha}$
    3. Scale by the current volatility forecast: $\text{VaR}_\alpha = -(\hat{\mu}_t + \hat{\sigma}_{t|t-1} \cdot \hat{q}_{1-\alpha})$

    This captures time-varying volatility while using the empirical distribution of shocks.

=== "Monte Carlo Simulation"

    1. Fit a parametric model (e.g., GARCH with Student-$t$ innovations)
    2. Simulate $N$ future return paths: $r_t^{(1)}, \ldots, r_t^{(N)}$
    3. Compute VaR as the empirical quantile of simulated losses

    Most flexible but computationally expensive.

---

## Expected Shortfall and Coherent Risk Measures

### Axioms of Coherence (Artzner et al., 1999)

A risk measure $\rho: \mathcal{L} \to \mathbb{R}$ mapping random losses to real numbers is **coherent** if it satisfies four axioms:

!!! note "Axiom 1: Monotonicity"
    If $L_1 \leq L_2$ almost surely, then $\rho(L_1) \leq \rho(L_2)$.

    **Interpretation:** A portfolio that always loses less should have lower risk.

!!! note "Axiom 2: Subadditivity"
    For any losses $L_1, L_2$:

    $$
    \rho(L_1 + L_2) \leq \rho(L_1) + \rho(L_2)
    $$

    **Interpretation:** Diversification should not increase risk. This is the axiom that VaR violates.

    ??? abstract "Why Subadditivity Matters"
        - **Decentralized risk management:** A firm's total risk is bounded by the sum of desk-level risks
        - **Capital allocation:** Risk capital can be meaningfully allocated to business units
        - **Regulatory consistency:** Merging two entities should not increase systemic risk capital requirements

!!! note "Axiom 3: Positive Homogeneity"
    For any $\lambda > 0$:

    $$
    \rho(\lambda L) = \lambda \cdot \rho(L)
    $$

    **Interpretation:** Doubling a position doubles the risk.

!!! note "Axiom 4: Translation Invariance"
    For any constant $c \in \mathbb{R}$:

    $$
    \rho(L + c) = \rho(L) + c
    $$

    **Interpretation:** Adding a certain loss $c$ increases risk by exactly $c$. Conversely, holding $c$ units of cash reduces risk by $c$.

### Expected Shortfall Definition

The **Expected Shortfall** (also called Conditional VaR or CVaR) at level $\alpha$ is:

$$
\boxed{\text{ES}_\alpha(L) = \frac{1}{1-\alpha} \int_\alpha^1 \text{VaR}_u(L) \, du}
$$

For continuous distributions, this simplifies to the **conditional tail expectation**:

$$
\text{ES}_\alpha(L) = E\left[L \mid L > \text{VaR}_\alpha(L)\right]
$$

!!! tip "Intuition"
    While VaR answers _"What is the minimum loss in the worst $(1-\alpha)\%$ of cases?"_, ES answers _"What is the **average** loss in the worst $(1-\alpha)\%$ of cases?"_. ES captures the entire shape of the tail, not just a single quantile.

### ES is Coherent

??? note "Proof of Subadditivity for ES"
    The key property to prove is subadditivity. We use the **dual representation** of ES:

    $$
    \text{ES}_\alpha(L) = \sup_{Q \in \mathcal{Q}_\alpha} E_Q[L]
    $$

    where $\mathcal{Q}_\alpha = \{Q \ll P : dQ/dP \leq 1/(1-\alpha)\}$ is the set of probability measures absolutely continuous with respect to $P$ with bounded Radon-Nikodym derivative.

    For any $Q \in \mathcal{Q}_\alpha$:

    $$
    E_Q[L_1 + L_2] = E_Q[L_1] + E_Q[L_2] \leq \text{ES}_\alpha(L_1) + \text{ES}_\alpha(L_2)
    $$

    Taking the supremum over $Q$ on the left side:

    $$
    \text{ES}_\alpha(L_1 + L_2) \leq \text{ES}_\alpha(L_1) + \text{ES}_\alpha(L_2) \qquad \square
    $$

    Monotonicity, positive homogeneity, and translation invariance follow directly from the integral representation.

### ES under Parametric Distributions

=== "Normal"

    If $L \sim N(\mu, \sigma^2)$:

    $$
    \text{ES}_\alpha = \mu + \sigma \cdot \frac{\phi(\Phi^{-1}(\alpha))}{1 - \alpha}
    $$

    where $\phi$ and $\Phi$ are the standard normal PDF and CDF.

=== "Student-$t$"

    If $L$ follows a location-scale Student-$t(\nu)$:

    $$
    \text{ES}_\alpha = \mu + \sigma \cdot \frac{f_\nu(t_\nu^{-1}(\alpha))}{1 - \alpha} \cdot \frac{\nu + (t_\nu^{-1}(\alpha))^2}{\nu - 1}
    $$

    where $f_\nu$ and $t_\nu^{-1}$ are the Student-$t$ PDF and quantile function with $\nu$ degrees of freedom.

=== "GARCH-filtered"

    For a GARCH model with conditional distribution $D$:

    $$
    \text{ES}_\alpha = -\left(\hat{\mu}_t + \hat{\sigma}_{t|t-1} \cdot \text{ES}_\alpha^{D}(z)\right)
    $$

    where $\text{ES}_\alpha^{D}(z)$ is the ES of the standardized innovation distribution.

### VaR vs ES: Comparison

| Property | VaR | ES |
|:---------|:----|:---|
| Monotonicity | :material-check: Yes | :material-check: Yes |
| Translation invariance | :material-check: Yes | :material-check: Yes |
| Positive homogeneity | :material-check: Yes | :material-check: Yes |
| **Subadditivity** | :material-close: **No** | :material-check: **Yes** |
| **Coherent** | :material-close: **No** | :material-check: **Yes** |
| Elicitability | :material-check: Yes | :material-close: No (jointly with VaR: yes) |
| Regulatory standard | Basel II | Basel III / FRTB |

!!! warning "Elicitability Trade-off"
    VaR is **elicitable** (there exists a scoring function for which VaR is the optimal point forecast), making backtesting straightforward. ES is **not elicitable** on its own (Gneiting, 2011), though the pair (VaR, ES) is jointly elicitable (Fissler & Ziegel, 2016). This complicates direct backtesting of ES.

---

## Backtesting: Statistical Foundations

Backtesting assesses whether a risk model's forecasts are consistent with observed losses. Define the **hit sequence** (violation indicator):

$$
I_t = \mathbb{1}\{L_t > \text{VaR}_{\alpha,t}\}
$$

Under a correctly specified model, $I_t$ should be an i.i.d. Bernoulli sequence with $E[I_t] = 1 - \alpha$.

### Kupiec Test --- Unconditional Coverage (1995)

The **POF (Proportion of Failures)** test checks whether the observed violation rate $\hat{p} = n/T$ matches the expected rate $1 - \alpha$.

**Hypotheses:**

$$
H_0: p = 1 - \alpha \qquad H_1: p \neq 1 - \alpha
$$

**Likelihood ratio statistic:**

$$
\boxed{LR_{uc} = -2 \log \frac{(1-\alpha)^{T-n} \alpha^n}{\hat{p}^n (1-\hat{p})^{T-n}} \overset{d}{\to} \chi^2(1)}
$$

where $n = \sum_{t=1}^{T} I_t$ is the number of violations and $T$ is the sample size.

??? note "Derivation"
    Under $H_0$, each $I_t \sim \text{Bernoulli}(1-\alpha)$ independently. The log-likelihood is:

    $$
    \ell(p) = n \log p + (T-n) \log(1-p)
    $$

    The MLE is $\hat{p} = n/T$. The LR statistic compares the restricted ($p = 1-\alpha$) and unrestricted models:

    $$
    LR_{uc} = 2[\ell(\hat{p}) - \ell(1-\alpha)]
    $$

    By Wilks' theorem, $LR_{uc} \overset{d}{\to} \chi^2(1)$ under $H_0$.

!!! warning "Low Power"
    The Kupiec test has low power in typical sample sizes ($T = 250$ trading days). At 99% VaR, we expect only $\approx 2.5$ violations per year, making it difficult to distinguish a good model from a bad one.

### Christoffersen Test --- Conditional Coverage (1998)

The Kupiec test only checks the **level** of violations, not their **timing**. Christoffersen (1998) proposes a joint test of:

1. **Unconditional coverage:** $E[I_t] = 1 - \alpha$
2. **Independence:** $I_t$ is serially independent

**Independence test.** Model $I_t$ as a first-order Markov chain with transition probabilities:

$$
\pi_{ij} = P(I_t = j \mid I_{t-1} = i), \qquad i,j \in \{0,1\}
$$

Under $H_0$ (independence): $\pi_{01} = \pi_{11} = \pi$.

**Likelihood ratio for independence:**

$$
LR_{ind} = -2 \log \frac{(1-\hat{\pi})^{n_{00}+n_{10}} \hat{\pi}^{n_{01}+n_{11}}}{(1-\hat{\pi}_{01})^{n_{00}} \hat{\pi}_{01}^{n_{01}} (1-\hat{\pi}_{11})^{n_{10}} \hat{\pi}_{11}^{n_{11}}} \overset{d}{\to} \chi^2(1)
$$

where $n_{ij}$ counts transitions from state $i$ to state $j$, $\hat{\pi}_{ij} = n_{ij}/(n_{i0} + n_{i1})$, and $\hat{\pi} = (n_{01}+n_{11})/T$.

**Joint conditional coverage test:**

$$
\boxed{LR_{cc} = LR_{uc} + LR_{ind} \overset{d}{\to} \chi^2(2)}
$$

!!! tip "Interpreting Violation Clustering"
    If VaR violations cluster (i.e., $\hat{\pi}_{11} > \hat{\pi}_{01}$), the model underestimates risk persistence --- a violation today predicts another tomorrow. This often indicates **misspecified volatility dynamics** (e.g., using constant variance instead of GARCH).

### Berkowitz Test --- Density Forecast (2001)

Rather than testing a single quantile (VaR), the **Berkowitz test** evaluates the entire forecast density using the **Probability Integral Transform (PIT)**:

$$
u_t = F_{t|t-1}(r_t)
$$

where $F_{t|t-1}$ is the forecast CDF. Under a correctly specified model:

$$
u_t \overset{\text{iid}}{\sim} U(0,1)
$$

Applying the inverse normal CDF: $z_t = \Phi^{-1}(u_t) \overset{\text{iid}}{\sim} N(0,1)$.

**Test procedure.** Fit an $\text{AR}(1)$ model to $\{z_t\}$:

$$
z_t = \mu + \rho \cdot z_{t-1} + \sigma \varepsilon_t
$$

**Hypotheses:** $H_0: \mu = 0, \rho = 0, \sigma = 1$ (i.e., $z_t \overset{\text{iid}}{\sim} N(0,1)$).

$$
LR_{\text{Berk}} = -2[\ell_0 - \ell_1] \overset{d}{\to} \chi^2(3)
$$

!!! info "Advantage of Berkowitz"
    The Berkowitz test evaluates the **entire distribution**, not just a single quantile. This provides greater power and detects misspecification in both tails, the center, and the dynamics of the forecast density.

### Engle & Manganelli --- Dynamic Quantile (DQ) Test (2004)

The **DQ test** extends the Christoffersen framework by regressing the centered hit variable $\text{Hit}_t = I_t - (1-\alpha)$ on lagged hits and VaR forecasts:

$$
\text{Hit}_t = \delta_0 + \sum_{k=1}^{K} \delta_k \text{Hit}_{t-k} + \delta_{K+1} \text{VaR}_t + u_t
$$

Under a correctly specified model, all coefficients should be zero:

$$
H_0: \delta_0 = \delta_1 = \cdots = \delta_{K+1} = 0
$$

The test statistic is a standard Wald test:

$$
DQ = \frac{\hat{\boldsymbol{\delta}}' \mathbf{X}' \mathbf{X} \hat{\boldsymbol{\delta}}}{\alpha(1-\alpha)} \overset{d}{\to} \chi^2(K+2)
$$

!!! tip "CAViaR Connection"
    The DQ test arises naturally from the **Conditional Autoregressive VaR (CAViaR)** framework of Engle & Manganelli (2004), where VaR is modeled directly as an autoregressive process rather than derived from a volatility model.

### Summary of Backtesting Methods

| Test | Null Hypothesis | Statistic | df | Tests |
|:-----|:----------------|:----------|:---|:------|
| Kupiec (1995) | $E[I_t] = 1-\alpha$ | $LR_{uc}$ | 1 | Unconditional coverage |
| Christoffersen (1998) | $E[I_t] = 1-\alpha$ + independence | $LR_{cc}$ | 2 | Coverage + independence |
| Berkowitz (2001) | $z_t \overset{\text{iid}}{\sim} N(0,1)$ | $LR_{\text{Berk}}$ | 3 | Full density |
| DQ (2004) | No predictability in hits | $DQ$ | $K+2$ | Dynamic quantile |

---

## Regulatory Framework

### Basel II (2004)

The Basel II framework established VaR as the primary market risk capital charge:

$$
\boxed{C_{\text{Basel II}} = \max\left\{\text{VaR}_{99\%,10d,t}, \; k \cdot \frac{1}{60} \sum_{i=1}^{60} \text{VaR}_{99\%,10d,t-i}\right\} + \text{SRC}}
$$

**Key parameters:**

- **Confidence level:** 99% (one-tailed)
- **Horizon:** 10 business days (two weeks)
- **Multiplier $k$:** Minimum 3, increased based on backtesting performance
- **SRC:** Specific risk charge

**Scaling rule.** The 10-day VaR is typically obtained by scaling the 1-day VaR:

$$
\text{VaR}_{10d} = \sqrt{10} \cdot \text{VaR}_{1d}
$$

!!! warning "Square-Root-of-Time Rule"
    The $\sqrt{10}$ scaling assumes i.i.d. returns, which is violated under GARCH dynamics. For GARCH(1,1) with high persistence ($\alpha + \beta \approx 1$), multi-step forecasts should use the proper recursive formula:

    $$
    E_t[\sigma_{t+h}^2] = \bar{\sigma}^2 + (\alpha + \beta)^{h-1}(\sigma_{t+1}^2 - \bar{\sigma}^2)
    $$

### Basel Traffic Light System

The backtesting framework uses a **traffic light** approach based on 250-day windows at 99% confidence:

| Zone | Violations | Multiplier $k$ | Interpretation |
|:-----|:-----------|:---------------|:---------------|
| :material-circle:{ .green } Green | 0--4 | 3.00 | Model accepted |
| :material-circle:{ .yellow } Yellow | 5 | 3.40 | Scrutiny required |
| :material-circle:{ .yellow } Yellow | 6 | 3.50 | |
| :material-circle:{ .yellow } Yellow | 7 | 3.65 | |
| :material-circle:{ .yellow } Yellow | 8 | 3.75 | |
| :material-circle:{ .yellow } Yellow | 9 | 3.85 | |
| :material-circle:{ .red } Red | 10+ | 4.00 | Model rejected |

### Basel III and the Shift to Expected Shortfall (2016)

Basel III replaced VaR with **Expected Shortfall** as the primary risk metric:

$$
\boxed{C_{\text{Basel III}} = \max\left\{\text{ES}_{97.5\%,t}, \; k \cdot \frac{1}{60} \sum_{i=1}^{60} \text{ES}_{97.5\%,t-i}\right\}}
$$

**Key changes from Basel II:**

| Aspect | Basel II | Basel III |
|:-------|:---------|:----------|
| Risk measure | VaR (99%) | ES (97.5%) |
| Horizon | 10 days uniform | Liquidity-adjusted (10--120 days) |
| Stress period | No | Yes (stressed ES) |
| Calibration | Current market | Stressed + current blend |
| Coherence | Not coherent | Coherent |

!!! info "Why 97.5% for ES?"
    Under normality, $\text{ES}_{97.5\%} \approx \text{VaR}_{99\%}$, ensuring approximate continuity with Basel II capital levels while adopting a coherent risk measure.

### FRTB --- Fundamental Review of the Trading Book (2019)

The **FRTB** represents the most comprehensive reform of market risk regulation:

**Internal Models Approach (IMA):**

- ES at 97.5% confidence, computed for each risk factor
- **Liquidity horizons:** 10, 20, 40, 60, 120 days depending on asset class
- **Stressed ES** calibrated to a 12-month stress period
- Capital formula incorporates both current and stressed ES:

$$
\text{IMCC} = \max\left\{\text{ES}_{t}^{RS}, \; \text{ES}_{t}^{RC}\right\} + \max\left\{\text{ES}_{t}^{RS,\text{stress}}, \; \text{ES}_{t}^{RC,\text{stress}}\right\}
$$

where $RS$ and $RC$ denote reduced and complete risk factor sets.

**P&L Attribution Test (PLAT):**

- Validates that the risk model's theoretical P&L matches actual trading desk P&L
- Desks failing PLAT fall back to the **Standardized Approach (SA)**

**Non-Modellable Risk Factors (NMRF):**

- Risk factors with insufficient observable data receive a stressed capital add-on
- Computed using stress scenarios rather than ES

!!! tip "Impact on GARCH Modeling"
    FRTB incentivizes sophisticated volatility models: GARCH with fat-tailed innovations naturally captures tail risk better than simple historical simulation, potentially reducing capital requirements under IMA. The archbox library's GARCH + Student-$t$ + ES pipeline is directly relevant to FRTB compliance.

---

## Multi-Period Risk Measures

### Scaling VaR over Horizons

For $h$-period VaR, three approaches exist:

**1. Direct estimation.** Fit a model to $h$-period returns directly. Accurate but wastes information.

**2. Square-root-of-time rule.** Assuming i.i.d. returns:

$$
\text{VaR}_{h} = \sqrt{h} \cdot \text{VaR}_1
$$

**3. GARCH multi-step forecasting.** For GARCH(1,1):

$$
E_t\left[\sum_{s=1}^{h} \sigma_{t+s}^2\right] = h \bar{\sigma}^2 + \frac{1 - (\alpha+\beta)^h}{1 - (\alpha+\beta)}(\sigma_{t+1}^2 - \bar{\sigma}^2)
$$

!!! warning "Scaling Bias"
    The square-root rule **underestimates** multi-period risk when volatility is persistent ($\alpha + \beta$ close to 1) and **overestimates** it when volatility mean-reverts quickly. GARCH-based multi-step forecasts are preferred for horizons beyond 1 day.

### ES Scaling

Expected Shortfall at horizon $h$ follows analogous logic. Under the FRTB's **liquidity-adjusted ES**:

$$
\text{ES}_{\text{adj}} = \sqrt{\text{ES}_{10d}^2 + \sum_{j} \left(\text{ES}_{LH_j}^{(j)}\right)^2 \cdot \frac{LH_j - LH_{j-1}}{LH_j}}
$$

where $LH_j$ are the liquidity horizons for each risk factor group.

---

## References

- Artzner, P., Delbaen, F., Eber, J.-M., & Heath, D. (1999). Coherent measures of risk. *Mathematical Finance*, 9(3), 203--228.
- Basel Committee on Banking Supervision (2006). *International convergence of capital measurement and capital standards: A revised framework*.
- Basel Committee on Banking Supervision (2016). *Minimum capital requirements for market risk*.
- Basel Committee on Banking Supervision (2019). *Minimum capital requirements for market risk (revised)*.
- Berkowitz, J. (2001). Testing density forecasts, with applications to risk management. *Journal of Business & Economic Statistics*, 19(4), 465--474.
- Christoffersen, P.F. (1998). Evaluating interval forecasts. *International Economic Review*, 39(4), 841--862.
- Engle, R.F., & Manganelli, S. (2004). CAViaR: Conditional autoregressive value at risk by regression quantiles. *Journal of Business & Economic Statistics*, 22(4), 367--381.
- Fissler, T., & Ziegel, J.F. (2016). Higher order elicitability and Osband's principle. *Annals of Statistics*, 44(4), 1680--1707.
- Gneiting, T. (2011). Making and evaluating point forecasts. *Journal of the American Statistical Association*, 106(494), 746--762.
- Kupiec, P.H. (1995). Techniques for verifying the accuracy of risk measurement models. *Journal of Derivatives*, 3(2), 73--84.
