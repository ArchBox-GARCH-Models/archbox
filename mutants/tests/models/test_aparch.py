"""Tests for APARCH model."""

from __future__ import annotations

import numpy as np

from archbox.models.aparch import APARCH


class TestAPARCH:
    """Test APARCH model."""

    def test_aparch_instantiation(self, sp500_returns: np.ndarray) -> None:
        model = APARCH(sp500_returns, p=1, q=1)
        assert model.volatility_process == "APARCH"
        assert model.num_params == 5  # omega, alpha, gamma, beta, delta
        assert len(model.param_names) == 5

    def test_aparch_variance_recursion(self, sp500_returns: np.ndarray) -> None:
        model = APARCH(sp500_returns, p=1, q=1)
        params = model.start_params
        backcast = model._backcast(model.endog)
        sigma2 = model._variance_recursion(params, model.endog, backcast)
        assert len(sigma2) == model.nobs
        assert np.all(sigma2 > 0)
        assert np.all(np.isfinite(sigma2))

    def test_aparch_fit_sp500(self, sp500_returns: np.ndarray) -> None:
        model = APARCH(sp500_returns, p=1, q=1)
        results = model.fit(disp=False)
        assert results is not None
        assert np.isfinite(results.loglike)

    def test_aparch_reduces_to_garch(self, sp500_returns: np.ndarray) -> None:
        """APARCH(delta=2, gamma=0) should produce same variance as GARCH."""
        from archbox.models.garch import GARCH

        garch_model = GARCH(sp500_returns, p=1, q=1)
        garch_results = garch_model.fit(disp=False)
        garch_params = garch_results.params  # omega, alpha, beta

        aparch_model = APARCH(sp500_returns, p=1, q=1)
        # Construct APARCH params: omega, alpha, gamma=0, beta, delta=2
        aparch_params = np.array(
            [
                garch_params[0],  # omega
                garch_params[1],  # alpha
                0.0,  # gamma = 0
                garch_params[2],  # beta
                2.0,  # delta = 2
            ]
        )

        backcast = aparch_model._backcast(aparch_model.endog)
        sigma2_aparch = aparch_model._variance_recursion(
            aparch_params, aparch_model.endog, backcast
        )

        backcast_g = garch_model._backcast(garch_model.endog)
        sigma2_garch = garch_model._variance_recursion(garch_params, garch_model.endog, backcast_g)

        np.testing.assert_allclose(
            sigma2_aparch,
            sigma2_garch,
            rtol=1e-4,
            err_msg="APARCH(delta=2,gamma=0) should match GARCH",
        )

    def test_aparch_forecast(self, sp500_returns: np.ndarray) -> None:
        model = APARCH(sp500_returns, p=1, q=1)
        results = model.fit(disp=False)
        forecast = results.forecast(horizon=10)
        assert forecast is not None
        assert len(forecast["variance"]) == 10
        assert np.all(np.isfinite(forecast["variance"]))

    def test_aparch_summary(self, sp500_returns: np.ndarray) -> None:
        model = APARCH(sp500_returns, p=1, q=1)
        results = model.fit(disp=False)
        summary = results.summary()
        assert summary is not None
        assert "APARCH" in str(summary)

    def test_aparch_transform_roundtrip(self, sp500_returns: np.ndarray) -> None:
        model = APARCH(sp500_returns, p=1, q=1)
        params = model.start_params
        constrained = model.transform_params(params)
        unconstrained = model.untransform_params(constrained)
        roundtrip = model.transform_params(unconstrained)
        np.testing.assert_allclose(constrained, roundtrip, rtol=1e-6)

    def test_aparch_delta_positive(self, sp500_returns: np.ndarray) -> None:
        """Estimated delta should be positive."""
        model = APARCH(sp500_returns, p=1, q=1)
        results = model.fit(disp=False)
        delta = results.params[-1]
        assert delta > 0, f"delta must be > 0, got {delta}"
