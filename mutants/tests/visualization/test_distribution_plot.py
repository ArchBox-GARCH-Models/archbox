"""Tests for distribution fit plots."""

from __future__ import annotations

from unittest.mock import MagicMock

import matplotlib
import numpy as np
import pytest

matplotlib.use("Agg")

from archbox.visualization.distribution_plot import plot_distribution_fit


@pytest.fixture
def mock_results():
    """Create mock results with standardized residuals."""
    rng = np.random.default_rng(42)
    T = 1000
    std_resid = rng.standard_normal(T)

    results = MagicMock()
    results.std_resid = std_resid
    results.resid = std_resid * 0.01
    results.conditional_volatility = np.full(T, 0.01)
    return results


class TestPlotDistributionFit:
    """Test plot_distribution_fit."""

    def test_generates_figure(self, mock_results):
        fig = plot_distribution_fit(mock_results)
        assert fig is not None

    def test_has_4_panels(self, mock_results):
        fig = plot_distribution_fit(mock_results)
        axes = fig.get_axes()
        assert len(axes) == 4

    def test_normal_distribution(self, mock_results):
        fig = plot_distribution_fit(mock_results, dist_name="normal")
        assert fig is not None

    def test_studentt_distribution(self, mock_results):
        fig = plot_distribution_fit(mock_results, dist_name="studentt")
        assert fig is not None

    def test_skewt_distribution(self, mock_results):
        fig = plot_distribution_fit(mock_results, dist_name="skewt")
        assert fig is not None

    def test_unknown_distribution_raises(self, mock_results):
        with pytest.raises(ValueError, match="Unknown distribution"):
            plot_distribution_fit(mock_results, dist_name="invalid")
