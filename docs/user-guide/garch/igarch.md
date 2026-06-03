---
title: "IGARCH"
description: "Integrated GARCH - GARCH model with unit root in variance, where shocks have permanent effects on conditional variance."
---

# IGARCH

!!! info "Quick Reference"
    **Class:** `archbox.models.igarch.IGARCH`
    **Import:** `from archbox import IGARCH`
    **R equivalent:** `rugarch::ugarchspec(variance.model = list(model = "iGARCH", garchOrder = c(1,1)))`
    **Python equivalent:** `arch.arch_model(returns, vol='GARCH', p=1, q=1)` com restricao $\alpha + \beta = 1$

## Overview

O modelo IGARCH (Integrated GARCH), introduzido por **Engle & Bollerslev (1986)**, e o caso limite do GARCH onde a soma dos coeficientes ARCH e GARCH e exatamente igual a 1 ($\alpha + \beta = 1$). Isso implica que choques na variancia condicional tem **efeito permanente** -- a variancia nao reverte a uma media de longo prazo.

O IGARCH pode ser visto como o analogo na variancia de um random walk na media: a melhor previsao de longo prazo da variancia futura e a variancia condicional corrente, independente do horizonte.

!!! warning "Variancia incondicional indefinida"
    No IGARCH, a variancia incondicional $E[\sigma_t^2]$ **nao existe** (ou e infinita). Isso significa que nao ha um nivel de "equilibrio" para o qual a volatilidade retorna. Na pratica, previsoes de longo prazo sao dominadas pela ultima observacao, nao por uma media historica.

**Quando usar:**

- Series com **persistencia muito alta** (GARCH estima $\alpha + \beta > 0.99$)
- Quando nao ha evidencia de reversao a media na volatilidade
- Como benchmark para testar se a persistencia e verdadeiramente unitaria
- Modelagem de risco com horizonte curto onde a reversao a media e irrelevante
- Metodo de calculo do **RiskMetrics** (caso especial com $\omega = 0$)

## Formulacao Matematica

### Equacao da Media

$$r_t = \mu + \epsilon_t, \qquad \epsilon_t = \sigma_t z_t, \qquad z_t \sim D(0, 1)$$

### Equacao da Variancia Condicional

O IGARCH(1,1) impoe a restricao $\alpha + \beta = 1$:

$$\sigma_t^2 = \omega + \alpha \epsilon_{t-1}^2 + (1 - \alpha) \sigma_{t-1}^2$$

onde:

| Parametro | Descricao | Restricao |
|-----------|-----------|-----------|
| $\omega$ | Intercepto | $\omega \geq 0$ |
| $\alpha$ | Coeficiente ARCH | $0 < \alpha < 1$ |
| $\beta = 1 - \alpha$ | Coeficiente GARCH (imposto) | $\beta = 1 - \alpha$ |

**Condicao de integracao:** $\alpha + \beta = 1$ (imposta, nao estimada separadamente)

### Caso Especial: RiskMetrics (EWMA)

Quando $\omega = 0$, o IGARCH se reduz ao modelo **Exponentially Weighted Moving Average (EWMA)**:

$$\sigma_t^2 = \lambda \sigma_{t-1}^2 + (1 - \lambda) \epsilon_{t-1}^2$$

onde $\lambda = \beta = 1 - \alpha$. O J.P. Morgan RiskMetrics usa $\lambda = 0.94$ para dados diarios.

!!! tip "IGARCH vs RiskMetrics"
    O IGARCH com $\omega > 0$ permite um leve drift na variancia condicional ao longo do tempo, enquanto o RiskMetrics puro ($\omega = 0$) e um filtro EWMA sem intercepto. Na pratica, a diferenca e pequena, mas $\omega > 0$ oferece mais flexibilidade.

### Previsao de Variancia

No IGARCH(1,1), a previsao $h$ passos a frente e:

$$E_t[\sigma_{t+h}^2] = \sigma_{t+1|t}^2 + (h - 1) \omega$$

A previsao cresce **linearmente** com o horizonte (via $\omega$), ao contrario do GARCH onde converge para a variancia incondicional:

```
Previsao de σ²

GARCH                         IGARCH
│          ─────────          │              ╱
│      ╱                      │            ╱
│    ╱                        │          ╱
│  ╱    var incondicional     │        ╱
│╱                            │      ╱
├──────────────── h           │    ╱
│  Converge                   │  ╱
│                             │╱
                              ├──────────────── h
                              │  Cresce linearmente
```

### Forma Geral: IGARCH(p,q)

$$\sigma_t^2 = \omega + \sum_{i=1}^{q} \alpha_i \epsilon_{t-i}^2 + \sum_{j=1}^{p} \beta_j \sigma_{t-j}^2$$

com restricao: $\sum_{i=1}^{q} \alpha_i + \sum_{j=1}^{p} \beta_j = 1$

## Quick Example

```python
from archbox import IGARCH
from archbox.datasets import load_dataset

# Carregar retornos
sp500 = load_dataset('sp500')

# Estimar IGARCH(1,1)
model = IGARCH(sp500['returns'], p=1, q=1)
results = model.fit()
print(results.summary())
```

