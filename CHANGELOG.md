# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Audit branch `fix/audit-2026-09`. This release corrects a number of results that
were silently wrong in 0.1.0, so read the **BREAKING** notes before upgrading.

### Fixed

#### Core results and forecasting

- **`ArchResults.persistence()` and `unconditional_variance()` are now
  model-specific.** They previously assumed a plain GARCH parameterisation and
  returned nonsense for EGARCH, GJR-GARCH, APARCH, FIGARCH, IGARCH, GARCH-M,
  Component GARCH and HAR-RV. Each `VolatilityModel` now implements
  `persistence(var_params, dist_params=None)` and
  `unconditional_variance(...)`, and `ArchResults` delegates to the model.
- **`ArchResults.forecast(horizon)` is correct for every model.** The one-step
  recursion hard-coded `omega + sum(alpha) * eps^2 + sum(beta) * sigma^2`, which
  is wrong for every non-GARCH member of the family. Forecasting now goes
  through `VolatilityModel.forecast_variance(var_params, resids, sigma2,
  horizon, dist_params=None)`; the returned dict still exposes `'variance'` and
  `'volatility'`.
- **GARCH-M in-mean term with non-normal innovations.** The lambda (risk
  premium) contribution to the mean equation was computed against a fixed normal
  likelihood, biasing every GARCH-M fit with a Student-t, skewed-t or GED
  conditional distribution.
- **Parameter bounds are enforced during estimation** instead of being checked
  only after the optimiser converged, so fits no longer return values outside
  the admissible region (for example negative `omega`).
- **`simulate()` lag handling.** The simulation recursion was off by one lag,
  so simulated series did not have the persistence of the parameters they were
  generated from. `simulate(n, params, seed=None)` now draws innovations from
  the *fitted* conditional distribution rather than always from a normal.
- **Skewed-t simulation** drew from an unskewed density; it now uses the
  distribution's inverse CDF.
- **numpy 2.x scalar conversion** in the multivariate log-likelihood.
- **Risk report transformer** no longer collides on the `var`/`es` names.

#### BREAKING: residual semantics

- `ArchResults.resid` now holds the **raw** residuals
  $\varepsilon_t = r_t - \mu$, on the same scale as the input returns.
  It previously held the *standardized* residuals.
- `ArchResults.std_resid` is the new attribute holding the **standardized**
  residuals $z_t = \varepsilon_t / \sigma_t$.
- Post-estimation diagnostics (`arch_lm_test`, `ljung_box_squared`,
  QQ-plots, Jarque-Bera) take `std_resid`; `sign_bias_test(resids, std_resids)`
  takes both. Code written against 0.1.0 that passed `results.resid` to a
  diagnostic must be updated to pass `results.std_resid`.
- `ArchResults.mu` exposes the fitted mean, and `ArchResults._sigma2` the
  conditional variance series backing `conditional_volatility`.

#### BREAKING: variance targeting is opt-in

- Variance targeting is no longer applied implicitly. Models declare support via
  the class attribute `supports_variance_targeting`, and callers request it
  explicitly (`fit(variance_targeting=True)` / `--variance-targeting` on the
  CLI). Requesting it on a model that does not support it now raises instead of
  silently ignoring the flag.

#### Distributions

- Conditional distributions are first-class: `_build_distribution` accepts
  either a `Distribution` instance or a string name, distribution objects
  implement `loglikelihood` / `ppf` / `cdf` / `simulate(n, rng)`, and their
  estimated parameters are exposed as `results._dist_params` (the trailing block
  of `results.params`) with names in `results.param_names`.

#### Risk, diagnostics, multivariate, regime and threshold

<!-- Placeholders: these areas are being fixed in parallel on the same branch.
     The merge agent replaces each bullet with the concrete list of fixes. -->

- **Risk**: _(pending — VaR/ES/EWMA/backtest fixes from the risk work stream)_
- **Diagnostics**: _(pending — test-statistic and reporting fixes from the
  diagnostics work stream)_
- **Multivariate**: _(pending — DCC/CCC/BEKK/GO-GARCH/DECO fixes from the
  multivariate work stream)_. Already landed: a vectorised module-level
  `correlation_loglike(corr_t, std_resids)` in `archbox/multivariate/base.py`.
- **Regime-switching**: _(pending — Hamilton filter / Kim smoother / EM fixes
  from the regime work stream)_
- **Threshold/STAR**: _(pending — SETAR/LSTAR/ESTAR and linearity-test fixes
  from the threshold work stream)_

### Changed

- **`import archbox` no longer imports matplotlib.** Subpackages
  (`archbox.multivariate`, `.regime`, `.threshold`, `.diagnostics`,
  `.distributions`, `.visualization`, `.report`, `.risk`, ...) are now resolved
  lazily through a module-level `__getattr__` (PEP 562), and the plotting
  helpers in `archbox.experiment` import `matplotlib.pyplot` inside the plotting
  functions. `archbox.GARCH` and `archbox.multivariate.DCC` both still work
  after a bare `import archbox`; the import loads 157 fewer modules and is about
  15% faster.
- **Library logging follows the standard convention.** `archbox` attaches a
  `logging.NullHandler` to its root logger instead of installing a
  `StreamHandler` on first `get_logger()` call, so importing archbox no longer
  writes to stderr. `configure_logging()` remains the opt-in way to turn output
  on, and repeated calls no longer stack handlers.
- **Benchmarks are deselected by default.** Wall-clock tests in
  `tests/benchmarks/` carry the `benchmark` marker and `addopts` includes
  `-m "not benchmark"`. Run them with `pytest tests/benchmarks -m benchmark -v -s`.
  Benchmarks that force a computation backend now restore it via a fixture, so a
  failed timing assertion can no longer leak `set_backend("python")` into the
  rest of the session.

### Added

- `[project.urls]` metadata (homepage, docs, repository, issues, changelog).
- Optional extra `numba = ["numba>=0.58"]`, matching what the docs advertise.
- Python 3.13 classifier and CI matrix entry.
- `benchmark` pytest marker, registered in `[tool.pytest.ini_options]`.

### Removed

- `archbox.utils.transforms` — dead code, nothing in the package imported it.
- `archbox.core.config` — dead code, superseded by explicit arguments.

### Documentation

- README now covers the whole library (univariate models, distributions,
  multivariate, regime-switching, threshold/STAR, risk, diagnostics, reports,
  CLI, numba extra) with verified import names, and states the alpha status and
  known limitations.
- `docs/api/cli.md` documents the CLI's real flags (`--var-method`,
  `--k-regimes`, `--order`, `--window`, `--variance-targeting`, `--mean`,
  `skewed-t`, and the mandatory `--model`), and the real JSON output keys.
- Every docs page that described `results.resid` as standardized, or passed it
  to `arch_lm_test` / `ljung_box_squared`, now uses `results.std_resid`.
- Calls to the non-existent `ljung_box_test` replaced with `ljung_box_squared`
  (which squares its input internally).
- 12 orphan documentation stubs that duplicated the nested pages were deleted;
  `benchmarks/performance.md` was added to the nav.
- `docs/contributing/changelog.md` now includes this file directly.
- Repository URLs point at `ArchBox-GARCH-Models/archbox` everywhere (README
  badges, `mkdocs.yml`, `docs/index.md`).
- The `08_complete_workflow` notebooks import names that actually exist
  (`GJRGARCH`, `MarkovSwitchingGARCH`, `ValueAtRisk`, `ExpectedShortfall`,
  `VaRBacktest`, `ljung_box_squared`, `minimum_variance_weights`).

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
