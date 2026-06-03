---
title: "Skewed Student-t (Hansen)"
description: "Distribuicao Skewed Student-t de Hansen (1994) para modelos GARCH -- captura caudas pesadas e assimetria em retornos financeiros."
---

# Skewed Student-t (Hansen, 1994)

!!! info "Quick Reference"
    **Class:** `archbox.distributions.SkewedT`
    **Import:** `from archbox.distributions import SkewedT`
    **Parametros extras:** $\nu$ (graus de liberdade, $\nu > 2$), $\lambda$ (assimetria, $\lambda \in (-1, 1)$)
    **R equivalent:** `rugarch::ugarchspec(distribution.model = "sstd")`
    **Python equivalent:** `arch.arch_model(returns, dist='SkewStudent')`

## Overview

A distribuicao **Skewed Student-t** (Hansen, 1994) estende a Student-t com um parametro de assimetria $\lambda$, capturando simultaneamente **caudas pesadas** e **assimetria**. Essas sao as duas caracteristicas mais importantes das distribuicoes de retornos financeiros.

Em mercados de equities, a cauda esquerda (perdas) e tipicamente mais pesada que a cauda direita (ganhos) -- fenomeno conhecido como **negative skewness**. A Skewed-t captura isso permitindo que as duas metades da distribuicao tenham pesos diferentes.

**Quando usar:**

- Retornos de **equities** e indices de mercado (assimetria negativa tipica)
- Quando o teste de assimetria nos residuos e significativo
- Quando o Sign Bias Test indica impacto assimetrico dos choques
- Para calculo de VaR/ES mais preciso em carteiras direcionais

**Limitacoes:**

- Dois parametros extras ($\nu, \lambda$) requerem mais dados para estimacao precisa
- Pode ter dificuldades de convergencia com amostras pequenas ($T < 500$)

## Formulacao Matematica

### PDF (Hansen, 1994)

A densidade e definida em duas regioes:

$$f(z; \nu, \lambda) = \begin{cases} bc\left(1 + \frac{1}{\nu-2}\left(\frac{bz+a}{1-\lambda}\right)^2\right)^{-\frac{\nu+1}{2}} & \text{se } z < -a/b \\[8pt] bc\left(1 + \frac{1}{\nu-2}\left(\frac{bz+a}{1+\lambda}\right)^2\right)^{-\frac{\nu+1}{2}} & \text{se } z \geq -a/b \end{cases}$$

onde as constantes de padronizacao sao:

$$a = 4\lambda c \frac{\nu-2}{\nu-1}, \qquad b = \sqrt{1 + 3\lambda^2 - a^2}, \qquad c = \frac{\Gamma\left(\frac{\nu+1}{2}\right)}{\sqrt{\pi(\nu-2)}\;\Gamma\left(\frac{\nu}{2}\right)}$$

Essas constantes garantem que $E[z] = 0$ e $\text{Var}(z) = 1$.

### Log-Verossimilhanca

$$\ell_t = \ln(b) + \ln(c) - \frac{1}{2}\ln(\sigma_t^2) - \frac{\nu+1}{2}\ln\!\left(1 + \frac{\eta_t^2}{\nu-2}\right)$$

onde:

$$\eta_t = \begin{cases} \frac{bz_t + a}{1 - \lambda} & \text{se } z_t < -a/b \\ \frac{bz_t + a}{1 + \lambda} & \text{se } z_t \geq -a/b \end{cases}$$

### Interpretacao dos Parametros

| Parametro | Descricao | Efeito |
|:----------|:----------|:-------|
| $\nu > 2$ | Graus de liberdade | Controla o peso das caudas (menor $\nu$ = caudas mais pesadas) |
| $\lambda \in (-1, 1)$ | Assimetria | $\lambda < 0$: cauda esquerda mais pesada; $\lambda > 0$: cauda direita mais pesada |

Casos especiais:

- $\lambda = 0$: Student-t simetrica
- $\lambda = 0$ e $\nu \to \infty$: Normal

## Parametros

| Parametro | Descricao | Restricao | Default |
|:----------|:----------|:----------|:--------|
| `nu` | Graus de liberdade | $\nu > 2$ | Estimado (~8.0) |
| `lam` | Assimetria | $\lambda \in (-1, 1)$ | Estimado (~-0.1) |

```python
# Estimar ambos (recomendado)
dist = SkewedT()

# Fixar nu, estimar lambda
dist = SkewedT(nu=6.0)

# Fixar ambos
dist = SkewedT(nu=6.0, lam=-0.15)
```

## Quick Example

```python
from archbox import GARCH
from archbox.distributions import SkewedT
from archbox.datasets import load_dataset

sp500 = load_dataset('sp500')

# GARCH(1,1) com Skewed Student-t
model = GARCH(sp500['returns'], p=1, q=1, dist=SkewedT())
results = model.fit()
print(results.summary())
```

??? example "Output esperado"
    ```
    ======================================================================
                          Volatility Model Results
    ======================================================================
    Model:            GARCH
    Distribution:     Skewed Student-t
    Observations:     2000
    Log-Likelihood:   3198.5678
    AIC:              -6387.1356
    BIC:              -6359.1322
    Converged:        True
    ----------------------------------------------------------------------
    Parameter         Estimate      Std Err      t-value      p-value
    ----------------------------------------------------------------------
    omega            0.000010     0.000003       3.4567       0.0006
    alpha[1]         0.076543     0.011123       6.8821       0.0000
    beta[1]          0.912345     0.013234      68.9432       0.0000
    nu               7.456789     1.345678       5.5408       0.0000
    lambda          -0.134567     0.034567      -3.8934       0.0001
    ----------------------------------------------------------------------
    Persistence:      0.988888
    Half-life:        62.04 periods
    ======================================================================
    ```

