---
title: "HAR-RV"
description: "Heterogeneous Autoregressive model of Realized Volatility - models realized volatility at daily, weekly, and monthly horizons using high-frequency data."
---

# HAR-RV

!!! info "Quick Reference"
    **Class:** `archbox.models.har_rv.HARRV`
    **Import:** `from archbox import HARRV`
    **R equivalent:** `HARmodel::HAREstimate()`
    **Python equivalent:** OLS com regressores agregados manualmente

!!! note "Nota sobre classificacao"
    O HAR-RV **nao e um modelo GARCH** -- nao modela a variancia condicional de retornos via log-verossimilhanca. E um modelo de **regressao linear para volatilidade realizada**, estimado por OLS ou WLS. Esta incluido nesta secao por ser um dos modelos de volatilidade mais importantes na literatura moderna.

## Overview

O modelo HAR-RV (Heterogeneous Autoregressive model of Realized Volatility), proposto por **Corsi (2009)**, e um modelo simples e eficaz para prever volatilidade realizada usando dados de alta frequencia. A ideia central e que o mercado e composto por **agentes com diferentes horizontes de investimento** (diario, semanal, mensal), e a volatilidade futura depende da volatilidade passada em cada um desses horizontes.

Apesar da formulacao simples (regressao linear com 3 regressores), o HAR-RV captura a **memoria longa** na volatilidade de forma parcimoniosa -- uma propriedade difícil de modelar com GARCH padrao.

**Quando usar:**

- Quando **dados de alta frequencia** (intraday) estao disponiveis
- Previsao de volatilidade realizada
- Quando a memoria longa na volatilidade e importante
- Como benchmark para modelos mais complexos (Realized GARCH, HAR-CJ)
- Quando se deseja um modelo transparente e facilmente interpretavel

## Formulacao Matematica

### Volatilidade Realizada

A volatilidade realizada diaria e construida a partir de retornos intraday:

$$RV_t = \sum_{i=1}^{M} r_{t,i}^2$$

onde $r_{t,i}$ sao os $M$ retornos intraday do dia $t$ (e.g., retornos de 5 minutos: $M = 78$ para um pregao de 6.5 horas).

### Modelo HAR-RV

O modelo HAR-RV usa tres componentes de volatilidade realizada em diferentes horizontes:

$$RV_t = \beta_0 + \beta_d RV_{t-1}^{(d)} + \beta_w RV_{t-1}^{(w)} + \beta_m RV_{t-1}^{(m)} + \epsilon_t$$

onde:

| Componente | Definicao | Horizonte |
|------------|-----------|-----------|
| $RV_{t-1}^{(d)} = RV_{t-1}$ | Volatilidade realizada diaria | 1 dia |
| $RV_{t-1}^{(w)} = \frac{1}{5}\sum_{i=1}^{5} RV_{t-i}$ | Media movel semanal | 5 dias |
| $RV_{t-1}^{(m)} = \frac{1}{22}\sum_{i=1}^{22} RV_{t-i}$ | Media movel mensal | 22 dias |

| Parametro | Descricao |
|-----------|-----------|
| $\beta_0$ | Intercepto (nivel base de volatilidade) |
| $\beta_d$ | Efeito de **traders diarios** (alta frequencia) |
| $\beta_w$ | Efeito de **investidores semanais** (media frequencia) |
| $\beta_m$ | Efeito de **investidores mensais** (baixa frequencia) |

### Interpretacao Heterogenea

A motivacao teorica do HAR-RV vem da **Heterogeneous Market Hypothesis (HMH)** de Muller et al. (1993):

```
Mercado Financeiro

Traders diarios     ──> beta_d: reagem a volatilidade de ontem
   (alta freq.)

Investidores        ──> beta_w: reagem a volatilidade da ultima semana
   semanais
   (media freq.)

Investidores        ──> beta_m: reagem a volatilidade do ultimo mes
   mensais
   (baixa freq.)

                         RV_t = beta_0 + beta_d * RV_d + beta_w * RV_w + beta_m * RV_m
```

!!! note "Por que funciona?"
    Apesar de ser uma regressao linear simples, o HAR-RV captura a memoria longa da volatilidade porque a combinacao de tres componentes com decaimento em diferentes velocidades **aproxima** o comportamento de um processo fracionariamente integrado. Corsi (2009) mostra que o HAR-RV produz previsoes competitivas com modelos muito mais complexos.

### Variante: HAR-RV em Log

Para dados com assimetria positiva, frequentemente usa-se a versao em logaritmo:

$$\log(RV_t) = \beta_0 + \beta_d \log(RV_{t-1}^{(d)}) + \beta_w \log(RV_{t-1}^{(w)}) + \beta_m \log(RV_{t-1}^{(m)}) + \epsilon_t$$

Esta versao garante previsoes positivas e erros mais proximos da normalidade.

