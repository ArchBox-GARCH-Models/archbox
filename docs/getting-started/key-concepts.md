# Key Concepts

## Volatility clustering

Financial returns exhibit **volatility clustering**: large changes tend to be
followed by large changes, and small changes by small changes. GARCH models
capture this phenomenon.

## The GARCH(p,q) model

The general model:

$$r_t = \mu + \varepsilon_t, \quad \varepsilon_t = \sigma_t z_t, \quad z_t \sim D(0,1)$$

$$\sigma^2_t = \omega + \sum_{i=1}^{q} \alpha_i \varepsilon_{t-i}^2 + \sum_{j=1}^{p} \beta_j \sigma^2_{t-j}$$

- **omega**: long-run variance component
- **alpha**: ARCH effect (reaction to shocks)
- **beta**: GARCH effect (persistence)
- **persistence**: alpha + beta (should be < 1 for stationarity)

## Model hierarchy

| Model | Key feature |
|:------|:-----------|
| GARCH | Symmetric volatility response |
| EGARCH | Asymmetric, log-space (no positivity constraint) |
| GJR-GARCH | Asymmetric leverage via indicator function |
| APARCH | Power-transformed asymmetric |
| DCC | Dynamic conditional correlation (multivariate) |
| MS-AR | Regime-switching dynamics |
| SETAR | Threshold autoregressive |

## Estimation

All models are estimated by **Maximum Likelihood Estimation (MLE)** using
SciPy's optimization routines. The log-likelihood depends on the chosen
conditional distribution (Normal, Student-t, Skewed-t, GED).

## Variance targeting

When `variance_targeting=True`, omega is fixed to satisfy:

$$\omega = \hat{\sigma}^2 (1 - \sum \alpha_i - \sum \beta_j)$$

This reduces the parameter space and can improve convergence.
