---
title: "MS-VAR"
description: "Markov-Switching VAR model - multivariate regime-switching for crisis transmission and contagion analysis."
---

# MS-VAR (Markov-Switching Vector Autoregressive)

!!! info "Quick Reference"
    **Class:** `archbox.regime.MarkovSwitchingVAR`
    **Import:** `from archbox.regime import MarkovSwitchingVAR`
    **R equivalent:** `MSwM::msmFit(VAR(y, p=1), k=2, sw=c(TRUE,TRUE))`
    **Python equivalent:** Nao disponivel diretamente em statsmodels

## Overview

O modelo MS-VAR (Markov-Switching Vector Autoregressive), desenvolvido por **Krolzig (1997)**, e a extensao multivariada do MS-AR. Ele permite modelar **multiplas series temporais simultaneamente** com parametros que mudam entre regimes, capturando nao apenas mudancas na dinamica individual de cada variavel, mas tambem alteracoes na **transmissao de choques entre variaveis** e na **estrutura de covariancia**.

O MS-VAR e particularmente poderoso para:

- **Contagio financeiro**: como crises se transmitem entre mercados/paises
- **Transmissao de politica monetaria**: como a taxa de juros afeta variaveis reais em diferentes regimes
- **Ciclos economicos multivariados**: identificar regimes comuns entre indicadores
- **Spillover de volatilidade**: como a volatilidade conjunta muda entre regimes

**Quando usar:**

- Multiplas series temporais com evidencia de mudancas estruturais comuns
- Analise de contagio e transmissao de crises entre mercados
- Quando a relacao entre variaveis muda ao longo do tempo
- Modelagem de politica monetaria em diferentes regimes macroeconomicos

## Formulacao Matematica

### Modelo Geral

Seja $\mathbf{y}_t = (y_{1t}, y_{2t}, \ldots, y_{nt})'$ um vetor de $n$ variaveis. O MS(K)-VAR(p) e:

$$\mathbf{y}_t = \boldsymbol{\mu}_{s_t} + \sum_{i=1}^{p} \boldsymbol{\Phi}_{i}(s_t) \, \mathbf{y}_{t-i} + \boldsymbol{\epsilon}_t, \qquad \boldsymbol{\epsilon}_t \sim N(\mathbf{0}, \boldsymbol{\Sigma}_{s_t})$$

onde:

| Componente | Dimensao | Descricao |
|------------|----------|-----------|
| $\boldsymbol{\mu}_{s_t}$ | $n \times 1$ | Vetor de interceptos regime-dependentes |
| $\boldsymbol{\Phi}_{i}(s_t)$ | $n \times n$ | Matrizes de coeficientes VAR regime-dependentes |
| $\boldsymbol{\Sigma}_{s_t}$ | $n \times n$ | Matriz de covariancia regime-dependente |
| $s_t \in \{0, \ldots, K-1\}$ | escalar | Variavel de regime (cadeia de Markov) |

### Tipos de Switching (Nomenclatura de Krolzig)

Uma contribuicao importante de Krolzig (1997) e a **classificacao sistematica** dos tipos de switching:

| Sigla | Nome | Intercepto | AR | Variancia | Descricao |
|-------|------|:----------:|:--:|:---------:|-----------|
| **MSI** | MS-Intercept | $\checkmark$ | | | Apenas intercepto muda |
| **MSM** | MS-Mean | $\checkmark$ | | | Media muda (formulacao mean-adjusted) |
| **MSA** | MS-Autoregressive | | $\checkmark$ | | Apenas coeficientes AR mudam |
| **MSH** | MS-Heteroskedastic | | | $\checkmark$ | Apenas covariancia muda |
| **MSIH** | MS-Intercept-Heteroskedastic | $\checkmark$ | | $\checkmark$ | Intercepto e covariancia mudam |
| **MSMH** | MS-Mean-Heteroskedastic | $\checkmark$ | | $\checkmark$ | Media e covariancia mudam |
| **MSIAH** | MS-Intercept-AR-Heteroskedastic | $\checkmark$ | $\checkmark$ | $\checkmark$ | Tudo muda |

!!! tip "Escolha do tipo de switching"
    - **MSIH-VAR**: O mais usado na pratica. Intercepto e variancia mudam, coeficientes AR fixos. Bom equilibrio entre flexibilidade e parcimonia.
    - **MSH-VAR**: Quando apenas a volatilidade muda (analogia com GARCH multivariado).
    - **MSIAH-VAR**: Maximo de flexibilidade, mas requer muitos dados. Risco de sobreajuste.

### Caso Bivariado: MS(2)-VAR(1)

Para $n = 2$ variaveis e $K = 2$ regimes:

$$\begin{pmatrix} y_{1t} \\ y_{2t} \end{pmatrix} = \begin{pmatrix} \mu_{1,s_t} \\ \mu_{2,s_t} \end{pmatrix} + \begin{pmatrix} \phi_{11}(s_t) & \phi_{12}(s_t) \\ \phi_{21}(s_t) & \phi_{22}(s_t) \end{pmatrix} \begin{pmatrix} y_{1,t-1} \\ y_{2,t-1} \end{pmatrix} + \begin{pmatrix} \epsilon_{1t} \\ \epsilon_{2t} \end{pmatrix}$$

Os coeficientes $\phi_{12}(s_t)$ e $\phi_{21}(s_t)$ capturam a **transmissao cruzada** entre as variaveis, que pode diferir entre regimes — por exemplo, o contagio entre mercados pode ser mais intenso durante crises.

### Numero de Parametros

O numero de parametros cresce rapidamente com $n$ e $K$:

| Componente | Parametros por regime | Total ($K$ regimes) |
|------------|:---------------------:|:-------------------:|
| Intercepto $\boldsymbol{\mu}$ | $n$ | $K \cdot n$ |
| AR $\boldsymbol{\Phi}_i$ | $n^2$ por lag | $K \cdot p \cdot n^2$ (se switching) |
| Covariancia $\boldsymbol{\Sigma}$ | $n(n+1)/2$ | $K \cdot n(n+1)/2$ |
| Transicao $P$ | - | $K(K-1)$ |

!!! warning "Maldição da dimensionalidade"
    Para $n=5$ variaveis, $K=2$ regimes, $p=2$ lags com MSIAH: $2 \times 5 + 2 \times 2 \times 25 + 2 \times 15 + 2 = 142$ parametros. Mantenha $n$ e $K$ pequenos ou restrinja o tipo de switching.

## Quick Example

```python
import numpy as np
from archbox.regime import MarkovSwitchingVAR
from archbox.datasets import load_dataset

# Carregar retornos de dois mercados
data = load_dataset('global_markets')
returns = data[['sp500', 'ftse100']].to_numpy()

# MS(2)-VAR(1) com intercepto e variancia switching
model = MarkovSwitchingVAR(returns, k_regimes=2, order=1)
results = model.fit()
print(results.summary())
```

??? example "Output esperado"
    ```
    =================================================================
      MS-VAR Results
    =================================================================
      Observations:    500
      Regimes:         2
      Parameters:      19
      Log-Likelihood:  1456.7823
      AIC:             -2875.5646
      BIC:             -2795.6789
      Converged:       True
      Iterations:      67
    =================================================================

      Regime Parameters:
    -----------------------------------------------------------------
      Regime 0:
        mu_1                 =    -0.082345
        mu_2                 =    -0.067891
        sigma_11             =     0.000245
        sigma_12             =     0.000189
        sigma_22             =     0.000198
      Regime 1:
        mu_1                 =     0.045123
        mu_2                 =     0.038456
        sigma_11             =     0.000067
        sigma_12             =     0.000034
        sigma_22             =     0.000058

      Transition Matrix P:
    -----------------------------------------------------------------
           Regime 0  Regime 1
      S=0  0.9234    0.0766
      S=1  0.0312    0.9688

      Expected Durations:
    -----------------------------------------------------------------
        Regime 0: 13.05 periods
        Regime 1: 32.05 periods

      Ergodic Probabilities:
    -----------------------------------------------------------------
        Regime 0: 0.2892
        Regime 1: 0.7108
    =================================================================
    ```

## Guia Detalhado

### Parametros do Construtor

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | array-like | obrigatorio | Matriz de series temporais, shape (T, n) |
| `k_regimes` | int | `2` | Numero de regimes ($K$) |
| `order` | int | `1` | Ordem VAR (numero de lags) |
| `switching_mean` | bool | `True` | Se True, intercepto muda entre regimes (MSI/MSM) |
| `switching_variance` | bool | `True` | Se True, covariancia muda entre regimes (MSH) |

### Parametros de `fit()`

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `max_iter` | int | `500` | Numero maximo de iteracoes do EM |
| `tol` | float | `1e-8` | Tolerancia para convergencia |
| `n_init` | int | `5` | Numero de inicializacoes aleatorias |
| `disp` | bool | `True` | Exibir progresso |

### Exemplo: Transmissao de Crises entre Mercados

