---
title: "Risk Plots"
description: "Risk visualization: VaR overlay, exceedances, VaR fan chart, ES vs VaR comparison, and traffic light backtest"
---

# Risk Plots

!!! abstract "Key Takeaway"
    ArchBox provides five risk visualizations: returns with VaR overlay, exceedance highlighting, multi-level VaR fan charts, ES vs VaR comparison, and Basel traffic light backtest charts. These plots are essential for communicating risk measures and validating models.

---

## Overview

After computing Value-at-Risk (VaR) and Expected Shortfall (ES), the results can be visualized to assess model adequacy and communicate risk:

```python
result.plot("var")                  # Returns with VaR overlay
result.plot("var-exceedances")      # Exceedances highlighted
result.plot("var-fan")              # Multiple confidence levels
result.plot("var-es")               # ES vs VaR comparison
result.plot("var-backtest")         # Traffic light backtest
```

---

## Plot Type 1: Returns with VaR Overlay

Displays the return series with the estimated VaR line, providing a visual sense of how often returns breach the risk threshold.

### Mathematical Context

The parametric VaR at confidence level $\alpha$ is:

$$\text{VaR}_{\alpha,t} = -(\mu_t + q_\alpha \cdot \sigma_t)$$

where $q_\alpha$ is the quantil of the standardized distribution and $\sigma_t$ is the conditional volatility.

### Basic Usage

```python
from archbox.models import GARCH
from archbox.risk import ValueAtRisk
from archbox.datasets import load_returns

returns = load_returns("sp500")

# Fit GARCH model
model = GARCH(returns, p=1, q=1, dist="student-t")
result = model.fit()

# Compute VaR
var = ValueAtRisk(result, alpha=0.05)
var_series = var.compute()

# Plot returns with VaR overlay
fig = var.plot("var")
```

??? example "Expected Output"
    The chart displays:

    - **Grey bars/line**: Daily log returns
    - **Red line**: 5% VaR (negative values, representing the loss threshold)
    - The VaR line moves with the conditional volatility -- wider during crises, tighter during calm periods
    - Returns below the VaR line are violations (expected ~5% of observations)
    - X-axis: dates; Y-axis: return values

### Full Customization

```python
fig = var.plot(
    "var",
    # VaR line
    var_color="#E74C3C",                # VaR line color
    var_linewidth=1.5,                  # VaR line width
    var_linestyle="-",                  # Line style
    var_label="VaR 5%",                 # Legend label
    # Returns
    return_color="#AEB6BF",             # Return bar/line color
    return_alpha=0.6,                   # Return transparency
    return_style="bar",                 # "bar" or "line"
    # Layout
    title="S&P 500 Returns with 5% VaR -- GARCH(1,1)-t",
    figsize=(14, 6),
    start_date="2018-01-01",
    ylabel="Log Returns",
    # Grid
    grid=True,
    grid_alpha=0.3,
)

fig.savefig("var_overlay.png", dpi=300, bbox_inches="tight")
```

??? example "Expected Output"
    The customized chart shows:

    - Grey vertical bars for daily returns with 60% transparency
    - Bold red VaR line tracking the lower tail boundary
    - The VaR line widens significantly during March 2020 (COVID crash)
    - Clean grid with subtle lines
    - Legend identifying the VaR level

---

## Plot Type 2: Exceedances (VaR Violations)

Highlights returns that breach the VaR threshold with colored markers. This is the key visual for backtesting -- too many exceedances indicate model underestimation of risk.

### Basic Usage

```python
# Exceedances plot
fig = var.plot("var-exceedances")
```

??? example "Expected Output"
    The chart displays:

    - **Grey line**: Daily returns
    - **Red line**: VaR threshold
    - **Red dots**: Returns that violate VaR (i.e., $r_t < -\text{VaR}_{\alpha,t}$)
    - Expected exceedance rate: $\alpha$ (e.g., 5% for VaR at 95% confidence)
    - Clusters of red dots indicate model failure during stress periods

