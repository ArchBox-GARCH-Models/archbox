---
title: Visualization API
description: Funcoes de visualizacao para volatilidade, correlacao, risco, regimes e diagnosticos
---

# Visualization API

!!! info "Modulo"
    ```python
    from archbox.visualization import (
        # Volatilidade
        plot_volatility, plot_variance_persistence,
        # News Impact
        plot_news_impact, plot_news_impact_comparison,
        # Diagnosticos
        plot_diagnostics, plot_distribution_fit,
        # Regimes
        plot_regimes, plot_transition_matrix,
        # Transicao
        plot_transition_function, plot_phase_diagram,
        # Correlacao
        plot_dynamic_correlation, plot_correlation_heatmap,
        plot_covariance_decomposition,
        # Risco
        plot_var_backtest, plot_traffic_light, plot_var_comparison,
    )
    ```

## Visao Geral

O modulo `archbox.visualization` fornece funcoes de alta qualidade para
visualizacao de resultados de modelos de volatilidade condicional:

| Categoria | Funcoes | Descricao |
|-----------|---------|-----------|
| **Volatilidade** | `plot_volatility`, `plot_variance_persistence` | Volatilidade condicional e persistencia |
| **News Impact** | `plot_news_impact`, `plot_news_impact_comparison` | Curva de impacto de noticias |
| **Diagnosticos** | `plot_diagnostics`, `plot_distribution_fit` | Paineis de diagnostico e ajuste |
| **Regimes** | `plot_regimes`, `plot_transition_matrix` | Regime-switching e transicoes |
| **Transicao** | `plot_transition_function`, `plot_phase_diagram` | LSTAR/ESTAR e diagramas de fase |
| **Correlacao** | `plot_dynamic_correlation`, `plot_correlation_heatmap`, `plot_covariance_decomposition` | Correlacao dinamica e covariancia |
| **Risco** | `plot_var_backtest`, `plot_traffic_light`, `plot_var_comparison` | VaR, semaforo e comparacao |

Todas as funcoes retornam objetos `matplotlib.figure.Figure` e aceitam
o parametro `theme` para controle visual.

---

## Plots de Volatilidade

### plot_volatility()

::: archbox.visualization.volatility_plot.plot_volatility
    options:
      show_root_heading: true
      show_source: true

Cria painel de 3 graficos: retornos, volatilidade condicional com bandas
de confianca e residuos padronizados.

```python
plot_volatility(
    results,
    annualize=False,
    ci=0.95,
    theme="professional",
    figsize=None,
    title=None
) -> Figure
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `results` | `ArchResults` | -- | Resultado de modelo ajustado |
| `annualize` | `bool` | `False` | Anualizar volatilidade ($\times \sqrt{252}$) |
| `ci` | `float` | `0.95` | Nivel de confianca das bandas |
| `theme` | `str \| Theme` | `"professional"` | Tema visual |
| `figsize` | `tuple \| None` | `None` | Tamanho da figura `(largura, altura)` |
| `title` | `str \| None` | `None` | Titulo customizado |

### Exemplo

```python
from archbox.models import GARCH
from archbox.visualization import plot_volatility
import numpy as np

np.random.seed(42)
returns = np.random.randn(1000) * 0.01

model = GARCH(returns, p=1, q=1)
result = model.fit(disp=False)

fig = plot_volatility(result, annualize=True, ci=0.95)
fig.savefig("volatilidade.png", dpi=150, bbox_inches="tight")
```

---

### plot_variance_persistence()

::: archbox.visualization.volatility_plot.plot_variance_persistence
    options:
      show_root_heading: true
      show_source: true

Plota a funcao de autocorrelacao (ACF) dos retornos ao quadrado com
sobreposicao do decaimento GARCH teorico e anotacao de meia-vida.

```python
plot_variance_persistence(
    results,
    max_lags=50,
    theme="professional",
    figsize=None
) -> Figure
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `results` | `ArchResults` | -- | Resultado de modelo ajustado |
| `max_lags` | `int` | `50` | Numero maximo de lags na ACF |
| `theme` | `str \| Theme` | `"professional"` | Tema visual |
| `figsize` | `tuple \| None` | `None` | Tamanho da figura |

---

## Plots de News Impact

### plot_news_impact()

::: archbox.visualization.news_impact_plot.plot_news_impact
    options:
      show_root_heading: true
      show_source: true

Plota a curva de impacto de noticias (News Impact Curve), que mostra
como choques $\varepsilon_{t-1}$ afetam a variancia condicional $\sigma_t^2$.

