---
title: Reports API
description: Geracao automatizada de relatorios em HTML, LaTeX e Markdown
---

# Reports API

!!! info "Modulo"
    ```python
    from archbox.report import ReportManager
    ```

## Visao Geral

O modulo `archbox.report` fornece um sistema completo de geracao de
relatorios para modelos de volatilidade condicional. O pipeline segue
tres etapas:

```
Resultados → Transformer → Template (Jinja2) → Exporter → Arquivo
```

| Componente | Classe | Descricao |
|------------|--------|-----------|
| **Orquestrador** | `ReportManager` | Coordena todo o pipeline |
| **Transformers** | `GARCHTransformer`, `MultivariateTransformer`, `RegimeTransformer`, `RiskTransformer` | Extraem dados dos resultados |
| **Templates** | Jinja2 | Templates HTML, LaTeX e Markdown |
| **Exporters** | `HTMLExporter`, `LaTeXExporter`, `MarkdownExporter` | Formatam e salvam o output |
| **CSS** | `CSSManager` | Estilos visuais para HTML |
| **Templates** | `TemplateManager` | Gerencia templates Jinja2 |

### Tipos de Relatorio

| Tipo | Descricao | Conteudo |
|------|-----------|----------|
| `"garch"` | Modelo GARCH univariado | Parametros, persistencia, meia-vida, diagnosticos, residuos |
| `"multivariate"` | Modelo multivariado | Parametros por serie, correlacao DCC, resumo |
| `"regime"` | Regime-switching | Matriz de transicao, duracoes, parametros por regime |
| `"risk"` | Analise de risco | VaR, ES, backtesting, semaforo, comparacao de metodos |

### Formatos de Saida

| Formato | Extensao | Caracteristicas |
|---------|----------|----------------|
| `"html"` | `.html` | Interativo, sidebar navegavel, secoes colapsaveis |
| `"latex"` | `.tex` | Tabelas booktabs, pronto para compilacao |
| `"markdown"` | `.md` | Compativel com GitHub/GitLab |

---

## ReportManager

::: archbox.report.report_manager.ReportManager
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - generate
        - list_report_types
        - list_formats

### Construtor

```python
ReportManager(template_dir=None)
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `template_dir` | `str \| Path \| None` | `None` | Diretorio de templates customizados (usa built-in se `None`) |

### Metodos

#### `generate()`

Gera relatorio completo a partir de resultados de um modelo.

```python
generate(
    results,
    report_type="garch",
    fmt="html",
    theme="professional",
    output_path=None,
    title=None
) -> str
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `results` | `ArchResults` | -- | Resultado de modelo ajustado |
| `report_type` | `str` | `"garch"` | Tipo: `"garch"`, `"multivariate"`, `"regime"`, `"risk"` |
| `fmt` | `str` | `"html"` | Formato: `"html"`, `"latex"`, `"markdown"` |
| `theme` | `str` | `"professional"` | Tema visual (apenas HTML) |
| `output_path` | `str \| Path \| None` | `None` | Caminho de saida (`None` = retorna string) |
| `title` | `str \| None` | `None` | Titulo customizado |

**Retorna**: `str` -- conteudo do relatorio (ou caminho se `output_path` fornecido).

#### `list_report_types()`

Retorna tipos de relatorio disponiveis.

```python
list_report_types() -> list[str]
# ['garch', 'multivariate', 'regime', 'risk']
```

#### `list_formats()`

Retorna formatos de saida disponiveis.

```python
list_formats() -> list[str]
# ['html', 'latex', 'markdown']
```

### Exemplo Basico

```python
from archbox.models import GARCH
from archbox.report import ReportManager
import numpy as np

np.random.seed(42)
returns = np.random.randn(1000) * 0.01

# Ajustar modelo
model = GARCH(returns, p=1, q=1)
result = model.fit(disp=False)

# Gerar relatorio HTML
manager = ReportManager()
html = manager.generate(result, report_type="garch", fmt="html")

# Salvar em arquivo
manager.generate(
    result,
    report_type="garch",
    fmt="html",
    output_path="relatorio_garch.html",
    title="Analise GARCH(1,1) - S&P 500"
)
```

---

## Transformers

