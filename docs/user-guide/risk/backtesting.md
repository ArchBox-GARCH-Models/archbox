---
title: "Backtesting de VaR e ES"
description: "Validacao estatistica de modelos de risco: Kupiec, Christoffersen, Dynamic Quantile e Basel traffic light system."
---

# Backtesting de VaR e ES

!!! info "Quick Reference"
    **Class:** `archbox.risk.backtest.VaRBacktest`
    **Import:** `from archbox.risk import VaRBacktest`
    **R equivalent:** `rugarch::VaRTest()`, `GAS::BacktestVaR()`
    **Python equivalent:** Manual implementation

## Overview

O **backtesting** e o processo de validacao estatistica das previsoes de risco. Um modelo de VaR que preve perdas a 5% deve, em media, apresentar violacoes (perdas reais excedendo o VaR) em exatamente 5% dos dias. O backtesting verifica se essa premissa e satisfeita.

**Quando usar:**

- Validacao regulatoria de modelos internos (Basel II/III)
- Comparacao entre modelos de volatilidade (GARCH vs EGARCH vs GJR)
- Monitoramento continuo da qualidade do modelo de risco
- Auditoria interna de limites de risco

**Testes disponiveis:**

| Teste | Hipotese | Referencia |
|-------|----------|-----------|
| **Kupiec (POF)** | Proporcao de violacoes = $\alpha$ | Kupiec (1995) |
| **Christoffersen (CC)** | Cobertura condicional (proporcao + independencia) | Christoffersen (1998) |
| **Dynamic Quantile (DQ)** | Ausencia de previsibilidade nas violacoes | Engle & Manganelli (2004) |

!!! warning "Backtesting e necessario, nao suficiente"
    Um modelo que "passa" no backtest nao e necessariamente bom — apenas nao foi rejeitado estatisticamente. Em periodos de baixa volatilidade, quase qualquer modelo passa. O verdadeiro teste e em periodos de estresse.

## Formulacao Matematica

### Variavel de Violacao (Hit Variable)

Defina a **hit variable** como o indicador de violacao do VaR:

$$I_t = \mathbb{1}\{r_t < \text{VaR}_{\alpha,t}\}$$

onde $r_t$ e o retorno observado e $\text{VaR}_{\alpha,t}$ e a previsao de VaR para o dia $t$.

Se o modelo estiver corretamente especificado:

$$E[I_t \mid \mathcal{F}_{t-1}] = \alpha$$

ou seja, as violacoes devem ser **iid Bernoulli** com probabilidade $\alpha$.

### Kupiec Test (1995) — Proportion of Failures

O teste de Kupiec avalia se a **proporcao observada** de violacoes e consistente com o nivel nominal $\alpha$:

$$H_0: \pi = \alpha \qquad \text{vs} \qquad H_1: \pi \neq \alpha$$

onde $\pi$ e a verdadeira probabilidade de violacao.

A estatistica de teste e o **Likelihood Ratio** (razao de verossimilhanca):

$$LR_{POF} = -2\left[x \ln(\alpha) + (n-x)\ln(1-\alpha) - x\ln\!\left(\frac{x}{n}\right) - (n-x)\ln\!\left(1 - \frac{x}{n}\right)\right]$$

onde:

- $n$ = numero total de observacoes
- $x$ = numero de violacoes
- $\hat{\pi} = x / n$ = proporcao observada de violacoes

$$LR_{POF} \xrightarrow{d} \chi^2(1)$$

!!! note "Interpretacao"
    Rejeitar $H_0$ (p-value < 0.05) indica que o modelo esta **mal calibrado**: ou subestima o risco (muitas violacoes) ou e excessivamente conservador (poucas violacoes).

### Christoffersen Test (1998) — Conditional Coverage

O teste de Kupiec verifica apenas a proporcao, mas ignora o **padrao temporal** das violacoes. Violacoes agrupadas (clusters) indicam que o modelo nao captura a dinamica temporal do risco.

O teste de Christoffersen combina **dois componentes**:

#### Teste de Independencia

Modele as transicoes entre estados de violacao como uma cadeia de Markov de primeira ordem:

