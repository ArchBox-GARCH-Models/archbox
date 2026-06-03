---
title: "Regime Plots"
description: "Regime-switching visualization: filtered/smoothed probabilities, regime classification, transition matrices, duration analysis, and distribution comparison"
---

# Regime Plots

!!! abstract "Key Takeaway"
    ArchBox provides six types of regime-switching visualizations: filtered probabilities with shaded regions, smoothed probability panels, regime classification overlays, transition matrix heatmaps, regime duration charts, and per-regime distribution comparisons. All plots support matplotlib and plotly backends with full customization.

---

## Overview

After fitting a Markov-Switching model, the regime structure can be visualized in multiple ways. The primary entry points are the `.plot()` method on the fitted result and standalone functions:

```python
result.plot("regimes")              # Filtered probabilities over returns
result.plot("smoothed")             # Smoothed probabilities panel
result.plot("regime-classify")      # Classification by dominant regime
result.plot("transition-matrix")    # Transition matrix heatmap
result.plot("regime-duration")      # Regime duration over time
result.plot("regime-distribution")  # Distribution comparison by regime
```

---

## Plot Type 1: Filtered Probabilities with Shaded Regions

Displays the return series with regime probabilities from the Hamilton filter as shaded background regions, giving an immediate sense of which regime is active at each point in time.

### Mathematical Background

The Hamilton filter produces filtered probabilities $\Pr(S_t = j \mid \mathcal{F}_t)$, where $S_t$ is the latent regime state and $\mathcal{F}_t$ is the information set up to time $t$. These are computed recursively:

$$\Pr(S_t = j \mid \mathcal{F}_t) = \frac{f(r_t \mid S_t = j, \mathcal{F}_{t-1}) \cdot \Pr(S_t = j \mid \mathcal{F}_{t-1})}{\sum_{k=1}^{K} f(r_t \mid S_t = k, \mathcal{F}_{t-1}) \cdot \Pr(S_t = k \mid \mathcal{F}_{t-1})}$$

Shaded regions indicate periods where a given regime dominates (probability above a threshold).

### Basic Usage

```python
from archbox.regime import MarkovSwitchingGARCH
from archbox.datasets import load_returns

returns = load_returns("sp500")
model = MarkovSwitchingGARCH(returns, k_regimes=2, p=1, q=1)
result = model.fit()

# Filtered probabilities with shaded regions
fig = result.plot("regimes")
```

??? example "Expected Output"
    The chart displays:

    - **Top panel**: Return series as a thin line
    - **Shaded regions**: Background color changes based on the dominant regime
    - **Blue shading**: Low-volatility regime (calm markets)
    - **Red shading**: High-volatility regime (crisis periods)
    - Shading intensity reflects the regime probability (darker = higher probability)
    - Transitions between regimes are clearly visible at color boundaries

### Full Customization

```python
fig = result.plot(
    "regimes",
    # Regime colors
    regime_colors=["#2E86C1", "#E74C3C"],       # Blue=calm, Red=crisis
    regime_labels=["Low Vol", "High Vol"],
    regime_alpha=0.3,                            # Shading transparency
    # Probability threshold
    threshold=0.5,                               # Min probability to shade
    # Returns
    return_color="#2C3E50",
    return_linewidth=0.8,
    return_alpha=0.7,
    # Annotations
    annotate_events={
        "2008-09-15": "Lehman Brothers",
        "2020-03-12": "COVID Crash",
        "2022-06-13": "Bear Market",
    },
    # Layout
    title="S&P 500 Regime Classification -- MS-GARCH(1,1)",
    figsize=(14, 6),
    start_date="2006-01-01",
    end_date="2023-12-31",
    ylabel="Log Returns",
    grid=True,
    grid_alpha=0.3,
)

fig.savefig("regime_filtered.png", dpi=300, bbox_inches="tight")
```

??? example "Expected Output"
    The customized chart shows:

    - Blue-shaded calm periods dominating most of the sample
    - Intense red shading during 2008--2009 (GFC), March 2020 (COVID), and mid-2022
    - Vertical dashed annotations marking key events
    - The return series visible through the semi-transparent regime shading
    - Transitions between regimes coincide with well-known market stress events

---

## Plot Type 2: Smoothed Probabilities Panel

Displays the Kim-smoothed regime probabilities $\Pr(S_t = j \mid \mathcal{F}_T)$ in a separate panel below the return series. Smoothed probabilities use the full sample information and produce cleaner regime identification than filtered probabilities.

### Mathematical Background

The Kim smoother produces:

$$\Pr(S_t = j \mid \mathcal{F}_T) = \sum_{k=1}^{K} \Pr(S_t = j \mid S_{t+1} = k, \mathcal{F}_T) \cdot \Pr(S_{t+1} = k \mid \mathcal{F}_T)$$

