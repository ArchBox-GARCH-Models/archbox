"""Fixtures shared by the wall-clock benchmark suite.

The benchmarks in this directory are deselected by default (``addopts`` carries
``-m "not benchmark"``); run them explicitly with::

    pytest tests/benchmarks -m benchmark
"""

from __future__ import annotations

from collections.abc import Iterator

import pytest

from tests.benchmarks.backend_state import backend_snapshot


@pytest.fixture
def restore_backend() -> Iterator[None]:
    """Restore the global computation backend after a test.

    ``set_backend`` mutates module-global state. Without this fixture a failing
    assertion leaves the process pinned to 'python' or 'numba' and silently
    changes the behaviour of every test that runs afterwards.
    """
    with backend_snapshot():
        yield
