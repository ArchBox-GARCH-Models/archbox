"""Tests for TAR model.

Tests:
- test_tar_two_regimes: TAR(2) recovers threshold (tol=10%)
- test_tar_reduces_to_ar: TAR with extreme threshold == AR linear
- test_tar_grid_search: Grid search finds c that minimizes RSS
- test_tar_different_variances: sigma_1 != sigma_2 estimated correctly
"""

from __future__ import annotations

import numpy as np

from archbox.threshold.tar import TAR


def _simulate_tar(
    n: int = 1000,
    c: float = 0.0,
    phi1: tuple[float, float] = (0.5, 0.3),
    phi2: tuple[float, float] = (-0.2, 0.8),
    sigma1: float = 0.5,
    sigma2: float = 0.5,
    seed: int = 42,
) -> np.ndarray:
    """Simulate TAR(1) data with known parameters."""
    rng = np.random.default_rng(seed)
    y = np.zeros(n)
    for t in range(1, n):
        if y[t - 1] <= c:
            y[t] = phi1[0] + phi1[1] * y[t - 1] + rng.standard_normal() * sigma1
        else:
            y[t] = phi2[0] + phi2[1] * y[t - 1] + rng.standard_normal() * sigma2
    return y


class TestTAR:
    """Tests for TAR model."""

    def test_tar_two_regimes(self) -> None:
        """TAR(2) with simulated data recovers threshold (tol=10% of range)."""
        c_true = 0.0
        y = _simulate_tar(n=2000, c=c_true, seed=42)

        model = TAR(y, order=1, delay=1)
        results = model.fit()

        # Threshold should be close to true value
        y_range = np.max(y) - np.min(y)
        assert abs(results.threshold - c_true) < 0.10 * y_range, (
            f"Threshold {results.threshold:.4f} too far from true {c_true}"
        )

        # Should have two regimes
        assert results.n_regimes == 2
        assert "regime_1" in results.params
        assert "regime_2" in results.params

    def test_tar_reduces_to_ar(self) -> None:
        """TAR with same parameters in both regimes should behave like AR."""
        rng = np.random.default_rng(42)
        n = 1000
        y = np.zeros(n)
        phi0, phi1_val = 0.5, 0.4
        for t in range(1, n):
            y[t] = phi0 + phi1_val * y[t - 1] + rng.standard_normal() * 0.5

        model = TAR(y, order=1, delay=1)
        results = model.fit()

        # Both regimes should have similar parameters
        p1 = results.params["regime_1"]
        p2 = results.params["regime_2"]
        assert np.allclose(p1, p2, atol=0.3), (
            f"Regime params too different for linear DGP: {p1} vs {p2}"
        )

    def test_tar_grid_search(self) -> None:
        """Grid search should find c that minimizes RSS."""
        c_true = 1.0
        y = _simulate_tar(n=2000, c=c_true, seed=123)

        model = TAR(y, order=1, delay=1, grid_points=500)
        results = model.fit()

        # Compute RSS at estimated threshold
        mask1 = model._s <= results.threshold
        mask2 = model._s > results.threshold
        rss_est = model._ols_rss(model._y[mask1], model._X[mask1])
        rss_est += model._ols_rss(model._y[mask2], model._X[mask2])

        # RSS at a random different threshold should be larger
        other_c = results.threshold + 2.0
        mask1_other = model._s <= other_c
        mask2_other = model._s > other_c
        if mask1_other.sum() > 3 and mask2_other.sum() > 3:
            rss_other = model._ols_rss(model._y[mask1_other], model._X[mask1_other])
            rss_other += model._ols_rss(model._y[mask2_other], model._X[mask2_other])
            assert rss_est <= rss_other + 1e-6, "Grid search did not minimize RSS"

    def test_tar_different_variances(self) -> None:
        """TAR with sigma_1 != sigma_2 should estimate different variances."""
        sigma1_true, sigma2_true = 0.3, 1.5
        y = _simulate_tar(n=3000, c=0.0, sigma1=sigma1_true, sigma2=sigma2_true, seed=42)

        model = TAR(y, order=1, delay=1)
        results = model.fit()

        s1_est = results.sigma2["regime_1"]
        s2_est = results.sigma2["regime_2"]

        # The variance ratio should be roughly preserved
        true_ratio = sigma2_true**2 / sigma1_true**2
        est_ratio = max(s1_est, s2_est) / min(s1_est, s2_est)
        assert est_ratio > 2.0, (
            f"Variance ratio {est_ratio:.2f} too small, expected ~{true_ratio:.2f}"
        )

    def test_tar_summary(self) -> None:
        """summary() should return a formatted string."""
        y = _simulate_tar(n=500, seed=42)
        model = TAR(y, order=1, delay=1)
        results = model.fit()
        summary = results.summary()
        assert isinstance(summary, str)
        assert "TAR" in summary
        assert "Threshold" in summary
        assert "regime_1" in summary

    def test_tar_external_threshold_var(self) -> None:
        """TAR with external threshold variable."""
        rng = np.random.default_rng(42)
        n = 1000
        s_ext = rng.standard_normal(n)
        y = np.zeros(n)
        c = 0.0
        for t in range(1, n):
            if s_ext[t - 1] <= c:
                y[t] = 0.5 + 0.3 * y[t - 1] + rng.standard_normal() * 0.5
            else:
                y[t] = -0.3 + 0.7 * y[t - 1] + rng.standard_normal() * 0.5

        model = TAR(y, order=1, delay=1, threshold_var=s_ext)
        results = model.fit()
        assert results.threshold is not None

    def test_tar_residuals_shape(self) -> None:
        """Residuals should have correct shape."""
        y = _simulate_tar(n=500, seed=42)
        model = TAR(y, order=1, delay=1)
        results = model.fit()
        assert len(results.resid) == results.nobs

    def test_tar_aic_bic(self) -> None:
        """AIC and BIC should be finite."""
        y = _simulate_tar(n=500, seed=42)
        model = TAR(y, order=1, delay=1)
        results = model.fit()
        assert np.isfinite(results.aic)
        assert np.isfinite(results.bic)
        assert results.bic > results.aic  # BIC penalizes more for n > ~7
