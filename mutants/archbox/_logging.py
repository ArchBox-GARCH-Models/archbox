"""Structured logging configuration for archbox."""

from __future__ import annotations

import logging
from typing import Any

try:
    import structlog

    HAS_STRUCTLOG = True
except ImportError:
    HAS_STRUCTLOG = False

_LOG_FORMAT = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
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


def get_logger(name: str) -> Any:
    args = [name]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_get_logger__mutmut_orig, x_get_logger__mutmut_mutants, args, kwargs, None
    )


def x_get_logger__mutmut_orig(name: str) -> Any:
    """Get a logger with the archbox namespace.

    Parameters
    ----------
    name : str
        Logger name (will be prefixed with 'archbox.').

    Returns
    -------
    Logger
        structlog logger if available, else standard logging.Logger.
    """
    if HAS_STRUCTLOG:
        return structlog.get_logger(f"archbox.{name}")

    logger = logging.getLogger(f"archbox.{name}")
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(_LOG_FORMAT))
        logger.addHandler(handler)
        logger.setLevel(logging.WARNING)
    return logger


def x_get_logger__mutmut_1(name: str) -> Any:
    """Get a logger with the archbox namespace.

    Parameters
    ----------
    name : str
        Logger name (will be prefixed with 'archbox.').

    Returns
    -------
    Logger
        structlog logger if available, else standard logging.Logger.
    """
    if HAS_STRUCTLOG:
        return structlog.get_logger(None)

    logger = logging.getLogger(f"archbox.{name}")
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(_LOG_FORMAT))
        logger.addHandler(handler)
        logger.setLevel(logging.WARNING)
    return logger


def x_get_logger__mutmut_2(name: str) -> Any:
    """Get a logger with the archbox namespace.

    Parameters
    ----------
    name : str
        Logger name (will be prefixed with 'archbox.').

    Returns
    -------
    Logger
        structlog logger if available, else standard logging.Logger.
    """
    if HAS_STRUCTLOG:
        return structlog.get_logger(f"archbox.{name}")

    logger = None
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(_LOG_FORMAT))
        logger.addHandler(handler)
        logger.setLevel(logging.WARNING)
    return logger


def x_get_logger__mutmut_3(name: str) -> Any:
    """Get a logger with the archbox namespace.

    Parameters
    ----------
    name : str
        Logger name (will be prefixed with 'archbox.').

    Returns
    -------
    Logger
        structlog logger if available, else standard logging.Logger.
    """
    if HAS_STRUCTLOG:
        return structlog.get_logger(f"archbox.{name}")

    logger = logging.getLogger(None)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(_LOG_FORMAT))
        logger.addHandler(handler)
        logger.setLevel(logging.WARNING)
    return logger


def x_get_logger__mutmut_4(name: str) -> Any:
    """Get a logger with the archbox namespace.

    Parameters
    ----------
    name : str
        Logger name (will be prefixed with 'archbox.').

    Returns
    -------
    Logger
        structlog logger if available, else standard logging.Logger.
    """
    if HAS_STRUCTLOG:
        return structlog.get_logger(f"archbox.{name}")

    logger = logging.getLogger(f"archbox.{name}")
    if logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(_LOG_FORMAT))
        logger.addHandler(handler)
        logger.setLevel(logging.WARNING)
    return logger


def x_get_logger__mutmut_5(name: str) -> Any:
    """Get a logger with the archbox namespace.

    Parameters
    ----------
    name : str
        Logger name (will be prefixed with 'archbox.').

    Returns
    -------
    Logger
        structlog logger if available, else standard logging.Logger.
    """
    if HAS_STRUCTLOG:
        return structlog.get_logger(f"archbox.{name}")

    logger = logging.getLogger(f"archbox.{name}")
    if not logger.handlers:
        handler = None
        handler.setFormatter(logging.Formatter(_LOG_FORMAT))
        logger.addHandler(handler)
        logger.setLevel(logging.WARNING)
    return logger


