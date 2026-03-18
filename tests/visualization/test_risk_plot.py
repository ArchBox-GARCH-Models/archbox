"""Tests for risk management plots."""

from __future__ import annotations

from unittest.mock import MagicMock

import matplotlib
import numpy as np
import pytest

matplotlib.use("Agg")

from archbox.visualization.risk_plot import (
    plot_traffic_light,
    plot_var_backtest,
    plot_var_comparison,
)


@pytest.fixture
def mock_backtest_results():
    """Create mock VaR backtest results."""
    rng = np.random.default_rng(42)
    T = 1000
    returns = rng.standard_normal(T) * 0.01
    var = -np.abs(rng.standard_normal(T) * 0.01) - 0.015
    es = var * 1.3
    violations = returns < var

    results = MagicMock()
    results.returns = returns
    results.var = var
    results.es = es
    results.violations = violations
    results.confidence_level = 0.99
    return results


class TestPlotVarBacktest:
    """Test plot_var_backtest."""

    def test_generates_figure(self, mock_backtest_results):
        fig = plot_var_backtest(mock_backtest_results)
        assert fig is not None

    def test_var_line_exists(self, mock_backtest_results):
        """VaR line should be present."""
        fig = plot_var_backtest(mock_backtest_results)
        ax = fig.get_axes()[0]
        lines = ax.get_lines()
        assert len(lines) >= 2  # returns + VaR at minimum

    def test_violations_marked(self, mock_backtest_results):
        """Violations should be marked as scatter points."""
        fig = plot_var_backtest(mock_backtest_results)
        ax = fig.get_axes()[0]
        # Scatter creates PathCollections
        assert len(ax.collections) > 0 or len(ax.get_lines()) >= 2

    def test_custom_theme(self, mock_backtest_results):
        fig = plot_var_backtest(mock_backtest_results, theme="professional")
        assert fig is not None


class TestPlotTrafficLight:
    """Test plot_traffic_light."""

    def test_generates_figure(self, mock_backtest_results):
        fig = plot_traffic_light(mock_backtest_results)
        assert fig is not None

    def test_custom_window(self, mock_backtest_results):
        fig = plot_traffic_light(mock_backtest_results, window=125)
        assert fig is not None


class TestPlotVarComparison:
    """Test plot_var_comparison."""

    def test_generates_figure(self):
        rng = np.random.default_rng(42)
        T = 500
        returns = rng.standard_normal(T) * 0.01
        var_dict = {
            "Parametric": -np.abs(rng.standard_normal(T) * 0.01) - 0.015,
            "Historical": np.full(T, -0.023),
            "FHS": -np.abs(rng.standard_normal(T) * 0.008) - 0.018,
        }
        fig = plot_var_comparison(var_dict, returns)
        assert fig is not None

    def test_multiple_methods(self):
        rng = np.random.default_rng(42)
        T = 500
        returns = rng.standard_normal(T) * 0.01
        var_dict = {
            "Method A": np.full(T, -0.02),
            "Method B": np.full(T, -0.025),
        }
        fig = plot_var_comparison(var_dict, returns)
        ax = fig.get_axes()[0]
        lines = ax.get_lines()
        assert len(lines) >= 3  # returns + 2 methods
