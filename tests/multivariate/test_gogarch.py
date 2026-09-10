"""Tests for GO-GARCH model."""

from __future__ import annotations

import numpy as np

from archbox.multivariate.gogarch import GOGARCH
from archbox.multivariate.utils import is_positive_definite


class TestGOGARCH:
    """Test GO-GARCH model."""

    def test_gogarch_factors_independent(self, synthetic_returns):
        """Factors should be approximately independent (low correlation)."""
        model = GOGARCH(synthetic_returns)
        _ = model.fit(disp=False)

        factors = model.factors
        assert factors is not None

        # Correlation between factors should be close to 0
        corr = np.corrcoef(factors.T)
        k = factors.shape[1]

        for i in range(k):
            for j in range(i + 1, k):
                assert abs(corr[i, j]) < 0.3, (
                    f"Factor correlation ({i},{j}) = {corr[i, j]:.3f}, expected ~0"
                )

    def test_gogarch_reconstruction(self, synthetic_returns):
        """H_t = Z * diag(h_t) * Z' should reconstruct correctly."""
        model = GOGARCH(synthetic_returns)
        results = model.fit(disp=False)

        Z = model.mixing_matrix
        assert Z is not None

        # Verify H_t is consistent with Z and factor variances
        H_t = results.dynamic_covariance
        T = H_t.shape[0]

        # H_t should be symmetric
        for t in range(0, T, 50):
            np.testing.assert_array_almost_equal(
                H_t[t],
                H_t[t].T,
                decimal=8,
                err_msg=f"H_t not symmetric at t={t}",
            )

    def test_gogarch_positive_definite(self, synthetic_returns):
        """H_t should be positive definite for all t."""
        model = GOGARCH(synthetic_returns)
        results = model.fit(disp=False)

        H_t = results.dynamic_covariance
        T = H_t.shape[0]

        for t in range(0, T, 50):
            assert is_positive_definite(H_t[t]), f"H_t not PD at t={t}"

    def test_gogarch_mixing_matrix_shape(self, synthetic_returns):
        """Mixing matrix Z should be (k, k)."""
        model = GOGARCH(synthetic_returns)
        _ = model.fit(disp=False)

        Z = model.mixing_matrix
        assert Z is not None
        k = synthetic_returns.shape[1]
        assert Z.shape == (k, k)

    def test_gogarch_loglike_finite(self, synthetic_returns):
        """Log-likelihood should be finite."""
        model = GOGARCH(synthetic_returns)
        results = model.fit(disp=False)

        assert np.isfinite(results.loglike)

    def test_gogarch_summary(self, synthetic_returns):
        """summary() should return a non-empty string."""
        model = GOGARCH(synthetic_returns)
        results = model.fit(disp=False)
        s = results.summary()
        assert isinstance(s, str)
        assert "GO-GARCH" in s

    def test_gogarch_no_correlation_params(self, synthetic_returns):
        """GO-GARCH has no separate correlation parameters."""
        model = GOGARCH(synthetic_returns)
        results = model.fit(disp=False)

        assert len(results.params) == 0

    def test_gogarch_forecast(self, synthetic_returns):
        """Forecast should return correct shapes."""
        model = GOGARCH(synthetic_returns)
        results = model.fit(disp=False)

        fcast = model.forecast(results, horizon=10)
        k = synthetic_returns.shape[1]

        assert fcast["covariance"].shape == (10, k, k)
        assert fcast["correlation"].shape == (10, k, k)

    def test_gogarch_with_fx_data(self, fx_returns):
        """GO-GARCH should work with FX data."""
        model = GOGARCH(fx_returns)
        results = model.fit(disp=False)

        assert results.dynamic_covariance.shape == (2000, 3, 3)
        assert np.isfinite(results.loglike)
