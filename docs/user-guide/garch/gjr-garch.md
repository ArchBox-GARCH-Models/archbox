---
title: "GJR-GARCH"
description: "GJR-GARCH model - captures the leverage effect via an indicator function for negative shocks."
---

# GJR-GARCH

!!! info "Quick Reference"
    **Class:** `archbox.models.gjr_garch.GJRGARCH`
    **Import:** `from archbox import GJRGARCH`
    **R equivalent:** `rugarch::ugarchspec(variance.model = list(model = "gjrGARCH", garchOrder = c(1,1)))`
    **Python equivalent:** `arch.arch_model(returns, vol='Garch', p=1, o=1, q=1)`

## Overview

O modelo GJR-GARCH, proposto por **Glosten, Jagannathan e Runkle (1993)**, e uma extensao do GARCH que captura o **efeito de alavancagem (leverage effect)** de forma elegante e intuitiva: um termo indicador $I_{t-i}$ "liga" um coeficiente adicional $\gamma$ quando o choque e negativo, amplificando o impacto de mas noticias sobre a volatilidade.

O GJR-GARCH e um dos modelos assimetricos mais populares na pratica por combinar:

- **Simplicidade**: Apenas um parametro adicional ($\gamma$) em relacao ao GARCH padrao
- **Interpretabilidade**: $\gamma$ mede diretamente a magnitude do efeito leverage
- **Eficacia empirica**: Consistentemente melhora o ajuste em dados acionarios

**Quando usar:**

- Retornos de acoes e indices onde o sign bias test rejeita simetria
- Quando se deseja uma interpretacao direta do efeito leverage ($\gamma$)
- Analise de risco onde a assimetria na volatilidade e economicamente relevante
- Extensao natural do GARCH(1,1) quando a simetria e rejeitada

## Formulacao Matematica

### Equacao da Media

$$r_t = \mu + \epsilon_t, \qquad \epsilon_t = \sigma_t z_t, \qquad z_t \sim D(0, 1)$$

### Equacao da Variancia Condicional

$$\sigma_t^2 = \omega + \sum_{i=1}^{q} (\alpha_i + \gamma_i I_{t-i}) \epsilon_{t-i}^2 + \sum_{j=1}^{p} \beta_j \sigma_{t-j}^2$$

onde $I_{t-i}$ e a **funcao indicadora** para choques negativos:

$$I_{t-i} = \begin{cases} 1 & \text{se } \epsilon_{t-i} < 0 \\ 0 & \text{se } \epsilon_{t-i} \geq 0 \end{cases}$$

| Parametro | Descricao | Restricao |
|-----------|-----------|-----------|
| $\omega$ | Intercepto (variancia de base) | $\omega > 0$ |
| $\alpha_i$ | Coeficientes ARCH (reacao a choques positivos) | $\alpha_i \geq 0$ |
| $\gamma_i$ | Coeficientes de leverage (impacto adicional de choques negativos) | $\alpha_i + \gamma_i \geq 0$ |
| $\beta_j$ | Coeficientes GARCH (persistencia) | $\beta_j \geq 0$ |
| $p$ | Ordem GARCH (lags da variancia) | $p \geq 1$ |
| $q$ | Ordem ARCH (lags dos choques) | $q \geq 1$ |

**Condicao de estacionariedade:** $\sum_{i=1}^{q} \alpha_i + \frac{1}{2}\sum_{i=1}^{q} \gamma_i + \sum_{j=1}^{p} \beta_j < 1$

### Caso Especial: GJR-GARCH(1,1)

$$\sigma_t^2 = \omega + (\alpha + \gamma I_{t-1}) \epsilon_{t-1}^2 + \beta \sigma_{t-1}^2$$

**Impacto de choques:**

- **Choque positivo** ($\epsilon_{t-1} > 0$): impacto = $\alpha \epsilon_{t-1}^2$
- **Choque negativo** ($\epsilon_{t-1} < 0$): impacto = $(\alpha + \gamma) \epsilon_{t-1}^2$

A variancia incondicional e:

$$\bar{\sigma}^2 = \frac{\omega}{1 - \alpha - \gamma/2 - \beta}$$

### Interpretacao do Parametro $\gamma$

O parametro $\gamma$ e a estrela do GJR-GARCH:

| Valor de $\gamma$ | Interpretacao |
|-------------------|---------------|
| $\gamma > 0$ | Efeito leverage: choques negativos geram mais volatilidade |
| $\gamma = 0$ | Sem assimetria (reduz ao GARCH simetrico) |
| $\gamma < 0$ | Efeito inverso (raro, mas possivel em commodities) |

