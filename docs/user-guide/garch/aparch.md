---
title: "APARCH"
description: "Asymmetric Power ARCH model - a flexible generalization that nests GARCH, GJR-GARCH and TARCH as special cases via the power parameter delta."
---

# APARCH

!!! info "Quick Reference"
    **Class:** `archbox.models.aparch.APARCH`
    **Import:** `from archbox import APARCH`
    **R equivalent:** `rugarch::ugarchspec(variance.model = list(model = "apARCH", garchOrder = c(1,1)))`
    **Python equivalent:** `arch.arch_model(returns, vol='APARCH', p=1, o=1, q=1)`

## Overview

O modelo APARCH (Asymmetric Power ARCH), proposto por **Ding, Granger e Engle (1993)**, e uma generalizacao notavel que **aninha sete modelos de volatilidade** como casos especiais atraves do parametro de potencia $\delta$. A formulacao modela $\sigma_t^\delta$ ao inves de $\sigma_t^2$, permitindo que os dados determinem a transformacao de potencia otima.

O artigo original de Ding, Granger e Engle (1993) demonstrou que a autocorrelacao de $|r_t|^d$ e maximizada para $d \approx 1$ (e nao $d = 2$), sugerindo que a especificacao quadratica do GARCH padrao pode nao ser otima. O APARCH deixa os dados "falarem" sobre qual potencia e mais adequada.

**Quando usar:**

- Quando se deseja flexibilidade maxima na modelagem de volatilidade
- Para testar se a especificacao quadratica ($\delta = 2$) e adequada
- Comparacoes formais entre diferentes modelos GARCH (via restricoes em $\delta$)
- Quando modelos mais simples (GARCH, GJR) apresentam diagnosticos insatisfatorios

**Modelos aninhados:**

| $\delta$ | $\gamma_i$ | Modelo resultante |
|----------|------------|-------------------|
| $\delta = 2$ | $\gamma_i = 0$ | GARCH |
| $\delta = 2$ | $\gamma_i \neq 0$ | GJR-GARCH |
| $\delta = 1$ | $\gamma_i = 0$ | AVARCH (Taylor, 1986) |
| $\delta = 1$ | $\gamma_i \neq 0$ | TARCH (Zakoian, 1994) |
| $\delta$ livre | $\gamma_i = 0$ | Power GARCH simetrico |
| $\delta$ livre | $\gamma_i \neq 0$ | APARCH completo |

## Formulacao Matematica

### Equacao da Media

$$r_t = \mu + \epsilon_t, \qquad \epsilon_t = \sigma_t z_t, \qquad z_t \sim D(0, 1)$$

### Equacao da Variancia Condicional

$$\sigma_t^\delta = \omega + \sum_{i=1}^{q} \alpha_i (|\epsilon_{t-i}| - \gamma_i \epsilon_{t-i})^\delta + \sum_{j=1}^{p} \beta_j \sigma_{t-j}^\delta$$

onde:

| Parametro | Descricao | Restricao |
|-----------|-----------|-----------|
| $\omega$ | Intercepto | $\omega > 0$ |
| $\alpha_i$ | Coeficientes de reacao a choques | $\alpha_i \geq 0$ |
| $\gamma_i$ | Parametros de assimetria (leverage) | $-1 < \gamma_i < 1$ |
| $\beta_j$ | Coeficientes de persistencia | $\beta_j \geq 0$ |
| $\delta$ | Potencia do desvio condicional | $\delta > 0$ |
| $p$ | Ordem GARCH (lags de $\sigma^\delta$) | $p \geq 1$ |
| $q$ | Ordem ARCH (lags dos choques) | $q \geq 1$ |

### Caso Especial: APARCH(1,1)

$$\sigma_t^\delta = \omega + \alpha (|\epsilon_{t-1}| - \gamma \epsilon_{t-1})^\delta + \beta \sigma_{t-1}^\delta$$

**Impacto assimetrico do termo** $(|\epsilon_{t-1}| - \gamma \epsilon_{t-1})$:

- **Choque positivo** ($\epsilon_{t-1} > 0$): $(1 - \gamma)|\epsilon_{t-1}|$
- **Choque negativo** ($\epsilon_{t-1} < 0$): $(1 + \gamma)|\epsilon_{t-1}|$

Se $\gamma > 0$, choques negativos sao amplificados pelo fator $(1 + \gamma)/(1 - \gamma)$.

### O Parametro $\delta$

O parametro $\delta$ controla a **transformacao de potencia** aplicada ao desvio-padrao condicional:

