"""Coverage tests for archbox/utils/news_impact.py - plot functions and compare."""

from __future__ import annotations

from unittest.mock import MagicMock

import matplotlib
import numpy as np
import pytest

matplotlib.use("Agg")

from archbox.utils.news_impact import (
    compare_news_impact,
    news_impact_curve,
    plot_news_impact,
)


def _make_mock_model_results():
    """Create mock model and results for news impact curve testing."""
    model = MagicMock()

    def _one_step_variance(eps: float, sigma2_ref: float, params) -> float:
        omega, alpha, beta = 0.01, 0.1, 0.85
        return omega + alpha * eps**2 + beta * sigma2_ref

    model._one_step_variance = _one_step_variance

    results = MagicMock()
    results.conditional_volatility = MagicMock()
    results.conditional_volatility.mean.return_value = 0.01
    results.params = np.array([0.01, 0.1, 0.85])

    return model, results


class TestNewsImpactCurve:
    """Tests for news_impact_curve function."""

    def test_basic(self) -> None:
        model, results = _make_mock_model_results()
        eps, sigma2 = news_impact_curve(model, results, n_points=50)
        assert len(eps) == 50
        assert len(sigma2) == 50
        assert np.all(np.isfinite(sigma2))
        assert np.all(sigma2 > 0)

    def test_custom_range(self) -> None:
        model, results = _make_mock_model_results()
        eps, sigma2 = news_impact_curve(model, results, n_points=20, sigma_range=5.0)
        assert len(eps) == 20

    def test_symmetric_for_garch(self) -> None:
        model, results = _make_mock_model_results()
        eps, sigma2 = news_impact_curve(model, results, n_points=101)
        mid = len(eps) // 2
        # GARCH is symmetric
        for i in range(1, mid):
            np.testing.assert_allclose(sigma2[mid - i], sigma2[mid + i], rtol=1e-10)


class TestPlotNewsImpact:
    """Tests for plot_news_impact function."""

    def test_basic_plot(self) -> None:
        import matplotlib.pyplot as plt

        eps = np.linspace(-0.03, 0.03, 50)
        sigma2 = 0.01 + 0.1 * eps**2
        ax = plot_news_impact(eps, sigma2, model_name="GARCH(1,1)")
        assert ax is not None
        plt.close("all")

    def test_plot_with_existing_ax(self) -> None:
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        eps = np.linspace(-0.03, 0.03, 50)
        sigma2 = 0.01 + 0.1 * eps**2
        returned_ax = plot_news_impact(eps, sigma2, model_name="Test", ax=ax)
        assert returned_ax is ax
        plt.close(fig)


class TestCompareNewsImpact:
    """Tests for compare_news_impact function."""

    def test_compare_multiple_models(self) -> None:
        import matplotlib.pyplot as plt

        model1, results1 = _make_mock_model_results()
        model2, results2 = _make_mock_model_results()
        # Modify model2 to be asymmetric
        def _asymmetric_variance(eps: float, sigma2_ref: float, params) -> float:
            omega, alpha, beta = 0.01, 0.1, 0.85
            gamma = 0.05 if eps < 0 else 0.0
            return omega + (alpha + gamma) * eps**2 + beta * sigma2_ref

        model2._one_step_variance = _asymmetric_variance

        models_results = [
            (model1, results1, "GARCH"),
            (model2, results2, "GJR-GARCH"),
        ]
        ax = compare_news_impact(models_results, n_points=50, sigma_range=2.0)
        assert ax is not None
        plt.close("all")

    def test_compare_with_existing_ax(self) -> None:
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        model1, results1 = _make_mock_model_results()
        models_results = [(model1, results1, "GARCH")]
        returned_ax = compare_news_impact(models_results, ax=ax)
        assert returned_ax is ax
        plt.close(fig)
