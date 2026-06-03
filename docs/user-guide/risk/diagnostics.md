---
title: "Diagnosticos de Risco"
description: "Loss functions, comparacao de modelos de risco, coverage analysis e calibration plots."
---

# Diagnosticos de Risco

!!! info "Quick Reference"
    **Module:** `archbox.risk.diagnostics`
    **Import:** `from archbox.risk import RiskDiagnostics`
    **R equivalent:** `rugarch::VaRloss()`, `GAS::BacktestVaR()`
    **Python equivalent:** Manual implementation

## Overview

Os **diagnosticos de risco** complementam o backtesting formal com metricas de qualidade preditiva, permitindo nao apenas verificar se o modelo esta calibrado, mas tambem **comparar** modelos concorrentes e identificar periodos de falha sistematica.

**Quando usar:**

- Selecao entre modelos de volatilidade concorrentes
- Avaliacao da qualidade das previsoes de VaR/ES ao longo do tempo
- Identificacao de periodos de underperformance do modelo
- Calibracao fina de parametros (distribuicao, graus de liberdade)

## Loss Functions para VaR

### Quantile Loss (Tick Loss)

A **quantile loss** (tambem chamada **tick loss** ou **check function**) e a funcao de perda natural para avaliar previsoes de quantis:

$$\rho_\alpha(r_t, q_t) = \begin{cases} \alpha \cdot (r_t - q_t) & \text{se } r_t \geq q_t \\ (1 - \alpha) \cdot (q_t - r_t) & \text{se } r_t < q_t \end{cases}$$

onde $q_t = \text{VaR}_{\alpha,t}$ e a previsao de VaR.

Forma compacta:

$$\rho_\alpha(r_t, q_t) = (r_t - q_t) \cdot (\alpha - \mathbb{1}\{r_t < q_t\})$$

!!! note "Propriedade fundamental"
    A quantile loss e **estritamente consistente** para o quantil $\alpha$: o valor que minimiza $E[\rho_\alpha(r_t, q)]$ e exatamente o quantil verdadeiro $F^{-1}(\alpha)$. Isso garante que a loss function rankeia modelos corretamente.

### Firm's Loss Function (Regulator)

A **regulatory loss function** penaliza assimetricamente as violacoes:

$$L_t^{firm} = \begin{cases} 1 + (r_t - \text{VaR}_t)^2 & \text{se } r_t < \text{VaR}_t \\ 0 & \text{caso contrario} \end{cases}$$

### Quadratic Loss

$$L_t^{quad} = (r_t - \text{VaR}_t)^2 \cdot \mathbb{1}\{r_t < \text{VaR}_t\}$$

### Exemplo: Calculando Loss Functions

```python
import numpy as np
from archbox import GARCH
from archbox.risk import ValueAtRisk, RiskDiagnostics
from archbox.datasets import load_dataset

# 1. Modelo e VaR
sp500 = load_dataset('sp500')
returns = sp500['returns']
model = GARCH(returns, p=1, q=1)
results = model.fit(disp=False)

var = ValueAtRisk(results, alpha=0.05)
var_normal = var.parametric(dist='normal')
var_t = var.parametric(dist='studentt', nu=6.0)

# 2. Loss functions
diag = RiskDiagnostics(returns, alpha=0.05)

ql_normal = diag.quantile_loss(var_normal)
ql_t = diag.quantile_loss(var_t)

print("=== Quantile Loss (menor = melhor) ===")
print(f"  Normal:    {ql_normal:.6f}")
print(f"  Student-t: {ql_t:.6f}")
print(f"  Melhor: {'Student-t' if ql_t < ql_normal else 'Normal'}")
```

??? example "Output esperado"
    ```
    === Quantile Loss (menor = melhor) ===
      Normal:    0.002134
      Student-t: 0.001987
      Melhor: Student-t
    ```

## Comparacao de Modelos

### Diebold-Mariano Test para VaR

O teste de **Diebold-Mariano (1995)** compara formalmente a capacidade preditiva de dois modelos de VaR:

$$H_0: E[d_t] = 0 \qquad \text{vs} \qquad H_1: E[d_t] \neq 0$$

onde $d_t = L_t^{(A)} - L_t^{(B)}$ e o diferencial de perda entre os modelos A e B.

A estatistica de teste com correcao HAC (Newey-West):

$$DM = \frac{\bar{d}}{\sqrt{\hat{V}(\bar{d}) / n}} \xrightarrow{d} N(0, 1)$$

onde $\hat{V}(\bar{d})$ e o estimador de variancia de longo prazo (HAC) de $\bar{d}$.

!!! tip "Interpretacao"
    Se $DM < 0$ e significativo, o modelo A e **superior** (menor loss). Se $DM > 0$ e significativo, o modelo B e superior. Se nao significativo, os modelos sao estatisticamente equivalentes.

