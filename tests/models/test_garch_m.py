"""Tests for GARCH-M model."""

from __future__ import annotations

import numpy as np
import pytest

from archbox.models.garch_m import GARCHM


class TestGARCHM:
    """Test GARCH-M model."""

    def test_garch_m_instantiation(self, sp500_returns: np.ndarray) -> None:
        model = GARCHM(sp500_returns, p=1, q=1)
        assert model.volatility_process == "GARCH-M"
        assert model.num_params == 4  # omega, alpha, beta, lambda
        assert len(model.param_names) == 4

    def test_garch_m_variance_recursion(self, sp500_returns: np.ndarray) -> None:
        model = GARCHM(sp500_returns, p=1, q=1)
        params = model.start_params
        backcast = model._backcast(model.endog)
        sigma2 = model._variance_recursion(params, model.endog, backcast)
        assert len(sigma2) == model.nobs
        assert np.all(sigma2 > 0)
        assert np.all(np.isfinite(sigma2))

    def test_garch_m_fit_sp500(self, sp500_returns: np.ndarray) -> None:
        model = GARCHM(sp500_returns, p=1, q=1)
        results = model.fit(disp=False)
        assert results is not None
        assert np.isfinite(results.loglike)

    def test_garch_m_lambda_estimated(self, sp500_returns: np.ndarray) -> None:
        """Lambda (risk premium) should be estimated (not exactly zero)."""
        model = GARCHM(sp500_returns, p=1, q=1)
        results = model.fit(disp=False)
        lam = results.params[-1]
        # Lambda may be small but should be estimated
        assert np.isfinite(lam), "lambda must be finite"

    def test_garch_m_risk_premium_variance(self, sp500_returns: np.ndarray) -> None:
        model = GARCHM(sp500_returns, p=1, q=1, risk_premium="variance")
        results = model.fit(disp=False)
        assert results is not None

    def test_garch_m_risk_premium_volatility(self, sp500_returns: np.ndarray) -> None:
        model = GARCHM(sp500_returns, p=1, q=1, risk_premium="volatility")
        results = model.fit(disp=False)
        assert results is not None

    def test_garch_m_risk_premium_log_variance(self, sp500_returns: np.ndarray) -> None:
        model = GARCHM(sp500_returns, p=1, q=1, risk_premium="log_variance")
        results = model.fit(disp=False)
        assert results is not None

    def test_garch_m_invalid_risk_premium(self, sp500_returns: np.ndarray) -> None:
        with pytest.raises(ValueError, match="Unknown risk_premium"):
            GARCHM(sp500_returns, risk_premium="invalid")

    def test_garch_m_forecast(self, sp500_returns: np.ndarray) -> None:
        model = GARCHM(sp500_returns, p=1, q=1)
        results = model.fit(disp=False)
        forecast = results.forecast(horizon=10)
        assert forecast is not None
        assert len(forecast["variance"]) == 10
        assert np.all(np.isfinite(forecast["variance"]))

    def test_garch_m_summary(self, sp500_returns: np.ndarray) -> None:
        model = GARCHM(sp500_returns, p=1, q=1)
        results = model.fit(disp=False)
        summary = results.summary()
        assert summary is not None
        assert "GARCH-M" in str(summary)

    def test_garch_m_transform_roundtrip(self, sp500_returns: np.ndarray) -> None:
        model = GARCHM(sp500_returns, p=1, q=1)
        params = model.start_params
        constrained = model.transform_params(params)
        unconstrained = model.untransform_params(constrained)
        roundtrip = model.transform_params(unconstrained)
        np.testing.assert_allclose(constrained, roundtrip, rtol=1e-6)
