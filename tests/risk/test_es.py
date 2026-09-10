"""Tests for Expected Shortfall (ES) implementations."""

from __future__ import annotations

from typing import Any

import numpy as np
import pytest
from scipy import stats

from archbox.risk.es import ExpectedShortfall
from archbox.risk.var import ValueAtRisk


class TestESGreaterThanVaR:
    """ES is always at least as extreme as the VaR at the same level."""

    def test_es_greater_than_var_normal(self, garch_results: Any) -> None:
        alpha = 0.05
        var_series = ValueAtRisk(garch_results, alpha=alpha).parametric(dist="normal")
        es_series = ExpectedShortfall(garch_results, alpha=alpha).parametric(dist="normal")

        assert np.all(es_series <= var_series)

    def test_es_greater_than_var_studentt(self, garch_results: Any) -> None:
        alpha = 0.05
        var_series = ValueAtRisk(garch_results, alpha=alpha).parametric(dist="studentt", nu=5.0)
        es_series = ExpectedShortfall(garch_results, alpha=alpha).parametric(
            dist="studentt", nu=5.0
        )

        assert np.all(es_series <= var_series)

    def test_es_greater_than_var_fitted_dist(self, garch_t_results: Any) -> None:
        alpha = 0.01
        var_series = ValueAtRisk(garch_t_results, alpha=alpha).parametric()
        es_series = ExpectedShortfall(garch_t_results, alpha=alpha).parametric()

        assert np.all(es_series <= var_series)


class TestESNormalFormula:
    """ES under the Normal matches the analytical formula."""

    def test_es_normal_formula(self, garch_results: Any) -> None:
        alpha = 0.05
        es_series = ExpectedShortfall(garch_results, alpha=alpha).parametric(dist="normal")

        sigma = garch_results.conditional_volatility
        z_alpha = stats.norm.ppf(alpha)
        expected = garch_results.mu - sigma * stats.norm.pdf(z_alpha) / alpha

        np.testing.assert_allclose(es_series, expected, rtol=1e-12)


class TestESStudentTFormula:
    """ES under the Student-t matches the analytical formula."""

    def test_es_student_t_formula(self, garch_results: Any) -> None:
        alpha = 0.05
        nu = 6.0
        es_series = ExpectedShortfall(garch_results, alpha=alpha).parametric(dist="studentt", nu=nu)

        sigma = garch_results.conditional_volatility
        t_alpha = stats.t.ppf(alpha, df=nu)
        f_nu = stats.t.pdf(t_alpha, df=nu)
        scale = np.sqrt((nu - 2) / nu)
        es_factor = (f_nu / alpha) * ((nu + t_alpha**2) / (nu - 1))
        expected = garch_results.mu - sigma * es_factor * scale

        np.testing.assert_allclose(es_series, expected, rtol=1e-12)

    def test_uses_fitted_nu_not_the_default(self, garch_t_estimated: Any) -> None:
        """Regression: the fitted nu drives the ES, not the hardcoded nu=8."""
        nu_hat = float(garch_t_estimated._dist_params[0])
        assert abs(nu_hat - 8.0) > 1.0

        es = ExpectedShortfall(garch_t_estimated, alpha=0.01)
        fitted = es.parametric(dist="studentt")

        t_alpha = stats.t.ppf(0.01, df=nu_hat)
        f_nu = stats.t.pdf(t_alpha, df=nu_hat)
        factor = (f_nu / 0.01) * ((nu_hat + t_alpha**2) / (nu_hat - 1.0))
        expected = (
            garch_t_estimated.mu
            - garch_t_estimated.conditional_volatility * factor * np.sqrt((nu_hat - 2.0) / nu_hat)
        )
        np.testing.assert_allclose(fitted, expected, rtol=1e-10)
        assert not np.allclose(fitted, es.parametric(dist="studentt", nu=8.0))


class TestESNumericTail:
    """The generic tail integral agrees with the analytical formulas."""

    def test_numeric_tail_matches_student_t_closed_form(self, garch_t_results: Any) -> None:
        alpha = 0.025
        es = ExpectedShortfall(garch_t_results, alpha=alpha)

        # The fitted distribution has a pinned nu -> generic (numeric) branch.
        numeric = es.parametric()
        closed_form = es.parametric(dist="studentt", nu=4.0)

        np.testing.assert_allclose(numeric, closed_form, rtol=2e-3)


