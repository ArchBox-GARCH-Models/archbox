---
title: Regime-Switching API
description: Referencia dos modelos Markov-Switching MS-AR, MS-VAR, MS-GARCH, Hamilton Filter e Kim Smoother
---

# Regime-Switching API

!!! info "Modulo"
    ```python
    from archbox.regime import (
        MarkovSwitchingMean, MarkovSwitchingMeanVar,
        MarkovSwitchingAR, MarkovSwitchingVAR, MarkovSwitchingGARCH,
        HamiltonFilter, KimSmoother, EMEstimator,
        RegimeResults,
    )
    ```

## Visao Geral

A archbox implementa 5 modelos Markov-Switching, todos herdando de
`MarkovSwitchingModel`. A estimacao e feita via algoritmo EM com o
**Hamilton Filter** (forward) e o **Kim Smoother** (backward).

| Classe | Modelo | Switching | Descricao |
|--------|--------|-----------|-----------|
| `MarkovSwitchingMean` | MS-Mean | $\mu$ | Apenas media muda entre regimes |
| `MarkovSwitchingMeanVar` | MS-MeanVar | $\mu, \sigma^2$ | Media e variancia mudam |
| `MarkovSwitchingAR` | MS-AR(p) | $\mu, \phi, \sigma^2$ | AR com parametros regime-dependentes |
| `MarkovSwitchingVAR` | MS-VAR(p) | $\mu, \Phi, \Sigma$ | VAR multivariado com switching |
| `MarkovSwitchingGARCH` | MS-GARCH | $\omega, \alpha, \beta$ | GARCH com regime-switching (Gray 1996) |

O modelo geral assume que o regime $S_t \in \{1, \ldots, K\}$ segue uma
cadeia de Markov de primeira ordem com matriz de transicao:

$$
P = \begin{bmatrix}
p_{11} & p_{12} & \cdots & p_{1K} \\
p_{21} & p_{22} & \cdots & p_{2K} \\
\vdots & \vdots & \ddots & \vdots \\
p_{K1} & p_{K2} & \cdots & p_{KK}
\end{bmatrix}
$$

onde $p_{ij} = P(S_t = j \mid S_{t-1} = i)$ e $\sum_j p_{ij} = 1$.

---

## MarkovSwitchingModel (Base)

::: archbox.regime.base.MarkovSwitchingModel
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - fit
        - loglike
        - forecast
        - simulate

### Construtor

```python
MarkovSwitchingModel(endog, k_regimes=2, order=1,
                     switching_mean=True, switching_variance=True,
                     switching_ar=False)
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | `array-like` | -- | Serie temporal de retornos |
| `k_regimes` | `int` | `2` | Numero de regimes $K$ |
| `order` | `int` | `1` | Ordem autorregressiva $p$ |
| `switching_mean` | `bool` | `True` | Media depende do regime |
| `switching_variance` | `bool` | `True` | Variancia depende do regime |
| `switching_ar` | `bool` | `False` | Coeficientes AR dependem do regime |

### Atributos

| Atributo | Tipo | Descricao |
|----------|------|-----------|
| `endog` | `ndarray` | Serie temporal |
| `nobs` | `int` | Numero de observacoes |
| `k_regimes` | `int` | Numero de regimes |
| `order` | `int` | Ordem AR |

### Metodos Principais

#### `fit()`

Ajusta o modelo via algoritmo EM (Expectation-Maximization).

```python
fit(method='em', maxiter=500, em_iter=100, tol=1e-8, verbose=True) -> RegimeResults
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `method` | `str` | `'em'` | Metodo de estimacao |
| `maxiter` | `int` | `500` | Maximo de iteracoes |
| `em_iter` | `int` | `100` | Iteracoes do passo EM |
| `tol` | `float` | `1e-8` | Tolerancia de convergencia |
| `verbose` | `bool` | `True` | Exibir progresso |

#### `forecast()`

Previsao dos retornos e probabilidades de regime $h$ passos a frente.

```python
forecast(horizon, params=None, transition_matrix=None,
         last_probs=None) -> dict[str, ndarray]
```

**Retorna** dicionario com:

- `'mean'`: media prevista por regime
- `'probs'`: probabilidades de regime previstas