??? example "Output esperado"
    ```
    ======================================================================
                          Volatility Model Results
    ======================================================================
    Model:            IGARCH(1,1)
    Distribution:     Normal
    Observations:     2000
    Log-Likelihood:   3142.5678
    AIC:              -6281.1356
    BIC:              -6269.8476
    Converged:        True
    ----------------------------------------------------------------------
    Parameter         Estimate      Std Err      t-value      p-value
    ----------------------------------------------------------------------
    omega             0.001234     0.000567       2.1764       0.0295
    alpha[1]          0.058432     0.012345       4.7333       0.0000
    beta[1]           0.941568     (imposed)        ---          ---
    ----------------------------------------------------------------------
    Persistence:      1.000000 (unit root)
    Note: Unconditional variance does not exist
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
| `dist` | str | `"normal"` | Distribuicao condicional |

### Parametros de `fit()`

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `method` | str | `"mle"` | Metodo de estimacao |
| `starting_values` | ndarray | `None` | Valores iniciais customizados |
| `disp` | bool | `True` | Exibir progresso da otimizacao |

### Exemplo Completo

```python
from archbox import IGARCH, GARCH
from archbox.datasets import load_dataset

# 1. Carregar dados
sp500 = load_dataset('sp500')
returns = sp500['returns']

# 2. Primeiro, verificar persistencia no GARCH
garch = GARCH(returns, p=1, q=1)
garch_res = garch.fit()
persistence = garch_res.persistence()
print(f"Persistencia GARCH: {persistence:.6f}")
print(f"  alpha + beta = {persistence:.6f}")
print(f"  Proximo de 1? {'Sim -> considerar IGARCH' if persistence > 0.99 else 'Nao'}")

# 3. Estimar IGARCH
igarch = IGARCH(returns, p=1, q=1)
igarch_res = igarch.fit()

# 4. Comparar
print(f"\n=== Comparacao ===")
print(f"GARCH  - AIC: {garch_res.aic:.4f}, alpha+beta: {persistence:.6f}")
print(f"IGARCH - AIC: {igarch_res.aic:.4f}, alpha+beta: 1.000000 (imposto)")

# 5. Previsao
forecast = igarch_res.forecast(horizon=10)
print("\nPrevisao de volatilidade (proximos 10 dias):")
print(forecast['volatility'])
```

### Resultados

| Atributo | Descricao |
|----------|-----------|
| `results.params` | Parametros estimados (ndarray) |
| `results.se` | Erros-padrao robustos |
| `results.tvalues` | Estatisticas t |
| `results.pvalues` | p-valores bilaterais |
| `results.loglike` | Log-verossimilhanca |
| `results.aic` | Criterio de Informacao de Akaike |
| `results.bic` | Criterio de Informacao Bayesiano |
| `results.conditional_volatility` | Serie de $\sigma_t$ |
| `results.resid` | Residuos padronizados ($z_t = \epsilon_t / \sigma_t$) |

| Metodo | Descricao |
|--------|-----------|
| `results.persistence()` | Retorna 1.0 (por construcao) |
| `results.forecast(horizon)` | Previsao de variancia/volatilidade |
| `results.summary()` | Tabela formatada de resultados |
| `results.plot("volatility")` | Grafico de retornos e volatilidade |
| `results.plot("residuals")` | Grafico de residuos padronizados |
| `results.to_dataframe()` | Exportar parametros como DataFrame |

## Interpretacao

### Persistencia Infinita

!!! warning "Implicacoes da persistencia unitaria"
    Com $\alpha + \beta = 1$:

    1. **Variancia incondicional nao existe**: nao ha nivel de "equilibrio" para a volatilidade
    2. **Choques sao permanentes**: um aumento de volatilidade nao se dissipa
    3. **Previsao**: $E_t[\sigma_{t+h}^2] = \sigma_{t+1|t}^2 + (h-1)\omega$ -- cresce linearmente
    4. **Meia-vida**: indefinida (infinita)

### Comparacao: GARCH vs IGARCH

| Propriedade | GARCH ($\alpha + \beta < 1$) | IGARCH ($\alpha + \beta = 1$) |
|-------------|------------------------------|-------------------------------|
| Variancia incondicional | $\sigma^2 = \frac{\omega}{1 - \alpha - \beta}$ | Nao existe |
| Reversao a media | Sim | Nao |
| Previsao longo prazo | Converge para $\sigma^2$ | Cresce linearmente |
| Meia-vida | Finita | Infinita |
| Choques | Transitorios | Permanentes |

### Teste de Raiz Unitaria na Variancia

Para testar se a persistencia e verdadeiramente unitaria, compare os modelos:

```python
from archbox import GARCH, IGARCH
from archbox.datasets import load_dataset

sp500 = load_dataset('sp500')
returns = sp500['returns']

garch_res = GARCH(returns, p=1, q=1).fit()
igarch_res = IGARCH(returns, p=1, q=1).fit()

