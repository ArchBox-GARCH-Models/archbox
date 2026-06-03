---
title: "MS-AR"
description: "Markov-Switching Autoregressive model - detects regime changes in mean, variance and AR dynamics."
---

# MS-AR (Markov-Switching Autoregressive)

!!! info "Quick Reference"
    **Class:** `archbox.regime.MarkovSwitchingAR`
    **Import:** `from archbox.regime import MarkovSwitchingAR`
    **R equivalent:** `MSwM::msmFit(lm(y ~ 1), k = 2, sw = c(TRUE, TRUE))`
    **Python equivalent:** `statsmodels.tsa.regime_switching.markov_autoregression.MarkovAutoregression`

## Overview

O modelo MS-AR (Markov-Switching Autoregressive), proposto por **Hamilton (1989)**, e o modelo de regime-switching mais classico e influente em econometria. Ele permite que a **media**, a **variancia** e opcionalmente os **coeficientes autorregressivos** de uma serie temporal mudem entre $K$ regimes discretos, governados por uma cadeia de Markov oculta.

O MS-AR e particularmente adequado para:

- **Ciclos economicos**: detectar alternancia entre expansao e recessao
- **Mudancas na volatilidade**: identificar regimes de alta e baixa volatilidade
- **Quebras estruturais recorrentes**: capturar mudancas que se repetem ao longo do tempo
- **Datacao de regimes**: estimar probabilidades de estar em cada regime a cada ponto no tempo

**Quando usar:**

- Series univariadas com evidencia de mudancas estruturais
- Quando se deseja classificar periodos em regimes distintos
- Modelagem de ciclos economicos (PIB, producao industrial)
- Series financeiras com alternancia entre periodos de calmaria e crise

## Formulacao Matematica

### Modelo Geral MS(K)-AR(p)

$$y_t = \mu_{s_t} + \sum_{i=1}^{p} \phi_{i,s_t} (y_{t-i} - \mu_{s_{t-i}}) + \sigma_{s_t} \epsilon_t, \qquad \epsilon_t \sim N(0, 1)$$

onde $s_t \in \{0, 1, \ldots, K-1\}$ e a variavel de regime que segue uma cadeia de Markov de primeira ordem com matriz de transicao:

$$P(s_t = j \mid s_{t-1} = i) = p_{ij}$$

### Componentes Regime-Dependentes

| Componente | Parametro | Switching | Descricao |
|------------|-----------|-----------|-----------|
| Media | $\mu_{s_t}$ | Sim (default) | Nivel medio em cada regime |
| Variancia | $\sigma^2_{s_t}$ | Sim (default) | Volatilidade em cada regime |
| AR | $\phi_{i,s_t}$ | Opcional | Dinamica autorregressiva em cada regime |

### Caso Especial: MS(2)-AR(p) com Media e Variancia Switching

O caso mais comum na pratica utiliza 2 regimes com media e variancia switching:

$$y_t = \mu_{s_t} + \sum_{i=1}^{p} \phi_i (y_{t-i} - \mu_{s_{t-i}}) + \sigma_{s_t} \epsilon_t$$

**Regime 0 (recessao/crise):**

- Media baixa (ou negativa): $\mu_0 < \mu_1$
- Alta volatilidade: $\sigma_0 > \sigma_1$

**Regime 1 (expansao/normalidade):**

- Media alta (positiva): $\mu_1 > \mu_0$
- Baixa volatilidade: $\sigma_1 < \sigma_0$

### Matriz de Transicao (2 regimes)

$$P = \begin{pmatrix} p_{00} & p_{01} \\ p_{10} & p_{11} \end{pmatrix} = \begin{pmatrix} p_{00} & 1 - p_{00} \\ 1 - p_{11} & p_{11} \end{pmatrix}$$

**Duracao esperada** de cada regime:

$$E[D_0] = \frac{1}{1 - p_{00}}, \qquad E[D_1] = \frac{1}{1 - p_{11}}$$

**Probabilidades ergoticas:**

$$\pi_0 = \frac{1 - p_{11}}{2 - p_{00} - p_{11}}, \qquad \pi_1 = \frac{1 - p_{00}}{2 - p_{00} - p_{11}}$$

### Log-Verossimilhanca

A log-verossimilhanca e computada integrando sobre todos os possiveis caminhos de regime via o **Hamilton filter**:

$$\log L = \sum_{t=1}^{T} \log \left( \sum_{j=0}^{K-1} f(y_t \mid s_t = j, \mathcal{Y}_{t-1}) \cdot P(s_t = j \mid \mathcal{Y}_{t-1}) \right)$$