def x_get_logger__mutmut_6(name: str) -> Any:
    """Get a logger with the archbox namespace.

    Parameters
    ----------
    name : str
        Logger name (will be prefixed with 'archbox.').

    Returns
    -------
    Logger
        structlog logger if available, else standard logging.Logger.
    """
    if HAS_STRUCTLOG:
        return structlog.get_logger(f"archbox.{name}")

    logger = logging.getLogger(f"archbox.{name}")
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(None)
        logger.addHandler(handler)
        logger.setLevel(logging.WARNING)
    return logger


def x_get_logger__mutmut_7(name: str) -> Any:
    """Get a logger with the archbox namespace.

    Parameters
    ----------
    name : str
        Logger name (will be prefixed with 'archbox.').

    Returns
    -------
    Logger
        structlog logger if available, else standard logging.Logger.
    """
    if HAS_STRUCTLOG:
        return structlog.get_logger(f"archbox.{name}")

    logger = logging.getLogger(f"archbox.{name}")
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(None))
        logger.addHandler(handler)
        logger.setLevel(logging.WARNING)
    return logger


def x_get_logger__mutmut_8(name: str) -> Any:
    """Get a logger with the archbox namespace.

    Parameters
    ----------
    name : str
        Logger name (will be prefixed with 'archbox.').

    Returns
    -------
    Logger
        structlog logger if available, else standard logging.Logger.
    """
    if HAS_STRUCTLOG:
        return structlog.get_logger(f"archbox.{name}")

    logger = logging.getLogger(f"archbox.{name}")
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(_LOG_FORMAT))
        logger.addHandler(None)
        logger.setLevel(logging.WARNING)
    return logger


def x_get_logger__mutmut_9(name: str) -> Any:
    """Get a logger with the archbox namespace.

    Parameters
    ----------
    name : str
        Logger name (will be prefixed with 'archbox.').

    Returns
    -------
    Logger
        structlog logger if available, else standard logging.Logger.
    """
    if HAS_STRUCTLOG:
        return structlog.get_logger(f"archbox.{name}")

    logger = logging.getLogger(f"archbox.{name}")
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(_LOG_FORMAT))
        logger.addHandler(handler)
        logger.setLevel(None)
    return logger


x_get_logger__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_get_logger__mutmut_1": x_get_logger__mutmut_1,
    "x_get_logger__mutmut_2": x_get_logger__mutmut_2,
    "x_get_logger__mutmut_3": x_get_logger__mutmut_3,
    "x_get_logger__mutmut_4": x_get_logger__mutmut_4,
    "x_get_logger__mutmut_5": x_get_logger__mutmut_5,
    "x_get_logger__mutmut_6": x_get_logger__mutmut_6,
    "x_get_logger__mutmut_7": x_get_logger__mutmut_7,
    "x_get_logger__mutmut_8": x_get_logger__mutmut_8,
    "x_get_logger__mutmut_9": x_get_logger__mutmut_9,
}
x_get_logger__mutmut_orig.__name__ = "x_get_logger"


def configure_logging(level: str = "WARNING", use_structlog: bool = True) -> None:
    args = [level, use_structlog]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_configure_logging__mutmut_orig, x_configure_logging__mutmut_mutants, args, kwargs, None
    )


def x_configure_logging__mutmut_orig(level: str = "WARNING", use_structlog: bool = True) -> None:
    """Configure archbox logging.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR).
    use_structlog : bool
        Use structlog if available.
    """
    if use_structlog and HAS_STRUCTLOG:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.ConsoleRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, level.upper(), logging.WARNING)
            ),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        logging.basicConfig(level=getattr(logging, level.upper(), logging.WARNING))


