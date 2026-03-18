"""Tests for ArchResults container."""

from __future__ import annotations

import tempfile
from pathlib import Path

import numpy as np
import pytest

from archbox.core.results import ArchResults
from archbox.core.volatility_model import VolatilityModel


class MockModel(VolatilityModel):
    """Mock model for testing ArchResults."""

    volatility_process = "MockGARCH"

    def __init__(self, endog, **kwargs):
        super().__init__(endog, **kwargs)
        self.q = 1
        self.p = 1

    def _variance_recursion(self, params, resids, backcast):
        return np.full(len(resids), np.var(resids))

    @property
    def start_params(self):
        return np.array([1e-6, 0.08, 0.91])

    @property
    def param_names(self):
        return ["omega", "alpha[1]", "beta[1]"]

    def transform_params(self, unconstrained):
        return np.exp(unconstrained)

    def untransform_params(self, constrained):
        return np.log(constrained)

    def bounds(self):
        return [(1e-12, None), (0, 1), (0, 1)]

    @property
    def num_params(self):
        return 3


@pytest.fixture
def mock_results(rng) -> ArchResults:
    """Create mock ArchResults for testing."""
    returns = rng.standard_normal(500) * 0.01
    model = MockModel(returns)

    params = np.array([1e-6, 0.08, 0.91])
    sigma2 = np.full(500, np.var(returns))
    se = np.array([1e-7, 0.02, 0.03])

    return ArchResults(
        model=model,
        params=params,
        loglike=-1500.0,
        sigma2=sigma2,
        se_robust=se,
        se_nonrobust=se * 0.9,
        convergence=True,
    )


class TestArchResults:
    """Test ArchResults container."""

    def test_summary_no_error(self, mock_results: ArchResults):
        """summary() should produce a formatted string without error."""
        s = mock_results.summary()
        assert isinstance(s, str)
        assert "omega" in s
        assert "alpha[1]" in s
        assert "beta[1]" in s
        assert "Persistence" in s

    def test_aic_formula(self, mock_results: ArchResults):
        """AIC = -2*loglike + 2*k."""
        k = len(mock_results.params)
        expected = -2 * mock_results.loglike + 2 * k
        assert abs(mock_results.aic - expected) < 1e-10

    def test_bic_formula(self, mock_results: ArchResults):
        """BIC = -2*loglike + k*log(n)."""
        k = len(mock_results.params)
        n = mock_results.nobs
        expected = -2 * mock_results.loglike + k * np.log(n)
        assert abs(mock_results.bic - expected) < 1e-10

    def test_hqic_formula(self, mock_results: ArchResults):
        """HQIC = -2*loglike + 2*k*log(log(n))."""
        k = len(mock_results.params)
        n = mock_results.nobs
        expected = -2 * mock_results.loglike + 2 * k * np.log(np.log(n))
        assert abs(mock_results.hqic - expected) < 1e-10

    def test_se_positive(self, mock_results: ArchResults):
        """Standard errors must all be > 0."""
        assert np.all(mock_results.se > 0)
        assert np.all(mock_results.se_robust > 0)
        assert np.all(mock_results.se_nonrobust > 0)

    def test_tvalues_finite(self, mock_results: ArchResults):
        assert np.all(np.isfinite(mock_results.tvalues))

    def test_pvalues_in_01(self, mock_results: ArchResults):
        assert np.all(mock_results.pvalues >= 0)
        assert np.all(mock_results.pvalues <= 1)

    def test_persistence(self, mock_results: ArchResults):
        """Persistence = sum(params[1:])."""
        expected = 0.08 + 0.91
        assert abs(mock_results.persistence() - expected) < 1e-10

    def test_half_life_positive(self, mock_results: ArchResults):
        hl = mock_results.half_life()
        assert hl > 0
        assert np.isfinite(hl)

    def test_unconditional_variance_positive(self, mock_results: ArchResults):
        uv = mock_results.unconditional_variance()
        assert uv > 0

    def test_forecast_shape(self, mock_results: ArchResults):
        fc = mock_results.forecast(horizon=10)
        assert "variance" in fc
        assert "volatility" in fc
        assert fc["variance"].shape == (10,)
        assert fc["volatility"].shape == (10,)

    def test_forecast_mean_reverts(self, mock_results: ArchResults):
        """Forecast should converge to unconditional variance."""
        fc = mock_results.forecast(horizon=500)
        uv = mock_results.unconditional_variance()
        # Last forecast should be close to unconditional variance
        assert abs(fc["variance"][-1] - uv) / uv < 0.01

    def test_conditional_volatility_shape(self, mock_results: ArchResults):
        assert mock_results.conditional_volatility.shape == (500,)

    def test_resid_shape(self, mock_results: ArchResults):
        assert mock_results.resid.shape == (500,)

    def test_to_dataframe(self, mock_results: ArchResults):
        df = mock_results.to_dataframe()
        assert list(df.columns) == ["estimate", "std_err", "t_value", "p_value"]
        assert list(df.index) == ["omega", "alpha[1]", "beta[1]"]

    def test_save_load(self, mock_results: ArchResults):
        with tempfile.NamedTemporaryFile(suffix=".pkl", delete=False) as f:
            path = Path(f.name)
        try:
            mock_results.save(path)
            loaded = ArchResults.load(path)
            np.testing.assert_array_equal(loaded.params, mock_results.params)
            assert loaded.loglike == mock_results.loglike
        finally:
            path.unlink(missing_ok=True)

    def test_repr(self, mock_results: ArchResults):
        r = repr(mock_results)
        assert "MockGARCH" in r
        assert "500" in r
