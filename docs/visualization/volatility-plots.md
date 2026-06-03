---
title: "Volatility Plots"
description: "Conditional volatility visualization: returns with bands, isolated volatility, fan charts, and model comparison plots"
---

# Volatility Plots

!!! abstract "Key Takeaway"
    ArchBox provides four types of volatility visualizations: returns with $\pm 2\sigma$ bands, isolated conditional volatility, fan charts for forecast intervals, and multi-model comparison overlays. All plots support matplotlib and plotly backends with full customization.

---

## Overview

After fitting any GARCH-family model, the estimated conditional volatility $\sigma_t$ can be visualized in multiple ways. The primary entry point is the `.plot()` method on the fitted result object:

```python
result.plot("volatility")           # Default: isolated volatility
result.plot("volatility-bands")     # Returns with ±2σ bands
result.plot("volatility-fan")       # Fan chart (forecast)
result.plot("volatility-compare")   # Multi-model overlay
```

---

## Plot Type 1: Returns with Volatility Bands

Displays the return series with $\pm k\sigma_t$ bands overlaid, where $k$ defaults to 2 (approximately 95% of observations under normality).

### Mathematical Background

The bands represent the conditional confidence interval:

$$r_t \in [\mu_t - k\sigma_t, \; \mu_t + k\sigma_t]$$

where $\mu_t$ is the conditional mean and $\sigma_t$ is the conditional standard deviation from the GARCH model. Points outside the bands indicate extreme returns relative to the model's expectations.

### Basic Usage

```python
from archbox.models import GARCH
from archbox.datasets import load_returns

returns = load_returns("sp500")
model = GARCH(returns, p=1, q=1, dist="student-t")
result = model.fit()

# Returns with ±2σ bands
fig = result.plot("volatility-bands")
```

??? example "Expected Output"
    The chart displays:

    - **Grey area**: $\pm 2\sigma_t$ confidence bands centered on zero (or the conditional mean)
    - **Black line**: Daily log returns
    - **Red dots** (optional): Returns that breach the bands (exceedances)
    - Bands widen during volatile periods (e.g., financial crises) and narrow during calm markets
    - The x-axis shows the date range; y-axis shows return values

### Full Customization

```python
fig = result.plot(
    "volatility-bands",
    # Band configuration
    k_sigma=2,                          # Band width (default: 2)
    show_exceedances=True,              # Highlight breaches
    exceedance_color="#E74C3C",         # Red dots for breaches
    # Styling
    band_color="#D7BDE2",               # Band fill color
    band_alpha=0.3,                     # Band transparency
    return_color="#2C3E50",             # Return line color
    return_alpha=0.7,                   # Return line transparency
    # Layout
    title="S&P 500 Returns with GARCH(1,1) Bands",
    figsize=(14, 6),
    start_date="2018-01-01",
    end_date="2023-12-31",
    # Annotations
    annotate_events={
        "2020-03-12": "COVID Crash",
        "2022-06-13": "Bear Market",
    },
    # Grid and axes
    grid=True,
    grid_alpha=0.3,
    ylabel="Log Returns",
)

# Export
fig.savefig("returns_bands.png", dpi=300, bbox_inches="tight")
```

??? example "Expected Output"
    The customized chart shows:

    - Light purple $\pm 2\sigma_t$ bands with 30% transparency
    - Dark blue-grey return line
    - Red dots marking exceedances (returns outside the bands)
    - Vertical dashed annotations at "COVID Crash" and "Bear Market" dates
    - Date range restricted to 2018--2023
    - Clean grid with subtle lines

---

## Plot Type 2: Conditional Volatility (Isolated)

Displays only the conditional volatility $\sigma_t$ as a time series. This is the most common plot for analyzing volatility dynamics.

### Basic Usage

```python
# Isolated conditional volatility
fig = result.plot("volatility")
```

??? example "Expected Output"
    The chart displays:

    - **Solid line**: Conditional volatility $\sigma_t$ over time
    - **Y-axis**: Annualized volatility (%) by default, or raw $\sigma_t$ with `annualize=False`
    - Peaks correspond to periods of market stress
    - The unconditional volatility $\bar{\sigma} = \sqrt{\omega / (1 - \alpha - \beta)}$ may appear as a horizontal dashed line

