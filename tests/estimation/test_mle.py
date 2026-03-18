"""Tests for MLEstimator."""

from __future__ import annotations

import numpy as np
import pytest

from archbox.core.volatility_model import VolatilityModel
from archbox.estimation.mle import MLEstimator


class SimpleGARCH(VolatilityModel):
    """Simple GARCH(1,1) for testing the estimator."""

    volatility_process = "GARCH"

    def __init__(self, endog: np.ndarray, **kwargs: object) -> None:
        self.p = 1
        self.q = 1
        super().__init__(endog, **kwargs)

    def _variance_recursion(
        self,
        params: np.ndarray,
        resids: np.ndarray,
        backcast: float,
    ) -> np.ndarray:
        omega, alpha, beta = params[0], params[1], params[2]
        T = len(resids)
        sigma2 = np.empty(T)
        sigma2[0] = backcast
        for t in range(1, T):
            sigma2[t] = omega + alpha * resids[t - 1] ** 2 + beta * sigma2[t - 1]
        return sigma2

    @property
    def start_params(self) -> np.ndarray:
        target_var = np.var(self.endog)
        return np.array([target_var * 0.05, 0.05, 0.90])

    @property
    def param_names(self) -> list[str]:
        return ["omega", "alpha[1]", "beta[1]"]

    def transform_params(self, unconstrained: np.ndarray) -> np.ndarray:
        return np.abs(unconstrained)

    def untransform_params(self, constrained: np.ndarray) -> np.ndarray:
        return constrained.copy()

    def bounds(self) -> list[tuple[float, float]]:
        return [(1e-12, None), (0, 1), (0, 1)]  # type: ignore[list-item]

    @property
    def num_params(self) -> int:
        return 3


@pytest.fixture
def garch_data(rng: np.random.Generator) -> np.ndarray:
    """Simulate GARCH(1,1) data for testing."""
    n = 1000
    omega, alpha, beta = 1e-5, 0.08, 0.90
    sigma2 = np.empty(n)
    returns = np.empty(n)
    sigma2[0] = omega / (1 - alpha - beta)
    returns[0] = np.sqrt(sigma2[0]) * rng.standard_normal()
    for t in range(1, n):
        sigma2[t] = omega + alpha * returns[t - 1] ** 2 + beta * sigma2[t - 1]
        returns[t] = np.sqrt(sigma2[t]) * rng.standard_normal()
    return returns


class TestMLEstimator:
    """Test MLE estimation."""

    def test_convergence(self, garch_data: np.ndarray) -> None:
        """Optimization should converge."""
        model = SimpleGARCH(garch_data, mean="zero")
        estimator = MLEstimator()
        results = estimator.fit(model, disp=False)
        assert results.convergence

    def test_params_reasonable(self, garch_data: np.ndarray) -> None:
        """Estimated parameters should be in reasonable range."""
        model = SimpleGARCH(garch_data, mean="zero")
        estimator = MLEstimator()
        results = estimator.fit(model, disp=False)

        omega, alpha, beta = results.params
        assert omega > 0
        assert 0 < alpha < 1
        assert 0 < beta < 1
        assert alpha + beta < 1

    def test_se_positive(self, garch_data: np.ndarray) -> None:
        """Standard errors should be positive."""
        model = SimpleGARCH(garch_data, mean="zero")
        estimator = MLEstimator()
        results = estimator.fit(model, disp=False)

        assert np.all(results.se_robust > 0)
        assert np.all(results.se_nonrobust > 0)

    def test_loglike_finite(self, garch_data: np.ndarray) -> None:
        """Log-likelihood should be finite."""
        model = SimpleGARCH(garch_data, mean="zero")
        estimator = MLEstimator()
        results = estimator.fit(model, disp=False)

        assert np.isfinite(results.loglike)

    def test_variance_targeting(self, garch_data: np.ndarray) -> None:
        """Variance targeting should produce valid results."""
        model = SimpleGARCH(garch_data, mean="zero")
        estimator = MLEstimator()
        results = estimator.fit(model, variance_targeting=True, disp=False)

        assert results.convergence
        omega, alpha, beta = results.params
        assert omega > 0
        assert alpha + beta < 1

        # omega should be consistent with variance targeting
        sample_var = np.var(garch_data)
        expected_omega = sample_var * (1 - alpha - beta)
        assert abs(omega - expected_omega) / expected_omega < 0.01

    def test_sigma2_shape(self, garch_data: np.ndarray) -> None:
        """Conditional variance should have correct shape."""
        model = SimpleGARCH(garch_data, mean="zero")
        estimator = MLEstimator()
        results = estimator.fit(model, disp=False)

        assert results.conditional_volatility.shape == (len(garch_data),)
        assert np.all(results.conditional_volatility > 0)
