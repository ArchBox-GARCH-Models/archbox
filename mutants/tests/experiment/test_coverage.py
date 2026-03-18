"""Coverage tests for experiment module: risk_analysis.py, validation.py, experiment.py."""

from __future__ import annotations

from unittest.mock import MagicMock

import matplotlib
import numpy as np
import pytest

matplotlib.use("Agg")

from archbox.experiment.risk_analysis import RiskAnalysisResult
from archbox.experiment.validation import ValidationResult

# ============================================================
# Tests for RiskAnalysisResult
# ============================================================


class TestRiskAnalysisResult:
    """Tests for RiskAnalysisResult dataclass."""

    @pytest.fixture()
    def risk_result(self) -> RiskAnalysisResult:
        rng = np.random.default_rng(42)
        n = 100
        var_series = rng.standard_normal(n) * 0.02 - 0.03
        es_series = var_series - 0.01
        return RiskAnalysisResult(
            model_name="GARCH(1,1)",
            alpha=0.05,
            var_series={"parametric": var_series},
            es_series={"parametric": es_series},
            backtest_results={},
        )

    def test_backtest_summary_empty(self, risk_result: RiskAnalysisResult) -> None:
        s = risk_result.backtest_summary()
        assert "GARCH(1,1)" in s
        assert "Alpha: 0.05" in s

    def test_backtest_summary_with_results(self) -> None:
        bt = MagicMock()
        bt.violation_ratio.return_value = 0.06
        bt.kupiec_test.return_value = MagicMock(pvalue=0.45)
        bt.basel_traffic_light.return_value = "green"

        result = RiskAnalysisResult(
            model_name="TestModel",
            alpha=0.05,
            var_series={},
            es_series={},
            backtest_results={"parametric": bt},
        )
        s = result.backtest_summary()
        assert "Violation ratio" in s
        assert "Kupiec p-value" in s
        assert "Traffic light" in s

    def test_plot_risk_parametric(self, risk_result: RiskAnalysisResult) -> None:
        import matplotlib.pyplot as plt

        ax = risk_result.plot_risk(method="parametric")
        assert ax is not None
        plt.close("all")

    def test_plot_risk_with_returns(self, risk_result: RiskAnalysisResult) -> None:
        import matplotlib.pyplot as plt

        rng = np.random.default_rng(42)
        returns = rng.standard_normal(200) * 0.01
        ax = risk_result.plot_risk(method="parametric", returns=returns)
        assert ax is not None
        plt.close("all")

    def test_plot_risk_with_existing_ax(self, risk_result: RiskAnalysisResult) -> None:
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        returned_ax = risk_result.plot_risk(method="parametric", ax=ax)
        assert returned_ax is ax
        plt.close(fig)

    def test_plot_risk_unknown_method(self, risk_result: RiskAnalysisResult) -> None:
        with pytest.raises(ValueError, match="Method 'unknown' not found"):
            risk_result.plot_risk(method="unknown")

    def test_plot_risk_without_es(self) -> None:
        import matplotlib.pyplot as plt

        rng = np.random.default_rng(42)
        result = RiskAnalysisResult(
            model_name="Test",
            alpha=0.05,
            var_series={"parametric": rng.standard_normal(50)},
            es_series={},
            backtest_results={},
        )
        ax = result.plot_risk(method="parametric")
        assert ax is not None
        plt.close("all")


# ============================================================
# Tests for ValidationResult
# ============================================================


