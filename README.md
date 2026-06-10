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

ARCH/GARCH volatility models for financial time series.

## Installation

```bash
pip install garchbox
```

The PyPI distribution is named `garchbox`; the import name is `archbox`.

For development:

```bash
pip install -e ".[dev]"
```

## Quick Start

```python
from archbox import GARCH
from archbox.datasets import load_dataset

sp500 = load_dataset('sp500')
returns = sp500['returns']

model = GARCH(returns, p=1, q=1)
results = model.fit()
print(results.summary())
forecast = results.forecast(horizon=10)
```

## License

MIT