### Variante: HAR-CJ (Jumps)

O HAR-CJ separa a volatilidade realizada em componente **continuo** e **saltos**:

$$RV_t = \beta_0 + \beta_d C_{t-1} + \beta_w C_{t-1}^{(w)} + \beta_m C_{t-1}^{(m)} + \gamma_d J_{t-1} + \epsilon_t$$

onde $C_t = RV_t - J_t$ (componente continuo) e $J_t$ sao os saltos estimados (Barndorff-Nielsen & Shephard, 2004).

## Quick Example

```python
from archbox import HARRV
from archbox.datasets import load_dataset

# Carregar volatilidade realizada (dados de alta frequencia)
rv_data = load_dataset('realized_volatility')

# Estimar HAR-RV
model = HARRV(rv_data['rv'])
results = model.fit()
print(results.summary())
```

??? example "Output esperado"
    ```
    ======================================================================
                          HAR-RV Model Results
    ======================================================================
    Model:            HAR-RV
    Method:           OLS
    Observations:     2000
    R-squared:        0.6234
    Adj. R-squared:   0.6228
    F-statistic:      1103.45
    Prob(F-stat):     0.0000
    ----------------------------------------------------------------------
    Parameter         Estimate      Std Err      t-value      p-value
    ----------------------------------------------------------------------
    beta_0            0.000023     0.000008       2.8750       0.0041
    beta_d            0.354567     0.023456      15.1148       0.0000
    beta_w            0.312345     0.034567       9.0357       0.0000
    beta_m            0.234567     0.045678       5.1353       0.0000
    ----------------------------------------------------------------------
    Sum of betas:     0.901479
    Newey-West SE:    HAC-robust (5 lags)
    ======================================================================
    ```

## Guia Detalhado

### Parametros do Construtor

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | array-like | obrigatorio | Serie de volatilidade realizada ($RV_t$) |
| `lags` | list | `[1, 5, 22]` | Horizontes para agregacao: diario, semanal, mensal |
| `log` | bool | `False` | Usar log-RV ($\log(RV_t)$) |
| `har_type` | str | `"standard"` | Tipo: `"standard"`, `"cj"` (continuous + jumps) |

### Parametros de `fit()`

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `method` | str | `"ols"` | Metodo de estimacao: `"ols"` ou `"wls"` |
| `cov_type` | str | `"HAC"` | Tipo de covariancia: `"HAC"` (Newey-West), `"HC0"` |
| `bandwidth` | int | `None` | Bandwidth para HAC (auto se `None`) |

### Exemplo Completo com Dados Intraday

```python
from archbox import HARRV
from archbox.datasets import load_dataset
import numpy as np

# 1. Carregar dados de volatilidade realizada
rv_data = load_dataset('realized_volatility')
rv = rv_data['rv']

print(f"Periodo: {rv.index[0]} a {rv.index[-1]}")
print(f"Observacoes: {len(rv)}")
print(f"RV media: {rv.mean():.6f}")
print(f"RV mediana: {rv.median():.6f}")

# 2. Estimar HAR-RV padrao
model = HARRV(rv, lags=[1, 5, 22])
results = model.fit()

# 3. Coeficientes
print("\n=== Coeficientes HAR-RV ===")
print(f"beta_0 (intercepto): {results.params['beta_0']:.6f}")
print(f"beta_d (diario):     {results.params['beta_d']:.4f}")
print(f"beta_w (semanal):    {results.params['beta_w']:.4f}")
print(f"beta_m (mensal):     {results.params['beta_m']:.4f}")

# 4. Contribuicao relativa
total = results.params['beta_d'] + results.params['beta_w'] + results.params['beta_m']
print(f"\nContribuicao relativa:")
print(f"  Diaria:  {results.params['beta_d']/total*100:.1f}%")
print(f"  Semanal: {results.params['beta_w']/total*100:.1f}%")
print(f"  Mensal:  {results.params['beta_m']/total*100:.1f}%")

# 5. Previsao
forecast = results.forecast(horizon=10)
print(f"\nPrevisao de RV (proximos 10 dias):")
print(forecast['rv'])
```

### Exemplo com HAR em Log

```python
from archbox import HARRV
from archbox.datasets import load_dataset

rv_data = load_dataset('realized_volatility')
rv = rv_data['rv']

# HAR-RV em log (previsoes sempre positivas)
model_log = HARRV(rv, lags=[1, 5, 22], log=True)
results_log = model_log.fit()

# HAR-RV padrao
model_std = HARRV(rv, lags=[1, 5, 22], log=False)
results_std = model_std.fit()

print("=== Comparacao HAR vs HAR-log ===")
print(f"HAR     R^2: {results_std.r_squared:.4f}")
print(f"HAR-log R^2: {results_log.r_squared:.4f}")
```

