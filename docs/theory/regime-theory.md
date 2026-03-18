# Regime-Switching Models - Theory

## Markov-Switching (Hamilton, 1989)

The model assumes the data-generating process depends on an unobserved regime $s_t$:

$$y_t = \mu_{s_t} + \sum_{i=1}^{p} \phi_{i,s_t} y_{t-i} + \sigma_{s_t} \varepsilon_t$$

### Transition probabilities

$$P(s_t = j | s_{t-1} = i) = p_{ij}$$

### Hamilton filter

The filter computes filtered probabilities $P(s_t | y_1, \ldots, y_t)$ using:

1. **Prediction**: $\hat{\xi}_{t|t-1} = P' \hat{\xi}_{t-1|t-1}$
2. **Update**: $\hat{\xi}_{t|t} \propto \hat{\xi}_{t|t-1} \odot f(y_t | s_t, \mathcal{F}_{t-1})$

### Kim smoother

Backward pass to compute smoothed probabilities $P(s_t | y_1, \ldots, y_T)$.

## References

- Hamilton, J.D. (1989). A New Approach to the Economic Analysis of Nonstationary Time Series.
- Kim, C.-J. (1994). Dynamic Linear Models with Markov-Switching.
