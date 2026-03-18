"""Tests for ArchExperiment pattern."""

from __future__ import annotations

import numpy as np
import pytest

from archbox.experiment.comparison import ComparisonResult
from archbox.experiment.experiment import ArchExperiment
from archbox.experiment.validation import ValidationResult


class TestComparisonResult:
    """Test ComparisonResult."""

    def test_ranking_sorts_by_criterion(self) -> None:
        """ranking() sorts models by given criterion."""
        cr = ComparisonResult(
            model_names=["A", "B", "C"],
            criteria={
                "aic": [100.0, 90.0, 110.0],
                "bic": [105.0, 95.0, 115.0],
            },
        )
        ranked = cr.ranking("aic")
        assert ranked.index.tolist() == ["B", "A", "C"]

    def test_best_model(self) -> None:
        """best_model() returns the model with lowest criterion."""
        cr = ComparisonResult(
            model_names=["GARCH", "EGARCH", "GJR"],
            criteria={
                "aic": [100.0, 90.0, 95.0],
                "bic": [105.0, 95.0, 100.0],
            },
        )
        assert cr.best_model("aic") == "EGARCH"
        assert cr.best_model("bic") == "EGARCH"

    def test_to_dataframe(self) -> None:
        """to_dataframe() returns a DataFrame."""
        cr = ComparisonResult(
            model_names=["A", "B"],
            criteria={"aic": [100.0, 90.0]},
        )
        df = cr.to_dataframe()
        assert len(df) == 2
        assert "aic" in df.columns

    def test_unknown_criterion_raises(self) -> None:
        """ranking() raises for unknown criterion."""
        cr = ComparisonResult(
            model_names=["A"],
            criteria={"aic": [100.0]},
        )
        with pytest.raises(ValueError, match="Unknown criterion"):
            cr.ranking("unknown")


class TestValidationResult:
    """Test ValidationResult."""

    def test_rmse_vol(self) -> None:
        """rmse_vol() returns positive float."""
        rng = np.random.default_rng(42)
        returns = rng.standard_normal(100) * 0.01
        vr = ValidationResult(
            model_name="GARCH",
            in_sample_size=1000,
            out_sample_size=100,
            forecast_volatility=np.full(100, 0.01),
            actual_returns=returns,
            actual_squared_returns=returns**2,
        )
        rmse = vr.rmse_vol()
        assert isinstance(rmse, float)
        assert rmse >= 0

    def test_var_violation_rate_raises_without_var(self) -> None:
        """var_violation_rate() raises when VaR not computed."""
        vr = ValidationResult(
            model_name="GARCH",
            in_sample_size=1000,
            out_sample_size=100,
            forecast_volatility=np.full(100, 0.01),
            actual_returns=np.zeros(100),
            actual_squared_returns=np.zeros(100),
        )
        with pytest.raises(ValueError, match="VaR series not computed"):
            vr.var_violation_rate()

    def test_var_violation_rate_computes(self) -> None:
        """var_violation_rate() returns valid rate."""
        rng = np.random.default_rng(42)
        returns = rng.standard_normal(100) * 0.01
        var_series = np.full(100, -0.02)
        vr = ValidationResult(
            model_name="GARCH",
            in_sample_size=1000,
            out_sample_size=100,
            forecast_volatility=np.full(100, 0.01),
            actual_returns=returns,
            actual_squared_returns=returns**2,
            var_series=var_series,
        )
        rate = vr.var_violation_rate()
        assert 0 <= rate <= 1


class TestArchExperiment:
    """Test ArchExperiment orchestrator."""

    def test_fit_all_models(self, sp500_returns: np.ndarray) -> None:
        """fit_all_models() fits multiple models."""
        exp = ArchExperiment(sp500_returns)
        results = exp.fit_all_models(
            [
                ("GARCH", {"p": 1, "q": 1}),
            ],
            disp=False,
        )
        assert len(results) == 1
        assert len(exp.fitted_models) == 1

    def test_compare_models_returns_ranking(self, sp500_returns: np.ndarray) -> None:
        """compare_models() returns ComparisonResult with ranking."""
        exp = ArchExperiment(sp500_returns)
        exp.fit_all_models(
            [
                ("GARCH", {"p": 1, "q": 1}),
            ],
            disp=False,
        )
        comparison = exp.compare_models(criteria=["aic", "bic"])
        assert isinstance(comparison, ComparisonResult)
        ranked = comparison.ranking("aic")
        assert len(ranked) == 1

    def test_compare_models_no_models_raises(self) -> None:
        """compare_models() raises when no models fitted."""
        exp = ArchExperiment(np.random.default_rng(42).standard_normal(500))
        with pytest.raises(RuntimeError, match="No models fitted"):
            exp.compare_models()

    def test_validate_model_produces_metrics(self, sp500_returns: np.ndarray) -> None:
        """validate_model() produces ValidationResult."""
        exp = ArchExperiment(sp500_returns)
        exp.fit_all_models(
            [
                ("GARCH", {"p": 1, "q": 1}),
            ],
            disp=False,
        )
        name = next(iter(exp.fitted_models))
        validation = exp.validate_model(name, test_size=200)
        assert isinstance(validation, ValidationResult)
        rmse = validation.rmse_vol()
        assert rmse >= 0
