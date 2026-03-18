"""Tests for report transformers."""

from __future__ import annotations

from unittest.mock import MagicMock

import numpy as np
import pytest

from archbox.report.transformers.garch import GARCHTransformer
from archbox.report.transformers.multivariate import MultivariateTransformer
from archbox.report.transformers.regime import RegimeTransformer
from archbox.report.transformers.risk import RiskTransformer


@pytest.fixture
def mock_garch_results():
    """Create mock GARCH results."""
    results = MagicMock()
    results.model_name = "GARCH(1,1)"
    results.nobs = 2500
    results.params = np.array([1.5e-6, 0.08, 0.91])
    results.param_names = ["omega", "alpha[1]", "beta[1]"]
    results.std_errors = np.array([3e-7, 0.01, 0.01])
    results.tvalues = np.array([5.0, 8.0, 91.0])
    results.pvalues = np.array([0.0001, 0.0001, 0.0001])
    results.persistence = 0.99
    results.unconditional_variance = 1.5e-4
    results.loglikelihood = 8500.0
    results.aic = -16990.0
    results.bic = -16970.0
    results.hqic = -16983.0
    results.conditional_volatility = np.abs(np.random.default_rng(42).standard_normal(2500)) * 0.01
    results.std_resid = np.random.default_rng(42).standard_normal(2500)
    results.arch_lm = {"stat": 1.5, "pvalue": 0.22}
    results.ljung_box_z2 = {"stat": 10.2, "pvalue": 0.45}
    results.sign_bias = {"stat": 0.8, "pvalue": 0.42}
    return results


@pytest.fixture
def mock_regime_results():
    """Create mock regime-switching results."""
    rng = np.random.default_rng(42)
    T = 500
    K = 2

    smoothed_probs = np.zeros((T, K))
    for t in range(T):
        p = 0.8 if rng.random() > 0.3 else 0.2
        smoothed_probs[t, 0] = p
        smoothed_probs[t, 1] = 1 - p

    results = MagicMock()
    results.model_name = "MS-GARCH(2)"
    results.n_regimes = 2
    results.nobs = T
    results.transition_matrix = np.array([[0.97, 0.03], [0.05, 0.95]])
    results.smoothed_probs = smoothed_probs
    results.regime_params = [
        {"omega": 1e-6, "alpha": 0.05, "beta": 0.90},
        {"omega": 5e-6, "alpha": 0.15, "beta": 0.80},
    ]
    results.loglikelihood = 4200.0
    results.aic = -8390.0
    results.bic = -8360.0
    return results


@pytest.fixture
def mock_risk_results():
    """Create mock risk analysis results."""
    rng = np.random.default_rng(42)
    T = 1000
    returns = rng.standard_normal(T) * 0.01
    var = -np.abs(rng.standard_normal(T) * 0.01) - 0.015
    violations = returns < var

    results = MagicMock()
    results.model_name = "GARCH VaR"
    results.confidence_level = 0.99
    results.returns = returns
    results.var = var
    results.es = var * 1.3
    results.violations = violations
    results.nobs = T
    return results


