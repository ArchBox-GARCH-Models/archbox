"""Tests for GJR-GARCH model."""

from __future__ import annotations

import numpy as np

from archbox.models.gjr_garch import GJRGARCH


class TestGJRGARCH:
    """Test GJR-GARCH model."""

    def test_gjr_instantiation(self, sp500_returns: np.ndarray):
        model = GJRGARCH(sp500_returns, p=1, q=1)
        assert model.volatility_process == "GJR-GARCH"
        assert model.num_params == 4  # omega, alpha, gamma, beta
        assert len(model.param_names) == 4

    def test_gjr_variance_recursion(self, sp500_returns: np.ndarray):
        model = GJRGARCH(sp500_returns, p=1, q=1)
        params = model.start_params
        backcast = model._backcast(model.endog)
        sigma2 = model._variance_recursion(params, model.endog, backcast)
        assert len(sigma2) == model.nobs
        assert np.all(sigma2 > 0), "GJR-GARCH variance must be positive"
        assert np.all(np.isfinite(sigma2)), "Variance must be finite"

    def test_gjr_fit_sp500(self, sp500_returns: np.ndarray):
        model = GJRGARCH(sp500_returns, p=1, q=1)
        results = model.fit(disp=False)
        assert results is not None
        assert np.isfinite(results.loglike)
        # Persistence check: alpha + beta + gamma/2 < 1
        alpha = results.params[1]
        gamma = results.params[2]
        beta = results.params[3]
        persistence = alpha + beta + gamma / 2.0
        assert persistence < 1.0, f"GJR persistence={persistence} must be < 1"

    def test_gjr_leverage(self, sp500_returns: np.ndarray):
        """Gamma should be positive for SP500 (negative shocks increase vol more)."""
        model = GJRGARCH(sp500_returns, p=1, q=1)
        results = model.fit(disp=False)
        gamma_idx = 2
        assert results.params[gamma_idx] > 0, (
            f"GJR gamma should be > 0 for SP500, got {results.params[gamma_idx]}"
        )

    def test_gjr_forecast(self, sp500_returns: np.ndarray):
        model = GJRGARCH(sp500_returns, p=1, q=1)
        results = model.fit(disp=False)
        forecast = results.forecast(horizon=10)
        assert forecast is not None
        assert len(forecast["variance"]) == 10
        assert np.all(np.isfinite(forecast["variance"]))

    def test_gjr_summary(self, sp500_returns: np.ndarray):
        model = GJRGARCH(sp500_returns, p=1, q=1)
        results = model.fit(disp=False)
        summary = results.summary()
        assert summary is not None
        assert "GJR-GARCH" in str(summary)

    def test_gjr_asymmetric_impact(self, sp500_returns: np.ndarray):
        """Negative shocks should produce higher variance than positive shocks."""
        model = GJRGARCH(sp500_returns, p=1, q=1)
        results = model.fit(disp=False)
        params = results.params
        sigma2_prev = np.var(sp500_returns)

        # Positive shock
        sigma2_pos = model._one_step_variance(0.01, sigma2_prev, params)
        # Negative shock (same magnitude)
        sigma2_neg = model._one_step_variance(-0.01, sigma2_prev, params)

        assert sigma2_neg > sigma2_pos, "Negative shock should produce higher variance"

    def test_gjr_transform_roundtrip(self, sp500_returns: np.ndarray):
        model = GJRGARCH(sp500_returns, p=1, q=1)
        params = model.start_params
        constrained = model.transform_params(params)
        unconstrained = model.untransform_params(constrained)
        roundtrip = model.transform_params(unconstrained)
        np.testing.assert_allclose(constrained, roundtrip, rtol=1e-6)
