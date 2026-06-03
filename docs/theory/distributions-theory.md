---
title: "Conditional Distributions Theory"
description: "Mathematical foundations of conditional distributions for financial returns: Student-t, Skewed Student-t, GED, Skewed GED, maximum likelihood estimation, and distribution selection criteria"
---

# Conditional Distributions --- Theoretical Foundations

!!! abstract "Key Takeaway"
    Financial returns exhibit **fat tails** (excess kurtosis) and often **asymmetry** (skewness), making the Gaussian distribution inadequate. The archbox library implements a family of **location-scale distributions** --- Student-$t$, Skewed Student-$t$ (Hansen, 1994), GED, and Skewed GED --- that nest the Normal as a special case and capture these empirical regularities. All distributions are parameterized to have **zero mean and unit variance**, allowing seamless integration with GARCH-type volatility models. This page provides complete density functions, moment derivations, MLE theory, and distribution selection criteria.

---

## Why the Normal Distribution is Insufficient

### Empirical Evidence

Let $r_t$ denote daily log-returns. Under the Gaussian assumption, $r_t \sim N(\mu, \sigma^2)$, the standardized returns $z_t = (r_t - \mu)/\sigma$ should satisfy:

- **Kurtosis:** $\kappa = E[z_t^4] = 3$
- **Skewness:** $\gamma = E[z_t^3] = 0$

In practice, daily equity returns typically show:

- **Excess kurtosis:** $\kappa \in [5, 50]$, with values above 10 common for individual stocks
- **Negative skewness:** $\gamma \in [-1, 0]$ for equity indices

!!! danger "Tail Risk Underestimation"
    Under the Normal distribution, $P(|z| > 4) \approx 6.3 \times 10^{-5}$ (once every 63 years at daily frequency). Empirically, 4-sigma events occur roughly once per year --- a factor of 60 more frequently. Using the Normal for risk management leads to **systematic underestimation of tail risk**.

### Location-Scale Distributions

A random variable $X$ belongs to the **location-scale family** if its distribution can be written as:

$$
X = \mu + \sigma Z, \qquad Z \sim D(0, 1)
$$

where $D(0,1)$ is a standardized distribution with $E[Z] = 0$ and $\text{Var}(Z) = 1$. This structure integrates naturally with GARCH models:

$$
r_t = \mu_t + \sigma_t z_t, \qquad z_t \sim D(0, 1; \boldsymbol{\theta})
$$

where $\boldsymbol{\theta}$ are distributional shape parameters (e.g., degrees of freedom, skewness).

---

## Student-$t$ Distribution

### Standard Student-$t$

The Student-$t$ distribution with $\nu > 0$ degrees of freedom has PDF:

$$
f_\nu(x) = \frac{\Gamma\left(\frac{\nu+1}{2}\right)}{\sqrt{\nu\pi} \; \Gamma\left(\frac{\nu}{2}\right)} \left(1 + \frac{x^2}{\nu}\right)^{-\frac{\nu+1}{2}}
$$

**Moments** (for $\nu > 2k$):

$$
E[X] = 0 \quad (\nu > 1), \qquad \text{Var}(X) = \frac{\nu}{\nu-2} \quad (\nu > 2)
$$

$$
\kappa = 3 + \frac{6}{\nu - 4} \quad (\nu > 4)
$$

### Standardized Student-$t$ (Zero Mean, Unit Variance)

For GARCH models, we need $E[z_t] = 0$ and $\text{Var}(z_t) = 1$. The **standardized** Student-$t$ is:

$$
z = \frac{X}{\sqrt{\nu/(\nu-2)}}
$$

with PDF:

$$
\boxed{f(z; \nu) = \frac{\Gamma\left(\frac{\nu+1}{2}\right)}{\sqrt{(\nu-2)\pi} \; \Gamma\left(\frac{\nu}{2}\right)} \left(1 + \frac{z^2}{\nu-2}\right)^{-\frac{\nu+1}{2}}}
$$

!!! info "Parameter Range"
    - $\nu > 2$: Required for finite variance (and hence valid GARCH integration)
    - $\nu > 4$: Required for finite kurtosis
    - $\nu \to \infty$: Converges to $N(0,1)$
    - Typical estimates for daily returns: $\nu \in [4, 12]$

### CDF

The CDF of the standardized Student-$t$ is:

$$
F(z; \nu) = I_{x(z)}\left(\frac{\nu}{2}, \frac{1}{2}\right)
$$

where $I_x(a,b)$ is the regularized incomplete beta function and $x(z) = \frac{\nu-2}{\nu - 2 + z^2} \cdot \frac{1+\text{sgn}(z)}{2}$.