class TestESReturnScale:
    """Regression: ES lives on the scale of the returns."""

    def test_historical_and_parametric_on_return_scale(
        self, garch_results: Any, returns: np.ndarray
    ) -> None:
        reference = abs(float(np.mean(returns[returns <= np.quantile(returns, 0.05)])))
        es = ExpectedShortfall(garch_results, alpha=0.05)

        hist = float(np.nanmedian(np.abs(es.historical(window=250))))
        param = float(np.median(np.abs(es.parametric())))
        fhs = float(np.nanmedian(np.abs(es.filtered_historical())))

        for value, name in ((hist, "historical"), (param, "parametric"), (fhs, "fhs")):
            assert 0.3 * reference < value < 3.0 * reference, f"{name} ES off the return scale"

    def test_historical_not_computed_on_standardized_residuals(self, garch_results: Any) -> None:
        es = ExpectedShortfall(garch_results, alpha=0.05)
        assert float(np.nanmedian(np.abs(es.historical(window=250)))) < 0.1


class TestESHistorical:
    """Historical ES."""

    def test_matches_definition(self, garch_results: Any) -> None:
        es = ExpectedShortfall(garch_results, alpha=0.05)
        es_hs = es.historical(window=250)

        returns = garch_results.mu + garch_results.resid
        t = 900
        window = returns[t - 250 : t]
        tail = window[window <= np.quantile(window, 0.05)]
        assert es_hs[t] == pytest.approx(float(np.mean(tail)))

    def test_es_historical_less_than_var(self, garch_results: Any) -> None:
        alpha = 0.05
        var_hs = ValueAtRisk(garch_results, alpha=alpha).historical(window=250)
        es_hs = ExpectedShortfall(garch_results, alpha=alpha).historical(window=250)

        valid = ~np.isnan(var_hs) & ~np.isnan(es_hs)
        assert np.all(es_hs[valid] <= var_hs[valid])

    def test_invalid_window(self, garch_results: Any) -> None:
        es = ExpectedShortfall(garch_results, alpha=0.05)
        with pytest.raises(ValueError, match="window must be a positive integer"):
            es.historical(window=-1)


class TestESFilteredHS:
    """Filtered Historical Simulation ES."""

    def test_matches_definition(self, garch_results: Any) -> None:
        es = ExpectedShortfall(garch_results, alpha=0.05)
        es_fhs = es.filtered_historical()

        z = garch_results.std_resid
        t = 900
        z_window = z[:t]
        tail = z_window[z_window <= np.quantile(z_window, 0.05)]
        expected = garch_results.mu + garch_results.conditional_volatility[t] * float(np.mean(tail))
        assert es_fhs[t] == pytest.approx(expected)

    def test_es_fhs_less_than_var(self, garch_results: Any) -> None:
        alpha = 0.05
        var_fhs = ValueAtRisk(garch_results, alpha=alpha).filtered_historical()
        es_fhs = ExpectedShortfall(garch_results, alpha=alpha).filtered_historical()

        valid = ~np.isnan(var_fhs) & ~np.isnan(es_fhs)
        assert np.all(es_fhs[valid] <= var_fhs[valid] + 1e-12)


class TestESMonteCarlo:
    """Monte-Carlo ES."""

    def test_monte_carlo_beyond_var(self, garch_results: Any) -> None:
        alpha = 0.05
        es = ExpectedShortfall(garch_results, alpha=alpha).monte_carlo(n_sims=20000, seed=1)
        var = ValueAtRisk(garch_results, alpha=alpha).monte_carlo(n_sims=20000, seed=1)

        assert es.shape == var.shape
        assert np.all(es <= var)

    def test_monte_carlo_matches_parametric_one_step(self, garch_results: Any) -> None:
        alpha = 0.05
        es_calc = ExpectedShortfall(garch_results, alpha=alpha)
        mc = float(es_calc.monte_carlo(n_sims=200000, seed=2)[0])

        sigma = float(np.sqrt(garch_results.forecast(horizon=1)["variance"][0]))
        z_alpha = stats.norm.ppf(alpha)
        analytic = garch_results.mu - sigma * stats.norm.pdf(z_alpha) / alpha

        assert mc == pytest.approx(analytic, rel=0.05)

    def test_seed_is_reproducible(self, garch_results: Any) -> None:
        es = ExpectedShortfall(garch_results, alpha=0.05)
        np.testing.assert_array_equal(
            es.monte_carlo(n_sims=1000, horizon=2, seed=4),
            es.monte_carlo(n_sims=1000, horizon=2, seed=4),
        )


class TestESEdgeCases:
    """Edge cases for ES."""

    def test_invalid_alpha(self, garch_results: Any) -> None:
        with pytest.raises(ValueError, match="alpha must be in"):
            ExpectedShortfall(garch_results, alpha=0.0)

    def test_invalid_distribution(self, garch_results: Any) -> None:
        es = ExpectedShortfall(garch_results, alpha=0.05)
        with pytest.raises(ValueError, match="Unknown distribution"):
            es.parametric(dist="invalid")

    def test_studentt_nu_too_small(self, garch_results: Any) -> None:
        es = ExpectedShortfall(garch_results, alpha=0.05)
        with pytest.raises(ValueError, match="Degrees of freedom"):
            es.parametric(dist="studentt", nu=2.0)
