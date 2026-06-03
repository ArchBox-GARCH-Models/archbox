---
title: "DECO-GARCH"
description: "Dynamic Equicorrelation GARCH — correlacao dinamica escalar para portfolios com centenas de ativos."
---

# DECO-GARCH (Dynamic Equicorrelation)

!!! info "Quick Reference"
    **Class:** `archbox.multivariate.DECO`
    **Import:** `from archbox.multivariate import DECO`
    **R equivalent:** `rmgarch::dccspec(uspec, model = "aDCC")` com restricao equicorrelation
    **Python equivalent:** Nao disponivel no pacote `arch`

## Overview

O modelo DECO (Dynamic Equicorrelation), proposto por **Engle & Kelly (2012)**, e uma simplificacao elegante do DCC que assume que **todas as correlacoes condicionais entre pares de ativos sao iguais** a um unico parametro escalar dinamico $\rho_t$. Essa restricao drastica reduz a complexidade e torna o modelo **escalavel para centenas ou milhares de ativos**.

A matriz de correlacao condicional do DECO tem a forma:

$$R_t = (1 - \rho_t) I_k + \rho_t \mathbf{1}_k \mathbf{1}_k'$$

onde $\rho_t$ e a equicorrelacao dinamica e $\mathbf{1}_k$ e um vetor de uns.

Apesar da simplicidade, o DECO captura o fenomeno empirico mais importante: a **correlacao media do mercado varia ao longo do tempo**, aumentando durante crises e diminuindo em periodos calmos. Para portfolios grandes e diversificados, essa dinamica e frequentemente o fator dominante.

**Quando usar:**

- Portfolios com muitos ativos ($k > 50$) onde DCC completo e caro demais
- Quando a correlacao entre ativos se move de forma similar (contagio)
- Calculo de VaR de portfolio com muitos componentes
- Analise de risco sistemico e co-movimento de mercado

## Formulacao Matematica

### Estimacao em Dois Passos

Como no DCC, o DECO usa estimacao em dois passos:

1. **Passo 1**: GARCH univariado para cada serie $\rightarrow$ $\sigma_{i,t}$, $z_{i,t}$
2. **Passo 2**: Estimacao da equicorrelacao dinamica $\rho_t$

### Recursao DCC Subjacente

O DECO parte da mesma recursao do DCC para a matriz auxiliar $Q_t$:

$$Q_t = (1 - a - b)\bar{Q} + a \, z_{t-1} z_{t-1}' + b \, Q_{t-1}$$

### Extracao da Equicorrelacao

A equicorrelacao escalar $\rho_t$ e extraida como a **media dos elementos fora da diagonal** da matriz $Q_t$ normalizada:

$$\rho_t = \frac{1}{k(k-1)} \sum_{i \neq j} \frac{q_{ij,t}}{\sqrt{q_{ii,t} \, q_{jj,t}}}$$

onde $q_{ij,t}$ sao os elementos de $Q_t$.

### Matriz de Correlacao Equicorrelacionada

$$R_t = (1 - \rho_t) I_k + \rho_t \mathbf{1}_k \mathbf{1}_k'$$

Equivalentemente:

$$R_t = \begin{pmatrix}
1 & \rho_t & \cdots & \rho_t \\
\rho_t & 1 & \cdots & \rho_t \\
\vdots & \vdots & \ddots & \vdots \\
\rho_t & \rho_t & \cdots & 1
\end{pmatrix}$$

### Covariancia Condicional

$$H_t = D_t \, R_t \, D_t$$

### Propriedade: Positiva-Definitividade

A matriz $R_t$ e positiva-definida se e somente se:

$$-\frac{1}{k-1} < \rho_t < 1$$

Para $k$ grande, o limite inferior e essencialmente 0, garantindo PD para qualquer $\rho_t > 0$.

### Restricoes

| Parametro | Restricao | Justificativa |
|-----------|-----------|---------------|
| $a$ | $a > 0$ | Reacao a choques |
| $b$ | $b > 0$ | Persistencia |
| $a + b$ | $a + b < 1$ | Estacionariedade |
| $\rho_t$ | $-1/(k-1) < \rho_t < 1$ | Positiva-definitividade |

## Quick Example

```python
import numpy as np
from archbox.multivariate import DECO
from archbox.datasets import load_dataset

# Carregar retornos de muitos ativos
returns = load_dataset('equity_portfolio')
endog = returns[['PETR4', 'VALE3', 'ITUB4', 'BBDC4', 'ABEV3']].values

# Estimar DECO-GARCH
model = DECO(endog, univariate_model="GARCH", univariate_order=(1, 1))
results = model.fit()
print(results.summary())
```

