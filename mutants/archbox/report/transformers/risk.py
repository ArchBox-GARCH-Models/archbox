"""Risk analysis results transformer for report generation.

Extracts VaR/ES series, backtest results, violation counts,
traffic light status, and method comparisons.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Annotated, Any, ClassVar

import numpy as np

MutantDict = Annotated[dict[str, Callable], "Mutant"]  # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):  # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os  # type: ignore

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]  # type: ignore
    if mutant_under_test == "fail":  # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException  # type: ignore

        raise MutmutProgrammaticFailException("Failed programmatically")  # type: ignore
    elif mutant_under_test == "stats":  # type: ignore
        from mutmut.__main__ import record_trampoline_hit  # type: ignore

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)  # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs)  # type: ignore
        return result  # type: ignore
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"  # type: ignore
    if not mutant_under_test.startswith(prefix):  # type: ignore
        result = orig(*call_args, **call_kwargs)  # type: ignore
        return result  # type: ignore
    mutant_name = mutant_under_test.rpartition(".")[-1]  # type: ignore
    if self_arg is not None:  # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)  # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)  # type: ignore
    return result  # type: ignore


class RiskTransformer:
    """Transform risk analysis results into report context.

    Extracts:
    - VaR and ES series
    - Backtest results (Kupiec, Christoffersen)
    - Violation counts and ratio
    - Traffic light status
    - Method comparisons
    """

    def transform(self, results: Any) -> dict[str, Any]:
        args = [results]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁRiskTransformerǁtransform__mutmut_orig"),
            object.__getattribute__(self, "xǁRiskTransformerǁtransform__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁRiskTransformerǁtransform__mutmut_orig(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_1(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = None

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_2(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = None
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_3(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["XXmodel_nameXX"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_4(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["MODEL_NAME"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_5(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(None, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_6(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, None, "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_7(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", None)
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_8(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr("model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_9(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_10(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = results.model_name
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_11(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "XXmodel_nameXX", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_12(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "MODEL_NAME", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_13(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "XXRisk AnalysisXX")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_14(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "risk analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_15(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "RISK ANALYSIS")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_16(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = None
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_17(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["XXconfidence_levelXX"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_18(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["CONFIDENCE_LEVEL"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_19(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(None, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_20(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, None, 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_21(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", None)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_22(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr("confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_23(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_24(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = results.confidence_level
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_25(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "XXconfidence_levelXX", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_26(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "CONFIDENCE_LEVEL", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_27(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 1.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_28(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = None

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_29(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["XXn_obsXX"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_30(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["N_OBS"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_31(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            None,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_32(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            None,
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_33(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            None,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_34(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_35(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_36(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = results.nobs

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_37(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "XXnobsXX",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_38(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "NOBS",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_39(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(None, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_40(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, None) else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_41(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr("returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_42(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns)
            if hasattr(
                results,
            )
            else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_43(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "XXreturnsXX") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_44(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "RETURNS") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_45(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 1,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_46(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(None, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_47(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, None):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_48(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr("var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_49(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(
            results,
        ):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_50(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "XXvarXX"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_51(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "VAR"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_52(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = None
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_53(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(None)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_54(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = None

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_55(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["XXvar_statsXX"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_56(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["VAR_STATS"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_57(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "XXmeanXX": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_58(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "MEAN": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_59(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(None),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_60(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(None)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_61(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "XXstdXX": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_62(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "STD": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_63(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(None),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_64(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(None)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_65(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "XXminXX": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_66(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "MIN": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_67(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(None),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_68(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(None)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_69(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "XXmaxXX": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_70(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "MAX": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_71(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(None),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_72(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(None)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_73(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") or results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_74(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(None, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_75(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, None) and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_76(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr("es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_77(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if (
            hasattr(
                results,
            )
            and results.es is not None
        ):
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_78(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "XXesXX") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_79(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "ES") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_80(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_81(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = None
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_82(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(None)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_83(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = None

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_84(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["XXes_statsXX"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_85(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["ES_STATS"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_86(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "XXmeanXX": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_87(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "MEAN": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_88(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(None),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_89(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(None)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_90(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "XXstdXX": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_91(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "STD": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_92(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(None),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_93(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(None)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_94(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "XXminXX": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_95(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "MIN": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_96(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(None),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_97(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(None)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_98(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "XXmaxXX": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_99(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "MAX": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_100(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(None),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_101(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(None)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_102(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = None

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_103(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["XXbacktestXX"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_104(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["BACKTEST"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_105(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(None)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_106(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = None

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_107(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["XXtraffic_lightXX"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_108(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["TRAFFIC_LIGHT"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_109(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(None)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_110(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(None, "comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_111(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, None):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_112(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr("comparison"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_113(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(
            results,
        ):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_114(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "XXcomparisonXX"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_115(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "COMPARISON"):
            context["method_comparison"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_116(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["method_comparison"] = None

        return context

    def xǁRiskTransformerǁtransform__mutmut_117(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["XXmethod_comparisonXX"] = results.comparison

        return context

    def xǁRiskTransformerǁtransform__mutmut_118(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RiskResults or BacktestResults
            Risk analysis results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Risk Analysis")
        context["confidence_level"] = getattr(results, "confidence_level", 0.99)
        context["n_obs"] = getattr(
            results,
            "nobs",
            len(results.returns) if hasattr(results, "returns") else 0,
        )

        # VaR/ES summary statistics
        if hasattr(results, "var"):
            var = np.asarray(results.var)
            context["var_stats"] = {
                "mean": float(np.mean(var)),
                "std": float(np.std(var)),
                "min": float(np.min(var)),
                "max": float(np.max(var)),
            }

        if hasattr(results, "es") and results.es is not None:
            es = np.asarray(results.es)
            context["es_stats"] = {
                "mean": float(np.mean(es)),
                "std": float(np.std(es)),
                "min": float(np.min(es)),
                "max": float(np.max(es)),
            }

        # Backtest results
        context["backtest"] = self._extract_backtest(results)

        # Traffic light
        context["traffic_light"] = self._compute_traffic_light(results)

        # Method comparison (if available)
        if hasattr(results, "comparison"):
            context["METHOD_COMPARISON"] = results.comparison

        return context

    xǁRiskTransformerǁtransform__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁRiskTransformerǁtransform__mutmut_1": xǁRiskTransformerǁtransform__mutmut_1,
        "xǁRiskTransformerǁtransform__mutmut_2": xǁRiskTransformerǁtransform__mutmut_2,
        "xǁRiskTransformerǁtransform__mutmut_3": xǁRiskTransformerǁtransform__mutmut_3,
        "xǁRiskTransformerǁtransform__mutmut_4": xǁRiskTransformerǁtransform__mutmut_4,
        "xǁRiskTransformerǁtransform__mutmut_5": xǁRiskTransformerǁtransform__mutmut_5,
        "xǁRiskTransformerǁtransform__mutmut_6": xǁRiskTransformerǁtransform__mutmut_6,
        "xǁRiskTransformerǁtransform__mutmut_7": xǁRiskTransformerǁtransform__mutmut_7,
        "xǁRiskTransformerǁtransform__mutmut_8": xǁRiskTransformerǁtransform__mutmut_8,
        "xǁRiskTransformerǁtransform__mutmut_9": xǁRiskTransformerǁtransform__mutmut_9,
        "xǁRiskTransformerǁtransform__mutmut_10": xǁRiskTransformerǁtransform__mutmut_10,
        "xǁRiskTransformerǁtransform__mutmut_11": xǁRiskTransformerǁtransform__mutmut_11,
        "xǁRiskTransformerǁtransform__mutmut_12": xǁRiskTransformerǁtransform__mutmut_12,
        "xǁRiskTransformerǁtransform__mutmut_13": xǁRiskTransformerǁtransform__mutmut_13,
        "xǁRiskTransformerǁtransform__mutmut_14": xǁRiskTransformerǁtransform__mutmut_14,
        "xǁRiskTransformerǁtransform__mutmut_15": xǁRiskTransformerǁtransform__mutmut_15,
        "xǁRiskTransformerǁtransform__mutmut_16": xǁRiskTransformerǁtransform__mutmut_16,
        "xǁRiskTransformerǁtransform__mutmut_17": xǁRiskTransformerǁtransform__mutmut_17,
        "xǁRiskTransformerǁtransform__mutmut_18": xǁRiskTransformerǁtransform__mutmut_18,
        "xǁRiskTransformerǁtransform__mutmut_19": xǁRiskTransformerǁtransform__mutmut_19,
        "xǁRiskTransformerǁtransform__mutmut_20": xǁRiskTransformerǁtransform__mutmut_20,
        "xǁRiskTransformerǁtransform__mutmut_21": xǁRiskTransformerǁtransform__mutmut_21,
        "xǁRiskTransformerǁtransform__mutmut_22": xǁRiskTransformerǁtransform__mutmut_22,
        "xǁRiskTransformerǁtransform__mutmut_23": xǁRiskTransformerǁtransform__mutmut_23,
        "xǁRiskTransformerǁtransform__mutmut_24": xǁRiskTransformerǁtransform__mutmut_24,
        "xǁRiskTransformerǁtransform__mutmut_25": xǁRiskTransformerǁtransform__mutmut_25,
        "xǁRiskTransformerǁtransform__mutmut_26": xǁRiskTransformerǁtransform__mutmut_26,
        "xǁRiskTransformerǁtransform__mutmut_27": xǁRiskTransformerǁtransform__mutmut_27,
        "xǁRiskTransformerǁtransform__mutmut_28": xǁRiskTransformerǁtransform__mutmut_28,
        "xǁRiskTransformerǁtransform__mutmut_29": xǁRiskTransformerǁtransform__mutmut_29,
        "xǁRiskTransformerǁtransform__mutmut_30": xǁRiskTransformerǁtransform__mutmut_30,
        "xǁRiskTransformerǁtransform__mutmut_31": xǁRiskTransformerǁtransform__mutmut_31,
        "xǁRiskTransformerǁtransform__mutmut_32": xǁRiskTransformerǁtransform__mutmut_32,
        "xǁRiskTransformerǁtransform__mutmut_33": xǁRiskTransformerǁtransform__mutmut_33,
        "xǁRiskTransformerǁtransform__mutmut_34": xǁRiskTransformerǁtransform__mutmut_34,
        "xǁRiskTransformerǁtransform__mutmut_35": xǁRiskTransformerǁtransform__mutmut_35,
        "xǁRiskTransformerǁtransform__mutmut_36": xǁRiskTransformerǁtransform__mutmut_36,
        "xǁRiskTransformerǁtransform__mutmut_37": xǁRiskTransformerǁtransform__mutmut_37,
        "xǁRiskTransformerǁtransform__mutmut_38": xǁRiskTransformerǁtransform__mutmut_38,
        "xǁRiskTransformerǁtransform__mutmut_39": xǁRiskTransformerǁtransform__mutmut_39,
        "xǁRiskTransformerǁtransform__mutmut_40": xǁRiskTransformerǁtransform__mutmut_40,
        "xǁRiskTransformerǁtransform__mutmut_41": xǁRiskTransformerǁtransform__mutmut_41,
        "xǁRiskTransformerǁtransform__mutmut_42": xǁRiskTransformerǁtransform__mutmut_42,
        "xǁRiskTransformerǁtransform__mutmut_43": xǁRiskTransformerǁtransform__mutmut_43,
        "xǁRiskTransformerǁtransform__mutmut_44": xǁRiskTransformerǁtransform__mutmut_44,
        "xǁRiskTransformerǁtransform__mutmut_45": xǁRiskTransformerǁtransform__mutmut_45,
        "xǁRiskTransformerǁtransform__mutmut_46": xǁRiskTransformerǁtransform__mutmut_46,
        "xǁRiskTransformerǁtransform__mutmut_47": xǁRiskTransformerǁtransform__mutmut_47,
        "xǁRiskTransformerǁtransform__mutmut_48": xǁRiskTransformerǁtransform__mutmut_48,
        "xǁRiskTransformerǁtransform__mutmut_49": xǁRiskTransformerǁtransform__mutmut_49,
        "xǁRiskTransformerǁtransform__mutmut_50": xǁRiskTransformerǁtransform__mutmut_50,
        "xǁRiskTransformerǁtransform__mutmut_51": xǁRiskTransformerǁtransform__mutmut_51,
        "xǁRiskTransformerǁtransform__mutmut_52": xǁRiskTransformerǁtransform__mutmut_52,
        "xǁRiskTransformerǁtransform__mutmut_53": xǁRiskTransformerǁtransform__mutmut_53,
        "xǁRiskTransformerǁtransform__mutmut_54": xǁRiskTransformerǁtransform__mutmut_54,
        "xǁRiskTransformerǁtransform__mutmut_55": xǁRiskTransformerǁtransform__mutmut_55,
        "xǁRiskTransformerǁtransform__mutmut_56": xǁRiskTransformerǁtransform__mutmut_56,
        "xǁRiskTransformerǁtransform__mutmut_57": xǁRiskTransformerǁtransform__mutmut_57,
        "xǁRiskTransformerǁtransform__mutmut_58": xǁRiskTransformerǁtransform__mutmut_58,
        "xǁRiskTransformerǁtransform__mutmut_59": xǁRiskTransformerǁtransform__mutmut_59,
        "xǁRiskTransformerǁtransform__mutmut_60": xǁRiskTransformerǁtransform__mutmut_60,
        "xǁRiskTransformerǁtransform__mutmut_61": xǁRiskTransformerǁtransform__mutmut_61,
        "xǁRiskTransformerǁtransform__mutmut_62": xǁRiskTransformerǁtransform__mutmut_62,
        "xǁRiskTransformerǁtransform__mutmut_63": xǁRiskTransformerǁtransform__mutmut_63,
        "xǁRiskTransformerǁtransform__mutmut_64": xǁRiskTransformerǁtransform__mutmut_64,
        "xǁRiskTransformerǁtransform__mutmut_65": xǁRiskTransformerǁtransform__mutmut_65,
        "xǁRiskTransformerǁtransform__mutmut_66": xǁRiskTransformerǁtransform__mutmut_66,
        "xǁRiskTransformerǁtransform__mutmut_67": xǁRiskTransformerǁtransform__mutmut_67,
        "xǁRiskTransformerǁtransform__mutmut_68": xǁRiskTransformerǁtransform__mutmut_68,
        "xǁRiskTransformerǁtransform__mutmut_69": xǁRiskTransformerǁtransform__mutmut_69,
        "xǁRiskTransformerǁtransform__mutmut_70": xǁRiskTransformerǁtransform__mutmut_70,
        "xǁRiskTransformerǁtransform__mutmut_71": xǁRiskTransformerǁtransform__mutmut_71,
        "xǁRiskTransformerǁtransform__mutmut_72": xǁRiskTransformerǁtransform__mutmut_72,
        "xǁRiskTransformerǁtransform__mutmut_73": xǁRiskTransformerǁtransform__mutmut_73,
        "xǁRiskTransformerǁtransform__mutmut_74": xǁRiskTransformerǁtransform__mutmut_74,
        "xǁRiskTransformerǁtransform__mutmut_75": xǁRiskTransformerǁtransform__mutmut_75,
        "xǁRiskTransformerǁtransform__mutmut_76": xǁRiskTransformerǁtransform__mutmut_76,
        "xǁRiskTransformerǁtransform__mutmut_77": xǁRiskTransformerǁtransform__mutmut_77,
        "xǁRiskTransformerǁtransform__mutmut_78": xǁRiskTransformerǁtransform__mutmut_78,
        "xǁRiskTransformerǁtransform__mutmut_79": xǁRiskTransformerǁtransform__mutmut_79,
        "xǁRiskTransformerǁtransform__mutmut_80": xǁRiskTransformerǁtransform__mutmut_80,
        "xǁRiskTransformerǁtransform__mutmut_81": xǁRiskTransformerǁtransform__mutmut_81,
        "xǁRiskTransformerǁtransform__mutmut_82": xǁRiskTransformerǁtransform__mutmut_82,
        "xǁRiskTransformerǁtransform__mutmut_83": xǁRiskTransformerǁtransform__mutmut_83,
        "xǁRiskTransformerǁtransform__mutmut_84": xǁRiskTransformerǁtransform__mutmut_84,
        "xǁRiskTransformerǁtransform__mutmut_85": xǁRiskTransformerǁtransform__mutmut_85,
        "xǁRiskTransformerǁtransform__mutmut_86": xǁRiskTransformerǁtransform__mutmut_86,
        "xǁRiskTransformerǁtransform__mutmut_87": xǁRiskTransformerǁtransform__mutmut_87,
        "xǁRiskTransformerǁtransform__mutmut_88": xǁRiskTransformerǁtransform__mutmut_88,
        "xǁRiskTransformerǁtransform__mutmut_89": xǁRiskTransformerǁtransform__mutmut_89,
        "xǁRiskTransformerǁtransform__mutmut_90": xǁRiskTransformerǁtransform__mutmut_90,
        "xǁRiskTransformerǁtransform__mutmut_91": xǁRiskTransformerǁtransform__mutmut_91,
        "xǁRiskTransformerǁtransform__mutmut_92": xǁRiskTransformerǁtransform__mutmut_92,
        "xǁRiskTransformerǁtransform__mutmut_93": xǁRiskTransformerǁtransform__mutmut_93,
        "xǁRiskTransformerǁtransform__mutmut_94": xǁRiskTransformerǁtransform__mutmut_94,
        "xǁRiskTransformerǁtransform__mutmut_95": xǁRiskTransformerǁtransform__mutmut_95,
        "xǁRiskTransformerǁtransform__mutmut_96": xǁRiskTransformerǁtransform__mutmut_96,
        "xǁRiskTransformerǁtransform__mutmut_97": xǁRiskTransformerǁtransform__mutmut_97,
        "xǁRiskTransformerǁtransform__mutmut_98": xǁRiskTransformerǁtransform__mutmut_98,
        "xǁRiskTransformerǁtransform__mutmut_99": xǁRiskTransformerǁtransform__mutmut_99,
        "xǁRiskTransformerǁtransform__mutmut_100": xǁRiskTransformerǁtransform__mutmut_100,
        "xǁRiskTransformerǁtransform__mutmut_101": xǁRiskTransformerǁtransform__mutmut_101,
        "xǁRiskTransformerǁtransform__mutmut_102": xǁRiskTransformerǁtransform__mutmut_102,
        "xǁRiskTransformerǁtransform__mutmut_103": xǁRiskTransformerǁtransform__mutmut_103,
        "xǁRiskTransformerǁtransform__mutmut_104": xǁRiskTransformerǁtransform__mutmut_104,
        "xǁRiskTransformerǁtransform__mutmut_105": xǁRiskTransformerǁtransform__mutmut_105,
        "xǁRiskTransformerǁtransform__mutmut_106": xǁRiskTransformerǁtransform__mutmut_106,
        "xǁRiskTransformerǁtransform__mutmut_107": xǁRiskTransformerǁtransform__mutmut_107,
        "xǁRiskTransformerǁtransform__mutmut_108": xǁRiskTransformerǁtransform__mutmut_108,
        "xǁRiskTransformerǁtransform__mutmut_109": xǁRiskTransformerǁtransform__mutmut_109,
        "xǁRiskTransformerǁtransform__mutmut_110": xǁRiskTransformerǁtransform__mutmut_110,
        "xǁRiskTransformerǁtransform__mutmut_111": xǁRiskTransformerǁtransform__mutmut_111,
        "xǁRiskTransformerǁtransform__mutmut_112": xǁRiskTransformerǁtransform__mutmut_112,
        "xǁRiskTransformerǁtransform__mutmut_113": xǁRiskTransformerǁtransform__mutmut_113,
        "xǁRiskTransformerǁtransform__mutmut_114": xǁRiskTransformerǁtransform__mutmut_114,
        "xǁRiskTransformerǁtransform__mutmut_115": xǁRiskTransformerǁtransform__mutmut_115,
        "xǁRiskTransformerǁtransform__mutmut_116": xǁRiskTransformerǁtransform__mutmut_116,
        "xǁRiskTransformerǁtransform__mutmut_117": xǁRiskTransformerǁtransform__mutmut_117,
        "xǁRiskTransformerǁtransform__mutmut_118": xǁRiskTransformerǁtransform__mutmut_118,
    }
    xǁRiskTransformerǁtransform__mutmut_orig.__name__ = "xǁRiskTransformerǁtransform"

    def _extract_backtest(self, results: Any) -> dict[str, Any]:
        args = [results]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁRiskTransformerǁ_extract_backtest__mutmut_orig"),
            object.__getattribute__(self, "xǁRiskTransformerǁ_extract_backtest__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁRiskTransformerǁ_extract_backtest__mutmut_orig(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_1(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = None

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_2(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(None, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_3(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, None):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_4(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr("violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_5(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(
            results,
        ):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_6(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "XXviolationsXX"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_7(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "VIOLATIONS"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_8(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = None
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_9(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(None, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_10(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=None)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_11(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_12(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(
                results.violations,
            )
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_13(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = None
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_14(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(None)
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_15(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(None))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_16(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = None
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_17(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = None
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_18(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(None, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_19(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, None, 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_20(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", None)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_21(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr("confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_22(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_23(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = results.confidence_level
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_24(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "XXconfidence_levelXX", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_25(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "CONFIDENCE_LEVEL", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_26(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 1.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_27(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = None

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_28(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs / (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_29(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 + cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_30(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (2 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_31(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = None
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_32(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["XXn_violationsXX"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_33(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["N_VIOLATIONS"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_34(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = None
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_35(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["XXn_observationsXX"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_36(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["N_OBSERVATIONS"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_37(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = None
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_38(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["XXexpected_violationsXX"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_39(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["EXPECTED_VIOLATIONS"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_40(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(None)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_41(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = None

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_42(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["XXviolation_ratioXX"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_43(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["VIOLATION_RATIO"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_44(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations * expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_45(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected >= 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_46(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 1 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_47(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 1.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_48(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(None, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_49(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, None):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_50(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr("kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_51(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(
            results,
        ):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_52(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "XXkupiecXX"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_53(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "KUPIEC"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_54(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = None

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_55(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["XXkupiecXX"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_56(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["KUPIEC"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_57(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(None, "christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_58(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, None):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_59(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr("christoffersen"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_60(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(
            results,
        ):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_61(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "XXchristoffersenXX"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_62(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "CHRISTOFFERSEN"):
            bt["christoffersen"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_63(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["christoffersen"] = None

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_64(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["XXchristoffersenXX"] = results.christoffersen

        return bt

    def xǁRiskTransformerǁ_extract_backtest__mutmut_65(self, results: Any) -> dict[str, Any]:
        """Extract backtest test results."""
        bt: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)
            cl = getattr(results, "confidence_level", 0.99)
            expected = n_obs * (1 - cl)

            bt["n_violations"] = n_violations
            bt["n_observations"] = n_obs
            bt["expected_violations"] = float(expected)
            bt["violation_ratio"] = n_violations / expected if expected > 0 else 0.0

        # Kupiec test
        if hasattr(results, "kupiec"):
            bt["kupiec"] = results.kupiec

        # Christoffersen test
        if hasattr(results, "christoffersen"):
            bt["CHRISTOFFERSEN"] = results.christoffersen

        return bt

    xǁRiskTransformerǁ_extract_backtest__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁRiskTransformerǁ_extract_backtest__mutmut_1": xǁRiskTransformerǁ_extract_backtest__mutmut_1,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_2": xǁRiskTransformerǁ_extract_backtest__mutmut_2,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_3": xǁRiskTransformerǁ_extract_backtest__mutmut_3,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_4": xǁRiskTransformerǁ_extract_backtest__mutmut_4,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_5": xǁRiskTransformerǁ_extract_backtest__mutmut_5,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_6": xǁRiskTransformerǁ_extract_backtest__mutmut_6,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_7": xǁRiskTransformerǁ_extract_backtest__mutmut_7,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_8": xǁRiskTransformerǁ_extract_backtest__mutmut_8,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_9": xǁRiskTransformerǁ_extract_backtest__mutmut_9,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_10": xǁRiskTransformerǁ_extract_backtest__mutmut_10,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_11": xǁRiskTransformerǁ_extract_backtest__mutmut_11,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_12": xǁRiskTransformerǁ_extract_backtest__mutmut_12,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_13": xǁRiskTransformerǁ_extract_backtest__mutmut_13,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_14": xǁRiskTransformerǁ_extract_backtest__mutmut_14,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_15": xǁRiskTransformerǁ_extract_backtest__mutmut_15,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_16": xǁRiskTransformerǁ_extract_backtest__mutmut_16,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_17": xǁRiskTransformerǁ_extract_backtest__mutmut_17,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_18": xǁRiskTransformerǁ_extract_backtest__mutmut_18,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_19": xǁRiskTransformerǁ_extract_backtest__mutmut_19,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_20": xǁRiskTransformerǁ_extract_backtest__mutmut_20,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_21": xǁRiskTransformerǁ_extract_backtest__mutmut_21,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_22": xǁRiskTransformerǁ_extract_backtest__mutmut_22,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_23": xǁRiskTransformerǁ_extract_backtest__mutmut_23,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_24": xǁRiskTransformerǁ_extract_backtest__mutmut_24,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_25": xǁRiskTransformerǁ_extract_backtest__mutmut_25,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_26": xǁRiskTransformerǁ_extract_backtest__mutmut_26,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_27": xǁRiskTransformerǁ_extract_backtest__mutmut_27,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_28": xǁRiskTransformerǁ_extract_backtest__mutmut_28,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_29": xǁRiskTransformerǁ_extract_backtest__mutmut_29,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_30": xǁRiskTransformerǁ_extract_backtest__mutmut_30,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_31": xǁRiskTransformerǁ_extract_backtest__mutmut_31,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_32": xǁRiskTransformerǁ_extract_backtest__mutmut_32,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_33": xǁRiskTransformerǁ_extract_backtest__mutmut_33,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_34": xǁRiskTransformerǁ_extract_backtest__mutmut_34,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_35": xǁRiskTransformerǁ_extract_backtest__mutmut_35,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_36": xǁRiskTransformerǁ_extract_backtest__mutmut_36,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_37": xǁRiskTransformerǁ_extract_backtest__mutmut_37,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_38": xǁRiskTransformerǁ_extract_backtest__mutmut_38,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_39": xǁRiskTransformerǁ_extract_backtest__mutmut_39,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_40": xǁRiskTransformerǁ_extract_backtest__mutmut_40,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_41": xǁRiskTransformerǁ_extract_backtest__mutmut_41,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_42": xǁRiskTransformerǁ_extract_backtest__mutmut_42,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_43": xǁRiskTransformerǁ_extract_backtest__mutmut_43,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_44": xǁRiskTransformerǁ_extract_backtest__mutmut_44,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_45": xǁRiskTransformerǁ_extract_backtest__mutmut_45,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_46": xǁRiskTransformerǁ_extract_backtest__mutmut_46,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_47": xǁRiskTransformerǁ_extract_backtest__mutmut_47,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_48": xǁRiskTransformerǁ_extract_backtest__mutmut_48,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_49": xǁRiskTransformerǁ_extract_backtest__mutmut_49,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_50": xǁRiskTransformerǁ_extract_backtest__mutmut_50,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_51": xǁRiskTransformerǁ_extract_backtest__mutmut_51,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_52": xǁRiskTransformerǁ_extract_backtest__mutmut_52,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_53": xǁRiskTransformerǁ_extract_backtest__mutmut_53,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_54": xǁRiskTransformerǁ_extract_backtest__mutmut_54,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_55": xǁRiskTransformerǁ_extract_backtest__mutmut_55,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_56": xǁRiskTransformerǁ_extract_backtest__mutmut_56,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_57": xǁRiskTransformerǁ_extract_backtest__mutmut_57,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_58": xǁRiskTransformerǁ_extract_backtest__mutmut_58,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_59": xǁRiskTransformerǁ_extract_backtest__mutmut_59,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_60": xǁRiskTransformerǁ_extract_backtest__mutmut_60,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_61": xǁRiskTransformerǁ_extract_backtest__mutmut_61,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_62": xǁRiskTransformerǁ_extract_backtest__mutmut_62,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_63": xǁRiskTransformerǁ_extract_backtest__mutmut_63,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_64": xǁRiskTransformerǁ_extract_backtest__mutmut_64,
        "xǁRiskTransformerǁ_extract_backtest__mutmut_65": xǁRiskTransformerǁ_extract_backtest__mutmut_65,
    }
    xǁRiskTransformerǁ_extract_backtest__mutmut_orig.__name__ = (
        "xǁRiskTransformerǁ_extract_backtest"
    )

    @staticmethod
    def _compute_traffic_light(results: Any) -> dict[str, Any]:
        """Compute Basel traffic light zone.

        Green: violations <= 4 (for 250 obs at 99%)
        Yellow: 5-9 violations
        Red: >= 10 violations
        """
        tl: dict[str, Any] = {}

        if hasattr(results, "violations"):
            violations = np.asarray(results.violations, dtype=bool)
            n_violations = int(np.sum(violations))
            n_obs = len(violations)

            # Scale thresholds based on sample size relative to 250
            scale = n_obs / 250
            green_max = int(4 * scale)
            yellow_max = int(9 * scale)

            if n_violations <= green_max:
                tl["zone"] = "green"
                tl["status"] = "Accurate"
            elif n_violations <= yellow_max:
                tl["zone"] = "yellow"
                tl["status"] = "Acceptable"
            else:
                tl["zone"] = "red"
                tl["status"] = "Inaccurate"

            tl["n_violations"] = n_violations
            tl["thresholds"] = {"green": green_max, "yellow": yellow_max}

        return tl
