"""Tests for ARCH-LM test."""

from __future__ import annotations

import numpy as np
import pytest
from scipy import stats

from archbox.diagnostics.arch_lm import TestResult, arch_lm_test


class TestArchLMRejectsARCH:
    """test_arch_lm_rejects_arch: ARCH-LM rejects for series with ARCH effects."""

    def test_arch_lm_rejects_arch(self, rng: np.random.Generator) -> None:
        # Generate ARCH(1) process
        n = 2000
        omega = 0.1
        alpha = 0.7

        e = np.empty(n)
        sigma2 = np.empty(n)
        sigma2[0] = omega / (1 - alpha)
        e[0] = np.sqrt(sigma2[0]) * rng.standard_normal()

        for t in range(1, n):
            sigma2[t] = omega + alpha * e[t - 1] ** 2
            e[t] = np.sqrt(sigma2[t]) * rng.standard_normal()

        result = arch_lm_test(e, lags=5)

        assert isinstance(result, TestResult)
        assert result.test_name == "ARCH-LM"
        assert (
            result.pvalue < 0.05
        ), f"ARCH-LM should reject for ARCH process, p={result.pvalue:.4f}"


class TestArchLMAcceptsIID:
    """test_arch_lm_accepts_iid: ARCH-LM does not reject for iid N(0,1)."""

    def test_arch_lm_accepts_iid(self, rng: np.random.Generator) -> None:
        e = rng.standard_normal(2000)
        result = arch_lm_test(e, lags=5)

        assert (
            result.pvalue > 0.05
        ), f"ARCH-LM should not reject for iid N(0,1), p={result.pvalue:.4f}"


class TestArchLMAfterGARCH:
    """test_arch_lm_after_garch: ARCH-LM does not reject standardized GARCH residuals."""

    def test_arch_lm_after_garch(self, rng: np.random.Generator) -> None:
        # Generate GARCH(1,1) and compute standardized residuals
        n = 2000
        omega, alpha, beta = 1e-6, 0.08, 0.91

        sigma2 = np.empty(n)
        returns = np.empty(n)
        sigma2[0] = omega / (1 - alpha - beta)

        for t in range(n):
            if t > 0:
                sigma2[t] = omega + alpha * returns[t - 1] ** 2 + beta * sigma2[t - 1]
            z = rng.standard_normal()
            returns[t] = np.sqrt(sigma2[t]) * z

        # Standardized residuals (using true sigma)
        std_resids = returns / np.sqrt(sigma2)

        result = arch_lm_test(std_resids, lags=5)

        assert (
            result.pvalue > 0.05
        ), f"ARCH-LM should not reject for GARCH standardized residuals, p={result.pvalue:.4f}"


class TestArchLMEdgeCases:
    """Edge cases for ARCH-LM."""

    def test_different_lags(self, rng: np.random.Generator) -> None:
        e = rng.standard_normal(500)

        for lags in [1, 5, 10]:
            result = arch_lm_test(e, lags=lags)
            assert result.lags == lags
            assert result.statistic >= 0
            assert 0 <= result.pvalue <= 1

    def test_lags_too_large(self) -> None:
        e = np.random.randn(20)
        with pytest.raises(ValueError, match="lags"):
            arch_lm_test(e, lags=19)


class TestArchLMResultDataclass:
    """The TestResult container must not be collected as a pytest test."""

    def test_test_attribute_is_false(self) -> None:
        assert TestResult.__test__ is False


class TestArchLMTailPrecision:
    """p-values come from the survival function, not from 1 - cdf."""

    def test_pvalue_is_positive_deep_in_the_tail(self, rng: np.random.Generator) -> None:
        n = 3000
        omega, alpha = 0.1, 0.85

        e = np.empty(n)
        sigma2 = np.empty(n)
        sigma2[0] = omega / (1 - alpha)
        e[0] = np.sqrt(sigma2[0]) * rng.standard_normal()
        for t in range(1, n):
            sigma2[t] = omega + alpha * e[t - 1] ** 2
            e[t] = np.sqrt(sigma2[t]) * rng.standard_normal()

        result = arch_lm_test(e, lags=5)

        # Large enough that 1 - chi2.cdf(stat) rounds to exactly 0.0.
        assert result.statistic > 100.0
        assert result.pvalue > 0.0
        assert result.pvalue == pytest.approx(
            float(stats.chi2.sf(result.statistic, df=5)), rel=1e-12
        )
