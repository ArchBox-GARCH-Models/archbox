---
title: "Themes & Customization"
description: "Plot themes and customization: built-in themes, color palettes, font configuration, custom themes, and matplotlib rcParams integration"
---

# Themes & Customization

!!! abstract "Key Takeaway"
    ArchBox provides five built-in themes (`archbox`, `academic`, `dark`, `minimal`, `bloomberg`) and a flexible customization system for colors, fonts, sizes, and grid styles. Themes integrate seamlessly with matplotlib `rcParams` and can be applied globally or per-plot.

---

## Overview

Every ArchBox plot accepts a `theme` parameter that controls the visual appearance. Themes can be set globally (affecting all subsequent plots) or per-plot:

```python
import archbox

# Global theme
archbox.set_plot_theme("academic")

# Per-plot override
result.plot("volatility", theme="dark")

# Reset to default
archbox.set_plot_theme("archbox")
```

---

## Built-in Themes

### Theme: `archbox` (Default)

The default theme with a clean, professional appearance suitable for reports and presentations.

```python
result.plot("volatility", theme="archbox")
```

??? example "Theme Properties"
    | Property | Value |
    |----------|-------|
    | Background | White (`#FFFFFF`) |
    | Text color | Dark grey (`#2C3E50`) |
    | Primary color | Deep purple (`#6C3483`) |
    | Accent color | Amber (`#F39C12`) |
    | Grid | Light grey, alpha 0.3 |
    | Font | DejaVu Sans, 11pt |
    | Figure size | 12 × 6 inches |
    | Spine | Bottom and left only |

### Theme: `academic`

Optimized for academic papers and journal submissions. Uses serif fonts, minimal decoration, and high-contrast black/grey palette.

```python
result.plot("volatility", theme="academic")
```

??? example "Theme Properties"
    | Property | Value |
    |----------|-------|
    | Background | White (`#FFFFFF`) |
    | Text color | Black (`#000000`) |
    | Primary color | Black (`#000000`) |
    | Accent color | Dark grey (`#404040`) |
    | Grid | None (clean for print) |
    | Font | Times New Roman, 12pt |
    | Figure size | 6.5 × 4 inches (journal column width) |
    | Spine | All four sides, thin |
    | Line width | 1.0 (thin for clarity at print size) |