class TestGARCHTransformer:
    """Test GARCHTransformer."""

    def test_transform_returns_dict(self, mock_garch_results):
        t = GARCHTransformer()
        ctx = t.transform(mock_garch_results)
        assert isinstance(ctx, dict)

    def test_extracts_params_table(self, mock_garch_results):
        t = GARCHTransformer()
        ctx = t.transform(mock_garch_results)
        assert "params_table" in ctx
        assert len(ctx["params_table"]) == 3
        assert ctx["params_table"][0]["name"] == "omega"

    def test_extracts_persistence(self, mock_garch_results):
        t = GARCHTransformer()
        ctx = t.transform(mock_garch_results)
        assert ctx["persistence"] == 0.99

    def test_computes_half_life(self, mock_garch_results):
        t = GARCHTransformer()
        ctx = t.transform(mock_garch_results)
        assert ctx["half_life"] is not None
        assert ctx["half_life"] > 0

    def test_extracts_diagnostics(self, mock_garch_results):
        t = GARCHTransformer()
        ctx = t.transform(mock_garch_results)
        assert "diagnostics" in ctx
        assert "arch_lm" in ctx["diagnostics"]

    def test_extracts_info_criteria(self, mock_garch_results):
        t = GARCHTransformer()
        ctx = t.transform(mock_garch_results)
        assert ctx["loglikelihood"] == 8500.0
        assert ctx["aic"] == -16990.0

    def test_extracts_volatility_stats(self, mock_garch_results):
        t = GARCHTransformer()
        ctx = t.transform(mock_garch_results)
        assert "volatility_stats" in ctx
        assert "annualized_mean" in ctx["volatility_stats"]

    def test_extracts_residual_stats(self, mock_garch_results):
        t = GARCHTransformer()
        ctx = t.transform(mock_garch_results)
        assert "residual_stats" in ctx
        assert "skewness" in ctx["residual_stats"]
        assert "kurtosis" in ctx["residual_stats"]


class TestRegimeTransformer:
    """Test RegimeTransformer."""

    def test_transform_returns_dict(self, mock_regime_results):
        t = RegimeTransformer()
        ctx = t.transform(mock_regime_results)
        assert isinstance(ctx, dict)

    def test_extracts_transition_matrix(self, mock_regime_results):
        t = RegimeTransformer()
        ctx = t.transform(mock_regime_results)
        assert "transition_matrix" in ctx
        assert len(ctx["transition_matrix"]) == 2

    def test_computes_expected_durations(self, mock_regime_results):
        t = RegimeTransformer()
        ctx = t.transform(mock_regime_results)
        assert "expected_durations" in ctx
        durations = ctx["expected_durations"]
        assert len(durations) == 2
        assert durations[0]["duration"] > 0

    def test_regime_classification(self, mock_regime_results):
        t = RegimeTransformer()
        ctx = t.transform(mock_regime_results)
        assert "regime_classification" in ctx
        assert "counts" in ctx["regime_classification"]
        assert sum(ctx["regime_classification"]["counts"]) == 500


class TestRiskTransformer:
    """Test RiskTransformer."""

    def test_transform_returns_dict(self, mock_risk_results):
        t = RiskTransformer()
        ctx = t.transform(mock_risk_results)
        assert isinstance(ctx, dict)

    def test_extracts_backtest(self, mock_risk_results):
        t = RiskTransformer()
        ctx = t.transform(mock_risk_results)
        assert "backtest" in ctx
        assert "n_violations" in ctx["backtest"]
        assert "violation_ratio" in ctx["backtest"]

    def test_computes_traffic_light(self, mock_risk_results):
        t = RiskTransformer()
        ctx = t.transform(mock_risk_results)
        assert "traffic_light" in ctx
        assert ctx["traffic_light"]["zone"] in ("green", "yellow", "red")

    def test_extracts_var_stats(self, mock_risk_results):
        t = RiskTransformer()
        ctx = t.transform(mock_risk_results)
        assert "var_stats" in ctx
        assert "mean" in ctx["var_stats"]

    def test_extracts_es_stats(self, mock_risk_results):
        t = RiskTransformer()
        ctx = t.transform(mock_risk_results)
        assert "es_stats" in ctx


class TestMultivariateTransformer:
    """Test MultivariateTransformer."""

    def test_transform_returns_dict(self):
        results = MagicMock()
        results.model_name = "DCC-GARCH"
        results.n_series = 3
        results.series_names = ["A", "B", "C"]
        results.nobs = 500
        results.loglikelihood = 3000.0
        results.aic = -5990.0
        results.bic = -5970.0
        results.dcc_a = 0.05
        results.dcc_b = 0.93
        results.dcc_persistence = 0.98
        del results.univariate_results
        del results.dynamic_correlations

        t = MultivariateTransformer()
        ctx = t.transform(results)
        assert isinstance(ctx, dict)
        assert ctx["model_name"] == "DCC-GARCH"
        assert ctx["n_series"] == 3
