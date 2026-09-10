"""Regression tests for backend state leaking out of the benchmark suite.

Before the fix, ``tests/benchmarks/test_performance.py`` called
``set_backend("python")``, asserted a timing bound, and only then called
``set_backend("auto")``. On a slow machine the assertion fired first, so the
reset never ran and the whole process stayed pinned to the pure-Python backend
for every subsequent test.

These tests are deliberately *not* marked ``benchmark``: they must run in the
default selection, because that is where the leak used to do damage.
"""

from __future__ import annotations

import pytest

from archbox.utils import backend as backend_module
from archbox.utils.backend import set_backend
from tests.benchmarks import conftest as benchmarks_conftest
from tests.benchmarks.backend_state import backend_snapshot


def test_snapshot_restores_backend_after_failure() -> None:
    """A failing assertion inside the snapshot must not leak the backend."""
    set_backend("auto")

    with pytest.raises(AssertionError), backend_snapshot():
        set_backend("python")
        assert backend_module._BACKEND == "python"
        raise AssertionError("simulated benchmark failure")

    assert backend_module._BACKEND == "auto"


def test_snapshot_restores_backend_after_success() -> None:
    """Normal exit restores the previous setting too."""
    set_backend("auto")

    with backend_snapshot():
        set_backend("python")

    assert backend_module._BACKEND == "auto"


def test_restore_backend_fixture_restores_on_failure() -> None:
    """The fixture the benchmarks use provides the same guarantee.

    The fixture body is driven directly (``__wrapped__`` is the undecorated
    generator function) so the assertion does not depend on test ordering.
    """
    set_backend("auto")

    generator = benchmarks_conftest.restore_backend.__wrapped__()
    next(generator)
    set_backend("python")
    assert backend_module._BACKEND == "python"

    with pytest.raises(AssertionError):
        generator.throw(AssertionError("simulated benchmark failure"))

    assert backend_module._BACKEND == "auto"
