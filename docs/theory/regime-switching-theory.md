---
title: "Regime-Switching Theory"
description: "Mathematical foundations of Markov-switching models: Markov chains, Hamilton filter, Kim smoother, EM algorithm, identification, and testing"
---

# Regime-Switching Models --- Theoretical Foundations

!!! abstract "Key Takeaway"
    Regime-switching models, pioneered by Hamilton (1989), capture **structural breaks and recurring states** in economic time series. The data-generating process depends on an unobserved discrete state variable that follows a first-order Markov chain. This page provides complete derivations of the Hamilton filter, Kim smoother, and EM algorithm, along with a thorough discussion of the identification challenges unique to this model class.

---

## Markov Chains

### Definition

A first-order Markov chain $\{s_t\}_{t=1}^T$ taking values in $\{1, 2, \ldots, K\}$ satisfies the **Markov property**:

$$
P(s_t = j \mid s_{t-1} = i, s_{t-2}, \ldots, s_1) = P(s_t = j \mid s_{t-1} = i) = p_{ij}
$$

The entire dynamics of the chain are captured by the $K \times K$ **transition matrix**:

$$
P = \begin{pmatrix}
p_{11} & p_{12} & \cdots & p_{1K} \\
p_{21} & p_{22} & \cdots & p_{2K} \\
\vdots & \vdots & \ddots & \vdots \\
p_{K1} & p_{K2} & \cdots & p_{KK}
\end{pmatrix}
$$

where each row sums to one:

$$
\sum_{j=1}^{K} p_{ij} = 1, \quad p_{ij} \geq 0 \quad \forall\, i, j
$$

