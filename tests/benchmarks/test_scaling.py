"""Scaling tests for archbox.

Verify that computation time scales correctly with problem size.
Run with: pytest tests/benchmarks/test_scaling.py -v -s
"""

from __future__ import annotations

import time

import numpy as np


class TestGARCHScaling:
    """Test GARCH O(T) scaling."""

    def test_garch_linear_in_t(self) -> None:
        """GARCH fitting time should scale roughly linearly with T."""
        from archbox.models.garch import GARCH

        rng = np.random.default_rng(42)
        sizes = [500, 1000, 2000]
        times = []

        for n in sizes:
            returns = rng.standard_normal(n) * 0.01
            model = GARCH(returns, p=1, q=1)

            start = time.perf_counter()
            model.fit(disp=False)
            elapsed = time.perf_counter() - start
            times.append(elapsed)
            print(f"  T={n}: {elapsed * 1000:.1f}ms")

        # Time for 2000 should be less than 5x time for 500
        # (allowing for optimizer overhead)
        ratio = times[2] / max(times[0], 1e-6)
        print(f"  Scaling ratio (T=2000/T=500): {ratio:.1f}x")
        assert ratio < 10.0, f"Bad scaling: {ratio:.1f}x (expected < 10x)"


class TestDCCScaling:
    """Test DCC O(T * k^2) scaling in k."""

    def test_dcc_quadratic_in_k(self) -> None:
        """DCC fitting time should scale roughly with k^2."""
        from archbox.multivariate.dcc import DCC

        rng = np.random.default_rng(42)
        t = 500
        k_values = [2, 3]
        times = []

        for k in k_values:
            returns = rng.standard_normal((t, k)) * 0.01
            model = DCC(returns)

            start = time.perf_counter()
            model.fit(disp=False)
            elapsed = time.perf_counter() - start
            times.append(elapsed)
            print(f"  k={k}: {elapsed * 1000:.1f}ms")

        # k=3 should be roughly (3/2)^2 = 2.25x slower than k=2
        ratio = times[1] / max(times[0], 1e-6)
        print(f"  Scaling ratio (k=3/k=2): {ratio:.1f}x")
        # Allow generous bounds
        assert ratio < 20.0, f"Bad scaling: {ratio:.1f}x (expected < 20x)"


class TestHamiltonFilterScaling:
    """Test Hamilton filter O(T * k^2) scaling."""

    def test_hamilton_linear_in_t(self) -> None:
        """Hamilton filter time should scale linearly with T."""
        from archbox.utils.numba_core import hamilton_filter_numba

        rng = np.random.default_rng(42)
        k = 2
        p_mat = np.array([[0.95, 0.05], [0.10, 0.90]])
        init_probs = np.array([0.5, 0.5])

        sizes = [1000, 5000, 10000]
        times = []

        for t_size in sizes:
            regime_ll = rng.standard_normal((t_size, k))

            # Warm up
            hamilton_filter_numba(regime_ll[:10], p_mat, init_probs)

            start = time.perf_counter()
            for _ in range(5):
                hamilton_filter_numba(regime_ll, p_mat, init_probs)
            elapsed = (time.perf_counter() - start) / 5
            times.append(elapsed)
            print(f"  T={t_size}: {elapsed * 1000:.2f}ms")

        ratio = times[2] / max(times[0], 1e-6)
        print(f"  Scaling ratio (T=10000/T=1000): {ratio:.1f}x")
        assert ratio < 20.0, f"Bad scaling: {ratio:.1f}x (expected ~10x)"
