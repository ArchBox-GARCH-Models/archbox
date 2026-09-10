"""Tests for LSTAR model.

Tests:
- test_lstar_fit_simulated: LSTAR with known DGP recovers gamma and c
- test_lstar_converges_to_tar: gamma -> inf (gamma=100) produces near-abrupt transition
- test_lstar_transition_midpoint: G(c; gamma, c) = 0.5 exactly
- test_lstar_forecast: Forecast via functional iteration (not NaN)
"""

from __future__ import annotations

import numpy as np

from archbox.threshold.lstar import LSTAR
from archbox.threshold.transition import logistic_transition


def _simulate_lstar(
    n: int = 1000,
    gamma: float = 5.0,
    c: float = 0.0,
    phi1: tuple[float, float] = (0.5, 0.3),
    phi2: tuple[float, float] = (-0.2, 0.8),
    sigma: float = 0.5,
    delay: int = 1,
    seed: int = 42,
) -> np.ndarray:
    """Simulate LSTAR(1) data with known parameters."""
    rng = np.random.default_rng(seed)
    y = np.zeros(n)
    for t in range(delay, n):
        s = y[t - delay]
        G = 1.0 / (1.0 + np.exp(-gamma * (s - c)))
        y[t] = (
            (phi1[0] + phi1[1] * y[t - 1]) * (1 - G)
            + (phi2[0] + phi2[1] * y[t - 1]) * G
            + rng.standard_normal() * sigma
        )
    return y


class TestLSTAR:
    """Tests for LSTAR model."""

    def test_lstar_fit_simulated(self) -> None:
        """LSTAR with known DGP should recover gamma and c approximately."""
        gamma_true, c_true = 5.0, 0.0
        y = _simulate_lstar(n=2000, gamma=gamma_true, c=c_true, seed=42)

        model = LSTAR(y, order=1, delay=1, gamma_grid=30, c_grid=30)
        results = model.fit()

        assert results.model_name == "LSTAR"
        assert results.n_regimes == 2

        # gamma should be positive and in a reasonable range
        est_gamma = results.transition_params["gamma"]
        assert est_gamma > 0.1, f"gamma too small: {est_gamma}"

        # c should be close to true value
        est_c = results.transition_params["c"]
        y_range = np.max(y) - np.min(y)
        assert abs(est_c - c_true) < 0.2 * y_range, f"c={est_c:.4f} too far from true {c_true}"

    def test_lstar_converges_to_tar(self) -> None:
        """For large gamma, LSTAR transition should be near-abrupt."""
        y = _simulate_lstar(n=2000, gamma=100.0, c=0.0, seed=42)

        model = LSTAR(y, order=1, delay=1, gamma_grid=30, c_grid=30)
        results = model.fit()

        G = results.transition_values
        # Most values should be near 0 or 1 (abrupt)
        near_extremes = np.sum((G < 0.1) | (G > 0.9))
        pct_extreme = near_extremes / len(G)
        assert pct_extreme > 0.5, f"Only {pct_extreme:.1%} near 0/1 - not converging to TAR"

    def test_lstar_transition_midpoint(self) -> None:
        """G(c; gamma, c) = 0.5 exactly for any gamma > 0."""
        for gamma in [0.5, 1.0, 5.0, 50.0]:
            for c in [-2.0, 0.0, 3.0]:
                G = logistic_transition(np.array([c]), gamma, c)
                assert abs(G[0] - 0.5) < 1e-10, f"G(c)={G[0]} != 0.5 for gamma={gamma}, c={c}"

    def test_lstar_forecast(self) -> None:
        """Forecast should produce finite values (not NaN)."""
        y = _simulate_lstar(n=1000, gamma=5.0, c=0.0, seed=42)
        model = LSTAR(y, order=1, delay=1, gamma_grid=20, c_grid=20)
        results = model.fit()

        fc = results.forecast(horizon=10)
        assert isinstance(fc, np.ndarray)
        assert fc.shape == (10,)
        assert np.all(np.isfinite(fc)), "Forecast contains NaN/Inf"

    def test_lstar_summary(self) -> None:
        """summary() should return formatted string with gamma and c."""
        y = _simulate_lstar(n=500, seed=42)
        model = LSTAR(y, order=1, delay=1, gamma_grid=15, c_grid=15)
        results = model.fit()
        summary = results.summary()
        assert isinstance(summary, str)
        assert "LSTAR" in summary
        assert "gamma" in summary

    def test_lstar_residuals(self) -> None:
        """Residuals should have correct shape and be approximately zero-mean."""
        y = _simulate_lstar(n=1000, seed=42)
        model = LSTAR(y, order=1, delay=1, gamma_grid=20, c_grid=20)
        results = model.fit()
        assert len(results.resid) == results.nobs
        assert abs(np.mean(results.resid)) < 0.1

    def test_lstar_no_refine(self) -> None:
        """LSTAR without NLS refinement should still work."""
        y = _simulate_lstar(n=500, seed=42)
        model = LSTAR(y, order=1, delay=1, gamma_grid=20, c_grid=20, refine=False)
        results = model.fit()
        assert results.model_name == "LSTAR"
        assert np.isfinite(results.loglike)

    def test_lstar_aic_bic(self) -> None:
        """AIC and BIC should be finite."""
        y = _simulate_lstar(n=500, seed=42)
        model = LSTAR(y, order=1, delay=1, gamma_grid=15, c_grid=15)
        results = model.fit()
        assert np.isfinite(results.aic)
        assert np.isfinite(results.bic)


