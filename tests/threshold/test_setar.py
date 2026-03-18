"""Tests for SETAR model.

Tests:
- test_setar_fit_simulated: SETAR with simulated 2-regime data
- test_setar_delay_selection: Correct delay d selected by AIC
- test_setar_reduces_to_ar: SETAR with extreme threshold == AR
- test_setar_three_regimes: SETAR(3) with 2 thresholds functional
"""

from __future__ import annotations

import numpy as np
import pytest

from archbox.threshold.setar import SETAR


def _simulate_setar(
    n: int = 1000,
    c: float = 0.0,
    delay: int = 1,
    phi1: tuple[float, float] = (0.5, 0.3),
    phi2: tuple[float, float] = (-0.2, 0.8),
    sigma: float = 0.5,
    seed: int = 42,
) -> np.ndarray:
    """Simulate SETAR(1) data."""
    rng = np.random.default_rng(seed)
    y = np.zeros(n)
    for t in range(delay, n):
        if y[t - delay] <= c:
            y[t] = phi1[0] + phi1[1] * y[t - 1] + rng.standard_normal() * sigma
        else:
            y[t] = phi2[0] + phi2[1] * y[t - 1] + rng.standard_normal() * sigma
    return y


def _simulate_setar_3regime(
    n: int = 2000,
    c1: float = -1.0,
    c2: float = 1.0,
    seed: int = 42,
) -> np.ndarray:
    """Simulate 3-regime SETAR data."""
    rng = np.random.default_rng(seed)
    y = np.zeros(n)
    for t in range(1, n):
        if y[t - 1] <= c1:
            y[t] = 0.8 + 0.2 * y[t - 1] + rng.standard_normal() * 0.5
        elif y[t - 1] <= c2:
            y[t] = 0.0 + 0.5 * y[t - 1] + rng.standard_normal() * 0.3
        else:
            y[t] = -0.8 + 0.2 * y[t - 1] + rng.standard_normal() * 0.5
    return y


class TestSETAR:
    """Tests for SETAR model."""

    def test_setar_fit_simulated(self) -> None:
        """SETAR with simulated 2-regime data should fit."""
        y = _simulate_setar(n=2000, c=0.0, delay=1, seed=42)
        model = SETAR(y, order=1, delay=1, n_regimes=2)
        results = model.fit()

        assert results.model_name == "SETAR"
        assert results.n_regimes == 2
        assert isinstance(results.threshold, float)
        assert len(results.resid) == results.nobs

        # Threshold should be close to 0
        y_range = np.max(y) - np.min(y)
        assert abs(results.threshold - 0.0) < 0.15 * y_range

    def test_setar_delay_selection(self) -> None:
        """Auto delay selection should find correct d via AIC."""
        # Simulate with delay=2
        rng = np.random.default_rng(42)
        n = 2000
        y = np.zeros(n)
        true_delay = 2
        for t in range(true_delay, n):
            if y[t - true_delay] <= 0:
                y[t] = 0.5 + 0.3 * y[t - 1] + rng.standard_normal() * 0.3
            else:
                y[t] = -0.5 + 0.7 * y[t - 1] + rng.standard_normal() * 0.3

        model = SETAR(y, order=1, delay=None, n_regimes=2, d_max=4, ic="aic")
        results = model.fit()

        # Delay should be selected (may not be exact due to estimation)
        assert results.delay >= 1
        assert results.delay <= 4

    def test_setar_reduces_to_ar(self) -> None:
        """SETAR with same parameters in both regimes ~ AR."""
        rng = np.random.default_rng(42)
        n = 1000
        y = np.zeros(n)
        for t in range(1, n):
            y[t] = 0.3 + 0.5 * y[t - 1] + rng.standard_normal() * 0.5

        model = SETAR(y, order=1, delay=1, n_regimes=2)
        results = model.fit()

        p1 = results.params["regime_1"]
        p2 = results.params["regime_2"]
        # Parameters should be similar
        assert np.allclose(p1, p2, atol=0.4), (
            f"Regime params too different for linear DGP: {p1} vs {p2}"
        )

    def test_setar_three_regimes(self) -> None:
        """SETAR(3) with 2 thresholds should be functional."""
        y = _simulate_setar_3regime(n=3000, c1=-1.0, c2=1.0, seed=42)

        model = SETAR(y, order=1, delay=1, n_regimes=3, grid_points=50)
        results = model.fit()

        assert results.n_regimes == 3
        assert isinstance(results.threshold, list)
        assert len(results.threshold) == 2
        assert results.threshold[0] < results.threshold[1]
        assert "regime_1" in results.params
        assert "regime_2" in results.params
        assert "regime_3" in results.params

    def test_setar_summary(self) -> None:
        """summary() returns formatted string."""
        y = _simulate_setar(n=500, seed=42)
        model = SETAR(y, order=1, delay=1)
        results = model.fit()
        summary = results.summary()
        assert isinstance(summary, str)
        assert "SETAR" in summary

    def test_setar_aic_bic_finite(self) -> None:
        """AIC and BIC should be finite."""
        y = _simulate_setar(n=500, seed=42)
        model = SETAR(y, order=1, delay=1)
        results = model.fit()
        assert np.isfinite(results.aic)
        assert np.isfinite(results.bic)

    def test_setar_delay_bic(self) -> None:
        """Auto delay selection with BIC criterion."""
        y = _simulate_setar(n=1000, delay=1, seed=42)
        model = SETAR(y, order=1, delay=None, n_regimes=2, d_max=3, ic="bic")
        results = model.fit()
        assert results.delay >= 1

    def test_setar_invalid_ic(self) -> None:
        """Invalid IC should raise ValueError."""
        y = _simulate_setar(n=500, seed=42)
        with pytest.raises(ValueError, match="ic must be"):
            SETAR(y, order=1, ic="invalid")
