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
        """Gray collapsing uses the filtered probabilities of the same pass."""
        y, _, _, _, _, _ = simulated_ms_garch_data
        model = MarkovSwitchingGARCH(y, k_regimes=2, p=1, q=1)

        params = model.start_params
        k = model.k_regimes
        T = model.nobs

        sigma2, h, filtered, _log_eta = model._gray_recursion(params)

        assert sigma2.shape == (T, k)
        assert h.shape == (T,)
        assert filtered.shape == (T, k)
        assert np.all(h > 0), "Collapsed variance should be positive"
        assert np.all(sigma2 > 0), "Regime variances should be positive"
        np.testing.assert_allclose(filtered.sum(axis=1), np.ones(T), atol=1e-10)

        # h_t = sum_j P(S_t=j | Y_t) * sigma2_t(j)
        expected_h = np.sum(filtered * sigma2, axis=1)
        np.testing.assert_allclose(h, expected_h, atol=1e-12)

        # sigma2_t(s) = omega_s + alpha_s * y_{t-1}^2 + beta_s * h_{t-1}
        for s in range(k):
            omega, alpha, beta = model._unpack_garch_params(params, s)
            expected = omega + alpha * y[:-1] ** 2 + beta * h[:-1]
            np.testing.assert_allclose(sigma2[1:, s], expected, rtol=1e-12)

    def test_regime_loglike_has_no_side_effects(self, simulated_ms_garch_data):
        """Evaluating a regime density must not mutate the model."""
        y, _, _, _, _, _ = simulated_ms_garch_data
        model = MarkovSwitchingGARCH(y, k_regimes=2, p=1, q=1)
        params = model.start_params

        first = model._regime_loglike(params, 0).copy()
        model._regime_loglike(params, 1)
        second = model._regime_loglike(params, 0)

        np.testing.assert_allclose(first, second, atol=0.0)
        assert not hasattr(model, "_sigma2") or model._sigma2 is None

    def test_loglike_matches_fit(self, simulated_ms_garch_data):
        """model.loglike(results.params) reproduces results.loglike."""
        y, _, _, _, _, _ = simulated_ms_garch_data
        model = MarkovSwitchingGARCH(y, k_regimes=2, p=1, q=1)
        results = model.fit(maxiter=100, tol=1e-8, verbose=False)

        assert results.converged
        assert model.loglike(results.params) == pytest.approx(results.loglike, abs=1e-6)

    def test_beats_start_params(self, simulated_ms_garch_data):
        """The fitted likelihood must improve on the starting values."""
        y, _, _, _, _, _ = simulated_ms_garch_data
        model = MarkovSwitchingGARCH(y, k_regimes=2, p=1, q=1)
        start_ll = model.loglike(model.start_params)
        results = model.fit(maxiter=200, tol=1e-8, verbose=False)

        assert results.loglike > start_ll

    def test_forecast_variance_positive(self, simulated_ms_garch_data):
        """Variance forecasts are positive and regime probabilities valid."""
        y, _, _, _, _, _ = simulated_ms_garch_data
        model = MarkovSwitchingGARCH(y, k_regimes=2, p=1, q=1)
        model.fit(maxiter=100, tol=1e-8, verbose=False)

        fc = model.forecast(10)
        assert np.all(fc["variance"] > 0)
        np.testing.assert_allclose(fc["mean"], 0.0, atol=1e-12)
        np.testing.assert_allclose(fc["regime_probs"].sum(axis=1), 1.0, atol=1e-10)

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