!!! note "Convention"
    We use the convention where $p_{ij} = P(s_t = j \mid s_{t-1} = i)$, so that $P$ is a **row-stochastic** matrix. Some references (including Hamilton's original paper) use the transpose convention with column-stochastic matrices. Both are equivalent; consistency is what matters.

### Properties of the Transition Matrix

**Irreducibility.** A Markov chain is **irreducible** if every state can be reached from every other state in a finite number of steps. Formally, for all pairs $(i, j)$ there exists $n \geq 1$ such that $P^n_{ij} > 0$. In financial applications with $K = 2$ (e.g., bull/bear markets), irreducibility is guaranteed whenever $p_{12} > 0$ and $p_{21} > 0$.

**Aperiodicity.** A state $i$ is aperiodic if $\gcd\{n \geq 1 : P^n_{ii} > 0\} = 1$. When all diagonal entries $p_{ii} > 0$, the chain is aperiodic.

**Ergodicity.** An irreducible, aperiodic Markov chain on a finite state space is **ergodic**. For an ergodic chain:

$$
\lim_{n \to \infty} P^n = \mathbf{1} \pi'
$$

where $\pi$ is the unique **stationary distribution** (ergodic probability vector).

### Stationary Distribution

The stationary distribution $\pi = (\pi_1, \pi_2, \ldots, \pi_K)'$ satisfies:

$$
\pi' P = \pi', \qquad \sum_{j=1}^{K} \pi_j = 1
$$

This is a left-eigenvector problem. Equivalently, $\pi$ solves:

$$
(P' - I_K) \pi = 0 \quad \text{subject to} \quad \mathbf{1}' \pi = 1
$$

**Two-regime case ($K = 2$).** With transition matrix:

$$
P = \begin{pmatrix} p_{11} & 1 - p_{11} \\ 1 - p_{22} & p_{22} \end{pmatrix}
$$

the stationary probabilities have closed-form solutions:

$$
\pi_1 = \frac{1 - p_{22}}{2 - p_{11} - p_{22}}, \qquad \pi_2 = \frac{1 - p_{11}}{2 - p_{11} - p_{22}}
$$

!!! example "Interpretation"
    If $p_{11} = 0.95$ and $p_{22} = 0.90$, then $\pi_1 = 0.10/0.15 = 2/3$ and $\pi_2 = 0.05/0.15 = 1/3$. The economy spends roughly twice as much time in regime 1 as in regime 2.

### Expected Duration of a Regime

The duration of regime $j$ (the number of consecutive periods the chain stays in state $j$) follows a **geometric distribution** with parameter $1 - p_{jj}$:

$$
P(\text{duration} = d \mid s_t = j) = p_{jj}^{d-1}(1 - p_{jj}), \quad d = 1, 2, \ldots
$$

The expected duration is:

$$
E[D_j] = \frac{1}{1 - p_{jj}}
$$

!!! example "Business Cycle Durations"
    If recessions ($s_t = 2$) have $p_{22} = 0.90$, the expected recession duration is $1/(1-0.90) = 10$ quarters. If expansions ($s_t = 1$) have $p_{11} = 0.975$, the expected expansion is $1/(1-0.975) = 40$ quarters. These asymmetric durations are a well-documented feature of business cycles.

---

## The Markov-Switching Model

### General Specification

The Markov-Switching Autoregressive model of order $p$, MS($K$)-AR($p$), is:

$$
y_t = \mu_{s_t} + \sum_{i=1}^{p} \phi_{i, s_t} (y_{t-i} - \mu_{s_{t-i}}) + \sigma_{s_t} \varepsilon_t, \qquad \varepsilon_t \overset{\text{iid}}{\sim} \mathcal{N}(0, 1)
$$

where $s_t \in \{1, 2, \ldots, K\}$ follows a first-order Markov chain with transition matrix $P$.

**Special cases:**

| Model | Switching Parameters |
|:------|:--------------------|
| MSI($K$)-AR($p$) | Intercept only: $\mu_{s_t}$ |
| MSM($K$)-AR($p$) | Mean only: $\mu_{s_t}$ |
| MSH($K$)-AR($p$) | Variance only: $\sigma_{s_t}^2$ |
| MSIH($K$)-AR($p$) | Intercept and variance |
| MSIAH($K$)-AR($p$) | All parameters switch |

### Conditional Density

Given $s_t = j$ and the information set $\mathcal{F}_{t-1} = \{y_{t-1}, y_{t-2}, \ldots\}$, the conditional density of $y_t$ under Gaussian innovations is:

$$
f(y_t \mid s_t = j, \mathcal{F}_{t-1}; \theta) = \frac{1}{\sqrt{2\pi}\, \sigma_j} \exp\left\{-\frac{(y_t - \mu_j(y_{t-1}, \ldots))^2}{2\sigma_j^2}\right\}
$$

where $\mu_j(y_{t-1}, \ldots) = \mu_j + \sum_{i=1}^{p} \phi_{i,j}(y_{t-i} - \mu_j)$ is the regime-dependent conditional mean.

---

## The Hamilton Filter

The Hamilton (1989) filter is a recursive algorithm for computing **filtered probabilities** $P(s_t = j \mid \mathcal{Y}_t; \theta)$, where $\mathcal{Y}_t = \{y_1, \ldots, y_t\}$ and $\theta$ collects all parameters.

### Derivation

**Step 0: Initialization.** Set the initial probabilities to the ergodic distribution:

$$
\hat{\xi}_{1|0} = \pi
$$

where $\hat{\xi}_{t|t-1}$ is the $K \times 1$ vector with $j$-th element $P(s_t = j \mid \mathcal{Y}_{t-1}; \theta)$.

**Step 1: Prediction.** Given filtered probabilities at $t-1$, predict the regime at $t$:

$$
\hat{\xi}_{t|t-1} = P' \hat{\xi}_{t-1|t-1}
$$

The $j$-th element is:

$$
P(s_t = j \mid \mathcal{Y}_{t-1}; \theta) = \sum_{i=1}^{K} p_{ij}\, P(s_{t-1} = i \mid \mathcal{Y}_{t-1}; \theta)
$$

**Step 2: Update.** Upon observing $y_t$, apply Bayes' theorem to update:

$$
P(s_t = j \mid \mathcal{Y}_t; \theta) = \frac{f(y_t \mid s_t = j, \mathcal{F}_{t-1};\theta) \cdot P(s_t = j \mid \mathcal{Y}_{t-1};\theta)}{\sum_{k=1}^{K} f(y_t \mid s_t = k, \mathcal{F}_{t-1};\theta) \cdot P(s_t = k \mid \mathcal{Y}_{t-1};\theta)}
$$

In vector notation:

$$
\hat{\xi}_{t|t} = \frac{\hat{\xi}_{t|t-1} \odot \eta_t}{\mathbf{1}' (\hat{\xi}_{t|t-1} \odot \eta_t)}
$$

where $\odot$ denotes element-wise multiplication and $\eta_t$ is the $K \times 1$ vector of conditional densities with $j$-th element $f(y_t \mid s_t = j, \mathcal{F}_{t-1}; \theta)$.

**Step 3: Likelihood contribution.** The denominator in the update step gives the predictive density:

$$
f(y_t \mid \mathcal{Y}_{t-1}; \theta) = \mathbf{1}'(\hat{\xi}_{t|t-1} \odot \eta_t) = \sum_{j=1}^{K} f(y_t \mid s_t = j, \mathcal{F}_{t-1}; \theta) \cdot P(s_t = j \mid \mathcal{Y}_{t-1}; \theta)
$$

### Log-Likelihood via Prediction Error Decomposition

The full log-likelihood is constructed by summing the log predictive densities:

$$
\ell(\theta) = \sum_{t=1}^{T} \log f(y_t \mid \mathcal{Y}_{t-1}; \theta) = \sum_{t=1}^{T} \log \left[\mathbf{1}' (\hat{\xi}_{t|t-1} \odot \eta_t)\right]
$$

This is the **prediction error decomposition**, analogous to the approach used in the Kalman filter for state-space models.

!!! tip "Algorithm Summary"
    ```
    Initialize: xi_pred = pi (ergodic distribution)
    For t = 1 to T:
        1. Compute eta_t[j] = f(y_t | s_t=j) for j = 1,...,K
        2. xi_filt = (xi_pred .* eta_t) / sum(xi_pred .* eta_t)
        3. log_lik += log(sum(xi_pred .* eta_t))
        4. xi_pred = P' * xi_filt
    Return log_lik, xi_filt_{1:T}
    ```

### Computational Complexity

The Hamilton filter has complexity $O(TK^2)$ per likelihood evaluation:

- At each time step: matrix-vector product $P' \hat{\xi}_{t-1|t-1}$ costs $O(K^2)$
- Element-wise operations and normalization cost $O(K)$
- Total: $T$ time steps $\times O(K^2)$ per step

For the common case $K = 2$, this reduces to $O(T)$, making the filter very efficient.

!!! warning "Numerical Stability"
    In practice, work with **log-densities** and use the log-sum-exp trick to avoid underflow:
    $$
    \log \sum_j e^{a_j} = \max_j(a_j) + \log \sum_j e^{a_j - \max_j(a_j)}
    $$
    This is critical for long time series or when regime densities differ by many orders of magnitude.

---

## The Kim Smoother

### Motivation

The Hamilton filter yields **filtered** probabilities $P(s_t \mid \mathcal{Y}_t)$ that use information up to time $t$. For parameter estimation and regime classification, we want **smoothed** probabilities $P(s_t \mid \mathcal{Y}_T)$ that use the full sample.

### Derivation

Kim (1994) derived an efficient backward recursion. Starting from the last observation $t = T$ where $\hat{\xi}_{T|T}$ is already available, iterate backward for $t = T-1, T-2, \ldots, 1$:

$$
P(s_t = i \mid \mathcal{Y}_T; \theta) = P(s_t = i \mid \mathcal{Y}_t; \theta) \sum_{j=1}^{K} \frac{p_{ij} \cdot P(s_{t+1} = j \mid \mathcal{Y}_T; \theta)}{P(s_{t+1} = j \mid \mathcal{Y}_t; \theta)}
$$

In vector notation:

$$
\hat{\xi}_{t|T} = \hat{\xi}_{t|t} \odot \left[P \left(\frac{\hat{\xi}_{t+1|T}}{\hat{\xi}_{t+1|t}}\right)\right]
$$

where division is element-wise.

!!! tip "Algorithm Summary"
    ```
    Initialize: xi_smooth[T] = xi_filt[T]
    For t = T-1 down to 1:
        xi_smooth[t] = xi_filt[t] .* (P * (xi_smooth[t+1] ./ xi_pred[t+1]))
    Return xi_smooth_{1:T}
    ```

### Joint Smoothed Probabilities

For the EM algorithm, we also need the **joint smoothed probabilities**:

$$
P(s_t = i, s_{t+1} = j \mid \mathcal{Y}_T; \theta) = \frac{P(s_t = i \mid \mathcal{Y}_t;\theta) \cdot p_{ij} \cdot P(s_{t+1} = j \mid \mathcal{Y}_T;\theta)}{P(s_{t+1} = j \mid \mathcal{Y}_t;\theta)}
$$

These are used to update the transition probabilities in the M-step.

### Relation to the Kalman Smoother

The Kim smoother is the **discrete-state analogue** of the Rauch-Tung-Striebel (RTS) smoother used in linear Gaussian state-space models. The parallel is:

| Component | Kalman / RTS | Hamilton / Kim |
|:----------|:-------------|:---------------|
| State | Continuous $\alpha_t \in \mathbb{R}^m$ | Discrete $s_t \in \{1, \ldots, K\}$ |
| Forward pass | Kalman filter | Hamilton filter |
| Backward pass | RTS smoother | Kim smoother |
| Output (forward) | $E[\alpha_t \mid \mathcal{Y}_t]$ | $P(s_t \mid \mathcal{Y}_t)$ |
| Output (backward) | $E[\alpha_t \mid \mathcal{Y}_T]$ | $P(s_t \mid \mathcal{Y}_T)$ |

Kim (1994) also showed how to combine both frameworks for models with **both** discrete regime switches and continuous latent states (the Kim filter-smoother).

---

## The EM Algorithm

The Expectation-Maximization algorithm (Dempster, Laird, and Rubin, 1977) is a natural approach for Markov-switching models because the regime sequence $\{s_t\}$ plays the role of **missing data**.

### Complete-Data Log-Likelihood

If the regimes $\{s_t\}_{t=1}^T$ were observed, the complete-data log-likelihood would be:

$$
\ell_c(\theta) = \log P(s_1; \theta) + \sum_{t=2}^{T} \log P(s_t \mid s_{t-1}; \theta) + \sum_{t=1}^{T} \log f(y_t \mid s_t, \mathcal{F}_{t-1}; \theta)
$$

This decomposes into three independent terms:

$$
\ell_c(\theta) = \underbrace{\sum_{j=1}^{K} \mathbb{1}(s_1 = j) \log \pi_j}_{\text{initial state}} + \underbrace{\sum_{t=2}^{T} \sum_{i=1}^{K} \sum_{j=1}^{K} \mathbb{1}(s_{t-1}=i, s_t=j) \log p_{ij}}_{\text{transitions}} + \underbrace{\sum_{t=1}^{T} \sum_{j=1}^{K} \mathbb{1}(s_t=j) \log f(y_t \mid s_t=j, \mathcal{F}_{t-1};\theta)}_{\text{observations}}
$$

### E-Step

The E-step computes the **expected complete-data log-likelihood** given current parameter estimates $\theta^{(n)}$ and the observed data $\mathcal{Y}_T$:

$$
Q(\theta \mid \theta^{(n)}) = E_{s \mid \mathcal{Y}_T, \theta^{(n)}}[\ell_c(\theta)]
$$

This requires replacing the indicator functions with their conditional expectations:

$$
E[\mathbb{1}(s_t = j) \mid \mathcal{Y}_T; \theta^{(n)}] = P(s_t = j \mid \mathcal{Y}_T; \theta^{(n)}) \equiv \hat{\xi}_{t|T}^{(j)}
$$

$$
E[\mathbb{1}(s_{t-1} = i, s_t = j) \mid \mathcal{Y}_T; \theta^{(n)}] = P(s_{t-1} = i, s_t = j \mid \mathcal{Y}_T; \theta^{(n)}) \equiv \hat{\xi}_{t-1,t|T}^{(i,j)}
$$

These are computed by running the Hamilton filter followed by the Kim smoother with the current parameters $\theta^{(n)}$.

The expected complete-data log-likelihood becomes:

$$
Q(\theta \mid \theta^{(n)}) = \sum_{j=1}^{K} \hat{\xi}_{1|T}^{(j)} \log \pi_j + \sum_{t=2}^{T} \sum_{i=1}^{K} \sum_{j=1}^{K} \hat{\xi}_{t-1,t|T}^{(i,j)} \log p_{ij} + \sum_{t=1}^{T} \sum_{j=1}^{K} \hat{\xi}_{t|T}^{(j)} \log f(y_t \mid s_t=j, \mathcal{F}_{t-1};\theta)
$$

### M-Step

The M-step maximizes $Q(\theta \mid \theta^{(n)})$ with respect to $\theta$.

**Transition probabilities.** Using Lagrange multipliers to enforce $\sum_j p_{ij} = 1$:

$$
\hat{p}_{ij}^{(n+1)} = \frac{\sum_{t=2}^{T} \hat{\xi}_{t-1,t|T}^{(i,j)}}{\sum_{t=2}^{T} \hat{\xi}_{t-1|T}^{(i)}} = \frac{\sum_{t=2}^{T} P(s_{t-1}=i, s_t=j \mid \mathcal{Y}_T; \theta^{(n)})}{\sum_{t=2}^{T} P(s_{t-1}=i \mid \mathcal{Y}_T; \theta^{(n)})}
$$

!!! info "Intuition"
    The updated transition probability $\hat{p}_{ij}$ is the ratio of expected transitions from $i$ to $j$ divided by the total expected time spent in state $i$. This is the weighted-average analogue of the maximum likelihood estimator for a multinomial distribution.

**Regime-dependent means (MSM case).** For a model with switching means only:

$$
\hat{\mu}_j^{(n+1)} = \frac{\sum_{t=1}^{T} \hat{\xi}_{t|T}^{(j)} \cdot y_t}{\sum_{t=1}^{T} \hat{\xi}_{t|T}^{(j)}}
$$

**Regime-dependent variances.** The updated variance for regime $j$:

$$
\hat{\sigma}_j^{2,(n+1)} = \frac{\sum_{t=1}^{T} \hat{\xi}_{t|T}^{(j)} \cdot (y_t - \hat{\mu}_j^{(n+1)})^2}{\sum_{t=1}^{T} \hat{\xi}_{t|T}^{(j)}}
$$

**AR coefficients.** For regime-dependent AR parameters, the M-step involves solving a weighted least squares problem:

$$
\hat{\phi}_j^{(n+1)} = \left(\sum_{t=1}^{T} \hat{\xi}_{t|T}^{(j)} X_t X_t'\right)^{-1} \left(\sum_{t=1}^{T} \hat{\xi}_{t|T}^{(j)} X_t y_t\right)
$$

where $X_t = (1, y_{t-1}, \ldots, y_{t-p})'$.

### Convergence Properties

!!! success "Monotonic Convergence"
    The EM algorithm guarantees that the observed-data log-likelihood **never decreases**:

    $$
    \ell(\theta^{(n+1)}) \geq \ell(\theta^{(n)})
    $$

    **Proof sketch:** By Jensen's inequality, $\ell(\theta) \geq Q(\theta \mid \theta^{(n)}) + H(\theta^{(n)} \mid \theta^{(n)})$ where $H$ is the entropy of the conditional distribution of the missing data. Since the M-step maximizes $Q$, we have $Q(\theta^{(n+1)} \mid \theta^{(n)}) \geq Q(\theta^{(n)} \mid \theta^{(n)})$, which implies $\ell(\theta^{(n+1)}) \geq \ell(\theta^{(n)})$.

**Convergence criterion.** The algorithm stops when:

$$
|\ell(\theta^{(n+1)}) - \ell(\theta^{(n)})| < \epsilon \qquad \text{or} \qquad \|\theta^{(n+1)} - \theta^{(n)}\| < \delta
$$

Typical values are $\epsilon = 10^{-8}$ and $\delta = 10^{-6}$.

!!! warning "Limitations"
    - EM converges to a **local** maximum (or saddle point), not necessarily the global maximum
    - Convergence can be **slow** near the optimum (linear rate)
    - Multiple starting values are recommended to explore the likelihood surface
    - Standard errors are not directly available --- use the **observed information matrix** or bootstrap

### EM vs Direct MLE

| Criterion | EM Algorithm | Direct MLE (numerical optimization) |
|:----------|:-------------|:------------------------------------|
| Implementation | Simple, closed-form M-step | Requires gradient/Hessian computation |
| Convergence speed | Linear (slow near optimum) | Quadratic (Newton-Raphson) |
| Monotonicity | Guaranteed | Not guaranteed |
| Constraints | Automatically enforced | Must be imposed explicitly |
| Standard errors | Requires separate computation | Available from Hessian |
| Robustness | Less sensitive to starting values | Can diverge from poor starts |

!!! tip "Practical Recommendation"
    A common strategy is to run EM for several iterations to get close to the optimum, then switch to numerical optimization (BFGS or Newton-Raphson) for final refinement and standard error computation. This combines the robustness of EM with the speed and inference capabilities of direct MLE.

---

## Identification and Testing

### The Identification Problem

Markov-switching models face a fundamental identification challenge. Under the null hypothesis of **no regime switching** ($K_0 = 1$ regime), the transition probabilities $p_{ij}$ and the parameters of the additional regimes are **not identified**. This is known as the **Davies problem** (Davies, 1977, 1987).

**Why standard tests fail:** The likelihood ratio statistic

$$
LR = 2[\ell(\hat{\theta}_{K}) - \ell(\hat{\theta}_{K_0})]
$$

does not have the usual $\chi^2$ distribution under $H_0: K = K_0$ because:

1. **Nuisance parameters under $H_0$**: The transition probabilities $p_{ij}$ appear only under $H_1$. Under $H_0$ (single regime), they are absent --- they are nuisance parameters that are not identified under the null.

2. **Boundary of parameter space**: Under $H_0$, certain parameters (e.g., $p_{12} = 0$) are on the boundary of the parameter space, violating the interior-point assumption of standard asymptotic theory.

3. **Non-standard information matrix**: The Fisher information matrix is singular under $H_0$.

### Label Switching

An inherent ambiguity in Markov-switching models is **label switching**: permuting the regime labels (e.g., swapping regimes 1 and 2) with appropriate permutation of transition probabilities yields an **observationally equivalent** model. For $K$ regimes, there are $K!$ equivalent labelings.

**Implications:**

- The likelihood function has (at least) $K!$ symmetric modes
- Maximum likelihood finds one labeling arbitrarily
- Ordering constraints (e.g., $\mu_1 < \mu_2$) are commonly imposed to achieve identification, but these are fragile when distributions overlap

!!! note "Bayesian Approaches"
    In Bayesian estimation, label switching creates multimodal posterior distributions. Solutions include permutation-invariant loss functions (Celeux et al., 2000) and relabeling algorithms (Stephens, 2000).

### Testing for the Number of Regimes

#### Hansen's (1992) Approach

Hansen (1992) proposed a testing framework that addresses the non-standard asymptotics. The key idea is to compute the **supremum of the likelihood ratio** over a grid of the nuisance parameters.

Under $H_0: K = 1$ vs $H_1: K = 2$:

$$
\text{sup-LR} = \sup_{\theta_2} 2[\ell(\hat{\theta}; K=2) - \ell(\hat{\theta}; K=1)]
$$

where the supremum is over the parameters that are unidentified under $H_0$.

**Critical values** are obtained via Hansen's (1996) standardized likelihood ratio bootstrap:

1. Estimate the model under $H_0$
2. Generate $B$ bootstrap samples from the $H_0$ model
3. For each bootstrap sample, compute the sup-LR statistic
4. The p-value is the proportion of bootstrap statistics exceeding the observed sup-LR

!!! warning "Computational Cost"
    This bootstrap procedure is computationally expensive: for each of $B$ bootstrap replications, one must estimate models under both $H_0$ and $H_1$. With $B = 1000$, this requires 2000 model estimations.

#### Garcia's (1998) Approach

Garcia (1998) tabulated asymptotic critical values for testing $H_0: K = 1$ vs $H_1: K = 2$ in specific Markov-switching model classes. The limiting distribution depends on the number of nuisance parameters and which parameters switch.

#### Practical Heuristics

When formal testing is impractical, practitioners rely on:

- **Information criteria** (AIC, BIC, HQIC) comparing models with different $K$
- **Regime classification measure** (RCM): $100 \cdot K^2 \frac{1}{T} \sum_{t=1}^{T} \prod_{j=1}^{K} \hat{\xi}_{t|T}^{(j)}$. Values near 0 indicate sharp classification; values near 100 indicate poor discrimination
- **Ang and Bekaert (2002) criterion**: regimes should have economically meaningful interpretation and sufficient observations

---

## Forecasting

### One-Step-Ahead Forecast

The optimal forecast of $y_{T+1}$ given $\mathcal{Y}_T$ integrates over the regime uncertainty:

$$
E[y_{T+1} \mid \mathcal{Y}_T] = \sum_{j=1}^{K} P(s_{T+1} = j \mid \mathcal{Y}_T) \cdot E[y_{T+1} \mid s_{T+1} = j, \mathcal{Y}_T]
$$

where:

$$
P(s_{T+1} = j \mid \mathcal{Y}_T) = \sum_{i=1}^{K} p_{ij} \cdot P(s_T = i \mid \mathcal{Y}_T)
$$

### Multi-Step Forecasts

For $h$-step-ahead forecasts, iterate the Chapman-Kolmogorov equation:

$$
P(s_{T+h} = j \mid \mathcal{Y}_T) = \left[(P')^h \hat{\xi}_{T|T}\right]_j
$$

As $h \to \infty$, the forecast probabilities converge to the ergodic distribution:

$$
\lim_{h \to \infty} P(s_{T+h} = j \mid \mathcal{Y}_T) = \pi_j
$$

and the forecast converges to the **unconditional mean**:

$$
\lim_{h \to \infty} E[y_{T+h} \mid \mathcal{Y}_T] = \sum_{j=1}^{K} \pi_j \mu_j
$$

---

## References

- Ang, A. and Bekaert, G. (2002). Regime Switches in Interest Rates. *Journal of Business & Economic Statistics*, 20(2), 163--182.
- Davies, R.B. (1977). Hypothesis Testing When a Nuisance Parameter Is Present Only Under the Alternative. *Biometrika*, 64(2), 247--254.
- Dempster, A.P., Laird, N.M., and Rubin, D.B. (1977). Maximum Likelihood from Incomplete Data via the EM Algorithm. *Journal of the Royal Statistical Society: Series B*, 39(1), 1--38.
- Garcia, R. (1998). Asymptotic Null Distribution of the Likelihood Ratio Test in Markov Switching Models. *International Economic Review*, 39(3), 763--788.
- Hamilton, J.D. (1989). A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle. *Econometrica*, 57(2), 357--384.
- Hansen, B.E. (1992). The Likelihood Ratio Test Under Nonstandard Conditions: Testing the Markov Switching Model of GNP. *Journal of Applied Econometrics*, 7(S1), S61--S82.
- Hansen, B.E. (1996). Inference When a Nuisance Parameter Is Not Identified Under the Null Hypothesis. *Econometrica*, 64(2), 413--430.
- Kim, C.-J. (1994). Dynamic Linear Models with Markov-Switching. *Journal of Econometrics*, 60(1--2), 1--22.
- Kim, C.-J. and Nelson, C.R. (1999). *State-Space Models with Regime Switching*. MIT Press.
