---
title: "FIGARCH"
description: "Fractionally Integrated GARCH - captures long memory in volatility through the fractional differencing operator."
---

# FIGARCH

!!! info "Quick Reference"
    **Class:** `archbox.models.figarch.FIGARCH`
    **Import:** `from archbox import FIGARCH`
    **R equivalent:** `rugarch::ugarchspec(variance.model = list(model = "fiGARCH", garchOrder = c(1,1)))`
    **Python equivalent:** `arch.arch_model(returns, vol='FIGARCH', p=1, q=1)`

## Overview

O modelo FIGARCH (Fractionally Integrated GARCH), proposto por **Baillie, Bollerslev & Mikkelsen (1996)**, estende o GARCH padrao para capturar **memoria longa** na volatilidade condicional. Enquanto o GARCH convencional assume decaimento exponencial na autocorrelacao dos retornos ao quadrado, o FIGARCH permite decaimento hiperbolico -- mais lento e consistente com evidencia empirica.

A ideia central e que a volatilidade de ativos financeiros exibe **persistencia intermediaria** entre o GARCH (memoria curta, $d=0$) e o IGARCH (raiz unitaria, $d=1$). O parametro fracionario $d \in (0, 1)$ controla a taxa de decaimento da memoria.

**Quando usar:**

- Series com autocorrelacao lenta nos retornos ao quadrado ($\epsilon_t^2$)
- Quando o teste KPSS ou GPH sugere memoria longa na volatilidade
- Quando a persistencia estimada no GARCH e muito proxima de 1
- Modelagem de taxas de cambio, indices de acoes com horizontes longos
- Quando GARCH subestima e IGARCH superestima a persistencia

## Formulacao Matematica

### Equacao da Media

$$r_t = \mu + \epsilon_t, \qquad \epsilon_t = \sigma_t z_t, \qquad z_t \sim D(0, 1)$$

onde $r_t$ sao os retornos, $\mu$ e a media condicional, $\sigma_t$ e o desvio-padrao condicional, e $z_t$ sao inovacoes padronizadas.

### Equacao da Variancia Condicional

O FIGARCH(1, d, 1) e definido usando o operador de diferenca fracionaria:

$$\sigma_t^2 = \omega + \left[1 - \beta(L) - (1 - \phi(L))(1 - L)^d\right] \epsilon_t^2 + \beta(L) \sigma_t^2$$

onde:

- $(1 - L)^d$ e o **operador de diferenca fracionaria** com $0 \leq d \leq 1$
- $L$ e o operador de defasagem: $L^k x_t = x_{t-k}$

A expansao de $(1-L)^d$ em serie infinita e:

$$(1-L)^d = \sum_{k=0}^{\infty} \binom{d}{k} (-L)^k = 1 - dL - \frac{d(1-d)}{2!}L^2 - \frac{d(1-d)(2-d)}{3!}L^3 - \cdots$$

| Parametro | Descricao | Restricao |
|-----------|-----------|-----------|
| $\omega$ | Intercepto (nivel base da variancia) | $\omega > 0$ |
| $d$ | Parametro de integracao fracionaria | $0 \leq d \leq 1$ |
| $\phi$ | Coeficiente ARCH do filtro fracionario | Estacionariedade |
| $\beta$ | Coeficiente GARCH (persistencia) | $0 \leq \beta < 1$ |

### Casos Especiais

| Valor de $d$ | Modelo | Memoria |
|--------------|--------|---------|
| $d = 0$ | GARCH(1,1) | Curta (decaimento exponencial) |
| $0 < d < 1$ | FIGARCH(1, d, 1) | Longa (decaimento hiperbolico) |
| $d = 1$ | IGARCH(1,1) | Infinita (raiz unitaria) |

### Funcao de Autocorrelacao

A chave da memoria longa e o comportamento da ACF dos retornos ao quadrado:

