"""Tests for MLEstimator."""

from __future__ import annotations

import numpy as np
import pytest

from archbox.core.volatility_model import VolatilityModel
from archbox.estimation.mle import MLEstimator
from archbox.models.aparch import APARCH
from archbox.models.component_garch import ComponentGARCH
from archbox.models.egarch import EGARCH
from archbox.models.figarch import FIGARCH
from archbox.models.garch import GARCH
from archbox.models.garch_m import GARCHM
from archbox.models.gjr_garch import GJRGARCH
from archbox.models.igarch import IGARCH


class SimpleGARCH(VolatilityModel):
    """Simple GARCH(1,1) for testing the estimator."""

    volatility_process = "GARCH"
    # Plain [omega, alpha, beta] layout, so targeting is meaningful here.
    supports_variance_targeting = True

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


class TestBoundsAreHonoured:
    """The declared bounds() must constrain the fitted parameters."""

    def test_fd_step_does_not_collapse_at_zero(self) -> None:
        from archbox.estimation.mle import _fd_step

        assert _fd_step(0.0) == pytest.approx(1e-8)
        assert _fd_step(1e-12) == pytest.approx(1e-8)
        assert _fd_step(2.0) == pytest.approx(2e-5)

    def test_projection_clips_to_declared_bounds(self) -> None:
        estimator = MLEstimator()
        params = np.array([-1.0, 50.0, 0.5])
        bounds = [(0.0, 1.0), (2.01, 10.0), (-np.inf, np.inf)]
        projected = estimator._project(params, bounds)
        np.testing.assert_allclose(projected, [0.0, 10.0, 0.5])

    def test_projection_ignores_mismatched_bounds(self) -> None:
        estimator = MLEstimator()
        params = np.array([-1.0, 50.0])
        np.testing.assert_allclose(estimator._project(params, [(0.0, 1.0)]), params)

    @pytest.mark.parametrize(
        ("cls", "kwargs"),
        [
            (APARCH, {"p": 1, "q": 1}),
            (GJRGARCH, {"p": 1, "q": 1}),
            (GARCHM, {"p": 1, "q": 1}),
            (ComponentGARCH, {}),
            (GARCH, {"p": 1, "q": 1, "dist": "studentt"}),
            (GARCH, {"p": 1, "q": 1, "dist": "skewt"}),
            (GARCH, {"p": 1, "q": 1, "dist": "ged"}),
            (GARCH, {"p": 1, "q": 1, "dist": "mixture-normal"}),
        ],
    )
    def test_fitted_params_inside_bounds(
        self, garch_data: np.ndarray, cls: type, kwargs: dict
    ) -> None:
        model = cls(garch_data, **kwargs)
        results = model.fit(disp=False)
        for name, value, (lo, hi) in zip(
            results.param_names, results.params, model.full_bounds(), strict=True
        ):
            assert lo <= value <= hi, f"{name}={value} outside [{lo}, {hi}]"

    def test_aparch_delta_inside_bounds(self, garch_data: np.ndarray) -> None:
        model = APARCH(garch_data, p=1, q=1)
        results = model.fit(disp=False)
        delta = dict(zip(results.param_names, results.params, strict=True))["delta"]
        assert 0.01 <= delta <= 10.0


class TestVarianceTargetingOptIn:
    """Variance targeting is only valid for the plain GARCH layout."""

    def test_garch_supports_targeting(self, garch_data: np.ndarray) -> None:
        assert GARCH.supports_variance_targeting is True
        results = GARCH(garch_data, p=1, q=1, mean="zero").fit(variance_targeting=True, disp=False)
        assert results.params[0] > 0

    @pytest.mark.parametrize(
        ("cls", "kwargs"),
        [
            (GJRGARCH, {}),
            (EGARCH, {}),
            (APARCH, {}),
            (ComponentGARCH, {}),
            (GARCHM, {}),
            (IGARCH, {}),
            (FIGARCH, {"truncation_lag": 50}),
        ],
    )
    def test_targeting_raises_for_other_layouts(
        self, garch_data: np.ndarray, cls: type, kwargs: dict
    ) -> None:
        model = cls(garch_data, **kwargs)
        with pytest.raises(ValueError, match="[Vv]ariance targeting"):
            model.fit(variance_targeting=True, disp=False)

    def test_targeting_fallback_keeps_omega_positive(
        self, garch_data: np.ndarray, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """An infeasible optimizer endpoint is rescaled, never emitted as omega <= 0."""
        from archbox.core.exceptions import ConvergenceWarning
        from archbox.estimation import mle as mle_module

        class _FakeResult:
            # persistence = exp(0) + exp(0) = 2 > 1 => infeasible
            x = np.array([0.0, 0.0])
            fun = -1.0
            success = True
            message = "fake"

        monkeypatch.setattr(mle_module.optimize, "minimize", lambda *args, **kwargs: _FakeResult())

        model = SimpleGARCH(garch_data, mean="zero")
        with pytest.warns(ConvergenceWarning):
            results = MLEstimator().fit(model, variance_targeting=True, disp=False)

        assert results.params[0] > 0
        assert results.convergence is False


class TestConvergenceAndStandardErrors:
    """Failures must be visible, and unreliable standard errors must be NaN."""

    def test_non_convergence_warns_and_flags(self, garch_data: np.ndarray) -> None:
        from archbox.core.exceptions import ConvergenceWarning

        model = SimpleGARCH(garch_data, mean="zero")
        with pytest.warns(ConvergenceWarning):
            results = MLEstimator().fit(model, maxiter=1, disp=False)
        assert results.convergence is False

    def test_non_pd_covariance_gives_nan_not_sqrt_abs(self) -> None:
        from archbox.core.exceptions import StandardErrorWarning

        with pytest.warns(StandardErrorWarning):
            se = MLEstimator._se_from_variance(
                np.array([4.0, -1.0, np.nan]), ["a", "b", "c"], "non-robust"
            )
        assert se[0] == pytest.approx(2.0)
        assert np.isnan(se[1])
        assert np.isnan(se[2])

    def test_singular_hessian_gives_nan_standard_errors(
        self, garch_data: np.ndarray, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        from archbox.core.exceptions import StandardErrorWarning

        model = SimpleGARCH(garch_data, mean="zero")
        estimator = MLEstimator()
        monkeypatch.setattr(
            MLEstimator, "_compute_hessian", lambda *args, **kwargs: np.zeros((3, 3))
        )
        with pytest.warns(StandardErrorWarning):
            se_robust, se_nonrobust = estimator._compute_standard_errors(
                model, model.start_params, model._backcast(model.endog)
            )
        assert np.all(np.isnan(se_robust))
        assert np.all(np.isnan(se_nonrobust))

    def test_nan_standard_errors_propagate_to_tvalues(self, garch_data: np.ndarray) -> None:
        """No 1e-20 floor: a NaN SE yields a NaN t-value, not a 1e20 one."""
        from archbox.core.results import ArchResults

        model = SimpleGARCH(garch_data, mean="zero")
        params = model.start_params
        nan_se = np.full(3, np.nan)
        results = ArchResults(
            model=model,
            params=params,
            loglike=1.0,
            sigma2=np.ones(len(garch_data)),
            se_robust=nan_se,
            se_nonrobust=nan_se,
            convergence=True,
        )
        assert np.all(np.isnan(results.tvalues))