In practice, the CDF and quantile function are computed using well-optimized library routines (`scipy.stats.t`).

---

## Skewed Student-$t$ (Hansen, 1994)

### Motivation

The symmetric Student-$t$ captures heavy tails but not the **asymmetric tail behavior** often observed in equity returns (left tail heavier than right). Hansen (1994) introduced a skewed version.

### Construction

The Skewed Student-$t$ is constructed by applying different scaling to the positive and negative halves of the standardized Student-$t$ distribution. With parameters $\nu > 2$ (degrees of freedom) and $\lambda \in (-1, 1)$ (skewness):

$$
\boxed{f(z; \nu, \lambda) = \begin{cases}
bc\left(1 + \frac{1}{\nu-2}\left(\frac{bz+a}{1-\lambda}\right)^2\right)^{-\frac{\nu+1}{2}} & \text{if } z < -a/b \\[6pt]
bc\left(1 + \frac{1}{\nu-2}\left(\frac{bz+a}{1+\lambda}\right)^2\right)^{-\frac{\nu+1}{2}} & \text{if } z \geq -a/b
\end{cases}}
$$

where the constants ensure zero mean and unit variance:

$$
a = 4\lambda c \frac{\nu-2}{\nu-1}, \qquad b = \sqrt{1 + 3\lambda^2 - a^2}, \qquad c = \frac{\Gamma\left(\frac{\nu+1}{2}\right)}{\sqrt{\pi(\nu-2)} \; \Gamma\left(\frac{\nu}{2}\right)}
$$

### Properties

??? note "Derivation of Constants $a$, $b$, $c$"
    The constant $c$ is the normalization of the standard Student-$t$ density. To ensure $E[z] = 0$:

    $$
    E[z] = \frac{-a}{b} \quad \Rightarrow \quad a = -b \cdot E[z_{\text{raw}}]
    $$

    where $z_{\text{raw}}$ is the raw (non-centered) skewed variable. The first moment of the half-$t$ distribution gives:

    $$
    E[z_{\text{raw}}] = -4\lambda c \frac{\nu-2}{\nu-1} / b
    $$

    Setting $E[z] = 0$ and $\text{Var}(z) = 1$ yields the expressions for $a$ and $b$.

**Interpretation of $\lambda$:**

- $\lambda = 0$: Symmetric Student-$t$ (reduces to standard case)
- $\lambda < 0$: Left tail heavier (negative skewness) --- common for equity indices
- $\lambda > 0$: Right tail heavier (positive skewness)

**Moments:**

$$
E[z] = 0, \qquad \text{Var}(z) = 1 \quad \text{(by construction)}
$$

$$
\text{Skewness} = -\frac{a}{b^3}\left(3b^2 + 6a^2 - 4a^2 \cdot \frac{\nu-2}{\nu-3}\right) \quad (\nu > 3)
$$

---

## Generalized Error Distribution (GED)

### Definition

The **Generalized Error Distribution** (also called Generalized Normal or Exponential Power Distribution) with shape parameter $\nu > 0$ has PDF:

$$
\boxed{f(z; \nu) = \frac{\nu}{2 \, c_\nu \, \Gamma(1/\nu)} \exp\left(-\frac{1}{2}\left|\frac{z}{c_\nu}\right|^\nu\right)}
$$

where the scaling constant ensures unit variance:

$$
c_\nu = \sqrt{\frac{2^{-2/\nu} \, \Gamma(1/\nu)}{\Gamma(3/\nu)}}
$$

### Special Cases

The GED nests several well-known distributions:

| $\nu$ | Distribution | Kurtosis |
|:-------|:-------------|:---------|
| 1 | Laplace (Double Exponential) | 6 |
| 2 | **Normal (Gaussian)** | 3 |
| $\to \infty$ | Uniform | 1.8 |

!!! tip "Tail Behavior"
    - $\nu < 2$: **Heavier tails** than the Normal (leptokurtic) --- appropriate for financial returns
    - $\nu = 2$: Exactly Normal
    - $\nu > 2$: **Lighter tails** than the Normal (platykurtic) --- rarely relevant for finance

    Typical estimates for daily returns: $\nu \in [1.0, 1.8]$.

### Moments

For the standardized GED with $E[z] = 0$ and $\text{Var}(z) = 1$:

$$
E[|z|^k] = \frac{2^{k/\nu} \, \Gamma\left(\frac{k+1}{\nu}\right)}{c_\nu^k \, \Gamma(1/\nu)}
$$

**Kurtosis:**

$$
\kappa = \frac{\Gamma(1/\nu) \, \Gamma(5/\nu)}{\Gamma(3/\nu)^2}
$$

