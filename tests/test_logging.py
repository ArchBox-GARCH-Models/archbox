"""Tests for archbox._logging module."""

from __future__ import annotations

import logging
from unittest.mock import patch

import pytest

from archbox._logging import HAS_STRUCTLOG, configure_logging, get_logger


class TestGetLogger:
    """Tests for get_logger function."""

    def test_get_logger_returns_logger(self) -> None:
        """get_logger should return a logger object."""
        logger = get_logger("test")
        assert logger is not None

    def test_get_logger_prefixes_name(self) -> None:
        """Logger name should be prefixed with 'archbox.'."""
        if not HAS_STRUCTLOG:
            logger = get_logger("mymodule")
            assert logger.name == "archbox.mymodule"

    def test_get_logger_adds_no_handler(self) -> None:
        """get_logger must not attach handlers to module loggers (library convention)."""
        name = "test_handler_dedup_unique"
        with patch("archbox._logging.HAS_STRUCTLOG", False):
            logger1 = get_logger(name)
            assert logger1.handlers == []
            logger2 = get_logger(name)
            assert logger2.handlers == []

    def test_get_logger_leaves_level_unset(self) -> None:
        """Module loggers must inherit their level, not pin it to WARNING."""
        with patch("archbox._logging.HAS_STRUCTLOG", False):
            logger = get_logger("test_level_unique")
            assert logger.level == logging.NOTSET

    def test_library_root_has_only_null_handler_by_default(self) -> None:
        """Importing archbox must not install a StreamHandler on the library logger."""
        root = logging.getLogger("archbox")
        null_handlers = [h for h in root.handlers if isinstance(h, logging.NullHandler)]
        assert null_handlers, "archbox root logger should carry a NullHandler"

    def test_records_propagate_to_library_root(self) -> None:
        """Module loggers propagate to 'archbox', so applications can capture them."""
        with patch("archbox._logging.HAS_STRUCTLOG", False):
            logger = get_logger("propagation_test_unique")
        assert logger.propagate is True
        assert logger.name.startswith("archbox.")

    @pytest.mark.skipif(not HAS_STRUCTLOG, reason="structlog not installed")
    def test_get_logger_with_structlog(self) -> None:
        """When structlog is available, get_logger should return a structlog logger."""
        logger = get_logger("structlog_test")
        assert logger is not None

    def test_get_logger_without_structlog(self) -> None:
        """When structlog is not available, should fall back to stdlib logging."""
        with patch("archbox._logging.HAS_STRUCTLOG", False):
            logger = get_logger("fallback_test_unique")
            assert isinstance(logger, logging.Logger)


class TestConfigureLogging:
    """Tests for configure_logging function."""

    @pytest.mark.skipif(not HAS_STRUCTLOG, reason="structlog not installed")
    def test_configure_with_structlog(self) -> None:
        """configure_logging with use_structlog=True should not raise."""
        configure_logging(level="DEBUG", use_structlog=True)

    def test_configure_without_structlog(self) -> None:
        """configure_logging with use_structlog=False should configure stdlib."""
        configure_logging(level="INFO", use_structlog=False)

    def test_configure_invalid_level_falls_back(self) -> None:
        """Invalid level string should fall back to WARNING."""
        # Should not raise
        configure_logging(level="NONEXISTENT", use_structlog=False)

    def test_configure_all_valid_levels(self) -> None:
        """All standard logging levels should work."""
        for level in ["DEBUG", "INFO", "WARNING", "ERROR"]:
            configure_logging(level=level, use_structlog=False)

    def test_configure_does_not_stack_handlers(self) -> None:
        """Repeated configure_logging calls must not duplicate stream handlers."""
        root = logging.getLogger("archbox")
        configure_logging(level="INFO", use_structlog=False)
        n_after_first = len(root.handlers)
        configure_logging(level="DEBUG", use_structlog=False)
        assert len(root.handlers) == n_after_first
        assert root.level == logging.DEBUG
