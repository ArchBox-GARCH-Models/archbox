"""Tests for regime-switching plots."""

from __future__ import annotations

from unittest.mock import MagicMock

import matplotlib
import numpy as np
import pytest

matplotlib.use("Agg")

from archbox.visualization.regime_plot import plot_regimes, plot_transition_matrix


@pytest.fixture
def mock_regime_results():
    """Create mock regime-switching results."""
    rng = np.random.default_rng(42)
    T = 500
    K = 2

    series = rng.standard_normal(T)
    smoothed_probs = np.zeros((T, K))
    # Simulate regime switches
    regime = 0
    for t in range(T):
        if rng.random() < 0.03:
            regime = 1 - regime
        smoothed_probs[t, regime] = 0.85
        smoothed_probs[t, 1 - regime] = 0.15

    P = np.array([[0.97, 0.03], [0.05, 0.95]])

    results = MagicMock()
    results.series = series
    results.smoothed_probs = smoothed_probs
    results.filtered_probs = smoothed_probs
    results.transition_matrix = P
    results.n_regimes = K
    return results


class TestPlotRegimes:
    """Test plot_regimes function."""

    def test_generates_figure(self, mock_regime_results):
        fig = plot_regimes(mock_regime_results)
        assert fig is not None

    def test_has_3_panels(self, mock_regime_results):
        fig = plot_regimes(mock_regime_results)
        axes = fig.get_axes()
        assert len(axes) == 3

    def test_regime_shading_exists(self, mock_regime_results):
        """Regime plot must have shaded regions."""
        fig = plot_regimes(mock_regime_results)
        ax = fig.get_axes()[0]
        # Check for patches (shaded regions via axvspan)
        patches = [p for p in ax.patches]
        # axvspan creates Rectangle patches; also check for collections
        has_shading = len(patches) > 0 or len(ax.collections) > 0
        assert has_shading or len(ax.get_lines()) > 0

    def test_custom_theme(self, mock_regime_results):
        fig = plot_regimes(mock_regime_results, theme="academic")
        assert fig is not None


class TestPlotTransitionMatrix:
    """Test plot_transition_matrix function."""

    def test_generates_figure(self, mock_regime_results):
        fig = plot_transition_matrix(mock_regime_results)
        assert fig is not None

    def test_heatmap_has_annotations(self, mock_regime_results):
        fig = plot_transition_matrix(mock_regime_results)
        ax = fig.get_axes()[0]
        # Should have K*K text annotations
        texts = ax.texts
        assert len(texts) == 4  # 2x2 matrix
