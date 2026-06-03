---
title: "GO-GARCH"
description: "Generalized Orthogonal GARCH — reducao de dimensionalidade via fatores ortogonais latentes."
---

# GO-GARCH (Generalized Orthogonal GARCH)

!!! info "Quick Reference"
    **Class:** `archbox.multivariate.GOGARCH`
    **Import:** `from archbox.multivariate import GOGARCH`
    **R equivalent:** `rmgarch::gogarchspec(mean.model = "constant")`
    **Python equivalent:** Nao disponivel no pacote `arch`

## Overview

O modelo GO-GARCH (Generalized Orthogonal GARCH), proposto por **van der Weide (2002)**, resolve o problema da dimensionalidade nos modelos multivariados de uma forma elegante: em vez de modelar diretamente a matriz de covariancia $k \times k$, ele decompoe os retornos em **fatores ortogonais (independentes)** e aplica GARCH univariado a cada fator separadamente.

A ideia e inspirada na Analise de Componentes Independentes (ICA):

1. Encontrar uma transformacao linear que mapeie os retornos para fatores independentes
2. Modelar a volatilidade de cada fator com GARCH univariado
3. Reconstruir a covariancia condicional $H_t$ a partir das volatilidades dos fatores

Isso reduz o problema de estimar uma matriz $k \times k$ para estimar $k$ modelos GARCH(1,1) independentes, com custo computacional essencialmente linear em $k$.

**Quando usar:**

- Numero moderado de ativos (5-20) onde DCC pode ser simplista
- Quando ha fatores de risco latentes subjacentes (setores, regioes, fatores macro)
- Reducao de dimensionalidade quando a estrutura fatorial e plausivel
- Comparacao com modelos de fatores em financas

## Formulacao Matematica

### Decomposicao em Fatores

Os retornos sao decompostos como:

$$\epsilon_t = Z \, f_t$$

onde:

| Simbolo | Descricao |
|---------|-----------|
| $\epsilon_t$ | Vetor de retornos (demeaned) $(k \times 1)$ |
| $Z$ | Matriz de mistura (mixing matrix) $(k \times k)$ |
| $f_t$ | Vetor de fatores ortogonais independentes $(k \times 1)$ |

### Ortogonalidade

Os fatores sao **estatisticamente independentes** (nao apenas nao correlacionados):

