---
title: "ArchExperiment"
description: "Workflow automatizado para comparacao de modelos ARCH/GARCH: pipeline, criterios de selecao e report."
---

# ArchExperiment

!!! info "Quick Reference"
    **Class:** `archbox.experiment.ArchExperiment`
    **Import:** `from archbox import ArchExperiment`
    **R equivalent:** Nenhum equivalente direto
    **Python equivalent:** Nenhum equivalente direto

## Overview

O **ArchExperiment** e um workflow automatizado para comparacao sistematica de modelos de volatilidade. Ele encapsula o pipeline completo de especificacao, estimacao, comparacao e reporte em uma interface unificada.

**Quando usar:**

- Selecionar o melhor modelo de volatilidade para uma serie temporal
- Comparar distribuicoes condicionais (Normal vs Student-t vs Mixture)
- Gerar relatorios de risco com multiplos modelos
- Automatizar backtesting comparativo

**Pipeline:**

```
Especificar modelos → Fit (paralelo) → Comparar → Selecionar → Report
```

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  add_model() │───>│    run()     │───>│  summary()   │───>│  report()   │
│             │    │             │    │             │    │             │
│ - GARCH     │    │ - Fit all   │    │ - AIC/BIC   │    │ - HTML      │
│ - EGARCH    │    │ - Parallel  │    │ - LogLik    │    │ - LaTeX     │
│ - GJR       │    │ - Backtest  │    │ - VaR test  │    │ - CSV       │
│ - ...       │    │             │    │ - Rankings  │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

## Quick Example

```python
import archbox as ab

# 1. Carregar dados
sp500 = ab.load_dataset('sp500')
returns = sp500['returns']

# 2. Configurar experimento
exp = ab.ArchExperiment(returns)

# 3. Adicionar modelos para comparacao
exp.add_model(ab.GARCH(1, 1))
exp.add_model(ab.EGARCH(1, 1))
exp.add_model(ab.GJR(1, 1))

# 4. Executar
exp.run()

# 5. Resultados
exp.summary()  # tabela comparativa
```

??? example "Output esperado"
    ```
    ================================================================
    ArchExperiment Summary
    ================================================================
    Data: 2000 observations
    Models: 3
    Best model (BIC): EGARCH(1,1)
    ================================================================

    Model            LogLik      AIC         BIC         VaR Kupiec p
    ----------------------------------------------------------------
    GARCH(1,1)       6234.12     -12460.24   -12437.89   0.6523
    EGARCH(1,1)      6248.56     -12487.12   -12459.34   0.7812
    GJR(1,1)         6245.89     -12481.78   -12454.00   0.7234

    Rankings:
      AIC:  1. EGARCH  2. GJR  3. GARCH
      BIC:  1. EGARCH  2. GJR  3. GARCH
    ================================================================
    ```

## Guia Detalhado

### Parametros do Construtor

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `returns` | array-like | obrigatorio | Serie de retornos |
| `alpha` | float | `0.05` | Nivel de significancia para backtesting de VaR |
| `n_jobs` | int | `-1` | Numero de processos paralelos (`-1` = todos os cores) |

### Metodos

| Metodo | Parametros | Descricao |
|--------|-----------|-----------|
| `add_model(model)` | model: ArchModel | Adiciona modelo ao experimento |
| `add_models(models)` | models: list | Adiciona lista de modelos |
| `run(disp)` | `disp=False` | Estima todos os modelos |
| `summary()` | -- | Tabela comparativa em texto |
| `results_table()` | -- | DataFrame com metricas |
| `best_model(criterion)` | `criterion='bic'` | Retorna o melhor modelo |
| `report(format)` | `format='html'` | Gera relatorio completo |
| `plot_comparison()` | -- | Visualizacao comparativa |
| `plot_volatilities()` | -- | Volatilidades estimadas sobrepostas |

### Especificando Modelos

```python
import archbox as ab

exp = ab.ArchExperiment(returns)

# Modelos individuais
exp.add_model(ab.GARCH(1, 1))
exp.add_model(ab.GARCH(2, 1))
exp.add_model(ab.EGARCH(1, 1))
exp.add_model(ab.GJR(1, 1))

# Ou em lote
exp.add_models([
    ab.GARCH(1, 1),
    ab.GARCH(2, 1),
    ab.EGARCH(1, 1),
    ab.GJR(1, 1),
])
```

### Modelos com Diferentes Distribuicoes

