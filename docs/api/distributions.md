---
title: Distributions API
description: Referencia das distribuicoes condicionais Normal, StudentT, SkewedT, GED e MixtureNormal
---

# Distributions API

!!! info "Modulo"
    ```python
    from archbox.distributions import (
        Normal, StudentT, SkewedT,
        GeneralizedError, MixtureNormal,
    )
    ```

## Visao Geral

As distribuicoes condicionais sao usadas para modelar as inovacoes
padronizadas $z_t = \varepsilon_t / \sigma_t$ nos modelos GARCH. Todas
herdam de `Distribution` e implementam uma interface comum.

| Classe | Distribuicao | Parametros extras | Caudas |
|--------|-------------|-------------------|--------|
| `Normal` | Gaussiana | -- | Finas |
| `StudentT` | Student-$t$ | $\nu$ (graus de liberdade) | Pesadas |
| `SkewedT` | Skewed Student-$t$ | $\nu$, $\lambda$ (assimetria) | Pesadas + assimetricas |
| `GeneralizedError` | GED | $p$ (shape) | Configuravel |
| `MixtureNormal` | Mistura de Normais | $w$, $\sigma^2$ (peso, variancia) | Pesadas |

### Interface Comum

Todos os metodos abaixo estao disponiveis em cada distribuicao:

| Metodo | Descricao |
|--------|-----------|
| `loglikelihood(resids, sigma2)` | Log-verossimilhanca por observacao |
| `ppf(q)` | Funcao quantil (inversa da CDF) |
| `cdf(x)` | Funcao de distribuicao acumulada |
| `simulate(n, rng)` | Gerar amostras aleatorias |
| `start_params()` | Valores iniciais para otimizacao |
| `bounds()` | Limites dos parametros |

**Properties**:

| Property | Descricao |
|----------|-----------|
| `num_params` | Numero de parametros de forma |
| `param_names` | Nomes dos parametros |

---

## Distribution (Base)

::: archbox.distributions.base.Distribution
    options:
      show_root_heading: true
      show_source: true
      members:
        - loglikelihood
        - ppf
        - cdf
        - simulate
        - start_params
        - bounds
        - num_params
        - param_names

### Descricao

Classe abstrata base para todas as distribuicoes condicionais.
Subclasses devem implementar todos os metodos abstratos.

A log-verossimilhanca de um modelo GARCH com distribuicao $f$ e:

$$
\ell(\theta) = \sum_{t=1}^{T} \left[ -\frac{1}{2} \ln \sigma^2_t + \ln f\left(\frac{\varepsilon_t}{\sigma_t}\right) \right]
$$

---

## Normal

::: archbox.distributions.normal.Normal
    options:
      show_root_heading: true
      show_source: true
      members:
        - loglikelihood
        - ppf
        - cdf
        - simulate

### Especificacao

Distribuicao Normal padrao:

$$
f(z) = \frac{1}{\sqrt{2\pi}} \exp\left(-\frac{z^2}{2}\right)
$$

Log-verossimilhanca:

$$
\ell_t = -\frac{1}{2} \left[ \ln(2\pi) + \ln(\sigma^2_t) + \frac{\varepsilon^2_t}{\sigma^2_t} \right]
$$

!!! note "Sem parametros extras"
    A distribuicao Normal nao tem parametros de forma adicionais
    (`num_params = 0`).

### Construtor

```python
Normal()
```

### Exemplo

```python
from archbox.distributions import Normal
import numpy as np

dist = Normal()

# Propriedades
print(f"Parametros: {dist.num_params}")  # 0
print(f"Nomes: {dist.param_names}")      # []

# Quantil (VaR)
var_95 = dist.ppf(0.05)
print(f"VaR 95%: {var_95:.4f}")  # -1.6449

# CDF
print(f"P(z < 0) = {dist.cdf(0):.4f}")  # 0.5000

# Simular
rng = np.random.default_rng(42)
samples = dist.simulate(1000, rng)
print(f"Media: {samples.mean():.3f}, Std: {samples.std():.3f}")
```

---

## StudentT

::: archbox.distributions.student_t.StudentT
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - loglikelihood
        - ppf
        - cdf
        - simulate

### Especificacao

Distribuicao Student-$t$ padronizada (variancia unitaria):

$$
f(z; \nu) = \frac{\Gamma\left(\frac{\nu+1}{2}\right)}{\sqrt{(\nu-2)\pi} \, \Gamma\left(\frac{\nu}{2}\right)} \left(1 + \frac{z^2}{\nu - 2}\right)^{-\frac{\nu+1}{2}}
$$

onde $\nu > 2$ sao os graus de liberdade.

!!! tip "Caudas pesadas"
    - $\nu \to \infty$: converge para a Normal
    - $\nu < 10$: caudas visivelmente mais pesadas
    - $\nu = 4$: curtose infinita

### Construtor

