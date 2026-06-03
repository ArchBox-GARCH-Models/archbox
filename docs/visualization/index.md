---
title: "Visualization"
description: "Overview of ArchBox visualization system: volatility, correlation, risk, regime, and diagnostic plots"
---

# Visualization

!!! abstract "Key Takeaway"
    ArchBox provides a unified plotting API for volatility, correlation, risk, and diagnostic charts. All plots support **matplotlib** (static, publication-quality) and **plotly** (interactive, browser-based) backends with consistent theming.

---

## Overview

Every fitted model in ArchBox exposes a `.plot()` method that dispatches to the appropriate visualization. The plotting system is designed around three principles:

1. **One-line defaults** -- sensible plots with zero configuration
2. **Full customization** -- colors, labels, date ranges, export formats
3. **Backend agnostic** -- switch between matplotlib and plotly with a single parameter

```python
from archbox.models import GARCH

model = GARCH(returns, p=1, q=1)
result = model.fit()

# One-line volatility plot (matplotlib)
result.plot("volatility")

# Interactive version (plotly)
result.plot("volatility", backend="plotly")
```

---

## Available Plot Types

| Category | Plot Type | Description | Page |
|----------|-----------|-------------|------|
| :material-chart-line: **Volatility** | Conditional volatility | $\sigma_t$ series over time | [Volatility Plots](volatility-plots.md) |
| :material-chart-line: **Volatility** | Returns with bands | Returns $\pm 2\sigma_t$ envelope | [Volatility Plots](volatility-plots.md) |
| :material-chart-line: **Volatility** | Fan chart | Multi-horizon forecast intervals | [Volatility Plots](volatility-plots.md) |
| :material-chart-line: **Volatility** | Model comparison | Multiple models overlaid | [Volatility Plots](volatility-plots.md) |
| :material-chart-scatter-plot: **Correlation** | Dynamic correlation | Pairwise $\rho_{ij,t}$ over time | [Correlation Plots](correlation-plots.md) |
| :material-chart-scatter-plot: **Correlation** | Correlation heatmap | Snapshot at a given date | [Correlation Plots](correlation-plots.md) |
| :material-chart-scatter-plot: **Correlation** | Animated heatmap | Temporal evolution of $R_t$ | [Correlation Plots](correlation-plots.md) |
| :material-chart-scatter-plot: **Correlation** | Covariance matrix | Conditional $H_t$ visualization | [Correlation Plots](correlation-plots.md) |
| :material-shield-alert: **Risk** | VaR overlay | Returns with VaR line | [Risk Plots](risk-plots.md) |
| :material-shield-alert: **Risk** | Exceedances | VaR violations highlighted | [Risk Plots](risk-plots.md) |
| :material-shield-alert: **Risk** | VaR fan chart | Multiple confidence levels | [Risk Plots](risk-plots.md) |
| :material-shield-alert: **Risk** | ES vs VaR | Comparative risk measures | [Risk Plots](risk-plots.md) |
| :material-shield-alert: **Risk** | Traffic light | Basel backtest visual | [Risk Plots](risk-plots.md) |
| :material-swap-horizontal: **Regimes** | Smoothed probabilities | Regime probabilities over time | [Regime Plots](regime-plots.md) |
| :material-stethoscope: **Diagnostics** | QQ-plot, ACF, News Impact | Residual analysis charts | [Diagnostic Plots](diagnostic-plots.md) |

---

## Backends

ArchBox supports two rendering backends. The backend can be set globally or per-plot.

=== "Matplotlib (default)"

    Best for **publications, reports, and static exports**. Produces high-resolution PNG, SVG, and PDF files.

    ```python
    # Global setting
    import archbox
    archbox.set_plot_backend("matplotlib")

    # Per-plot override
    result.plot("volatility", backend="matplotlib")
    ```

    **Pros:** Publication-quality output, full LaTeX support, PDF/SVG export, no browser needed.

    **Cons:** Static only, no zoom/pan interaction.

