"""Cross-model tests for the VolatilityModel moments/forecast API.

Every univariate model must expose ``persistence``, ``unconditional_variance``,
``conditional_variance`` and ``forecast_variance`` at the model level, and
``ArchResults`` must delegate to them instead of assuming a GARCH(1,1) layout.
"""

from __future__ import annotations

import numpy as np
import pytest

from archbox import APARCH, EGARCH, FIGARCH, GARCH, GARCHM, GJRGARCH, IGARCH, ComponentGARCH
from archbox.datasets import load_dataset


@pytest.fixture(scope="module")
def returns() -> np.ndarray:
    """SP500 returns on their natural ~0.01 scale."""
    return load_dataset("sp500")["returns"].to_numpy(dtype=np.float64)


def _build(name: str, data: np.ndarray) -> object:
    """Instantiate a model by name with test-friendly settings."""
    builders = {
        "GARCH": lambda: GARCH(data),
        "EGARCH": lambda: EGARCH(data),
        "GJRGARCH": lambda: GJRGARCH(data),
        "APARCH": lambda: APARCH(data),
        # A short truncation keeps the O(T*K) FIGARCH recursion fast in tests.
        "FIGARCH": lambda: FIGARCH(data, truncation_lag=50),
        "IGARCH": lambda: IGARCH(data),
        "GARCHM": lambda: GARCHM(data),
        "ComponentGARCH": lambda: ComponentGARCH(data),
    }
    return builders[name]()


ALL_MODELS = [
    "GARCH",
    "EGARCH",
    "GJRGARCH",
    "APARCH",
    "FIGARCH",
    "IGARCH",
    "GARCHM",
    "ComponentGARCH",
]


@pytest.fixture(scope="module")
def fitted(returns: np.ndarray) -> dict[str, object]:
    """Fit every univariate model once for the whole module."""
    out: dict[str, object] = {}
    for name in ALL_MODELS:
        model = _build(name, returns)
        out[name] = model.fit(disp=False)  # type: ignore[attr-defined]
    return out


@pytest.mark.parametrize("name", ALL_MODELS)
def test_forecast_positive_and_finite(name: str, fitted: dict[str, object]) -> None:
    """Every model must forecast strictly positive, finite variances."""
    results = fitted[name]
    fc = results.forecast(horizon=10)  # type: ignore[attr-defined]
    variance = fc["variance"]
    assert variance.shape == (10,)
    assert np.all(np.isfinite(variance)), f"{name} produced non-finite forecasts"
    assert np.all(variance > 0), f"{name} produced non-positive forecasts: {variance}"
    assert np.all(fc["volatility"] > 0)


@pytest.mark.parametrize("name", ALL_MODELS)
def test_one_step_forecast_same_order_as_last_sigma2(name: str, fitted: dict[str, object]) -> None:
    """The 1-step forecast must sit on the same scale as the last fitted sigma^2."""
    results = fitted[name]
    fc = results.forecast(horizon=1)["variance"][0]  # type: ignore[attr-defined]
    last = float(results._sigma2[-1])  # type: ignore[attr-defined]
    assert 0.1 * last < fc < 10.0 * last, f"{name}: 1-step {fc:.3e} vs last sigma2 {last:.3e}"


@pytest.mark.parametrize("name", ALL_MODELS)
def test_persistence_finite_and_positive(name: str, fitted: dict[str, object]) -> None:
    """Persistence must be a finite positive number for every model."""
    pers = results_persistence = fitted[name].persistence()  # type: ignore[attr-defined]
    assert np.isfinite(pers), f"{name} persistence not finite: {results_persistence}"
    assert pers > 0


@pytest.mark.parametrize("name", ALL_MODELS)
def test_conditional_variance_matches_fitted_path(name: str, fitted: dict[str, object]) -> None:
    """``model.conditional_variance`` reproduces the sigma^2 stored on the results."""
    results = fitted[name]
    model = results._model  # type: ignore[attr-defined]
    sigma2 = model.conditional_variance(results.params)  # type: ignore[attr-defined]
    assert sigma2.shape == results._sigma2.shape  # type: ignore[attr-defined]
    assert np.all(sigma2 > 0)
    np.testing.assert_allclose(sigma2, results._sigma2, rtol=1e-10)  # type: ignore[attr-defined]


@pytest.mark.parametrize("name", ALL_MODELS)
def test_resid_is_raw_and_std_resid_is_standardized(
    name: str, fitted: dict[str, object], returns: np.ndarray
) -> None:
    """``resid`` is on the return scale; ``std_resid`` has unit-ish variance."""
    results = fitted[name]
    resid = results.resid  # type: ignore[attr-defined]
    std_resid = results.std_resid  # type: ignore[attr-defined]

    assert abs(resid.std() - returns.std()) / returns.std() < 0.05
    assert 0.8 < std_resid.std() < 1.2
    # The two series differ by orders of magnitude on 0.01-scale returns.
    assert std_resid.std() > 10.0 * resid.std()


@pytest.mark.parametrize("name", ALL_MODELS)
def test_forecast_rejects_non_positive_horizon(name: str, fitted: dict[str, object]) -> None:
    """A zero or negative horizon is a ValueError, not a silent empty forecast."""
    with pytest.raises(ValueError, match="horizon"):
        fitted[name].forecast(horizon=0)  # type: ignore[attr-defined]