onde $f(y_t \mid s_t = j, \mathcal{Y}_{t-1})$ e a densidade condicional no regime $j$:

$$f(y_t \mid s_t = j, \mathcal{Y}_{t-1}) = \frac{1}{\sqrt{2\pi \sigma_j^2}} \exp\left( -\frac{(y_t - \mu_j - \sum_i \phi_i (y_{t-i} - \mu_{s_{t-i}}))^2}{2\sigma_j^2} \right)$$

## Quick Example

```python
from archbox.regime import MarkovSwitchingAR
from archbox.datasets import load_dataset

# Carregar crescimento do PIB dos EUA
gdp = load_dataset('us_gdp_quarterly')

# MS(2)-AR(4) classico de Hamilton
model = MarkovSwitchingAR(gdp['growth'], k_regimes=2, order=4)
results = model.fit()
print(results.summary())
```

??? example "Output esperado"
    ```
    =================================================================
      MS-AR Results
    =================================================================
      Observations:    220
      Regimes:         2
      Parameters:      12
      Log-Likelihood:  -198.4532
      AIC:             420.9064
      BIC:             461.5678
      Converged:       True
      Iterations:      42
    =================================================================

      Regime Parameters:
    -----------------------------------------------------------------
      Regime 0:
        mu                   =    -0.358942
        sigma                =     1.682345
        phi_1                =     0.012341
        phi_2                =    -0.058672
        phi_3                =    -0.023456
        phi_4                =    -0.198234
      Regime 1:
        mu                   =     1.164523
        sigma                =     0.769821
        phi_1                =     0.012341
        phi_2                =    -0.058672
        phi_3                =    -0.023456
        phi_4                =    -0.198234

      Transition Matrix P:
    -----------------------------------------------------------------
           Regime 0  Regime 1
      S=0  0.7534    0.2466
      S=1  0.0452    0.9548

      Expected Durations:
    -----------------------------------------------------------------
        Regime 0: 4.06 periods
        Regime 1: 22.12 periods

      Ergodic Probabilities:
    -----------------------------------------------------------------
        Regime 0: 0.1553
        Regime 1: 0.8447
    =================================================================
    ```

## Guia Detalhado

### Parametros do Construtor

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | array-like | obrigatorio | Serie temporal de observacoes, shape (T,) |
| `k_regimes` | int | `2` | Numero de regimes ($K$) |
| `order` | int | `4` | Ordem AR (numero de lags) |
| `switching_mean` | bool | `True` | Se True, a media muda entre regimes |
| `switching_variance` | bool | `True` | Se True, a variancia muda entre regimes |
| `switching_ar` | bool | `False` | Se True, coeficientes AR mudam entre regimes |

### Parametros de `fit()`

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `max_iter` | int | `500` | Numero maximo de iteracoes do EM |
| `tol` | float | `1e-8` | Tolerancia para convergencia |
| `n_init` | int | `5` | Numero de inicializacoes aleatorias |
| `disp` | bool | `True` | Exibir progresso da estimacao |

### Exemplo: Detectando Recessoes no PIB dos EUA

O exemplo classico de Hamilton (1989) utiliza o crescimento do PIB trimestral dos EUA para identificar regimes de expansao e recessao:

```python
from archbox.regime import MarkovSwitchingAR
from archbox.datasets import load_dataset
import numpy as np

# 1. Carregar dados
gdp = load_dataset('us_gdp_quarterly')
growth = gdp['growth'].to_numpy()

# 2. Estimar MS(2)-AR(4) com media e variancia switching
model = MarkovSwitchingAR(
    growth,
    k_regimes=2,
    order=4,
    switching_mean=True,
    switching_variance=True,
    switching_ar=False,
)
results = model.fit()

# 3. Identificar regimes
# Regime com menor media = recessao
regime_params = results.regime_params
mu_0 = regime_params[0]['mu']
mu_1 = regime_params[1]['mu']
recession_regime = 0 if mu_0 < mu_1 else 1

print(f"Regime de recessao: {recession_regime}")
print(f"  Media: {regime_params[recession_regime]['mu']:.4f}")
print(f"  Sigma: {regime_params[recession_regime]['sigma']:.4f}")

expansion_regime = 1 - recession_regime
print(f"\nRegime de expansao: {expansion_regime}")
print(f"  Media: {regime_params[expansion_regime]['mu']:.4f}")
print(f"  Sigma: {regime_params[expansion_regime]['sigma']:.4f}")

# 4. Probabilidade de recessao ao longo do tempo
recession_prob = results.smoothed_probs[:, recession_regime]
print(f"\nPeriodos com P(recessao) > 0.5: {(recession_prob > 0.5).sum()}")

# 5. Duracao esperada de cada regime
durations = results.expected_durations()
print(f"Duracao esperada da recessao: {durations[recession_regime]:.1f} trimestres")
print(f"Duracao esperada da expansao: {durations[expansion_regime]:.1f} trimestres")

# 6. Visualizar
results.plot_regimes(y=growth)
results.plot_probabilities(regime=recession_regime)
```

