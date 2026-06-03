---
title: "GARCH Theory"
description: "Mathematical foundations of ARCH/GARCH models: stylized facts, stationarity, news impact curves, maximum likelihood estimation, and volatility forecasting"
---

# GARCH Models --- Theoretical Foundations

!!! abstract "Key Takeaway"
    The GARCH family models **conditional heteroskedasticity** --- the empirical regularity that financial return volatility clusters in time. Starting from the ARCH model of Engle (1982), through the GARCH generalization of Bollerslev (1986), to asymmetric extensions (EGARCH, GJR-GARCH), these models capture the key stylized facts of financial returns: volatility clustering, fat tails, and leverage effects. This page provides complete derivations, estimation theory, and forecasting formulas.

---

## Stylized Facts of Financial Returns

Before introducing models, we review the empirical regularities that motivate them. Let $r_t$ denote the log-return of a financial asset at time $t$.

### Volatility Clustering

Large (small) price changes tend to be followed by large (small) price changes. Formally, while returns $r_t$ show little serial correlation, the squared returns $r_t^2$ and absolute returns $|r_t|$ exhibit significant positive autocorrelation that decays slowly:

$$
\text{Corr}(r_t, r_{t-k}) \approx 0, \qquad \text{Corr}(r_t^2, r_{t-k}^2) > 0 \text{ for large } k
$$

!!! info "Mandelbrot (1963)"
    _"Large changes tend to be followed by large changes --- of either sign --- and small changes tend to be followed by small changes."_ This observation predates formal ARCH modeling by two decades.

### Fat Tails (Leptokurtosis)

The unconditional distribution of returns has heavier tails than the normal distribution. The excess kurtosis is strictly positive:

$$
\kappa = \frac{E[(r_t - \mu)^4]}{(E[(r_t - \mu)^2])^2} - 3 > 0
$$

Typical daily equity returns exhibit kurtosis values between 5 and 50, far exceeding the Gaussian value of 3.

### Leverage Effect

Negative returns tend to increase future volatility more than positive returns of the same magnitude. First documented by Black (1976), this asymmetry is attributed to changes in financial leverage: a price decline raises the debt-to-equity ratio, increasing the riskiness of the firm.

$$
\text{Corr}(r_t, \sigma_{t+1}^2) < 0
$$

---

## The ARCH Model (Engle, 1982)

### Model Specification

The Autoregressive Conditional Heteroskedasticity (ARCH) model specifies a **mean equation** and a **variance equation**:

$$
r_t = \mu + \varepsilon_t, \qquad \varepsilon_t = \sigma_t z_t, \qquad z_t \overset{\text{iid}}{\sim} D(0, 1)
$$

where $D(0,1)$ is a distribution with zero mean and unit variance (typically standard normal or standardized Student-$t$).

The conditional variance follows an $\text{ARCH}(q)$ process:

$$
\sigma_t^2 = \omega + \sum_{i=1}^{q} \alpha_i \varepsilon_{t-i}^2
$$

with parameter constraints:

- $\omega > 0$ (positive baseline variance)
- $\alpha_i \geq 0$ for all $i$ (non-negativity)

### Interpretation

The ARCH model captures **volatility clustering**: a large shock $\varepsilon_{t-1}^2$ raises the conditional variance $\sigma_t^2$, making a subsequent large shock more likely. The variance is **time-varying and predictable** based on past shocks.

!!! warning "Practical Limitation"
    Pure ARCH models require high orders $q$ to capture the persistent volatility dynamics observed in practice. For daily equity returns, $q \geq 10$ is typically needed, resulting in many parameters and potential overfitting.

---

## The GARCH Model (Bollerslev, 1986)

### Model Specification

The Generalized ARCH, or $\text{GARCH}(p,q)$, model addresses the parsimony problem by adding lagged conditional variances:

$$
\sigma_t^2 = \omega + \sum_{i=1}^{q} \alpha_i \varepsilon_{t-i}^2 + \sum_{j=1}^{p} \beta_j \sigma_{t-j}^2
$$

with constraints:

- $\omega > 0$
- $\alpha_i \geq 0$, $\beta_j \geq 0$