### Full Customization

```python
fig = var.plot(
    "var-exceedances",
    # Exceedance markers
    exceedance_color="#E74C3C",         # Marker color
    exceedance_marker="o",              # Marker shape
    exceedance_size=30,                 # Marker size
    exceedance_alpha=0.8,              # Marker transparency
    # Non-exceedance returns
    return_color="#AEB6BF",
    return_alpha=0.4,
    # VaR line
    var_color="#C0392B",
    var_linewidth=1.2,
    # Statistics annotation
    show_stats=True,                    # Show exceedance count/rate
    stats_position="upper right",
    # Layout
    title="VaR Exceedances -- GARCH(1,1) Student-t",
    figsize=(14, 6),
    start_date="2015-01-01",
)
```

??? example "Expected Output"
    The chart shows:

    - Grey return series with low transparency
    - Dark red VaR line
    - Bright red circles at each violation point
    - A text box in the upper-right corner showing:
        - Total observations: 2,014
        - Exceedances: 98 (4.87%)
        - Expected: 5.00%
        - Ratio: 0.97 (close to 1.0 indicates good calibration)
    - Violation clusters visible during 2015 China crash, 2018 volatility spike, and 2020 COVID crash

---

## Plot Type 3: VaR Fan Chart (Multiple Confidence Levels)

Displays VaR at multiple confidence levels simultaneously, creating a layered view of the risk distribution.

### Basic Usage

```python
# Compute VaR at multiple levels
from archbox.risk import ValueAtRisk

var_multi = ValueAtRisk(result, alpha=[0.01, 0.025, 0.05, 0.10])
var_series = var_multi.compute()

# Fan chart
fig = var_multi.plot("var-fan")
```

??? example "Expected Output"
    The chart displays:

    - **Return series** in the center
    - **Graduated bands** below zero, each representing a VaR level:
        - Lightest band: VaR 10% (least extreme)
        - Medium band: VaR 5%
        - Darker band: VaR 2.5%
        - Darkest band: VaR 1% (most extreme)
    - The bands create a "fan" that widens during volatile periods
    - Returns penetrating deeper bands represent increasingly extreme events

### Full Customization

```python
fig = var_multi.plot(
    "var-fan",
    # Levels
    alphas=[0.01, 0.025, 0.05, 0.10],
    labels=["1%", "2.5%", "5%", "10%"],
    # Colors (graduated)
    palette="Reds",                     # Color palette
    # Or explicit colors:
    # colors=["#922B21", "#C0392B", "#E74C3C", "#F1948A"],
    band_alpha=0.3,                     # Band transparency
    # Returns
    return_color="#2C3E50",
    return_linewidth=0.8,
    # Layout
    title="VaR Fan Chart -- Multiple Confidence Levels",
    figsize=(14, 7),
    start_date="2019-01-01",
    ylabel="Log Returns / VaR",
    # Legend
    show_legend=True,
    legend_loc="lower left",
)
```

??? example "Expected Output"
    The fan chart shows:

    - A thin dark blue return line
    - Four graduated red bands below, widening during crises
    - The 1% VaR band (darkest red) is the outermost, rarely breached
    - The 10% VaR band (lightest) is closest to zero, more frequently breached
    - During March 2020, all bands expand dramatically
    - Legend shows the confidence level for each band

---

## Plot Type 4: ES vs VaR Comparison

Displays both VaR and Expected Shortfall on the same axes, highlighting the additional information ES provides about tail risk.

### Mathematical Context

Expected Shortfall (CVaR) is the expected loss conditional on exceeding VaR:

$$\text{ES}_\alpha = E[L \mid L > \text{VaR}_\alpha] = \frac{1}{1-\alpha} \int_\alpha^1 \text{VaR}_u \, du$$

ES is always more conservative than VaR: $\text{ES}_\alpha \geq \text{VaR}_\alpha$.

