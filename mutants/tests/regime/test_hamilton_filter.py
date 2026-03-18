"""Tests for Hamilton Filter.

Test suite following the spec:
- test_filtered_probs_sum_to_one
- test_predicted_probs_sum_to_one
- test_ergodic_probs_sum_to_one
- test_loglike_finite
- test_two_regime_simple
"""

from __future__ import annotations

import numpy as np
import pytest

from archbox.regime.hamilton_filter import HamiltonFilter


@pytest.fixture
def simple_two_regime_data():
    """Generate simple two-regime data for testing.

    Regime 0: N(-2, 0.5^2), Regime 1: N(2, 0.5^2)
    Clear separation so filter should work well.
    """
    rng = np.random.default_rng(123)
    T = 200
    P = np.array([[0.95, 0.05], [0.10, 0.90]])

    regimes = np.zeros(T, dtype=int)
    regimes[0] = 1
    for t in range(1, T):
        regimes[t] = rng.choice(2, p=P[regimes[t - 1]])

    mu = [-2.0, 2.0]
    sigma = [0.5, 0.5]
    y = np.array([mu[s] + sigma[s] * rng.standard_normal() for s in regimes])

    return y, regimes, P, mu, sigma


@pytest.fixture
def regime_loglike_fn_factory():
    """Factory for regime log-likelihood functions."""

    def make_fn(y, mu, sigma):
        def fn(t, s):
            return float(
                -0.5 * np.log(2 * np.pi) - np.log(sigma[s]) - 0.5 * ((y[t] - mu[s]) / sigma[s]) ** 2
            )

        return fn

    return make_fn


class TestHamiltonFilterProbabilities:
    """Test probability constraints."""

    def test_filtered_probs_sum_to_one(self, simple_two_regime_data, regime_loglike_fn_factory):
        """sum(xi_{t|t}) == 1 for all t (tol=1e-10)."""
        y, _, P, mu, sigma = simple_two_regime_data
        fn = regime_loglike_fn_factory(y, mu, sigma)

        hfilter = HamiltonFilter()
        filtered, _, _, _ = hfilter.filter(y, fn, P)

        row_sums = filtered.sum(axis=1)
        np.testing.assert_allclose(row_sums, np.ones(len(y)), atol=1e-10)

    def test_predicted_probs_sum_to_one(self, simple_two_regime_data, regime_loglike_fn_factory):
        """sum(xi_{t|t-1}) == 1 for all t."""
        y, _, P, mu, sigma = simple_two_regime_data
        fn = regime_loglike_fn_factory(y, mu, sigma)

        hfilter = HamiltonFilter()
        _, predicted, _, _ = hfilter.filter(y, fn, P)

        row_sums = predicted.sum(axis=1)
        np.testing.assert_allclose(row_sums, np.ones(len(y)), atol=1e-10)

    def test_ergodic_probs_sum_to_one(self):
        """sum(pi) == 1."""
        P = np.array([[0.95, 0.05], [0.10, 0.90]])

        hfilter = HamiltonFilter()
        pi = hfilter.ergodic_probabilities(P)

        assert abs(pi.sum() - 1.0) < 1e-10
        assert all(pi >= 0)

    def test_ergodic_probs_values(self):
        """Check ergodic probabilities for known P.

        For P = [[0.95, 0.05], [0.10, 0.90]]:
        pi_0 = 0.10 / (0.05 + 0.10) = 2/3
        pi_1 = 0.05 / (0.05 + 0.10) = 1/3
        """
        P = np.array([[0.95, 0.05], [0.10, 0.90]])
        hfilter = HamiltonFilter()
        pi = hfilter.ergodic_probabilities(P)

        np.testing.assert_allclose(pi[0], 2.0 / 3.0, atol=1e-10)
        np.testing.assert_allclose(pi[1], 1.0 / 3.0, atol=1e-10)

    def test_filtered_probs_in_range(self, simple_two_regime_data, regime_loglike_fn_factory):
        """0 <= xi_{t|t}(j) <= 1 for all t, j."""
        y, _, P, mu, sigma = simple_two_regime_data
        fn = regime_loglike_fn_factory(y, mu, sigma)

        hfilter = HamiltonFilter()
        filtered, _, _, _ = hfilter.filter(y, fn, P)

        assert np.all(filtered >= -1e-10)
        assert np.all(filtered <= 1.0 + 1e-10)


