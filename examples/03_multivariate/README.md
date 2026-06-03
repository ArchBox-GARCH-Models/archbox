# Multivariate GARCH Models

This module contains examples, tutorials, and cross-validation scripts for
multivariate GARCH models implemented in **archbox**.

## Models Covered

### CCC - Constant Conditional Correlation (Bollerslev, 1990)

The CCC model assumes that conditional correlations between assets are constant
over time, while individual conditional variances follow univariate GARCH
processes. The conditional covariance matrix is decomposed as:

    H_t = D_t R D_t

where D_t = diag(sqrt(h_{1t}), ..., sqrt(h_{kt})) contains the conditional
standard deviations from univariate GARCH models and R is a constant correlation
matrix. The CCC model is computationally efficient and serves as a baseline for
more flexible specifications.

### DCC - Dynamic Conditional Correlation (Engle, 2002)

The DCC model extends CCC by allowing correlations to vary over time. The
correlation dynamics follow:

    Q_t = (1 - a - b) Q_bar + a (e_{t-1} e_{t-1}') + b Q_{t-1}
    R_t = diag(Q_t)^{-1/2} Q_t diag(Q_t)^{-1/2}

where Q_bar is the unconditional correlation matrix and e_t are standardized
residuals. Parameters a and b control the speed of mean reversion and
persistence. DCC is the most widely used multivariate GARCH model in practice.

### BEKK (Engle and Kroner, 1995)

The BEKK model directly parameterizes the conditional covariance matrix:

    H_t = C'C + A' eps_{t-1} eps_{t-1}' A + B' H_{t-1} B

where C is lower triangular and A, B are parameter matrices. The BEKK
representation guarantees positive definiteness of H_t by construction. The
full BEKK model has many parameters (O(k^2) each for A and B), so diagonal
or scalar variants are often used in practice.

### GO-GARCH - Generalized Orthogonal GARCH (van der Weide, 2002)

GO-GARCH decomposes asset returns into uncorrelated factors using a mixing
matrix Z:

    r_t = Z f_t
    f_t ~ (0, diag(h_{1t}, ..., h_{kt}))

where each factor follows a univariate GARCH process. The conditional covariance
matrix is then H_t = Z diag(h_{1t}, ..., h_{kt}) Z'. GO-GARCH reduces the
dimensionality problem by modeling k univariate processes instead of a full
k x k matrix.

### DECO - Dynamic Equicorrelation (Engle and Kelly, 2012)

DECO simplifies DCC by assuming that all pairwise correlations are equal at
each point in time:

    R_t = (1 - rho_t) I_k + rho_t J_k

where rho_t is a scalar equicorrelation that varies over time and J_k is a
matrix of ones. This dramatic dimensionality reduction makes DECO scalable
to very large cross-sections (hundreds of assets) while still capturing the
broad dynamics of correlation.

## Datasets

| File | Description | Dimensions | Seed |
|------|-------------|------------|------|
| `data/fx_majors.csv` | DCC-simulated FX returns (EUR/USD, GBP/USD, JPY/USD, CHF/USD) | 2000 x 5 | 50 |
| `data/sector_indices.csv` | Sector index returns (Technology, Finance, Healthcare, Energy, Consumer) | 2000 x 6 | 51 |

Both datasets are generated with fixed seeds for full reproducibility. See
`utils/data_generator.py` for the simulation methodology.

## Directory Structure

```
03_multivariate/
├── README.md              # This file
├── notebooks/             # Jupyter tutorial notebooks
├── solutions/             # Complete solution notebooks
├── R/                     # R validation scripts (rugarch, rmgarch)
├── Stata/                 # Stata validation scripts (.do files)
├── data/                  # Synthetic datasets
├── utils/                 # Data generators and plot helpers
│   ├── __init__.py
│   ├── data_generator.py
│   ├── generate_datasets.py
│   └── plot_helpers.py
└── outputs/               # Generated figures and tables
```

## References

- Bollerslev, T. (1990). Modelling the Coherence in Short-Run Nominal Exchange Rates: A Multivariate Generalized ARCH Model. *Review of Economics and Statistics*, 72(3), 498-505.
- Engle, R. (2002). Dynamic Conditional Correlation: A Simple Class of Multivariate Generalized Autoregressive Conditional Heteroskedasticity Models. *Journal of Business & Economic Statistics*, 20(3), 339-350.
- Engle, R. and Kroner, K. (1995). Multivariate Simultaneous Generalized ARCH. *Econometric Theory*, 11(1), 122-150.
- van der Weide, R. (2002). GO-GARCH: A Multivariate Generalized Orthogonal GARCH Model. *Journal of Applied Econometrics*, 17(5), 549-564.
- Engle, R. and Kelly, B. (2012). Dynamic Equicorrelation. *Journal of Business & Economic Statistics*, 30(2), 212-228.
