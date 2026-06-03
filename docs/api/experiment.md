---
title: Experiment API
description: ArchExperiment - workflow de alto nivel para ajuste, comparacao e validacao de modelos
---

# Experiment API

!!! info "Modulo"
    ```python
    from archbox.experiment import (
        ArchExperiment,
        ComparisonResult,
        ValidationResult,
        RiskAnalysisResult,
    )
    ```

## Visao Geral

O modulo `archbox.experiment` fornece uma API de alto nivel para o workflow
completo de modelagem de volatilidade:

```
Dados → Ajustar Modelos → Comparar → Validar → Analise de Risco → Relatorio
```

| Classe | Descricao |
|--------|-----------|
| `ArchExperiment` | Orquestrador principal do workflow |
| `ComparisonResult` | Resultado da comparacao entre modelos |
| `ValidationResult` | Resultado da validacao out-of-sample |
| `RiskAnalysisResult` | Resultado da analise de risco |

---

## ArchExperiment

::: archbox.experiment.experiment.ArchExperiment
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - fit_all_models
        - compare_models
        - validate_model
        - risk_analysis
        - save_master_report

### Construtor

```python
ArchExperiment(returns, mean="constant")
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `returns` | `array-like` | -- | Serie temporal de retornos |
| `mean` | `str` | `"constant"` | Especificacao da media: `"constant"` ou `"zero"` |

### Metodos

#### `fit_all_models()`

Ajusta multiplos modelos de volatilidade em sequencia.

```python
fit_all_models(model_specs, disp=False) -> dict[str, ArchResults]
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `model_specs` | `list[tuple[str, dict]]` | -- | Lista de `(tipo_modelo, kwargs)` |
| `disp` | `bool` | `False` | Exibir progresso da otimizacao |

**Modelos disponiveis:**

| Tipo | Classe | Parametros Tipicos |
|------|--------|-------------------|
| `"GARCH"` | `GARCH` | `p`, `q` |
| `"EGARCH"` | `EGARCH` | `p`, `q` |
| `"GJR"` | `GJR_GARCH` | `p`, `q` |
| `"APARCH"` | `APARCH` | `p`, `q` |
| `"FIGARCH"` | `FIGARCH` | `p`, `d`, `q` |
| `"IGARCH"` | `IGARCH` | `p`, `q` |
| `"Component"` | `ComponentGARCH` | -- |

**Retorna**: `dict[str, ArchResults]` -- dicionario mapeando nomes automaticos
(ex: `"GARCH(1,1)"`) para resultados.

#### `compare_models()`

Compara todos os modelos ajustados por criterios de informacao.

```python
compare_models(criteria=None) -> ComparisonResult
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `criteria` | `list[str] \| None` | `None` | Criterios (default: `["aic", "bic", "loglike", "persistence"]`) |

!!! note "Pre-requisito"
    Requer que `fit_all_models()` tenha sido executado previamente.

#### `validate_model()`

Validacao out-of-sample de um modelo especifico.

```python
validate_model(model_name=None, test_size=500, horizon=1) -> ValidationResult
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `model_name` | `str \| None` | `None` | Nome do modelo (`None` = melhor por AIC) |
| `test_size` | `int` | `500` | Tamanho da amostra de teste |
| `horizon` | `int` | `1` | Horizonte de previsao |

#### `risk_analysis()`

Analise de risco completa com backtesting.

```python
risk_analysis(model=None, alpha=0.05, methods=None) -> RiskAnalysisResult
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `model` | `str \| None` | `None` | Nome do modelo (`None` = melhor por AIC) |
| `alpha` | `float` | `0.05` | Nivel de significancia (VaR 95%) |
| `methods` | `list[str] \| None` | `None` | Metodos de VaR (default: todos disponiveis) |

#### `save_master_report()`

Gera relatorio HTML consolidado com todos os resultados.

```python
save_master_report(path, theme="professional") -> None
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `path` | `str` | -- | Caminho do arquivo HTML de saida |
| `theme` | `str` | `"professional"` | Tema visual |

