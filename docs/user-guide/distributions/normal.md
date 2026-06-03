---
title: "Normal (Gaussiana)"
description: "Distribuicao Normal condicional para modelos GARCH -- baseline para comparacao com distribuicoes de caudas pesadas."
---

# Normal (Gaussiana)

!!! info "Quick Reference"
    **Class:** `archbox.distributions.Normal`
    **Import:** `from archbox.distributions import Normal`
    **Parametros extras:** Nenhum
    **R equivalent:** `rugarch::ugarchspec(distribution.model = "norm")`
    **Python equivalent:** `arch.arch_model(returns, dist='Normal')`

## Overview

A distribuicao **Normal** (Gaussiana) e a escolha padrao e o ponto de partida para qualquer modelagem GARCH. Com media zero e variancia unitaria para as inovacoes padronizadas $z_t$, ela assume que os retornos (condicionados a volatilidade) seguem uma distribuicao simetrica com caudas exponencialmente decrescentes.

**Quando usar:**

- Como **baseline** para comparacao com outras distribuicoes
- Quando os residuos padronizados nao apresentam excesso de curtose significativo
- Para estimacao inicial rapida (menos parametros = convergencia mais facil)
- Quando o foco e a dinamica da volatilidade e nao a forma distribucional

**Limitacoes:**

- Subestima a probabilidade de eventos extremos (caudas leves)
- Assume simetria perfeita (sem assimetria)
- VaR e ES calculados com Normal sao excessivamente otimistas
- Curtose fixa em 3 (retornos financeiros tipicamente tem curtose > 3)

## Formulacao Matematica

### PDF

A funcao densidade de probabilidade da Normal padrao:

$$f(z) = \frac{1}{\sqrt{2\pi}} \exp\left(-\frac{z^2}{2}\right)$$

### Log-Verossimilhanca

Para o modelo GARCH com distribuicao Normal, a log-verossimilhanca por observacao e:

$$\ell_t = -\frac{1}{2} \left[ \ln(2\pi) + \ln(\sigma_t^2) + \frac{\epsilon_t^2}{\sigma_t^2} \right]$$

onde $\epsilon_t = r_t - \mu$ sao os residuos e $\sigma_t^2$ e a variancia condicional.

### Propriedades

| Propriedade | Valor |
|:------------|:------|
| Media | $E[z] = 0$ |
| Variancia | $\text{Var}(z) = 1$ |
| Assimetria | $S = 0$ |
| Curtose | $K = 3$ |
| Excesso de curtose | $K - 3 = 0$ |

## Quick Example

```python
from archbox import GARCH
from archbox.distributions import Normal
from archbox.datasets import load_dataset

sp500 = load_dataset('sp500')

# GARCH(1,1) com distribuicao Normal (default)
model = GARCH(sp500['returns'], p=1, q=1, dist=Normal())
results = model.fit()
print(results.summary())
```

??? example "Output esperado"
    ```
    ======================================================================
                          Volatility Model Results
    ======================================================================
    Model:            GARCH
    Distribution:     Normal
    Observations:     2000
    Log-Likelihood:   3125.4567
    AIC:              -6244.9134
    BIC:              -6228.1256
    Converged:        True
    ----------------------------------------------------------------------
    Parameter         Estimate      Std Err      t-value      p-value
    ----------------------------------------------------------------------
    omega            0.000012     0.000004       3.1245       0.0018
    alpha[1]         0.085432     0.012345       6.9205       0.0000
    beta[1]          0.901234     0.015678      57.4821       0.0000
    ----------------------------------------------------------------------
    Persistence:      0.986666
    Half-life:        51.63 periods
    ======================================================================
    ```

## Guia Detalhado

### Usando como Distribuicao Default

A Normal e a distribuicao padrao -- se voce nao especificar `dist`, o ArchBox usa `Normal()`:

```python
from archbox import GARCH
from archbox.datasets import load_dataset

sp500 = load_dataset('sp500')

# Estas duas chamadas sao equivalentes
model1 = GARCH(sp500['returns'], p=1, q=1)
model2 = GARCH(sp500['returns'], p=1, q=1, dist=Normal())
```

### Verificando Adequacao com QQ-Plot

O QQ-plot e o diagnostico visual mais importante para avaliar se a Normal e adequada:

```python
from archbox import GARCH
from archbox.distributions import Normal
from archbox.datasets import load_dataset
import matplotlib.pyplot as plt
from scipy import stats

sp500 = load_dataset('sp500')
model = GARCH(sp500['returns'], p=1, q=1, dist=Normal())
results = model.fit()

# QQ-plot dos residuos padronizados
fig, ax = plt.subplots(figsize=(6, 6))
stats.probplot(results.resid, dist="norm", plot=ax)
ax.set_title("QQ-Plot: Residuos vs. Normal")
plt.tight_layout()
plt.show()
```

!!! tip "Interpretacao"
    Se as caudas do QQ-plot desviam da diagonal (formato "S"), os dados tem caudas mais pesadas que a Normal. Considere usar [Student-t](student-t.md) ou [Skewed-t](skewed-t.md).

### Teste de Normalidade nos Residuos

```python
from scipy import stats

# Jarque-Bera test
jb_stat, jb_pval = stats.jarque_bera(results.resid)
print(f"Jarque-Bera: {jb_stat:.4f}, p-valor: {jb_pval:.4f}")

# Curtose e assimetria
print(f"Curtose: {stats.kurtosis(results.resid, fisher=False):.4f}")
print(f"Assimetria: {stats.skew(results.resid):.4f}")
```

!!! note "Na pratica"
    Para a maioria das series financeiras diarias, o teste Jarque-Bera rejeitara a normalidade dos residuos padronizados. Isso nao invalida o modelo GARCH -- apenas indica que uma distribuicao de caudas pesadas pode melhorar o ajuste.

### Comparando Normal vs. Student-t

```python
from archbox import GARCH
from archbox.distributions import Normal, StudentT
from archbox.datasets import load_dataset

sp500 = load_dataset('sp500')

# Normal
res_n = GARCH(sp500['returns'], p=1, q=1, dist=Normal()).fit()

# Student-t
res_t = GARCH(sp500['returns'], p=1, q=1, dist=StudentT()).fit()

print(f"Normal  - LogLik: {res_n.loglike:.2f}, BIC: {res_n.bic:.2f}")
print(f"Student - LogLik: {res_t.loglike:.2f}, BIC: {res_t.bic:.2f}")
```

## Equivalentes em R e Python

=== "ArchBox"

    ```python
    from archbox import GARCH
    from archbox.distributions import Normal

    model = GARCH(returns, p=1, q=1, dist=Normal())
    results = model.fit()
    ```

=== "R (rugarch)"

    ```r
    spec <- ugarchspec(
      variance.model = list(model = "sGARCH"),
      distribution.model = "norm"
    )
    fit <- ugarchfit(spec, data = returns)
    ```

=== "Python (arch)"

    ```python
    from arch import arch_model

    am = arch_model(returns, vol='Garch', p=1, q=1, dist='Normal')
    res = am.fit()
    ```

## References

- Bollerslev, T. (1986). Generalized Autoregressive Conditional Heteroskedasticity. *Journal of Econometrics*, 31(3), 307--327.
- Engle, R. F. (1982). Autoregressive Conditional Heteroscedasticity with Estimates of the Variance of United Kingdom Inflation. *Econometrica*, 50(4), 987--1007.

## See Also

- [Student-t](student-t.md) -- Caudas pesadas simetricas quando a Normal nao e suficiente
- [Skewed-t](skewed-t.md) -- Caudas pesadas com assimetria
- [Guia de Selecao](choosing.md) -- Como comparar distribuicoes sistematicamente
- [GARCH(p,q)](../garch/garch.md) -- Modelo base de volatilidade condicional
