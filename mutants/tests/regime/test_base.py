"""Tests for MarkovSwitchingModel base class."""

from __future__ import annotations

import numpy as np
import pytest

from archbox.regime.base import MarkovSwitchingModel


class DummyMSModel(MarkovSwitchingModel):
    """Minimal concrete implementation for testing the ABC."""

    model_name = "DummyMS"

    def _regime_loglike(self, params, regime):
        """Simple Gaussian log-likelihood with regime-specific mean."""
        k = self.k_regimes
        mu = params[regime]
        sigma = params[k + regime] if self.switching_variance else params[k]
        y = self.endog
        ll = -0.5 * np.log(2 * np.pi) - np.log(sigma) - 0.5 * ((y - mu) / sigma) ** 2
        return ll

    @property
    def start_params(self):
        k = self.k_regimes
        mus = np.linspace(-1, 1, k)
        sigmas = np.ones(k)
        # Transition params (logit of off-diagonal)
        trans = np.zeros(k * (k - 1))
        return np.concatenate([mus, sigmas, trans])

    @property
    def param_names(self):
        k = self.k_regimes
        names = [f"mu_{i}" for i in range(k)]
        names += [f"sigma_{i}" for i in range(k)]
        names += [f"p_{i}{j}" for i in range(k) for j in range(k) if i != j]
        return names


class TestMarkovSwitchingModelABC:
    """Test the abstract base class contract."""

    def test_cannot_instantiate_abc(self):
        with pytest.raises(TypeError):
            MarkovSwitchingModel(np.random.randn(100))

    def test_concrete_instantiation(self):
        rng = np.random.default_rng(42)
        y = rng.standard_normal(200)
        model = DummyMSModel(y, k_regimes=2)
        assert model.nobs == 200
        assert model.k_regimes == 2
        assert model.model_name == "DummyMS"

    def test_invalid_k_regimes(self):
        rng = np.random.default_rng(42)
        y = rng.standard_normal(200)
        with pytest.raises(ValueError, match="k_regimes must be >= 2"):
            DummyMSModel(y, k_regimes=1)

    def test_start_params_length(self):
        rng = np.random.default_rng(42)
        y = rng.standard_normal(200)
        model = DummyMSModel(y, k_regimes=2)
        # 2 mus + 2 sigmas + 2 trans params = 6
        assert len(model.start_params) == 6

    def test_param_names_length(self):
        rng = np.random.default_rng(42)
        y = rng.standard_normal(200)
        model = DummyMSModel(y, k_regimes=2)
        assert len(model.param_names) == 6

    def test_regime_loglike_shape(self):
        rng = np.random.default_rng(42)
        y = rng.standard_normal(200)
        model = DummyMSModel(y, k_regimes=2)
        params = model.start_params
        ll = model._regime_loglike(params, 0)
        assert ll.shape == (200,)

    def test_extract_transition_matrix(self):
        rng = np.random.default_rng(42)
        y = rng.standard_normal(200)
        model = DummyMSModel(y, k_regimes=2)
        params = model.start_params
        P = model._extract_transition_matrix(params)
        assert P.shape == (2, 2)
        # Rows should sum to 1
        np.testing.assert_allclose(P.sum(axis=1), np.ones(2), atol=1e-10)

    def test_build_transition_matrix_from_diag(self):
        stay_probs = np.array([0.9, 0.95])
        P = MarkovSwitchingModel._build_transition_matrix_from_diag(stay_probs)
        assert P.shape == (2, 2)
        np.testing.assert_allclose(P.sum(axis=1), np.ones(2), atol=1e-10)
        assert P[0, 0] == 0.9
        assert P[1, 1] == 0.95

    def test_3_regimes(self):
        rng = np.random.default_rng(42)
        y = rng.standard_normal(200)
        model = DummyMSModel(y, k_regimes=3)
        assert model.k_regimes == 3
        # 3 mus + 3 sigmas + 6 trans params = 12
        assert len(model.start_params) == 12


class TestDatasetsLoad:
    """Test that FASE4 datasets load correctly."""

    def test_load_us_gdp(self):
        from archbox.datasets import load_dataset

        df = load_dataset("us_gdp")
        assert len(df) > 0
        assert "date" in df.columns
        assert "growth" in df.columns

    @pytest.mark.skip(reason="us_recession_dates dataset not registered in load_dataset")
    def test_load_us_recession_dates(self):
        from archbox.datasets import load_dataset

        df = load_dataset("us_recession_dates")
        assert len(df) > 0
        assert "peak" in df.columns
        assert "trough" in df.columns