```python
import numpy as np
from archbox.regime import MarkovSwitchingVAR
from archbox.datasets import load_dataset

# 1. Carregar retornos de mercados desenvolvidos e emergentes
data = load_dataset('global_markets')
returns = data[['sp500', 'bovespa']].to_numpy()

# 2. Estimar MSIH(2)-VAR(1)
# intercepto e variancia switching, AR fixo
model = MarkovSwitchingVAR(
    returns,
    k_regimes=2,
    order=1,
    switching_mean=True,
    switching_variance=True,
)
results = model.fit()

# 3. Analisar regimes
for k in range(results.k_regimes):
    params = results.regime_params[k]
    print(f"\n--- Regime {k} ---")
    for name, value in params.items():
        print(f"  {name}: {value:.6f}")

# 4. Matriz de transicao
P = results.transition_matrix
print(f"\nMatriz de transicao:")
print(P)

# 5. Duracao esperada
durations = results.expected_durations()
for k, d in enumerate(durations):
    print(f"Regime {k}: duracao esperada = {d:.1f} periodos")

# 6. Probabilidades ergoticas
ergodic = results.ergodic_probabilities()
for k, pi in enumerate(ergodic):
    print(f"Regime {k}: probabilidade ergotica = {pi:.4f}")

# 7. Identificar regime de crise
# Regime com maior variancia = crise
sigma_0 = results.regime_params[0].get('sigma_11', 0)
sigma_1 = results.regime_params[1].get('sigma_11', 0)
crisis_regime = 0 if sigma_0 > sigma_1 else 1
print(f"\nRegime de crise: {crisis_regime}")

# 8. Probabilidade de crise ao longo do tempo
crisis_prob = results.smoothed_probs[:, crisis_regime]
print(f"Periodos em crise (P > 0.5): {(crisis_prob > 0.5).sum()}")

# 9. Visualizar
results.plot_regimes()
results.plot_probabilities(regime=crisis_regime)
```

### Analise de Contagio

O MS-VAR permite analisar como a transmissao de choques entre mercados muda entre regimes:

```python
# Comparar correlacao entre regimes
for k in range(results.k_regimes):
    params = results.regime_params[k]
    # Extrair elementos da covariancia
    s11 = params.get('sigma_11', 1)
    s12 = params.get('sigma_12', 0)
    s22 = params.get('sigma_22', 1)
    corr = s12 / np.sqrt(s11 * s22)
    print(f"Regime {k}: correlacao = {corr:.4f}")

# Interpretacao:
# Se corr_crise > corr_normal -> contagio
# Os mercados ficam mais correlacionados durante crises
```

### Resultados

| Atributo | Descricao |
|----------|-----------|
| `results.params` | Todos os parametros estimados (ndarray) |
| `results.regime_params` | Parametros organizados por regime (dict) |
| `results.transition_matrix` | Matriz de transicao $P$, shape (K, K) |
| `results.filtered_probs` | Probabilidades filtradas, shape (T, K) |
| `results.smoothed_probs` | Probabilidades suavizadas, shape (T, K) |
| `results.predicted_probs` | Probabilidades preditas, shape (T, K) |
| `results.loglike` | Log-verossimilhanca |
| `results.aic` | Criterio de Informacao de Akaike |
| `results.bic` | Criterio de Informacao Bayesiano |

| Metodo | Descricao |
|--------|-----------|
| `results.summary()` | Tabela formatada de resultados |
| `results.expected_durations()` | Duracao esperada de cada regime |
| `results.ergodic_probabilities()` | Probabilidades ergoticas |
| `results.classify()` | Classificar observacoes em regimes |
| `results.plot_regimes(y)` | Grafico com shading de regimes |
| `results.plot_probabilities(regime)` | Grafico de probabilidades |

## Interpretacao

### Tipos de Switching na Pratica

A escolha do tipo de switching depende da hipotese economica:

**MSH-VAR** (apenas variancia switching):

- Hipotese: as relacoes entre variaveis sao estaveis, mas a volatilidade conjunta muda
- Uso: mercados com regime de calma vs. turbulencia, sem mudanca nas relacoes causais

**MSIH-VAR** (intercepto + variancia switching):

- Hipotese: o nivel medio e a volatilidade mudam simultaneamente
- Uso: ciclos economicos onde recessoes tem media negativa e alta volatilidade

**MSIAH-VAR** (tudo switching):

- Hipotese: toda a estrutura de dependencia muda entre regimes
- Uso: mudancas profundas na transmissao (e.g., antes/depois de uma uniao monetaria)

### Contagio vs. Interdependencia

O MS-VAR permite distinguir entre:

- **Interdependencia**: correlacao alta que persiste em todos os regimes → nao e contagio
- **Contagio**: aumento significativo na correlacao/transmissao durante o regime de crise

$$\rho_{\text{crise}} \gg \rho_{\text{normal}} \Rightarrow \text{Evidencia de contagio}$$

