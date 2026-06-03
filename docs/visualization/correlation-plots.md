---
title: "Correlation Plots"
description: "Dynamic correlation visualization: pairwise time series, heatmaps, animated heatmaps, and conditional covariance matrices"
---

# Correlation Plots

!!! abstract "Key Takeaway"
    ArchBox provides four correlation visualizations for multivariate models: pairwise dynamic correlation over time, static heatmaps at a given date, animated heatmaps showing temporal evolution, and conditional covariance matrix plots. All are designed for DCC, BEKK, CCC, and GO-GARCH results.

---

## Overview

After fitting a multivariate GARCH model (DCC, BEKK, CCC, GO-GARCH), the time-varying correlation matrix $R_t$ and covariance matrix $H_t$ can be visualized:

```python
result.plot("correlation")          # Pairwise dynamic correlation
result.plot("correlation-heatmap")  # Heatmap at a specific date
result.plot("correlation-animated") # Animated temporal evolution
result.plot("covariance")           # Conditional covariance matrix
```

### Mathematical Context

In the DCC model, the conditional correlation matrix evolves as:

$$Q_t = (1 - a - b)\bar{Q} + a \, z_{t-1} z_{t-1}' + b \, Q_{t-1}$$

$$R_t = \text{diag}(Q_t)^{-1/2} \, Q_t \, \text{diag}(Q_t)^{-1/2}$$

where $R_t$ is the correlation matrix with elements $\rho_{ij,t} \in [-1, 1]$.

---

## Plot Type 1: Dynamic Correlation (Time Series)

Displays the pairwise conditional correlation $\rho_{ij,t}$ over time for selected asset pairs.

### Basic Usage

```python
from archbox.multivariate import DCC
from archbox.datasets import load_returns

# Load multivariate returns
returns = load_returns("portfolio_3")  # 3-asset portfolio

# Fit DCC-GARCH
model = DCC(returns, p=1, q=1)
result = model.fit()

# Plot all pairwise correlations
fig = result.plot("correlation")
```

??? example "Expected Output"
    The chart displays:

    - One line per asset pair (e.g., 3 pairs for a 3-asset portfolio)
    - **X-axis**: Date range matching the sample
    - **Y-axis**: Correlation coefficient $\rho_{ij,t} \in [-1, 1]$
    - Horizontal dashed line at $\rho = 0$
    - Correlations rise during market stress (flight to correlation) and fall during calm periods
    - Each pair in a distinct color with legend labels (e.g., "SPY-TLT", "SPY-GLD")

### Full Customization

```python
fig = result.plot(
    "correlation",
    # Pair selection
    pairs=[("SPY", "TLT"), ("SPY", "GLD")],  # Specific pairs
    # Styling
    colors=["#6C3483", "#E74C3C"],
    linewidths=[1.5, 1.5],
    linestyles=["-", "--"],
    # Reference lines
    show_unconditional=True,            # Horizontal line at ρ̄_ij
    show_zero=True,                     # Horizontal line at 0
    # Shaded regions
    shade_crisis=True,                  # Shade NBER recessions
    shade_color="#F5B7B1",
    shade_alpha=0.2,
    # Layout
    title="Dynamic Correlation -- DCC-GARCH(1,1)",
    figsize=(14, 6),
    start_date="2015-01-01",
    ylabel="Conditional Correlation",
    legend_loc="lower left",
)
```

??? example "Expected Output"
    The customized chart shows:

    - Two correlation series: SPY-TLT in purple (solid) and SPY-GLD in red (dashed)
    - Horizontal dashed lines at each pair's unconditional correlation
    - Light red shading during NBER recession periods
    - SPY-TLT correlation typically negative (stocks vs. bonds), rising toward zero during crises
    - SPY-GLD correlation more volatile, reflecting gold's mixed role as a hedge

---

## Plot Type 2: Correlation Heatmap (Static Snapshot)

Displays the correlation matrix $R_t$ at a specific date as a color-coded heatmap.

### Basic Usage

```python
# Heatmap at a specific date
fig = result.plot("correlation-heatmap", date="2020-03-16")
```

