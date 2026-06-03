---
title: "CCC-GARCH"
description: "Constant Conditional Correlation GARCH — modelo multivariado com correlacao constante e volatilidades dinamicas."
---

# CCC-GARCH (Constant Conditional Correlation)

!!! info "Quick Reference"
    **Class:** `archbox.multivariate.CCC`
    **Import:** `from archbox.multivariate import CCC`
    **R equivalent:** `rmgarch::dccspec(uspec, dccOrder = c(0, 0))` ou `ccgarch::eccc.estimation()`
    **Python equivalent:** Nao disponivel no pacote `arch`

## Overview

O modelo CCC (Constant Conditional Correlation), proposto por **Bollerslev (1990)**, e o precursor dos modelos GARCH multivariados baseados em correlacao. A premissa central e simples mas poderosa: as **volatilidades** de cada serie sao **dinamicas** (modeladas por GARCH univariado), mas a **correlacao** entre as series e **constante** ao longo do tempo.

A matriz de covariancia condicional e:

$$H_t = D_t \, R \, D_t$$

onde $D_t$ contem as volatilidades dinamicas e $R$ e uma matriz de correlacao fixa.

O CCC e atrativo por sua simplicidade e eficiencia computacional. Ele serve como **benchmark** para modelos com correlacao dinamica (DCC, DECO) — se a correlacao e de fato constante, o CCC e preferivel por parcimonia. A hipotese de correlacao constante pode ser testada formalmente com o **teste de Engle & Sheppard (2001)**.

**Quando usar:**

- Quando as correlacoes entre ativos sao estaveis ao longo do tempo
- Como benchmark antes de estimar modelos mais complexos (DCC)
- Quando parsimonia e prioritaria (poucos parametros de correlacao)
- Portfolios onde a estrutura de correlacao nao muda significativamente

## Formulacao Matematica

### Decomposicao da Covariancia

$$H_t = D_t \, R \, D_t$$

onde:

| Simbolo | Descricao |
|---------|-----------|
| $H_t$ | Matriz de covariancia condicional ($k \times k$) |
| $D_t$ | $\text{diag}(\sigma_{1,t}, \ldots, \sigma_{k,t})$ — volatilidades condicionais |
| $R$ | Matriz de correlacao **constante** ($k \times k$) |

### Volatilidades Dinamicas

Cada volatilidade individual $\sigma_{i,t}^2$ segue um GARCH(1,1):

$$\sigma_{i,t}^2 = \omega_i + \alpha_i \epsilon_{i,t-1}^2 + \beta_i \sigma_{i,t-1}^2, \quad i = 1, \ldots, k$$

### Correlacao Constante

A matriz $R$ e estimada como a correlacao amostral dos residuos padronizados:

$$\hat{R} = \frac{1}{T} \sum_{t=1}^{T} z_t z_t'$$

onde $z_t = D_t^{-1} \epsilon_t$ sao os residuos padronizados pelas volatilidades condicionais.

### Numero de Parametros

| Componente | Parametros |
|------------|:---:|
| GARCH univariados | $3k$ (para GARCH(1,1): $\omega_i, \alpha_i, \beta_i$) |
| Correlacao $R$ | $k(k-1)/2$ (elementos unicos fora da diagonal) |
| **Total** | $3k + k(k-1)/2$ |

!!! note "Parametros de Correlacao"
    Embora $R$ tenha $k(k-1)/2$ elementos, eles **nao sao otimizados** — sao estimados diretamente como a correlacao amostral dos residuos padronizados. Isso torna a estimacao extremamente rapida.

### Log-Verossimilhanca

