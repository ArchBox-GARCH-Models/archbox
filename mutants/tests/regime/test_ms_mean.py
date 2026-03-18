"""Tests for MS-Mean and MS-Mean-Var models.

Tests:
- Fit on simulated data
- Recover true regime means
- Summary works
- Switching variance vs constant variance
"""

from __future__ import annotations

import numpy as np
import pytest

from archbox.regime.ms_mean import MarkovSwitchingMean, MarkovSwitchingMeanVar


@pytest.fixture
def simulated_ms_mean_data():
    """Generate clear two-regime mean-switching data."""
    rng = np.random.default_rng(42)
    T = 500

    P = np.array([[0.95, 0.05], [0.10, 0.90]])
    mu = [-2.0, 2.0]
    sigma = 0.8  # constant

    regimes = np.zeros(T, dtype=int)
    regimes[0] = 1
    for t in range(1, T):
        regimes[t] = rng.choice(2, p=P[regimes[t - 1]])

    y = np.array([mu[s] + sigma * rng.standard_normal() for s in regimes])
    return y, regimes, P, mu, sigma


@pytest.fixture
def simulated_ms_meanvar_data():
    """Generate clear two-regime mean-variance-switching data."""
    rng = np.random.default_rng(42)
    T = 500

    P = np.array([[0.95, 0.05], [0.10, 0.90]])
    mu = [-1.5, 1.5]
    sigma = [1.5, 0.5]

    regimes = np.zeros(T, dtype=int)
    regimes[0] = 1
    for t in range(1, T):
        regimes[t] = rng.choice(2, p=P[regimes[t - 1]])

    y = np.array([mu[s] + sigma[s] * rng.standard_normal() for s in regimes])
    return y, regimes, P, mu, sigma


class TestMarkovSwitchingMean:
    """Tests for MS-Mean model."""

    def test_fit_simulated_data(self, simulated_ms_mean_data):
        """Model should fit without errors."""
        y, _, _, _, _ = simulated_ms_mean_data
        model = MarkovSwitchingMean(y, k_regimes=2)
        results = model.fit(maxiter=200, tol=1e-8, verbose=False)

        assert results.converged
        assert np.isfinite(results.loglike)

    def test_recover_true_means(self, simulated_ms_mean_data):
        """Model should approximately recover true regime means."""
        y, _, _, true_mu, _ = simulated_ms_mean_data
        model = MarkovSwitchingMean(y, k_regimes=2)
        results = model.fit(maxiter=200, tol=1e-8, verbose=False)

        estimated_means = sorted([results.regime_params[s]["mu"] for s in range(2)])
        true_means = sorted(true_mu)

        for est, true in zip(estimated_means, true_means, strict=True):
            assert abs(est - true) < 1.0, f"Mean recovery failed: est={est:.3f}, true={true:.3f}"

    def test_recover_true_regimes(self, simulated_ms_mean_data):
        """Smoothed probabilities should detect regimes."""
        y, true_regimes, _, _, _ = simulated_ms_mean_data
        model = MarkovSwitchingMean(y, k_regimes=2)
        results = model.fit(maxiter=200, tol=1e-8, verbose=False)

        classified = results.classify()

        # May be flipped (regime 0 <-> 1), so check both
        accuracy1 = np.mean(classified == true_regimes)
        accuracy2 = np.mean(classified == (1 - true_regimes))
        accuracy = max(accuracy1, accuracy2)

        assert accuracy > 0.80, f"Regime detection accuracy too low: {accuracy:.2f}"

    def test_summary_works(self, simulated_ms_mean_data):
        """summary() should return a formatted string."""
        y, _, _, _, _ = simulated_ms_mean_data
        model = MarkovSwitchingMean(y, k_regimes=2)
        results = model.fit(maxiter=100, tol=1e-8, verbose=False)

        summary = results.summary()
        assert isinstance(summary, str)
        assert len(summary) > 100
        assert "MS-Mean" in summary

    def test_constant_variance(self, simulated_ms_mean_data):
        """MS-Mean should have same sigma for both regimes."""
        y, _, _, _, _ = simulated_ms_mean_data
        model = MarkovSwitchingMean(y, k_regimes=2)
        results = model.fit(maxiter=100, tol=1e-8, verbose=False)

        sigma_0 = results.regime_params[0]["sigma"]
        sigma_1 = results.regime_params[1]["sigma"]
        assert (
            abs(sigma_0 - sigma_1) < 1e-10
        ), f"MS-Mean should have constant sigma: {sigma_0} vs {sigma_1}"

    def test_model_name(self):
        """Model name should be MS-Mean."""
        y = np.random.randn(100)
        model = MarkovSwitchingMean(y, k_regimes=2)
        assert model.model_name == "MS-Mean"

    def test_param_names(self):
        """Param names should include mu and sigma."""
        y = np.random.randn(100)
        model = MarkovSwitchingMean(y, k_regimes=2)
        names = model.param_names
        assert "mu_0" in names
        assert "mu_1" in names
        assert "sigma" in names


