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


class _AlwaysInfeasible(_ConcreteMultivar):
    """Model whose second-step objective can never be evaluated."""

    model_name = "AlwaysInfeasible"

    @property
    def start_params(self) -> NDArray[np.float64]:
        return np.array([0.5])

    @property
    def param_names(self) -> list[str]:
        return ["theta"]

    def _second_step_neg_loglike(self, params, std_resids):
        return float(np.inf)


class _NonPDCorrelation(_ConcreteMultivar):
    """Model returning a singular correlation matrix, so the loglike is -inf."""

    model_name = "NonPD"

    def _correlation_recursion(self, params, std_resids):
        T, k = std_resids.shape
        R_t = np.zeros((T, k, k))
        R_t[:] = np.ones((k, k))  # singular
        return R_t


class TestUnivariateModelArgument:
    """The ``univariate_model`` argument must actually be honoured."""

    def test_default_is_garch(self, synthetic_returns):
        """The default keeps the historical GARCH behaviour."""
        from archbox.models.garch import GARCH
        from archbox.multivariate import CCC

        results = CCC(synthetic_returns).fit(disp=False)
        for res in results.univariate_results:
            assert isinstance(res._model, GARCH)

    def test_named_model_is_used(self, synthetic_returns):
        """Passing 'EGARCH' fits EGARCH on every series."""
        from archbox.models.egarch import EGARCH
        from archbox.multivariate import CCC

        results = CCC(synthetic_returns, univariate_model="EGARCH").fit(disp=False)
        for res in results.univariate_results:
            assert isinstance(res._model, EGARCH)

    def test_model_class_is_used(self, synthetic_returns):
        """A model class can be passed directly."""
        from archbox.models.gjr_garch import GJRGARCH
        from archbox.multivariate import CCC

        results = CCC(synthetic_returns, univariate_model=GJRGARCH).fit(disp=False)
        for res in results.univariate_results:
            assert isinstance(res._model, GJRGARCH)

    def test_factory_is_used(self, synthetic_returns):
        """A callable factory taking only the series is supported."""
        from archbox.models.garch import GARCH
        from archbox.multivariate import CCC

        def factory(series):
            return GARCH(series, p=1, q=2, mean="constant")

        results = CCC(synthetic_returns, univariate_model=factory).fit(disp=False)
        for res in results.univariate_results:
            assert res._model.q == 2

    def test_univariate_order_is_honoured(self, synthetic_returns):
        """The (p, q) order reaches the univariate models."""
        from archbox.multivariate import CCC

        results = CCC(synthetic_returns, univariate_order=(2, 1)).fit(disp=False)
        for res in results.univariate_results:
            assert res._model.p == 2
            assert res._model.q == 1

    def test_univariate_dist_is_honoured(self, synthetic_returns):
        """A non-normal conditional distribution reaches the univariate models."""
        from archbox.multivariate import CCC

        results = CCC(synthetic_returns, univariate_dist="studentt").fit(disp=False)
        for res in results.univariate_results:
            assert res._dist_params.size == 1

    def test_unknown_name_raises(self, synthetic_returns):
        """An unknown model name fails fast, at construction time."""
        from archbox.multivariate import CCC

        with pytest.raises(ValueError, match="Unknown univariate_model"):
            CCC(synthetic_returns, univariate_model="NOT-A-MODEL")

    def test_bad_type_raises(self, synthetic_returns):
        """A non-callable, non-string spec is a TypeError."""
        from archbox.multivariate import CCC

        with pytest.raises(TypeError, match="univariate_model"):
            CCC(synthetic_returns, univariate_model=17)


class TestFitMethodArgument:
    """``fit(method=...)`` must be honoured, not silently ignored."""

    def test_unknown_method_raises(self, synthetic_returns):
        """An unsupported method is rejected instead of ignored."""
        from archbox.multivariate import DCC

        model = DCC(synthetic_returns)
        with pytest.raises(ValueError, match="method"):
            model.fit(method="full_mle", disp=False)

    def test_supported_method_accepted(self, synthetic_returns):
        """The documented method still works."""
        from archbox.multivariate import DCC

        results = DCC(synthetic_returns).fit(method="two_step", disp=False)
        assert np.isfinite(results.loglike)


