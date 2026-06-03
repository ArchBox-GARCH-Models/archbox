---
title: API Reference
description: Referencia completa da API publica da archbox
---

# API Reference

!!! info "Modulo principal"
    ```python
    import archbox
    ```
    A archbox expoe todos os modelos via submodulos dedicados.

## Visao Geral

A API da archbox esta organizada em modulos tematicos. Cada modulo contem
classes de modelo, containers de resultado e funcoes auxiliares.

| Modulo | Import | Descricao |
|--------|--------|-----------|
| **Core** | `archbox.core` | Classes base `VolatilityModel`, `ArchResults`, excepcoes |
| **GARCH** | `archbox.models` | 8 modelos univariados: GARCH, EGARCH, GJR, APARCH, FIGARCH, IGARCH, GARCH-M, Component |
| **HAR** | `archbox.models` | HAR-RV e variantes para volatilidade realizada |
| **Multivariado** | `archbox.multivariate` | DCC, BEKK, CCC, GO-GARCH, DECO |
| **Regime-Switching** | `archbox.regime` | MS-AR, MS-VAR, MS-GARCH |
| **Threshold** | `archbox.threshold` | TAR, SETAR, LSTAR, ESTAR |
| **Distribuicoes** | `archbox.distributions` | Normal, Student-t, Skewed-t, GED |
| **Risco** | `archbox.risk` | VaR, Expected Shortfall, EWMA, Backtesting |
| **Diagnosticos** | `archbox.diagnostics` | Ljung-Box, ARCH-LM, Sign Bias, News Impact |
| **Visualizacao** | `archbox.visualization` | Plots de volatilidade, correlacao, regimes |
| **Reports** | `archbox.report` | Geracao automatica de relatorios |
| **Experiment** | `archbox.experiment` | Framework de comparacao de modelos |
| **Datasets** | `archbox.datasets` | Dados de exemplo para testes e tutoriais |
| **CLI** | `archbox.cli` | Interface de linha de comando |

---

## Convencoes da API

### Nomenclatura

- **Classes de modelo** seguem o padrao `NomeDoModelo` em PascalCase (ex: `GARCH`, `EGARCH`, `GJRGARCH`)
- **Classes de resultado** usam o sufixo `Results` (ex: `ArchResults`, `MultivarResults`, `HARRVResults`)
- **Metodos publicos** usam snake_case (ex: `fit()`, `forecast()`, `summary()`)

### Parametros Comuns

Todos os modelos univariados aceitam:

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `endog` | `array-like` | -- | Serie temporal de retornos |
| `p` | `int` | `1` | Ordem GARCH (termos de variancia defasada) |
| `q` | `int` | `1` | Ordem ARCH (termos de residuos quadrados defasados) |
| `mean` | `str` | `'constant'` | Modelo da media: `'constant'` ou `'zero'` |
| `dist` | `str` | `'normal'` | Distribuicao condicional |

### Retornos Padrao

| Metodo | Retorno | Descricao |
|--------|---------|-----------|
| `fit()` | `ArchResults` | Container com parametros, volatilidade, diagnosticos |
| `forecast(horizon)` | `dict` | Dicionario com `'variance'` e `'volatility'` |
| `simulate(n, params)` | `tuple[ndarray, ndarray]` | `(retornos, volatilidade_condicional)` |
| `summary()` | `str` | Tabela formatada com estatisticas |
| `loglike(params)` | `float` | Log-verossimilhanca total |

### Atributos de Resultado

Todos os objetos `ArchResults` contem:

| Atributo | Tipo | Descricao |
|----------|------|-----------|
| `params` | `ndarray` | Parametros estimados |
| `param_names` | `list[str]` | Nomes dos parametros |
| `loglike` | `float` | Log-verossimilhanca no otimo |
| `aic` | `float` | Criterio de Informacao de Akaike |
| `bic` | `float` | Criterio de Informacao Bayesiano |
| `conditional_volatility` | `ndarray` | Serie $\sigma_t$ |
| `resid` | `ndarray` | Residuos padronizados $z_t = \varepsilon_t / \sigma_t$ |
| `se` | `ndarray` | Erros-padrao (robustos por default) |
| `tvalues` | `ndarray` | Estatisticas t |
| `pvalues` | `ndarray` | p-valores |

---

## Como Navegar a Referencia

=== "Por tipo de modelo"

    - Modelos **univariados** de volatilidade: [GARCH](garch.md)
    - Volatilidade **realizada**: [HAR](har.md)
    - Modelos **multivariados**: [Multivariado](multivariate.md)

=== "Por funcionalidade"

    - Classes base e interfaces: [Core](core.md)
    - Distribuicoes condicionais: [Distribuicoes](distributions.md)
    - Gestao de risco: [Risco](risk.md)

=== "Por nivel de experiencia"

    - **Iniciante**: Comece com [Core](core.md) para entender a interface base, depois [GARCH](garch.md) para o modelo padrao
    - **Intermediario**: Explore [HAR](har.md) e [Multivariado](multivariate.md)
    - **Avancado**: Consulte [Regime-Switching](regime-switching.md) e [Threshold](threshold.md)

---

## Exemplo Rapido

```python
from archbox.models import GARCH

# Ajustar GARCH(1,1)
model = GARCH(returns, p=1, q=1)
result = model.fit()

# Resumo dos resultados
print(result.summary())

# Previsao 10 passos a frente
forecasts = result.forecast(horizon=10)
print(forecasts['volatility'])
```
