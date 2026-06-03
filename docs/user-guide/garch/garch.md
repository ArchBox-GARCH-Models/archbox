---
title: "GARCH(p,q)"
description: "Generalized Autoregressive Conditional Heteroskedasticity model - the standard model for conditional volatility in financial time series."
---

# GARCH(p,q)

!!! info "Quick Reference"
    **Class:** `archbox.models.garch.GARCH`
    **Import:** `from archbox import GARCH`
    **R equivalent:** `rugarch::ugarchspec(variance.model = list(model = "sGARCH", garchOrder = c(1,1)))`
    **Python equivalent:** `arch.arch_model(returns, vol='Garch', p=1, q=1)`

## Overview

O modelo GARCH (Generalized Autoregressive Conditional Heteroskedasticity), proposto por **Bollerslev (1986)**, e a extensao do ARCH de Engle (1982) que se tornou o modelo padrao para volatilidade condicional em financas empiricas. A ideia central e que a variancia dos retornos financeiros nao e constante: ela se agrupa em **clusters de volatilidade** -- periodos de alta volatilidade sao seguidos por periodos de alta volatilidade, e vice-versa.

O GARCH(p,q) modela a variancia condicional $\sigma_t^2$ como funcao dos choques passados ao quadrado ($\epsilon_{t-i}^2$) e das proprias variancias condicionais passadas ($\sigma_{t-j}^2$). Isso captura tres fatos estilizados fundamentais das series financeiras:

- **Clustering de volatilidade**: periodos turbulentos e calmos se agrupam
- **Caudas pesadas**: retornos financeiros tem distribuicao leptocurtica
- **Reversao a media**: a volatilidade tende a retornar ao seu nivel de longo prazo

**Quando usar:**

- Modelar e prever volatilidade de ativos financeiros
- Calcular Value-at-Risk (VaR) e Expected Shortfall (ES)
- Ponderar estimadores por heteroscedasticidade condicional
- Benchmark para comparar com modelos GARCH mais complexos

## Formulacao Matematica

### Equacao da Media

$$r_t = \mu + \epsilon_t, \qquad \epsilon_t = \sigma_t z_t, \qquad z_t \sim D(0, 1)$$

onde $r_t$ sao os retornos, $\mu$ e a media condicional, $\sigma_t$ e o desvio-padrao condicional, e $z_t$ sao inovacoes padronizadas com distribuicao $D(0,1)$ (Normal, Student-t, Skewed-t, GED).

### Equacao da Variancia Condicional

$$\sigma_t^2 = \omega + \sum_{i=1}^{q} \alpha_i \epsilon_{t-i}^2 + \sum_{j=1}^{p} \beta_j \sigma_{t-j}^2$$

onde:

| Parametro | Descricao | Restricao |
|-----------|-----------|-----------|
| $\omega$ | Intercepto (variancia de base) | $\omega > 0$ |
| $\alpha_i$ | Coeficientes ARCH (reacao a choques) | $\alpha_i \geq 0$ |
| $\beta_j$ | Coeficientes GARCH (persistencia) | $\beta_j \geq 0$ |
| $p$ | Ordem GARCH (lags da variancia) | $p \geq 1$ |
| $q$ | Ordem ARCH (lags dos choques) | $q \geq 1$ |

**Condicao de estacionariedade:** $\sum_{i=1}^{q} \alpha_i + \sum_{j=1}^{p} \beta_j < 1$

### Caso Especial: GARCH(1,1)

O caso mais utilizado na pratica:

$$\sigma_t^2 = \omega + \alpha \epsilon_{t-1}^2 + \beta \sigma_{t-1}^2$$

com apenas 3 parametros ($\omega, \alpha, \beta$). A variancia incondicional (de longo prazo) e:

$$\bar{\sigma}^2 = \frac{\omega}{1 - \alpha - \beta}$$

### Log-Verossimilhanca (distribuicao Normal)

$$\ell(\theta) = -\frac{T}{2} \ln(2\pi) - \frac{1}{2} \sum_{t=1}^{T} \left[ \ln(\sigma_t^2) + \frac{\epsilon_t^2}{\sigma_t^2} \right]$$

onde $\theta = (\mu, \omega, \alpha_1, \ldots, \alpha_q, \beta_1, \ldots, \beta_p)$.

## Quick Example

```python
from archbox import GARCH
from archbox.datasets import load_dataset

# Carregar retornos
sp500 = load_dataset('sp500')

# Estimar GARCH(1,1)
model = GARCH(sp500['returns'], p=1, q=1)
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
    Uncond. Variance: 8.994e-04
    Uncond. Vol:      2.999e-02
    ======================================================================
    ```