where $\mathcal{F}_T$ denotes the full sample. These smoothed probabilities are less noisy than filtered probabilities because they incorporate future observations.

### Basic Usage

```python
# Smoothed probabilities in separate panel
fig = result.plot("smoothed")
```

??? example "Expected Output"
    The chart displays two vertically stacked panels:

    - **Top panel**: Return series
    - **Bottom panel**: Smoothed probability $\Pr(S_t = \text{High Vol} \mid \mathcal{F}_T)$
    - The probability line oscillates between 0 and 1
    - Values near 1 indicate the high-volatility regime is dominant
    - Values near 0 indicate the low-volatility regime
    - Transitions are sharper than in the filtered version

### Full Customization

```python
fig = result.plot(
    "smoothed",
    # Which regime to plot
    regime=1,                               # 0-indexed; 1 = high-vol
    # Probability line
    prob_color="#6C3483",
    prob_linewidth=1.5,
    fill=True,                              # Fill area under probability
    fill_alpha=0.2,
    # Threshold line
    show_threshold=True,
    threshold=0.5,
    threshold_color="#7F8C8D",
    threshold_style="--",
    # Returns panel
    return_color="#2C3E50",
    return_linewidth=0.8,
    # Layout
    title="Smoothed Regime Probabilities -- MS-GARCH(1,1)",
    figsize=(14, 8),
    height_ratios=[2, 1],                   # Top:bottom panel ratio
    start_date="2006-01-01",
)
```

??? example "Expected Output"
    The two-panel chart shows:

    - **Top panel**: Returns with visible volatility clustering
    - **Bottom panel**: Purple smoothed probability line with light fill
    - Horizontal dashed line at 0.5 threshold
    - Probability spikes to ~1.0 during 2008--2009, March 2020, and 2022
    - During calm markets, probability stays near 0
    - Transitions are cleaner and more decisive than filtered probabilities

---

## Plot Type 3: Regime Classification

Colors each observation by its dominant regime (the regime with the highest posterior probability), creating a clear segmentation of the return series.

### Basic Usage

```python
# Regime classification
fig = result.plot("regime-classify")
```

??? example "Expected Output"
    The chart displays:

    - **Scatter plot**: Each return colored by its dominant regime
    - **Blue dots**: Observations classified as low-volatility regime
    - **Red dots**: Observations classified as high-volatility regime
    - The classification creates a clear visual separation
    - High-volatility observations tend to have larger absolute returns
    - Regime switches appear as transitions between dot colors

### Full Customization

```python
fig = result.plot(
    "regime-classify",
    # Classification
    regime_colors=["#2E86C1", "#E74C3C", "#27AE60"],   # Up to K regimes
    regime_labels=["Low Vol", "High Vol", "Crisis"],
    marker_size=15,
    marker_alpha=0.7,
    # Conditional volatility overlay
    show_volatility=True,
    vol_color="#7F8C8D",
    vol_linewidth=1.0,
    vol_alpha=0.5,
    # Layout
    title="Regime Classification -- MS-GARCH(1,1)",
    figsize=(14, 6),
    start_date="2006-01-01",
    ylabel="Log Returns",
    show_legend=True,
    legend_loc="upper left",
)
```

??? example "Expected Output"
    The classification chart shows:

    - Blue dots during calm market periods (small returns)
    - Red dots during volatile periods (large positive and negative returns)
    - Optional grey volatility line overlaid showing conditional $\sigma_t$
    - Clear correspondence between regime color and volatility magnitude
    - Legend identifying each regime

---

## Plot Type 4: Transition Matrix Heatmap

Visualizes the estimated transition probability matrix $P$ as a heatmap, providing insight into regime persistence and switching dynamics.

### Mathematical Background

The transition matrix $P$ has elements:

$$p_{ij} = \Pr(S_{t+1} = j \mid S_t = i)$$

High diagonal elements indicate persistent regimes (the regime tends to stay once entered). Off-diagonal elements indicate switching probabilities. Expected regime duration is:

$$E[D_j] = \frac{1}{1 - p_{jj}}$$

### Basic Usage

```python
# Transition matrix heatmap
fig = result.plot("transition-matrix")
```

??? example "Expected Output"
    The chart displays:

    - **Heatmap**: $K \times K$ matrix with color intensity proportional to probability
    - **Cell values**: Numeric probabilities displayed in each cell
    - **Diagonal**: Typically high values (e.g., 0.97, 0.93) indicating persistence
    - **Off-diagonal**: Small values (e.g., 0.03, 0.07) indicating rare switching
    - Color scale: darker = higher probability

### Full Customization

