"""Helper for isolating the global computation-backend setting in tests.

``archbox.utils.backend.set_backend`` mutates a module-global. Benchmarks that
force a backend must put it back even when an assertion fails, otherwise every
test that runs afterwards silently uses the wrong code path.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from archbox.utils import backend as backend_module


@contextmanager
def backend_snapshot() -> Iterator[None]:
    """Restore ``archbox.utils.backend._BACKEND`` on exit, including on error."""
    saved = backend_module._BACKEND
    try:
        yield
    finally:
        backend_module._BACKEND = saved
