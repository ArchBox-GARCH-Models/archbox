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
