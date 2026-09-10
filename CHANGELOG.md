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

#### BREAKING: subpackage API changes

- `MultivariateVolatilityModel.covariance(corr_t, t)` and `.correlation(corr_t, t)`
  were removed — they read mutable model state. Use `results.covariance(t)` /
  `results.correlation(t)`.
- `ThresholdResults.forecast(h)` and `ThresholdModel.forecast(results, h)` return
  an array of point forecasts; the simulated intervals and paths moved to
  `forecast_intervals(h, n_sims, alpha, seed)` (previously
  `forecast(h)["mean"]`, `["lower"]`, ...).
- `MarkovSwitchingGARCH` no longer exposes `_sigma2`, `_h_collapsed` or
  `update_collapsed_variance`; use `conditional_variances(params)` and
  `results.conditional_variances`. `simulate` returns `int64` regime labels
  (previously float).
- `nyblom_test` raises `ValueError` for more than `MAX_NYBLOM_PARAMS = 20`
  parameters instead of extrapolating critical values linearly.
- Risk measures now require a results object exposing `resid` (raw),
  `std_resid`, `conditional_volatility` and `mu`; objects that only had the old
  standardized `resid` raise `TypeError`.

#### Risk (VaR, ES, EWMA, backtesting)

- **VaR and ES are back on the scale of the returns.** Every method mixed raw
  and standardized quantities; historical VaR on `sp500` reported `-1.9` where
  the empirical 5% quantile is `-0.0199`. A new `archbox.risk.base.RiskMeasure`
  reads the documented results contract (`resid`, `std_resid`,
  `conditional_volatility`, `mu`) and raises `TypeError` naming what is missing
  instead of falling back to `endog` or inventing a mean.
- **The fitted conditional distribution is used by default.** `parametric()`
  and the innovation quantiles previously hard-coded a normal or `nu = 8`;
  `dist=None, nu=None` now uses the model's own distribution and *estimated*
  shape parameters (Normal and Student-t in closed form, GED / skewed-t /
  mixture by numerical inversion). An explicit `dist`/`nu` still overrides;
  unknown names raise `ValueError` and `nu <= 2` is rejected.
- **Definitions corrected.** `historical()` quantiles the raw returns over a
  strictly-past rolling window; `filtered_historical()` is
  `mu + sigma_t * quantile(std_resid[:t])`.
- **`monte_carlo()` simulates the fitted model.** It is seeded and vectorised,
  draws innovations from the fitted distribution, propagates each model's own
  variance recursion (verified against `results.forecast(h)['variance']` to
  within 1% for GARCH/GJR/EGARCH at h = 1..5) and handles the GARCH-M in-mean
  offset. `ExpectedShortfall.monte_carlo()` is new. Both return the per-step
  measure for `r_{T+h+1}`, shape `(horizon,)`.
- **Basel traffic light.** `VaRBacktest.basel_zones(window)` derives the
  yellow/red boundaries from `Binomial(n, alpha)` (95% / 99.99% cumulative). It
  reproduces the published 250-day/1% table exactly (5, 10) and scales to other
  levels, so a correctly specified 5% VaR is now green rather than red.
- **Backtest input validation.** Empty or all-NaN input raises `ValueError` at
  construction, non-finite pairs are dropped (not just NaN), and every rate
  method checks that observations remain.
- `EWMAResult` exposes `resid` and `std_resid` (`resids` kept as an alias), so
  an EWMA fit satisfies the same contract as a model fit.
- `ArchExperiment.risk_analysis` validates method names (`ValueError`, not
  `KeyError`), takes a `seed`, backtests each in-sample series against the raw
  returns aligned by length, and treats `monte-carlo` as a forecast rather than
  a degenerate one-observation backtest. `validate_model` gained `alpha` and
  fills `ValidationResult.var_series`; `var_violation_rate` checks length
  alignment and drops non-finite pairs.

#### Diagnostics

