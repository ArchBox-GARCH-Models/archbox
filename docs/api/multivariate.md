---
title: Multivariate API
description: Referencia dos modelos multivariados DCC, BEKK, CCC, GO-GARCH e DECO
---

# Multivariate API

!!! info "Modulo"
    ```python
    from archbox.multivariate import DCC, CCC, BEKK, GOGARCH, DECO
    from archbox.multivariate import MultivarResults
    ```

## Visao Geral

A archbox implementa 5 modelos multivariados de volatilidade condicional.
Todos herdam de `MultivariateVolatilityModel` e retornam `MultivarResults`.

| Classe | Modelo | Parametros | Caracteristica principal |
|--------|--------|------------|--------------------------|
| `DCC` | DCC-GARCH | $a, b$ | Correlacao dinamica via recursao |
| `CCC` | CCC-GARCH | -- | Correlacao constante (amostra) |
| `BEKK` | BEKK-GARCH | $C, A, B$ | Parametrizacao direta da covariancia |
| `GOGARCH` | GO-GARCH | -- | Fatores independentes via ICA |
| `DECO` | DECO-GARCH | $a, b$ | Equicorrelacao dinamica escalar |

A decomposicao fundamental e:

$$
H_t = D_t \cdot R_t \cdot D_t
$$

onde $D_t = \text{diag}(\sigma_{1,t}, \ldots, \sigma_{k,t})$ sao as volatilidades
individuais e $R_t$ e a matriz de correlacao condicional.

---

## MultivariateVolatilityModel (Base)

::: archbox.multivariate.base.MultivariateVolatilityModel
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - fit
        - forecast
        - portfolio_variance
        - covariance
        - correlation

### Construtor

```python
MultivariateVolatilityModel(endog, univariate_model='GARCH', univariate_order=(1, 1))
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | `ndarray` | -- | Retornos shape $(T, k)$ com $k \geq 2$ series |
| `univariate_model` | `str` | `'GARCH'` | Modelo GARCH univariado para cada serie |
| `univariate_order` | `tuple[int, int]` | `(1, 1)` | Ordem $(p, q)$ do GARCH univariado |

### Atributos

| Atributo | Tipo | Descricao |
|----------|------|-----------|
| `endog` | `ndarray` | Retornos $(T, k)$ |
| `T` | `int` | Numero de observacoes |
| `k` | `int` | Numero de series |
| `model_name` | `str` | Nome do modelo (ex: `"DCC-GARCH"`) |

### Metodos Comuns

#### `fit()`

Ajusta o modelo em dois passos:

1. Ajusta GARCH univariado para cada serie
2. Estima parametros de correlacao via MLE

```python
fit(method='two_step', disp=True) -> MultivarResults
```

#### `forecast()`

Previsao de $H_{T+h}$ para $h = 1, \ldots, \text{horizon}$.

```python
forecast(results, horizon=10) -> dict
```

**Retorna** dicionario com:

- `'covariance'`: shape `(horizon, k, k)`
- `'correlation'`: shape `(horizon, k, k)`

#### `portfolio_variance()`

Calcula variancia do portfolio $w' H_t w$ para todo $t$.

```python
portfolio_variance(weights, cov_t) -> ndarray  # shape (T,)
```

#### `covariance()` / `correlation()`

Extrai a matriz de covariancia/correlacao no instante $t$.

```python
covariance(corr_t, t) -> ndarray   # shape (k, k)
correlation(corr_t, t) -> ndarray  # shape (k, k)
```

---

## DCC

::: archbox.multivariate.dcc.DCC
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - fit
        - forecast

### Especificacao

**Recursao DCC** (Engle, 2002):

$$
Q_t = (1 - a - b) \bar{Q} + a \cdot z_{t-1} z'_{t-1} + b \cdot Q_{t-1}
$$

$$
R_t = \text{diag}(Q_t)^{-1/2} \cdot Q_t \cdot \text{diag}(Q_t)^{-1/2}
$$

onde $\bar{Q}$ e a correlacao incondicional dos residuos padronizados.

### Construtor

```python
DCC(endog, univariate_model='GARCH', univariate_order=(1, 1))
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | `ndarray` | -- | Retornos $(T, k)$ |
| `univariate_model` | `str` | `'GARCH'` | Modelo univariado |
| `univariate_order` | `tuple` | `(1, 1)` | Ordem do GARCH |