### Basic Usage

```python
from archbox.risk import ValueAtRisk, ExpectedShortfall

var = ValueAtRisk(result, alpha=0.05).compute()
es = ExpectedShortfall(result, alpha=0.05).compute()

# Comparative plot
from archbox.visualization import plot_var_es

fig = plot_var_es(returns, var, es)
```

??? example "Expected Output"
    The chart displays:

    - **Grey bars**: Daily returns
    - **Red line**: 5% VaR
    - **Dark red dashed line**: 5% ES (always below VaR)
    - **Shaded area**: Gap between VaR and ES, representing additional tail risk
    - ES captures the magnitude of extreme losses that VaR ignores
    - The gap widens during heavy-tailed regimes

### Full Customization

```python
fig = plot_var_es(
    returns, var, es,
    # VaR styling
    var_color="#E74C3C",
    var_linewidth=1.5,
    var_linestyle="-",
    var_label="VaR 5%",
    # ES styling
    es_color="#922B21",
    es_linewidth=1.5,
    es_linestyle="--",
    es_label="ES 5%",
    # Gap shading
    shade_gap=True,                     # Shade area between VaR and ES
    gap_color="#F5B7B1",
    gap_alpha=0.3,
    # Returns
    return_color="#AEB6BF",
    return_alpha=0.5,
    # Layout
    title="VaR vs Expected Shortfall -- GARCH(1,1)-t",
    figsize=(14, 6),
    start_date="2018-01-01",
    ylabel="Returns / Risk Measures",
)
```

??? example "Expected Output"
    The comparison chart shows:

    - Returns as faded grey bars
    - Solid red VaR line
    - Dashed dark red ES line, consistently below VaR
    - Light pink shading between the two lines
    - The gap between VaR and ES is larger during heavy-tailed periods
    - During calm markets, VaR and ES are closer together
    - During crises, the gap widens substantially, showing ES captures more tail risk

---

## Plot Type 5: Traffic Light Backtest

Visualizes the Basel II/III traffic light system for VaR backtesting. The number of exceedances in a 250-day window determines the zone:

| Zone | Exceedances (at 99% VaR) | Color | Interpretation |
|------|--------------------------|-------|----------------|
| **Green** | 0--4 | :material-circle:{ style="color: #27AE60" } | Model adequate |
| **Yellow** | 5--9 | :material-circle:{ style="color: #F39C12" } | Potential issues |
| **Red** | 10+ | :material-circle:{ style="color: #E74C3C" } | Model inadequate |

### Basic Usage

```python
from archbox.risk import backtest_var

# Run backtest
bt = backtest_var(returns, var_series, window=250)

# Traffic light plot
fig = bt.plot("traffic-light")
```

??? example "Expected Output"
    The chart displays:

    - **Top panel**: Returns with VaR line and exceedance markers
    - **Bottom panel**: Rolling exceedance count over a 250-day window
    - **Color zones**: Green (0--4), Yellow (5--9), Red (10+) background bands
    - The rolling count line moves through the zones over time
    - A horizontal dashed line at the expected count ($250 \times 0.01 = 2.5$)

### Full Customization

```python
fig = bt.plot(
    "traffic-light",
    # Window
    window=250,                         # Rolling window size
    alpha=0.01,                         # VaR confidence level
    # Zone colors
    green_color="#27AE60",
    yellow_color="#F39C12",
    red_color="#E74C3C",
    zone_alpha=0.15,                    # Background zone transparency
    # Exceedance line
    count_color="#2C3E50",
    count_linewidth=1.5,
    # Expected line
    show_expected=True,
    expected_color="#7F8C8D",
    expected_style="--",
    # Layout
    title="Basel Traffic Light Backtest -- VaR 99%",
    figsize=(14, 8),
    # Panel ratio
    height_ratios=[2, 1],              # Top:bottom panel ratio
)
```

