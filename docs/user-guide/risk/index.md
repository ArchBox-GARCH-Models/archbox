---
title: "Gestao de Risco"
description: "Visao geral das metricas de risco: VaR, Expected Shortfall e EWMA no archbox."
---

# Gestao de Risco

!!! info "Quick Reference"
    **Modulo:** `archbox.risk`
    **Import:** `from archbox.risk import ValueAtRisk, ExpectedShortfall, EWMA, VaRBacktest`
    **R equivalent:** `rugarch::ugarchroll()`, `rmgarch`
    **Python equivalent:** `arch.univariate.ARCHModelResult.forecast()`

## Overview

O modulo de **gestao de risco** do archbox implementa as principais metricas quantitativas de risco de mercado utilizadas por instituicoes financeiras, reguladores e gestores de carteira. O framework segue o pipeline padrao da industria: **modelo de volatilidade $\rightarrow$ distribuicao condicional $\rightarrow$ metrica de risco $\rightarrow$ backtesting**.

Apos estimar um modelo de volatilidade condicional (GARCH, EGARCH, GJR-GARCH, etc.), as metricas de risco sao calculadas diretamente a partir dos resultados do modelo, garantindo consistencia entre estimacao e medicao de risco.

## Contexto Regulatorio: Basel III/IV

!!! note "Regulacao e metricas de risco"
    O **Comite de Basileia (BCBS)** define os requisitos minimos de capital para risco de mercado. A evolucao regulatoria e diretamente refletida nas metricas implementadas:

    - **Basel II (1996/2004)**: VaR a 99% com janela de 10 dias como metrica principal
    - **Basel III (2010)**: Introducao do **Expected Shortfall (ES)** a 97.5% como substituto do VaR
    - **Basel IV / FRTB (2019+)**: ES como metrica principal; VaR mantido apenas para backtesting

    A transicao de VaR para ES reflete a necessidade de capturar **tail risk** — perdas extremas que o VaR, por ser apenas um quantil, nao consegue medir adequadamente.

## Metricas Disponveis

| Metrica | Classe | Descricao | Regulacao |
|---------|--------|-----------|-----------|
| **Value-at-Risk** | `ValueAtRisk` | Perda maxima com nivel de confianca | Basel II (metrica principal), Basel III (backtesting) |
| **Expected Shortfall** | `ExpectedShortfall` | Perda esperada alem do VaR | Basel III/IV (metrica principal) |
| **EWMA** | `EWMA` | Volatilidade com decaimento exponencial | RiskMetrics (padrao da industria) |
| **Backtesting** | `VaRBacktest` | Validacao estatistica do VaR | Basel (exigencia regulatoria) |

## Pipeline de Risco

O fluxo completo de gestao de risco no archbox segue 4 etapas:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  1. Volatilidade │────>│  2. Distribuicao │────>│  3. Metrica     │────>│  4. Backtesting  │
│                 │     │                 │     │                 │     │                 │
│  GARCH(1,1)     │     │  Normal          │     │  VaR            │     │  Kupiec          │
│  EGARCH         │     │  Student-t       │     │  ES / CVaR      │     │  Christoffersen   │
│  GJR-GARCH      │     │  Skew-t          │     │  EWMA           │     │  Basel Traffic    │
│  EWMA           │     │  GED             │     │                 │     │  Light           │
└─────────────────┘     └─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Exemplo do Pipeline Completo

```python
from archbox import GARCH
from archbox.risk import ValueAtRisk, ExpectedShortfall, VaRBacktest
from archbox.datasets import load_dataset

# 1. Modelo de volatilidade
sp500 = load_dataset('sp500')
model = GARCH(sp500['returns'], p=1, q=1)
results = model.fit()

# 2. Metricas de risco (distribuicao Normal)
var_calc = ValueAtRisk(results, alpha=0.05)
var_series = var_calc.parametric(dist='normal')

es_calc = ExpectedShortfall(results, alpha=0.05)
es_series = es_calc.parametric(dist='normal')

# 3. Backtesting do VaR
backtest = VaRBacktest(sp500['returns'], var_series, alpha=0.05)
print(backtest.summary())
```

