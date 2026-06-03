---
title: Threshold API
description: Referencia dos modelos TAR, SETAR, LSTAR, ESTAR e testes de linearidade
---

# Threshold API

!!! info "Modulo"
    ```python
    from archbox.threshold import TAR, SETAR, LSTAR, ESTAR
    from archbox.threshold import ThresholdResults, TestResult
    from archbox.threshold import (
        linearity_test, transition_type_test,
        tsay_test, hansen_threshold_test,
    )
    from archbox.threshold import (
        logistic_transition, exponential_transition,
    )
    ```

## Visao Geral

A archbox implementa 4 modelos threshold/STAR, todos herdando de
`ThresholdModel`. Sao modelos nao-lineares onde a dinamica muda
dependendo de uma variavel de transicao.

| Classe | Modelo | Transicao | Descricao |
|--------|--------|-----------|-----------|
| `TAR` | Threshold AR | Indicadora | Mudanca abrupta no threshold |
| `SETAR` | Self-Exciting TAR | Indicadora | TAR com $y_{t-d}$ como variavel de transicao |
| `LSTAR` | Logistic STAR | Logistica | Transicao suave via funcao logistica |
| `ESTAR` | Exponential STAR | Exponencial | Transicao suave simetrica |

O modelo geral STAR (Smooth Transition AR):

$$
y_t = (\phi'_1 x_t)(1 - G(s_t; \gamma, c)) + (\phi'_2 x_t) G(s_t; \gamma, c) + \varepsilon_t
$$

onde $G(\cdot)$ e a funcao de transicao, $s_t$ e a variavel de transicao,
$\gamma$ controla a velocidade da transicao e $c$ e o threshold.

---

## ThresholdModel (Base)

::: archbox.threshold.base.ThresholdModel
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
ThresholdModel(endog, order=1, delay=1, n_regimes=2)
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | `array-like` | -- | Serie temporal |
| `order` | `int` | `1` | Ordem AR $p$ |
| `delay` | `int` | `1` | Delay $d$ da variavel de transicao $y_{t-d}$ |
| `n_regimes` | `int` | `2` | Numero de regimes |

### Atributos

| Atributo | Tipo | Descricao |
|----------|------|-----------|
| `endog` | `ndarray` | Serie temporal |
| `nobs` | `int` | Numero de observacoes |
| `order` | `int` | Ordem AR |
| `delay` | `int` | Delay da transicao |
| `n_regimes` | `int` | Numero de regimes |

### Metodos Principais

#### `fit()`

Ajusta o modelo via minimos quadrados concentrados (CLS).

```python
fit(method='cls') -> ThresholdResults
```

#### `forecast()`

Previsao $h$ passos a frente via simulacao (Bootstrap ou analitica).

```python
forecast(results, horizon=10) -> dict[str, ndarray]
```

#### `simulate()`

Simula dados do modelo threshold.

```python
simulate(n, params_regime1, params_regime2, transition_params,
         sigma=1.0, seed=None) -> ndarray
```

---

## TAR

::: archbox.threshold.tar.TAR
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - fit

### Especificacao

**Threshold Autoregressive** (Tong, 1978):

$$
y_t = \begin{cases}
\phi'_1 x_t + \varepsilon_{1,t} & \text{se } z_t \leq c \\
\phi'_2 x_t + \varepsilon_{2,t} & \text{se } z_t > c
\end{cases}
$$

onde $z_t$ e uma variavel de transicao exogena e $c$ e o threshold.

A funcao de transicao e a indicadora:

$$
G(z_t; c) = \mathbf{1}(z_t > c)
$$

### Construtor

```python
TAR(endog, order=1, delay=1, n_regimes=2,
    threshold_var=None, grid_points=300)
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | `array-like` | -- | Serie temporal |
| `order` | `int` | `1` | Ordem AR $p$ |
| `delay` | `int` | `1` | Delay $d$ |
| `n_regimes` | `int` | `2` | Numero de regimes |
| `threshold_var` | `ndarray` | `None` | Variavel de transicao exogena (se `None`, usa $y_{t-d}$) |
| `grid_points` | `int` | `300` | Pontos do grid para busca do threshold |

### Exemplo

```python
from archbox.threshold import TAR
import numpy as np

np.random.seed(42)
y = np.random.randn(500) * 0.01

