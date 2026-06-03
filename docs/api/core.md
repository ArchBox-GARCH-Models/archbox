---
title: Core API
description: Classes base, containers de resultado e excepcoes da archbox
---

# Core API

!!! info "Modulo"
    ```python
    from archbox.core import VolatilityModel, ArchResults
    from archbox.core import ArchBoxError, ConvergenceError, ValidationError, StationarityError
    ```

## Visao Geral

O modulo `archbox.core` contem as classes fundamentais da biblioteca:

- **`VolatilityModel`** -- Classe abstrata base para todos os modelos de volatilidade
- **`ArchResults`** -- Container de resultados para modelos ajustados
- **Excepcoes** -- Hierarquia de erros especificos

---

## VolatilityModel

::: archbox.core.volatility_model.VolatilityModel
    options:
      show_root_heading: true
      show_source: true
      members:
        - fit
        - loglike
        - loglike_per_obs
        - simulate
        - start_params
        - param_names
        - num_params
        - bounds
        - transform_params
        - untransform_params

### Construtor

```python
VolatilityModel(endog, mean='constant', dist='normal')
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | `array-like` | -- | Serie temporal de retornos |
| `mean` | `str` | `'constant'` | `'constant'` (remove a media) ou `'zero'` |
| `dist` | `str` | `'normal'` | Distribuicao condicional dos residuos |

### Atributos

| Atributo | Tipo | Descricao |
|----------|------|-----------|
| `endog` | `ndarray` | Retornos (demeaned se `mean='constant'`) |
| `nobs` | `int` | Numero de observacoes |
| `mu` | `float` | Media estimada (0 se `mean='zero'`) |
| `dist` | `Distribution` | Instancia da distribuicao condicional |
| `volatility_process` | `str` | Nome do processo (ex: `"GARCH"`, `"EGARCH"`) |

### Metodos Principais

#### `fit()`

Ajusta o modelo via Maxima Verossimilhanca (MLE).

```python
fit(method='mle', starting_values=None, variance_targeting=False, disp=True) -> ArchResults
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `method` | `str` | `'mle'` | Metodo de estimacao |
| `starting_values` | `ndarray` | `None` | Valores iniciais customizados |
| `variance_targeting` | `bool` | `False` | Fixar $\omega = \bar{\sigma}^2 (1 - \text{persistencia})$ |
| `disp` | `bool` | `True` | Exibir progresso da otimizacao |

#### `loglike()`

Calcula a log-verossimilhanca total.

```python
loglike(params, backcast=None) -> float
```

#### `loglike_per_obs()`

Calcula a log-verossimilhanca por observacao.

```python
loglike_per_obs(params, backcast=None) -> ndarray
```

#### `simulate()`

Simula retornos e volatilidade a partir do modelo.

```python
simulate(n, params, seed=None) -> tuple[ndarray, ndarray]
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `n` | `int` | -- | Numero de observacoes a simular |
| `params` | `ndarray` | -- | Parametros do modelo |
| `seed` | `int` | `None` | Semente para reproducibilidade |

**Retorna**: `(retornos, volatilidade_condicional)`, cada um com shape `(n,)`.

### Metodos Abstratos

Subclasses **devem** implementar:

| Metodo | Descricao |
|--------|-----------|
| `_variance_recursion(params, resids, backcast)` | Recursao da variancia condicional |
| `start_params` | Valores iniciais dos parametros (property) |
| `param_names` | Nomes dos parametros (property) |
| `num_params` | Numero de parametros (property) |
| `bounds()` | Limites para o otimizador |
| `transform_params(unconstrained)` | Transformacao para espaco restrito |
| `untransform_params(constrained)` | Transformacao para espaco irrestrito |

### Exemplo

```python
from archbox.models import GARCH
import numpy as np

# VolatilityModel e abstrata - use uma subclasse
returns = np.random.randn(1000) * 0.01
model = GARCH(returns, p=1, q=1, mean='constant')

# Atributos disponiveis antes do fit
print(f"Observacoes: {model.nobs}")
print(f"Media: {model.mu:.6f}")
print(f"Processo: {model.volatility_process}")

