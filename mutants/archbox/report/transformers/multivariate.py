"""Multivariate GARCH results transformer for report generation.

Extends GARCH transformer with DCC/BEKK-specific data extraction.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Annotated, Any, ClassVar

import numpy as np

from archbox.report.transformers.garch import GARCHTransformer

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


class MultivariateTransformer:
    """Transform multivariate GARCH results into report context.

    Extracts everything from GARCHTransformer (per series) plus:
    - DCC/BEKK parameters
    - Dynamic correlations summary
    - Portfolio metrics
    """

    def __init__(self) -> None:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMultivariateTransformerǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁMultivariateTransformerǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMultivariateTransformerǁ__init____mutmut_orig(self) -> None:
        """Initialize multivariate transformer with GARCH sub-transformer."""
        self._garch_transformer = GARCHTransformer()

    def xǁMultivariateTransformerǁ__init____mutmut_1(self) -> None:
        """Initialize multivariate transformer with GARCH sub-transformer."""
        self._garch_transformer = None

    xǁMultivariateTransformerǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMultivariateTransformerǁ__init____mutmut_1": xǁMultivariateTransformerǁ__init____mutmut_1
    }
    xǁMultivariateTransformerǁ__init____mutmut_orig.__name__ = "xǁMultivariateTransformerǁ__init__"

    def transform(self, results: Any) -> dict[str, Any]:
        args = [results]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMultivariateTransformerǁtransform__mutmut_orig"),
            object.__getattribute__(self, "xǁMultivariateTransformerǁtransform__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMultivariateTransformerǁtransform__mutmut_orig(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_1(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = None

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_2(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = None
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_3(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["XXmodel_nameXX"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_4(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["MODEL_NAME"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_5(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(None, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_6(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, None, "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_7(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", None)
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_8(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr("model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_9(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_10(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = results.model_name
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_11(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "XXmodel_nameXX", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_12(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "MODEL_NAME", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_13(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "XXDCC-GARCHXX")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_14(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "dcc-garch")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_15(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = None
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_16(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["XXn_seriesXX"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_17(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["N_SERIES"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_18(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(None, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_19(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, None, 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_20(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", None)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_21(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr("n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_22(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_23(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = results.n_series
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_24(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "XXn_seriesXX", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_25(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "N_SERIES", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_26(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 1)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_27(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = None
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_28(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["XXseries_namesXX"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_29(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["SERIES_NAMES"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_30(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(None, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_31(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, None, [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_32(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", None)
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_33(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr("series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_34(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_35(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = results.series_names
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_36(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "XXseries_namesXX", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_37(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "SERIES_NAMES", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_38(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = None

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_39(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["XXn_obsXX"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_40(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["N_OBS"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_41(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(None, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_42(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, None, 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_43(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", None)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_44(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr("nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_45(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_46(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = results.nobs

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_47(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "XXnobsXX", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_48(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "NOBS", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_49(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 1)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_50(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(None, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_51(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, None):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_52(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr("univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_53(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(
            results,
        ):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_54(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "XXunivariate_resultsXX"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_55(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "UNIVARIATE_RESULTS"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_56(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = None
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_57(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["XXseries_paramsXX"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_58(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["SERIES_PARAMS"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_59(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(None):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_60(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = None
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_61(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(None)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_62(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = None
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_63(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["XXseries_indexXX"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_64(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["SERIES_INDEX"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_65(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = None
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_66(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["XXseries_namesXX"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_67(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["SERIES_NAMES"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_68(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i <= len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_69(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = None
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_70(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["XXseries_nameXX"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_71(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["SERIES_NAME"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_72(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(None)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_73(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["XXseries_paramsXX"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_74(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["SERIES_PARAMS"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_75(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = None

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_76(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["XXcorrelation_paramsXX"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_77(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["CORRELATION_PARAMS"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_78(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(None)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_79(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(None, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_80(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, None):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_81(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr("dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_82(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(
            results,
        ):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_83(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "XXdynamic_correlationsXX"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_84(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "DYNAMIC_CORRELATIONS"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_85(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = None
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_86(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(None)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_87(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = None
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_88(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[2]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_89(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = None
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_90(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(None):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_91(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(None, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_92(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, None):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_93(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_94(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(
                    i + 1,
                ):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_95(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i - 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_96(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 2, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_97(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = None
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_98(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = None
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_99(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["XXseries_namesXX"][i]
                        if i < len(context["series_names"])
                        else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_100(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["SERIES_NAMES"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_101(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i <= len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_102(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = None
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_103(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["XXseries_namesXX"][j]
                        if j < len(context["series_names"])
                        else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_104(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["SERIES_NAMES"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_105(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j <= len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_106(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(None)
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_107(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "XXpairXX": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_108(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "PAIR": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_109(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "XXmeanXX": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_110(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "MEAN": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_111(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(None),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_112(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(None)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_113(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "XXstdXX": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_114(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "STD": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_115(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(None),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_116(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(None)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_117(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "XXminXX": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_118(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "MIN": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_119(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(None),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_120(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(None)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_121(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "XXmaxXX": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_122(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "MAX": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_123(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(None),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_124(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(None)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_125(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = None

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_126(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["XXcorrelation_summaryXX"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_127(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["CORRELATION_SUMMARY"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_128(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = None
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_129(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["XXloglikelihoodXX"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_130(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["LOGLIKELIHOOD"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_131(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(None, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_132(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, None, None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_133(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr("loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_134(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_135(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = results.loglikelihood
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_136(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "XXloglikelihoodXX", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_137(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "LOGLIKELIHOOD", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_138(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = None
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_139(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["XXaicXX"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_140(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["AIC"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_141(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(None, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_142(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, None, None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_143(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr("aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_144(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_145(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = results.aic
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_146(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "XXaicXX", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_147(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "AIC", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_148(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = None

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_149(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["XXbicXX"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_150(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["BIC"] = getattr(results, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_151(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(None, "bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_152(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, None, None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_153(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr("bic", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_154(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_155(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = results.bic

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_156(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "XXbicXX", None)

        return context

    def xǁMultivariateTransformerǁtransform__mutmut_157(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : MultivariateResults
            Fitted multivariate model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "DCC-GARCH")
        context["n_series"] = getattr(results, "n_series", 0)
        context["series_names"] = getattr(results, "series_names", [])
        context["n_obs"] = getattr(results, "nobs", 0)

        # Per-series parameters (if available)
        if hasattr(results, "univariate_results"):
            context["series_params"] = []
            for i, uni_result in enumerate(results.univariate_results):
                series_ctx = self._garch_transformer.transform(uni_result)
                series_ctx["series_index"] = i
                name = (
                    context["series_names"][i]
                    if i < len(context["series_names"])
                    else f"Series {i}"
                )
                series_ctx["series_name"] = name
                context["series_params"].append(series_ctx)

        # DCC/BEKK specific parameters
        context["correlation_params"] = self._extract_correlation_params(results)

        # Correlation summary
        if hasattr(results, "dynamic_correlations"):
            corr = np.asarray(results.dynamic_correlations)
            n_assets = corr.shape[1]
            corr_summary = []
            for i in range(n_assets):
                for j in range(i + 1, n_assets):
                    rho_ij = corr[:, i, j]
                    name_i = (
                        context["series_names"][i] if i < len(context["series_names"]) else f"S{i}"
                    )
                    name_j = (
                        context["series_names"][j] if j < len(context["series_names"]) else f"S{j}"
                    )
                    corr_summary.append(
                        {
                            "pair": f"{name_i}-{name_j}",
                            "mean": float(np.mean(rho_ij)),
                            "std": float(np.std(rho_ij)),
                            "min": float(np.min(rho_ij)),
                            "max": float(np.max(rho_ij)),
                        }
                    )
            context["correlation_summary"] = corr_summary

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "BIC", None)

        return context

    xǁMultivariateTransformerǁtransform__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMultivariateTransformerǁtransform__mutmut_1": xǁMultivariateTransformerǁtransform__mutmut_1,
        "xǁMultivariateTransformerǁtransform__mutmut_2": xǁMultivariateTransformerǁtransform__mutmut_2,
        "xǁMultivariateTransformerǁtransform__mutmut_3": xǁMultivariateTransformerǁtransform__mutmut_3,
        "xǁMultivariateTransformerǁtransform__mutmut_4": xǁMultivariateTransformerǁtransform__mutmut_4,
        "xǁMultivariateTransformerǁtransform__mutmut_5": xǁMultivariateTransformerǁtransform__mutmut_5,
        "xǁMultivariateTransformerǁtransform__mutmut_6": xǁMultivariateTransformerǁtransform__mutmut_6,
        "xǁMultivariateTransformerǁtransform__mutmut_7": xǁMultivariateTransformerǁtransform__mutmut_7,
        "xǁMultivariateTransformerǁtransform__mutmut_8": xǁMultivariateTransformerǁtransform__mutmut_8,
        "xǁMultivariateTransformerǁtransform__mutmut_9": xǁMultivariateTransformerǁtransform__mutmut_9,
        "xǁMultivariateTransformerǁtransform__mutmut_10": xǁMultivariateTransformerǁtransform__mutmut_10,
        "xǁMultivariateTransformerǁtransform__mutmut_11": xǁMultivariateTransformerǁtransform__mutmut_11,
        "xǁMultivariateTransformerǁtransform__mutmut_12": xǁMultivariateTransformerǁtransform__mutmut_12,
        "xǁMultivariateTransformerǁtransform__mutmut_13": xǁMultivariateTransformerǁtransform__mutmut_13,
        "xǁMultivariateTransformerǁtransform__mutmut_14": xǁMultivariateTransformerǁtransform__mutmut_14,
        "xǁMultivariateTransformerǁtransform__mutmut_15": xǁMultivariateTransformerǁtransform__mutmut_15,
        "xǁMultivariateTransformerǁtransform__mutmut_16": xǁMultivariateTransformerǁtransform__mutmut_16,
        "xǁMultivariateTransformerǁtransform__mutmut_17": xǁMultivariateTransformerǁtransform__mutmut_17,
        "xǁMultivariateTransformerǁtransform__mutmut_18": xǁMultivariateTransformerǁtransform__mutmut_18,
        "xǁMultivariateTransformerǁtransform__mutmut_19": xǁMultivariateTransformerǁtransform__mutmut_19,
        "xǁMultivariateTransformerǁtransform__mutmut_20": xǁMultivariateTransformerǁtransform__mutmut_20,
        "xǁMultivariateTransformerǁtransform__mutmut_21": xǁMultivariateTransformerǁtransform__mutmut_21,
        "xǁMultivariateTransformerǁtransform__mutmut_22": xǁMultivariateTransformerǁtransform__mutmut_22,
        "xǁMultivariateTransformerǁtransform__mutmut_23": xǁMultivariateTransformerǁtransform__mutmut_23,
        "xǁMultivariateTransformerǁtransform__mutmut_24": xǁMultivariateTransformerǁtransform__mutmut_24,
        "xǁMultivariateTransformerǁtransform__mutmut_25": xǁMultivariateTransformerǁtransform__mutmut_25,
        "xǁMultivariateTransformerǁtransform__mutmut_26": xǁMultivariateTransformerǁtransform__mutmut_26,
        "xǁMultivariateTransformerǁtransform__mutmut_27": xǁMultivariateTransformerǁtransform__mutmut_27,
        "xǁMultivariateTransformerǁtransform__mutmut_28": xǁMultivariateTransformerǁtransform__mutmut_28,
        "xǁMultivariateTransformerǁtransform__mutmut_29": xǁMultivariateTransformerǁtransform__mutmut_29,
        "xǁMultivariateTransformerǁtransform__mutmut_30": xǁMultivariateTransformerǁtransform__mutmut_30,
        "xǁMultivariateTransformerǁtransform__mutmut_31": xǁMultivariateTransformerǁtransform__mutmut_31,
        "xǁMultivariateTransformerǁtransform__mutmut_32": xǁMultivariateTransformerǁtransform__mutmut_32,
        "xǁMultivariateTransformerǁtransform__mutmut_33": xǁMultivariateTransformerǁtransform__mutmut_33,
        "xǁMultivariateTransformerǁtransform__mutmut_34": xǁMultivariateTransformerǁtransform__mutmut_34,
        "xǁMultivariateTransformerǁtransform__mutmut_35": xǁMultivariateTransformerǁtransform__mutmut_35,
        "xǁMultivariateTransformerǁtransform__mutmut_36": xǁMultivariateTransformerǁtransform__mutmut_36,
        "xǁMultivariateTransformerǁtransform__mutmut_37": xǁMultivariateTransformerǁtransform__mutmut_37,
        "xǁMultivariateTransformerǁtransform__mutmut_38": xǁMultivariateTransformerǁtransform__mutmut_38,
        "xǁMultivariateTransformerǁtransform__mutmut_39": xǁMultivariateTransformerǁtransform__mutmut_39,
        "xǁMultivariateTransformerǁtransform__mutmut_40": xǁMultivariateTransformerǁtransform__mutmut_40,
        "xǁMultivariateTransformerǁtransform__mutmut_41": xǁMultivariateTransformerǁtransform__mutmut_41,
        "xǁMultivariateTransformerǁtransform__mutmut_42": xǁMultivariateTransformerǁtransform__mutmut_42,
        "xǁMultivariateTransformerǁtransform__mutmut_43": xǁMultivariateTransformerǁtransform__mutmut_43,
        "xǁMultivariateTransformerǁtransform__mutmut_44": xǁMultivariateTransformerǁtransform__mutmut_44,
        "xǁMultivariateTransformerǁtransform__mutmut_45": xǁMultivariateTransformerǁtransform__mutmut_45,
        "xǁMultivariateTransformerǁtransform__mutmut_46": xǁMultivariateTransformerǁtransform__mutmut_46,
        "xǁMultivariateTransformerǁtransform__mutmut_47": xǁMultivariateTransformerǁtransform__mutmut_47,
        "xǁMultivariateTransformerǁtransform__mutmut_48": xǁMultivariateTransformerǁtransform__mutmut_48,
        "xǁMultivariateTransformerǁtransform__mutmut_49": xǁMultivariateTransformerǁtransform__mutmut_49,
        "xǁMultivariateTransformerǁtransform__mutmut_50": xǁMultivariateTransformerǁtransform__mutmut_50,
        "xǁMultivariateTransformerǁtransform__mutmut_51": xǁMultivariateTransformerǁtransform__mutmut_51,
        "xǁMultivariateTransformerǁtransform__mutmut_52": xǁMultivariateTransformerǁtransform__mutmut_52,
        "xǁMultivariateTransformerǁtransform__mutmut_53": xǁMultivariateTransformerǁtransform__mutmut_53,
        "xǁMultivariateTransformerǁtransform__mutmut_54": xǁMultivariateTransformerǁtransform__mutmut_54,
        "xǁMultivariateTransformerǁtransform__mutmut_55": xǁMultivariateTransformerǁtransform__mutmut_55,
        "xǁMultivariateTransformerǁtransform__mutmut_56": xǁMultivariateTransformerǁtransform__mutmut_56,
        "xǁMultivariateTransformerǁtransform__mutmut_57": xǁMultivariateTransformerǁtransform__mutmut_57,
        "xǁMultivariateTransformerǁtransform__mutmut_58": xǁMultivariateTransformerǁtransform__mutmut_58,
        "xǁMultivariateTransformerǁtransform__mutmut_59": xǁMultivariateTransformerǁtransform__mutmut_59,
        "xǁMultivariateTransformerǁtransform__mutmut_60": xǁMultivariateTransformerǁtransform__mutmut_60,
        "xǁMultivariateTransformerǁtransform__mutmut_61": xǁMultivariateTransformerǁtransform__mutmut_61,
        "xǁMultivariateTransformerǁtransform__mutmut_62": xǁMultivariateTransformerǁtransform__mutmut_62,
        "xǁMultivariateTransformerǁtransform__mutmut_63": xǁMultivariateTransformerǁtransform__mutmut_63,
        "xǁMultivariateTransformerǁtransform__mutmut_64": xǁMultivariateTransformerǁtransform__mutmut_64,
        "xǁMultivariateTransformerǁtransform__mutmut_65": xǁMultivariateTransformerǁtransform__mutmut_65,
        "xǁMultivariateTransformerǁtransform__mutmut_66": xǁMultivariateTransformerǁtransform__mutmut_66,
        "xǁMultivariateTransformerǁtransform__mutmut_67": xǁMultivariateTransformerǁtransform__mutmut_67,
        "xǁMultivariateTransformerǁtransform__mutmut_68": xǁMultivariateTransformerǁtransform__mutmut_68,
        "xǁMultivariateTransformerǁtransform__mutmut_69": xǁMultivariateTransformerǁtransform__mutmut_69,
        "xǁMultivariateTransformerǁtransform__mutmut_70": xǁMultivariateTransformerǁtransform__mutmut_70,
        "xǁMultivariateTransformerǁtransform__mutmut_71": xǁMultivariateTransformerǁtransform__mutmut_71,
        "xǁMultivariateTransformerǁtransform__mutmut_72": xǁMultivariateTransformerǁtransform__mutmut_72,
        "xǁMultivariateTransformerǁtransform__mutmut_73": xǁMultivariateTransformerǁtransform__mutmut_73,
        "xǁMultivariateTransformerǁtransform__mutmut_74": xǁMultivariateTransformerǁtransform__mutmut_74,
        "xǁMultivariateTransformerǁtransform__mutmut_75": xǁMultivariateTransformerǁtransform__mutmut_75,
        "xǁMultivariateTransformerǁtransform__mutmut_76": xǁMultivariateTransformerǁtransform__mutmut_76,
        "xǁMultivariateTransformerǁtransform__mutmut_77": xǁMultivariateTransformerǁtransform__mutmut_77,
        "xǁMultivariateTransformerǁtransform__mutmut_78": xǁMultivariateTransformerǁtransform__mutmut_78,
        "xǁMultivariateTransformerǁtransform__mutmut_79": xǁMultivariateTransformerǁtransform__mutmut_79,
        "xǁMultivariateTransformerǁtransform__mutmut_80": xǁMultivariateTransformerǁtransform__mutmut_80,
        "xǁMultivariateTransformerǁtransform__mutmut_81": xǁMultivariateTransformerǁtransform__mutmut_81,
        "xǁMultivariateTransformerǁtransform__mutmut_82": xǁMultivariateTransformerǁtransform__mutmut_82,
        "xǁMultivariateTransformerǁtransform__mutmut_83": xǁMultivariateTransformerǁtransform__mutmut_83,
        "xǁMultivariateTransformerǁtransform__mutmut_84": xǁMultivariateTransformerǁtransform__mutmut_84,
        "xǁMultivariateTransformerǁtransform__mutmut_85": xǁMultivariateTransformerǁtransform__mutmut_85,
        "xǁMultivariateTransformerǁtransform__mutmut_86": xǁMultivariateTransformerǁtransform__mutmut_86,
        "xǁMultivariateTransformerǁtransform__mutmut_87": xǁMultivariateTransformerǁtransform__mutmut_87,
        "xǁMultivariateTransformerǁtransform__mutmut_88": xǁMultivariateTransformerǁtransform__mutmut_88,
        "xǁMultivariateTransformerǁtransform__mutmut_89": xǁMultivariateTransformerǁtransform__mutmut_89,
        "xǁMultivariateTransformerǁtransform__mutmut_90": xǁMultivariateTransformerǁtransform__mutmut_90,
        "xǁMultivariateTransformerǁtransform__mutmut_91": xǁMultivariateTransformerǁtransform__mutmut_91,
        "xǁMultivariateTransformerǁtransform__mutmut_92": xǁMultivariateTransformerǁtransform__mutmut_92,
        "xǁMultivariateTransformerǁtransform__mutmut_93": xǁMultivariateTransformerǁtransform__mutmut_93,
        "xǁMultivariateTransformerǁtransform__mutmut_94": xǁMultivariateTransformerǁtransform__mutmut_94,
        "xǁMultivariateTransformerǁtransform__mutmut_95": xǁMultivariateTransformerǁtransform__mutmut_95,
        "xǁMultivariateTransformerǁtransform__mutmut_96": xǁMultivariateTransformerǁtransform__mutmut_96,
        "xǁMultivariateTransformerǁtransform__mutmut_97": xǁMultivariateTransformerǁtransform__mutmut_97,
        "xǁMultivariateTransformerǁtransform__mutmut_98": xǁMultivariateTransformerǁtransform__mutmut_98,
        "xǁMultivariateTransformerǁtransform__mutmut_99": xǁMultivariateTransformerǁtransform__mutmut_99,
        "xǁMultivariateTransformerǁtransform__mutmut_100": xǁMultivariateTransformerǁtransform__mutmut_100,
        "xǁMultivariateTransformerǁtransform__mutmut_101": xǁMultivariateTransformerǁtransform__mutmut_101,
        "xǁMultivariateTransformerǁtransform__mutmut_102": xǁMultivariateTransformerǁtransform__mutmut_102,
        "xǁMultivariateTransformerǁtransform__mutmut_103": xǁMultivariateTransformerǁtransform__mutmut_103,
        "xǁMultivariateTransformerǁtransform__mutmut_104": xǁMultivariateTransformerǁtransform__mutmut_104,
        "xǁMultivariateTransformerǁtransform__mutmut_105": xǁMultivariateTransformerǁtransform__mutmut_105,
        "xǁMultivariateTransformerǁtransform__mutmut_106": xǁMultivariateTransformerǁtransform__mutmut_106,
        "xǁMultivariateTransformerǁtransform__mutmut_107": xǁMultivariateTransformerǁtransform__mutmut_107,
        "xǁMultivariateTransformerǁtransform__mutmut_108": xǁMultivariateTransformerǁtransform__mutmut_108,
        "xǁMultivariateTransformerǁtransform__mutmut_109": xǁMultivariateTransformerǁtransform__mutmut_109,
        "xǁMultivariateTransformerǁtransform__mutmut_110": xǁMultivariateTransformerǁtransform__mutmut_110,
        "xǁMultivariateTransformerǁtransform__mutmut_111": xǁMultivariateTransformerǁtransform__mutmut_111,
        "xǁMultivariateTransformerǁtransform__mutmut_112": xǁMultivariateTransformerǁtransform__mutmut_112,
        "xǁMultivariateTransformerǁtransform__mutmut_113": xǁMultivariateTransformerǁtransform__mutmut_113,
        "xǁMultivariateTransformerǁtransform__mutmut_114": xǁMultivariateTransformerǁtransform__mutmut_114,
        "xǁMultivariateTransformerǁtransform__mutmut_115": xǁMultivariateTransformerǁtransform__mutmut_115,
        "xǁMultivariateTransformerǁtransform__mutmut_116": xǁMultivariateTransformerǁtransform__mutmut_116,
        "xǁMultivariateTransformerǁtransform__mutmut_117": xǁMultivariateTransformerǁtransform__mutmut_117,
        "xǁMultivariateTransformerǁtransform__mutmut_118": xǁMultivariateTransformerǁtransform__mutmut_118,
        "xǁMultivariateTransformerǁtransform__mutmut_119": xǁMultivariateTransformerǁtransform__mutmut_119,
        "xǁMultivariateTransformerǁtransform__mutmut_120": xǁMultivariateTransformerǁtransform__mutmut_120,
        "xǁMultivariateTransformerǁtransform__mutmut_121": xǁMultivariateTransformerǁtransform__mutmut_121,
        "xǁMultivariateTransformerǁtransform__mutmut_122": xǁMultivariateTransformerǁtransform__mutmut_122,
        "xǁMultivariateTransformerǁtransform__mutmut_123": xǁMultivariateTransformerǁtransform__mutmut_123,
        "xǁMultivariateTransformerǁtransform__mutmut_124": xǁMultivariateTransformerǁtransform__mutmut_124,
        "xǁMultivariateTransformerǁtransform__mutmut_125": xǁMultivariateTransformerǁtransform__mutmut_125,
        "xǁMultivariateTransformerǁtransform__mutmut_126": xǁMultivariateTransformerǁtransform__mutmut_126,
        "xǁMultivariateTransformerǁtransform__mutmut_127": xǁMultivariateTransformerǁtransform__mutmut_127,
        "xǁMultivariateTransformerǁtransform__mutmut_128": xǁMultivariateTransformerǁtransform__mutmut_128,
        "xǁMultivariateTransformerǁtransform__mutmut_129": xǁMultivariateTransformerǁtransform__mutmut_129,
        "xǁMultivariateTransformerǁtransform__mutmut_130": xǁMultivariateTransformerǁtransform__mutmut_130,
        "xǁMultivariateTransformerǁtransform__mutmut_131": xǁMultivariateTransformerǁtransform__mutmut_131,
        "xǁMultivariateTransformerǁtransform__mutmut_132": xǁMultivariateTransformerǁtransform__mutmut_132,
        "xǁMultivariateTransformerǁtransform__mutmut_133": xǁMultivariateTransformerǁtransform__mutmut_133,
        "xǁMultivariateTransformerǁtransform__mutmut_134": xǁMultivariateTransformerǁtransform__mutmut_134,
        "xǁMultivariateTransformerǁtransform__mutmut_135": xǁMultivariateTransformerǁtransform__mutmut_135,
        "xǁMultivariateTransformerǁtransform__mutmut_136": xǁMultivariateTransformerǁtransform__mutmut_136,
        "xǁMultivariateTransformerǁtransform__mutmut_137": xǁMultivariateTransformerǁtransform__mutmut_137,
        "xǁMultivariateTransformerǁtransform__mutmut_138": xǁMultivariateTransformerǁtransform__mutmut_138,
        "xǁMultivariateTransformerǁtransform__mutmut_139": xǁMultivariateTransformerǁtransform__mutmut_139,
        "xǁMultivariateTransformerǁtransform__mutmut_140": xǁMultivariateTransformerǁtransform__mutmut_140,
        "xǁMultivariateTransformerǁtransform__mutmut_141": xǁMultivariateTransformerǁtransform__mutmut_141,
        "xǁMultivariateTransformerǁtransform__mutmut_142": xǁMultivariateTransformerǁtransform__mutmut_142,
        "xǁMultivariateTransformerǁtransform__mutmut_143": xǁMultivariateTransformerǁtransform__mutmut_143,
        "xǁMultivariateTransformerǁtransform__mutmut_144": xǁMultivariateTransformerǁtransform__mutmut_144,
        "xǁMultivariateTransformerǁtransform__mutmut_145": xǁMultivariateTransformerǁtransform__mutmut_145,
        "xǁMultivariateTransformerǁtransform__mutmut_146": xǁMultivariateTransformerǁtransform__mutmut_146,
        "xǁMultivariateTransformerǁtransform__mutmut_147": xǁMultivariateTransformerǁtransform__mutmut_147,
        "xǁMultivariateTransformerǁtransform__mutmut_148": xǁMultivariateTransformerǁtransform__mutmut_148,
        "xǁMultivariateTransformerǁtransform__mutmut_149": xǁMultivariateTransformerǁtransform__mutmut_149,
        "xǁMultivariateTransformerǁtransform__mutmut_150": xǁMultivariateTransformerǁtransform__mutmut_150,
        "xǁMultivariateTransformerǁtransform__mutmut_151": xǁMultivariateTransformerǁtransform__mutmut_151,
        "xǁMultivariateTransformerǁtransform__mutmut_152": xǁMultivariateTransformerǁtransform__mutmut_152,
        "xǁMultivariateTransformerǁtransform__mutmut_153": xǁMultivariateTransformerǁtransform__mutmut_153,
        "xǁMultivariateTransformerǁtransform__mutmut_154": xǁMultivariateTransformerǁtransform__mutmut_154,
        "xǁMultivariateTransformerǁtransform__mutmut_155": xǁMultivariateTransformerǁtransform__mutmut_155,
        "xǁMultivariateTransformerǁtransform__mutmut_156": xǁMultivariateTransformerǁtransform__mutmut_156,
        "xǁMultivariateTransformerǁtransform__mutmut_157": xǁMultivariateTransformerǁtransform__mutmut_157,
    }
    xǁMultivariateTransformerǁtransform__mutmut_orig.__name__ = (
        "xǁMultivariateTransformerǁtransform"
    )

    @staticmethod
    def _extract_correlation_params(results: Any) -> dict[str, Any]:
        """Extract DCC/BEKK correlation model parameters."""
        params: dict[str, Any] = {}
        if hasattr(results, "dcc_a"):
            params["dcc_a"] = float(results.dcc_a)
        if hasattr(results, "dcc_b"):
            params["dcc_b"] = float(results.dcc_b)
        if hasattr(results, "dcc_persistence"):
            params["dcc_persistence"] = float(results.dcc_persistence)
        return params