- **`full_diagnostics` no longer swallows failures.** Every
  `contextlib.suppress(Exception)` / bare `except: pass` is gone: inapplicable
  tests land in `DiagnosticReport.skipped` with a reason (printed by
  `summary()`), and a missing/empty/non-finite input raises. It reads
  `std_resid` for ARCH-LM, Ljung-Box on z² and Jarque-Bera, and the raw `resid`
  for the sign-bias regression, per Engle-Ng.
- The `lags` argument is honoured: defaults are now `arch_lm_lags = [1, 5, lags]`
  and `lb_lags = [5, lags, 2*lags]` (identical to the old fixed lists at
  `lags=10`).
- **Nyblom is wired in.** Per-observation scores come from `results.scores`, or
  from central finite differences of `loglike_per_obs` at the estimates,
  demeaned (the MLE first-order condition makes exact scores sum to zero, so the
  numerical drift would otherwise read as parameter instability). It skips with
  an explicit reason when the model has no `loglike_per_obs`, `k > 20` or
  `T <= k`.
- **Nyblom critical values replaced with Hansen (1992) Table 1** for k = 1..20,
  independently reproduced by Monte-Carlo simulation of the limiting functional.
  The linear `k * cv(1)` extrapolation beyond the table is gone;
  `nyblom_test` raises `ValueError` above `MAX_NYBLOM_PARAMS = 20`.
- **`engle_sheppard_test` is now the Engle & Sheppard (2001) test**: the
  above-diagonal elements of `(R^{-1/2} D_t^{-1} r_t)(.)' - I` stacked into one
  artificial regression on a constant and `s` lags, `chi2(s+1)`. Empirical size
  went from identically 0 to 0.030 (k=3, T=500, lags=5) with strong power; the
  residual conservativeness is documented.
- **p-values use survival functions** (`sf`) everywhere instead of `1 - cdf`, so
  deep-tail statistics no longer return exactly 0: `arch_lm`, `ljung_box`,
  `hong_spillover`, `sign_bias` (three t-tests and the F-test),
  `engle_sheppard`, `diagnostics`.
- `sign_bias_test` guards tiny samples (`MIN_SIGN_BIAS_OBS = 6`); it used to
  divide by `n - 4` and return garbage.

#### Multivariate

- **Standardized residuals.** `_fit_univariate` reads `res.std_resid` and
  `res.conditional_volatility` from each univariate fit instead of re-deriving
  them.
- **DECO** got DCC's five-start optimisation and a closed-form equicorrelation
  likelihood (`equicorrelation_loglike`, tested equal to `correlation_loglike`)
  in place of a single start and a per-`t` Python loop; on simulated DCC data it
  recovers a = 0.0475, b = 0.8838 (true 0.05 / 0.90) with finite standard errors.
- **`univariate_model` is honoured**: a name, a `VolatilityModel` subclass or a
  callable factory, plus `univariate_dist`; `supported_methods` per model with a
  `_check_method` guard. Non-convergence now raises `ConvergenceError` or warns
  and sets `results.converged = False`, and the `±1e10` sentinels no longer leak
  into the reported likelihood.
- **Forecasts fixed.** DCC/DECO keep the full Q path (`results.extras["q_path"]`)
  so h=1 is the exact in-sample recursion one step ahead; BEKK h=1 uses
  `eps_T eps_T'`; conditional variances come from each univariate
  `ArchResults.forecast(horizon)`.
- **GO-GARCH no longer needs scikit-learn** — `pca_whiten` and `fast_ica` are
  implemented in numpy and exported; `seed` replaces the hard-coded
  `random_state=42`; loops run over `n_components`, and unspanned idiosyncratic
  variance keeps `H_t` positive definite when `m < k`.
- **BEKK**: the `k` mean parameters count towards AIC/BIC, `C`'s diagonal is
  bounded strictly positive, the Engle-Kroner spectral-radius stationarity
  constraint is enforced (`BEKK.stationarity_measure`) and the likelihood is
  vectorised.