- **GARCH:** $\rho(k) \sim c \cdot r^k$ (decaimento **exponencial**)
- **FIGARCH:** $\rho(k) \sim c \cdot k^{2d-1}$ (decaimento **hiperbolico**)

```
ACF de ε²

GARCH                         FIGARCH
│                              │
│█                             │█
│█                             │██
│█░                            │███
│█░░                           │████░
│█░░░░░░                       │█████░░░░░░
│█░░░░░░░░░░░░                 │██████░░░░░░░░░░░░░
├──────────── Lag              ├──────────────────── Lag
    Decaimento rapido              Decaimento lento
    (exponencial)                  (hiperbolico)
```

!!! note "Intuicao"
    No GARCH, um choque de volatilidade e "esquecido" exponencialmente rapido. No FIGARCH, o efeito de choques passados persiste por muito mais tempo -- a autocorrelacao decai como uma funcao potencia, nao exponencial. Isso e consistente com a observacao empirica de que clusters de volatilidade podem durar semanas ou meses.

## Quick Example

```python
from archbox import FIGARCH
from archbox.datasets import load_dataset

# Carregar retornos
sp500 = load_dataset('sp500')

# Estimar FIGARCH(1,d,1)
model = FIGARCH(sp500['returns'], p=1, q=1)
results = model.fit()
print(results.summary())
```

??? example "Output esperado"
    ```
    ======================================================================
                          Volatility Model Results
    ======================================================================
    Model:            FIGARCH(1,d,1)
    Distribution:     Normal
    Observations:     2000
    Log-Likelihood:   3156.8745
    AIC:              -6305.7490
    BIC:              -6283.1731
    Converged:        True
    ----------------------------------------------------------------------
    Parameter         Estimate      Std Err      t-value      p-value
    ----------------------------------------------------------------------
    omega             0.012345     0.004567       2.7034       0.0069
    d                 0.423567     0.078234       5.4143       0.0000
    phi[1]            0.198432     0.089123       2.2265       0.0260
    beta[1]           0.512345     0.098765       5.1876       0.0000
    ----------------------------------------------------------------------
    Fractional d:     0.423567
    Persistence:      Long memory (hyperbolic decay)
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
| `d_init` | float | `0.3` | Valor inicial para o parametro $d$ |
| `disp` | bool | `True` | Exibir progresso da otimizacao |

### Exemplo Completo

```python
from archbox import FIGARCH, GARCH
from archbox.datasets import load_dataset
from archbox.diagnostics import ljung_box_test, arch_lm_test

# 1. Carregar dados
sp500 = load_dataset('sp500')
returns = sp500['returns']

# 2. Comparar GARCH vs FIGARCH
garch = GARCH(returns, p=1, q=1)
garch_res = garch.fit()

figarch = FIGARCH(returns, p=1, q=1)
figarch_res = figarch.fit()

# 3. Comparar criterios de informacao
print("=== Comparacao GARCH vs FIGARCH ===")
print(f"GARCH   - AIC: {garch_res.aic:.4f}, BIC: {garch_res.bic:.4f}")
print(f"FIGARCH - AIC: {figarch_res.aic:.4f}, BIC: {figarch_res.bic:.4f}")

# 4. Parametro de memoria longa
print(f"\nParametro d: {figarch_res.params['d']:.4f}")
print(f"  d=0 -> GARCH, d=1 -> IGARCH")
print(f"  Estimado: memoria {'longa' if figarch_res.params['d'] > 0.1 else 'curta'}")

# 5. ACF dos residuos ao quadrado
import numpy as np

z_garch = garch_res.resid**2
z_figarch = figarch_res.resid**2

