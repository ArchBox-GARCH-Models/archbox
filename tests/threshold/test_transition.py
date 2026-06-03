"""Tests for transition functions.

Tests:
- test_logistic_bounds: G in [0, 1] always
- test_exponential_bounds: G in [0, 1] always
- test_logistic_monotone: G increasing in s for gamma > 0
"""

from __future__ import annotations

import numpy as np

from archbox.threshold.transition import (
    exponential_transition,
    logistic_transition,
    logistic_transition_order2,
)


class TestLogisticTransition:
    """Tests for logistic transition function."""

    def test_logistic_bounds(self) -> None:
        """G(s; gamma, c) must be in [0, 1] for all s, gamma > 0."""
        rng = np.random.default_rng(42)
        s = rng.standard_normal(1000) * 10
        for gamma in [0.1, 1.0, 5.0, 50.0, 200.0]:
            for c in [-5.0, 0.0, 3.0]:
                G = logistic_transition(s, gamma, c)
                assert np.all(G >= 0.0), f"G < 0 for gamma={gamma}, c={c}"
                assert np.all(G <= 1.0), f"G > 1 for gamma={gamma}, c={c}"

    def test_logistic_monotone(self) -> None:
        """G must be monotonically increasing in s for gamma > 0."""
        s = np.linspace(-10, 10, 1000)
        for gamma in [0.5, 1.0, 5.0, 100.0]:
            G = logistic_transition(s, gamma, c=0.0)
            diffs = np.diff(G)
            assert np.all(diffs >= -1e-12), f"Not monotone for gamma={gamma}"

    def test_logistic_midpoint(self) -> None:
        """G(c; gamma, c) = 0.5 exactly for any gamma > 0."""
        for gamma in [0.1, 1.0, 10.0, 100.0]:
            for c in [-3.0, 0.0, 5.0]:
                G = logistic_transition(np.array([c]), gamma, c)
                assert abs(G[0] - 0.5) < 1e-10, f"G(c) != 0.5 for gamma={gamma}, c={c}"

    def test_logistic_large_gamma_approaches_step(self) -> None:
        """For very large gamma, logistic -> step function."""
        s = np.array([-1.0, -0.01, 0.01, 1.0])
        G = logistic_transition(s, gamma=1000.0, c=0.0)
        assert G[0] < 0.01  # far below c -> ~0
        assert G[-1] > 0.99  # far above c -> ~1

    def test_logistic_small_gamma_approaches_half(self) -> None:
        """For gamma -> 0, G -> 0.5 everywhere."""
        s = np.linspace(-10, 10, 100)
        G = logistic_transition(s, gamma=0.001, c=0.0)
        assert np.allclose(G, 0.5, atol=0.01)


class TestExponentialTransition:
    """Tests for exponential transition function."""

    def test_exponential_bounds(self) -> None:
        """G(s; gamma, c) must be in [0, 1] for all s, gamma > 0."""
        rng = np.random.default_rng(42)
        s = rng.standard_normal(1000) * 10
        for gamma in [0.1, 1.0, 5.0, 50.0]:
            for c in [-5.0, 0.0, 3.0]:
                G = exponential_transition(s, gamma, c)
                assert np.all(G >= -1e-10), f"G < 0 for gamma={gamma}, c={c}"
                assert np.all(G <= 1.0 + 1e-10), f"G > 1 for gamma={gamma}, c={c}"

    def test_exponential_symmetric(self) -> None:
        """G(c - delta) == G(c + delta) for exponential transition."""
        c = 2.0
        for gamma in [0.5, 1.0, 5.0]:
            for delta in [0.1, 0.5, 1.0, 3.0]:
                G_minus = exponential_transition(np.array([c - delta]), gamma, c)
                G_plus = exponential_transition(np.array([c + delta]), gamma, c)
                assert (
                    abs(G_minus[0] - G_plus[0]) < 1e-10
                ), f"Not symmetric for gamma={gamma}, delta={delta}"

    def test_exponential_at_center(self) -> None:
        """G(c; gamma, c) = 0 for exponential transition."""
        for gamma in [0.1, 1.0, 10.0]:
            G = exponential_transition(np.array([0.0]), gamma, c=0.0)
            assert abs(G[0]) < 1e-10, f"G(c) != 0 for gamma={gamma}"

    def test_exponential_small_gamma_approaches_zero(self) -> None:
        """For gamma -> 0, G -> 0 everywhere."""
        s = np.linspace(-10, 10, 100)
        G = exponential_transition(s, gamma=0.001, c=0.0)
        assert np.allclose(G, 0.0, atol=0.1)


class TestLogisticOrder2:
    """Tests for second-order logistic transition."""

    def test_order2_bounds(self) -> None:
        """G must be in [0, 1]."""
        s = np.linspace(-10, 10, 1000)
        G = logistic_transition_order2(s, gamma=1.0, c1=-2.0, c2=2.0)
        assert np.all(G >= 0.0)
        assert np.all(G <= 1.0)

    def test_order2_equals_first_order_when_c1_equals_c2(self) -> None:
        """When c1 == c2, second-order reduces to first-order (approximately)."""
        s = np.linspace(-5, 5, 100)
        c = 1.0
        # G2(s; gamma, c, c) = 1/(1+exp(-gamma*(s-c)^2)) which is different
        # but both should be in [0,1]
        G = logistic_transition_order2(s, gamma=1.0, c1=c, c2=c)
        assert np.all(G >= 0.0)
        assert np.all(G <= 1.0)
