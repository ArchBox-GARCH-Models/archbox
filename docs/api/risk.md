---
title: Risk API
description: Referencia de VaR, Expected Shortfall, EWMA e backtesting
---

# Risk API

!!! info "Modulo"
    ```python
    from archbox.risk import ValueAtRisk, ExpectedShortfall, EWMA, VaRBacktest
    ```

## Visao Geral

O modulo `archbox.risk` fornece ferramentas para gestao de risco baseada
em modelos de volatilidade condicional:

| Classe | Descricao | Metodos |
|--------|-----------|---------|
| `ValueAtRisk` | Value-at-Risk condicional | `parametric()`, `historical()`, `filtered_historical()`, `monte_carlo()` |
| `ExpectedShortfall` | Expected Shortfall (CVaR) | `parametric()`, `historical()`, `filtered_historical()`, `monte_carlo()` |
| `EWMA` | RiskMetrics EWMA | `fit()`, `covariance()`, `forecast()` |
| `VaRBacktest` | Backtesting de VaR | `kupiec_pof()`, `christoffersen()`, `traffic_light()` |

A ideia central e combinar modelos GARCH (volatilidade condicional) com
distribuicoes adequadas para obter medidas de risco condicionais:

$$
\text{VaR}_{\alpha,t} = \mu_t + \sigma_t \cdot q_\alpha
$$

$$
\text{ES}_{\alpha,t} = \mu_t + \sigma_t \cdot E[z \mid z \leq q_\alpha]
$$

onde $q_\alpha$ e o quantil da distribuicao condicional e $\sigma_t$ e a
volatilidade condicional estimada pelo GARCH.

---

## ValueAtRisk

::: archbox.risk.var.ValueAtRisk
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - parametric
        - historical
        - filtered_historical
        - monte_carlo

### Construtor

```python
ValueAtRisk(results, alpha=0.05)
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `results` | `ArchResults` | -- | Resultado de um modelo GARCH ajustado |
| `alpha` | `float` | `0.05` | Nivel de confianca ($\alpha = 0.05$ → VaR 95%) |

### Atributos

| Atributo | Tipo | Descricao |
|----------|------|-----------|
| `results` | `ArchResults` | Modelo ajustado |
| `alpha` | `float` | Nivel de significancia |
| `returns` | `ndarray` | Serie de retornos |
| `conditional_volatility` | `ndarray` | $\sigma_t$ do modelo |
| `mu` | `float` | Media estimada |

### Metodos

#### `parametric()`

VaR parametrico usando distribuicao condicional:

$$
\text{VaR}_{\alpha,t} = \mu + \sigma_t \cdot F^{-1}(\alpha)
$$

```python
parametric(dist='normal', nu=8.0) -> ndarray
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `dist` | `str` | `'normal'` | Distribuicao: `'normal'` ou `'student-t'` |
| `nu` | `float` | `8.0` | Graus de liberdade (para Student-$t$) |

#### `historical()`

VaR por simulacao historica com janela movel.

```python
historical(window=250) -> ndarray
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `window` | `int` | `250` | Tamanho da janela (dias uteis ~ 1 ano) |

#### `filtered_historical()`

VaR por simulacao historica filtrada (FHS). Combina residuos padronizados
historicos com volatilidade condicional corrente:

$$
\text{VaR}_{\alpha,t} = \mu + \sigma_t \cdot q_\alpha(\hat{z}_{1:T})
$$

```python
filtered_historical() -> ndarray
```

#### `monte_carlo()`

VaR via simulacao Monte Carlo.

```python
monte_carlo(n_sim=10000, seed=None) -> ndarray
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `n_sim` | `int` | `10000` | Numero de simulacoes |
| `seed` | `int` | `None` | Semente para reproducibilidade |

### Exemplo

```python
from archbox.models import GARCH
from archbox.risk import ValueAtRisk
import numpy as np

np.random.seed(42)
returns = np.random.randn(1000) * 0.01

# Ajustar GARCH
model = GARCH(returns, p=1, q=1)
result = model.fit(disp=False)

# VaR 95%
var = ValueAtRisk(result, alpha=0.05)

var_param = var.parametric(dist='normal')
var_hist = var.historical(window=250)
var_fhs = var.filtered_historical()
var_mc = var.monte_carlo(n_sim=10000, seed=42)

print(f"VaR parametrico (ultimo): {var_param[-1]:.6f}")
print(f"VaR historico (ultimo): {var_hist[-1]:.6f}")
print(f"VaR FHS (ultimo): {var_fhs[-1]:.6f}")
print(f"VaR Monte Carlo (ultimo): {var_mc[-1]:.6f}")
```

---

## ExpectedShortfall

::: archbox.risk.es.ExpectedShortfall
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - parametric
        - historical
        - filtered_historical
        - monte_carlo

### Construtor