print("\nACF de residuos ao quadrado (lag 20):")
print(f"  GARCH:   {np.corrcoef(z_garch[20:], z_garch[:-20])[0,1]:.4f}")
print(f"  FIGARCH: {np.corrcoef(z_figarch[20:], z_figarch[:-20])[0,1]:.4f}")
```

### Resultados

| Atributo | Descricao |
|----------|-----------|
| `results.params` | Parametros estimados (ndarray) |
| `results.params['d']` | Parametro fracionario $d$ |
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
| `results.forecast(horizon)` | Previsao de variancia/volatilidade |
| `results.summary()` | Tabela formatada de resultados |
| `results.plot("volatility")` | Grafico de retornos e volatilidade |
| `results.plot("residuals")` | Grafico de residuos padronizados |
| `results.to_dataframe()` | Exportar parametros como DataFrame |

## Interpretacao

### Parametro de Integracao Fracionaria ($d$)

O parametro $d$ e o centro do modelo FIGARCH -- ele controla a **velocidade de decaimento** da memoria na volatilidade:

| Valor de $d$ | Interpretacao | Implicacao Pratica |
|--------------|---------------|-------------------|
| $d \approx 0$ | Memoria curta | GARCH padrao e suficiente |
| $0.2 < d < 0.5$ | Memoria longa moderada | Tipico de retornos diarios |
| $0.5 < d < 0.8$ | Memoria longa forte | Series muito persistentes |
| $d \approx 1$ | Integracao unitaria | Usar IGARCH |

!!! tip "Regra pratica"
    Para retornos diarios de acoes e indices, valores tipicos de $d$ estao entre **0.3 e 0.5**. Para taxas de cambio, $d$ tende a ser um pouco maior (0.4 a 0.6).

### Teste de Significancia de $d$

```python
d_hat = figarch_res.params['d']
d_se = figarch_res.se['d']
t_stat = d_hat / d_se
print(f"d = {d_hat:.4f} (se = {d_se:.4f})")
print(f"t-stat = {t_stat:.4f}")
print(f"H0: d=0 (GARCH) -> {'Rejeita' if abs(t_stat) > 1.96 else 'Nao rejeita'}")
```

### Comparacao de ACF: GARCH vs FIGARCH

```python
from archbox import GARCH, FIGARCH
from archbox.datasets import load_dataset
import numpy as np

sp500 = load_dataset('sp500')
returns = sp500['returns']

# Estimar ambos
garch_res = GARCH(returns, p=1, q=1).fit()
figarch_res = FIGARCH(returns, p=1, q=1).fit()

# ACF dos residuos ao quadrado
z2_garch = garch_res.resid**2
z2_figarch = figarch_res.resid**2

print("Lag | ACF(GARCH) | ACF(FIGARCH)")
print("----|------------|-------------")
for lag in [1, 5, 10, 20, 50]:
    acf_g = np.corrcoef(z2_garch[lag:], z2_garch[:-lag])[0,1]
    acf_f = np.corrcoef(z2_figarch[lag:], z2_figarch[:-lag])[0,1]
    print(f"  {lag:2d} |   {acf_g:+.4f}  |   {acf_f:+.4f}")
```

??? example "Output esperado"
    ```
    Lag | ACF(GARCH) | ACF(FIGARCH)
    ----|------------|-------------
       1 |   +0.0523  |   +0.0312
       5 |   +0.0287  |   +0.0198
      10 |   +0.0198  |   +0.0145
      20 |   +0.0102  |   +0.0067
      50 |   +0.0045  |   +0.0021
    ```

!!! note "Interpretacao"
    Se o FIGARCH captura corretamente a memoria longa, os residuos ao quadrado devem apresentar **menos autocorrelacao** que os do GARCH, especialmente em lags longos. O GARCH pode deixar autocorrelacao residual nos lags distantes porque assume decaimento exponencial.

## Diagnosticos

### Ljung-Box nos Residuos Padronizados ao Quadrado

```python
from archbox.diagnostics import ljung_box_test

lb_result = ljung_box_test(figarch_res.resid**2, lags=20)
print(f"Ljung-Box Q(20): {lb_result.statistic:.4f}")
print(f"p-valor: {lb_result.pvalue:.4f}")
# p > 0.05 -> modelo capturou a dinamica da variancia
```

### Teste ARCH-LM

```python
from archbox.diagnostics import arch_lm_test

