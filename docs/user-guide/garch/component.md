---
title: "Component GARCH"
description: "Component GARCH model - decomposes conditional variance into short-run (transitory) and long-run (trend) components."
---

# Component GARCH

!!! info "Quick Reference"
    **Class:** `archbox.models.component_garch.ComponentGARCH`
    **Import:** `from archbox import ComponentGARCH`
    **R equivalent:** `rugarch::ugarchspec(variance.model = list(model = "csGARCH"))`
    **Python equivalent:** Nao disponivel nativamente no pacote `arch`

## Overview

O modelo Component GARCH, proposto por **Engle & Lee (1999)**, decompoe a variancia condicional em dois componentes: um de **longo prazo** (tendencia permanente) e um de **curto prazo** (desvio transitorio). Essa separacao permite que a volatilidade oscile em torno de uma tendencia que ela mesma evolui ao longo do tempo.

No GARCH padrao, a variancia incondicional e uma constante fixa ($\bar{\sigma}^2 = \omega / (1 - \alpha - \beta)$). O Component GARCH relaxa essa hipotese ao substituir a constante por um processo lento -- capturando a observacao empirica de que o "nivel normal" de volatilidade varia entre periodos calmos e turbulentos.

**Quando usar:**

- Series com **mudancas no nivel** de volatilidade ao longo do tempo
- Quando GARCH padrao mostra persistencia muito alta (possivelmente espuria)
- Modelagem de horizontes longos onde a tendencia de volatilidade importa
- Analise de ciclos de volatilidade (expansao vs crise)
- Separacao de efeitos de curto prazo (noticias) e longo prazo (estruturais)

## Formulacao Matematica

### Equacao da Media

$$r_t = \mu + \epsilon_t, \qquad \epsilon_t = \sigma_t z_t, \qquad z_t \sim D(0, 1)$$

### Equacao da Variancia Condicional

O Component GARCH decompoe $\sigma_t^2$ em dois componentes:

**Componente de Curto Prazo (transitorio):**

$$\sigma_t^2 - q_t = \alpha(\epsilon_{t-1}^2 - q_{t-1}) + \beta(\sigma_{t-1}^2 - q_{t-1})$$

**Componente de Longo Prazo (permanente/tendencia):**

$$q_t = \omega + \rho \, q_{t-1} + \phi(\epsilon_{t-1}^2 - \sigma_{t-1}^2)$$

Combinando:

$$\sigma_t^2 = q_t + \alpha(\epsilon_{t-1}^2 - q_{t-1}) + \beta(\sigma_{t-1}^2 - q_{t-1})$$

onde:

| Parametro | Descricao | Restricao |
|-----------|-----------|-----------|
| $\omega$ | Intercepto do componente de longo prazo | $\omega > 0$ |
| $\alpha$ | ARCH do componente transitorio | $\alpha \geq 0$ |
| $\beta$ | GARCH do componente transitorio | $\beta \geq 0$ |
| $\rho$ | Persistencia do componente permanente | $0 < \rho < 1$ |
| $\phi$ | Sensibilidade do componente permanente a choques | $\phi \geq 0$ |

**Condicoes:**

- Componente transitorio: $\alpha + \beta < 1$ (reversao rapida)
- Componente permanente: $\rho$ proximo de 1 (reversao lenta)
- Tipicamente: $\alpha + \beta < \rho$ (curto prazo reverte mais rapido que longo prazo)

### Interpretacao dos Componentes

```
Variancia condicional σ²_t

    │        ╱╲                  ╱╲
    │  ╱╲  ╱    ╲    ╱╲       ╱    ╲  ╱╲
    │╱    ╲╱      ╲╱╱    ╲   ╱      ╲╱    ╲     σ²_t (total)
    │                      ╲╱
    │
    │   ────────╲                 ╱──────
    │            ╲──────────────╱           q_t (tendencia)
    │
    │  ╱╲  ╱╲        ╱╲       ╱╲  ╱╲
    │╱    ╲╱  ╲╱╲╱╲╱╱  ╲╱╲╱╱╱  ╲╱    ╲    σ²_t - q_t (transitorio)
    ├─────────────────────────────────── t
      Periodo calmo    Crise    Recuperacao
```

