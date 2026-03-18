# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-03-17

### Added

- **Core**: VolatilityModel ABC, ArchResults, MLEstimator
- **Models**: GARCH, EGARCH, GJR-GARCH, APARCH, FIGARCH, IGARCH, GARCH-M, Component GARCH, HAR-RV
- **Distributions**: Normal, Student-t, Skewed-t, GED
- **Multivariate**: DCC, CCC, BEKK, GO-GARCH, DECO
- **Regime-Switching**: MS-Mean, MS-AR, MS-VAR, MS-GARCH, Hamilton filter, Kim smoother
- **Threshold**: SETAR, LSTAR, ESTAR, linearity tests
- **Risk**: VaR (parametric, historical, filtered HS, Monte Carlo), Expected Shortfall, backtesting (Kupiec, Christoffersen, traffic light)
- **Diagnostics**: ARCH-LM, Ljung-Box, Jarque-Bera, sign/size bias, news impact curve
- **Reporting**: HTML/JSON report generation
- **CLI**: archbox estimate, risk, backtest, regime commands
- **Experiment**: ArchExperiment pattern for model comparison workflows
- **Datasets**: 11 built-in datasets (SP500, FTSE100, Bitcoin, FX, sectors, realized vol, GDP, unemployment, industrial production, IBOVESPA, USD/BRL)
- **Numba**: Optional JIT acceleration for GARCH, EGARCH, Hamilton filter, DCC recursion
- **Documentation**: MkDocs Material with ~24 pages
- **Quality**: 10-phase QA (ruff, pyright, coverage, security, complexity, docstrings, hypothesis, pre-commit, structlog, mutation testing)