- **`MultivarResults` is a real results object** (moved to
  `archbox/multivariate/results.py`, re-exported from `base`): `std_errors` from
  a numerical Hessian, `tvalues`, `converged`, `std_resid`,
  `conditional_covariance`/`_correlation`, `covariance(t)`/`correlation(t)`,
  `summary()`, `params_frame()` and DataFrame accessors that preserve column
  names.
- `archbox/multivariate/utils.py` is no longer dead code: it provides the shared
  `validate_multivariate_returns`, stack-aware `cov_to_corr`/`corr_to_cov`,
  `numerical_hessian` and `standard_errors_from_hessian`.

#### Regime-switching

- **The pre-sample no longer poisons the likelihood.** MS-AR/MS-VAR condition on
  the first `p` observations (`_t_start`, `nobs_effective`) and score them `0.0`
  instead of `-1e10`; the filter, likelihood and M-step all start at `t = p`,
  and probability paths are padded back to length `T`. MS-AR on `us_gdp` now
  converges in 64 iterations to a log-likelihood of `-372.884` on 303 effective
  observations (previously `-1e10` after 2 iterations). BIC uses the effective
  sample.
- **MS-VAR M-step** is the exact weighted multivariate least squares for the
  intercept *and* `Phi` per regime, followed by the weighted residual
  covariance; `results.coefficients` and `results.intercepts` are exposed.
  Start values now split pooled-OLS residuals into quantile groups, which
  escapes the flat-start local optimum (test data: -2543.868 in 17 iterations
  and 100% regime classification, versus -2867.35 and 72% before).
- **MS-GARCH** uses one Gray (1996) forward pass that computes the
  regime-conditional variances, the Hamilton filter and the collapsed
  `h_{t-1}` together. `_regime_loglike` no longer mutates model state
  (`_sigma2`, `_h_collapsed` and `update_collapsed_variance` are replaced by
  `conditional_variances(params)`), and estimation maximises the filter
  likelihood directly over a parameterisation that keeps `alpha + beta < 1`.
