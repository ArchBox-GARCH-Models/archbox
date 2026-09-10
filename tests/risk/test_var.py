"""Tests for Value at Risk (VaR) implementations."""

from __future__ import annotations

from typing import Any

import numpy as np
import pytest
from scipy import stats

from archbox.models.egarch import EGARCH
from archbox.models.garch import GARCH
from archbox.models.gjr_garch import GJRGARCH
from archbox.risk.var import ValueAtRisk


class TestParametricVaRNormal:
    """Parametric VaR under the Normal: mu + sigma_t * Phi^{-1}(alpha)."""

    def test_parametric_var_normal(self, garch_results: Any) -> None:
        var = ValueAtRisk(garch_results, alpha=0.05)
        var_series = var.parametric(dist="normal")

        expected = garch_results.mu + garch_results.conditional_volatility * stats.norm.ppf(0.05)
        np.testing.assert_allclose(var_series, expected, rtol=1e-12)

    def test_default_uses_fitted_distribution(self, garch_results: Any) -> None:
        """With a Gaussian fit, the default and 'normal' agree."""
        var = ValueAtRisk(garch_results, alpha=0.05)
        np.testing.assert_allclose(var.parametric(), var.parametric(dist="normal"), rtol=1e-12)


class TestParametricVaRStudentT:
    """Student-t VaR is heavier-tailed than the Normal and uses the fitted nu."""

    def test_parametric_var_student_t(self, garch_results: Any) -> None:
        var = ValueAtRisk(garch_results, alpha=0.01)

        var_normal = var.parametric(dist="normal")
        var_studentt = var.parametric(dist="studentt", nu=5.0)

        assert np.all(var_studentt < var_normal), (
            "Student-t VaR should be more extreme than Normal VaR"
        )

    def test_uses_fitted_nu_not_the_default(self, garch_t_estimated: Any) -> None:
        """Regression: the fitted nu is used, not the hardcoded nu=8."""
        nu_hat = float(garch_t_estimated._dist_params[0])
        assert abs(nu_hat - 8.0) > 1.0, "fixture should not have a fitted nu near the old default"

        var = ValueAtRisk(garch_t_estimated, alpha=0.01)
        fitted = var.parametric(dist="studentt")

        expected = garch_t_estimated.mu + garch_t_estimated.conditional_volatility * (
            stats.t.ppf(0.01, df=nu_hat) * np.sqrt((nu_hat - 2.0) / nu_hat)
        )
        np.testing.assert_allclose(fitted, expected, rtol=1e-10)

        default_nu = var.parametric(dist="studentt", nu=8.0)
        assert not np.allclose(fitted, default_nu), "explicit nu=8 must differ from the fitted nu"

    def test_fixed_shape_distribution_is_honoured(self, garch_t_results: Any) -> None:
        """A distribution instance with a pinned nu drives the default quantile."""
        var = ValueAtRisk(garch_t_results, alpha=0.01)
        quantile = stats.t.ppf(0.01, df=4.0) * np.sqrt(2.0 / 4.0)

        expected = garch_t_results.mu + garch_t_results.conditional_volatility * quantile
        np.testing.assert_allclose(var.parametric(), expected, rtol=1e-8)

    def test_explicit_nu_without_name_is_student_t(self, garch_results: Any) -> None:
        var = ValueAtRisk(garch_results, alpha=0.01)
        np.testing.assert_allclose(
            var.parametric(nu=6.0), var.parametric(dist="studentt", nu=6.0), rtol=1e-12
        )


class TestReturnScale:
    """Regression: every VaR method lives on the scale of the returns."""

    @staticmethod
    def _reference(returns: np.ndarray) -> float:
        return abs(float(np.quantile(returns, 0.05)))

    def test_historical_on_return_scale(self, garch_results: Any, returns: np.ndarray) -> None:
        var = ValueAtRisk(garch_results, alpha=0.05)
        hist = var.historical(window=250)
        median = float(np.nanmedian(np.abs(hist)))

        reference = self._reference(returns)
        assert 0.3 * reference < median < 3.0 * reference, (
            f"historical VaR {median:.4f} is off the return scale ({reference:.4f})"
        )

    def test_filtered_historical_on_return_scale(
        self, garch_results: Any, returns: np.ndarray
    ) -> None:
        var = ValueAtRisk(garch_results, alpha=0.05)
        median = float(np.nanmedian(np.abs(var.filtered_historical())))

        reference = self._reference(returns)
        assert 0.3 * reference < median < 3.0 * reference

    def test_parametric_on_return_scale(self, garch_results: Any, returns: np.ndarray) -> None:
        var = ValueAtRisk(garch_results, alpha=0.05)
        median = float(np.median(np.abs(var.parametric())))

        reference = self._reference(returns)
        assert 0.3 * reference < median < 3.0 * reference

    def test_monte_carlo_on_return_scale(self, garch_results: Any, returns: np.ndarray) -> None:
        var = ValueAtRisk(garch_results, alpha=0.05)
        value = abs(float(var.monte_carlo(n_sims=20000, seed=0)[0]))

        reference = self._reference(returns)
        assert 0.3 * reference < value < 3.0 * reference