lm_result = arch_lm_test(figarch_res.resid, lags=10)
print(f"ARCH-LM(10): {lm_result.statistic:.4f}")
print(f"p-valor: {lm_result.pvalue:.4f}")
```

### Workflow Completo de Diagnostico

```python
from archbox import FIGARCH
from archbox.datasets import load_dataset
from archbox.diagnostics import ljung_box_test, arch_lm_test

# 1. Estimar modelo
sp500 = load_dataset('sp500')
model = FIGARCH(sp500['returns'], p=1, q=1)
results = model.fit()

# 2. Residuos padronizados
z = results.resid

# 3. Diagnosticos
print("=== Ljung-Box (z^2) ===")
lb = ljung_box_test(z**2, lags=20)
print(f"  Q(20) = {lb.statistic:.4f}, p = {lb.pvalue:.4f}")

print("\n=== ARCH-LM ===")
lm = arch_lm_test(z, lags=10)
print(f"  LM(10) = {lm.statistic:.4f}, p = {lm.pvalue:.4f}")

# 4. Visualizacao
results.plot("volatility")
results.plot("residuals")
```

## Equivalentes em R e Python

=== "ArchBox"

    ```python
    from archbox import FIGARCH
    from archbox.datasets import load_dataset

    sp500 = load_dataset('sp500')
    model = FIGARCH(sp500['returns'], p=1, q=1)
    results = model.fit()
    print(results.summary())

    # Previsao
    forecast = results.forecast(horizon=10)
    ```

=== "R (rugarch)"

    ```r
    library(rugarch)

    spec <- ugarchspec(
      variance.model = list(model = "fiGARCH", garchOrder = c(1, 1)),
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

    am = arch_model(returns, vol='FIGARCH', p=1, q=1, dist='Normal')
    res = am.fit()
    print(res.summary())

    # Previsao
    forecast = res.forecast(horizon=10)
    ```

| Funcionalidade | ArchBox | rugarch (R) | arch (Python) |
|---------------|---------|-------------|---------------|
| Especificacao | `FIGARCH(y, p=1, q=1)` | `ugarchspec(model="fiGARCH")` | `arch_model(y, vol='FIGARCH')` |
| Estimacao | `model.fit()` | `ugarchfit(spec, data)` | `am.fit()` |
| Previsao | `results.forecast(h)` | `ugarchforecast(fit, n.ahead=h)` | `res.forecast(horizon=h)` |
| Parametro d | `results.params['d']` | `coef(fit)['d']` | `res.params['d']` |

## References

- Baillie, R. T., Bollerslev, T., & Mikkelsen, H. O. (1996). Fractionally Integrated Generalized Autoregressive Conditional Heteroskedasticity. *Journal of Econometrics*, 74(1), 3--30.
- Bollerslev, T., & Mikkelsen, H. O. (1996). Modeling and Pricing Long Memory in Stock Market Volatility. *Journal of Econometrics*, 73(1), 151--184.
- Chung, C.-F. (1999). Estimating the Fractionally Integrated GARCH Model. *National Taiwan University Working Paper*.
- Francq, C., & Zakoian, J.-M. (2019). *GARCH Models: Structure, Statistical Inference and Financial Applications* (2nd ed.). Wiley.

## See Also

- [GARCH(p,q)](garch.md) -- Modelo simetrico padrao (caso $d=0$)
- [IGARCH](igarch.md) -- Modelo integrado (caso $d=1$)
- [Distribuicoes Condicionais](../distributions/index.md) -- Escolha da distribuicao para os erros
- [Diagnosticos: ARCH-LM](../../diagnostics/arch-lm.md) -- Teste para efeitos ARCH residuais
- [Diagnosticos: Ljung-Box](../../diagnostics/ljung-box.md) -- Teste de autocorrelacao nos residuos