class TestMarkovSwitchingMeanVar:
    """Tests for MS-Mean-Var model."""

    def test_fit_simulated_data(self, simulated_ms_meanvar_data):
        """Model should fit without errors."""
        y, _, _, _, _ = simulated_ms_meanvar_data
        model = MarkovSwitchingMeanVar(y, k_regimes=2)
        results = model.fit(maxiter=200, tol=1e-8, verbose=False)

        assert results.converged
        assert np.isfinite(results.loglike)

    def test_recover_different_variances(self, simulated_ms_meanvar_data):
        """Model should detect different variances per regime."""
        y, _, _, _, true_sigma = simulated_ms_meanvar_data
        model = MarkovSwitchingMeanVar(y, k_regimes=2)
        results = model.fit(maxiter=200, tol=1e-8, verbose=False)

        estimated_sigmas = sorted([results.regime_params[s]["sigma"] for s in range(2)])

        # The smaller sigma should be clearly smaller
        assert (
            estimated_sigmas[0] < estimated_sigmas[1]
        ), "MS-Mean-Var should detect different regime variances"

    def test_recover_true_regimes(self, simulated_ms_meanvar_data):
        """Smoothed probabilities should detect regimes."""
        y, true_regimes, _, _, _ = simulated_ms_meanvar_data
        model = MarkovSwitchingMeanVar(y, k_regimes=2)
        results = model.fit(maxiter=200, tol=1e-8, verbose=False)

        classified = results.classify()
        accuracy1 = np.mean(classified == true_regimes)
        accuracy2 = np.mean(classified == (1 - true_regimes))
        accuracy = max(accuracy1, accuracy2)

        assert accuracy > 0.75, f"Regime detection accuracy too low: {accuracy:.2f}"

    def test_summary_works(self, simulated_ms_meanvar_data):
        """summary() should return a formatted string."""
        y, _, _, _, _ = simulated_ms_meanvar_data
        model = MarkovSwitchingMeanVar(y, k_regimes=2)
        results = model.fit(maxiter=100, tol=1e-8, verbose=False)

        summary = results.summary()
        assert isinstance(summary, str)
        assert "MS-Mean-Var" in summary

    def test_switching_variance_flag(self):
        """Model should have switching_variance=True."""
        y = np.random.randn(100)
        model = MarkovSwitchingMeanVar(y, k_regimes=2)
        assert model.switching_variance is True
        assert model.switching_mean is True

    def test_model_name(self):
        """Model name should be MS-Mean-Var."""
        y = np.random.randn(100)
        model = MarkovSwitchingMeanVar(y, k_regimes=2)
        assert model.model_name == "MS-Mean-Var"

    def test_param_names(self):
        """Param names should include mu_i and sigma_i for each regime."""
        y = np.random.randn(100)
        model = MarkovSwitchingMeanVar(y, k_regimes=2)
        names = model.param_names
        assert "mu_0" in names
        assert "mu_1" in names
        assert "sigma_0" in names
        assert "sigma_1" in names


class TestMSMeanVsStatsmodels:
    """Comparison tests (sanity checks)."""

    def test_loglike_reasonable(self, simulated_ms_mean_data):
        """Log-likelihood should be reasonable for well-specified model."""
        y, _, _, _, _ = simulated_ms_mean_data
        model = MarkovSwitchingMean(y, k_regimes=2)
        results = model.fit(maxiter=200, tol=1e-8, verbose=False)

        # Per-obs loglike should be roughly between -5 and 0 for standard normal-ish data
        per_obs_ll = results.loglike / results.nobs
        assert -5.0 < per_obs_ll < 0.0, f"Per-obs loglike seems off: {per_obs_ll:.3f}"
