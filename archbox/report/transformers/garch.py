"""GARCH results transformer for report generation.

Extracts parameters, diagnostics, and visualization data from
fitted GARCH model results.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

import numpy as np


class GARCHTransformer:
    """Transform GARCH results into report template context.

    Extracts:
    - Parameter table (name, value, SE, t-stat, p-value, significance)
    - Persistence, half-life, unconditional variance
    - Information criteria (AIC, BIC, HQIC, loglike)
    - Diagnostics (ARCH-LM, Sign Bias, Ljung-Box z^2)
    - Conditional volatility array
    - News impact curve data
    """

    def transform(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : ArchResults
            Fitted GARCH model results.

        Returns
        -------
        dict
            Template context with all extracted data.
        """
        context: dict[str, Any] = {}

        # Model info
        context["model_name"] = getattr(results, "model_name", "GARCH")
        context["n_obs"] = getattr(results, "nobs", 0)
        context["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Parameters table
        context["params_table"] = self._extract_params_table(results)

        # Persistence and related metrics
        persistence_attr = getattr(results, "persistence", None)
        context["persistence"] = (
            persistence_attr() if callable(persistence_attr) else persistence_attr
        )
        uncond_var_attr = getattr(results, "unconditional_variance", None)
        context["unconditional_variance"] = (
            uncond_var_attr() if callable(uncond_var_attr) else uncond_var_attr
        )
        context["half_life"] = self._compute_half_life(results)

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)
        context["hqic"] = getattr(results, "hqic", None)

        # Diagnostics
        context["diagnostics"] = self._extract_diagnostics(results)

        # Volatility data (for charts)
        if hasattr(results, "conditional_volatility"):
            vol = np.asarray(results.conditional_volatility)
            context["volatility_stats"] = {
                "mean": float(np.mean(vol)),
                "std": float(np.std(vol)),
                "min": float(np.min(vol)),
                "max": float(np.max(vol)),
                "annualized_mean": float(np.mean(vol) * np.sqrt(252)),
            }

        # Residual stats
        if hasattr(results, "std_resid") and results.std_resid is not None:
            z = np.asarray(results.std_resid)
            context["residual_stats"] = {
                "mean": float(np.mean(z)),
                "std": float(np.std(z)),
                "skewness": float(self._skewness(z)),
                "kurtosis": float(self._kurtosis(z)),
            }

        return context

    def _extract_params_table(self, results: Any) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = getattr(results, "param_names", None)
        std_errors = getattr(results, "std_errors", None)
        tvalues = getattr(results, "tvalues", None)
        pvalues = getattr(results, "pvalues", None)

        if params is None:
            return table

        n_params = len(params)
        if param_names is None:
            param_names = [f"param_{i}" for i in range(n_params)]

        for i in range(n_params):
            row: dict[str, Any] = {
                "name": param_names[i] if i < len(param_names) else f"param_{i}",
                "value": float(params[i]),
            }
            if std_errors is not None and i < len(std_errors):
                row["std_error"] = float(std_errors[i])
            if tvalues is not None and i < len(tvalues):
                row["t_stat"] = float(tvalues[i])
            if pvalues is not None and i < len(pvalues):
                row["p_value"] = float(pvalues[i])
                row["significance"] = self._significance_stars(pvalues[i])
            table.append(row)

        return table

    def _extract_diagnostics(self, results: Any) -> dict[str, Any]:
        """Extract diagnostic test results."""
        diag: dict[str, Any] = {}

        # ARCH-LM test
        if hasattr(results, "arch_lm"):
            diag["arch_lm"] = results.arch_lm

        # Ljung-Box on squared residuals
        if hasattr(results, "ljung_box_z2"):
            diag["ljung_box_z2"] = results.ljung_box_z2

        # Sign bias test
        if hasattr(results, "sign_bias"):
            diag["sign_bias"] = results.sign_bias

        return diag

    @staticmethod
    def _compute_half_life(results: Any) -> float | None:
        """Compute half-life of volatility shocks."""
        persistence_attr = getattr(results, "persistence", None)
        raw = persistence_attr() if callable(persistence_attr) else persistence_attr
        if raw is not None:
            persistence = float(raw)  # type: ignore[arg-type]
            if 0 < persistence < 1:
                return float(np.log(0.5) / np.log(persistence))
        return None

    @staticmethod
    def _significance_stars(pvalue: float) -> str:
        """Return significance stars."""
        p = float(pvalue)
        if p < 0.01:
            return "***"
        elif p < 0.05:
            return "**"
        elif p < 0.10:
            return "*"
        return ""

    @staticmethod
    def _skewness(x: Any) -> float:
        """Compute skewness."""
        x = np.asarray(x)
        m3 = np.mean((x - np.mean(x)) ** 3)
        s3 = np.std(x, ddof=1) ** 3
        return float(m3 / s3) if s3 > 0 else 0.0

    @staticmethod
    def _kurtosis(x: Any) -> float:
        """Compute excess kurtosis."""
        x = np.asarray(x)
        m4 = np.mean((x - np.mean(x)) ** 4)
        s4 = np.std(x, ddof=1) ** 4
        return float(m4 / s4 - 3.0) if s4 > 0 else 0.0
