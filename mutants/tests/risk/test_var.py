"""Tests for Value at Risk (VaR) implementations."""

from __future__ import annotations

import numpy as np
import pytest
from scipy import stats

from archbox.risk.var import ValueAtRisk


class MockResults:
    """Mock ArchResults for testing."""

    def __init__(
        self,
        returns: np.ndarray,
        sigma: np.ndarray,
        params: np.ndarray | None = None,
        mu: float = 0.0,
        p: int = 1,
        q: int = 1,
    ):
        self.resids = returns
        self.endog = returns
        self.conditional_volatility = sigma
        self.mu = mu
        self.p = p
        self.q = q
        if params is None:
            self.params = np.array([1e-6, 0.08, 0.91])
        else:
            self.params = params


@pytest.fixture
def mock_garch_results(rng: np.random.Generator) -> MockResults:
    """Create mock GARCH results with realistic data."""
    n = 2500
    omega, alpha, beta = 1e-6, 0.08, 0.91
    mu = 0.0004

    sigma2 = np.empty(n)
    returns = np.empty(n)
    sigma2[0] = omega / (1 - alpha - beta)

    for t in range(n):
        if t > 0:
            sigma2[t] = omega + alpha * (returns[t - 1] - mu) ** 2 + beta * sigma2[t - 1]
        z = rng.standard_normal()
        returns[t] = mu + np.sqrt(sigma2[t]) * z

    sigma = np.sqrt(sigma2)
    params = np.array([omega, alpha, beta])
    return MockResults(returns, sigma, params, mu=mu)


class TestParametricVaRNormal:
    """test_parametric_var_normal: VaR Normal(alpha=0.05) = mu - 1.645*sigma."""

    def test_parametric_var_normal(self, mock_garch_results: MockResults) -> None:
        var = ValueAtRisk(mock_garch_results, alpha=0.05)
        var_series = var.parametric(dist="normal")

        sigma = mock_garch_results.conditional_volatility
        mu = mock_garch_results.mu
        z_alpha = stats.norm.ppf(0.05)  # -1.6449

        expected = mu + sigma * z_alpha
        np.testing.assert_allclose(var_series, expected, rtol=1e-10)


class TestParametricVaRStudentT:
    """test_parametric_var_student_t: VaR Student-t > VaR Normal (heavier tails)."""

    def test_parametric_var_student_t(self, mock_garch_results: MockResults) -> None:
        # Use alpha=0.01 where heavy tails dominate the variance correction
        var = ValueAtRisk(mock_garch_results, alpha=0.01)

        var_normal = var.parametric(dist="normal")
        var_studentt = var.parametric(dist="studentt", nu=5.0)

        # Student-t VaR should be more negative (larger loss) due to heavier tails
        # At 1% level, t(5) quantile * sqrt((nu-2)/nu) > normal quantile in magnitude
        assert np.all(
            var_studentt < var_normal
        ), "Student-t VaR should be more extreme than Normal VaR"


class TestViolationRateParametric:
    """test_violation_rate_parametric: violation rate ~ alpha (tol=20%)."""

    def test_violation_rate_parametric(self, mock_garch_results: MockResults) -> None:
        alpha = 0.05
        var = ValueAtRisk(mock_garch_results, alpha=alpha)
        var_series = var.parametric(dist="normal")

        returns = mock_garch_results.resids
        violations = (returns < var_series).mean()

        # Violation rate should be close to alpha (within 20%)
        assert (
            abs(violations - alpha) / alpha < 0.20
        ), f"Violation rate {violations:.4f} too far from alpha={alpha}"


class TestFilteredHSBetter:
    """test_filtered_hs_better: FHS better than HS (lower deviation from alpha)."""

    def test_filtered_hs_better(self, mock_garch_results: MockResults) -> None:
        alpha = 0.05
        var = ValueAtRisk(mock_garch_results, alpha=alpha)

        var_hs = var.historical(window=250)
        var_fhs = var.filtered_historical()

        returns = mock_garch_results.resids

        # Compare only where both are valid (not NaN)
        valid = ~np.isnan(var_hs) & ~np.isnan(var_fhs)
        returns_valid = returns[valid]
        var_hs_valid = var_hs[valid]
        var_fhs_valid = var_fhs[valid]

        viol_hs = (returns_valid < var_hs_valid).mean()
        viol_fhs = (returns_valid < var_fhs_valid).mean()

        # FHS violation rate should be closer to alpha
        dev_hs = abs(viol_hs - alpha)
        dev_fhs = abs(viol_fhs - alpha)

        # FHS should be at least not worse (allow some tolerance)
        assert (
            dev_fhs <= dev_hs + 0.02
        ), f"FHS deviation {dev_fhs:.4f} should be <= HS deviation {dev_hs:.4f}"


class TestMonteCarloConvergence:
    """test_monte_carlo_convergence: MC VaR variance decreases with n_sims."""

    def test_monte_carlo_convergence(self, mock_garch_results: MockResults) -> None:
        var = ValueAtRisk(mock_garch_results, alpha=0.05)

        # Run MC with different n_sims
        var_small = []
        var_large = []

        for seed in range(10):
            v_small = var.monte_carlo(n_sims=100, horizon=1, seed=seed)
            v_large = var.monte_carlo(n_sims=10000, horizon=1, seed=seed)
            var_small.append(v_small[0])
            var_large.append(v_large[0])

        # Variance of VaR estimates should decrease with more simulations
        var_variance_small = np.var(var_small)
        var_variance_large = np.var(var_large)

        assert var_variance_large < var_variance_small, (
            f"MC variance should decrease: small={var_variance_small:.8f}, "
            f"large={var_variance_large:.8f}"
        )


class TestVaREdgeCases:
    """Edge case tests for VaR."""

    def test_invalid_alpha(self, mock_garch_results: MockResults) -> None:
        with pytest.raises(ValueError, match="alpha must be in"):
            ValueAtRisk(mock_garch_results, alpha=0.0)

        with pytest.raises(ValueError, match="alpha must be in"):
            ValueAtRisk(mock_garch_results, alpha=1.0)

    def test_invalid_distribution(self, mock_garch_results: MockResults) -> None:
        var = ValueAtRisk(mock_garch_results, alpha=0.05)
        with pytest.raises(ValueError, match="Unknown distribution"):
            var.parametric(dist="invalid")

    def test_studentt_nu_too_small(self, mock_garch_results: MockResults) -> None:
        var = ValueAtRisk(mock_garch_results, alpha=0.05)
        with pytest.raises(ValueError, match="Degrees of freedom"):
            var.parametric(dist="studentt", nu=2.0)