$$\ell(\theta) = -\frac{T}{2} \left[ k \ln(2\pi) + \ln|R| + \sum_{t=1}^{T} \left( 2 \ln|D_t| + z_t' R^{-1} z_t \right) \right]$$

## Quick Example

```python
import numpy as np
from archbox.multivariate import CCC
from archbox.datasets import load_dataset

# Carregar retornos de portfolio
returns = load_dataset('equity_portfolio')
endog = returns[['PETR4', 'VALE3', 'ITUB4']].values

# Estimar CCC-GARCH
model = CCC(endog, univariate_model="GARCH", univariate_order=(1, 1))
results = model.fit()
print(results.summary())
```

??? example "Output esperado"
    ```
    ======================================================================
              Multivariate Volatility Model Results - CCC
    ======================================================================
    Model:            CCC-GARCH(1,1)
    Method:           Two-step
    Series:           3
    Observations:     2000
    Log-Likelihood:   9812.3456
    AIC:              -19612.6912
    BIC:              -19585.1234
    ----------------------------------------------------------------------
    Constant Correlation Matrix (R)
    ----------------------------------------------------------------------
                  Series 0    Series 1    Series 2
    Series 0      1.0000      0.6543      0.4321
    Series 1      0.6543      1.0000      0.3876
    Series 2      0.4321      0.3876      1.0000

    Univariate GARCH Results
    ----------------------------------------------------------------------
    Series 0: omega=1.2e-05, alpha=0.0854, beta=0.9012
    Series 1: omega=1.5e-05, alpha=0.0923, beta=0.8945
    Series 2: omega=8.7e-06, alpha=0.0712, beta=0.9156
    ======================================================================
    ```

## Guia Detalhado

### Parametros do Construtor

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | ndarray $(T, k)$ | obrigatorio | Matriz de retornos |
| `univariate_model` | str | `"GARCH"` | Modelo GARCH para cada serie |
| `univariate_order` | tuple | `(1, 1)` | Ordem $(p, q)$ do GARCH |

### Parametros de `fit()`

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `method` | str | `"two_step"` | Metodo de estimacao |
| `disp` | bool | `True` | Exibir progresso |

### Acessando a Correlacao Constante

```python
# Matriz de correlacao constante
R = results.constant_correlation
print("Correlacao constante R:")
print(R)

# Correlacao entre serie 0 e serie 1
print(f"Corr(0, 1) = {R[0, 1]:.4f}")
```

### Covariancia Condicional e Portfolio

```python
import numpy as np
from archbox.multivariate.portfolio import (
    portfolio_volatility,
    minimum_variance_weights,
    risk_decomposition
)

# Covariancia condicional H_t = D_t R D_t
H_t = results.dynamic_covariance

# Volatilidade do portfolio
weights = np.array([0.4, 0.3, 0.3])
port_vol = portfolio_volatility(weights, H_t)
print(f"Volatilidade media do portfolio: {port_vol.mean():.4f}")

# Pesos de minima variancia (usando covariancia media)
H_mean = H_t.mean(axis=0)
mvp = minimum_variance_weights(H_mean)
print(f"Pesos MVP: {mvp}")

# Decomposicao de risco
decomp = risk_decomposition(weights, H_t[-1])
print(f"Contribuicao de risco: {decomp['risk_contribution']}")
```

### Teste de Correlacao Constante (Engle & Sheppard)

O **teste de Engle & Sheppard (2001)** verifica se a hipotese de correlacao constante e adequada. Sob $H_0$: a correlacao e constante; sob $H_1$: a correlacao e dinamica (DCC).

```python
from archbox.diagnostics import engle_sheppard_test

# Testar H0: correlacao constante
z = results.std_resids  # Residuos padronizados
es_result = engle_sheppard_test(z, lags=5)
print(f"Engle-Sheppard LM({5}): {es_result.statistic:.4f}")
print(f"p-valor: {es_result.pvalue:.4f}")
```

!!! tip "Interpretacao do Teste"
    - **p > 0.05**: Nao rejeita $H_0$ — correlacao constante e adequada, use CCC
    - **p < 0.05**: Rejeita $H_0$ — correlacao e dinamica, considere [DCC](dcc.md)

### Workflow: CCC vs. DCC

```python
from archbox.multivariate import CCC, DCC
from archbox.diagnostics import engle_sheppard_test

# 1. Estimar CCC como baseline
ccc_results = CCC(endog).fit()

# 2. Testar correlacao constante
z = ccc_results.std_resids
es = engle_sheppard_test(z, lags=5)
print(f"Teste de correlacao constante: p = {es.pvalue:.4f}")

if es.pvalue < 0.05:
    # 3. Correlacao dinamica -> estimar DCC
    print("Correlacao dinamica detectada. Estimando DCC...")
    dcc_results = DCC(endog).fit()
    print(f"CCC AIC: {ccc_results.aic:.4f}")
    print(f"DCC AIC: {dcc_results.aic:.4f}")
else:
    print("Correlacao constante adequada. CCC e suficiente.")
```

## Interpretacao

### Correlacao Constante

A matriz $R$ fornece a estrutura de dependencia media entre os ativos:

| Valor de $\rho_{ij}$ | Interpretacao |
|:---:|---------------|
| $> 0.7$ | Alta correlacao positiva — pouca diversificacao |
| $0.3 - 0.7$ | Correlacao moderada — diversificacao parcial |
| $-0.3 - 0.3$ | Baixa correlacao — boa diversificacao |
| $< -0.3$ | Correlacao negativa — excelente para hedging |

### CCC vs. DCC: Quando a Correlacao e Constante?

Na pratica, a correlacao constante e uma hipotese razoavel quando:

- O periodo amostral e curto e estavel (sem crises)
- Os ativos sao do mesmo setor/mercado com relacao estrutural estavel
- A frequencia dos dados e baixa (mensal vs. diaria)

!!! warning "Limitacao Importante"
    Em periodos de crise financeira, as correlacoes entre ativos tendem a **aumentar drasticamente**. O CCC nao captura esse efeito, subestimando o risco de portfolio durante crises. Se sua amostra inclui crises, prefira [DCC](dcc.md) ou [DECO](deco.md).

## Diagnosticos

```python
from archbox.diagnostics import ljung_box_test, engle_sheppard_test

# 1. Residuos padronizados: GARCH univariados capturam a dinamica?
z = results.std_resids
for i in range(z.shape[1]):
    lb = ljung_box_test(z[:, i]**2, lags=10)
    print(f"Serie {i} - Ljung-Box Q(10): p={lb.pvalue:.4f}")

# 2. Teste de correlacao constante
es = engle_sheppard_test(z, lags=5)
print(f"\nEngle-Sheppard: p={es.pvalue:.4f}")
if es.pvalue < 0.05:
    print("AVISO: Correlacao dinamica detectada. Considere DCC.")

# 3. Comparacao com DCC
from archbox.multivariate import DCC
dcc_results = DCC(endog).fit()
print(f"\nCCC AIC: {results.aic:.4f}")
print(f"DCC AIC: {dcc_results.aic:.4f}")
```

Consulte [Diagnosticos Multivariados](diagnostics.md) para testes completos.

## Equivalentes em R e Python

=== "ArchBox"

    ```python
    from archbox.multivariate import CCC

    model = CCC(endog, univariate_model="GARCH", univariate_order=(1, 1))
    results = model.fit()
    print(results.summary())

    # Correlacao constante
    print(results.constant_correlation)
    ```

=== "R (ccgarch / rmgarch)"

    ```r
    library(ccgarch)

    # CCC-GARCH
    fit <- eccc.estimation(
      a = a_init, A = A_init, B = B_init, R = R_init,
      dvar = returns, model = "extended"
    )

    # Ou via rmgarch com dccOrder = c(0, 0)
    library(rmgarch)
    spec <- dccspec(uspec = mspec, dccOrder = c(0, 0))
    fit <- dccfit(spec, data = returns)
    ```

| Funcionalidade | ArchBox | ccgarch (R) |
|---------------|---------|-------------|
| Especificacao | `CCC(endog)` | `eccc.estimation(...)` |
| Correlacao | `results.constant_correlation` | `fit$R` |
| Covariancia | `results.dynamic_covariance` | `fit$H` |
| Teste CCC | `engle_sheppard_test(z)` | Manual |

## References

- Bollerslev, T. (1990). Modelling the Coherence in Short-Run Nominal Exchange Rates: A Multivariate Generalized ARCH Model. *Review of Economics and Statistics*, 72(3), 498--505.
- Engle, R. F., & Sheppard, K. (2001). Theoretical and Empirical Properties of Dynamic Conditional Correlation Multivariate GARCH. *NBER Working Paper* No. 8554.
- Tse, Y. K. (2000). A Test for Constant Correlations in a Multivariate GARCH Model. *Journal of Econometrics*, 98(1), 107--127.
- Bauwens, L., Laurent, S., & Rombouts, J. V. K. (2006). Multivariate GARCH models: A survey. *Journal of Applied Econometrics*, 21(1), 79--109.

## See Also

- [DCC](dcc.md) — Extensao com correlacao dinamica
- [DECO](deco.md) — Correlacao dinamica escalar para muitos ativos
- [BEKK](bekk.md) — Alternativa com covariancia direta
- [Diagnosticos Multivariados](diagnostics.md) — Teste de Engle-Sheppard detalhado
- [Guia de Selecao](choosing-model.md) — CCC vs. DCC: criterios de decisao
