# Installation

## Requirements

- Python >= 3.11
- NumPy >= 1.24
- SciPy >= 1.10
- pandas >= 2.0
- matplotlib >= 3.7

## Install from PyPI

```bash
pip install archbox
```

## Install from source

```bash
git clone https://github.com/nodesecon/archbox.git
cd archbox
pip install -e ".[dev]"
```

## Optional dependencies

### Numba acceleration

For significantly faster model fitting:

```bash
pip install archbox[numba]
```

This enables JIT-compiled inner loops for GARCH recursion, Hamilton filter, and DCC recursion.

### Documentation

To build the documentation locally:

```bash
pip install archbox[docs]
mkdocs serve
```

## Verify installation

```python
import archbox
print(f"archbox version: {archbox.__version__}")

from archbox.datasets import load_dataset
sp500 = load_dataset('sp500')
print(f"SP500 dataset: {len(sp500)} observations")
```
