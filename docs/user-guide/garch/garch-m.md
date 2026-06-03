---
title: "GARCH-in-Mean"
description: "GARCH-M model - includes conditional volatility in the mean equation to capture the risk-return tradeoff."
---

# GARCH-in-Mean (GARCH-M)

!!! info "Quick Reference"
    **Class:** `archbox.models.garch_m.GARCHM`
    **Import:** `from archbox import GARCHM`
    **R equivalent:** `rugarch::ugarchspec(mean.model = list(archm = TRUE, archpow = 2))`
    **Python equivalent:** `arch.arch_model(returns, mean='ARX', vol='GARCH', p=1, q=1)` com regressores manuais

## Overview

O modelo GARCH-in-Mean (GARCH-M), proposto por **Engle, Lilien & Robins (1987)**, estende o GARCH padrao ao incluir a **volatilidade condicional como variavel explicativa na equacao da media**. Isso permite testar e estimar o **premio de risco** -- a compensacao adicional que investidores exigem por suportar maior incerteza.

A motivacao teorica vem diretamente da teoria financeira: pelo CAPM e modelos intertemporais de precificacao, o retorno esperado de um ativo deveria ser proporcional ao seu risco. O GARCH-M operacionaliza essa ideia ao modelar a relacao retorno-risco de forma condicional.

**Quando usar:**

- Testar a hipotese de premio de risco em series financeiras
- Mercados acionarios: o retorno esperado aumenta com a volatilidade?
- Titulos de renda fixa: a taxa de juros reflete o risco?
- Modelagem conjunta de media e variancia condicionais
- Quando a teoria financeira sugere relacao retorno-risco

## Formulacao Matematica

### Equacao da Media

$$r_t = \mu + \lambda \sigma_t^{\delta} + \epsilon_t, \qquad \epsilon_t = \sigma_t z_t, \qquad z_t \sim D(0, 1)$$

onde:

| Parametro | Descricao | Restricao |
|-----------|-----------|-----------|
| $\mu$ | Intercepto da media | Nenhuma |
| $\lambda$ | **Premio de risco** | Nenhuma (esperado $\lambda > 0$) |
| $\delta$ | Potencia da volatilidade | $\delta \in \{1, 2\}$ |
| $\sigma_t^{\delta}$ | Variancia ($\delta=2$) ou desvio-padrao ($\delta=1$) condicional | |

**Interpretacao de $\delta$:**

| $\delta$ | Termo na media | Interpretacao |
|----------|----------------|---------------|
| $\delta = 1$ | $\lambda \sigma_t$ | Retorno proporcional ao desvio-padrao |
| $\delta = 2$ | $\lambda \sigma_t^2$ | Retorno proporcional a variancia |

### Equacao da Variancia Condicional

A equacao da variancia segue o GARCH(1,1) padrao:

$$\sigma_t^2 = \omega + \alpha \epsilon_{t-1}^2 + \beta \sigma_{t-1}^2$$

| Parametro | Descricao | Restricao |
|-----------|-----------|-----------|
| $\omega$ | Intercepto | $\omega > 0$ |
| $\alpha$ | Coeficiente ARCH | $\alpha \geq 0$ |
| $\beta$ | Coeficiente GARCH | $\beta \geq 0$ |

**Condicao de estacionariedade:** $\alpha + \beta < 1$

### Retorno Esperado Condicional

O retorno esperado condicional no GARCH-M e:

$$E_t[r_{t+1}] = \mu + \lambda \sigma_{t+1|t}^{\delta}$$

!!! note "Interpretacao economica"
    Se $\lambda > 0$ e estatisticamente significativo, investidores **exigem retorno adicional** proporcional ao risco (medido pela volatilidade). Isso e consistente com investidores avessos ao risco. Se $\lambda \leq 0$ ou nao significativo, a evidencia nao suporta um premio de risco condicional.

### Log-Verossimilhanca

Para a distribuicao Normal:

$$\ell(\theta) = -\frac{T}{2}\log(2\pi) - \frac{1}{2}\sum_{t=1}^{T}\left[\log(\sigma_t^2) + \frac{(r_t - \mu - \lambda \sigma_t^{\delta})^2}{\sigma_t^2}\right]$$

## Quick Example

```python
from archbox import GARCHM
from archbox.datasets import load_dataset

# Carregar retornos
sp500 = load_dataset('sp500')

# Estimar GARCH-M(1,1) com desvio-padrao na media
model = GARCHM(sp500['returns'], p=1, q=1, delta=1)
results = model.fit()
print(results.summary())
```