## Guia Detalhado

### Parametros do Construtor

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | array-like | obrigatorio | Serie de retornos |
| `p` | int | `1` | Ordem GARCH (lags de $\sigma^2$) |
| `q` | int | `1` | Ordem ARCH (lags de $\epsilon^2$) |
| `mean` | str | `"constant"` | Modelo de media: `"constant"` ou `"zero"` |
| `dist` | str | `"normal"` | Distribuicao condicional: `"normal"` |

### Parametros de `fit()`

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `method` | str | `"mle"` | Metodo de estimacao |
| `starting_values` | ndarray | `None` | Valores iniciais customizados |
| `variance_targeting` | bool | `False` | Fixar $\omega$ via variancia amostral |
| `disp` | bool | `True` | Exibir progresso da otimizacao |

### Especificando Ordens

```python
from archbox import GARCH
from archbox.datasets import load_dataset

sp500 = load_dataset('sp500')

# GARCH(1,1) - padrao e mais usado
model_11 = GARCH(sp500['returns'], p=1, q=1)
results_11 = model_11.fit()

# GARCH(1,2) - dois lags ARCH
model_12 = GARCH(sp500['returns'], p=1, q=2)
results_12 = model_12.fit()

# GARCH(2,1) - dois lags GARCH
model_21 = GARCH(sp500['returns'], p=2, q=1)
results_21 = model_21.fit()

# Comparar via BIC
print(f"GARCH(1,1) BIC: {results_11.bic:.4f}")
print(f"GARCH(1,2) BIC: {results_12.bic:.4f}")
print(f"GARCH(2,1) BIC: {results_21.bic:.4f}")
```

### Modelo de Media

```python
# Media constante (default): r_t = mu + eps_t
model_const = GARCH(sp500['returns'], p=1, q=1, mean="constant")

# Media zero: r_t = eps_t (usar quando retornos ja estao demeaned)
model_zero = GARCH(sp500['returns'], p=1, q=1, mean="zero")
```

### Variance Targeting

Variance targeting fixa $\omega = \bar{\sigma}^2 (1 - \alpha - \beta)$ usando a variancia amostral, reduzindo o numero de parametros livres e melhorando a estabilidade numerica:

```python
results_vt = model.fit(variance_targeting=True)
```

### Previsao

```python
# Previsao de volatilidade para os proximos 10 dias
forecast = results.forecast(horizon=10)

print("Variancia prevista:")
print(forecast['variance'])

print("\nVolatilidade prevista:")
print(forecast['volatility'])
```

### Resultados

| Atributo | Descricao |
|----------|-----------|
| `results.params` | Parametros estimados (ndarray) |
| `results.se` | Erros-padrao robustos (Bollerslev-Wooldridge) |
| `results.tvalues` | Estatisticas t |
| `results.pvalues` | p-valores bilaterais |
| `results.loglike` | Log-verossimilhanca |
| `results.aic` | Criterio de Informacao de Akaike |
| `results.bic` | Criterio de Informacao Bayesiano |
| `results.conditional_volatility` | Serie de $\sigma_t$ |
| `results.resid` | Residuos padronizados ($z_t = \epsilon_t / \sigma_t$) |

| Metodo | Descricao |
|--------|-----------|
| `results.persistence()` | $\sum \alpha_i + \sum \beta_j$ |
| `results.half_life()` | Meia-vida dos choques de volatilidade |
| `results.unconditional_variance()` | $\omega / (1 - \text{persistencia})$ |
| `results.forecast(horizon)` | Previsao de variancia/volatilidade |
| `results.summary()` | Tabela formatada de resultados |
| `results.plot("volatility")` | Grafico de retornos e volatilidade |
| `results.plot("residuals")` | Grafico de residuos padronizados |
| `results.to_dataframe()` | Exportar parametros como DataFrame |

## Interpretacao

### Persistencia

A **persistencia** mede a velocidade com que a volatilidade retorna ao seu nivel de longo prazo apos um choque:

$$\text{Persistencia} = \sum_{i=1}^{q} \alpha_i + \sum_{j=1}^{p} \beta_j$$

| Valor | Interpretacao |
|-------|---------------|
| $< 0.90$ | Baixa persistencia -- choques dissipam rapido |
| $0.90 - 0.99$ | Alta persistencia -- tipico de retornos diarios |
| $\approx 1.0$ | Persistencia unitaria -- IGARCH, choques permanentes |
| $> 1.0$ | Nao estacionario -- modelo mal especificado |