$$E[f_t f_t'] = \Lambda_t = \text{diag}(h_{1,t}, \ldots, h_{k,t})$$

onde cada $h_{i,t}$ e a variancia condicional do fator $i$.

### GARCH nos Fatores

Cada fator $f_{i,t}$ segue um GARCH(1,1) independente:

$$h_{i,t} = \omega_i + \alpha_i f_{i,t-1}^2 + \beta_i h_{i,t-1}, \quad i = 1, \ldots, k$$

### Reconstrucao da Covariancia

A covariancia condicional dos retornos originais e:

$$H_t = Z \, \Lambda_t \, Z'$$

Substituindo:

$$H_t = Z \, \text{diag}(h_{1,t}, \ldots, h_{k,t}) \, Z'$$

!!! note "Intuicao"
    A covariancia entre os retornos varia ao longo do tempo apenas porque as **variancias dos fatores** $h_{i,t}$ variam. A **estrutura de mistura** $Z$ e fixa. Isso e analogo a ter fatores de risco cujas contribuicoes mudam de intensidade.

### Estimacao via ICA

A matriz de mistura $Z$ e estimada usando **Independent Component Analysis (ICA)**:

1. Branqueamento (whitening): $\tilde{\epsilon}_t = \Sigma^{-1/2} \epsilon_t$
2. Rotacao ICA: encontrar $W$ tal que $f_t = W \tilde{\epsilon}_t$ sejam maximamente independentes
3. Matriz de mistura: $Z = \Sigma^{1/2} W^{-1}$

### Numero de Parametros

| Componente | Parametros |
|------------|:---:|
| Matriz de mistura $Z$ | Estimada por ICA (nao otimizada por MLE) |
| GARCH por fator | $3k$ (para GARCH(1,1)) |
| **Total otimizado** | $3k$ |

Comparacao para $k = 10$: BEKK Full = 255, DCC = 32, GO-GARCH = 30.

## Quick Example

```python
import numpy as np
from archbox.multivariate import GOGARCH
from archbox.datasets import load_dataset

# Carregar retornos de portfolio
returns = load_dataset('equity_portfolio')
endog = returns[['PETR4', 'VALE3', 'ITUB4', 'BBDC4', 'ABEV3']].values

# Estimar GO-GARCH
model = GOGARCH(endog, univariate_model="GARCH", univariate_order=(1, 1))
results = model.fit()
print(results.summary())
```

??? example "Output esperado"
    ```
    ======================================================================
              Multivariate Volatility Model Results - GO-GARCH
    ======================================================================
    Model:            GO-GARCH(1,1)
    Method:           ICA + Univariate GARCH
    Series:           5
    Components:       5
    Observations:     2000
    Log-Likelihood:   12345.6789
    AIC:              -24661.3578
    BIC:              -24577.4567

    Mixing Matrix Z
    ----------------------------------------------------------------------
          F1       F2       F3       F4       F5
    S0    0.423   -0.312    0.156    0.087   -0.045
    S1    0.387    0.298   -0.234    0.123    0.067
    S2    0.156   -0.087    0.456   -0.312    0.198
    S3    0.298    0.156    0.123    0.456   -0.234
    S4    0.087    0.423   -0.087    0.067    0.456

    Factor GARCH Results
    ----------------------------------------------------------------------
    Factor 0: omega=2.3e-05, alpha=0.1234, beta=0.8567
    Factor 1: omega=1.8e-05, alpha=0.0945, beta=0.8912
    Factor 2: omega=1.2e-05, alpha=0.0712, beta=0.9134
    Factor 3: omega=9.8e-06, alpha=0.0634, beta=0.9245
    Factor 4: omega=5.6e-06, alpha=0.0523, beta=0.9378
    ======================================================================
    ```

## Guia Detalhado

### Parametros do Construtor

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | ndarray $(T, k)$ | obrigatorio | Matriz de retornos |
| `n_components` | int | `None` | Numero de fatores (default: $k$) |
| `univariate_model` | str | `"GARCH"` | Modelo GARCH para cada fator |
| `univariate_order` | tuple | `(1, 1)` | Ordem $(p, q)$ do GARCH |

### Parametros de `fit()`

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `method` | str | `"two_step"` | Metodo de estimacao |
| `disp` | bool | `True` | Exibir progresso |

### Acessando Fatores e Mixing Matrix

```python
# Matriz de mistura Z
Z = model.mixing_matrix
print("Mixing matrix Z:")
print(Z)

# Fatores independentes
factors = model.factors  # shape: (T, k)
print(f"Fatores shape: {factors.shape}")

# Verificar independencia dos fatores
corr_factors = np.corrcoef(factors.T)
print("Correlacao entre fatores (deve ser ~identidade):")
print(np.round(corr_factors, 3))
```

### Reducao de Dimensionalidade

```python
# Usar menos componentes que series (opcional)
model_reduced = GOGARCH(endog, n_components=3)  # 3 fatores para 5 series
results_reduced = model_reduced.fit()

# Comparar variancia explicada
print(f"GO-GARCH completo  AIC: {results.aic:.4f}")
print(f"GO-GARCH reduzido  AIC: {results_reduced.aic:.4f}")
```

### Portfolio com GO-GARCH

```python
import numpy as np
from archbox.multivariate.portfolio import (
    portfolio_volatility,
    minimum_variance_weights_dynamic,
    risk_decomposition
)

# Covariancia condicional H_t = Z * diag(h_t) * Z'
H_t = results.dynamic_covariance

# Volatilidade do portfolio equal-weighted
k = endog.shape[1]
weights = np.ones(k) / k
port_vol = portfolio_volatility(weights, H_t)
print(f"Volatilidade media do portfolio: {port_vol.mean():.4f}")

# Pesos otimos dinamicos
mvp_weights = minimum_variance_weights_dynamic(H_t)
print(f"Pesos MVP (ultimo dia): {np.round(mvp_weights[-1], 4)}")

# Decomposicao de risco
decomp = risk_decomposition(weights, H_t[-1])
print(f"Contribuicao de risco: {np.round(decomp['risk_contribution'], 4)}")
```

## Interpretacao

### Mixing Matrix

A matriz de mistura $Z$ revela como os fatores latentes contribuem para cada serie:

```python
import pandas as pd

Z = model.mixing_matrix
names = ['PETR4', 'VALE3', 'ITUB4', 'BBDC4', 'ABEV3']
factors = [f'F{i+1}' for i in range(Z.shape[1])]

df_Z = pd.DataFrame(Z, index=names, columns=factors)
print("Mixing Matrix:")
print(df_Z.round(3))
```

!!! tip "Interpretacao dos Fatores"
    - **Fator com loadings similares**: fator de mercado (beta)
    - **Fator com loadings opostos**: fator long-short (ex: value vs growth)
    - **Fator com loading concentrado**: fator especifico de um ativo/setor

    A interpretacao e analoga a fatores em PCA, mas com a vantagem de independencia estatistica.

### Volatilidade dos Fatores

```python
# Volatilidade condicional de cada fator
for i, univ in enumerate(results.univariate_results):
    alpha = univ.params[1]
    beta = univ.params[2]
    print(f"Fator {i}: alpha={alpha:.4f}, beta={beta:.4f}, "
          f"persist={alpha+beta:.4f}")
```

### GO-GARCH vs. PCA-GARCH

| Aspecto | GO-GARCH (ICA) | PCA-GARCH |
|---------|----------------|-----------|
| Objetivo | Fatores **independentes** | Fatores **nao correlacionados** |
| Metodo | Maximiza nao-Gaussianidade | Maximiza variancia explicada |
| Ordem dos fatores | Nao ordenados | Ordenados por variancia |
| Distribuicao | Nao-Gaussiana por construcao | Pode ser Gaussiana |

## Diagnosticos

```python
import numpy as np
from archbox.diagnostics import ljung_box_test
from archbox.multivariate.utils import is_positive_definite

# 1. Residuos dos fatores
z = results.std_resids
for i in range(z.shape[1]):
    lb = ljung_box_test(z[:, i]**2, lags=10)
    print(f"Fator {i} - Ljung-Box Q(10): p={lb.pvalue:.4f}")

# 2. Independencia dos fatores
factors = model.factors
corr = np.corrcoef(factors.T)
max_off_diag = np.max(np.abs(corr - np.eye(corr.shape[0])))
print(f"\nMaxima correlacao off-diagonal: {max_off_diag:.4f}")
print("(Deve ser proximo de 0)")

# 3. Positiva-definitividade
H_t = results.dynamic_covariance
n_non_pd = sum(not is_positive_definite(H_t[t]) for t in range(H_t.shape[0]))
print(f"\nMatrizes nao PD: {n_non_pd} de {H_t.shape[0]}")

# 4. Comparacao com DCC
from archbox.multivariate import DCC
dcc_results = DCC(endog).fit()
print(f"\nGO-GARCH AIC: {results.aic:.4f}")
print(f"DCC      AIC: {dcc_results.aic:.4f}")
```

Consulte [Diagnosticos Multivariados](diagnostics.md) para testes completos.

## Equivalentes em R e Python

=== "ArchBox"

    ```python
    from archbox.multivariate import GOGARCH

    model = GOGARCH(endog, n_components=None, univariate_order=(1, 1))
    results = model.fit()
    print(results.summary())

    # Fatores e mixing matrix
    Z = model.mixing_matrix
    factors = model.factors
    ```

=== "R (rmgarch)"

    ```r
    library(rugarch)
    library(rmgarch)

    # Especificacao univariada
    uspec <- ugarchspec(
      variance.model = list(model = "sGARCH", garchOrder = c(1, 1)),
      mean.model = list(armaOrder = c(0, 0))
    )
    mspec <- multispec(replicate(5, uspec))

    # Especificacao GO-GARCH
    gospec <- gogarchspec(
      mean.model = "constant",
      variance.model = "sGARCH",
      distribution.model = "mvnorm",
      ica = "fastica"
    )

    # Estimacao
    gofit <- gogarchfit(gospec, data = returns)
    show(gofit)

    # Fatores e mixing matrix
    factors <- gofit@mfit$Z  # Mixing matrix
    ```

| Funcionalidade | ArchBox | rmgarch (R) |
|---------------|---------|-------------|
| Especificacao | `GOGARCH(endog)` | `gogarchspec(...)` |
| Estimacao | `model.fit()` | `gogarchfit(spec, data)` |
| Mixing matrix | `model.mixing_matrix` | `gofit@mfit$Z` |
| Fatores | `model.factors` | `gofit@mfit$Y` |
| Covariancia | `results.dynamic_covariance` | `rcov(gofit)` |

## References

- van der Weide, R. (2002). GO-GARCH: A Multivariate Generalized Orthogonal GARCH Model. *Journal of Applied Econometrics*, 17(5), 549--564.
- Boswijk, H. P., & van der Weide, R. (2011). Method of Moments Estimation of GO-GARCH Models. *Journal of Econometrics*, 163(1), 118--126.
- Alexander, C. (2001). Orthogonal GARCH. In C. Alexander (Ed.), *Mastering Risk* (Vol. 2, pp. 21--38). Financial Times Prentice Hall.
- Bauwens, L., Laurent, S., & Rombouts, J. V. K. (2006). Multivariate GARCH models: A survey. *Journal of Applied Econometrics*, 21(1), 79--109.

## See Also

- [DCC](dcc.md) — Alternativa com correlacao dinamica direta
- [DECO](deco.md) — Equicorrelacao para muitos ativos
- [CCC](ccc.md) — Modelo mais simples com correlacao constante
- [Diagnosticos Multivariados](diagnostics.md) — Testes de especificacao
- [Guia de Selecao](choosing-model.md) — GO-GARCH vs. alternativas