??? example "Output esperado"
    ```
    ======================================================================
                          Volatility Model Results
    ======================================================================
    Model:            GARCH-M(1,1)
    Distribution:     Normal
    Risk term:        lambda * sigma^1
    Observations:     2000
    Log-Likelihood:   3150.8923
    AIC:              -6291.7846
    BIC:              -6263.6328
    Converged:        True
    ----------------------------------------------------------------------
    Parameter         Estimate      Std Err      t-value      p-value
    ----------------------------------------------------------------------
    mu                0.023456     0.012345       1.8999       0.0575
    lambda            0.078912     0.034567       2.2833       0.0224
    omega             0.012345     0.004321       2.8569       0.0043
    alpha[1]          0.087654     0.018765       4.6711       0.0000
    beta[1]           0.897654     0.021345      42.0547       0.0000
    ----------------------------------------------------------------------
    Persistence:      0.985308
    Half-life:        46.80 periods
    Risk premium:     lambda = 0.0789 (significant at 5%)
    ======================================================================
    ```

## Guia Detalhado

### Parametros do Construtor

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | array-like | obrigatorio | Serie de retornos |
| `p` | int | `1` | Ordem GARCH (lags de $\sigma^2$) |
| `q` | int | `1` | Ordem ARCH (lags de $\epsilon^2$) |
| `delta` | int | `2` | Potencia da volatilidade na media: `1` ou `2` |
| `mean` | str | `"constant"` | Modelo de media base |
| `dist` | str | `"normal"` | Distribuicao condicional |

### Parametros de `fit()`

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `method` | str | `"mle"` | Metodo de estimacao |
| `starting_values` | ndarray | `None` | Valores iniciais customizados |
| `disp` | bool | `True` | Exibir progresso da otimizacao |

### Exemplo com Equity Premium

```python
from archbox import GARCHM
from archbox.datasets import load_dataset

# 1. Carregar dados de retornos de mercado
sp500 = load_dataset('sp500')
returns = sp500['returns']

# 2. Comparar delta=1 (desvio-padrao) vs delta=2 (variancia)
print("=== GARCH-M com delta=1 (sigma) ===")
model_sd = GARCHM(returns, p=1, q=1, delta=1)
res_sd = model_sd.fit()
print(f"  lambda = {res_sd.params['lambda']:.4f}")
print(f"  t-stat = {res_sd.tvalues['lambda']:.4f}")
print(f"  p-valor = {res_sd.pvalues['lambda']:.4f}")
print(f"  AIC = {res_sd.aic:.4f}")

print("\n=== GARCH-M com delta=2 (sigma^2) ===")
model_var = GARCHM(returns, p=1, q=1, delta=2)
res_var = model_var.fit()
print(f"  lambda = {res_var.params['lambda']:.4f}")
print(f"  t-stat = {res_var.tvalues['lambda']:.4f}")
print(f"  p-valor = {res_var.pvalues['lambda']:.4f}")
print(f"  AIC = {res_var.aic:.4f}")

# 3. Qual especificacao preferir?
better = "delta=1" if res_sd.aic < res_var.aic else "delta=2"
print(f"\nMelhor pelo AIC: {better}")
```

### Exemplo com Teste de Premio de Risco

```python
from archbox import GARCHM, GARCH
from archbox.datasets import load_dataset

sp500 = load_dataset('sp500')
returns = sp500['returns']

# 1. GARCH padrao (sem premio de risco)
garch = GARCH(returns, p=1, q=1)
garch_res = garch.fit()

# 2. GARCH-M (com premio de risco)
garchm = GARCHM(returns, p=1, q=1, delta=2)
garchm_res = garchm.fit()

# 3. Teste de razao de verossimilhanca
# H0: lambda = 0 (sem premio de risco)
lr_stat = 2 * (garchm_res.loglike - garch_res.loglike)
from scipy import stats
p_value = 1 - stats.chi2.cdf(lr_stat, df=1)

print("=== Teste de Premio de Risco ===")
print(f"H0: lambda = 0 (sem premio)")
print(f"LR statistic: {lr_stat:.4f}")
print(f"p-valor: {p_value:.4f}")
print(f"Resultado: {'Rejeita H0 -> premio de risco significativo' if p_value < 0.05 else 'Nao rejeita -> sem evidencia de premio'}")
```

### Resultados