Os transformers extraem dados dos resultados e preparam o contexto para
os templates Jinja2.

### GARCHTransformer

::: archbox.report.transformers.garch.GARCHTransformer
    options:
      show_root_heading: true
      show_source: true
      members:
        - transform

Extrai dados de modelos GARCH univariados.

```python
GARCHTransformer().transform(results) -> dict[str, Any]
```

**Chaves retornadas:**

| Chave | Tipo | Descricao |
|-------|------|-----------|
| `model_name` | `str` | Nome do modelo |
| `n_obs` | `int` | Numero de observacoes |
| `generated_at` | `str` | Data/hora de geracao |
| `params_table` | `list[dict]` | Parametros com `name`, `value`, `std_error`, `t_stat`, `p_value`, `significance` |
| `persistence` | `float` | Persistencia $\alpha + \beta$ |
| `unconditional_variance` | `float` | $\bar{\sigma}^2$ |
| `half_life` | `float \| None` | Meia-vida em periodos |
| `aic` | `float` | Criterio de informacao de Akaike |
| `bic` | `float` | Criterio de informacao Bayesiano |
| `loglikelihood` | `float` | Log-verossimilhanca |
| `diagnostics` | `dict` | ARCH-LM, Ljung-Box, Sign Bias |
| `volatility_stats` | `dict` | Estatisticas da volatilidade |
| `residual_stats` | `dict` | Estatisticas dos residuos |

---

### MultivariateTransformer

::: archbox.report.transformers.multivariate.MultivariateTransformer
    options:
      show_root_heading: true
      show_source: true
      members:
        - transform

Extrai dados de modelos multivariados (DCC, CCC).

```python
MultivariateTransformer().transform(results) -> dict[str, Any]
```

**Chaves adicionais ao GARCH:**

| Chave | Tipo | Descricao |
|-------|------|-----------|
| `n_series` | `int` | Numero de series |
| `series_names` | `list[str]` | Nomes das series |
| `series_params` | `list[dict]` | Parametros por serie |
| `correlation_params` | `dict` | `dcc_a`, `dcc_b`, `dcc_persistence` |
| `correlation_summary` | `dict` | Estatisticas da correlacao |

---

### RegimeTransformer

::: archbox.report.transformers.regime.RegimeTransformer
    options:
      show_root_heading: true
      show_source: true
      members:
        - transform

Extrai dados de modelos regime-switching.

```python
RegimeTransformer().transform(results) -> dict[str, Any]
```

**Chaves especificas:**

| Chave | Tipo | Descricao |
|-------|------|-----------|
| `n_regimes` | `int` | Numero de regimes |
| `transition_matrix` | `list[list[float]]` | Matriz de transicao |
| `expected_durations` | `list[dict]` | `regime` e `duration` por regime |
| `regime_params` | `dict` | Parametros por regime |
| `regime_classification` | `dict` | Contagens e proporcoes |

---

### RiskTransformer

::: archbox.report.transformers.risk.RiskTransformer
    options:
      show_root_heading: true
      show_source: true
      members:
        - transform

Extrai dados de analise de risco.

```python
RiskTransformer().transform(results) -> dict[str, Any]
```

**Chaves especificas:**

| Chave | Tipo | Descricao |
|-------|------|-----------|
| `confidence_level` | `float` | Nivel de confianca |
| `var_stats` | `dict` | Media, desvio, min, max do VaR |
| `es_stats` | `dict` | Estatisticas do ES |
| `backtest` | `dict` | Violacoes, Kupiec, Christoffersen |
| `traffic_light` | `dict` | `zone`, `status`, `n_violations` |
| `method_comparison` | `dict` | Comparacao entre metodos |

---

## Exporters

### HTMLExporter

::: archbox.report.exporters.html.HTMLExporter
    options:
      show_root_heading: true
      show_source: true
      members:
        - export

Exporta relatorios HTML com CSS tematico, sidebar navegavel e secoes
colapsaveis (JavaScript integrado).

