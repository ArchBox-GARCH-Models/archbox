---
title: "BEKK-GARCH"
description: "BEKK multivariate GARCH — garante positiva-definitividade da covariancia condicional por construcao."
---

# BEKK-GARCH

!!! info "Quick Reference"
    **Class:** `archbox.multivariate.BEKK`
    **Import:** `from archbox.multivariate import BEKK`
    **R equivalent:** `mgarchBEKK::BEKK(data)` ou `rmgarch` com BEKK spec
    **Python equivalent:** Nao disponivel no pacote `arch`

## Overview

O modelo BEKK, proposto por **Engle & Kroner (1995)** (nomeado a partir das iniciais de Baba, Engle, Kraft e Kroner), e um modelo GARCH multivariado que garante **positiva-definitividade** da matriz de covariancia condicional $H_t$ por construcao. Diferentemente do DCC, que decompoe a covariancia em volatilidades e correlacoes, o BEKK modela $H_t$ diretamente.

A principal vantagem do BEKK e a garantia matematica de que $H_t$ e sempre positiva-definida, sem necessidade de restricoes adicionais ou ajustes numericos. Porem, essa flexibilidade vem ao custo de um grande numero de parametros, tornando o modelo impraticavel para mais de 4-5 series.

**Quando usar:**

- Portfolios pequenos (2-5 ativos) onde precisao e prioritaria
- Quando a positiva-definitividade deve ser garantida por construcao
- Estudos de transmissao de volatilidade entre poucos mercados
- Hedging entre pares de ativos

## Formulacao Matematica

### BEKK Full

A formulacao completa do BEKK(1,1) e:

$$H_t = C'C + A' \epsilon_{t-1} \epsilon_{t-1}' A + B' H_{t-1} B$$

onde:

| Simbolo | Dimensao | Descricao |
|---------|----------|-----------|
| $H_t$ | $k \times k$ | Matriz de covariancia condicional |
| $C$ | $k \times k$ | Matriz triangular inferior (intercepto) |
| $A$ | $k \times k$ | Matriz de parametros ARCH (reacao a choques) |
| $B$ | $k \times k$ | Matriz de parametros GARCH (persistencia) |
| $\epsilon_t$ | $k \times 1$ | Vetor de residuos |

!!! note "Por que e positiva-definida?"
    Se $H_0$ e positiva-definida, entao para qualquer $t$:

    - $C'C$ e positiva semi-definida (e positiva-definida se $C$ tem diagonal positiva)
    - $A' \epsilon_{t-1} \epsilon_{t-1}' A$ e positiva semi-definida
    - $B' H_{t-1} B$ e positiva semi-definida (por inducao)

    A soma de matrizes positiva semi-definidas com pelo menos uma positiva-definida resulta em positiva-definida.

### Numero de Parametros (Full BEKK)

Para $k$ series:

| Componente | Parametros |
|------------|:---:|
| $C$ (triangular inferior) | $k(k+1)/2$ |
| $A$ (cheia) | $k^2$ |
| $B$ (cheia) | $k^2$ |
| **Total** | $k(k+1)/2 + 2k^2$ |

| $k$ | Total de parametros |
|:---:|:---:|
| 2 | 11 |
| 3 | 24 |
| 5 | 65 |
| 10 | 255 |

### BEKK Diagonal

Para reduzir o numero de parametros, a versao diagonal restringe $A$ e $B$ a matrizes diagonais:

$$H_t = C'C + A' \odot (\epsilon_{t-1} \epsilon_{t-1}') + B' \odot H_{t-1}$$

onde $\odot$ denota multiplicacao elemento a elemento (Hadamard product) com as matrizes diagonais $A$ e $B$.

| Componente | Parametros (Diagonal) |
|------------|:---:|
| $C$ (triangular inferior) | $k(k+1)/2$ |
| $A$ (diagonal) | $k$ |
| $B$ (diagonal) | $k$ |
| **Total** | $k(k+1)/2 + 2k$ |

| $k$ | Full BEKK | Diagonal BEKK |
|:---:|:---:|:---:|
| 2 | 11 | 7 |
| 3 | 24 | 12 |
| 5 | 65 | 25 |
| 10 | 255 | 75 |

!!! tip "Recomendacao"
    Use **Diagonal BEKK** como padrao. So use **Full BEKK** quando:

    - Voce tem poucos ativos ($k \leq 3$)
    - Precisa modelar transmissao cruzada de volatilidade (spillover de A para B)
    - Tem amostra grande o suficiente para estimar todos os parametros

### Variancia Incondicional

A variancia incondicional do BEKK(1,1) e:

$$\text{vec}(\bar{H}) = (I_{k^2} - A' \otimes A' - B' \otimes B')^{-1} \, \text{vec}(C'C)$$

onde $\otimes$ e o produto de Kronecker e $\text{vec}(\cdot)$ empilha as colunas de uma matriz.

## Quick Example

```python
import numpy as np
from archbox.multivariate import BEKK
from archbox.datasets import load_dataset

# Carregar retornos de dois ativos
returns = load_dataset('equity_portfolio')
endog = returns[['PETR4', 'VALE3']].values

# Estimar BEKK Diagonal
model = BEKK(endog, variant="diagonal")
results = model.fit()
print(results.summary())
```

??? example "Output esperado"
    ```
    ======================================================================
              Multivariate Volatility Model Results - BEKK
    ======================================================================
    Model:            BEKK-Diagonal
    Method:           MLE
    Series:           2
    Observations:     2000
    Log-Likelihood:   6543.2109
    AIC:              -13072.4218
    BIC:              -13033.1234
    ----------------------------------------------------------------------
    Parameter         Estimate      Std Err      t-value      p-value
    ----------------------------------------------------------------------
    C[0,0]           0.002345     0.000456       5.1425       0.0000
    C[1,0]           0.001234     0.000345       3.5768       0.0003
    C[1,1]           0.001987     0.000398       4.9925       0.0000
    A[0]             0.287654     0.034567       8.3220       0.0000
    A[1]             0.312345     0.037890       8.2434       0.0000
    B[0]             0.934567     0.015678      59.6087       0.0000
    B[1]             0.921234     0.018901      48.7393       0.0000
    ======================================================================
    ```

## Guia Detalhado

### Parametros do Construtor

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | ndarray $(T, k)$ | obrigatorio | Matriz de retornos |
| `variant` | str | `"diagonal"` | `"diagonal"` ou `"full"` |
| `univariate_model` | str | `"GARCH"` | Modelo GARCH univariado (para valores iniciais) |
| `univariate_order` | tuple | `(1, 1)` | Ordem do GARCH univariado |

### Parametros de `fit()`

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `method` | str | `"mle"` | Metodo de estimacao (MLE completo) |
| `disp` | bool | `True` | Exibir progresso |

### Full BEKK vs. Diagonal BEKK

```python
from archbox.multivariate import BEKK

# Diagonal BEKK (recomendado para k >= 3)
model_diag = BEKK(endog, variant="diagonal")
results_diag = model_diag.fit()

# Full BEKK (apenas para k <= 3)
model_full = BEKK(endog, variant="full")
results_full = model_full.fit()

# Comparar
print(f"Diagonal BEKK - AIC: {results_diag.aic:.4f} ({len(results_diag.params)} params)")
print(f"Full BEKK     - AIC: {results_full.aic:.4f} ({len(results_full.params)} params)")
```

### Transmissao de Volatilidade (Full BEKK)

No Full BEKK, os elementos fora da diagonal de $A$ e $B$ capturam **transmissao cruzada de volatilidade** (spillover):

```python
# Full BEKK com 2 ativos
model = BEKK(endog, variant="full")
results = model.fit()

# Interpretar spillover
# A[0,1]: como choques na serie 1 afetam a volatilidade da serie 0
# B[0,1]: como a volatilidade passada da serie 1 afeta a da serie 0
print("Parametros do modelo:")
print(results.summary())
```

### Portfolio com BEKK

```python
import numpy as np
from archbox.multivariate.portfolio import (
    portfolio_volatility,
    minimum_variance_weights_dynamic,
    risk_decomposition
)

# Covariancia condicional
H_t = results.dynamic_covariance

# Volatilidade do portfolio
weights = np.array([0.6, 0.4])
port_vol = portfolio_volatility(weights, H_t)
print(f"Volatilidade media: {port_vol.mean():.4f}")

# Pesos de minima variancia
mvp = minimum_variance_weights_dynamic(H_t)
print(f"Pesos MVP (ultimo dia): {mvp[-1]}")

# Decomposicao de risco
decomp = risk_decomposition(weights, H_t[-1])
print(f"Contribuicao de risco: {decomp['risk_contribution']}")
```

## Interpretacao

### Matrizes de Parametros

Para um BEKK(1,1) bivariado com Full parametrizacao:

$$A = \begin{pmatrix} a_{11} & a_{12} \\ a_{21} & a_{22} \end{pmatrix}, \qquad
B = \begin{pmatrix} b_{11} & b_{12} \\ b_{21} & b_{22} \end{pmatrix}$$

| Elemento | Interpretacao |
|----------|---------------|
| $a_{ii}$ | Reacao da volatilidade de $i$ ao seu proprio choque |
| $a_{ij}$ ($i \neq j$) | **Spillover ARCH**: choque em $j$ afeta volatilidade de $i$ |
| $b_{ii}$ | Persistencia propria da volatilidade de $i$ |
| $b_{ij}$ ($i \neq j$) | **Spillover GARCH**: volatilidade passada de $j$ afeta $i$ |

!!! warning "Cuidado com a Interpretacao"
    No BEKK, os parametros sao transformados quadraticamente ($A' \cdot A$, $B' \cdot B$), portanto nao podem ser interpretados diretamente como no DCC. Use a **news impact surface** para interpretar o impacto de choques.

### Persistencia

A persistencia do BEKK e medida pelos autovalores de $A' \otimes A' + B' \otimes B'$. Se todos os autovalores estao dentro do circulo unitario, o processo e estacionario.

```python
# Verificar estacionariedade
persistence = results.persistence()
print(f"Persistencia (maior autovalor): {persistence:.6f}")
# < 1.0 -> estacionario
```

## Diagnosticos

```python
from archbox.diagnostics import ljung_box_test
from archbox.multivariate.utils import is_positive_definite

# 1. Residuos padronizados
z = results.std_resids
for i in range(z.shape[1]):
    lb = ljung_box_test(z[:, i]**2, lags=10)
    print(f"Serie {i} - Ljung-Box Q(10): p={lb.pvalue:.4f}")

# 2. Positiva-definitividade (deve ser 100% por construcao)
H_t = results.dynamic_covariance
all_pd = all(is_positive_definite(H_t[t]) for t in range(H_t.shape[0]))
print(f"Todas H_t positiva-definidas: {all_pd}")

# 3. Comparar com DCC
from archbox.multivariate import DCC
dcc_results = DCC(endog).fit()
print(f"\nBEKK AIC: {results.aic:.4f}")
print(f"DCC  AIC: {dcc_results.aic:.4f}")
```

Consulte [Diagnosticos Multivariados](diagnostics.md) para testes completos.

## Equivalentes em R e Python

=== "ArchBox"

    ```python
    from archbox.multivariate import BEKK

    model = BEKK(endog, variant="diagonal")
    results = model.fit()
    print(results.summary())

    # Covariancia dinamica
    H_t = results.dynamic_covariance
    ```

=== "R (mgarchBEKK / rmgarch)"

    ```r
    library(mgarchBEKK)

    # Full BEKK
    fit <- BEKK(data, order = c(1, 1), params = "Full")
    summary(fit)

    # Diagonal BEKK
    fit_diag <- BEKK(data, order = c(1, 1), params = "Diagonal")
    ```

| Funcionalidade | ArchBox | mgarchBEKK (R) |
|---------------|---------|----------------|
| Full BEKK | `BEKK(endog, variant="full")` | `BEKK(data, params="Full")` |
| Diagonal BEKK | `BEKK(endog, variant="diagonal")` | `BEKK(data, params="Diagonal")` |
| Estimacao | `model.fit()` | `BEKK(data, ...)` |
| Covariancia | `results.dynamic_covariance` | `fit$H` |

## References

- Engle, R. F., & Kroner, K. F. (1995). Multivariate Simultaneous Generalized ARCH. *Econometric Theory*, 11(1), 122--150.
- Baba, Y., Engle, R. F., Kraft, D. F., & Kroner, K. F. (1990). Multivariate Simultaneous Generalized ARCH. Unpublished manuscript, University of California, San Diego.
- Caporin, M., & McAleer, M. (2012). Do We Really Need Both BEKK and DCC? A Tale of Two Multivariate GARCH Models. *Journal of Economic Surveys*, 26(4), 736--751.
- Bauwens, L., Laurent, S., & Rombouts, J. V. K. (2006). Multivariate GARCH models: A survey. *Journal of Applied Econometrics*, 21(1), 79--109.

## See Also

- [DCC](dcc.md) — Alternativa escalavel com estimacao em dois passos
- [CCC](ccc.md) — Caso mais simples com correlacao constante
- [Diagnosticos Multivariados](diagnostics.md) — Testes de especificacao
- [Guia de Selecao](choosing-model.md) — BEKK vs. DCC: quando usar cada um