```python
import archbox as ab

exp = ab.ArchExperiment(returns)

# Mesmo modelo, diferentes distribuicoes
exp.add_model(ab.GARCH(1, 1, dist='normal'), name='GARCH-N')
exp.add_model(ab.GARCH(1, 1, dist='student-t'), name='GARCH-t')
exp.add_model(ab.GARCH(1, 1, dist='ged'), name='GARCH-GED')

# Modelos assimetricos com Student-t
exp.add_model(ab.EGARCH(1, 1, dist='student-t'), name='EGARCH-t')
exp.add_model(ab.GJR(1, 1, dist='student-t'), name='GJR-t')

exp.run()
exp.summary()
```

??? example "Output esperado"
    ```
    ================================================================
    ArchExperiment Summary
    ================================================================
    Data: 2000 observations
    Models: 5
    Best model (BIC): EGARCH-t
    ================================================================

    Model            LogLik      AIC         BIC         VaR Kupiec p
    ----------------------------------------------------------------
    GARCH-N          6234.12     -12460.24   -12437.89   0.6523
    GARCH-t          6252.34     -12494.68   -12466.90   0.7891
    GARCH-GED        6248.90     -12487.80   -12460.02   0.7456
    EGARCH-t         6261.45     -12510.90   -12477.69   0.8234
    GJR-t            6258.12     -12504.24   -12471.03   0.8012

    Rankings:
      AIC:  1. EGARCH-t  2. GJR-t  3. GARCH-t  4. GARCH-GED  5. GARCH-N
      BIC:  1. EGARCH-t  2. GJR-t  3. GARCH-t  4. GARCH-GED  5. GARCH-N
    ================================================================
    ```

## Criterios de Comparacao

### Criterios de Informacao

| Criterio | Formula | Descricao |
|----------|---------|-----------|
| **AIC** | $-2\ell + 2k$ | Akaike Information Criterion |
| **BIC** | $-2\ell + k\ln(n)$ | Bayesian Information Criterion |
| **HQC** | $-2\ell + 2k\ln(\ln(n))$ | Hannan-Quinn Criterion |

onde $\ell$ e a log-verossimilhanca, $k$ o numero de parametros e $n$ o tamanho da amostra.

!!! note "AIC vs BIC"
    O **BIC** penaliza mais modelos complexos (especialmente para $n$ grande) e tende a selecionar modelos mais **parcimoniosos**. O **AIC** favorece capacidade preditiva. Na pratica, use BIC para selecao de modelo e AIC para previsao.

### Log-Likelihood

A log-verossimilhanca permite comparar modelos diretamente quando tem o mesmo numero de parametros. Maior e melhor.

### VaR Backtest

O Kupiec test (p-value) e incluido automaticamente como criterio adicional. Modelos com p-value muito baixo sao mal calibrados.

### Acessando Resultados Detalhados

```python
import archbox as ab

exp = ab.ArchExperiment(returns)
exp.add_model(ab.GARCH(1, 1))
exp.add_model(ab.EGARCH(1, 1))
exp.add_model(ab.GJR(1, 1))
exp.run()

# DataFrame com todas as metricas
df = exp.results_table()
print(df.to_string())

# Melhor modelo por criterio
best_bic = exp.best_model(criterion='bic')
print(f"\nMelhor modelo (BIC): {best_bic.name}")
print(f"  BIC: {best_bic.bic:.2f}")
print(f"  Parametros: {best_bic.params}")

best_aic = exp.best_model(criterion='aic')
print(f"\nMelhor modelo (AIC): {best_aic.name}")

# Acessar resultados individuais
for name, result in exp.fitted_models.items():
    print(f"\n{name}:")
    print(f"  omega={result.params['omega']:.6f}")
    print(f"  alpha={result.params['alpha[1]']:.4f}")
    print(f"  beta={result.params['beta[1]']:.4f}")
    print(f"  Persistencia: {result.persistence:.4f}")
```

## Visualizacoes Automaticas

### Comparacao de Volatilidades

```python
import archbox as ab

exp = ab.ArchExperiment(returns)
exp.add_model(ab.GARCH(1, 1))
exp.add_model(ab.EGARCH(1, 1))
exp.add_model(ab.GJR(1, 1))
exp.run()

# Plot de volatilidades sobrepostas
fig = exp.plot_volatilities()
fig.savefig('volatilities_comparison.png', dpi=150, bbox_inches='tight')
```

### Comparacao de Metricas

