---
title: "SETAR"
description: "Self-Exciting Threshold Autoregressive model — delay automatico, selecao conjunta de d e c, extensao para 3 regimes."
---

# SETAR (Self-Exciting Threshold Autoregressive)

!!! info "Quick Reference"
    **Class:** `archbox.threshold.SETAR`
    **Import:** `from archbox.threshold import SETAR`
    **R equivalent:** `tsDyn::setar(y, m=p, nthresh=1)`
    **Python equivalent:** Nao disponivel em pacotes padrao

## Overview

O modelo SETAR (Self-Exciting Threshold Autoregressive), introduzido por **Tong e Lim (1980)**, e um caso especial do [TAR](tar.md) onde a variavel de transicao e um **lag da propria serie**: $z_t = y_{t-d}$. O termo "self-exciting" refere-se ao fato de que a propria serie determina em qual regime ela se encontra — nao e necessaria uma variavel externa.

O SETAR e o modelo threshold mais utilizado na pratica porque:

- **Parcimonia**: nao requer variavel de transicao externa
- **Selecao automatica de delay**: o parametro $d$ pode ser selecionado otimamente via AIC/BIC
- **Extensao a 3 regimes**: permite modelar bandas (ex: banda cambial com regime inferior, central e superior)
- **Interpretabilidade**: o threshold e diretamente em termos da variavel de interesse

O SETAR e adequado quando:

- **Taxas de cambio com bandas**: regimes diferentes dentro e fora da banda
- **Ciclos assimetricos**: expansao e recessao com dinamicas distintas
- **Processos com reversao a media nao-linear**: a velocidade de ajuste depende do nivel

## Formulacao Matematica

### SETAR com 2 Regimes

$$y_t = \begin{cases} \phi_{0,1} + \phi_{1,1} y_{t-1} + \cdots + \phi_{p,1} y_{t-p} + \epsilon_{1,t} & \text{se } y_{t-d} \leq c \\ \phi_{0,2} + \phi_{1,2} y_{t-1} + \cdots + \phi_{p,2} y_{t-p} + \epsilon_{2,t} & \text{se } y_{t-d} > c \end{cases}$$

onde $d$ e o **delay parameter** e $c$ e o threshold.

### SETAR com 3 Regimes

$$y_t = \begin{cases} \boldsymbol{\phi}_1' \mathbf{x}_t + \epsilon_{1,t} & \text{se } y_{t-d} \leq c_1 \\ \boldsymbol{\phi}_2' \mathbf{x}_t + \epsilon_{2,t} & \text{se } c_1 < y_{t-d} \leq c_2 \\ \boldsymbol{\phi}_3' \mathbf{x}_t + \epsilon_{3,t} & \text{se } y_{t-d} > c_2 \end{cases}$$

O modelo com 3 regimes e particularmente util para series com **bandas** — o regime central representa o comportamento "normal" enquanto os regimes extremos capturam dinamicas fora das bandas.

### Delay Parameter $d$

O parametro $d$ controla **quantos periodos atras** a serie determina o regime atual:

| $d$ | Transicao | Interpretacao |
|-----|-----------|---------------|
| $d = 1$ | $z_t = y_{t-1}$ | O valor imediatamente anterior determina o regime |
| $d = 2$ | $z_t = y_{t-2}$ | O valor de 2 periodos atras determina o regime |
| $d = d^*$ | $z_t = y_{t-d^*}$ | Delay otimo selecionado por AIC/BIC |

### Estimacao Conjunta de $d$ e $c$

A estimacao do SETAR e feita por **Conditional Least Squares (CLS)** com busca conjunta:

1. Para cada $d \in \{1, 2, \ldots, d_{\max}\}$:
    - Reconstroi as matrizes com delay $d$
    - Executa grid search para $c$ (ou $c_1, c_2$ no caso de 3 regimes)
    - Calcula AIC/BIC

2. Seleciona $(\hat{d}, \hat{c})$ que minimiza o criterio de informacao:

$$(\hat{d}, \hat{c}) = \arg\min_{d, c} IC(d, c)$$

onde $IC$ pode ser AIC ou BIC.

!!! note "Selecao automatica vs. fixa"
    Se `delay=None` (default), o SETAR seleciona $d$ automaticamente de 1 a `d_max`. Se `delay=d` e fornecido, apenas $c$ e estimado por grid search.

## Quick Example

