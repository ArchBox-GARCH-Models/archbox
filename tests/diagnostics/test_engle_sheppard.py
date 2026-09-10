"""Tests for Engle-Sheppard CCC vs DCC test."""

from __future__ import annotations

import numpy as np
import pytest
from scipy import stats

from archbox.diagnostics.engle_sheppard import EngleSheppardResult, engle_sheppard_test


def _simulate_dcc(rng: np.random.Generator, n_obs: int, k: int) -> np.ndarray:
    """Simulate a DCC(1,1) correlation recursion with unit-variance shocks."""
    a, b = 0.05, 0.93
    q_bar = np.full((k, k), 0.3) + 0.7 * np.eye(k)
    q = q_bar.copy()
    eps = np.zeros(k)
    out = np.empty((n_obs, k))
    for t in range(n_obs):
        q = q_bar * (1 - a - b) + a * np.outer(eps, eps) + b * q
        scale = np.sqrt(np.diag(q))
        corr = q / np.outer(scale, scale)
        eps = np.linalg.cholesky(corr) @ rng.standard_normal(k)
        out[t] = eps
    return out


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

    def test_rejects_dcc_recursion(self, rng: np.random.Generator) -> None:
        z = _simulate_dcc(rng, 1500, 3)

        result = engle_sheppard_test(z, lags=5)

        assert result.pvalue < 0.01, f"Should reject CCC for DCC(1,1) data, p={result.pvalue:.4f}"


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


class TestEngleSheppardSize:
    """Monte-Carlo size of the test under H0."""

    @pytest.mark.parametrize("lags", [1, 5])
    def test_size_under_h0(self, lags: int) -> None:
        """Rejection rate at the 5% level for k=3, T=500.

        The previous implementation averaged the per-pair T*R^2 statistics
        and compared that average with chi2(q), which never rejected
        (empirical size 0%). The pooled Engle-Sheppard regression has a
        usable, mildly conservative size instead.
        """
        n_mc = 200
        rejections = 0
        for i in range(n_mc):
            z = np.random.default_rng(i).standard_normal((500, 3))
            rejections += engle_sheppard_test(z, lags=lags).pvalue < 0.05
        rate = rejections / n_mc
        assert 0.01 <= rate <= 0.09, f"empirical size {rate:.3f} at lags={lags}"


class TestEngleSheppardStatistic:
    """Structure of the statistic itself."""

    def test_pvalue_is_chi2_sf_with_q_plus_one_df(self, rng: np.random.Generator) -> None:
        z = rng.standard_normal((800, 3))
        result = engle_sheppard_test(z, lags=4)

        assert result.pvalue == pytest.approx(
            float(stats.chi2.sf(result.statistic, df=5)), rel=1e-12
        )

    def test_statistic_is_non_negative(self, rng: np.random.Generator) -> None:
        for seed in range(5):
            z = np.random.default_rng(seed).standard_normal((300, 4))
            assert engle_sheppard_test(z, lags=2).statistic >= 0.0

    def test_invariant_to_series_order(self, rng: np.random.Generator) -> None:
        z = _simulate_dcc(rng, 800, 3)
        base = engle_sheppard_test(z, lags=2)
        permuted = engle_sheppard_test(z[:, [2, 0, 1]], lags=2)

        assert permuted.statistic == pytest.approx(base.statistic, rel=1e-8)


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

    def test_rejects_non_positive_lags(self, rng: np.random.Generator) -> None:
        with pytest.raises(ValueError, match="lags must be"):
            engle_sheppard_test(rng.standard_normal((100, 2)), lags=0)

    def test_rejects_too_many_lags(self, rng: np.random.Generator) -> None:
        with pytest.raises(ValueError, match="less than"):
            engle_sheppard_test(rng.standard_normal((20, 2)), lags=25)

    def test_rejects_singular_correlation(self) -> None:
        base = np.random.default_rng(0).standard_normal((200, 1))
        z = np.column_stack([base, base])  # perfectly correlated
        with pytest.raises(ValueError, match="positive definite"):
            engle_sheppard_test(z, lags=1)
