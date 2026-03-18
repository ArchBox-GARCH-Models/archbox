"""Backend management for archbox.

Controls whether numba-accelerated or pure Python implementations are used.
"""

from __future__ import annotations

from typing import Literal

from archbox.utils.numba_core import HAS_NUMBA

# Current backend setting
_BACKEND: Literal["auto", "numba", "python"] = "auto"
from collections.abc import Callable
from typing import Annotated, ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"]  # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):  # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os  # type: ignore

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]  # type: ignore
    if mutant_under_test == "fail":  # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException  # type: ignore

        raise MutmutProgrammaticFailException("Failed programmatically")  # type: ignore
    elif mutant_under_test == "stats":  # type: ignore
        from mutmut.__main__ import record_trampoline_hit  # type: ignore

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)  # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs)  # type: ignore
        return result  # type: ignore
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"  # type: ignore
    if not mutant_under_test.startswith(prefix):  # type: ignore
        result = orig(*call_args, **call_kwargs)  # type: ignore
        return result  # type: ignore
    mutant_name = mutant_under_test.rpartition(".")[-1]  # type: ignore
    if self_arg is not None:  # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)  # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)  # type: ignore
    return result  # type: ignore


def set_backend(backend: Literal["auto", "numba", "python"]) -> None:
    args = [backend]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_set_backend__mutmut_orig, x_set_backend__mutmut_mutants, args, kwargs, None
    )


def x_set_backend__mutmut_orig(backend: Literal["auto", "numba", "python"]) -> None:
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


def x_set_backend__mutmut_1(backend: Literal["auto", "numba", "python"]) -> None:
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
    valid = None
    if backend not in valid:
        msg = f"Unknown backend '{backend}'. Valid: {valid}"
        raise ValueError(msg)
    if backend == "numba" and not HAS_NUMBA:
        msg = "numba is not installed. Install with: pip install numba"
        raise ImportError(msg)
    _BACKEND = backend


def x_set_backend__mutmut_2(backend: Literal["auto", "numba", "python"]) -> None:
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
    valid = ("XXautoXX", "numba", "python")
    if backend not in valid:
        msg = f"Unknown backend '{backend}'. Valid: {valid}"
        raise ValueError(msg)
    if backend == "numba" and not HAS_NUMBA:
        msg = "numba is not installed. Install with: pip install numba"
        raise ImportError(msg)
    _BACKEND = backend


def x_set_backend__mutmut_3(backend: Literal["auto", "numba", "python"]) -> None:
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
    valid = ("AUTO", "numba", "python")
    if backend not in valid:
        msg = f"Unknown backend '{backend}'. Valid: {valid}"
        raise ValueError(msg)
    if backend == "numba" and not HAS_NUMBA:
        msg = "numba is not installed. Install with: pip install numba"
        raise ImportError(msg)
    _BACKEND = backend


def x_set_backend__mutmut_4(backend: Literal["auto", "numba", "python"]) -> None:
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
    valid = ("auto", "XXnumbaXX", "python")
    if backend not in valid:
        msg = f"Unknown backend '{backend}'. Valid: {valid}"
        raise ValueError(msg)
    if backend == "numba" and not HAS_NUMBA:
        msg = "numba is not installed. Install with: pip install numba"
        raise ImportError(msg)
    _BACKEND = backend


def x_set_backend__mutmut_5(backend: Literal["auto", "numba", "python"]) -> None:
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
    valid = ("auto", "NUMBA", "python")
    if backend not in valid:
        msg = f"Unknown backend '{backend}'. Valid: {valid}"
        raise ValueError(msg)
    if backend == "numba" and not HAS_NUMBA:
        msg = "numba is not installed. Install with: pip install numba"
        raise ImportError(msg)
    _BACKEND = backend


def x_set_backend__mutmut_6(backend: Literal["auto", "numba", "python"]) -> None:
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
    valid = ("auto", "numba", "XXpythonXX")
    if backend not in valid:
        msg = f"Unknown backend '{backend}'. Valid: {valid}"
        raise ValueError(msg)
    if backend == "numba" and not HAS_NUMBA:
        msg = "numba is not installed. Install with: pip install numba"
        raise ImportError(msg)
    _BACKEND = backend


def x_set_backend__mutmut_7(backend: Literal["auto", "numba", "python"]) -> None:
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
    valid = ("auto", "numba", "PYTHON")
    if backend not in valid:
        msg = f"Unknown backend '{backend}'. Valid: {valid}"
        raise ValueError(msg)
    if backend == "numba" and not HAS_NUMBA:
        msg = "numba is not installed. Install with: pip install numba"
        raise ImportError(msg)
    _BACKEND = backend


def x_set_backend__mutmut_8(backend: Literal["auto", "numba", "python"]) -> None:
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
    if backend in valid:
        msg = f"Unknown backend '{backend}'. Valid: {valid}"
        raise ValueError(msg)
    if backend == "numba" and not HAS_NUMBA:
        msg = "numba is not installed. Install with: pip install numba"
        raise ImportError(msg)
    _BACKEND = backend


