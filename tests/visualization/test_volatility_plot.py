"""Tests for volatility plot."""

from __future__ import annotations

from unittest.mock import MagicMock

import matplotlib
import numpy as np
import pytest

matplotlib.use("Agg")

from archbox.visualization.export import export_pdf, export_png, export_svg
from archbox.visualization.volatility_plot import plot_variance_persistence, plot_volatility


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
    results.persistence = 0.95
    return results


class TestPlotVolatility:
    """Test plot_volatility function."""

    def test_generates_figure(self, mock_results):
        fig = plot_volatility(mock_results)
        assert fig is not None
        axes = fig.get_axes()
        assert len(axes) == 3

    def test_annualize(self, mock_results):
        fig = plot_volatility(mock_results, annualize=True)
        assert fig is not None

    def test_custom_theme(self, mock_results):
        fig = plot_volatility(mock_results, theme="academic")
        assert fig is not None

    def test_custom_title(self, mock_results):
        fig = plot_volatility(mock_results, title="Test Title")
        assert fig is not None

    def test_export_png_creates_file(self, mock_results, tmp_path):
        fig = plot_volatility(mock_results)
        outpath = tmp_path / "vol.png"
        result = export_png(fig, outpath)
        assert result.exists()
        assert result.stat().st_size > 0

    def test_export_svg_creates_file(self, mock_results, tmp_path):
        fig = plot_volatility(mock_results)
        outpath = tmp_path / "vol.svg"
        result = export_svg(fig, outpath)
        assert result.exists()
        assert result.stat().st_size > 0

    def test_export_pdf_creates_file(self, mock_results, tmp_path):
        fig = plot_volatility(mock_results)
        outpath = tmp_path / "vol.pdf"
        result = export_pdf(fig, outpath)
        assert result.exists()
        assert result.stat().st_size > 0


class TestPlotVariancePersistence:
    """Test plot_variance_persistence function."""

    def test_generates_figure(self, mock_results):
        fig = plot_variance_persistence(mock_results)
        assert fig is not None

    def test_with_persistence(self, mock_results):
        fig = plot_variance_persistence(mock_results)
        assert fig is not None

    def test_without_persistence(self, mock_results):
        mock_results.persistence = None
        fig = plot_variance_persistence(mock_results)
        assert fig is not None