---

## Skewed GED

### Construction

The Skewed GED extends the GED with an asymmetry parameter $\lambda \in (-1, 1)$, following the Fernandez and Steel (1998) approach of inverse-scale factors:

$$
\boxed{f(z; \nu, \lambda) = \frac{2}{\xi + 1/\xi} \begin{cases}
g\left(\xi(z - m)/s; \nu\right) & \text{if } z < m/s \\[4pt]
g\left((z - m)/(s\xi); \nu\right) & \text{if } z \geq m/s
\end{cases}}
$$

where $g(\cdot; \nu)$ is the standardized GED density, $\xi = \exp(\lambda)$ is the asymmetry ratio, and:

$$
m = \frac{2 \, c_\nu \, \Gamma(2/\nu)}{\Gamma(1/\nu)}\left(\xi - \frac{1}{\xi}\right), \qquad s = \sqrt{\left(\xi^2 + \frac{1}{\xi^2} - 1\right) \cdot \frac{\Gamma(3/\nu)}{\Gamma(1/\nu)} \cdot \frac{1}{c_\nu^2} - m^2}
$$

The constants $m$ and $s$ ensure $E[z] = 0$ and $\text{Var}(z) = 1$.

### Properties

- $\lambda = 0$ ($\xi = 1$): Reduces to symmetric GED
- $\lambda < 0$ ($\xi < 1$): Heavier left tail
- $\lambda > 0$ ($\xi > 1$): Heavier right tail
- Nests Normal ($\nu = 2, \lambda = 0$), Laplace ($\nu = 1, \lambda = 0$), Skewed Laplace ($\nu = 1$)

---

## Maximum Likelihood Estimation

### General Framework

Given a GARCH model with conditional mean $\mu_t(\boldsymbol{\theta})$ and conditional variance $\sigma_t^2(\boldsymbol{\theta})$, the standardized innovations are:

$$
z_t = \frac{r_t - \mu_t(\boldsymbol{\theta})}{\sigma_t(\boldsymbol{\theta})}
$$

The **log-likelihood** for a sample of $T$ observations is:

$$
\ell(\boldsymbol{\theta}, \boldsymbol{\eta}) = \sum_{t=1}^{T} \left[\log f(z_t; \boldsymbol{\eta}) - \frac{1}{2}\log \sigma_t^2(\boldsymbol{\theta})\right]
$$

where $\boldsymbol{\theta}$ are the GARCH parameters and $\boldsymbol{\eta}$ are the distributional shape parameters.

### Log-Likelihoods by Distribution

=== "Normal"

    $$
    \ell_t = -\frac{1}{2}\log(2\pi) - \frac{1}{2}\log \sigma_t^2 - \frac{z_t^2}{2}
    $$

    No shape parameters. This is the **quasi-maximum likelihood (QML)** baseline.

=== "Student-$t$"

    $$
    \ell_t = \log\Gamma\!\left(\frac{\nu+1}{2}\right) - \log\Gamma\!\left(\frac{\nu}{2}\right) - \frac{1}{2}\log\left[(\nu-2)\pi\right] - \frac{1}{2}\log \sigma_t^2 - \frac{\nu+1}{2}\log\left(1 + \frac{z_t^2}{\nu-2}\right)
    $$

    Shape parameter: $\nu > 2$.

=== "Skewed Student-$t$"

    $$
    \ell_t = \log(bc) - \frac{1}{2}\log \sigma_t^2 - \frac{\nu+1}{2}\log\left(1 + \frac{1}{\nu-2}\left(\frac{bz_t + a}{1 + \lambda \cdot \text{sgn}(z_t + a/b)}\right)^2\right)
    $$

    Shape parameters: $\nu > 2$, $\lambda \in (-1, 1)$.

=== "GED"

    $$
    \ell_t = \log\!\left(\frac{\nu}{2c_\nu}\right) - \log\Gamma\!\left(\frac{1}{\nu}\right) - \frac{1}{2}\log \sigma_t^2 - \frac{1}{2}\left|\frac{z_t}{c_\nu}\right|^\nu
    $$

    Shape parameter: $\nu > 0$.

=== "Skewed GED"

    $$
    \ell_t = \log\!\left(\frac{2}{s(\xi + 1/\xi)}\right) + \log g\!\left(\frac{z_t - m/s}{s \cdot (1 + \lambda \cdot \text{sgn}(z_t - m/s)) / (\xi^{\text{sgn}(z_t-m/s)})}; \nu\right) - \frac{1}{2}\log \sigma_t^2
    $$

    Shape parameters: $\nu > 0$, $\lambda \in (-1, 1)$.