| Valor de $\delta$ | Transformacao | Modelo equivalente |
|-------------------|---------------|--------------------|
| $\delta = 2$ | Variancia condicional ($\sigma_t^2$) | GARCH / GJR-GARCH |
| $\delta = 1$ | Desvio-padrao condicional ($\sigma_t$) | TARCH / AVARCH |
| $\delta$ livre | Potencia otima estimada dos dados | APARCH completo |

!!! note "Resultado empirico de Ding, Granger e Engle (1993)"
    Em seu estudo original com retornos diarios do S&P 500 (1928--1991), os autores encontraram $\hat{\delta} \approx 1.43$, entre as especificacoes de variancia ($\delta = 2$) e desvio-padrao ($\delta = 1$). Isso sugere que a transformacao quadratica usada pelo GARCH padrao nao e necessariamente otima.

### Condicao de Estacionariedade

Para o APARCH(1,1) com inovacoes Normais:

$$\alpha E[(|z_t| - \gamma z_t)^\delta] + \beta < 1$$

onde a esperanca $E[(|z_t| - \gamma z_t)^\delta]$ depende da distribuicao de $z_t$ e do valor de $\delta$.

## Quick Example

```python
from archbox import APARCH
from archbox.datasets import load_dataset

# Carregar retornos
sp500 = load_dataset('sp500')

# Estimar APARCH(1,1) - delta e estimado livremente
model = APARCH(sp500['returns'], p=1, q=1)
results = model.fit()
print(results.summary())
```

??? example "Output esperado"
    ```
    ======================================================================
                          Volatility Model Results
    ======================================================================
    Model:            APARCH
    Distribution:     Normal
    Observations:     2000
    Log-Likelihood:   3156.4523
    AIC:              -6302.9046
    BIC:              -6274.5407
    Converged:        True
    ----------------------------------------------------------------------
    Parameter         Estimate      Std Err      t-value      p-value
    ----------------------------------------------------------------------
    omega            0.000085     0.000032       2.6543       0.0079
    alpha[1]         0.068432     0.012876       5.3148       0.0000
    gamma[1]         0.482345     0.098765       4.8838       0.0000
    beta[1]          0.912567     0.015432      59.1367       0.0000
    delta            1.432100     0.198765       7.2054       0.0000
    ----------------------------------------------------------------------
    Persistence:      0.978234
    Half-life:        31.47 periods
    Uncond. Variance: 8.654e-04
    Uncond. Vol:      2.942e-02
    ======================================================================
    ```

## Guia Detalhado

### Parametros do Construtor

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | array-like | obrigatorio | Serie de retornos |
| `p` | int | `1` | Ordem GARCH (lags de $\sigma^\delta$) |
| `q` | int | `1` | Ordem ARCH (lags dos choques) |
| `mean` | str | `"constant"` | Modelo de media: `"constant"` ou `"zero"` |
| `dist` | str | `"normal"` | Distribuicao condicional: `"normal"` |

!!! note "Parametro delta"
    O parametro $\delta$ nao e especificado no construtor -- ele e **estimado livremente** a partir dos dados durante `fit()`. O valor inicial padrao e $\delta_0 = 2.0$ (equivalente ao GARCH).

### Parametros de `fit()`

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `method` | str | `"mle"` | Metodo de estimacao |
| `starting_values` | ndarray | `None` | Valores iniciais customizados |
| `disp` | bool | `True` | Exibir progresso da otimizacao |

### Exemplo Completo

```python
from archbox import APARCH
from archbox.datasets import load_dataset

# 1. Carregar dados
sp500 = load_dataset('sp500')
returns = sp500['returns']

# 2. Estimar APARCH(1,1)
model = APARCH(returns, p=1, q=1)
results = model.fit()

# 3. Extrair parametros
omega = results.params[0]
alpha = results.params[1]
gamma = results.params[2]
beta  = results.params[3]
delta = results.params[4]

print(f"omega:  {omega:.6f}")
print(f"alpha:  {alpha:.6f}")
print(f"gamma:  {gamma:.6f}  (assimetria)")
print(f"beta:   {beta:.6f}  (persistencia)")
print(f"delta:  {delta:.4f}  (potencia)")

# 4. Interpretar delta
if abs(delta - 2.0) < 0.1:
    print("\ndelta ≈ 2: especificacao quadratica (GARCH-like)")
elif abs(delta - 1.0) < 0.1:
    print("\ndelta ≈ 1: especificacao em desvio-padrao (TARCH-like)")
else:
    print(f"\ndelta = {delta:.2f}: potencia intermediaria estimada dos dados")

# 5. Razao de impacto assimetrico
ratio = (1 + gamma) / (1 - gamma)
print(f"\nRazao de impacto (neg/pos): {ratio:.2f}x")

# 6. Metricas de volatilidade
print(f"\nPersistencia: {results.persistence():.6f}")
print(f"Meia-vida: {results.half_life():.1f} periodos")
print(f"Variancia incondicional: {results.unconditional_variance():.6e}")

# 7. Previsao
forecast = results.forecast(horizon=10)
print("\nVolatilidade prevista (proximos 10 dias):")
print(forecast['volatility'])
```