| De \ Para | Sem violacao ($I_t = 0$) | Violacao ($I_t = 1$) |
|-----------|--------------------------|----------------------|
| $I_{t-1} = 0$ | $1 - \pi_{01}$ | $\pi_{01}$ |
| $I_{t-1} = 1$ | $1 - \pi_{11}$ | $\pi_{11}$ |

$$H_0: \pi_{01} = \pi_{11} \qquad \text{(independencia)}$$

A estatistica de independencia e:

$$LR_{ind} = -2\ln\!\left(\frac{(1-\hat{\pi})^{n_{00}+n_{10}} \cdot \hat{\pi}^{n_{01}+n_{11}}}{(1-\hat{\pi}_{01})^{n_{00}} \cdot \hat{\pi}_{01}^{n_{01}} \cdot (1-\hat{\pi}_{11})^{n_{10}} \cdot \hat{\pi}_{11}^{n_{11}}}\right)$$

onde $n_{ij}$ e o numero de transicoes do estado $i$ para o estado $j$.

$$LR_{ind} \xrightarrow{d} \chi^2(1)$$

#### Teste de Cobertura Condicional

O teste de cobertura condicional combina ambos os componentes:

$$LR_{CC} = LR_{POF} + LR_{ind} \xrightarrow{d} \chi^2(2)$$

!!! tip "Qual teste usar?"
    O teste de Christoffersen e **estritamente superior** ao de Kupiec, pois detecta tanto calibracao incorreta quanto clustering de violacoes. Use Kupiec apenas quando a amostra for muito pequena ($n < 100$).

### Dynamic Quantile Test (Engle & Manganelli, 2004)

O teste DQ generaliza o teste de independencia usando uma **regressao linear**:

$$\text{Hit}_t = \delta_0 + \sum_{k=1}^{K} \delta_k \text{Hit}_{t-k} + \delta_{K+1} \text{VaR}_{\alpha,t} + u_t$$

onde $\text{Hit}_t = I_t - \alpha$ e a hit variable centralizada.

$$H_0: \delta_0 = \delta_1 = \cdots = \delta_{K+1} = 0$$

A estatistica de teste:

$$DQ = \frac{\hat{\boldsymbol{\delta}}' \mathbf{X}' \mathbf{X} \hat{\boldsymbol{\delta}}}{\alpha(1-\alpha)} \xrightarrow{d} \chi^2(K+2)$$

!!! note "Vantagem do DQ"
    O DQ detecta dependencias de **ordem superior** nas violacoes e testa se o VaR tem poder preditivo sobre as proprias violacoes — uma condicao que nenhum modelo bem especificado deveria exibir.

## Traffic Light System (Basel)

O **Basel traffic light system** e o framework regulatorio para avaliar modelos internos de VaR. Baseado em 250 dias de backtesting com VaR a 99% ($\alpha = 0.01$):

| Zona | Violacoes | Prob. Cumulativa | Penalidade | Acao |
|------|-----------|-----------------|-----------|------|
| :green_circle: **Verde** | 0--4 | 10.8%--89.2% | Nenhuma | Modelo aceito |
| :yellow_circle: **Amarelo** | 5 | 95.9% | +0.40 | Investigacao |
| :yellow_circle: **Amarelo** | 6 | 98.6% | +0.50 | Investigacao |
| :yellow_circle: **Amarelo** | 7 | 99.5% | +0.65 | Investigacao |
| :yellow_circle: **Amarelo** | 8 | 99.9% | +0.75 | Investigacao |
| :yellow_circle: **Amarelo** | 9 | 100.0% | +0.85 | Investigacao |
| :red_circle: **Vermelho** | 10+ | -- | +1.00 | Modelo rejeitado |

A **penalidade** e um multiplicador adicional sobre o requerimento de capital:

$$\text{Capital} = \max\left(VaR_{t-1}, \, m_c \cdot \frac{1}{60}\sum_{i=1}^{60} VaR_{t-i}\right)$$

onde $m_c = 3 + k$ e $k$ e o fator de penalidade da tabela acima.

!!! warning "Zona vermelha"
    Na zona vermelha, o regulador pode exigir a substituicao do modelo interno por uma abordagem padronizada, resultando em requerimentos de capital significativamente maiores.

## Quick Example

