"""Tests for RegimeResults container."""

from __future__ import annotations

import numpy as np
import pytest

from archbox.regime.results import RegimeResults


@pytest.fixture
def sample_results():
    """Create a sample RegimeResults for testing."""
    T = 100
    k = 2
    np.random.seed(42)

    params = np.array([1.0, -1.0, 0.5, 0.8])
    regime_params = {
        0: {"mu": 1.0, "sigma": 0.5},
        1: {"mu": -1.0, "sigma": 0.8},
    }
    P = np.array([[0.95, 0.05], [0.10, 0.90]])

    filtered = np.random.dirichlet([5, 5], size=T)
    smoothed = np.random.dirichlet([5, 5], size=T)
    predicted = np.random.dirichlet([5, 5], size=T)

    return RegimeResults(
        params=params,
        regime_params=regime_params,
        transition_matrix=P,
        filtered_probs=filtered,
        smoothed_probs=smoothed,
        predicted_probs=predicted,
        loglike=-250.0,
        nobs=T,
        k_regimes=k,
        model_name="TestModel",
        param_names=["mu_0", "mu_1", "sigma_0", "sigma_1"],
    )


class TestRegimeResultsAttributes:
    """Test basic attributes."""

    def test_aic(self, sample_results: RegimeResults) -> None:
        """AIC should be -2*loglike + 2*k."""
        expected = -2 * (-250.0) + 2 * 4
        assert abs(sample_results.aic - expected) < 1e-10

    def test_bic(self, sample_results: RegimeResults) -> None:
        """BIC should be -2*loglike + log(n)*k."""
        expected = -2 * (-250.0) + np.log(100) * 4
        assert abs(sample_results.bic - expected) < 1e-10

    def test_n_params(self, sample_results: RegimeResults) -> None:
        assert sample_results.n_params == 4

    def test_nobs(self, sample_results: RegimeResults) -> None:
        assert sample_results.nobs == 100


class TestRegimeResultsMethods:
    """Test methods."""

    def test_expected_durations(self, sample_results: RegimeResults) -> None:
        """E[duration] = 1 / (1 - p_jj)."""
        durations = sample_results.expected_durations()
        np.testing.assert_allclose(durations[0], 1.0 / 0.05, atol=1e-10)
        np.testing.assert_allclose(durations[1], 1.0 / 0.10, atol=1e-10)

    def test_ergodic_probabilities(self, sample_results: RegimeResults) -> None:
        """Ergodic probs should sum to 1."""
        pi = sample_results.ergodic_probabilities()
        assert abs(pi.sum() - 1.0) < 1e-10
        assert all(pi >= 0)

    def test_ergodic_probs_values(self, sample_results: RegimeResults) -> None:
        """For P = [[0.95, 0.05], [0.10, 0.90]]:
        pi_0 = 0.10 / (0.05 + 0.10) = 2/3
        pi_1 = 0.05 / (0.05 + 0.10) = 1/3
        """
        pi = sample_results.ergodic_probabilities()
        np.testing.assert_allclose(pi[0], 2.0 / 3.0, atol=1e-6)
        np.testing.assert_allclose(pi[1], 1.0 / 3.0, atol=1e-6)

    def test_classify(self, sample_results: RegimeResults) -> None:
        """classify should return integer labels."""
        labels = sample_results.classify()
        assert labels.shape == (100,)
        assert labels.dtype == np.int64
        assert set(labels.tolist()).issubset({0, 1})

    def test_summary(self, sample_results: RegimeResults) -> None:
        """summary should return non-empty string."""
        s = sample_results.summary()
        assert isinstance(s, str)
        assert len(s) > 50
        assert "TestModel" in s
        assert "Transition" in s
        assert "Duration" in s
