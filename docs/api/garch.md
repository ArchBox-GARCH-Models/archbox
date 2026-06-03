---
title: GARCH API
description: Referencia dos 8 modelos GARCH univariados da archbox
---

# GARCH API

!!! info "Modulo"
    ```python
    from archbox.models import (
        GARCH, EGARCH, GJRGARCH, APARCH,
        FIGARCH, IGARCH, GARCHM, ComponentGARCH,
    )
    ```

## Visao Geral

A archbox implementa 8 variantes de modelos GARCH univariados. Todos herdam
de [`VolatilityModel`](core.md#volatilitymodel) e retornam [`ArchResults`](core.md#archresults).

| Classe | Modelo | Parametros | Caracteristica principal |
|--------|--------|------------|--------------------------|
| `GARCH` | GARCH(p,q) | $\omega, \alpha_i, \beta_j$ | Modelo simetrico padrao |
| `EGARCH` | EGARCH(p,q) | $\omega, \alpha_i, \gamma_i, \beta_j$ | Log-variancia, sem restricao de positividade |
| `GJRGARCH` | GJR-GARCH(p,q) | $\omega, \alpha_i, \gamma_i, \beta_j$ | Threshold para assimetria (leverage) |
| `APARCH` | APARCH(p,q) | $\omega, \alpha_i, \gamma_i, \beta_j, \delta$ | Potencia assimetrica flexivel |
| `FIGARCH` | FIGARCH(1,d,1) | $\omega, \phi, d, \beta$ | Memoria longa fracionaria |
| `IGARCH` | IGARCH(1,1) | $\omega, \alpha$ | Persistencia unitaria |
| `GARCHM` | GARCH-M(p,q) | $\omega, \alpha_i, \beta_j, \lambda$ | Volatilidade na equacao da media |
| `ComponentGARCH` | CGARCH | $\omega, \alpha, \beta, \alpha_p, \beta_p$ | Componentes permanente + transitorio |

---

## GARCH

::: archbox.models.garch.GARCH
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - fit
        - simulate

### Especificacao

$$
\sigma^2_t = \omega + \sum_{i=1}^{q} \alpha_i \varepsilon^2_{t-i} + \sum_{j=1}^{p} \beta_j \sigma^2_{t-j}
$$

### Construtor

```python
GARCH(endog, p=1, q=1, mean='constant', dist='normal')
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | `array-like` | -- | Serie de retornos |
| `p` | `int` | `1` | Numero de termos GARCH ($\beta$) |
| `q` | `int` | `1` | Numero de termos ARCH ($\alpha$) |
| `mean` | `str` | `'constant'` | Modelo da media |
| `dist` | `str` | `'normal'` | Distribuicao condicional |

### Parametros Estimados

Para GARCH(1,1): `[omega, alpha_1, beta_1]`

| Parametro | Restricao | Descricao |
|-----------|-----------|-----------|
| $\omega$ | $> 0$ | Intercepto |
| $\alpha_i$ | $\geq 0$ | Peso dos choques passados |
| $\beta_j$ | $\geq 0$ | Peso da variancia passada |
| | $\sum \alpha + \sum \beta < 1$ | Estacionariedade |

### Exemplo

```python
from archbox.models import GARCH
import numpy as np

returns = np.random.randn(1000) * 0.01

model = GARCH(returns, p=1, q=1)
result = model.fit(disp=False)
print(result.summary())

# Previsao
fc = result.forecast(horizon=10)
print(fc['volatility'])

# Simulacao
sim_ret, sim_vol = model.simulate(n=500, params=result.params, seed=42)
```

---

## EGARCH

::: archbox.models.egarch.EGARCH
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - fit

### Especificacao

$$
\ln(\sigma^2_t) = \omega + \sum_{i=1}^{q} \alpha_i |z_{t-i}| + \sum_{i=1}^{q} \gamma_i z_{t-i} + \sum_{j=1}^{p} \beta_j \ln(\sigma^2_{t-j})
$$

onde $z_t = \varepsilon_t / \sigma_t$ sao os residuos padronizados.

!!! tip "Vantagem"
    Como a equacao modela $\ln(\sigma^2_t)$, nao ha necessidade de
    restricoes de positividade nos parametros.

### Construtor

```python
EGARCH(endog, p=1, q=1, mean='constant', dist='normal')
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | `array-like` | -- | Serie de retornos |
| `p` | `int` | `1` | Termos GARCH |
| `q` | `int` | `1` | Termos ARCH |
| `mean` | `str` | `'constant'` | Modelo da media |
| `dist` | `str` | `'normal'` | Distribuicao condicional |

### Parametros Estimados

Para EGARCH(1,1): `[omega, alpha_1, gamma_1, beta_1]`

| Parametro | Descricao |
|-----------|-----------|
| $\omega$ | Intercepto |
| $\alpha_i$ | Efeito de magnitude (choques simetricos) |
| $\gamma_i$ | Efeito de sinal (leverage); $\gamma < 0$ indica assimetria |
| $\beta_j$ | Persistencia |

### Exemplo

```python
from archbox.models import EGARCH
import numpy as np

returns = np.random.randn(1000) * 0.01
model = EGARCH(returns, p=1, q=1)
result = model.fit(disp=False)

# gamma < 0 indica efeito leverage
print(f"Efeito leverage (gamma): {result.params[2]:.4f}")
print(result.summary())
```

---

## GJR-GARCH

::: archbox.models.gjr_garch.GJRGARCH
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - fit

### Especificacao

$$
\sigma^2_t = \omega + \sum_{i=1}^{q} (\alpha_i + \gamma_i \cdot \mathbb{1}_{\{\varepsilon_{t-i} < 0\}}) \varepsilon^2_{t-i} + \sum_{j=1}^{p} \beta_j \sigma^2_{t-j}
$$

onde $\mathbb{1}_{\{\varepsilon < 0\}}$ e a funcao indicadora para choques negativos.

### Construtor

```python
GJRGARCH(endog, p=1, q=1, mean='constant', dist='normal')
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | `array-like` | -- | Serie de retornos |
| `p` | `int` | `1` | Termos GARCH |
| `q` | `int` | `1` | Termos ARCH |
| `mean` | `str` | `'constant'` | Modelo da media |
| `dist` | `str` | `'normal'` | Distribuicao condicional |

### Parametros Estimados

Para GJR-GARCH(1,1): `[omega, alpha_1, gamma_1, beta_1]`

| Parametro | Restricao | Descricao |
|-----------|-----------|-----------|
| $\omega$ | $> 0$ | Intercepto |
| $\alpha_i$ | $\geq 0$ | Impacto de choques positivos |
| $\gamma_i$ | $\geq 0$ | Impacto **adicional** de choques negativos |
| $\beta_j$ | $\geq 0$ | Persistencia |

### Exemplo

```python
from archbox.models import GJRGARCH
import numpy as np

returns = np.random.randn(1000) * 0.01
model = GJRGARCH(returns, p=1, q=1)
result = model.fit(disp=False)

# gamma > 0 indica que choques negativos tem maior impacto
print(f"Assimetria (gamma): {result.params[2]:.4f}")
print(result.summary())
```

---

## APARCH

::: archbox.models.aparch.APARCH
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - fit

### Especificacao

$$
\sigma^\delta_t = \omega + \sum_{i=1}^{q} \alpha_i (|\varepsilon_{t-i}| - \gamma_i \varepsilon_{t-i})^\delta + \sum_{j=1}^{p} \beta_j \sigma^\delta_{t-j}
$$

onde $\delta > 0$ e o parametro de potencia e $|\gamma_i| \leq 1$ controla a assimetria.

!!! tip "Flexibilidade"
    APARCH aninha GARCH ($\delta=2, \gamma=0$), GJR-GARCH ($\delta=2$)
    e modelos de desvio absoluto ($\delta=1$).

### Construtor

```python
APARCH(endog, p=1, q=1, mean='constant', dist='normal')
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | `array-like` | -- | Serie de retornos |
| `p` | `int` | `1` | Termos GARCH |
| `q` | `int` | `1` | Termos ARCH |
| `mean` | `str` | `'constant'` | Modelo da media |
| `dist` | `str` | `'normal'` | Distribuicao condicional |

### Parametros Estimados

Para APARCH(1,1): `[omega, alpha_1, gamma_1, beta_1, delta]`

| Parametro | Restricao | Descricao |
|-----------|-----------|-----------|
| $\omega$ | $> 0$ | Intercepto |
| $\alpha_i$ | $\geq 0$ | Coeficiente ARCH |
| $\gamma_i$ | $[-1, 1]$ | Assimetria |
| $\beta_j$ | $\geq 0$ | Persistencia |
| $\delta$ | $> 0$ | Parametro de potencia |

### Exemplo

```python
from archbox.models import APARCH
import numpy as np

returns = np.random.randn(1000) * 0.01
model = APARCH(returns, p=1, q=1)
result = model.fit(disp=False)

# delta estimado
print(f"Potencia (delta): {result.params[4]:.4f}")
print(result.summary())
```

---

## FIGARCH

::: archbox.models.figarch.FIGARCH
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - fit

### Especificacao

$$
\sigma^2_t = \frac{\omega}{1-\beta} + \sum_{k=1}^{\infty} \lambda_k \varepsilon^2_{t-k}
$$

onde os coeficientes $\lambda_k$ sao determinados pelo parametro fracionario $d$,
com $0 \leq d \leq 1$ controlando a memoria longa.

!!! note "Memoria longa"
    - $d = 0$: GARCH padrao (memoria curta)
    - $0 < d < 1$: Memoria longa fracionaria
    - $d = 1$: IGARCH (persistencia unitaria)

### Construtor

```python
FIGARCH(endog, truncation_lag=1000, mean='constant', dist='normal')
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | `array-like` | -- | Serie de retornos |
| `truncation_lag` | `int` | `1000` | Lag de truncamento para expansao fracionaria |
| `mean` | `str` | `'constant'` | Modelo da media |
| `dist` | `str` | `'normal'` | Distribuicao condicional |

### Parametros Estimados

`[omega, phi, d, beta]`

| Parametro | Restricao | Descricao |
|-----------|-----------|-----------|
| $\omega$ | $> 0$ | Intercepto |
| $\phi$ | $[0, 1)$ | Coeficiente ARCH |
| $d$ | $[0, 1]$ | Parametro de integracao fracionaria |
| $\beta$ | $[0, 1)$ | Coeficiente GARCH |

### Exemplo

```python
from archbox.models import FIGARCH
import numpy as np

returns = np.random.randn(2000) * 0.01
model = FIGARCH(returns, truncation_lag=500)
result = model.fit(disp=False)

# d proximo de 0.5 indica memoria longa significativa
print(f"Parametro d: {result.params[2]:.4f}")
print(result.summary())
```

---

## IGARCH

::: archbox.models.igarch.IGARCH
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - fit

### Especificacao

$$
\sigma^2_t = \omega + \alpha \varepsilon^2_{t-1} + (1 - \alpha) \sigma^2_{t-1}
$$

Caso especial de GARCH(1,1) com $\alpha + \beta = 1$ (persistencia unitaria).

!!! note "Persistencia"
    No IGARCH choques de volatilidade persistem indefinidamente.
    Nao existe variancia incondicional finita.

### Construtor

```python
IGARCH(endog, mean='constant', dist='normal')
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | `array-like` | -- | Serie de retornos |
| `mean` | `str` | `'constant'` | Modelo da media |
| `dist` | `str` | `'normal'` | Distribuicao condicional |

### Parametros Estimados

`[omega, alpha]` (beta = 1 - alpha e implicito)

| Parametro | Restricao | Descricao |
|-----------|-----------|-----------|
| $\omega$ | $> 0$ | Intercepto |
| $\alpha$ | $(0, 1)$ | Peso dos choques |

### Exemplo

```python
from archbox.models import IGARCH
import numpy as np

returns = np.random.randn(1000) * 0.01
model = IGARCH(returns)
result = model.fit(disp=False)

print(f"alpha: {result.params[1]:.4f}")
print(f"beta (implicito): {1 - result.params[1]:.4f}")
print(result.summary())
```

---

## GARCH-M

::: archbox.models.garch_m.GARCHM
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - fit

### Especificacao

**Equacao da media:**

$$
r_t = \mu + \lambda \cdot g(\sigma^2_t) + \varepsilon_t
$$

onde $g(\cdot)$ depende do tipo de `risk_premium`:

| `risk_premium` | $g(\sigma^2_t)$ |
|----------------|-----------------|
| `'variance'` | $\sigma^2_t$ |
| `'volatility'` | $\sigma_t$ |
| `'log_variance'` | $\ln(\sigma^2_t)$ |

**Equacao da variancia** (GARCH padrao):

$$
\sigma^2_t = \omega + \sum_{i=1}^{q} \alpha_i \varepsilon^2_{t-i} + \sum_{j=1}^{p} \beta_j \sigma^2_{t-j}
$$

### Construtor

```python
GARCHM(endog, p=1, q=1, risk_premium='variance', mean='constant', dist='normal')
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | `array-like` | -- | Serie de retornos |
| `p` | `int` | `1` | Termos GARCH |
| `q` | `int` | `1` | Termos ARCH |
| `risk_premium` | `str` | `'variance'` | Tipo de premio de risco |
| `mean` | `str` | `'constant'` | Modelo da media |
| `dist` | `str` | `'normal'` | Distribuicao condicional |

### Parametros Estimados

Para GARCH-M(1,1): `[omega, alpha_1, beta_1, lambda]`

| Parametro | Descricao |
|-----------|-----------|
| $\omega$ | Intercepto da variancia |
| $\alpha_i$ | Coeficiente ARCH |
| $\beta_j$ | Coeficiente GARCH |
| $\lambda$ | Premio de risco (volatilidade na media) |

!!! tip "Interpretacao"
    $\lambda > 0$ indica que maior risco (volatilidade) esta associado
    a maiores retornos esperados -- consistente com a teoria financeira.

### Exemplo

```python
from archbox.models import GARCHM
import numpy as np

returns = np.random.randn(1000) * 0.01
model = GARCHM(returns, p=1, q=1, risk_premium='volatility')
result = model.fit(disp=False)

print(f"Premio de risco (lambda): {result.params[3]:.4f}")
print(result.summary())
```

---

## Component GARCH

::: archbox.models.component_garch.ComponentGARCH
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - fit

### Especificacao

**Componente permanente (tendencia):**

$$
q_t = \omega + \alpha_p (\varepsilon^2_{t-1} - \sigma^2_{t-1}) + \beta_p \cdot q_{t-1}
$$

**Componente transitorio:**

$$
\sigma^2_t - q_t = \alpha (\varepsilon^2_{t-1} - q_{t-1}) + \beta (\sigma^2_{t-1} - q_{t-1})
$$

**Variancia total:** $\sigma^2_t = q_t + (\sigma^2_t - q_t)$

### Construtor

```python
ComponentGARCH(endog, mean='constant', dist='normal')
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | `array-like` | -- | Serie de retornos |
| `mean` | `str` | `'constant'` | Modelo da media |
| `dist` | `str` | `'normal'` | Distribuicao condicional |

### Parametros Estimados

`[omega, alpha, beta, alpha_p, beta_p]`

| Parametro | Descricao |
|-----------|-----------|
| $\omega$ | Nivel de longo prazo |
| $\alpha$ | ARCH do componente transitorio |
| $\beta$ | GARCH do componente transitorio |
| $\alpha_p$ | ARCH do componente permanente |
| $\beta_p$ | GARCH do componente permanente |

### Exemplo

```python
from archbox.models import ComponentGARCH
import numpy as np

returns = np.random.randn(1000) * 0.01
model = ComponentGARCH(returns)
result = model.fit(disp=False)

print(f"Persistencia transitoria (alpha+beta): {result.params[1]+result.params[2]:.4f}")
print(f"Persistencia permanente (beta_p): {result.params[4]:.4f}")
print(result.summary())
```

---

## Comparacao Rapida

=== "Simetricos"

    ```python
    from archbox.models import GARCH, IGARCH, FIGARCH, ComponentGARCH

    # GARCH padrao
    m1 = GARCH(returns, p=1, q=1)

    # Persistencia unitaria
    m2 = IGARCH(returns)

    # Memoria longa
    m3 = FIGARCH(returns, truncation_lag=500)

    # Dois componentes
    m4 = ComponentGARCH(returns)
    ```

=== "Assimetricos"

    ```python
    from archbox.models import EGARCH, GJRGARCH, APARCH

    # Log-variancia (sem restricao de positividade)
    m1 = EGARCH(returns, p=1, q=1)

    # Threshold (leverage simples)
    m2 = GJRGARCH(returns, p=1, q=1)

    # Potencia flexivel
    m3 = APARCH(returns, p=1, q=1)
    ```

=== "Media condicional"

    ```python
    from archbox.models import GARCHM

    # Risco na equacao da media
    m1 = GARCHM(returns, risk_premium='variance')
    m2 = GARCHM(returns, risk_premium='volatility')
    m3 = GARCHM(returns, risk_premium='log_variance')
    ```

---

## Ver Tambem

- [Core](core.md) -- Classe base `VolatilityModel` e resultado `ArchResults`
- [HAR](har.md) -- Modelo HAR-RV para volatilidade realizada
- [Multivariado](multivariate.md) -- Extensoes multivariadas (DCC, BEKK, etc.)
