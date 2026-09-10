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


class TestTransitionParametrization:
    """Softmax (multinomial-logit) row parametrization of P."""

    @pytest.mark.parametrize("k", [2, 3, 4, 5])
    def test_valid_stochastic_matrix_for_any_k(self, k):
        """Random logits must always produce a valid stochastic matrix."""
        rng = np.random.default_rng(0)
        for _ in range(50):
            logits = rng.normal(scale=5.0, size=k * (k - 1))
            P = MarkovSwitchingModel._transition_matrix_from_logits(logits, k)
            assert P.shape == (k, k)
            assert np.all(P >= 0.0), f"negative probability in {P}"
            assert np.all(P <= 1.0), f"probability above one in {P}"
            np.testing.assert_allclose(P.sum(axis=1), np.ones(k), atol=1e-12)

    def test_zero_logits_give_uniform_rows(self):
        """Zero logits map to uniform transition probabilities."""
        for k in (2, 3, 4):
            P = MarkovSwitchingModel._transition_matrix_from_logits(np.zeros(k * (k - 1)), k)
            np.testing.assert_allclose(P, np.full((k, k), 1.0 / k), atol=1e-12)

    def test_roundtrip_logits(self):
        """matrix -> logits -> matrix is the identity."""
        P = np.array(
            [
                [0.90, 0.07, 0.03],
                [0.10, 0.85, 0.05],
                [0.02, 0.08, 0.90],
            ]
        )
        logits = MarkovSwitchingModel._transition_matrix_to_logits(P)
        assert logits.shape == (6,)
        back = MarkovSwitchingModel._transition_matrix_from_logits(logits, 3)
        np.testing.assert_allclose(back, P, atol=1e-10)

    def test_set_transition_params_roundtrip(self):
        """Writing P into params and reading it back is lossless."""
        rng = np.random.default_rng(1)
        y = rng.standard_normal(100)
        model = DummyMSModel(y, k_regimes=3)
        params = np.concatenate([np.linspace(-1, 1, 3), np.ones(3), np.zeros(3 * 2)])
        P = np.array([[0.8, 0.15, 0.05], [0.1, 0.7, 0.2], [0.05, 0.05, 0.90]])
        new_params = model._set_transition_params(params, P)
        np.testing.assert_allclose(model._extract_transition_matrix(new_params), P, atol=1e-10)
        # only the transition block changed
        np.testing.assert_allclose(new_params[:6], params[:6], atol=0.0)

    def test_three_regime_extraction_is_valid(self):
        """The k=3 start params give a valid matrix (regression: k>=3 bug)."""
        rng = np.random.default_rng(2)
        y = rng.standard_normal(200)
        model = DummyMSModel(y, k_regimes=3)
        P = model._extract_transition_matrix(model.start_params)
        assert np.all(P >= 0.0)
        np.testing.assert_allclose(P.sum(axis=1), np.ones(3), atol=1e-12)


class TestLoglikePerformance:
    """The likelihood must be O(T*k), not O(T^2*k)."""

    def test_regime_loglike_called_once_per_regime(self):
        """loglike() must not recompute the regime densities per (t, s)."""

        class CountingModel(DummyMSModel):
            calls = 0

            def _regime_loglike(self, params, regime):
                type(self).calls += 1
                return super()._regime_loglike(params, regime)

        rng = np.random.default_rng(3)
        y = rng.standard_normal(300)
        model = CountingModel(y, k_regimes=2)
        CountingModel.calls = 0
        value = model.loglike(model.start_params)
        assert np.isfinite(value)
        assert CountingModel.calls == 2, f"expected k=2 calls, got {CountingModel.calls}"


class TestForecastAndSimulate:
    """Real forecasts and simulation from the fitted parameters."""

    @staticmethod
    def _fit_meanvar():
        from archbox.regime.ms_mean import MarkovSwitchingMeanVar

        rng = np.random.default_rng(11)
        T = 600
        P = np.array([[0.95, 0.05], [0.10, 0.90]])
        regimes = np.zeros(T, dtype=int)
        for t in range(1, T):
            regimes[t] = rng.choice(2, p=P[regimes[t - 1]])
        mu = [-2.0, 2.0]
        sigma = [0.5, 1.0]
        y = np.array([mu[s] + sigma[s] * rng.standard_normal() for s in regimes])
        model = MarkovSwitchingMeanVar(y, k_regimes=2)
        results = model.fit(maxiter=300, tol=1e-10, verbose=False)
        return model, results

    def test_forecast_structure(self):
        """forecast() returns mean, variance and regime probabilities."""
        model, _results = self._fit_meanvar()
        fc = model.forecast(6)

        assert set(fc) == {"mean", "variance", "regime_probs"}
        assert fc["mean"].shape == (6,)
        assert fc["variance"].shape == (6,)
        assert fc["regime_probs"].shape == (6, 2)
        np.testing.assert_allclose(fc["regime_probs"].sum(axis=1), 1.0, atol=1e-10)
        assert np.all(np.isfinite(fc["mean"]))
        assert np.all(fc["variance"] > 0)
        assert np.any(fc["mean"] != 0.0), "forecast must not be identically zero"

    def test_forecast_uses_params(self):
        """Different parameters give different forecasts."""
        model, results = self._fit_meanvar()
        shifted = results.params.copy()
        shifted[0] += 5.0
        shifted[1] += 5.0
        base = model.forecast(3)["mean"]
        moved = model.forecast(3, params=shifted)["mean"]
        np.testing.assert_allclose(moved - base, 5.0, atol=1e-8)

    def test_forecast_converges_to_ergodic_mixture(self):
        """At long horizons the mixture mean uses the ergodic probabilities."""
        model, results = self._fit_meanvar()
        fc = model.forecast(400)
        ergodic = results.ergodic_probabilities()
        mus = np.array([results.regime_params[s]["mu"] for s in range(2)])
        np.testing.assert_allclose(fc["regime_probs"][-1], ergodic, atol=1e-6)
        np.testing.assert_allclose(fc["mean"][-1], float(ergodic @ mus), atol=1e-6)

    def test_forecast_horizon_validation(self):
        """A non-positive horizon is rejected."""
        model, _ = self._fit_meanvar()
        with pytest.raises(ValueError, match="horizon"):
            model.forecast(0)

    def test_simulate_uses_params(self):
        """simulate() draws from the fitted regime distributions, not N(0,1)."""
        model, results = self._fit_meanvar()
        y, regimes, probs = model.simulate(4000, results.params, seed=7)

        assert y.shape == (4000,)
        assert regimes.shape == (4000,)
        assert probs.shape == (4000, 2)
        np.testing.assert_allclose(probs.sum(axis=1), 1.0, atol=1e-12)

        for s in range(2):
            mask = regimes == s
            assert mask.sum() > 100
            assert abs(y[mask].mean() - results.regime_params[s]["mu"]) < 0.2
            assert abs(y[mask].std() - results.regime_params[s]["sigma"]) < 0.2

    def test_simulate_is_reproducible(self):
        """The same seed gives the same path."""
        model, results = self._fit_meanvar()
        y1, r1, _ = model.simulate(200, results.params, seed=3)
        y2, r2, _ = model.simulate(200, results.params, seed=3)
        np.testing.assert_allclose(y1, y2, atol=0.0)
        np.testing.assert_array_equal(r1, r2)

    def test_forecast_requires_params(self):
        """Forecasting before fitting raises."""
        rng = np.random.default_rng(5)
        model = DummyMSModel(rng.standard_normal(50), k_regimes=2)
        with pytest.raises(RuntimeError, match="Fit the model first"):
            model.forecast(2)
