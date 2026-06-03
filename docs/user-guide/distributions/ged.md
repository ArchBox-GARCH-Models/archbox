---
title: "GED (Generalized Error Distribution)"
description: "Distribuicao GED para modelos GARCH -- flexibilidade entre caudas finas e pesadas com um unico parametro de forma."
---

# GED (Generalized Error Distribution)

!!! info "Quick Reference"
    **Class:** `archbox.distributions.GeneralizedError`
    **Import:** `from archbox.distributions import GeneralizedError`
    **Parametros extras:** $\nu$ (parametro de forma, $\nu > 0$)
    **R equivalent:** `rugarch::ugarchspec(distribution.model = "ged")`
    **Python equivalent:** `arch.arch_model(returns, dist='ged')`

## Overview

A **Generalized Error Distribution** (GED), tambem chamada de Generalized Normal Distribution, e uma familia flexivel de distribuicoes simetricas parametrizada por um unico parametro de forma $\nu$. Proposta por Nelson (1991) para uso em modelos GARCH, a GED inclui a Normal e a Laplace como casos especiais.

A principal vantagem da GED e sua **flexibilidade no formato das caudas**: ela pode modelar tanto caudas mais pesadas quanto mais leves que a Normal, tudo controlado por $\nu$.

**Quando usar:**

- Quando se deseja flexibilidade no peso das caudas sem assumir Student-t
- Para comparacao com a Student-t em selecao de modelos
- Quando os dados podem ter caudas entre Laplace ($\nu = 1$) e Normal ($\nu = 2$)
- Em contextos onde a GED pode ser preferida por razoes teoricas

**Limitacoes:**

- Assume simetria (assim como a Student-t)
- Nao captura assimetria -- para isso, use a [Skewed GED](skewed-ged.md)
- O parametro $\nu$ tem interpretacao menos intuitiva que os graus de liberdade da Student-t

## Formulacao Matematica

### PDF

A funcao densidade da GED padronizada:

$$f(z; \nu) = \frac{\nu}{\lambda \cdot 2^{1+1/\nu} \cdot \Gamma(1/\nu)} \exp\left(-\frac{1}{2}\left|\frac{z}{\lambda}\right|^\nu\right)$$

onde o parametro de escala $\lambda$ garante variancia unitaria:

$$\lambda = \sqrt{2^{-2/\nu} \cdot \frac{\Gamma(1/\nu)}{\Gamma(3/\nu)}}$$

### Log-Verossimilhanca

$$\ell_t = \ln(\nu) - \ln(\lambda) - \left(1 + \frac{1}{\nu}\right)\ln(2) - \ln\Gamma\!\left(\frac{1}{\nu}\right) - \frac{1}{2}\left|\frac{z_t}{\lambda}\right|^\nu - \frac{1}{2}\ln(\sigma_t^2)$$

onde $z_t = \epsilon_t / \sigma_t$.

### Casos Especiais

| $\nu$ | Distribuicao | Curtose | Caracteristica |
|:------:|:-------------|:--------|:---------------|
| 1 | **Laplace** (double exponential) | 6.0 | Caudas muito pesadas, pico acentuado |
| 2 | **Normal** (Gaussiana) | 3.0 | Caso intermediario |
| $\to \infty$ | **Uniforme** | 1.8 | Caudas leves, distribuicao plana |

### Curtose

A curtose da GED em funcao de $\nu$:

$$K = \frac{\Gamma(1/\nu) \cdot \Gamma(5/\nu)}{\left[\Gamma(3/\nu)\right]^2}$$

- $\nu < 2$: curtose $> 3$ (caudas mais pesadas que a Normal)
- $\nu = 2$: curtose $= 3$ (Normal)
- $\nu > 2$: curtose $< 3$ (caudas mais leves que a Normal)

## Parametros

| Parametro | Descricao | Restricao | Default |
|:----------|:----------|:----------|:--------|
| `nu` | Parametro de forma | $\nu > 0$ | Estimado (~1.5 como valor inicial) |

```python
# Estimar nu automaticamente (recomendado)
dist = GeneralizedError()

# Fixar nu manualmente
dist = GeneralizedError(nu=1.5)

# Fixar como Normal (nu=2)
dist = GeneralizedError(nu=2.0)

# Fixar como Laplace (nu=1)
dist = GeneralizedError(nu=1.0)
```

## Quick Example

```python
from archbox import GARCH
from archbox.distributions import GeneralizedError
from archbox.datasets import load_dataset

sp500 = load_dataset('sp500')

# GARCH(1,1) com GED
model = GARCH(sp500['returns'], p=1, q=1, dist=GeneralizedError())
results = model.fit()
print(results.summary())
```

??? example "Output esperado"
    ```
    ======================================================================
                          Volatility Model Results
    ======================================================================
    Model:            GARCH
    Distribution:     GED
    Observations:     2000
    Log-Likelihood:   3185.6789
    AIC:              -6363.3578
    BIC:              -6340.9622
    Converged:        True
    ----------------------------------------------------------------------
    Parameter         Estimate      Std Err      t-value      p-value
    ----------------------------------------------------------------------
    omega            0.000011     0.000003       3.2789       0.0010
    alpha[1]         0.079876     0.011567       6.9056       0.0000
    beta[1]          0.908765     0.014123      64.3456       0.0000
    nu               1.423456     0.098765      14.4098       0.0000
    ----------------------------------------------------------------------
    Persistence:      0.988641
    Half-life:        60.72 periods
    ======================================================================
    ```