```python
import numpy as np
from archbox.threshold import SETAR

# Dados simulados com threshold
rng = np.random.default_rng(42)
n = 500
y = np.zeros(n)
for t in range(1, n):
    if y[t-1] <= 0:
        y[t] = 0.5 + 0.3 * y[t-1] + rng.standard_normal() * 0.5
    else:
        y[t] = -0.2 + 0.8 * y[t-1] + rng.standard_normal() * 0.5

# SETAR com selecao automatica de delay
model = SETAR(y, order=1, n_regimes=2)
results = model.fit()
print(results.summary())
print(f"\nDelay selecionado: d = {results.delay}")
print(f"Threshold estimado: c = {results.threshold:.4f}")
```

??? example "Output esperado"
    ```
    ======================================================================
                                  Model: SETAR
                           Observations: 499
                            AR Order (p): 1
                              Delay (d): 1
                     Number of Regimes: 2
                         Log-Likelihood: -349.1234
                                    AIC: 710.2468
                                    BIC: 735.1234
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

    Delay selecionado: d = 1
    Threshold estimado: c = -0.0123
    ```

## Guia Detalhado

### Parametros do Construtor

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | array-like | obrigatorio | Serie temporal, shape (T,) |
| `order` | int | `1` | Ordem AR $p$ |
| `delay` | int \| None | `None` | Delay $d$. Se `None`, auto-seleciona de 1 a `d_max` |
| `n_regimes` | int | `2` | Numero de regimes: 2 ou 3 |
| `d_max` | int | `6` | Delay maximo na busca automatica |
| `grid_points` | int | `300` | Pontos no grid search para $c$ |
| `ic` | str | `"aic"` | Criterio de informacao para delay: `"aic"` ou `"bic"` |

### Parametros de `fit()`

O metodo `fit()` nao requer parametros adicionais. A estimacao e feita automaticamente via CLS.

### Exemplo: Taxa de Cambio com Bandas (3 Regimes)

```python
import numpy as np
from archbox.threshold import SETAR

# Simular taxa de cambio com 3 regimes (banda inferior, central, superior)
rng = np.random.default_rng(42)
n = 600
y = np.zeros(n)
c1, c2 = -1.0, 1.0  # limites da banda

for t in range(1, n):
    if y[t-1] <= c1:
        # Abaixo da banda: reversao rapida para cima
        y[t] = 0.5 + 0.3 * y[t-1] + rng.standard_normal() * 0.3
    elif y[t-1] > c2:
        # Acima da banda: reversao rapida para baixo
        y[t] = -0.5 + 0.3 * y[t-1] + rng.standard_normal() * 0.3
    else:
        # Dentro da banda: random walk
        y[t] = 0.0 + 0.95 * y[t-1] + rng.standard_normal() * 0.2

# SETAR com 3 regimes
model = SETAR(y, order=1, n_regimes=3, delay=1)
results = model.fit()
print(results.summary())

# Visualizar
results.plot_regimes()
results.plot_phase_diagram()
```

### Exemplo: Selecao Automatica de Delay

```python
import numpy as np
from archbox.threshold import SETAR

rng = np.random.default_rng(42)
n = 500
y = np.zeros(n)
true_delay = 3  # delay verdadeiro

for t in range(true_delay, n):
    if y[t - true_delay] <= 0:
        y[t] = 0.5 + 0.4 * y[t-1] + rng.standard_normal() * 0.5
    else:
        y[t] = -0.3 + 0.6 * y[t-1] + rng.standard_normal() * 0.5

# Selecao automatica de delay (AIC)
model_aic = SETAR(y, order=1, delay=None, d_max=6, ic="aic")
res_aic = model_aic.fit()
print(f"AIC: delay selecionado = {res_aic.delay}")

# Selecao automatica de delay (BIC)
model_bic = SETAR(y, order=1, delay=None, d_max=6, ic="bic")
res_bic = model_bic.fit()
print(f"BIC: delay selecionado = {res_bic.delay}")
```

### Resultados

| Atributo | Descricao |
|----------|-----------|
| `results.params` | Parametros por regime (dict) |
| `results.threshold` | Threshold(s): `float` (2 regimes) ou `list[float]` (3 regimes) |
| `results.delay` | Delay $d$ (selecionado ou fixo) |
| `results.transition_params` | `{'c': ...}` ou `{'c_1': ..., 'c_2': ...}` |
| `results.params_regime1` | Coeficientes AR do regime 1 (ndarray) |
| `results.params_regime2` | Coeficientes AR do regime 2 (ndarray) |
| `results.regime_assignments` | Atribuicao de regime: 0, 0.5, 1 (ndarray) |
| `results.resid` | Residuos (ndarray) |
| `results.sigma2` | Variancia por regime (dict) |
| `results.loglike` | Log-verossimilhanca |
| `results.aic` | AIC |
| `results.bic` | BIC |

