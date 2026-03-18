"""Regime-switching results transformer for report generation.

Extracts regime parameters, transition matrix, smoothed probabilities,
expected durations, and regime classification.
"""

from __future__ import annotations

from typing import Any

import numpy as np


class RegimeTransformer:
    """Transform regime-switching results into report context.

    Extracts:
    - Parameters per regime
    - Transition matrix
    - Smoothed probabilities
    - Expected durations
    - Regime classification
    """

    def transform(self, results: Any) -> dict[str, Any]:
        """Transform results to template context.

        Parameters
        ----------
        results : RegimeResults
            Fitted regime-switching model results.

        Returns
        -------
        dict
            Template context.
        """
        context: dict[str, Any] = {}

        context["model_name"] = getattr(results, "model_name", "Markov-Switching")
        context["n_regimes"] = int(getattr(results, "n_regimes", 2))
        context["n_obs"] = getattr(results, "nobs", 0)

        # Transition matrix
        if hasattr(results, "transition_matrix"):
            trans = np.asarray(results.transition_matrix)
            context["transition_matrix"] = trans.tolist()

            # Expected durations: E[D_k] = 1 / (1 - p_kk)
            n_states = trans.shape[0]
            durations = []
            for k in range(n_states):
                d = 1.0 / (1.0 - trans[k, k]) if trans[k, k] < 1 else float("inf")
                durations.append({"regime": k + 1, "duration": d})
            context["expected_durations"] = durations

        # Per-regime parameters
        if hasattr(results, "regime_params"):
            context["regime_params"] = []
            for k, params in enumerate(results.regime_params):
                regime_ctx = {
                    "regime": k + 1,
                    "params": params if isinstance(params, dict) else {"value": params},
                }
                context["regime_params"].append(regime_ctx)

        # Smoothed probabilities summary
        if hasattr(results, "smoothed_probs"):
            probs = np.asarray(results.smoothed_probs)
            n_states = probs.shape[1]
            regime_class = np.argmax(probs, axis=1)
            context["regime_classification"] = {
                "counts": [int(np.sum(regime_class == k)) for k in range(n_states)],
                "proportions": [float(np.mean(regime_class == k)) for k in range(n_states)],
            }

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context