### Construcao Manual da Volatilidade Realizada

```python
import numpy as np
import pandas as pd

# Se voce tem retornos intraday (e.g., 5 minutos)
# intraday_returns: DataFrame com index = datetime, colunas = ['returns']

def compute_realized_volatility(intraday_returns, freq='5min'):
    """Calcula volatilidade realizada diaria a partir de retornos intraday."""
    # Agrupar por dia e somar retornos ao quadrado
    rv = intraday_returns.groupby(intraday_returns.index.date).apply(
        lambda x: (x['returns']**2).sum()
    )
    rv.index = pd.DatetimeIndex(rv.index)
    rv.name = 'rv'
    return rv

# Exemplo:
# rv_daily = compute_realized_volatility(intraday_5min)
# model = HARRV(rv_daily)
# results = model.fit()
```

### Resultados

| Atributo | Descricao |
|----------|-----------|
| `results.params` | Coeficientes estimados |
| `results.se` | Erros-padrao (HAC-robustos por default) |
| `results.tvalues` | Estatisticas t |
| `results.pvalues` | p-valores |
| `results.r_squared` | Coeficiente de determinacao $R^2$ |
| `results.adj_r_squared` | $R^2$ ajustado |
| `results.fvalue` | Estatistica F |
| `results.resid` | Residuos |
| `results.fitted` | Valores ajustados ($\hat{RV}_t$) |

| Metodo | Descricao |
|--------|-----------|
| `results.forecast(horizon)` | Previsao iterativa de $RV$ |
| `results.summary()` | Tabela formatada |
| `results.plot("fit")` | Grafico de $RV_t$ observado vs ajustado |
| `results.plot("forecast")` | Grafico de previsao |
| `results.to_dataframe()` | Exportar coeficientes como DataFrame |

## Interpretacao

### Os Tres Betas

| Coeficiente | Agente de mercado | Tipico | Interpretacao |
|-------------|-------------------|--------|---------------|
| $\beta_d$ | Traders de alta frequencia | 0.3 -- 0.5 | Volatilidade de curto prazo |
| $\beta_w$ | Investidores semanais | 0.2 -- 0.4 | Volatilidade de medio prazo |
| $\beta_m$ | Investidores mensais | 0.1 -- 0.3 | Volatilidade de longo prazo |

!!! tip "Regra pratica"
    - $\beta_d + \beta_w + \beta_m < 1$: volatilidade estacionaria (reverte a media)
    - $\beta_d + \beta_w + \beta_m \approx 1$: alta persistencia
    - Geralmente $\beta_d > \beta_w > \beta_m$: efeito diario domina

### $R^2$ como Medida de Previsibilidade

O $R^2$ do HAR-RV e uma medida direta de quao previsivel e a volatilidade:

| $R^2$ | Interpretacao |
|-------|---------------|
| 0.3 -- 0.4 | Previsibilidade moderada (tipico de acoes individuais) |
| 0.5 -- 0.7 | Boa previsibilidade (tipico de indices e FX) |
| $> 0.7$ | Alta previsibilidade (dados limpos, alta liquidez) |

### Comparacao HAR-RV vs GARCH

| Aspecto | GARCH | HAR-RV |
|---------|-------|--------|
| **Dados** | Retornos diarios | Volatilidade realizada (intraday) |
| **Estimacao** | MLE | OLS |
| **Variavel modelada** | Variancia condicional (latente) | Volatilidade realizada (observada) |
| **Memoria longa** | Nao captura (exceto FIGARCH) | Captura via tres horizontes |
| **Interpretacao** | Parametros ARCH/GARCH | Betas por horizonte |
| **Complexidade** | Otimizacao nao-linear | Regressao linear |
| **Dados necessarios** | Retornos diarios | Retornos intraday |

## Diagnosticos

### Teste de Autocorrelacao nos Residuos

```python
from archbox.diagnostics import ljung_box_test

lb_result = ljung_box_test(results.resid, lags=10)
print(f"Ljung-Box Q(10): {lb_result.statistic:.4f}")
print(f"p-valor: {lb_result.pvalue:.4f}")
# p > 0.05 -> residuos nao autocorrelacionados
```

### Teste de Heterocedasticidade

```python
from archbox.diagnostics import arch_lm_test

lm_result = arch_lm_test(results.resid, lags=5)
print(f"ARCH-LM(5): {lm_result.statistic:.4f}")
print(f"p-valor: {lm_result.pvalue:.4f}")
```

### Avaliacao de Previsao (Out-of-Sample)

