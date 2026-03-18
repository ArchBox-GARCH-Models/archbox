"""Tests for Hong volatility spillover test."""

from __future__ import annotations

import numpy as np
import pytest

from archbox.diagnostics.hong_spillover import HongSpilloverResult, hong_spillover_test


class TestHongDetectsSpillover:
    """Hong detects volatility spillover."""

    def test_detects_spillover(self, rng: np.random.Generator) -> None:
        T = 2000
        z2 = rng.standard_normal(T)

        sigma2_1 = np.empty(T)
        z1 = np.empty(T)
        sigma2_1[0] = 1.0
        z1[0] = rng.standard_normal()

        for t in range(1, T):
            # Spillover: vol of series 1 depends on squared shocks from series 2
            sigma2_1[t] = 0.5 + 0.3 * z2[t - 1] ** 2 + 0.2 * sigma2_1[t - 1]
            z1[t] = np.sqrt(sigma2_1[t]) * rng.standard_normal()

        # Standardize (approx)
        z1_std = z1 / np.std(z1)
        z2_std = z2 / np.std(z2)

        result = hong_spillover_test(z1_std, z2_std, bandwidth=10)

        assert isinstance(result, HongSpilloverResult)
        assert (
            result.statistic > 0
        ), f"Hong statistic should be positive with spillover, got {result.statistic:.4f}"


class TestHongNoSpillover:
    """Hong does not reject for independent series."""

    def test_no_spillover(self, rng: np.random.Generator) -> None:
        T = 2000
        z1 = rng.standard_normal(T)
        z2 = rng.standard_normal(T)

        result = hong_spillover_test(z1, z2, bandwidth=10)

        assert (
            result.pvalue > 0.01
        ), f"Hong should not strongly reject for independent series, p={result.pvalue:.4f}"


class TestHongEdgeCases:
    """Edge cases."""

    def test_mismatched_lengths(self) -> None:
        with pytest.raises(ValueError, match="same length"):
            hong_spillover_test(np.random.randn(100), np.random.randn(50))

    def test_auto_bandwidth(self, rng: np.random.Generator) -> None:
        z1 = rng.standard_normal(1000)
        z2 = rng.standard_normal(1000)
        result = hong_spillover_test(z1, z2)
        # bandwidth should be floor(T^(1/3)) = floor(9.999...) = 9
        assert result.bandwidth == 9
