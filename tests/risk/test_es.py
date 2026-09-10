"""Tests for Expected Shortfall (ES) implementations."""

from __future__ import annotations

import numpy as np
import pytest
from scipy import stats

from archbox.risk.es import ExpectedShortfall
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


class TestESGreaterThanVaR:
    """test_es_greater_than_var: ES > VaR always (in absolute loss)."""

    def test_es_greater_than_var_normal(self, mock_garch_results: MockResults) -> None:
        alpha = 0.05
        var = ValueAtRisk(mock_garch_results, alpha=alpha)
        es = ExpectedShortfall(mock_garch_results, alpha=alpha)

        var_series = var.parametric(dist="normal")
        es_series = es.parametric(dist="normal")

        # ES should always be more negative (larger loss) than VaR
        assert np.all(es_series <= var_series), (
            "ES must always be <= VaR (more negative, larger expected loss)"
        )

    def test_es_greater_than_var_studentt(self, mock_garch_results: MockResults) -> None:
        alpha = 0.05
        var = ValueAtRisk(mock_garch_results, alpha=alpha)
        es = ExpectedShortfall(mock_garch_results, alpha=alpha)

        var_series = var.parametric(dist="studentt", nu=5.0)
        es_series = es.parametric(dist="studentt", nu=5.0)

        assert np.all(es_series <= var_series), "ES must always be <= VaR for Student-t"


class TestESNormalFormula:
    """test_es_normal_formula: ES Normal matches analytical formula."""

    def test_es_normal_formula(self, mock_garch_results: MockResults) -> None:
        alpha = 0.05
        es = ExpectedShortfall(mock_garch_results, alpha=alpha)
        es_series = es.parametric(dist="normal")

        # Analytical formula: ES = mu - sigma * phi(z_alpha) / alpha
        sigma = mock_garch_results.conditional_volatility
        mu = mock_garch_results.mu
        z_alpha = stats.norm.ppf(alpha)
        phi_z = stats.norm.pdf(z_alpha)
        expected = mu - sigma * phi_z / alpha

        np.testing.assert_allclose(es_series, expected, rtol=1e-10)


class TestESStudentTFormula:
    """test_es_student_t_formula: ES Student-t matches analytical formula."""

    def test_es_student_t_formula(self, mock_garch_results: MockResults) -> None:
        alpha = 0.05
        nu = 6.0
        es = ExpectedShortfall(mock_garch_results, alpha=alpha)
        es_series = es.parametric(dist="studentt", nu=nu)

        # Analytical formula
        sigma = mock_garch_results.conditional_volatility
        mu = mock_garch_results.mu
        t_alpha = stats.t.ppf(alpha, df=nu)
        f_nu = stats.t.pdf(t_alpha, df=nu)
        scale = np.sqrt((nu - 2) / nu)
        es_factor = (f_nu / alpha) * ((nu + t_alpha**2) / (nu - 1))
        expected = mu - sigma * es_factor * scale

        np.testing.assert_allclose(es_series, expected, rtol=1e-10)


class TestESHistorical:
    """Tests for historical ES."""

    def test_es_historical_less_than_var(self, mock_garch_results: MockResults) -> None:
        alpha = 0.05
        var = ValueAtRisk(mock_garch_results, alpha=alpha)
        es = ExpectedShortfall(mock_garch_results, alpha=alpha)

        var_hs = var.historical(window=250)
        es_hs = es.historical(window=250)

        valid = ~np.isnan(var_hs) & ~np.isnan(es_hs)
        assert np.all(es_hs[valid] <= var_hs[valid]), "Historical ES must be <= Historical VaR"


class TestESFilteredHS:
    """Tests for Filtered Historical Simulation ES."""

    def test_es_fhs_less_than_var(self, mock_garch_results: MockResults) -> None:
        alpha = 0.05
        var = ValueAtRisk(mock_garch_results, alpha=alpha)
        es = ExpectedShortfall(mock_garch_results, alpha=alpha)

        var_fhs = var.filtered_historical()
        es_fhs = es.filtered_historical()

        valid = ~np.isnan(var_fhs) & ~np.isnan(es_fhs)
        assert np.all(es_fhs[valid] <= var_fhs[valid] + 1e-12), "FHS ES must be <= FHS VaR"


class TestESEdgeCases:
    """Edge case tests for ES."""

    def test_invalid_alpha(self, mock_garch_results: MockResults) -> None:
        with pytest.raises(ValueError, match="alpha must be in"):
            ExpectedShortfall(mock_garch_results, alpha=0.0)

    def test_invalid_distribution(self, mock_garch_results: MockResults) -> None:
        es = ExpectedShortfall(mock_garch_results, alpha=0.05)
        with pytest.raises(ValueError, match="Unknown distribution"):
            es.parametric(dist="invalid")

    def test_studentt_nu_too_small(self, mock_garch_results: MockResults) -> None:
        es = ExpectedShortfall(mock_garch_results, alpha=0.05)
        with pytest.raises(ValueError, match="Degrees of freedom"):
            es.parametric(dist="studentt", nu=2.0)
