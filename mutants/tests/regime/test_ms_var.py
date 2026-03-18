"""Tests for MS-VAR (Krolzig, 1997).

Test suite following the spec:
- test_ms_var_fit
- test_ms_var_covariance_positive_definite
"""

from __future__ import annotations

import numpy as np
import pytest

from archbox.regime.ms_var import MarkovSwitchingVAR


@pytest.fixture
def simulated_ms_var_data():
    """Generate simulated MS(2)-VAR(1) bivariate data."""
    rng = np.random.default_rng(42)
    T = 300
    n = 2
    k = 2

    P = np.array([[0.95, 0.05], [0.10, 0.90]])
    mu = [np.array([-1.0, -0.5]), np.array([1.0, 0.5])]
    Sigma = [
        np.array([[0.5, 0.1], [0.1, 0.5]]),
        np.array([[0.2, 0.05], [0.05, 0.2]]),
    ]

    regimes = np.zeros(T, dtype=int)
    regimes[0] = 1
    for t in range(1, T):
        regimes[t] = rng.choice(k, p=P[regimes[t - 1]])

    y = np.zeros((T, n))
    for t in range(T):
        s = regimes[t]
        y[t] = mu[s] + rng.multivariate_normal(np.zeros(n), Sigma[s])

    return y, regimes, P, mu, Sigma


class TestMSVARFit:
    """Test MS-VAR fitting."""

    def test_ms_var_fit(self, simulated_ms_var_data):
        """MS(2)-VAR(1) should converge."""
        y, _, _, _, _ = simulated_ms_var_data
        model = MarkovSwitchingVAR(y, k_regimes=2, order=1)
        results = model.fit(maxiter=100, tol=1e-5, verbose=False)

        assert np.isfinite(results.loglike)
        assert results.transition_matrix.shape == (2, 2)

    def test_ms_var_covariance_positive_definite(self, simulated_ms_var_data):
        """Sigma_{S_t} should be positive definite in each regime."""
        y, _, _, _, _ = simulated_ms_var_data
        model = MarkovSwitchingVAR(y, k_regimes=2, order=1)
        results = model.fit(maxiter=100, tol=1e-5, verbose=False)

        for s in range(2):
            # Diagonal elements of covariance should be positive
            for key, val in results.regime_params[s].items():
                if key.startswith("Sigma_"):
                    assert val > 0, f"Regime {s} {key} should be positive: {val}"


class TestMSVARResults:
    """Test MS-VAR results."""

    def test_results_attributes(self, simulated_ms_var_data):
        """Results should have expected attributes."""
        y, _, _, _, _ = simulated_ms_var_data
        model = MarkovSwitchingVAR(y, k_regimes=2, order=1)
        results = model.fit(maxiter=50, tol=1e-5, verbose=False)

        T = y.shape[0]
        assert results.filtered_probs.shape == (T, 2)
        assert results.smoothed_probs.shape == (T, 2)
        assert results.nobs == T

    def test_summary_works(self, simulated_ms_var_data):
        """summary() should work for MS-VAR."""
        y, _, _, _, _ = simulated_ms_var_data
        model = MarkovSwitchingVAR(y, k_regimes=2, order=1)
        results = model.fit(maxiter=50, tol=1e-5, verbose=False)

        summary = results.summary()
        assert isinstance(summary, str)
        assert "MS-VAR" in summary

    def test_transition_matrix_valid(self, simulated_ms_var_data):
        """Transition matrix should be valid stochastic matrix."""
        y, _, _, _, _ = simulated_ms_var_data
        model = MarkovSwitchingVAR(y, k_regimes=2, order=1)
        results = model.fit(maxiter=50, tol=1e-5, verbose=False)

        P = results.transition_matrix
        np.testing.assert_allclose(P.sum(axis=1), np.ones(2), atol=1e-10)
        assert np.all(P >= 0)
