# GARCH Models - Theory

## ARCH Model (Engle, 1982)

The Autoregressive Conditional Heteroskedasticity (ARCH) model:

$$r_t = \mu + \varepsilon_t, \quad \varepsilon_t = \sigma_t z_t, \quad z_t \sim D(0,1)$$

$$\sigma^2_t = \omega + \sum_{i=1}^{q} \alpha_i \varepsilon^2_{t-i}$$

## GARCH Model (Bollerslev, 1986)

The Generalized ARCH model adds lagged conditional variance:

$$\sigma^2_t = \omega + \sum_{i=1}^{q} \alpha_i \varepsilon^2_{t-i} + \sum_{j=1}^{p} \beta_j \sigma^2_{t-j}$$

### Stationarity condition

$$\sum_{i=1}^{q} \alpha_i + \sum_{j=1}^{p} \beta_j < 1$$

### Unconditional variance

$$E[\sigma^2_t] = \frac{\omega}{1 - \sum \alpha_i - \sum \beta_j}$$

## EGARCH (Nelson, 1991)

$$\log(\sigma^2_t) = \omega + \alpha(|z_{t-1}| - E|z|) + \gamma z_{t-1} + \beta \log(\sigma^2_{t-1})$$

## GJR-GARCH (Glosten et al., 1993)

$$\sigma^2_t = \omega + (\alpha + \gamma I_{t-1}) \varepsilon^2_{t-1} + \beta \sigma^2_{t-1}$$

## APARCH (Ding et al., 1993)

$$\sigma^\delta_t = \omega + \alpha(|\varepsilon_{t-1}| - \gamma \varepsilon_{t-1})^\delta + \beta \sigma^\delta_{t-1}$$

## References

- Bollerslev, T. (1986). Generalized Autoregressive Conditional Heteroskedasticity.
- Engle, R.F. (1982). Autoregressive Conditional Heteroscedasticity.
- Nelson, D.B. (1991). Conditional Heteroskedasticity in Asset Returns.
- Glosten, L.R., Jagannathan, R., & Runkle, D.E. (1993). On the Relation between Expected Value and Volatility.
- Ding, Z., Granger, C.W.J., & Engle, R.F. (1993). A Long Memory Property of Stock Market Returns.