```python
persistence = results.persistence()
print(f"Persistencia: {persistence:.6f}")
```

### Variancia Incondicional

A variancia de longo prazo (incondicional) para a qual o processo reverte:

$$\bar{\sigma}^2 = \frac{\omega}{1 - \alpha - \beta}$$

```python
uncond_var = results.unconditional_variance()
uncond_vol = uncond_var ** 0.5
print(f"Variancia incondicional: {uncond_var:.6e}")
print(f"Volatilidade incondicional (anualizada): {uncond_vol * (252**0.5):.4f}")
```

### Meia-Vida

Numero de periodos para um choque de volatilidade decair pela metade:

$$\text{Meia-vida} = \frac{\ln(0.5)}{\ln(\alpha + \beta)}$$

```python
hl = results.half_life()
print(f"Meia-vida: {hl:.1f} periodos")
# Ex: meia-vida de 50 dias -> choques de volatilidade sao bastante persistentes
```

### Interpretacao dos Coeficientes

Para um GARCH(1,1) com $\alpha = 0.08$ e $\beta = 0.90$:

- **$\alpha = 0.08$**: Um choque no retorno de ontem contribui com 8% para a variancia de hoje. Quanto maior $\alpha$, mais reativo o modelo a novos choques.
- **$\beta = 0.90$**: A variancia condicional de ontem contribui com 90% para a de hoje. Quanto maior $\beta$, mais suave e a dinamica da volatilidade.
- **$\alpha + \beta = 0.98$**: Alta persistencia -- choques demoram cerca de $\ln(0.5)/\ln(0.98) \approx 34$ dias para decair pela metade.

## Diagnosticos

Apos estimar o GARCH, e essencial verificar se o modelo capturou adequadamente a dinamica da variancia condicional. Os diagnosticos sao aplicados nos **residuos padronizados** $z_t = \epsilon_t / \sigma_t$, que devem se comportar como inovacoes i.i.d.

### Ljung-Box nos Residuos Padronizados ao Quadrado

Testa se ainda resta autocorrelacao serial nos residuos ao quadrado $z_t^2$. Rejeicao indica que o modelo nao capturou toda a dinamica ARCH.

```python
from archbox.diagnostics import ljung_box_test

# Testar autocorrelacao em z_t^2
lb_result = ljung_box_test(results.resid**2, lags=10)
print(f"Ljung-Box Q(10): {lb_result.statistic:.4f}")
print(f"p-valor: {lb_result.pvalue:.4f}")
# p > 0.05 -> nao rejeita H0: sem autocorrelacao residual -> modelo OK
```

!!! tip "Interpretacao"
    - **p > 0.05**: O modelo capturou a dinamica da variancia. Bom ajuste.
    - **p < 0.05**: Resta dependencia nos residuos. Considere aumentar a ordem (p,q) ou usar um modelo alternativo (EGARCH, GJR-GARCH).

### Teste ARCH-LM

Testa a presenca de efeitos ARCH remanescentes nos residuos padronizados. Complementa o Ljung-Box.

```python
from archbox.diagnostics import arch_lm_test

lm_result = arch_lm_test(results.resid, lags=5)
print(f"ARCH-LM({5}): {lm_result.statistic:.4f}")
print(f"p-valor: {lm_result.pvalue:.4f}")
# p > 0.05 -> sem efeitos ARCH residuais -> modelo OK
```

### QQ-Plot dos Residuos

Avaliacao visual da adequacao da distribuicao condicional:

```python
import matplotlib.pyplot as plt
from scipy import stats

fig, ax = plt.subplots(figsize=(6, 6))
stats.probplot(results.resid, dist="norm", plot=ax)
ax.set_title("QQ-Plot: Residuos Padronizados vs. Normal")
plt.tight_layout()
plt.show()
```

!!! note "Interpretacao do QQ-Plot"
    - **Pontos sobre a linha diagonal**: distribuicao Normal e adequada.
    - **Caudas acima da linha**: caudas mais pesadas que a Normal. Considere usar `dist="studentt"` ou `dist="skewt"`.

### Sign Bias Test

Testa se choques positivos e negativos tem impacto diferente sobre a volatilidade -- indicando necessidade de modelos assimetricos (EGARCH, GJR-GARCH):

```python
from archbox.diagnostics import sign_bias_test

sb_result = sign_bias_test(results.resid)
print(sb_result)
# Rejeicao -> considerar EGARCH ou GJR-GARCH
```

### Workflow Completo de Diagnostico