model = TAR(y, order=2, delay=1)
result = model.fit()

print(result.summary())
print(f"Threshold estimado: {result.threshold:.4f}")
print(f"Regime 1: {(result.regime_assignments == 0).sum()} obs")
print(f"Regime 2: {(result.regime_assignments == 1).sum()} obs")
```

---

## SETAR

::: archbox.threshold.setar.SETAR
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - fit

### Especificacao

**Self-Exciting Threshold AR** (Tong, 1983):

$$
y_t = \begin{cases}
\phi'_1 x_t + \varepsilon_{1,t} & \text{se } y_{t-d} \leq c \\
\phi'_2 x_t + \varepsilon_{2,t} & \text{se } y_{t-d} > c
\end{cases}
$$

A variavel de transicao e o proprio $y_{t-d}$ (self-exciting). O delay
$d$ pode ser selecionado automaticamente via criterio de informacao.

!!! tip "Selecao automatica de delay"
    Quando `delay=None`, o SETAR testa todos os delays de $1$ ate `d_max`
    e seleciona o que minimiza o criterio de informacao escolhido (`ic`).

### Construtor

```python
SETAR(endog, order=1, delay=None, n_regimes=2,
      d_max=6, grid_points=300, ic='aic')
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | `array-like` | -- | Serie temporal |
| `order` | `int` | `1` | Ordem AR $p$ |
| `delay` | `int\|None` | `None` | Delay $d$ (`None` = selecao automatica) |
| `n_regimes` | `int` | `2` | Numero de regimes (2 ou 3) |
| `d_max` | `int` | `6` | Delay maximo na selecao automatica |
| `grid_points` | `int` | `300` | Pontos do grid para busca |
| `ic` | `str` | `'aic'` | Criterio de informacao (`'aic'` ou `'bic'`) |

### Exemplo

```python
from archbox.threshold import SETAR
import numpy as np

np.random.seed(42)
y = np.random.randn(500) * 0.01

# SETAR com selecao automatica de delay
model = SETAR(y, order=2, delay=None, n_regimes=2, ic='bic')
result = model.fit()

print(result.summary())
print(f"Delay selecionado: {result.delay}")
print(f"Threshold: {result.threshold:.4f}")
```

---

## LSTAR

::: archbox.threshold.lstar.LSTAR
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - fit

### Especificacao

**Logistic Smooth Transition AR** (Terasvirta, 1994):

$$
y_t = \phi'_1 x_t (1 - G(s_t)) + \phi'_2 x_t \, G(s_t) + \varepsilon_t
$$

com funcao de transicao logistica:

$$
G(s_t; \gamma, c) = \frac{1}{1 + \exp(-\gamma(s_t - c))}
$$

onde $\gamma > 0$ controla a velocidade da transicao e $c$ e o
parametro de localizacao (threshold).

!!! note "Casos limite"
    - $\gamma \to 0$: modelo linear (sem transicao)
    - $\gamma \to \infty$: TAR (transicao abrupta)

### Construtor

```python
LSTAR(endog, order=1, delay=1, gamma_grid=50, c_grid=50, refine=True)
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | `array-like` | -- | Serie temporal |
| `order` | `int` | `1` | Ordem AR $p$ |
| `delay` | `int` | `1` | Delay $d$ |
| `gamma_grid` | `int` | `50` | Pontos no grid de $\gamma$ |
| `c_grid` | `int` | `50` | Pontos no grid de $c$ |
| `refine` | `bool` | `True` | Refinar via otimizacao numerica |

### Exemplo

```python
from archbox.threshold import LSTAR
import numpy as np

np.random.seed(42)
y = np.random.randn(500) * 0.01

model = LSTAR(y, order=2, delay=1)
result = model.fit()

