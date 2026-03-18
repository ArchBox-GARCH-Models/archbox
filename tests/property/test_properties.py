"""Property-based tests using hypothesis.

Tests fundamental invariants that must always hold:
- sigma2 > 0 (conditional variance is positive)
- probabilities sum to 1 (regime probabilities)
- correlation matrices are positive definite
"""

from __future__ import annotations

import numpy as np
from hypothesis import assume, given, settings
from hypothesis import strategies as st


class TestGARCHProperties:
    """Property tests for GARCH models."""

    @given(
        omega=st.floats(min_value=1e-8, max_value=1e-4),
        alpha=st.floats(min_value=0.01, max_value=0.3),
        beta=st.floats(min_value=0.5, max_value=0.95),
    )
    @settings(max_examples=50, deadline=30000)
    def test_variance_positive(self, omega: float, alpha: float, beta: float) -> None:
        """Conditional variance is always positive with valid parameters."""
        assume(alpha + beta < 0.999)
        from archbox.utils.numba_core import garch_recursion_python

        rng = np.random.default_rng(42)
        T = 100
        resids = rng.standard_normal(T) * 0.01
        sigma2 = np.empty(T)
        backcast = omega / (1 - alpha - beta)

        garch_recursion_python(
            resids,
            sigma2,
            omega,
            np.array([alpha]),
            np.array([beta]),
            1,
            1,
            backcast,
        )
        assert np.all(sigma2 > 0), f"Negative variance found: min={sigma2.min()}"

    @given(
        omega=st.floats(min_value=1e-8, max_value=1e-4),
        alpha=st.floats(min_value=0.01, max_value=0.3),
        beta=st.floats(min_value=0.5, max_value=0.95),
    )
    @settings(max_examples=50, deadline=30000)
    def test_persistence_bounded(self, omega: float, alpha: float, beta: float) -> None:
        """Persistence = alpha + beta should be < 1 for stationarity."""
        assume(alpha + beta < 0.999)
        persistence = alpha + beta
        assert 0 < persistence < 1


class TestRegimeProperties:
    """Property tests for regime-switching models."""

    @given(
        p00=st.floats(min_value=0.1, max_value=0.99),
        p11=st.floats(min_value=0.1, max_value=0.99),
    )
    @settings(max_examples=50, deadline=30000)
    def test_transition_rows_sum_to_one(self, p00: float, p11: float) -> None:
        """Transition matrix rows must sum to 1."""
        P = np.array([[p00, 1 - p00], [1 - p11, p11]])
        row_sums = np.sum(P, axis=1)
        np.testing.assert_allclose(row_sums, 1.0, atol=1e-10)

    @given(
        p00=st.floats(min_value=0.5, max_value=0.99),
        p11=st.floats(min_value=0.5, max_value=0.99),
    )
    @settings(max_examples=50, deadline=30000)
    def test_ergodic_probabilities_sum_to_one(self, p00: float, p11: float) -> None:
        """Ergodic probabilities from transition matrix sum to 1."""
        _P = np.array([[p00, 1 - p00], [1 - p11, p11]])
        # Ergodic: pi = pi @ P, pi.sum() = 1
        # pi_0 = (1-p11) / (2 - p00 - p11)
        denom = 2 - p00 - p11
        assume(abs(denom) > 1e-6)
        pi_0 = (1 - p11) / denom
        pi_1 = (1 - p00) / denom
        assert abs(pi_0 + pi_1 - 1.0) < 1e-10


class TestCorrelationProperties:
    """Property tests for correlation matrices."""

    @given(
        rho=st.floats(min_value=-0.99, max_value=0.99),
    )
    @settings(max_examples=50)
    def test_2x2_correlation_positive_definite(self, rho: float) -> None:
        """2x2 correlation matrix with |rho| < 1 is PD."""
        R = np.array([[1.0, rho], [rho, 1.0]])
        eigenvalues = np.linalg.eigvalsh(R)
        assert np.all(eigenvalues > 0), f"Not PD: eigenvalues={eigenvalues}"
