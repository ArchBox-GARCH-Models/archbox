"""ArchExperiment - orchestrator for volatility analysis workflows."""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray

from archbox.experiment.comparison import ComparisonResult
from archbox.experiment.risk_analysis import RiskAnalysisResult
from archbox.experiment.validation import ValidationResult


class ArchExperiment:
    """Orchestrator for volatility analysis experiments.

    Provides a high-level API for fitting multiple models, comparing them,
    validating out-of-sample, and generating risk analysis reports.

    Parameters
    ----------
    returns : array-like
        Time series of returns.
    mean : str
        Mean model: 'constant' or 'zero'.

    Examples
    --------
    >>> from archbox.experiment import ArchExperiment
    >>> from archbox.datasets import load_dataset
    >>> sp500 = load_dataset('sp500')
    >>> exp = ArchExperiment(sp500['returns'])
    >>> exp.fit_all_models([
    ...     ('GARCH', {'p': 1, 'q': 1}),
    ...     ('EGARCH', {'p': 1, 'q': 1}),
    ... ])
    >>> comparison = exp.compare_models()
    >>> print(comparison.best_model())
    """

    def __init__(
        self,
        returns: Any,
        mean: str = "constant",
    ) -> None:
        """Initialize experiment with return data and mean model."""
        self.returns = np.asarray(returns, dtype=np.float64)
        self.mean = mean
        self.fitted_models: dict[str, Any] = {}
        self.model_specs: dict[str, tuple[str, dict[str, Any]]] = {}

    def _build_model(
        self,
        model_type: str,
        returns: NDArray[np.float64],
        kwargs: dict[str, Any],
    ) -> Any:
        """Build a model instance from type and kwargs.

        Parameters
        ----------
        model_type : str
            Model class name (e.g., 'GARCH', 'EGARCH', 'GJR').
        returns : NDArray[np.float64]
            Returns data.
        kwargs : dict
            Additional keyword arguments for the model.

        Returns
        -------
        VolatilityModel
            Configured model instance.
        """
        mean = kwargs.pop("mean", self.mean)
        dist = kwargs.pop("dist", "normal")

        model_map: dict[str, type] = {}
        key = model_type.upper()

        if key == "GARCH":
            from archbox.models.garch import GARCH

            model_map["GARCH"] = GARCH
        elif key == "EGARCH":
            from archbox.models.egarch import EGARCH

            model_map["EGARCH"] = EGARCH
        elif key == "GJR":
            from archbox.models.gjr_garch import GJRGARCH

            model_map["GJR"] = GJRGARCH
        elif key == "APARCH":
            from archbox.models.aparch import APARCH

            model_map["APARCH"] = APARCH
        elif key == "COMPONENT":
            from archbox.models.component_garch import ComponentGARCH

            model_map["COMPONENT"] = ComponentGARCH
        elif key == "FIGARCH":
            from archbox.models.figarch import FIGARCH

            model_map["FIGARCH"] = FIGARCH
        elif key == "IGARCH":
            from archbox.models.igarch import IGARCH

            model_map["IGARCH"] = IGARCH
        elif key == "GARCH-M":
            from archbox.models.garch_m import GARCHM

            model_map["GARCH-M"] = GARCHM

        cls = model_map.get(key)
        if cls is None:
            msg = f"Unknown model type: {model_type}"
            raise ValueError(msg)

        return cls(returns, dist=dist, mean=mean, **kwargs)

    def fit_all_models(
        self,
        model_specs: list[tuple[str, dict[str, Any]]],
        disp: bool = False,
    ) -> dict[str, Any]:
        """Fit multiple volatility models.

        Parameters
        ----------
        model_specs : list[tuple[str, dict]]
            List of (model_type, kwargs) tuples.
            Example: [('GARCH', {'p': 1, 'q': 1}), ('EGARCH', {'p': 1, 'q': 1})]
        disp : bool
            Display optimization progress.

        Returns
        -------
        dict[str, Any]
            Dictionary mapping model names to fitted results.
        """
        for model_type, kwargs in model_specs:
            kwargs_copy = kwargs.copy()
            dist = kwargs_copy.get("dist", "normal")
            p = kwargs_copy.get("p", 1)
            q = kwargs_copy.get("q", 1)
            name = f"{model_type}({p},{q})-{dist}"

            model = self._build_model(model_type, self.returns, kwargs_copy)
            results = model.fit(disp=disp)
            self.fitted_models[name] = results
            self.model_specs[name] = (model_type, kwargs.copy())

        return self.fitted_models

    def compare_models(
        self,
        criteria: list[str] | None = None,
    ) -> ComparisonResult:
        """Compare fitted models by information criteria.

        Parameters
        ----------
        criteria : list[str], optional
            Criteria to compare. Default: ['aic', 'bic', 'loglike', 'persistence'].

        Returns
        -------
        ComparisonResult
            Comparison results with ranking and best model.
        """
        if not self.fitted_models:
            msg = "No models fitted. Call fit_all_models() first."
            raise RuntimeError(msg)

        if criteria is None:
            criteria = ["aic", "bic", "loglike", "persistence"]

        model_names = list(self.fitted_models.keys())
        criteria_values: dict[str, list[float]] = {c: [] for c in criteria}
        results_list = []

        for name in model_names:
            result = self.fitted_models[name]
            results_list.append(result)
            for c in criteria:
                if c == "aic":
                    criteria_values[c].append(float(result.aic))
                elif c == "bic":
                    criteria_values[c].append(float(result.bic))
                elif c == "loglike":
                    criteria_values[c].append(float(result.loglike))
                elif c == "persistence":
                    criteria_values[c].append(float(result.persistence()))
                else:
                    criteria_values[c].append(float(getattr(result, c, np.nan)))

        return ComparisonResult(
            model_names=model_names,
            criteria=criteria_values,
            results=results_list,
        )

    def validate_model(
        self,
        model_name: str | None = None,
        test_size: int = 500,
        horizon: int = 1,
    ) -> ValidationResult:
        """Validate a model out-of-sample.

        Parameters
        ----------
        model_name : str, optional
            Name of the model to validate. If None, uses the first fitted model.
        test_size : int
            Number of out-of-sample observations.
        horizon : int
            Forecast horizon.

        Returns
        -------
        ValidationResult
            Validation results with RMSE and MAE.
        """
        if model_name is None:
            model_name = next(iter(self.fitted_models))

        if model_name not in self.fitted_models:
            msg = f"Model '{model_name}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        # Split data
        n = len(self.returns)
        if test_size >= n:
            msg = f"test_size ({test_size}) must be less than data length ({n})"
            raise ValueError(msg)

        train_returns = self.returns[: n - test_size]
        test_returns = self.returns[n - test_size :]

        # Re-fit on training data
        model_type, kwargs = self.model_specs[model_name]
        kwargs_copy = kwargs.copy()
        model = self._build_model(model_type, train_returns, kwargs_copy)
        train_result = model.fit(disp=False)

        # Forecast volatility for test period
        forecast = train_result.forecast(horizon=test_size)
        if isinstance(forecast, dict) and "variance" in forecast:
            forecast_vol = np.sqrt(forecast["variance"])
        else:
            forecast_vol = forecast

        # Ensure correct length
        if hasattr(forecast_vol, "__len__"):
            forecast_vol = np.asarray(forecast_vol, dtype=np.float64)
            if len(forecast_vol) > test_size:
                forecast_vol = forecast_vol[:test_size]
            elif len(forecast_vol) < test_size:
                pad = np.full(test_size - len(forecast_vol), forecast_vol[-1])
                forecast_vol = np.concatenate([forecast_vol, pad])
        else:
            forecast_vol = np.full(test_size, float(forecast_vol))  # type: ignore[arg-type]

        return ValidationResult(
            model_name=model_name,
            in_sample_size=len(train_returns),
            out_sample_size=test_size,
            forecast_volatility=forecast_vol,
            actual_returns=test_returns,
            actual_squared_returns=test_returns**2,
        )

    def risk_analysis(
        self,
        model: str | None = None,
        alpha: float = 0.05,
        methods: list[str] | None = None,
    ) -> RiskAnalysisResult:
        """Run risk analysis with backtest.

        Parameters
        ----------
        model : str, optional
            Model name. If None, uses the first fitted model.
        alpha : float
            Significance level.
        methods : list[str], optional
            VaR methods. Default: ['parametric'].

        Returns
        -------
        RiskAnalysisResult
            Risk analysis results.
        """
        if model is None:
            model = next(iter(self.fitted_models))

        if model not in self.fitted_models:
            msg = f"Model '{model}' not found. Available: {list(self.fitted_models.keys())}"
            raise ValueError(msg)

        if methods is None:
            methods = ["parametric"]

        result = self.fitted_models[model]

        from archbox.risk.es import ExpectedShortfall
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(result, alpha=alpha)
        es_calc = ExpectedShortfall(result, alpha=alpha)

        var_series: dict[str, Any] = {}
        es_series: dict[str, Any] = {}
        backtest_results: dict[str, Any] = {}

        for method in methods:
            if method == "parametric":
                var_series[method] = var_calc.parametric()
                es_series[method] = es_calc.parametric()
            elif method == "historical":
                var_series[method] = var_calc.historical()
                es_series[method] = es_calc.historical()
            elif method == "filtered-hs":
                var_series[method] = var_calc.filtered_historical()
                es_series[method] = es_calc.filtered_historical()
            elif method == "monte-carlo":
                var_series[method] = var_calc.monte_carlo()

            # Backtest
            from archbox.risk.backtest import VaRBacktest

            test_returns = self.returns[-len(var_series[method]) :]
            bt = VaRBacktest(test_returns, var_series[method], alpha=alpha)
            backtest_results[method] = bt

        return RiskAnalysisResult(
            model_name=model,
            alpha=alpha,
            var_series=var_series,
            es_series=es_series,
            backtest_results=backtest_results,
        )

    def save_master_report(
        self,
        path: str,
        theme: str = "professional",
    ) -> None:
        """Save a consolidated master report.

        Parameters
        ----------
        path : str
            Output file path (HTML).
        theme : str
            Report theme.
        """
        from archbox.report.report_manager import ReportManager

        manager = ReportManager()
        manager.generate(
            results=self.fitted_models,
            report_type="garch",
            fmt="html",
            theme=theme,
            output_path=path,
        )