Para GARCH(1,1): $\sigma_t^2 = \omega + \alpha \varepsilon_{t-1}^2 + \beta \sigma^2$
(parabola simetrica).

Para EGARCH/GJR: curva assimetrica refletindo o efeito leverage.

```python
plot_news_impact(
    results,
    n_points=200,
    n_sigma=3.0,
    theme="professional",
    figsize=None,
    title=None
) -> Figure
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `results` | `ArchResults` | -- | Resultado de modelo ajustado |
| `n_points` | `int` | `200` | Pontos na curva |
| `n_sigma` | `float` | `3.0` | Amplitude em desvios-padrao |
| `theme` | `str \| Theme` | `"professional"` | Tema visual |
| `figsize` | `tuple \| None` | `None` | Tamanho da figura |
| `title` | `str \| None` | `None` | Titulo customizado |

---

### plot_news_impact_comparison()

::: archbox.visualization.news_impact_plot.plot_news_impact_comparison
    options:
      show_root_heading: true
      show_source: true

Compara curvas de impacto de noticias de multiplos modelos no mesmo grafico.

```python
plot_news_impact_comparison(
    results_list,
    labels=None,
    n_points=200,
    n_sigma=3.0,
    theme="professional",
    figsize=None,
    title=None
) -> Figure
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `results_list` | `list[ArchResults]` | -- | Lista de resultados de modelos |
| `labels` | `list[str] \| None` | `None` | Nomes dos modelos na legenda |
| `n_points` | `int` | `200` | Pontos em cada curva |
| `n_sigma` | `float` | `3.0` | Amplitude em desvios-padrao |
| `theme` | `str \| Theme` | `"professional"` | Tema visual |
| `figsize` | `tuple \| None` | `None` | Tamanho da figura |
| `title` | `str \| None` | `None` | Titulo customizado |

### Exemplo

```python
from archbox.models import GARCH, EGARCH, GJR_GARCH
from archbox.visualization import plot_news_impact_comparison
import numpy as np

np.random.seed(42)
returns = np.random.randn(1000) * 0.01

# Ajustar 3 modelos
garch_res = GARCH(returns, p=1, q=1).fit(disp=False)
egarch_res = EGARCH(returns, p=1, q=1).fit(disp=False)
gjr_res = GJR_GARCH(returns, p=1, q=1).fit(disp=False)

fig = plot_news_impact_comparison(
    [garch_res, egarch_res, gjr_res],
    labels=["GARCH", "EGARCH", "GJR-GARCH"]
)
```

---

## Plots de Diagnosticos

### plot_diagnostics()

::: archbox.visualization.diagnostics_plot.plot_diagnostics
    options:
      show_root_heading: true
      show_source: true

Painel 2x2 com diagnosticos de residuos:

1. **Residuos padronizados** ao longo do tempo
2. **ACF** de $z_t^2$ (autocorrelacao dos quadrados)
3. **QQ-Plot** contra distribuicao Normal
4. **Histograma** com sobreposicao da Normal

```python
plot_diagnostics(
    results,
    max_lags=30,
    theme="professional",
    figsize=None,
    title=None
) -> Figure
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `results` | `ArchResults` | -- | Resultado de modelo ajustado |
| `max_lags` | `int` | `30` | Lags maximos na ACF |
| `theme` | `str \| Theme` | `"professional"` | Tema visual |
| `figsize` | `tuple \| None` | `None` | Tamanho da figura |
| `title` | `str \| None` | `None` | Titulo customizado |

### Exemplo

```python
from archbox.models import GARCH
from archbox.visualization import plot_diagnostics
import numpy as np

np.random.seed(42)
returns = np.random.randn(1000) * 0.01

model = GARCH(returns, p=1, q=1)
result = model.fit(disp=False)

fig = plot_diagnostics(result, max_lags=20)
fig.savefig("diagnosticos.png", dpi=150)
```

---

### plot_distribution_fit()

::: archbox.visualization.distribution_plot.plot_distribution_fit
    options:
      show_root_heading: true
      show_source: true

Painel 2x2 avaliando o ajuste da distribuicao condicional:

1. **Histograma** com ajuste da distribuicao
2. **QQ-Plot** contra a distribuicao especificada
3. **Comparacao de caudas** (log-escala)
4. **CDF empirica vs teorica**

```python
plot_distribution_fit(
    results,
    dist_name="normal",
    theme="professional",
    figsize=None,
    title=None
) -> Figure
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `results` | `ArchResults` | -- | Resultado de modelo ajustado |
| `dist_name` | `str` | `"normal"` | Distribuicao: `"normal"`, `"studentt"`, `"skewt"` |
| `theme` | `str \| Theme` | `"professional"` | Tema visual |
| `figsize` | `tuple \| None` | `None` | Tamanho da figura |
| `title` | `str \| None` | `None` | Titulo customizado |