### Full Customization

```python
fig = result.plot(
    "volatility",
    # Scale
    annualize=True,                     # Annualize (×√252), default True
    log_scale=False,                    # Log y-axis
    # Styling
    color="#6C3483",                    # Line color
    linewidth=1.5,                      # Line width
    fill=True,                          # Fill area under curve
    fill_alpha=0.15,                    # Fill transparency
    # Reference lines
    show_unconditional=True,            # Horizontal line at σ̄
    unconditional_style="--",           # Dashed line
    quantiles=[0.05, 0.95],             # Show 5th/95th percentile bands
    # Layout
    title="Conditional Volatility -- GARCH(1,1) Student-t",
    figsize=(12, 5),
    start_date="2015-01-01",
    ylabel="Annualized Volatility (%)",
)
```

??? example "Expected Output"
    The chart shows:

    - Purple solid line for $\sigma_t$ with light purple fill underneath
    - Horizontal dashed line at unconditional volatility level (~15--20% for equity indices)
    - Faint bands at 5th and 95th percentiles of the volatility distribution
    - Volatility clustering is clearly visible: periods of high volatility persist before mean-reverting

---

## Plot Type 3: Fan Chart (Forecast Intervals)

Displays multi-step-ahead volatility forecasts with expanding confidence intervals, creating a "fan" shape that reflects increasing uncertainty over the forecast horizon.

### Mathematical Background

For an $h$-step-ahead forecast, the GARCH model produces:

$$\hat{\sigma}_{t+h|t}^2 = \omega + (\alpha + \beta) \hat{\sigma}_{t+h-1|t}^2$$

The fan chart shows forecast intervals at multiple confidence levels (e.g., 50%, 75%, 90%, 95%), with wider intervals for longer horizons.

### Basic Usage

```python
# Generate forecast
forecast = result.forecast(horizon=30)

# Fan chart
fig = forecast.plot("fan")
```

??? example "Expected Output"
    The chart displays:

    - **Center line**: Point forecast of $\sigma_{t+h}$
    - **Graduated bands**: Nested confidence intervals (darker = narrower = higher confidence)
    - **X-axis**: Forecast horizon (days ahead)
    - Bands expand with horizon, reflecting increasing uncertainty
    - For stationary GARCH, the forecast converges to unconditional volatility as $h \to \infty$

### Full Customization

```python
fig = forecast.plot(
    "fan",
    # Intervals
    levels=[0.50, 0.75, 0.90, 0.95],   # Confidence levels
    palette="Purples",                   # Color palette for bands
    # Point forecast
    center_color="#6C3483",             # Center line color
    center_linewidth=2.0,              # Center line width
    # Historical context
    show_history=True,                  # Show last N obs of σ_t
    history_periods=60,                 # Number of historical obs
    history_color="#AEB6BF",            # Historical line color
    # Layout
    title="30-Day Volatility Forecast -- GARCH(1,1)",
    figsize=(12, 6),
    ylabel="Annualized Volatility (%)",
    # Annotations
    show_convergence=True,              # Mark unconditional level
)
```

??? example "Expected Output"
    The chart shows:

    - 60 days of historical volatility in grey on the left
    - A vertical dashed line marking the forecast origin
    - 30-day forecast with 4 nested bands (50%, 75%, 90%, 95%) in graduated purple shades
    - The center forecast line converging toward the unconditional volatility
    - A horizontal dashed line at the unconditional level $\bar{\sigma}$

---

## Plot Type 4: Multi-Model Comparison

Overlays conditional volatility from multiple models on the same axes for visual comparison.

### Basic Usage

```python
from archbox.models import GARCH, EGARCH, GJR

# Fit multiple models
garch = GARCH(returns, p=1, q=1).fit()
egarch = EGARCH(returns, p=1, q=1).fit()
gjr = GJR(returns, p=1, q=1).fit()

# Compare volatilities
from archbox.visualization import compare_volatility

fig = compare_volatility(
    models=[garch, egarch, gjr],
    labels=["GARCH(1,1)", "EGARCH(1,1)", "GJR-GARCH(1,1)"],
)
```

