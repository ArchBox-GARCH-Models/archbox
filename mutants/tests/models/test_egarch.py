"""Tests for EGARCH model."""

from __future__ import annotations

import numpy as np

from archbox.models.egarch import EGARCH


class TestEGARCH:
    """Test EGARCH model."""

    def test_egarch_instantiation(self, sp500_returns: np.ndarray):
        model = EGARCH(sp500_returns, p=1, q=1)
        assert model.volatility_process == "EGARCH"
        assert model.num_params == 4  # omega, alpha, gamma, beta
        assert len(model.param_names) == 4

    def test_egarch_variance_recursion(self, sp500_returns: np.ndarray):
        model = EGARCH(sp500_returns, p=1, q=1)
        params = model.start_params
        backcast = model._backcast(model.endog)
        sigma2 = model._variance_recursion(params, model.endog, backcast)
        assert len(sigma2) == model.nobs
        assert np.all(sigma2 > 0), "EGARCH variance must be positive"
        assert np.all(np.isfinite(sigma2)), "Variance must be finite"

    def test_egarch_fit_sp500(self, sp500_returns: np.ndarray):
        model = EGARCH(sp500_returns, p=1, q=1)
        results = model.fit(disp=False)
        assert results is not None
        assert np.isfinite(results.loglike)
        # EGARCH should have beta close to persistence ~0.98
        beta_idx = 3  # omega, alpha, gamma, beta
        assert abs(results.params[beta_idx]) < 1.0, "Beta must satisfy |beta| < 1"

    def test_egarch_leverage(self, sp500_returns: np.ndarray):
        """Gamma should be negative for SP500 (negative shocks increase vol more)."""
        model = EGARCH(sp500_returns, p=1, q=1)
        results = model.fit(disp=False)
        gamma_idx = 2  # omega, alpha, gamma, beta
        assert (
            results.params[gamma_idx] < 0
        ), f"EGARCH gamma should be < 0 for SP500, got {results.params[gamma_idx]}"

    def test_egarch_no_positivity_constraint(self, sp500_returns: np.ndarray):
        """EGARCH should accept negative omega and alpha (no positivity constraint)."""
        model = EGARCH(sp500_returns, p=1, q=1)
        # Use params with negative omega - should not error
        params = np.array([-0.1, 0.1, -0.05, 0.95])
        backcast = model._backcast(model.endog)
        sigma2 = model._variance_recursion(params, model.endog, backcast)
        assert np.all(sigma2 > 0), "EGARCH always produces positive variance"

    def test_egarch_forecast(self, sp500_returns: np.ndarray):
        model = EGARCH(sp500_returns, p=1, q=1)
        results = model.fit(disp=False)
        forecast = results.forecast(horizon=10)
        assert forecast is not None
        assert len(forecast["variance"]) == 10
        assert np.all(np.isfinite(forecast["variance"])), "Forecast must not contain NaN"

    def test_egarch_summary(self, sp500_returns: np.ndarray):
        model = EGARCH(sp500_returns, p=1, q=1)
        results = model.fit(disp=False)
        summary = results.summary()
        assert summary is not None
        assert "EGARCH" in str(summary)

    def test_egarch_transform_roundtrip(self, sp500_returns: np.ndarray):
        model = EGARCH(sp500_returns, p=1, q=1)
        params = model.start_params
        constrained = model.transform_params(params)
        unconstrained = model.untransform_params(constrained)
        roundtrip = model.transform_params(unconstrained)
        np.testing.assert_allclose(constrained, roundtrip, rtol=1e-6)
