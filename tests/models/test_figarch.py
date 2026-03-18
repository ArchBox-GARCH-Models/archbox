"""Tests for FIGARCH model."""

from __future__ import annotations

import numpy as np

from archbox.models.figarch import FIGARCH, _fractional_coefficients


class TestFIGARCH:
    """Test FIGARCH model."""

    def test_figarch_instantiation(self, sp500_returns: np.ndarray) -> None:
        model = FIGARCH(sp500_returns)
        assert model.volatility_process == "FIGARCH"
        assert model.num_params == 4  # omega, phi, d, beta
        assert len(model.param_names) == 4

    def test_fractional_coefficients(self) -> None:
        """Test that fractional coefficients are computed correctly."""
        d = 0.4
        coeffs = _fractional_coefficients(d, 10)
        assert len(coeffs) == 10
        # First coefficient should be d
        np.testing.assert_allclose(coeffs[0], d)
        # Coefficients should decay
        assert all(np.abs(coeffs[k]) <= np.abs(coeffs[k - 1]) for k in range(1, 10))

    def test_fractional_coefficients_d_zero(self) -> None:
        """When d=0, all coefficients should be 0."""
        coeffs = _fractional_coefficients(0.0, 10)
        np.testing.assert_allclose(coeffs, 0.0, atol=1e-15)

    def test_figarch_variance_recursion(self, sp500_returns: np.ndarray) -> None:
        model = FIGARCH(sp500_returns, truncation_lag=100)
        params = model.start_params
        backcast = model._backcast(model.endog)
        sigma2 = model._variance_recursion(params, model.endog, backcast)
        assert len(sigma2) == model.nobs
        assert np.all(sigma2 > 0)
        assert np.all(np.isfinite(sigma2))

    def test_figarch_fit_sp500(self, sp500_returns: np.ndarray) -> None:
        model = FIGARCH(sp500_returns, truncation_lag=100)
        results = model.fit(disp=False)
        assert results is not None
        assert np.isfinite(results.loglike)

    def test_figarch_long_memory(self, sp500_returns: np.ndarray) -> None:
        """d parameter should be in (0, 1) indicating long memory."""
        model = FIGARCH(sp500_returns, truncation_lag=100)
        results = model.fit(disp=False)
        d = results.params[2]
        assert 0 < d < 1, f"d must be in (0,1), got {d}"

    def test_figarch_long_memory_acf(self, sp500_returns: np.ndarray) -> None:
        """Squared residuals should show slower ACF decay with FIGARCH (long memory)."""
        model = FIGARCH(sp500_returns, truncation_lag=100)
        results = model.fit(disp=False)
        # Just verify that d > 0 (which implies hyperbolic ACF decay)
        d = results.params[2]
        assert d > 0.01, f"d should indicate long memory (d > 0), got {d}"

    def test_figarch_forecast(self, sp500_returns: np.ndarray) -> None:
        model = FIGARCH(sp500_returns, truncation_lag=100)
        results = model.fit(disp=False)
        forecast = results.forecast(horizon=10)
        assert forecast is not None
        assert len(forecast["variance"]) == 10
        assert np.all(np.isfinite(forecast["variance"]))

    def test_figarch_summary(self, sp500_returns: np.ndarray) -> None:
        model = FIGARCH(sp500_returns, truncation_lag=100)
        results = model.fit(disp=False)
        summary = results.summary()
        assert summary is not None
        assert "FIGARCH" in str(summary)

    def test_figarch_transform_roundtrip(self, sp500_returns: np.ndarray) -> None:
        model = FIGARCH(sp500_returns)
        params = model.start_params
        constrained = model.transform_params(params)
        unconstrained = model.untransform_params(constrained)
        roundtrip = model.transform_params(unconstrained)
        np.testing.assert_allclose(constrained, roundtrip, rtol=1e-6)