def x_configure_logging__mutmut_1(level: str = "XXWARNINGXX", use_structlog: bool = True) -> None:
    """Configure archbox logging.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR).
    use_structlog : bool
        Use structlog if available.
    """
    if use_structlog and HAS_STRUCTLOG:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.ConsoleRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, level.upper(), logging.WARNING)
            ),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        logging.basicConfig(level=getattr(logging, level.upper(), logging.WARNING))


def x_configure_logging__mutmut_2(level: str = "warning", use_structlog: bool = True) -> None:
    """Configure archbox logging.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR).
    use_structlog : bool
        Use structlog if available.
    """
    if use_structlog and HAS_STRUCTLOG:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.ConsoleRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, level.upper(), logging.WARNING)
            ),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        logging.basicConfig(level=getattr(logging, level.upper(), logging.WARNING))


def x_configure_logging__mutmut_3(level: str = "WARNING", use_structlog: bool = False) -> None:
    """Configure archbox logging.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR).
    use_structlog : bool
        Use structlog if available.
    """
    if use_structlog and HAS_STRUCTLOG:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.ConsoleRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, level.upper(), logging.WARNING)
            ),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        logging.basicConfig(level=getattr(logging, level.upper(), logging.WARNING))


def x_configure_logging__mutmut_4(level: str = "WARNING", use_structlog: bool = True) -> None:
    """Configure archbox logging.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR).
    use_structlog : bool
        Use structlog if available.
    """
    if use_structlog or HAS_STRUCTLOG:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.ConsoleRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, level.upper(), logging.WARNING)
            ),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        logging.basicConfig(level=getattr(logging, level.upper(), logging.WARNING))


def x_configure_logging__mutmut_5(level: str = "WARNING", use_structlog: bool = True) -> None:
    """Configure archbox logging.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR).
    use_structlog : bool
        Use structlog if available.
    """
    if use_structlog and HAS_STRUCTLOG:
        structlog.configure(
            processors=None,
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, level.upper(), logging.WARNING)
            ),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        logging.basicConfig(level=getattr(logging, level.upper(), logging.WARNING))


def x_configure_logging__mutmut_6(level: str = "WARNING", use_structlog: bool = True) -> None:
    """Configure archbox logging.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR).
    use_structlog : bool
        Use structlog if available.
    """
    if use_structlog and HAS_STRUCTLOG:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.ConsoleRenderer(),
            ],
            wrapper_class=None,
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        logging.basicConfig(level=getattr(logging, level.upper(), logging.WARNING))


def x_configure_logging__mutmut_7(level: str = "WARNING", use_structlog: bool = True) -> None:
    """Configure archbox logging.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR).
    use_structlog : bool
        Use structlog if available.
    """
    if use_structlog and HAS_STRUCTLOG:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.ConsoleRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, level.upper(), logging.WARNING)
            ),
            context_class=None,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        logging.basicConfig(level=getattr(logging, level.upper(), logging.WARNING))


def x_configure_logging__mutmut_8(level: str = "WARNING", use_structlog: bool = True) -> None:
    """Configure archbox logging.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR).
    use_structlog : bool
        Use structlog if available.
    """
    if use_structlog and HAS_STRUCTLOG:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.ConsoleRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, level.upper(), logging.WARNING)
            ),
            context_class=dict,
            logger_factory=None,
            cache_logger_on_first_use=True,
        )
    else:
        logging.basicConfig(level=getattr(logging, level.upper(), logging.WARNING))


def x_configure_logging__mutmut_9(level: str = "WARNING", use_structlog: bool = True) -> None:
    """Configure archbox logging.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR).
    use_structlog : bool
        Use structlog if available.
    """
    if use_structlog and HAS_STRUCTLOG:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.ConsoleRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, level.upper(), logging.WARNING)
            ),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=None,
        )
    else:
        logging.basicConfig(level=getattr(logging, level.upper(), logging.WARNING))