??? example "Expected Output"
    The chart displays:

    - A square heatmap with asset names on both axes
    - Color scale from **blue** ($\rho = -1$) through **white** ($\rho = 0$) to **red** ($\rho = +1$)
    - Diagonal elements fixed at 1.0
    - Numeric correlation values annotated in each cell
    - Title showing the date: "Conditional Correlation Matrix -- 2020-03-16"

### Full Customization

```python
fig = result.plot(
    "correlation-heatmap",
    date="2020-03-16",
    # Color
    cmap="RdBu_r",                      # Colormap (diverging)
    vmin=-1.0,                          # Color scale min
    vmax=1.0,                           # Color scale max
    # Annotations
    annotate=True,                      # Show numeric values
    fmt=".2f",                          # Number format
    fontsize=10,                        # Annotation font size
    # Layout
    title="Correlation Matrix -- COVID Crash (2020-03-16)",
    figsize=(8, 7),
    # Masking
    mask_upper=True,                    # Show only lower triangle
)
```

??? example "Expected Output"
    The heatmap shows:

    - Lower triangle only (upper masked for clarity)
    - Red/blue diverging colormap centered at zero
    - Two-decimal correlation values in each cell
    - During the COVID crash, most equity pairs show elevated positive correlation (~0.7--0.9)
    - Bond-equity pairs may show negative or near-zero correlation

### Comparing Two Dates

```python
from archbox.visualization import compare_heatmaps

fig = compare_heatmaps(
    result,
    dates=["2019-12-31", "2020-03-16"],
    titles=["Pre-COVID (2019-12-31)", "COVID Crash (2020-03-16)"],
    figsize=(16, 7),
)
```

??? example "Expected Output"
    Side-by-side heatmaps showing:

    - **Left**: Pre-COVID correlation structure (moderate, diversified correlations)
    - **Right**: COVID crash correlation structure (elevated correlations, breakdown of diversification)
    - The visual contrast highlights the "correlation breakdown" phenomenon in crisis periods

---

## Plot Type 3: Animated Heatmap (Temporal Evolution)

Creates an animated visualization of the correlation matrix evolving over time. Available only with the Plotly backend.

### Basic Usage

```python
# Animated heatmap (plotly only)
fig = result.plot(
    "correlation-animated",
    backend="plotly",
)
```

??? example "Expected Output"
    An interactive animation showing:

    - A heatmap that evolves frame-by-frame over time
    - A **play/pause** button and a **slider** for manual navigation
    - The date displayed as the animation title
    - Color transitions reveal how correlations shift during different market regimes
    - Smooth transitions between frames

### Full Customization

```python
fig = result.plot(
    "correlation-animated",
    backend="plotly",
    # Animation
    freq="M",                           # Frame frequency: D, W, M, Q
    fps=5,                              # Frames per second
    transition_duration=300,            # Transition in ms
    # Date range
    start_date="2018-01-01",
    end_date="2023-12-31",
    # Color
    cmap="RdBu_r",
    vmin=-1.0,
    vmax=1.0,
    # Layout
    title="Dynamic Correlation Evolution",
    figsize=(8, 7),
)

# Save as HTML
fig.write_html("correlation_animation.html")
```

??? example "Expected Output"
    The interactive animation shows:

    - Monthly snapshots from 2018 to 2023
    - Each frame is a complete correlation heatmap
    - The slider allows jumping to any month
    - During the COVID period (March 2020), correlations spike visibly
    - Post-crisis, correlations gradually return to pre-crisis levels

---

## Plot Type 4: Conditional Covariance Matrix

Visualizes the full conditional covariance matrix $H_t$ elements over time, or as a 3D surface.

### Mathematical Context

The conditional covariance matrix decomposes as:

$$H_t = D_t R_t D_t$$

where $D_t = \text{diag}(\sigma_{1,t}, \ldots, \sigma_{N,t})$ contains the individual conditional volatilities.

### Basic Usage

```python
# Covariance elements over time
fig = result.plot("covariance")
```

??? example "Expected Output"
    A multi-panel chart showing:

    - One subplot per unique element of $H_t$ (variances on diagonal, covariances off-diagonal)
    - **Diagonal panels**: Individual conditional variances $\sigma_{i,t}^2$
    - **Off-diagonal panels**: Conditional covariances $h_{ij,t} = \sigma_{i,t} \sigma_{j,t} \rho_{ij,t}$
    - All panels share the same x-axis (date range)

