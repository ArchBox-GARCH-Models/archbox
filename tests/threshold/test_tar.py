"""Tests for TAR model.

Tests:
- test_tar_two_regimes: TAR(2) recovers threshold (tol=10%)
- test_tar_reduces_to_ar: TAR with extreme threshold == AR linear
- test_tar_grid_search: Grid search finds c that minimizes RSS
- test_tar_different_variances: sigma_1 != sigma_2 estimated correctly
"""

from __future__ import annotations

import numpy as np
import pytest

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
        assert (
            abs(results.threshold - c_true) < 0.10 * y_range
        ), f"Threshold {results.threshold:.4f} too far from true {c_true}"

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
        assert np.allclose(
            p1, p2, atol=0.3
        ), f"Regime params too different for linear DGP: {p1} vs {p2}"

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
        assert (
            est_ratio > 2.0
        ), f"Variance ratio {est_ratio:.2f} too small, expected ~{true_ratio:.2f}"

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


class TestTARThreeRegimes:
    """TAR must actually fit three regimes when asked (audit finding #1)."""

    @staticmethod
    def _simulate_3regime(n: int = 3000, seed: int = 5) -> np.ndarray:
        rng = np.random.default_rng(seed)
        y = np.zeros(n)
        for t in range(1, n):
            if y[t - 1] < -0.5:
                y[t] = -0.3 + 0.6 * y[t - 1] + rng.standard_normal() * 0.3
            elif y[t - 1] > 0.5:
                y[t] = 0.3 - 0.6 * y[t - 1] + rng.standard_normal() * 0.3
            else:
                y[t] = 0.9 * y[t - 1] + rng.standard_normal() * 0.3
        return y

    def test_three_regimes_fitted(self) -> None:
        y = self._simulate_3regime()
        results = TAR(y, order=1, delay=1, n_regimes=3, grid_points=60).fit()

        assert results.n_regimes == 3
        assert isinstance(results.threshold, list)
        assert results.threshold[0] < results.threshold[1]
        assert set(results.params) == {"regime_1", "regime_2", "regime_3"}
        assert results.params_regime3 is not None
        # DGP slopes are 0.6 (lower), 0.9 (middle) and -0.6 (upper); the upper
        # regime is visited rarely, so it is checked by sign and magnitude.
        assert abs(results.params_regime1[1] - 0.6) < 0.25
        assert abs(results.params_regime2[1] - 0.9) < 0.25
        assert -0.95 < results.params_regime3[1] < -0.3

    def test_three_regime_residuals_and_forecast(self) -> None:
        y = self._simulate_3regime(n=2000, seed=6)
        results = TAR(y, order=1, delay=1, n_regimes=3, grid_points=50).fit()
        assert len(results.resid) == results.nobs
        assert np.all(np.isfinite(results.resid))
        fc = results.forecast(horizon=5)
        assert fc.shape == (5,)
        assert np.all(np.isfinite(fc))

    def test_invalid_n_regimes(self) -> None:
        y = _simulate_tar(n=500, seed=42)
        with pytest.raises(ValueError, match="n_regimes must be 2 or 3"):
            TAR(y, order=1, delay=1, n_regimes=4)


