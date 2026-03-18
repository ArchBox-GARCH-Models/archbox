"""Tests for ESTAR model.

Tests:
- test_estar_symmetric_transition: G(c-delta) == G(c+delta) for all delta
- test_estar_fit_simulated: ESTAR with known DGP recovers parameters
- test_estar_gamma_zero_linear: gamma ~ 0 => model near linear
"""

from __future__ import annotations

import numpy as np

from archbox.threshold.estar import ESTAR
from archbox.threshold.transition import exponential_transition


def _simulate_estar(
    n: int = 1000,
    gamma: float = 3.0,
    c: float = 0.0,
    phi1: tuple[float, float] = (0.5, 0.3),
    phi2: tuple[float, float] = (-0.2, 0.8),
    sigma: float = 0.5,
    delay: int = 1,
    seed: int = 42,
) -> np.ndarray:
    """Simulate ESTAR(1) data with known parameters."""
    rng = np.random.default_rng(seed)
    y = np.zeros(n)
    for t in range(delay, n):
        s = y[t - delay]
        g_val = 1.0 - np.exp(-gamma * (s - c) ** 2)
        y[t] = (
            (phi1[0] + phi1[1] * y[t - 1]) * (1 - g_val)
            + (phi2[0] + phi2[1] * y[t - 1]) * g_val
            + rng.standard_normal() * sigma
        )
    return y


class TestESTAR:
    """Tests for ESTAR model."""

    def test_estar_symmetric_transition(self) -> None:
        """G(c - delta) == G(c + delta) for all delta (exponential is symmetric)."""
        c = 2.0
        for gamma in [0.5, 1.0, 5.0, 20.0]:
            for delta in [0.1, 0.5, 1.0, 3.0, 5.0]:
                g_minus = exponential_transition(np.array([c - delta]), gamma, c)
                g_plus = exponential_transition(np.array([c + delta]), gamma, c)
                assert abs(g_minus[0] - g_plus[0]) < 1e-10, (
                    f"Not symmetric for gamma={gamma}, delta={delta}: "
                    f"G(c-d)={g_minus[0]:.10f} != G(c+d)={g_plus[0]:.10f}"
                )

    def test_estar_fit_simulated(self) -> None:
        """ESTAR with known DGP should recover parameters approximately."""
        gamma_true, c_true = 3.0, 0.0
        y = _simulate_estar(n=2000, gamma=gamma_true, c=c_true, seed=42)

        model = ESTAR(y, order=1, delay=1, gamma_grid=30, c_grid=30)
        results = model.fit()

        assert results.model_name == "ESTAR"
        assert results.n_regimes == 2

        # gamma should be positive
        est_gamma = results.transition_params["gamma"]
        assert est_gamma > 0.1, f"gamma too small: {est_gamma}"

        # c should be near true value
        est_c = results.transition_params["c"]
        y_range = np.max(y) - np.min(y)
        assert abs(est_c - c_true) < 0.25 * y_range, f"c={est_c:.4f} too far from true {c_true}"

    def test_estar_gamma_zero_linear(self) -> None:
        """With gamma ~ 0, ESTAR should be near linear (G ~ 0 everywhere)."""
        s = np.linspace(-5, 5, 1000)
        g = exponential_transition(s, gamma=0.001, c=0.0)
        # G should be near 0 everywhere for small gamma
        assert np.allclose(g, 0.0, atol=0.05), f"G not near 0 for gamma~0: max(G)={np.max(g):.4f}"

    def test_estar_at_center(self) -> None:
        """G(c; gamma, c) = 0 for exponential transition."""
        for gamma in [0.5, 1.0, 10.0, 100.0]:
            g = exponential_transition(np.array([0.0]), gamma, c=0.0)
            assert abs(g[0]) < 1e-10, f"G(c) != 0 for gamma={gamma}: G(c)={g[0]}"

    def test_estar_summary(self) -> None:
        """summary() should return formatted string."""
        y = _simulate_estar(n=500, seed=42)
        model = ESTAR(y, order=1, delay=1, gamma_grid=15, c_grid=15)
        results = model.fit()
        summary = results.summary()
        assert isinstance(summary, str)
        assert "ESTAR" in summary
        assert "gamma" in summary

    def test_estar_residuals(self) -> None:
        """Residuals should have correct shape."""
        y = _simulate_estar(n=1000, seed=42)
        model = ESTAR(y, order=1, delay=1, gamma_grid=20, c_grid=20)
        results = model.fit()
        assert len(results.resid) == results.nobs

    def test_estar_transition_values_bounded(self) -> None:
        """All transition values should be in [0, 1]."""
        y = _simulate_estar(n=1000, seed=42)
        model = ESTAR(y, order=1, delay=1, gamma_grid=20, c_grid=20)
        results = model.fit()
        assert np.all(results.transition_values >= -1e-10)
        assert np.all(results.transition_values <= 1.0 + 1e-10)

    def test_estar_aic_bic(self) -> None:
        """AIC and BIC should be finite."""
        y = _simulate_estar(n=500, seed=42)
        model = ESTAR(y, order=1, delay=1, gamma_grid=15, c_grid=15)
        results = model.fit()
        assert np.isfinite(results.aic)
        assert np.isfinite(results.bic)

    def test_estar_no_refine(self) -> None:
        """ESTAR without NLS refinement should still work."""
        y = _simulate_estar(n=500, seed=42)
        model = ESTAR(y, order=1, delay=1, gamma_grid=20, c_grid=20, refine=False)
        results = model.fit()
        assert results.model_name == "ESTAR"
        assert np.isfinite(results.loglike)

    def test_estar_forecast(self) -> None:
        """Forecast should produce finite values."""
        y = _simulate_estar(n=1000, seed=42)
        model = ESTAR(y, order=1, delay=1, gamma_grid=20, c_grid=20)
        results = model.fit()
        fc = results.forecast(horizon=5)
        assert "mean" in fc
        assert len(fc["mean"]) == 5
        assert np.all(np.isfinite(fc["mean"]))