```python
from archbox import GARCH
from archbox.risk import ValueAtRisk, VaRBacktest
from archbox.datasets import load_dataset

# 1. Estimar modelo e calcular VaR
sp500 = load_dataset('sp500')
model = GARCH(sp500['returns'], p=1, q=1)
results = model.fit()

var = ValueAtRisk(results, alpha=0.01)
var_series = var.parametric(dist='normal')

# 2. Backtesting
bt = VaRBacktest(sp500['returns'], var_series, alpha=0.01)
print(bt.summary())
```

??? example "Output esperado"
    ```
    ============================================================
    VaR Backtest Summary
    ============================================================
      Observations:      2000
      VaR level (alpha): 0.0100
      Violations:        22
      Violation rate:    0.0110
      Violation ratio:   1.1000

    ------------------------------------------------------------
    Statistical Tests
    ------------------------------------------------------------
      Kupiec POF:        statistic=0.1823, pvalue=0.6694
      Christoffersen CC: statistic=0.4512, pvalue=0.7983
      Dynamic Quantile:  statistic=3.2145, pvalue=0.7817

    ------------------------------------------------------------
      Basel Traffic Light: GREEN (4 violations in last 250 days)
    ============================================================
    ```

## Guia Detalhado

### Parametros do Construtor

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `returns` | array-like | obrigatorio | Serie de retornos observados |
| `var_series` | array-like | obrigatorio | Serie de previsoes de VaR |
| `alpha` | float | `0.05` | Nivel de significancia do VaR |

### Metodos

| Metodo | Parametros | Descricao |
|--------|-----------|-----------|
| `kupiec_test()` | -- | Teste de proporcao de falhas (POF) |
| `christoffersen_test()` | -- | Teste de cobertura condicional |
| `dq_test(lags)` | `lags=5` | Teste Dynamic Quantile |
| `basel_traffic_light(window)` | `window=250` | Classificacao Basel |
| `violation_ratio()` | -- | Razao violacoes observadas / esperadas |
| `summary()` | -- | Relatorio completo de backtesting |

### Rolling Window Backtest Completo

O backtesting com **janela rolante** (rolling window) e a abordagem mais robusta, pois re-estima o modelo a cada passo:

```python
import numpy as np
from archbox import GARCH
from archbox.risk import ValueAtRisk, VaRBacktest
from archbox.datasets import load_dataset

# Dados
sp500 = load_dataset('sp500')
returns = sp500['returns']
n = len(returns)

# Parametros do backtest
window = 1000         # janela de estimacao
alpha = 0.01          # VaR a 99%
var_forecasts = np.full(n, np.nan)

# Rolling window: re-estima GARCH a cada dia
for t in range(window, n):
    # Janela de estimacao
    train = returns[t - window:t]

    # Estimar GARCH(1,1)
    model = GARCH(train, p=1, q=1)
    results = model.fit(disp=False)

    # Previsao de VaR para t+1
    var_calc = ValueAtRisk(results, alpha=alpha)
    var_1step = var_calc.parametric(dist='normal')
    var_forecasts[t] = var_1step[-1]  # ultimo valor = previsao

# Backtesting no periodo out-of-sample
oos_returns = returns[window:]
oos_var = var_forecasts[window:]

bt = VaRBacktest(oos_returns, oos_var, alpha=alpha)
print(bt.summary())

# Testes individuais
kupiec = bt.kupiec_test()
print(f"\nKupiec POF: stat={kupiec.statistic:.4f}, p={kupiec.pvalue:.4f}")

chris = bt.christoffersen_test()
print(f"Christoffersen CC: stat={chris.statistic:.4f}, p={chris.pvalue:.4f}")

dq = bt.dq_test(lags=5)
print(f"Dynamic Quantile: stat={dq.statistic:.4f}, p={dq.pvalue:.4f}")

traffic = bt.basel_traffic_light()
print(f"\nBasel Traffic Light: {traffic}")
```

??? example "Output esperado"
    ```
    ============================================================
    VaR Backtest Summary
    ============================================================
      Observations:      1000
      VaR level (alpha): 0.0100
      Violations:        12
      Violation rate:    0.0120
      Violation ratio:   1.2000

    ------------------------------------------------------------
    Statistical Tests
    ------------------------------------------------------------
      Kupiec POF:        statistic=0.3812, pvalue=0.5371
      Christoffersen CC: statistic=0.8234, pvalue=0.6624
      Dynamic Quantile:  statistic=4.5123, pvalue=0.6074

    ------------------------------------------------------------
      Basel Traffic Light: GREEN (3 violations in last 250 days)
    ============================================================

    Kupiec POF: stat=0.3812, p=0.5371
    Christoffersen CC: stat=0.8234, p=0.6624
    Dynamic Quantile: stat=4.5123, p=0.6074

    Basel Traffic Light: GREEN
    ```

