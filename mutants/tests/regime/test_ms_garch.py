"""Tests for MS-GARCH (Gray, 1996).

Test suite following the spec:
- test_ms_garch_two_regimes
- test_ms_garch_variance_positive
- test_gray_collapsing
"""

from __future__ import annotations

import numpy as np
import pytest

from archbox.regime.ms_garch import MarkovSwitchingGARCH


@pytest.fixture
def simulated_ms_garch_data():
    """Generate two-regime GARCH data."""
    rng = np.random.default_rng(42)
    T = 500
    k = 2

    P = np.array([[0.95, 0.05], [0.10, 0.90]])

    # Regime 0: high volatility, regime 1: low volatility
    omega = [1e-5, 5e-6]
    alpha = [0.15, 0.05]
    beta = [0.80, 0.90]

    regimes = np.zeros(T, dtype=int)
    regimes[0] = 1
    for t in range(1, T):
        regimes[t] = rng.choice(k, p=P[regimes[t - 1]])

    y = np.zeros(T)
    sigma2 = np.zeros(T)
    sigma2[0] = 1e-4  # Initial variance
    y[0] = np.sqrt(sigma2[0]) * rng.standard_normal()

    for t in range(1, T):
        s = regimes[t]
        sigma2[t] = omega[s] + alpha[s] * y[t - 1] ** 2 + beta[s] * sigma2[t - 1]
        y[t] = np.sqrt(sigma2[t]) * rng.standard_normal()

    return y, regimes, P, omega, alpha, beta


class TestMSGARCHTwoRegimes:
    """Test two-regime MS-GARCH."""

    def test_ms_garch_two_regimes(self, simulated_ms_garch_data):
        """MS-GARCH should fit with two regimes."""
        y, _, _, _, _, _ = simulated_ms_garch_data
        model = MarkovSwitchingGARCH(y, k_regimes=2, p=1, q=1)
        results = model.fit(maxiter=100, tol=1e-6, verbose=False)

        assert np.isfinite(results.loglike)
        assert results.transition_matrix.shape == (2, 2)

    def test_ms_garch_variance_positive(self, simulated_ms_garch_data):
        """Conditional variance should be positive in both regimes."""
        y, _, _, _, _, _ = simulated_ms_garch_data
        model = MarkovSwitchingGARCH(y, k_regimes=2, p=1, q=1)
        results = model.fit(maxiter=100, tol=1e-6, verbose=False)

        # Check GARCH params are positive
        for s in range(2):
            rp = results.regime_params[s]
            assert rp["omega"] > 0, f"omega_{s} should be positive"
            assert rp["alpha"] >= 0, f"alpha_{s} should be non-negative"
            assert rp["beta"] >= 0, f"beta_{s} should be non-negative"

    def test_gray_collapsing(self, simulated_ms_garch_data):
        """Test that Gray collapsing produces valid h_{t-1}."""
        y, _, _, _, _, _ = simulated_ms_garch_data
        model = MarkovSwitchingGARCH(y, k_regimes=2, p=1, q=1)

        # Run one iteration to populate sigma2 and collapsed h
        params = model.start_params
        k = model.k_regimes
        T = model.nobs

        # Compute regime loglikes (populates _sigma2)
        for s in range(k):
            model._regime_loglike(params, s)

        # Create fake filtered probs
        filtered_probs = np.ones((T, k)) / k
        model.update_collapsed_variance(filtered_probs)

        h = model._h_collapsed
        assert h is not None
        assert h.shape == (T,)
        assert np.all(h > 0), "Collapsed variance should be positive"

        # h should be weighted average of regime variances
        if model._sigma2 is not None:
            for t in range(T):
                expected_h = np.sum(filtered_probs[t] * model._sigma2[t])
                np.testing.assert_allclose(
                    h[t],
                    expected_h,
                    atol=1e-10,
                    err_msg=f"h[{t}] should be weighted average",
                )

    def test_persistence_per_regime(self, simulated_ms_garch_data):
        """Persistence (alpha + beta) should be < 1 per regime."""
        y, _, _, _, _, _ = simulated_ms_garch_data
        model = MarkovSwitchingGARCH(y, k_regimes=2, p=1, q=1)
        results = model.fit(maxiter=100, tol=1e-6, verbose=False)

        for s in range(2):
            persistence = results.regime_params[s]["persistence"]
            assert persistence < 1.0, f"Regime {s} persistence >= 1: {persistence:.4f}"


class TestMSGARCHResults:
    """Test MS-GARCH results."""

    def test_summary_works(self, simulated_ms_garch_data):
        """summary() should work for MS-GARCH."""
        y, _, _, _, _, _ = simulated_ms_garch_data
        model = MarkovSwitchingGARCH(y, k_regimes=2, p=1, q=1)
        results = model.fit(maxiter=50, tol=1e-6, verbose=False)

        summary = results.summary()
        assert isinstance(summary, str)
        assert "MS-GARCH" in summary

    def test_param_names(self):
        """Param names should include omega, alpha, beta per regime."""
        y = np.random.randn(100) * 0.01
        model = MarkovSwitchingGARCH(y, k_regimes=2, p=1, q=1)
        names = model.param_names
        assert "omega_0" in names
        assert "alpha_0" in names
        assert "beta_0" in names
        assert "omega_1" in names
