"""Tests for numba-optimized core functions."""

from __future__ import annotations

import numpy as np
import pytest

from archbox.utils.backend import get_backend, set_backend, use_numba
from archbox.utils.numba_core import (
    HAS_NUMBA,
    dcc_recursion_numba,
    egarch_recursion_numba,
    egarch_recursion_python,
    garch_recursion_numba,
    garch_recursion_python,
    hamilton_filter_numba,
)


class TestGARCHRecursion:
    """Test GARCH recursion equivalence."""

    def test_numba_matches_python(self):
        """Numba and Python GARCH recursion produce same results."""
        rng = np.random.default_rng(42)
        nobs = 1000
        resids = rng.standard_normal(nobs) * 0.01
        omega = 1.5e-6
        alphas = np.array([0.08])
        betas = np.array([0.91])
        backcast = float(np.var(resids))

        sigma2_numba = np.empty(nobs)
        sigma2_python = np.empty(nobs)

        garch_recursion_numba(resids, sigma2_numba, omega, alphas, betas, 1, 1, backcast)
        garch_recursion_python(resids, sigma2_python, omega, alphas, betas, 1, 1, backcast)

        np.testing.assert_allclose(sigma2_numba, sigma2_python, rtol=1e-10)

    def test_garch_variance_positive(self):
        """GARCH recursion produces positive variances."""
        rng = np.random.default_rng(42)
        nobs = 500
        resids = rng.standard_normal(nobs) * 0.01
        omega = 1e-6
        alphas = np.array([0.1])
        betas = np.array([0.85])
        backcast = float(np.var(resids))

        sigma2 = np.empty(nobs)
        garch_recursion_numba(resids, sigma2, omega, alphas, betas, 1, 1, backcast)
        assert np.all(sigma2 > 0)

    def test_garch_higher_order(self):
        """GARCH(2,2) recursion works."""
        rng = np.random.default_rng(42)
        nobs = 500
        resids = rng.standard_normal(nobs) * 0.01
        omega = 1e-6
        alphas = np.array([0.05, 0.03])
        betas = np.array([0.45, 0.45])
        backcast = float(np.var(resids))

        sigma2 = np.empty(nobs)
        garch_recursion_numba(resids, sigma2, omega, alphas, betas, 2, 2, backcast)
        assert np.all(sigma2 > 0)
        assert np.all(np.isfinite(sigma2))


class TestEGARCHRecursion:
    """Test EGARCH recursion equivalence."""

    def test_numba_matches_python(self):
        """Numba and Python EGARCH recursion produce same results."""
        rng = np.random.default_rng(42)
        nobs = 500
        resids = rng.standard_normal(nobs) * 0.01
        omega = -0.1
        alpha = 0.12
        gamma = -0.05
        beta = 0.98
        backcast = float(np.log(np.var(resids)))

        log_sigma2_numba = np.empty(nobs)
        log_sigma2_python = np.empty(nobs)

        egarch_recursion_numba(resids, log_sigma2_numba, omega, alpha, gamma, beta, backcast)
        egarch_recursion_python(resids, log_sigma2_python, omega, alpha, gamma, beta, backcast)

        np.testing.assert_allclose(log_sigma2_numba, log_sigma2_python, rtol=1e-10)


class TestHamiltonFilter:
    """Test Hamilton filter."""

    def test_filtered_probs_sum_to_one(self):
        """Filtered probabilities sum to 1."""
        rng = np.random.default_rng(42)
        nobs = 100
        k = 2
        regime_ll = rng.standard_normal((nobs, k)) * 0.5
        trans_mat = np.array([[0.95, 0.05], [0.10, 0.90]])
        init_probs = np.array([0.5, 0.5])

        filtered, predicted, _marginal_ll = hamilton_filter_numba(regime_ll, trans_mat, init_probs)

        # Filtered probs sum to 1
        prob_sums = np.sum(filtered, axis=1)
        np.testing.assert_allclose(prob_sums, 1.0, atol=1e-6)

        # Predicted probs sum to 1
        pred_sums = np.sum(predicted, axis=1)
        np.testing.assert_allclose(pred_sums, 1.0, atol=1e-6)

        # All probs in [0, 1]
        assert np.all(filtered >= -1e-10)
        assert np.all(filtered <= 1 + 1e-10)


class TestDCCRecursion:
    """Test DCC recursion."""

    def test_dcc_produces_valid_q_matrices(self):
        """DCC recursion produces symmetric Q matrices."""
        rng = np.random.default_rng(42)
        nobs = 200
        k = 2
        std_resids = rng.standard_normal((nobs, k))
        q_bar = np.corrcoef(std_resids.T)
        a = 0.05
        b = 0.93

        q_mat = dcc_recursion_numba(std_resids, q_bar, a, b)

        assert q_mat.shape == (nobs, k, k)
        # Q should be approximately symmetric
        for t in range(nobs):
            np.testing.assert_allclose(q_mat[t], q_mat[t].T, atol=1e-10)


class TestBackend:
    """Test backend management."""

    def test_set_get_backend(self):
        """set_backend / get_backend round-trips."""
        set_backend("python")
        assert get_backend() == "python"
        assert not use_numba()

        set_backend("auto")
        # Reset
        if HAS_NUMBA:
            assert get_backend() == "numba"
        else:
            assert get_backend() == "python"

    def test_invalid_backend_raises(self):
        """Invalid backend raises ValueError."""
        with pytest.raises(ValueError, match="Unknown backend"):
            set_backend("cuda")  # type: ignore[arg-type]

    def test_numba_backend_without_numba(self):
        """Forcing numba without installation raises ImportError."""
        if HAS_NUMBA:
            pytest.skip("numba is installed")
        with pytest.raises(ImportError, match="numba is not installed"):
            set_backend("numba")


class TestPerformance:
    """Test that numba version is measurably faster (if available)."""

    @pytest.mark.skipif(not HAS_NUMBA, reason="numba not installed")
    def test_numba_speedup(self):
        """Numba version should be faster than Python for large T."""
        import time

        rng = np.random.default_rng(42)
        nobs = 10000
        resids = rng.standard_normal(nobs) * 0.01
        omega = 1.5e-6
        alphas = np.array([0.08])
        betas = np.array([0.91])
        backcast = float(np.var(resids))

        # Warm up numba
        sigma2 = np.empty(nobs)
        garch_recursion_numba(resids, sigma2, omega, alphas, betas, 1, 1, backcast)

        # Time numba
        n_runs = 10
        start = time.perf_counter()
        for _ in range(n_runs):
            sigma2 = np.empty(nobs)
            garch_recursion_numba(resids, sigma2, omega, alphas, betas, 1, 1, backcast)
        numba_time = (time.perf_counter() - start) / n_runs

        # Time python
        start = time.perf_counter()
        for _ in range(n_runs):
            sigma2 = np.empty(nobs)
            garch_recursion_python(resids, sigma2, omega, alphas, betas, 1, 1, backcast)
        python_time = (time.perf_counter() - start) / n_runs

        speedup = python_time / max(numba_time, 1e-10)
        print(
            f"\nNumba speedup: {speedup:.1f}x (python={python_time * 1000:.2f}ms, "
            f"numba={numba_time * 1000:.2f}ms)"
        )
        # Numba should be at least 5x faster for T=10000
        assert speedup > 5.0
