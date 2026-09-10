"""Tests for Nyblom stability test."""

from __future__ import annotations

import numpy as np
import pytest

from archbox.diagnostics.nyblom import (
    _CRITICAL_VALUES,
    MAX_NYBLOM_PARAMS,
    NyblomResult,
    nyblom_test,
)


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

    def test_size_under_h0(self) -> None:
        """Empirical size at 5% must be close to 5% with the Hansen table.

        With the old table (whose k >= 2 rows were far too small, e.g.
        0.574 instead of 0.749 at k = 2) this rejection rate was well above
        the nominal level.
        """
        n_mc = 300
        T = 400
        k = 3
        rejections = 0
        for i in range(n_mc):
            scores = np.random.default_rng(10_000 + i).standard_normal((T, k))
            scores -= scores.mean(axis=0)
            rejections += nyblom_test(scores).joint_rejects_5pct
        rate = rejections / n_mc
        assert 0.01 <= rate <= 0.10, f"empirical size {rate:.3f} far from 5%"


class TestNyblomCriticalValues:
    """The tabulated critical values must match Hansen (1992), Table 1."""

    @pytest.mark.parametrize(
        ("k", "expected"),
        [
            (1, (0.353, 0.470, 0.748)),
            (2, (0.610, 0.749, 1.07)),
            (3, (0.846, 1.01, 1.35)),
            (4, (1.07, 1.24, 1.60)),
            (5, (1.28, 1.47, 1.88)),
            (10, (2.29, 2.54, 3.05)),
            (15, (3.26, 3.54, 4.07)),
            (20, (4.22, 4.52, 5.13)),
        ],
    )
    def test_table_entries(self, k: int, expected: tuple[float, float, float]) -> None:
        assert _CRITICAL_VALUES[k] == pytest.approx(expected, abs=1e-12)

    def test_table_covers_1_to_20(self) -> None:
        assert sorted(_CRITICAL_VALUES) == list(range(1, MAX_NYBLOM_PARAMS + 1))

    def test_critical_values_increase_with_k_and_confidence(self) -> None:
        for k in range(1, MAX_NYBLOM_PARAMS + 1):
            cv10, cv5, cv1 = _CRITICAL_VALUES[k]
            assert cv10 < cv5 < cv1
            if k > 1:
                prev = _CRITICAL_VALUES[k - 1]
                assert cv10 > prev[0]
                assert cv5 > prev[1]
                assert cv1 > prev[2]

    def test_result_uses_the_table_for_its_k(self, rng: np.random.Generator) -> None:
        scores = rng.standard_normal((500, 4))
        result = nyblom_test(scores)
        assert result.critical_values_joint == _CRITICAL_VALUES[4]
        assert result.critical_values_individual == _CRITICAL_VALUES[1]

    def test_no_linear_scaling_beyond_the_table(self, rng: np.random.Generator) -> None:
        """k > 20 used to fall back on a bogus `k * cv(1)` extrapolation."""
        scores = rng.standard_normal((500, MAX_NYBLOM_PARAMS + 1))
        with pytest.raises(ValueError, match="no tabulated"):
            nyblom_test(scores)

    def test_asymptotic_null_matches_the_table(self) -> None:
        """Simulate int_0^1 ||B_k(r)||^2 dr and compare with the table.

        The joint statistic converges to that Cramer-von Mises functional of
        a k-dimensional Brownian bridge.
        """
        rng = np.random.default_rng(2024)
        n_grid = 500
        n_rep = 20_000
        grid = np.arange(1, n_grid + 1) / n_grid
        noise = rng.standard_normal((n_rep, n_grid)) / np.sqrt(n_grid)
        bridge = np.cumsum(noise, axis=1)
        bridge -= np.outer(bridge[:, -1], grid)
        cvm = (bridge**2).mean(axis=1)

        for k in (1, 2, 3, 5):
            draws = cvm[: (n_rep // k) * k].reshape(-1, k).sum(axis=1)
            simulated = np.quantile(draws, [0.90, 0.95])
            tabulated = _CRITICAL_VALUES[k][:2]
            assert simulated == pytest.approx(
                tabulated, rel=0.05
            ), f"k={k}: simulated {simulated} vs table {tabulated}"


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

    def test_too_few_observations(self, rng: np.random.Generator) -> None:
        scores = rng.standard_normal((3, 4))
        with pytest.raises(ValueError, match="T > k"):
            nyblom_test(scores)

    def test_rejects_3d_input(self, rng: np.random.Generator) -> None:
        with pytest.raises(ValueError, match="1D or 2D"):
            nyblom_test(rng.standard_normal((10, 3, 2)))