print(result.summary())
print(f"gamma = {result.transition_params['gamma']:.2f}")
print(f"c = {result.transition_params['c']:.4f}")
```

---

## ESTAR

::: archbox.threshold.estar.ESTAR
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - fit

### Especificacao

**Exponential Smooth Transition AR** (Terasvirta, 1994):

$$
y_t = \phi'_1 x_t (1 - G(s_t)) + \phi'_2 x_t \, G(s_t) + \varepsilon_t
$$

com funcao de transicao exponencial:

$$
G(s_t; \gamma, c) = 1 - \exp(-\gamma(s_t - c)^2)
$$

!!! note "Simetria"
    A funcao exponencial e **simetrica** em torno de $c$, o que significa
    que o comportamento do regime externo e o mesmo para desvios positivos
    e negativos de $c$. Use LSTAR para transicoes assimetricas.

### Construtor

```python
ESTAR(endog, order=1, delay=1, gamma_grid=50, c_grid=50, refine=True)
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | `array-like` | -- | Serie temporal |
| `order` | `int` | `1` | Ordem AR $p$ |
| `delay` | `int` | `1` | Delay $d$ |
| `gamma_grid` | `int` | `50` | Pontos no grid de $\gamma$ |
| `c_grid` | `int` | `50` | Pontos no grid de $c$ |
| `refine` | `bool` | `True` | Refinar via otimizacao numerica |

### Exemplo

```python
from archbox.threshold import ESTAR
import numpy as np

np.random.seed(42)
y = np.random.randn(500) * 0.01

model = ESTAR(y, order=2, delay=1)
result = model.fit()

print(result.summary())
print(f"gamma = {result.transition_params['gamma']:.2f}")
print(f"c = {result.transition_params['c']:.4f}")
```

---

## ThresholdResults

::: archbox.threshold.results.ThresholdResults
    options:
      show_root_heading: true
      show_source: true
      members:
        - summary

### Atributos

| Atributo | Tipo | Descricao |
|----------|------|-----------|
| `model_name` | `str` | Nome do modelo (`"TAR"`, `"SETAR"`, `"LSTAR"`, `"ESTAR"`) |
| `params` | `ndarray` | Todos os parametros estimados |
| `threshold` | `float` | Threshold estimado $c$ |
| `delay` | `int` | Delay utilizado $d$ |
| `transition_params` | `dict` | Parametros da funcao de transicao (`gamma`, `c`) |
| `params_regime1` | `ndarray` | Coeficientes do regime 1 |
| `params_regime2` | `ndarray` | Coeficientes do regime 2 |
| `regime_assignments` | `ndarray` | Regime de cada observacao |
| `transition_values` | `ndarray` | $G(s_t)$ para cada $t$ |
| `resid` | `ndarray` | Residuos |
| `sigma2` | `float` | Variancia dos residuos |
| `loglike` | `float` | Log-verossimilhanca |
| `aic` | `float` | $\text{AIC} = -2\ell + 2k$ |
| `bic` | `float` | $\text{BIC} = -2\ell + k \ln(n)$ |
| `nobs` | `int` | Numero de observacoes |
| `order` | `int` | Ordem AR |
| `n_regimes` | `int` | Numero de regimes |
| `linearity_test` | `TestResult\|None` | Resultado do teste de linearidade |

---

## Testes de Linearidade

### `linearity_test()`

::: archbox.threshold.tests_linearity.linearity_test
    options:
      show_root_heading: true
      show_source: true

Teste LM de Luukkonen-Saikkonen-Terasvirta (1988) para nao-linearidade.

$H_0$: modelo linear vs. $H_1$: modelo STAR.

```python
linearity_test(endog, order=1, delay=1) -> TestResult
```

### `transition_type_test()`

::: archbox.threshold.tests_linearity.transition_type_test
    options:
      show_root_heading: true
      show_source: true

Teste de Terasvirta (1994) para tipo de transicao (LSTAR vs ESTAR).

```python
transition_type_test(endog, order=1, delay=1) -> TestResult
```

### `tsay_test()`

::: archbox.threshold.tests_linearity.tsay_test
    options:
      show_root_heading: true
      show_source: true

Teste de Tsay (1989) para nao-linearidade threshold.

```python
tsay_test(endog, order=1, delay=1) -> TestResult
```

### `hansen_threshold_test()`

::: archbox.threshold.tests_linearity.hansen_threshold_test
    options:
      show_root_heading: true
      show_source: true

Teste de Hansen (1996) para threshold com p-valor via bootstrap.

```python
hansen_threshold_test(endog, order=1, delay=1, n_bootstrap=1000) -> TestResult
```

### TestResult

| Atributo | Tipo | Descricao |
|----------|------|-----------|
| `statistic` | `float` | Estatistica do teste |
| `pvalue` | `float` | p-valor |
| `test_name` | `str` | Nome do teste |
| `detail` | `str` | Detalhes adicionais |

