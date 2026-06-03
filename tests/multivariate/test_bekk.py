"""Tests for BEKK-GARCH model."""

from __future__ import annotations

import numpy as np
import pytest

from archbox.multivariate.bekk import BEKK
from archbox.multivariate.utils import is_positive_definite


class TestBEKKGARCH:
    """Test BEKK-GARCH model."""

    @pytest.fixture
    def bekk_returns(self, rng):
        """Generate returns suitable for BEKK (2 series, 300 obs)."""
        n, k = 300, 2
        R = np.array([[1.0, 0.5], [0.5, 1.0]])
        L = np.linalg.cholesky(R)
        z = rng.standard_normal((n, k))
        returns = (z @ L.T) * 0.01
        return returns

    def test_bekk_h_positive_definite(self, bekk_returns):
        """H_t should be positive definite for all t."""
        model = BEKK(bekk_returns, variant="diagonal")
        results = model.fit(disp=False)

        H_t = results.dynamic_covariance
        T = H_t.shape[0]

        for t in range(0, T, 30):
            assert is_positive_definite(H_t[t]), f"H_t not PD at t={t}"

    def test_bekk_covariance_symmetric(self, bekk_returns):
        """H_t should be symmetric for all t."""
        model = BEKK(bekk_returns, variant="diagonal")
        results = model.fit(disp=False)

        H_t = results.dynamic_covariance
        T = H_t.shape[0]

        for t in range(0, T, 30):
            np.testing.assert_array_almost_equal(
                H_t[t],
                H_t[t].T,
                decimal=10,
                err_msg=f"H_t not symmetric at t={t}",
            )

    def test_bekk_diagonal_fewer_params(self):
        """Diagonal BEKK should have fewer params than full BEKK."""
        k = 3
        returns = np.random.randn(200, k) * 0.01

        full_model = BEKK(returns, variant="full")
        diag_model = BEKK(returns, variant="diagonal")

        # Full: k(k+1)/2 + 2*k^2
        expected_full = k * (k + 1) // 2 + 2 * k * k
        # Diagonal: k(k+1)/2 + 2*k
        expected_diag = k * (k + 1) // 2 + 2 * k

        assert (
            full_model.num_params == expected_full
        ), f"Full BEKK k={k}: expected {expected_full}, got {full_model.num_params}"
        assert (
            diag_model.num_params == expected_diag
        ), f"Diag BEKK k={k}: expected {expected_diag}, got {diag_model.num_params}"
        assert diag_model.num_params < full_model.num_params

    def test_bekk_full_params_count(self):
        """Check parameter counts for various k."""
        for k, expected in [(2, 11), (3, 24), (5, 65)]:
            returns = np.random.randn(100, k) * 0.01
            model = BEKK(returns, variant="full")
            assert (
                model.num_params == expected
            ), f"Full BEKK k={k}: expected {expected}, got {model.num_params}"

    def test_bekk_diagonal_params_count(self):
        """Check diagonal parameter counts for various k."""
        for k, expected in [(2, 7), (3, 12), (5, 25)]:
            returns = np.random.randn(100, k) * 0.01
            model = BEKK(returns, variant="diagonal")
            assert (
                model.num_params == expected
            ), f"Diag BEKK k={k}: expected {expected}, got {model.num_params}"

    def test_bekk_loglike_finite(self, bekk_returns):
        """Log-likelihood should be finite."""
        model = BEKK(bekk_returns, variant="diagonal")
        results = model.fit(disp=False)

        assert np.isfinite(results.loglike)

    def test_bekk_summary(self, bekk_returns):
        """summary() should return a non-empty string."""
        model = BEKK(bekk_returns, variant="diagonal")
        results = model.fit(disp=False)
        s = results.summary()
        assert isinstance(s, str)
        assert "BEKK" in s
        assert len(s) > 50

    def test_bekk_forecast(self, bekk_returns):
        """Forecast should return correct shapes and converge."""
        model = BEKK(bekk_returns, variant="diagonal")
        results = model.fit(disp=False)

        fcast = model.forecast(results, horizon=50)
        k = bekk_returns.shape[1]

        assert fcast["covariance"].shape == (50, k, k)
        assert fcast["correlation"].shape == (50, k, k)

        # Check that forecasts are PD
        for h in range(50):
            assert is_positive_definite(fcast["covariance"][h]), f"Forecast not PD at h={h}"

    def test_bekk_forecast_converges(self, bekk_returns):
        """Long-horizon forecast should converge (successive H's become similar)."""
        model = BEKK(bekk_returns, variant="diagonal")
        results = model.fit(disp=False)

        fcast = model.forecast(results, horizon=200)

        # Check convergence: difference between successive forecasts should shrink
        diff_early = np.max(np.abs(fcast["covariance"][1] - fcast["covariance"][0]))
        diff_late = np.max(np.abs(fcast["covariance"][-1] - fcast["covariance"][-2]))

        assert diff_late < diff_early + 1e-10, "Forecast not converging"

    def test_bekk_invalid_variant(self, bekk_returns):
        """Invalid variant should raise ValueError."""
        with pytest.raises(ValueError, match="variant"):
            BEKK(bekk_returns, variant="invalid")

    def test_bekk_correlation_from_covariance(self, bekk_returns):
        """Derived R_t should have diagonal = 1 and elements in [-1, 1]."""
        model = BEKK(bekk_returns, variant="diagonal")
        results = model.fit(disp=False)

        R_t = results.dynamic_correlation
        T, k, _ = R_t.shape

        for t in range(0, T, 30):
            np.testing.assert_array_almost_equal(
                np.diag(R_t[t]),
                np.ones(k),
                decimal=4,
                err_msg=f"R_t diagonal not 1 at t={t}",
            )
            assert np.all(R_t[t] >= -1.0 - 0.01), f"R has elements < -1 at t={t}"
            assert np.all(R_t[t] <= 1.0 + 0.01), f"R has elements > 1 at t={t}"
