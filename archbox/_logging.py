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

# Library convention (see the "Configuring Logging for a Library" section of the
# Python logging HOWTO): archbox attaches only a NullHandler to its root logger.
# Nothing is emitted unless the *application* configures logging, either with
# `logging.basicConfig()` / its own handlers or with `configure_logging()` below.
_ROOT_LOGGER = logging.getLogger("archbox")
_ROOT_LOGGER.addHandler(logging.NullHandler())


def get_logger(name: str) -> Any:
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

    return logging.getLogger(f"archbox.{name}")


def configure_logging(level: str = "WARNING", use_structlog: bool = True) -> None:
    """Configure archbox logging.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR).
    use_structlog : bool
        Use structlog if available.

    Notes
    -----
    Importing archbox never configures logging on its own; call this function
    (or configure the standard library ``logging`` module yourself) to opt in to
    log output.
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
        numeric_level = getattr(logging, level.upper(), logging.WARNING)
        # Opt-in output: attach a single stream handler to the archbox root
        # logger. Repeated calls only adjust the level, they do not stack
        # handlers (which would duplicate every record).
        for existing in _ROOT_LOGGER.handlers:
            if isinstance(existing, logging.StreamHandler) and not isinstance(
                existing, logging.NullHandler
            ):
                break
        else:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter(_LOG_FORMAT))
            _ROOT_LOGGER.addHandler(handler)
        _ROOT_LOGGER.setLevel(numeric_level)
