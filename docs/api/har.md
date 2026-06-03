---
title: HAR API
description: Referencia do modelo HAR-RV e variantes para volatilidade realizada
---

# HAR API

!!! info "Modulo"
    ```python
    from archbox.models import HARRV
    from archbox.models.har_rv import HARRVResults
    ```

## Visao Geral

O modulo HAR implementa o modelo **Heterogeneous Autoregressive Realized Volatility**
(Corsi, 2009), que modela a volatilidade realizada como funcao de componentes
em diferentes horizontes temporais.

| Classe | Descricao |
|--------|-----------|
| `HARRV` | HAR-RV padrao com componentes diario, semanal e mensal |
| `HARRVResults` | Container de resultados (regressao OLS) |

!!! note "Diferenca em relacao aos modelos GARCH"
    O HAR-RV usa **regressao OLS** sobre a volatilidade realizada,
    nao estimacao por Maxima Verossimilhanca. A interface e ligeiramente
    diferente da classe base `VolatilityModel`.

---

## HARRV

::: archbox.models.har_rv.HARRV
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - fit

### Especificacao

$$
RV_t = \beta_0 + \beta_d \cdot RV^{(d)}_{t-1} + \beta_w \cdot RV^{(w)}_{t-1} + \beta_m \cdot RV^{(m)}_{t-1} + \varepsilon_t
$$

onde:

- $RV^{(d)}_{t-1} = RV_{t-1}$ -- volatilidade realizada diaria
- $RV^{(w)}_{t-1} = \frac{1}{5} \sum_{i=0}^{4} RV_{t-1-i}$ -- media semanal (5 dias)
- $RV^{(m)}_{t-1} = \frac{1}{22} \sum_{i=0}^{21} RV_{t-1-i}$ -- media mensal (22 dias)

### Construtor

```python
HARRV(realized_variance, components=None)
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `realized_variance` | `array-like` | -- | Serie de volatilidade realizada diaria |
| `components` | `list[str]` | `['daily', 'weekly', 'monthly']` | Componentes HAR a incluir |

**Componentes disponiveis:**

| Componente | Lag | Descricao |
|------------|-----|-----------|
| `'daily'` | 1 dia | Volatilidade realizada do dia anterior |
| `'weekly'` | 5 dias | Media movel de 5 dias |
| `'monthly'` | 22 dias | Media movel de 22 dias |

### Metodos

#### `fit()`

Ajusta o modelo HAR-RV via OLS.

```python
fit(method='ols') -> HARRVResults
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `method` | `str` | `'ols'` | Metodo de estimacao |

### Exemplo

```python
from archbox.models import HARRV
import numpy as np

# Simular volatilidade realizada
np.random.seed(42)
rv = np.abs(np.random.randn(500)) * 0.0002

# HAR-RV padrao (daily + weekly + monthly)
model = HARRV(rv)
result = model.fit()
print(result.summary())

# Previsao
fc = result.forecast(horizon=5)
print(f"RV prevista (5d): {fc}")
```

---

## HARRVResults

::: archbox.models.har_rv.HARRVResults
    options:
      show_root_heading: true
      show_source: true
      members:
        - summary
        - forecast

### Atributos

| Atributo | Tipo | Descricao |
|----------|------|-----------|
| `params` | `ndarray` | Coeficientes $[\beta_0, \beta_d, \beta_w, \beta_m]$ |
| `param_names` | `list[str]` | Nomes dos parametros |
| `std_errors` | `ndarray` | Erros-padrao OLS |
| `t_values` | `ndarray` | Estatisticas t |
| `r_squared` | `float` | $R^2$ |
| `adj_r_squared` | `float` | $R^2$ ajustado |
| `residuals` | `ndarray` | Residuos da regressao |
| `fitted_values` | `ndarray` | Valores ajustados |
| `nobs` | `int` | Numero de observacoes usadas |

### Metodos

#### `summary()`

Gera tabela formatada com coeficientes, erros-padrao, t-valores e $R^2$.

```python
result.summary() -> str
```

**Saida tipica:**
```
============================================================
HAR-RV Regression Results
============================================================
Observations: 478
R-squared: 0.456789
Adj. R-squared: 0.453123
------------------------------------------------------------
Parameter          Estimate      Std.Err      t-value
------------------------------------------------------------
beta_0             0.000045     0.000012       3.7500
beta_d             0.350000     0.045000       7.7778
beta_w             0.280000     0.060000       4.6667
beta_m             0.250000     0.055000       4.5455
============================================================
```

#### `forecast()`

Previsao iterativa da volatilidade realizada.

```python
result.forecast(horizon=1) -> ndarray
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `horizon` | `int` | `1` | Numero de passos a frente |

**Retorna**: `ndarray` com shape `(horizon,)`.

---

## Variantes do HAR

O modelo pode ser customizado selecionando diferentes componentes:

=== "HAR-RV completo"

    ```python
    # Componentes diario + semanal + mensal (padrao)
    model = HARRV(rv, components=['daily', 'weekly', 'monthly'])
    ```

=== "HAR-RV diario + semanal"

    ```python
    # Sem componente mensal
    model = HARRV(rv, components=['daily', 'weekly'])
    ```

=== "HAR-RV apenas diario"

    ```python
    # AR(1) na volatilidade realizada
    model = HARRV(rv, components=['daily'])
    ```

---

## Exemplo Completo

```python
from archbox.models import HARRV
import numpy as np

# Simular volatilidade realizada com autocorrelacao
np.random.seed(42)
n = 1000
rv = np.zeros(n)
rv[0] = 0.0001
for t in range(1, n):
    rv[t] = 0.00002 + 0.35 * rv[t-1] + 0.0001 * np.random.randn()**2

# Ajustar HAR-RV
model = HARRV(rv)
result = model.fit()

# Resumo
print(result.summary())

# Importancia dos componentes
for name, coef, se in zip(result.param_names, result.params, result.std_errors):
    print(f"{name}: {coef:.6f} (t={coef/se:.2f})")

# R-quadrado
print(f"\nR²: {result.r_squared:.4f}")
print(f"R² ajustado: {result.adj_r_squared:.4f}")

# Previsao
fc = result.forecast(horizon=10)
print(f"\nPrevisao RV (10 dias): {fc}")
```

---

## Referencia

Corsi, F. (2009). A Simple Approximate Long-Memory Model of Realized Volatility.
*Journal of Financial Econometrics*, 7(2), 174-196.

---

## Ver Tambem

- [GARCH](garch.md) -- Modelos GARCH parametricos para volatilidade condicional
- [Core](core.md) -- Classe base `VolatilityModel` (HAR-RV tem interface propria)
- [Multivariado](multivariate.md) -- Modelos multivariados