### Selecao de Modelo

```python
# Comparar especificacoes via BIC
configs = [
    {"switching_mean": False, "switching_variance": True},   # MSH
    {"switching_mean": True,  "switching_variance": False},   # MSI
    {"switching_mean": True,  "switching_variance": True},    # MSIH
]

labels = ["MSH-VAR", "MSI-VAR", "MSIH-VAR"]

for label, cfg in zip(labels, configs):
    model = MarkovSwitchingVAR(returns, k_regimes=2, order=1, **cfg)
    res = model.fit()
    print(f"{label}: LogL={res.loglike:.2f}, AIC={res.aic:.2f}, BIC={res.bic:.2f}")
```

!!! note "Parcimonia"
    O BIC tende a selecionar modelos mais parcimoniosos que o AIC. Para MS-VAR com muitos parametros, o BIC e geralmente preferivel para evitar sobreajuste.

## Diagnosticos

### Verificar Convergencia e Robustez

```python
# Multiplas inicializacoes
model = MarkovSwitchingVAR(returns, k_regimes=2, order=1)
results = model.fit(n_init=10)

print(f"Convergiu: {results.converged}")
print(f"Iteracoes: {results.n_iter}")
print(f"LogL: {results.loglike:.4f}")
```

### Qualidade da Classificacao

```python
# RCM para MS-VAR
smoothed = results.smoothed_probs
rcm = 400.0 / results.nobs * np.sum(
    smoothed[:, 0] * smoothed[:, 1]
)
print(f"RCM: {rcm:.2f} (0=perfeita, 100=nenhuma separacao)")
```

### Escolha da Ordem VAR

```python
# Comparar ordens de lag
for p in [1, 2, 3]:
    model = MarkovSwitchingVAR(returns, k_regimes=2, order=p)
    res = model.fit()
    print(f"MS(2)-VAR({p}): BIC={res.bic:.2f}")
```

## Equivalentes em R e Python

=== "ArchBox"

    ```python
    from archbox.regime import MarkovSwitchingVAR

    model = MarkovSwitchingVAR(returns, k_regimes=2, order=1)
    results = model.fit()
    print(results.summary())
    ```

=== "R (MSwM)"

    ```r
    library(MSwM)

    # VAR base com p=1
    var_mod <- VAR(y, p = 1)

    # MS(2)-VAR com switching
    ms_var <- msmFit(var_mod, k = 2, sw = c(TRUE, TRUE))
    summary(ms_var)
    ```

=== "R (MSBVAR)"

    ```r
    library(MSBVAR)

    # MS(2)-VAR(1)
    ms_var <- msbvar(
      Y = y,
      p = 1,
      h = 2,
      lambda0 = 0.1,
      lambda1 = 0.1
    )
    summary(ms_var)
    ```

| Funcionalidade | ArchBox | MSwM (R) | MSBVAR (R) |
|---------------|---------|----------|------------|
| Especificacao | `MarkovSwitchingVAR(y, k_regimes=2, order=1)` | `msmFit(VAR(y,p=1), k=2)` | `msbvar(Y=y, p=1, h=2)` |
| Tipos de switching | `switching_mean`, `switching_variance` | `sw=c(...)` | Via priors |
| Estimacao | EM | EM | Bayesiano (Gibbs) |
| Probabilidades | `results.smoothed_probs` | `@Fit@smoProb` | Posterior draws |

## References

- Krolzig, H.-M. (1997). *Markov-Switching Vector Autoregressions: Modelling, Statistical Inference, and Application to Business Cycle Analysis*. Springer.
- Krolzig, H.-M. (1998). Econometric Modelling of Markov-Switching Vector Autoregressions using MSVAR for Ox. *Discussion Paper, Department of Economics, University of Oxford*.
- Hamilton, J. D. (1989). A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle. *Econometrica*, 57(2), 357--384.
- Ang, A., & Bekaert, G. (2002). International Asset Allocation with Regime Shifts. *Review of Financial Studies*, 15(4), 1137--1187.
- Forbes, K. J., & Rigobon, R. (2002). No Contagion, Only Interdependence: Measuring Stock Market Comovements. *The Journal of Finance*, 57(5), 2223--2261.

## See Also

- [Regime-Switching: Visao Geral](index.md) -- Introducao e comparacao de modelos
- [MS-AR](ms-ar.md) -- Versao univariada do modelo
- [MS-GARCH](ms-garch.md) -- Volatilidade condicional com mudanca de regime
- [DCC](../multivariate/dcc.md) -- Correlacao dinamica sem regimes
- [BEKK](../multivariate/bekk.md) -- Covariancia dinamica sem regimes
