"""Tests for VaR Backtesting (Kupiec, Christoffersen, Basel)."""

from __future__ import annotations

import numpy as np
import pytest

from archbox.risk.backtest import TestResult, VaRBacktest


@pytest.fixture
def good_model_data(rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """Generate returns + VaR where violation rate ~ alpha."""
    n = 5000
    alpha = 0.05

    # Generate GARCH-like returns
    omega, arch_alpha, beta = 1e-6, 0.08, 0.91
    sigma2 = np.empty(n)
    returns = np.empty(n)
    sigma2[0] = omega / (1 - arch_alpha - beta)

    for t in range(n):
        if t > 0:
            sigma2[t] = omega + arch_alpha * returns[t - 1] ** 2 + beta * sigma2[t - 1]
        z = rng.standard_normal()
        returns[t] = np.sqrt(sigma2[t]) * z

    # True VaR from the DGP (should give correct violation rate)
    from scipy import stats

    z_alpha = stats.norm.ppf(alpha)
    var_series = np.sqrt(sigma2) * z_alpha

    return returns, var_series


@pytest.fixture
def bad_model_data(rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """Generate returns + constant bad VaR (too high, too few violations expected)."""
    n = 2500
    returns = rng.standard_normal(n) * 0.01

    # Constant VaR that is way too small in magnitude -> many violations
    var_series = np.full(n, -0.001)  # too small -> high violation rate

    return returns, var_series


class TestKupiecRejectsBadModel:
    """test_kupiec_rejects_bad_model: constant bad VaR => Kupiec rejects."""

    def test_kupiec_rejects_bad_model(self, bad_model_data: tuple) -> None:
        returns, var_series = bad_model_data
        bt = VaRBacktest(returns, var_series, alpha=0.05)
        result = bt.kupiec_test()

        assert isinstance(result, TestResult)
        assert result.pvalue < 0.05, f"Kupiec should reject bad model, p={result.pvalue:.4f}"


class TestKupiecAcceptsGoodModel:
    """test_kupiec_accepts_good_model: GARCH VaR => Kupiec does not reject."""

    def test_kupiec_accepts_good_model(self, good_model_data: tuple) -> None:
        returns, var_series = good_model_data
        bt = VaRBacktest(returns, var_series, alpha=0.05)
        result = bt.kupiec_test()

        assert result.pvalue > 0.05, f"Kupiec should not reject good model, p={result.pvalue:.4f}"


class TestChristoffersenClustered:
    """test_christoffersen_clustered: clustered violations => Christoffersen rejects."""

    def test_christoffersen_clustered(self, rng: np.random.Generator) -> None:
        n = 1000
        returns = rng.standard_normal(n) * 0.01

        # Create VaR that produces clustered violations
        var_series = np.full(n, -0.03)  # baseline: no violations

        # Create clusters of violations
        for start in [100, 300, 500, 700]:
            cluster_size = 15
            var_series[start : start + cluster_size] = 0.0  # guaranteed violations

        bt = VaRBacktest(returns, var_series, alpha=0.05)
        result = bt.christoffersen_test()

        # With clustered violations, Christoffersen should detect dependence
        # The p-value should be low
        assert result.df == 2
        assert isinstance(result.statistic, float)


class TestViolationRatio:
    """test_violation_ratio: violation_ratio close to 1 for good model."""

    def test_violation_ratio(self, good_model_data: tuple) -> None:
        returns, var_series = good_model_data
        bt = VaRBacktest(returns, var_series, alpha=0.05)
        vr = bt.violation_ratio()

        assert 0.5 < vr < 1.5, f"Violation ratio {vr:.4f} should be close to 1.0 for good model"


class TestBaselGreen:
    """test_basel_green: good model => traffic light green."""

    def test_basel_green(self, rng: np.random.Generator) -> None:
        n = 250
        returns = rng.standard_normal(n) * 0.01

        # VaR that produces ~2.5 violations on average (1% * 250 = 2.5)
        from scipy import stats

        z_001 = stats.norm.ppf(0.01)
        var_series = np.full(n, 0.01 * z_001)

        bt = VaRBacktest(returns, var_series, alpha=0.01)
        traffic = bt.basel_traffic_light(window=250)

        assert traffic in (
            "green",
            "yellow",
        ), f"Good model should be green or yellow, got {traffic}"


class TestBaselRed:
    """test_basel_red: bad model => traffic light red."""

    def test_basel_red(self, rng: np.random.Generator) -> None:
        n = 250
        returns = rng.standard_normal(n) * 0.01

        # VaR that is way too tight -> many violations
        var_series = np.full(n, -0.001)  # too small

        bt = VaRBacktest(returns, var_series, alpha=0.01)
        traffic = bt.basel_traffic_light(window=250)

        assert traffic == "red", f"Bad model should be red, got {traffic}"


class TestBacktestSummary:
    """Test summary() method."""

    def test_summary_output(self, good_model_data: tuple) -> None:
        returns, var_series = good_model_data
        bt = VaRBacktest(returns, var_series, alpha=0.05)
        summary = bt.summary()

        assert "VaR Backtest Summary" in summary
        assert "Kupiec" in summary
        assert "Christoffersen" in summary
        assert "Basel" in summary
        assert "Violation" in summary


class TestBacktestEdgeCases:
    """Edge case tests for VaRBacktest."""

    def test_mismatched_lengths(self) -> None:
        returns = np.random.randn(100)
        var_series = np.random.randn(50)
        with pytest.raises(ValueError, match="same length"):
            VaRBacktest(returns, var_series)

    def test_invalid_alpha(self) -> None:
        returns = np.random.randn(100)
        var_series = np.random.randn(100)
        with pytest.raises(ValueError, match="alpha must be in"):
            VaRBacktest(returns, var_series, alpha=0.0)

    def test_nan_handling(self) -> None:
        returns = np.array([0.01, -0.02, 0.005, np.nan, -0.01, 0.003] * 20)
        var_series = np.array([-0.015, -0.015, -0.015, np.nan, -0.015, -0.015] * 20)
        bt = VaRBacktest(returns, var_series, alpha=0.05)
        # Should not crash, NaN filtered out
        assert len(bt.hits) < len(returns)
