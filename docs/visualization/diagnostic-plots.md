---
title: "Diagnostic Plots"
description: "Model diagnostic visualization: ACF/PACF, QQ-plots, residual histograms, news impact curves, PIT histograms, and 4-panel diagnostic grids"
---

# Diagnostic Plots

!!! abstract "Key Takeaway"
    ArchBox provides seven diagnostic visualizations plus a combined 4-panel grid: ACF/PACF of standardized residuals, ACF/PACF of squared residuals, QQ-plots, residual histograms with fitted distributions, news impact curve comparisons, standardized residual time series, and PIT histograms. These plots are essential for validating model adequacy.

---

## Overview

After fitting any GARCH-family model, the standardized residuals $z_t = r_t / \sigma_t$ should behave as i.i.d. draws from the assumed distribution. Diagnostic plots provide visual evidence of model adequacy:

```python
result.plot("diagnostics")          # 4-panel diagnostic grid
result.plot("acf")                  # ACF of standardized residuals
result.plot("acf-squared")         # ACF of squared residuals
result.plot("qq")                   # QQ-plot
result.plot("histogram")           # Histogram with fitted distribution
result.plot("residuals")           # Standardized residuals over time
result.plot("news-impact")         # News impact curve
result.plot("pit")                 # PIT histogram
```

---

## Plot Type 1: 4-Panel Diagnostic Grid

The most common diagnostic visualization: four key plots arranged in a $2 \times 2$ grid for rapid model assessment.

### Basic Usage

```python
from archbox.models import GARCH
from archbox.datasets import load_returns

returns = load_returns("sp500")
model = GARCH(returns, p=1, q=1, dist="student-t")
result = model.fit()

# 4-panel diagnostic grid
fig = result.plot("diagnostics")
```

??? example "Expected Output"
    The $2 \times 2$ grid displays:

    - **Top-left**: Standardized residuals $z_t$ over time -- should look like white noise
    - **Top-right**: ACF of squared residuals $z_t^2$ -- bars should fall within confidence bands
    - **Bottom-left**: QQ-plot against theoretical distribution -- points should follow the diagonal
    - **Bottom-right**: Histogram of $z_t$ with fitted distribution overlay

### Full Customization

```python
fig = result.plot(
    "diagnostics",
    # Panel selection (default: all four)
    panels=["residuals", "acf-squared", "qq", "histogram"],
    # Grid layout
    layout=(2, 2),                          # Rows × columns
    figsize=(14, 10),                       # Overall figure size
    # Shared options
    color="#6C3483",                        # Primary color
    confidence_color="#AEB6BF",            # Confidence band color
    confidence_alpha=0.2,                  # Band transparency
    # ACF options
    acf_lags=40,                           # Number of lags
    acf_alpha=0.05,                        # Significance level
    # QQ options
    qq_dist="student-t",                   # Reference distribution
    qq_marker_size=15,                     # Point size
    qq_line_color="#E74C3C",              # 45° line color
    # Histogram options
    hist_bins=50,                          # Number of bins
    hist_density=True,                     # Normalize to density
    # Layout
    title="Model Diagnostics -- GARCH(1,1) Student-t",
    tight_layout=True,
)

fig.savefig("diagnostics_grid.png", dpi=300, bbox_inches="tight")
```

??? example "Expected Output"
    The customized grid shows:

    - **Top-left**: Purple residual series with no visible patterns
    - **Top-right**: ACF bars mostly within grey confidence bands (no significant autocorrelation in $z_t^2$)
    - **Bottom-left**: QQ points closely following the red 45° line, with slight deviations in the tails
    - **Bottom-right**: Histogram with Student-$t$ density curve overlaid, matching well in the center and tails

!!! tip "Interpretation Guide"
    A well-specified model shows: (1) no patterns in residuals, (2) no significant ACF bars, (3) QQ points on the diagonal, (4) histogram matching the fitted distribution. Systematic deviations indicate model misspecification.

---

## Plot Type 2: ACF/PACF of Standardized Residuals