### Resultados

| Atributo | Descricao |
|----------|-----------|
| `results.params` | Todos os parametros estimados (ndarray) |
| `results.regime_params` | Parametros organizados por regime (dict) |
| `results.transition_matrix` | Matriz de transicao $P$, shape (K, K) |
| `results.filtered_probs` | Probabilidades filtradas $P(s_t=j \mid \mathcal{Y}_t)$, shape (T, K) |
| `results.smoothed_probs` | Probabilidades suavizadas $P(s_t=j \mid \mathcal{Y}_T)$, shape (T, K) |
| `results.predicted_probs` | Probabilidades preditas $P(s_t=j \mid \mathcal{Y}_{t-1})$, shape (T, K) |
| `results.loglike` | Log-verossimilhanca |
| `results.aic` | Criterio de Informacao de Akaike |
| `results.bic` | Criterio de Informacao Bayesiano |
| `results.converged` | Se a estimacao convergiu |
| `results.n_iter` | Numero de iteracoes ate convergencia |

| Metodo | Descricao |
|--------|-----------|
| `results.summary()` | Tabela formatada com todos os resultados |
| `results.expected_durations()` | Duracao esperada de cada regime: $1/(1-p_{jj})$ |
| `results.ergodic_probabilities()` | Probabilidades ergoticas (estacionarias) |
| `results.classify(threshold)` | Classificar cada observacao no regime mais provavel |
| `results.plot_regimes(y)` | Grafico da serie com shading de regimes |
| `results.plot_probabilities(regime)` | Grafico das probabilidades de regime |

## Interpretacao

### Identificacao de Regimes

A identificacao dos regimes e feita *a posteriori* com base nos parametros estimados. Convencoes comuns:

| Criterio | Regime 0 | Regime 1 |
|----------|----------|----------|
| Media | Baixa ($\mu_0 < \mu_1$) | Alta ($\mu_1 > \mu_0$) |
| Volatilidade | Alta ($\sigma_0 > \sigma_1$) | Baixa ($\sigma_1 < \sigma_0$) |
| Interpretacao (PIB) | Recessao | Expansao |
| Interpretacao (mercado) | Bear market / crise | Bull market / normalidade |

!!! warning "Label switching"
    Os regimes nao tem identidade fixa — o otimizador pode rotular regime 0 como expansao e regime 1 como recessao, ou vice-versa. Sempre identifique os regimes pelos parametros estimados, nao pelo indice numerico.

### Persistencia dos Regimes

Regimes tipicamente sao altamente persistentes ($p_{jj} > 0.9$), o que significa que a economia tende a permanecer no regime atual. Valores tipicos para dados trimestrais do PIB:

- $p_{00}$ (persistencia da recessao): 0.70--0.85 → duracao de 3--7 trimestres
- $p_{11}$ (persistencia da expansao): 0.93--0.97 → duracao de 14--33 trimestres

### Comparacao de Modelos

```python
from archbox.regime import MarkovSwitchingAR

# Comparar diferentes especificacoes
specs = [
    {"order": 1, "switching_ar": False},
    {"order": 2, "switching_ar": False},
    {"order": 4, "switching_ar": False},
    {"order": 4, "switching_ar": True},
]

for spec in specs:
    model = MarkovSwitchingAR(growth, k_regimes=2, **spec)
    res = model.fit()
    ar_label = "SW-AR" if spec["switching_ar"] else "AR"
    print(f"MS(2)-{ar_label}({spec['order']}): "
          f"LogL={res.loglike:.2f}, AIC={res.aic:.2f}, BIC={res.bic:.2f}")
```

### Numero de Regimes

A escolha do numero de regimes $K$ e uma das decisoes mais importantes. Na pratica:

- **$K = 2$**: Caso mais comum. Suficiente para a maioria das aplicacoes (expansao/recessao, alta/baixa vol)
- **$K = 3$**: Util quando ha um regime intermediario (e.g., crescimento moderado)
- **$K > 3$**: Raramente justificado; risco de sobreajuste e dificuldade de interpretacao