??? example "Output esperado"
    ```
    ======================================================================
              Multivariate Volatility Model Results - DECO
    ======================================================================
    Model:            DECO-GARCH(1,1)
    Method:           Two-step
    Series:           5
    Observations:     2000
    Log-Likelihood:   12234.5678
    AIC:              -24457.1356
    BIC:              -24424.3456
    ----------------------------------------------------------------------
    Equicorrelation Parameters
    ----------------------------------------------------------------------
    Parameter         Estimate      Std Err      t-value      p-value
    ----------------------------------------------------------------------
    a                0.038765     0.007654       5.0649       0.0000
    b                0.945678     0.010234      92.3789       0.0000
    ----------------------------------------------------------------------
    Persistence (a+b): 0.984443

    Equicorrelation rho_t
    ----------------------------------------------------------------------
    Mean:     0.4523
    Min:      0.2134
    Max:      0.7856
    Std:      0.0876
    ======================================================================
    ```

## Guia Detalhado

### Parametros do Construtor

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | ndarray $(T, k)$ | obrigatorio | Matriz de retornos |
| `univariate_model` | str | `"GARCH"` | Modelo GARCH univariado |
| `univariate_order` | tuple | `(1, 1)` | Ordem $(p, q)$ do GARCH |

### Parametros de `fit()`

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `method` | str | `"two_step"` | Metodo de estimacao |
| `disp` | bool | `True` | Exibir progresso |

### Equicorrelacao Dinamica

```python
# Serie temporal da equicorrelacao
rho_t = model.equicorrelation  # shape: (T,)

print(f"Equicorrelacao media: {rho_t.mean():.4f}")
print(f"Equicorrelacao min:   {rho_t.min():.4f}")
print(f"Equicorrelacao max:   {rho_t.max():.4f}")

# Visualizar
import matplotlib.pyplot as plt
plt.figure(figsize=(12, 4))
plt.plot(rho_t)
plt.title('Equicorrelacao Dinamica')
plt.ylabel(r'$\rho_t$')
plt.axhline(rho_t.mean(), color='r', linestyle='--', label='Media')
plt.legend()
plt.tight_layout()
plt.show()
```

### Portfolio com DECO

```python
import numpy as np
from archbox.multivariate.portfolio import (
    portfolio_volatility,
    minimum_variance_weights_dynamic,
    risk_decomposition
)

# Covariancia condicional
H_t = results.dynamic_covariance

# Equal-weighted portfolio
k = endog.shape[1]
weights = np.ones(k) / k
port_vol = portfolio_volatility(weights, H_t)
print(f"Volatilidade media do portfolio: {port_vol.mean():.4f}")

# Pesos otimos dinamicos
mvp_weights = minimum_variance_weights_dynamic(H_t)
print(f"Pesos MVP (ultimo dia): {np.round(mvp_weights[-1], 4)}")

# Decomposicao de risco
decomp = risk_decomposition(weights, H_t[-1])
print(f"Volatilidade do portfolio: {decomp['portfolio_volatility']:.4f}")
print(f"Contribuicao de risco: {np.round(decomp['risk_contribution'], 4)}")
```

### DECO para Risco Sistemico

A equicorrelacao $\rho_t$ e um indicador natural de **risco sistemico**:

```python
import numpy as np

rho_t = model.equicorrelation

# Identificar periodos de alta correlacao (crises)
threshold = np.percentile(rho_t, 95)
crisis_periods = rho_t > threshold
print(f"Threshold de crise (p95): {threshold:.4f}")
print(f"Dias em crise: {crisis_periods.sum()} de {len(rho_t)}")
```

!!! tip "Equicorrelacao como Indicador de Crise"
    Quando $\rho_t$ sobe abruptamente, significa que todos os ativos estao se movendo juntos — tipico de eventos de **flight-to-quality** ou **contagio financeiro**. Valores de $\rho_t > 0.7$ geralmente indicam estresse de mercado.

### Previsao

```python
# Previsao de covariancia
forecast = model.forecast(results, horizon=10)
print("Covariancia prevista (h=1):")
print(forecast['covariance'][0])

# Equicorrelacao prevista converge para media incondicional
a, b = results.params
rho_bar = rho_t.mean()
print(f"\nEquicorrelacao incondicional: {rho_bar:.4f}")
```

## Interpretacao

### Equicorrelacao $\rho_t$

| Faixa de $\rho_t$ | Interpretacao |
|:---:|---------------|
| $< 0.2$ | Baixa co-dependencia — alta diversificacao efetiva |
| $0.2 - 0.5$ | Correlacao moderada — diversificacao parcial |
| $0.5 - 0.7$ | Alta correlacao — diversificacao limitada |
| $> 0.7$ | Correlacao muito alta — crise / contagio |

