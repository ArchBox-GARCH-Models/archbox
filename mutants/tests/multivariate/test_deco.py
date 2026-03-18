"""Tests for DECO model."""

from __future__ import annotations

import numpy as np

from archbox.multivariate.deco import DECO
from archbox.multivariate.utils import is_positive_definite


class TestDECO:
    """Test DECO model."""

    def test_deco_scalar_correlation(self, synthetic_returns):
        """All off-diagonal elements of R_t should be equal (equicorrelation)."""
        model = DECO(synthetic_returns)
        results = model.fit(disp=False)

        R_t = results.dynamic_correlation
        T, k, _ = R_t.shape

        for t in range(0, T, 50):
            R = R_t[t]
            # Extract off-diagonal elements
            off_diag = R[np.triu_indices(k, k=1)]
            # All off-diagonal should be the same value
            if len(off_diag) > 1:
                np.testing.assert_array_almost_equal(
                    off_diag,
                    off_diag[0] * np.ones_like(off_diag),
                    decimal=10,
                    err_msg=f"Off-diagonal not equal at t={t}",
                )

    def test_deco_positive_definite(self, synthetic_returns):
        """R_t should be positive definite for all t."""
        model = DECO(synthetic_returns)
        results = model.fit(disp=False)

        R_t = results.dynamic_correlation
        T = R_t.shape[0]

        for t in range(0, T, 50):
            assert is_positive_definite(R_t[t]), f"R_t not PD at t={t}"

    def test_deco_rho_bounds(self, synthetic_returns):
        """rho_t should be in (-1/(k-1), 1)."""
        model = DECO(synthetic_returns)
        _ = model.fit(disp=False)

        rho = model.equicorrelation
        assert rho is not None

        k = synthetic_returns.shape[1]
        lower_bound = -1.0 / (k - 1)

        assert np.all(rho > lower_bound - 1e-6), f"rho_t below lower bound {lower_bound}"
        assert np.all(rho < 1.0 + 1e-6), "rho_t above 1"

    def test_deco_diagonal_one(self, synthetic_returns):
        """Diagonal of R_t should be 1."""
        model = DECO(synthetic_returns)
        results = model.fit(disp=False)

        R_t = results.dynamic_correlation
        T, k, _ = R_t.shape

        for t in range(0, T, 50):
            np.testing.assert_array_almost_equal(
                np.diag(R_t[t]),
                np.ones(k),
                decimal=10,
            )

    def test_deco_symmetric(self, synthetic_returns):
        """R_t should be symmetric."""
        model = DECO(synthetic_returns)
        results = model.fit(disp=False)

        R_t = results.dynamic_correlation
        T = R_t.shape[0]

        for t in range(0, T, 50):
            np.testing.assert_array_almost_equal(
                R_t[t],
                R_t[t].T,
                decimal=10,
            )

    def test_deco_persistence(self, synthetic_returns):
        """a + b should be < 1."""
        model = DECO(synthetic_returns)
        results = model.fit(disp=False)

        a, b = results.params[0], results.params[1]
        assert a > 0
        assert b > 0
        assert a + b < 1.0

    def test_deco_loglike_finite(self, synthetic_returns):
        """Log-likelihood should be finite."""
        model = DECO(synthetic_returns)
        results = model.fit(disp=False)

        assert np.isfinite(results.loglike)

    def test_deco_summary(self, synthetic_returns):
        """summary() should return a non-empty string."""
        model = DECO(synthetic_returns)
        results = model.fit(disp=False)
        s = results.summary()
        assert isinstance(s, str)
        assert "DECO" in s

    def test_deco_scales_with_k(self, rng):
        """DECO should work with k=10 (many series)."""
        n, k = 300, 10
        R = np.eye(k) * 0.6 + np.ones((k, k)) * 0.4
        L = np.linalg.cholesky(R)
        z = rng.standard_normal((n, k))
        returns = (z @ L.T) * 0.01

        model = DECO(returns)
        results = model.fit(disp=False)

        assert results.dynamic_correlation.shape == (n, k, k)
        assert np.isfinite(results.loglike)

    def test_deco_rho_varies(self, synthetic_returns):
        """rho_t should vary over time (dynamic)."""
        model = DECO(synthetic_returns)
        _ = model.fit(disp=False)

        rho = model.equicorrelation
        assert rho is not None

        # Should not be constant
        assert np.std(rho) > 1e-6, "rho_t appears constant"

    def test_deco_forecast(self, synthetic_returns):
        """Forecast should return correct shapes."""
        model = DECO(synthetic_returns)
        results = model.fit(disp=False)

        fcast = model.forecast(results, horizon=10)
        k = synthetic_returns.shape[1]

        assert fcast["covariance"].shape == (10, k, k)
        assert fcast["correlation"].shape == (10, k, k)

    def test_deco_h_positive_definite(self, synthetic_returns):
        """H_t should be positive definite."""
        model = DECO(synthetic_returns)
        results = model.fit(disp=False)

        H_t = results.dynamic_covariance
        T = H_t.shape[0]

        for t in range(0, T, 50):
            assert is_positive_definite(H_t[t]), f"H_t not PD at t={t}"