```python
# Bar chart com AIC, BIC
fig = exp.plot_comparison(metric='bic')
fig.savefig('bic_comparison.png', dpi=150, bbox_inches='tight')
```

### News Impact Curves

```python
# News impact curves sobrepostas
fig = exp.plot_news_impact()
fig.savefig('news_impact_comparison.png', dpi=150, bbox_inches='tight')
```

!!! tip "Visualizacao rapida"
    O metodo `plot_comparison()` aceita `metric='all'` para gerar um grid com todas as metricas de uma vez.

## Export de Resultados

### HTML Report

```python
import archbox as ab

exp = ab.ArchExperiment(returns)
exp.add_model(ab.GARCH(1, 1))
exp.add_model(ab.EGARCH(1, 1))
exp.add_model(ab.GJR(1, 1))
exp.run()

# Report HTML completo
exp.report('html', output='experiment_report.html')
```

O report HTML inclui:

- Tabela comparativa de metricas
- Graficos de volatilidade
- Resultados de backtesting
- News impact curves
- Parametros estimados de cada modelo

### LaTeX Report

```python
# Report em LaTeX (para artigos/dissertacoes)
exp.report('latex', output='experiment_report.tex')
```

### CSV Export

```python
# Exportar metricas como CSV
df = exp.results_table()
df.to_csv('experiment_results.csv', index=False)

# Exportar volatilidades
vol_df = exp.volatilities_dataframe()
vol_df.to_csv('volatilities.csv')
```

## Exemplo Completo: Pipeline de Producao

```python
import archbox as ab
import numpy as np

# =====================================================
# 1. Dados
# =====================================================
sp500 = ab.load_dataset('sp500')
returns = sp500['returns']

# =====================================================
# 2. Configurar experimento amplo
# =====================================================
exp = ab.ArchExperiment(returns, alpha=0.01)

# Modelos simetricos
exp.add_model(ab.GARCH(1, 1, dist='normal'), name='GARCH(1,1)-N')
exp.add_model(ab.GARCH(1, 1, dist='student-t'), name='GARCH(1,1)-t')
exp.add_model(ab.GARCH(2, 1, dist='student-t'), name='GARCH(2,1)-t')

# Modelos assimetricos
exp.add_model(ab.EGARCH(1, 1, dist='normal'), name='EGARCH(1,1)-N')
exp.add_model(ab.EGARCH(1, 1, dist='student-t'), name='EGARCH(1,1)-t')
exp.add_model(ab.GJR(1, 1, dist='normal'), name='GJR(1,1)-N')
exp.add_model(ab.GJR(1, 1, dist='student-t'), name='GJR(1,1)-t')

# =====================================================
# 3. Executar (estimacao paralela)
# =====================================================
exp.run(disp=False)

# =====================================================
# 4. Resultados
# =====================================================

# Tabela resumo
print(exp.summary())

# Melhor modelo
best = exp.best_model(criterion='bic')
print(f"\n>>> Modelo selecionado: {best.name}")
print(f"    BIC: {best.bic:.2f}")
print(f"    Persistencia: {best.persistence:.4f}")

# =====================================================
# 5. Analise do modelo selecionado
# =====================================================

# Volatilidade condicional
sigma = best.conditional_volatility
print(f"\nVolatilidade media: {sigma.mean():.6f}")
print(f"Volatilidade max:   {sigma.max():.6f}")

# VaR e ES com o melhor modelo
var = ab.ValueAtRisk(best, alpha=0.01)
var_series = var.parametric(dist='studentt')
print(f"VaR medio (1%): {var_series.mean():.6f}")

es = ab.ExpectedShortfall(best, alpha=0.01)
es_series = es.parametric(dist='studentt')
print(f"ES medio (1%):  {es_series.mean():.6f}")

# Backtest do modelo selecionado
bt = ab.VaRBacktest(returns, var_series, alpha=0.01)
print(f"\nBasel Traffic Light: {bt.basel_traffic_light()}")

# =====================================================
# 6. Export
# =====================================================
exp.report('html', output='model_selection_report.html')
exp.results_table().to_csv('model_comparison.csv', index=False)
```