```python
from archbox import HARRV
from archbox.datasets import load_dataset
import numpy as np

rv_data = load_dataset('realized_volatility')
rv = rv_data['rv']

# Dividir em treino e teste
n_test = 252  # ultimo ano
rv_train = rv[:-n_test]
rv_test = rv[-n_test:]

# Estimar no treino
model = HARRV(rv_train, lags=[1, 5, 22])
results = model.fit()

# Previsao rolling 1-passo
forecasts = results.rolling_forecast(rv_test)

# Metricas
mse = np.mean((rv_test - forecasts)**2)
mae = np.mean(np.abs(rv_test - forecasts))
r2_oos = 1 - mse / np.var(rv_test)

print(f"=== Out-of-Sample (1 ano) ===")
print(f"MSE: {mse:.8f}")
print(f"MAE: {mae:.6f}")
print(f"R^2 OOS: {r2_oos:.4f}")
```

### Workflow Completo

```python
from archbox import HARRV
from archbox.datasets import load_dataset
from archbox.diagnostics import ljung_box_test

# 1. Carregar dados
rv_data = load_dataset('realized_volatility')
rv = rv_data['rv']

# 2. Estimar HAR-RV
model = HARRV(rv, lags=[1, 5, 22])
results = model.fit()

# 3. Resumo
print(results.summary())

# 4. Diagnosticos
z = results.resid
print("\n=== Ljung-Box (residuos) ===")
lb = ljung_box_test(z, lags=10)
print(f"  Q(10) = {lb.statistic:.4f}, p = {lb.pvalue:.4f}")

# 5. Previsao
forecast = results.forecast(horizon=5)
print(f"\nPrevisao de RV (proximos 5 dias):")
print(forecast['rv'])

# 6. Visualizacao
results.plot("fit")
```

## Equivalentes em R e Python

=== "ArchBox"

    ```python
    from archbox import HARRV
    from archbox.datasets import load_dataset

    rv_data = load_dataset('realized_volatility')
    model = HARRV(rv_data['rv'], lags=[1, 5, 22])
    results = model.fit()
    print(results.summary())

    # Previsao
    forecast = results.forecast(horizon=10)
    ```

=== "R (HARmodel)"

    ```r
    library(HARmodel)

    # Estimar HAR-RV padrao
    fit <- HAREstimate(
      RM = rv,
      periods = c(1, 5, 22),
      type = "HAR"
    )
    summary(fit)

    # Previsao
    forecast <- predict(fit, n.ahead = 10)
    ```

=== "Python (statsmodels)"

    ```python
    import pandas as pd
    import statsmodels.api as sm

    # Construir regressores manualmente
    rv_d = rv.shift(1)                          # diario
    rv_w = rv.rolling(5).mean().shift(1)        # semanal
    rv_m = rv.rolling(22).mean().shift(1)       # mensal

    X = pd.DataFrame({
        'rv_d': rv_d, 'rv_w': rv_w, 'rv_m': rv_m
    }).dropna()
    X = sm.add_constant(X)
    y = rv.loc[X.index]

    model = sm.OLS(y, X)
    res = model.fit(cov_type='HAC', cov_kwds={'maxlags': 5})
    print(res.summary())
    ```

| Funcionalidade | ArchBox | HARmodel (R) | statsmodels (Python) |
|---------------|---------|--------------|---------------------|
| Especificacao | `HARRV(rv, lags=[1,5,22])` | `HAREstimate(RM=rv, periods=c(1,5,22))` | Manual (OLS) |
| Estimacao | `model.fit()` | Automatica | `model.fit(cov_type='HAC')` |
| Previsao | `results.forecast(h)` | `predict(fit, n.ahead=h)` | Manual |
| HAC SE | Automatico | Automatico | `cov_type='HAC'` |
| Log-HAR | `HARRV(rv, log=True)` | `type="HAR-log"` | Manual |

## References

- Corsi, F. (2009). A Simple Approximate Long-Memory Model of Realized Volatility. *Journal of Financial Econometrics*, 7(2), 174--196.
- Muller, U. A., Dacorogna, M. M., Dave, R. D., Olsen, R. B., Pictet, O. V., & Von Weizsacker, J. E. (1997). Volatilities of Different Time Resolutions -- Analyzing the Dynamics of Market Components. *Journal of Empirical Finance*, 4(2-3), 213--239.
- Andersen, T. G., Bollerslev, T., Diebold, F. X., & Labys, P. (2003). Modeling and Forecasting Realized Volatility. *Econometrica*, 71(2), 579--625.
- Barndorff-Nielsen, O. E., & Shephard, N. (2004). Power and Bipower Variation with Stochastic Volatility and Jumps. *Journal of Financial Econometrics*, 2(1), 1--37.

## See Also

- [GARCH(p,q)](garch.md) -- Modelo de variancia condicional padrao
- [FIGARCH](figarch.md) -- Modelo GARCH com memoria longa
- [Distribuicoes Condicionais](../distributions/index.md) -- Distribuicoes para modelos GARCH
- [Diagnosticos: Ljung-Box](../../diagnostics/ljung-box.md) -- Teste de autocorrelacao