Displays the autocorrelation function (ACF) and partial autocorrelation function (PACF) of the standardized residuals $z_t$. Significant bars indicate remaining serial dependence in the mean.

### Mathematical Background

The sample autocorrelation at lag $k$ is:

$$\hat{\rho}(k) = \frac{\sum_{t=k+1}^{T}(z_t - \bar{z})(z_{t-k} - \bar{z})}{\sum_{t=1}^{T}(z_t - \bar{z})^2}$$

Under the null of no autocorrelation, $\hat{\rho}(k) \sim \mathcal{N}(0, 1/T)$, giving approximate 95% confidence bands at $\pm 1.96 / \sqrt{T}$.

### Basic Usage

```python
# ACF of standardized residuals
fig = result.plot("acf")
```

??? example "Expected Output"
    The chart displays:

    - **Vertical bars**: Sample autocorrelation at each lag
    - **Blue dashed lines**: 95% confidence bands ($\pm 1.96/\sqrt{T}$)
    - **X-axis**: Lag (1 to max_lag)
    - **Y-axis**: Autocorrelation coefficient
    - For a well-specified model, bars should fall within the bands
    - Significant bars at low lags suggest mean misspecification

### Full Customization

```python
fig = result.plot(
    "acf",
    # ACF options
    max_lags=40,                            # Number of lags
    alpha=0.05,                             # Confidence level
    show_pacf=True,                         # Show PACF alongside ACF
    # Styling
    bar_color="#6C3483",
    bar_width=0.3,
    confidence_color="#AEB6BF",
    confidence_alpha=0.2,
    zero_line=True,
    # Layout
    title="ACF/PACF of Standardized Residuals",
    figsize=(14, 5),
)
```

??? example "Expected Output"
    The side-by-side chart shows:

    - **Left panel**: ACF with purple bars, grey confidence bands
    - **Right panel**: PACF with purple bars, grey confidence bands
    - Most bars within bands, confirming no significant serial dependence
    - Any significant bars are flagged visually

---

## Plot Type 3: ACF/PACF of Squared Residuals

Displays the autocorrelation of $z_t^2$. This is the critical diagnostic for GARCH models -- significant bars indicate remaining ARCH effects (the model has not captured all conditional heteroskedasticity).

### Basic Usage

```python
# ACF of squared residuals
fig = result.plot("acf-squared")
```

??? example "Expected Output"
    The chart displays:

    - **Vertical bars**: Sample autocorrelation of $z_t^2$ at each lag
    - **Dashed lines**: 95% confidence bands
    - For a well-specified GARCH model, bars should be within bands
    - Significant bars indicate remaining volatility clustering not captured by the model

### Full Customization

```python
fig = result.plot(
    "acf-squared",
    max_lags=40,
    alpha=0.05,
    show_pacf=True,
    # Styling
    bar_color="#E74C3C",
    confidence_color="#AEB6BF",
    # Annotations
    show_ljung_box=True,                    # Overlay Ljung-Box p-values
    ljung_box_lags=[10, 20, 40],
    # Layout
    title="ACF of Squared Standardized Residuals",
    figsize=(14, 5),
)
```

??? example "Expected Output"
    The chart shows:

    - Red bars for $z_t^2$ autocorrelation
    - Grey confidence bands
    - Text annotation with Ljung-Box test results:
        - $Q(10) = 8.32$, $p = 0.597$
        - $Q(20) = 15.71$, $p = 0.734$
        - $Q(40) = 38.14$, $p = 0.556$
    - All p-values above 0.05 confirms no remaining ARCH effects

---

## Plot Type 4: QQ-Plot

Compares the empirical quantiles of the standardized residuals against the theoretical quantiles of the assumed distribution. Deviations from the 45° line indicate distributional misspecification.

### Mathematical Background

The QQ-plot compares ordered standardized residuals $z_{(i)}$ against theoretical quantiles:

$$q_i = F^{-1}\left(\frac{i - 0.5}{T}\right)$$

