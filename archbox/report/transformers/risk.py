"""Risk analysis results transformer for report generation.

Extracts VaR/ES series, backtest results, violation counts,
traffic light status, and method comparisons.
"""

from __future__ import annotations

from typing import Any

import numpy as np


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

    def _extract_backtest(self, results: Any) -> dict[str, Any]:
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