??? example "Expected Output"
    The two-panel chart shows:

    - **Top panel**:
        - Daily returns as a grey line
        - 1% VaR as a red line
        - Red dots at each exceedance
    - **Bottom panel**:
        - Rolling 250-day exceedance count as a dark line
        - Green background zone (0--4 exceedances)
        - Yellow background zone (5--9 exceedances)
        - Red background zone (10+ exceedances)
        - Horizontal dashed line at expected count (2.5)
        - The line stays mostly in the green zone for a well-calibrated model
        - Potential spikes into yellow during crisis periods

---

## Complete Risk Visualization Workflow

```python
import numpy as np
from archbox.models import GARCH
from archbox.risk import ValueAtRisk, ExpectedShortfall, backtest_var
from archbox.visualization import plot_var_es
from archbox.datasets import load_returns

# Data and model
returns = load_returns("sp500")
model = GARCH(returns, p=1, q=1, dist="student-t")
result = model.fit()

# --- Plot 1: VaR overlay ---
var = ValueAtRisk(result, alpha=0.05)
var_series = var.compute()
fig1 = var.plot("var", title="S&P 500 -- VaR 5%")
fig1.savefig("risk_var_overlay.pdf", bbox_inches="tight")

# --- Plot 2: Exceedances ---
fig2 = var.plot(
    "var-exceedances",
    show_stats=True,
    title="VaR Exceedances",
)
fig2.savefig("risk_exceedances.pdf", bbox_inches="tight")

# --- Plot 3: Multi-level fan chart ---
var_multi = ValueAtRisk(result, alpha=[0.01, 0.025, 0.05, 0.10])
fig3 = var_multi.plot("var-fan", title="VaR Fan Chart")
fig3.savefig("risk_fan.pdf", bbox_inches="tight")

# --- Plot 4: ES vs VaR ---
es = ExpectedShortfall(result, alpha=0.05)
es_series = es.compute()
fig4 = plot_var_es(
    returns, var_series, es_series,
    title="VaR vs Expected Shortfall",
    shade_gap=True,
)
fig4.savefig("risk_var_es.pdf", bbox_inches="tight")

# --- Plot 5: Traffic light backtest ---
var_99 = ValueAtRisk(result, alpha=0.01).compute()
bt = backtest_var(returns, var_99, window=250)
fig5 = bt.plot("traffic-light", title="Basel Traffic Light Backtest")
fig5.savefig("risk_backtest.pdf", bbox_inches="tight")

print(f"Backtest summary:")
print(f"  Exceedances: {bt.n_exceedances} / {bt.n_observations}")
print(f"  Rate: {bt.exceedance_rate:.2%} (expected: 1.00%)")
print(f"  Zone: {bt.zone}")
```

---

## Common Customization Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `backend` | `str` | `"matplotlib"` | `"matplotlib"` or `"plotly"` |
| `theme` | `str` | `"archbox"` | Plot theme |
| `figsize` | `tuple` | `(14, 6)` | Figure size in inches |
| `title` | `str` | Auto | Plot title |
| `ylabel` | `str` | Auto | Y-axis label |
| `start_date` | `str` | `None` | Start date filter |
| `end_date` | `str` | `None` | End date filter |
| `alpha` | `float/list` | `0.05` | VaR confidence level(s) |
| `grid` | `bool` | `True` | Show grid |
| `dpi` | `int` | `150` | Export resolution |

---

## See Also

- [Visualization Overview](index.md) -- backends, themes, and export formats
- [Volatility Plots](volatility-plots.md) -- conditional volatility charts
- [Correlation Plots](correlation-plots.md) -- multivariate correlation visualization
- [VaR User Guide](../user-guide/risk/var.md) -- VaR computation details
- [Expected Shortfall](../user-guide/risk/es.md) -- ES computation
- [Backtesting](../user-guide/risk/backtesting.md) -- formal backtest procedures
- [Risk Theory](../theory/risk-theory.md) -- mathematical foundations
