"""Tests for diagnostic plots."""

from __future__ import annotations

from unittest.mock import MagicMock

import matplotlib
import numpy as np
import pytest

matplotlib.use("Agg")

from archbox.visualization.diagnostics_plot import plot_diagnostics


@pytest.fixture
def mock_results():
    """Create mock results for testing."""
    rng = np.random.default_rng(42)
    T = 500
    resid = rng.standard_normal(T) * 0.01
    sigma = np.abs(rng.standard_normal(T)) * 0.01 + 0.005
    std_resid = resid / np.maximum(sigma, 1e-12)

    results = MagicMock()
    results.resid = resid
    results.conditional_volatility = sigma
    results.std_resid = std_resid
    return results


class TestPlotDiagnostics:
    """Test plot_diagnostics function."""

    def test_generates_figure(self, mock_results):
        fig = plot_diagnostics(mock_results)
        assert fig is not None

    def test_has_4_panels(self, mock_results):
        """Diagnostic plot must have exactly 4 subplots."""
        fig = plot_diagnostics(mock_results)
        axes = fig.get_axes()
        assert len(axes) == 4

    def test_panel_titles(self, mock_results):
        """Each panel should have a title."""
        fig = plot_diagnostics(mock_results)
        axes = fig.get_axes()
        titles = [ax.get_title() for ax in axes]
        assert "Standardized Residuals" in titles
        assert r"ACF of $z_t^2$" in titles
        assert "QQ-Plot (Normal)" in titles
        assert "Histogram of Standardized Residuals" in titles

    def test_custom_theme(self, mock_results):
        fig = plot_diagnostics(mock_results, theme="risk")
        assert fig is not None

    def test_custom_title(self, mock_results):
        fig = plot_diagnostics(mock_results, title="GARCH(1,1) Diagnostics")
        assert fig is not None

    def test_fallback_std_resid(self, mock_results):
        """Should compute std_resid from resid/sigma when not available."""
        mock_results.std_resid = None
        fig = plot_diagnostics(mock_results)
        assert fig is not None
        axes = fig.get_axes()
        assert len(axes) == 4
