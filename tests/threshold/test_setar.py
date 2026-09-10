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


def _simulate_setar_3regime_strong(n: int = 2000, seed: int = 2) -> np.ndarray:
    """Three regimes with clearly distinct slopes (c1=-0.5, c2=0.5)."""
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
        assert np.allclose(
            p1, p2, atol=0.4
        ), f"Regime params too different for linear DGP: {p1} vs {p2}"

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


class TestSETARThreeRegimes:
    """Regression tests for the three-regime SETAR (audit finding #1)."""

    def test_regime3_params_exposed(self) -> None:
        """The upper regime's coefficients must reach the results object."""
        y = _simulate_setar_3regime_strong(n=3000, seed=2)
        results = SETAR(y, order=1, delay=1, n_regimes=3, grid_points=60).fit()

        assert results.params_regime3 is not None
        assert len(results.params_regimes) == 3
        assert np.allclose(results.params_regime1, results.params["regime_1"])
        assert np.allclose(results.params_regime2, results.params["regime_2"])
        assert np.allclose(results.params_regime3, results.params["regime_3"])
        # Slopes of the DGP: 0.6 (lower), 0.9 (middle), -0.6 (upper).
        # DGP slopes are 0.6 (lower), 0.9 (middle) and -0.6 (upper); the upper
        # regime is visited rarely, so it is checked by sign and magnitude.
        assert abs(results.params_regime1[1] - 0.6) < 0.25
        assert abs(results.params_regime2[1] - 0.9) < 0.25
        assert -0.95 < results.params_regime3[1] < -0.3

    def test_forecast_uses_upper_regime(self) -> None:
        """A one-step forecast above c_2 must use regime 3's coefficients."""
        y = _simulate_setar_3regime_strong(n=3000, seed=2)
        model = SETAR(y, order=1, delay=1, n_regimes=3, grid_points=60)
        results = model.fit()
        c1, c2 = results.threshold

        # Append an observation clearly above the upper threshold so that the
        # one-step forecast must come from regime 3.
        y_high = np.append(y, c2 + 2.0)
        model_high = SETAR(y_high, order=1, delay=1, n_regimes=3, grid_points=60)
        model_high.delay = 1
        fc = model_high.forecast(results, horizon=1)

        x = np.array([1.0, y_high[-1]])
        assert np.isclose(fc[0], float(x @ results.params_regime3))
        # And it differs from what the middle regime would have produced.
        assert not np.isclose(fc[0], float(x @ results.params_regime2))
        assert c1 < c2

    def test_forecast_returns_point_array(self) -> None:
        """forecast() returns an ndarray of point forecasts, not a dict."""
        y = _simulate_setar_3regime_strong(n=2000, seed=7)
        results = SETAR(y, order=1, delay=1, n_regimes=3, grid_points=50).fit()
        fc = results.forecast(horizon=6)
        assert isinstance(fc, np.ndarray)
        assert fc.shape == (6,)
        assert np.all(np.isfinite(fc))

    def test_forecast_intervals_separate_method(self) -> None:
        """Intervals and paths live in forecast_intervals()."""
        y = _simulate_setar_3regime_strong(n=2000, seed=7)
        results = SETAR(y, order=1, delay=1, n_regimes=3, grid_points=50).fit()
        out = results.forecast_intervals(horizon=4, n_sims=200, alpha=0.10, seed=0)
        assert out["paths"].shape == (200, 4)
        for key in ("mean", "median", "lower", "upper"):
            assert out[key].shape == (4,)
        assert np.all(out["lower"] <= out["upper"])


class TestSETARDelaySelection:
    """Delay selection must compare a common effective sample (audit #5)."""

    @pytest.mark.parametrize("seed", [42, 7, 11])
    def test_true_delay_recovered(self, seed: int) -> None:
        """AIC on a common sample recovers the generating delay d=2."""
        rng = np.random.default_rng(seed)
        n = 2000
        y = np.zeros(n)
        for t in range(2, n):
            if y[t - 2] <= 0:
                y[t] = 0.5 + 0.3 * y[t - 1] + rng.standard_normal() * 0.3
            else:
                y[t] = -0.5 + 0.7 * y[t - 1] + rng.standard_normal() * 0.3

        results = SETAR(y, order=1, delay=None, n_regimes=2, d_max=4, ic="aic").fit()
        assert results.delay == 2

    def test_candidate_samples_have_equal_length(self) -> None:
        """Every candidate delay is scored on the same number of observations."""
        y = _simulate_setar(n=800, seed=3)
        model = SETAR(y, order=1, delay=None, d_max=5)
        lengths = {len(model._rebuild_for_delay(d, start=5)[0]) for d in range(1, 6)}
        assert lengths == {len(y) - 5}


class TestSETARParameterCount:
    """AIC/BIC parameter counts must agree between TAR and SETAR (audit #5)."""

    def test_setar_matches_tar_for_fixed_delay(self) -> None:
        from archbox.threshold.tar import TAR

        y = _simulate_setar(n=1000, seed=0)
        tar_res = TAR(y, order=1, delay=1).fit()
        setar_res = SETAR(y, order=1, delay=1).fit()
        assert setar_res.nobs == tar_res.nobs
        assert np.isclose(setar_res.loglike, tar_res.loglike)
        assert np.isclose(setar_res.aic, tar_res.aic)
        assert np.isclose(setar_res.bic, tar_res.bic)

    def test_auto_delay_counts_the_delay(self) -> None:
        """Selecting d from the data costs exactly one extra parameter."""
        y = _simulate_setar(n=1000, seed=0)
        fixed = SETAR(y, order=1, delay=1).fit()
        auto = SETAR(y, order=1, delay=None, d_max=1).fit()
        assert auto.delay == fixed.delay
        assert auto.nobs == fixed.nobs
        assert np.isclose(auto.aic - fixed.aic, 2.0)