# Ajustar
result = model.fit(disp=False)
```

---

## ArchResults

::: archbox.core.results.ArchResults
    options:
      show_root_heading: true
      show_source: true
      members:
        - summary
        - forecast
        - persistence
        - half_life
        - unconditional_variance
        - plot
        - to_dataframe
        - save
        - load

### Construtor

```python
ArchResults(model, params, loglike, sigma2, se_robust, se_nonrobust, convergence)
```

!!! note "Nota"
    Usuarios normalmente nao constroem `ArchResults` diretamente.
    O objeto e retornado por `model.fit()`.

### Atributos

| Atributo | Tipo | Descricao |
|----------|------|-----------|
| `params` | `ndarray` | Parametros estimados |
| `param_names` | `list[str]` | Nomes dos parametros |
| `loglike` | `float` | Log-verossimilhanca no otimo |
| `nobs` | `int` | Numero de observacoes |
| `convergence` | `bool` | Se a otimizacao convergiu |
| `se_robust` | `ndarray` | Erros-padrao robustos (Bollerslev-Wooldridge) |
| `se_nonrobust` | `ndarray` | Erros-padrao nao-robustos (Hessiana inversa) |
| `se` | `ndarray` | Erros-padrao default (robustos) |
| `tvalues` | `ndarray` | Estatisticas t |
| `pvalues` | `ndarray` | p-valores (bilateral) |
| `conditional_volatility` | `ndarray` | $\sigma_t = \sqrt{\sigma^2_t}$ |
| `resid` | `ndarray` | Residuos padronizados $z_t = \varepsilon_t / \sigma_t$ |
| `aic` | `float` | $\text{AIC} = -2\ell + 2k$ |
| `bic` | `float` | $\text{BIC} = -2\ell + k \ln(n)$ |
| `hqic` | `float` | $\text{HQIC} = -2\ell + 2k \ln(\ln(n))$ |

### Metodos

#### `summary()`

Gera tabela formatada com parametros, erros-padrao, t-valores, p-valores,
log-verossimilhanca, AIC/BIC, persistencia e meia-vida.

```python
result.summary() -> str
```

#### `forecast()`

Previsao da variancia condicional $h$ passos a frente.

Para GARCH(1,1):

$$
E[\sigma^2_{T+h}] = \bar{\sigma}^2 + (\alpha + \beta)^{h-1} (\sigma^2_{T+1} - \bar{\sigma}^2)
$$

```python
result.forecast(horizon=1, method='analytic') -> dict
```

**Retorna** dicionario com chaves:

- `'variance'`: variancia prevista, shape `(horizon,)`
- `'volatility'`: volatilidade prevista (raiz quadrada), shape `(horizon,)`

#### `persistence()`

Calcula a persistencia: $\sum \alpha_i + \sum \beta_j$.

```python
result.persistence() -> float
```

!!! tip "Interpretacao"
    - Persistencia $< 1$: processo estacionario
    - Persistencia $\approx 1$: choques demoram para dissipar (IGARCH)
    - Persistencia $\geq 1$: processo nao-estacionario

#### `half_life()`

Meia-vida dos choques de volatilidade:

$$
\text{half-life} = \frac{\ln(0.5)}{\ln(\text{persistencia})}
$$

```python
result.half_life() -> float
```

#### `unconditional_variance()`

Variancia incondicional (longo prazo):

$$
\bar{\sigma}^2 = \frac{\omega}{1 - \text{persistencia}}
$$

```python
result.unconditional_variance() -> float
```

#### `plot()`

Plota volatilidade condicional ou diagnosticos de residuos.

```python
result.plot(which='volatility') -> Figure
```

| Valor `which` | Descricao |
|---------------|-----------|
| `'volatility'` | Retornos + volatilidade condicional |
| `'residuals'` | Residuos padronizados + histograma |

#### `to_dataframe()`

Exporta estimativas como `pandas.DataFrame`.

```python
result.to_dataframe() -> pd.DataFrame
# Colunas: estimate, std_err, t_value, p_value
```

#### `save()` / `load()`

Persistencia via pickle.

```python
result.save('model_results.pkl')
loaded = ArchResults.load('model_results.pkl')
```

### Exemplo Completo

```python
from archbox.models import GARCH
import numpy as np

returns = np.random.randn(1000) * 0.01

model = GARCH(returns, p=1, q=1)
result = model.fit(disp=False)

# Resumo
print(result.summary())

# Metricas
print(f"Persistencia: {result.persistence():.4f}")
print(f"Meia-vida: {result.half_life():.1f} periodos")
print(f"Variancia incondicional: {result.unconditional_variance():.6e}")

# Previsao
fc = result.forecast(horizon=5)
print(f"Volatilidade prevista (5d): {fc['volatility']}")

# Exportar
df = result.to_dataframe()
print(df)

# Plot
fig = result.plot(which='volatility')
```

---

## Config

::: archbox.core.config.ArchBoxConfig
    options:
      show_root_heading: true
      show_source: true

---

## Excepcoes

::: archbox.core.exceptions
    options:
      show_root_heading: true
      show_source: true

### Hierarquia

```
ArchBoxError (base)
├── ConvergenceError    -- otimizacao nao convergiu
├── ValidationError     -- dados ou parametros invalidos
└── StationarityError   -- condicoes de estacionariedade violadas
```

### Exemplo

```python
from archbox.core import ConvergenceError, ValidationError
from archbox.models import GARCH
import numpy as np

try:
    model = GARCH(np.array([1.0, 2.0]), p=1, q=1)  # poucas obs
    result = model.fit(disp=False)
except ValidationError as e:
    print(f"Dados invalidos: {e}")
except ConvergenceError as e:
    print(f"Nao convergiu: {e}")
```

---

## Ver Tambem

- [GARCH](garch.md) -- Modelos univariados que herdam de `VolatilityModel`
- [HAR](har.md) -- HAR-RV (modelo de regressao, interface diferente)
- [Multivariado](multivariate.md) -- `MultivariateVolatilityModel` e `MultivarResults`
