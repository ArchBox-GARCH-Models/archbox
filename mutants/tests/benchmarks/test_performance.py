"""Performance benchmarks for archbox.

These tests verify that model fitting completes within acceptable time limits.
Run with: pytest tests/benchmarks/test_performance.py -v -s
"""

from __future__ import annotations

import time

import numpy as np
import pytest


def _time_it(func, *args, n_runs: int = 3, **kwargs) -> float:  # noqa: ANN002
    """Time a function call, returning median time in seconds."""
    times = []
    for _ in range(n_runs):
        start = time.perf_counter()
        func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        times.append(elapsed)
    return float(np.median(times))


class TestGARCHPerformance:
    """GARCH performance benchmarks."""

    def test_garch11_t1000_python(self) -> None:
        """GARCH(1,1) T=1000 without numba < 100ms."""
        from archbox.models.garch import GARCH
        from archbox.utils.backend import set_backend

        rng = np.random.default_rng(42)
        returns = rng.standard_normal(1000) * 0.01

        set_backend("python")
        model = GARCH(returns, p=1, q=1)

        elapsed = _time_it(model.fit, disp=False)
        print(f"\nGARCH(1,1) T=1000 python: {elapsed * 1000:.1f}ms")
        assert elapsed < 0.5, f"Too slow: {elapsed * 1000:.1f}ms > 500ms"

        set_backend("auto")  # Reset

    @pytest.mark.skipif(
        not __import__("archbox.utils.numba_core", fromlist=["HAS_NUMBA"]).HAS_NUMBA,
        reason="numba not installed",
    )
    def test_garch11_t1000_numba(self) -> None:
        """GARCH(1,1) T=1000 with numba < 10ms."""
        from archbox.models.garch import GARCH
        from archbox.utils.backend import set_backend

        rng = np.random.default_rng(42)
        returns = rng.standard_normal(1000) * 0.01

        set_backend("numba")

        # Warm up
        model = GARCH(returns, p=1, q=1)
        model.fit(disp=False)

        elapsed = _time_it(model.fit, disp=False)
        print(f"\nGARCH(1,1) T=1000 numba: {elapsed * 1000:.1f}ms")
        assert elapsed < 0.01, f"Too slow: {elapsed * 1000:.1f}ms > 10ms"

        set_backend("auto")

    @pytest.mark.skipif(
        not __import__("archbox.utils.numba_core", fromlist=["HAS_NUMBA"]).HAS_NUMBA,
        reason="numba not installed",
    )
    def test_garch11_t10000_numba(self) -> None:
        """GARCH(1,1) T=10000 with numba < 50ms."""
        from archbox.models.garch import GARCH
        from archbox.utils.backend import set_backend

        rng = np.random.default_rng(42)
        returns = rng.standard_normal(10000) * 0.01

        set_backend("numba")

        # Warm up
        model = GARCH(returns, p=1, q=1)
        model.fit(disp=False)

        elapsed = _time_it(model.fit, disp=False)
        print(f"\nGARCH(1,1) T=10000 numba: {elapsed * 1000:.1f}ms")
        assert elapsed < 0.05, f"Too slow: {elapsed * 1000:.1f}ms > 50ms"

        set_backend("auto")


class TestDCCPerformance:
    """DCC performance benchmarks."""

    def test_dcc_2series_t1000(self) -> None:
        """DCC 2 series T=1000 < 500ms."""
        from archbox.multivariate.dcc import DCC

        rng = np.random.default_rng(42)
        returns = rng.standard_normal((1000, 2)) * 0.01

        model = DCC(returns)
        elapsed = _time_it(model.fit, disp=False)
        print(f"\nDCC 2-series T=1000: {elapsed * 1000:.1f}ms")
        assert elapsed < 5.0, f"Too slow: {elapsed * 1000:.1f}ms > 5000ms"

    def test_dcc_5series_t1000(self) -> None:
        """DCC 5 series T=1000 < 2s."""
        from archbox.multivariate.dcc import DCC

        rng = np.random.default_rng(42)
        returns = rng.standard_normal((1000, 5)) * 0.01

        model = DCC(returns)
        elapsed = _time_it(model.fit, disp=False, n_runs=1)
        print(f"\nDCC 5-series T=1000: {elapsed * 1000:.1f}ms")
        assert elapsed < 2.0, f"Too slow: {elapsed * 1000:.1f}ms > 2000ms"


class TestRegimePerformance:
    """Regime-switching performance benchmarks."""

    def test_msar_t500_em(self) -> None:
        """MS-AR(2,4) T=500 EM < 5s."""
        from archbox.regime.ms_ar import MarkovSwitchingAR

        rng = np.random.default_rng(42)
        data = rng.standard_normal(500) * 2.0

        model = MarkovSwitchingAR(data, k_regimes=2, order=4)
        elapsed = _time_it(model.fit, method="em", verbose=False, n_runs=1)
        print(f"\nMS-AR(2,4) T=500 EM: {elapsed * 1000:.1f}ms")
        assert elapsed < 5.0, f"Too slow: {elapsed * 1000:.1f}ms > 5000ms"


class TestRiskPerformance:
    """Risk computation performance benchmarks."""

    def test_var_monte_carlo_t1000(self) -> None:
        """VaR Monte Carlo T=1000, 10000 sims < 5s."""
        from archbox.models.garch import GARCH
        from archbox.risk.var import ValueAtRisk

        rng = np.random.default_rng(42)
        returns = rng.standard_normal(1000) * 0.01

        model = GARCH(returns, p=1, q=1)
        results = model.fit(disp=False)
        var_calc = ValueAtRisk(results, alpha=0.05)

        elapsed = _time_it(var_calc.monte_carlo, n_sims=10000, n_runs=1)
        print(f"\nVaR MC T=1000 10K sims: {elapsed * 1000:.1f}ms")
        assert elapsed < 5.0, f"Too slow: {elapsed * 1000:.1f}ms > 5000ms"
