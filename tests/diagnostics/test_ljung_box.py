"""Tests for Ljung-Box on squared residuals."""

from __future__ import annotations

import numpy as np
import pytest

from archbox.diagnostics.ljung_box import LjungBoxResult, ljung_box_squared


class TestLjungBoxRejectsARCH:
    """Ljung-Box rejects for series with ARCH effects."""

    def test_rejects_arch_in_raw(self, rng: np.random.Generator) -> None:
        # ARCH(1) process -> squared residuals are autocorrelated
        n = 2000
        omega, alpha = 0.1, 0.7

        e = np.empty(n)
        sigma2 = np.empty(n)
        sigma2[0] = omega / (1 - alpha)
        e[0] = np.sqrt(sigma2[0]) * rng.standard_normal()

        for t in range(1, n):
            sigma2[t] = omega + alpha * e[t - 1] ** 2
            e[t] = np.sqrt(sigma2[t]) * rng.standard_normal()

        # Treat raw residuals as if "standardized" by constant sigma
        result = ljung_box_squared(e / np.std(e), lags=10)

        assert isinstance(result, LjungBoxResult)
        assert result.pvalue < 0.05, (
            f"Ljung-Box should reject for ARCH process, p={result.pvalue:.4f}"
        )


class TestLjungBoxAcceptsIID:
    """Ljung-Box does not reject for iid N(0,1)."""

    def test_accepts_iid(self, rng: np.random.Generator) -> None:
        z = rng.standard_normal(2000)
        result = ljung_box_squared(z, lags=10)

        assert result.pvalue > 0.05, f"Ljung-Box should not reject for iid, p={result.pvalue:.4f}"


class TestLjungBoxAcceptsGARCHResiduals:
    """Ljung-Box does not reject GARCH standardized residuals."""

    def test_accepts_garch_residuals(self, rng: np.random.Generator) -> None:
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

        std_resids = returns / np.sqrt(sigma2)
        result = ljung_box_squared(std_resids, lags=10)

        assert result.pvalue > 0.05, (
            f"Ljung-Box should not reject GARCH residuals, p={result.pvalue:.4f}"
        )


class TestLjungBoxEdgeCases:
    """Edge case tests."""

    def test_different_lags(self, rng: np.random.Generator) -> None:
        z = rng.standard_normal(500)

        for lags in [1, 5, 10, 20]:
            result = ljung_box_squared(z, lags=lags)
            assert result.lags == lags
            assert result.statistic >= 0
            assert 0 <= result.pvalue <= 1

    def test_lags_too_large(self) -> None:
        z = np.random.randn(20)
        with pytest.raises(ValueError, match="lags"):
            ljung_box_squared(z, lags=20)