---

## Plots de Regimes

### plot_regimes()

::: archbox.visualization.regime_plot.plot_regimes
    options:
      show_root_heading: true
      show_source: true

Painel de 3 graficos para modelos regime-switching:

1. **Serie temporal** com sombreamento por regime
2. **Probabilidades** de cada regime ao longo do tempo
3. **Duracoes esperadas** dos regimes

```python
plot_regimes(
    results,
    which_probs="smoothed",
    threshold=0.5,
    theme="professional",
    figsize=None,
    title=None
) -> Figure
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `results` | regime result | -- | Resultado de modelo regime-switching |
| `which_probs` | `str` | `"smoothed"` | `"smoothed"` ou `"filtered"` |
| `threshold` | `float` | `0.5` | Limiar para classificacao de regime |
| `theme` | `str \| Theme` | `"professional"` | Tema visual |
| `figsize` | `tuple \| None` | `None` | Tamanho da figura |
| `title` | `str \| None` | `None` | Titulo customizado |

---

### plot_transition_matrix()

::: archbox.visualization.regime_plot.plot_transition_matrix
    options:
      show_root_heading: true
      show_source: true

Heatmap da matriz de transicao entre regimes.

```python
plot_transition_matrix(
    results,
    theme="professional",
    figsize=None,
    title=None
) -> Figure
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `results` | regime result | -- | Resultado de modelo regime-switching |
| `theme` | `str \| Theme` | `"professional"` | Tema visual |
| `figsize` | `tuple \| None` | `None` | Tamanho da figura |
| `title` | `str \| None` | `None` | Titulo customizado |

---

## Plots de Transicao (Threshold)

### plot_transition_function()

::: archbox.visualization.transition_plot.plot_transition_function
    options:
      show_root_heading: true
      show_source: true

Plota a funcao de transicao $G(s_t; \gamma, c)$ para modelos LSTAR/ESTAR:

- **LSTAR**: $G(s) = \frac{1}{1 + \exp(-\gamma(s - c))}$
- **ESTAR**: $G(s) = 1 - \exp(-\gamma(s - c)^2)$

```python
plot_transition_function(
    results,
    gamma_values=None,
    n_points=300,
    theme="professional",
    figsize=None,
    title=None
) -> Figure
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `results` | threshold result | -- | Resultado de modelo threshold |
| `gamma_values` | `list[float] \| None` | `None` | Valores de $\gamma$ para comparacao |
| `n_points` | `int` | `300` | Pontos na curva |
| `theme` | `str \| Theme` | `"professional"` | Tema visual |
| `figsize` | `tuple \| None` | `None` | Tamanho da figura |
| `title` | `str \| None` | `None` | Titulo customizado |

---

### plot_phase_diagram()

::: archbox.visualization.transition_plot.plot_phase_diagram
    options:
      show_root_heading: true
      show_source: true

Diagrama de fase: $y_t$ vs $y_{t-1}$ colorido pelo valor da funcao de
transicao (regime).

```python
plot_phase_diagram(
    results,
    theme="professional",
    figsize=None,
    title=None
) -> Figure
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `results` | threshold result | -- | Resultado de modelo threshold |
| `theme` | `str \| Theme` | `"professional"` | Tema visual |
| `figsize` | `tuple \| None` | `None` | Tamanho da figura |
| `title` | `str \| None` | `None` | Titulo customizado |

---

## Plots de Correlacao

### plot_dynamic_correlation()

::: archbox.visualization.correlation_plot.plot_dynamic_correlation
    options:
      show_root_heading: true
      show_source: true

Serie temporal da correlacao condicional dinamica (DCC) entre dois ativos,
com linha de referencia CCC (correlacao constante).