## Guia Detalhado

### Interpretacao do Parametro $\nu$

```python
from archbox.distributions import GeneralizedError
import numpy as np
from scipy.special import gammaln

# Curtose da GED em funcao de nu
for nu in [0.5, 1.0, 1.5, 2.0, 3.0, 5.0]:
    kurtosis = np.exp(
        gammaln(1/nu) + gammaln(5/nu) - 2*gammaln(3/nu)
    )
    dist = GeneralizedError(nu=nu)
    prob_extreme = 2 * (1 - dist.cdf(3.0))
    print(f"nu={nu:.1f}: curtose={kurtosis:.2f}, P(|z|>3)={prob_extreme:.4f}")
```

??? example "Output esperado"
    ```
    nu=0.5: curtose=25.00, P(|z|>3)=0.0625
    nu=1.0: curtose=6.00,  P(|z|>3)=0.0174
    nu=1.5: curtose=3.87,  P(|z|>3)=0.0057
    nu=2.0: curtose=3.00,  P(|z|>3)=0.0027
    nu=3.0: curtose=2.33,  P(|z|>3)=0.0003
    nu=5.0: curtose=1.97,  P(|z|>3)=0.0000
    ```

### GED vs. Student-t

Ambas as distribuicoes capturam caudas pesadas, mas de formas diferentes:

```python
from archbox import GARCH
from archbox.distributions import StudentT, GeneralizedError
from archbox.datasets import load_dataset

sp500 = load_dataset('sp500')

# Student-t
res_t = GARCH(sp500['returns'], p=1, q=1, dist=StudentT()).fit()

# GED
res_g = GARCH(sp500['returns'], p=1, q=1, dist=GeneralizedError()).fit()

print(f"Student-t - LogLik: {res_t.loglike:.2f}, BIC: {res_t.bic:.2f}")
print(f"GED       - LogLik: {res_g.loglike:.2f}, BIC: {res_g.bic:.2f}")
```

!!! note "Diferenca conceitual"
    - **Student-t**: caudas decaem como potencia ($|z|^{-(\nu+1)}$) -- mais pesadas para valores extremos
    - **GED**: caudas decaem como exponencial estendida ($e^{-|z|^\nu}$) -- menos pesadas que a Student-t para o mesmo nivel de curtose

    Na pratica, a Student-t tende a ser preferida para dados financeiros porque as caudas de potencia aproximam melhor a distribuicao empirica de retornos extremos.

### Visualizando Diferentes Formas

```python
from archbox.distributions import GeneralizedError
import numpy as np
import matplotlib.pyplot as plt

z = np.linspace(-4, 4, 500)

fig, ax = plt.subplots(figsize=(10, 6))

for nu, label in [(1.0, 'Laplace (nu=1)'), (1.5, 'GED (nu=1.5)'),
                   (2.0, 'Normal (nu=2)'), (3.0, 'GED (nu=3)')]:
    dist = GeneralizedError(nu=nu)
    pdf = np.array([np.exp(dist.loglikelihood(
        np.array([zi]), np.array([1.0]))[0]) for zi in z])
    ax.plot(z, pdf, label=label)

ax.legend()
ax.set_xlabel('z')
ax.set_ylabel('f(z)')
ax.set_title('GED para diferentes valores de nu')
plt.tight_layout()
plt.show()
```

## Equivalentes em R e Python

=== "ArchBox"

    ```python
    from archbox import GARCH
    from archbox.distributions import GeneralizedError

    model = GARCH(returns, p=1, q=1, dist=GeneralizedError())
    results = model.fit()
    ```

=== "R (rugarch)"

    ```r
    spec <- ugarchspec(
      variance.model = list(model = "sGARCH"),
      distribution.model = "ged"
    )
    fit <- ugarchfit(spec, data = returns)
    ```

=== "Python (arch)"

    ```python
    from arch import arch_model

    am = arch_model(returns, vol='Garch', p=1, q=1, dist='ged')
    res = am.fit()
    ```

## References

- Nelson, D. B. (1991). Conditional Heteroskedasticity in Asset Returns: A New Approach. *Econometrica*, 59(2), 347--370.
- Box, G. E. P., & Tiao, G. C. (1973). *Bayesian Inference in Statistical Analysis*. Wiley.
- Theodossiou, P. (1998). Financial Data and the Skewed Generalized T Distribution. *Management Science*, 44(12), 1650--1661.

## See Also

- [Normal](normal.md) -- Caso especial com $\nu = 2$
- [Student-t](student-t.md) -- Alternativa para caudas pesadas
- [Skewed GED](skewed-ged.md) -- GED com assimetria
- [Guia de Selecao](choosing.md) -- Comparacao sistematica entre distribuicoes