### Score Functions

The **score vector** is the gradient of the log-likelihood with respect to parameters:

$$
\mathbf{s}_t(\boldsymbol{\psi}) = \frac{\partial \ell_t}{\partial \boldsymbol{\psi}}, \qquad \boldsymbol{\psi} = (\boldsymbol{\theta}', \boldsymbol{\eta}')'
$$

=== "Student-$t$ Score for $\nu$"

    $$
    \frac{\partial \ell_t}{\partial \nu} = \frac{1}{2}\left[\psi\!\left(\frac{\nu+1}{2}\right) - \psi\!\left(\frac{\nu}{2}\right) - \frac{1}{\nu-2} - \log\!\left(1 + \frac{z_t^2}{\nu-2}\right) + \frac{(\nu+1)z_t^2}{(\nu-2)^2 + (\nu-2)z_t^2}\right]
    $$

    where $\psi(\cdot)$ is the digamma function.

=== "GED Score for $\nu$"

    $$
    \frac{\partial \ell_t}{\partial \nu} = \frac{1}{\nu} + \frac{\psi(1/\nu)}{\nu^2} + \frac{1}{\nu}\left[\frac{\psi(3/\nu)}{\nu} - \frac{\psi(1/\nu)}{\nu}\right]\frac{1}{2c_\nu^2} - \frac{1}{2}\left|\frac{z_t}{c_\nu}\right|^\nu \log\!\left|\frac{z_t}{c_\nu}\right|
    $$

### Information Matrix and Asymptotic Theory

The **Fisher information matrix** is:

$$
\mathcal{I}(\boldsymbol{\psi}) = -E\left[\frac{\partial^2 \ell_t}{\partial \boldsymbol{\psi} \partial \boldsymbol{\psi}'}\right] = E\left[\mathbf{s}_t \mathbf{s}_t'\right]
$$

Under standard regularity conditions (Bollerslev & Wooldridge, 1992):

$$
\sqrt{T}\left(\hat{\boldsymbol{\psi}}_{\text{MLE}} - \boldsymbol{\psi}_0\right) \overset{d}{\to} N\left(\mathbf{0}, \mathcal{I}(\boldsymbol{\psi}_0)^{-1}\right)
$$

!!! warning "Robust Standard Errors"
    In practice, the information matrix equality $\mathcal{I} = E[\mathbf{s}_t \mathbf{s}_t'] = -E[\mathbf{H}_t]$ may not hold due to model misspecification. The **sandwich estimator** (also called robust or QML standard errors) is preferred:

    $$
    \text{Var}(\hat{\boldsymbol{\psi}}) = \mathbf{A}^{-1} \mathbf{B} \mathbf{A}^{-1} / T
    $$

    where $\mathbf{A} = T^{-1}\sum_t \mathbf{H}_t$ (Hessian) and $\mathbf{B} = T^{-1}\sum_t \mathbf{s}_t \mathbf{s}_t'$ (outer product of gradients).

### Numerical Optimization

!!! tip "Practical Considerations"
    - **Starting values:** Use QML (Normal) estimates for GARCH parameters, then add distributional parameters
    - **Constraints:** Transform constrained parameters: $\nu = 2 + \exp(\tilde{\nu})$ ensures $\nu > 2$ for Student-$t$; $\lambda = (1 - \exp(-\tilde{\lambda}))/(1 + \exp(-\tilde{\lambda}))$ maps $\mathbb{R} \to (-1,1)$
    - **Optimizer:** L-BFGS-B or SLSQP for bound-constrained optimization; Nelder-Mead as fallback
    - **Gradient:** Analytical gradients when available; otherwise central differences with step $\Delta = 10^{-5}$

---

## Distribution Selection

### Information Criteria

Given a model with log-likelihood $\ell$ and $k$ parameters estimated from $T$ observations:

$$
\text{AIC} = -2\ell + 2k
$$

$$
\text{BIC} = -2\ell + k \log T
$$

$$
\text{HQC} = -2\ell + 2k \log\log T
$$

!!! info "Interpretation"
    - **AIC** (Akaike, 1974): Minimizes Kullback-Leibler divergence; tends to select more complex models
    - **BIC** (Schwarz, 1978): Consistent model selector; penalizes complexity more heavily for large $T$
    - **HQC** (Hannan-Quinn, 1979): Intermediate penalty; consistent under weaker conditions than BIC

    Lower values indicate better fit. BIC is generally preferred for distribution selection in GARCH models, as the sample sizes are typically large enough that consistency matters.

### Goodness-of-Fit Tests

#### Kolmogorov-Smirnov Test

Tests whether the PIT residuals $u_t = F(z_t; \hat{\boldsymbol{\eta}})$ follow $U(0,1)$:

$$
D_n = \sup_x |F_n(x) - F_0(x)|
$$

where $F_n$ is the empirical CDF and $F_0$ is the hypothesized CDF.

!!! warning "Parameter Estimation Effect"
    The standard KS critical values assume known parameters. When parameters are estimated, the test is **conservative** (actual size < nominal size). The Lilliefors correction or bootstrap-based critical values should be used.

#### Anderson-Darling Test

A weighted version of the KS test that gives more weight to the **tails**:

$$
A^2 = -T - \frac{1}{T}\sum_{t=1}^{T} \left[(2t-1)\log u_{(t)} + (2T+1-2t)\log(1-u_{(t)})\right]
$$

where $u_{(t)}$ are the ordered PIT values. The Anderson-Darling test is more powerful than KS for detecting tail deviations --- precisely what matters for risk management.

### Visual Diagnostics: QQ-Plots

The **quantile-quantile plot** compares empirical quantiles of standardized residuals against theoretical quantiles of the assumed distribution:

$$
\text{Plot:} \quad \left(F^{-1}\left(\frac{t-0.5}{T}\right), \; z_{(t)}\right), \qquad t = 1, \ldots, T
$$

where $z_{(t)}$ are the order statistics and $F^{-1}$ is the theoretical quantile function.

**Interpreting QQ-plots:**

| Pattern | Interpretation |
|:--------|:---------------|
| Points on 45° line | Good fit |
| S-curve (concave then convex) | Heavier tails than assumed |
| Inverse S-curve | Lighter tails than assumed |
| Deviation at left tail only | Left tail misspecification |
| Systematic curvature | Wrong distributional family |

!!! tip "Decision Framework"
    A practical workflow for distribution selection:

    1. Fit GARCH with Normal, Student-$t$, Skewed-$t$, GED, and Skewed GED
    2. Compare BIC across specifications
    3. Verify with QQ-plots and Anderson-Darling test on PIT residuals
    4. For risk management: prioritize tail fit (Anderson-Darling) over overall fit (KS)

---

## Comparison of Distributions

| Distribution | Parameters | Kurtosis Range | Skewness | Normal as Limit |
|:-------------|:-----------|:---------------|:---------|:----------------|
| Normal | --- | 3 (fixed) | 0 (fixed) | --- |
| Student-$t$ | $\nu > 2$ | $(3, \infty)$ | 0 (fixed) | $\nu \to \infty$ |
| Skewed-$t$ | $\nu > 2$, $\lambda \in (-1,1)$ | $(3, \infty)$ | $(-\infty, \infty)$ | $\nu \to \infty$, $\lambda = 0$ |
| GED | $\nu > 0$ | $(1.8, 6)$ | 0 (fixed) | $\nu = 2$ |
| Skewed GED | $\nu > 0$, $\lambda \in (-1,1)$ | $(1.8, 6)$ | $(-\infty, \infty)$ | $\nu = 2$, $\lambda = 0$ |

!!! tip "Which Distribution to Use?"
    - **Student-$t$:** Default choice for daily financial returns. Captures excess kurtosis with a single parameter.
    - **Skewed-$t$:** When equity index returns show significant negative skewness.
    - **GED:** Alternative to Student-$t$; offers different tail decay (exponential vs. polynomial).
    - **Skewed GED:** Maximum flexibility; useful when both skewness and kurtosis deviate from Normal.
    - **Normal:** Only for QML estimation or when higher-frequency data (intraday) approaches Gaussian behavior.

---

## References

- Akaike, H. (1974). A new look at the statistical model identification. *IEEE Transactions on Automatic Control*, 19(6), 716--723.
- Bollerslev, T., & Wooldridge, J.M. (1992). Quasi-maximum likelihood estimation and inference in dynamic models with time-varying covariances. *Econometric Reviews*, 11(2), 143--172.
- Fernandez, C., & Steel, M.F.J. (1998). On Bayesian modeling of fat tails and skewness. *Journal of the American Statistical Association*, 93(441), 359--371.
- Hansen, B.E. (1994). Autoregressive conditional density estimation. *International Economic Review*, 35(3), 705--730.
- Hannan, E.J., & Quinn, B.G. (1979). The determination of the order of an autoregression. *Journal of the Royal Statistical Society: Series B*, 41(2), 190--195.
- Nelson, D.B. (1991). Conditional heteroskedasticity in asset returns: A new approach. *Econometrica*, 59(2), 347--370.
- Schwarz, G. (1978). Estimating the dimension of a model. *Annals of Statistics*, 6(2), 461--464.