```python
plot_dynamic_correlation(
    results,
    i=0,
    j=1,
    ccc_reference=True,
    theme="professional",
    figsize=None,
    title=None
) -> Figure
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `results` | `MultivarResults` | -- | Resultado de modelo DCC |
| `i` | `int` | `0` | Indice do primeiro ativo |
| `j` | `int` | `1` | Indice do segundo ativo |
| `ccc_reference` | `bool` | `True` | Mostrar referencia CCC |
| `theme` | `str \| Theme` | `"professional"` | Tema visual |
| `figsize` | `tuple \| None` | `None` | Tamanho da figura |
| `title` | `str \| None` | `None` | Titulo customizado |

---

### plot_correlation_heatmap()

::: archbox.visualization.correlation_plot.plot_correlation_heatmap
    options:
      show_root_heading: true
      show_source: true

Heatmap da matriz de correlacao em um ponto no tempo ou media temporal.

```python
plot_correlation_heatmap(
    results,
    t=None,
    theme="professional",
    figsize=None,
    title=None
) -> Figure
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `results` | `MultivarResults` | -- | Resultado de modelo multivariado |
| `t` | `int \| None` | `None` | Indice temporal (`None` = media) |
| `theme` | `str \| Theme` | `"professional"` | Tema visual |
| `figsize` | `tuple \| None` | `None` | Tamanho da figura |
| `title` | `str \| None` | `None` | Titulo customizado |

---

### plot_covariance_decomposition()

::: archbox.visualization.correlation_plot.plot_covariance_decomposition
    options:
      show_root_heading: true
      show_source: true

Grafico de area empilhada das variancias condicionais (decomposicao da
covariancia).

```python
plot_covariance_decomposition(
    results,
    theme="professional",
    figsize=None,
    title=None
) -> Figure
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `results` | `MultivarResults` | -- | Resultado de modelo multivariado |
| `theme` | `str \| Theme` | `"professional"` | Tema visual |
| `figsize` | `tuple \| None` | `None` | Tamanho da figura |
| `title` | `str \| None` | `None` | Titulo customizado |

---

## Plots de Risco

### plot_var_backtest()

::: archbox.visualization.risk_plot.plot_var_backtest
    options:
      show_root_heading: true
      show_source: true

Visualizacao de backtesting de VaR: retornos com linha de VaR e
marcacao de violacoes.

```python
plot_var_backtest(
    backtest_results,
    theme="risk",
    figsize=None,
    title=None
) -> Figure
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `backtest_results` | `VaRBacktest` | -- | Resultado de backtesting |
| `theme` | `str \| Theme` | `"risk"` | Tema visual (default: tema de risco) |
| `figsize` | `tuple \| None` | `None` | Tamanho da figura |
| `title` | `str \| None` | `None` | Titulo customizado |

---

### plot_traffic_light()

::: archbox.visualization.risk_plot.plot_traffic_light
    options:
      show_root_heading: true
      show_source: true

Semaforo de Basileia III: contagem movel de violacoes com zonas
verde/amarela/vermelha.

```python
plot_traffic_light(
    backtest_results,
    window=250,
    theme="risk",
    figsize=None,
    title=None
) -> Figure
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `backtest_results` | `VaRBacktest` | -- | Resultado de backtesting |
| `window` | `int` | `250` | Janela movel (dias uteis) |
| `theme` | `str \| Theme` | `"risk"` | Tema visual |
| `figsize` | `tuple \| None` | `None` | Tamanho da figura |
| `title` | `str \| None` | `None` | Titulo customizado |

---

### plot_var_comparison()

::: archbox.visualization.risk_plot.plot_var_comparison
    options:
      show_root_heading: true
      show_source: true

Compara multiplos metodos de VaR sobrepostos aos retornos.

```python
plot_var_comparison(
    var_dict,
    returns,
    theme="risk",
    figsize=None,
    title=None
) -> Figure
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `var_dict` | `dict[str, ndarray]` | -- | `{"metodo": var_series, ...}` |
| `returns` | `ndarray` | -- | Serie de retornos |
| `theme` | `str \| Theme` | `"risk"` | Tema visual |
| `figsize` | `tuple \| None` | `None` | Tamanho da figura |
| `title` | `str \| None` | `None` | Titulo customizado |

### Exemplo

```python
from archbox.models import GARCH
from archbox.risk import ValueAtRisk, VaRBacktest
from archbox.visualization import plot_var_backtest, plot_var_comparison
import numpy as np

np.random.seed(42)
returns = np.random.randn(1000) * 0.01

model = GARCH(returns, p=1, q=1)
result = model.fit(disp=False)

var = ValueAtRisk(result, alpha=0.05)
var_normal = var.parametric(dist='normal')
var_t = var.parametric(dist='student-t', nu=5)
var_fhs = var.filtered_historical()

# Comparacao de metodos
fig = plot_var_comparison(
    {"Normal": var_normal, "Student-t(5)": var_t, "FHS": var_fhs},
    returns
)

# Backtesting visual
bt = VaRBacktest(returns, var_normal, alpha=0.05)
fig_bt = plot_var_backtest(bt)
```