!!! tip "Journal Requirements"
    The `academic` theme produces figures that meet common journal specifications: single-column width (6.5"), serif fonts, and minimal visual clutter. Adjust `figsize` for double-column layouts.

### Theme: `dark`

Dark background theme for presentations and dashboards with high visual impact.

```python
result.plot("volatility", theme="dark")
```

??? example "Theme Properties"
    | Property | Value |
    |----------|-------|
    | Background | Dark charcoal (`#1C1C1C`) |
    | Text color | Light grey (`#E0E0E0`) |
    | Primary color | Cyan (`#00BCD4`) |
    | Accent color | Amber (`#FFC107`) |
    | Grid | Dark grey (`#333333`), alpha 0.5 |
    | Font | Helvetica, 12pt |
    | Figure size | 14 × 7 inches |
    | Spine | None (borderless) |

### Theme: `minimal`

Ultra-clean theme with maximum data-ink ratio. Removes all non-essential elements following Tufte's principles.

```python
result.plot("volatility", theme="minimal")
```

??? example "Theme Properties"
    | Property | Value |
    |----------|-------|
    | Background | White (`#FFFFFF`) |
    | Text color | Dark grey (`#333333`) |
    | Primary color | Steel blue (`#4682B4`) |
    | Accent color | Coral (`#FF6B6B`) |
    | Grid | None |
    | Font | Helvetica Neue, 10pt |
    | Figure size | 10 × 5 inches |
    | Spine | Bottom only (range frame) |
    | Tick marks | Minimal, outward |

### Theme: `bloomberg`

Inspired by Bloomberg Terminal aesthetics. Dark background with distinctive orange/white color scheme.

```python
result.plot("volatility", theme="bloomberg")
```

??? example "Theme Properties"
    | Property | Value |
    |----------|-------|
    | Background | Bloomberg black (`#0B0B0B`) |
    | Text color | White (`#FFFFFF`) |
    | Primary color | Bloomberg orange (`#FF6600`) |
    | Accent color | White (`#FFFFFF`) |
    | Grid | Dark grey (`#1A1A1A`), alpha 0.8 |
    | Font | Consolas (monospace), 11pt |
    | Figure size | 14 × 7 inches |
    | Spine | None |
    | Line width | 1.5 |

---

## Theme Comparison

```python
import matplotlib.pyplot as plt
from archbox.models import GARCH
from archbox.datasets import load_returns

returns = load_returns("sp500")
result = GARCH(returns, p=1, q=1).fit()

themes = ["archbox", "academic", "dark", "minimal", "bloomberg"]

fig, axes = plt.subplots(len(themes), 1, figsize=(14, 4 * len(themes)))

for ax, theme in zip(axes, themes):
    result.plot("volatility", theme=theme, ax=ax, title=f"Theme: {theme}")

plt.tight_layout()
fig.savefig("theme_comparison.png", dpi=200, bbox_inches="tight")
```

---

## Global Customization

### Color Palette

Override the default color palette globally:

```python
import archbox

archbox.set_plot_theme("archbox", colors={
    "primary": "#1A5276",
    "secondary": "#E74C3C",
    "accent": "#27AE60",
    "background": "#FAFAFA",
    "text": "#2C3E50",
    "grid": "#D5D8DC",
})
```

### Figure Size

Set default figure sizes globally:

```python
archbox.set_plot_theme("archbox", figsize=(16, 8))
```

### Fonts

Configure font family, size, and weight:

```python
archbox.set_plot_theme("archbox", fonts={
    "family": "Helvetica",
    "size": 12,
    "title_size": 16,
    "label_size": 12,
    "tick_size": 10,
    "legend_size": 10,
    "weight": "normal",
    "title_weight": "bold",
})
```

### Grid and Background

Control grid lines and background appearance:

```python
archbox.set_plot_theme("archbox", grid={
    "visible": True,
    "color": "#E0E0E0",
    "alpha": 0.5,
    "linewidth": 0.5,
    "linestyle": "--",
    "which": "major",        # "major", "minor", or "both"
})
```

---

## Per-Plot Customization

Override theme settings for individual plots without changing the global theme:

```python
# Global theme is "archbox"
archbox.set_plot_theme("archbox")

# This specific plot uses dark theme
fig = result.plot(
    "volatility",
    theme="dark",
    figsize=(16, 8),
    title="Custom Dark Plot",
)

# This plot uses default "archbox" theme
fig2 = result.plot("volatility")
```

### Per-Plot Type Defaults

Set default customizations for specific plot types:

```python
archbox.set_plot_defaults("volatility", {
    "figsize": (14, 6),
    "color": "#6C3483",
    "fill": True,
    "fill_alpha": 0.15,
    "annualize": True,
})

archbox.set_plot_defaults("diagnostics", {
    "figsize": (14, 10),
    "layout": (2, 2),
    "color": "#2E86C1",
})

archbox.set_plot_defaults("regimes", {
    "figsize": (14, 7),
    "regime_colors": ["#2E86C1", "#E74C3C"],
    "regime_alpha": 0.3,
})
```

---

## Creating a Custom Theme

Define a fully custom theme using a dictionary:

```python
import archbox

my_theme = {
    "name": "corporate",
    # Colors
    "colors": {
        "primary": "#003366",           # Navy blue
        "secondary": "#CC0000",         # Corporate red
        "accent": "#006633",            # Forest green
        "background": "#FFFFFF",
        "text": "#333333",
        "grid": "#CCCCCC",
    },
    # Color cycle for multi-series plots
    "color_cycle": [
        "#003366", "#CC0000", "#006633",
        "#FF9900", "#660099", "#009999",
    ],
    # Figure
    "figsize": (12, 6),
    "dpi": 150,
    # Fonts
    "fonts": {
        "family": "Arial",
        "size": 11,
        "title_size": 14,
        "label_size": 11,
        "tick_size": 9,
        "legend_size": 9,
        "weight": "normal",
        "title_weight": "bold",
    },
    # Grid
    "grid": {
        "visible": True,
        "color": "#CCCCCC",
        "alpha": 0.4,
        "linewidth": 0.5,
        "linestyle": "-",
    },
    # Spines
    "spines": {
        "left": True,
        "bottom": True,
        "right": False,
        "top": False,
        "linewidth": 0.8,
    },
    # Line defaults
    "linewidth": 1.5,
    "marker_size": 5,
}

# Register the custom theme
archbox.register_theme("corporate", my_theme)

# Use it
result.plot("volatility", theme="corporate")
```

---

## Publication-Ready Example

A complete workflow for producing journal-quality figures:

```python
import archbox
from archbox.models import GARCH, EGARCH, GJR
from archbox.visualization import compare_volatility
from archbox.datasets import load_returns

# --- Step 1: Configure the academic theme with customizations ---
archbox.set_plot_theme("academic", fonts={
    "family": "Times New Roman",
    "size": 11,
    "title_size": 12,
    "label_size": 11,
    "tick_size": 9,
})

# --- Step 2: Load data and fit models ---
returns = load_returns("sp500")
garch = GARCH(returns, p=1, q=1, dist="student-t").fit()
egarch = EGARCH(returns, p=1, q=1, dist="student-t").fit()
gjr = GJR(returns, p=1, q=1, dist="student-t").fit()

# --- Step 3: Figure 1 -- Conditional Volatility ---
fig1 = garch.plot(
    "volatility",
    figsize=(6.5, 3.5),                     # Single-column width
    color="#000000",
    linewidth=0.8,
    fill=True,
    fill_alpha=0.1,
    title="",                               # No title (use LaTeX caption)
    ylabel="Annualized Volatility (%)",
    grid=False,
)
fig1.savefig("fig1_volatility.pdf", bbox_inches="tight")

# --- Step 4: Figure 2 -- Diagnostic Grid ---
fig2 = garch.plot(
    "diagnostics",
    figsize=(6.5, 5.5),
    color="#000000",
    title="",
)
fig2.savefig("fig2_diagnostics.pdf", bbox_inches="tight")

# --- Step 5: Figure 3 -- Model Comparison ---
fig3 = compare_volatility(
    models=[garch, egarch, gjr],
    labels=["GARCH(1,1)", "EGARCH(1,1)", "GJR(1,1)"],
    colors=["#000000", "#666666", "#999999"],
    linestyles=["-", "--", "-."],
    linewidths=[1.0, 0.8, 0.8],
    figsize=(6.5, 3.5),
    title="",
    ylabel="Annualized Volatility (%)",
    grid=False,
)
fig3.savefig("fig3_comparison.pdf", bbox_inches="tight")

# --- Step 6: Figure 4 -- Regime Analysis ---
from archbox.regime import MarkovSwitchingGARCH

ms = MarkovSwitchingGARCH(returns, k_regimes=2, p=1, q=1).fit()

fig4 = ms.plot(
    "smoothed",
    figsize=(6.5, 5.0),
    prob_color="#000000",
    fill=True,
    fill_alpha=0.15,
    title="",
    height_ratios=[2, 1],
)
fig4.savefig("fig4_regimes.pdf", bbox_inches="tight")

print("All figures exported as PDF for LaTeX inclusion.")
```

!!! tip "LaTeX Integration"
    Include the exported PDFs in your LaTeX document:
    ```latex
    \begin{figure}[htbp]
        \centering
        \includegraphics[width=\columnwidth]{fig1_volatility.pdf}
        \caption{Conditional volatility from the GARCH(1,1)-$t$ model
        applied to S\&P~500 daily returns, 2000--2023. Shaded area
        represents the annualized conditional standard deviation.}
        \label{fig:volatility}
    \end{figure}
    ```

---

## Integration with Matplotlib rcParams

ArchBox themes are thin wrappers around matplotlib's `rcParams`. You can access and modify the underlying parameters directly:

### Reading Current Theme as rcParams

```python
import archbox

# Get the current theme as a dictionary of rcParams
params = archbox.get_theme_rcparams()
print(params)
```

??? example "Expected Output"
    ```python
    {
        'figure.figsize': (12, 6),
        'figure.dpi': 150,
        'figure.facecolor': '#FFFFFF',
        'axes.facecolor': '#FFFFFF',
        'axes.edgecolor': '#2C3E50',
        'axes.labelcolor': '#2C3E50',
        'axes.labelsize': 12,
        'axes.titlesize': 16,
        'axes.grid': True,
        'grid.color': '#D5D8DC',
        'grid.alpha': 0.3,
        'grid.linewidth': 0.5,
        'font.family': ['sans-serif'],
        'font.sans-serif': ['DejaVu Sans'],
        'font.size': 11,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'lines.linewidth': 1.5,
        ...
    }
    ```

### Using rcParams Directly

```python
import matplotlib.pyplot as plt

# Apply ArchBox theme via rcParams
with plt.rc_context(archbox.get_theme_rcparams("academic")):
    fig, ax = plt.subplots()
    ax.plot(returns.values, color="black", linewidth=0.8)
    ax.set_ylabel("Log Returns")
    fig.savefig("custom_plot.pdf", bbox_inches="tight")
```

### Mixing with Matplotlib Styles

```python
import matplotlib.pyplot as plt

# Combine ArchBox theme with matplotlib style
plt.style.use("seaborn-v0_8-whitegrid")
archbox.set_plot_theme("archbox")  # ArchBox overrides take priority

# Or use matplotlib context manager
with plt.style.context("ggplot"):
    result.plot("volatility", theme="archbox")
```

---

## Color Palettes for Multi-Series Plots

ArchBox provides color palettes optimized for financial data visualization:

```python
from archbox.visualization import get_palette

# Named palettes
colors = get_palette("default", n=5)       # Default archbox colors
colors = get_palette("colorblind", n=5)    # Colorblind-safe palette
colors = get_palette("sequential", n=5)    # Sequential purple shades
colors = get_palette("diverging", n=5)     # Blue-to-red diverging

# Use in plots
fig = compare_volatility(
    models=models,
    colors=get_palette("colorblind", n=len(models)),
)
```

!!! warning "Colorblind Accessibility"
    When producing figures for publication, prefer the `"colorblind"` palette to ensure accessibility. Combine with distinct line styles (`"-"`, `"--"`, `"-."`) for additional differentiation.

### Available Palettes

| Palette | Description | Best For |
|---------|-------------|----------|
| `"default"` | ArchBox brand colors (purple, red, blue, green, amber) | General use |
| `"colorblind"` | Okabe-Ito colorblind-safe palette | Publications |
| `"sequential"` | Light-to-dark gradient in primary color | Ordered data |
| `"diverging"` | Blue--white--red diverging scale | Correlations, heatmaps |
| `"categorical"` | High-contrast categorical colors | Multi-model comparison |
| `"muted"` | Pastel tones for background elements | Shading, fills |

---

## Common Customization Options

All plots accept these theme-related parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `theme` | `str` | `"archbox"` | Theme name |
| `figsize` | `tuple` | Theme default | Figure size in inches |
| `dpi` | `int` | `150` | Resolution |
| `title` | `str` | Auto | Plot title (`""` to suppress) |
| `grid` | `bool` | Theme default | Show grid |
| `backend` | `str` | `"matplotlib"` | `"matplotlib"` or `"plotly"` |

---

## See Also

- [Visualization Overview](index.md) -- backends, themes, and export formats
- [Volatility Plots](volatility-plots.md) -- conditional volatility charts
- [Correlation Plots](correlation-plots.md) -- multivariate correlation visualization
- [Risk Plots](risk-plots.md) -- VaR and ES charts
- [Regime Plots](regime-plots.md) -- regime-switching visualization
- [Diagnostic Plots](diagnostic-plots.md) -- model diagnostics
