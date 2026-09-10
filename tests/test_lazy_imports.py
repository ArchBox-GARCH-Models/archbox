"""Tests for the lazy subpackage machinery in ``archbox/__init__.py``.

Two things are asserted here:

1. Every subpackage is reachable as an attribute of ``archbox`` without an
   explicit ``import archbox.<name>`` (PEP 562 module ``__getattr__``).
2. A bare ``import archbox`` does not drag in matplotlib. It used to, because
   ``archbox.experiment`` imported ``matplotlib.pyplot`` at module scope, which
   cost every importer the full matplotlib import even when they never plotted.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

import archbox

LAZY_SUBMODULES = [
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

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("name", LAZY_SUBMODULES)
def test_subpackage_reachable_as_attribute(name: str) -> None:
    """`archbox.<subpackage>` resolves without an explicit import."""
    module = getattr(archbox, name)
    assert module.__name__ == f"archbox.{name}"


def test_documented_entry_points() -> None:
    """The two names the README promises after a bare `import archbox`."""
    assert archbox.GARCH.__name__ == "GARCH"
    assert archbox.multivariate.DCC.__name__ == "DCC"


def test_unknown_attribute_raises_attribute_error() -> None:
    """__getattr__ must not swallow typos into an ImportError or None."""
    with pytest.raises(AttributeError, match="no attribute 'does_not_exist'"):
        _ = archbox.does_not_exist  # type: ignore[attr-defined]


def test_all_names_are_resolvable() -> None:
    """Everything advertised in __all__ can actually be got at."""
    for name in archbox.__all__:
        assert getattr(archbox, name) is not None


def test_dir_lists_lazy_submodules() -> None:
    """dir(archbox) surfaces the lazily imported subpackages."""
    listed = dir(archbox)
    for name in LAZY_SUBMODULES:
        assert name in listed


def _import_in_fresh_interpreter(code: str) -> str:
    """Run `code` in a clean interpreter rooted at the repo, return its stdout."""
    proc = subprocess.run(  # noqa: S603
        [sys.executable, "-c", code],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=True,
    )
    return proc.stdout.strip()


def test_bare_import_does_not_load_matplotlib() -> None:
    """`import archbox` must stay free of matplotlib (regression test)."""
    out = _import_in_fresh_interpreter("import sys, archbox; print('matplotlib' in sys.modules)")
    assert out == "False", "importing archbox pulled in matplotlib"


def test_bare_import_does_not_load_visualization_or_report() -> None:
    """The heavyweight plotting/report subpackages are not imported eagerly."""
    out = _import_in_fresh_interpreter(
        "import sys, archbox; "
        "print(any(m.startswith(('archbox.visualization', 'archbox.report')) "
        "for m in sys.modules))"
    )
    assert out == "False"


def test_plotting_still_works_after_lazy_import() -> None:
    """Moving the matplotlib import inside the method did not break plotting."""
    import matplotlib

    matplotlib.use("Agg")

    from archbox.experiment import ComparisonResult

    comparison = ComparisonResult(
        model_names=["GARCH(1,1)", "EGARCH(1,1)"],
        criteria={"aic": [-100.0, -110.0]},
    )
    ax = comparison.plot_comparison("aic")
    assert ax is not None