class TestTARExogenousThreshold:
    """The exogenous threshold variable drives both the fit and the forecast."""

    @staticmethod
    def _simulate(n: int = 2000, seed: int = 42) -> tuple[np.ndarray, np.ndarray]:
        rng = np.random.default_rng(seed)
        s_ext = rng.standard_normal(n)
        y = np.zeros(n)
        for t in range(1, n):
            if s_ext[t - 1] <= 0.0:
                y[t] = 0.5 + 0.3 * y[t - 1] + rng.standard_normal() * 0.5
            else:
                y[t] = -0.3 + 0.7 * y[t - 1] + rng.standard_normal() * 0.5
        return y, s_ext

    def test_threshold_recovered(self) -> None:
        y, s_ext = self._simulate()
        results = TAR(y, order=1, delay=1, threshold_var=s_ext).fit()
        # True split of the exogenous variable is at zero.
        assert abs(results.threshold) < 0.25
        assert results.params_regime1[0] > results.params_regime2[0]

    def test_forecast_uses_exogenous_variable(self) -> None:
        y, s_ext = self._simulate(n=1000, seed=3)
        model = TAR(y, order=1, delay=1, threshold_var=s_ext)
        results = model.fit()

        # One step ahead the relevant threshold value is z_{T-1}, which is
        # known: the forecast must come from the regime it selects.
        s_last = s_ext[-1]
        regime = results.params_regime2 if s_last > results.threshold else results.params_regime1
        x = np.array([1.0, y[-1]])
        fc = model.forecast(results, horizon=1)
        assert np.isclose(fc[0], float(x @ regime))

    def test_effective_length_threshold_var_accepted(self) -> None:
        y, s_ext = self._simulate(n=600, seed=9)
        full = TAR(y, order=1, delay=1, threshold_var=s_ext).fit()
        # Same variable supplied already aligned with the effective sample.
        eff = TAR(y, order=1, delay=1, threshold_var=s_ext[:-1]).fit()
        assert np.isclose(full.threshold, eff.threshold)
        assert np.allclose(full.params_regime1, eff.params_regime1)

    def test_long_horizon_warns_about_held_threshold(self) -> None:
        """Beyond the delay the exogenous variable is unknown: warn and hold."""
        y, s_ext = self._simulate(n=600, seed=5)
        model = TAR(y, order=1, delay=1, threshold_var=s_ext)
        results = model.fit()
        with pytest.warns(UserWarning, match="exceeds the delay"):
            fc = model.forecast(results, horizon=4)
        assert fc.shape == (4,)
        assert np.all(np.isfinite(fc))

    def test_nan_threshold_var_rejected(self) -> None:
        y, s_ext = self._simulate(n=400, seed=1)
        s_bad = s_ext.copy()
        s_bad[10] = np.nan
        with pytest.raises(ValueError, match="non-finite"):
            TAR(y, order=1, delay=1, threshold_var=s_bad)


class TestTARLinearityField:
    """results.linearity_test is populated by the fit (audit finding #6)."""

    def test_linearity_test_populated(self) -> None:
        y = _simulate_tar(n=1500, c=0.0, seed=42)
        results = TAR(y, order=1, delay=1).fit()
        assert results.linearity_test is not None
        assert results.linearity_test.test_name == "Luukkonen-Saikkonen-Terasvirta"
        assert np.isfinite(results.linearity_test.statistic)
        assert results.linearity_test.pvalue < 0.05
        assert "Linearity Test" in results.summary()


class TestHardThresholdLoglike:
    """The packaged log-likelihood matches the base-class formula."""

    def test_two_regime_loglike_matches_base(self) -> None:
        y = _simulate_tar(n=1500, c=0.0, seed=1)
        model = TAR(y, order=1, delay=1)
        results = model.fit()
        ll = model.loglike(
            results.params_regimes,
            [results.sigma2["regime_1"], results.sigma2["regime_2"]],
            results.transition_values,
        )
        assert np.isclose(ll, results.loglike)

    def test_three_regime_loglike_and_resid_match_base(self) -> None:
        y = TestTARThreeRegimes._simulate_3regime(n=2000, seed=8)
        model = TAR(y, order=1, delay=1, n_regimes=3, grid_points=50)
        results = model.fit()
        sigma2 = [results.sigma2[f"regime_{i}"] for i in (1, 2, 3)]
        ll = model.loglike(results.params_regimes, sigma2, results.transition_values)
        assert np.isclose(ll, results.loglike)

        fitted = model.fitted_values(model._X, results.transition_values, results.params_regimes)
        assert np.allclose(model._y - fitted, results.resid)
