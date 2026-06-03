---
title: "Student-t"
description: "Distribuicao Student-t condicional para modelos GARCH -- captura caudas pesadas simetricas em retornos financeiros."
---

# Student-t

!!! info "Quick Reference"
    **Class:** `archbox.distributions.StudentT`
    **Import:** `from archbox.distributions import StudentT`
    **Parametros extras:** $\nu$ (graus de liberdade, $\nu > 2$)
    **R equivalent:** `rugarch::ugarchspec(distribution.model = "std")`
    **Python equivalent:** `arch.arch_model(returns, dist='StudentsT')`

## Overview

A distribuicao **Student-t** (Bollerslev, 1987) e a extensao mais natural da Normal para capturar **caudas pesadas** em retornos financeiros. Com apenas um parametro adicional -- os graus de liberdade $\nu$ -- ela permite modelar o excesso de curtose tipicamente observado em series financeiras.

A intuicao e simples: retornos financeiros tem mais observacoes extremas do que a Normal preve. A Student-t acomoda isso com caudas que decaem como potencia (polynomially) em vez de exponencialmente, atribuindo maior probabilidade a eventos extremos.

**Quando usar:**

- Retornos financeiros com **caudas pesadas simetricas**
- Quando o QQ-plot contra a Normal mostra desvios nas caudas (formato "S")
- Quando o teste de Jarque-Bera rejeita normalidade dos residuos
- Como passo intermediario antes de testar distribuicoes assimetricas

**Limitacoes:**

- Assume simetria: caudas esquerda e direita sao identicas
- Nao captura a assimetria tipica de retornos de equities (crashes > rallies)
- Para capturar assimetria, use a [Skewed Student-t](skewed-t.md)

## Formulacao Matematica

### PDF

A funcao densidade da Student-t padronizada (media zero, variancia unitaria):

$$f(z; \nu) = \frac{\Gamma\left(\frac{\nu+1}{2}\right)}{\sqrt{\pi(\nu-2)}\;\Gamma\left(\frac{\nu}{2}\right)} \left(1 + \frac{z^2}{\nu-2}\right)^{-\frac{\nu+1}{2}}$$

onde $\nu > 2$ sao os graus de liberdade e $\Gamma(\cdot)$ e a funcao Gamma.

!!! note "Padronizacao"
    A distribuicao e padronizada para ter variancia unitaria dividindo por $\sqrt{\nu/(\nu-2)}$. Isso garante que $E[z_t] = 0$ e $\text{Var}(z_t) = 1$, compativel com a estrutura do modelo GARCH.

### Log-Verossimilhanca

$$\ell_t = \ln\Gamma\!\left(\frac{\nu+1}{2}\right) - \ln\Gamma\!\left(\frac{\nu}{2}\right) - \frac{1}{2}\ln\left[\pi(\nu-2)\right] - \frac{1}{2}\ln(\sigma_t^2) - \frac{\nu+1}{2}\ln\!\left(1 + \frac{z_t^2}{\nu-2}\right)$$

onde $z_t = \epsilon_t / \sigma_t$ sao os residuos padronizados.

### Curtose

A curtose da Student-t em funcao de $\nu$:

$$K = \frac{3(\nu - 2)}{\nu - 4}, \qquad \nu > 4$$

| $\nu$ | Curtose | Interpretacao |
|:------:|:-------:|:--------------|
| 4.1 | 63.0 | Caudas extremamente pesadas |
| 5 | 9.0 | Caudas muito pesadas |
| 8 | 4.5 | Caudas moderadamente pesadas |
| 15 | 3.55 | Caudas levemente pesadas |
| 30 | 3.23 | Proximo da Normal |
| $\infty$ | 3.0 | Normal |

### Convergencia para a Normal

Quando $\nu \to \infty$, a Student-t converge para a Normal:

$$\lim_{\nu \to \infty} f(z; \nu) = \frac{1}{\sqrt{2\pi}} \exp\left(-\frac{z^2}{2}\right)$$

Na pratica, $\nu > 30$ produz resultados praticamente identicos a Normal.

## Parametros

| Parametro | Descricao | Restricao | Default |
|:----------|:----------|:----------|:--------|
| `nu` | Graus de liberdade | $\nu > 2$ | Estimado via MLE (~8.0 como valor inicial) |

```python
# Estimar nu automaticamente (recomendado)
dist = StudentT()

# Fixar nu manualmente
dist = StudentT(nu=5.0)
```

## Quick Example

```python
from archbox import GARCH
from archbox.distributions import StudentT
from archbox.datasets import load_dataset

sp500 = load_dataset('sp500')

# GARCH(1,1) com Student-t
model = GARCH(sp500['returns'], p=1, q=1, dist=StudentT())
results = model.fit()
print(results.summary())
```

