"""Regime-switching results transformer for report generation.

Extracts regime parameters, transition matrix, smoothed probabilities,
expected durations, and regime classification.
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
        args = [results]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁRegimeTransformerǁtransform__mutmut_orig"),
            object.__getattribute__(self, "xǁRegimeTransformerǁtransform__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁRegimeTransformerǁtransform__mutmut_orig(self, results: Any) -> dict[str, Any]:
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

    def xǁRegimeTransformerǁtransform__mutmut_1(self, results: Any) -> dict[str, Any]:
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
        context: dict[str, Any] = None

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

    def xǁRegimeTransformerǁtransform__mutmut_2(self, results: Any) -> dict[str, Any]:
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

        context["model_name"] = None
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

    def xǁRegimeTransformerǁtransform__mutmut_3(self, results: Any) -> dict[str, Any]:
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

        context["XXmodel_nameXX"] = getattr(results, "model_name", "Markov-Switching")
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

    def xǁRegimeTransformerǁtransform__mutmut_4(self, results: Any) -> dict[str, Any]:
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

        context["MODEL_NAME"] = getattr(results, "model_name", "Markov-Switching")
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

    def xǁRegimeTransformerǁtransform__mutmut_5(self, results: Any) -> dict[str, Any]:
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

        context["model_name"] = getattr(None, "model_name", "Markov-Switching")
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

    def xǁRegimeTransformerǁtransform__mutmut_6(self, results: Any) -> dict[str, Any]:
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

        context["model_name"] = getattr(results, None, "Markov-Switching")
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

    def xǁRegimeTransformerǁtransform__mutmut_7(self, results: Any) -> dict[str, Any]:
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

        context["model_name"] = getattr(results, "model_name", None)
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

    def xǁRegimeTransformerǁtransform__mutmut_8(self, results: Any) -> dict[str, Any]:
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

        context["model_name"] = getattr("model_name", "Markov-Switching")
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

    def xǁRegimeTransformerǁtransform__mutmut_9(self, results: Any) -> dict[str, Any]:
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

        context["model_name"] = getattr(results, "Markov-Switching")
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

    def xǁRegimeTransformerǁtransform__mutmut_10(self, results: Any) -> dict[str, Any]:
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

        context["model_name"] = results.model_name
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

    def xǁRegimeTransformerǁtransform__mutmut_11(self, results: Any) -> dict[str, Any]:
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

        context["model_name"] = getattr(results, "XXmodel_nameXX", "Markov-Switching")
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

    def xǁRegimeTransformerǁtransform__mutmut_12(self, results: Any) -> dict[str, Any]:
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

        context["model_name"] = getattr(results, "MODEL_NAME", "Markov-Switching")
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

    def xǁRegimeTransformerǁtransform__mutmut_13(self, results: Any) -> dict[str, Any]:
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

        context["model_name"] = getattr(results, "model_name", "XXMarkov-SwitchingXX")
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

    def xǁRegimeTransformerǁtransform__mutmut_14(self, results: Any) -> dict[str, Any]:
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

        context["model_name"] = getattr(results, "model_name", "markov-switching")
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

    def xǁRegimeTransformerǁtransform__mutmut_15(self, results: Any) -> dict[str, Any]:
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

        context["model_name"] = getattr(results, "model_name", "MARKOV-SWITCHING")
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

    def xǁRegimeTransformerǁtransform__mutmut_16(self, results: Any) -> dict[str, Any]:
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
        context["n_regimes"] = None
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

    def xǁRegimeTransformerǁtransform__mutmut_17(self, results: Any) -> dict[str, Any]:
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
        context["XXn_regimesXX"] = int(getattr(results, "n_regimes", 2))
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

    def xǁRegimeTransformerǁtransform__mutmut_18(self, results: Any) -> dict[str, Any]:
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
        context["N_REGIMES"] = int(getattr(results, "n_regimes", 2))
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

    def xǁRegimeTransformerǁtransform__mutmut_19(self, results: Any) -> dict[str, Any]:
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
        context["n_regimes"] = int(None)
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

    def xǁRegimeTransformerǁtransform__mutmut_20(self, results: Any) -> dict[str, Any]:
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
        context["n_regimes"] = int(getattr(None, "n_regimes", 2))
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

    def xǁRegimeTransformerǁtransform__mutmut_21(self, results: Any) -> dict[str, Any]:
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
        context["n_regimes"] = int(getattr(results, None, 2))
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

    def xǁRegimeTransformerǁtransform__mutmut_22(self, results: Any) -> dict[str, Any]:
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
        context["n_regimes"] = int(getattr(results, "n_regimes", None))
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

    def xǁRegimeTransformerǁtransform__mutmut_23(self, results: Any) -> dict[str, Any]:
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
        context["n_regimes"] = int(getattr("n_regimes", 2))
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

    def xǁRegimeTransformerǁtransform__mutmut_24(self, results: Any) -> dict[str, Any]:
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
        context["n_regimes"] = int(getattr(results, 2))
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

    def xǁRegimeTransformerǁtransform__mutmut_25(self, results: Any) -> dict[str, Any]:
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
        context["n_regimes"] = int(results.n_regimes)
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

    def xǁRegimeTransformerǁtransform__mutmut_26(self, results: Any) -> dict[str, Any]:
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
        context["n_regimes"] = int(getattr(results, "XXn_regimesXX", 2))
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

    def xǁRegimeTransformerǁtransform__mutmut_27(self, results: Any) -> dict[str, Any]:
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
        context["n_regimes"] = int(getattr(results, "N_REGIMES", 2))
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

    def xǁRegimeTransformerǁtransform__mutmut_28(self, results: Any) -> dict[str, Any]:
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
        context["n_regimes"] = int(getattr(results, "n_regimes", 3))
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

    def xǁRegimeTransformerǁtransform__mutmut_29(self, results: Any) -> dict[str, Any]:
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
        context["n_obs"] = None

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

    def xǁRegimeTransformerǁtransform__mutmut_30(self, results: Any) -> dict[str, Any]:
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
        context["XXn_obsXX"] = getattr(results, "nobs", 0)

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

    def xǁRegimeTransformerǁtransform__mutmut_31(self, results: Any) -> dict[str, Any]:
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
        context["N_OBS"] = getattr(results, "nobs", 0)

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

    def xǁRegimeTransformerǁtransform__mutmut_32(self, results: Any) -> dict[str, Any]:
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
        context["n_obs"] = getattr(None, "nobs", 0)

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

    def xǁRegimeTransformerǁtransform__mutmut_33(self, results: Any) -> dict[str, Any]:
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
        context["n_obs"] = getattr(results, None, 0)

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

    def xǁRegimeTransformerǁtransform__mutmut_34(self, results: Any) -> dict[str, Any]:
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
        context["n_obs"] = getattr(results, "nobs", None)

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

    def xǁRegimeTransformerǁtransform__mutmut_35(self, results: Any) -> dict[str, Any]:
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
        context["n_obs"] = getattr("nobs", 0)

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

    def xǁRegimeTransformerǁtransform__mutmut_36(self, results: Any) -> dict[str, Any]:
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
        context["n_obs"] = getattr(results, 0)

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

    def xǁRegimeTransformerǁtransform__mutmut_37(self, results: Any) -> dict[str, Any]:
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
        context["n_obs"] = results.nobs

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

    def xǁRegimeTransformerǁtransform__mutmut_38(self, results: Any) -> dict[str, Any]:
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
        context["n_obs"] = getattr(results, "XXnobsXX", 0)

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

    def xǁRegimeTransformerǁtransform__mutmut_39(self, results: Any) -> dict[str, Any]:
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
        context["n_obs"] = getattr(results, "NOBS", 0)

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

    def xǁRegimeTransformerǁtransform__mutmut_40(self, results: Any) -> dict[str, Any]:
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
        context["n_obs"] = getattr(results, "nobs", 1)

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

    def xǁRegimeTransformerǁtransform__mutmut_41(self, results: Any) -> dict[str, Any]:
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
        if hasattr(None, "transition_matrix"):
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

    def xǁRegimeTransformerǁtransform__mutmut_42(self, results: Any) -> dict[str, Any]:
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
        if hasattr(results, None):
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

    def xǁRegimeTransformerǁtransform__mutmut_43(self, results: Any) -> dict[str, Any]:
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
        if hasattr("transition_matrix"):
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

    def xǁRegimeTransformerǁtransform__mutmut_44(self, results: Any) -> dict[str, Any]:
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
        if hasattr(
            results,
        ):
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

    def xǁRegimeTransformerǁtransform__mutmut_45(self, results: Any) -> dict[str, Any]:
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
        if hasattr(results, "XXtransition_matrixXX"):
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

    def xǁRegimeTransformerǁtransform__mutmut_46(self, results: Any) -> dict[str, Any]:
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
        if hasattr(results, "TRANSITION_MATRIX"):
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

    def xǁRegimeTransformerǁtransform__mutmut_47(self, results: Any) -> dict[str, Any]:
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
            trans = None
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

    def xǁRegimeTransformerǁtransform__mutmut_48(self, results: Any) -> dict[str, Any]:
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
            trans = np.asarray(None)
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

    def xǁRegimeTransformerǁtransform__mutmut_49(self, results: Any) -> dict[str, Any]:
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
            context["transition_matrix"] = None

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

    def xǁRegimeTransformerǁtransform__mutmut_50(self, results: Any) -> dict[str, Any]:
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
            context["XXtransition_matrixXX"] = trans.tolist()

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

    def xǁRegimeTransformerǁtransform__mutmut_51(self, results: Any) -> dict[str, Any]:
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
            context["TRANSITION_MATRIX"] = trans.tolist()

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

    def xǁRegimeTransformerǁtransform__mutmut_52(self, results: Any) -> dict[str, Any]:
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
            n_states = None
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

    def xǁRegimeTransformerǁtransform__mutmut_53(self, results: Any) -> dict[str, Any]:
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
            n_states = trans.shape[1]
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

    def xǁRegimeTransformerǁtransform__mutmut_54(self, results: Any) -> dict[str, Any]:
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
            durations = None
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

    def xǁRegimeTransformerǁtransform__mutmut_55(self, results: Any) -> dict[str, Any]:
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
            for k in range(None):
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

    def xǁRegimeTransformerǁtransform__mutmut_56(self, results: Any) -> dict[str, Any]:
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
                d = None
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

    def xǁRegimeTransformerǁtransform__mutmut_57(self, results: Any) -> dict[str, Any]:
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
                d = 1.0 * (1.0 - trans[k, k]) if trans[k, k] < 1 else float("inf")
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

    def xǁRegimeTransformerǁtransform__mutmut_58(self, results: Any) -> dict[str, Any]:
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
                d = 2.0 / (1.0 - trans[k, k]) if trans[k, k] < 1 else float("inf")
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

    def xǁRegimeTransformerǁtransform__mutmut_59(self, results: Any) -> dict[str, Any]:
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
                d = 1.0 / (1.0 + trans[k, k]) if trans[k, k] < 1 else float("inf")
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

    def xǁRegimeTransformerǁtransform__mutmut_60(self, results: Any) -> dict[str, Any]:
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
                d = 1.0 / (2.0 - trans[k, k]) if trans[k, k] < 1 else float("inf")
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

    def xǁRegimeTransformerǁtransform__mutmut_61(self, results: Any) -> dict[str, Any]:
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
                d = 1.0 / (1.0 - trans[k, k]) if trans[k, k] <= 1 else float("inf")
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

    def xǁRegimeTransformerǁtransform__mutmut_62(self, results: Any) -> dict[str, Any]:
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
                d = 1.0 / (1.0 - trans[k, k]) if trans[k, k] < 2 else float("inf")
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

    def xǁRegimeTransformerǁtransform__mutmut_63(self, results: Any) -> dict[str, Any]:
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
                d = 1.0 / (1.0 - trans[k, k]) if trans[k, k] < 1 else float(None)
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

    def xǁRegimeTransformerǁtransform__mutmut_64(self, results: Any) -> dict[str, Any]:
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
                d = 1.0 / (1.0 - trans[k, k]) if trans[k, k] < 1 else float("XXinfXX")
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

    def xǁRegimeTransformerǁtransform__mutmut_65(self, results: Any) -> dict[str, Any]:
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
                d = 1.0 / (1.0 - trans[k, k]) if trans[k, k] < 1 else float("INF")
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

    def xǁRegimeTransformerǁtransform__mutmut_66(self, results: Any) -> dict[str, Any]:
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
                durations.append(None)
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

    def xǁRegimeTransformerǁtransform__mutmut_67(self, results: Any) -> dict[str, Any]:
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
                durations.append({"XXregimeXX": k + 1, "duration": d})
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

    def xǁRegimeTransformerǁtransform__mutmut_68(self, results: Any) -> dict[str, Any]:
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
                durations.append({"REGIME": k + 1, "duration": d})
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

    def xǁRegimeTransformerǁtransform__mutmut_69(self, results: Any) -> dict[str, Any]:
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
                durations.append({"regime": k - 1, "duration": d})
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

    def xǁRegimeTransformerǁtransform__mutmut_70(self, results: Any) -> dict[str, Any]:
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
                durations.append({"regime": k + 2, "duration": d})
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

    def xǁRegimeTransformerǁtransform__mutmut_71(self, results: Any) -> dict[str, Any]:
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
                durations.append({"regime": k + 1, "XXdurationXX": d})
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

    def xǁRegimeTransformerǁtransform__mutmut_72(self, results: Any) -> dict[str, Any]:
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
                durations.append({"regime": k + 1, "DURATION": d})
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

    def xǁRegimeTransformerǁtransform__mutmut_73(self, results: Any) -> dict[str, Any]:
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
            context["expected_durations"] = None

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

    def xǁRegimeTransformerǁtransform__mutmut_74(self, results: Any) -> dict[str, Any]:
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
            context["XXexpected_durationsXX"] = durations

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

    def xǁRegimeTransformerǁtransform__mutmut_75(self, results: Any) -> dict[str, Any]:
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
            context["EXPECTED_DURATIONS"] = durations

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

    def xǁRegimeTransformerǁtransform__mutmut_76(self, results: Any) -> dict[str, Any]:
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
        if hasattr(None, "regime_params"):
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

    def xǁRegimeTransformerǁtransform__mutmut_77(self, results: Any) -> dict[str, Any]:
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
        if hasattr(results, None):
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

    def xǁRegimeTransformerǁtransform__mutmut_78(self, results: Any) -> dict[str, Any]:
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
        if hasattr("regime_params"):
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

    def xǁRegimeTransformerǁtransform__mutmut_79(self, results: Any) -> dict[str, Any]:
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
        if hasattr(
            results,
        ):
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

    def xǁRegimeTransformerǁtransform__mutmut_80(self, results: Any) -> dict[str, Any]:
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
        if hasattr(results, "XXregime_paramsXX"):
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

    def xǁRegimeTransformerǁtransform__mutmut_81(self, results: Any) -> dict[str, Any]:
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
        if hasattr(results, "REGIME_PARAMS"):
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

    def xǁRegimeTransformerǁtransform__mutmut_82(self, results: Any) -> dict[str, Any]:
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
            context["regime_params"] = None
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

    def xǁRegimeTransformerǁtransform__mutmut_83(self, results: Any) -> dict[str, Any]:
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
            context["XXregime_paramsXX"] = []
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

    def xǁRegimeTransformerǁtransform__mutmut_84(self, results: Any) -> dict[str, Any]:
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
            context["REGIME_PARAMS"] = []
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

    def xǁRegimeTransformerǁtransform__mutmut_85(self, results: Any) -> dict[str, Any]:
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
            for k, params in enumerate(None):
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

    def xǁRegimeTransformerǁtransform__mutmut_86(self, results: Any) -> dict[str, Any]:
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
                regime_ctx = None
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

    def xǁRegimeTransformerǁtransform__mutmut_87(self, results: Any) -> dict[str, Any]:
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
                    "XXregimeXX": k + 1,
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

    def xǁRegimeTransformerǁtransform__mutmut_88(self, results: Any) -> dict[str, Any]:
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
                    "REGIME": k + 1,
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

    def xǁRegimeTransformerǁtransform__mutmut_89(self, results: Any) -> dict[str, Any]:
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
                    "regime": k - 1,
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

    def xǁRegimeTransformerǁtransform__mutmut_90(self, results: Any) -> dict[str, Any]:
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
                    "regime": k + 2,
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

    def xǁRegimeTransformerǁtransform__mutmut_91(self, results: Any) -> dict[str, Any]:
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
                    "XXparamsXX": params if isinstance(params, dict) else {"value": params},
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

    def xǁRegimeTransformerǁtransform__mutmut_92(self, results: Any) -> dict[str, Any]:
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
                    "PARAMS": params if isinstance(params, dict) else {"value": params},
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

    def xǁRegimeTransformerǁtransform__mutmut_93(self, results: Any) -> dict[str, Any]:
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
                    "params": params if isinstance(params, dict) else {"XXvalueXX": params},
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

    def xǁRegimeTransformerǁtransform__mutmut_94(self, results: Any) -> dict[str, Any]:
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
                    "params": params if isinstance(params, dict) else {"VALUE": params},
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

    def xǁRegimeTransformerǁtransform__mutmut_95(self, results: Any) -> dict[str, Any]:
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
                context["regime_params"].append(None)

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

    def xǁRegimeTransformerǁtransform__mutmut_96(self, results: Any) -> dict[str, Any]:
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
                context["XXregime_paramsXX"].append(regime_ctx)

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

    def xǁRegimeTransformerǁtransform__mutmut_97(self, results: Any) -> dict[str, Any]:
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
                context["REGIME_PARAMS"].append(regime_ctx)

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

    def xǁRegimeTransformerǁtransform__mutmut_98(self, results: Any) -> dict[str, Any]:
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
        if hasattr(None, "smoothed_probs"):
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

    def xǁRegimeTransformerǁtransform__mutmut_99(self, results: Any) -> dict[str, Any]:
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
        if hasattr(results, None):
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

    def xǁRegimeTransformerǁtransform__mutmut_100(self, results: Any) -> dict[str, Any]:
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
        if hasattr("smoothed_probs"):
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

    def xǁRegimeTransformerǁtransform__mutmut_101(self, results: Any) -> dict[str, Any]:
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
        if hasattr(
            results,
        ):
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

    def xǁRegimeTransformerǁtransform__mutmut_102(self, results: Any) -> dict[str, Any]:
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
        if hasattr(results, "XXsmoothed_probsXX"):
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

    def xǁRegimeTransformerǁtransform__mutmut_103(self, results: Any) -> dict[str, Any]:
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
        if hasattr(results, "SMOOTHED_PROBS"):
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

    def xǁRegimeTransformerǁtransform__mutmut_104(self, results: Any) -> dict[str, Any]:
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
            probs = None
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

    def xǁRegimeTransformerǁtransform__mutmut_105(self, results: Any) -> dict[str, Any]:
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
            probs = np.asarray(None)
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

    def xǁRegimeTransformerǁtransform__mutmut_106(self, results: Any) -> dict[str, Any]:
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
            n_states = None
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

    def xǁRegimeTransformerǁtransform__mutmut_107(self, results: Any) -> dict[str, Any]:
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
            n_states = probs.shape[2]
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

    def xǁRegimeTransformerǁtransform__mutmut_108(self, results: Any) -> dict[str, Any]:
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
            regime_class = None
            context["regime_classification"] = {
                "counts": [int(np.sum(regime_class == k)) for k in range(n_states)],
                "proportions": [float(np.mean(regime_class == k)) for k in range(n_states)],
            }

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_109(self, results: Any) -> dict[str, Any]:
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
            regime_class = np.argmax(None, axis=1)
            context["regime_classification"] = {
                "counts": [int(np.sum(regime_class == k)) for k in range(n_states)],
                "proportions": [float(np.mean(regime_class == k)) for k in range(n_states)],
            }

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_110(self, results: Any) -> dict[str, Any]:
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
            regime_class = np.argmax(probs, axis=None)
            context["regime_classification"] = {
                "counts": [int(np.sum(regime_class == k)) for k in range(n_states)],
                "proportions": [float(np.mean(regime_class == k)) for k in range(n_states)],
            }

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_111(self, results: Any) -> dict[str, Any]:
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
            regime_class = np.argmax(axis=1)
            context["regime_classification"] = {
                "counts": [int(np.sum(regime_class == k)) for k in range(n_states)],
                "proportions": [float(np.mean(regime_class == k)) for k in range(n_states)],
            }

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_112(self, results: Any) -> dict[str, Any]:
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
            regime_class = np.argmax(
                probs,
            )
            context["regime_classification"] = {
                "counts": [int(np.sum(regime_class == k)) for k in range(n_states)],
                "proportions": [float(np.mean(regime_class == k)) for k in range(n_states)],
            }

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_113(self, results: Any) -> dict[str, Any]:
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
            regime_class = np.argmax(probs, axis=2)
            context["regime_classification"] = {
                "counts": [int(np.sum(regime_class == k)) for k in range(n_states)],
                "proportions": [float(np.mean(regime_class == k)) for k in range(n_states)],
            }

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_114(self, results: Any) -> dict[str, Any]:
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
            context["regime_classification"] = None

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_115(self, results: Any) -> dict[str, Any]:
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
            context["XXregime_classificationXX"] = {
                "counts": [int(np.sum(regime_class == k)) for k in range(n_states)],
                "proportions": [float(np.mean(regime_class == k)) for k in range(n_states)],
            }

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_116(self, results: Any) -> dict[str, Any]:
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
            context["REGIME_CLASSIFICATION"] = {
                "counts": [int(np.sum(regime_class == k)) for k in range(n_states)],
                "proportions": [float(np.mean(regime_class == k)) for k in range(n_states)],
            }

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_117(self, results: Any) -> dict[str, Any]:
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
                "XXcountsXX": [int(np.sum(regime_class == k)) for k in range(n_states)],
                "proportions": [float(np.mean(regime_class == k)) for k in range(n_states)],
            }

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_118(self, results: Any) -> dict[str, Any]:
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
                "COUNTS": [int(np.sum(regime_class == k)) for k in range(n_states)],
                "proportions": [float(np.mean(regime_class == k)) for k in range(n_states)],
            }

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_119(self, results: Any) -> dict[str, Any]:
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
                "counts": [int(None) for k in range(n_states)],
                "proportions": [float(np.mean(regime_class == k)) for k in range(n_states)],
            }

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_120(self, results: Any) -> dict[str, Any]:
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
                "counts": [int(np.sum(None)) for k in range(n_states)],
                "proportions": [float(np.mean(regime_class == k)) for k in range(n_states)],
            }

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_121(self, results: Any) -> dict[str, Any]:
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
                "counts": [int(np.sum(regime_class != k)) for k in range(n_states)],
                "proportions": [float(np.mean(regime_class == k)) for k in range(n_states)],
            }

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_122(self, results: Any) -> dict[str, Any]:
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
                "counts": [int(np.sum(regime_class == k)) for k in range(None)],
                "proportions": [float(np.mean(regime_class == k)) for k in range(n_states)],
            }

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_123(self, results: Any) -> dict[str, Any]:
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
                "XXproportionsXX": [float(np.mean(regime_class == k)) for k in range(n_states)],
            }

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_124(self, results: Any) -> dict[str, Any]:
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
                "PROPORTIONS": [float(np.mean(regime_class == k)) for k in range(n_states)],
            }

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_125(self, results: Any) -> dict[str, Any]:
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
                "proportions": [float(None) for k in range(n_states)],
            }

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_126(self, results: Any) -> dict[str, Any]:
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
                "proportions": [float(np.mean(None)) for k in range(n_states)],
            }

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_127(self, results: Any) -> dict[str, Any]:
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
                "proportions": [float(np.mean(regime_class != k)) for k in range(n_states)],
            }

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_128(self, results: Any) -> dict[str, Any]:
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
                "proportions": [float(np.mean(regime_class == k)) for k in range(None)],
            }

        # Information criteria
        context["loglikelihood"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_129(self, results: Any) -> dict[str, Any]:
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
        context["loglikelihood"] = None
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_130(self, results: Any) -> dict[str, Any]:
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
        context["XXloglikelihoodXX"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_131(self, results: Any) -> dict[str, Any]:
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
        context["LOGLIKELIHOOD"] = getattr(results, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_132(self, results: Any) -> dict[str, Any]:
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
        context["loglikelihood"] = getattr(None, "loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_133(self, results: Any) -> dict[str, Any]:
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
        context["loglikelihood"] = getattr(results, None, None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_134(self, results: Any) -> dict[str, Any]:
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
        context["loglikelihood"] = getattr("loglikelihood", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_135(self, results: Any) -> dict[str, Any]:
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
        context["loglikelihood"] = getattr(results, None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_136(self, results: Any) -> dict[str, Any]:
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
        context["loglikelihood"] = results.loglikelihood
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_137(self, results: Any) -> dict[str, Any]:
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
        context["loglikelihood"] = getattr(results, "XXloglikelihoodXX", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_138(self, results: Any) -> dict[str, Any]:
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
        context["loglikelihood"] = getattr(results, "LOGLIKELIHOOD", None)
        context["aic"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_139(self, results: Any) -> dict[str, Any]:
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
        context["aic"] = None
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_140(self, results: Any) -> dict[str, Any]:
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
        context["XXaicXX"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_141(self, results: Any) -> dict[str, Any]:
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
        context["AIC"] = getattr(results, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_142(self, results: Any) -> dict[str, Any]:
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
        context["aic"] = getattr(None, "aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_143(self, results: Any) -> dict[str, Any]:
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
        context["aic"] = getattr(results, None, None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_144(self, results: Any) -> dict[str, Any]:
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
        context["aic"] = getattr("aic", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_145(self, results: Any) -> dict[str, Any]:
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
        context["aic"] = getattr(results, None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_146(self, results: Any) -> dict[str, Any]:
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
        context["aic"] = results.aic
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_147(self, results: Any) -> dict[str, Any]:
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
        context["aic"] = getattr(results, "XXaicXX", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_148(self, results: Any) -> dict[str, Any]:
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
        context["aic"] = getattr(results, "AIC", None)
        context["bic"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_149(self, results: Any) -> dict[str, Any]:
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
        context["bic"] = None

        return context

    def xǁRegimeTransformerǁtransform__mutmut_150(self, results: Any) -> dict[str, Any]:
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
        context["XXbicXX"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_151(self, results: Any) -> dict[str, Any]:
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
        context["BIC"] = getattr(results, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_152(self, results: Any) -> dict[str, Any]:
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
        context["bic"] = getattr(None, "bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_153(self, results: Any) -> dict[str, Any]:
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
        context["bic"] = getattr(results, None, None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_154(self, results: Any) -> dict[str, Any]:
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
        context["bic"] = getattr("bic", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_155(self, results: Any) -> dict[str, Any]:
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
        context["bic"] = getattr(results, None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_156(self, results: Any) -> dict[str, Any]:
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
        context["bic"] = results.bic

        return context

    def xǁRegimeTransformerǁtransform__mutmut_157(self, results: Any) -> dict[str, Any]:
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
        context["bic"] = getattr(results, "XXbicXX", None)

        return context

    def xǁRegimeTransformerǁtransform__mutmut_158(self, results: Any) -> dict[str, Any]:
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
        context["bic"] = getattr(results, "BIC", None)

        return context

    xǁRegimeTransformerǁtransform__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁRegimeTransformerǁtransform__mutmut_1": xǁRegimeTransformerǁtransform__mutmut_1,
        "xǁRegimeTransformerǁtransform__mutmut_2": xǁRegimeTransformerǁtransform__mutmut_2,
        "xǁRegimeTransformerǁtransform__mutmut_3": xǁRegimeTransformerǁtransform__mutmut_3,
        "xǁRegimeTransformerǁtransform__mutmut_4": xǁRegimeTransformerǁtransform__mutmut_4,
        "xǁRegimeTransformerǁtransform__mutmut_5": xǁRegimeTransformerǁtransform__mutmut_5,
        "xǁRegimeTransformerǁtransform__mutmut_6": xǁRegimeTransformerǁtransform__mutmut_6,
        "xǁRegimeTransformerǁtransform__mutmut_7": xǁRegimeTransformerǁtransform__mutmut_7,
        "xǁRegimeTransformerǁtransform__mutmut_8": xǁRegimeTransformerǁtransform__mutmut_8,
        "xǁRegimeTransformerǁtransform__mutmut_9": xǁRegimeTransformerǁtransform__mutmut_9,
        "xǁRegimeTransformerǁtransform__mutmut_10": xǁRegimeTransformerǁtransform__mutmut_10,
        "xǁRegimeTransformerǁtransform__mutmut_11": xǁRegimeTransformerǁtransform__mutmut_11,
        "xǁRegimeTransformerǁtransform__mutmut_12": xǁRegimeTransformerǁtransform__mutmut_12,
        "xǁRegimeTransformerǁtransform__mutmut_13": xǁRegimeTransformerǁtransform__mutmut_13,
        "xǁRegimeTransformerǁtransform__mutmut_14": xǁRegimeTransformerǁtransform__mutmut_14,
        "xǁRegimeTransformerǁtransform__mutmut_15": xǁRegimeTransformerǁtransform__mutmut_15,
        "xǁRegimeTransformerǁtransform__mutmut_16": xǁRegimeTransformerǁtransform__mutmut_16,
        "xǁRegimeTransformerǁtransform__mutmut_17": xǁRegimeTransformerǁtransform__mutmut_17,
        "xǁRegimeTransformerǁtransform__mutmut_18": xǁRegimeTransformerǁtransform__mutmut_18,
        "xǁRegimeTransformerǁtransform__mutmut_19": xǁRegimeTransformerǁtransform__mutmut_19,
        "xǁRegimeTransformerǁtransform__mutmut_20": xǁRegimeTransformerǁtransform__mutmut_20,
        "xǁRegimeTransformerǁtransform__mutmut_21": xǁRegimeTransformerǁtransform__mutmut_21,
        "xǁRegimeTransformerǁtransform__mutmut_22": xǁRegimeTransformerǁtransform__mutmut_22,
        "xǁRegimeTransformerǁtransform__mutmut_23": xǁRegimeTransformerǁtransform__mutmut_23,
        "xǁRegimeTransformerǁtransform__mutmut_24": xǁRegimeTransformerǁtransform__mutmut_24,
        "xǁRegimeTransformerǁtransform__mutmut_25": xǁRegimeTransformerǁtransform__mutmut_25,
        "xǁRegimeTransformerǁtransform__mutmut_26": xǁRegimeTransformerǁtransform__mutmut_26,
        "xǁRegimeTransformerǁtransform__mutmut_27": xǁRegimeTransformerǁtransform__mutmut_27,
        "xǁRegimeTransformerǁtransform__mutmut_28": xǁRegimeTransformerǁtransform__mutmut_28,
        "xǁRegimeTransformerǁtransform__mutmut_29": xǁRegimeTransformerǁtransform__mutmut_29,
        "xǁRegimeTransformerǁtransform__mutmut_30": xǁRegimeTransformerǁtransform__mutmut_30,
        "xǁRegimeTransformerǁtransform__mutmut_31": xǁRegimeTransformerǁtransform__mutmut_31,
        "xǁRegimeTransformerǁtransform__mutmut_32": xǁRegimeTransformerǁtransform__mutmut_32,
        "xǁRegimeTransformerǁtransform__mutmut_33": xǁRegimeTransformerǁtransform__mutmut_33,
        "xǁRegimeTransformerǁtransform__mutmut_34": xǁRegimeTransformerǁtransform__mutmut_34,
        "xǁRegimeTransformerǁtransform__mutmut_35": xǁRegimeTransformerǁtransform__mutmut_35,
        "xǁRegimeTransformerǁtransform__mutmut_36": xǁRegimeTransformerǁtransform__mutmut_36,
        "xǁRegimeTransformerǁtransform__mutmut_37": xǁRegimeTransformerǁtransform__mutmut_37,
        "xǁRegimeTransformerǁtransform__mutmut_38": xǁRegimeTransformerǁtransform__mutmut_38,
        "xǁRegimeTransformerǁtransform__mutmut_39": xǁRegimeTransformerǁtransform__mutmut_39,
        "xǁRegimeTransformerǁtransform__mutmut_40": xǁRegimeTransformerǁtransform__mutmut_40,
        "xǁRegimeTransformerǁtransform__mutmut_41": xǁRegimeTransformerǁtransform__mutmut_41,
        "xǁRegimeTransformerǁtransform__mutmut_42": xǁRegimeTransformerǁtransform__mutmut_42,
        "xǁRegimeTransformerǁtransform__mutmut_43": xǁRegimeTransformerǁtransform__mutmut_43,
        "xǁRegimeTransformerǁtransform__mutmut_44": xǁRegimeTransformerǁtransform__mutmut_44,
        "xǁRegimeTransformerǁtransform__mutmut_45": xǁRegimeTransformerǁtransform__mutmut_45,
        "xǁRegimeTransformerǁtransform__mutmut_46": xǁRegimeTransformerǁtransform__mutmut_46,
        "xǁRegimeTransformerǁtransform__mutmut_47": xǁRegimeTransformerǁtransform__mutmut_47,
        "xǁRegimeTransformerǁtransform__mutmut_48": xǁRegimeTransformerǁtransform__mutmut_48,
        "xǁRegimeTransformerǁtransform__mutmut_49": xǁRegimeTransformerǁtransform__mutmut_49,
        "xǁRegimeTransformerǁtransform__mutmut_50": xǁRegimeTransformerǁtransform__mutmut_50,
        "xǁRegimeTransformerǁtransform__mutmut_51": xǁRegimeTransformerǁtransform__mutmut_51,
        "xǁRegimeTransformerǁtransform__mutmut_52": xǁRegimeTransformerǁtransform__mutmut_52,
        "xǁRegimeTransformerǁtransform__mutmut_53": xǁRegimeTransformerǁtransform__mutmut_53,
        "xǁRegimeTransformerǁtransform__mutmut_54": xǁRegimeTransformerǁtransform__mutmut_54,
        "xǁRegimeTransformerǁtransform__mutmut_55": xǁRegimeTransformerǁtransform__mutmut_55,
        "xǁRegimeTransformerǁtransform__mutmut_56": xǁRegimeTransformerǁtransform__mutmut_56,
        "xǁRegimeTransformerǁtransform__mutmut_57": xǁRegimeTransformerǁtransform__mutmut_57,
        "xǁRegimeTransformerǁtransform__mutmut_58": xǁRegimeTransformerǁtransform__mutmut_58,
        "xǁRegimeTransformerǁtransform__mutmut_59": xǁRegimeTransformerǁtransform__mutmut_59,
        "xǁRegimeTransformerǁtransform__mutmut_60": xǁRegimeTransformerǁtransform__mutmut_60,
        "xǁRegimeTransformerǁtransform__mutmut_61": xǁRegimeTransformerǁtransform__mutmut_61,
        "xǁRegimeTransformerǁtransform__mutmut_62": xǁRegimeTransformerǁtransform__mutmut_62,
        "xǁRegimeTransformerǁtransform__mutmut_63": xǁRegimeTransformerǁtransform__mutmut_63,
        "xǁRegimeTransformerǁtransform__mutmut_64": xǁRegimeTransformerǁtransform__mutmut_64,
        "xǁRegimeTransformerǁtransform__mutmut_65": xǁRegimeTransformerǁtransform__mutmut_65,
        "xǁRegimeTransformerǁtransform__mutmut_66": xǁRegimeTransformerǁtransform__mutmut_66,
        "xǁRegimeTransformerǁtransform__mutmut_67": xǁRegimeTransformerǁtransform__mutmut_67,
        "xǁRegimeTransformerǁtransform__mutmut_68": xǁRegimeTransformerǁtransform__mutmut_68,
        "xǁRegimeTransformerǁtransform__mutmut_69": xǁRegimeTransformerǁtransform__mutmut_69,
        "xǁRegimeTransformerǁtransform__mutmut_70": xǁRegimeTransformerǁtransform__mutmut_70,
        "xǁRegimeTransformerǁtransform__mutmut_71": xǁRegimeTransformerǁtransform__mutmut_71,
        "xǁRegimeTransformerǁtransform__mutmut_72": xǁRegimeTransformerǁtransform__mutmut_72,
        "xǁRegimeTransformerǁtransform__mutmut_73": xǁRegimeTransformerǁtransform__mutmut_73,
        "xǁRegimeTransformerǁtransform__mutmut_74": xǁRegimeTransformerǁtransform__mutmut_74,
        "xǁRegimeTransformerǁtransform__mutmut_75": xǁRegimeTransformerǁtransform__mutmut_75,
        "xǁRegimeTransformerǁtransform__mutmut_76": xǁRegimeTransformerǁtransform__mutmut_76,
        "xǁRegimeTransformerǁtransform__mutmut_77": xǁRegimeTransformerǁtransform__mutmut_77,
        "xǁRegimeTransformerǁtransform__mutmut_78": xǁRegimeTransformerǁtransform__mutmut_78,
        "xǁRegimeTransformerǁtransform__mutmut_79": xǁRegimeTransformerǁtransform__mutmut_79,
        "xǁRegimeTransformerǁtransform__mutmut_80": xǁRegimeTransformerǁtransform__mutmut_80,
        "xǁRegimeTransformerǁtransform__mutmut_81": xǁRegimeTransformerǁtransform__mutmut_81,
        "xǁRegimeTransformerǁtransform__mutmut_82": xǁRegimeTransformerǁtransform__mutmut_82,
        "xǁRegimeTransformerǁtransform__mutmut_83": xǁRegimeTransformerǁtransform__mutmut_83,
        "xǁRegimeTransformerǁtransform__mutmut_84": xǁRegimeTransformerǁtransform__mutmut_84,
        "xǁRegimeTransformerǁtransform__mutmut_85": xǁRegimeTransformerǁtransform__mutmut_85,
        "xǁRegimeTransformerǁtransform__mutmut_86": xǁRegimeTransformerǁtransform__mutmut_86,
        "xǁRegimeTransformerǁtransform__mutmut_87": xǁRegimeTransformerǁtransform__mutmut_87,
        "xǁRegimeTransformerǁtransform__mutmut_88": xǁRegimeTransformerǁtransform__mutmut_88,
        "xǁRegimeTransformerǁtransform__mutmut_89": xǁRegimeTransformerǁtransform__mutmut_89,
        "xǁRegimeTransformerǁtransform__mutmut_90": xǁRegimeTransformerǁtransform__mutmut_90,
        "xǁRegimeTransformerǁtransform__mutmut_91": xǁRegimeTransformerǁtransform__mutmut_91,
        "xǁRegimeTransformerǁtransform__mutmut_92": xǁRegimeTransformerǁtransform__mutmut_92,
        "xǁRegimeTransformerǁtransform__mutmut_93": xǁRegimeTransformerǁtransform__mutmut_93,
        "xǁRegimeTransformerǁtransform__mutmut_94": xǁRegimeTransformerǁtransform__mutmut_94,
        "xǁRegimeTransformerǁtransform__mutmut_95": xǁRegimeTransformerǁtransform__mutmut_95,
        "xǁRegimeTransformerǁtransform__mutmut_96": xǁRegimeTransformerǁtransform__mutmut_96,
        "xǁRegimeTransformerǁtransform__mutmut_97": xǁRegimeTransformerǁtransform__mutmut_97,
        "xǁRegimeTransformerǁtransform__mutmut_98": xǁRegimeTransformerǁtransform__mutmut_98,
        "xǁRegimeTransformerǁtransform__mutmut_99": xǁRegimeTransformerǁtransform__mutmut_99,
        "xǁRegimeTransformerǁtransform__mutmut_100": xǁRegimeTransformerǁtransform__mutmut_100,
        "xǁRegimeTransformerǁtransform__mutmut_101": xǁRegimeTransformerǁtransform__mutmut_101,
        "xǁRegimeTransformerǁtransform__mutmut_102": xǁRegimeTransformerǁtransform__mutmut_102,
        "xǁRegimeTransformerǁtransform__mutmut_103": xǁRegimeTransformerǁtransform__mutmut_103,
        "xǁRegimeTransformerǁtransform__mutmut_104": xǁRegimeTransformerǁtransform__mutmut_104,
        "xǁRegimeTransformerǁtransform__mutmut_105": xǁRegimeTransformerǁtransform__mutmut_105,
        "xǁRegimeTransformerǁtransform__mutmut_106": xǁRegimeTransformerǁtransform__mutmut_106,
        "xǁRegimeTransformerǁtransform__mutmut_107": xǁRegimeTransformerǁtransform__mutmut_107,
        "xǁRegimeTransformerǁtransform__mutmut_108": xǁRegimeTransformerǁtransform__mutmut_108,
        "xǁRegimeTransformerǁtransform__mutmut_109": xǁRegimeTransformerǁtransform__mutmut_109,
        "xǁRegimeTransformerǁtransform__mutmut_110": xǁRegimeTransformerǁtransform__mutmut_110,
        "xǁRegimeTransformerǁtransform__mutmut_111": xǁRegimeTransformerǁtransform__mutmut_111,
        "xǁRegimeTransformerǁtransform__mutmut_112": xǁRegimeTransformerǁtransform__mutmut_112,
        "xǁRegimeTransformerǁtransform__mutmut_113": xǁRegimeTransformerǁtransform__mutmut_113,
        "xǁRegimeTransformerǁtransform__mutmut_114": xǁRegimeTransformerǁtransform__mutmut_114,
        "xǁRegimeTransformerǁtransform__mutmut_115": xǁRegimeTransformerǁtransform__mutmut_115,
        "xǁRegimeTransformerǁtransform__mutmut_116": xǁRegimeTransformerǁtransform__mutmut_116,
        "xǁRegimeTransformerǁtransform__mutmut_117": xǁRegimeTransformerǁtransform__mutmut_117,
        "xǁRegimeTransformerǁtransform__mutmut_118": xǁRegimeTransformerǁtransform__mutmut_118,
        "xǁRegimeTransformerǁtransform__mutmut_119": xǁRegimeTransformerǁtransform__mutmut_119,
        "xǁRegimeTransformerǁtransform__mutmut_120": xǁRegimeTransformerǁtransform__mutmut_120,
        "xǁRegimeTransformerǁtransform__mutmut_121": xǁRegimeTransformerǁtransform__mutmut_121,
        "xǁRegimeTransformerǁtransform__mutmut_122": xǁRegimeTransformerǁtransform__mutmut_122,
        "xǁRegimeTransformerǁtransform__mutmut_123": xǁRegimeTransformerǁtransform__mutmut_123,
        "xǁRegimeTransformerǁtransform__mutmut_124": xǁRegimeTransformerǁtransform__mutmut_124,
        "xǁRegimeTransformerǁtransform__mutmut_125": xǁRegimeTransformerǁtransform__mutmut_125,
        "xǁRegimeTransformerǁtransform__mutmut_126": xǁRegimeTransformerǁtransform__mutmut_126,
        "xǁRegimeTransformerǁtransform__mutmut_127": xǁRegimeTransformerǁtransform__mutmut_127,
        "xǁRegimeTransformerǁtransform__mutmut_128": xǁRegimeTransformerǁtransform__mutmut_128,
        "xǁRegimeTransformerǁtransform__mutmut_129": xǁRegimeTransformerǁtransform__mutmut_129,
        "xǁRegimeTransformerǁtransform__mutmut_130": xǁRegimeTransformerǁtransform__mutmut_130,
        "xǁRegimeTransformerǁtransform__mutmut_131": xǁRegimeTransformerǁtransform__mutmut_131,
        "xǁRegimeTransformerǁtransform__mutmut_132": xǁRegimeTransformerǁtransform__mutmut_132,
        "xǁRegimeTransformerǁtransform__mutmut_133": xǁRegimeTransformerǁtransform__mutmut_133,
        "xǁRegimeTransformerǁtransform__mutmut_134": xǁRegimeTransformerǁtransform__mutmut_134,
        "xǁRegimeTransformerǁtransform__mutmut_135": xǁRegimeTransformerǁtransform__mutmut_135,
        "xǁRegimeTransformerǁtransform__mutmut_136": xǁRegimeTransformerǁtransform__mutmut_136,
        "xǁRegimeTransformerǁtransform__mutmut_137": xǁRegimeTransformerǁtransform__mutmut_137,
        "xǁRegimeTransformerǁtransform__mutmut_138": xǁRegimeTransformerǁtransform__mutmut_138,
        "xǁRegimeTransformerǁtransform__mutmut_139": xǁRegimeTransformerǁtransform__mutmut_139,
        "xǁRegimeTransformerǁtransform__mutmut_140": xǁRegimeTransformerǁtransform__mutmut_140,
        "xǁRegimeTransformerǁtransform__mutmut_141": xǁRegimeTransformerǁtransform__mutmut_141,
        "xǁRegimeTransformerǁtransform__mutmut_142": xǁRegimeTransformerǁtransform__mutmut_142,
        "xǁRegimeTransformerǁtransform__mutmut_143": xǁRegimeTransformerǁtransform__mutmut_143,
        "xǁRegimeTransformerǁtransform__mutmut_144": xǁRegimeTransformerǁtransform__mutmut_144,
        "xǁRegimeTransformerǁtransform__mutmut_145": xǁRegimeTransformerǁtransform__mutmut_145,
        "xǁRegimeTransformerǁtransform__mutmut_146": xǁRegimeTransformerǁtransform__mutmut_146,
        "xǁRegimeTransformerǁtransform__mutmut_147": xǁRegimeTransformerǁtransform__mutmut_147,
        "xǁRegimeTransformerǁtransform__mutmut_148": xǁRegimeTransformerǁtransform__mutmut_148,
        "xǁRegimeTransformerǁtransform__mutmut_149": xǁRegimeTransformerǁtransform__mutmut_149,
        "xǁRegimeTransformerǁtransform__mutmut_150": xǁRegimeTransformerǁtransform__mutmut_150,
        "xǁRegimeTransformerǁtransform__mutmut_151": xǁRegimeTransformerǁtransform__mutmut_151,
        "xǁRegimeTransformerǁtransform__mutmut_152": xǁRegimeTransformerǁtransform__mutmut_152,
        "xǁRegimeTransformerǁtransform__mutmut_153": xǁRegimeTransformerǁtransform__mutmut_153,
        "xǁRegimeTransformerǁtransform__mutmut_154": xǁRegimeTransformerǁtransform__mutmut_154,
        "xǁRegimeTransformerǁtransform__mutmut_155": xǁRegimeTransformerǁtransform__mutmut_155,
        "xǁRegimeTransformerǁtransform__mutmut_156": xǁRegimeTransformerǁtransform__mutmut_156,
        "xǁRegimeTransformerǁtransform__mutmut_157": xǁRegimeTransformerǁtransform__mutmut_157,
        "xǁRegimeTransformerǁtransform__mutmut_158": xǁRegimeTransformerǁtransform__mutmut_158,
    }
    xǁRegimeTransformerǁtransform__mutmut_orig.__name__ = "xǁRegimeTransformerǁtransform"