The standard $\text{GARCH}(1,1)$ is by far the most widely used specification:

$$
\sigma_t^2 = \omega + \alpha \varepsilon_{t-1}^2 + \beta \sigma_{t-1}^2
$$

!!! tip "GARCH(1,1) Dominance"
    Hansen and Lunde (2005) compared 330 ARCH-type models on exchange rate data and found that _"nothing beats a GARCH(1,1)"_ --- higher-order and more complex specifications rarely provide significant out-of-sample forecasting gains.

### GARCH as ARMA in Squared Residuals

Define $\nu_t = \varepsilon_t^2 - \sigma_t^2$ (the variance innovation). Then:

$$
\varepsilon_t^2 = \omega + (\alpha + \beta) \varepsilon_{t-1}^2 + \nu_t - \beta \nu_{t-1}
$$

This shows that $\varepsilon_t^2$ follows an $\text{ARMA}(1,1)$ process, providing intuition for why GARCH captures long memory in squared returns more parsimoniously than pure ARCH.

---

## Stationarity Conditions

### Weak Stationarity

The $\text{GARCH}(p,q)$ process is **covariance-stationary** if and only if:

$$
\boxed{\sum_{i=1}^{q} \alpha_i + \sum_{j=1}^{p} \beta_j < 1}
$$

??? note "Derivation"
    Taking unconditional expectations of the variance equation:

    $$
    E[\sigma_t^2] = \omega + \sum_{i=1}^{q} \alpha_i E[\varepsilon_{t-i}^2] + \sum_{j=1}^{p} \beta_j E[\sigma_{t-j}^2]
    $$

    Under stationarity, $E[\varepsilon_t^2] = E[\sigma_t^2] = \bar{\sigma}^2$ for all $t$, so:

    $$
    \bar{\sigma}^2 = \omega + \left(\sum_{i=1}^{q} \alpha_i + \sum_{j=1}^{p} \beta_j\right) \bar{\sigma}^2
    $$

    Solving:

    $$
    \bar{\sigma}^2 = \frac{\omega}{1 - \sum_{i=1}^{q} \alpha_i - \sum_{j=1}^{p} \beta_j}
    $$

    This is well-defined and positive only when $\sum \alpha_i + \sum \beta_j < 1$.

### Unconditional Variance

For the stationary $\text{GARCH}(1,1)$:

$$
\bar{\sigma}^2 = E[\sigma_t^2] = \frac{\omega}{1 - \alpha - \beta}
$$

This is the **long-run** or **unconditional** variance to which the conditional variance reverts.

### Persistence

The quantity $\alpha + \beta$ measures **persistence** of volatility shocks:

| $\alpha + \beta$ | Interpretation |
|:---:|:---|
| $\approx 0$ | Shocks die out instantly |
| $0.9 - 0.99$ | Typical for daily financial data |
| $= 1$ | **IGARCH** --- integrated, shocks persist forever |
| $> 1$ | Explosive, non-stationary |

### Unconditional Kurtosis

For the $\text{GARCH}(1,1)$ with Gaussian innovations ($z_t \sim N(0,1)$), the unconditional kurtosis of $\varepsilon_t$ is:

$$
\kappa_{\varepsilon} = 3 \cdot \frac{1 - (\alpha + \beta)^2}{1 - (\alpha + \beta)^2 - 2\alpha^2}
$$

provided $1 - (\alpha + \beta)^2 - 2\alpha^2 > 0$. This shows that even with Gaussian innovations, GARCH generates **unconditional fat tails** ($\kappa_\varepsilon > 3$), explaining the observed leptokurtosis without requiring a fat-tailed innovation distribution.

---

## Asymmetric GARCH Models

The standard GARCH model imposes a **symmetric** response to positive and negative shocks. The asymmetric extensions below capture the **leverage effect**.

### EGARCH (Nelson, 1991)

The Exponential GARCH models the **log** of the conditional variance:

$$
\ln(\sigma_t^2) = \omega + \alpha\left(|z_{t-1}| - E[|z_{t-1}|]\right) + \gamma z_{t-1} + \beta \ln(\sigma_{t-1}^2)
$$

where $z_{t-1} = \varepsilon_{t-1}/\sigma_{t-1}$ is the standardized residual.

