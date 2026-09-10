"""Tests for HAR-RV model."""

from __future__ import annotations

import numpy as np
import pytest

from archbox.models.har_rv import HARRV


class TestHARRV:
    """Test HAR-RV model."""

    @pytest.fixture()
    def simulated_rv(self, rng: np.random.Generator) -> np.ndarray:
        """Generate simulated realized variance series."""
        n = 500
        rv = np.empty(n)
        rv[0] = 0.0001
        for t in range(1, n):
            rv[t] = 0.00001 + 0.3 * rv[t - 1] + 0.0001 * rng.standard_normal() ** 2
            rv[t] = max(rv[t], 1e-8)
        return rv

    def test_har_rv_instantiation(self, simulated_rv: np.ndarray) -> None:
        model = HARRV(simulated_rv)
        assert model.components == ["daily", "weekly", "monthly"]

    def test_har_rv_fit_ols(self, simulated_rv: np.ndarray) -> None:
        model = HARRV(simulated_rv)
        results = model.fit(method="ols")
        assert results is not None
        assert len(results.params) == 4  # const + daily + weekly + monthly
        assert np.all(np.isfinite(results.params))

    def test_har_rv_r_squared(self, simulated_rv: np.ndarray) -> None:
        model = HARRV(simulated_rv)
        results = model.fit(method="ols")
        assert 0 <= results.r_squared <= 1, f"R^2 must be in [0,1], got {results.r_squared}"

    def test_har_rv_matches_ols(self, simulated_rv: np.ndarray) -> None:
        """HAR-RV by OLS should match manual OLS computation."""
        model = HARRV(simulated_rv)
        results = model.fit(method="ols")

        # Manual OLS using numpy
        X, y = model._build_regressors()
        beta_manual = np.linalg.lstsq(X, y, rcond=None)[0]
        np.testing.assert_allclose(
            results.params,
            beta_manual,
            rtol=1e-10,
            err_msg="HAR-RV OLS should match manual OLS",
        )

    def test_har_rv_summary(self, simulated_rv: np.ndarray) -> None:
        model = HARRV(simulated_rv)
        results = model.fit(method="ols")
        summary = results.summary()
        assert summary is not None
        assert "HAR-RV" in summary
        assert "R-squared" in summary

    def test_har_rv_forecast(self, simulated_rv: np.ndarray) -> None:
        model = HARRV(simulated_rv)
        results = model.fit(method="ols")
        forecast = results.forecast(horizon=5)
        assert len(forecast) == 5
        assert np.all(np.isfinite(forecast))
        assert np.all(forecast >= 0)

    def test_har_rv_forecast_is_not_constant(self, simulated_rv: np.ndarray) -> None:
        """The forecast iterates the HAR regression instead of repeating a value."""
        model = HARRV(simulated_rv)
        results = model.fit(method="ols")
        forecast = results.forecast(horizon=10)
        assert len(np.unique(forecast)) > 1, "forecast must not be a constant series"

    def test_har_rv_forecast_first_step_matches_regression(self, simulated_rv: np.ndarray) -> None:
        """Step 1 equals beta_0 + sum_c beta_c * mean(last lag_c observations)."""
        model = HARRV(simulated_rv)
        results = model.fit(method="ols")
        regressors = [1.0]
        for comp in model.components:
            lag = model._component_lags[comp]
            regressors.append(float(np.mean(simulated_rv[-lag:])))
        expected = float(np.dot(results.params, regressors))
        assert results.forecast(horizon=1)[0] == pytest.approx(expected, rel=1e-12)

    def test_har_rv_forecast_rejects_bad_horizon(self, simulated_rv: np.ndarray) -> None:
        model = HARRV(simulated_rv)
        results = model.fit(method="ols")
        with pytest.raises(ValueError, match="horizon"):
            results.forecast(horizon=0)

    def test_har_rv_rejects_nan(self) -> None:
        rv = np.full(100, 1e-4)
        rv[5] = np.nan
        with pytest.raises(ValueError, match="NaN"):
            HARRV(rv)

    def test_har_rv_rejects_negative(self) -> None:
        rv = np.full(100, 1e-4)
        rv[5] = -1e-4
        with pytest.raises(ValueError, match="non-negative"):
            HARRV(rv)

    def test_har_rv_rejects_unknown_component(self, simulated_rv: np.ndarray) -> None:
        with pytest.raises(ValueError, match="Unknown HAR components"):
            HARRV(simulated_rv, components=["daily", "yearly"])

    def test_har_rv_custom_components(self, simulated_rv: np.ndarray) -> None:
        """Test with daily+weekly only."""
        model = HARRV(simulated_rv, components=["daily", "weekly"])
        results = model.fit(method="ols")
        assert len(results.params) == 3  # const + daily + weekly

    def test_har_rv_param_names(self, simulated_rv: np.ndarray) -> None:
        model = HARRV(simulated_rv)
        results = model.fit(method="ols")
        assert results.param_names == ["beta_0", "beta_d", "beta_w", "beta_m"]

    def test_har_rv_residuals_shape(self, simulated_rv: np.ndarray) -> None:
        model = HARRV(simulated_rv)
        results = model.fit(method="ols")
        assert len(results.residuals) == results.nobs
        assert len(results.fitted_values) == results.nobs

    def test_har_rv_invalid_method(self, simulated_rv: np.ndarray) -> None:
        model = HARRV(simulated_rv)
        with pytest.raises(ValueError, match="Unknown method"):
            model.fit(method="invalid")