### Resultados

| Atributo | Descricao |
|----------|-----------|
| `results.params` | Parametros estimados: $[\omega, \alpha_1, \gamma_1, \beta_1, \delta]$ |
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
| `results.persistence()` | Persistencia do modelo |
| `results.half_life()` | Meia-vida dos choques de volatilidade |
| `results.unconditional_variance()` | Variancia incondicional de longo prazo |
| `results.forecast(horizon)` | Previsao de variancia/volatilidade |
| `results.summary()` | Tabela formatada de resultados |
| `results.plot("volatility")` | Grafico de retornos e volatilidade |
| `results.plot("residuals")` | Grafico de residuos padronizados |
| `results.to_dataframe()` | Exportar parametros como DataFrame |

## Interpretacao

### Casos Especiais e Testes de Restricao

O APARCH aninha diversos modelos como casos especiais. Isso permite **testes formais** via restricao de parametros:

| Restricao | Modelo aninhado | Teste |
|-----------|----------------|-------|
| $\delta = 2$, $\gamma = 0$ | GARCH(1,1) | LR test: $H_0: \delta = 2, \gamma = 0$ |
| $\delta = 2$ | GJR-GARCH(1,1) | LR test: $H_0: \delta = 2$ |
| $\delta = 1$, $\gamma = 0$ | AVARCH (Taylor) | LR test: $H_0: \delta = 1, \gamma = 0$ |
| $\delta = 1$ | TARCH (Zakoian) | LR test: $H_0: \delta = 1$ |
| $\gamma = 0$ | Power GARCH simetrico | t-test: $H_0: \gamma = 0$ |

```python
# Testar se delta = 2 (GARCH padrao e adequado)
delta_hat = results.params[4]
delta_se = results.se[4]
t_stat = (delta_hat - 2.0) / delta_se
print(f"Teste H0: delta = 2")
print(f"  delta = {delta_hat:.4f}, SE = {delta_se:.4f}")
print(f"  t = {t_stat:.4f}")
if abs(t_stat) > 1.96:
    print("  Rejeita H0: especificacao quadratica nao e otima")
else:
    print("  Nao rejeita H0: GARCH padrao pode ser suficiente")
```

### Flexibilidade vs Parcimonia

!!! warning "Trade-off"
    O APARCH tem **um parametro a mais** que o GJR-GARCH ($\delta$). Embora mais flexivel, este parametro adicional pode causar:

    - **Dificuldades de convergencia** em amostras pequenas ($T < 500$)
    - **Multicolinearidade** entre $\delta$ e os demais parametros
    - **Overfitting**: BIC pode penalizar o parametro extra

    **Regra pratica**: Use APARCH quando $T > 1000$ e quando ha evidencia de que $\delta \neq 2$ (via teste t ou comparacao de BIC com GJR-GARCH).

### Interpretacao do Parametro $\gamma$

No APARCH, $\gamma$ tem a mesma interpretacao de assimetria que no GJR, mas dentro da transformacao de potencia:

- $\gamma > 0$: efeito leverage (choques negativos amplificados)
- $\gamma = 0$: simetria (Power GARCH)
- $|\gamma|$ proximo de 1: assimetria extrema

```python
gamma = results.params[2]
ratio = (1 + gamma) / (1 - gamma)
print(f"gamma = {gamma:.4f}")
print(f"Amplificacao relativa (neg/pos): {ratio:.2f}x")
```

### Comparacao de Modelos