def x_configure_logging__mutmut_10(level: str = "WARNING", use_structlog: bool = True) -> None:
    """Configure archbox logging.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR).
    use_structlog : bool
        Use structlog if available.
    """
    if use_structlog and HAS_STRUCTLOG:
        structlog.configure(
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, level.upper(), logging.WARNING)
            ),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        logging.basicConfig(level=getattr(logging, level.upper(), logging.WARNING))


def x_configure_logging__mutmut_11(level: str = "WARNING", use_structlog: bool = True) -> None:
    """Configure archbox logging.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR).
    use_structlog : bool
        Use structlog if available.
    """
    if use_structlog and HAS_STRUCTLOG:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.ConsoleRenderer(),
            ],
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        logging.basicConfig(level=getattr(logging, level.upper(), logging.WARNING))


def x_configure_logging__mutmut_12(level: str = "WARNING", use_structlog: bool = True) -> None:
    """Configure archbox logging.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR).
    use_structlog : bool
        Use structlog if available.
    """
    if use_structlog and HAS_STRUCTLOG:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.ConsoleRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, level.upper(), logging.WARNING)
            ),
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        logging.basicConfig(level=getattr(logging, level.upper(), logging.WARNING))


def x_configure_logging__mutmut_13(level: str = "WARNING", use_structlog: bool = True) -> None:
    """Configure archbox logging.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR).
    use_structlog : bool
        Use structlog if available.
    """
    if use_structlog and HAS_STRUCTLOG:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.ConsoleRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, level.upper(), logging.WARNING)
            ),
            context_class=dict,
            cache_logger_on_first_use=True,
        )
    else:
        logging.basicConfig(level=getattr(logging, level.upper(), logging.WARNING))


def x_configure_logging__mutmut_14(level: str = "WARNING", use_structlog: bool = True) -> None:
    """Configure archbox logging.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR).
    use_structlog : bool
        Use structlog if available.
    """
    if use_structlog and HAS_STRUCTLOG:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.ConsoleRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, level.upper(), logging.WARNING)
            ),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
        )
    else:
        logging.basicConfig(level=getattr(logging, level.upper(), logging.WARNING))


def x_configure_logging__mutmut_15(level: str = "WARNING", use_structlog: bool = True) -> None:
    """Configure archbox logging.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR).
    use_structlog : bool
        Use structlog if available.
    """
    if use_structlog and HAS_STRUCTLOG:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.ConsoleRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(None),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        logging.basicConfig(level=getattr(logging, level.upper(), logging.WARNING))


def x_configure_logging__mutmut_16(level: str = "WARNING", use_structlog: bool = True) -> None:
    """Configure archbox logging.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR).
    use_structlog : bool
        Use structlog if available.
    """
    if use_structlog and HAS_STRUCTLOG:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.ConsoleRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(None, level.upper(), logging.WARNING)
            ),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        logging.basicConfig(level=getattr(logging, level.upper(), logging.WARNING))


def x_configure_logging__mutmut_17(level: str = "WARNING", use_structlog: bool = True) -> None:
    """Configure archbox logging.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR).
    use_structlog : bool
        Use structlog if available.
    """
    if use_structlog and HAS_STRUCTLOG:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.ConsoleRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, None, logging.WARNING)
            ),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        logging.basicConfig(level=getattr(logging, level.upper(), logging.WARNING))


def x_configure_logging__mutmut_18(level: str = "WARNING", use_structlog: bool = True) -> None:
    """Configure archbox logging.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR).
    use_structlog : bool
        Use structlog if available.
    """
    if use_structlog and HAS_STRUCTLOG:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.ConsoleRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, level.upper(), None)
            ),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        logging.basicConfig(level=getattr(logging, level.upper(), logging.WARNING))


def x_configure_logging__mutmut_19(level: str = "WARNING", use_structlog: bool = True) -> None:
    """Configure archbox logging.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR).
    use_structlog : bool
        Use structlog if available.
    """
    if use_structlog and HAS_STRUCTLOG:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.ConsoleRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(level.upper(), logging.WARNING)
            ),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        logging.basicConfig(level=getattr(logging, level.upper(), logging.WARNING))