where $F^{-1}$ is the inverse CDF of the assumed distribution. If the model is correct, points should lie on the $y = x$ line.

### Basic Usage

```python
# QQ-plot against assumed distribution
fig = result.plot("qq")
```

??? example "Expected Output"
    The chart displays:

    - **Scatter points**: Each point is $(q_i, z_{(i)})$
    - **Red diagonal line**: The $y = x$ reference line
    - Points near the line indicate good fit
    - Points above the line in the right tail: heavier right tail than assumed
    - Points below the line in the left tail: heavier left tail than assumed

### Full Customization

```python
fig = result.plot(
    "qq",
    # Distribution
    dist="student-t",                       # "normal", "student-t", "ged", "skew-t"
    df=None,                                # Use estimated df (auto)
    # Styling
    marker_color="#6C3483",
    marker_size=15,
    marker_alpha=0.6,
    line_color="#E74C3C",
    line_linewidth=2.0,
    # Confidence envelope
    show_envelope=True,                     # Pointwise confidence band
    envelope_alpha=0.05,
    envelope_color="#D7BDE2",
    # Layout
    title="QQ-Plot -- Standardized Residuals vs Student-t",
    figsize=(8, 8),
    xlabel="Theoretical Quantiles",
    ylabel="Sample Quantiles",
)
```

??? example "Expected Output"
    The QQ-plot shows:

    - Purple scatter points closely following the red diagonal
    - Light purple confidence envelope around the diagonal
    - Near-perfect fit in the center (quantiles -2 to +2)
    - Slight deviations in extreme tails (expected with finite samples)
    - The Student-$t$ distribution captures the tail behavior much better than a normal QQ-plot would

!!! warning "Normal vs Heavy-Tailed"
    Always match the QQ-plot distribution to the one used in estimation. Using a normal QQ-plot for a Student-$t$ model will show apparent tail misfit that is actually captured by the model.

---

## Plot Type 5: Residual Histogram with Fitted Distribution

Overlays the fitted parametric distribution on the histogram of standardized residuals, providing a direct visual comparison of the empirical and theoretical densities.

### Basic Usage

```python
# Histogram with fitted distribution
fig = result.plot("histogram")
```

??? example "Expected Output"
    The chart displays:

    - **Histogram**: Normalized density of standardized residuals $z_t$
    - **Solid curve**: Fitted distribution density (e.g., Student-$t$ with estimated $\nu$)
    - **Dashed curve** (optional): Standard normal for comparison
    - The histogram should closely match the fitted distribution
    - Excess kurtosis is visible as heavier tails than the normal reference

### Full Customization

```python
fig = result.plot(
    "histogram",
    # Histogram
    bins=60,
    hist_color="#D7BDE2",
    hist_alpha=0.6,
    hist_edgecolor="#6C3483",
    density=True,
    # Fitted distribution
    fitted_color="#6C3483",
    fitted_linewidth=2.5,
    fitted_label="Student-t (ν={:.1f})".format(result.params["df"]),
    # Normal reference
    show_normal=True,
    normal_color="#7F8C8D",
    normal_style="--",
    normal_label="Normal",
    # Statistics
    show_stats=True,                        # Mean, std, skew, kurtosis
    stats_position="upper right",
    # Layout
    title="Distribution of Standardized Residuals",
    figsize=(10, 6),
    xlabel="Standardized Residuals",
    ylabel="Density",
)
```

??? example "Expected Output"
    The histogram shows:

    - Light purple bars forming a bell-shaped distribution
    - Solid purple Student-$t(\nu = 7.2)$ curve fitting the histogram closely
    - Dashed grey normal curve for comparison -- narrower tails than the data
    - Stats box: mean $\approx 0.00$, std $\approx 1.00$, skewness $\approx -0.15$, kurtosis $\approx 4.8$
    - The Student-$t$ captures the excess kurtosis that the normal misses

---

## Plot Type 6: News Impact Curve

