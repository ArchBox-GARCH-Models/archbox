"""archbox - ARCH/GARCH volatility models for financial time series.

The most common entry points (model classes, datasets, risk measures) are
imported eagerly.  Every subpackage is additionally reachable as an attribute
of ``archbox`` without an explicit ``import archbox.<name>``; those are resolved
lazily through the module-level ``__getattr__`` so that ``import archbox`` stays
cheap and does not pull in heavyweight optional machinery (matplotlib, the
report/visualization stacks, numba) unless it is actually used.

    >>> import archbox
    >>> archbox.GARCH                     # eager
    >>> archbox.multivariate.DCC          # imported on first attribute access
"""

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING, Any

from archbox.__version__ import __version__
from archbox.datasets import list_datasets, load_dataset
from archbox.experiment import ArchExperiment
from archbox.models import (
    APARCH,
    EGARCH,
    FIGARCH,
    GARCH,
    GARCHM,
    GJRGARCH,
    HARRV,
    IGARCH,
    ComponentGARCH,
)
from archbox.risk import ExpectedShortfall, ValueAtRisk

if TYPE_CHECKING:  # pragma: no cover - import-time typing only
    from archbox import (
        cli,
        core,
        datasets,
        diagnostics,
        distributions,
        estimation,
        experiment,
        models,
        multivariate,
        regime,
        report,
        risk,
        threshold,
        utils,
        visualization,
    )

_LAZY_SUBMODULES: frozenset[str] = frozenset(
    {
        "cli",
        "core",
        "datasets",
        "diagnostics",
        "distributions",
        "estimation",
        "experiment",
        "models",
        "multivariate",
        "regime",
        "report",
        "risk",
        "threshold",
        "utils",
        "visualization",
    }
)

__all__ = [
    "__version__",
    # Univariate models
    "GARCH",
    "EGARCH",
    "GJRGARCH",
    "APARCH",
    "FIGARCH",
    "IGARCH",
    "GARCHM",
    "ComponentGARCH",
    "HARRV",
    # Risk measures
    "ValueAtRisk",
    "ExpectedShortfall",
    # Workflows and data
    "ArchExperiment",
    "load_dataset",
    "list_datasets",
    # Lazily imported subpackages
    "cli",
    "core",
    "datasets",
    "diagnostics",
    "distributions",
    "estimation",
    "experiment",
    "models",
    "multivariate",
    "regime",
    "report",
    "risk",
    "threshold",
    "utils",
    "visualization",
]


def __getattr__(name: str) -> Any:
    """Import subpackages on first attribute access (PEP 562)."""
    if name in _LAZY_SUBMODULES:
        module = importlib.import_module(f"archbox.{name}")
        globals()[name] = module
        return module
    msg = f"module 'archbox' has no attribute {name!r}"
    raise AttributeError(msg)


def __dir__() -> list[str]:
    """Expose eager and lazy names to ``dir()`` and tab completion."""
    return sorted(__all__)