class TestHistoricalDefinition:
    """Historical simulation quantiles the RAW returns, not the residuals."""

    def test_matches_rolling_quantile_of_returns(self, garch_results: Any) -> None:
        var = ValueAtRisk(garch_results, alpha=0.05)
        hist = var.historical(window=250)

        returns = garch_results.mu + garch_results.resid
        for t in (250, 700, len(returns) - 1):
            assert hist[t] == pytest.approx(float(np.quantile(returns[t - 250 : t], 0.05)))

        assert np.all(np.isnan(hist[:250])), "the first `window` values must be NaN"

    def test_not_computed_on_standardized_residuals(self, garch_results: Any) -> None:
        """The old bug returned quantiles of z_t (order of magnitude ~1.9)."""
        var = ValueAtRisk(garch_results, alpha=0.05)
        hist = var.historical(window=250)
        assert float(np.nanmedian(np.abs(hist))) < 0.1

    def test_invalid_window(self, garch_results: Any) -> None:
        var = ValueAtRisk(garch_results, alpha=0.05)
        with pytest.raises(ValueError, match="window must be a positive integer"):
            var.historical(window=0)


class TestFilteredHistoricalDefinition:
    """FHS scales the standardized-residual quantile by the volatility."""

    def test_matches_definition(self, garch_results: Any) -> None:
        var = ValueAtRisk(garch_results, alpha=0.05)
        fhs = var.filtered_historical()

        z = garch_results.std_resid
        sigma = garch_results.conditional_volatility
        for t in (50, 400, len(z) - 1):
            expected = garch_results.mu + sigma[t] * float(np.quantile(z[:t], 0.05))
            assert fhs[t] == pytest.approx(expected)

        assert np.all(np.isnan(fhs[:50]))

    def test_filtered_hs_not_worse_than_hs(self, garch_results: Any) -> None:
        alpha = 0.05
        var = ValueAtRisk(garch_results, alpha=alpha)

        var_hs = var.historical(window=250)
        var_fhs = var.filtered_historical()
        returns = garch_results.mu + garch_results.resid

        valid = ~np.isnan(var_hs) & ~np.isnan(var_fhs)
        viol_hs = float((returns[valid] < var_hs[valid]).mean())
        viol_fhs = float((returns[valid] < var_fhs[valid]).mean())

        assert abs(viol_fhs - alpha) <= abs(viol_hs - alpha) + 0.02


class TestViolationRateParametric:
    """The parametric VaR of a fitted model has a violation rate near alpha."""

    def test_violation_rate_parametric(self, garch_results: Any) -> None:
        alpha = 0.05
        var = ValueAtRisk(garch_results, alpha=alpha)
        var_series = var.parametric()

        returns = garch_results.mu + garch_results.resid
        violations = float((returns < var_series).mean())

        assert abs(violations - alpha) / alpha < 0.30, (
            f"Violation rate {violations:.4f} too far from alpha={alpha}"
        )