!!! note "Intuicao economica"
    - **$q_t$ (longo prazo)**: Representa o nivel "estrutural" de volatilidade -- influenciado por fatores macroeconomicos, politica monetaria, e regime de mercado. Evolui lentamente.
    - **$\sigma_t^2 - q_t$ (curto prazo)**: Captura as flutuacoes transitorias causadas por noticias, surpresas de lucros, e eventos de mercado. Reverte rapidamente a zero.

### Meia-Vida dos Componentes

Cada componente tem sua propria velocidade de reversao:

$$\text{Meia-vida (transitorio)} = \frac{\ln(0.5)}{\ln(\alpha + \beta)}$$

$$\text{Meia-vida (permanente)} = \frac{\ln(0.5)}{\ln(\rho)}$$

## Quick Example

```python
from archbox import ComponentGARCH
from archbox.datasets import load_dataset

# Carregar retornos
sp500 = load_dataset('sp500')

# Estimar Component GARCH
model = ComponentGARCH(sp500['returns'])
results = model.fit()
print(results.summary())
```

??? example "Output esperado"
    ```
    ======================================================================
                          Volatility Model Results
    ======================================================================
    Model:            Component GARCH
    Distribution:     Normal
    Observations:     2000
    Log-Likelihood:   3162.4567
    AIC:              -6314.9134
    BIC:              -6286.7616
    Converged:        True
    ----------------------------------------------------------------------
    Parameter         Estimate      Std Err      t-value      p-value
    ----------------------------------------------------------------------
    omega             0.000045     0.000012       3.7500       0.0002
    alpha             0.054321     0.015678       3.4649       0.0005
    beta              0.432109     0.087654       4.9297       0.0000
    rho               0.987654     0.004321     228.5543       0.0000
    phi               0.023456     0.008765       2.6762       0.0074
    ----------------------------------------------------------------------
    Short-run persistence (alpha+beta):  0.486430
    Long-run persistence (rho):          0.987654
    Short-run half-life:                 0.96 periods
    Long-run half-life:                  55.72 periods
    ======================================================================
    ```

## Guia Detalhado

### Parametros do Construtor

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | array-like | obrigatorio | Serie de retornos |
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
from archbox import ComponentGARCH, GARCH
from archbox.datasets import load_dataset

# 1. Carregar dados
sp500 = load_dataset('sp500')
returns = sp500['returns']

# 2. Comparar GARCH padrao vs Component GARCH
garch = GARCH(returns, p=1, q=1)
garch_res = garch.fit()

cgarch = ComponentGARCH(returns)
cgarch_res = cgarch.fit()

# 3. Comparar criterios de informacao
print("=== Comparacao ===")
print(f"GARCH     - AIC: {garch_res.aic:.4f}, BIC: {garch_res.bic:.4f}")
print(f"Component - AIC: {cgarch_res.aic:.4f}, BIC: {cgarch_res.bic:.4f}")

# 4. Decomposicao
print(f"\n=== Componentes ===")
print(f"Curto prazo (alpha+beta): {cgarch_res.params['alpha'] + cgarch_res.params['beta']:.4f}")
print(f"Longo prazo (rho):        {cgarch_res.params['rho']:.4f}")
print(f"Meia-vida curto prazo:    {cgarch_res.half_life_short():.1f} periodos")
print(f"Meia-vida longo prazo:    {cgarch_res.half_life_long():.1f} periodos")

# 5. Extrair componentes
q_t = cgarch_res.long_run_component       # tendencia
s_t = cgarch_res.short_run_component      # transitorio
sigma2_t = cgarch_res.conditional_volatility**2  # total

print(f"\nVariancia media:")
print(f"  Total:       {sigma2_t.mean():.6f}")
print(f"  Longo prazo: {q_t.mean():.6f}")
print(f"  Curto prazo: {s_t.mean():.6f}")
```

### Visualizacao dos Componentes

```python
from archbox import ComponentGARCH
from archbox.datasets import load_dataset
import numpy as np

sp500 = load_dataset('sp500')
results = ComponentGARCH(sp500['returns']).fit()

# Plotar decomposicao
results.plot("components")