class TestHamiltonFilterLoglikelihood:
    """Test log-likelihood computation."""

    def test_loglike_finite(self, simple_two_regime_data, regime_loglike_fn_factory):
        """loglike is not NaN or Inf."""
        y, _, P, mu, sigma = simple_two_regime_data
        fn = regime_loglike_fn_factory(y, mu, sigma)

        hfilter = HamiltonFilter()
        _, _, loglike, marginal = hfilter.filter(y, fn, P)

        assert np.isfinite(loglike)
        assert np.all(np.isfinite(marginal))

    def test_loglike_negative(self, simple_two_regime_data, regime_loglike_fn_factory):
        """Log-likelihood should be negative for continuous distributions."""
        y, _, P, mu, sigma = simple_two_regime_data
        fn = regime_loglike_fn_factory(y, mu, sigma)

        hfilter = HamiltonFilter()
        _, _, loglike, _ = hfilter.filter(y, fn, P)

        # For Gaussian, loglike is typically negative
        assert loglike < 0

    def test_marginal_loglike_shape(self, simple_two_regime_data, regime_loglike_fn_factory):
        """Marginal log-likelihood should have shape (T,)."""
        y, _, P, mu, sigma = simple_two_regime_data
        fn = regime_loglike_fn_factory(y, mu, sigma)

        hfilter = HamiltonFilter()
        _, _, _, marginal = hfilter.filter(y, fn, P)

        assert marginal.shape == (len(y),)


class TestHamiltonFilterRegimeDetection:
    """Test regime detection with well-separated data."""

    def test_two_regime_simple(self, simple_two_regime_data, regime_loglike_fn_factory):
        """MS-Mean(2) with simulated data recovers regimes."""
        y, true_regimes, P, mu, sigma = simple_two_regime_data
        fn = regime_loglike_fn_factory(y, mu, sigma)

        hfilter = HamiltonFilter()
        filtered, _, _, _ = hfilter.filter(y, fn, P)

        # Classify based on filtered probabilities
        detected = np.argmax(filtered, axis=1)

        # Should match true regimes most of the time
        accuracy = np.mean(detected == true_regimes)
        assert accuracy > 0.85, f"Regime detection accuracy too low: {accuracy:.2f}"

    def test_three_regimes(self):
        """Test filter works with 3 regimes."""
        rng = np.random.default_rng(42)
        T = 300
        k = 3
        P = np.array(
            [
                [0.90, 0.05, 0.05],
                [0.05, 0.90, 0.05],
                [0.05, 0.05, 0.90],
            ]
        )
        mu = [-3.0, 0.0, 3.0]
        sigma = [0.5, 0.5, 0.5]

        regimes = np.zeros(T, dtype=int)
        for t in range(1, T):
            regimes[t] = rng.choice(k, p=P[regimes[t - 1]])
        y = np.array([mu[s] + sigma[s] * rng.standard_normal() for s in regimes])

        def fn(t, s):
            return float(
                -0.5 * np.log(2 * np.pi) - np.log(sigma[s]) - 0.5 * ((y[t] - mu[s]) / sigma[s]) ** 2
            )

        hfilter = HamiltonFilter()
        filtered, predicted, loglike, marginal = hfilter.filter(y, fn, P)

        assert filtered.shape == (T, k)
        np.testing.assert_allclose(filtered.sum(axis=1), np.ones(T), atol=1e-10)
        assert np.isfinite(loglike)


class TestHamiltonFilterVectorized:
    """Test vectorized filter variant."""

    def test_vectorized_matches_scalar(self, simple_two_regime_data, regime_loglike_fn_factory):
        """Vectorized filter should produce same results as scalar."""
        y, _, P, mu, sigma = simple_two_regime_data
        fn = regime_loglike_fn_factory(y, mu, sigma)

        # Pre-compute regime log-likelihoods
        T = len(y)
        k = 2
        regime_lls = np.zeros((T, k))
        for t in range(T):
            for s in range(k):
                regime_lls[t, s] = fn(t, s)

        hfilter = HamiltonFilter()
        filt1, pred1, ll1, marg1 = hfilter.filter(y, fn, P)
        filt2, pred2, ll2, marg2 = hfilter.filter_vectorized(regime_lls, P)

        np.testing.assert_allclose(filt1, filt2, atol=1e-10)
        np.testing.assert_allclose(pred1, pred2, atol=1e-10)
        np.testing.assert_allclose(ll1, ll2, atol=1e-10)
        np.testing.assert_allclose(marg1, marg2, atol=1e-10)