??? example "Output esperado"
    ```
    ================================================================
    ArchExperiment Summary
    ================================================================
    Data: 2000 observations
    Models: 7
    Best model (BIC): EGARCH(1,1)-t
    ================================================================

    Model              LogLik      AIC         BIC         VaR Kupiec p
    ------------------------------------------------------------------
    GARCH(1,1)-N       6234.12     -12460.24   -12437.89   0.4523
    GARCH(1,1)-t       6252.34     -12494.68   -12466.90   0.6891
    GARCH(2,1)-t       6253.01     -12494.02   -12460.81   0.7012
    EGARCH(1,1)-N      6248.56     -12487.12   -12459.34   0.5812
    EGARCH(1,1)-t      6265.89     -12519.78   -12486.57   0.8234
    GJR(1,1)-N         6245.89     -12481.78   -12454.00   0.5234
    GJR(1,1)-t         6262.12     -12512.24   -12479.03   0.8012

    Rankings:
      AIC:  1. EGARCH(1,1)-t  2. GJR(1,1)-t  3. GARCH(2,1)-t  ...
      BIC:  1. EGARCH(1,1)-t  2. GJR(1,1)-t  3. GARCH(1,1)-t  ...
    ================================================================

    >>> Modelo selecionado: EGARCH(1,1)-t
        BIC: -12486.57
        Persistencia: 0.9876

    Volatilidade media: 0.012345
    Volatilidade max:   0.065432
    VaR medio (1%): -0.032145
    ES medio (1%):  -0.041234

    Basel Traffic Light: GREEN
    ```

## Equivalentes em R e Python

=== "ArchBox"

    ```python
    import archbox as ab

    exp = ab.ArchExperiment(returns)
    exp.add_model(ab.GARCH(1, 1))
    exp.add_model(ab.EGARCH(1, 1))
    exp.add_model(ab.GJR(1, 1))
    exp.run()
    exp.summary()
    exp.report('html')
    ```

=== "R (rugarch)"

    ```r
    library(rugarch)

    # Nao ha equivalente direto - comparacao manual:
    specs <- list(
      sGARCH = ugarchspec(variance.model = list(model = "sGARCH")),
      eGARCH = ugarchspec(variance.model = list(model = "eGARCH")),
      gjrGARCH = ugarchspec(variance.model = list(model = "gjrGARCH"))
    )

    fits <- lapply(specs, function(s) ugarchfit(s, data = returns))
    sapply(fits, infocriteria)  # Matriz de AIC, BIC, etc.
    ```

=== "Python (arch)"

    ```python
    from arch import arch_model

    # Nao ha equivalente direto - comparacao manual:
    models = {
        'GARCH': arch_model(returns, vol='Garch', p=1, q=1),
        'EGARCH': arch_model(returns, vol='EGARCH', p=1, q=1),
        'GJR': arch_model(returns, vol='GARCH', p=1, o=1, q=1),
    }

    results = {k: m.fit(disp='off') for k, m in models.items()}
    for name, res in results.items():
        print(f"{name}: AIC={res.aic:.2f}, BIC={res.bic:.2f}")
    ```

| Funcionalidade | ArchBox | rugarch (R) | arch (Python) |
|---------------|---------|-------------|---------------|
| Pipeline automatizado | `ArchExperiment` | Manual | Manual |
| Estimacao paralela | `exp.run()` | Manual (parallel) | Manual |
| Tabela comparativa | `exp.summary()` | `infocriteria()` | Manual |
| Selecao automatica | `exp.best_model()` | Manual | Manual |
| Report HTML | `exp.report('html')` | Manual (knitr) | Manual |
| Visualizacoes | `exp.plot_*()` | Manual (ggplot2) | Manual |

## References

- Burnham, K.P. & Anderson, D.R. (2002). *Model Selection and Multimodel Inference*. 2nd ed. Springer.
- Hansen, P.R. & Lunde, A. (2005). A Forecast Comparison of Volatility Models: Does Anything Beat a GARCH(1,1)? *Journal of Applied Econometrics*, 20(7), 873--889.
- Engle, R.F. & Patton, A.J. (2001). What Good is a Volatility Model? *Quantitative Finance*, 1(2), 237--245.
- Laurent, S., Rombouts, J.V.K., & Violante, F. (2012). On the Forecasting Accuracy of Multivariate GARCH Models. *Journal of Applied Econometrics*, 27(6), 934--955.

## See Also

- [Modelos GARCH](garch/index.md) -- GARCH, EGARCH, GJR-GARCH
- [Distribuicoes Condicionais](distributions/index.md) -- Normal, Student-t, GED
- [Backtesting de VaR](risk/backtesting.md) -- Validacao estatistica
- [Diagnosticos de Risco](risk/diagnostics.md) -- Loss functions e comparacao
- [Gestao de Risco](risk/index.md) -- Pipeline completo de risco