**Key properties:**

- **No positivity constraints** on parameters are needed --- the exponential guarantees $\sigma_t^2 > 0$
- The term $\gamma z_{t-1}$ captures asymmetry: $\gamma < 0$ implies negative shocks increase volatility more
- For $z_t \sim N(0,1)$: $E[|z_t|] = \sqrt{2/\pi}$

!!! note "Stationarity"
    The EGARCH(1,1) is stationary if $|\beta| < 1$. Since the model is specified in logs, there is no non-negativity constraint to enforce.

### GJR-GARCH (Glosten, Jagannathan, and Runkle, 1993)

$$
\sigma_t^2 = \omega + \left(\alpha + \gamma \mathbb{I}_{[\varepsilon_{t-1} < 0]}\right) \varepsilon_{t-1}^2 + \beta \sigma_{t-1}^2
$$

where $\mathbb{I}_{[\varepsilon_{t-1} < 0]}$ is an indicator function equal to 1 when $\varepsilon_{t-1} < 0$.

**Interpretation:**

- Positive shocks: impact = $\alpha$
- Negative shocks: impact = $\alpha + \gamma$
- Leverage effect when $\gamma > 0$

**Stationarity condition:**

$$
\alpha + \beta + \frac{\gamma}{2} < 1
$$

??? note "Derivation of GJR Stationarity"
    Taking unconditional expectations:

    $$
    E[\sigma_t^2] = \omega + \alpha E[\varepsilon_{t-1}^2] + \gamma E[\varepsilon_{t-1}^2 \cdot \mathbb{I}_{[\varepsilon_{t-1}<0]}] + \beta E[\sigma_{t-1}^2]
    $$

    Since $z_t$ is symmetric around zero with unit variance, $E[\varepsilon_t^2 \cdot \mathbb{I}_{[\varepsilon_t < 0]}] = \frac{1}{2} E[\varepsilon_t^2]$. Substituting:

    $$
    \bar{\sigma}^2 = \omega + \left(\alpha + \frac{\gamma}{2}\right) \bar{\sigma}^2 + \beta \bar{\sigma}^2
    $$

    This yields $\bar{\sigma}^2 = \omega / (1 - \alpha - \gamma/2 - \beta)$, requiring $\alpha + \gamma/2 + \beta < 1$.

### APARCH (Ding, Granger, and Engle, 1993)

The Asymmetric Power ARCH nests several models through a power parameter $\delta > 0$:

$$
\sigma_t^{\delta} = \omega + \alpha\left(|\varepsilon_{t-1}| - \gamma \varepsilon_{t-1}\right)^{\delta} + \beta \sigma_{t-1}^{\delta}
$$

where $|\gamma| < 1$ controls asymmetry and $\delta$ is estimated from the data.

!!! info "Nesting"
    - $\delta = 2, \gamma = 0$: standard GARCH
    - $\delta = 2$: GJR-GARCH (with reparametrization)
    - $\delta = 1$: Taylor/Schwert GARCH on standard deviations

---

## News Impact Curve

### Definition

The **News Impact Curve** (NIC), introduced by Engle and Ng (1993), measures the impact of past return shocks on current conditional variance. Formally, it is the mapping:

$$
\text{NIC}(\varepsilon_{t-1}) = \sigma_t^2 \big|_{\sigma_{t-1}^2 = \bar{\sigma}^2}
$$

evaluated as a function of $\varepsilon_{t-1}$, holding the lagged variance at its unconditional level.

### GARCH(1,1) --- Symmetric

$$
\text{NIC}(\varepsilon_{t-1}) = \omega + \beta \bar{\sigma}^2 + \alpha \varepsilon_{t-1}^2
$$

This is a **symmetric parabola** centered at $\varepsilon_{t-1} = 0$. Positive and negative shocks of the same magnitude have identical impact on volatility.

### EGARCH(1,1) --- Asymmetric, Exponential

$$
\text{NIC}(\varepsilon_{t-1}) = A \cdot \exp\left(\frac{\alpha |\varepsilon_{t-1}| + \gamma \varepsilon_{t-1}}{\bar{\sigma}}\right)
$$