### Parametros Estimados

| Parametro | Restricao | Descricao |
|-----------|-----------|-----------|
| $a$ | $> 0$ | Peso da inovacao de correlacao |
| $b$ | $> 0$ | Persistencia da correlacao |
| | $a + b < 1$ | Estacionariedade |

### Exemplo

```python
from archbox.multivariate import DCC
import numpy as np

# Tres series de retornos
returns = np.random.randn(500, 3) * 0.01

model = DCC(returns)
result = model.fit(disp=False)

print(result.summary())

# Correlacao dinamica entre series 0 e 1
result.plot_correlation(0, 1)

# Previsao
fc = model.forecast(result, horizon=10)
print(f"Covariancia prevista (1d):\n{fc['covariance'][0]}")
```

---

## CCC

::: archbox.multivariate.ccc.CCC
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - fit

### Especificacao

**Correlacao Condicional Constante** (Bollerslev, 1990):

$$
R_t = \bar{R} \quad \forall t
$$

$$
H_t = D_t \cdot \bar{R} \cdot D_t
$$

onde $\bar{R}$ e a matriz de correlacao amostral dos residuos padronizados.

!!! note "Sem parametros de correlacao"
    O CCC nao estima parametros de correlacao -- usa a correlacao amostral.
    A unica estimacao e dos GARCH univariados.

### Construtor

```python
CCC(endog, univariate_model='GARCH', univariate_order=(1, 1))
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | `ndarray` | -- | Retornos $(T, k)$ |
| `univariate_model` | `str` | `'GARCH'` | Modelo univariado |
| `univariate_order` | `tuple` | `(1, 1)` | Ordem do GARCH |

### Exemplo

```python
from archbox.multivariate import CCC
import numpy as np

returns = np.random.randn(500, 3) * 0.01

model = CCC(returns)
result = model.fit(disp=False)

print(result.summary())

# Correlacao constante
print(f"Correlacao (constante):\n{result.dynamic_correlation[0]}")
```

---

## BEKK

::: archbox.multivariate.bekk.BEKK
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - fit

### Especificacao

**BEKK** (Baba-Engle-Kraft-Kroner, 1990):

$$
H_t = C'C + A' \varepsilon_{t-1} \varepsilon'_{t-1} A + B' H_{t-1} B
$$

onde $C$ e triangular inferior, $A$ e $B$ sao matrizes de parametros.

!!! note "Variante diagonal"
    Na variante diagonal, $A$ e $B$ sao diagonais, reduzindo o numero
    de parametros de $O(k^2)$ para $O(k)$.

### Construtor

```python
BEKK(endog, variant='diagonal', univariate_model='GARCH', univariate_order=(1, 1))
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | `ndarray` | -- | Retornos $(T, k)$ |
| `variant` | `str` | `'diagonal'` | `'full'` ou `'diagonal'` |
| `univariate_model` | `str` | `'GARCH'` | Modelo univariado |
| `univariate_order` | `tuple` | `(1, 1)` | Ordem do GARCH |

### Parametros Estimados (Diagonal)

| Parametro | Dimensao | Descricao |
|-----------|----------|-----------|
| $C$ | $k(k+1)/2$ | Elementos da triangular inferior |
| $A$ | $k$ | Diagonal de $A$ (impacto dos choques) |
| $B$ | $k$ | Diagonal de $B$ (persistencia) |

### Exemplo

```python
from archbox.multivariate import BEKK
import numpy as np

returns = np.random.randn(500, 2) * 0.01

model = BEKK(returns, variant='diagonal')
result = model.fit(disp=False)

print(result.summary())

# Covariancia dinamica
result.plot_covariance(0, 1)
```

---

## GO-GARCH

::: archbox.multivariate.gogarch.GOGARCH
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - fit

