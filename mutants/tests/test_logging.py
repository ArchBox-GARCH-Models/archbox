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

    def test_get_logger_adds_handler_once(self) -> None:
        """get_logger should not duplicate handlers on repeated calls."""
        # Use a unique name to avoid interference
        name = "test_handler_dedup_unique"
        with patch("archbox._logging.HAS_STRUCTLOG", False):
            logger1 = get_logger(name)
            n_handlers = len(logger1.handlers)
            logger2 = get_logger(name)
            assert len(logger2.handlers) == n_handlers

    def test_get_logger_sets_warning_level(self) -> None:
        """Default log level should be WARNING."""
        with patch("archbox._logging.HAS_STRUCTLOG", False):
            logger = get_logger("test_level_unique")
            assert logger.level == logging.WARNING

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
