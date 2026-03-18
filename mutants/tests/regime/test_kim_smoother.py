"""Tests for Kim Smoother.

Test suite following the spec:
- test_smoothed_probs_sum_to_one
- test_smoothed_leq_one
- test_smoothed_last_equals_filtered
- test_smoothed_smoother_than_filtered
"""

from __future__ import annotations

import numpy as np
import pytest

from archbox.regime.hamilton_filter import HamiltonFilter
from archbox.regime.kim_smoother import KimSmoother


@pytest.fixture
def filter_results():
    """Run Hamilton filter on synthetic two-regime data and return results."""
    rng = np.random.default_rng(123)
    T = 300
    P = np.array([[0.95, 0.05], [0.10, 0.90]])

    regimes = np.zeros(T, dtype=int)
    regimes[0] = 1
    for t in range(1, T):
        regimes[t] = rng.choice(2, p=P[regimes[t - 1]])

    mu = [-2.0, 2.0]
    sigma = [0.5, 0.5]
    y = np.array([mu[s] + sigma[s] * rng.standard_normal() for s in regimes])

    # Pre-compute regime log-likelihoods
    k = 2
    regime_lls = np.zeros((T, k))
    for t in range(T):
        for s in range(k):
            regime_lls[t, s] = (
                -0.5 * np.log(2 * np.pi) - np.log(sigma[s]) - 0.5 * ((y[t] - mu[s]) / sigma[s]) ** 2
            )

    hfilter = HamiltonFilter()
    filtered, predicted, loglike, marginal = hfilter.filter_vectorized(regime_lls, P)

    return {
        "y": y,
        "regimes": regimes,
        "P": P,
        "mu": mu,
        "sigma": sigma,
        "filtered": filtered,
        "predicted": predicted,
        "loglike": loglike,
    }


class TestKimSmootherProbabilities:
    """Test smoothed probability constraints."""

    def test_smoothed_probs_sum_to_one(self, filter_results):
        """sum(xi_{t|T}) == 1 for all t (tol=1e-10)."""
        smoother = KimSmoother()
        smoothed = smoother.smooth(
            filter_results["filtered"],
            filter_results["predicted"],
            filter_results["P"],
        )

        row_sums = smoothed.sum(axis=1)
        np.testing.assert_allclose(row_sums, np.ones(len(row_sums)), atol=1e-10)

    def test_smoothed_leq_one(self, filter_results):
        """0 <= xi_{t|T}(j) <= 1 for all t, j."""
        smoother = KimSmoother()
        smoothed = smoother.smooth(
            filter_results["filtered"],
            filter_results["predicted"],
            filter_results["P"],
        )

        assert np.all(smoothed >= -1e-10)
        assert np.all(smoothed <= 1.0 + 1e-10)

    def test_smoothed_last_equals_filtered(self, filter_results):
        """xi_{T|T} == xi_{T|T} (last point identical)."""
        smoother = KimSmoother()
        smoothed = smoother.smooth(
            filter_results["filtered"],
            filter_results["predicted"],
            filter_results["P"],
        )

        np.testing.assert_allclose(smoothed[-1], filter_results["filtered"][-1], atol=1e-10)

    def test_smoothed_smoother_than_filtered(self, filter_results):
        """Smoothed probs should be less volatile than filtered probs.

        The standard deviation of smoothed probabilities across time
        should not exceed that of filtered probabilities (they use
        more information, so they are smoother).
        """
        smoother = KimSmoother()
        smoothed = smoother.smooth(
            filter_results["filtered"],
            filter_results["predicted"],
            filter_results["P"],
        )

        filtered = filter_results["filtered"]

        # Compare variance of regime 0 probability time series
        filtered_var = np.var(np.diff(filtered[:, 0]))
        smoothed_var = np.var(np.diff(smoothed[:, 0]))

        # Smoothed should have smaller or similar variance in differences
        # (less jumpy)
        assert (
            smoothed_var <= filtered_var * 1.1
        ), f"Smoothed variance {smoothed_var:.6f} > Filtered variance {filtered_var:.6f}"


