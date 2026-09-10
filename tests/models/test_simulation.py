"""Tests for VolatilityModel.simulate across every univariate model.

The simulation is a single O(n) forward pass: sigma^2_t must depend on the
shock drawn at t-1 (never on the shock drawn at t), and the recursion must be
the model's own. Each test below re-derives sigma^2_t from the returned path
with the model's formula and asserts an exact match.
"""

from __future__ import annotations

import numpy as np
import pytest

from archbox.core.volatility_model import SimulationResult
from archbox.models.aparch import APARCH
from archbox.models.component_garch import ComponentGARCH
from archbox.models.egarch import EGARCH
from archbox.models.figarch import FIGARCH
from archbox.models.garch import GARCH
from archbox.models.garch_m import GARCHM
from archbox.models.gjr_garch import GJRGARCH
from archbox.models.igarch import IGARCH

N_SIM = 400


@pytest.fixture
def series(rng: np.random.Generator) -> np.ndarray:
    """Short synthetic return series used to construct the models."""
    return rng.standard_normal(500) * 0.01


class TestSimulateRecursion:
    """Each model's simulated variance follows its own recursion exactly."""

    def test_garch(self, series: np.ndarray) -> None:
        model = GARCH(series, p=1, q=1, mean="zero")
        params = np.array([1e-6, 0.08, 0.90])
        rets, var = model.simulate(N_SIM, params, seed=1)

        expected = params[0] + params[1] * rets[:-1] ** 2 + params[2] * var[:-1]
        np.testing.assert_allclose(var[1:], expected, rtol=1e-12)

    def test_gjr(self, series: np.ndarray) -> None:
        model = GJRGARCH(series, p=1, q=1, mean="zero")
        omega, alpha, gamma, beta = 1e-6, 0.04, 0.06, 0.90
        rets, var = model.simulate(N_SIM, np.array([omega, alpha, gamma, beta]), seed=2)

        indicator = (rets[:-1] < 0).astype(float)
        expected = omega + (alpha + gamma * indicator) * rets[:-1] ** 2 + beta * var[:-1]
        np.testing.assert_allclose(var[1:], expected, rtol=1e-12)

    def test_egarch(self, series: np.ndarray) -> None:
        model = EGARCH(series, p=1, q=1, mean="zero")
        omega, alpha, gamma, beta = -0.1, 0.12, -0.05, 0.98
        rets, var = model.simulate(N_SIM, np.array([omega, alpha, gamma, beta]), seed=3)

        z = rets[:-1] / np.sqrt(var[:-1])
        expected = np.exp(
            omega + beta * np.log(var[:-1]) + alpha * (np.abs(z) - np.sqrt(2.0 / np.pi)) + gamma * z
        )
        np.testing.assert_allclose(var[1:], expected, rtol=1e-10)

    def test_aparch(self, series: np.ndarray) -> None:
        model = APARCH(series, p=1, q=1, mean="zero")
        omega, alpha, gamma, beta, delta = 1e-5, 0.06, 0.3, 0.90, 1.5
        rets, var = model.simulate(N_SIM, np.array([omega, alpha, gamma, beta, delta]), seed=4)

        shock = np.maximum(np.abs(rets[:-1]) - gamma * rets[:-1], 0.0) ** delta
        sigma_delta = omega + alpha * shock + beta * var[:-1] ** (delta / 2.0)
        np.testing.assert_allclose(var[1:], sigma_delta ** (2.0 / delta), rtol=1e-10)

    def test_igarch(self, series: np.ndarray) -> None:
        model = IGARCH(series, mean="zero")
        omega, alpha = 1e-6, 0.06
        rets, var = model.simulate(N_SIM, np.array([omega, alpha]), seed=5)

        expected = omega + alpha * rets[:-1] ** 2 + (1.0 - alpha) * var[:-1]
        np.testing.assert_allclose(var[1:], expected, rtol=1e-12)

    def test_figarch(self, series: np.ndarray) -> None:
        model = FIGARCH(series, truncation_lag=50, mean="zero")
        omega, phi, d, beta = 1e-6, 0.2, 0.4, 0.3
        rets, var = model.simulate(N_SIM, np.array([omega, phi, d, beta]), seed=6)

        lam = model._compute_lambda_coefficients(phi, d, beta, 50)
        omega_star = omega / (1.0 - beta)
        for t in (1, 5, 60, N_SIM - 1):
            n_used = min(t, 50)
            past = rets[t - n_used : t][::-1] ** 2
            expected = omega_star + float(np.dot(lam[:n_used], past))
            assert var[t] == pytest.approx(expected, rel=1e-12)

    def test_component_garch(self, series: np.ndarray) -> None:
        model = ComponentGARCH(series, mean="zero")
        omega, alpha, beta, alpha_p, beta_p = 1e-4, 0.05, 0.10, 0.04, 0.98
        rets, var = model.simulate(N_SIM, np.array([omega, alpha, beta, alpha_p, beta_p]), seed=7)

        # Re-run the permanent/transitory recursion on the simulated shocks.
        q_prev, h_prev = var[0], 0.0
        for t in range(1, N_SIM):
            eps2 = rets[t - 1] ** 2
            q_next = max(omega + beta_p * (q_prev - omega) + alpha_p * (eps2 - var[t - 1]), 1e-12)
            h_next = alpha * (eps2 - q_prev) + beta * h_prev
            assert var[t] == pytest.approx(max(q_next + h_next, 1e-12), rel=1e-12)
            q_prev, h_prev = q_next, h_next

    def test_garch_m(self, series: np.ndarray) -> None:
        model = GARCHM(series, p=1, q=1, risk_premium="variance", mean="zero")
        omega, alpha, beta, lam = 1e-6, 0.08, 0.90, 3.0
        rets, var = model.simulate(N_SIM, np.array([omega, alpha, beta, lam]), seed=8)

        # The return carries the risk premium; the variance recursion is driven
        # by the shock, i.e. by the return net of the premium.
        eps = rets - lam * var
        expected = omega + alpha * eps[:-1] ** 2 + beta * var[:-1]
        np.testing.assert_allclose(var[1:], expected, rtol=1e-10)
        assert not np.allclose(rets, eps), "lambda != 0 must shift the simulated returns"