### Exemplo Completo

```python
from archbox.experiment import ArchExperiment
import numpy as np

np.random.seed(42)
returns = np.random.randn(1000) * 0.01

# 1. Criar experimento
exp = ArchExperiment(returns, mean="constant")

# 2. Ajustar multiplos modelos
exp.fit_all_models([
    ("GARCH", {"p": 1, "q": 1}),
    ("GARCH", {"p": 2, "q": 1}),
    ("EGARCH", {"p": 1, "q": 1}),
    ("GJR", {"p": 1, "q": 1}),
], disp=False)

# 3. Comparar modelos
comparison = exp.compare_models()
print(comparison.ranking("aic"))
print(f"Melhor modelo: {comparison.best_model('aic')}")

# 4. Validar melhor modelo
validation = exp.validate_model(test_size=200)
print(f"RMSE: {validation.rmse_vol():.6f}")
print(f"MAE: {validation.mae_vol():.6f}")

# 5. Analise de risco
risk = exp.risk_analysis(alpha=0.05)
print(risk.backtest_summary())

# 6. Relatorio consolidado
exp.save_master_report("analise_completa.html")
```

---

## ComparisonResult

::: archbox.experiment.comparison.ComparisonResult
    options:
      show_root_heading: true
      show_source: true
      members:
        - ranking
        - best_model
        - to_dataframe
        - plot_comparison

### Atributos

| Atributo | Tipo | Descricao |
|----------|------|-----------|
| `model_names` | `list[str]` | Nomes dos modelos comparados |
| `criteria` | `dict[str, list[float]]` | Valores de cada criterio por modelo |
| `results` | `list[ArchResults]` | Resultados dos modelos |

### Metodos

#### `ranking()`

Ordena modelos por um criterio especifico.

```python
ranking(criterion="aic") -> pd.DataFrame
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `criterion` | `str` | `"aic"` | Criterio: `"aic"`, `"bic"`, `"loglike"`, `"persistence"` |

**Retorna**: DataFrame com modelos ordenados (menor AIC/BIC = melhor).

#### `best_model()`

Retorna o nome do melhor modelo pelo criterio.

```python
best_model(criterion="aic") -> str
```

#### `to_dataframe()`

Exporta comparacao completa como DataFrame.

```python
to_dataframe() -> pd.DataFrame
```

#### `plot_comparison()`

Grafico de barras comparando modelos por criterio.

```python
plot_comparison(criterion="aic", ax=None) -> plt.Axes
```

### Exemplo

```python
from archbox.experiment import ArchExperiment
import numpy as np

np.random.seed(42)
returns = np.random.randn(1000) * 0.01

exp = ArchExperiment(returns)
exp.fit_all_models([
    ("GARCH", {"p": 1, "q": 1}),
    ("EGARCH", {"p": 1, "q": 1}),
    ("GJR", {"p": 1, "q": 1}),
], disp=False)

comp = exp.compare_models()

# Ranking por AIC
print(comp.ranking("aic"))

# Ranking por BIC
print(comp.ranking("bic"))

# DataFrame completo
df = comp.to_dataframe()
print(df)