### Exemplo de Testes

```python
from archbox.threshold import (
    linearity_test, tsay_test,
    hansen_threshold_test, transition_type_test,
)
import numpy as np

np.random.seed(42)
y = np.random.randn(500) * 0.01

# Teste LM (rapido)
lm = linearity_test(y, order=2, delay=1)
print(f"LM: stat={lm.statistic:.3f}, p={lm.pvalue:.4f}")

# Teste de Tsay
tsay = tsay_test(y, order=2, delay=1)
print(f"Tsay: stat={tsay.statistic:.3f}, p={tsay.pvalue:.4f}")

# Teste de Hansen (bootstrap - mais lento)
hansen = hansen_threshold_test(y, order=2, delay=1, n_bootstrap=999)
print(f"Hansen: stat={hansen.statistic:.3f}, p={hansen.pvalue:.4f}")

# Tipo de transicao
tt = transition_type_test(y, order=2, delay=1)
print(f"Tipo: {tt.detail}")
```

---

## Funcoes de Transicao

::: archbox.threshold.transition.logistic_transition
    options:
      show_root_heading: true
      show_source: true

::: archbox.threshold.transition.exponential_transition
    options:
      show_root_heading: true
      show_source: true

### `logistic_transition()`

$$
G(s; \gamma, c) = \frac{1}{1 + \exp(-\gamma(s - c))}
$$

```python
logistic_transition(s, gamma, c) -> ndarray
```

### `exponential_transition()`

$$
G(s; \gamma, c) = 1 - \exp(-\gamma(s - c)^2)
$$

```python
exponential_transition(s, gamma, c) -> ndarray
```

### Exemplo

```python
from archbox.threshold import logistic_transition, exponential_transition
import numpy as np

s = np.linspace(-3, 3, 100)

# Logistica com diferentes gamma
g_slow = logistic_transition(s, gamma=1, c=0)
g_fast = logistic_transition(s, gamma=10, c=0)

# Exponencial
g_exp = exponential_transition(s, gamma=1, c=0)
```

---

## Exemplo Completo: Workflow STAR

```python
from archbox.threshold import (
    SETAR, LSTAR, ESTAR,
    linearity_test, transition_type_test,
)
import numpy as np

np.random.seed(42)
y = np.random.randn(500) * 0.01

# 1. Testar linearidade
lm = linearity_test(y, order=2, delay=1)
print(f"Teste de linearidade: p={lm.pvalue:.4f}")

if lm.pvalue < 0.05:
    # 2. Escolher tipo de transicao
    tt = transition_type_test(y, order=2, delay=1)
    print(f"Tipo sugerido: {tt.detail}")

    # 3. Ajustar modelo
    model = LSTAR(y, order=2, delay=1)
    result = model.fit()
    print(result.summary())
else:
    # Modelo linear e suficiente
    model = SETAR(y, order=2, n_regimes=2)
    result = model.fit()
    print(result.summary())
```

---

## Referencias

- Tong, H. (1978). On a Threshold Model.
  *Pattern Recognition and Signal Processing*, Sijthoff & Noordhoff.
- Tong, H. (1983). *Threshold Models in Non-linear Time Series Analysis*.
  Springer-Verlag.
- Terasvirta, T. (1994). Specification, Estimation, and Evaluation of
  Smooth Transition Autoregressive Models.
  *Journal of the American Statistical Association*, 89(425), 208-218.
- Luukkonen, R., Saikkonen, P. & Terasvirta, T. (1988). Testing
  Linearity Against Smooth Transition Autoregressive Models.
  *Biometrika*, 75(3), 491-499.
- Hansen, B.E. (1996). Inference When a Nuisance Parameter Is Not
  Identified Under the Null Hypothesis.
  *Econometrica*, 64(2), 413-430.
- Tsay, R.S. (1989). Testing and Modeling Threshold Autoregressive
  Processes. *Journal of the American Statistical Association*,
  84(405), 231-240.

---

## Ver Tambem

- [Core](core.md) -- Classe base `VolatilityModel`
- [Regime-Switching](regime-switching.md) -- Modelos Markov-Switching (alternativa probabilistica)
- [Distributions](distributions.md) -- Distribuicoes condicionais
