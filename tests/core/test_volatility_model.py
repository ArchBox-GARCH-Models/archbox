"""Tests for VolatilityModel base class."""

from __future__ import annotations

import numpy as np
import pytest

from archbox.core.volatility_model import VolatilityModel


class DummyModel(VolatilityModel):
    """Minimal concrete implementation for testing the ABC."""

    volatility_process = "Dummy"

    def __init__(self, endog, **kwargs):
        super().__init__(endog, **kwargs)

    def _variance_recursion(self, params, resids, backcast):
        sigma2 = np.full(len(resids), params[0])
        return sigma2

    @property
    def start_params(self):
        return np.array([np.var(self.endog)])

    @property
    def param_names(self):
        return ["sigma2"]

    def transform_params(self, unconstrained):
        return np.exp(unconstrained)

    def untransform_params(self, constrained):
        return np.log(constrained)

    def bounds(self):
        return [(1e-12, None)]

    @property
    def num_params(self):
        return 1


class TestVolatilityModelABC:
    """Test the abstract base class contract."""

    def test_cannot_instantiate_abc(self):
        with pytest.raises(TypeError):
            VolatilityModel(np.random.randn(100))

    def test_concrete_instantiation(self, rng):
        returns = rng.standard_normal(200)
        model = DummyModel(returns)
        assert model.nobs == 200
        assert model.volatility_process == "Dummy"

    def test_demean_constant(self, rng):
        returns = rng.standard_normal(200) + 0.5
        model = DummyModel(returns, mean="constant")
        assert abs(np.mean(model.endog)) < 1e-10

    def test_mean_zero(self, rng):
        returns = rng.standard_normal(200) + 0.5
        model = DummyModel(returns, mean="zero")
        assert model.mu == 0.0

    def test_backcast_positive(self, rng):
        returns = rng.standard_normal(200)
        model = DummyModel(returns)
        bc = model._backcast(model.endog)
        assert bc > 0

    def test_loglike_returns_float(self, rng):
        returns = rng.standard_normal(200)
        model = DummyModel(returns)
        ll = model.loglike(model.start_params)
        assert isinstance(ll, float)
        assert np.isfinite(ll)

    def test_param_names(self, rng):
        returns = rng.standard_normal(200)
        model = DummyModel(returns)
        assert model.param_names == ["sigma2"]

    def test_num_params(self, rng):
        returns = rng.standard_normal(200)
        model = DummyModel(returns)
        assert model.num_params == 1

    def test_invalid_mean_model(self, rng):
        returns = rng.standard_normal(200)
        with pytest.raises(ValueError, match="Unknown mean model"):
            DummyModel(returns, mean="invalid")

    def test_validation_nan(self):
        returns = np.array([1.0, 2.0, np.nan] + [0.0] * 10)
        with pytest.raises(ValueError, match="NaN"):
            DummyModel(returns)

    def test_validation_too_short(self):
        returns = np.array([1.0, 2.0, 3.0])
        with pytest.raises(ValueError, match="at least 10"):
            DummyModel(returns)
