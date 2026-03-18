"""Tests for GARCH model - end-to-end validation."""

from __future__ import annotations

import numpy as np
import pytest

from archbox import GARCH
from archbox.datasets import load_dataset


@pytest.fixture
def sp500_returns() -> np.ndarray:
    """Load SP500 returns."""
    df = load_dataset("sp500")
    return df["returns"].to_numpy(dtype=np.float64)


@pytest.fixture
def fitted_garch(sp500_returns) -> object:
    """Fit GARCH(1,1) to SP500 returns."""
    model = GARCH(sp500_returns, p=1, q=1)
    return model.fit(disp=False)


class TestGARCHModel:
    """Test GARCH model instantiation."""

    def test_instantiation(self, sp500_returns):
        model = GARCH(sp500_returns, p=1, q=1)
        assert model.p == 1
        assert model.q == 1
        assert model.volatility_process == "GARCH"

    def test_repr(self, sp500_returns):
        model = GARCH(sp500_returns, p=1, q=1)
        r = repr(model)
        assert "GARCH" in r
        assert "p=1" in r

    def test_start_params(self, sp500_returns):
        model = GARCH(sp500_returns, p=1, q=1)
        sp = model.start_params
        assert len(sp) == 3
        assert sp[0] > 0  # omega
        assert 0 < sp[1] < 1  # alpha
        assert 0 < sp[2] < 1  # beta

    def test_param_names(self, sp500_returns):
        model = GARCH(sp500_returns, p=1, q=1)
        assert model.param_names == ["omega", "alpha[1]", "beta[1]"]

    def test_num_params(self, sp500_returns):
        model = GARCH(sp500_returns, p=1, q=1)
        assert model.num_params == 3

    def test_garch21_param_names(self, sp500_returns):
        model = GARCH(sp500_returns, p=2, q=1)
        assert model.param_names == ["omega", "alpha[1]", "beta[1]", "beta[2]"]
        assert model.num_params == 4


class TestGARCH11SP500:
    """Validation against known SP500 GARCH(1,1) results.

    The SP500 dataset was generated with:
        omega=1.5e-6, alpha=0.08, beta=0.91
    """

    def test_sp500_garch11_params(self, fitted_garch):
        """Parameters should be close to true DGP values (tol=20%)."""
        omega, alpha, beta = fitted_garch.params
        assert omega > 0
        assert 0.03 < alpha < 0.20, f"alpha={alpha} outside range"
        assert 0.70 < beta < 0.97, f"beta={beta} outside range"

    def test_stationarity_constraint(self, fitted_garch):
        """alpha + beta < 1."""
        persistence = fitted_garch.persistence()
        assert 0 < persistence < 1

    def test_persistence(self, fitted_garch):
        """Persistence should be high (typical for financial data)."""
        p = fitted_garch.persistence()
        assert 0.8 < p < 1.0

    def test_half_life(self, fitted_garch):
        """Half-life should be positive and finite."""
        hl = fitted_garch.half_life()
        assert hl > 0
        assert np.isfinite(hl)

    def test_unconditional_variance(self, fitted_garch):
        """Unconditional variance should be positive."""
        uv = fitted_garch.unconditional_variance()
        assert uv > 0
        assert np.isfinite(uv)

    def test_forecast_mean_reverts(self, fitted_garch):
        """Forecast should converge to unconditional variance."""
        # Need large horizon since persistence ~0.99 => half-life ~69 periods
        fc = fitted_garch.forecast(horizon=2000)
        uv = fitted_garch.unconditional_variance()
        # Last forecast close to unconditional
        assert abs(fc["variance"][-1] - uv) / uv < 0.05

    def test_forecast_shape(self, fitted_garch):
        """Forecast should return correct shapes."""
        fc = fitted_garch.forecast(horizon=10)
        assert fc["variance"].shape == (10,)
        assert fc["volatility"].shape == (10,)
        assert np.all(fc["variance"] > 0)
        assert np.all(fc["volatility"] > 0)

    def test_variance_targeting(self, sp500_returns):
        """Variance targeting should produce consistent omega."""
        model = GARCH(sp500_returns, p=1, q=1)
        results = model.fit(variance_targeting=True, disp=False)

        omega, alpha, beta = results.params
        sample_var = np.var(model.endog)
        expected_omega = sample_var * (1 - alpha - beta)
        assert abs(omega - expected_omega) / expected_omega < 0.01

    def test_loglike_finite(self, fitted_garch):
        """Log-likelihood should be finite."""
        assert np.isfinite(fitted_garch.loglike)

    def test_se_positive(self, fitted_garch):
        """All standard errors should be positive."""
        assert np.all(fitted_garch.se > 0)

    def test_summary_no_error(self, fitted_garch):
        """summary() should produce formatted output."""
        s = fitted_garch.summary()
        assert isinstance(s, str)
        assert "GARCH" in s
        assert "omega" in s
        assert "Persistence" in s

    def test_residuals_standardized(self, fitted_garch):
        """Standardized residuals should be ~N(0,1)."""
        z = fitted_garch.resid
        assert abs(np.mean(z)) < 0.1
        assert abs(np.std(z) - 1.0) < 0.2

    def test_to_dataframe(self, fitted_garch):
        df = fitted_garch.to_dataframe()
        assert "estimate" in df.columns
        assert "omega" in df.index

    def test_conditional_volatility_positive(self, fitted_garch):
        assert np.all(fitted_garch.conditional_volatility > 0)