# Grafico
ax = comp.plot_comparison("bic")
```

---

## ValidationResult

::: archbox.experiment.validation.ValidationResult
    options:
      show_root_heading: true
      show_source: true
      members:
        - rmse_vol
        - mae_vol
        - var_violation_rate
        - plot_forecast_vs_actual

### Atributos

| Atributo | Tipo | Descricao |
|----------|------|-----------|
| `model_name` | `str` | Nome do modelo validado |
| `in_sample_size` | `int` | Tamanho da amostra in-sample |
| `out_sample_size` | `int` | Tamanho da amostra out-of-sample |
| `forecast_volatility` | `ndarray` | Volatilidade prevista |
| `actual_returns` | `ndarray` | Retornos realizados |
| `actual_squared_returns` | `ndarray` | Retornos quadrados (proxy de variancia) |
| `var_series` | `ndarray \| None` | Serie de VaR (se calculada) |
| `alpha` | `float` | Nivel de significancia |

### Metodos

#### `rmse_vol()`

Root Mean Squared Error entre variancia prevista e retornos quadrados:

$$
\text{RMSE} = \sqrt{\frac{1}{T} \sum_{t=1}^{T} (\hat{\sigma}_t^2 - r_t^2)^2}
$$

```python
rmse_vol() -> float
```

#### `mae_vol()`

Mean Absolute Error:

$$
\text{MAE} = \frac{1}{T} \sum_{t=1}^{T} |\hat{\sigma}_t^2 - r_t^2|
$$

```python
mae_vol() -> float
```

#### `var_violation_rate()`

Taxa de violacoes do VaR (fracao de retornos abaixo do VaR).

```python
var_violation_rate() -> float
```

#### `plot_forecast_vs_actual()`

Grafico da volatilidade prevista vs retornos quadrados realizados.

```python
plot_forecast_vs_actual(ax=None) -> plt.Axes
```

---

## RiskAnalysisResult

::: archbox.experiment.risk_analysis.RiskAnalysisResult
    options:
      show_root_heading: true
      show_source: true
      members:
        - backtest_summary
        - plot_risk

### Atributos

| Atributo | Tipo | Descricao |
|----------|------|-----------|
| `model_name` | `str` | Nome do modelo |
| `alpha` | `float` | Nivel de significancia |
| `var_series` | `dict[str, ndarray]` | Series de VaR por metodo |
| `es_series` | `dict[str, ndarray]` | Series de ES por metodo |
| `backtest_results` | `dict[str, Any]` | Resultados de backtesting |

### Metodos

#### `backtest_summary()`

Resumo formatado dos resultados de backtesting.

```python
backtest_summary() -> str
```

#### `plot_risk()`

Visualizacao de VaR e retornos.

```python
plot_risk(method="parametric", returns=None, ax=None) -> plt.Axes
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `method` | `str` | `"parametric"` | Metodo de VaR |
| `returns` | `ndarray \| None` | `None` | Retornos para sobreposicao |
| `ax` | `plt.Axes \| None` | `None` | Axes existentes |

---

## Workflow Tipico

```python
from archbox.experiment import ArchExperiment
from archbox.datasets import load_dataset
import numpy as np

# Carregar dados
data = load_dataset("sp500")
returns = data["returns"].values

# Criar experimento
exp = ArchExperiment(returns, mean="constant")

# Ajustar familia de modelos
exp.fit_all_models([
    ("GARCH", {"p": 1, "q": 1}),
    ("GARCH", {"p": 1, "q": 2}),
    ("GARCH", {"p": 2, "q": 1}),
    ("EGARCH", {"p": 1, "q": 1}),
    ("GJR", {"p": 1, "q": 1}),
], disp=False)

# Comparar e selecionar melhor modelo
comp = exp.compare_models(criteria=["aic", "bic", "loglike", "persistence"])
print("=== Ranking AIC ===")
print(comp.ranking("aic"))
print(f"\nMelhor modelo (AIC): {comp.best_model('aic')}")
print(f"Melhor modelo (BIC): {comp.best_model('bic')}")

# Validar out-of-sample
val = exp.validate_model(test_size=250, horizon=1)
print(f"\n=== Validacao {val.model_name} ===")
print(f"RMSE vol: {val.rmse_vol():.6e}")
print(f"MAE vol: {val.mae_vol():.6e}")

# Analise de risco
risk = exp.risk_analysis(alpha=0.05)
print(f"\n=== Risco ===")
print(risk.backtest_summary())

# Relatorio final
exp.save_master_report("analise_sp500.html", theme="professional")
```

---

## Ver Tambem

- [Core](core.md) -- `ArchResults` retornado pelos modelos
- [GARCH](garch.md) -- Modelos univariados de volatilidade
- [Risk](risk.md) -- VaR, ES e backtesting
- [Reports](reports.md) -- `ReportManager` para relatorios customizados
- [Datasets](datasets.md) -- Datasets para experimentacao