class TestKimSmootherVectorized:
    """Test vectorized implementation matches loop version."""

    def test_vectorized_matches_loop(self, filter_results):
        """Vectorized smooth should match loop-based smooth."""
        smoother = KimSmoother()

        smoothed_loop = smoother.smooth(
            filter_results["filtered"],
            filter_results["predicted"],
            filter_results["P"],
        )
        smoothed_vec = smoother.smooth_vectorized(
            filter_results["filtered"],
            filter_results["predicted"],
            filter_results["P"],
        )

        np.testing.assert_allclose(smoothed_loop, smoothed_vec, atol=1e-10)


class TestKimSmootherJoint:
    """Test joint smoothed probabilities."""

    def test_joint_smoothed_shape(self, filter_results):
        """Joint smoothed should have shape (T-1, k, k)."""
        smoother = KimSmoother()
        smoothed = smoother.smooth(
            filter_results["filtered"],
            filter_results["predicted"],
            filter_results["P"],
        )
        joint = smoother.joint_smoothed(
            filter_results["filtered"],
            filter_results["predicted"],
            smoothed,
            filter_results["P"],
        )

        T = filter_results["filtered"].shape[0]
        k = filter_results["P"].shape[0]
        assert joint.shape == (T - 1, k, k)

    def test_joint_smoothed_sum_to_one(self, filter_results):
        """sum_{i,j} P(S_t=i, S_{t+1}=j | Y_T) == 1 for all t."""
        smoother = KimSmoother()
        smoothed = smoother.smooth(
            filter_results["filtered"],
            filter_results["predicted"],
            filter_results["P"],
        )
        joint = smoother.joint_smoothed(
            filter_results["filtered"],
            filter_results["predicted"],
            smoothed,
            filter_results["P"],
        )

        for t in range(joint.shape[0]):
            np.testing.assert_allclose(joint[t].sum(), 1.0, atol=1e-8)

    def test_joint_smoothed_nonnegative(self, filter_results):
        """Joint smoothed probabilities should be non-negative."""
        smoother = KimSmoother()
        smoothed = smoother.smooth(
            filter_results["filtered"],
            filter_results["predicted"],
            filter_results["P"],
        )
        joint = smoother.joint_smoothed(
            filter_results["filtered"],
            filter_results["predicted"],
            smoothed,
            filter_results["P"],
        )

        assert np.all(joint >= -1e-10)

    def test_joint_marginal_consistency(self, filter_results):
        """sum_j P(S_t=i, S_{t+1}=j | Y_T) ~ P(S_t=i | Y_T) for interior t."""
        smoother = KimSmoother()
        smoothed = smoother.smooth(
            filter_results["filtered"],
            filter_results["predicted"],
            filter_results["P"],
        )
        joint = smoother.joint_smoothed(
            filter_results["filtered"],
            filter_results["predicted"],
            smoothed,
            filter_results["P"],
        )

        # For t in interior (not first or last), marginal should match smoothed
        for t in range(1, joint.shape[0] - 1):
            marginal_i = joint[t].sum(axis=1)  # sum over j -> P(S_t=i|Y_T)
            np.testing.assert_allclose(marginal_i, smoothed[t], atol=0.05)


class TestKimSmootherThreeRegimes:
    """Test smoother with 3 regimes."""

    def test_three_regimes(self):
        """Smoother should work with k=3."""
        rng = np.random.default_rng(42)
        T = 200
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

        regime_lls = np.zeros((T, k))
        for t in range(T):
            for s in range(k):
                regime_lls[t, s] = (
                    -0.5 * np.log(2 * np.pi)
                    - np.log(sigma[s])
                    - 0.5 * ((y[t] - mu[s]) / sigma[s]) ** 2
                )

        hfilter = HamiltonFilter()
        filtered, predicted, _, _ = hfilter.filter_vectorized(regime_lls, P)

        smoother = KimSmoother()
        smoothed = smoother.smooth(filtered, predicted, P)

        assert smoothed.shape == (T, k)
        np.testing.assert_allclose(smoothed.sum(axis=1), np.ones(T), atol=1e-10)
        np.testing.assert_allclose(smoothed[-1], filtered[-1], atol=1e-10)