class TestConvergenceReporting:
    """Failed optimizations must be reported, never silently swallowed."""

    def test_all_starts_failing_sets_converged_false(self, synthetic_returns):
        """A model whose objective is never feasible warns and flags itself."""
        from archbox.core.exceptions import ConvergenceWarning

        model = _AlwaysInfeasible(synthetic_returns)
        with pytest.warns(ConvergenceWarning, match="none of the optimizer"):
            results = model.fit(disp=False)
        assert results.converged is False

    def test_non_finite_loglike_raises(self, synthetic_returns):
        """A degenerate correlation path raises instead of reporting -1e10."""
        from archbox.core.exceptions import ConvergenceError

        model = _NonPDCorrelation(synthetic_returns)
        with pytest.raises(ConvergenceError):
            model.fit(disp=False)

    def test_loglikelihood_returns_minus_inf_not_sentinel(self, synthetic_returns):
        """``_loglikelihood`` signals failure with -inf, not -1e10."""
        model = _ConcreteMultivar(synthetic_returns)
        T, k = 50, 3
        singular = np.ones((T, k, k))
        z = np.zeros((T, k))
        vol = np.ones((T, k))
        assert model._loglikelihood(singular, z, vol) == -np.inf

    def test_successful_fit_is_marked_converged(self, synthetic_returns):
        """A normal DCC fit reports converged=True."""
        from archbox.multivariate import DCC

        assert DCC(synthetic_returns).fit(disp=False).converged is True


class TestCorrelationLoglike:
    """The vectorised correlation likelihood matches an explicit loop."""

    def test_matches_loop(self, rng):
        """Batched slogdet/solve give the same value as a per-t loop."""
        from archbox.multivariate.base import correlation_loglike

        T, k = 120, 3
        z = rng.standard_normal((T, k))
        base = np.array([[1.0, 0.3, 0.1], [0.3, 1.0, -0.2], [0.1, -0.2, 1.0]])
        R_t = np.stack([base * (0.9 + 0.05 * np.sin(t)) + np.eye(k) * 0.1 for t in range(T)])
        R_t = np.stack([r / np.sqrt(np.outer(np.diag(r), np.diag(r))) for r in R_t])

        expected = 0.0
        for t in range(T):
            _sign, logdet = np.linalg.slogdet(R_t[t])
            zt = z[t]
            quad = zt @ np.linalg.solve(R_t[t], zt)
            expected += -0.5 * (logdet + quad - zt @ zt)

        assert np.isclose(correlation_loglike(R_t, z), expected, rtol=1e-10)

    def test_non_pd_returns_minus_inf(self, rng):
        """A singular R_t yields -inf, not a large sentinel."""
        from archbox.multivariate.base import correlation_loglike

        z = rng.standard_normal((10, 2))
        R_t = np.ones((10, 2, 2))
        assert correlation_loglike(R_t, z) == -np.inf


class TestPandasPassthrough:
    """Column names of a DataFrame input must survive into the results."""

    def test_series_names_preserved(self, fx_frame):
        """The fitted results carry the input column names."""
        from archbox.multivariate import DCC

        results = DCC(fx_frame).fit(disp=False)
        assert results.series_names == list(fx_frame.columns)

    def test_frames_are_labelled(self, fx_frame):
        """The DataFrame accessors use the input columns and index."""
        from archbox.multivariate import DCC

        results = DCC(fx_frame).fit(disp=False)

        vol = results.conditional_volatility_frame()
        assert list(vol.columns) == list(fx_frame.columns)
        assert vol.index.equals(fx_frame.index)

        z = results.std_resid_frame()
        assert list(z.columns) == list(fx_frame.columns)

        corr = results.correlation_frame(-1)
        assert list(corr.columns) == list(fx_frame.columns)
        assert list(corr.index) == list(fx_frame.columns)

        cov = results.covariance_frame(-1)
        np.testing.assert_allclose(cov.to_numpy(), results.dynamic_covariance[-1])

    def test_numpy_input_gets_default_names(self, synthetic_returns):
        """Plain ndarray input still yields usable placeholder names."""
        from archbox.multivariate import CCC

        results = CCC(synthetic_returns).fit(disp=False)
        assert results.series_names == ["series_0", "series_1", "series_2"]

    def test_arrays_stay_arrays(self, fx_frame):
        """The ndarray attributes are not silently turned into DataFrames."""
        from archbox.multivariate import CCC

        results = CCC(fx_frame).fit(disp=False)
        assert isinstance(results.conditional_volatility, np.ndarray)
        assert isinstance(results.std_resids, np.ndarray)