- **Parameters are written back.** The transition matrix is stored in `params`
  as multinomial-logit tails, the final E-step runs at the converged values, and
  `model.loglike(results.params) == results.loglike` exactly for MS-Mean, MS-AR,
  MS-VAR and MS-GARCH. The initial-state distribution stays out of `params`
  (it would change every subclass's `start_params` length) and is exposed as
  `results.init_probs`.
- **`forecast(h)`** propagates the last filtered probabilities through `P` and
  returns `{'mean', 'variance', 'regime_probs'}` as mixture moments;
  `simulate` draws the chain from its ergodic distribution and observations from
  the fitted regime distributions.
- **Transition parameterisation** is a softmax over each row with the diagonal
  as reference, with an exact inverse; the previous element-wise logistic map
  produced negative diagonal probabilities for `k >= 3`.
- **MS-AR** documents the implemented (Kim-style, intercept-switching)
  specification, and its M-step is the exact conditional maximiser (one stacked
  weighted least squares with weights `P(S_t=s|Y_T)/sigma_s^2`). Numerical
  Hessian standard errors, `converged` and effective-sample BIC are reported for
  every model.
- **Performance**: `_regime_loglikes` is evaluated once per likelihood call
  (O(T·k), asserted by a test), and the `T x T` `np.diag(weights)` matrices are
  gone.
- The MSwM validation fixture was regenerated with real R (MSwM 1.5); the
  generator script is committed. archbox attains a log-likelihood at least as
  high as MSwM on both specifications, and reproduces MSwM to ~1% when it adopts
  MSwM's (non-maximising) M-step weighting.
- `archbox/report/transformers/regime.py` iterated `enumerate(results.regime_params)`
  over a dict (yielding the keys as parameters) and read attributes that never
  existed; it now accepts a dict or a sequence and falls back to `k_regimes` /
  `loglike`.

#### Threshold / STAR

- **Three-regime models work end to end.** `ThresholdResults` carries
  `params_regimes` (with `params_regime1/2/3` as aliases), regime selection goes
  through `regime_weights(G)`, and TAR genuinely fits `n_regimes=3`; SETAR now
  subclasses TAR and shares `archbox/threshold/_hard_fit.py`.
- **Forecasting**: `forecast(h)` returns point forecasts as an array and the new
  `forecast_intervals(h, n_sims, alpha, seed)` returns
  `mean/median/lower/upper/paths`. With `TAR(threshold_var=...)` the exogenous
  variable drives the forecast (`s_t = z_{t-d}`, known while `h <= d`, held
  afterwards with a `UserWarning`) and is delayed consistently at fit time.
- **Linearity tests**: the LST auxiliary regression drops the columns that
  duplicate the design when `d <= p`, so `df_num` counts genuinely added
  regressors (6 rather than 9 at p=2, d=1) and empirical size went from ~0 to
  ~0.04. `tsay_test` is now Tsay (1989) — arranged autoregression, recursive
  standardized predictive residuals, F-test (size ~0.035, power ~1).
  `hansen_threshold_test` is a sup-F test over the trimmed threshold grid with a
  wild bootstrap that re-fits the null on each replication.
- **STAR gamma is scale-equivariant**: the grid and the upper bound are scaled by
  `std(s)^k` (k = 1 logistic, 2 exponential) instead of a fixed cap of 500, and
  the optimiser's `success` flag drives `results.converged`.
- **SETAR delay selection** scores every candidate `d` on a common effective
  sample and re-estimates the winner on its own full sample; parameter counts
  come from one shared helper, so TAR and fixed-delay SETAR report identical
  AIC/BIC and automatic delay selection costs exactly one parameter.
- Non-finite `endog` (and `threshold_var`) are rejected, `loglike` is generalised
  to n regimes and is what the models actually use, and `results.linearity_test`
  and `results.param_names` are populated by every fit.

#### CLI and reports

- `archbox risk --var-method monte-carlo` paired a one-step Monte-Carlo VaR with
  a full in-sample filtered-historical ES series; it now calls
  `ExpectedShortfall.monte_carlo()`, and an unknown method raises instead of
  silently falling back to the parametric ES.
- The multivariate report transformer's DCC parameter block was dead against
  real results (`MultivarResults` has no `dcc_a`/`dcc_b`); it now reads
  `params`/`param_names` and derives `dcc_persistence`.

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
- `ExpectedShortfall.monte_carlo()`, `VaRBacktest.basel_zones()`, and
  `RiskMeasure.innovation_quantile()` / `innovation_tail_mean()`.
- `DiagnosticReport.skipped`, reporting which diagnostics were not applicable
  and why.
- `archbox.multivariate.utils`: `numerical_hessian`,
  `standard_errors_from_hessian`, stack-aware `cov_to_corr`/`corr_to_cov`,
  `validate_multivariate_returns`; `pca_whiten` and `fast_ica` (numpy
  replacements for the scikit-learn dependency); `equicorrelation_loglike`.
- `MultivarResults.summary()`, `params_frame()` and the DataFrame accessors.
- Regime results expose `coefficients`, `intercepts`, `init_probs`,
  `std_errors`, `converged`, `nobs_effective` and
  `MarkovSwitchingGARCH.conditional_variances`.
- `ThresholdResults.forecast_intervals()`, `params_regimes`, `regime_weights()`
  and a populated `linearity_test` on every fit.
- End-to-end CLI tests that execute the `risk`, `backtest` and `regime`
  subcommands on a generated CSV (`tests/cli/test_cli_commands.py`).

### Removed

- `archbox.utils.transforms` — dead code, nothing in the package imported it.
- `archbox.core.config` — dead code, superseded by explicit arguments.
- The scikit-learn dependency of GO-GARCH (PCA whitening and FastICA are now
  implemented in numpy).

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
