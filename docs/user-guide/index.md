---
title: User Guide
description: Comprehensive guides for all volatility models, distributions, and risk management tools in ArchBox.
---

# User Guide

ArchBox provides **30+ models and tools** across 6 families, covering the main approaches to conditional volatility modeling, regime-switching dynamics, threshold nonlinearity, and financial risk management used in applied research and industry.

All models follow a consistent API: pass your returns series, set model parameters, and call `.fit()`. Results objects provide `.summary()`, parameter tables, conditional volatility, diagnostic tests, forecasting, and export capabilities.

<div class="grid cards" markdown>

- :material-chart-line: **[GARCH Univariado](garch/index.md)**

    ---

    GARCH, EGARCH, GJR-GARCH, APARCH, FIGARCH, IGARCH, GARCH-M, Component GARCH, HAR-RV -- 9 modelos de volatilidade condicional

- :material-chart-bell-curve-cumulative: **[Distribuicoes](distributions/index.md)**

    ---

    Normal, Student-t, Skewed-t, GED, Skewed GED -- distribuicoes condicionais para caudas pesadas e assimetria

- :material-chart-scatter-plot: **[Multivariado](multivariate/index.md)**

    ---

    DCC, BEKK, CCC, GO-GARCH, DECO -- modelagem conjunta de volatilidade e correlacao condicional

- :material-swap-horizontal: **[Regime-Switching](regime-switching/index.md)**

    ---

    MS-AR, MS-VAR, MS-GARCH, Hamilton Filter -- modelos com mudanca de regime Markoviano

- :material-toggle-switch: **[Threshold/STAR](threshold/index.md)**

    ---

    TAR, SETAR, LSTAR, ESTAR -- modelos de transicao suave e abrupta com testes de linearidade

- :material-shield-alert: **[Gestao de Risco](risk/index.md)**

    ---

    VaR, Expected Shortfall, EWMA, Backtesting -- ferramentas de mensuacao e validacao de risco

</div>

## Learning Path

O caminho recomendado para aprender ArchBox depende do seu objetivo:

| Objetivo | Caminho Sugerido | Nivel |
|----------|-----------------|-------|
| Modelar volatilidade de um ativo | GARCH Univariado :material-arrow-right: Distribuicoes :material-arrow-right: Gestao de Risco | Iniciante |
| Portfolio e correlacao dinamica | GARCH Univariado :material-arrow-right: Multivariado :material-arrow-right: Gestao de Risco | Intermediario |
| Detectar mudancas estruturais | Regime-Switching :material-arrow-right: Threshold/STAR | Intermediario |
| Workflow completo de risco | GARCH :material-arrow-right: Distribuicoes :material-arrow-right: Multivariado :material-arrow-right: Risco | Avancado |

!!! tip "Recomendacao"
    Comece pelo [GARCH(p,q)](garch/garch.md) -- e o modelo fundamental que serve de base para todas as extensoes. Depois explore as [distribuicoes condicionais](distributions/index.md) para capturar caudas pesadas, e em seguida avance para os modelos mais especializados.

## Quick Example

```python
from archbox import GARCH
from archbox.datasets import load_dataset

# Carregar retornos do S&P 500
sp500 = load_dataset('sp500')

# Estimar GARCH(1,1) com distribuicao normal
model = GARCH(sp500['returns'], p=1, q=1)
results = model.fit()
print(results.summary())
```

## See Also

- [Getting Started](../getting-started/index.md) -- Instalacao e primeiros passos
- [Tutorials](../tutorials/index.md) -- Notebooks interativos com exemplos completos
- [Diagnostics](../diagnostics/index.md) -- Testes de especificacao e avaliacao de modelos
- [API Reference](../api/index.md) -- Referencia tecnica completa
