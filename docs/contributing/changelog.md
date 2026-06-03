---
title: "Changelog"
description: "ArchBox version history — all releases with key changes, new models, and improvements."
---

# Changelog

All notable changes to ArchBox are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and ArchBox adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**Sections**: Added, Changed, Fixed, Deprecated, Removed, Security, Performance.

---

## [Unreleased]

### Added

#### Comprehensive Documentation

- Full MkDocs Material documentation with 110+ pages
- Theory sections with MathJax equations for all model families
- API Reference for all public modules
- Tutorials covering fundamentals through advanced workflows
- Visualization gallery with diagnostic, volatility, and risk plots
- FAQ (general, advanced, troubleshooting)
- Benchmarks against R `rugarch` and Python `arch`

---

## [0.1.0] — 2026-03

### Summary

**Initial Release — Complete Volatility Modeling Suite**

ArchBox v0.1.0 provides a comprehensive toolkit for conditional volatility modeling, multivariate analysis, regime-switching, threshold models, and risk management.

### Added

#### Univariate GARCH Models

- **GARCH(p,q)** — Bollerslev (1986) with MLE estimation
- **EGARCH** — Nelson (1991) exponential GARCH for asymmetric volatility
- **GJR-GARCH** — Glosten, Jagannathan & Runkle (1993) threshold GARCH
- **APARCH** — Ding, Granger & Engle (1993) asymmetric power ARCH
- **FIGARCH** — Baillie, Bollerslev & Mikkelsen (1996) fractionally integrated GARCH
- **IGARCH** — Integrated GARCH for unit-root volatility
- **GARCH-M** — GARCH-in-Mean with risk premium in the mean equation
- **Component GARCH** — Engle & Lee (1999) transitory and permanent components
- **HAR-RV** — Corsi (2009) Heterogeneous Autoregressive model for realized volatility

#### Error Distributions

- **Normal** — Gaussian distribution
- **Student-t** — Heavy-tailed distribution with degrees of freedom parameter
- **Skewed Student-t** — Hansen (1994) skewed t-distribution
- **GED** — Generalized Error Distribution
- **Skewed GED** — Asymmetric GED

#### Multivariate Models

- **DCC** — Engle (2002) Dynamic Conditional Correlation
- **BEKK** — Engle & Kroner (1995) multivariate GARCH
- **CCC** — Bollerslev (1990) Constant Conditional Correlation
- **GO-GARCH** — van der Weide (2002) Generalized Orthogonal GARCH
- **DECO** — Engle & Kelly (2012) Dynamic Equicorrelation

#### Regime-Switching Models

- **MS-AR** — Hamilton (1989) Markov-Switching Autoregressive
- **MS-VAR** — Krolzig (1997) Markov-Switching VAR
- **MS-GARCH** — Haas, Mittnik & Paolella (2004) regime-switching volatility
- **Hamilton Filter** — Filtered regime probabilities
- **Kim Smoother** — Kim (1994) smoothed regime probabilities
- **EM Algorithm** — Expectation-Maximization for regime estimation

#### Threshold and STAR Models

- **TAR** — Threshold Autoregressive model
- **SETAR** — Self-Exciting TAR with endogenous threshold
- **LSTAR** — Logistic Smooth Transition Autoregressive
- **ESTAR** — Exponential Smooth Transition Autoregressive
- **Linearity Tests** — LM tests for threshold effects

#### Risk Management

- **Value-at-Risk (VaR)** — Parametric, historical simulation, and GARCH-based
- **Expected Shortfall (ES)** — Conditional tail expectation
- **EWMA** — RiskMetrics exponentially weighted moving average
- **Backtesting** — Kupiec, Christoffersen, and DQ tests

#### Diagnostic Tests

- **Ljung-Box** — Serial correlation in residuals and squared residuals
- **ARCH-LM** — Engle (1982) test for remaining ARCH effects
- **Jarque-Bera** — Normality test
- **Kolmogorov-Smirnov** — Distribution goodness-of-fit
- **Information Criteria** — AIC, BIC, HQIC for model selection
- **Likelihood Ratio** — Nested model comparison
- **Sign Bias** — Engle & Ng (1993) asymmetry test
- **News Impact Curve** — Visualization of asymmetric volatility response
- **Persistence** — Half-life and unconditional variance

#### Visualization

- Volatility plots with confidence bands
- Correlation heatmaps and time-varying correlation plots
- Risk dashboards (VaR, ES, P&L)
- Regime probability plots
- Diagnostic plots (ACF, QQ, residuals)
- Customizable themes

#### Infrastructure

- **ArchExperiment** — Unified workflow for model comparison
- **CLI** — Command-line interface for common operations
- **Datasets** — Built-in financial datasets for examples and testing
- **Reports** — HTML and summary report generation

### Performance

| Benchmark | ArchBox | R `rugarch` |
|---|---|---|
| GARCH(1,1) fit (T=5000) | ~0.3s | ~0.5s |
| DCC(1,1) 5 assets | ~2.1s | ~3.8s |
| VaR backtest (1000 windows) | ~15s | ~28s |

---

## Versioning Policy

ArchBox uses [Semantic Versioning](https://semver.org/):

| Component | When incremented |
|---|---|
| **Major** (X.0.0) | Incompatible API changes |
| **Minor** (0.X.0) | New features, backward compatible |
| **Patch** (0.0.X) | Bug fixes, backward compatible |

---

## See Also

- [Contributing Guide](contributing.md) — How to contribute
- [Roadmap](roadmap.md) — Planned features
- [API Reference](../api/index.md) — Full API documentation