### Especificacao

**Generalized Orthogonal GARCH** (van der Weide, 2002):

$$
r_t = Z f_t, \quad f_t = \Sigma_t^{1/2} \eta_t
$$

onde $Z$ e a matriz de mixing (ICA), $f_t$ sao fatores independentes e
cada fator segue um GARCH univariado.

$$
H_t = Z \cdot \text{diag}(\sigma^2_{1,t}, \ldots, \sigma^2_{k,t}) \cdot Z'
$$

!!! note "Sem parametros de correlacao"
    GO-GARCH nao tem parametros de correlacao para estimar.
    A estrutura de dependencia e capturada pela decomposicao ICA.

### Construtor

```python
GOGARCH(endog, n_components=None, univariate_model='GARCH', univariate_order=(1, 1))
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | `ndarray` | -- | Retornos $(T, k)$ |
| `n_components` | `int` | `None` (= $k$) | Numero de componentes ICA |
| `univariate_model` | `str` | `'GARCH'` | Modelo univariado |
| `univariate_order` | `tuple` | `(1, 1)` | Ordem do GARCH |

### Exemplo

```python
from archbox.multivariate import GOGARCH
import numpy as np

returns = np.random.randn(500, 3) * 0.01

model = GOGARCH(returns)
result = model.fit(disp=False)

print(result.summary())

# Covariancia em t=100
print(f"H_100:\n{result.dynamic_covariance[100]}")
```

---

## DECO

::: archbox.multivariate.deco.DECO
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - fit

### Especificacao

**Dynamic Equicorrelation** (Engle & Kelly, 2012):

$$
R_t = (1 - \rho_t) I_k + \rho_t \mathbf{1}\mathbf{1}'
$$

onde $\rho_t$ e a equicorrelacao escalar dinamica:

$$
\rho_t = \frac{1}{k(k-1)} \left( \mathbf{1}' \tilde{R}_t \mathbf{1} - k \right)
$$

!!! tip "Quando usar DECO"
    DECO e ideal para portfolios com **muitas series** onde estimar
    matrizes de correlacao completas seria computacionalmente proibitivo.
    Assume que todas as correlacoes pairwise sao iguais em cada instante.

### Construtor

```python
DECO(endog, univariate_model='GARCH', univariate_order=(1, 1))
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | `ndarray` | -- | Retornos $(T, k)$ |
| `univariate_model` | `str` | `'GARCH'` | Modelo univariado |
| `univariate_order` | `tuple` | `(1, 1)` | Ordem do GARCH |

### Parametros Estimados

| Parametro | Restricao | Descricao |
|-----------|-----------|-----------|
| $a$ | $> 0$ | Peso da inovacao |
| $b$ | $> 0$ | Persistencia |
| | $a + b < 1$ | Estacionariedade |

### Exemplo

```python
from archbox.multivariate import DECO
import numpy as np

returns = np.random.randn(500, 5) * 0.01

model = DECO(returns)
result = model.fit(disp=False)

print(result.summary())

# Equicorrelacao dinamica
rho_t = result.dynamic_correlation[:, 0, 1]
print(f"Correlacao media: {rho_t.mean():.4f}")
```

---

## MultivarResults

::: archbox.multivariate.base.MultivarResults
    options:
      show_root_heading: true
      show_source: true
      members:
        - summary
        - plot_correlation
        - plot_covariance
        - portfolio_volatility

### Atributos

| Atributo | Tipo | Descricao |
|----------|------|-----------|
| `model` | `MultivariateVolatilityModel` | Modelo ajustado |
| `univariate_results` | `list[ArchResults]` | Resultados de cada GARCH univariado |
| `params` | `ndarray` | Parametros do modelo de correlacao |
| `dynamic_correlation` | `ndarray` | $R_t$ para todo $t$, shape $(T, k, k)$ |
| `dynamic_covariance` | `ndarray` | $H_t = D_t R_t D_t$, shape $(T, k, k)$ |
| `conditional_volatility` | `ndarray` | $\sigma_{i,t}$ para cada serie, shape $(T, k)$ |
| `std_resids` | `ndarray` | Residuos padronizados $z_t$, shape $(T, k)$ |
| `loglike` | `float` | Log-verossimilhanca total |
| `aic` | `float` | Criterio de Informacao de Akaike |
| `bic` | `float` | Criterio de Informacao Bayesiano |
| `n_obs` | `int` | Numero de observacoes |
| `n_series` | `int` | Numero de series |

