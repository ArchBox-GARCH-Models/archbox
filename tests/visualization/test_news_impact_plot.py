"""Tests for news impact curve plots."""

from __future__ import annotations

from unittest.mock import MagicMock

import matplotlib
import numpy as np
import pytest

matplotlib.use("Agg")

from archbox.visualization.news_impact_plot import plot_news_impact, plot_news_impact_comparison


@pytest.fixture
def mock_garch_results():
    """Create mock GARCH results."""
    rng = np.random.default_rng(42)
    T = 500
    results = MagicMock()
    results.resid = rng.standard_normal(T) * 0.01
    results.conditional_volatility = np.abs(rng.standard_normal(T)) * 0.01 + 0.005
    results.params = np.array([1.5e-6, 0.08, 0.91])
    results.model_name = "GARCH(1,1)"
    # Remove news_impact so fallback is used
    del results.news_impact
    return results


@pytest.fixture
def mock_egarch_results():
    """Create mock EGARCH results with asymmetry."""
    rng = np.random.default_rng(123)
    T = 500
    results = MagicMock()
    results.resid = rng.standard_normal(T) * 0.01
    results.conditional_volatility = np.abs(rng.standard_normal(T)) * 0.01 + 0.005
    results.model_name = "EGARCH(1,1)"

    # Provide news_impact method that shows asymmetry
    sigma_bar = float(np.mean(results.conditional_volatility))

    def news_impact(n_points: int = 200, n_sigma: float = 3.0):
        eps = np.linspace(-n_sigma * sigma_bar, n_sigma * sigma_bar, n_points)
        # Asymmetric: negative shocks have larger impact
        sigma2 = sigma_bar**2 + 0.15 * eps**2 - 0.05 * eps * (eps < 0)
        return eps, sigma2

    results.news_impact = news_impact
    return results


class TestPlotNewsImpact:
    """Test plot_news_impact function."""

    def test_generates_figure(self, mock_garch_results):
        fig = plot_news_impact(mock_garch_results)
        assert fig is not None
        axes = fig.get_axes()
        assert len(axes) >= 1

    def test_egarch_asymmetry(self, mock_egarch_results):
        """News impact for EGARCH should show asymmetry."""
        fig = plot_news_impact(mock_egarch_results)
        assert fig is not None

        # Get the plotted data from the first line
        ax = fig.get_axes()[0]
        lines = ax.get_lines()
        assert len(lines) >= 1

        # Verify the curve exists
        xdata = lines[0].get_xdata()
        ydata = lines[0].get_ydata()
        assert len(xdata) > 0
        assert len(ydata) > 0

        # For EGARCH, negative shocks should produce higher variance
        mid = len(xdata) // 2
        left_max = np.max(ydata[:mid])  # negative shocks
        right_max = np.max(ydata[mid:])  # positive shocks
        assert left_max > right_max, "EGARCH should show asymmetry"

    def test_custom_theme(self, mock_garch_results):
        fig = plot_news_impact(mock_garch_results, theme="academic")
        assert fig is not None


class TestPlotNewsImpactComparison:
    """Test plot_news_impact_comparison function."""

    def test_comparison(self, mock_garch_results, mock_egarch_results):
        fig = plot_news_impact_comparison(
            [mock_garch_results, mock_egarch_results],
            labels=["GARCH", "EGARCH"],
        )
        assert fig is not None
        ax = fig.get_axes()[0]
        # Should have 2 model curves + vertical line
        lines = ax.get_lines()
        assert len(lines) >= 2

    def test_auto_labels(self, mock_garch_results, mock_egarch_results):
        fig = plot_news_impact_comparison([mock_garch_results, mock_egarch_results])
        assert fig is not None