!!! note "Magnitude do leverage"
    A **razao de impacto assimetrico** e $(\alpha + \gamma) / \alpha$. Por exemplo, se $\alpha = 0.05$ e $\gamma = 0.10$, um choque negativo tem $3\times$ mais impacto na volatilidade que um choque positivo de mesma magnitude.

### News Impact Curve

A NIC do GJR-GARCH e uma **parabola por partes** (piecewise quadratic):

$$\text{NIC}(\epsilon_{t-1}) = \begin{cases} \omega + \beta \sigma^2 + \alpha \epsilon_{t-1}^2 & \text{se } \epsilon_{t-1} \geq 0 \\[6pt] \omega + \beta \sigma^2 + (\alpha + \gamma) \epsilon_{t-1}^2 & \text{se } \epsilon_{t-1} < 0 \end{cases}$$

```
Volatilidade (σ²)
     │
     │╲                  GJR-GARCH
     │ ╲               ╱
     │  ╲            ╱
     │   ╲         ╱
     │    ╲      ╱    GARCH (α)
     │     ╲   ╱    ╱
     │      ╲╱   ╱    (inclinacao α+γ)
     │      ╱╲ ╱
     │    ╱   ╲    (inclinacao α)
     │  ╱
     │╱
     ├──────────────────────── Choque (ε)
   Negativo    0    Positivo
```

!!! note "NIC do GJR-GARCH"
    A NIC e composta por duas parabolas com vertices no mesmo ponto ($\epsilon = 0$), mas com inclinacoes diferentes: $\alpha$ para choques positivos e $\alpha + \gamma$ para choques negativos. A descontinuidade na derivada em $\epsilon = 0$ e a assinatura visual do GJR-GARCH.

## Quick Example

```python
from archbox import GJRGARCH
from archbox.datasets import load_dataset

# Carregar retornos
sp500 = load_dataset('sp500')

# Estimar GJR-GARCH(1,1)
model = GJRGARCH(sp500['returns'], p=1, q=1)
results = model.fit()
print(results.summary())
```

??? example "Output esperado"
    ```
    ======================================================================
                          Volatility Model Results
    ======================================================================
    Model:            GJR-GARCH
    Distribution:     Normal
    Observations:     2000
    Log-Likelihood:   3152.8734
    AIC:              -6297.7468
    BIC:              -6275.1709
    Converged:        True
    ----------------------------------------------------------------------
    Parameter         Estimate      Std Err      t-value      p-value
    ----------------------------------------------------------------------
    omega            0.000010     0.000003       3.4521       0.0006
    alpha[1]         0.032145     0.011234       2.8613       0.0042
    gamma[1]         0.105678     0.019876       5.3170       0.0000
    beta[1]          0.908432     0.014567      62.3654       0.0000
    ----------------------------------------------------------------------
    Persistence:      0.993416
    Half-life:        104.81 periods
    Uncond. Variance: 8.876e-04
    Uncond. Vol:      2.979e-02
    ======================================================================
    ```

## Guia Detalhado

### Parametros do Construtor

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | array-like | obrigatorio | Serie de retornos |
| `p` | int | `1` | Ordem GARCH (lags de $\sigma^2$) |
| `q` | int | `1` | Ordem ARCH (lags de $\epsilon^2$ e indicadora) |
| `mean` | str | `"constant"` | Modelo de media: `"constant"` ou `"zero"` |
| `dist` | str | `"normal"` | Distribuicao condicional: `"normal"` |

### Parametros de `fit()`

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `method` | str | `"mle"` | Metodo de estimacao |
| `starting_values` | ndarray | `None` | Valores iniciais customizados |
| `variance_targeting` | bool | `False` | Fixar $\omega$ via variancia amostral |
| `disp` | bool | `True` | Exibir progresso da otimizacao |

### Motivacao: Sign Bias Test

Antes de estimar um GJR-GARCH, e boa pratica verificar se ha evidencia estatistica de assimetria nos residuos do GARCH simetrico:

```python
from archbox import GARCH, GJRGARCH
from archbox.datasets import load_dataset
from archbox.diagnostics import sign_bias_test

sp500 = load_dataset('sp500')

# 1. Estimar GARCH(1,1) simetrico
garch = GARCH(sp500['returns'], p=1, q=1)
garch_results = garch.fit()

# 2. Sign bias test nos residuos do GARCH
sb = sign_bias_test(garch_results.resid)
print(sb)
# Se rejeita -> assimetria presente -> justifica GJR-GARCH

# 3. Estimar GJR-GARCH(1,1)
gjr = GJRGARCH(sp500['returns'], p=1, q=1)
gjr_results = gjr.fit()

# 4. Comparar modelos via BIC
print(f"\nGARCH   BIC: {garch_results.bic:.4f}")
print(f"GJR     BIC: {gjr_results.bic:.4f}")
print(f"Melhoria: {garch_results.bic - gjr_results.bic:.4f}")
```

### Exemplo Completo

```python
from archbox import GJRGARCH
from archbox.datasets import load_dataset

# 1. Carregar dados
sp500 = load_dataset('sp500')
returns = sp500['returns']

# 2. Estimar GJR-GARCH(1,1)
model = GJRGARCH(returns, p=1, q=1)
results = model.fit()

# 3. Extrair parametros
omega = results.params[0]
alpha = results.params[1]
gamma = results.params[2]
beta  = results.params[3]

print(f"omega:  {omega:.6f}")
print(f"alpha:  {alpha:.6f}  (reacao a choques positivos)")
print(f"gamma:  {gamma:.6f}  (leverage adicional p/ choques negativos)")
print(f"beta:   {beta:.6f}  (persistencia)")

# 4. Razao de impacto assimetrico
ratio = (alpha + gamma) / alpha
print(f"\nRazao de impacto: {ratio:.2f}x")
print(f"Choques negativos geram {ratio:.1f}x mais volatilidade que positivos")

# 5. Metricas
print(f"\nPersistencia: {results.persistence():.6f}")
print(f"Meia-vida: {results.half_life():.1f} periodos")
print(f"Variancia incondicional: {results.unconditional_variance():.6e}")

# 6. Previsao
forecast = results.forecast(horizon=10)
print("\nVolatilidade prevista (proximos 10 dias):")
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
| `results.persistence()` | $\alpha + \gamma/2 + \beta$ |
| `results.half_life()` | Meia-vida dos choques de volatilidade |
| `results.unconditional_variance()` | $\omega / (1 - \alpha - \gamma/2 - \beta)$ |
| `results.forecast(horizon)` | Previsao de variancia/volatilidade |
| `results.summary()` | Tabela formatada de resultados |
| `results.plot("volatility")` | Grafico de retornos e volatilidade |
| `results.plot("residuals")` | Grafico de residuos padronizados |
| `results.to_dataframe()` | Exportar parametros como DataFrame |

## Interpretacao

### Magnitude do Efeito Leverage

Para um GJR-GARCH(1,1) com $\alpha = 0.03$, $\gamma = 0.11$, $\beta = 0.91$:

- **Choque positivo** de 1%: aumento na variancia = $0.03 \times (0.01)^2 = 3.0 \times 10^{-6}$
- **Choque negativo** de 1%: aumento na variancia = $(0.03 + 0.11) \times (0.01)^2 = 1.4 \times 10^{-5}$
- Choques negativos tem $\frac{0.14}{0.03} \approx 4.7\times$ mais impacto

### Persistencia

No GJR-GARCH, a persistencia inclui metade do parametro gamma (pois choques negativos ocorrem aproximadamente 50% do tempo):

$$\text{Persistencia} = \alpha + \frac{\gamma}{2} + \beta$$

```python
persistence = results.persistence()
print(f"Persistencia: {persistence:.6f}")
```

### Variancia Incondicional

$$\bar{\sigma}^2 = \frac{\omega}{1 - \alpha - \gamma/2 - \beta}$$

```python
uncond_var = results.unconditional_variance()
uncond_vol = uncond_var ** 0.5
print(f"Variancia incondicional: {uncond_var:.6e}")
print(f"Volatilidade incondicional (anualizada): {uncond_vol * (252**0.5):.4f}")
```

### Teste de Significancia do Leverage

Se $\gamma$ nao e significativamente diferente de zero, o GJR-GARCH reduz ao GARCH simetrico:

```python
# p-valor do parametro gamma
gamma_pvalue = results.pvalues[2]
print(f"gamma = {results.params[2]:.6f}, p-valor = {gamma_pvalue:.4f}")

if gamma_pvalue < 0.05:
    print("Efeito leverage significativo -> GJR-GARCH justificado")
else:
    print("Leverage nao significativo -> GARCH simetrico pode ser suficiente")
```

## Diagnosticos

### Ljung-Box nos Residuos Padronizados ao Quadrado

```python
from archbox.diagnostics import ljung_box_test

