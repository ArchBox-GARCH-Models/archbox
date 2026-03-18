"""Multivariate GARCH results transformer for report generation.

Extends GARCH transformer with DCC/BEKK-specific data extraction.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from archbox.report.transformers.garch import GARCHTransformer


class MultivariateTransformer:
    """Transform multivariate GARCH results into report context.

    Extracts everything from GARCHTransformer (per series) plus:
    - DCC/BEKK parameters
    - Dynamic correlations summary
    - Portfolio metrics
    """

    def __init__(self) -> None:
        """Initialize multivariate transformer with GARCH sub-transformer."""
        self._garch_transformer = GARCHTransformer()

    def transform(self, results: Any) -> dict[str, Any]:
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
