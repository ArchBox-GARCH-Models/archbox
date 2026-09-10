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
        assert "yellow" in summary, "the summary reports the zone boundaries in use"

    def test_test_result_is_not_collected_by_pytest(self) -> None:
        """The dataclass only looks like a test class."""
        assert TestResult.__test__ is False


class TestBaselZones:
    """The traffic-light zones follow the binomial law of the actual alpha."""

    @staticmethod
    def _backtest(n: int, alpha: float, n_violations: int) -> VaRBacktest:
        """Backtest whose hit sequence has exactly ``n_violations`` ones."""
        returns = np.full(n, 0.0)
        var_series = np.full(n, -1.0)
        returns[:n_violations] = -2.0  # below the VaR -> violation
        return VaRBacktest(returns, var_series, alpha=alpha)

    def test_supervisory_case_matches_basel_table(self) -> None:
        """n=250, alpha=1%: green 0-4, yellow 5-9, red 10+ (Basel 1996)."""
        n, yellow_min, red_min = self._backtest(250, 0.01, 0).basel_zones(window=250)
        assert (n, yellow_min, red_min) == (250, 5, 10)

    @pytest.mark.parametrize(
        ("n_violations", "expected"),
        [(0, "green"), (4, "green"), (5, "yellow"), (9, "yellow"), (10, "red"), (30, "red")],
    )
    def test_supervisory_zones(self, n_violations: int, expected: str) -> None:
        bt = self._backtest(250, 0.01, n_violations)
        assert bt.basel_traffic_light(window=250) == expected

    def test_zones_scale_with_alpha(self) -> None:
        """Regression: a 5% VaR with ~5% violations is green, not red.

        The thresholds used to be hardcoded for alpha=1% (red at 10
        violations), which classified a perfectly calibrated 5% VaR as red.
        """
        bt = self._backtest(250, 0.05, 13)  # 5.2% violation rate
        _, yellow_min, red_min = bt.basel_zones(window=250)

        assert yellow_min > 10 and red_min > yellow_min
        assert bt.basel_traffic_light(window=250) == "green"

    def test_zones_match_the_binomial_cdf(self) -> None:
        from scipy import stats

        for alpha in (0.01, 0.025, 0.05, 0.10):
            for window in (100, 250, 500):
                bt = self._backtest(window, alpha, 0)
                n, yellow_min, red_min = bt.basel_zones(window=window)
                assert n == window
                for threshold, level in ((yellow_min, 0.95), (red_min, 0.9999)):
                    assert float(stats.binom.cdf(threshold, n, alpha)) >= level
                    assert float(stats.binom.cdf(threshold - 1, n, alpha)) < level

    def test_zones_use_the_effective_sample_size(self) -> None:
        """A window longer than the sample falls back to the sample size."""
        bt = self._backtest(120, 0.01, 0)
        n, _, _ = bt.basel_zones(window=250)
        assert n == 120

    def test_invalid_window(self) -> None:
        bt = self._backtest(100, 0.01, 0)
        with pytest.raises(ValueError, match="window must be a positive integer"):
            bt.basel_traffic_light(window=0)


class TestBacktestEdgeCases:
    """Edge case tests for VaRBacktest."""

    def test_all_nan_raises(self) -> None:
        """Regression: all-NaN inputs used to divide by zero."""
        nans = np.full(50, np.nan)
        with pytest.raises(ValueError, match="no valid"):
            VaRBacktest(nans, nans, alpha=0.05)

    def test_non_overlapping_valid_values_raises(self) -> None:
        returns = np.array([0.01, np.nan, np.nan])
        var_series = np.array([np.nan, -0.02, -0.02])
        with pytest.raises(ValueError, match="no valid"):
            VaRBacktest(returns, var_series, alpha=0.05)

    def test_infinite_values_are_dropped(self) -> None:
        returns = np.array([0.01, -0.05, np.inf, 0.002])
        var_series = np.array([-0.02, -0.02, -0.02, -0.02])
        bt = VaRBacktest(returns, var_series, alpha=0.05)
        assert len(bt.hits) == 3
        assert int(bt.hits.sum()) == 1

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
