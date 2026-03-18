"""Tests for MultivariateVolatilityModel base class."""

from __future__ import annotations

import numpy as np
import pytest
from numpy.typing import NDArray

from archbox.multivariate.base import MultivariateVolatilityModel


class _ConcreteMultivar(MultivariateVolatilityModel):
    """Minimal concrete subclass for testing validation."""

    model_name = "TestModel"

    def _correlation_recursion(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        T, k = std_resids.shape
        R_t = np.zeros((T, k, k))
        for t in range(T):
            R_t[t] = np.eye(k)
        return R_t

    @property
    def start_params(self) -> NDArray[np.float64]:
        return np.array([], dtype=np.float64)

    @property
    def param_names(self) -> list[str]:
        return []


class TestMultivariateVolatilityModelABC:
    """Test the abstract base class contract."""

    def test_cannot_instantiate_abc(self, rng):
        """MultivariateVolatilityModel cannot be instantiated directly."""
        returns = rng.standard_normal((200, 3))
        with pytest.raises(TypeError):
            MultivariateVolatilityModel(returns)

    def test_validation_1d_input(self, rng):
        """1D input should raise ValueError."""
        returns = rng.standard_normal(200)
        with pytest.raises(ValueError, match="2D"):
            _ConcreteMultivar(returns)

    def test_validation_single_series(self, rng):
        """Single series should raise ValueError."""
        returns = rng.standard_normal((200, 1))
        with pytest.raises(ValueError, match="at least 2"):
            _ConcreteMultivar(returns)

    def test_validation_too_short(self, rng):
        """Short series should raise ValueError."""
        returns = rng.standard_normal((10, 3))
        with pytest.raises(ValueError, match="at least 20"):
            _ConcreteMultivar(returns)

    def test_validation_nan(self, rng):
        """NaN in data should raise ValueError."""
        returns = rng.standard_normal((200, 3))
        returns[50, 1] = np.nan
        with pytest.raises(ValueError, match="NaN"):
            _ConcreteMultivar(returns)


class TestMultivarResultsDatasets:
    """Test that datasets load correctly."""

    def test_fx_majors_loads(self, fx_data):
        """fx_majors dataset should load correctly."""
        assert len(fx_data) == 2000
        assert "usd_eur" in fx_data.columns
        assert "usd_gbp" in fx_data.columns
        assert "usd_jpy" in fx_data.columns

    def test_sector_indices_loads(self, sector_data):
        """sector_indices dataset should load correctly."""
        assert len(sector_data) == 2000
        assert "tech" in sector_data.columns
        assert "finance" in sector_data.columns

    def test_fx_returns_shape(self, fx_returns):
        """FX returns should be (2000, 3)."""
        assert fx_returns.shape == (2000, 3)

    def test_sector_returns_shape(self, sector_returns):
        """Sector returns should be (2000, 5)."""
        assert sector_returns.shape == (2000, 5)

    def test_no_nan_fx(self, fx_returns):
        """FX returns should have no NaN."""
        assert not np.any(np.isnan(fx_returns))

    def test_no_nan_sector(self, sector_returns):
        """Sector returns should have no NaN."""
        assert not np.any(np.isnan(sector_returns))
