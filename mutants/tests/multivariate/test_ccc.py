"""Tests for CCC-GARCH model."""

from __future__ import annotations

import numpy as np

from archbox.multivariate.ccc import CCC
from archbox.multivariate.utils import is_positive_definite


class TestCCCGARCH:
    """Test CCC-GARCH model."""

    def test_ccc_constant_correlation(self, synthetic_returns):
        """R_t should be constant for all t."""
        model = CCC(synthetic_returns)
        results = model.fit(disp=False)

        R_t = results.dynamic_correlation
        T = R_t.shape[0]

        # All R_t should be identical
        R_first = R_t[0]
        for t in range(1, T):
            np.testing.assert_array_almost_equal(
                R_t[t],
                R_first,
                decimal=10,
                err_msg=f"R_t not constant at t={t}",
            )

    def test_ccc_r_matches_sample_correlation(self, synthetic_returns):
        """R should be close to sample correlation of standardized residuals."""
        model = CCC(synthetic_returns)
        results = model.fit(disp=False)

        # Get sample correlation of standardized residuals
        z = results.std_resids
        R_sample = np.corrcoef(z.T)

        # R from model
        R_model = results.dynamic_correlation[0]

        np.testing.assert_array_almost_equal(
            R_model,
            R_sample,
            decimal=2,
            err_msg="R does not match sample correlation of std resids",
        )

    def test_ccc_positive_definite_H(self, synthetic_returns):
        """H_t should be positive definite for all t."""
        model = CCC(synthetic_returns)
        results = model.fit(disp=False)

        H_t = results.dynamic_covariance
        T = H_t.shape[0]

        for t in range(0, T, 50):  # Check every 50th
            assert is_positive_definite(H_t[t]), f"H_t not PD at t={t}"

    def test_ccc_correlation_diagonal_one(self, synthetic_returns):
        """Diagonal of R should be 1."""
        model = CCC(synthetic_returns)
        results = model.fit(disp=False)

        R = results.dynamic_correlation[0]
        np.testing.assert_array_almost_equal(
            np.diag(R),
            np.ones(synthetic_returns.shape[1]),
            decimal=10,
        )

    def test_ccc_correlation_bounds(self, synthetic_returns):
        """R_{ij} should be in [-1, 1]."""
        model = CCC(synthetic_returns)
        results = model.fit(disp=False)

        R = results.dynamic_correlation[0]
        assert np.all(R >= -1.0 - 1e-10), "R has elements < -1"
        assert np.all(R <= 1.0 + 1e-10), "R has elements > 1"

    def test_ccc_correlation_symmetric(self, synthetic_returns):
        """R should be symmetric."""
        model = CCC(synthetic_returns)
        results = model.fit(disp=False)

        R = results.dynamic_correlation[0]
        np.testing.assert_array_almost_equal(
            R,
            R.T,
            decimal=10,
            err_msg="R is not symmetric",
        )

    def test_ccc_no_correlation_params(self, synthetic_returns):
        """CCC has no correlation parameters to estimate."""
        model = CCC(synthetic_returns)
        results = model.fit(disp=False)

        assert len(results.params) == 0
        assert model.param_names == []

    def test_ccc_summary(self, synthetic_returns):
        """summary() should return a non-empty string."""
        model = CCC(synthetic_returns)
        results = model.fit(disp=False)
        s = results.summary()
        assert isinstance(s, str)
        assert "CCC-GARCH" in s
        assert len(s) > 100

    def test_ccc_portfolio_volatility(self, synthetic_returns):
        """Portfolio volatility should be positive."""
        model = CCC(synthetic_returns)
        results = model.fit(disp=False)

        k = synthetic_returns.shape[1]
        w = np.ones(k) / k
        port_vol = results.portfolio_volatility(w)

        assert port_vol.shape == (synthetic_returns.shape[0],)
        assert np.all(port_vol >= 0)
        assert np.all(np.isfinite(port_vol))

    def test_ccc_loglike_finite(self, synthetic_returns):
        """Log-likelihood should be finite."""
        model = CCC(synthetic_returns)
        results = model.fit(disp=False)

        assert np.isfinite(results.loglike)

    def test_ccc_forecast(self, synthetic_returns):
        """Forecast should return correct shapes."""
        model = CCC(synthetic_returns)
        results = model.fit(disp=False)

        fcast = model.forecast(results, horizon=5)
        k = synthetic_returns.shape[1]

        assert fcast["covariance"].shape == (5, k, k)
        assert fcast["correlation"].shape == (5, k, k)

        # Correlation forecast should be constant R
        for h in range(5):
            np.testing.assert_array_almost_equal(
                fcast["correlation"][h],
                results.dynamic_correlation[0],
                decimal=10,
            )

    def test_ccc_with_fx_data(self, fx_returns):
        """CCC should work with real FX data (3 series)."""
        model = CCC(fx_returns)
        results = model.fit(disp=False)

        assert results.dynamic_correlation.shape == (2000, 3, 3)
        assert results.dynamic_covariance.shape == (2000, 3, 3)
        assert np.isfinite(results.loglike)
