---
title: Installation
description: Install ArchBox via pip, conda, or from source with all dependencies
---

# Installation

This guide covers all the ways to install ArchBox and configure optional dependencies for performance and development.

---

## Requirements

| Dependency   | Minimum Version | Purpose                          |
|:-------------|:---------------:|:---------------------------------|
| Python       | >= 3.11         | Language runtime                 |
| NumPy        | >= 1.24         | Array operations                 |
| SciPy        | >= 1.10         | Optimization and distributions   |
| pandas       | >= 2.0          | Time series data structures      |
| matplotlib   | >= 3.7          | Plotting and visualization       |

---

## Install via pip

=== "Basic"

    ```bash
    pip install garchbox
    ```

=== "With Numba acceleration"

    ```bash
    pip install "garchbox[numba]"
    ```

    !!! tip "Recommended for large datasets"

        Numba enables JIT-compiled inner loops for GARCH recursion, Hamilton filter, and DCC estimation, delivering significant speedups on datasets with 5,000+ observations.

=== "All extras"

    ```bash
    pip install "garchbox[numba,dev,docs]"
    ```

!!! note "Package name"

    The package is published on PyPI as **`garchbox`** but imported in Python as **`archbox`**:

    ```python
    import archbox
    print(archbox.__version__)
    ```

---

## Install via conda

If you use conda, you can install the dependencies first and then install ArchBox via pip:

```bash
conda create -n archbox python=3.12 numpy scipy pandas matplotlib
conda activate archbox
pip install garchbox
```

---

## Install for Development

Clone the repository and install in editable mode with development dependencies:

```bash
git clone https://github.com/ArchBox-GARCH-Models/archbox.git
cd archbox
pip install -e ".[dev]"
```

The extras `garchbox` declares:

| Extra   | Packages                                      | Purpose                       |
|:--------|:----------------------------------------------|:------------------------------|
| `numba` | numba >= 0.58                                 | JIT-accelerated inner loops   |
| `dev`   | pytest, pytest-cov, ruff, pyright             | Testing and linting           |
| `docs`  | mkdocs-material, mkdocstrings, pymdown-extensions, mike | Documentation build |

These are the only extras `garchbox` declares. Anything else you see referenced
(for example `garchbox[test]`) is not a real extra -- the test tooling lives in
`dev`.

To run the test suite after installing:

```bash
pytest
```

Wall-clock benchmarks are excluded from the default run. To include them:

```bash
pytest tests/benchmarks -m benchmark -v -s
```

To build and preview the documentation locally:

```bash
pip install -e ".[docs]"
mkdocs serve
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## Optional Dependencies

| Package     | Install Command              | Purpose                                        |
|:------------|:-----------------------------|:-----------------------------------------------|
| numba       | `pip install "garchbox[numba]"` | JIT-compiled GARCH recursion, Hamilton filter, DCC recursion |
| structlog   | `pip install structlog`         | Structured log records from `archbox._logging.configure_logging` |
| jupyterlab  | `pip install jupyterlab`        | Run the tutorials in `examples/` as notebooks |

---

## Verify Installation

Run this script to confirm everything is working:

```python
import archbox
print(f"ArchBox version: {archbox.__version__}")

from archbox.datasets import load_dataset, list_datasets

# List available datasets
print(f"Available datasets: {list_datasets()}")

# Load sample data
sp500 = load_dataset("sp500")
print(f"SP500 dataset: {len(sp500)} observations")
print(f"Columns: {list(sp500.columns)}")
```

Expected output:

```text
ArchBox version: 0.1.0
Available datasets: ['bitcoin', 'ftse100', 'fx_majors', 'ibovespa', ...]
SP500 dataset: 2500 observations
Columns: ['date', 'returns']
```

!!! warning "Import name vs. package name"

    Remember: `pip install garchbox` but `import archbox`. If you get `ModuleNotFoundError: No module named 'archbox'`, check that you installed `garchbox` (with the 'g' prefix).

---

## Troubleshooting

??? question "ModuleNotFoundError: No module named 'archbox'"

    Make sure you installed the correct package name:

    ```bash
    pip install garchbox
    ```

    If using virtual environments, verify the environment is activated:

    ```bash
    which python
    pip list | grep garchbox
    ```

??? question "NumPy/SciPy version conflicts"

    If you encounter version conflicts, create a fresh virtual environment:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/macOS
    # .venv\Scripts\activate   # Windows
    pip install garchbox
    ```

??? question "Numba installation fails"

    Numba requires a compatible LLVM toolchain. On some systems:

    ```bash
    # Try conda instead of pip for Numba
    conda install numba
    pip install garchbox
    ```

??? question "matplotlib backend issues on headless servers"

    If you see errors about missing display on a remote server:

    ```python
    import matplotlib
    matplotlib.use("Agg")  # Non-interactive backend
    import archbox
    ```

    Or set the environment variable:

    ```bash
    export MPLBACKEND=Agg
    ```

??? question "Permission errors during pip install"

    Avoid using `sudo pip install`. Use a virtual environment instead:

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install garchbox
    ```

---

## Next Steps

With ArchBox installed, head to the [Quick Start](quickstart.md) tutorial to estimate your first GARCH model.