class TestGJRPersistence:
    """GJR-GARCH persistence uses the leverage-adjusted formula."""

    def test_formula(self, fitted: dict[str, object]) -> None:
        """persistence == sum(alpha) + sum(gamma)/2 + sum(beta)."""
        results = fitted["GJRGARCH"]
        named = dict(zip(results.param_names, results.params, strict=True))  # type: ignore[attr-defined]
        expected = named["alpha[1]"] + 0.5 * named["gamma[1]"] + named["beta[1]"]
        assert abs(results.persistence() - expected) < 1e-12  # type: ignore[attr-defined]

    def test_below_one_on_sp500(self, fitted: dict[str, object]) -> None:
        """The naive sum(params[1:]) gave 1.0014 on sp500; the correct one is < 1."""
        assert fitted["GJRGARCH"].persistence() < 1.0  # type: ignore[attr-defined]

    def test_half_life_finite(self, fitted: dict[str, object]) -> None:
        """A stationary GJR fit must have a finite, positive half-life."""
        hl = fitted["GJRGARCH"].half_life()  # type: ignore[attr-defined]
        assert np.isfinite(hl)
        assert hl > 0

    def test_unconditional_variance_positive(self, fitted: dict[str, object]) -> None:
        """omega / (1 - persistence) is finite and positive on sp500."""
        uv = fitted["GJRGARCH"].unconditional_variance()  # type: ignore[attr-defined]
        assert np.isfinite(uv)
        assert uv > 0

    def test_summary_reports_finite_persistence(self, fitted: dict[str, object]) -> None:
        """summary() must not print inf for a stationary GJR fit."""
        summary = fitted["GJRGARCH"].summary()  # type: ignore[attr-defined]
        assert "inf" not in summary
        assert "Persistence" in summary


class TestEGARCHMoments:
    """EGARCH persistence and forecasts."""

    def test_persistence_is_sum_of_betas(self, fitted: dict[str, object]) -> None:
        """EGARCH persistence lives on the log-variance: it is sum(beta)."""
        results = fitted["EGARCH"]
        named = dict(zip(results.param_names, results.params, strict=True))  # type: ignore[attr-defined]
        assert abs(results.persistence() - named["beta[1]"]) < 1e-12  # type: ignore[attr-defined]

    def test_forecast_strictly_positive(self, fitted: dict[str, object]) -> None:
        """The GARCH-layout forecast used to make EGARCH variance go negative."""
        variance = fitted["EGARCH"].forecast(horizon=25)["variance"]  # type: ignore[attr-defined]
        assert np.all(variance > 0)
        assert np.all(np.isfinite(variance))

    def test_forecast_is_deterministic(self, fitted: dict[str, object]) -> None:
        """The Monte-Carlo forecast uses a fixed seed, so repeated calls agree."""
        results = fitted["EGARCH"]
        first = results.forecast(horizon=8)["variance"]  # type: ignore[attr-defined]
        second = results.forecast(horizon=8)["variance"]  # type: ignore[attr-defined]
        np.testing.assert_array_equal(first, second)


class TestAPARCHMoments:
    """APARCH persistence must not fold delta into the sum."""

    def test_persistence_excludes_delta(self, fitted: dict[str, object]) -> None:
        """persistence = sum_i alpha_i E[(|z|-gamma_i z)^delta] + sum(beta)."""
        results = fitted["APARCH"]
        named = dict(zip(results.param_names, results.params, strict=True))  # type: ignore[attr-defined]
        naive = sum(v for k, v in named.items() if k != "omega")
        pers = results.persistence()  # type: ignore[attr-defined]
        assert pers < 1.0
        assert abs(pers - naive) > 1.0, "delta must not be summed into persistence"

    def test_forecast_is_deterministic(self, fitted: dict[str, object]) -> None:
        """Fixed-seed Monte-Carlo means repeated forecasts are identical."""
        results = fitted["APARCH"]
        first = results.forecast(horizon=8)["variance"]  # type: ignore[attr-defined]
        second = results.forecast(horizon=8)["variance"]  # type: ignore[attr-defined]
        np.testing.assert_array_equal(first, second)


class TestIGARCHMoments:
    """IGARCH is integrated: persistence 1, infinite long-run variance."""

    def test_persistence_exactly_one(self, fitted: dict[str, object]) -> None:
        assert fitted["IGARCH"].persistence() == 1.0  # type: ignore[attr-defined]

    def test_unconditional_variance_infinite(self, fitted: dict[str, object]) -> None:
        assert fitted["IGARCH"].unconditional_variance() == float("inf")  # type: ignore[attr-defined]

    def test_half_life_infinite(self, fitted: dict[str, object]) -> None:
        assert fitted["IGARCH"].half_life() == float("inf")  # type: ignore[attr-defined]

    def test_forecast_drifts_up_by_omega(self, fitted: dict[str, object]) -> None:
        """sigma^2_{T+h} = omega*(h-1) + sigma^2_{T+1}; the old code returned 0.0."""
        results = fitted["IGARCH"]
        omega = float(results.params[0])  # type: ignore[attr-defined]
        variance = results.forecast(horizon=6)["variance"]  # type: ignore[attr-defined]
        assert np.all(variance > 0)
        np.testing.assert_allclose(np.diff(variance), omega, rtol=1e-10)


class TestMeanRevertingForecasts:
    """Stationary models converge to their unconditional variance."""

    @pytest.mark.parametrize("name", ["GARCH", "GJRGARCH", "GARCHM", "ComponentGARCH"])
    def test_converges_to_unconditional(self, name: str, fitted: dict[str, object]) -> None:
        results = fitted[name]
        uv = results.unconditional_variance()  # type: ignore[attr-defined]
        assert np.isfinite(uv) and uv > 0
        variance = results.forecast(horizon=4000)["variance"]  # type: ignore[attr-defined]
        assert abs(variance[-1] - uv) / uv < 0.05