!!! note "Teste formal para o numero de regimes"
    O likelihood ratio test padrao nao e valido para testar $K$ vs $K+1$ regimes (os parametros nao identificados sob $H_0$ violam as condicoes de regularidade). Criterios de informacao (AIC, BIC) sao a abordagem mais comum na pratica.

## Diagnosticos

### Verificar Convergencia

```python
# Verificar se o EM convergiu
print(f"Convergiu: {results.converged}")
print(f"Iteracoes: {results.n_iter}")

# Multiplas inicializacoes para robustez
model = MarkovSwitchingAR(growth, k_regimes=2, order=4)
results = model.fit(n_init=10)  # 10 inicializacoes
```

### Qualidade da Classificacao

```python
# Regime Classification Measure (RCM)
# Valores proximos de 0 = boa classificacao
# Valores proximos de 100 = classificacao incerta
smoothed = results.smoothed_probs
rcm = 400.0 / results.nobs * np.sum(
    smoothed[:, 0] * smoothed[:, 1]
)
print(f"RCM: {rcm:.2f}")
if rcm < 50:
    print("Boa separacao entre regimes")
else:
    print("Classificacao incerta — regimes pouco distintos")
```

### Analise de Residuos

```python
# Classificar e analisar residuos por regime
regimes = results.classify()
for k in range(results.k_regimes):
    mask = regimes == k
    y_regime = growth[mask]
    mu_k = results.regime_params[k]['mu']
    residuals = y_regime - mu_k
    print(f"Regime {k}: n={mask.sum()}, "
          f"mean_resid={residuals.mean():.4f}, "
          f"std_resid={residuals.std():.4f}")
```

## Equivalentes em R e Python

=== "ArchBox"

    ```python
    from archbox.regime import MarkovSwitchingAR
    from archbox.datasets import load_dataset

    gdp = load_dataset('us_gdp_quarterly')
    model = MarkovSwitchingAR(gdp['growth'], k_regimes=2, order=4)
    results = model.fit()
    print(results.summary())

    # Probabilidades suavizadas
    smoothed = results.smoothed_probs
    ```

=== "R (MSwM)"

    ```r
    library(MSwM)

    # Modelo linear base
    mod <- lm(growth ~ 1)

    # MS(2) com switching na media e variancia
    ms_fit <- msmFit(mod, k = 2, sw = c(TRUE, TRUE))
    summary(ms_fit)
    plotProb(ms_fit, which = 1)
    ```

=== "Python (statsmodels)"

    ```python
    import statsmodels.api as sm

    mod = sm.tsa.MarkovAutoregression(
        growth,
        k_regimes=2,
        order=4,
        switching_variance=True,
    )
    res = mod.fit()
    print(res.summary())

    # Probabilidades suavizadas
    smoothed = res.smoothed_marginal_probabilities
    ```

| Funcionalidade | ArchBox | MSwM (R) | statsmodels (Python) |
|---------------|---------|----------|---------------------|
| Especificacao | `MarkovSwitchingAR(y, k_regimes=2, order=4)` | `msmFit(lm(y~1), k=2)` | `MarkovAutoregression(y, k_regimes=2, order=4)` |
| Estimacao | `model.fit()` | Automatica em `msmFit` | `mod.fit()` |
| Probabilidades | `results.smoothed_probs` | `ms_fit@Fit@smoProb` | `res.smoothed_marginal_probabilities` |
| Classificacao | `results.classify()` | Manual via probs | Manual via probs |
| Matriz P | `results.transition_matrix` | `ms_fit@transMat` | `res.params` (extrair) |
| Visualizacao | `results.plot_regimes(y)` | `plotProb(ms_fit)` | Manual com matplotlib |

## References

- Hamilton, J. D. (1989). A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle. *Econometrica*, 57(2), 357--384.
- Hamilton, J. D. (1994). *Time Series Analysis*. Princeton University Press. Chapter 22.
- Kim, C.-J. (1994). Dynamic Linear Models with Markov-Switching. *Journal of Econometrics*, 60(1-2), 1--22.
- Kim, C.-J., & Nelson, C. R. (1999). *State-Space Models with Regime Switching*. MIT Press.

## See Also

- [Regime-Switching: Visao Geral](index.md) -- Introducao e comparacao de modelos
- [MS-VAR](ms-var.md) -- Extensao multivariada do MS-AR
- [MS-GARCH](ms-garch.md) -- Volatilidade condicional com mudanca de regime
- [GARCH(p,q)](../garch/garch.md) -- Modelo de volatilidade condicional sem regime
- [Modelos Threshold](../threshold/index.md) -- Alternativa com transicao deterministica