### Metodos

#### `summary()`

Gera resumo com parametros univariados e de correlacao.

```python
result.summary() -> str
```

#### `plot_correlation()`

Plota correlacao dinamica entre duas series.

```python
result.plot_correlation(i, j)
```

#### `plot_covariance()`

Plota covariancia dinamica entre duas series.

```python
result.plot_covariance(i, j)
```

#### `portfolio_volatility()`

Calcula volatilidade do portfolio ao longo do tempo.

```python
result.portfolio_volatility(weights) -> ndarray  # shape (T,)
```

---

## Exemplo Completo: Portfolio com DCC

```python
from archbox.multivariate import DCC
import numpy as np

# Simular retornos de 3 ativos
np.random.seed(42)
returns = np.random.randn(500, 3) * 0.01

# Ajustar DCC-GARCH
model = DCC(returns, univariate_order=(1, 1))
result = model.fit(disp=False)

# Resumo
print(result.summary())

# Correlacao dinamica
result.plot_correlation(0, 1)
result.plot_correlation(0, 2)

# Previsao da covariancia
fc = model.forecast(result, horizon=10)
print(f"Covariancia prevista (1d):\n{fc['covariance'][0]}")
print(f"Correlacao prevista (1d):\n{fc['correlation'][0]}")

# Portfolio equal-weight
weights = np.array([1/3, 1/3, 1/3])
port_vol = result.portfolio_volatility(weights)
print(f"Volatilidade media do portfolio: {port_vol.mean():.6f}")

# Variancia do portfolio
port_var = model.portfolio_variance(weights, result.dynamic_covariance)
print(f"Variancia media do portfolio: {port_var.mean():.8f}")
```

---

## Comparacao dos Modelos

=== "Correlacao dinamica"

    ```python
    from archbox.multivariate import DCC, DECO

    # DCC: correlacao completa
    dcc = DCC(returns).fit(disp=False)

    # DECO: equicorrelacao escalar
    deco = DECO(returns).fit(disp=False)
    ```

=== "Correlacao constante"

    ```python
    from archbox.multivariate import CCC

    # CCC: baseline simples
    ccc = CCC(returns).fit(disp=False)
    ```

=== "Parametrizacao direta"

    ```python
    from archbox.multivariate import BEKK, GOGARCH

    # BEKK: parametrizacao da covariancia
    bekk = BEKK(returns, variant='diagonal').fit(disp=False)

    # GO-GARCH: fatores independentes
    go = GOGARCH(returns).fit(disp=False)
    ```

---

## Referencias

- Bollerslev, T. (1990). Modelling the Coherence in Short-Run Nominal Exchange Rates.
  *Review of Economics and Statistics*, 72(3), 498-505.
- Engle, R.F. (2002). Dynamic Conditional Correlation.
  *Journal of Business & Economic Statistics*, 20(3), 339-350.
- Engle, R.F. & Kelly, B.T. (2012). Dynamic Equicorrelation.
  *Journal of Business & Economic Statistics*, 30(2), 212-228.
- Engle, R.F. & Kroner, K.F. (1995). Multivariate Simultaneous Generalized ARCH.
  *Econometric Theory*, 11(1), 122-150.
- van der Weide, R. (2002). GO-GARCH: A Multivariate Generalized Orthogonal GARCH Model.
  *Journal of Applied Econometrics*, 17(5), 549-564.

---

## Ver Tambem

- [Core](core.md) -- Classe base `VolatilityModel` e `ArchResults`
- [GARCH](garch.md) -- Modelos GARCH univariados
- [HAR](har.md) -- HAR-RV para volatilidade realizada
