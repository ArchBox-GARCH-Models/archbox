# Risk Measures - Theory

## Value at Risk (VaR)

$$\text{VaR}_\alpha = \inf\{x : P(L > x) \leq 1 - \alpha\}$$

### Methods

1. **Parametric**: $\text{VaR}_\alpha = \mu_t + \sigma_t \cdot q_\alpha(D)$
2. **Historical Simulation**: empirical quantile of returns
3. **Filtered Historical Simulation**: empirical quantile of standardized residuals, rescaled
4. **Monte Carlo**: simulation-based quantile

## Expected Shortfall (ES)

$$\text{ES}_\alpha = E[L | L > \text{VaR}_\alpha]$$

## Backtesting

### Kupiec test (1995)

Tests if violation rate matches expected rate:

$$LR_{uc} = -2 \log\frac{\alpha^n (1-\alpha)^{T-n}}{\hat{p}^n (1-\hat{p})^{T-n}} \sim \chi^2(1)$$

### Christoffersen test (1998)

Tests independence of violations (no clustering).

### Basel traffic light

| Zone | Violations (at 99%) | Action |
|:-----|:--------------------|:-------|
| Green | 0-4 | No action |
| Yellow | 5-9 | Increase capital |
| Red | 10+ | Regulatory action |

## References

- Kupiec, P.H. (1995). Techniques for Verifying the Accuracy of Risk Measurement Models.
- Christoffersen, P. (1998). Evaluating Interval Forecasts.
- Basel Committee on Banking Supervision (2006). International Convergence of Capital Measurement.