```python
fig = result.plot(
    "transition-matrix",
    # Heatmap
    cmap="YlOrRd",                          # Color map
    annot=True,                             # Show values in cells
    fmt=".4f",                              # Number format
    vmin=0.0,
    vmax=1.0,
    # Cell labels
    cell_fontsize=14,
    cell_fontweight="bold",
    # Axis labels
    regime_labels=["Low Vol", "High Vol"],
    xlabel="To Regime",
    ylabel="From Regime",
    # Duration annotation
    show_duration=True,                     # Show expected duration
    # Layout
    title="Transition Probability Matrix",
    figsize=(8, 6),
)
```

??? example "Expected Output"
    The heatmap shows:

    - A $2 \times 2$ matrix with warm colors
    - Diagonal cells in dark orange/red: $p_{11} = 0.9754$, $p_{22} = 0.9312$
    - Off-diagonal cells in light yellow: $p_{12} = 0.0246$, $p_{21} = 0.0688$
    - Text annotation below: "Expected durations: Low Vol = 40.7 days, High Vol = 14.5 days"
    - Color bar on the right showing the probability scale

---

## Plot Type 5: Regime Duration Over Time

Displays the duration (in periods) of each regime episode over time, providing insight into how long regimes persist and whether duration patterns change.

### Basic Usage

```python
# Regime duration
fig = result.plot("regime-duration")
```

??? example "Expected Output"
    The chart displays:

    - **Bar chart**: Each bar represents one regime episode
    - **Bar height**: Duration in trading days
    - **Bar color**: Regime identity (blue for calm, red for volatile)
    - **X-axis**: Time (start date of each episode)
    - Long blue bars during calm periods, shorter red bars during crises
    - Pattern reveals whether regime dynamics change over time

### Full Customization

```python
fig = result.plot(
    "regime-duration",
    # Bar styling
    regime_colors=["#2E86C1", "#E74C3C"],
    regime_labels=["Low Vol", "High Vol"],
    bar_alpha=0.8,
    bar_width=5,                            # Bar width in days
    edgecolor="#2C3E50",
    # Statistics
    show_mean_duration=True,                # Horizontal lines at mean
    mean_style="--",
    mean_linewidth=1.5,
    # Layout
    title="Regime Duration Analysis -- MS-GARCH(1,1)",
    figsize=(14, 6),
    ylabel="Duration (trading days)",
    show_legend=True,
)
```

??? example "Expected Output"
    The duration chart shows:

    - Blue bars for calm regime episodes (typically 30--100+ days)
    - Red bars for volatile episodes (typically 10--30 days)
    - Horizontal dashed lines at mean duration for each regime
    - The asymmetry is clear: calm regimes last much longer than crisis regimes
    - Some crisis episodes are very short (1--5 days), indicating brief spikes

---

## Plot Type 6: Distribution Comparison by Regime

Compares the empirical distribution of returns across regimes, revealing the distinct statistical properties of each regime.

### Basic Usage

```python
# Distribution comparison
fig = result.plot("regime-distribution")
```

??? example "Expected Output"
    The chart displays:

    - **Overlaid histograms/KDEs**: One distribution per regime
    - **Blue curve**: Low-volatility regime (narrow, centered near zero)
    - **Red curve**: High-volatility regime (wide, heavier tails)
    - The visual difference in spread directly reflects the volatility difference
    - Summary statistics shown for each regime

### Full Customization

```python
fig = result.plot(
    "regime-distribution",
    # Plot type
    kind="kde",                             # "hist", "kde", or "both"
    # KDE/histogram options
    bins=50,                                # Number of histogram bins
    kde_bandwidth=0.5,                      # KDE bandwidth multiplier
    # Styling
    regime_colors=["#2E86C1", "#E74C3C"],
    regime_labels=["Low Vol", "High Vol"],
    fill_alpha=0.3,
    line_alpha=0.9,
    linewidth=2.0,
    # Normal overlay
    show_normal=True,                       # Overlay normal distribution
    normal_color="#7F8C8D",
    normal_style="--",
    # Statistics
    show_stats=True,                        # Show mean, std, skew, kurt
    stats_position="upper right",
    # Layout
    title="Return Distribution by Regime",
    figsize=(10, 6),
    xlabel="Log Returns",
    ylabel="Density",
    show_legend=True,
)
```

??? example "Expected Output"
    The distribution comparison shows:

    - Blue KDE curve: narrow with $\mu \approx 0.04\%$, $\sigma \approx 0.8\%$
    - Red KDE curve: wide with $\mu \approx -0.02\%$, $\sigma \approx 2.1\%$
    - Dashed grey normal distribution for reference
    - Stat box showing moments for each regime
    - The high-volatility regime has heavier tails and a slightly negative mean
    - Clear visual evidence of regime-dependent distributions

---

## Complete Regime Visualization Workflow

