"""Tests for Engle-Sheppard CCC vs DCC test."""

from __future__ import annotations

import numpy as np
import pytest

from archbox.diagnostics.engle_sheppard import EngleSheppardResult, engle_sheppard_test


class TestEngleSheppardRejectsCCCForDCC:
    """test_engle_sheppard_rejects_ccc: rejects CCC for DCC data."""

    def test_rejects_ccc_for_dcc(self, rng: np.random.Generator) -> None:
        T = 2000
        k = 2

        # Time-varying correlation using a sine wave
        rho_t = 0.3 + 0.4 * np.sin(2 * np.pi * np.arange(T) / 500)

        z = np.empty((T, k))
        for t in range(T):
            corr = np.array([[1, rho_t[t]], [rho_t[t], 1]])
            L = np.linalg.cholesky(corr)
            z[t] = L @ rng.standard_normal(k)

        result = engle_sheppard_test(z, lags=1)

        assert isinstance(result, EngleSheppardResult)
        assert result.pvalue < 0.10, f"Should reject CCC for DCC data, p={result.pvalue:.4f}"


class TestEngleSheppardAcceptsCCC:
    """Engle-Sheppard does not reject for true CCC data."""

    def test_accepts_ccc(self, rng: np.random.Generator) -> None:
        T = 2000
        k = 2
        rho = 0.5

        corr = np.array([[1, rho], [rho, 1]])
        L = np.linalg.cholesky(corr)

        z = np.empty((T, k))
        for t in range(T):
            z[t] = L @ rng.standard_normal(k)

        result = engle_sheppard_test(z, lags=1)

        assert (
            result.pvalue > 0.05
        ), f"Should not reject CCC for constant correlation, p={result.pvalue:.4f}"


class TestEngleSheppardEdgeCases:
    """Edge cases."""

    def test_needs_2d(self) -> None:
        z = np.random.randn(100)
        with pytest.raises(ValueError, match="2D"):
            engle_sheppard_test(z)

    def test_needs_2_series(self) -> None:
        z = np.random.randn(100, 1)
        with pytest.raises(ValueError, match="at least 2"):
            engle_sheppard_test(z)

    def test_3_series(self, rng: np.random.Generator) -> None:
        T = 500
        z = rng.standard_normal((T, 3))
        result = engle_sheppard_test(z, lags=1)
        assert isinstance(result, EngleSheppardResult)
