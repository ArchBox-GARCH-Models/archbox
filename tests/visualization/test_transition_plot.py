"""Tests for transition function plots."""

from __future__ import annotations

from unittest.mock import MagicMock

import matplotlib
import numpy as np
import pytest

matplotlib.use("Agg")

from archbox.visualization.transition_plot import (
    _compute_transition,
    plot_phase_diagram,
    plot_transition_function,
)


@pytest.fixture
def mock_star_results():
    """Create mock STAR results."""
    rng = np.random.default_rng(42)
    T = 500

    series = np.cumsum(rng.standard_normal(T)) * 0.1
    s_t = series[:-1]  # transition variable = lagged series

    smoothed_probs = np.zeros((T, 2))
    gamma = 3.0
    c = 0.0
    G = 1.0 / (1.0 + np.exp(-gamma * (series - c)))
    smoothed_probs[:, 1] = G
    smoothed_probs[:, 0] = 1 - G

    results = MagicMock()
    results.series = series
    results.transition_variable = s_t
    results.gamma = gamma
    results.c = c
    results.transition_type = "LSTAR"
    results.smoothed_probs = smoothed_probs
    return results


class TestPlotTransitionFunction:
    """Test plot_transition_function."""

    def test_generates_figure(self, mock_star_results):
        fig = plot_transition_function(mock_star_results)
        assert fig is not None

    def test_transition_in_01(self, mock_star_results):
        """G(s) must be in [0, 1]."""
        fig = plot_transition_function(mock_star_results)
        ax = fig.get_axes()[0]
        for line in ax.get_lines():
            ydata = line.get_ydata()
            if len(ydata) > 10:  # Skip reference lines
                assert np.all(ydata >= -0.01), "G(s) should be >= 0"
                assert np.all(ydata <= 1.01), "G(s) should be <= 1"

    def test_multiple_gamma(self, mock_star_results):
        fig = plot_transition_function(mock_star_results, gamma_values=[1.0, 5.0, 10.0])
        assert fig is not None
        ax = fig.get_axes()[0]
        # Main curve + 3 gamma + reference lines
        lines = ax.get_lines()
        assert len(lines) >= 4

    def test_estar_transition(self, mock_star_results):
        mock_star_results.transition_type = "ESTAR"
        fig = plot_transition_function(mock_star_results)
        assert fig is not None


class TestComputeTransition:
    """Test _compute_transition helper."""

    def test_lstar_sigmoid_shape(self):
        s = np.linspace(-5, 5, 100)
        G = _compute_transition(s, gamma=1.0, c=0.0, trans_type="LSTAR")
        assert np.all(G >= 0)
        assert np.all(G <= 1)
        # Should be monotonically increasing
        assert np.all(np.diff(G) >= 0)

    def test_lstar_at_threshold(self):
        G = _compute_transition(np.array([0.0]), gamma=1.0, c=0.0, trans_type="LSTAR")
        assert abs(G[0] - 0.5) < 1e-10

    def test_estar_at_threshold(self):
        G = _compute_transition(np.array([0.0]), gamma=1.0, c=0.0, trans_type="ESTAR")
        assert abs(G[0] - 0.0) < 1e-10  # ESTAR: G(c) = 0

    def test_unknown_type_raises(self):
        with pytest.raises(ValueError, match="Unknown transition type"):
            _compute_transition(np.array([0.0]), gamma=1.0, c=0.0, trans_type="INVALID")


class TestPlotPhaseDiagram:
    """Test plot_phase_diagram."""

    def test_generates_figure(self, mock_star_results):
        fig = plot_phase_diagram(mock_star_results)
        assert fig is not None

    def test_has_scatter(self, mock_star_results):
        fig = plot_phase_diagram(mock_star_results)
        ax = fig.get_axes()[0]
        # Should have scatter collections
        assert len(ax.collections) > 0