class TestValidationResult:
    """Tests for ValidationResult dataclass."""

    @pytest.fixture()
    def validation_result(self) -> ValidationResult:
        rng = np.random.default_rng(42)
        n = 100
        actual = rng.standard_normal(n) * 0.01
        forecast_vol = np.abs(actual) + 0.005
        return ValidationResult(
            model_name="GARCH(1,1)",
            in_sample_size=500,
            out_sample_size=n,
            forecast_volatility=forecast_vol,
            actual_returns=actual,
            actual_squared_returns=actual**2,
            var_series=-forecast_vol * 1.65,
            alpha=0.05,
        )

    def test_rmse_vol(self, validation_result: ValidationResult) -> None:
        rmse = validation_result.rmse_vol()
        assert rmse > 0
        assert np.isfinite(rmse)

    def test_mae_vol(self, validation_result: ValidationResult) -> None:
        mae = validation_result.mae_vol()
        assert mae > 0
        assert np.isfinite(mae)

    def test_var_violation_rate(self, validation_result: ValidationResult) -> None:
        rate = validation_result.var_violation_rate()
        assert 0.0 <= rate <= 1.0

    def test_var_violation_rate_no_var(self) -> None:
        rng = np.random.default_rng(42)
        n = 50
        result = ValidationResult(
            model_name="Test",
            in_sample_size=200,
            out_sample_size=n,
            forecast_volatility=np.ones(n) * 0.01,
            actual_returns=rng.standard_normal(n) * 0.01,
            actual_squared_returns=np.ones(n) * 0.0001,
            var_series=None,
        )
        with pytest.raises(ValueError, match="VaR series not computed"):
            result.var_violation_rate()

    def test_plot_forecast_vs_actual(self, validation_result: ValidationResult) -> None:
        import matplotlib.pyplot as plt

        ax = validation_result.plot_forecast_vs_actual()
        assert ax is not None
        plt.close("all")

    def test_plot_forecast_with_existing_ax(self, validation_result: ValidationResult) -> None:
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        returned_ax = validation_result.plot_forecast_vs_actual(ax=ax)
        assert returned_ax is ax
        plt.close(fig)


# ============================================================
# Tests for ArchExperiment (uncovered parts)
# ============================================================


class TestArchExperimentEdgeCases:
    """Tests for ArchExperiment edge cases."""

    def test_init(self) -> None:
        from archbox.experiment.experiment import ArchExperiment

        rng = np.random.default_rng(42)
        returns = rng.standard_normal(500) * 0.01
        exp = ArchExperiment(returns)
        assert len(exp.fitted_models) == 0

    def test_compare_models_no_fitted_raises(self) -> None:
        from archbox.experiment.experiment import ArchExperiment

        rng = np.random.default_rng(42)
        returns = rng.standard_normal(500) * 0.01
        exp = ArchExperiment(returns)
        with pytest.raises(RuntimeError, match="No models fitted"):
            exp.compare_models()

    def test_build_model_unknown_type(self) -> None:
        from archbox.experiment.experiment import ArchExperiment

        rng = np.random.default_rng(42)
        returns = rng.standard_normal(500) * 0.01
        exp = ArchExperiment(returns)
        with pytest.raises(ValueError, match="Unknown model type"):
            exp._build_model("UNKNOWN_MODEL", returns, {})

    def test_validate_model_not_found(self) -> None:
        from archbox.experiment.experiment import ArchExperiment

        rng = np.random.default_rng(42)
        returns = rng.standard_normal(500) * 0.01
        exp = ArchExperiment(returns)
        exp.fitted_models["dummy"] = MagicMock()
        with pytest.raises(ValueError, match="not found"):
            exp.validate_model(model_name="nonexistent")

    def test_validate_model_test_size_too_large(self) -> None:
        from archbox.experiment.experiment import ArchExperiment

        rng = np.random.default_rng(42)
        returns = rng.standard_normal(500) * 0.01
        exp = ArchExperiment(returns)
        exp.fitted_models["dummy"] = MagicMock()
        exp.model_specs["dummy"] = ("GARCH", {"p": 1, "q": 1})
        with pytest.raises(ValueError, match="test_size"):
            exp.validate_model(model_name="dummy", test_size=600)

    def test_risk_analysis_model_not_found(self) -> None:
        from archbox.experiment.experiment import ArchExperiment

        rng = np.random.default_rng(42)
        returns = rng.standard_normal(500) * 0.01
        exp = ArchExperiment(returns)
        exp.fitted_models["dummy"] = MagicMock()
        with pytest.raises(ValueError, match="not found"):
            exp.risk_analysis(model="nonexistent")
