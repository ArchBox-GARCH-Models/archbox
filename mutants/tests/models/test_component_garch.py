"""Tests for Component GARCH model."""

from __future__ import annotations

import numpy as np

from archbox.models.component_garch import ComponentGARCH


class TestComponentGARCH:
    """Test Component GARCH model."""

    def test_component_garch_instantiation(self, sp500_returns: np.ndarray) -> None:
        model = ComponentGARCH(sp500_returns)
        assert model.volatility_process == "Component GARCH"
        assert model.num_params == 5  # omega, alpha, beta, alpha_p, beta_p
        assert len(model.param_names) == 5

    def test_component_garch_variance_recursion(self, sp500_returns: np.ndarray) -> None:
        model = ComponentGARCH(sp500_returns)
        params = model.start_params
        backcast = model._backcast(model.endog)
        sigma2 = model._variance_recursion(params, model.endog, backcast)
        assert len(sigma2) == model.nobs
        assert np.all(sigma2 > 0)
        assert np.all(np.isfinite(sigma2))

    def test_component_garch_fit_sp500(self, sp500_returns: np.ndarray) -> None:
        model = ComponentGARCH(sp500_returns)
        results = model.fit(disp=False)
        assert results is not None
        assert np.isfinite(results.loglike)

    def test_component_decomposition(self, sp500_returns: np.ndarray) -> None:
        """q_t + h_t == sigma^2_t always."""
        model = ComponentGARCH(sp500_returns)
        results = model.fit(disp=False)
        params = results.params
        backcast = model._backcast(model.endog)
        sigma2, q, h = model.variance_decomposition(params, model.endog, backcast)
        np.testing.assert_allclose(
            sigma2,
            q + h,
            rtol=1e-10,
            err_msg="sigma^2_t must equal q_t + h_t",
        )

    def test_component_beta_p_close_to_one(self, sp500_returns: np.ndarray) -> None:
        """beta_p (permanent component) should be close to 1."""
        model = ComponentGARCH(sp500_returns)
        results = model.fit(disp=False)
        beta_p = results.params[4]
        assert 0 < beta_p < 1, f"beta_p must be in (0,1), got {beta_p}"

    def test_component_garch_forecast(self, sp500_returns: np.ndarray) -> None:
        model = ComponentGARCH(sp500_returns)
        results = model.fit(disp=False)
        forecast = results.forecast(horizon=10)
        assert forecast is not None
        assert len(forecast["variance"]) == 10
        assert np.all(np.isfinite(forecast["variance"]))

    def test_component_garch_summary(self, sp500_returns: np.ndarray) -> None:
        model = ComponentGARCH(sp500_returns)
        results = model.fit(disp=False)
        summary = results.summary()
        assert summary is not None
        assert "Component GARCH" in str(summary)

    def test_component_garch_transform_roundtrip(self, sp500_returns: np.ndarray) -> None:
        model = ComponentGARCH(sp500_returns)
        params = model.start_params
        constrained = model.transform_params(params)
        unconstrained = model.untransform_params(constrained)
        roundtrip = model.transform_params(unconstrained)
        np.testing.assert_allclose(constrained, roundtrip, rtol=1e-6)