### Pipeline Rapido com EWMA

Para estimativas rapidas sem otimizacao numerica:

```python
from archbox.risk import EWMA, ValueAtRisk

# EWMA nao requer otimizacao — apenas lambda
ewma = EWMA(returns, lam=0.94)
ewma_result = ewma.fit()

# VaR a partir do EWMA
var_calc = ValueAtRisk(ewma_result, alpha=0.01)
var_series = var_calc.parametric(dist='normal')
```

## Escolhendo a Metrica

| Cenario | Metrica Recomendada | Justificativa |
|---------|-------------------|---------------|
| Relatorio regulatorio (Basel III+) | **ES** a 97.5% | Exigencia regulatoria |
| Backtesting e validacao | **VaR** a 99% | Testes estatisticos bem estabelecidos |
| Estimativa rapida / monitoramento diario | **EWMA** | Sem otimizacao, atualizacao trivial |
| Gestao interna de limites | **VaR** a 95% ou 99% | Interpretacao intuitiva |
| Analise de tail risk | **ES** | Captura magnitude das perdas extremas |
| Carteira com fat tails | **ES** com Student-t | Subaditividade + caudas pesadas |

!!! tip "Recomendacao pratica"
    Na pratica, utilize **VaR para comunicacao e limites** (facil de explicar) e **ES para decisoes de alocacao** (captura tail risk). O EWMA e ideal para **dashboards em tempo real** onde velocidade importa mais que precisao estatistica.

## Abordagens de Calculo

O archbox suporta tres abordagens para VaR e ES:

=== "Parametrico"

    Utiliza o modelo GARCH + distribuicao analitica. Mais eficiente e permite previsao forward-looking.

    ```python
    var = ValueAtRisk(results, alpha=0.05)
    var_parametric = var.parametric(dist='normal')
    ```

=== "Historico"

    Baseado no quantil empirico dos retornos observados. Nao assume distribuicao parametrica.

    ```python
    var = ValueAtRisk(results, alpha=0.05)
    var_hist = var.historical(window=250)
    ```

=== "Monte Carlo"

    Simula caminhos futuros a partir do modelo GARCH estimado.

    ```python
    var = ValueAtRisk(results, alpha=0.05)
    var_mc = var.monte_carlo(n_sims=10000, horizon=1, seed=42)
    ```

## References

- JP Morgan (1996). *RiskMetrics Technical Document*. 4th ed.
- Artzner, P., Delbaen, F., Eber, J.-M., & Heath, D. (1999). Coherent Measures of Risk. *Mathematical Finance*, 9(3), 203--228.
- McNeil, A.J., Frey, R., & Embrechts, P. (2015). *Quantitative Risk Management*. 2nd ed. Princeton University Press.
- Basel Committee on Banking Supervision (2019). *Minimum Capital Requirements for Market Risk*. Bank for International Settlements.
- Kupiec, P.H. (1995). Techniques for Verifying the Accuracy of Risk Measurement Models. *Journal of Derivatives*, 3(2), 73--84.
- Christoffersen, P.F. (1998). Evaluating Interval Forecasts. *International Economic Review*, 39(4), 841--862.

## See Also

- [Value-at-Risk (VaR)](var.md) -- Tres abordagens para calculo do VaR
- [Expected Shortfall (ES/CVaR)](es.md) -- Medida coerente de risco
- [EWMA / RiskMetrics](ewma.md) -- Volatilidade com decaimento exponencial
- [Modelos GARCH](../garch/index.md) -- Modelos de volatilidade condicional
- [Distribuicoes Condicionais](../distributions/index.md) -- Escolha da distribuicao para os erros