```python
ExpectedShortfall(results, alpha=0.05)
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `results` | `ArchResults` | -- | Resultado de um modelo GARCH ajustado |
| `alpha` | `float` | `0.05` | Nivel de confianca |

### Descricao

O Expected Shortfall (CVaR) e a perda esperada **dado que** o VaR foi
excedido:

$$
\text{ES}_\alpha = E[r_t \mid r_t \leq \text{VaR}_\alpha]
$$

Para a distribuicao Normal:

$$
\text{ES}_{\alpha,t} = \mu + \sigma_t \cdot \frac{\phi(z_\alpha)}{\alpha}
$$

onde $\phi(\cdot)$ e a PDF da Normal padrao e $z_\alpha = \Phi^{-1}(\alpha)$.

!!! tip "ES vs VaR"
    O ES e uma medida de risco **coerente** (satisfaz subaditividade),
    enquanto o VaR nao. O ES captura o risco na cauda alem do VaR.

### Metodos

Os metodos sao analogos ao `ValueAtRisk`:

#### `parametric()`

```python
parametric(dist='normal', nu=8.0) -> ndarray
```

#### `historical()`

```python
historical(window=250) -> ndarray
```

#### `filtered_historical()`

```python
filtered_historical() -> ndarray
```

#### `monte_carlo()`

```python
monte_carlo(n_sim=10000, seed=None) -> ndarray
```

### Exemplo

```python
from archbox.models import GARCH
from archbox.risk import ExpectedShortfall
import numpy as np

np.random.seed(42)
returns = np.random.randn(1000) * 0.01

model = GARCH(returns, p=1, q=1)
result = model.fit(disp=False)

es = ExpectedShortfall(result, alpha=0.05)

es_param = es.parametric(dist='normal')
es_t = es.parametric(dist='student-t', nu=5)

print(f"ES Normal (ultimo): {es_param[-1]:.6f}")
print(f"ES Student-t (ultimo): {es_t[-1]:.6f}")
```

---

## EWMA

::: archbox.risk.ewma.EWMA
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - fit
        - covariance
        - forecast

### Especificacao

**Exponentially Weighted Moving Average** (RiskMetrics, J.P. Morgan 1996):

$$
\sigma^2_t = \lambda \sigma^2_{t-1} + (1 - \lambda) r^2_{t-1}
$$

Caso especial do IGARCH(1,1) sem intercepto ($\omega = 0$, $\alpha = 1 - \lambda$,
$\beta = \lambda$).

!!! note "Valores tipicos de $\lambda$"
    - $\lambda = 0.94$: dados diarios (RiskMetrics)
    - $\lambda = 0.97$: dados mensais

### Construtor

```python
EWMA(returns, lam=0.94)
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `returns` | `array-like` | -- | Serie de retornos |
| `lam` | `float` | `0.94` | Fator de decaimento $\lambda$ |

### Atributos

| Atributo | Tipo | Descricao |
|----------|------|-----------|
| `returns` | `ndarray` | Serie de retornos |
| `lam` | `float` | Fator de decaimento |

### Metodos

#### `fit()`

Ajusta o modelo EWMA (calcula a volatilidade condicional).

```python
fit() -> EWMAResult
```

#### `covariance()`

Calcula a matriz de covariancia EWMA para dados multivariados.

```python
covariance(returns_matrix) -> ndarray
```

#### `forecast()`

Previsao da volatilidade $h$ passos a frente.

```python
forecast(horizon=1) -> dict
```

### EWMAResult

| Atributo | Tipo | Descricao |
|----------|------|-----------|
| `conditional_volatility` | `ndarray` | $\sigma_t$ |
| `conditional_variance` | `ndarray` | $\sigma^2_t$ |
| `returns` | `ndarray` | Retornos |
| `lam` | `float` | Fator de decaimento |
| `resids` | `ndarray` | Residuos |
| `mu` | `float` | Media estimada |

### Exemplo

```python
from archbox.risk import EWMA
import numpy as np

np.random.seed(42)
returns = np.random.randn(500) * 0.01

# EWMA com lambda = 0.94 (RiskMetrics diario)
model = EWMA(returns, lam=0.94)
result = model.fit()

print(f"Volatilidade media: {result.conditional_volatility.mean():.6f}")
print(f"Volatilidade final: {result.conditional_volatility[-1]:.6f}")

# Previsao
fc = model.forecast(horizon=5)
print(f"Previsao 5d: {fc}")
```

---

## VaRBacktest

::: archbox.risk.backtest.VaRBacktest
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - kupiec_pof
        - christoffersen
        - traffic_light
        - summary

### Construtor