### Full Customization

```python
fig = result.plot(
    "covariance",
    # Selection
    elements=[("SPY", "SPY"), ("SPY", "TLT"), ("TLT", "TLT")],
    # Styling
    colors=["#6C3483", "#E74C3C", "#2E86C1"],
    fill=True,
    fill_alpha=0.1,
    # Layout
    title="Conditional Covariance Elements -- DCC-GARCH",
    figsize=(14, 10),
    layout="grid",                      # "grid" or "stacked"
    sharex=True,
)
```

??? example "Expected Output"
    A 2x2 grid of subplots showing:

    - **Top-left**: SPY variance $\sigma_{\text{SPY},t}^2$ (largest magnitude, spikes during crises)
    - **Top-right**: SPY-TLT covariance $h_{\text{SPY,TLT},t}$ (often negative, reflecting stock-bond hedge)
    - **Bottom-left**: TLT-SPY covariance (symmetric, same as top-right)
    - **Bottom-right**: TLT variance $\sigma_{\text{TLT},t}^2$ (lower magnitude, spikes during rate shocks)
    - Each panel has a light color fill under the curve

---

## Complete DCC-GARCH Example

A full workflow from estimation to publication-ready correlation plots:

```python
import numpy as np
from archbox.multivariate import DCC
from archbox.datasets import load_returns

# Load 5-asset portfolio
returns = load_returns("portfolio_5")
print(f"Assets: {returns.columns.tolist()}")
print(f"Sample: {returns.index[0]} to {returns.index[-1]}")
print(f"Observations: {len(returns)}")

# Fit DCC-GARCH(1,1)
model = DCC(returns, p=1, q=1, dist="student-t")
result = model.fit()

# --- Plot 1: Dynamic correlations ---
fig1 = result.plot(
    "correlation",
    pairs=[("SPY", "TLT"), ("SPY", "GLD"), ("TLT", "GLD")],
    title="Dynamic Pairwise Correlations",
    figsize=(14, 6),
)
fig1.savefig("dcc_correlations.pdf", bbox_inches="tight")

# --- Plot 2: Heatmap comparison ---
from archbox.visualization import compare_heatmaps

fig2 = compare_heatmaps(
    result,
    dates=["2019-06-30", "2020-03-16", "2023-06-30"],
    titles=["Pre-COVID", "COVID Crash", "Post-COVID"],
    figsize=(20, 6),
    mask_upper=True,
)
fig2.savefig("dcc_heatmaps.pdf", bbox_inches="tight")

# --- Plot 3: Animated evolution ---
fig3 = result.plot(
    "correlation-animated",
    backend="plotly",
    freq="M",
    start_date="2019-01-01",
    end_date="2023-12-31",
)
fig3.write_html("dcc_animation.html")

# --- Plot 4: Covariance matrix ---
fig4 = result.plot(
    "covariance",
    layout="grid",
    figsize=(16, 12),
)
fig4.savefig("dcc_covariance.pdf", bbox_inches="tight")
```

---

## Common Customization Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `backend` | `str` | `"matplotlib"` | `"matplotlib"` or `"plotly"` |
| `theme` | `str` | `"archbox"` | Plot theme |
| `figsize` | `tuple` | `(12, 6)` | Figure size in inches |
| `title` | `str` | Auto | Plot title |
| `start_date` | `str` | `None` | Start date filter |
| `end_date` | `str` | `None` | End date filter |
| `cmap` | `str` | `"RdBu_r"` | Colormap for heatmaps |
| `annotate` | `bool` | `True` | Show values on heatmaps |
| `grid` | `bool` | `True` | Show grid lines |
| `dpi` | `int` | `150` | Export resolution |

---

## See Also

- [Visualization Overview](index.md) -- backends, themes, and export formats
- [Volatility Plots](volatility-plots.md) -- univariate volatility charts
- [Risk Plots](risk-plots.md) -- VaR and ES visualizations
- [DCC User Guide](../user-guide/multivariate/dcc.md) -- DCC model estimation
- [Multivariate Theory](../theory/multivariate-theory.md) -- mathematical foundations