def x_set_backend__mutmut_9(backend: Literal["auto", "numba", "python"]) -> None:
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
        msg = None
        raise ValueError(msg)
    if backend == "numba" and not HAS_NUMBA:
        msg = "numba is not installed. Install with: pip install numba"
        raise ImportError(msg)
    _BACKEND = backend


def x_set_backend__mutmut_10(backend: Literal["auto", "numba", "python"]) -> None:
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
        raise ValueError(None)
    if backend == "numba" and not HAS_NUMBA:
        msg = "numba is not installed. Install with: pip install numba"
        raise ImportError(msg)
    _BACKEND = backend


def x_set_backend__mutmut_11(backend: Literal["auto", "numba", "python"]) -> None:
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
    if backend == "numba" or not HAS_NUMBA:
        msg = "numba is not installed. Install with: pip install numba"
        raise ImportError(msg)
    _BACKEND = backend


def x_set_backend__mutmut_12(backend: Literal["auto", "numba", "python"]) -> None:
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
    if backend != "numba" and not HAS_NUMBA:
        msg = "numba is not installed. Install with: pip install numba"
        raise ImportError(msg)
    _BACKEND = backend


def x_set_backend__mutmut_13(backend: Literal["auto", "numba", "python"]) -> None:
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
    if backend == "XXnumbaXX" and not HAS_NUMBA:
        msg = "numba is not installed. Install with: pip install numba"
        raise ImportError(msg)
    _BACKEND = backend


def x_set_backend__mutmut_14(backend: Literal["auto", "numba", "python"]) -> None:
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
    if backend == "NUMBA" and not HAS_NUMBA:
        msg = "numba is not installed. Install with: pip install numba"
        raise ImportError(msg)
    _BACKEND = backend


def x_set_backend__mutmut_15(backend: Literal["auto", "numba", "python"]) -> None:
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
    if backend == "numba" and HAS_NUMBA:
        msg = "numba is not installed. Install with: pip install numba"
        raise ImportError(msg)
    _BACKEND = backend


def x_set_backend__mutmut_16(backend: Literal["auto", "numba", "python"]) -> None:
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
        msg = None
        raise ImportError(msg)
    _BACKEND = backend


def x_set_backend__mutmut_17(backend: Literal["auto", "numba", "python"]) -> None:
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
        msg = "XXnumba is not installed. Install with: pip install numbaXX"
        raise ImportError(msg)
    _BACKEND = backend


def x_set_backend__mutmut_18(backend: Literal["auto", "numba", "python"]) -> None:
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
        msg = "numba is not installed. install with: pip install numba"
        raise ImportError(msg)
    _BACKEND = backend


def x_set_backend__mutmut_19(backend: Literal["auto", "numba", "python"]) -> None:
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
        msg = "NUMBA IS NOT INSTALLED. INSTALL WITH: PIP INSTALL NUMBA"
        raise ImportError(msg)
    _BACKEND = backend


def x_set_backend__mutmut_20(backend: Literal["auto", "numba", "python"]) -> None:
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
        raise ImportError(None)
    _BACKEND = backend


def x_set_backend__mutmut_21(backend: Literal["auto", "numba", "python"]) -> None:
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
    _BACKEND = None


x_set_backend__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_set_backend__mutmut_1": x_set_backend__mutmut_1,
    "x_set_backend__mutmut_2": x_set_backend__mutmut_2,
    "x_set_backend__mutmut_3": x_set_backend__mutmut_3,
    "x_set_backend__mutmut_4": x_set_backend__mutmut_4,
    "x_set_backend__mutmut_5": x_set_backend__mutmut_5,
    "x_set_backend__mutmut_6": x_set_backend__mutmut_6,
    "x_set_backend__mutmut_7": x_set_backend__mutmut_7,
    "x_set_backend__mutmut_8": x_set_backend__mutmut_8,
    "x_set_backend__mutmut_9": x_set_backend__mutmut_9,
    "x_set_backend__mutmut_10": x_set_backend__mutmut_10,
    "x_set_backend__mutmut_11": x_set_backend__mutmut_11,
    "x_set_backend__mutmut_12": x_set_backend__mutmut_12,
    "x_set_backend__mutmut_13": x_set_backend__mutmut_13,
    "x_set_backend__mutmut_14": x_set_backend__mutmut_14,
    "x_set_backend__mutmut_15": x_set_backend__mutmut_15,
    "x_set_backend__mutmut_16": x_set_backend__mutmut_16,
    "x_set_backend__mutmut_17": x_set_backend__mutmut_17,
    "x_set_backend__mutmut_18": x_set_backend__mutmut_18,
    "x_set_backend__mutmut_19": x_set_backend__mutmut_19,
    "x_set_backend__mutmut_20": x_set_backend__mutmut_20,
    "x_set_backend__mutmut_21": x_set_backend__mutmut_21,
}
x_set_backend__mutmut_orig.__name__ = "x_set_backend"