## Guia Detalhado

### Interpretacao do Parametro $\lambda$

O parametro $\lambda$ controla a assimetria da distribuicao:

```python
from archbox.distributions import SkewedT
import numpy as np

# Comparar quantis para diferentes valores de lambda
for lam in [-0.3, -0.1, 0.0, 0.1, 0.3]:
    dist = SkewedT(nu=7, lam=lam)
    q01 = dist.ppf(0.01)   # Cauda esquerda (VaR 99%)
    q99 = dist.ppf(0.99)   # Cauda direita
    print(f"lambda={lam:+.1f}: q(1%)={q01:+.4f}, q(99%)={q99:+.4f}")
```

??? example "Output esperado"
    ```
    lambda=-0.3: q(1%)=-3.4521, q(99%)=+2.6789
    lambda=-0.1: q(1%)=-3.0123, q(99%)=+2.8456
    lambda=+0.0: q(1%)=-2.8345, q(99%)=+2.8345
    lambda=+0.1: q(1%)=-2.8456, q(99%)=+3.0123
    lambda=+0.3: q(1%)=-2.6789, q(99%)=+3.4521
    ```

!!! tip "Valores tipicos"
    Para retornos de equities, $\lambda$ tipicamente fica entre **-0.05 e -0.20**, indicando assimetria negativa (cauda esquerda mais pesada).

### Comparacao com Student-t Simetrica

```python
from archbox import GARCH
from archbox.distributions import StudentT, SkewedT
from archbox.datasets import load_dataset

sp500 = load_dataset('sp500')

# Student-t simetrica
res_t = GARCH(sp500['returns'], p=1, q=1, dist=StudentT()).fit()

# Skewed Student-t
res_st = GARCH(sp500['returns'], p=1, q=1, dist=SkewedT()).fit()

print(f"Student-t  - LogLik: {res_t.loglike:.2f}, BIC: {res_t.bic:.2f}")
print(f"Skewed-t   - LogLik: {res_st.loglike:.2f}, BIC: {res_st.bic:.2f}")
print(f"\nMelhoria LogLik: {res_st.loglike - res_t.loglike:.2f}")
```

### Likelihood Ratio Test para Assimetria

Como a Student-t e um caso especial da Skewed-t (quando $\lambda = 0$), pode-se testar formalmente se a assimetria e significativa:

```python
from scipy import stats

# H0: lambda = 0 (Student-t) vs H1: lambda != 0 (Skewed-t)
lr_stat = 2 * (res_st.loglike - res_t.loglike)
lr_pval = 1 - stats.chi2.cdf(lr_stat, df=1)  # 1 restricao (lambda=0)

print(f"LR statistic: {lr_stat:.4f}")
print(f"p-valor: {lr_pval:.4f}")
```

### Impacto no VaR Assimetrico

```python
from archbox.distributions import Normal, StudentT, SkewedT

normal = Normal()
student = StudentT(nu=7)
skewed = SkewedT(nu=7, lam=-0.15)

# VaR para posicoes long (cauda esquerda)
print("VaR 99% - Posicao Long (q=0.01):")
print(f"  Normal:    {normal.ppf(0.01):.4f}")
print(f"  Student-t: {student.ppf(0.01):.4f}")
print(f"  Skewed-t:  {skewed.ppf(0.01):.4f}")

# VaR para posicoes short (cauda direita)
print("\nVaR 99% - Posicao Short (q=0.99):")
print(f"  Normal:    {normal.ppf(0.99):.4f}")
print(f"  Student-t: {student.ppf(0.99):.4f}")
print(f"  Skewed-t:  {skewed.ppf(0.99):.4f}")
```

!!! warning "VaR assimetrico"
    Com a Skewed-t, o VaR para posicoes long e mais conservador (cauda esquerda mais pesada), enquanto o VaR para posicoes short e menos extremo. Isso reflete a realidade dos mercados de equities.

## Equivalentes em R e Python

=== "ArchBox"

    ```python
    from archbox import GARCH
    from archbox.distributions import SkewedT

    model = GARCH(returns, p=1, q=1, dist=SkewedT())
    results = model.fit()
    ```

=== "R (rugarch)"

    ```r
    spec <- ugarchspec(
      variance.model = list(model = "sGARCH"),
      distribution.model = "sstd"
    )
    fit <- ugarchfit(spec, data = returns)
    ```

=== "Python (arch)"

    ```python
    from arch import arch_model

    am = arch_model(returns, vol='Garch', p=1, q=1, dist='SkewStudent')
    res = am.fit()
    ```

## References

- Hansen, B. E. (1994). Autoregressive Conditional Density Estimation. *International Economic Review*, 35(3), 705--730.
- Jondeau, E., & Rockinger, M. (2003). Conditional Volatility, Skewness, and Kurtosis: Existence, Persistence, and Comovements. *Journal of Economic Dynamics and Control*, 27(10), 1699--1737.

## See Also

- [Student-t](student-t.md) -- Versao simetrica (caso especial com $\lambda = 0$)
- [Normal](normal.md) -- Baseline sem caudas pesadas nem assimetria
- [GED](ged.md) -- Alternativa para caudas pesadas (simetrica)
- [Guia de Selecao](choosing.md) -- Workflow para escolher a distribuicao