# Ou manualmente:
# results.plot("volatility")     # sigma_t total
# results.plot("long_run")       # q_t (tendencia)
# results.plot("short_run")      # sigma_t^2 - q_t (transitorio)
```

### Resultados

| Atributo | Descricao |
|----------|-----------|
| `results.params` | Parametros estimados |
| `results.se` | Erros-padrao robustos |
| `results.tvalues` | Estatisticas t |
| `results.pvalues` | p-valores bilaterais |
| `results.loglike` | Log-verossimilhanca |
| `results.aic` | Criterio de Informacao de Akaike |
| `results.bic` | Criterio de Informacao Bayesiano |
| `results.conditional_volatility` | Serie de $\sigma_t$ (total) |
| `results.long_run_component` | Serie de $q_t$ (tendencia) |
| `results.short_run_component` | Serie de $\sigma_t^2 - q_t$ (transitorio) |
| `results.resid` | Residuos padronizados |

| Metodo | Descricao |
|--------|-----------|
| `results.half_life_short()` | Meia-vida do componente transitorio |
| `results.half_life_long()` | Meia-vida do componente permanente |
| `results.forecast(horizon)` | Previsao de variancia/volatilidade |
| `results.summary()` | Tabela formatada |
| `results.plot("components")` | Grafico dos componentes decompostos |
| `results.plot("volatility")` | Grafico de retornos e volatilidade total |
| `results.to_dataframe()` | Exportar parametros como DataFrame |

## Interpretacao

### Componente de Longo Prazo ($q_t$)

O parametro $\rho$ controla a persistencia do componente permanente:

| Valor de $\rho$ | Interpretacao |
|-----------------|---------------|
| $\rho = 0.95$ | Meia-vida $\approx$ 14 periodos |
| $\rho = 0.99$ | Meia-vida $\approx$ 69 periodos |
| $\rho = 0.999$ | Meia-vida $\approx$ 693 periodos |

!!! tip "Interpretacao de $\rho$"
    Valores tipicos de $\rho$ para retornos diarios estao entre **0.98 e 0.999**. Isso significa que o nivel "estrutural" de volatilidade pode levar meses ou anos para mudar significativamente.

### Componente de Curto Prazo ($\sigma_t^2 - q_t$)

| Parametro | Interpretacao |
|-----------|---------------|
| $\alpha$ grande | Alta sensibilidade a choques recentes |
| $\beta$ grande | Maior inércia no componente transitorio |
| $\alpha + \beta$ | Persistencia do componente de curto prazo |

### Comparacao com GARCH Padrao

| Aspecto | GARCH | Component GARCH |
|---------|-------|-----------------|
| Variancia incondicional | Constante ($\bar{\sigma}^2$) | Varia no tempo ($q_t$) |
| Persistencia | $\alpha + \beta$ (unica) | Duas: $\alpha + \beta$ (curta) e $\rho$ (longa) |
| Parametros | 3 ($\omega, \alpha, \beta$) | 5 ($\omega, \alpha, \beta, \rho, \phi$) |
| Reversao a media | Para constante | Para tendencia movel |
| Persistencia espuria | Possivel | Resolvida pela decomposicao |

!!! note "Persistencia espuria no GARCH"
    Quando a variancia incondicional muda ao longo do tempo (e.g., entre periodos calmos e de crise), o GARCH padrao pode estimar $\alpha + \beta$ proximo de 1 **espuriamente** -- nao porque choques sao permanentes, mas porque o modelo confunde mudanca de nivel com alta persistencia. O Component GARCH resolve isso ao separar a tendencia do componente transitorio.

### Quando Component GARCH e Melhor?

```python
from archbox import GARCH, ComponentGARCH
from archbox.datasets import load_dataset
from scipy import stats

sp500 = load_dataset('sp500')
returns = sp500['returns']

garch_res = GARCH(returns, p=1, q=1).fit()
cgarch_res = ComponentGARCH(returns).fit()

# Teste LR: Component GARCH aninha GARCH?
# H0: rho = alpha+beta e phi = 0 (GARCH padrao)
lr_stat = 2 * (cgarch_res.loglike - garch_res.loglike)
p_value = 1 - stats.chi2.cdf(lr_stat, df=2)

print(f"=== Teste Component vs GARCH ===")
print(f"LR statistic: {lr_stat:.4f}")
print(f"p-valor: {p_value:.4f}")
print(f"{'Component GARCH preferido' if p_value < 0.05 else 'GARCH padrao suficiente'}")
```

## Diagnosticos

### Ljung-Box nos Residuos Padronizados ao Quadrado

```python
from archbox.diagnostics import ljung_box_test