| Atributo | Descricao |
|----------|-----------|
| `results.params` | Parametros estimados (inclui $\lambda$) |
| `results.params['lambda']` | Premio de risco estimado |
| `results.se` | Erros-padrao robustos (Bollerslev-Wooldridge) |
| `results.tvalues` | Estatisticas t |
| `results.pvalues` | p-valores bilaterais |
| `results.loglike` | Log-verossimilhanca |
| `results.aic` | Criterio de Informacao de Akaike |
| `results.bic` | Criterio de Informacao Bayesiano |
| `results.conditional_volatility` | Serie de $\sigma_t$ |
| `results.conditional_mean` | Serie de $\mu + \lambda \sigma_t^{\delta}$ |
| `results.resid` | Residuos padronizados |

| Metodo | Descricao |
|--------|-----------|
| `results.persistence()` | Persistencia da variancia ($\alpha + \beta$) |
| `results.half_life()` | Meia-vida dos choques |
| `results.unconditional_variance()` | Variancia incondicional |
| `results.forecast(horizon)` | Previsao de media e variancia |
| `results.summary()` | Tabela formatada |
| `results.plot("volatility")` | Grafico de retornos e volatilidade |
| `results.plot("mean")` | Grafico da media condicional |
| `results.to_dataframe()` | Exportar parametros como DataFrame |

## Interpretacao

### O Parametro $\lambda$ (Premio de Risco)

O parametro $\lambda$ e o centro do modelo GARCH-M:

| Valor de $\lambda$ | Interpretacao |
|--------------------|---------------|
| $\lambda > 0$ (significativo) | Investidores exigem retorno maior em periodos de alta volatilidade |
| $\lambda \approx 0$ (nao significativo) | Sem evidencia de premio de risco condicional |
| $\lambda < 0$ (significativo) | Retornos menores em alta volatilidade (raro, possivel em safe havens) |

!!! tip "Significancia estatistica"
    A significancia de $\lambda$ e testada via estatistica t padrao: $t = \hat{\lambda} / se(\hat{\lambda})$. Se $|t| > 1.96$, o premio de risco e significativo a 5%. A literatura empirica encontra resultados **mistos** -- $\lambda$ frequentemente e positivo mas nem sempre significativo.

### Impacto Economico

```python
# Calcular o impacto do premio de risco
lambda_hat = garchm_res.params['lambda']
vol_mean = garchm_res.conditional_volatility.mean()

if garchm_res.delta == 1:
    risk_premium_mean = lambda_hat * vol_mean
    print(f"Premio de risco medio: {risk_premium_mean:.4f}")
    print(f"  = lambda ({lambda_hat:.4f}) x sigma_medio ({vol_mean:.4f})")
elif garchm_res.delta == 2:
    risk_premium_mean = lambda_hat * vol_mean**2
    print(f"Premio de risco medio: {risk_premium_mean:.4f}")
    print(f"  = lambda ({lambda_hat:.4f}) x sigma^2_medio ({vol_mean**2:.6f})")

print(f"Premio anualizado: {risk_premium_mean * 252:.2f}%")
```

### Comparacao com GARCH Padrao

| Aspecto | GARCH | GARCH-M |
|---------|-------|---------|
| Equacao da media | $r_t = \mu + \epsilon_t$ | $r_t = \mu + \lambda\sigma_t^{\delta} + \epsilon_t$ |
| Premio de risco | Nao modelado | $\lambda \sigma_t^{\delta}$ |
| Parametros | $\omega, \alpha, \beta$ | $\omega, \alpha, \beta, \lambda$ |
| Media condicional | Constante | Varia com volatilidade |
| Aplicacao | Modelagem de volatilidade | Relacao risco-retorno |

## Diagnosticos

### Ljung-Box nos Residuos Padronizados

```python
from archbox.diagnostics import ljung_box_test

# Testar residuos (nao ao quadrado) para autocorrelacao na media
lb_mean = ljung_box_test(garchm_res.resid, lags=10)
print(f"Ljung-Box na media Q(10): {lb_mean.statistic:.4f}, p = {lb_mean.pvalue:.4f}")

# Testar residuos ao quadrado para autocorrelacao na variancia
lb_var = ljung_box_test(garchm_res.resid**2, lags=10)
print(f"Ljung-Box na variancia Q(10): {lb_var.statistic:.4f}, p = {lb_var.pvalue:.4f}")
```

### Teste ARCH-LM

