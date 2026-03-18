"""Coverage tests for threshold module: base.py, results.py, transition.py."""

from __future__ import annotations

import matplotlib
import numpy as np
import pytest
from numpy.typing import NDArray

matplotlib.use("Agg")

from archbox.threshold.base import ThresholdModel
from archbox.threshold.results import TestResult, ThresholdResults
from archbox.threshold.transition import (
    exponential_transition,
    logistic_transition,
    logistic_transition_order2,
    plot_transition,
)

# --- Concrete subclass for testing ThresholdModel ---


class _ConcreteThreshold(ThresholdModel):
    """Minimal concrete subclass for testing the abstract base."""

    model_name = "TestModel"

    def _transition_function(
        self, s: NDArray[np.float64], params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        gamma, c = params[0], params[1]
        return logistic_transition(s, gamma, c)

    @property
    def start_params(self) -> NDArray[np.float64]:
        return np.array([1.0, 0.0, 0.5, 0.3, 0.5, 0.3, 1.0, 0.0])

    @property
    def param_names(self) -> list[str]:
        return ["gamma", "c", "const1", "phi1_1", "const2", "phi1_2"]

    def _fit_cls(self):
        g_vals = self._transition_function(self._s, np.array([1.0, 0.0]))
        beta1, resid1, _ = self._ols_fit(self._y, self._X)
        beta2, resid2, _ = self._ols_fit(self._y, self._X)
        resid = resid1 * (1 - g_vals) + resid2 * g_vals
        sigma2_1 = float(np.var(resid1))
        sigma2_2 = float(np.var(resid2))
        ll = self.loglike(beta1, beta2, sigma2_1, sigma2_2, g_vals)
        n_params = len(beta1) + len(beta2) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(len(self._y)) * n_params
        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=0.0,
            delay=self.delay,
            transition_params={"gamma": 1.0, "c": 0.0},
            transition_params_array=np.array([1.0, 0.0]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g_vals,
            transition_values=g_vals,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=len(self._y),
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )


def _make_series(n: int = 200) -> NDArray[np.float64]:
    """Generate a simple AR(1) series with regime switching."""
    rng = np.random.default_rng(42)
    y = np.zeros(n)
    for t in range(1, n):
        if y[t - 1] > 0:
            y[t] = 0.5 + 0.3 * y[t - 1] + rng.standard_normal()
        else:
            y[t] = -0.5 + 0.7 * y[t - 1] + rng.standard_normal()
    return y


# ============================================================
# Tests for ThresholdModel base class
# ============================================================


class TestThresholdModelBase:
    """Tests for ThresholdModel abstract base class (via concrete subclass)."""

    def test_init_basic(self) -> None:
        y = _make_series(200)
        model = _ConcreteThreshold(y, order=1, delay=1, n_regimes=2)
        assert model.nobs == 200
        assert model.order == 1
        assert model.delay == 1

    def test_init_insufficient_obs(self) -> None:
        with pytest.raises(ValueError, match="Insufficient observations"):
            _ConcreteThreshold(np.random.default_rng(0).standard_normal(10), order=1, delay=1)

    def test_init_invalid_order(self) -> None:
        with pytest.raises(ValueError, match="order must be >= 1"):
            _ConcreteThreshold(_make_series(), order=0)

    def test_init_invalid_delay(self) -> None:
        with pytest.raises(ValueError, match="delay must be >= 1"):
            _ConcreteThreshold(_make_series(), delay=0)

    def test_init_invalid_n_regimes(self) -> None:
        with pytest.raises(ValueError, match="n_regimes must be 2 or 3"):
            _ConcreteThreshold(_make_series(), n_regimes=4)

    def test_build_matrices_shapes(self) -> None:
        y = _make_series(200)
        model = _ConcreteThreshold(y, order=2, delay=1)
        assert model._y.shape[0] == model._X.shape[0]
        assert model._X.shape[1] == 3  # const + 2 lags
        assert model._s.shape[0] == model._y.shape[0]

    def test_fit_unknown_method(self) -> None:
        model = _ConcreteThreshold(_make_series())
        with pytest.raises(ValueError, match="Unknown estimation method"):
            model.fit(method="mle")

    def test_fit_cls(self) -> None:
        model = _ConcreteThreshold(_make_series())
        result = model.fit()
        assert isinstance(result, ThresholdResults)
        assert np.isfinite(result.loglike)

    def test_loglike(self) -> None:
        model = _ConcreteThreshold(_make_series())
        n = len(model._y)
        k = model.order + 1
        params1 = np.zeros(k)
        params2 = np.zeros(k)
        g = np.full(n, 0.5)
        ll = model.loglike(params1, params2, 1.0, 1.0, g)
        assert np.isfinite(ll)

    def test_forecast(self) -> None:
        model = _ConcreteThreshold(_make_series())
        result = model.fit()
        fc = model.forecast(result, horizon=5)
        assert "mean" in fc
        assert len(fc["mean"]) == 5
        assert np.all(np.isfinite(fc["mean"]))

    def test_simulate(self) -> None:
        model = _ConcreteThreshold(_make_series())
        params1 = np.array([0.0, 0.5])
        params2 = np.array([0.0, 0.3])
        trans = np.array([1.0, 0.0])
        sim = model.simulate(100, params1, params2, trans, sigma=1.0, seed=42)
        assert len(sim) == 100
        assert np.all(np.isfinite(sim))

    def test_ols_fit(self) -> None:
        rng = np.random.default_rng(42)
        X = np.column_stack([np.ones(50), rng.standard_normal(50)])
        y = X @ np.array([1.0, 2.0]) + rng.standard_normal(50) * 0.1
        beta, resid, rss = ThresholdModel._ols_fit(y, X)
        assert len(beta) == 2
        assert len(resid) == 50
        assert rss > 0

    def test_ols_rss(self) -> None:
        rng = np.random.default_rng(42)
        X = np.column_stack([np.ones(50), rng.standard_normal(50)])
        y = X @ np.array([1.0, 2.0]) + rng.standard_normal(50) * 0.1
        rss = ThresholdModel._ols_rss(y, X)
        assert rss > 0

    def test_plot_transition(self) -> None:
        import matplotlib.pyplot as plt

        model = _ConcreteThreshold(_make_series())
        result = model.fit()
        fig = model.plot_transition(result)
        assert fig is not None
        plt.close(fig)

    def test_plot_phase_diagram(self) -> None:
        import matplotlib.pyplot as plt

        model = _ConcreteThreshold(_make_series())
        result = model.fit()
        fig = model.plot_phase_diagram(result)
        assert fig is not None
        plt.close(fig)


# ============================================================
# Tests for ThresholdResults
# ============================================================


class TestThresholdResults:
    """Tests for ThresholdResults dataclass."""

    @pytest.fixture()
    def results(self) -> ThresholdResults:
        model = _ConcreteThreshold(_make_series())
        return model.fit()

    def test_summary_basic(self, results: ThresholdResults) -> None:
        s = results.summary()
        assert "TestModel" in s
        assert "Log-Likelihood" in s
        assert "AIC" in s
        assert "BIC" in s

    def test_summary_with_list_threshold(self) -> None:
        model = _ConcreteThreshold(_make_series())
        res = model.fit()
        # Override threshold to be a list
        res.threshold = [-1.0, 1.0]
        s = res.summary()
        assert "c_1" in s
        assert "c_2" in s

    def test_summary_with_linearity_test(self, results: ThresholdResults) -> None:
        results.linearity_test = TestResult(statistic=5.0, pvalue=0.01, test_name="LM")
        s = results.summary()
        assert "Linearity Test" in s
        assert "LM" in s

    def test_plot_transition(self, results: ThresholdResults) -> None:
        import matplotlib.pyplot as plt

        fig = results.plot_transition()
        assert fig is not None
        plt.close(fig)

    def test_plot_regimes(self, results: ThresholdResults) -> None:
        import matplotlib.pyplot as plt

        fig = results.plot_regimes()
        assert fig is not None
        plt.close(fig)

    def test_plot_phase_diagram(self, results: ThresholdResults) -> None:
        import matplotlib.pyplot as plt

        fig = results.plot_phase_diagram()
        assert fig is not None
        plt.close(fig)

    def test_plot_fit(self, results: ThresholdResults) -> None:
        import matplotlib.pyplot as plt

        fig = results.plot_fit()
        assert fig is not None
        plt.close(fig)

    def test_forecast_via_results(self, results: ThresholdResults) -> None:
        fc = results.forecast(horizon=3)
        assert "mean" in fc
        assert len(fc["mean"]) == 3

    def test_forecast_no_model_raises(self) -> None:
        model = _ConcreteThreshold(_make_series())
        res = model.fit()
        res._model = None
        with pytest.raises(RuntimeError, match="Model reference not available"):
            res.forecast(horizon=5)


class TestTestResult:
    """Tests for TestResult dataclass."""

    def test_creation(self) -> None:
        tr = TestResult(statistic=3.5, pvalue=0.02, test_name="LM", detail="info")
        assert tr.statistic == 3.5
        assert tr.pvalue == 0.02
        assert tr.test_name == "LM"
        assert tr.detail == "info"


# ============================================================
# Tests for transition functions (coverage of plot and edge cases)
# ============================================================


class TestTransitionPlot:
    """Tests for plot_transition function."""

    def test_plot_logistic(self) -> None:
        import matplotlib.pyplot as plt

        s = np.linspace(-5, 5, 100)
        fig = plot_transition(s, [0.5, 1.0, 5.0], c=0.0, transition_type="logistic")
        assert fig is not None
        plt.close(fig)

    def test_plot_exponential(self) -> None:
        import matplotlib.pyplot as plt

        s = np.linspace(-5, 5, 100)
        fig = plot_transition(s, [0.5, 1.0, 5.0], c=0.0, transition_type="exponential")
        assert fig is not None
        plt.close(fig)

    def test_plot_unknown_type_raises(self) -> None:
        s = np.linspace(-5, 5, 100)
        with pytest.raises(ValueError, match="Unknown transition type"):
            plot_transition(s, [1.0], c=0.0, transition_type="unknown")

    def test_logistic_extreme_values(self) -> None:
        """Test logistic with extreme exponent values (clip paths)."""
        s = np.array([-1000.0, 1000.0])
        g = logistic_transition(s, gamma=100.0, c=0.0)
        assert g[0] < 1e-10
        assert g[1] > 1.0 - 1e-10

    def test_exponential_extreme_values(self) -> None:
        """Test exponential with extreme exponent values (clip paths)."""
        s = np.array([-100.0, 100.0])
        g = exponential_transition(s, gamma=10.0, c=0.0)
        assert np.all(g >= 0)
        assert np.all(g <= 1.0)

    def test_logistic_order2_extreme(self) -> None:
        s = np.array([-1000.0, 0.0, 1000.0])
        g = logistic_transition_order2(s, gamma=100.0, c1=-1.0, c2=1.0)
        assert np.all(g >= 0)
        assert np.all(g <= 1.0)
