"""Tests for correlation plots."""

from __future__ import annotations

from unittest.mock import MagicMock

import matplotlib
import numpy as np
import pytest

matplotlib.use("Agg")

from archbox.visualization.correlation_plot import (
    plot_correlation_heatmap,
    plot_covariance_decomposition,
    plot_dynamic_correlation,
)


@pytest.fixture
def mock_multivar_results():
    """Create mock multivariate results."""
    rng = np.random.default_rng(42)
    T = 500
    K = 3

    # Dynamic correlations (T, K, K)
    dynamic_corr = np.zeros((T, K, K))
    for t in range(T):
        # Base correlation + small random fluctuation
        rho = 0.3 + 0.1 * np.sin(2 * np.pi * t / 250) + rng.standard_normal() * 0.02
        R = np.eye(K)
        for i in range(K):
            for j in range(i + 1, K):
                R[i, j] = rho + rng.standard_normal() * 0.05
                R[j, i] = R[i, j]
        dynamic_corr[t] = R

    # Dynamic covariances (T, K, K)
    dynamic_cov = np.zeros((T, K, K))
    for t in range(T):
        vols = 0.01 + rng.random(K) * 0.005
        D = np.diag(vols)
        dynamic_cov[t] = D @ dynamic_corr[t] @ D

    results = MagicMock()
    results.dynamic_correlations = dynamic_corr
    results.dynamic_covariances = dynamic_cov
    results.series_names = ["SPY", "TLT", "GLD"]
    return results


class TestPlotDynamicCorrelation:
    """Test plot_dynamic_correlation."""

    def test_generates_figure(self, mock_multivar_results):
        fig = plot_dynamic_correlation(mock_multivar_results, i=0, j=1)
        assert fig is not None

    def test_with_ccc_reference(self, mock_multivar_results):
        fig = plot_dynamic_correlation(mock_multivar_results, i=0, j=1, ccc_reference=True)
        assert fig is not None


class TestPlotCorrelationHeatmap:
    """Test plot_correlation_heatmap."""

    def test_generates_figure(self, mock_multivar_results):
        fig = plot_correlation_heatmap(mock_multivar_results)
        assert fig is not None

    def test_heatmap_kxk_cells(self, mock_multivar_results):
        """Heatmap should have K*K text annotations."""
        fig = plot_correlation_heatmap(mock_multivar_results)
        ax = fig.get_axes()[0]
        texts = ax.texts
        assert len(texts) == 9  # 3x3

    def test_specific_time(self, mock_multivar_results):
        fig = plot_correlation_heatmap(mock_multivar_results, t=100)
        assert fig is not None


class TestPlotCovarianceDecomposition:
    """Test plot_covariance_decomposition."""

    def test_generates_figure(self, mock_multivar_results):
        fig = plot_covariance_decomposition(mock_multivar_results)
        assert fig is not None
