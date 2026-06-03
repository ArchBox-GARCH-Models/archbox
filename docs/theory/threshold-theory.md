---
title: "Threshold & STAR Theory"
description: "Mathematical foundations of threshold autoregressive (TAR) and smooth transition autoregressive (STAR) models: transition functions, linearity tests, NLS estimation, and diagnostics"
---

# Threshold and STAR Models --- Theoretical Foundations

!!! abstract "Key Takeaway"
    Threshold and Smooth Transition Autoregressive models capture **regime-dependent dynamics** driven by an observable transition variable. Unlike Markov-switching models where regimes are latent, threshold models define regimes explicitly via the level of a variable crossing a threshold. TAR models feature **abrupt** switches; STAR models feature **gradual** transitions governed by a logistic or exponential function. This page provides complete derivations of the models, linearity tests, and estimation theory.

---

## Threshold Autoregressive Models (TAR)

### General Formulation

The Threshold Autoregressive model with $K$ regimes, TAR($K$, $p$), introduced by Tong (1978, 1983), is:

$$
y_t = \phi_0^{(j)} + \sum_{i=1}^{p} \phi_i^{(j)} y_{t-i} + \sigma^{(j)} \varepsilon_t, \qquad \text{if } c_{j-1} < q_t \leq c_j
$$

where:

- $q_t$ is the **transition variable** (typically a lag of $y_t$, i.e., $q_t = y_{t-d}$ for delay $d$)
- $c_0 = -\infty < c_1 < c_2 < \cdots < c_{K-1} < c_K = +\infty$ are the **threshold values**
- $\phi^{(j)} = (\phi_0^{(j)}, \phi_1^{(j)}, \ldots, \phi_p^{(j)})'$ are regime-$j$ AR coefficients
- $\sigma^{(j)} > 0$ is the regime-$j$ error standard deviation
- $\varepsilon_t \overset{\text{iid}}{\sim} (0, 1)$

### Self-Exciting TAR (SETAR)

When $q_t = y_{t-d}$ for some delay $d \geq 1$, the model is called **Self-Exciting TAR** (SETAR). The two-regime SETAR($2$, $p$) is:

$$
y_t = \begin{cases}
\phi_0^{(1)} + \sum_{i=1}^{p} \phi_i^{(1)} y_{t-i} + \sigma^{(1)} \varepsilon_t & \text{if } y_{t-d} \leq c \\[6pt]
\phi_0^{(2)} + \sum_{i=1}^{p} \phi_i^{(2)} y_{t-i} + \sigma^{(2)} \varepsilon_t & \text{if } y_{t-d} > c
\end{cases}
$$

!!! info "Compact Notation"
    Using the indicator function $I(\cdot)$:

    $$
    y_t = (\phi_0^{(1)} + \phi_1^{(1)} y_{t-1} + \cdots)(1 - I_t) + (\phi_0^{(2)} + \phi_1^{(2)} y_{t-1} + \cdots)I_t + \varepsilon_t
    $$

    where $I_t = \mathbb{1}(y_{t-d} > c)$.

### Estimation: Grid Search + Conditional OLS

The threshold parameter $c$ enters non-linearly and non-smoothly (via the indicator function), so gradient-based optimization is not applicable. The standard approach is **concentrated least squares**:

**Step 1.** Define a grid of candidate thresholds $\mathcal{C} = \{c^{(1)}, c^{(2)}, \ldots, c^{(M)}\}$ from the observed values of $q_t$, typically using the $[\pi_0, 1-\pi_0]$ quantile range (e.g., $\pi_0 = 0.15$) to ensure sufficient observations in each regime.

**Step 2.** For each $c^{(m)} \in \mathcal{C}$, partition the sample and estimate regime-specific AR coefficients by OLS:

$$
\hat{\phi}^{(j)}(c^{(m)}) = \left(X_j' X_j\right)^{-1} X_j' Y_j, \qquad j = 1, 2
$$

where $X_j$ and $Y_j$ contain the observations assigned to regime $j$ given threshold $c^{(m)}$.

**Step 3.** Compute the concentrated sum of squared residuals:

$$
S(c^{(m)}) = \sum_{j=1}^{K} \sum_{t \in \mathcal{T}_j(c^{(m)})} \left(y_t - X_t' \hat{\phi}^{(j)}(c^{(m)})\right)^2
$$

**Step 4.** Select the threshold that minimizes the concentrated SSR:

$$
\hat{c} = \arg\min_{c^{(m)} \in \mathcal{C}} S(c^{(m)})
$$

The final coefficient estimates are $\hat{\phi}^{(j)} = \hat{\phi}^{(j)}(\hat{c})$.

### Inference on the Threshold: Hansen (2000)

Hansen (2000) showed that the least squares estimator $\hat{c}$ is **super-consistent** (converges at rate $T$) under appropriate conditions.

**Confidence intervals** for $c$ are constructed by inverting the likelihood ratio statistic:

$$
LR_T(c) = T \frac{S(c) - S(\hat{c})}{S(\hat{c})}
$$

The $(1-\alpha)$ confidence region is:

$$
\Gamma_{1-\alpha} = \{c : LR_T(c) \leq \text{critical value}\}
$$

!!! note "Non-standard Distribution"
    The asymptotic distribution of $LR_T(c_0)$ where $c_0$ is the true threshold is not $\chi^2$. Hansen (2000) provides tabulated critical values. For $\alpha = 0.05$, the critical value is 7.35.

---

## Smooth Transition Functions

### The STAR Model

The Smooth Transition Autoregressive model (Granger and Terasvirta, 1993; Terasvirta, 1994) replaces the abrupt regime switch of the TAR with a **smooth transition function** $G(q_t; \gamma, c)$:

$$
y_t = \phi_0^{(1)} + \sum_{i=1}^{p} \phi_i^{(1)} y_{t-i} + \left(\phi_0^{(2)} + \sum_{i=1}^{p} \phi_i^{(2)} y_{t-i}\right) G(q_t; \gamma, c) + \varepsilon_t
$$

Or more compactly:

$$
y_t = X_t' \phi^{(1)} + X_t' \phi^{(2)} G(q_t; \gamma, c) + \varepsilon_t
$$

where $X_t = (1, y_{t-1}, \ldots, y_{t-p})'$, $q_t = y_{t-d}$, $G(\cdot) \in [0, 1]$, and $\varepsilon_t \sim \text{iid}(0, \sigma^2)$.

**Interpretation:** At any time $t$, the model is a **weighted average** of two linear AR models. The weight $G(q_t; \gamma, c) \in [0,1]$ varies smoothly with the transition variable $q_t$:

- When $G = 0$: pure regime 1 with parameters $\phi^{(1)}$
- When $G = 1$: pure regime 2 with parameters $\phi^{(1)} + \phi^{(2)}$
- For intermediate values: a blend of both regimes

### Logistic STAR (LSTAR)

The **logistic** transition function is:

$$
G(q_t; \gamma, c) = \frac{1}{1 + \exp\left(-\gamma(q_t - c)\right)}, \qquad \gamma > 0
$$

**Properties:**

- **Monotonically increasing** in $q_t$: transitions from regime 1 (low $q_t$) to regime 2 (high $q_t$)
- **Location parameter** $c$: the midpoint of the transition ($G = 0.5$ when $q_t = c$)
- **Speed parameter** $\gamma$: controls how fast the transition occurs

**Limiting behavior:**

$$
\lim_{\gamma \to \infty} G(q_t; \gamma, c) = \begin{cases} 0 & \text{if } q_t < c \\ 0.5 & \text{if } q_t = c \\ 1 & \text{if } q_t > c \end{cases}
= \mathbb{1}(q_t > c)
$$

$$
\lim_{\gamma \to 0} G(q_t; \gamma, c) = 0.5
$$

!!! info "LSTAR $\to$ TAR"
    As $\gamma \to \infty$, the logistic function becomes a step function and the LSTAR model converges to a TAR model. As $\gamma \to 0$, the model collapses to a **linear AR** with coefficients $\phi^{(1)} + 0.5 \cdot \phi^{(2)}$.

### Exponential STAR (ESTAR)

The **exponential** transition function is:

$$
G(q_t; \gamma, c) = 1 - \exp\left(-\gamma(q_t - c)^2\right), \qquad \gamma > 0
$$

**Properties:**

- **Symmetric** around $c$: large deviations from $c$ in either direction push $G$ toward 1
- $G(c; \gamma, c) = 0$: at $q_t = c$, the model is in pure regime 1
- As $|q_t - c| \to \infty$: $G \to 1$, the model approaches regime 2
- **U-shaped response**: small and large values of $q_t$ induce different dynamics than moderate values

**Limiting behavior:**

$$
\lim_{\gamma \to \infty} G(q_t; \gamma, c) = \begin{cases} 0 & \text{if } q_t = c \\ 1 & \text{if } q_t \neq c \end{cases}
$$

$$
\lim_{\gamma \to 0} G(q_t; \gamma, c) = 0
$$

!!! tip "Economic Interpretation"
    The ESTAR model naturally captures **mean-reverting behavior**: deviations from an equilibrium level $c$ trigger different dynamics. This is widely used for real exchange rate models (purchasing power parity), where large deviations from PPP trigger arbitrage.

### Comparison of Transition Functions

| Feature | LSTAR | ESTAR |
|:--------|:------|:------|
| Symmetry | Asymmetric (monotonic) | Symmetric (U-shaped) |
| $G$ at $q_t = c$ | 0.5 | 0 |
| $G$ as $q_t \to +\infty$ | 1 | 1 |
| $G$ as $q_t \to -\infty$ | 0 | 1 |
| $\gamma \to \infty$ limit | TAR (step function) | 0 everywhere except $q_t = c$ |
| Typical application | Business cycle asymmetry | Mean reversion, PPP |

---

## Linearity Tests

Before estimating a nonlinear model, we should test whether the data actually exhibit threshold-type nonlinearity. Several tests are available.

### Luukkonen, Saikkonen, and Terasvirta (1988) LM Test

#### The Identification Problem in Direct Testing

A direct test of $H_0: \gamma = 0$ (linearity) in the STAR model faces the same identification issue as Markov-switching models: under $H_0$, the parameters $c$ and $\phi^{(2)}$ are not identified. Luukkonen et al. (1988) circumvented this by replacing $G(q_t; \gamma, c)$ with a **Taylor approximation** around $\gamma = 0$.

#### Derivation

For the LSTAR model, the third-order Taylor expansion of $G(q_t; \gamma, c)$ around $\gamma = 0$ gives:

$$
G(q_t; \gamma, c) \approx \frac{1}{2} + \frac{\gamma}{4}(q_t - c) - \frac{\gamma^3}{48}(q_t - c)^3 + O(\gamma^5)
$$

Substituting into the STAR model and collecting terms:

$$
y_t = \beta_0' X_t + \beta_1' X_t q_t + \beta_2' X_t q_t^2 + \beta_3' X_t q_t^3 + u_t
$$

The null hypothesis of linearity becomes:

$$
H_0: \beta_1 = \beta_2 = \beta_3 = 0
$$

which is testable with a standard **LM (Lagrange Multiplier)** test.

#### Test Procedure

1. Estimate the linear AR($p$) model: $y_t = \phi_0 + \sum_{i=1}^{p} \phi_i y_{t-i} + u_t$
2. Regress residuals $\hat{u}_t$ on $X_t$, $X_t q_t$, $X_t q_t^2$, $X_t q_t^3$
3. Compute $LM = T \cdot R^2$ from this auxiliary regression

Under $H_0$:

$$
LM \overset{d}{\to} \chi^2(3(p+1))
$$

An $F$-version with better finite-sample properties is also available.

!!! warning "Power Considerations"
    The Taylor expansion approach introduces regressors that may be nearly collinear (powers of $q_t$), reducing power in small samples. Dropping the $q_t^2$ term (which contributes weakly) can improve power.

### Choosing Between LSTAR and ESTAR

Terasvirta (1994) proposed a **sequential testing** procedure based on the auxiliary regression:

$$
y_t = \beta_0' X_t + \beta_1' X_t q_t + \beta_2' X_t q_t^2 + \beta_3' X_t q_t^3 + u_t
$$

Test the following sequence:

1. $H_{04}: \beta_3 = 0$ (given $\beta_1 = \beta_2 = 0$)
2. $H_{03}: \beta_2 = 0 \mid \beta_3 = 0$
3. $H_{02}: \beta_1 = 0 \mid \beta_2 = \beta_3 = 0$

**Decision rule:**

- If $H_{03}$ has the **strongest rejection** (smallest p-value): choose **ESTAR**
- Otherwise: choose **LSTAR**

!!! info "Intuition"
    The even-powered term $q_t^2$ appears in the Taylor expansion of the **exponential** function (which is symmetric), while odd-powered terms $q_t$ and $q_t^3$ appear in the **logistic** expansion (which is asymmetric). Strong evidence against $H_{03}$ (the $q_t^2$ term) points to ESTAR.

### Tsay's (1989) F-Test

Tsay (1989) proposed a test for threshold nonlinearity based on **arranged autoregression**.

**Procedure:**

1. Sort observations by the transition variable $q_t = y_{t-d}$
2. Fit recursive least squares, starting from the first $k_0$ observations
3. Compute the **predictive residuals** $\tilde{e}_t$ from the recursive regressions
4. Regress $\tilde{e}_t$ on $X_t = (1, y_{t-1}, \ldots, y_{t-p})'$
5. Use the $F$-statistic from this regression

Under linearity:

$$
F = \frac{(\text{SSR}_0 - \text{SSR}_1) / (p+1)}{\text{SSR}_1 / (T - 2p - 2)} \overset{d}{\to} F(p+1, T-2p-2)
$$

!!! tip "Advantages"
    Tsay's test does not require specifying the form of nonlinearity (logistic vs exponential). It has good power against a broad class of threshold-type alternatives.

### Hansen's (1996) Sup-LR Test

For testing $H_0$: linear AR vs $H_1$: TAR, the likelihood ratio is:

$$
LR_T(c) = T[\log S_0 - \log S(c)]
$$

where $S_0$ is the SSR under linearity and $S(c)$ is the concentrated SSR given threshold $c$.

Since $c$ is not identified under $H_0$, the sup-LR statistic is:

$$
\text{sup-}LR_T = \sup_{c \in \mathcal{C}} LR_T(c)
$$

**Bootstrap procedure for p-values:**

1. Estimate the linear AR model under $H_0$, obtaining residuals $\hat{e}_t$
2. For $b = 1, \ldots, B$:
    - Generate $\{y_t^{*b}\}$ from the estimated $H_0$ model with resampled residuals $\{e_t^{*b}\}$
    - Compute $\text{sup-}LR_T^{*b}$ for the bootstrap sample
3. The bootstrap p-value is $\hat{p} = \frac{1}{B} \sum_{b=1}^{B} \mathbb{1}(\text{sup-}LR_T^{*b} \geq \text{sup-}LR_T)$

Hansen (1996) showed that this **fixed-regressor bootstrap** provides asymptotically valid inference even under the non-standard null distribution.

---

## Estimation of STAR Models

### Nonlinear Least Squares (NLS)

Given the STAR model:

$$
y_t = X_t' \phi^{(1)} + X_t' \phi^{(2)} G(q_t; \gamma, c) + \varepsilon_t
$$

the NLS estimator minimizes:

$$
Q(\theta) = \sum_{t=1}^{T} \left(y_t - X_t' \phi^{(1)} - X_t' \phi^{(2)} G(q_t; \gamma, c)\right)^2
$$

where $\theta = (\phi^{(1)\prime}, \phi^{(2)\prime}, \gamma, c)'$.

### Concentrated NLS via Grid Search

The parameters $\gamma$ and $c$ enter nonlinearly, while $\phi^{(1)}$ and $\phi^{(2)}$ enter linearly (given $\gamma$ and $c$). This suggests a **concentrated** estimation strategy.

**Step 1: Grid over $(\gamma, c)$.** Define grids $\mathcal{G} = \{\gamma^{(1)}, \ldots, \gamma^{(M_\gamma)}\}$ and $\mathcal{C} = \{c^{(1)}, \ldots, c^{(M_c)}\}$.

**Step 2: Conditional OLS.** For each pair $(\gamma^{(m)}, c^{(l)})$, compute $G_t^{(m,l)} = G(q_t; \gamma^{(m)}, c^{(l)})$ and run OLS on:

$$
y_t = X_t' \phi^{(1)} + (X_t G_t^{(m,l)})' \phi^{(2)} + \varepsilon_t
$$

This is a linear regression with regressors $X_t$ and $X_t \cdot G_t^{(m,l)}$:

$$
\hat{\phi}(\gamma^{(m)}, c^{(l)}) = \left(Z_t' Z_t\right)^{-1} Z_t' Y
$$

where $Z_t = (X_t', (X_t G_t^{(m,l)})')'$.

**Step 3: Select best $(\gamma, c)$.** Choose the pair minimizing:

$$
S(\gamma^{(m)}, c^{(l)}) = \sum_{t=1}^{T} \hat{\varepsilon}_t^2(\gamma^{(m)}, c^{(l)})
$$

**Step 4: Refine.** Use the grid-search solution as starting values for numerical NLS optimization (e.g., Gauss-Newton or Levenberg-Marquardt).

!!! tip "Scaling of $\gamma$"
    It is common to **standardize** $\gamma$ by the standard deviation of $q_t$:

    $$
    G(q_t; \gamma, c) = \frac{1}{1 + \exp(-\gamma / \hat{\sigma}_q \cdot (q_t - c))}
    $$

    This makes $\gamma$ comparable across datasets and improves numerical optimization.

### Identification Issues When $\gamma$ Is Small

When $\gamma \approx 0$, the STAR model is nearly linear, and the parameters $c$ and $\phi^{(2)}$ become **weakly identified**:

$$
G(q_t; \gamma, c) \approx \frac{1}{2} + \frac{\gamma}{4}(q_t - c) + O(\gamma^3) \approx \frac{1}{2} \quad \text{as } \gamma \to 0
$$

**Consequences:**

- The objective function $Q(\theta)$ becomes **flat** in the $(\gamma, c)$ direction
- Standard errors for $\gamma$ and $c$ become very large
- The Hessian may be nearly singular, causing optimization to fail

!!! warning "Davies' Problem Again"
    This is another manifestation of the Davies (1977) problem: when $\gamma = 0$, the parameter $c$ vanishes from the model, so we cannot test $\gamma = 0$ with standard methods. This is why the linearity tests in the previous section use Taylor expansions rather than direct tests on $\gamma$.

### Asymptotic Properties

Under regularity conditions (Terasvirta, 1994), the NLS estimator $\hat{\theta}$ is **consistent** and **asymptotically normal**:

$$
\sqrt{T}(\hat{\theta} - \theta_0) \overset{d}{\to} \mathcal{N}(0, \sigma^2 V^{-1})
$$

where:

$$
V = \lim_{T \to \infty} \frac{1}{T} \sum_{t=1}^{T} E\left[\frac{\partial m_t(\theta_0)}{\partial \theta} \frac{\partial m_t(\theta_0)}{\partial \theta'}\right]
$$

and $m_t(\theta) = X_t' \phi^{(1)} + X_t' \phi^{(2)} G(q_t; \gamma, c)$ is the conditional mean.

Standard errors are computed from the **sandwich estimator** or, under homoskedasticity, from $\hat{\sigma}^2 (\hat{V})^{-1}$ with $\hat{V} = T^{-1} \sum_t \hat{g}_t \hat{g}_t'$ where $\hat{g}_t = \partial m_t / \partial \theta |_{\hat{\theta}}$.

---

## Evaluation and Diagnostics

### Tests of No Remaining Nonlinearity

After estimating a STAR model, one should verify that the model has captured all nonlinearity. This is done by testing whether an **additional** transition function is needed.

The **additive STAR** test augments the model:

$$
y_t = X_t' \phi^{(1)} + X_t' \phi^{(2)} G_1(q_t; \hat{\gamma}_1, \hat{c}_1) + X_t' \phi^{(3)} G_2(q_t; \gamma_2, c_2) + u_t
$$

Under $H_0: \phi^{(3)} = 0$ (no additional transition), the same Taylor expansion trick applies. Use the LM test with auxiliary regression of residuals on $X_t q_t$, $X_t q_t^2$, $X_t q_t^3$.

### Parameter Constancy Test

Eitrheim and Terasvirta (1996) proposed testing whether the parameters of a STAR model are **constant over time**. Under the alternative, parameters change smoothly as a function of time:

$$
\phi^{(j)}_t = \phi^{(j)} + \psi^{(j)} G^*(t; \gamma^*, c^*)
$$

The LM test replaces $G^*$ by a Taylor expansion in $t$:

- Regress STAR residuals on $X_t t$, $X_t t^2$, $X_t t^3$
- Compute $LM = T \cdot R^2 \sim \chi^2(3(p+1))$

### ARCH in Residuals

Nonlinear mean models can induce apparent heteroskedasticity. After fitting a STAR model, test for remaining ARCH effects:

$$
\hat{u}_t^2 = \alpha_0 + \sum_{i=1}^{q} \alpha_i \hat{u}_{t-i}^2 + v_t
$$

using the standard Engle (1982) LM test. If ARCH effects remain, consider a **STAR-GARCH** model.

### Model Selection

When multiple STAR specifications are candidates, use:

- **AIC** and **BIC** for comparing non-nested models
- **Likelihood ratio tests** for nested models (e.g., LSTAR vs linear)
- **Out-of-sample forecasting** performance for practical evaluation

!!! tip "Modeling Cycle"
    Terasvirta (1994) recommended the following modeling cycle:

    1. **Specify** the linear model (lag order $p$, delay $d$)
    2. **Test** for nonlinearity (LM test)
    3. **Choose** LSTAR vs ESTAR (sequential test)
    4. **Estimate** by NLS with grid search
    5. **Evaluate** with misspecification tests
    6. If misspecification found, return to step 1

---

## Extensions

### Multiple Transition Variables

The STAR model can be extended to allow transitions driven by different variables:

$$
y_t = X_t' \phi^{(1)} + X_t' \phi^{(2)} G_1(q_{1t}; \gamma_1, c_1) + X_t' \phi^{(3)} G_2(q_{2t}; \gamma_2, c_2) + \varepsilon_t
$$

### Time-Varying STAR (TV-STAR)

Lundbergh, Terasvirta, and van Dijk (2003) introduced the TV-STAR model where parameters change smoothly over time:

$$
y_t = X_t' \phi^{(1)}(t) + X_t' \phi^{(2)}(t) G(q_t; \gamma, c) + \varepsilon_t
$$

with $\phi^{(j)}(t) = \phi^{(j)} + \psi^{(j)} G^*(t/T; \kappa, \tau)$ modeling structural change.

### STAR-GARCH

Combining threshold effects in the mean with GARCH effects in the variance:

$$
y_t = X_t' \phi^{(1)} + X_t' \phi^{(2)} G(q_t; \gamma, c) + \varepsilon_t, \qquad \varepsilon_t = \sigma_t z_t
$$

$$
\sigma_t^2 = \omega + \alpha \varepsilon_{t-1}^2 + \beta \sigma_{t-1}^2
$$

---

## References

- Davies, R.B. (1977). Hypothesis Testing When a Nuisance Parameter Is Present Only Under the Alternative. *Biometrika*, 64(2), 247--254.
- Eitrheim, O. and Terasvirta, T. (1996). Testing the Adequacy of Smooth Transition Autoregressive Models. *Journal of Econometrics*, 74(1), 59--75.
- Granger, C.W.J. and Terasvirta, T. (1993). *Modelling Non-Linear Economic Relationships*. Oxford University Press.
- Hansen, B.E. (1996). Inference When a Nuisance Parameter Is Not Identified Under the Null Hypothesis. *Econometrica*, 64(2), 413--430.
- Hansen, B.E. (2000). Sample Splitting and Threshold Estimation. *Econometrica*, 68(3), 575--603.
- Lundbergh, S., Terasvirta, T., and van Dijk, D. (2003). Time-Varying Smooth Transition Autoregressive Models. *Journal of Business & Economic Statistics*, 21(1), 104--121.
- Luukkonen, R., Saikkonen, P., and Terasvirta, T. (1988). Testing Linearity Against Smooth Transition Autoregressive Models. *Biometrika*, 75(3), 491--499.
- Terasvirta, T. (1994). Specification, Estimation, and Evaluation of Smooth Transition Autoregressive Models. *Journal of the American Statistical Association*, 89(425), 208--218.
- Tong, H. (1978). On a Threshold Model. In: *Pattern Recognition and Signal Processing* (C.H. Chen, ed.), Sijthoff & Noordhoff, 101--141.
- Tong, H. (1983). *Threshold Models in Non-linear Time Series Analysis*. Springer.
- Tsay, R.S. (1989). Testing and Modeling Threshold Autoregressive Processes. *Journal of the American Statistical Association*, 84(405), 231--240.