class TestStandardizedResiduals:
    """Step 2 must consume ArchResults.std_resid, not resid/sigma twice."""

    def test_std_resids_match_univariate_std_resid(self, synthetic_returns):
        """The z_t handed to the correlation step are the standardized residuals."""
        from archbox.multivariate import CCC

        results = CCC(synthetic_returns).fit(disp=False)
        for i, res in enumerate(results.univariate_results):
            np.testing.assert_allclose(results.std_resids[:, i], res.std_resid)

    def test_std_resids_are_unit_scale(self, synthetic_returns):
        """z_t has roughly unit variance, unlike raw returns divided twice."""
        from archbox.multivariate import CCC

        results = CCC(synthetic_returns).fit(disp=False)
        assert 0.5 < float(np.std(results.std_resids)) < 2.0

    def test_std_resid_accessor(self, synthetic_returns):
        """``results.std_resid`` mirrors ``results.std_resids``."""
        from archbox.multivariate import CCC

        results = CCC(synthetic_returns).fit(disp=False)
        assert results.std_resid is results.std_resids


class TestResultsAreSelfContained:
    """covariance()/correlation() must read the results, not model state."""

    def test_covariance_reads_results_not_model(self, synthetic_returns, rng):
        """Clearing the model's cached state must not change an existing result."""
        from archbox.multivariate import CCC

        model = CCC(synthetic_returns)
        results = model.fit(disp=False)
        before = results.covariance(-1).copy()

        # Any stale model state must be unused by the results object.
        model._conditional_volatility = None
        model._std_resids = None

        np.testing.assert_allclose(results.covariance(-1), before)
        np.testing.assert_allclose(results.covariance(-1), results.dynamic_covariance[-1])
        np.testing.assert_allclose(results.correlation(0), results.dynamic_correlation[0])

    def test_results_forecast_delegates(self, synthetic_returns):
        """``results.forecast`` returns the same as ``model.forecast``."""
        from archbox.multivariate import DCC

        model = DCC(synthetic_returns)
        results = model.fit(disp=False)
        a = results.forecast(horizon=3)
        b = model.forecast(results, horizon=3)
        np.testing.assert_allclose(a["covariance"], b["covariance"])

    def test_conditional_covariance_alias(self, synthetic_returns):
        """``conditional_covariance`` mirrors ``dynamic_covariance``."""
        from archbox.multivariate import CCC

        results = CCC(synthetic_returns).fit(disp=False)
        assert results.conditional_covariance is results.dynamic_covariance
        assert results.conditional_correlation is results.dynamic_correlation


class TestStandardErrors:
    """Standard errors come from the second-step numerical Hessian."""

    def test_dcc_standard_errors_finite_on_dynamic_data(self, dcc_returns):
        """At an interior optimum the SEs are finite and positive."""
        from archbox.multivariate import DCC

        results = DCC(dcc_returns).fit(disp=False)
        assert results.std_errors.shape == results.params.shape
        assert np.all(np.isfinite(results.std_errors))
        assert np.all(results.std_errors > 0)
        assert np.all(np.isfinite(results.tvalues))

    def test_never_reports_a_fake_number(self, synthetic_returns):
        """A corner solution reports nan rather than a made-up number."""
        from archbox.multivariate import DCC

        results = DCC(synthetic_returns).fit(disp=False)
        assert results.std_errors.shape == (2,)
        finite = np.isfinite(results.std_errors)
        assert np.all(results.std_errors[finite] > 0)

    def test_no_params_gives_empty_std_errors(self, synthetic_returns):
        """CCC has no second-step parameters, so no standard errors."""
        from archbox.multivariate import CCC

        results = CCC(synthetic_returns).fit(disp=False)
        assert results.std_errors.shape == (0,)

    def test_summary_lists_named_parameters(self, dcc_returns):
        """summary() names the parameters and shows their standard errors."""
        from archbox.multivariate import DCC

        results = DCC(dcc_returns).fit(disp=False)
        s = results.summary()
        assert "std err" in s
        assert "Converged" in s
        for name in results.param_names:
            assert name in s