---

## Temas

### Theme

::: archbox.visualization.themes.Theme
    options:
      show_root_heading: true
      show_source: true
      members:
        - to_matplotlib_rcparams
        - to_plotly_template

Configuracao visual para todos os graficos.

| Atributo | Tipo | Descricao |
|----------|------|-----------|
| `name` | `str` | Nome do tema |
| `colors` | `dict` | Paleta de cores |
| `font_family` | `str` | Familia de fontes |
| `font_sizes` | `dict` | Tamanhos de fonte |
| `line_widths` | `dict` | Espessuras de linha |
| `figure_size` | `tuple` | Tamanho padrao `(largura, altura)` |
| `dpi` | `int` | Resolucao (pontos por polegada) |
| `grid_alpha` | `float` | Transparencia do grid |

### Temas Pre-definidos

| Tema | Descricao | Uso Ideal |
|------|-----------|-----------|
| `"professional"` | Estilo limpo e corporativo | Relatorios e apresentacoes |
| `"academic"` | Estilo para publicacoes | Papers e teses |
| `"presentation"` | Alto contraste, fontes grandes | Slides e conferencias |
| `"risk"` | Cores de alerta (verde/amarelo/vermelho) | Dashboards de risco |

### Funcoes de Tema

```python
from archbox.visualization.themes import get_theme, list_themes, register_theme

# Listar temas disponiveis
print(list_themes())  # ['professional', 'academic', 'presentation', 'risk']

# Obter tema
theme = get_theme("academic")

# Registrar tema customizado
from archbox.visualization.themes import Theme
meu_tema = Theme(
    name="custom",
    colors={"primary": "#1a1a2e", "secondary": "#16213e"},
    font_family="serif",
    font_sizes={"title": 14, "label": 11, "tick": 9},
    line_widths={"main": 1.5, "secondary": 1.0},
    figure_size=(10, 6),
    dpi=150,
    grid_alpha=0.3
)
register_theme("custom", meu_tema)
```

---

## Exportacao

### Funcoes de Export

::: archbox.visualization.export
    options:
      show_root_heading: true
      show_source: true

| Funcao | Formato | Descricao |
|--------|---------|-----------|
| `export_png()` | PNG | Bitmap com DPI configuravel |
| `export_svg()` | SVG | Vetorial para web |
| `export_pdf()` | PDF | Vetorial para impressao |
| `export_html()` | HTML | Interativo (Plotly) |

```python
from archbox.visualization.export import export_png, export_svg, export_pdf, export_html

# Exportar em diferentes formatos
export_png(fig, "grafico.png", dpi=300)
export_svg(fig, "grafico.svg")
export_pdf(fig, "grafico.pdf")
export_html(fig, "grafico.html")
```

| Parametro | Tipo | Default | Descricao |
|-----------|------|---------|-----------|
| `fig` | `Figure` | -- | Figura matplotlib |
| `filepath` | `str \| Path` | -- | Caminho de saida |
| `dpi` | `int` | `150` | Resolucao (apenas PNG) |
| `transparent` | `bool` | `False` | Fundo transparente |
| `bbox_inches` | `str` | `"tight"` | Ajuste de margens |

---

## Exemplo Completo

```python
from archbox.models import GARCH
from archbox.visualization import (
    plot_volatility, plot_diagnostics, plot_news_impact
)
from archbox.visualization.themes import get_theme
from archbox.visualization.export import export_png
import numpy as np

np.random.seed(42)
returns = np.random.randn(1000) * 0.01

# Ajustar modelo
model = GARCH(returns, p=1, q=1)
result = model.fit(disp=False)

# Volatilidade com tema academico
fig_vol = plot_volatility(result, annualize=True, theme="academic")
export_png(fig_vol, "volatilidade.png", dpi=300)

# Diagnosticos
fig_diag = plot_diagnostics(result, max_lags=20, theme="professional")
export_png(fig_diag, "diagnosticos.png", dpi=300)

# News Impact Curve
fig_nic = plot_news_impact(result, theme="presentation")
export_png(fig_nic, "news_impact.png", dpi=300)
```

---

## Ver Tambem

- [Core](core.md) -- `ArchResults` usado como input dos plots
- [Diagnostics](diagnostics.md) -- Testes estatisticos complementares
- [Risk](risk.md) -- `VaRBacktest` para `plot_var_backtest()`
- [Multivariado](multivariate.md) -- `MultivarResults` para plots de correlacao
- [Reports](reports.md) -- Geracao de relatorios com figuras integradas