### Exemplo: Diebold-Mariano

```python
import numpy as np
from archbox import GARCH, EGARCH, GJR
from archbox.risk import ValueAtRisk, RiskDiagnostics
from archbox.datasets import load_dataset

# 1. Estimar modelos
sp500 = load_dataset('sp500')
returns = sp500['returns']

garch_res = GARCH(returns, p=1, q=1).fit(disp=False)
egarch_res = EGARCH(returns, p=1, q=1).fit(disp=False)
gjr_res = GJR(returns, p=1, q=1).fit(disp=False)

alpha = 0.05
var_garch = ValueAtRisk(garch_res, alpha=alpha).parametric(dist='normal')
var_egarch = ValueAtRisk(egarch_res, alpha=alpha).parametric(dist='normal')
var_gjr = ValueAtRisk(gjr_res, alpha=alpha).parametric(dist='normal')

# 2. Comparacao Diebold-Mariano
diag = RiskDiagnostics(returns, alpha=alpha)

dm_ge = diag.diebold_mariano(var_garch, var_egarch)
print(f"GARCH vs EGARCH: DM={dm_ge.statistic:.4f}, p={dm_ge.pvalue:.4f}")

dm_gj = diag.diebold_mariano(var_garch, var_gjr)
print(f"GARCH vs GJR:    DM={dm_gj.statistic:.4f}, p={dm_gj.pvalue:.4f}")

dm_ej = diag.diebold_mariano(var_egarch, var_gjr)
print(f"EGARCH vs GJR:   DM={dm_ej.statistic:.4f}, p={dm_ej.pvalue:.4f}")
```

??? example "Output esperado"
    ```
    GARCH vs EGARCH: DM=-1.2345, p=0.2170
    GARCH vs GJR:    DM=-2.1456, p=0.0319
    EGARCH vs GJR:   DM=-0.8912, p=0.3728
    ```

## Coverage Analysis

A **coverage analysis** avalia a taxa de violacoes em diferentes subperiodos, identificando se o modelo falha sistematicamente em determinados regimes de mercado.

### Excedencias por Periodo

```python
import numpy as np
from archbox import GARCH
from archbox.risk import ValueAtRisk, RiskDiagnostics
from archbox.datasets import load_dataset

# 1. Modelo e VaR
sp500 = load_dataset('sp500')
returns = sp500['returns']
model = GARCH(returns, p=1, q=1)
results = model.fit(disp=False)

var = ValueAtRisk(results, alpha=0.05)
var_series = var.parametric(dist='normal')

# 2. Coverage analysis
diag = RiskDiagnostics(returns, alpha=0.05)
coverage = diag.coverage_analysis(var_series, periods='quarterly')

print("=== Coverage por Trimestre ===")
print(f"{'Periodo':<12} {'Obs':<6} {'Viol.':<7} {'Taxa':<8} {'Esperado':<10} {'Status'}")
print("-" * 55)
for period in coverage:
    status = "OK" if abs(period['rate'] - 0.05) < 0.03 else "ATENCAO"
    print(f"{period['name']:<12} {period['n']:<6} {period['violations']:<7} "
          f"{period['rate']:<8.4f} {0.05:<10.4f} {status}")
```

### Excedencias Condicionais

Analise de violacoes condicionadas ao nivel de volatilidade:

```python
# Excedencias em diferentes regimes de volatilidade
diag = RiskDiagnostics(returns, alpha=0.05)
cond_coverage = diag.conditional_coverage(
    var_series,
    conditioning_var=results.conditional_volatility,
    n_bins=4
)

print("=== Coverage Condicional (por quartil de volatilidade) ===")
print(f"{'Quartil':<10} {'Vol Media':<12} {'Taxa Viol.':<12} {'Esperado'}")
print("-" * 48)
for q in cond_coverage:
    print(f"{q['quantile']:<10} {q['avg_vol']:<12.6f} "
          f"{q['violation_rate']:<12.4f} {0.05:.4f}")
```

!!! warning "Padrao tipico"
    Modelos GARCH com distribuicao Normal tendem a **subestimar** o risco em periodos de alta volatilidade (mais violacoes no quartil superior). A distribuicao Student-t ou FHS corrige parcialmente esse problema.

## Calibration Plots

Os **calibration plots** visualizam a qualidade da calibracao do modelo de risco:

### VaR vs Retornos

```python
import numpy as np
from archbox import GARCH
from archbox.risk import ValueAtRisk, RiskDiagnostics
from archbox.datasets import load_dataset

# 1. Modelo e VaR
sp500 = load_dataset('sp500')
returns = sp500['returns']
model = GARCH(returns, p=1, q=1)
results = model.fit(disp=False)

var = ValueAtRisk(results, alpha=0.05)
var_series = var.parametric(dist='normal')

# 2. Calibration plot
diag = RiskDiagnostics(returns, alpha=0.05)
fig = diag.calibration_plot(var_series)
fig.savefig('calibration_var.png', dpi=150, bbox_inches='tight')
```