class TestMonteCarlo:
    """Monte-Carlo VaR: model-aware, distribution-aware, reproducible."""

    def test_monte_carlo_convergence(self, garch_results: Any) -> None:
        var = ValueAtRisk(garch_results, alpha=0.05)

        small = [var.monte_carlo(n_sims=100, horizon=1, seed=s)[0] for s in range(10)]
        large = [var.monte_carlo(n_sims=10000, horizon=1, seed=s)[0] for s in range(10)]

        assert np.var(large) < np.var(small)

    def test_seed_is_reproducible(self, garch_results: Any) -> None:
        var = ValueAtRisk(garch_results, alpha=0.05)
        first = var.monte_carlo(n_sims=2000, horizon=3, seed=7)
        second = var.monte_carlo(n_sims=2000, horizon=3, seed=7)
        np.testing.assert_array_equal(first, second)
        assert not np.allclose(first, var.monte_carlo(n_sims=2000, horizon=3, seed=8))

    def test_multi_step_is_not_deterministic(self, garch_results: Any) -> None:
        """Regression: h > 1 used to ignore the draw entirely."""
        var = ValueAtRisk(garch_results, alpha=0.05)
        values = np.array([var.monte_carlo(n_sims=4000, horizon=4, seed=s) for s in range(6)])
        assert np.all(values.std(axis=0) > 0), "multi-step VaR must depend on the simulation"

    @pytest.mark.parametrize("model_cls", [GARCH, GJRGARCH, EGARCH])
    def test_one_step_matches_model_forecast(self, returns: np.ndarray, model_cls: type) -> None:
        """The 1-step MC quantile matches each model's own variance forecast."""
        results = model_cls(returns).fit(disp=False)
        var = ValueAtRisk(results, alpha=0.05)

        mc = float(var.monte_carlo(n_sims=200000, seed=3)[0])
        sigma = float(np.sqrt(results.forecast(horizon=1)["variance"][0]))
        analytic = results.mu + sigma * stats.norm.ppf(0.05)

        assert mc == pytest.approx(analytic, rel=0.05)

    @pytest.mark.parametrize("model_cls", [GARCH, GJRGARCH, EGARCH])
    def test_simulated_path_variance_matches_the_forecast(
        self, returns: np.ndarray, model_cls: type
    ) -> None:
        """The simulated multi-step variance tracks each model's own recursion."""
        results = model_cls(returns).fit(disp=False)
        var = ValueAtRisk(results, alpha=0.05)

        sims = var._simulate_future_returns(50000, 5, seed=0)
        empirical = np.var(sims, axis=0)
        forecast = results.forecast(horizon=5)["variance"]

        np.testing.assert_allclose(empirical, forecast, rtol=0.05)

    def test_multi_step_first_element_matches_one_step(self, garch_results: Any) -> None:
        """The path recursion continues the fitted history from the same point."""
        var = ValueAtRisk(garch_results, alpha=0.05)
        one = float(var.monte_carlo(n_sims=100000, horizon=1, seed=11)[0])
        multi = float(var.monte_carlo(n_sims=100000, horizon=3, seed=11)[0])
        assert multi == pytest.approx(one, rel=0.05)

    def test_draws_from_the_fitted_distribution(self, garch_t_results: Any) -> None:
        """A Student-t(4) fit gives a fatter MC tail than the Normal quantile."""
        var = ValueAtRisk(garch_t_results, alpha=0.01)
        mc = float(var.monte_carlo(n_sims=200000, seed=5)[0])

        sigma = float(np.sqrt(garch_t_results.forecast(horizon=1)["variance"][0]))
        normal_var = garch_t_results.mu + sigma * stats.norm.ppf(0.01)
        t_var = garch_t_results.mu + sigma * garch_t_results._fitted_dist().ppf(0.01)

        assert mc < normal_var, "Student-t innovations must produce a fatter tail"
        assert mc == pytest.approx(t_var, rel=0.10)

    def test_horizon_shape(self, garch_results: Any) -> None:
        var = ValueAtRisk(garch_results, alpha=0.05)
        assert var.monte_carlo(n_sims=500, horizon=4, seed=0).shape == (4,)

    def test_requires_fitted_model(self, garch_results: Any) -> None:
        class Fake:
            mu = 0.0
            resid = np.zeros(10)
            std_resid = np.zeros(10)
            conditional_volatility = np.ones(10) * 0.01

        var = ValueAtRisk(Fake(), alpha=0.05)
        with pytest.raises(TypeError, match="requires results from a fitted archbox"):
            var.monte_carlo(n_sims=10)

    def test_invalid_n_sims(self, garch_results: Any) -> None:
        var = ValueAtRisk(garch_results, alpha=0.05)
        with pytest.raises(ValueError, match="n_sims must be a positive integer"):
            var.monte_carlo(n_sims=0)
        with pytest.raises(ValueError, match="horizon must be a positive integer"):
            var.monte_carlo(n_sims=10, horizon=0)


class TestVaREdgeCases:
    """Edge cases for VaR."""

    def test_invalid_alpha(self, garch_results: Any) -> None:
        with pytest.raises(ValueError, match="alpha must be in"):
            ValueAtRisk(garch_results, alpha=0.0)

        with pytest.raises(ValueError, match="alpha must be in"):
            ValueAtRisk(garch_results, alpha=1.0)

    def test_invalid_distribution(self, garch_results: Any) -> None:
        var = ValueAtRisk(garch_results, alpha=0.05)
        with pytest.raises(ValueError, match="Unknown distribution"):
            var.parametric(dist="invalid")

    def test_studentt_nu_too_small(self, garch_results: Any) -> None:
        var = ValueAtRisk(garch_results, alpha=0.05)
        with pytest.raises(ValueError, match="Degrees of freedom"):
            var.parametric(dist="studentt", nu=2.0)

    def test_results_without_the_risk_api(self) -> None:
        class Empty:
            pass

        with pytest.raises(TypeError, match="does not expose the fitted-model risk API"):
            ValueAtRisk(Empty(), alpha=0.05)

    def test_results_without_residuals(self) -> None:
        class NoResid:
            mu = 0.0
            conditional_volatility = np.ones(5)

        with pytest.raises(TypeError, match="exposes no raw residuals"):
            ValueAtRisk(NoResid(), alpha=0.05)

    def test_mismatched_series_lengths(self) -> None:
        class Mismatch:
            mu = 0.0
            conditional_volatility = np.ones(5)
            resid = np.ones(7)

        with pytest.raises(ValueError, match="same length"):
            ValueAtRisk(Mismatch(), alpha=0.05)