where $A = \bar{\sigma}^{2\beta} \exp\left(\omega - \alpha\sqrt{2/\pi}\right)$.

With $\gamma < 0$, the curve is steeper for negative shocks and flatter for positive shocks, producing a pronounced **asymmetry**.

### GJR-GARCH(1,1) --- Asymmetric, Piecewise

$$
\text{NIC}(\varepsilon_{t-1}) = \begin{cases} \omega + \beta\bar{\sigma}^2 + \alpha\varepsilon_{t-1}^2 & \text{if } \varepsilon_{t-1} \geq 0 \\ \omega + \beta\bar{\sigma}^2 + (\alpha + \gamma)\varepsilon_{t-1}^2 & \text{if } \varepsilon_{t-1} < 0 \end{cases}
$$

Two parabolas joined at the origin. With $\gamma > 0$, the left branch is steeper.

### Visual Comparison

=== "Symmetric vs Asymmetric"

    ```
       sigma^2
         |          EGARCH
         |         /
         |        / GJR
         |       /./
         |      /./ GARCH
         |    ./ /
         |  ./  /
         | /   /
         |/ __/____________
         |  .    .    .    epsilon
        /|.
       / |
      /  |    (negative shocks have
     /   |     larger impact for
    /    |     EGARCH and GJR)
    ```

=== "Economic Interpretation"

    The **leverage effect** captured by asymmetric models has a clear economic rationale:

    1. **Balance sheet channel**: A stock price decline raises leverage (debt/equity), increasing default risk and hence volatility
    2. **Volatility feedback**: Higher expected volatility raises the required risk premium, depressing the stock price further
    3. **Behavioral**: Bad news generates more uncertainty and trading activity than good news of the same magnitude

---

## Maximum Likelihood Estimation

### Conditional Log-Likelihood

Given a sample $\{r_1, \ldots, r_T\}$ and assuming $z_t \sim N(0,1)$, the conditional log-likelihood is:

$$
\ell(\theta) = \sum_{t=1}^{T} \ell_t(\theta) = -\frac{T}{2}\ln(2\pi) - \frac{1}{2}\sum_{t=1}^{T}\left[\ln(\sigma_t^2(\theta)) + \frac{\varepsilon_t^2}{\sigma_t^2(\theta)}\right]
$$

where $\theta = (\mu, \omega, \alpha_1, \ldots, \alpha_q, \beta_1, \ldots, \beta_p)'$ is the parameter vector and $\varepsilon_t = r_t - \mu$.

??? note "Student-$t$ Log-Likelihood"
    For $z_t \sim t_\nu$ (standardized Student-$t$ with $\nu$ degrees of freedom):

    $$
    \ell_t(\theta, \nu) = \ln\Gamma\!\left(\frac{\nu+1}{2}\right) - \ln\Gamma\!\left(\frac{\nu}{2}\right) - \frac{1}{2}\ln\left[(\nu-2)\pi\sigma_t^2\right] - \frac{\nu+1}{2}\ln\!\left(1 + \frac{\varepsilon_t^2}{(\nu-2)\sigma_t^2}\right)
    $$

    This adds $\nu$ as an additional parameter to be estimated.

### Score and Information

The score vector for the GARCH(1,1) is:

$$
\frac{\partial \ell_t}{\partial \theta} = \frac{1}{2\sigma_t^2}\left(\frac{\varepsilon_t^2}{\sigma_t^2} - 1\right) \frac{\partial \sigma_t^2}{\partial \theta}
$$

where the variance derivatives satisfy the recursion:

$$
\frac{\partial \sigma_t^2}{\partial \omega} = 1 + \beta \frac{\partial \sigma_{t-1}^2}{\partial \omega}, \qquad
\frac{\partial \sigma_t^2}{\partial \alpha} = \varepsilon_{t-1}^2 + \beta \frac{\partial \sigma_{t-1}^2}{\partial \alpha}, \qquad
\frac{\partial \sigma_t^2}{\partial \beta} = \sigma_{t-1}^2 + \beta \frac{\partial \sigma_{t-1}^2}{\partial \beta}
$$

### Optimization Algorithms