### PIT Histogram (Probability Integral Transform)

O histograma PIT verifica se as probabilidades previstas sao uniformemente distribuidas:

```python
# PIT histogram: se o modelo esta correto, as probabilidades
# transformadas devem ser U(0,1)
fig = diag.pit_histogram(var_series, bins=20)
fig.savefig('pit_histogram.png', dpi=150, bbox_inches='tight')
```

!!! note "Interpretacao do PIT"
    Um histograma PIT uniforme indica modelo bem calibrado. Excesso de massa na cauda esquerda (valores proximos de 0) indica subestimacao do risco. Excesso na cauda direita indica superestimacao.

## ES Backtesting

### McNeil & Frey (2000) Bootstrap Test

O backtesting do Expected Shortfall e mais desafiador que o do VaR. McNeil & Frey (2000) propoe um teste baseado nos **residuos de excedencia**:

$$e_t = \frac{r_t - ES_{\alpha,t}}{\sigma_t} \quad \text{para } t \text{ onde } r_t < \text{VaR}_{\alpha,t}$$

Sob $H_0$ (modelo correto), $E[e_t] = 0$.

O teste usa bootstrap para construir intervalos de confianca para $\bar{e}$.

```python
from archbox import GARCH
from archbox.risk import ValueAtRisk, ExpectedShortfall, RiskDiagnostics
from archbox.datasets import load_dataset

# 1. Modelo, VaR e ES
sp500 = load_dataset('sp500')
returns = sp500['returns']
model = GARCH(returns, p=1, q=1)
results = model.fit(disp=False)

alpha = 0.05
var = ValueAtRisk(results, alpha=alpha)
es = ExpectedShortfall(results, alpha=alpha)
var_series = var.parametric(dist='normal')
es_series = es.parametric(dist='normal')

# 2. ES backtest (McNeil & Frey)
diag = RiskDiagnostics(returns, alpha=alpha)
es_test = diag.es_backtest(var_series, es_series, method='mcneil_frey')

print("=== ES Backtest (McNeil & Frey) ===")
print(f"  Excedencias analisadas: {es_test.n_exceed}")
print(f"  Residuo medio: {es_test.mean_residual:.6f}")
print(f"  Bootstrap p-value: {es_test.pvalue:.4f}")
print(f"  Resultado: {'Modelo aceito' if es_test.pvalue > 0.05 else 'Modelo rejeitado'}")
```

??? example "Output esperado"
    ```
    === ES Backtest (McNeil & Frey) ===
      Excedencias analisadas: 98
      Residuo medio: -0.001234
      Bootstrap p-value: 0.3456
      Resultado: Modelo aceito
    ```

### Acerbi & Szekely (2014) Test

Teste mais recente baseado na integral da funcao de distribuicao empirica:

$$Z_2 = \frac{1}{n \cdot \alpha} \sum_{t=1}^{n} \frac{r_t \cdot \mathbb{1}\{r_t < \text{VaR}_{\alpha,t}\}}{ES_{\alpha,t}} + 1$$

Sob $H_0$: $E[Z_2] = 0$.

```python
# ES backtest (Acerbi & Szekely)
es_test_as = diag.es_backtest(var_series, es_series, method='acerbi_szekely')
print(f"Acerbi-Szekely Z2: {es_test_as.statistic:.4f}, p={es_test_as.pvalue:.4f}")
```

## Pipeline Completo de Diagnosticos

```python
import numpy as np
from archbox import GARCH, EGARCH, GJR
from archbox.risk import ValueAtRisk, ExpectedShortfall, VaRBacktest, RiskDiagnostics
from archbox.datasets import load_dataset

# 1. Dados
sp500 = load_dataset('sp500')
returns = sp500['returns']
alpha = 0.05

# 2. Estimar modelos
models = {
    'GARCH': GARCH(returns, p=1, q=1).fit(disp=False),
    'EGARCH': EGARCH(returns, p=1, q=1).fit(disp=False),
    'GJR': GJR(returns, p=1, q=1).fit(disp=False),
}

# 3. Calcular VaR para cada modelo
var_series = {}
for name, res in models.items():
    var = ValueAtRisk(res, alpha=alpha)
    var_series[name] = var.parametric(dist='studentt', nu=6.0)

# 4. Backtesting
print("=== Backtesting ===")
for name, vs in var_series.items():
    bt = VaRBacktest(returns, vs, alpha=alpha)
    kupiec = bt.kupiec_test()
    vr = bt.violation_ratio()
    print(f"  {name:<8}: VR={vr:.3f}, Kupiec p={kupiec.pvalue:.4f}")

# 5. Loss functions
print("\n=== Quantile Loss ===")
diag = RiskDiagnostics(returns, alpha=alpha)
for name, vs in var_series.items():
    ql = diag.quantile_loss(vs)
    print(f"  {name:<8}: {ql:.6f}")

# 6. Comparacao pairwise (Diebold-Mariano)
print("\n=== Diebold-Mariano ===")
names = list(var_series.keys())
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        dm = diag.diebold_mariano(var_series[names[i]], var_series[names[j]])
        winner = names[i] if dm.statistic < 0 else names[j]
        sig = "*" if dm.pvalue < 0.05 else ""
        print(f"  {names[i]} vs {names[j]}: DM={dm.statistic:.4f}, "
              f"p={dm.pvalue:.4f} {sig} -> {winner}")

# 7. Coverage analysis
print("\n=== Coverage Analysis (GARCH) ===")
coverage = diag.coverage_analysis(var_series['GARCH'], periods='quarterly')
for period in coverage[:4]:
    print(f"  {period['name']}: taxa={period['rate']:.4f} (esperado={alpha:.4f})")
```