??? example "Output esperado"
    ```
    ======================================================================
                          Volatility Model Results
    ======================================================================
    Model:            GARCH
    Distribution:     Student-t
    Observations:     2000
    Log-Likelihood:   3189.2345
    AIC:              -6370.4690
    BIC:              -6348.0734
    Converged:        True
    ----------------------------------------------------------------------
    Parameter         Estimate      Std Err      t-value      p-value
    ----------------------------------------------------------------------
    omega            0.000010     0.000003       3.3456       0.0008
    alpha[1]         0.078123     0.011234       6.9543       0.0000
    beta[1]          0.910456     0.013456      67.6543       0.0000
    nu               7.234500     1.234567       5.8601       0.0000
    ----------------------------------------------------------------------
    Persistence:      0.988579
    Half-life:        60.38 periods
    ======================================================================
    ```

## Guia Detalhado

### Interpretacao do Parametro $\nu$

O parametro $\nu$ controla o peso das caudas:

```python
from archbox.distributions import StudentT
import numpy as np

# Visualizar o efeito de nu
for nu in [4, 6, 8, 15, 30]:
    dist = StudentT(nu=nu)
    # Probabilidade de |z| > 3 (evento extremo)
    prob_extreme = 2 * (1 - dist.cdf(3.0))
    print(f"nu={nu:2d}: P(|z|>3) = {prob_extreme:.4f}")
```

??? example "Output esperado"
    ```
    nu= 4: P(|z|>3) = 0.0284
    nu= 6: P(|z|>3) = 0.0120
    nu= 8: P(|z|>3) = 0.0072
    nu=15: P(|z|>3) = 0.0042
    nu=30: P(|z|>3) = 0.0032
    # Normal:  P(|z|>3) = 0.0027
    ```

!!! tip "Regra pratica"
    - $\nu < 6$: caudas muito pesadas -- comum em mercados emergentes e criptomoedas
    - $6 \leq \nu \leq 10$: tipico para equities de mercados desenvolvidos
    - $\nu > 15$: caudas leves -- a Normal pode ser suficiente

### Fixando vs. Estimando $\nu$

```python
from archbox import GARCH
from archbox.distributions import StudentT
from archbox.datasets import load_dataset

sp500 = load_dataset('sp500')

# Estimar nu via MLE (recomendado)
res_free = GARCH(sp500['returns'], p=1, q=1, dist=StudentT()).fit()

# Fixar nu = 5 (caudas pesadas)
res_fixed = GARCH(sp500['returns'], p=1, q=1, dist=StudentT(nu=5)).fit()

print(f"nu estimado: {res_free.params[-1]:.2f}")
print(f"BIC (livre): {res_free.bic:.2f}")
print(f"BIC (nu=5):  {res_fixed.bic:.2f}")
```

### Impacto no VaR

A escolha da distribuicao tem impacto direto no calculo de risco:

```python
from archbox.distributions import Normal, StudentT
import numpy as np

normal = Normal()
student = StudentT(nu=6)

# VaR 99% (quantil 1%)
var_normal = normal.ppf(0.01)
var_student = student.ppf(0.01)

print(f"VaR 99% (Normal):    z = {var_normal:.4f}")
print(f"VaR 99% (Student-t): z = {var_student:.4f}")
print(f"Diferenca relativa:  {(var_student/var_normal - 1)*100:.1f}%")
```

!!! warning "Subestimacao de risco"
    Com $\nu = 6$, o quantil 1% da Student-t e cerca de 30% mais extremo que o da Normal. Usar a Normal quando os dados tem caudas pesadas leva a subestimacao sistematica do VaR.

## Equivalentes em R e Python

=== "ArchBox"

    ```python
    from archbox import GARCH
    from archbox.distributions import StudentT

    model = GARCH(returns, p=1, q=1, dist=StudentT())
    results = model.fit()
    ```

=== "R (rugarch)"

    ```r
    spec <- ugarchspec(
      variance.model = list(model = "sGARCH"),
      distribution.model = "std"
    )
    fit <- ugarchfit(spec, data = returns)
    ```

=== "Python (arch)"

    ```python
    from arch import arch_model

    am = arch_model(returns, vol='Garch', p=1, q=1, dist='StudentsT')
    res = am.fit()
    ```

## References

- Bollerslev, T. (1987). A Conditionally Heteroskedastic Time Series Model for Speculative Prices and Rates of Return. *Review of Economics and Statistics*, 69(3), 542--547.
- Bollerslev, T. (1986). Generalized Autoregressive Conditional Heteroskedasticity. *Journal of Econometrics*, 31(3), 307--327.
- Fiorentini, G., Sentana, E., & Calzolari, G. (2003). Maximum Likelihood Estimation and Inference in Multivariate Conditionally Heteroscedastic Dynamic Regression Models with Student t Innovations. *Journal of Business & Economic Statistics*, 21(4), 532--546.

## See Also

- [Normal](normal.md) -- Baseline sem caudas pesadas
- [Skewed Student-t](skewed-t.md) -- Student-t com assimetria
- [GED](ged.md) -- Alternativa para caudas pesadas
- [Guia de Selecao](choosing.md) -- Como escolher entre distribuicoes