lb_result = ljung_box_test(cgarch_res.resid**2, lags=10)
print(f"Ljung-Box Q(10): {lb_result.statistic:.4f}")
print(f"p-valor: {lb_result.pvalue:.4f}")
```

### Teste ARCH-LM

```python
from archbox.diagnostics import arch_lm_test

lm_result = arch_lm_test(cgarch_res.resid, lags=5)
print(f"ARCH-LM(5): {lm_result.statistic:.4f}")
print(f"p-valor: {lm_result.pvalue:.4f}")
```

### Workflow Completo de Diagnostico

```python
from archbox import ComponentGARCH
from archbox.datasets import load_dataset
from archbox.diagnostics import ljung_box_test, arch_lm_test

# 1. Estimar modelo
sp500 = load_dataset('sp500')
model = ComponentGARCH(sp500['returns'])
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

# 4. Componentes
print(f"\n=== Decomposicao ===")
print(f"  Meia-vida curto prazo: {results.half_life_short():.1f} periodos")
print(f"  Meia-vida longo prazo: {results.half_life_long():.1f} periodos")

# 5. Visualizacao
results.plot("components")
```

## Equivalentes em R e Python

=== "ArchBox"

    ```python
    from archbox import ComponentGARCH
    from archbox.datasets import load_dataset

    sp500 = load_dataset('sp500')
    model = ComponentGARCH(sp500['returns'])
    results = model.fit()
    print(results.summary())

    # Componentes
    q_t = results.long_run_component
    s_t = results.short_run_component
    ```

=== "R (rugarch)"

    ```r
    library(rugarch)

    spec <- ugarchspec(
      variance.model = list(
        model = "csGARCH",    # Component Spline GARCH
        garchOrder = c(1, 1)
      ),
      mean.model = list(armaOrder = c(0, 0), include.mean = TRUE),
      distribution.model = "norm"
    )

    fit <- ugarchfit(spec = spec, data = returns)
    show(fit)

    # Componente permanente
    q_t <- fit@fit$q
    ```

=== "Python (arch)"

    ```python
    # O pacote arch nao implementa Component GARCH nativamente.
    # Use ArchBox ou rugarch para este modelo.

    from archbox import ComponentGARCH
    model = ComponentGARCH(returns)
    results = model.fit()
    ```

| Funcionalidade | ArchBox | rugarch (R) | arch (Python) |
|---------------|---------|-------------|---------------|
| Especificacao | `ComponentGARCH(y)` | `ugarchspec(model="csGARCH")` | Nao disponivel |
| Componente LP | `results.long_run_component` | `fit@fit$q` | --- |
| Componente CP | `results.short_run_component` | Manual | --- |
| Meia-vida LP | `results.half_life_long()` | Manual | --- |
| Meia-vida CP | `results.half_life_short()` | Manual | --- |

## References

- Engle, R. F., & Lee, G. G. J. (1999). A Long-Run and Short-Run Component Model of Stock Return Volatility. In R. Engle & H. White (Eds.), *Cointegration, Causality and Forecasting: A Festschrift in Honor of Clive W.J. Granger* (pp. 475--497). Oxford University Press.
- Ding, Z., & Granger, C. W. J. (1996). Modeling Volatility Persistence of Speculative Returns: A New Approach. *Journal of Econometrics*, 73(1), 185--215.
- Maheu, J. M. (2005). Can GARCH Models Capture Long-Range Dependence? *Studies in Nonlinear Dynamics & Econometrics*, 9(4), Article 1.
- Francq, C., & Zakoian, J.-M. (2019). *GARCH Models: Structure, Statistical Inference and Financial Applications* (2nd ed.). Wiley.

## See Also

- [GARCH(p,q)](garch.md) -- Modelo padrao (variancia incondicional constante)
- [FIGARCH](figarch.md) -- Modelo fracionario (memoria longa via parametro $d$)
- [IGARCH](igarch.md) -- Modelo integrado (persistencia unitaria)
- [Distribuicoes Condicionais](../distributions/index.md) -- Escolha da distribuicao para os erros
- [Diagnosticos: ARCH-LM](../../diagnostics/arch-lm.md) -- Teste para efeitos ARCH residuais