```python
HTMLExporter().export(
    rendered_content,
    output_path=None,
    include_plotly=True
) -> str
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `rendered_content` | `str` | -- | HTML renderizado pelo template |
| `output_path` | `str \| Path \| None` | `None` | Caminho de saida |
| `include_plotly` | `bool` | `True` | Incluir Plotly.js para graficos interativos |

---

### LaTeXExporter

::: archbox.report.exporters.latex.LaTeXExporter
    options:
      show_root_heading: true
      show_source: true
      members:
        - export
        - format_table
        - format_figure

Exporta relatorios LaTeX com tabelas booktabs.

```python
LaTeXExporter().export(rendered_content, output_path=None) -> str
```

#### `format_table()`

Gera tabela LaTeX com pacote booktabs.

```python
format_table(headers, rows, caption="", label="") -> str
```

#### `format_figure()`

Gera bloco de figura LaTeX.

```python
format_figure(image_path, caption="", label="", width="0.9\\textwidth") -> str
```

---

### MarkdownExporter

::: archbox.report.exporters.markdown.MarkdownExporter
    options:
      show_root_heading: true
      show_source: true
      members:
        - export
        - format_table
        - format_image

Exporta relatorios em Markdown (GitHub-flavored).

```python
MarkdownExporter().export(rendered_content, output_path=None) -> str
```

---

## CSSManager

::: archbox.report.css_manager.CSSManager
    options:
      show_root_heading: true
      show_source: true
      members:
        - get_css

Gerencia estilos CSS em 3 camadas:

1. **Base** -- Reset, layout, tipografia
2. **Componente** -- Tabelas, cards, navegacao
3. **Tema** -- Cores e estilos especificos do tema

```python
CSSManager().get_css(theme="professional") -> str
```

---

## TemplateManager

::: archbox.report.template_manager.TemplateManager
    options:
      show_root_heading: true
      show_source: true
      members:
        - render
        - list_templates

Gerencia templates Jinja2 com filtros customizados.

```python
manager = TemplateManager(template_dir=None)
rendered = manager.render("garch_html.html", context)
```

### Filtros Jinja2 Disponiveis

| Filtro | Descricao | Exemplo |
|--------|-----------|---------|
| `fmt_number` | Formata numero com casas decimais | `{{ 0.1234 \| fmt_number(4) }}` → `0.1234` |
| `fmt_pvalue` | Formata p-valor com notacao cientifica | `{{ 0.001 \| fmt_pvalue }}` → `0.001` |
| `fmt_percent` | Formata como porcentagem | `{{ 0.05 \| fmt_percent }}` → `5.00%` |
| `significance_stars` | Estrelas de significancia | `{{ 0.001 \| significance_stars }}` → `***` |

---

## Exemplo Completo: Multiplos Formatos

```python
from archbox.models import GARCH
from archbox.report import ReportManager
import numpy as np

np.random.seed(42)
returns = np.random.randn(1000) * 0.01

model = GARCH(returns, p=1, q=1)
result = model.fit(disp=False)

manager = ReportManager()

# HTML com tema profissional
manager.generate(
    result,
    report_type="garch",
    fmt="html",
    theme="professional",
    output_path="report.html",
    title="GARCH(1,1) Analysis"
)

# LaTeX para publicacao
manager.generate(
    result,
    report_type="garch",
    fmt="latex",
    output_path="report.tex"
)

# Markdown para repositorio
manager.generate(
    result,
    report_type="garch",
    fmt="markdown",
    output_path="report.md"
)

# Listar opcoes
print(f"Tipos: {manager.list_report_types()}")
print(f"Formatos: {manager.list_formats()}")
```

---

## Templates Customizados

Para usar templates customizados, passe o diretorio ao construtor:

```python
from archbox.report import ReportManager

# Templates customizados
manager = ReportManager(template_dir="meus_templates/")

# O diretorio deve conter templates Jinja2 nomeados como:
# garch_html.html, garch_latex.tex, garch_markdown.md
# multivariate_html.html, etc.
```

!!! tip "Estrutura do Template"
    Os templates recebem um dicionario `context` com todas as chaves
    retornadas pelo transformer correspondente. Consulte a documentacao
    de cada transformer para as chaves disponiveis.

---

## Ver Tambem

- [Core](core.md) -- `ArchResults` usado como input
- [Experiment](experiment.md) -- `ArchExperiment.save_master_report()` para relatorios consolidados
- [Visualization](visualization.md) -- Graficos que podem ser integrados aos relatorios
