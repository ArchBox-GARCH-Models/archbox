"""Tests for Nyblom stability test."""

from __future__ import annotations

import numpy as np

from archbox.diagnostics.nyblom import NyblomResult, nyblom_test


class TestNyblomDetectsInstability:
    """test_nyblom_detects_instability: Nyblom rejects for unstable parameters."""

    def test_nyblom_detects_instability(self, rng: np.random.Generator) -> None:
        T = 1000
        k = 3

        scores1 = rng.standard_normal((T // 2, k)) + 0.0
        scores2 = rng.standard_normal((T // 2, k)) + 2.0  # shift
        scores = np.vstack([scores1, scores2])

        result = nyblom_test(scores)

        assert isinstance(result, NyblomResult)
        assert result.num_params == k

        assert result.joint_rejects_5pct, (
            f"Nyblom should detect instability, "
            f"statistic={result.joint_statistic:.4f}, "
            f"5% cv={result.critical_values_joint[1]:.4f}"
        )


class TestNyblomAcceptsStable:
    """Nyblom does not reject for stable (constant) parameters."""

    def test_nyblom_accepts_stable(self, rng: np.random.Generator) -> None:
        # Generate iid scores (constant parameters)
        # Demean so scores satisfy MLE first-order condition: sum(g_t) = 0
        T = 1000
        k = 3
        scores = rng.standard_normal((T, k))
        scores -= scores.mean(axis=0)

        result = nyblom_test(scores)

        assert not result.joint_rejects_5pct, (
            f"Nyblom should not reject for stable parameters, "
            f"statistic={result.joint_statistic:.4f}, "
            f"5% cv={result.critical_values_joint[1]:.4f}"
        )


class TestNyblomIndividual:
    """Test individual parameter statistics."""

    def test_individual_stats_shape(self, rng: np.random.Generator) -> None:
        T = 500
        k = 4
        scores = rng.standard_normal((T, k))
        result = nyblom_test(scores)

        assert len(result.individual_statistics) == k

    def test_individual_detects_single_break(self, rng: np.random.Generator) -> None:
        T = 1000
        k = 3
        scores = rng.standard_normal((T, k))

        # Add break to only parameter 0
        scores[T // 2 :, 0] += 3.0

        result = nyblom_test(scores)

        # Individual stat for param 0 should be largest
        assert result.individual_statistics[0] > result.individual_statistics[1]
        assert result.individual_statistics[0] > result.individual_statistics[2]


class TestNyblomEdgeCases:
    """Edge cases."""

    def test_1d_scores(self, rng: np.random.Generator) -> None:
        scores = rng.standard_normal(500)
        result = nyblom_test(scores)
        assert result.num_params == 1

    def test_repr(self, rng: np.random.Generator) -> None:
        scores = rng.standard_normal((500, 2))
        result = nyblom_test(scores)
        text = repr(result)
        assert "Nyblom" in text