Visualizes how past shocks $\varepsilon_{t-1}$ affect current conditional variance $\sigma_t^2$, comparing different GARCH-family models.

### Mathematical Background

The news impact curve (NIC) plots $\sigma_t^2$ as a function of $\varepsilon_{t-1}$, holding all other information constant:

- **GARCH**: $\text{NIC}(\varepsilon) = \omega + \alpha \varepsilon^2 + \beta \bar{\sigma}^2$ (symmetric)
- **EGARCH**: Asymmetric -- negative shocks have larger impact
- **GJR-GARCH**: $\text{NIC}(\varepsilon) = \omega + (\alpha + \gamma \cdot \mathbb{1}_{\varepsilon < 0}) \varepsilon^2 + \beta \bar{\sigma}^2$

### Basic Usage

```python
from archbox.visualization import plot_news_impact_comparison

# Fit multiple models
from archbox.models import GARCH, EGARCH, GJR

garch = GARCH(returns, p=1, q=1).fit()
egarch = EGARCH(returns, p=1, q=1).fit()
gjr = GJR(returns, p=1, q=1).fit()

# Comparative news impact curves
fig = plot_news_impact_comparison(
    models=[garch, egarch, gjr],
    labels=["GARCH(1,1)", "EGARCH(1,1)", "GJR-GARCH(1,1)"],
)
```

??? example "Expected Output"
    The chart displays:

    - **X-axis**: Shock $\varepsilon_{t-1}$ ranging from negative to positive
    - **Y-axis**: Conditional variance $\sigma_t^2$
    - **GARCH**: Symmetric U-shape (same response to positive and negative shocks)
    - **EGARCH**: Asymmetric -- steeper slope for negative shocks (leverage effect)
    - **GJR-GARCH**: Asymmetric -- steeper left branch due to $\gamma$ indicator
    - All curves are tangent at $\varepsilon = 0$

### Full Customization

```python
fig = plot_news_impact_comparison(
    models=[garch, egarch, gjr],
    labels=["GARCH", "EGARCH", "GJR"],
    # Range
    shock_range=(-4, 4),                    # σ units
    n_points=200,
    # Styling
    colors=["#6C3483", "#E74C3C", "#2E86C1"],
    linewidths=[2.0, 1.5, 1.5],
    linestyles=["-", "--", "-."],
    # Reference
    show_zero_line=True,
    zero_color="#7F8C8D",
    # Layout
    title="News Impact Curve Comparison",
    figsize=(10, 6),
    xlabel="Shock (εₜ₋₁)",
    ylabel="Conditional Variance (σ²ₜ)",
    legend_loc="upper center",
)
```

??? example "Expected Output"
    The comparison shows:

    - Purple solid symmetric GARCH curve
    - Red dashed EGARCH curve -- steeper on the left (negative shocks)
    - Blue dash-dot GJR curve -- a kink at $\varepsilon = 0$ showing the leverage term
    - The leverage effect is clearly visible: negative shocks increase volatility more than positive shocks of equal magnitude

---

## Plot Type 7: PIT Histogram (Probability Integral Transform)

If the model is correctly specified, the PIT values $u_t = F(z_t; \hat{\theta})$ should be i.i.d. $\text{Uniform}(0,1)$. The PIT histogram tests this visually.

### Mathematical Background

The Probability Integral Transform states that if $z_t \sim F$, then:

$$u_t = F(z_t; \hat{\theta}) \sim \text{Uniform}(0,1)$$

A well-calibrated model produces a flat PIT histogram. Deviations indicate:

- **U-shape**: Underdispersion (tails too thin)
- **Inverted U**: Overdispersion (tails too heavy)
- **Skewed**: Location or asymmetry misspecification

### Basic Usage

```python
# PIT histogram
fig = result.plot("pit")
```

??? example "Expected Output"
    The chart displays:

    - **Histogram**: PIT values binned into 20 equal-width bins
    - **Horizontal dashed line**: Expected count under Uniform(0,1)
    - **Confidence bands**: 95% confidence interval for each bin
    - A flat histogram indicates correct specification
    - Bars outside the confidence bands indicate misspecification