class TestLSTARGammaScaling:
    """Gamma is searched in units of 1/std(s) (audit finding #4)."""

    def test_gamma_grid_is_scale_equivariant(self) -> None:
        """Rescaling the data rescales gamma exactly, leaving G unchanged."""
        y = _simulate_lstar(n=1500, gamma=5.0, c=0.0, seed=42)
        base = LSTAR(y, order=1, delay=1, gamma_grid=20, c_grid=20).fit()
        scaled = LSTAR(100.0 * y, order=1, delay=1, gamma_grid=20, c_grid=20).fit()

        ratio = base.transition_params["gamma"] / scaled.transition_params["gamma"]
        assert abs(ratio - 100.0) < 1e-6 * 100.0
        assert np.allclose(base.transition_values, scaled.transition_values, atol=1e-8)
        assert np.isclose(
            scaled.transition_params["c"], 100.0 * base.transition_params["c"], rtol=1e-4
        )

    def test_gamma_bound_scales_with_data(self) -> None:
        """The old hard cap of 500 is replaced by a scaled bound."""
        from archbox.datasets import load_dataset

        returns = load_dataset("sp500")["returns"].to_numpy()[:1500]
        model = LSTAR(returns, order=1, delay=1, gamma_grid=15, c_grid=15)
        # Return-scale data (std ~ 0.01) needs gamma far above the old cap.
        assert model.gamma_max > 500.0
        assert np.isclose(model.gamma_max, 500.0 / np.std(model._s))

        results = model.fit()
        assert results.transition_params["gamma"] > 500.0
        assert np.isfinite(results.loglike)
        assert np.all(np.isfinite(results.forecast(horizon=3)))

    def test_converged_flag_present(self) -> None:
        """The Nelder-Mead success flag is recorded on the results."""
        y = _simulate_lstar(n=800, seed=42)
        results = LSTAR(y, order=1, delay=1, gamma_grid=15, c_grid=15).fit()
        assert isinstance(results.converged, bool)
        assert results.converged
        assert "Converged" in results.summary()

    def test_no_refine_is_converged(self) -> None:
        y = _simulate_lstar(n=500, seed=42)
        results = LSTAR(y, order=1, delay=1, gamma_grid=15, c_grid=15, refine=False).fit()
        assert results.converged

    def test_refinement_never_worsens_the_fit(self) -> None:
        """The refined (gamma, c) is kept only if it lowers the RSS."""
        y = _simulate_lstar(n=800, gamma=5.0, seed=7)
        refined = LSTAR(y, order=1, delay=1, gamma_grid=15, c_grid=15).fit()
        grid_only = LSTAR(y, order=1, delay=1, gamma_grid=15, c_grid=15, refine=False).fit()
        assert np.sum(refined.resid**2) <= np.sum(grid_only.resid**2) + 1e-8