#### `simulate()`

Simula retornos com regime-switching.

```python
simulate(n, params, transition_matrix=None, seed=None) -> tuple[ndarray, ndarray, ndarray]
```

**Retorna** `(retornos, regimes, volatilidade)`.

---

## MarkovSwitchingMean

::: archbox.regime.ms_mean.MarkovSwitchingMean
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - fit

### Especificacao

Modelo onde apenas a media muda entre regimes:

$$
y_t = \mu_{S_t} + \varepsilon_t, \quad \varepsilon_t \sim N(0, \sigma^2)
$$

### Construtor

```python
MarkovSwitchingMean(endog, k_regimes=2)
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | `array-like` | -- | Serie temporal |
| `k_regimes` | `int` | `2` | Numero de regimes |

### Exemplo

```python
from archbox.regime import MarkovSwitchingMean
import numpy as np

returns = np.random.randn(500) * 0.01
model = MarkovSwitchingMean(returns, k_regimes=2)
result = model.fit(verbose=False)

print(result.summary())
print(f"Duracao esperada regime 1: {result.expected_durations()[0]:.1f}")
```

---

## MarkovSwitchingMeanVar

::: archbox.regime.ms_mean.MarkovSwitchingMeanVar
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - fit

### Especificacao

Media **e** variancia mudam entre regimes:

$$
y_t = \mu_{S_t} + \varepsilon_t, \quad \varepsilon_t \sim N(0, \sigma^2_{S_t})
$$

### Construtor

```python
MarkovSwitchingMeanVar(endog, k_regimes=2)
```

### Exemplo

```python
from archbox.regime import MarkovSwitchingMeanVar
import numpy as np

returns = np.random.randn(500) * 0.01
model = MarkovSwitchingMeanVar(returns, k_regimes=2)
result = model.fit(verbose=False)

print(result.summary())

# Probabilidades suavizadas
print(f"P(regime=1) media: {result.smoothed_probs[:, 0].mean():.3f}")
```

---

## MarkovSwitchingAR (MS-AR)

::: archbox.regime.ms_ar.MarkovSwitchingAR
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - fit

### Especificacao

Modelo autorregressivo com parametros regime-dependentes:

$$
y_t = \mu_{S_t} + \sum_{i=1}^{p} \phi_{i,S_t} \, y_{t-i} + \varepsilon_t, \quad \varepsilon_t \sim N(0, \sigma^2_{S_t})
$$

### Construtor

```python
MarkovSwitchingAR(endog, k_regimes=2, order=4,
                  switching_mean=True, switching_variance=True,
                  switching_ar=False)
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | `array-like` | -- | Serie temporal |
| `k_regimes` | `int` | `2` | Numero de regimes |
| `order` | `int` | `4` | Ordem AR $p$ |
| `switching_mean` | `bool` | `True` | Media regime-dependente |
| `switching_variance` | `bool` | `True` | Variancia regime-dependente |
| `switching_ar` | `bool` | `False` | Coeficientes AR regime-dependentes |

### Parametros Estimados

| Parametro | Por regime | Descricao |
|-----------|------------|-----------|
| $\mu_{S_t}$ | Sim (se `switching_mean`) | Intercepto |
| $\phi_{i,S_t}$ | Opcional (`switching_ar`) | Coeficientes AR |
| $\sigma^2_{S_t}$ | Sim (se `switching_variance`) | Variancia |
| $p_{ij}$ | -- | Probabilidades de transicao |

### Exemplo

```python
from archbox.regime import MarkovSwitchingAR
import numpy as np

np.random.seed(42)
returns = np.random.randn(1000) * 0.01

# MS-AR(2) com 2 regimes
model = MarkovSwitchingAR(returns, k_regimes=2, order=2)
result = model.fit(verbose=False)

print(result.summary())

# Matriz de transicao
print(f"Matriz de transicao:\n{result.transition_matrix}")

# Duracao esperada de cada regime
durations = result.expected_durations()
print(f"Duracao esperada: {durations}")

# Classificar regimes
regimes = result.classify(threshold=0.5)
print(f"Regime 1: {(regimes == 0).sum()} obs")
print(f"Regime 2: {(regimes == 1).sum()} obs")
```

