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


class TestGARCHMParameterLayout:
    """lambda belongs to the variance/mean block; shape parameters trail it."""

    def test_lambda_index_is_not_the_last_entry_with_shape_params(
        self, sp500_returns: np.ndarray
    ) -> None:
        model = GARCHM(sp500_returns, p=1, q=1, dist="studentt")
        results = model.fit(disp=False)
        named = dict(zip(results.param_names, results.params, strict=True))

        assert results.param_names == ["omega", "alpha[1]", "beta[1]", "lambda", "nu"]
        assert named["lambda"] != named["nu"]
        assert np.isfinite(named["lambda"])
        assert abs(named["lambda"]) < 50.0, "lambda must stay on a sane scale"
        assert named["nu"] > 2.0

    def test_blocks_read_lambda_from_the_variance_block(self, sp500_returns: np.ndarray) -> None:
        model = GARCHM(sp500_returns, p=1, q=1, dist="studentt")
        params = np.array([1e-6, 0.08, 0.90, 0.5, 7.0])  # [.. lambda, nu]
        _, _, _, lam = model._garchm_blocks(params)
        assert lam == pytest.approx(0.5)

    def test_loglike_uses_the_distribution_shape_parameters(
        self, sp500_returns: np.ndarray
    ) -> None:
        model = GARCHM(sp500_returns, p=1, q=1, dist="studentt")
        base = np.array([1e-6, 0.08, 0.90, 0.5, 5.0])
        other = np.array([1e-6, 0.08, 0.90, 0.5, 30.0])
        assert model.loglike(base) != model.loglike(other)

    def test_lambda_changes_the_likelihood(self, sp500_returns: np.ndarray) -> None:
        model = GARCHM(sp500_returns, p=1, q=1)
        zero_lambda = np.array([1e-6, 0.08, 0.90, 0.0])
        some_lambda = np.array([1e-6, 0.08, 0.90, 5.0])
        assert model.loglike(zero_lambda) != model.loglike(some_lambda)

    def test_conditional_variance_matches_the_likelihood_path(
        self, sp500_returns: np.ndarray
    ) -> None:
        model = GARCHM(sp500_returns, p=1, q=1, dist="studentt")
        results = model.fit(disp=False)
        backcast = model._backcast(model.endog)
        sigma2, _ = model._garchm_joint_recursion(results.params, backcast)
        np.testing.assert_allclose(results.conditional_volatility, np.sqrt(sigma2), rtol=1e-10)