# Teste de razao de verossimilhanca
lr_stat = 2 * (garch_res.loglike - igarch_res.loglike)
print(f"LR statistic: {lr_stat:.4f}")
print(f"  H0: alpha + beta = 1 (IGARCH)")
print(f"  H1: alpha + beta < 1 (GARCH)")

# Sob H0, LR ~ chi2(1)
from scipy import stats
p_value = 1 - stats.chi2.cdf(lr_stat, df=1)
print(f"  p-valor: {p_value:.4f}")
print(f"  {'Rejeita H0 -> GARCH' if p_value < 0.05 else 'Nao rejeita -> IGARCH'}")
```

### Relacao com RiskMetrics

```python
from archbox import IGARCH
from archbox.datasets import load_dataset

sp500 = load_dataset('sp500')
returns = sp500['returns']

# IGARCH padrao (com omega)
igarch_res = IGARCH(returns, p=1, q=1).fit()

# Equivalente RiskMetrics: lambda = 0.94
# sigma2_t = 0.94 * sigma2_{t-1} + 0.06 * eps2_{t-1}
print(f"IGARCH alpha: {igarch_res.params['alpha']:.4f}")
print(f"IGARCH beta:  {1 - igarch_res.params['alpha']:.4f}")
print(f"RiskMetrics lambda: 0.94 (fixo)")
```

## Diagnosticos

### Ljung-Box nos Residuos Padronizados ao Quadrado

```python
from archbox.diagnostics import ljung_box_test

lb_result = ljung_box_test(igarch_res.resid**2, lags=10)
print(f"Ljung-Box Q(10): {lb_result.statistic:.4f}")
print(f"p-valor: {lb_result.pvalue:.4f}")
```

### Teste ARCH-LM

```python
from archbox.diagnostics import arch_lm_test

lm_result = arch_lm_test(igarch_res.resid, lags=5)
print(f"ARCH-LM(5): {lm_result.statistic:.4f}")
print(f"p-valor: {lm_result.pvalue:.4f}")
```

### Workflow Completo de Diagnostico

```python
from archbox import IGARCH
from archbox.datasets import load_dataset
from archbox.diagnostics import ljung_box_test, arch_lm_test

# 1. Estimar modelo
sp500 = load_dataset('sp500')
model = IGARCH(sp500['returns'], p=1, q=1)
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

# 4. Visualizacao
results.plot("volatility")
results.plot("residuals")
```

## Equivalentes em R e Python

=== "ArchBox"

    ```python
    from archbox import IGARCH
    from archbox.datasets import load_dataset

    sp500 = load_dataset('sp500')
    model = IGARCH(sp500['returns'], p=1, q=1)
    results = model.fit()
    print(results.summary())

    # Previsao
    forecast = results.forecast(horizon=10)
    ```

=== "R (rugarch)"

    ```r
    library(rugarch)

    spec <- ugarchspec(
      variance.model = list(model = "iGARCH", garchOrder = c(1, 1)),
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
    from arch.univariate import GARCH

    # arch nao tem IGARCH nativo; usar restricao manual
    am = arch_model(returns, vol='GARCH', p=1, q=1, dist='Normal')
    res = am.fit(constraints={'alpha + beta = 1'})
    print(res.summary())
    ```

| Funcionalidade | ArchBox | rugarch (R) | arch (Python) |
|---------------|---------|-------------|---------------|
| Especificacao | `IGARCH(y, p=1, q=1)` | `ugarchspec(model="iGARCH")` | Manual (restricao) |
| Estimacao | `model.fit()` | `ugarchfit(spec, data)` | `am.fit(constraints=...)` |
| Previsao | `results.forecast(h)` | `ugarchforecast(fit, n.ahead=h)` | `res.forecast(horizon=h)` |
| Persistencia | `results.persistence()` -> 1.0 | `persistence(fit)` -> 1.0 | Manual |

## References

- Engle, R. F., & Bollerslev, T. (1986). Modelling the Persistence of Conditional Variances. *Econometric Reviews*, 5(1), 1--50.
- Nelson, D. B. (1990). Stationarity and Persistence in the GARCH(1,1) Model. *Econometric Theory*, 6(3), 318--334.
- J.P. Morgan (1996). *RiskMetrics -- Technical Document* (4th ed.).
- Francq, C., & Zakoian, J.-M. (2019). *GARCH Models: Structure, Statistical Inference and Financial Applications* (2nd ed.). Wiley.

## See Also

- [GARCH(p,q)](garch.md) -- Modelo simetrico padrao
- [FIGARCH](figarch.md) -- Modelo fracionario (caso intermediario, $0 < d < 1$)
- [Distribuicoes Condicionais](../distributions/index.md) -- Escolha da distribuicao para os erros
- [Diagnosticos: ARCH-LM](../../diagnostics/arch-lm.md) -- Teste para efeitos ARCH residuais
- [Diagnosticos: Ljung-Box](../../diagnostics/ljung-box.md) -- Teste de autocorrelacao nos residuos