=== "BFGS"

    The **Broyden-Fletcher-Goldfarb-Shanno** algorithm is the default for GARCH estimation. It is a quasi-Newton method that builds an approximation to the inverse Hessian using gradient information:

    $$
    \theta_{k+1} = \theta_k - \lambda_k H_k^{-1} \nabla \ell(\theta_k)
    $$

    where $H_k$ is the approximate Hessian and $\lambda_k$ is the step size from a line search.

    **Advantages:** Fast convergence near the optimum, good numerical stability.

=== "Nelder-Mead"

    A **derivative-free simplex** method useful when the likelihood surface is irregular or gradients are unreliable. Slower convergence but more robust to non-smooth regions.

    **When to use:** As a fallback when BFGS fails to converge, or for initial parameter exploration.

=== "Two-Stage Strategy"

    A practical approach used in archbox:

    1. **Stage 1:** Nelder-Mead with loose tolerance to find the right basin of attraction
    2. **Stage 2:** BFGS from the Stage 1 solution for precise convergence

### Robust Standard Errors (Bollerslev-Wooldridge)

When the distributional assumption may be misspecified, the **Quasi-Maximum Likelihood (QML)** estimator remains consistent under correct specification of the conditional mean and variance. The robust (sandwich) covariance matrix is:

$$
\boxed{\text{Var}(\hat{\theta}) = J^{-1} I J^{-1}}
$$

where:

$$
J = -\frac{1}{T}\sum_{t=1}^{T} \frac{\partial^2 \ell_t}{\partial \theta \partial \theta'} \bigg|_{\hat{\theta}} \qquad \text{(Hessian, or outer product approximation)}
$$

$$
I = \frac{1}{T}\sum_{t=1}^{T} \frac{\partial \ell_t}{\partial \theta} \frac{\partial \ell_t}{\partial \theta'} \bigg|_{\hat{\theta}} \qquad \text{(outer product of gradients, OPG)}
$$

!!! warning "When to Use Robust Standard Errors"
    If the true innovation distribution is not Gaussian, ordinary MLE standard errors (based on $J^{-1}$ alone) are **inconsistent**. The Bollerslev-Wooldridge sandwich estimator provides valid inference under distributional misspecification, at the cost of reduced efficiency. In archbox, robust standard errors are the **default**.

### Information Criteria

For model selection among competing GARCH specifications:

| Criterion | Formula | Penalty |
|:---:|:---:|:---:|
| AIC | $-2\ell(\hat{\theta}) + 2k$ | Light |
| BIC | $-2\ell(\hat{\theta}) + k\ln(T)$ | Heavy |
| HQIC | $-2\ell(\hat{\theta}) + 2k\ln(\ln(T))$ | Medium |

where $k$ is the number of estimated parameters and $T$ is the sample size.

!!! tip "Model Selection in Practice"
    BIC is **consistent** (selects the true model as $T \to \infty$) while AIC tends to overfit. For GARCH models, BIC typically selects more parsimonious specifications, which often perform better out-of-sample.

---

## Volatility Forecasting

### One-Step-Ahead Forecast

For the $\text{GARCH}(1,1)$, the one-step-ahead conditional variance forecast at time $T$ is:

$$
\hat{\sigma}_{T+1}^2 = \omega + \alpha \varepsilon_T^2 + \beta \sigma_T^2
$$

This is computed directly from the last observation and the filtered variance.

### Multi-Step-Ahead Forecast

The $h$-step-ahead forecast is obtained by iterating the conditional expectation. For the $\text{GARCH}(1,1)$:

$$
\boxed{E_T[\sigma_{T+h}^2] = \bar{\sigma}^2 + (\alpha + \beta)^{h-1}\left(\sigma_{T+1}^2 - \bar{\sigma}^2\right)}
$$

??? note "Derivation"
    Starting from:

    $$
    \sigma_{T+h}^2 = \omega + \alpha \varepsilon_{T+h-1}^2 + \beta \sigma_{T+h-1}^2
    $$

    Taking conditional expectations $E_T[\cdot] = E[\cdot | \mathcal{F}_T]$:

    $$
    E_T[\sigma_{T+h}^2] = \omega + (\alpha + \beta) E_T[\sigma_{T+h-1}^2]
    $$

    since $E_T[\varepsilon_{T+h-1}^2] = E_T[\sigma_{T+h-1}^2]$ for $h \geq 2$. This is a **first-order linear difference equation** in $E_T[\sigma_{T+h}^2]$ with solution:

    $$
    E_T[\sigma_{T+h}^2] = \bar{\sigma}^2 + (\alpha + \beta)^{h-1}(\sigma_{T+1}^2 - \bar{\sigma}^2)
    $$

    where $\bar{\sigma}^2 = \omega/(1 - \alpha - \beta)$ is the unconditional variance.

### Mean Reversion

Since $\alpha + \beta < 1$ for stationary processes:

$$
\lim_{h \to \infty} E_T[\sigma_{T+h}^2] = \bar{\sigma}^2
$$

The forecast **reverts to the unconditional variance** at a rate governed by the persistence $\alpha + \beta$. The **half-life** of a volatility shock is:

$$
h^* = \frac{\ln(0.5)}{\ln(\alpha + \beta)}
$$

For $\alpha + \beta = 0.95$, the half-life is approximately 13.5 days.

### Forecast Confidence Intervals

The forecast uncertainty around $E_T[\sigma_{T+h}^2]$ can be quantified. For the $\text{GARCH}(1,1)$ with Gaussian innovations, the variance of the $h$-step forecast error is:

$$
\text{Var}_T(\sigma_{T+h}^2) = 2\alpha^2 \sum_{i=0}^{h-2} (\alpha + \beta)^{2i} \cdot (\bar{\sigma}^2)^2 \cdot (1 + \text{higher-order terms})
$$

In practice, **simulation-based** (bootstrap or Monte Carlo) confidence intervals are preferred due to the complexity of the analytical expressions:

```python
from archbox.models import GARCH

model = GARCH(p=1, q=1)
result = model.fit(returns)

# Analytical h-step forecast
forecasts = result.forecast(horizon=10)

# Simulation-based confidence intervals
sim_forecasts = result.forecast(horizon=10, method="simulation", n_simulations=10000)
```

### IGARCH: The Unit Root Case

When $\alpha + \beta = 1$ (Integrated GARCH), the process has a unit root in variance:

$$
E_T[\sigma_{T+h}^2] = \sigma_{T+1}^2 + (h-1)\omega
$$

The forecast grows **linearly** with the horizon and never reverts to a finite long-run level. IGARCH is often observed empirically for daily returns, suggesting near-permanent volatility shocks or structural breaks.

---

## References

- Black, F. (1976). Studies of stock market volatility changes. _Proceedings of the American Statistical Association_, Business and Economic Statistics Section, 177--181.
- Bollerslev, T. (1986). Generalized autoregressive conditional heteroskedasticity. _Journal of Econometrics_, 31(3), 307--327.
- Bollerslev, T., & Wooldridge, J.M. (1992). Quasi-maximum likelihood estimation and inference in dynamic models with time-varying covariances. _Econometric Reviews_, 11(2), 143--172.
- Ding, Z., Granger, C.W.J., & Engle, R.F. (1993). A long memory property of stock market returns and a new model. _Journal of Empirical Finance_, 1(1), 83--106.
- Engle, R.F. (1982). Autoregressive conditional heteroscedasticity with estimates of the variance of United Kingdom inflation. _Econometrica_, 50(4), 987--1007.
- Engle, R.F., & Ng, V.K. (1993). Measuring and testing the impact of news on volatility. _Journal of Finance_, 48(5), 1749--1778.
- Glosten, L.R., Jagannathan, R., & Runkle, D.E. (1993). On the relation between the expected value and the volatility of the nominal excess return on stocks. _Journal of Finance_, 48(5), 1779--1801.
- Hansen, P.R., & Lunde, A. (2005). A forecast comparison of volatility models: does anything beat a GARCH(1,1)? _Journal of Applied Econometrics_, 20(7), 873--889.
- Mandelbrot, B. (1963). The variation of certain speculative prices. _Journal of Business_, 36(4), 394--419.
- Nelson, D.B. (1991). Conditional heteroskedasticity in asset returns: a new approach. _Econometrica_, 59(2), 347--370.