lb_result = ljung_box_test(results.resid**2, lags=10)
print(f"Ljung-Box Q(10): {lb_result.statistic:.4f}")
print(f"p-valor: {lb_result.pvalue:.4f}")
```

### Teste ARCH-LM

```python
from archbox.diagnostics import arch_lm_test

lm_result = arch_lm_test(results.resid, lags=5)
print(f"ARCH-LM(5): {lm_result.statistic:.4f}")
print(f"p-valor: {lm_result.pvalue:.4f}")
```

### Sign Bias Test pos-Estimacao

O sign bias test deve **nao rejeitar** apos o GJR-GARCH, confirmando que a assimetria foi capturada:

```python
from archbox.diagnostics import sign_bias_test

sb_result = sign_bias_test(results.resid)
print(sb_result)
# p > 0.05 -> assimetria capturada pelo GJR-GARCH
```

### Workflow Completo de Diagnostico

```python
from archbox import GJRGARCH
from archbox.datasets import load_dataset
from archbox.diagnostics import ljung_box_test, arch_lm_test, sign_bias_test

# 1. Estimar modelo
sp500 = load_dataset('sp500')
model = GJRGARCH(sp500['returns'], p=1, q=1)
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
    from archbox import GJRGARCH
    from archbox.datasets import load_dataset

    sp500 = load_dataset('sp500')
    model = GJRGARCH(sp500['returns'], p=1, q=1)
    results = model.fit()
    print(results.summary())

    # Previsao
    forecast = results.forecast(horizon=10)
    ```

=== "R (rugarch)"

    ```r
    library(rugarch)

    spec <- ugarchspec(
      variance.model = list(model = "gjrGARCH", garchOrder = c(1, 1)),
      mean.model = list(armaOrder = c(0, 0), include.mean = TRUE),
      distribution.model = "norm"
    )

    fit <- ugarchfit(spec = spec, data = returns)
    show(fit)

    # News impact curve
    ni <- newsimpact(fit)
    plot(ni)

    # Previsao
    forecast <- ugarchforecast(fit, n.ahead = 10)
    ```

=== "Python (arch)"

    ```python
    from arch import arch_model

    # Em arch, GJR-GARCH usa o=1 para o termo de leverage
    am = arch_model(returns, vol='Garch', p=1, o=1, q=1, dist='Normal')
    res = am.fit()
    print(res.summary())

    # Previsao
    forecast = res.forecast(horizon=10)
    ```

| Funcionalidade | ArchBox | rugarch (R) | arch (Python) |
|---------------|---------|-------------|---------------|
| Especificacao | `GJRGARCH(y, p=1, q=1)` | `ugarchspec(model="gjrGARCH")` | `arch_model(y, p=1, o=1, q=1)` |
| Estimacao | `model.fit()` | `ugarchfit(spec, data)` | `am.fit()` |
| Previsao | `results.forecast(h)` | `ugarchforecast(fit, n.ahead=h)` | `res.forecast(horizon=h)` |
| Persistencia | `results.persistence()` | `persistence(fit)` | Manual |
| Meia-vida | `results.half_life()` | Manual | Manual |
| Leverage ($\gamma$) | `results.params[2]` | `coef(fit)['gamma1']` | `res.params['gamma[1]']` |

## References

- Glosten, L. R., Jagannathan, R., & Runkle, D. E. (1993). On the Relation between the Expected Value and the Volatility of the Nominal Excess Return on Stocks. *The Journal of Finance*, 48(5), 1779--1801.
- Engle, R. F., & Ng, V. K. (1993). Measuring and Testing the Impact of News on Volatility. *The Journal of Finance*, 48(5), 1749--1778.
- Black, F. (1976). Studies of Stock Market Volatility Changes. *Proceedings of the American Statistical Association, Business and Economic Statistics Section*, 177--181.
- Francq, C., & Zakoian, J.-M. (2019). *GARCH Models: Structure, Statistical Inference and Financial Applications* (2nd ed.). Wiley.

## See Also

- [GARCH(p,q)](garch.md) -- Modelo simetrico padrao
- [EGARCH](egarch.md) -- Modelo assimetrico com log-variancia
- [APARCH](aparch.md) -- Modelo assimetrico de potencia generalizada
- [Distribuicoes Condicionais](../distributions/index.md) -- Escolha da distribuicao para os erros
- [Diagnosticos: Sign Bias](../../diagnostics/sign-bias.md) -- Teste de assimetria nos residuos
- [Diagnosticos: ARCH-LM](../../diagnostics/arch-lm.md) -- Teste para efeitos ARCH residuais