### Full Customization

```python
fig = result.plot(
    "pit",
    # Histogram
    bins=20,
    hist_color="#6C3483",
    hist_alpha=0.7,
    hist_edgecolor="white",
    # Reference line
    show_uniform=True,
    uniform_color="#E74C3C",
    uniform_style="--",
    uniform_linewidth=2.0,
    # Confidence
    show_confidence=True,
    confidence_alpha=0.05,
    confidence_color="#AEB6BF",
    # KS test
    show_ks_test=True,                      # Kolmogorov-Smirnov p-value
    # Layout
    title="PIT Histogram -- GARCH(1,1) Student-t",
    figsize=(10, 5),
    xlabel="PIT Values",
    ylabel="Frequency",
)
```

??? example "Expected Output"
    The PIT histogram shows:

    - 20 purple bars of approximately equal height
    - Red dashed horizontal line at the expected uniform level
    - Grey confidence bands around the expected level
    - All bars within the confidence bands
    - KS test annotation: $D = 0.023$, $p = 0.412$ (cannot reject uniformity)
    - The flat histogram confirms the Student-$t$ distributional assumption is adequate

---

## Plot Type 8: Standardized Residuals Over Time

Displays the standardized residuals $z_t = r_t / \sigma_t$ as a time series. If the model is well-specified, this should resemble white noise with constant unit variance.

### Basic Usage

```python
# Standardized residuals
fig = result.plot("residuals")
```

??? example "Expected Output"
    The chart displays:

    - **Line/scatter**: Standardized residuals over time
    - **Horizontal lines**: $\pm 2$ and $\pm 3$ reference lines
    - Residuals should appear as white noise with no patterns
    - No visible clustering (volatility clustering has been removed)
    - Occasional extreme values ($|z_t| > 3$) are expected

### Full Customization

```python
fig = result.plot(
    "residuals",
    # Styling
    color="#2C3E50",
    linewidth=0.5,
    alpha=0.7,
    # Reference lines
    show_bands=True,
    band_levels=[2, 3],                     # ±2σ and ±3σ
    band_colors=["#F39C12", "#E74C3C"],    # Yellow at ±2, red at ±3
    band_alpha=0.15,
    # Extreme values
    highlight_extremes=True,
    extreme_threshold=3.0,
    extreme_color="#E74C3C",
    extreme_size=20,
    # Layout
    title="Standardized Residuals -- GARCH(1,1)",
    figsize=(14, 5),
    ylabel="Standardized Residuals (zₜ)",
    start_date="2006-01-01",
)
```

??? example "Expected Output"
    The residual plot shows:

    - Thin dark line oscillating around zero with constant variance
    - Yellow shaded bands at $\pm 2$ (encompassing ~95% of observations)
    - Red shaded bands at $\pm 3$ (encompassing ~99.7%)
    - Red dots marking extreme residuals exceeding $\pm 3$
    - No visible volatility clustering -- the GARCH model has removed it
    - The visual appearance is consistent with i.i.d. noise

---

## Complete Diagnostic Workflow