## Equivalentes em R e Python

=== "ArchBox"

    ```python
    from archbox.risk import RiskDiagnostics

    diag = RiskDiagnostics(returns, alpha=0.05)

    # Loss functions
    ql = diag.quantile_loss(var_series)

    # Comparacao
    dm = diag.diebold_mariano(var_a, var_b)

    # Coverage
    coverage = diag.coverage_analysis(var_series, periods='quarterly')

    # ES backtest
    es_test = diag.es_backtest(var_series, es_series)
    ```

=== "R (rugarch)"

    ```r
    library(rugarch)
    library(GAS)

    # Quantile loss manual
    tick_loss <- function(r, q, alpha) {
      (r - q) * (alpha - as.numeric(r < q))
    }

    # Diebold-Mariano via forecast package
    library(forecast)
    dm.test(loss_a, loss_b, alternative = "two.sided")

    # ES backtest
    # McNeil-Frey: manual ou via esback package
    library(esback)
    esr_backtest(r = returns, e = es, v = var, alpha = 0.05)
    ```

=== "Python (arch)"

    ```python
    from scipy import stats
    import numpy as np

    # Quantile loss manual
    def quantile_loss(returns, var, alpha):
        diff = returns - var
        return np.mean(diff * (alpha - (diff < 0)))

    # Diebold-Mariano manual
    def dm_test(loss_a, loss_b):
        d = loss_a - loss_b
        dm_stat = d.mean() / (d.std() / np.sqrt(len(d)))
        p_value = 2 * (1 - stats.norm.cdf(abs(dm_stat)))
        return dm_stat, p_value
    ```

| Funcionalidade | ArchBox | rugarch (R) | arch (Python) |
|---------------|---------|-------------|---------------|
| Quantile Loss | `diag.quantile_loss()` | `VaRloss()` | Manual |
| Diebold-Mariano | `diag.diebold_mariano()` | `dm.test()` (forecast) | Manual |
| Coverage Analysis | `diag.coverage_analysis()` | Manual | Manual |
| ES Backtest | `diag.es_backtest()` | `esr_backtest()` (esback) | Manual |
| Calibration Plot | `diag.calibration_plot()` | Manual | Manual |
| PIT Histogram | `diag.pit_histogram()` | `pit()` (rugarch) | Manual |

## References

- Diebold, F.X. & Mariano, R.S. (1995). Comparing Predictive Accuracy. *Journal of Business & Economic Statistics*, 13(3), 253--263.
- Gonzalez-Rivera, G., Lee, T.-H., & Mishra, S. (2004). Forecasting Volatility: A Reality Check Based on Option Pricing, Utility Function, Value-at-Risk, and Predictive Likelihood. *International Journal of Forecasting*, 20(4), 629--645.
- McNeil, A.J. & Frey, R. (2000). Estimation of Tail-Related Risk Measures for Heteroscedastic Financial Time Series: An Extreme Value Approach. *Journal of Empirical Finance*, 7(3-4), 271--300.
- Acerbi, C. & Szekely, B. (2014). Back-testing Expected Shortfall. *Risk*, 27(11), 76--81.
- Gneiting, T. (2011). Making and Evaluating Point Forecasts. *Journal of the American Statistical Association*, 106(494), 746--762.

## See Also

- [Backtesting de VaR/ES](backtesting.md) -- Testes formais de backtesting
- [Value-at-Risk (VaR)](var.md) -- Calculo das previsoes de VaR
- [Expected Shortfall (ES/CVaR)](es.md) -- Medida coerente de risco
- [ArchExperiment](../experiment.md) -- Comparacao automatizada de modelos
- [Gestao de Risco: Overview](index.md) -- Pipeline completo de risco
