---
title: "Multivariate GARCH Theory"
description: "Mathematical foundations of multivariate GARCH models: vech representation, positive-definiteness, BEKK, DCC, CCC, two-step estimation, and asymptotic theory"
---

# Multivariate GARCH --- Theoretical Foundations

!!! abstract "Key Takeaway"
    Multivariate GARCH models capture **time-varying covariances and correlations** between multiple financial assets. The central challenge is ensuring the conditional covariance matrix $H_t$ remains **positive-definite** at every time step while keeping the number of parameters manageable. This page covers the vech representation, the dimensionality problem, and three major approaches: BEKK (positive-definiteness by construction), DCC (by decomposition), and CCC (by restriction). We detail the two-step estimation procedure and its asymptotic properties.

---

## Motivation

### Why Multivariate Volatility?

In portfolio management and risk analysis, we need not only individual asset volatilities but also their **dynamic co-movements**. Consider a portfolio of $k$ assets with weight vector $w$:

$$
\sigma_{p,t}^2 = w' H_t w
$$

where $H_t$ is the $k \times k$ conditional covariance matrix. Key applications include:

- **Portfolio optimization** under time-varying risk
- **Value-at-Risk** for multi-asset positions
- **Hedge ratios** that adapt to changing correlations
- **Contagion analysis** and spillover measurement

!!! info "Empirical Motivation"
    Correlations between financial assets are **not constant**. They tend to increase during market crises (correlation breakdown) and decrease during calm periods. Models that assume constant correlations can severely underestimate portfolio risk during stress episodes.

### The General Multivariate GARCH

Let $\mathbf{r}_t = (\mathbf{r}_{1,t}, \ldots, \mathbf{r}_{k,t})'$ be a $k$-vector of returns with:

$$
\mathbf{r}_t = \boldsymbol{\mu}_t + \boldsymbol{\varepsilon}_t, \qquad \boldsymbol{\varepsilon}_t = H_t^{1/2} \mathbf{z}_t, \qquad \mathbf{z}_t \overset{\text{iid}}{\sim} D(\mathbf{0}, I_k)
$$

where $H_t = \text{Var}(\boldsymbol{\varepsilon}_t | \mathcal{F}_{t-1})$ is the conditional covariance matrix. The challenge: specifying the dynamics of $H_t$ such that:

1. $H_t$ is **positive-definite** for all $t$ and all parameter values
2. The number of parameters remains **tractable**
3. The model is **estimable** with available data

---

## The vech Representation and Dimensionality

### The vech Operator

The **vech** (half-vectorization) operator stacks the lower-triangular elements of a symmetric $k \times k$ matrix into a vector of dimension $k^* = k(k+1)/2$:

$$
\text{vech}(H_t) = (h_{11,t}, h_{21,t}, h_{22,t}, h_{31,t}, \ldots, h_{kk,t})'
$$

For example, with $k = 3$:

$$
H_t = \begin{pmatrix} h_{11} & h_{12} & h_{13} \\ h_{12} & h_{22} & h_{23} \\ h_{13} & h_{23} & h_{33} \end{pmatrix} \implies \text{vech}(H_t) = \begin{pmatrix} h_{11} \\ h_{12} \\ h_{22} \\ h_{13} \\ h_{23} \\ h_{33} \end{pmatrix}
$$

### The General VEC Model

The most general multivariate GARCH(1,1), the **VEC model** (Bollerslev, Engle, and Wooldridge, 1988), specifies:

$$
\text{vech}(H_t) = \mathbf{c} + A \, \text{vech}(\boldsymbol{\varepsilon}_{t-1}\boldsymbol{\varepsilon}_{t-1}') + B \, \text{vech}(H_{t-1})
$$

where $\mathbf{c}$ is a $k^* \times 1$ vector and $A, B$ are $k^* \times k^*$ matrices.

### The Curse of Dimensionality

The number of parameters in the unrestricted VEC model grows rapidly:

| $k$ (assets) | $k^*$ | Parameters in $A$ and $B$ | Total |
|:---:|:---:|:---:|:---:|
| 2 | 3 | $2 \times 9 = 18$ | 21 |
| 5 | 15 | $2 \times 225 = 450$ | 465 |
| 10 | 55 | $2 \times 3{,}025 = 6{,}050$ | 6,105 |
| 50 | 1,275 | $2 \times 1{,}625{,}625$ | $> 3.2 \times 10^6$ |

!!! warning "Impractical for Large $k$"
    With just 10 assets, the unrestricted VEC has over 6,000 parameters. Moreover, there is no guarantee that $H_t$ will be positive-definite. This motivates restricted parameterizations.

---

## Positive-Definiteness

### Why It Matters

The conditional covariance matrix $H_t$ **must** be positive-definite (PD) at every time step because:

1. **Mathematical requirement**: Variances must be positive ($h_{ii,t} > 0$) and the covariance matrix must define a valid probability distribution
2. **Portfolio variance**: $\sigma_{p,t}^2 = w'H_t w > 0$ for all non-zero $w$ requires PD
3. **Likelihood evaluation**: The Gaussian log-likelihood involves $\ln|H_t|$ and $H_t^{-1}$, both requiring PD

### How Each Model Guarantees PD

=== "BEKK --- By Construction"

    The BEKK parameterization uses **quadratic forms** that are PD by construction:

    $$
    H_t = C'C + A' \boldsymbol{\varepsilon}_{t-1}\boldsymbol{\varepsilon}_{t-1}' A + B' H_{t-1} B
    $$

    - $C'C$ is PD if $C$ is lower-triangular with positive diagonal
    - $A' \boldsymbol{\varepsilon}_{t-1}\boldsymbol{\varepsilon}_{t-1}' A$ is positive semi-definite (PSD) for any $A$
    - $B' H_{t-1} B$ is PSD if $H_{t-1}$ is PD
    - **Sum of PD + PSD + PSD = PD**

    No parameter constraints beyond the structure of $C$ are needed.

=== "DCC --- By Decomposition"

    DCC **decomposes** the covariance into volatilities and correlations:

    $$
    H_t = D_t R_t D_t
    $$

    where $D_t = \text{diag}(\sigma_{1,t}, \ldots, \sigma_{k,t})$ with each $\sigma_{i,t} > 0$ from univariate GARCH, and $R_t$ is a **valid correlation matrix** (PD with unit diagonal).

    - $D_t$ is PD (positive diagonal)
    - $R_t$ is PD (guaranteed by construction via $Q_t$ normalization)
    - $H_t = D_t R_t D_t$ is PD as a congruence transformation of PD matrices

=== "CCC --- By Restriction"

    CCC assumes a **constant** correlation matrix $R$:

    $$
    H_t = D_t R D_t
    $$

    $R$ is estimated as the sample correlation of standardized residuals, which is PD almost surely for $T > k$. The restriction $R_t = R$ trivially maintains PD if the initial estimate is PD.

### Numerical Verification

In practice, numerical errors can erode positive-definiteness. archbox employs:

1. **Eigenvalue check**: Verify $\lambda_{\min}(H_t) > \epsilon$ for a small tolerance $\epsilon > 0$
2. **Cholesky factorization**: If $H_t = LL'$ succeeds, $H_t$ is PD
3. **Regularization**: If PD is violated, replace $H_t \leftarrow H_t + \epsilon I_k$

---

## CCC: Constant Conditional Correlation (Bollerslev, 1990)

### Specification

$$
H_t = D_t R D_t
$$

where:

- $D_t = \text{diag}(\sigma_{1,t}, \ldots, \sigma_{k,t})$ with each $\sigma_{i,t}^2$ following a univariate GARCH
- $R$ is a constant $k \times k$ positive-definite correlation matrix

### Estimation

1. Estimate $k$ univariate GARCH models to obtain $\hat{\sigma}_{i,t}$
2. Compute standardized residuals: $\hat{z}_{i,t} = \varepsilon_{i,t} / \hat{\sigma}_{i,t}$
3. Estimate $R$ as the sample correlation of $\hat{\mathbf{z}}_t$:

$$
\hat{R} = \frac{1}{T}\sum_{t=1}^{T} \hat{\mathbf{z}}_t \hat{\mathbf{z}}_t'
$$

### Limitations

The assumption of constant correlations is strong and frequently rejected by formal tests (Engle and Sheppard, 2001). CCC serves as a useful **baseline** and **building block** for DCC.

---

## DCC: Dynamic Conditional Correlation (Engle, 2002)

### Specification

The DCC model extends CCC by allowing the correlation matrix to vary over time:

$$
H_t = D_t R_t D_t
$$

The correlation dynamics are specified through a proxy process $Q_t$:

$$
Q_t = (1 - a - b)\bar{Q} + a(\mathbf{z}_{t-1}\mathbf{z}_{t-1}') + b Q_{t-1}
$$

where:

- $\bar{Q} = E[\mathbf{z}_t \mathbf{z}_t']$ is the unconditional correlation of standardized residuals
- $a \geq 0$, $b \geq 0$, $a + b < 1$

The correlation matrix is obtained by normalizing $Q_t$:

$$
R_t = \text{diag}(Q_t)^{-1/2} \, Q_t \, \text{diag}(Q_t)^{-1/2}
$$

This ensures $R_t$ has unit diagonal and is PD whenever $Q_t$ is PD.

??? note "Why $R_t$ is a Valid Correlation Matrix"
    Let $q_{ii,t}$ denote the $i$-th diagonal element of $Q_t$. Then:

    $$
    r_{ij,t} = \frac{q_{ij,t}}{\sqrt{q_{ii,t} q_{jj,t}}}
    $$

    By Cauchy-Schwarz, $|r_{ij,t}| \leq 1$, and $r_{ii,t} = 1$. Since $Q_t$ is PD (as a convex combination of PD and PSD matrices), its normalization $R_t$ is also PD.

### Two-Step Estimation

The key computational advantage of DCC is that it can be estimated in **two steps**:

#### Step 1: Univariate GARCH

Estimate $k$ separate univariate GARCH models by MLE. For each asset $i$:

$$
\hat{\theta}_i = \arg\max_{\theta_i} \sum_{t=1}^{T} \ell_{i,t}(\theta_i)
$$

where $\ell_{i,t}$ is the univariate Gaussian log-likelihood:

$$
\ell_{i,t}(\theta_i) = -\frac{1}{2}\left[\ln(2\pi) + \ln(\sigma_{i,t}^2) + \frac{\varepsilon_{i,t}^2}{\sigma_{i,t}^2}\right]
$$

Compute standardized residuals: $\hat{z}_{i,t} = \varepsilon_{i,t} / \hat{\sigma}_{i,t}$.

#### Step 2: Correlation Parameters

Given the standardized residuals from Step 1, estimate the DCC parameters $(a, b)$ by maximizing the **correlation log-likelihood**:

$$
\ell_C(a, b) = -\frac{1}{2}\sum_{t=1}^{T}\left[k\ln(2\pi) + 2\ln|D_t| + \ln|R_t| + \mathbf{z}_t' R_t^{-1} \mathbf{z}_t\right]
$$

Since $D_t$ is fixed from Step 1, this simplifies to:

$$
\ell_C(a, b) \propto -\frac{1}{2}\sum_{t=1}^{T}\left[\ln|R_t(a,b)| + \mathbf{z}_t' R_t^{-1}(a,b) \mathbf{z}_t - \mathbf{z}_t'\mathbf{z}_t\right]
$$

!!! tip "Computational Advantage"
    Two-step estimation reduces a problem with $O(k)$ parameters in a single optimization to $k$ small univariate problems plus one 2-parameter optimization. For $k = 50$ assets, this is the difference between estimating ~50 parameters jointly vs. 50 separate 3-parameter problems + 1 two-parameter problem.

### Efficiency vs Consistency

| Property | Two-Step DCC | Full MLE |
|:---|:---:|:---:|
| **Consistency** | Yes | Yes |
| **Asymptotic normality** | Yes | Yes |
| **Efficiency** | Lower (ignores cross-equation info) | Optimal |
| **Computational cost** | $O(k)$ | $O(k^2)$ to $O(k^3)$ |
| **Feasibility for large $k$** | Yes | Often infeasible |

The two-step estimator is **consistent** but not fully efficient. Engle (2002) shows that the efficiency loss is typically small, making the two-step approach dominant in practice.

---

## BEKK (Engle and Kroner, 1995)

### Specification

The BEKK(1,1,K) model is:

$$
H_t = C'C + \sum_{n=1}^{K} A_n' \boldsymbol{\varepsilon}_{t-1}\boldsymbol{\varepsilon}_{t-1}' A_n + \sum_{n=1}^{K} B_n' H_{t-1} B_n
$$

The scalar BEKK ($K=1$ with $A = a I_k$, $B = b I_k$) reduces to:

$$
H_t = C'C + a^2 \boldsymbol{\varepsilon}_{t-1}\boldsymbol{\varepsilon}_{t-1}' + b^2 H_{t-1}
$$

### Parameter Count

For the full BEKK(1,1,1):

| Component | Parameters |
|:---|:---:|
| $C$ (lower triangular) | $k(k+1)/2$ |
| $A$ (unrestricted $k \times k$) | $k^2$ |
| $B$ (unrestricted $k \times k$) | $k^2$ |
| **Total** | $k(k+1)/2 + 2k^2$ |

For $k = 5$: 65 parameters. For $k = 10$: 255 parameters.

### Stationarity Condition

The BEKK(1,1,1) is covariance-stationary if all eigenvalues of $A \otimes A + B \otimes B$ have modulus less than 1:

$$
\rho(A \otimes A + B \otimes B) < 1
$$

where $\otimes$ denotes the Kronecker product and $\rho(\cdot)$ is the spectral radius.

??? note "Derivation"
    Applying the vech operator and using the relationship $\text{vech}(X'YX) = (X \otimes X)' \text{vech}(Y)$ for the appropriate duplication/elimination matrices, the BEKK can be written in VEC form:

    $$
    \text{vech}(H_t) = \text{vech}(C'C) + \mathcal{A} \, \text{vech}(\boldsymbol{\varepsilon}_{t-1}\boldsymbol{\varepsilon}_{t-1}') + \mathcal{B} \, \text{vech}(H_{t-1})
    $$

    where $\mathcal{A}$ and $\mathcal{B}$ are functions of $A \otimes A$ and $B \otimes B$. Stationarity requires $\rho(\mathcal{A} + \mathcal{B}) < 1$, which corresponds to $\rho(A \otimes A + B \otimes B) < 1$.

### Unconditional Covariance

Under stationarity, the unconditional covariance is:

$$
\text{vech}(\bar{H}) = (I_{k^*} - \mathcal{A} - \mathcal{B})^{-1} \text{vech}(C'C)
$$

### Estimation

BEKK is estimated by **full MLE** maximizing:

$$
\ell(\theta) = -\frac{T}{2} k\ln(2\pi) - \frac{1}{2}\sum_{t=1}^{T}\left[\ln|H_t| + \boldsymbol{\varepsilon}_t' H_t^{-1} \boldsymbol{\varepsilon}_t\right]
$$

!!! warning "Computational Cost"
    Full BEKK requires inverting and computing the determinant of $H_t$ at each time step, costing $O(Tk^3)$. For large $k$, DCC is strongly preferred.

---

## GO-GARCH (van der Weide, 2002)

### Concept

The Generalized Orthogonal GARCH decomposes multivariate volatility through **independent factors**:

$$
\boldsymbol{\varepsilon}_t = Z \mathbf{f}_t
$$

where $Z$ is a $k \times k$ mixing matrix and $\mathbf{f}_t$ contains independent factors, each following a univariate GARCH:

$$
H_t = Z \, \Lambda_t \, Z'
$$

with $\Lambda_t = \text{diag}(\sigma_{f_1,t}^2, \ldots, \sigma_{f_k,t}^2)$.

**Positive-definiteness** is guaranteed since $\Lambda_t$ has positive diagonal entries and $Z$ is full rank.

---

## Asymptotic Theory

### Consistency

Under regularity conditions (correct specification, interior parameter values, finite fourth moments):

$$
\hat{\theta} \xrightarrow{p} \theta_0 \quad \text{as } T \to \infty
$$

This holds for both full MLE and the two-step estimator.

### Asymptotic Normality

#### Full MLE

$$
\sqrt{T}(\hat{\theta} - \theta_0) \xrightarrow{d} N\left(\mathbf{0}, \mathcal{I}(\theta_0)^{-1}\right)
$$

where $\mathcal{I}(\theta_0) = -E\left[\frac{\partial^2 \ell_t}{\partial \theta \partial \theta'}\right]$ is the Fisher information matrix.

#### Two-Step DCC

For the two-step DCC estimator, Engle (2002) and Engle and Sheppard (2001) show:

$$
\sqrt{T}(\hat{\phi} - \phi_0) \xrightarrow{d} N\left(\mathbf{0}, V_\phi\right)
$$

where $\hat{\phi} = (a, b)'$ and the asymptotic variance accounts for the estimation error from Step 1:

$$
V_\phi = \left(\frac{\partial^2 \ell_C}{\partial \phi \partial \phi'}\right)^{-1} \Sigma_\phi \left(\frac{\partial^2 \ell_C}{\partial \phi \partial \phi'}\right)^{-1}
$$

The matrix $\Sigma_\phi$ includes a correction term for the **generated regressors** problem:

$$
\Sigma_\phi = \text{Var}\left(\frac{\partial \ell_C}{\partial \phi}\right) + \text{Cov}\left(\frac{\partial \ell_C}{\partial \phi}, \frac{\partial \ell_1}{\partial \theta_1}\right) V_{\theta_1}^{-1} \text{Cov}\left(\frac{\partial \ell_1}{\partial \theta_1}, \frac{\partial \ell_C}{\partial \phi}\right)
$$

where $\ell_1$ is the Step 1 likelihood and $V_{\theta_1}$ is the asymptotic variance of the Step 1 estimator.

!!! note "Practical Implication"
    Ignoring the Step 1 estimation error leads to **understated** standard errors for the DCC parameters. archbox computes the full sandwich correction by default.

### Robust Standard Errors for Two-Step

Following the Bollerslev-Wooldridge approach for the multivariate case:

$$
\text{Var}(\hat{\theta}) = J^{-1} I J^{-1}
$$

where now:

$$
J = \frac{1}{T}\sum_{t=1}^{T} \frac{\partial^2 \ell_t}{\partial \theta \partial \theta'}, \qquad I = \frac{1}{T}\sum_{t=1}^{T} \frac{\partial \ell_t}{\partial \theta} \frac{\partial \ell_t}{\partial \theta'}
$$

For the DCC two-step case, $\theta$ is partitioned as $(\theta_1', \phi')'$ and the block structure of $J$ and $I$ is exploited for computational efficiency.

---

## Model Comparison Summary

| Model | PD Guarantee | Parameters ($k=5$) | Estimation | Dynamic Correlations |
|:---:|:---:|:---:|:---:|:---:|
| VEC | None | 465 | Full MLE | Yes |
| BEKK | By construction | 65 | Full MLE | Yes |
| CCC | By restriction | $5 \times 3 + 10 = 25$ | Two-step | No |
| DCC | By decomposition | $5 \times 3 + 10 + 2 = 27$ | Two-step | Yes |
| GO-GARCH | By construction | $5 \times 3 + 10 = 25$ | Two-step | Yes |

!!! tip "Choosing a Model"
    - **CCC**: Baseline model; use when correlations are stable
    - **DCC**: Default choice for most applications; good balance of flexibility and parsimony
    - **BEKK**: When cross-asset volatility spillovers are of primary interest
    - **GO-GARCH**: When factor-based decomposition is desired

---

## References

- Bollerslev, T. (1990). Modelling the coherence in short-run nominal exchange rates: a multivariate generalized ARCH model. _Review of Economics and Statistics_, 72(3), 498--505.
- Bollerslev, T., Engle, R.F., & Wooldridge, J.M. (1988). A capital asset pricing model with time-varying covariances. _Journal of Political Economy_, 96(1), 116--131.
- Engle, R.F. (2002). Dynamic conditional correlation: a simple class of multivariate generalized autoregressive conditional heteroskedasticity models. _Journal of Business & Economic Statistics_, 20(3), 339--350.
- Engle, R.F., & Kroner, K.F. (1995). Multivariate simultaneous generalized ARCH. _Econometric Theory_, 11(1), 122--150.
- Engle, R.F., & Sheppard, K. (2001). Theoretical and empirical properties of dynamic conditional correlation multivariate GARCH. _NBER Working Paper_ No. 8554.
- van der Weide, R. (2002). GO-GARCH: a multivariate generalized orthogonal GARCH model. _Journal of Applied Econometrics_, 17(5), 549--564.