```python
from archbox.diagnostics import arch_lm_test

lm_result = arch_lm_test(garchm_res.resid, lags=5)
print(f"ARCH-LM(5): {lm_result.statistic:.4f}")
print(f"p-valor: {lm_result.pvalue:.4f}")
```

### Workflow Completo de Diagnostico

```python
from archbox import GARCHM
from archbox.datasets import load_dataset
from archbox.diagnostics import ljung_box_test, arch_lm_test

# 1. Estimar modelo
sp500 = load_dataset('sp500')
model = GARCHM(sp500['returns'], p=1, q=1, delta=2)
results = model.fit()

# 2. Residuos padronizados
z = results.resid

# 3. Diagnosticos
print("=== Ljung-Box (z) - media ===")
lb_m = ljung_box_test(z, lags=10)
print(f"  Q(10) = {lb_m.statistic:.4f}, p = {lb_m.pvalue:.4f}")

print("\n=== Ljung-Box (z^2) - variancia ===")
lb_v = ljung_box_test(z**2, lags=10)
print(f"  Q(10) = {lb_v.statistic:.4f}, p = {lb_v.pvalue:.4f}")

print("\n=== ARCH-LM ===")
lm = arch_lm_test(z, lags=5)
print(f"  LM(5) = {lm.statistic:.4f}, p = {lm.pvalue:.4f}")

# 4. Premio de risco
print(f"\n=== Premio de Risco ===")
print(f"  lambda = {results.params['lambda']:.4f}")
print(f"  t-stat = {results.tvalues['lambda']:.4f}")
print(f"  Significativo a 5%? {'Sim' if results.pvalues['lambda'] < 0.05 else 'Nao'}")

# 5. Visualizacao
results.plot("volatility")
results.plot("mean")
```

## Equivalentes em R e Python

=== "ArchBox"

    ```python
    from archbox import GARCHM
    from archbox.datasets import load_dataset

    sp500 = load_dataset('sp500')
    model = GARCHM(sp500['returns'], p=1, q=1, delta=2)
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
      mean.model = list(
        armaOrder = c(0, 0),
        include.mean = TRUE,
        archm = TRUE,      # ativar GARCH-in-Mean
        archpow = 2         # delta: 1 = sigma, 2 = sigma^2
      ),
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

    # arch nao tem GARCH-M nativo
    # Solucao: estimar em duas etapas ou usar regressores
    am = arch_model(returns, mean='ARX', vol='GARCH', p=1, q=1)
    # Nota: requer implementacao manual do termo de risco
    ```

| Funcionalidade | ArchBox | rugarch (R) | arch (Python) |
|---------------|---------|-------------|---------------|
| Especificacao | `GARCHM(y, delta=2)` | `ugarchspec(archm=TRUE, archpow=2)` | Manual |
| Premio de risco | `results.params['lambda']` | `coef(fit)['archm']` | Manual |
| Previsao media | `results.forecast(h)` | `ugarchforecast(fit)@forecast$seriesFor` | Manual |
| Teste lambda | `results.tvalues['lambda']` | `fit@fit$tval['archm']` | Manual |

## References

- Engle, R. F., Lilien, D. M., & Robins, R. P. (1987). Estimating Time Varying Risk Premia in the Term Structure: The ARCH-M Model. *Econometrica*, 55(2), 391--407.
- Bollerslev, T., Engle, R. F., & Wooldridge, J. M. (1988). A Capital Asset Pricing Model with Time-Varying Covariances. *Journal of Political Economy*, 96(1), 116--131.
- Glosten, L. R., Jagannathan, R., & Runkle, D. E. (1993). On the Relation Between the Expected Value and the Volatility of the Nominal Excess Return on Stocks. *The Journal of Finance*, 48(5), 1779--1801.
- Francq, C., & Zakoian, J.-M. (2019). *GARCH Models: Structure, Statistical Inference and Financial Applications* (2nd ed.). Wiley.

## See Also

- [GARCH(p,q)](garch.md) -- Modelo simetrico padrao (sem premio de risco)
- [EGARCH](egarch.md) -- EGARCH com efeito leverage
- [Distribuicoes Condicionais](../distributions/index.md) -- Escolha da distribuicao para os erros
- [Diagnosticos: ARCH-LM](../../diagnostics/arch-lm.md) -- Teste para efeitos ARCH residuais
- [Diagnosticos: Ljung-Box](../../diagnostics/ljung-box.md) -- Teste de autocorrelacao