```python
VaRBacktest(returns, var_estimates, alpha=0.05)
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `returns` | `ndarray` | -- | Retornos realizados |
| `var_estimates` | `ndarray` | -- | Estimativas de VaR (mesmo tamanho) |
| `alpha` | `float` | `0.05` | Nivel de confianca |

### Atributos

| Atributo | Tipo | Descricao |
|----------|------|-----------|
| `returns` | `ndarray` | Retornos realizados |
| `var_estimates` | `ndarray` | Estimativas de VaR |
| `alpha` | `float` | Nivel de significancia |
| `exceptions` | `ndarray` | Indicador de violacoes ($r_t < \text{VaR}_t$) |

### Metodos

#### `kupiec_pof()`

Teste de Kupiec (1995) - Proportion of Failures.

$H_0$: frequencia de violacoes e consistente com $\alpha$.

$$
LR_{POF} = 2 \left[ n_1 \ln\left(\frac{n_1/n}{\alpha}\right) + n_0 \ln\left(\frac{n_0/n}{1-\alpha}\right) \right] \sim \chi^2(1)
$$

```python
kupiec_pof() -> TestResult
```

#### `christoffersen()`

Teste de Christoffersen (1998) - Independencia das violacoes.

$H_0$: violacoes sao independentes.

```python
christoffersen() -> TestResult
```

#### `traffic_light()`

Semaforo de Basileia III para adequacao do modelo de VaR.

```python
traffic_light() -> str
```

**Retorna**: `'green'`, `'yellow'` ou `'red'`.

| Zona | Violacoes (250 dias, 99%) | Interpretacao |
|------|---------------------------|---------------|
| Verde | 0-4 | Modelo adequado |
| Amarelo | 5-9 | Atencao necessaria |
| Vermelho | 10+ | Modelo inadequado |

#### `summary()`

Resumo completo com todos os testes.

```python
summary() -> str
```

### Exemplo

```python
from archbox.models import GARCH
from archbox.risk import ValueAtRisk, VaRBacktest
import numpy as np

np.random.seed(42)
returns = np.random.randn(1000) * 0.01

# Ajustar GARCH e calcular VaR
model = GARCH(returns, p=1, q=1)
result = model.fit(disp=False)
var = ValueAtRisk(result, alpha=0.05)
var_series = var.parametric(dist='normal')

# Backtesting
bt = VaRBacktest(returns, var_series, alpha=0.05)

# Testes individuais
kupiec = bt.kupiec_pof()
print(f"Kupiec: stat={kupiec.statistic:.3f}, p={kupiec.pvalue:.4f}")

chris = bt.christoffersen()
print(f"Christoffersen: stat={chris.statistic:.3f}, p={chris.pvalue:.4f}")

# Semaforo
print(f"Traffic light: {bt.traffic_light()}")

# Resumo completo
print(bt.summary())
```

---

## Exemplo Completo: Pipeline de Risco

```python
from archbox.models import GARCH
from archbox.risk import ValueAtRisk, ExpectedShortfall, EWMA, VaRBacktest
import numpy as np

np.random.seed(42)
returns = np.random.randn(1000) * 0.01

# === 1. Modelos de Volatilidade ===

# GARCH(1,1)
garch = GARCH(returns, p=1, q=1)
garch_result = garch.fit(disp=False)

# EWMA (RiskMetrics)
ewma = EWMA(returns, lam=0.94)
ewma_result = ewma.fit()

# === 2. Medidas de Risco (GARCH) ===

var = ValueAtRisk(garch_result, alpha=0.05)
es = ExpectedShortfall(garch_result, alpha=0.05)

var_normal = var.parametric(dist='normal')
var_t = var.parametric(dist='student-t', nu=5)
es_normal = es.parametric(dist='normal')

print(f"VaR 95% Normal (ultimo): {var_normal[-1]:.6f}")
print(f"VaR 95% t(5) (ultimo): {var_t[-1]:.6f}")
print(f"ES 95% Normal (ultimo): {es_normal[-1]:.6f}")

# === 3. Backtesting ===

bt_normal = VaRBacktest(returns, var_normal, alpha=0.05)
bt_t = VaRBacktest(returns, var_t, alpha=0.05)

print(f"\n--- Backtesting VaR Normal ---")
print(f"Violacoes: {bt_normal.exceptions.sum()}/{len(returns)}")
print(f"Taxa: {bt_normal.exceptions.mean():.4f} (esperado: 0.05)")
print(f"Kupiec p-valor: {bt_normal.kupiec_pof().pvalue:.4f}")
print(f"Semaforo: {bt_normal.traffic_light()}")

print(f"\n--- Backtesting VaR t(5) ---")
print(f"Violacoes: {bt_t.exceptions.sum()}/{len(returns)}")
print(f"Kupiec p-valor: {bt_t.kupiec_pof().pvalue:.4f}")
print(f"Semaforo: {bt_t.traffic_light()}")
```

---

## Referencias

- Kupiec, P.H. (1995). Techniques for Verifying the Accuracy of Risk
  Measurement Models. *Journal of Derivatives*, 3(2), 73-84.
- Christoffersen, P.F. (1998). Evaluating Interval Forecasts.
  *International Economic Review*, 39(4), 841-862.
- McNeil, A.J. & Frey, R. (2000). Estimation of Tail-Related Risk
  Measures for Heteroscedastic Financial Time Series.
  *Journal of Empirical Finance*, 7(3-4), 271-300.
- J.P. Morgan (1996). *RiskMetrics -- Technical Document*. 4th Edition.

---

## Ver Tambem

- [Core](core.md) -- `ArchResults` usado como input do VaR/ES
- [GARCH](garch.md) -- Modelos de volatilidade condicional
- [Distributions](distributions.md) -- Distribuicoes para VaR parametrico
- [Regime-Switching](regime-switching.md) -- Regime-dependent risk