```python
StudentT(nu=None)
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `nu` | `float\|None` | `None` | Graus de liberdade fixos. Se `None`, sera estimado via MLE |

### Parametros

| Parametro | Restricao | Descricao |
|-----------|-----------|-----------|
| $\nu$ | $> 2$ | Graus de liberdade |

### Exemplo

```python
from archbox.distributions import StudentT
import numpy as np

# nu estimado via MLE
dist = StudentT()
print(f"Parametros: {dist.num_params}")  # 1
print(f"Nomes: {dist.param_names}")      # ['nu']

# nu fixo
dist_fixed = StudentT(nu=5)
print(f"Parametros: {dist_fixed.num_params}")  # 0

# Quantil (caudas mais pesadas que Normal)
var_95_normal = -1.6449
var_95_t5 = dist_fixed.ppf(0.05)
print(f"VaR 95% (t5): {var_95_t5:.4f}")  # mais extremo

# Log-verossimilhanca
rng = np.random.default_rng(42)
resids = rng.standard_normal(100)
sigma2 = np.ones(100) * 0.01
ll = dist_fixed.loglikelihood(resids, sigma2)
print(f"Log-lik: {ll.sum():.2f}")
```

---

## SkewedT

::: archbox.distributions.skewed_t.SkewedT
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - loglikelihood
        - ppf
        - cdf
        - simulate

### Especificacao

Distribuicao Skewed Student-$t$ (Hansen, 1994):

$$
f(z; \nu, \lambda) = \begin{cases}
bc \left(1 + \frac{1}{\nu-2}\left(\frac{bz+a}{1-\lambda}\right)^2\right)^{-\frac{\nu+1}{2}} & z < -a/b \\
bc \left(1 + \frac{1}{\nu-2}\left(\frac{bz+a}{1+\lambda}\right)^2\right)^{-\frac{\nu+1}{2}} & z \geq -a/b
\end{cases}
$$

onde $\lambda \in (-1, 1)$ controla a assimetria, $\nu > 2$ os graus de
liberdade, e $a$, $b$, $c$ sao constantes de normalizacao.

!!! tip "Interpretacao de $\lambda$"
    - $\lambda = 0$: distribuicao simetrica (Student-$t$ padrao)
    - $\lambda > 0$: cauda direita mais pesada (assimetria positiva)
    - $\lambda < 0$: cauda esquerda mais pesada (assimetria negativa)

### Construtor

```python
SkewedT(nu=None, lambda_=None)
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `nu` | `float\|None` | `None` | Graus de liberdade (estimado se `None`) |
| `lambda_` | `float\|None` | `None` | Parametro de assimetria (estimado se `None`) |

### Parametros

| Parametro | Restricao | Descricao |
|-----------|-----------|-----------|
| $\nu$ | $> 2$ | Graus de liberdade |
| $\lambda$ | $(-1, 1)$ | Assimetria |

### Exemplo

```python
from archbox.distributions import SkewedT
import numpy as np

# Ambos parametros estimados
dist = SkewedT()
print(f"Parametros: {dist.num_params}")  # 2
print(f"Nomes: {dist.param_names}")      # ['nu', 'lambda']

# Quantis assimetricos
dist_skew = SkewedT(nu=5, lambda_=-0.3)
q_left = dist_skew.ppf(0.05)
q_right = dist_skew.ppf(0.95)
print(f"Quantil 5%: {q_left:.4f}")
print(f"Quantil 95%: {q_right:.4f}")
# |q_left| > |q_right| devido a assimetria negativa
```

---

## GeneralizedError (GED)

::: archbox.distributions.ged.GeneralizedError
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - loglikelihood
        - ppf
        - cdf
        - simulate

### Especificacao

Distribuicao de Erro Generalizado:

$$
f(z; p) = \frac{p}{2 \lambda \Gamma(1/p)} \exp\left(-\left|\frac{z}{\lambda}\right|^p\right)
$$

onde $\lambda = \left[\frac{2^{-2/p} \Gamma(1/p)}{\Gamma(3/p)}\right]^{1/2}$
e uma constante de padronizacao e $p > 0$ e o parametro de forma.

!!! tip "Casos especiais"
    - $p = 1$: distribuicao de Laplace (caudas mais pesadas)
    - $p = 2$: distribuicao Normal
    - $p > 2$: caudas mais leves que a Normal

### Construtor

```python
GeneralizedError(p=None)
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `p` | `float\|None` | `None` | Parametro de forma (estimado se `None`) |

### Parametros

| Parametro | Restricao | Descricao |
|-----------|-----------|-----------|
| $p$ | $> 0$ | Parametro de forma |

### Exemplo

```python
from archbox.distributions import GeneralizedError
import numpy as np

# p estimado
dist = GeneralizedError()
print(f"Parametros: {dist.num_params}")  # 1

# p fixo
dist_laplace = GeneralizedError(p=1.0)
dist_normal = GeneralizedError(p=2.0)