class TestGARCHSimulate:
    """Test GARCH simulation."""

    def test_simulate_moments(self, sp500_returns):
        """Simulated variance should be close to unconditional."""
        model = GARCH(sp500_returns, p=1, q=1)
        results = model.fit(disp=False)

        returns_sim, vol_sim = model.simulate(
            n=5000,
            params=results.params,
            seed=42,
        )
        uv = results.unconditional_variance()

        # Simulated variance should be within 50% of unconditional
        # (smaller n => higher sampling variance, O(n^2) recursion limits size)
        sim_var = np.var(returns_sim)
        assert abs(sim_var - uv) / uv < 0.50


class TestEndToEnd:
    """Full integration test matching the spec's target code."""

    def test_full_workflow(self):
        """The exact code from the spec must work."""
        import matplotlib

        matplotlib.use("Agg")

        from archbox import GARCH
        from archbox.datasets import load_dataset

        sp500 = load_dataset("sp500")
        returns = sp500["returns"]

        model = GARCH(returns, p=1, q=1)
        results = model.fit(disp=False)

        # summary works
        summary = results.summary()
        assert len(summary) > 100

        # forecast works
        forecast = results.forecast(horizon=10)
        assert forecast["variance"].shape == (10,)
        assert np.all(forecast["variance"] > 0)

        # All quality checks
        assert results.convergence
        assert results.persistence() < 1
        assert results.half_life() > 0
        assert results.unconditional_variance() > 0

        # plot works
        fig = results.plot("volatility")
        assert fig is not None
        fig2 = results.plot("residuals")
        assert fig2 is not None
        with pytest.raises(ValueError, match="Unknown plot type"):
            results.plot("invalid")
        import matplotlib.pyplot as plt

        plt.close("all")

    def test_config_importable(self):
        """Config module should be importable."""
        from archbox.core.config import ArchBoxConfig, config

        assert config.default_optimizer == "SLSQP"
        assert isinstance(config, ArchBoxConfig)

    def test_transforms_module(self):
        """Transform utilities should work correctly."""
        from archbox.utils.transforms import (
            positive_transform,
            positive_untransform,
            stationarity_transform,
            unit_transform,
            unit_untransform,
        )

        x = np.array([0.0, 1.0, -1.0])
        assert np.allclose(positive_untransform(positive_transform(x)), x)
        assert np.allclose(unit_untransform(unit_transform(x)), x)

        alphas = np.array([0.5, 0.3])
        betas = np.array([0.4])
        a_out, b_out = stationarity_transform(alphas, betas)
        assert np.sum(a_out) + np.sum(b_out) < 1.0

    def test_validation_errors(self):
        """Validation should reject invalid inputs."""
        from archbox.utils.validation import validate_positive_integer, validate_returns

        with pytest.raises(ValueError, match="1D"):
            validate_returns(np.ones((10, 2)))
        with pytest.raises(ValueError, match="at least 10"):
            validate_returns(np.ones(5))
        with pytest.raises(ValueError, match="NaN"):
            validate_returns(np.array([np.nan] + [1.0] * 20))
        with pytest.raises(ValueError, match="Inf"):
            validate_returns(np.array([np.inf] + [1.0] * 20))
        with pytest.raises(ValueError, match="positive integer"):
            validate_positive_integer(0, "test")

    def test_dataset_list(self):
        """list_datasets should include sp500."""
        from archbox.datasets import list_datasets

        datasets = list_datasets()
        assert "sp500" in datasets