### Comparacao de Modelos via Backtesting

```python
import numpy as np
from archbox import GARCH, EGARCH, GJR
from archbox.risk import ValueAtRisk, VaRBacktest
from archbox.datasets import load_dataset

sp500 = load_dataset('sp500')
returns = sp500['returns']

# Estimar multiplos modelos
models = {
    'GARCH(1,1)': GARCH(returns, p=1, q=1),
    'EGARCH(1,1)': EGARCH(returns, p=1, q=1),
    'GJR-GARCH(1,1)': GJR(returns, p=1, q=1),
}

alpha = 0.01
results_table = []

for name, model in models.items():
    res = model.fit(disp=False)
    var = ValueAtRisk(res, alpha=alpha)
    var_series = var.parametric(dist='studentt', nu=6.0)

    bt = VaRBacktest(returns, var_series, alpha=alpha)
    kupiec = bt.kupiec_test()
    chris = bt.christoffersen_test()
    vr = bt.violation_ratio()
    traffic = bt.basel_traffic_light()

    results_table.append({
        'Modelo': name,
        'Violacoes': f"{(returns < var_series).sum()}",
        'Viol. Ratio': f"{vr:.4f}",
        'Kupiec p': f"{kupiec.pvalue:.4f}",
        'Christ. p': f"{chris.pvalue:.4f}",
        'Basel': traffic,
    })

# Exibir resultados
print(f"{'Modelo':<18} {'Viol.':<7} {'Ratio':<8} {'Kupiec p':<10} {'Christ. p':<10} {'Basel'}")
print("-" * 65)
for r in results_table:
    print(f"{r['Modelo']:<18} {r['Violacoes']:<7} {r['Viol. Ratio']:<8} "
          f"{r['Kupiec p']:<10} {r['Christ. p']:<10} {r['Basel']}")
```

### Backtesting com Multiplas Distribuicoes

```python
from archbox import GARCH
from archbox.risk import ValueAtRisk, VaRBacktest
from archbox.datasets import load_dataset

sp500 = load_dataset('sp500')
returns = sp500['returns']
model = GARCH(returns, p=1, q=1)
results = model.fit(disp=False)

alpha = 0.01
var = ValueAtRisk(results, alpha=alpha)

# Testar diferentes distribuicoes
dists = {
    'Normal': var.parametric(dist='normal'),
    'Student-t (nu=6)': var.parametric(dist='studentt', nu=6.0),
    'Student-t (nu=4)': var.parametric(dist='studentt', nu=4.0),
    'FHS': var.filtered_historical(),
}

print(f"{'Distribuicao':<20} {'Viol.':<7} {'Ratio':<8} {'Kupiec p':<10} {'Basel'}")
print("-" * 55)

for dist_name, var_series in dists.items():
    valid = ~np.isnan(var_series)
    bt = VaRBacktest(returns[valid], var_series[valid], alpha=alpha)
    kupiec = bt.kupiec_test()
    vr = bt.violation_ratio()
    traffic = bt.basel_traffic_light()
    n_viol = (returns[valid] < var_series[valid]).sum()
    print(f"{dist_name:<20} {n_viol:<7} {vr:<8.4f} {kupiec.pvalue:<10.4f} {traffic}")
```

## Interpretacao

### Decisao com Base nos Testes

| Resultado | Interpretacao | Acao |
|-----------|-------------|------|
| Kupiec $p > 0.05$, Christ. $p > 0.05$ | Modelo bem calibrado | Manter o modelo |
| Kupiec $p < 0.05$, $\hat{\pi} > \alpha$ | Subestima risco (muitas violacoes) | Aumentar conservadorismo: usar Student-t ou FHS |
| Kupiec $p < 0.05$, $\hat{\pi} < \alpha$ | Excessivamente conservador | Revisar distribuicao (pode usar Normal) |
| Kupiec $p > 0.05$, Christ. $p < 0.05$ | Violacoes agrupadas (clustering) | Modelo GARCH pode estar mal especificado |
| DQ $p < 0.05$ | VaR tem poder preditivo nas violacoes | Revisar especificacao do modelo |