### Parametros $a$ e $b$

A interpretacao e analoga ao DCC:

| Parametro | Interpretacao |
|-----------|---------------|
| $a$ grande | Equicorrelacao reage rapidamente a choques de mercado |
| $b$ grande | Equicorrelacao e persistente, muda lentamente |
| $a + b \approx 1$ | Choques na correlacao sao quase permanentes |

### DECO vs. DCC

| Aspecto | DECO | DCC |
|---------|------|-----|
| Parametros de correlacao | 2 ($a$, $b$) | 2 ($a$, $b$) |
| Correlacoes pairwise | Todas iguais $(\rho_t)$ | Diferentes por par |
| Complexidade computacional | $O(k)$ | $O(k^2)$ |
| Dimensao maxima pratica | $k > 500$ | $k \leq 100$ |
| Precisao por par | Baixa | Alta |

!!! warning "Limitacao"
    A premissa de equicorrelacao e forte. Se os ativos tem estruturas de correlacao muito diferentes (ex: acoes domesticas vs. internacionais), o DECO pode ser inadequado. Use [DCC](dcc.md) para capturar heterogeneidade nas correlacoes.

## Diagnosticos

```python
from archbox.diagnostics import ljung_box_test
from archbox.multivariate.utils import is_positive_definite

# 1. Residuos padronizados
z = results.std_resids
for i in range(z.shape[1]):
    lb = ljung_box_test(z[:, i]**2, lags=10)
    print(f"Serie {i} - Ljung-Box Q(10): p={lb.pvalue:.4f}")

# 2. Positiva-definitividade
H_t = results.dynamic_covariance
n_non_pd = sum(not is_positive_definite(H_t[t]) for t in range(H_t.shape[0]))
print(f"\nMatrizes nao PD: {n_non_pd} de {H_t.shape[0]}")

# 3. Comparacao DECO vs DCC vs CCC
from archbox.multivariate import DCC, CCC

dcc_results = DCC(endog).fit()
ccc_results = CCC(endog).fit()

print(f"\nDECO AIC: {results.aic:.4f}")
print(f"DCC  AIC: {dcc_results.aic:.4f}")
print(f"CCC  AIC: {ccc_results.aic:.4f}")
```

Consulte [Diagnosticos Multivariados](diagnostics.md) para testes completos.

## Equivalentes em R e Python

=== "ArchBox"

    ```python
    from archbox.multivariate import DECO

    model = DECO(endog, univariate_model="GARCH", univariate_order=(1, 1))
    results = model.fit()
    print(results.summary())

    # Equicorrelacao dinamica
    rho_t = model.equicorrelation
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
    mspec <- multispec(replicate(k, uspec))

    # DCC com restricao de equicorrelacao
    # (rmgarch nao tem DECO nativo, mas pode ser simulado)
    dccspec <- dccspec(uspec = mspec, dccOrder = c(1, 1))
    dccfit <- dccfit(dccspec, data = returns)

    # Extrair equicorrelacao media
    R <- rcor(dccfit)
    rho_t <- apply(R, 3, function(x) mean(x[upper.tri(x)]))
    ```

| Funcionalidade | ArchBox | rmgarch (R) |
|---------------|---------|-------------|
| Especificacao | `DECO(endog)` | Nao nativo |
| Equicorrelacao | `model.equicorrelation` | Manual |
| Covariancia | `results.dynamic_covariance` | `rcov(fit)` |
| Parametros | `results.params` → `[a, b]` | Via DCC |

## References

- Engle, R. F., & Kelly, B. T. (2012). Dynamic Equicorrelation. *Journal of Business & Economic Statistics*, 30(2), 212--228.
- Engle, R. F. (2002). Dynamic Conditional Correlation: A Simple Class of Multivariate Generalized Autoregressive Conditional Heteroskedasticity Models. *Journal of Business & Economic Statistics*, 20(3), 339--350.
- Bauwens, L., Laurent, S., & Rombouts, J. V. K. (2006). Multivariate GARCH models: A survey. *Journal of Applied Econometrics*, 21(1), 79--109.

## See Also

- [DCC](dcc.md) — Modelo mais flexivel com correlacoes heterogeneas
- [CCC](ccc.md) — Caso especial com correlacao constante
- [Diagnosticos Multivariados](diagnostics.md) — Testes de especificacao
- [Guia de Selecao](choosing-model.md) — DECO vs. DCC: criterios de decisao