```python
from archbox import GARCH, GJRGARCH, APARCH
from archbox.datasets import load_dataset

sp500 = load_dataset('sp500')
returns = sp500['returns']

# Estimar os tres modelos
garch_res = GARCH(returns, p=1, q=1).fit()
gjr_res   = GJRGARCH(returns, p=1, q=1).fit()
aparch_res = APARCH(returns, p=1, q=1).fit()

# Comparar via criterios de informacao
print(f"{'Modelo':<15} {'LogLik':>10} {'AIC':>12} {'BIC':>12} {'Params':>7}")
print("-" * 58)
for name, res in [("GARCH", garch_res), ("GJR-GARCH", gjr_res), ("APARCH", aparch_res)]:
    print(f"{name:<15} {res.loglike:>10.2f} {res.aic:>12.2f} {res.bic:>12.2f} {len(res.params):>7}")
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

### Sign Bias Test

```python
from archbox.diagnostics import sign_bias_test

sb_result = sign_bias_test(results.resid)
print(sb_result)
```

### Workflow Completo de Diagnostico

```python
from archbox import APARCH
from archbox.datasets import load_dataset
from archbox.diagnostics import ljung_box_test, arch_lm_test, sign_bias_test

# 1. Estimar modelo
sp500 = load_dataset('sp500')
model = APARCH(sp500['returns'], p=1, q=1)
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
    from archbox import APARCH
    from archbox.datasets import load_dataset

    sp500 = load_dataset('sp500')
    model = APARCH(sp500['returns'], p=1, q=1)
    results = model.fit()
    print(results.summary())

    # Verificar delta estimado
    print(f"delta = {results.params[-1]:.4f}")

    # Previsao
    forecast = results.forecast(horizon=10)
    ```

=== "R (rugarch)"

    ```r
    library(rugarch)

    spec <- ugarchspec(
      variance.model = list(model = "apARCH", garchOrder = c(1, 1)),
      mean.model = list(armaOrder = c(0, 0), include.mean = TRUE),
      distribution.model = "norm"
    )

    fit <- ugarchfit(spec = spec, data = returns)
    show(fit)

    # Extrair delta estimado
    coef(fit)["delta"]

    # News impact curve
    ni <- newsimpact(fit)
    plot(ni)

    # Previsao
    forecast <- ugarchforecast(fit, n.ahead = 10)
    ```

=== "Python (arch)"

    ```python
    from arch import arch_model

    # Em arch, APARCH nao e diretamente suportado
    # Use o=1 para assimetria e power= para delta fixo
    am = arch_model(returns, vol='APARCH', p=1, o=1, q=1, dist='Normal')
    res = am.fit()
    print(res.summary())
    ```

| Funcionalidade | ArchBox | rugarch (R) | arch (Python) |
|---------------|---------|-------------|---------------|
| Especificacao | `APARCH(y, p=1, q=1)` | `ugarchspec(model="apARCH")` | `arch_model(y, vol='APARCH')` |
| Estimacao | `model.fit()` | `ugarchfit(spec, data)` | `am.fit()` |
| Previsao | `results.forecast(h)` | `ugarchforecast(fit, n.ahead=h)` | `res.forecast(horizon=h)` |
| Delta estimado | `results.params[-1]` | `coef(fit)['delta']` | `res.params['delta']` |
| Persistencia | `results.persistence()` | `persistence(fit)` | Manual |
| Meia-vida | `results.half_life()` | Manual | Manual |

## References

- Ding, Z., Granger, C. W. J., & Engle, R. F. (1993). A Long Memory Property of Stock Market Returns and a New Model. *Journal of Empirical Finance*, 1(1), 83--106.
- Taylor, S. J. (1986). *Modelling Financial Time Series*. Wiley.
- Zakoian, J.-M. (1994). Threshold Heteroskedastic Models. *Journal of Economic Dynamics and Control*, 18(5), 931--955.
- Francq, C., & Zakoian, J.-M. (2019). *GARCH Models: Structure, Statistical Inference and Financial Applications* (2nd ed.). Wiley.
- He, C., & Terasvirta, T. (1999). Properties of Moments of a Family of GARCH Processes. *Journal of Econometrics*, 92(1), 173--192.

## See Also

- [GARCH(p,q)](garch.md) -- Modelo simetrico padrao (caso especial: $\delta = 2$, $\gamma = 0$)
- [GJR-GARCH](gjr-garch.md) -- Modelo assimetrico com indicadora (caso especial: $\delta = 2$)
- [EGARCH](egarch.md) -- Modelo assimetrico com log-variancia
- [Distribuicoes Condicionais](../distributions/index.md) -- Escolha da distribuicao para os erros
- [Diagnosticos: Sign Bias](../../diagnostics/sign-bias.md) -- Teste de assimetria nos residuos
- [Diagnosticos: ARCH-LM](../../diagnostics/arch-lm.md) -- Teste para efeitos ARCH residuais
