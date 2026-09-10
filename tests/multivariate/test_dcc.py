"""Tests for DCC-GARCH model."""

from __future__ import annotations

import numpy as np

from archbox.multivariate.dcc import DCC
from archbox.multivariate.utils import is_positive_definite


class TestDCCGARCH:
    """Test DCC-GARCH model."""

    def test_dcc_correlation_bounds(self, synthetic_returns):
        """R_{ij,t} should be in [-1, 1] for all t, i, j."""
        model = DCC(synthetic_returns)
        results = model.fit(disp=False)

        R_t = results.dynamic_correlation
        assert np.all(R_t >= -1.0 - 1e-8), "R has elements < -1"
        assert np.all(R_t <= 1.0 + 1e-8), "R has elements > 1"

    def test_dcc_correlation_diagonal_one(self, synthetic_returns):
        """R_{ii,t} should be 1 for all t, i."""
        model = DCC(synthetic_returns)
        results = model.fit(disp=False)

        R_t = results.dynamic_correlation
        T, k, _ = R_t.shape

        for t in range(0, T, 50):
            np.testing.assert_array_almost_equal(
                np.diag(R_t[t]),
                np.ones(k),
                decimal=6,
                err_msg=f"Diagonal not 1 at t={t}",
            )

    def test_dcc_positive_definite(self, synthetic_returns):
        """H_t should be positive definite for all t."""
        model = DCC(synthetic_returns)
        results = model.fit(disp=False)

        H_t = results.dynamic_covariance
        T = H_t.shape[0]

        for t in range(0, T, 50):
            assert is_positive_definite(H_t[t]), f"H_t not PD at t={t}"

    def test_dcc_persistence(self, synthetic_returns):
        """a + b should be < 1."""
        model = DCC(synthetic_returns)
        results = model.fit(disp=False)

        a, b = results.params[0], results.params[1]
        assert a > 0, f"a should be positive, got {a}"
        assert b > 0, f"b should be positive, got {b}"
        assert a + b < 1.0, f"a + b should be < 1, got {a + b}"

    def test_dcc_forecast_converges_to_qbar(self, synthetic_returns):
        """Forecast correlation should converge to Q_bar for large h."""
        model = DCC(synthetic_returns)
        results = model.fit(disp=False)

        fcast = model.forecast(results, horizon=200)
        R_long = fcast["correlation"][-1]

        # Should converge toward Q_bar (normalized)
        # Check that it's close to a valid correlation matrix
        k = synthetic_returns.shape[1]
        np.testing.assert_array_almost_equal(
            np.diag(R_long),
            np.ones(k),
            decimal=4,
            err_msg="Long-horizon forecast diagonal not 1",
        )

    def test_dcc_dynamic_correlation_varies(self, synthetic_returns):
        """R_t should vary over time (not constant like CCC)."""
        model = DCC(synthetic_returns)
        results = model.fit(disp=False)

        R_t = results.dynamic_correlation

        # Check that not all R_t are identical
        diffs = np.max(np.abs(R_t[1:] - R_t[:-1]), axis=(1, 2))
        assert np.max(diffs) > 1e-6, "DCC correlation appears constant"

    def test_dcc_loglike_finite(self, synthetic_returns):
        """Log-likelihood should be finite."""
        model = DCC(synthetic_returns)
        results = model.fit(disp=False)

        assert np.isfinite(results.loglike)

    def test_dcc_summary(self, synthetic_returns):
        """summary() should return a non-empty string."""
        model = DCC(synthetic_returns)
        results = model.fit(disp=False)
        s = results.summary()
        assert isinstance(s, str)
        assert "DCC-GARCH" in s
        assert "a" in s or "b" in s

    def test_dcc_correlation_symmetric(self, synthetic_returns):
        """R_t should be symmetric for all t."""
        model = DCC(synthetic_returns)
        results = model.fit(disp=False)

        R_t = results.dynamic_correlation
        T = R_t.shape[0]

        for t in range(0, T, 50):
            np.testing.assert_array_almost_equal(
                R_t[t],
                R_t[t].T,
                decimal=10,
                err_msg=f"R_t not symmetric at t={t}",
            )

    def test_dcc_portfolio_volatility(self, synthetic_returns):
        """Portfolio volatility should be positive."""
        model = DCC(synthetic_returns)
        results = model.fit(disp=False)

        k = synthetic_returns.shape[1]
        w = np.ones(k) / k
        port_vol = results.portfolio_volatility(w)

        assert port_vol.shape == (synthetic_returns.shape[0],)
        assert np.all(port_vol >= 0)
        assert np.all(np.isfinite(port_vol))

    def test_dcc_forecast_shapes(self, synthetic_returns):
        """Forecast should return correct shapes."""
        model = DCC(synthetic_returns)
        results = model.fit(disp=False)

        fcast = model.forecast(results, horizon=10)
        k = synthetic_returns.shape[1]

        assert fcast["covariance"].shape == (10, k, k)
        assert fcast["correlation"].shape == (10, k, k)

    def test_dcc_with_fx_data(self, fx_returns):
        """DCC should work with FX data (3 series)."""
        model = DCC(fx_returns)
        results = model.fit(disp=False)

        assert results.dynamic_correlation.shape == (2000, 3, 3)
        assert results.dynamic_covariance.shape == (2000, 3, 3)
        assert np.isfinite(results.loglike)

        a, b = results.params[0], results.params[1]
        assert 0 < a < 1
        assert 0 < b < 1
        assert a + b < 1

    def test_dcc_improves_over_ccc(self, synthetic_returns):
        """DCC log-likelihood should be >= CCC (more flexible model)."""
        from archbox.multivariate.ccc import CCC

        ccc_model = CCC(synthetic_returns)
        ccc_results = ccc_model.fit(disp=False)

        dcc_model = DCC(synthetic_returns)
        dcc_results = dcc_model.fit(disp=False)

        # DCC should have at least as good loglike (or very close)
        # Note: in some cases CCC might be slightly better due to optimization
        assert dcc_results.loglike >= ccc_results.loglike - 1.0, (
            f"DCC loglike ({dcc_results.loglike:.2f}) should be >= "
            f"CCC loglike ({ccc_results.loglike:.2f})"
        )


