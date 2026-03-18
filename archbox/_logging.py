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

    logger = logging.getLogger(f"archbox.{name}")
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(_LOG_FORMAT))
        logger.addHandler(handler)
        logger.setLevel(logging.WARNING)
    return logger


def configure_logging(level: str = "WARNING", use_structlog: bool = True) -> None:
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
