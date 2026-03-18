# Multivariate GARCH - Theory

## DCC (Engle, 2002)

The Dynamic Conditional Correlation model decomposes the conditional covariance:

$$H_t = D_t R_t D_t$$

where $D_t = \text{diag}(\sigma_{1,t}, \ldots, \sigma_{k,t})$ and $R_t$ is the dynamic
correlation matrix.

### DCC dynamics

$$Q_t = (1 - a - b) \bar{Q} + a (z_{t-1} z'_{t-1}) + b Q_{t-1}$$

$$R_t = \text{diag}(Q_t)^{-1/2} Q_t \text{diag}(Q_t)^{-1/2}$$

## CCC (Bollerslev, 1990)

The Constant Conditional Correlation model assumes $R_t = R$ (constant).

## BEKK (Engle & Kroner, 1995)

$$H_t = C'C + A' \varepsilon_{t-1} \varepsilon'_{t-1} A + B' H_{t-1} B$$

## References

- Engle, R.F. (2002). Dynamic Conditional Correlation.
- Bollerslev, T. (1990). Modelling the Coherence in Short-Run Nominal Exchange Rates.
- Engle, R.F. & Kroner, K.F. (1995). Multivariate Simultaneous Generalized ARCH.
