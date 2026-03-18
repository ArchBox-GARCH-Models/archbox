"""Tests for IGARCH model."""

from __future__ import annotations

import numpy as np

from archbox.models.igarch import IGARCH


class TestIGARCH:
    """Test IGARCH model."""

    def test_igarch_instantiation(self, sp500_returns: np.ndarray) -> None:
        model = IGARCH(sp500_returns)
        assert model.volatility_process == "IGARCH"
        assert model.num_params == 2  # omega, alpha (beta = 1 - alpha)
        assert len(model.param_names) == 2

    def test_igarch_variance_recursion(self, sp500_returns: np.ndarray) -> None:
        model = IGARCH(sp500_returns)
        params = model.start_params
        backcast = model._backcast(model.endog)
        sigma2 = model._variance_recursion(params, model.endog, backcast)
        assert len(sigma2) == model.nobs
        assert np.all(sigma2 > 0)
        assert np.all(np.isfinite(sigma2))

    def test_igarch_fit_sp500(self, sp500_returns: np.ndarray) -> None:
        model = IGARCH(sp500_returns)
        results = model.fit(disp=False)
        assert results is not None
        assert np.isfinite(results.loglike)

    def test_igarch_persistence_one(self, sp500_returns: np.ndarray) -> None:
        """alpha + beta == 1 exactly (beta = 1 - alpha)."""
        model = IGARCH(sp500_returns)
        results = model.fit(disp=False)
        alpha = results.params[1]
        beta = 1.0 - alpha
        persistence = alpha + beta
        np.testing.assert_allclose(
            persistence,
            1.0,
            atol=1e-10,
            err_msg=f"IGARCH persistence must be exactly 1, got {persistence}",
        )

    def test_igarch_alpha_in_range(self, sp500_returns: np.ndarray) -> None:
        """alpha must be in (0, 1)."""
        model = IGARCH(sp500_returns)
        results = model.fit(disp=False)
        alpha = results.params[1]
        assert 0 < alpha < 1, f"alpha must be in (0,1), got {alpha}"

    def test_igarch_forecast(self, sp500_returns: np.ndarray) -> None:
        model = IGARCH(sp500_returns)
        results = model.fit(disp=False)
        forecast = results.forecast(horizon=10)
        assert forecast is not None
        assert len(forecast["variance"]) == 10
        assert np.all(np.isfinite(forecast["variance"]))

    def test_igarch_summary(self, sp500_returns: np.ndarray) -> None:
        model = IGARCH(sp500_returns)
        results = model.fit(disp=False)
        summary = results.summary()
        assert summary is not None
        assert "IGARCH" in str(summary)

    def test_igarch_transform_roundtrip(self, sp500_returns: np.ndarray) -> None:
        model = IGARCH(sp500_returns)
        params = model.start_params
        constrained = model.transform_params(params)
        unconstrained = model.untransform_params(constrained)
        roundtrip = model.transform_params(unconstrained)
        np.testing.assert_allclose(constrained, roundtrip, rtol=1e-6)
