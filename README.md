# archbox

[![CI](https://github.com/ArchBox-GARCH-Models/archbox/actions/workflows/ci.yml/badge.svg)](https://github.com/ArchBox-GARCH-Models/archbox/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/ArchBox-GARCH-Models/archbox/branch/main/graph/badge.svg)](https://codecov.io/gh/ArchBox-GARCH-Models/archbox)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![PyPI version](https://badge.fury.io/py/garchbox.svg)](https://badge.fury.io/py/garchbox)
[![Python versions](https://img.shields.io/pypi/pyversions/garchbox)](https://pypi.org/project/garchbox/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Development Status](https://img.shields.io/badge/development%20status-alpha-orange)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/garchbox?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/garchbox)
[![Documentation](https://readthedocs.org/projects/archbox/badge/?version=latest)](https://archbox.readthedocs.io/)

Conditional volatility modelling for financial time series: the GARCH family,
multivariate GARCH, Markov-switching and threshold/STAR models, plus VaR/ES risk
tooling, specification diagnostics, reports and a CLI.

> **Names.** The PyPI distribution is `garchbox`; the import name is `archbox`.
> `pip install garchbox`, then `import archbox`.

---

## Installation

```bash
pip install garchbox                 # core
pip install "garchbox[numba]"        # + JIT-accelerated recursions
pip install "garchbox[dev]"          # pytest, pytest-cov, ruff, pyright
pip install "garchbox[docs]"         # mkdocs-material, mkdocstrings, mike
```

Requires Python >= 3.11. Runtime dependencies: numpy, scipy, pandas, matplotlib.

From a clone, for development:

```bash
pip install -e ".[dev]"
```

---

## Quick start

```python
from archbox import GARCH
from archbox.datasets import load_dataset

returns = load_dataset("sp500")["returns"]

model = GARCH(returns, p=1, q=1, dist="student-t")
results = model.fit(disp=False)

print(results.summary())
print(results.persistence(), results.half_life(), results.unconditional_variance())

fc = results.forecast(horizon=10)
print(fc["variance"], fc["volatility"])
```

`import archbox` is deliberately light: subpackages (`archbox.multivariate`,
`archbox.regime`, `archbox.threshold`, `archbox.risk`, `archbox.diagnostics`,
`archbox.distributions`, `archbox.visualization`, `archbox.report`) are resolved
lazily on first attribute access, and matplotlib is only imported when you
actually plot.

```python
import archbox

archbox.GARCH               # eager
archbox.multivariate.DCC    # imported on demand
```

---

## What's in the box

### Univariate volatility models

All live in `archbox.models`; the nine below are also re-exported at top level.

| Class | Model | Reference |
|---|---|---|
| `GARCH` | GARCH(p, q) | Bollerslev (1986) |
| `EGARCH` | Exponential GARCH | Nelson (1991) |
| `GJRGARCH` | Threshold/leverage GARCH | Glosten, Jagannathan & Runkle (1993) |
| `APARCH` | Asymmetric Power ARCH | Ding, Granger & Engle (1993) |
| `FIGARCH` | Fractionally integrated GARCH | Baillie, Bollerslev & Mikkelsen (1996) |
| `IGARCH` | Integrated GARCH | Engle & Bollerslev (1986) |
| `GARCHM` | GARCH-in-Mean | Engle, Lilien & Robins (1987) |
| `ComponentGARCH` | Permanent + transitory components | Engle & Lee (1999) |
| `HARRV` | HAR for realized volatility | Corsi (2009) |

```python
from archbox import APARCH, EGARCH, GJRGARCH
from archbox.datasets import load_dataset

returns = load_dataset("sp500")["returns"]

egarch = EGARCH(returns, p=1, q=1).fit(disp=False)
gjr = GJRGARCH(returns, p=1, q=1).fit(disp=False)
aparch = APARCH(returns, p=1, q=1).fit(disp=False)

for name, res in [("EGARCH", egarch), ("GJR", gjr), ("APARCH", aparch)]:
    print(f"{name:8s} aic={res.aic:12.2f}  persistence={res.persistence():.4f}")
```

Every model exposes `persistence()`, `unconditional_variance()`,
`conditional_variance()`, `forecast_variance()` and `simulate(n, params,
seed=...)`; the class attribute `supports_variance_targeting` says whether
`fit(variance_targeting=True)` is available.

### Conditional distributions

`archbox.distributions` provides `Normal`, `StudentT`, `SkewedT`,
`GeneralizedError` (GED) and `MixtureNormal`. Pass a name to any model:

```python
from archbox import GARCH

for dist in ("normal", "student-t", "skewed-t", "ged"):
    res = GARCH(returns, p=1, q=1, dist=dist).fit(disp=False)
    print(f"{dist:10s} loglike={res.loglike:12.2f}  bic={res.bic:12.2f}")
```

Estimated shape/skew parameters are appended to `results.params` (names in
`results.param_names`).

### Multivariate GARCH

`archbox.multivariate`: `CCC`, `DCC`, `BEKK`, `GOGARCH`, `DECO`, plus portfolio
helpers (`minimum_variance_weights`, `portfolio_variance`,
`portfolio_volatility`, `risk_contribution`, `risk_decomposition`, ...).

```python
from archbox.datasets import load_dataset
from archbox.multivariate import DCC, minimum_variance_weights

fx = load_dataset("fx_majors")
returns = fx.drop(columns="date").to_numpy()

res = DCC(returns, univariate_model="GARCH", univariate_order=(1, 1)).fit(disp=False)

print(res.summary())
print(res.dynamic_correlation.shape)   # (T, k, k)
print(minimum_variance_weights(res.dynamic_covariance[-1]))
```

### Regime switching

`archbox.regime`: `MarkovSwitchingMean`, `MarkovSwitchingMeanVar`,
`MarkovSwitchingAR`, `MarkovSwitchingVAR`, `MarkovSwitchingGARCH`, with
`HamiltonFilter`, `KimSmoother` and `EMEstimator` available directly.

```python
from archbox.datasets import load_dataset
from archbox.regime import MarkovSwitchingAR

gdp = load_dataset("us_gdp")
growth = gdp.drop(columns="date").iloc[:, 0].dropna().to_numpy()

res = MarkovSwitchingAR(growth, k_regimes=2, order=2).fit(method="em", verbose=False)
print(res.summary())
print(res.transition_matrix)
```

### Threshold and STAR

`archbox.threshold`: `TAR`, `SETAR`, `LSTAR`, `ESTAR`, the transition functions,
and the linearity tests `linearity_test`, `transition_type_test`, `tsay_test`,
`hansen_threshold_test`.

```python
from archbox.datasets import load_dataset
from archbox.threshold import SETAR, linearity_test

ip = load_dataset("industrial_production")
series = ip.drop(columns="date").iloc[:, 0].dropna().to_numpy()

print(linearity_test(series, order=2, delay=1))
res = SETAR(series, order=2, n_regimes=2).fit()
print(res.summary())
```

### Risk: VaR, ES, EWMA, backtesting

`archbox.risk`: `ValueAtRisk`, `ExpectedShortfall`, `EWMA`, `VaRBacktest`.

```python
from archbox import GARCH
from archbox.datasets import load_dataset
from archbox.risk import EWMA, ExpectedShortfall, ValueAtRisk, VaRBacktest

returns = load_dataset("sp500")["returns"].to_numpy()
res = GARCH(returns, p=1, q=1).fit(disp=False)

var = ValueAtRisk(res, alpha=0.05)
var_param = var.parametric()
var_fhs = var.filtered_historical()
var_mc = var.monte_carlo(n_sims=10_000)

es = ExpectedShortfall(res, alpha=0.05).parametric()

bt = VaRBacktest(returns[-500:], var_param[-500:], alpha=0.05)
print(bt.summary())
print(bt.violation_ratio(), bt.kupiec_test(), bt.christoffersen_test())
print(bt.basel_traffic_light())

ewma = EWMA(returns, lam=0.94).fit()
print(ewma.conditional_volatility[-1])
```

### Diagnostics

`archbox.diagnostics`: `arch_lm_test`, `ljung_box_squared`, `sign_bias_test`,
`nyblom_test`, `engle_sheppard_test`, `hong_spillover_test`, and
`full_diagnostics` / `DiagnosticReport` for the whole battery.

```python
from archbox.diagnostics import arch_lm_test, ljung_box_squared, sign_bias_test

print(arch_lm_test(res.std_resid, lags=5))
print(ljung_box_squared(res.std_resid, lags=10))
print(sign_bias_test(res.resid, res.std_resid))
```

> **`resid` is raw, `std_resid` is standardized.** `results.resid` holds
> $\varepsilon_t = r_t - \mu$ on the scale of the returns; `results.std_resid`
> holds $z_t = \varepsilon_t / \sigma_t$. Diagnostics test the standardized
> series. This changed from 0.1.0 — see the CHANGELOG.

### Model comparison workflows

```python
from archbox.datasets import load_dataset
from archbox.experiment import ArchExperiment

returns = load_dataset("sp500")["returns"].to_numpy()

exp = ArchExperiment(returns)
exp.fit_all_models([
    ("GARCH", {"p": 1, "q": 1}),
    ("EGARCH", {"p": 1, "q": 1}),
    ("GJR", {"p": 1, "q": 1}),
])
comparison = exp.compare_models()
print(comparison.ranking("aic"))
print(comparison.best_model("aic"))
```

### Visualization and reports

```python
from archbox.report import ReportManager
from archbox.visualization import plot_volatility

fig = plot_volatility(res)
html = ReportManager().generate(res, report_type="garch", fmt="html")
```

`archbox.visualization` also has `plot_diagnostics`, `plot_news_impact`,
`plot_regimes`, `plot_transition_matrix`, `plot_dynamic_correlation`,
`plot_correlation_heatmap`, `plot_distribution_fit`, `plot_var_backtest`,
`plot_traffic_light` and more.

### Datasets

Eleven built-in datasets for examples and tests:

```python
from archbox.datasets import list_datasets, load_dataset

print(list_datasets())
# ['bitcoin', 'ftse100', 'fx_majors', 'ibovespa', 'industrial_production',
#  'realized_vol', 'sector_indices', 'sp500', 'us_gdp', 'us_unemployment', 'usdbrl']
```

### Command line

```bash
archbox estimate  --model garch   --data returns.csv --p 1 --q 1 --dist student-t
archbox risk      --model garch   --data returns.csv --var-method filtered-hs --alpha 0.01
archbox backtest  --model egarch  --data returns.csv --alpha 0.01 --window 250
archbox regime    --model ms-ar   --data gdp.csv     --k-regimes 2 --order 2
```

`--model` and `--data` are required on every subcommand. Full flag reference:
[CLI docs](https://archbox.readthedocs.io/en/latest/api/cli/).

### Optional numba acceleration

```bash
pip install "garchbox[numba]"
```

```python
from archbox.utils.backend import set_backend

set_backend("numba")   # 'auto' (default) | 'numba' | 'python'
```

Accelerates the GARCH and EGARCH recursions, the Hamilton filter and the DCC
recursion. Without numba installed everything falls back to vectorised NumPy.

---

## Alpha status and known limitations

archbox is classified `Development Status :: 3 - Alpha`. Be aware that:

- **The API is not stable.** Pre-1.0, minor releases may break compatibility.
  Breaking changes are flagged under **BREAKING** in [CHANGELOG.md](CHANGELOG.md).
- **`resid` changed meaning** after 0.1.0 (raw instead of standardized). Code
  written against 0.1.0 that fed `results.resid` into a diagnostic must switch
  to `results.std_resid`.
- **Variance targeting is opt-in** and not supported by every model; check
  `Model.supports_variance_targeting` before passing
  `fit(variance_targeting=True)`.
- **Estimation is maximum likelihood via SciPy**, so convergence on short or
  badly scaled samples is not guaranteed. Use returns on a decimal scale
  (`0.01` = 1%), not percentages; percentage-scaled inputs routinely produce
  degenerate variance parameters.
- **Standard errors** come from a numerical Hessian; they are asymptotic and can
  be unreliable near the boundary of the parameter space.
- **BEKK and GO-GARCH scale poorly** in the number of series; DCC/DECO are the
  practical choice beyond a handful of assets.
- **No levels Ljung-Box test.** archbox ships `ljung_box_squared` (on $z_t^2$)
  only; for autocorrelation in the residual levels use
  `statsmodels.stats.diagnostic.acorr_ljungbox`.
- **Benchmarks in `tests/benchmarks/` assert wall-clock times** and are
  therefore deselected by default; they can fail on slow or loaded machines.
- Cross-validation against `rugarch` (R) and `arch` (Python) is ongoing; treat
  published numbers as indicative rather than certified.

---

## Development

```bash
pip install -e ".[dev]"

pytest                                        # benchmarks excluded by default
pytest tests/benchmarks -m benchmark -v -s    # run the wall-clock benchmarks
ruff check archbox/ tests/
pyright archbox/
mkdocs build --strict                         # needs the [docs] extra
```

Pre-commit hooks (ruff, ruff-format, pyright, whitespace/format checks):

```bash
pre-commit install
```

---

## Documentation

Full documentation: <https://archbox.readthedocs.io/>

---

## License

MIT — see [LICENSE](LICENSE).
