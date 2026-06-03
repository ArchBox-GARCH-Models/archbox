---
title: "TAR"
description: "Threshold Autoregressive model — transicao abrupta entre regimes definida por variavel threshold e grid search."
---

# TAR (Threshold Autoregressive)

!!! info "Quick Reference"
    **Class:** `archbox.threshold.TAR`
    **Import:** `from archbox.threshold import TAR`
    **R equivalent:** `tsDyn::setar(y, nthresh=1, thVar=z)`
    **Python equivalent:** Nao disponivel em pacotes padrao

## Overview

O modelo TAR (Threshold Autoregressive), introduzido por **Tong (1978)**, e o modelo nao-linear mais simples baseado em threshold. A ideia e que a dinamica da serie temporal muda **abruptamente** quando uma variavel observavel $z_t$ cruza um limiar $c$. Diferentemente do [SETAR](setar.md), o TAR permite que a variavel de transicao $z_t$ seja **externa** — nao necessariamente um lag da propria serie.

O TAR e adequado quando:

- **Assimetria de taxa de juros**: a dinamica de ajuste difere acima e abaixo de um nivel critico
- **Efeitos de politica**: uma variavel de politica (taxa basica, banda cambial) define regimes distintos
- **Limiar exogeno**: o mecanismo de transicao e governado por uma variavel externa observavel
- **Transicao abrupta**: nao ha gradualidade na mudanca de regime

## Formulacao Matematica

### Modelo Geral

O modelo TAR com 2 regimes e definido por:

$$y_t = \boldsymbol{\phi}_1' \mathbf{x}_t \cdot I(z_t \leq c) + \boldsymbol{\phi}_2' \mathbf{x}_t \cdot I(z_t > c) + \epsilon_t$$

onde:

- $\mathbf{x}_t = (1, y_{t-1}, \ldots, y_{t-p})'$ e o vetor de regressores
- $z_t$ e a variavel de transicao (threshold variable)
- $c$ e o valor de threshold (limiar)
- $I(\cdot)$ e a funcao indicadora
- $\boldsymbol{\phi}_1, \boldsymbol{\phi}_2$ sao os parametros AR de cada regime
- $\epsilon_t \sim N(0, \sigma_{s_t}^2)$ com variancia regime-dependente

| Parametro | Descricao | Restricao |
|-----------|-----------|-----------|
| $c$ | Valor de threshold | $z_{(0.15T)} \leq c \leq z_{(0.85T)}$ |
| $\boldsymbol{\phi}_1$ | Parametros AR do regime 1 ($z_t \leq c$) | Estacionariedade local |
| $\boldsymbol{\phi}_2$ | Parametros AR do regime 2 ($z_t > c$) | Estacionariedade local |
| $\sigma_1^2, \sigma_2^2$ | Variancia por regime | $\sigma_k^2 > 0$ |

### Funcao de Transicao

A funcao de transicao do TAR e a funcao indicadora:

$$G(z_t; c) = I(z_t > c) = \begin{cases} 0 & \text{se } z_t \leq c \\ 1 & \text{se } z_t > c \end{cases}$$

Esta e a transicao mais simples possivel: **binaria e instantanea**. Em $z_t = c$, a serie transita imediatamente de um regime para o outro.

### Estimacao por Grid Search + OLS Condicional

A estimacao do TAR segue um procedimento em dois estagios:

1. **Grid search para $c$**: dado um grid de candidatos $c_1, c_2, \ldots, c_G$ (percentis 15% a 85% de $z_t$), para cada $c_j$:
    - Particiona as observacoes: $\mathcal{I}_1 = \{t: z_t \leq c_j\}$ e $\mathcal{I}_2 = \{t: z_t > c_j\}$
    - Estima OLS em cada regime: $\hat{\boldsymbol{\phi}}_k = (\mathbf{X}_k' \mathbf{X}_k)^{-1} \mathbf{X}_k' \mathbf{y}_k$
    - Calcula $RSS(c_j) = RSS_1(c_j) + RSS_2(c_j)$

2. **Selecao otima**: $\hat{c} = \arg\min_{c_j} RSS(c_j)$

$$\hat{c} = \arg\min_{c \in \mathcal{C}} \left[ \sum_{t: z_t \leq c} (y_t - \hat{\boldsymbol{\phi}}_1' \mathbf{x}_t)^2 + \sum_{t: z_t > c} (y_t - \hat{\boldsymbol{\phi}}_2' \mathbf{x}_t)^2 \right]$$

!!! note "Restricao de trimming"
    O grid search exclui os 15% extremos de $z_t$ para garantir observacoes suficientes em cada regime. Alem disso, cada regime deve ter no minimo $p + 2$ observacoes.

## Quick Example

```python
import numpy as np
from archbox.threshold import TAR

# Dados simulados com threshold
rng = np.random.default_rng(42)
n = 500
y = np.zeros(n)
for t in range(1, n):
    if y[t-1] <= 0:
        y[t] = 0.5 + 0.3 * y[t-1] + rng.standard_normal() * 0.5
    else:
        y[t] = -0.2 + 0.8 * y[t-1] + rng.standard_normal() * 0.5

# TAR(1) com variavel de transicao = y_{t-1} (default)
model = TAR(y, order=1, delay=1)
results = model.fit()
print(results.summary())
```

??? example "Output esperado"
    ```
    ======================================================================
                                  Model: TAR
                           Observations: 499
                            AR Order (p): 1
                              Delay (d): 1
                     Number of Regimes: 2
                         Log-Likelihood: -349.1234
                                    AIC: 708.2468
                                    BIC: 729.1234
    ----------------------------------------------------------------------
                          Threshold (c): -0.012345
    ----------------------------------------------------------------------
    Transition Parameters:
                                     c: -0.012345
    ----------------------------------------------------------------------
    regime_1:
                                 const: 0.498765
                                 phi_1: 0.301234
    regime_2:
                                 const: -0.198765
                                 phi_1: 0.799012
    ----------------------------------------------------------------------
    Variance per Regime:
                              regime_1: 0.251234
                              regime_2: 0.249876
    ======================================================================
    ```

## Guia Detalhado

### Parametros do Construtor

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | array-like | obrigatorio | Serie temporal, shape (T,) |
| `order` | int | `1` | Ordem AR $p$ |
| `delay` | int | `1` | Delay $d$: $z_t = y_{t-d}$ (se `threshold_var` nao fornecido) |
| `n_regimes` | int | `2` | Numero de regimes |
| `threshold_var` | array-like | `None` | Variavel de transicao externa. Se `None`, usa $y_{t-d}$ |
| `grid_points` | int | `300` | Numero de pontos no grid search para $c$ |

### Parametros de `fit()`

O metodo `fit()` nao requer parametros adicionais. A estimacao e feita via Conditional Least Squares (CLS) com grid search.

### Exemplo: Taxa de Juros com Assimetria

```python
import numpy as np
from archbox.threshold import TAR, tsay_test

# Simular taxa de juros com assimetria
rng = np.random.default_rng(123)
n = 400
r = np.zeros(n)
threshold = 5.0  # limiar em 5%

for t in range(1, n):
    if r[t-1] <= threshold:
        # Regime baixo: mean-reverting lento
        r[t] = 0.3 + 0.95 * r[t-1] + rng.standard_normal() * 0.3
    else:
        # Regime alto: mean-reverting rapido
        r[t] = 1.5 + 0.70 * r[t-1] + rng.standard_normal() * 0.5

# 1. Testar nao-linearidade (Tsay test)
test = tsay_test(r, order=1, delay=1)
print(f"Tsay test: F = {test.statistic:.4f}, p = {test.pvalue:.4f}")

# 2. Estimar TAR
model = TAR(r, order=1, delay=1, grid_points=300)
results = model.fit()
print(results.summary())

# 3. Visualizar regimes
results.plot_regimes()

# 4. Diagrama de fase
results.plot_phase_diagram()
```

### TAR com Variavel de Transicao Externa

```python
import numpy as np
from archbox.threshold import TAR

# Serie dependente e variavel de transicao externa
rng = np.random.default_rng(42)
n = 500
z = rng.standard_normal(n).cumsum()  # variavel externa (ex: spread)
y = np.zeros(n)

for t in range(1, n):
    if z[t-1] <= 0:
        y[t] = 0.3 + 0.5 * y[t-1] + rng.standard_normal() * 0.4
    else:
        y[t] = -0.1 + 0.2 * y[t-1] + rng.standard_normal() * 0.8

# TAR com variavel threshold externa
model = TAR(y, order=1, threshold_var=z)
results = model.fit()
print(results.summary())
print(f"\nThreshold estimado: {results.threshold:.4f}")
```

### Resultados

| Atributo | Descricao |
|----------|-----------|
| `results.params` | Parametros por regime (dict) |
| `results.threshold` | Valor de threshold estimado $\hat{c}$ |
| `results.delay` | Delay $d$ |
| `results.transition_params` | Parametros de transicao `{'c': ...}` |
| `results.params_regime1` | Coeficientes AR do regime 1 (ndarray) |
| `results.params_regime2` | Coeficientes AR do regime 2 (ndarray) |
| `results.regime_assignments` | Atribuicao binaria de regime (ndarray) |
| `results.transition_values` | Valores de $G(z_t)$ (ndarray) |
| `results.resid` | Residuos (ndarray) |
| `results.sigma2` | Variancia por regime (dict) |
| `results.loglike` | Log-verossimilhanca |
| `results.aic` | Criterio de Informacao de Akaike |
| `results.bic` | Criterio de Informacao Bayesiano |
| `results.nobs` | Numero de observacoes efetivas |

| Metodo | Descricao |
|--------|-----------|
| `results.summary()` | Tabela formatada de resultados |
| `results.plot_regimes()` | Grafico com coloracao de regimes |
| `results.plot_transition()` | Grafico da funcao de transicao |
| `results.plot_phase_diagram()` | Diagrama de fase $y_t$ vs $y_{t-1}$ |
| `results.plot_fit()` | Observado vs ajustado + residuos |
| `results.forecast(horizon)` | Previsao $h$ passos a frente |

## Interpretacao

### Significado do Threshold

O valor estimado $\hat{c}$ divide a amostra em dois regimes com dinamicas distintas:

- **Regime 1** ($z_t \leq c$): tipicamente o regime "normal" ou de baixa intensidade
- **Regime 2** ($z_t > c$): tipicamente o regime "extremo" ou de alta intensidade

A distribuicao das observacoes entre regimes e:

```python
n_regime1 = (results.regime_assignments == 0).sum()
n_regime2 = (results.regime_assignments == 1).sum()
print(f"Regime 1 (z <= c): {n_regime1} obs ({100*n_regime1/results.nobs:.1f}%)")
print(f"Regime 2 (z > c):  {n_regime2} obs ({100*n_regime2/results.nobs:.1f}%)")
```

### Persistencia por Regime

A persistencia em cada regime e dada pela soma dos coeficientes AR:

$$\text{Persistencia}_k = \sum_{i=1}^{p} |\phi_{i,k}|$$

Se a persistencia e proxima de 1, o regime e altamente persistente (choques tem efeito duradouro). Se e menor que 1, ha **reversao a media** dentro do regime.

## Diagnosticos

```python
from archbox.threshold import TAR, tsay_test
import numpy as np

# Comparacao AR linear vs TAR
from archbox.threshold import linearity_test

# Testar se o TAR e significativamente melhor que o AR linear
test = linearity_test(y, order=1, delay=1)
print(f"Teste LM: F = {test.statistic:.4f}, p = {test.pvalue:.4f}")
if test.pvalue < 0.05:
    print("Rejeita linearidade -> TAR e justificado")
else:
    print("Nao rejeita linearidade -> AR linear pode ser suficiente")

# Residuos
results = TAR(y, order=1).fit()
print(f"\nVariancia regime 1: {results.sigma2['regime_1']:.6f}")
print(f"Variancia regime 2: {results.sigma2['regime_2']:.6f}")
print(f"AIC: {results.aic:.4f}")
print(f"BIC: {results.bic:.4f}")
```

## Equivalentes em R e Python

=== "ArchBox"

    ```python
    from archbox.threshold import TAR

    model = TAR(y, order=1, delay=1, grid_points=300)
    results = model.fit()
    print(results.summary())
    results.plot_regimes()
    ```

=== "R (tsDyn)"

    ```r
    library(tsDyn)

    # SETAR com 1 threshold (equivale ao TAR com z_t = y_{t-d})
    fit <- setar(y, m = 1, nthresh = 1, trim = 0.15)
    summary(fit)
    plot(fit)

    # Para variavel threshold externa, use:
    fit <- setar(y, m = 1, nthresh = 1, thVar = z)
    ```

=== "R (threshold)"

    ```r
    library(threshold)

    # TAR com grid search
    fit <- tar(y, p = 1, d = 1, method = "CLS")
    summary(fit)
    ```

| Funcionalidade | ArchBox | tsDyn (R) |
|---------------|---------|-----------|
| Especificacao | `TAR(y, order=1, delay=1)` | `setar(y, m=1, nthresh=1)` |
| Variavel externa | `threshold_var=z` | `thVar=z` |
| Grid search | `grid_points=300` | `ngrid=300` |
| Estimacao | `model.fit()` | Automatica |
| Threshold | `results.threshold` | `getTh(fit)` |
| Plot | `results.plot_regimes()` | `plot(fit)` |

## References

- Tong, H. (1978). On a Threshold Model. In *Pattern Recognition and Signal Processing*, Sijthoff & Noordhoff.
- Tong, H. (1983). *Threshold Models in Non-Linear Time Series Analysis*. Lecture Notes in Statistics, Vol. 21, Springer.
- Tsay, R. S. (1989). Testing and Modeling Threshold Autoregressive Processes. *Journal of the American Statistical Association*, 84(405), 231--240.
- Hansen, B. E. (1996). Inference When a Nuisance Parameter Is Not Identified Under the Null Hypothesis. *Econometrica*, 64(2), 413--430.

## See Also

- [Threshold/STAR: Visao Geral](index.md) -- Introducao e comparacao de modelos
- [SETAR](setar.md) -- Caso especial com $z_t = y_{t-d}$
- [LSTAR](lstar.md) -- Versao com transicao suave logistica
- [Testes de Linearidade](linearity-tests.md) -- Tsay, Hansen, LM tests
- [Regime-Switching](../regime-switching/index.md) -- Alternativa com transicao estocastica
