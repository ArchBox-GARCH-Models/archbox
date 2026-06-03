---
title: "Roadmap"
description: "ArchBox development roadmap — planned features, priorities, and future directions."
---

# Roadmap

ArchBox aims to be the most comprehensive Python library for conditional volatility modeling, multivariate GARCH, regime-switching, and financial risk management. This roadmap outlines planned features, organized by priority.

!!! info "Current Status"
    ArchBox v0.1.0 is the current release with 9 univariate GARCH models, 5 multivariate models, regime-switching, threshold/STAR, risk management, and 10+ diagnostic tests.

---

## Next Release (v0.2.0)

Features actively planned for the next minor release.

### Realized Volatility Enhancements

- **Realized Kernels** — Barndorff-Nielsen et al. (2008) noise-robust realized volatility
- **Bipower Variation** — Jump-robust volatility estimation
- **HAR-RV extensions** — HAR-CJ (continuous/jump), HAR-RS (realized semivariance)
- **Realized GARCH** — Hansen, Huang & Shao (2012) linking realized and conditional volatility

### Additional Univariate Models

- **TGARCH** — Zakoian (1994) threshold GARCH on standard deviations
- **NAGARCH** — Engle & Ng (1993) nonlinear asymmetric GARCH
- **AVGARCH** — Absolute value GARCH
- **CGARCH enhancements** — Time-varying permanent component

### Forecasting Improvements

- **Multi-step forecasting** — Direct and iterated h-step ahead forecasts
- **Forecast combination** — Equal-weight, BMA, and optimal combination
- **Rolling window evaluation** — Expanding and fixed-window backtests
- **Density forecasts** — Full predictive distribution, not just point forecasts

---

## High Priority

Features planned for upcoming releases.

### GPU Acceleration

- **CuPy backend** — GPU-accelerated matrix operations for multivariate models
- **JAX backend** — Automatic differentiation for gradient-based optimization
- **Automatic backend selection** — Transparent CPU/GPU switching based on problem size
- **Batch estimation** — Parallel model fitting across multiple assets

### Bayesian GARCH

- **Bayesian GARCH(p,q)** — MCMC estimation with conjugate and non-informative priors
- **Bayesian EGARCH** — Posterior inference for asymmetric volatility
- **Bayesian DCC** — Hierarchical priors for correlation dynamics
- **Model comparison** — Bayes factors and marginal likelihoods via bridge sampling

### Copula Models

- **Copula-GARCH** — Marginal GARCH + copula dependence (Patton, 2006)
- **Time-varying copulas** — Dynamic copula parameters
- **Vine copulas** — High-dimensional dependence modeling
- **Copula families** — Gaussian, Student-t, Clayton, Frank, Gumbel, Joe

---

## Medium Priority

Features planned for future releases.

### Stochastic Volatility

- **SV model** — Taylor (1986) basic stochastic volatility
- **SV-t** — Heavy-tailed stochastic volatility
- **SV with jumps** — Bates (1996) jump-diffusion volatility
- **Particle filter estimation** — Sequential Monte Carlo for SV models

### High-Frequency Volatility

- **Realized GARCH** — Hansen, Huang & Shao (2012)
- **HEAVY model** — Shephard & Sheppard (2010) high-frequency and low-frequency
- **Tick data processing** — Trade and quote data aggregation
- **Microstructure noise** — Pre-averaging and kernel methods

### Portfolio Risk

- **Risk parity** — Equal risk contribution portfolios with GARCH covariances
- **CVaR optimization** — Conditional Value-at-Risk portfolio optimization
- **Stress testing** — Scenario analysis with regime-switching models
- **Systemic risk** — CoVaR, MES, SRISK measures

### Machine Learning Integration

- **Neural GARCH** — LSTM/GRU-augmented volatility models
- **Random forest VaR** — Ensemble methods for risk quantiles
- **Gradient boosted volatility** — XGBoost for volatility prediction
- **Hybrid models** — GARCH + ML residual correction

---

## Long-Term Vision

Exploratory features for future major releases.

### Streaming / Online Estimation

- **Online GARCH** — Recursive parameter updating for real-time volatility
- **Streaming VaR** — Real-time risk monitoring with adaptive windows
- **Event-driven updates** — Volatility updates triggered by market events
- **Dashboard integration** — Live volatility dashboards via WebSocket

### Distributed Computing

- **Dask integration** — Out-of-core estimation for large asset universes
- **Ray support** — Distributed bootstrap and cross-validation
- **Cloud-native workflows** — AWS/GCP/Azure integration for production risk systems

### Cross-Platform Tools

- **R `rugarch` translator** — Convert R volatility scripts to ArchBox Python code
- **Stata converter** — Translate Stata `arch` commands to ArchBox
- **Excel add-in** — Spreadsheet interface for common volatility models

### Advanced Multivariate

- **Factor DCC** — Dimensionality reduction for large portfolios
- **Regime-switching DCC** — Markov-switching correlation dynamics
- **Spatial GARCH** — Network-based volatility spillovers
- **Infinite-dimensional GARCH** — Functional data volatility models

---

## Documentation Roadmap

### Completed

- [x] Phase 1: Documentation infrastructure and MkDocs setup
- [x] Phase 2: Getting Started and User Guide pages
- [x] Phase 3: Theory pages with MathJax equations
- [x] Phase 4: Diagnostics, Tutorials, and Visualization guides
- [x] Phase 5: API Reference, FAQ, and Benchmarks
- [x] Phase 6: Contributing, Changelog, Roadmap, and Final Review

### Planned

- [ ] Maintenance: Regular updates as features are added
- [ ] Expansion: Community-contributed tutorials and case studies
- [ ] Translations: Spanish, Portuguese, Chinese documentation

---

## How to Influence the Roadmap

### Feature Requests

Open a [GitHub Issue](https://github.com/NodesEcon/archbox/issues) with the `[Feature]` label. Include:

1. **Use case**: What problem does it solve?
2. **Description**: What should the feature do?
3. **References**: Academic papers, existing implementations (R, Stata, MATLAB)
4. **Priority justification**: Why is this important for volatility modeling?

### Community Voting

React with a thumbs-up on existing feature request issues to signal demand. Features with more community interest are prioritized higher.

### Contributions

The fastest way to get a feature is to implement it yourself! See the [Contributing Guide](contributing.md) for templates and process. We provide mentorship for first-time contributors.

---

## Release Schedule

### Versioning

ArchBox follows [Semantic Versioning](https://semver.org/):

| Version | Cadence | Content |
|---|---|---|
| **Major** (X.0.0) | As needed | Breaking API changes |
| **Minor** (0.X.0) | Every 2-3 months | New features, backward compatible |
| **Patch** (0.0.X) | As needed | Bug fixes, documentation updates |

### Release Process

1. Feature freeze 1 week before release
2. Release candidate published for testing
3. Final release after validation
4. Changelog and migration notes published

### Support Policy

- **Current major version**: Full support (bug fixes, security patches, new features)
- **Previous major version**: Security patches only for 6 months after new major release
- **Older versions**: Community support only

---

## See Also

- [Contributing Guide](contributing.md) — How to contribute code and documentation
- [Changelog](changelog.md) — Version history
- [Code of Conduct](code-of-conduct.md) — Community standards
- [API Reference](../api/index.md) — Full API documentation