### Violation Ratio

A **violation ratio** e uma metrica intuitiva de calibracao:

$$VR = \frac{\hat{\pi}}{\alpha} = \frac{x / n}{\alpha}$$

| VR | Interpretacao |
|----|-------------|
| $VR \approx 1.0$ | Modelo perfeitamente calibrado |
| $VR > 1.5$ | Modelo subestima risco significativamente |
| $VR < 0.5$ | Modelo excessivamente conservador |

!!! tip "Regra pratica"
    Um violation ratio entre **0.8 e 1.2** e geralmente aceitavel. Valores acima de 1.5 devem disparar uma revisao do modelo.

## Equivalentes em R e Python

=== "ArchBox"

    ```python
    from archbox.risk import VaRBacktest

    bt = VaRBacktest(returns, var_series, alpha=0.01)
    kupiec = bt.kupiec_test()
    chris = bt.christoffersen_test()
    dq = bt.dq_test(lags=5)
    traffic = bt.basel_traffic_light()
    print(bt.summary())
    ```

=== "R (rugarch)"

    ```r
    library(rugarch)
    library(GAS)

    # Via rugarch rolling forecast
    roll <- ugarchroll(spec, data = returns,
                       n.ahead = 1, forecast.length = 500,
                       refit.every = 25)

    # Backtest VaR
    report(roll, type = "VaR", VaR.alpha = 0.01, conf.level = 0.95)

    # Via GAS package
    BacktestVaR(returns, VaR, alpha = 0.01)
    ```

=== "Python (arch)"

    ```python
    from arch import arch_model
    import numpy as np
    from scipy import stats

    # Implementacao manual do Kupiec
    def kupiec_test(returns, var_series, alpha):
        violations = returns < var_series
        n = len(returns)
        x = violations.sum()
        pi_hat = x / n

        lr = -2 * (x * np.log(alpha) + (n - x) * np.log(1 - alpha)
                    - x * np.log(pi_hat) - (n - x) * np.log(1 - pi_hat))
        p_value = 1 - stats.chi2.cdf(lr, df=1)
        return lr, p_value
    ```

| Funcionalidade | ArchBox | rugarch (R) | arch (Python) |
|---------------|---------|-------------|---------------|
| Kupiec Test | `bt.kupiec_test()` | `VaRTest()` (GAS) | Manual |
| Christoffersen | `bt.christoffersen_test()` | `VaRTest()` (GAS) | Manual |
| Dynamic Quantile | `bt.dq_test()` | Manual | Manual |
| Basel Traffic Light | `bt.basel_traffic_light()` | Manual | Manual |
| Rolling Backtest | `VaRBacktest` + loop | `ugarchroll()` | Manual |
| Violation Ratio | `bt.violation_ratio()` | Manual | Manual |

## References

- Kupiec, P.H. (1995). Techniques for Verifying the Accuracy of Risk Measurement Models. *Journal of Derivatives*, 3(2), 73--84.
- Christoffersen, P.F. (1998). Evaluating Interval Forecasts. *International Economic Review*, 39(4), 841--862.
- Engle, R.F. & Manganelli, S. (2004). CAViaR: Conditional Autoregressive Value at Risk by Regression Quantiles. *Journal of Business & Economic Statistics*, 22(4), 367--381.
- Basel Committee on Banking Supervision (2019). *Minimum Capital Requirements for Market Risk*. Bank for International Settlements.
- Campbell, S.D. (2006). A Review of Backtesting and Backtesting Procedures. *Journal of Risk*, 9(2), 1--17.

## See Also

- [Value-at-Risk (VaR)](var.md) -- Calculo das previsoes de VaR
- [Expected Shortfall (ES/CVaR)](es.md) -- Medida coerente de risco
- [Diagnosticos de Risco](diagnostics.md) -- Loss functions e comparacao de modelos
- [Gestao de Risco: Overview](index.md) -- Pipeline completo de risco
- [ArchExperiment](../experiment.md) -- Comparacao automatizada de modelos