class TestSimulateGeneral:
    """Behaviour shared by every model."""

    def test_result_is_a_named_tuple(self, series: np.ndarray) -> None:
        model = GARCH(series, p=1, q=1, mean="zero")
        result = model.simulate(50, np.array([1e-6, 0.08, 0.90]), seed=9)

        assert isinstance(result, SimulationResult)
        returns, variance = result  # backward-compatible 2-tuple unpacking
        np.testing.assert_allclose(result.returns, returns)
        np.testing.assert_allclose(result.variance, variance)
        np.testing.assert_allclose(result.volatility, np.sqrt(variance))

    def test_seed_is_reproducible(self, series: np.ndarray) -> None:
        model = GARCH(series, p=1, q=1, mean="zero")
        params = np.array([1e-6, 0.08, 0.90])
        first = model.simulate(100, params, seed=42)
        second = model.simulate(100, params, seed=42)
        third = model.simulate(100, params, seed=43)

        np.testing.assert_allclose(first.returns, second.returns)
        assert not np.allclose(first.returns, third.returns)

    def test_invalid_n_raises(self, series: np.ndarray) -> None:
        model = GARCH(series, p=1, q=1, mean="zero")
        with pytest.raises(ValueError):
            model.simulate(0, np.array([1e-6, 0.08, 0.90]))

    def test_uses_model_distribution(self, series: np.ndarray) -> None:
        """Innovations come from the fitted distribution, not always N(0,1)."""
        params = np.array([1e-6, 0.08, 0.90, 3.0])  # last entry is nu

        model_t = GARCH(series, p=1, q=1, mean="zero", dist="studentt")
        rets_t, var_t = model_t.simulate(20000, params, seed=11)
        z_t = rets_t / np.sqrt(var_t)

        model_n = GARCH(series, p=1, q=1, mean="zero", dist="normal")
        rets_n, var_n = model_n.simulate(20000, params[:3], seed=11)
        z_n = rets_n / np.sqrt(var_n)

        kurt_t = float(np.mean(z_t**4) / np.mean(z_t**2) ** 2)
        kurt_n = float(np.mean(z_n**4) / np.mean(z_n**2) ** 2)
        assert kurt_t > kurt_n + 2.0, f"t innovations should be fat-tailed: {kurt_t} vs {kurt_n}"

    def test_starts_at_unconditional_variance(self, series: np.ndarray) -> None:
        model = GARCH(series, p=1, q=1, mean="zero")
        params = np.array([1e-6, 0.08, 0.90])
        _, var = model.simulate(10, params, seed=12)
        assert var[0] == pytest.approx(model.unconditional_variance(params), rel=1e-12)

    def test_mean_variance_near_unconditional(self, series: np.ndarray) -> None:
        """A long simulation reproduces the model's unconditional variance."""
        model = GARCH(series, p=1, q=1, mean="zero")
        params = np.array([1e-5, 0.05, 0.85])  # moderate persistence: stable moments
        rets, var = model.simulate(50000, params, seed=13)
        uncond = model.unconditional_variance(params)
        assert abs(float(np.var(rets)) - uncond) / uncond < 0.2
        assert abs(float(np.mean(var)) - uncond) / uncond < 0.2