class TestDCCForecastRecursion:
    """The DCC forecast must project the stored Q path, not R_T."""

    def test_q_path_stored_on_results(self, dcc_returns):
        """The full Q path is stored so the forecast never re-derives it from R."""
        model = DCC(dcc_returns)
        results = model.fit(disp=False)

        q_path = results.extras["q_path"]
        assert q_path.shape == (dcc_returns.shape[0], 3, 3)
        np.testing.assert_allclose(q_path[-1], results.extras["q_last"])
        # Q_T is *not* R_T: its diagonal is not identically one.
        assert not np.allclose(np.diag(q_path[-1]), np.ones(3), atol=1e-6)

    def test_forecast_one_step_matches_recursion(self, dcc_returns):
        """h=1 must equal the in-sample recursion applied one step ahead."""
        from archbox.multivariate.dcc import normalize_q

        model = DCC(dcc_returns)
        results = model.fit(disp=False)

        a, b = results.params
        q_bar = results.extras["q_bar"]
        q_last = results.extras["q_last"]
        z_last = results.extras["z_last"]

        q_next = (1.0 - a - b) * q_bar + a * np.outer(z_last, z_last) + b * q_last
        r_next = normalize_q(q_next)

        fcast = model.forecast(results, horizon=5)
        np.testing.assert_allclose(fcast["correlation"][0], r_next, rtol=1e-12, atol=1e-14)

    def test_forecast_keeps_the_a_z_z_term(self, dcc_returns):
        """Dropping a*z_T z_T' would make h=1 equal the pure mean-reverting step."""
        model = DCC(dcc_returns)
        results = model.fit(disp=False)

        from archbox.multivariate.dcc import normalize_q

        a, b = results.params
        q_bar = results.extras["q_bar"]
        q_last = results.extras["q_last"]
        without_shock = normalize_q((1.0 - a - b) * q_bar + b * q_last)

        fcast = model.forecast(results, horizon=1)
        assert not np.allclose(fcast["correlation"][0], without_shock, atol=1e-6)

    def test_forecast_multi_step_recursion(self, dcc_returns):
        """h>1 uses Q_{T+h} = (1-a-b) Q_bar + (a+b) Q_{T+h-1}."""
        from archbox.multivariate.dcc import normalize_q

        model = DCC(dcc_returns)
        results = model.fit(disp=False)

        a, b = results.params
        q_bar = results.extras["q_bar"]
        q = results.extras["q_last"]
        z_last = results.extras["z_last"]

        q = (1.0 - a - b) * q_bar + a * np.outer(z_last, z_last) + b * q
        q = (1.0 - a - b) * q_bar + (a + b) * q

        fcast = model.forecast(results, horizon=2)
        np.testing.assert_allclose(fcast["correlation"][1], normalize_q(q), rtol=1e-12)

    def test_forecast_uses_univariate_variance_forecast(self, dcc_returns):
        """Covariance forecasts must use ArchResults.forecast, not the last sigma."""
        model = DCC(dcc_returns)
        results = model.fit(disp=False)

        fcast = model.forecast(results, horizon=6)
        diag = np.diagonal(fcast["covariance"], axis1=1, axis2=2)
        for i, res in enumerate(results.univariate_results):
            np.testing.assert_allclose(diag[:, i], res.forecast(horizon=6)["variance"], rtol=1e-10)

    def test_forecast_rejects_zero_horizon(self, synthetic_returns):
        """horizon < 1 is a programming error, not a silent empty result."""
        import pytest

        model = DCC(synthetic_returns)
        results = model.fit(disp=False)
        with pytest.raises(ValueError, match="horizon"):
            model.forecast(results, horizon=0)


class TestDCCEstimator:
    """Estimator quality on data with known DCC dynamics."""

    def test_recovers_true_parameters(self, dcc_returns):
        """DCC recovers the simulated (a, b) and reports finite standard errors."""
        model = DCC(dcc_returns)
        results = model.fit(disp=False)

        a, b = results.params
        assert results.converged
        assert abs(a - 0.05) < 0.03, f"a={a} far from 0.05"
        assert abs(b - 0.90) < 0.10, f"b={b} far from 0.90"
        assert np.all(np.isfinite(results.std_errors))
        assert np.all(results.std_errors > 0)

    def test_loglike_beats_ccc_on_dynamic_data(self, dcc_returns):
        """On dynamic-correlation data DCC must beat CCC by a clear margin."""
        from archbox.multivariate.ccc import CCC

        ccc = CCC(dcc_returns).fit(disp=False)
        dcc = DCC(dcc_returns).fit(disp=False)
        assert dcc.loglike > ccc.loglike + 5.0