def get_backend() -> str:
    args = []  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_get_backend__mutmut_orig, x_get_backend__mutmut_mutants, args, kwargs, None
    )


def x_get_backend__mutmut_orig() -> str:
    """Get the current active backend.

    Returns
    -------
    str
        'numba' or 'python' (resolves 'auto').
    """
    if _BACKEND == "auto":
        return "numba" if HAS_NUMBA else "python"
    return _BACKEND


def x_get_backend__mutmut_1() -> str:
    """Get the current active backend.

    Returns
    -------
    str
        'numba' or 'python' (resolves 'auto').
    """
    if _BACKEND != "auto":
        return "numba" if HAS_NUMBA else "python"
    return _BACKEND


def x_get_backend__mutmut_2() -> str:
    """Get the current active backend.

    Returns
    -------
    str
        'numba' or 'python' (resolves 'auto').
    """
    if _BACKEND == "XXautoXX":
        return "numba" if HAS_NUMBA else "python"
    return _BACKEND


def x_get_backend__mutmut_3() -> str:
    """Get the current active backend.

    Returns
    -------
    str
        'numba' or 'python' (resolves 'auto').
    """
    if _BACKEND == "AUTO":
        return "numba" if HAS_NUMBA else "python"
    return _BACKEND


def x_get_backend__mutmut_4() -> str:
    """Get the current active backend.

    Returns
    -------
    str
        'numba' or 'python' (resolves 'auto').
    """
    if _BACKEND == "auto":
        return "XXnumbaXX" if HAS_NUMBA else "python"
    return _BACKEND


def x_get_backend__mutmut_5() -> str:
    """Get the current active backend.

    Returns
    -------
    str
        'numba' or 'python' (resolves 'auto').
    """
    if _BACKEND == "auto":
        return "NUMBA" if HAS_NUMBA else "python"
    return _BACKEND


def x_get_backend__mutmut_6() -> str:
    """Get the current active backend.

    Returns
    -------
    str
        'numba' or 'python' (resolves 'auto').
    """
    if _BACKEND == "auto":
        return "numba" if HAS_NUMBA else "XXpythonXX"
    return _BACKEND


def x_get_backend__mutmut_7() -> str:
    """Get the current active backend.

    Returns
    -------
    str
        'numba' or 'python' (resolves 'auto').
    """
    if _BACKEND == "auto":
        return "numba" if HAS_NUMBA else "PYTHON"
    return _BACKEND


x_get_backend__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_get_backend__mutmut_1": x_get_backend__mutmut_1,
    "x_get_backend__mutmut_2": x_get_backend__mutmut_2,
    "x_get_backend__mutmut_3": x_get_backend__mutmut_3,
    "x_get_backend__mutmut_4": x_get_backend__mutmut_4,
    "x_get_backend__mutmut_5": x_get_backend__mutmut_5,
    "x_get_backend__mutmut_6": x_get_backend__mutmut_6,
    "x_get_backend__mutmut_7": x_get_backend__mutmut_7,
}
x_get_backend__mutmut_orig.__name__ = "x_get_backend"


def use_numba() -> bool:
    args = []  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_use_numba__mutmut_orig, x_use_numba__mutmut_mutants, args, kwargs, None
    )


def x_use_numba__mutmut_orig() -> bool:
    """Check if numba should be used for current configuration.

    Returns
    -------
    bool
        True if numba should be used.
    """
    backend = get_backend()
    return backend == "numba"


def x_use_numba__mutmut_1() -> bool:
    """Check if numba should be used for current configuration.

    Returns
    -------
    bool
        True if numba should be used.
    """
    backend = None
    return backend == "numba"


def x_use_numba__mutmut_2() -> bool:
    """Check if numba should be used for current configuration.

    Returns
    -------
    bool
        True if numba should be used.
    """
    backend = get_backend()
    return backend != "numba"


def x_use_numba__mutmut_3() -> bool:
    """Check if numba should be used for current configuration.

    Returns
    -------
    bool
        True if numba should be used.
    """
    backend = get_backend()
    return backend == "XXnumbaXX"


def x_use_numba__mutmut_4() -> bool:
    """Check if numba should be used for current configuration.

    Returns
    -------
    bool
        True if numba should be used.
    """
    backend = get_backend()
    return backend == "NUMBA"


x_use_numba__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_use_numba__mutmut_1": x_use_numba__mutmut_1,
    "x_use_numba__mutmut_2": x_use_numba__mutmut_2,
    "x_use_numba__mutmut_3": x_use_numba__mutmut_3,
    "x_use_numba__mutmut_4": x_use_numba__mutmut_4,
}
x_use_numba__mutmut_orig.__name__ = "x_use_numba"


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