??? example "Expected Output"
    The chart displays:

    - Three overlaid volatility lines, each in a distinct color
    - A legend identifying each model
    - All models track the same broad pattern but differ in magnitude during stress periods
    - EGARCH and GJR-GARCH typically show higher peaks due to leverage effects
    - The y-axis shows annualized volatility (%)

### Full Customization

```python
fig = compare_volatility(
    models=[garch, egarch, gjr],
    labels=["GARCH(1,1)", "EGARCH(1,1)", "GJR-GARCH(1,1)"],
    # Styling
    colors=["#6C3483", "#E74C3C", "#2E86C1"],
    linewidths=[1.5, 1.2, 1.2],
    linestyles=["-", "--", "-."],
    # Reference
    show_unconditional=True,            # Show each model's σ̄
    # Layout
    title="Model Comparison -- Conditional Volatility",
    figsize=(14, 6),
    start_date="2019-01-01",
    end_date="2023-12-31",
    ylabel="Annualized Volatility (%)",
    legend_loc="upper left",
    # Information criteria inset
    show_ic_table=True,                 # Inset table with AIC/BIC
)
```

??? example "Expected Output"
    The comparison chart shows:

    - Three volatility series in purple (solid), red (dashed), and blue (dash-dot)
    - Horizontal dashed lines at each model's unconditional volatility
    - A small inset table in the upper-right corner showing AIC and BIC for each model
    - The legend in the upper-left corner
    - Divergences between models are most visible during high-volatility regimes

---

## Common Customization Options

All volatility plots accept these shared parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `backend` | `str` | `"matplotlib"` | `"matplotlib"` or `"plotly"` |
| `theme` | `str` | `"archbox"` | Plot theme name |
| `figsize` | `tuple` | `(12, 6)` | Figure size in inches |
| `title` | `str` | Auto | Plot title |
| `ylabel` | `str` | Auto | Y-axis label |
| `start_date` | `str` | `None` | Start date filter (`"YYYY-MM-DD"`) |
| `end_date` | `str` | `None` | End date filter |
| `annualize` | `bool` | `True` | Annualize volatility ($\times \sqrt{252}$) |
| `grid` | `bool` | `True` | Show grid lines |
| `grid_alpha` | `float` | `0.3` | Grid transparency |
| `dpi` | `int` | `150` | Resolution for raster export |

---

## Export

All volatility plots return a figure object that can be saved in multiple formats:

=== "Matplotlib"

    ```python
    fig = result.plot("volatility")

    # High-resolution PNG
    fig.savefig("volatility.png", dpi=300, bbox_inches="tight")

    # Scalable vector graphic
    fig.savefig("volatility.svg", bbox_inches="tight")

    # PDF for LaTeX inclusion
    fig.savefig("volatility.pdf", bbox_inches="tight")
    ```

=== "Plotly"

    ```python
    fig = result.plot("volatility", backend="plotly")

    # Interactive HTML
    fig.write_html("volatility.html", include_plotlyjs="cdn")

    # Static image (requires kaleido)
    fig.write_image("volatility.png", scale=2, width=1200, height=600)
    fig.write_image("volatility.svg", width=1200, height=600)
    fig.write_image("volatility.pdf", width=1200, height=600)
    ```

!!! tip "LaTeX Integration"
    For academic papers, export as PDF and include with `\includegraphics`:
    ```latex
    \begin{figure}[htbp]
        \centering
        \includegraphics[width=\textwidth]{volatility.pdf}
        \caption{Conditional volatility from GARCH(1,1) with Student-$t$ innovations.}
        \label{fig:volatility}
    \end{figure}
    ```

---

## See Also

- [Visualization Overview](index.md) -- backends, themes, and export formats
- [Correlation Plots](correlation-plots.md) -- multivariate correlation visualization
- [Risk Plots](risk-plots.md) -- VaR and ES charts
- [GARCH User Guide](../user-guide/garch/garch.md) -- model estimation details
- [Forecast Evaluation](../diagnostics/forecast-evaluation.md) -- forecast accuracy assessment