=== "Plotly (interactive)"

    Best for **exploration, dashboards, and presentations**. Renders in the browser with zoom, pan, and hover tooltips.

    ```python
    # Global setting
    import archbox
    archbox.set_plot_backend("plotly")

    # Per-plot override
    result.plot("volatility", backend="plotly")
    ```

    **Pros:** Interactive zoom/pan, hover data inspection, easy HTML embedding.

    **Cons:** Requires browser, larger file sizes, less control over fine typography.

!!! tip "Installation"
    Matplotlib is included as a core dependency. For Plotly support, install the optional dependency:
    ```bash
    pip install archbox[plotly]
    ```

---

## Themes

ArchBox provides built-in themes that apply consistent styling across all plot types.

| Theme | Description | Best For |
|-------|-------------|----------|
| `"archbox"` | Default deep purple/amber theme | General use |
| `"academic"` | Clean, minimal with serif fonts | Academic papers |
| `"dark"` | Dark background with bright accents | Presentations, dashboards |
| `"minimal"` | Reduced chrome, focus on data | Reports |
| `"bloomberg"` | Finance terminal-inspired | Trading desks |

```python
import archbox

# Set global theme
archbox.set_plot_theme("academic")

# Per-plot override
result.plot("volatility", theme="dark")
```

Each theme controls: background color, grid style, font family, color palette, line widths, and axis formatting.

!!! info "Custom Themes"
    You can create custom themes by passing a dictionary of matplotlib/plotly parameters:
    ```python
    my_theme = {
        "background": "#1a1a2e",
        "palette": ["#e94560", "#0f3460", "#16213e"],
        "font_family": "Fira Code",
        "grid_alpha": 0.2,
    }
    archbox.set_plot_theme(my_theme)
    ```

---

## Quick Example

A complete example from data to publication-ready volatility plot:

```python
import numpy as np
from archbox.models import GARCH
from archbox.datasets import load_returns

# Load sample data
returns = load_returns("sp500")

# Fit GARCH(1,1) with Student-t innovations
model = GARCH(returns, p=1, q=1, dist="student-t")
result = model.fit()

# Plot conditional volatility with returns overlay
fig = result.plot(
    "volatility",
    show_returns=True,
    title="S&P 500 Conditional Volatility -- GARCH(1,1)",
    figsize=(12, 6),
    colors={"volatility": "#6C3483", "returns": "#AEB6BF"},
    start_date="2020-01-01",
)

# Export to multiple formats
fig.savefig("volatility.png", dpi=300, bbox_inches="tight")
fig.savefig("volatility.svg", bbox_inches="tight")
fig.savefig("volatility.pdf", bbox_inches="tight")
```

??? example "Expected Output"
    The plot displays:

    - **Top panel**: Daily returns as a grey bar chart with $\pm 2\sigma_t$ bands in purple
    - **Bottom panel**: Conditional volatility $\sigma_t$ as a solid purple line
    - **X-axis**: Date range from 2020-01-01 onwards
    - **Y-axis (top)**: Returns in percentage
    - **Y-axis (bottom)**: Annualized volatility (%)
    - Volatility spikes are clearly visible during market stress periods (e.g., COVID-19 crash in March 2020)

---

## Export Formats

All plots can be exported to the following formats:

| Format | Extension | Use Case | Backend |
|--------|-----------|----------|---------|
| PNG | `.png` | Web, slides | Both |
| SVG | `.svg` | Scalable web graphics | Both |
| PDF | `.pdf` | Publications, LaTeX | Matplotlib |
| HTML | `.html` | Interactive dashboards | Plotly |

```python
# Matplotlib export
fig = result.plot("volatility")
fig.savefig("plot.png", dpi=300, bbox_inches="tight")
fig.savefig("plot.pdf", bbox_inches="tight")

# Plotly export
fig = result.plot("volatility", backend="plotly")
fig.write_html("plot.html")
fig.write_image("plot.png", scale=2)
```

---

## See Also

- [Volatility Plots](volatility-plots.md) -- conditional volatility and forecast charts
- [Correlation Plots](correlation-plots.md) -- dynamic correlation and heatmaps
- [Risk Plots](risk-plots.md) -- VaR, ES, and backtest visualizations
- [Regime Plots](regime-plots.md) -- regime probability charts
- [Diagnostic Plots](diagnostic-plots.md) -- residual analysis and model checks
- [Themes](themes.md) -- complete theme customization guide