```python
import numpy as np
from archbox.regime import MarkovSwitchingGARCH
from archbox.datasets import load_returns

# Load data
returns = load_returns("sp500")

# Fit MS-GARCH model
model = MarkovSwitchingGARCH(
    returns, k_regimes=2, p=1, q=1, dist="student-t"
)
result = model.fit()

# --- Plot 1: Filtered probabilities with shaded regions ---
fig1 = result.plot(
    "regimes",
    regime_colors=["#2E86C1", "#E74C3C"],
    regime_labels=["Low Vol", "High Vol"],
    annotate_events={
        "2008-09-15": "Lehman Brothers",
        "2020-03-12": "COVID Crash",
    },
    title="Filtered Regime Probabilities",
)
fig1.savefig("regime_filtered.pdf", bbox_inches="tight")

# --- Plot 2: Smoothed probabilities ---
fig2 = result.plot(
    "smoothed",
    regime=1,
    fill=True,
    title="Smoothed Probability of High-Vol Regime",
)
fig2.savefig("regime_smoothed.pdf", bbox_inches="tight")

# --- Plot 3: Regime classification ---
fig3 = result.plot(
    "regime-classify",
    show_volatility=True,
    title="Regime Classification",
)
fig3.savefig("regime_classify.pdf", bbox_inches="tight")

# --- Plot 4: Transition matrix ---
fig4 = result.plot(
    "transition-matrix",
    show_duration=True,
    regime_labels=["Low Vol", "High Vol"],
    title="Transition Matrix",
)
fig4.savefig("regime_transition.pdf", bbox_inches="tight")

# --- Plot 5: Regime duration ---
fig5 = result.plot(
    "regime-duration",
    show_mean_duration=True,
    title="Regime Duration Analysis",
)
fig5.savefig("regime_duration.pdf", bbox_inches="tight")

# --- Plot 6: Distribution by regime ---
fig6 = result.plot(
    "regime-distribution",
    kind="both",
    show_stats=True,
    title="Return Distribution by Regime",
)
fig6.savefig("regime_distribution.pdf", bbox_inches="tight")

# Summary
print(f"Transition matrix:\n{result.transition_matrix}")
print(f"\nRegime 0 (Low Vol):  μ={result.regime_means[0]:.4f}, "
      f"σ={result.regime_volatilities[0]:.4f}")
print(f"Regime 1 (High Vol): μ={result.regime_means[1]:.4f}, "
      f"σ={result.regime_volatilities[1]:.4f}")
print(f"\nExpected durations: {result.expected_durations}")
```

---

## Common Customization Options

All regime plots accept these shared parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `backend` | `str` | `"matplotlib"` | `"matplotlib"` or `"plotly"` |
| `theme` | `str` | `"archbox"` | Plot theme name |
| `figsize` | `tuple` | `(14, 6)` | Figure size in inches |
| `title` | `str` | Auto | Plot title |
| `ylabel` | `str` | Auto | Y-axis label |
| `start_date` | `str` | `None` | Start date filter (`"YYYY-MM-DD"`) |
| `end_date` | `str` | `None` | End date filter |
| `regime_colors` | `list` | Auto | Colors for each regime |
| `regime_labels` | `list` | Auto | Labels for each regime |
| `grid` | `bool` | `True` | Show grid lines |
| `dpi` | `int` | `150` | Resolution for raster export |

---

## Export

All regime plots return a figure object that can be saved in multiple formats:

=== "Matplotlib"

    ```python
    fig = result.plot("regimes")

    # High-resolution PNG
    fig.savefig("regimes.png", dpi=300, bbox_inches="tight")

    # PDF for LaTeX
    fig.savefig("regimes.pdf", bbox_inches="tight")

    # SVG for web
    fig.savefig("regimes.svg", bbox_inches="tight")
    ```

=== "Plotly"

    ```python
    fig = result.plot("regimes", backend="plotly")

    # Interactive HTML
    fig.write_html("regimes.html", include_plotlyjs="cdn")

    # Static export (requires kaleido)
    fig.write_image("regimes.png", scale=2, width=1200, height=600)
    ```

!!! tip "Financial Crisis Analysis"
    Regime plots are particularly effective for identifying and communicating structural breaks in volatility. Combine with event annotations to create compelling visualizations of how markets transition between calm and crisis states.

---

## See Also

- [Visualization Overview](index.md) -- backends, themes, and export formats
- [Volatility Plots](volatility-plots.md) -- conditional volatility charts
- [Risk Plots](risk-plots.md) -- VaR and ES charts
- [Diagnostic Plots](diagnostic-plots.md) -- model diagnostics
- [MS-GARCH User Guide](../user-guide/regime-switching/ms-garch.md) -- model estimation details
- [Hamilton Filter](../user-guide/regime-switching/hamilton-filter.md) -- filtering algorithm