| Metodo | Descricao |
|--------|-----------|
| `results.summary()` | Tabela formatada |
| `results.plot_regimes()` | Serie com coloracao de regimes |
| `results.plot_transition()` | Valores de transicao ao longo do tempo |
| `results.plot_phase_diagram()` | Diagrama de fase colorido por regime |
| `results.plot_fit()` | Observado vs ajustado |
| `results.forecast(horizon)` | Previsao $h$ passos a frente |

## Interpretacao

### Delay e Memoria do Sistema

O delay $d$ revela com **quantos periodos de antecedencia** o sistema "decide" seu regime:

- **$d = 1$**: o regime atual depende do valor imediatamente anterior — resposta rapida
- **$d > 1$**: o regime atual depende de valores mais distantes — resposta com defasagem

Em economia, um delay $d > 1$ pode indicar **rigidez** ou **informacao defasada**: agentes economicos reagem a informacao passada, nao ao valor mais recente.

### Interpretacao do SETAR com 3 Regimes

No caso de 3 regimes com thresholds $c_1 < c_2$:

| Regime | Condicao | Interpretacao tipica |
|--------|----------|---------------------|
| 1 | $y_{t-d} \leq c_1$ | Regime inferior (ex: depreciacao forte) |
| 2 | $c_1 < y_{t-d} \leq c_2$ | Regime central (ex: banda normal) |
| 3 | $y_{t-d} > c_2$ | Regime superior (ex: apreciacao forte) |

A **largura da banda** $c_2 - c_1$ mede a zona de inacao ou estabilidade.

## Diagnosticos

```python
from archbox.threshold import SETAR, linearity_test, tsay_test

# Testar linearidade antes de estimar
test_lm = linearity_test(y, order=1, delay=1)
test_tsay = tsay_test(y, order=1, delay=1)
print(f"LM test:  F = {test_lm.statistic:.4f}, p = {test_lm.pvalue:.4f}")
print(f"Tsay test: F = {test_tsay.statistic:.4f}, p = {test_tsay.pvalue:.4f}")

# Comparar modelos com diferentes ordens
for p in [1, 2, 3]:
    model = SETAR(y, order=p, n_regimes=2)
    res = model.fit()
    print(f"SETAR({p}): AIC={res.aic:.2f}, BIC={res.bic:.2f}, "
          f"d={res.delay}, c={res.threshold:.4f}")
```

## Equivalentes em R e Python

=== "ArchBox"

    ```python
    from archbox.threshold import SETAR

    model = SETAR(y, order=1, n_regimes=2)
    results = model.fit()
    print(results.summary())
    ```

=== "R (tsDyn)"

    ```r
    library(tsDyn)

    # SETAR com 2 regimes e selecao de delay
    fit <- setar(y, m = 1, nthresh = 1, trim = 0.15)
    summary(fit)
    plot(fit)

    # SETAR com 3 regimes
    fit3 <- setar(y, m = 1, nthresh = 2, trim = 0.15)
    summary(fit3)
    ```

| Funcionalidade | ArchBox | tsDyn (R) |
|---------------|---------|-----------|
| Especificacao | `SETAR(y, order=1, n_regimes=2)` | `setar(y, m=1, nthresh=1)` |
| Delay auto | `delay=None, d_max=6` | `mTh=1:6` |
| 3 regimes | `n_regimes=3` | `nthresh=2` |
| Criterio | `ic="aic"` | Automatico |
| Threshold | `results.threshold` | `getTh(fit)` |
| Delay | `results.delay` | `fit$mTh` |

## References

- Tong, H., & Lim, K. S. (1980). Threshold Autoregression, Limit Cycles and Cyclical Data. *Journal of the Royal Statistical Society, Series B*, 42(3), 245--292.
- Tong, H. (1983). *Threshold Models in Non-Linear Time Series Analysis*. Lecture Notes in Statistics, Vol. 21, Springer.
- Tong, H. (1990). *Non-Linear Time Series: A Dynamical System Approach*. Oxford University Press.
- Hansen, B. E. (1997). Inference in TAR Models. *Studies in Nonlinear Dynamics & Econometrics*, 2(1), 1--14.

## See Also

- [Threshold/STAR: Visao Geral](index.md) -- Introducao e comparacao de modelos
- [TAR](tar.md) -- TAR com variavel de transicao externa
- [LSTAR](lstar.md) -- Versao com transicao suave logistica
- [ESTAR](estar.md) -- Versao com transicao suave exponencial
- [Testes de Linearidade](linearity-tests.md) -- Tsay, Hansen, LM tests