# Comparar quantis
print(f"VaR 95% (GED p=1): {dist_laplace.ppf(0.05):.4f}")
print(f"VaR 95% (GED p=2): {dist_normal.ppf(0.05):.4f}")
```

---

## MixtureNormal

::: archbox.distributions.mixture_normal.MixtureNormal
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - loglikelihood
        - ppf
        - cdf
        - simulate

### Especificacao

Mistura de duas distribuicoes Normais:

$$
f(z; w, \sigma^2_2) = w \cdot \phi(z) + (1 - w) \cdot \frac{1}{\sigma_2} \phi\left(\frac{z}{\sigma_2}\right)
$$

onde $w \in (0, 1)$ e o peso da primeira componente e $\sigma^2_2$
e a variancia da segunda componente (a primeira tem $\sigma^2_1 = 1$).

!!! note "Padronizacao"
    A mistura e padronizada para ter variancia unitaria:
    $w + (1 - w)\sigma^2_2 = 1$.

### Construtor

```python
MixtureNormal(w=None, sigma2=None)
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `w` | `float\|None` | `None` | Peso da 1a componente (estimado se `None`) |
| `sigma2` | `float\|None` | `None` | Variancia da 2a componente (estimado se `None`) |

### Parametros

| Parametro | Restricao | Descricao |
|-----------|-----------|-----------|
| $w$ | $(0, 1)$ | Peso da 1a componente |
| $\sigma^2_2$ | $> 0$ | Variancia da 2a componente |

### Exemplo

```python
from archbox.distributions import MixtureNormal
import numpy as np

dist = MixtureNormal()
print(f"Parametros: {dist.num_params}")  # 2

# Mistura com componente de alta variancia
dist_mix = MixtureNormal(w=0.9, sigma2=4.0)

rng = np.random.default_rng(42)
samples = dist_mix.simulate(10000, rng)
print(f"Curtose: {float(np.mean(samples**4) / np.mean(samples**2)**2):.2f}")
# Curtose > 3 (caudas pesadas)
```

---

## Uso com Modelos GARCH

As distribuicoes sao integradas automaticamente na estimacao dos modelos:

=== "Normal (default)"

    ```python
    from archbox.models import GARCH

    model = GARCH(returns, p=1, q=1, dist='normal')
    result = model.fit(disp=False)
    ```

=== "Student-t"

    ```python
    from archbox.models import GARCH

    model = GARCH(returns, p=1, q=1, dist='student-t')
    result = model.fit(disp=False)
    # nu estimado automaticamente
    ```

=== "Skewed-t"

    ```python
    from archbox.models import GARCH

    model = GARCH(returns, p=1, q=1, dist='skewed-t')
    result = model.fit(disp=False)
    # nu e lambda estimados automaticamente
    ```

=== "GED"

    ```python
    from archbox.models import GARCH

    model = GARCH(returns, p=1, q=1, dist='ged')
    result = model.fit(disp=False)
    ```

---

## Comparacao de Distribuicoes

```python
from archbox.distributions import Normal, StudentT, SkewedT, GeneralizedError
import numpy as np

dists = {
    'Normal': Normal(),
    'Student-t(5)': StudentT(nu=5),
    'Skewed-t(5, -0.3)': SkewedT(nu=5, lambda_=-0.3),
    'GED(1.5)': GeneralizedError(p=1.5),
}

print(f"{'Distribuicao':<25} {'VaR 1%':>10} {'VaR 5%':>10} {'ES 5%':>10}")
print("-" * 60)
for name, dist in dists.items():
    var1 = dist.ppf(0.01)
    var5 = dist.ppf(0.05)
    print(f"{name:<25} {var1:>10.4f} {var5:>10.4f}")
```

---

## Selecao de Distribuicao

!!! tip "Criterios de selecao"
    Use AIC/BIC para comparar modelos com diferentes distribuicoes:

    ```python
    from archbox.models import GARCH

    for dist_name in ['normal', 'student-t', 'skewed-t', 'ged']:
        model = GARCH(returns, p=1, q=1, dist=dist_name)
        result = model.fit(disp=False)
        print(f"{dist_name:<12} AIC={result.aic:.2f}  BIC={result.bic:.2f}")
    ```

---

## Referencias

- Bollerslev, T. & Wooldridge, J.M. (1992). Quasi-Maximum Likelihood
  Estimation and Inference in Dynamic Models with Time-Varying
  Covariances. *Econometric Reviews*, 11(2), 143-172.
- Hansen, B.E. (1994). Autoregressive Conditional Density Estimation.
  *International Economic Review*, 35(3), 705-730.
- Nelson, D.B. (1991). Conditional Heteroskedasticity in Asset Returns:
  A New Approach. *Econometrica*, 59(2), 347-370.

---

## Ver Tambem

- [Core](core.md) -- `VolatilityModel` com parametro `dist`
- [GARCH](garch.md) -- Modelos que utilizam as distribuicoes
- [Risk](risk.md) -- VaR e ES com diferentes distribuicoes
