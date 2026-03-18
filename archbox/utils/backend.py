"""Backend management for archbox.

Controls whether numba-accelerated or pure Python implementations are used.
"""

from __future__ import annotations

from typing import Literal

from archbox.utils.numba_core import HAS_NUMBA

# Current backend setting
_BACKEND: Literal["auto", "numba", "python"] = "auto"


def set_backend(backend: Literal["auto", "numba", "python"]) -> None:
    """Set the computation backend.

    Parameters
    ----------
    backend : str
        Backend to use:
        - 'auto': use numba if available, else python
        - 'numba': force numba (raises if not installed)
        - 'python': force pure python

    Raises
    ------
    ImportError
        If backend='numba' but numba is not installed.
    ValueError
        If backend is not recognized.
    """
    global _BACKEND  # noqa: PLW0603
    valid = ("auto", "numba", "python")
    if backend not in valid:
        msg = f"Unknown backend '{backend}'. Valid: {valid}"
        raise ValueError(msg)
    if backend == "numba" and not HAS_NUMBA:
        msg = "numba is not installed. Install with: pip install numba"
        raise ImportError(msg)
    _BACKEND = backend


def get_backend() -> str:
    """Get the current active backend.

    Returns
    -------
    str
        'numba' or 'python' (resolves 'auto').
    """
    if _BACKEND == "auto":
        return "numba" if HAS_NUMBA else "python"
    return _BACKEND


def use_numba() -> bool:
    """Check if numba should be used for current configuration.

    Returns
    -------
    bool
        True if numba should be used.
    """
    backend = get_backend()
    return backend == "numba"


def get_garch_recursion():  # type: ignore[no-untyped-def]
    """Get the appropriate GARCH recursion function.

    Returns
    -------
    callable
        garch_recursion_numba or garch_recursion_python.
    """
    if use_numba():
        from archbox.utils.numba_core import garch_recursion_numba

        return garch_recursion_numba
    else:
        from archbox.utils.numba_core import garch_recursion_python

        return garch_recursion_python


def get_egarch_recursion():  # type: ignore[no-untyped-def]
    """Get the appropriate EGARCH recursion function.

    Returns
    -------
    callable
        egarch_recursion_numba or egarch_recursion_python.
    """
    if use_numba():
        from archbox.utils.numba_core import egarch_recursion_numba

        return egarch_recursion_numba
    else:
        from archbox.utils.numba_core import egarch_recursion_python

        return egarch_recursion_python


def get_hamilton_filter():  # type: ignore[no-untyped-def]
    """Get the appropriate Hamilton filter function.

    Returns
    -------
    callable
        hamilton_filter_numba (always, as it has pure Python fallback via decorator).
    """
    from archbox.utils.numba_core import hamilton_filter_numba

    return hamilton_filter_numba


def get_dcc_recursion():  # type: ignore[no-untyped-def]
    """Get the appropriate DCC recursion function.

    Returns
    -------
    callable
        dcc_recursion_numba (always, as it has pure Python fallback via decorator).
    """
    from archbox.utils.numba_core import dcc_recursion_numba

    return dcc_recursion_numba