```python
from archbox import GARCH
from archbox.datasets import load_dataset
from archbox.diagnostics import ljung_box_test, arch_lm_test, sign_bias_test

# 1. Estimar modelo
sp500 = load_dataset('sp500')
model = GARCH(sp500['returns'], p=1, q=1)
results = model.fit()

# 2. Residuos padronizados
z = results.resid

# 3. Diagnosticos
print("=== Ljung-Box (z^2) ===")
lb = ljung_box_test(z**2, lags=10)
print(f"  Q(10) = {lb.statistic:.4f}, p = {lb.pvalue:.4f}")

print("\n=== ARCH-LM ===")
lm = arch_lm_test(z, lags=5)
print(f"  LM(5) = {lm.statistic:.4f}, p = {lm.pvalue:.4f}")

print("\n=== Sign Bias ===")
sb = sign_bias_test(z)
print(f"  {sb}")

# 4. Visualizacao
results.plot("volatility")
results.plot("residuals")
```

## Equivalentes em R e Python

=== "ArchBox"

    ```python
    from archbox import GARCH
    from archbox.datasets import load_dataset

    sp500 = load_dataset('sp500')
    model = GARCH(sp500['returns'], p=1, q=1)
    results = model.fit()
    print(results.summary())

    # Previsao
    forecast = results.forecast(horizon=10)
    ```

=== "R (rugarch)"

    ```r
    library(rugarch)

    spec <- ugarchspec(
      variance.model = list(model = "sGARCH", garchOrder = c(1, 1)),
      mean.model = list(armaOrder = c(0, 0), include.mean = TRUE),
      distribution.model = "norm"
    )

    fit <- ugarchfit(spec = spec, data = returns)
    show(fit)

    # Previsao
    forecast <- ugarchforecast(fit, n.ahead = 10)
    ```

=== "Python (arch)"

    ```python
    from arch import arch_model

    am = arch_model(returns, vol='Garch', p=1, q=1, dist='Normal')
    res = am.fit()
    print(res.summary())

    # Previsao
    forecast = res.forecast(horizon=10)
    ```

| Funcionalidade | ArchBox | rugarch (R) | arch (Python) |
|---------------|---------|-------------|---------------|
| Especificacao | `GARCH(y, p=1, q=1)` | `ugarchspec(garchOrder=c(1,1))` | `arch_model(y, p=1, q=1)` |
| Estimacao | `model.fit()` | `ugarchfit(spec, data)` | `am.fit()` |
| Previsao | `results.forecast(h)` | `ugarchforecast(fit, n.ahead=h)` | `res.forecast(horizon=h)` |
| Persistencia | `results.persistence()` | `persistence(fit)` | `res.params['alpha[1]'] + res.params['beta[1]']` |
| Meia-vida | `results.half_life()` | Manual | Manual |
| Var. incondicional | `results.unconditional_variance()` | `uncvariance(fit)` | Manual |
| Simulacao | `model.simulate(n, params)` | `ugarchsim(fit, n.sim)` | `am.simulate(params, n)` |

## References

- Bollerslev, T. (1986). Generalized Autoregressive Conditional Heteroskedasticity. *Journal of Econometrics*, 31(3), 307--327.
- Engle, R. F. (1982). Autoregressive Conditional Heteroscedasticity with Estimates of the Variance of United Kingdom Inflation. *Econometrica*, 50(4), 987--1007.
- Bollerslev, T., Chou, R. Y., & Kroner, K. F. (1992). ARCH Modeling in Finance: A Review of the Theory and Empirical Evidence. *Journal of Econometrics*, 52(1-2), 5--59.
- Francq, C., & Zakoian, J.-M. (2019). *GARCH Models: Structure, Statistical Inference and Financial Applications* (2nd ed.). Wiley.
- Hansen, P. R., & Lunde, A. (2005). A Forecast Comparison of Volatility Models: Does Anything Beat a GARCH(1,1)? *Journal of Applied Econometrics*, 20(7), 873--889.

## See Also

- [EGARCH](egarch.md) -- Extensao com efeito leverage logaritmico
- [GJR-GARCH](gjr-garch.md) -- Extensao com leverage via indicadora
- [Distribuicoes Condicionais](../distributions/index.md) -- Escolha da distribuicao para os erros
- [Diagnosticos: ARCH-LM](../../diagnostics/arch-lm.md) -- Teste para efeitos ARCH residuais
- [Diagnosticos: Ljung-Box](../../diagnostics/ljung-box.md) -- Teste de autocorrelacao serial
- [Theory: GARCH](../../theory/garch-theory.md) -- Fundamentos teoricos detalhados