---

## MarkovSwitchingVAR (MS-VAR)

::: archbox.regime.ms_var.MarkovSwitchingVAR
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - fit

### Especificacao

VAR multivariado com parametros regime-dependentes:

$$
\mathbf{y}_t = \boldsymbol{\mu}_{S_t} + \sum_{i=1}^{p} \Phi_{i,S_t} \, \mathbf{y}_{t-i} + \boldsymbol{\varepsilon}_t, \quad \boldsymbol{\varepsilon}_t \sim N(\mathbf{0}, \Sigma_{S_t})
$$

### Construtor

```python
MarkovSwitchingVAR(endog, k_regimes=2, order=1,
                   switching_mean=True, switching_variance=True)
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | `ndarray` | -- | Retornos $(T, k)$ multivariados |
| `k_regimes` | `int` | `2` | Numero de regimes |
| `order` | `int` | `1` | Ordem VAR $p$ |
| `switching_mean` | `bool` | `True` | Intercepto regime-dependente |
| `switching_variance` | `bool` | `True` | Covariancia regime-dependente |

### Exemplo

```python
from archbox.regime import MarkovSwitchingVAR
import numpy as np

np.random.seed(42)
returns = np.random.randn(500, 2) * 0.01

model = MarkovSwitchingVAR(returns, k_regimes=2, order=1)
result = model.fit(verbose=False)

print(result.summary())
```

---

## MarkovSwitchingGARCH (MS-GARCH)

::: archbox.regime.ms_garch.MarkovSwitchingGARCH
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - fit

### Especificacao

GARCH(p,q) com parametros regime-dependentes (Gray, 1996):

$$
\sigma^2_{t|S_t} = \omega_{S_t} + \alpha_{S_t} \varepsilon^2_{t-1} + \beta_{S_t} \sigma^2_{t-1}
$$

Usa a abordagem de **collapsing** de Gray (1996) para manter a variancia
condicional tratavel:

$$
\sigma^2_{t-1} = \sum_{j=1}^{K} P(S_{t-1}=j \mid \mathcal{F}_{t-1}) \cdot \sigma^2_{t-1|S_{t-1}=j}
$$

### Construtor

```python
MarkovSwitchingGARCH(endog, k_regimes=2, p=1, q=1, method='gray')
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | `array-like` | -- | Serie temporal de retornos |
| `k_regimes` | `int` | `2` | Numero de regimes |
| `p` | `int` | `1` | Ordem ARCH |
| `q` | `int` | `1` | Ordem GARCH |
| `method` | `str` | `'gray'` | Metodo de collapsing |

### Parametros Estimados

| Parametro | Por regime | Descricao |
|-----------|------------|-----------|
| $\omega_{S_t}$ | Sim | Intercepto GARCH |
| $\alpha_{S_t}$ | Sim | Coeficiente ARCH |
| $\beta_{S_t}$ | Sim | Coeficiente GARCH |
| $p_{ij}$ | -- | Probabilidades de transicao |

### Exemplo

```python
from archbox.regime import MarkovSwitchingGARCH
import numpy as np

np.random.seed(42)
returns = np.random.randn(1000) * 0.01

# MS-GARCH(1,1) com 2 regimes
model = MarkovSwitchingGARCH(returns, k_regimes=2, p=1, q=1)
result = model.fit(verbose=False)

print(result.summary())

# Probabilidades filtradas vs suavizadas
print(f"P(alta vol) filtrada media: {result.filtered_probs[:, 1].mean():.3f}")
print(f"P(alta vol) suavizada media: {result.smoothed_probs[:, 1].mean():.3f}")
```

---

## HamiltonFilter

::: archbox.regime.hamilton_filter.HamiltonFilter
    options:
      show_root_heading: true
      show_source: true
      members:
        - filter
        - filter_vectorized
        - ergodic_probabilities

### Descricao

Implementa o filtro de Hamilton (1989) para calcular as probabilidades
filtradas $P(S_t = j \mid \mathcal{F}_t)$ iterativamente.

O algoritmo forward processa cada observacao:

$$
\xi_{t|t} = \frac{\xi_{t|t-1} \odot f(y_t \mid S_t, \mathcal{F}_{t-1})}{\mathbf{1}' [\xi_{t|t-1} \odot f(y_t \mid S_t, \mathcal{F}_{t-1})]}
$$

$$
\xi_{t+1|t} = P' \cdot \xi_{t|t}
$$

### Metodos

#### `filter()`

Executa o filtro de Hamilton completo.

```python
HamiltonFilter.filter(endog, regime_loglike_fn, transition_matrix,
                      init_probs=None) -> tuple[ndarray, ndarray, float, ndarray]
```

**Retorna**: `(filtered_probs, predicted_probs, loglike, regime_loglikes)`

#### `filter_vectorized()`

Versao vetorizada do filtro (mais rapida para dados pre-computados).

```python
HamiltonFilter.filter_vectorized(regime_loglikes, transition_matrix,
                                  init_probs=None) -> tuple[ndarray, ndarray, float, ndarray]
```

#### `ergodic_probabilities()`

Calcula as probabilidades ergoticas (estacionarias) da cadeia de Markov.

```python
HamiltonFilter.ergodic_probabilities(transition_matrix) -> ndarray
```

$$
\pi = (A'A)^{-1} A' e_1, \quad A = \begin{bmatrix} I - P' \\ \mathbf{1}' \end{bmatrix}
$$

### Exemplo

```python
from archbox.regime import HamiltonFilter
import numpy as np

# Matriz de transicao
P = np.array([[0.95, 0.05],
              [0.10, 0.90]])

# Probabilidades ergoticas
pi = HamiltonFilter.ergodic_probabilities(P)
print(f"Prob. ergoticas: {pi}")
# [0.667, 0.333]
```

---

## KimSmoother

::: archbox.regime.kim_smoother.KimSmoother
    options:
      show_root_heading: true
      show_source: true
      members:
        - smooth
        - smooth_vectorized
        - joint_smoothed

### Descricao

Implementa o suavizador de Kim (1994) para calcular as probabilidades
suavizadas $P(S_t = j \mid \mathcal{F}_T)$ usando toda a amostra.

O algoritmo backward:

$$
P(S_t = j \mid \mathcal{F}_T) = \sum_{i=1}^{K} \frac{P(S_{t+1} = i \mid \mathcal{F}_T) \cdot p_{ji} \cdot P(S_t = j \mid \mathcal{F}_t)}{P(S_{t+1} = i \mid \mathcal{F}_t)}
$$

### Metodos

#### `smooth()`

Executa o suavizamento backward.

```python
KimSmoother.smooth(filtered_probs, predicted_probs,
                   transition_matrix) -> ndarray
```

**Retorna**: `smoothed_probs` com shape `(T, K)`.

#### `joint_smoothed()`

Calcula probabilidades conjuntas suavizadas $P(S_t = i, S_{t+1} = j \mid \mathcal{F}_T)$.

```python
KimSmoother.joint_smoothed(filtered_probs, predicted_probs,
                           smoothed_probs, transition_matrix) -> ndarray
```

**Retorna**: shape `(T-1, K, K)`.

---

## EMEstimator

::: archbox.regime.em.EMEstimator
    options:
      show_root_heading: true
      show_source: true
      members:
        - fit

### Descricao

Algoritmo Expectation-Maximization para estimacao dos parametros
do modelo Markov-Switching.

1. **E-step**: Hamilton Filter + Kim Smoother → probabilidades suavizadas
2. **M-step**: Atualiza parametros via MLE condicional nos regimes

```python
EMEstimator().fit(model, maxiter=500, tol=1e-8, verbose=True) -> RegimeResults
```

---

## RegimeResults

::: archbox.regime.results.RegimeResults
    options:
      show_root_heading: true
      show_source: true
      members:
        - summary
        - expected_durations
        - ergodic_probabilities
        - classify
        - plot_regimes
        - plot_probabilities

### Atributos

| Atributo | Tipo | Descricao |
|----------|------|-----------|
| `params` | `ndarray` | Parametros estimados |
| `param_names` | `list[str]` | Nomes dos parametros |
| `regime_params` | `dict` | Parametros por regime |
| `transition_matrix` | `ndarray` | Matriz de transicao $P$, shape $(K, K)$ |
| `filtered_probs` | `ndarray` | $P(S_t=j \mid \mathcal{F}_t)$, shape $(T, K)$ |
| `smoothed_probs` | `ndarray` | $P(S_t=j \mid \mathcal{F}_T)$, shape $(T, K)$ |
| `predicted_probs` | `ndarray` | $P(S_t=j \mid \mathcal{F}_{t-1})$, shape $(T, K)$ |
| `loglike` | `float` | Log-verossimilhanca |
| `aic` | `float` | $\text{AIC} = -2\ell + 2k$ |
| `bic` | `float` | $\text{BIC} = -2\ell + k \ln(n)$ |
| `nobs` | `int` | Numero de observacoes |
| `k_regimes` | `int` | Numero de regimes |
| `n_params` | `int` | Numero de parametros |
| `converged` | `bool` | Se o EM convergiu |
| `n_iter` | `int` | Numero de iteracoes |
| `model_name` | `str` | Nome do modelo |

### Metodos

#### `summary()`

Gera tabela formatada com parametros por regime, matriz de transicao,
duracao esperada e criterios de informacao.

```python
result.summary() -> str
```

#### `expected_durations()`

Duracao esperada de cada regime:

$$
E[D_j] = \frac{1}{1 - p_{jj}}
$$

```python
result.expected_durations() -> ndarray  # shape (K,)
```

#### `ergodic_probabilities()`

Probabilidades de longo prazo de cada regime.

```python
result.ergodic_probabilities() -> ndarray  # shape (K,)
```

#### `classify()`

Classifica cada observacao no regime mais provavel.

```python
result.classify(threshold=0.5) -> ndarray  # shape (T,)
```

#### `plot_regimes()` / `plot_probabilities()`

Visualizacao dos regimes e probabilidades filtradas/suavizadas.

```python
result.plot_regimes()
result.plot_probabilities()
```

---

## Exemplo Completo: Ciclos Economicos com MS-AR

```python
from archbox.regime import MarkovSwitchingAR, HamiltonFilter
import numpy as np

np.random.seed(42)

# Simular serie com 2 regimes (expansao/recessao)
n = 500
returns = np.concatenate([
    np.random.randn(250) * 0.005 + 0.001,   # Expansao
    np.random.randn(250) * 0.015 - 0.002,   # Recessao
])

# Ajustar MS-AR(1) com 2 regimes
model = MarkovSwitchingAR(returns, k_regimes=2, order=1)
result = model.fit(verbose=False)

# Resumo
print(result.summary())

# Matriz de transicao
print(f"\nMatriz de transicao:\n{result.transition_matrix}")

# Duracao esperada
durations = result.expected_durations()
print(f"\nDuracao esperada (regimes): {durations}")

# Probabilidades ergoticas
ergodic = result.ergodic_probabilities()
print(f"Probabilidades ergoticas: {ergodic}")

# Classificacao
regimes = result.classify()
print(f"\nRegime 1: {(regimes == 0).sum()} obs")
print(f"Regime 2: {(regimes == 1).sum()} obs")

# Visualizacao
result.plot_probabilities()
result.plot_regimes()
```

---

## Referencias

- Hamilton, J.D. (1989). A New Approach to the Economic Analysis of
  Nonstationary Time Series and the Business Cycle.
  *Econometrica*, 57(2), 357-384.
- Kim, C.-J. (1994). Dynamic Linear Models with Markov-Switching.
  *Journal of Econometrics*, 60(1-2), 1-22.
- Gray, S.F. (1996). Modeling the Conditional Distribution of Interest
  Rates as a Regime-Switching Process.
  *Journal of Financial Economics*, 42(1), 27-62.
- Krolzig, H.-M. (1997). *Markov-Switching Vector Autoregressions*.
  Springer-Verlag.

---

## Ver Tambem

- [Core](core.md) -- Classe base `VolatilityModel`
- [Threshold](threshold.md) -- Modelos threshold/STAR (alternativa a regime-switching)
- [Distributions](distributions.md) -- Distribuicoes condicionais
- [Risk](risk.md) -- Gestao de risco
