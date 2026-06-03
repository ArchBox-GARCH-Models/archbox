---
title: "Contributing Guide"
description: "How to contribute to ArchBox — setup, code standards, testing, and PR process."
---

# Contributing to ArchBox

Thank you for your interest in contributing to ArchBox! Whether you are reporting a bug, proposing a feature, improving documentation, or submitting code, your help is welcome and appreciated.

## Types of Contributions

| Type | Where | Description |
|------|-------|-------------|
| Bug reports | [GitHub Issues](https://github.com/NodesEcon/archbox/issues) | Reproducible problem with expected vs. actual behavior |
| Feature requests | [GitHub Issues](https://github.com/NodesEcon/archbox/issues) | Proposals with `[Feature]` label |
| Code (PR) | [Pull Requests](https://github.com/NodesEcon/archbox/pulls) | New models, tests, bug fixes |
| Documentation | `docs/` directory | Tutorials, API docs, examples |
| Test additions | `tests/` directory | Unit, integration, and validation tests |

---

## Development Setup

### 1. Fork and Clone

```bash
git clone https://github.com/YOUR_USERNAME/archbox.git
cd archbox
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
# venv\Scripts\activate    # Windows
```

### 3. Install in Development Mode

```bash
pip install -e ".[dev]"
```

### 4. Install Documentation Dependencies (Optional)

```bash
pip install -e ".[docs]"
```

### 5. Verify Setup

```bash
pytest tests/ -v --tb=short
```

### Development Dependencies

| Tool | Version | Purpose |
|------|---------|---------|
| pytest | >= 7.0 | Testing framework |
| pytest-cov | >= 4.0 | Coverage measurement |
| ruff | >= 0.4 | Linting and formatting |
| pyright | >= 1.1 | Static type checking |

---

## Code Standards

### Style

- **Formatter / Linter**: ruff (line length 100)
- **Target Python**: 3.11+
- **Type hints**: Required for all public API functions and methods
- **Docstrings**: NumPy-style for all public classes and methods

```bash
# Format
ruff format archbox/

# Lint with auto-fix
ruff check archbox/ --fix

# Type check
pyright archbox/
```

### Docstring Convention

ArchBox uses **NumPy-style** docstrings. Every public class and function must include:

```python
def fit_garch(returns, p=1, q=1, dist="normal"):
    """Estimate a GARCH(p,q) model via maximum likelihood.

    Parameters
    ----------
    returns : np.ndarray
        Array of log-returns.
    p : int, default=1
        Order of the GARCH (lagged variance) term.
    q : int, default=1
        Order of the ARCH (lagged squared residual) term.
    dist : str, default='normal'
        Error distribution: 'normal', 'student-t', 'skewed-t', 'ged'.

    Returns
    -------
    GARCHResult
        Fitted model results with parameters, standard errors,
        log-likelihood, and conditional volatility series.

    Raises
    ------
    ValueError
        If p or q is negative.
    ConvergenceError
        If the optimizer fails to converge.

    Examples
    --------
    >>> from archbox.models import GARCH
    >>> model = GARCH(returns, p=1, q=1)
    >>> result = model.fit()
    >>> print(result.params)

    References
    ----------
    .. [1] Bollerslev, T. (1986). Generalized autoregressive conditional
           heteroskedasticity. *Journal of Econometrics*, 31(3), 307-327.
    """
```

### Branch Naming

Use descriptive branch names:

- `feature/add-figarch-model` — New features
- `fix/egarch-convergence` — Bug fixes
- `docs/update-risk-tutorial` — Documentation changes
- `test/add-bekk-validation` — Test additions

### Commit Messages

```text
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `style`, `chore`

**Example**:

```text
feat(models): Add FIGARCH model for long memory volatility

Implements the Fractionally Integrated GARCH model
(Baillie, Bollerslev & Mikkelsen, 1996) with MLE
estimation and fractional differencing.

Closes #42
```

---

## Adding a New Volatility Model

Place your code in the appropriate module directory. Every model must:

1. Inherit from the appropriate base class
2. Implement `fit()` returning a results object
3. Have comprehensive tests with known reference values
4. Be exported from the package `__init__.py`
5. Have a documentation page

### Where to Place Code

| Model Family | Directory | Description |
|---|---|---|
| Univariate GARCH | `archbox/models/` | GARCH, EGARCH, GJR, APARCH, etc. |
| Distributions | `archbox/distributions/` | Student-t, GED, Skewed-t, etc. |
| Multivariate | `archbox/multivariate/` | DCC, BEKK, CCC, GO-GARCH |
| Regime-Switching | `archbox/regime/` | MS-AR, MS-GARCH, Hamilton filter |
| Threshold/STAR | `archbox/threshold/` | TAR, SETAR, LSTAR, ESTAR |
| Risk Management | `archbox/risk/` | VaR, ES, EWMA, Backtesting |
| Diagnostics | `archbox/diagnostics/` | Ljung-Box, ARCH-LM, Sign Bias |
| Visualization | `archbox/visualization/` | Plotting functions |

---

## Running Tests

```bash
# All tests
pytest tests/ -v

# Specific module
pytest tests/models/ -v
pytest tests/multivariate/ -v

# Specific test file
pytest tests/models/test_egarch.py -v

# With coverage
pytest tests/ --cov=archbox --cov-report=html --cov-branch

# Quick smoke test
pytest tests/ -v --tb=short -x
```

### Writing Tests

```python
import numpy as np
import pytest
from archbox.models import GARCH


class TestGARCH:
    """Tests for GARCH(p,q) model."""

    @pytest.fixture
    def returns(self):
        """Generate synthetic returns for testing."""
        np.random.seed(42)
        return np.random.standard_normal(1000) * 0.01

    def test_basic_estimation(self, returns):
        """Test that estimation runs and returns results."""
        model = GARCH(returns, p=1, q=1)
        result = model.fit()
        assert result.params is not None
        assert len(result.params) > 0

    def test_conditional_volatility_positive(self, returns):
        """Test that conditional volatility is always positive."""
        model = GARCH(returns, p=1, q=1)
        result = model.fit()
        assert np.all(result.conditional_volatility > 0)

    def test_stationarity_constraint(self, returns):
        """Test that alpha + beta < 1 for stationarity."""
        model = GARCH(returns, p=1, q=1)
        result = model.fit()
        alpha = result.params["alpha[1]"]
        beta = result.params["beta[1]"]
        assert alpha + beta < 1.0
```

### Validation Against R or Stata

For models with R (`rugarch`) or Stata equivalents, add validation tests:

```python
def test_against_rugarch_reference(self):
    """Validate GARCH(1,1) against R rugarch package."""
    # R reference values (from validated R script)
    r_params = {
        "omega": 1.05e-06,
        "alpha[1]": 0.089,
        "beta[1]": 0.901,
    }

    model = GARCH(returns, p=1, q=1)
    result = model.fit()

    for param, r_val in r_params.items():
        np.testing.assert_allclose(
            result.params[param], r_val, rtol=1e-2,
            err_msg=f"{param} doesn't match R rugarch"
        )
```

---

## Building Documentation

ArchBox uses MkDocs with Material theme:

```bash
# Local preview with auto-reload
mkdocs serve

# Build static site
mkdocs build
```

Documentation source lives in `docs/`. API reference, tutorials, and theory pages are written in Markdown with MkDocs Material admonitions, tabs, and MathJax equations.

### MathJax Equations

Use `$...$` for inline math and `$$...$$` for display math:

```markdown
The GARCH(1,1) conditional variance is $\sigma_t^2 = \omega + \alpha \epsilon_{t-1}^2 + \beta \sigma_{t-1}^2$.

$$
\sigma_t^2 = \omega + \sum_{i=1}^{q} \alpha_i \epsilon_{t-i}^2 + \sum_{j=1}^{p} \beta_j \sigma_{t-j}^2
$$
```

---

## Pull Request Process

### Step-by-Step

1. **Create a feature branch**:
    ```bash
    git checkout -b feature/my-new-feature
    ```

2. **Make changes**: code, tests, documentation.

3. **Run checks locally**:
    ```bash
    pytest tests/ -v
    ruff check archbox/
    ruff format archbox/ --check
    ```

4. **Commit with a clear message**:
    ```bash
    git commit -m "feat(models): Add FIGARCH model

    - Implements Baillie, Bollerslev & Mikkelsen (1996)
    - Adds fractional differencing operator
    - Includes 12 unit tests with R validation

    Closes #42"
    ```

5. **Push and open a PR**:
    ```bash
    git push origin feature/my-new-feature
    ```

6. **Fill out the PR template and address review comments.**

### PR Checklist

- [ ] Tests pass locally (`pytest tests/ -v`)
- [ ] Linter passes (`ruff check archbox/`)
- [ ] New code has tests
- [ ] Public API has docstrings (NumPy style)
- [ ] Documentation updated (if applicable)
- [ ] Exports added to `__init__.py` (if applicable)

---

## Areas Needing Contributions

We especially welcome contributions in these areas:

| Area | Priority | Description |
|------|----------|-------------|
| GPU acceleration | High | CuPy/JAX backends for large-scale estimation |
| Bayesian GARCH | High | MCMC estimation for GARCH models |
| Copula models | Medium | Copula-based multivariate volatility |
| Streaming/online | Medium | Real-time volatility updating |
| Additional tests | Medium | Validation against R `rugarch`, Stata `arch` |
| Tutorials | Low | Applied examples with real financial data |
| Translations | Low | Documentation in other languages |

---

## Reporting Issues

File issues on [GitHub](https://github.com/NodesEcon/archbox/issues) with:

1. A clear title describing the problem
2. **Minimal reproducible example** (MRE)
3. Expected vs. actual behavior
4. ArchBox version: `pip show garchbox`
5. Python version: `python --version`

---

## Recognition

Contributors are recognized in:

- The [Changelog](changelog.md)
- Release notes

---

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

## Questions?

- **General questions**: [GitHub Discussions](https://github.com/NodesEcon/archbox/discussions)
- **Bug reports**: [GitHub Issues](https://github.com/NodesEcon/archbox/issues)
- **Feature requests**: [GitHub Issues](https://github.com/NodesEcon/archbox/issues) with `[Feature]` label

---

## See Also

- [Code of Conduct](code-of-conduct.md) — Community standards
- [Changelog](changelog.md) — Version history
- [Roadmap](roadmap.md) — Planned features
- [API Reference](../api/index.md) — Full API documentation