```python
from archbox.models import GARCH, EGARCH, GJR
from archbox.visualization import plot_news_impact_comparison
from archbox.datasets import load_returns

# Data and model
returns = load_returns("sp500")
model = GARCH(returns, p=1, q=1, dist="student-t")
result = model.fit()

# --- Quick diagnostic: 4-panel grid ---
fig1 = result.plot(
    "diagnostics",
    figsize=(14, 10),
    title="GARCH(1,1) Student-t Diagnostics",
)
fig1.savefig("diagnostics_grid.pdf", bbox_inches="tight")

# --- Detailed ACF analysis ---
fig2 = result.plot(
    "acf-squared",
    max_lags=40,
    show_ljung_box=True,
    title="ACF of Squared Residuals",
)
fig2.savefig("diagnostics_acf.pdf", bbox_inches="tight")

# --- QQ-plot with confidence envelope ---
fig3 = result.plot(
    "qq",
    show_envelope=True,
    title="QQ-Plot vs Student-t",
)
fig3.savefig("diagnostics_qq.pdf", bbox_inches="tight")

# --- Histogram ---
fig4 = result.plot(
    "histogram",
    bins=60,
    show_normal=True,
    show_stats=True,
    title="Residual Distribution",
)
fig4.savefig("diagnostics_hist.pdf", bbox_inches="tight")

# --- PIT histogram ---
fig5 = result.plot(
    "pit",
    show_ks_test=True,
    title="PIT Histogram",
)
fig5.savefig("diagnostics_pit.pdf", bbox_inches="tight")

# --- News impact comparison ---
egarch = EGARCH(returns, p=1, q=1, dist="student-t").fit()
gjr = GJR(returns, p=1, q=1, dist="student-t").fit()

fig6 = plot_news_impact_comparison(
    models=[result, egarch, gjr],
    labels=["GARCH(1,1)", "EGARCH(1,1)", "GJR(1,1)"],
    title="News Impact Curve Comparison",
)
fig6.savefig("diagnostics_nic.pdf", bbox_inches="tight")

# --- Print diagnostic summary ---
print("Diagnostic Summary:")
print(f"  Ljung-Box Q(10) on z²: p = {result.diagnostics.ljung_box_p:.4f}")
print(f"  ARCH-LM(5): p = {result.diagnostics.arch_lm_p:.4f}")
print(f"  KS test (PIT): p = {result.diagnostics.ks_p:.4f}")
print(f"  Jarque-Bera: p = {result.diagnostics.jb_p:.4f}")
```

---

## Common Customization Options

All diagnostic plots accept these shared parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `backend` | `str` | `"matplotlib"` | `"matplotlib"` or `"plotly"` |
| `theme` | `str` | `"archbox"` | Plot theme name |
| `figsize` | `tuple` | varies | Figure size in inches |
| `title` | `str` | Auto | Plot title |
| `color` | `str` | `"#6C3483"` | Primary plot color |
| `alpha` | `float` | `0.05` | Statistical significance level |
| `grid` | `bool` | `True` | Show grid lines |
| `dpi` | `int` | `150` | Resolution for raster export |

---

## Export

All diagnostic plots return a figure object:

=== "Matplotlib"

    ```python
    fig = result.plot("diagnostics")

    fig.savefig("diagnostics.png", dpi=300, bbox_inches="tight")
    fig.savefig("diagnostics.pdf", bbox_inches="tight")
    fig.savefig("diagnostics.svg", bbox_inches="tight")
    ```

=== "Plotly"

    ```python
    fig = result.plot("diagnostics", backend="plotly")

    fig.write_html("diagnostics.html", include_plotlyjs="cdn")
    fig.write_image("diagnostics.png", scale=2, width=1400, height=1000)
    ```

!!! tip "Publication Workflow"
    For academic papers, use the 4-panel grid as a single figure:
    ```latex
    \begin{figure}[htbp]
        \centering
        \includegraphics[width=\textwidth]{diagnostics_grid.pdf}
        \caption{Diagnostic plots for the GARCH(1,1)-$t$ model: standardized residuals (top-left),
        ACF of squared residuals (top-right), QQ-plot (bottom-left), and residual histogram (bottom-right).}
        \label{fig:diagnostics}
    \end{figure}
    ```

---

## See Also

- [Visualization Overview](index.md) -- backends, themes, and export formats
- [Volatility Plots](volatility-plots.md) -- conditional volatility charts
- [Regime Plots](regime-plots.md) -- regime-switching visualization
- [Themes & Customization](themes.md) -- styling and publication-ready themes
- [Ljung-Box Test](../diagnostics/ljung-box.md) -- formal serial correlation test
- [ARCH-LM Test](../diagnostics/arch-lm.md) -- formal ARCH effects test
- [News Impact](../diagnostics/news-impact.md) -- news impact curve details
