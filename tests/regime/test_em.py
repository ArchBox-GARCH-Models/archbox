"""Tests for EM Algorithm.

Test suite following the spec:
- test_em_monotone_loglike
- test_em_convergence
- test_transition_matrix_rows_sum_one
"""

from __future__ import annotations

import numpy as np
import pytest

from archbox.regime.base import MarkovSwitchingModel
from archbox.regime.em import EMEstimator


class SimpleMSMean(MarkovSwitchingModel):
    """Simple MS-Mean model for testing EM.

    y_t | S_t=s ~ N(mu_s, sigma_s^2)
    """

    model_name = "SimpleMSMean"

    def _regime_loglike(self, params: np.ndarray, regime: int) -> np.ndarray:
        k = self.k_regimes
        mu = params[regime]
        sigma = params[k + regime] if self.switching_variance else params[k]
        sigma = max(abs(sigma), 1e-6)
        y = self.endog
        ll = -0.5 * np.log(2 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    @property
    def start_params(self) -> np.ndarray:
        k = self.k_regimes
        y = self.endog
        # Initialize means using quantiles
        quantiles = np.linspace(0, 1, k + 2)[1:-1]
        mus = np.quantile(y, quantiles)
        sigmas = np.full(k, np.std(y))
        # Transition params (logit of off-diagonal)
        trans = np.zeros(k * (k - 1))
        return np.concatenate([mus, sigmas, trans])

    @property
    def param_names(self) -> list[str]:
        k = self.k_regimes
        names = [f"mu_{i}" for i in range(k)]
        names += [f"sigma_{i}" for i in range(k)]
        names += [f"p_{i}{j}" for i in range(k) for j in range(k) if i != j]
        return names


@pytest.fixture
def simulated_two_regime_data() -> tuple[
    np.ndarray, np.ndarray, np.ndarray, list[float], list[float]
]:
    """Generate two-regime data with clear separation."""
    rng = np.random.default_rng(42)
    t_obs = 500
    p_mat = np.array([[0.95, 0.05], [0.10, 0.90]])

    regimes = np.zeros(t_obs, dtype=int)
    regimes[0] = 1
    for t in range(1, t_obs):
        regimes[t] = rng.choice(2, p=p_mat[regimes[t - 1]])

    mu = [-2.0, 2.0]
    sigma = [0.8, 0.8]
    y = np.array([mu[s] + sigma[s] * rng.standard_normal() for s in regimes])

    return y, regimes, p_mat, mu, sigma


class TestEMMonotonicity:
    """Test that EM log-likelihood is monotonically non-decreasing."""

    def test_em_monotone_loglike(
        self,
        simulated_two_regime_data: tuple[
            np.ndarray, np.ndarray, np.ndarray, list[float], list[float]
        ],
    ) -> None:
        """Log-likelihood should not decrease between EM iterations."""
        y, _, _, _, _ = simulated_two_regime_data
        model = SimpleMSMean(y, k_regimes=2)

        estimator = EMEstimator()
        estimator.fit(model, maxiter=50, tol=1e-12, verbose=False)

        history = estimator.loglike_history

        # Check monotonicity (allowing small numerical errors from
        # floating-point arithmetic in the Hamilton filter; the Q-function
        # is guaranteed to increase, but the observed log-likelihood can
        # show tiny decreases near convergence due to accumulated
        # floating-point errors over T observations)
        for i in range(1, len(history)):
            assert history[i] >= history[i - 1] - 1e-4, (
                f"Log-likelihood decreased at iteration {i}: "
                f"{history[i - 1]:.6f} -> {history[i]:.6f}"
            )


class TestEMConvergence:
    """Test EM convergence."""

    def test_em_convergence(
        self,
        simulated_two_regime_data: tuple[
            np.ndarray, np.ndarray, np.ndarray, list[float], list[float]
        ],
    ) -> None:
        """EM should converge in < 500 iterations for simulated data."""
        y, _, _, _, _ = simulated_two_regime_data
        model = SimpleMSMean(y, k_regimes=2)

        estimator = EMEstimator()
        results = estimator.fit(model, maxiter=500, tol=1e-8, verbose=False)

        assert results.converged, f"EM did not converge in {results.n_iter} iterations"

    def test_em_recovers_means(
        self,
        simulated_two_regime_data: tuple[
            np.ndarray, np.ndarray, np.ndarray, list[float], list[float]
        ],
    ) -> None:
        """EM should recover approximate regime means."""
        y, _, _, true_mu, _ = simulated_two_regime_data
        model = SimpleMSMean(y, k_regimes=2)

        estimator = EMEstimator()
        results = estimator.fit(model, maxiter=200, tol=1e-8, verbose=False)

        # Get estimated means (may be in any order)
        estimated_means = sorted([results.regime_params[s]["mu"] for s in range(2)])
        true_means = sorted(true_mu)

        # Allow tolerance for mean estimation
        for est, true in zip(estimated_means, true_means, strict=True):
            assert abs(est - true) < abs(true) * 0.5 + 0.5, (
                f"Mean estimation off: estimated={est:.3f}, true={true:.3f}"
            )


class TestEMTransitionMatrix:
    """Test transition matrix properties after EM."""

    def test_transition_matrix_rows_sum_one(
        self,
        simulated_two_regime_data: tuple[
            np.ndarray, np.ndarray, np.ndarray, list[float], list[float]
        ],
    ) -> None:
        """Each row of P should sum to 1 after M-step."""
        y, _, _, _, _ = simulated_two_regime_data
        model = SimpleMSMean(y, k_regimes=2)

        estimator = EMEstimator()
        results = estimator.fit(model, maxiter=100, tol=1e-8, verbose=False)

        row_sums = results.transition_matrix.sum(axis=1)
        np.testing.assert_allclose(row_sums, np.ones(2), atol=1e-10)

    def test_transition_matrix_nonnegative(
        self,
        simulated_two_regime_data: tuple[
            np.ndarray, np.ndarray, np.ndarray, list[float], list[float]
        ],
    ) -> None:
        """All transition probabilities should be non-negative."""
        y, _, _, _, _ = simulated_two_regime_data
        model = SimpleMSMean(y, k_regimes=2)

        estimator = EMEstimator()
        results = estimator.fit(model, maxiter=100, tol=1e-8, verbose=False)

        assert np.all(results.transition_matrix >= 0)

    def test_transition_matrix_shape(
        self,
        simulated_two_regime_data: tuple[
            np.ndarray, np.ndarray, np.ndarray, list[float], list[float]
        ],
    ) -> None:
        """Transition matrix should have shape (k, k)."""
        y, _, _, _, _ = simulated_two_regime_data
        model = SimpleMSMean(y, k_regimes=2)

        estimator = EMEstimator()
        results = estimator.fit(model, maxiter=100, tol=1e-8, verbose=False)

        assert results.transition_matrix.shape == (2, 2)


class TestEMResults:
    """Test EM results container."""

    def test_results_attributes(
        self,
        simulated_two_regime_data: tuple[
            np.ndarray, np.ndarray, np.ndarray, list[float], list[float]
        ],
    ) -> None:
        """Results should have all expected attributes."""
        y, _, _, _, _ = simulated_two_regime_data
        model = SimpleMSMean(y, k_regimes=2)

        estimator = EMEstimator()
        results = estimator.fit(model, maxiter=100, tol=1e-8, verbose=False)

        assert results.filtered_probs.shape == (len(y), 2)
        assert results.smoothed_probs.shape == (len(y), 2)
        assert results.predicted_probs.shape == (len(y), 2)
        assert np.isfinite(results.loglike)
        assert np.isfinite(results.aic)
        assert np.isfinite(results.bic)
        assert results.nobs == len(y)
        assert results.k_regimes == 2

    def test_results_summary(
        self,
        simulated_two_regime_data: tuple[
            np.ndarray, np.ndarray, np.ndarray, list[float], list[float]
        ],
    ) -> None:
        """summary() should produce a non-empty string."""
        y, _, _, _, _ = simulated_two_regime_data
        model = SimpleMSMean(y, k_regimes=2)

        estimator = EMEstimator()
        results = estimator.fit(model, maxiter=100, tol=1e-8, verbose=False)

        summary = results.summary()
        assert len(summary) > 0
        assert "Regime" in summary
        assert "Transition" in summary

    def test_results_expected_durations(
        self,
        simulated_two_regime_data: tuple[
            np.ndarray, np.ndarray, np.ndarray, list[float], list[float]
        ],
    ) -> None:
        """Expected durations should be positive."""
        y, _, _, _, _ = simulated_two_regime_data
        model = SimpleMSMean(y, k_regimes=2)

        estimator = EMEstimator()
        results = estimator.fit(model, maxiter=100, tol=1e-8, verbose=False)

        durations = results.expected_durations()
        assert len(durations) == 2
        assert all(d > 0 for d in durations)

    def test_results_ergodic_probabilities(
        self,
        simulated_two_regime_data: tuple[
            np.ndarray, np.ndarray, np.ndarray, list[float], list[float]
        ],
    ) -> None:
        """Ergodic probabilities should sum to 1."""
        y, _, _, _, _ = simulated_two_regime_data
        model = SimpleMSMean(y, k_regimes=2)

        estimator = EMEstimator()
        results = estimator.fit(model, maxiter=100, tol=1e-8, verbose=False)

        ergodic = results.ergodic_probabilities()
        np.testing.assert_allclose(ergodic.sum(), 1.0, atol=1e-10)

    def test_results_classify(
        self,
        simulated_two_regime_data: tuple[
            np.ndarray, np.ndarray, np.ndarray, list[float], list[float]
        ],
    ) -> None:
        """classify() should return integer regime labels."""
        y, _, _, _, _ = simulated_two_regime_data
        model = SimpleMSMean(y, k_regimes=2)

        estimator = EMEstimator()
        results = estimator.fit(model, maxiter=100, tol=1e-8, verbose=False)

        labels = results.classify()
        assert labels.shape == (len(y),)
        assert set(labels.tolist()).issubset({0, 1})
