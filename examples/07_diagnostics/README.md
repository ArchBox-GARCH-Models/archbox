# Module 07: Diagnostic Tests for GARCH Models

This module demonstrates diagnostic tools for validating GARCH-family models.
It covers residual-based tests, parameter stability, and asymmetry diagnostics.

## Concepts

### ARCH-LM Test (Engle 1982)

The ARCH-LM test checks for remaining ARCH effects in model residuals. If the model
is correctly specified, standardized residuals should be free of conditional heteroscedasticity.

The test regresses squared standardized residuals on their lags:

$$\hat{z}_t^2 = \alpha_0 + \alpha_1 \hat{z}_{t-1}^2 + \cdots + \alpha_q \hat{z}_{t-q}^2 + u_t$$

The test statistic is $LM = T \cdot R^2 \sim \chi^2(q)$, where $T$ is the sample size
and $R^2$ is from the auxiliary regression. A significant result indicates the model
has not fully captured the ARCH dynamics.

### Sign Bias Test (Engle-Ng 1993)

The sign bias test checks whether positive and negative shocks affect future volatility
differently, which a symmetric GARCH model cannot capture.

Three regressions are run on standardized residuals $\hat{z}_t$:

1. **Sign bias**: $\hat{z}_t^2 = c + b_1 S_{t-1}^- + u_t$
2. **Negative size bias**: $\hat{z}_t^2 = c + b_2 S_{t-1}^- \epsilon_{t-1} + u_t$
3. **Positive size bias**: $\hat{z}_t^2 = c + b_3 (1 - S_{t-1}^-) \epsilon_{t-1} + u_t$

where $S_{t-1}^- = \mathbb{1}(\epsilon_{t-1} < 0)$. Significant coefficients suggest
an asymmetric model (EGARCH, GJR-GARCH) may be more appropriate.

### Ljung-Box Test

The Ljung-Box test checks for serial correlation in residuals or squared residuals:

$$Q(m) = T(T+2) \sum_{k=1}^{m} \frac{\hat{\rho}_k^2}{T-k} \sim \chi^2(m)$$

Applied to standardized residuals, it tests for remaining autocorrelation in the mean.
Applied to squared standardized residuals, it tests for remaining ARCH effects (similar
to ARCH-LM but using a portmanteau approach).

### Nyblom Stability Test (Nyblom 1989)

The Nyblom test checks whether model parameters are constant over the sample period.
Under the null hypothesis, parameters are fixed; under the alternative, they follow
a random walk.

The test statistic for individual parameter $\theta_i$ is:

$$L_i = \frac{1}{T^2 \hat{V}_{ii}} \sum_{t=1}^{T} \left( \sum_{s=1}^{t} \hat{u}_{si} \right)^2$$

where $\hat{u}_{si}$ are the score contributions and $\hat{V}_{ii}$ is the corresponding
element of the variance matrix. A joint test statistic tests all parameters simultaneously.

Structural breaks, regime changes, or gradual parameter drift will lead to rejection.

### News Impact Curve (Engle-Ng 1993)

The news impact curve (NIC) visualizes how a shock at time $t-1$ affects the conditional
variance at time $t$, holding all other information constant.

For GARCH(1,1): $\sigma_t^2 = \omega + \alpha \epsilon_{t-1}^2 + \beta \bar{\sigma}^2$ (symmetric parabola)

For GJR-GARCH: $\sigma_t^2 = \omega + (\alpha + \gamma \mathbb{1}_{\epsilon<0}) \epsilon_{t-1}^2 + \beta \bar{\sigma}^2$ (asymmetric parabola)

For EGARCH: $\ln \sigma_t^2 = \omega + \alpha |z_{t-1}| + \gamma z_{t-1} + \beta \ln \bar{\sigma}^2$ (asymmetric exponential)

Comparing NIC across models reveals which captures asymmetric responses best.

## Datasets

- **sp500_returns.csv**: 2500 synthetic S&P 500 daily returns (GARCH(1,1), seed=42)
- **misspecified_returns.csv**: 2500 returns from EGARCH DGP (seed=70) - exhibits sign bias when fitted with symmetric GARCH
- **structural_break_returns.csv**: 2500 returns with structural break at midpoint (seed=71) - detectable by Nyblom test

All datasets are generated with fixed seeds for reproducibility.

## Structure

```
07_diagnostics/
├── README.md              # This file
├── notebooks/             # Jupyter tutorial notebooks
├── solutions/             # Complete solution notebooks
├── R/                     # R validation scripts
├── Stata/                 # Stata validation scripts
├── data/                  # CSV datasets
│   └── sp500_returns.csv
├── utils/                 # Python utilities
│   ├── __init__.py
│   ├── data_generator.py  # Synthetic data generators
│   ├── generate_datasets.py  # Script to regenerate CSVs
│   └── plot_helpers.py    # Visualization functions
└── outputs/               # Saved figures and results
```

## References

- Engle, R.F. (1982). Autoregressive Conditional Heteroscedasticity with Estimates of the Variance of United Kingdom Inflation. *Econometrica*, 50(4), 987-1007.
- Engle, R.F. & Ng, V.K. (1993). Measuring and Testing the Impact of News on Volatility. *Journal of Finance*, 48(5), 1749-1778.
- Ljung, G.M. & Box, G.E.P. (1978). On a Measure of Lack of Fit in Time Series Models. *Biometrika*, 65(2), 297-303.
- Nyblom, J. (1989). Testing for the Constancy of Parameters Over Time. *Journal of the American Statistical Association*, 84(405), 223-230.
- Nelson, D.B. (1991). Conditional Heteroskedasticity in Asset Returns: A New Approach. *Econometrica*, 59(2), 347-370.