def x_configure_logging__mutmut_20(level: str = "WARNING", use_structlog: bool = True) -> None:
    """Configure archbox logging.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR).
    use_structlog : bool
        Use structlog if available.
    """
    if use_structlog and HAS_STRUCTLOG:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.ConsoleRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(getattr(logging, logging.WARNING)),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        logging.basicConfig(level=getattr(logging, level.upper(), logging.WARNING))


def x_configure_logging__mutmut_21(level: str = "WARNING", use_structlog: bool = True) -> None:
    """Configure archbox logging.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR).
    use_structlog : bool
        Use structlog if available.
    """
    if use_structlog and HAS_STRUCTLOG:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.ConsoleRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(
                    logging,
                    level.upper(),
                )
            ),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        logging.basicConfig(level=getattr(logging, level.upper(), logging.WARNING))


def x_configure_logging__mutmut_22(level: str = "WARNING", use_structlog: bool = True) -> None:
    """Configure archbox logging.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR).
    use_structlog : bool
        Use structlog if available.
    """
    if use_structlog and HAS_STRUCTLOG:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.ConsoleRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, level.lower(), logging.WARNING)
            ),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        logging.basicConfig(level=getattr(logging, level.upper(), logging.WARNING))


def x_configure_logging__mutmut_23(level: str = "WARNING", use_structlog: bool = True) -> None:
    """Configure archbox logging.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR).
    use_structlog : bool
        Use structlog if available.
    """
    if use_structlog and HAS_STRUCTLOG:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.ConsoleRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, level.upper(), logging.WARNING)
            ),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=False,
        )
    else:
        logging.basicConfig(level=getattr(logging, level.upper(), logging.WARNING))


def x_configure_logging__mutmut_24(level: str = "WARNING", use_structlog: bool = True) -> None:
    """Configure archbox logging.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR).
    use_structlog : bool
        Use structlog if available.
    """
    if use_structlog and HAS_STRUCTLOG:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.ConsoleRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, level.upper(), logging.WARNING)
            ),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        logging.basicConfig(level=None)


def x_configure_logging__mutmut_25(level: str = "WARNING", use_structlog: bool = True) -> None:
    """Configure archbox logging.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR).
    use_structlog : bool
        Use structlog if available.
    """
    if use_structlog and HAS_STRUCTLOG:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.ConsoleRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, level.upper(), logging.WARNING)
            ),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        logging.basicConfig(level=getattr(None, level.upper(), logging.WARNING))


def x_configure_logging__mutmut_26(level: str = "WARNING", use_structlog: bool = True) -> None:
    """Configure archbox logging.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR).
    use_structlog : bool
        Use structlog if available.
    """
    if use_structlog and HAS_STRUCTLOG:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.ConsoleRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, level.upper(), logging.WARNING)
            ),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        logging.basicConfig(level=getattr(logging, None, logging.WARNING))


def x_configure_logging__mutmut_27(level: str = "WARNING", use_structlog: bool = True) -> None:
    """Configure archbox logging.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR).
    use_structlog : bool
        Use structlog if available.
    """
    if use_structlog and HAS_STRUCTLOG:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.ConsoleRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, level.upper(), logging.WARNING)
            ),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        logging.basicConfig(level=getattr(logging, level.upper(), None))


def x_configure_logging__mutmut_28(level: str = "WARNING", use_structlog: bool = True) -> None:
    """Configure archbox logging.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR).
    use_structlog : bool
        Use structlog if available.
    """
    if use_structlog and HAS_STRUCTLOG:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.ConsoleRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, level.upper(), logging.WARNING)
            ),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        logging.basicConfig(level=getattr(level.upper(), logging.WARNING))


def x_configure_logging__mutmut_29(level: str = "WARNING", use_structlog: bool = True) -> None:
    """Configure archbox logging.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR).
    use_structlog : bool
        Use structlog if available.
    """
    if use_structlog and HAS_STRUCTLOG:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.ConsoleRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, level.upper(), logging.WARNING)
            ),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        logging.basicConfig(level=getattr(logging, logging.WARNING))


def x_configure_logging__mutmut_30(level: str = "WARNING", use_structlog: bool = True) -> None:
    """Configure archbox logging.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR).
    use_structlog : bool
        Use structlog if available.
    """
    if use_structlog and HAS_STRUCTLOG:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.ConsoleRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, level.upper(), logging.WARNING)
            ),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        logging.basicConfig(
            level=getattr(
                logging,
                level.upper(),
            )
        )


def x_configure_logging__mutmut_31(level: str = "WARNING", use_structlog: bool = True) -> None:
    """Configure archbox logging.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR).
    use_structlog : bool
        Use structlog if available.
    """
    if use_structlog and HAS_STRUCTLOG:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.ConsoleRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, level.upper(), logging.WARNING)
            ),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        logging.basicConfig(level=getattr(logging, level.lower(), logging.WARNING))


x_configure_logging__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_configure_logging__mutmut_1": x_configure_logging__mutmut_1,
    "x_configure_logging__mutmut_2": x_configure_logging__mutmut_2,
    "x_configure_logging__mutmut_3": x_configure_logging__mutmut_3,
    "x_configure_logging__mutmut_4": x_configure_logging__mutmut_4,
    "x_configure_logging__mutmut_5": x_configure_logging__mutmut_5,
    "x_configure_logging__mutmut_6": x_configure_logging__mutmut_6,
    "x_configure_logging__mutmut_7": x_configure_logging__mutmut_7,
    "x_configure_logging__mutmut_8": x_configure_logging__mutmut_8,
    "x_configure_logging__mutmut_9": x_configure_logging__mutmut_9,
    "x_configure_logging__mutmut_10": x_configure_logging__mutmut_10,
    "x_configure_logging__mutmut_11": x_configure_logging__mutmut_11,
    "x_configure_logging__mutmut_12": x_configure_logging__mutmut_12,
    "x_configure_logging__mutmut_13": x_configure_logging__mutmut_13,
    "x_configure_logging__mutmut_14": x_configure_logging__mutmut_14,
    "x_configure_logging__mutmut_15": x_configure_logging__mutmut_15,
    "x_configure_logging__mutmut_16": x_configure_logging__mutmut_16,
    "x_configure_logging__mutmut_17": x_configure_logging__mutmut_17,
    "x_configure_logging__mutmut_18": x_configure_logging__mutmut_18,
    "x_configure_logging__mutmut_19": x_configure_logging__mutmut_19,
    "x_configure_logging__mutmut_20": x_configure_logging__mutmut_20,
    "x_configure_logging__mutmut_21": x_configure_logging__mutmut_21,
    "x_configure_logging__mutmut_22": x_configure_logging__mutmut_22,
    "x_configure_logging__mutmut_23": x_configure_logging__mutmut_23,
    "x_configure_logging__mutmut_24": x_configure_logging__mutmut_24,
    "x_configure_logging__mutmut_25": x_configure_logging__mutmut_25,
    "x_configure_logging__mutmut_26": x_configure_logging__mutmut_26,
    "x_configure_logging__mutmut_27": x_configure_logging__mutmut_27,
    "x_configure_logging__mutmut_28": x_configure_logging__mutmut_28,
    "x_configure_logging__mutmut_29": x_configure_logging__mutmut_29,
    "x_configure_logging__mutmut_30": x_configure_logging__mutmut_30,
    "x_configure_logging__mutmut_31": x_configure_logging__mutmut_31,
}
x_configure_logging__mutmut_orig.__name__ = "x_configure_logging"
