"""GARCH results transformer for report generation.

Extracts parameters, diagnostics, and visualization data from
fitted GARCH model results.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
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
        args = [results]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGARCHTransformerǁtransform__mutmut_orig"),
            object.__getattribute__(self, "xǁGARCHTransformerǁtransform__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGARCHTransformerǁtransform__mutmut_orig(self, results: Any) -> dict[str, Any]:
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

    def xǁGARCHTransformerǁtransform__mutmut_1(self, results: Any) -> dict[str, Any]:
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
        context: dict[str, Any] = None

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

    def xǁGARCHTransformerǁtransform__mutmut_2(self, results: Any) -> dict[str, Any]:
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
        context["model_name"] = None
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

    def xǁGARCHTransformerǁtransform__mutmut_3(self, results: Any) -> dict[str, Any]:
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
        context["XXmodel_nameXX"] = getattr(results, "model_name", "GARCH")
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

    def xǁGARCHTransformerǁtransform__mutmut_4(self, results: Any) -> dict[str, Any]:
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
        context["MODEL_NAME"] = getattr(results, "model_name", "GARCH")
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

    def xǁGARCHTransformerǁtransform__mutmut_5(self, results: Any) -> dict[str, Any]:
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
        context["model_name"] = getattr(None, "model_name", "GARCH")
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

    def xǁGARCHTransformerǁtransform__mutmut_6(self, results: Any) -> dict[str, Any]:
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
        context["model_name"] = getattr(results, None, "GARCH")
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

    def xǁGARCHTransformerǁtransform__mutmut_7(self, results: Any) -> dict[str, Any]:
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
        context["model_name"] = getattr(results, "model_name", None)
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

    def xǁGARCHTransformerǁtransform__mutmut_8(self, results: Any) -> dict[str, Any]:
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
        context["model_name"] = ("model_name").GARCH
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

    def xǁGARCHTransformerǁtransform__mutmut_9(self, results: Any) -> dict[str, Any]:
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
        context["model_name"] = results.GARCH
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

    def xǁGARCHTransformerǁtransform__mutmut_10(self, results: Any) -> dict[str, Any]:
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
        context["model_name"] = results.model_name
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

    def xǁGARCHTransformerǁtransform__mutmut_11(self, results: Any) -> dict[str, Any]:
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
        context["model_name"] = getattr(results, "XXmodel_nameXX", "GARCH")
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

    def xǁGARCHTransformerǁtransform__mutmut_12(self, results: Any) -> dict[str, Any]:
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
        context["model_name"] = getattr(results, "MODEL_NAME", "GARCH")
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

    def xǁGARCHTransformerǁtransform__mutmut_13(self, results: Any) -> dict[str, Any]:
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
        context["model_name"] = getattr(results, "model_name", "XXGARCHXX")
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

    def xǁGARCHTransformerǁtransform__mutmut_14(self, results: Any) -> dict[str, Any]:
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
        context["model_name"] = getattr(results, "model_name", "garch")
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

    def xǁGARCHTransformerǁtransform__mutmut_15(self, results: Any) -> dict[str, Any]:
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
        context["n_obs"] = None
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

    def xǁGARCHTransformerǁtransform__mutmut_16(self, results: Any) -> dict[str, Any]:
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
        context["XXn_obsXX"] = getattr(results, "nobs", 0)
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

    def xǁGARCHTransformerǁtransform__mutmut_17(self, results: Any) -> dict[str, Any]:
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
        context["N_OBS"] = getattr(results, "nobs", 0)
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

    def xǁGARCHTransformerǁtransform__mutmut_18(self, results: Any) -> dict[str, Any]:
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
        context["n_obs"] = getattr(None, "nobs", 0)
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

    def xǁGARCHTransformerǁtransform__mutmut_19(self, results: Any) -> dict[str, Any]:
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
        context["n_obs"] = getattr(results, None, 0)
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

    def xǁGARCHTransformerǁtransform__mutmut_20(self, results: Any) -> dict[str, Any]:
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
        context["n_obs"] = getattr(results, "nobs", None)
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

    def xǁGARCHTransformerǁtransform__mutmut_21(self, results: Any) -> dict[str, Any]:
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
        context["n_obs"] = getattr("nobs", 0)
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

    def xǁGARCHTransformerǁtransform__mutmut_22(self, results: Any) -> dict[str, Any]:
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
        context["n_obs"] = getattr(results, 0)
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

    def xǁGARCHTransformerǁtransform__mutmut_23(self, results: Any) -> dict[str, Any]:
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
        context["n_obs"] = results.nobs
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

    def xǁGARCHTransformerǁtransform__mutmut_24(self, results: Any) -> dict[str, Any]:
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
        context["n_obs"] = getattr(results, "XXnobsXX", 0)
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

    def xǁGARCHTransformerǁtransform__mutmut_25(self, results: Any) -> dict[str, Any]:
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
        context["n_obs"] = getattr(results, "NOBS", 0)
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

    def xǁGARCHTransformerǁtransform__mutmut_26(self, results: Any) -> dict[str, Any]:
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
        context["n_obs"] = getattr(results, "nobs", 1)
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

    def xǁGARCHTransformerǁtransform__mutmut_27(self, results: Any) -> dict[str, Any]:
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
        context["generated_at"] = None

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

    def xǁGARCHTransformerǁtransform__mutmut_28(self, results: Any) -> dict[str, Any]:
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
        context["XXgenerated_atXX"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

    def xǁGARCHTransformerǁtransform__mutmut_29(self, results: Any) -> dict[str, Any]:
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
        context["GENERATED_AT"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

    def xǁGARCHTransformerǁtransform__mutmut_30(self, results: Any) -> dict[str, Any]:
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
        context["generated_at"] = datetime.now().strftime(None)

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

    def xǁGARCHTransformerǁtransform__mutmut_31(self, results: Any) -> dict[str, Any]:
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
        context["generated_at"] = datetime.now().strftime("XX%Y-%m-%d %H:%M:%SXX")

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

    def xǁGARCHTransformerǁtransform__mutmut_32(self, results: Any) -> dict[str, Any]:
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
        context["generated_at"] = datetime.now().strftime("%y-%m-%d %h:%m:%s")

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

    def xǁGARCHTransformerǁtransform__mutmut_33(self, results: Any) -> dict[str, Any]:
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
        context["generated_at"] = datetime.now().strftime("%Y-%M-%D %H:%M:%S")

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

    def xǁGARCHTransformerǁtransform__mutmut_34(self, results: Any) -> dict[str, Any]:
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
        context["params_table"] = None

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

    def xǁGARCHTransformerǁtransform__mutmut_35(self, results: Any) -> dict[str, Any]:
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
        context["XXparams_tableXX"] = self._extract_params_table(results)

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

    def xǁGARCHTransformerǁtransform__mutmut_36(self, results: Any) -> dict[str, Any]:
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
        context["PARAMS_TABLE"] = self._extract_params_table(results)

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

    def xǁGARCHTransformerǁtransform__mutmut_37(self, results: Any) -> dict[str, Any]:
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
        context["params_table"] = self._extract_params_table(None)

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

    def xǁGARCHTransformerǁtransform__mutmut_38(self, results: Any) -> dict[str, Any]:
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
        persistence_attr = None
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

    def xǁGARCHTransformerǁtransform__mutmut_39(self, results: Any) -> dict[str, Any]:
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
        persistence_attr = getattr(None, "persistence", None)
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

    def xǁGARCHTransformerǁtransform__mutmut_40(self, results: Any) -> dict[str, Any]:
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
        persistence_attr = getattr(results, None, None)
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

    def xǁGARCHTransformerǁtransform__mutmut_41(self, results: Any) -> dict[str, Any]:
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
        persistence_attr = getattr("persistence", None)
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

    def xǁGARCHTransformerǁtransform__mutmut_42(self, results: Any) -> dict[str, Any]:
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
        persistence_attr = getattr(results, None)
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

    def xǁGARCHTransformerǁtransform__mutmut_43(self, results: Any) -> dict[str, Any]:
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
        persistence_attr = results.persistence
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

    def xǁGARCHTransformerǁtransform__mutmut_44(self, results: Any) -> dict[str, Any]:
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
        persistence_attr = getattr(results, "XXpersistenceXX", None)
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

    def xǁGARCHTransformerǁtransform__mutmut_45(self, results: Any) -> dict[str, Any]:
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
        persistence_attr = getattr(results, "PERSISTENCE", None)
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

    def xǁGARCHTransformerǁtransform__mutmut_46(self, results: Any) -> dict[str, Any]:
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
        context["persistence"] = None
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

    def xǁGARCHTransformerǁtransform__mutmut_47(self, results: Any) -> dict[str, Any]:
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
        context["XXpersistenceXX"] = (
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

    def xǁGARCHTransformerǁtransform__mutmut_48(self, results: Any) -> dict[str, Any]:
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
        context["PERSISTENCE"] = (
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

    def xǁGARCHTransformerǁtransform__mutmut_49(self, results: Any) -> dict[str, Any]:
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
        context["persistence"] = persistence_attr() if callable(None) else persistence_attr
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

    def xǁGARCHTransformerǁtransform__mutmut_50(self, results: Any) -> dict[str, Any]:
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
        uncond_var_attr = None
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

    def xǁGARCHTransformerǁtransform__mutmut_51(self, results: Any) -> dict[str, Any]:
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
        uncond_var_attr = getattr(None, "unconditional_variance", None)
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

    def xǁGARCHTransformerǁtransform__mutmut_52(self, results: Any) -> dict[str, Any]:
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
        uncond_var_attr = getattr(results, None, None)
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

    def xǁGARCHTransformerǁtransform__mutmut_53(self, results: Any) -> dict[str, Any]:
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
        uncond_var_attr = getattr("unconditional_variance", None)
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

    def xǁGARCHTransformerǁtransform__mutmut_54(self, results: Any) -> dict[str, Any]:
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
        uncond_var_attr = getattr(results, None)
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

    def xǁGARCHTransformerǁtransform__mutmut_55(self, results: Any) -> dict[str, Any]:
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
        uncond_var_attr = results.unconditional_variance
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

    def xǁGARCHTransformerǁtransform__mutmut_56(self, results: Any) -> dict[str, Any]:
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
        uncond_var_attr = getattr(results, "XXunconditional_varianceXX", None)
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

    def xǁGARCHTransformerǁtransform__mutmut_57(self, results: Any) -> dict[str, Any]:
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
        uncond_var_attr = getattr(results, "UNCONDITIONAL_VARIANCE", None)
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

    def xǁGARCHTransformerǁtransform__mutmut_58(self, results: Any) -> dict[str, Any]:
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
        context["unconditional_variance"] = None
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

    def xǁGARCHTransformerǁtransform__mutmut_59(self, results: Any) -> dict[str, Any]:
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
        context["XXunconditional_varianceXX"] = (
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

    def xǁGARCHTransformerǁtransform__mutmut_60(self, results: Any) -> dict[str, Any]:
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
        context["UNCONDITIONAL_VARIANCE"] = (
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

    def xǁGARCHTransformerǁtransform__mutmut_61(self, results: Any) -> dict[str, Any]:
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
        context["unconditional_variance"] = uncond_var_attr() if callable(None) else uncond_var_attr
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

    def xǁGARCHTransformerǁtransform__mutmut_62(self, results: Any) -> dict[str, Any]:
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
        context["half_life"] = None

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

    def xǁGARCHTransformerǁtransform__mutmut_63(self, results: Any) -> dict[str, Any]:
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
        context["XXhalf_lifeXX"] = self._compute_half_life(results)

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

    def xǁGARCHTransformerǁtransform__mutmut_64(self, results: Any) -> dict[str, Any]:
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
        context["HALF_LIFE"] = self._compute_half_life(results)

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

    def xǁGARCHTransformerǁtransform__mutmut_65(self, results: Any) -> dict[str, Any]:
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
        context["half_life"] = self._compute_half_life(None)

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

    def xǁGARCHTransformerǁtransform__mutmut_66(self, results: Any) -> dict[str, Any]:
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
        context["loglikelihood"] = None
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

    def xǁGARCHTransformerǁtransform__mutmut_67(self, results: Any) -> dict[str, Any]:
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
        context["XXloglikelihoodXX"] = getattr(results, "loglikelihood", None)
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

    def xǁGARCHTransformerǁtransform__mutmut_68(self, results: Any) -> dict[str, Any]:
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
        context["LOGLIKELIHOOD"] = getattr(results, "loglikelihood", None)
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

    def xǁGARCHTransformerǁtransform__mutmut_69(self, results: Any) -> dict[str, Any]:
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
        context["loglikelihood"] = getattr(None, "loglikelihood", None)
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

    def xǁGARCHTransformerǁtransform__mutmut_70(self, results: Any) -> dict[str, Any]:
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
        context["loglikelihood"] = getattr(results, None, None)
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

    def xǁGARCHTransformerǁtransform__mutmut_71(self, results: Any) -> dict[str, Any]:
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
        context["loglikelihood"] = getattr("loglikelihood", None)
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

    def xǁGARCHTransformerǁtransform__mutmut_72(self, results: Any) -> dict[str, Any]:
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
        context["loglikelihood"] = getattr(results, None)
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

    def xǁGARCHTransformerǁtransform__mutmut_73(self, results: Any) -> dict[str, Any]:
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
        context["loglikelihood"] = results.loglikelihood
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

    def xǁGARCHTransformerǁtransform__mutmut_74(self, results: Any) -> dict[str, Any]:
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
        context["loglikelihood"] = getattr(results, "XXloglikelihoodXX", None)
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

    def xǁGARCHTransformerǁtransform__mutmut_75(self, results: Any) -> dict[str, Any]:
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
        context["loglikelihood"] = getattr(results, "LOGLIKELIHOOD", None)
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

    def xǁGARCHTransformerǁtransform__mutmut_76(self, results: Any) -> dict[str, Any]:
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
        context["aic"] = None
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

    def xǁGARCHTransformerǁtransform__mutmut_77(self, results: Any) -> dict[str, Any]:
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
        context["XXaicXX"] = getattr(results, "aic", None)
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

    def xǁGARCHTransformerǁtransform__mutmut_78(self, results: Any) -> dict[str, Any]:
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
        context["AIC"] = getattr(results, "aic", None)
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

    def xǁGARCHTransformerǁtransform__mutmut_79(self, results: Any) -> dict[str, Any]:
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
        context["aic"] = getattr(None, "aic", None)
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

    def xǁGARCHTransformerǁtransform__mutmut_80(self, results: Any) -> dict[str, Any]:
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
        context["aic"] = getattr(results, None, None)
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

    def xǁGARCHTransformerǁtransform__mutmut_81(self, results: Any) -> dict[str, Any]:
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
        context["aic"] = getattr("aic", None)
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

    def xǁGARCHTransformerǁtransform__mutmut_82(self, results: Any) -> dict[str, Any]:
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
        context["aic"] = getattr(results, None)
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

    def xǁGARCHTransformerǁtransform__mutmut_83(self, results: Any) -> dict[str, Any]:
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
        context["aic"] = results.aic
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

    def xǁGARCHTransformerǁtransform__mutmut_84(self, results: Any) -> dict[str, Any]:
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
        context["aic"] = getattr(results, "XXaicXX", None)
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

    def xǁGARCHTransformerǁtransform__mutmut_85(self, results: Any) -> dict[str, Any]:
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
        context["aic"] = getattr(results, "AIC", None)
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

    def xǁGARCHTransformerǁtransform__mutmut_86(self, results: Any) -> dict[str, Any]:
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
        context["bic"] = None
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

    def xǁGARCHTransformerǁtransform__mutmut_87(self, results: Any) -> dict[str, Any]:
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
        context["XXbicXX"] = getattr(results, "bic", None)
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

    def xǁGARCHTransformerǁtransform__mutmut_88(self, results: Any) -> dict[str, Any]:
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
        context["BIC"] = getattr(results, "bic", None)
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

    def xǁGARCHTransformerǁtransform__mutmut_89(self, results: Any) -> dict[str, Any]:
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
        context["bic"] = getattr(None, "bic", None)
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

    def xǁGARCHTransformerǁtransform__mutmut_90(self, results: Any) -> dict[str, Any]:
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
        context["bic"] = getattr(results, None, None)
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

    def xǁGARCHTransformerǁtransform__mutmut_91(self, results: Any) -> dict[str, Any]:
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
        context["bic"] = getattr("bic", None)
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

    def xǁGARCHTransformerǁtransform__mutmut_92(self, results: Any) -> dict[str, Any]:
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
        context["bic"] = getattr(results, None)
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

    def xǁGARCHTransformerǁtransform__mutmut_93(self, results: Any) -> dict[str, Any]:
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
        context["bic"] = results.bic
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

    def xǁGARCHTransformerǁtransform__mutmut_94(self, results: Any) -> dict[str, Any]:
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
        context["bic"] = getattr(results, "XXbicXX", None)
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

    def xǁGARCHTransformerǁtransform__mutmut_95(self, results: Any) -> dict[str, Any]:
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
        context["bic"] = getattr(results, "BIC", None)
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

    def xǁGARCHTransformerǁtransform__mutmut_96(self, results: Any) -> dict[str, Any]:
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
        context["hqic"] = None

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

    def xǁGARCHTransformerǁtransform__mutmut_97(self, results: Any) -> dict[str, Any]:
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
        context["XXhqicXX"] = getattr(results, "hqic", None)

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

    def xǁGARCHTransformerǁtransform__mutmut_98(self, results: Any) -> dict[str, Any]:
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
        context["HQIC"] = getattr(results, "hqic", None)

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

    def xǁGARCHTransformerǁtransform__mutmut_99(self, results: Any) -> dict[str, Any]:
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
        context["hqic"] = getattr(None, "hqic", None)

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

    def xǁGARCHTransformerǁtransform__mutmut_100(self, results: Any) -> dict[str, Any]:
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
        context["hqic"] = getattr(results, None, None)

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

    def xǁGARCHTransformerǁtransform__mutmut_101(self, results: Any) -> dict[str, Any]:
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
        context["hqic"] = getattr("hqic", None)

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

    def xǁGARCHTransformerǁtransform__mutmut_102(self, results: Any) -> dict[str, Any]:
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
        context["hqic"] = getattr(results, None)

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

    def xǁGARCHTransformerǁtransform__mutmut_103(self, results: Any) -> dict[str, Any]:
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
        context["hqic"] = results.hqic

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

    def xǁGARCHTransformerǁtransform__mutmut_104(self, results: Any) -> dict[str, Any]:
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
        context["hqic"] = getattr(results, "XXhqicXX", None)

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

    def xǁGARCHTransformerǁtransform__mutmut_105(self, results: Any) -> dict[str, Any]:
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
        context["hqic"] = getattr(results, "HQIC", None)

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

    def xǁGARCHTransformerǁtransform__mutmut_106(self, results: Any) -> dict[str, Any]:
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
        context["diagnostics"] = None

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

    def xǁGARCHTransformerǁtransform__mutmut_107(self, results: Any) -> dict[str, Any]:
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
        context["XXdiagnosticsXX"] = self._extract_diagnostics(results)

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

    def xǁGARCHTransformerǁtransform__mutmut_108(self, results: Any) -> dict[str, Any]:
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
        context["DIAGNOSTICS"] = self._extract_diagnostics(results)

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

    def xǁGARCHTransformerǁtransform__mutmut_109(self, results: Any) -> dict[str, Any]:
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
        context["diagnostics"] = self._extract_diagnostics(None)

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

    def xǁGARCHTransformerǁtransform__mutmut_110(self, results: Any) -> dict[str, Any]:
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
        if hasattr(None, "conditional_volatility"):
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

    def xǁGARCHTransformerǁtransform__mutmut_111(self, results: Any) -> dict[str, Any]:
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
        if hasattr(results, None):
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

    def xǁGARCHTransformerǁtransform__mutmut_112(self, results: Any) -> dict[str, Any]:
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
        if hasattr("conditional_volatility"):
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

    def xǁGARCHTransformerǁtransform__mutmut_113(self, results: Any) -> dict[str, Any]:
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
        if hasattr(
            results,
        ):
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

    def xǁGARCHTransformerǁtransform__mutmut_114(self, results: Any) -> dict[str, Any]:
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
        if hasattr(results, "XXconditional_volatilityXX"):
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

    def xǁGARCHTransformerǁtransform__mutmut_115(self, results: Any) -> dict[str, Any]:
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
        if hasattr(results, "CONDITIONAL_VOLATILITY"):
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

    def xǁGARCHTransformerǁtransform__mutmut_116(self, results: Any) -> dict[str, Any]:
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
            vol = None
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

    def xǁGARCHTransformerǁtransform__mutmut_117(self, results: Any) -> dict[str, Any]:
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
            vol = np.asarray(None)
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

    def xǁGARCHTransformerǁtransform__mutmut_118(self, results: Any) -> dict[str, Any]:
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
            context["volatility_stats"] = None

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

    def xǁGARCHTransformerǁtransform__mutmut_119(self, results: Any) -> dict[str, Any]:
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
            context["XXvolatility_statsXX"] = {
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

    def xǁGARCHTransformerǁtransform__mutmut_120(self, results: Any) -> dict[str, Any]:
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
            context["VOLATILITY_STATS"] = {
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

    def xǁGARCHTransformerǁtransform__mutmut_121(self, results: Any) -> dict[str, Any]:
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
                "XXmeanXX": float(np.mean(vol)),
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

    def xǁGARCHTransformerǁtransform__mutmut_122(self, results: Any) -> dict[str, Any]:
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
                "MEAN": float(np.mean(vol)),
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

    def xǁGARCHTransformerǁtransform__mutmut_123(self, results: Any) -> dict[str, Any]:
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
                "mean": float(None),
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

    def xǁGARCHTransformerǁtransform__mutmut_124(self, results: Any) -> dict[str, Any]:
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
                "mean": float(np.mean(None)),
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

    def xǁGARCHTransformerǁtransform__mutmut_125(self, results: Any) -> dict[str, Any]:
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
                "XXstdXX": float(np.std(vol)),
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

    def xǁGARCHTransformerǁtransform__mutmut_126(self, results: Any) -> dict[str, Any]:
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
                "STD": float(np.std(vol)),
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

    def xǁGARCHTransformerǁtransform__mutmut_127(self, results: Any) -> dict[str, Any]:
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
                "std": float(None),
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

    def xǁGARCHTransformerǁtransform__mutmut_128(self, results: Any) -> dict[str, Any]:
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
                "std": float(np.std(None)),
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

    def xǁGARCHTransformerǁtransform__mutmut_129(self, results: Any) -> dict[str, Any]:
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
                "XXminXX": float(np.min(vol)),
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

    def xǁGARCHTransformerǁtransform__mutmut_130(self, results: Any) -> dict[str, Any]:
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
                "MIN": float(np.min(vol)),
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

    def xǁGARCHTransformerǁtransform__mutmut_131(self, results: Any) -> dict[str, Any]:
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
                "min": float(None),
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

    def xǁGARCHTransformerǁtransform__mutmut_132(self, results: Any) -> dict[str, Any]:
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
                "min": float(np.min(None)),
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

    def xǁGARCHTransformerǁtransform__mutmut_133(self, results: Any) -> dict[str, Any]:
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
                "XXmaxXX": float(np.max(vol)),
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

    def xǁGARCHTransformerǁtransform__mutmut_134(self, results: Any) -> dict[str, Any]:
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
                "MAX": float(np.max(vol)),
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

    def xǁGARCHTransformerǁtransform__mutmut_135(self, results: Any) -> dict[str, Any]:
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
                "max": float(None),
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

    def xǁGARCHTransformerǁtransform__mutmut_136(self, results: Any) -> dict[str, Any]:
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
                "max": float(np.max(None)),
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

    def xǁGARCHTransformerǁtransform__mutmut_137(self, results: Any) -> dict[str, Any]:
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
                "XXannualized_meanXX": float(np.mean(vol) * np.sqrt(252)),
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

    def xǁGARCHTransformerǁtransform__mutmut_138(self, results: Any) -> dict[str, Any]:
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
                "ANNUALIZED_MEAN": float(np.mean(vol) * np.sqrt(252)),
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

    def xǁGARCHTransformerǁtransform__mutmut_139(self, results: Any) -> dict[str, Any]:
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
                "annualized_mean": float(None),
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

    def xǁGARCHTransformerǁtransform__mutmut_140(self, results: Any) -> dict[str, Any]:
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
                "annualized_mean": float(np.mean(vol) / np.sqrt(252)),
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

    def xǁGARCHTransformerǁtransform__mutmut_141(self, results: Any) -> dict[str, Any]:
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
                "annualized_mean": float(np.mean(None) * np.sqrt(252)),
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

    def xǁGARCHTransformerǁtransform__mutmut_142(self, results: Any) -> dict[str, Any]:
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
                "annualized_mean": float(np.mean(vol) * np.sqrt(None)),
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

    def xǁGARCHTransformerǁtransform__mutmut_143(self, results: Any) -> dict[str, Any]:
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
                "annualized_mean": float(np.mean(vol) * np.sqrt(253)),
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

    def xǁGARCHTransformerǁtransform__mutmut_144(self, results: Any) -> dict[str, Any]:
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
        if hasattr(results, "std_resid") or results.std_resid is not None:
            z = np.asarray(results.std_resid)
            context["residual_stats"] = {
                "mean": float(np.mean(z)),
                "std": float(np.std(z)),
                "skewness": float(self._skewness(z)),
                "kurtosis": float(self._kurtosis(z)),
            }

        return context

    def xǁGARCHTransformerǁtransform__mutmut_145(self, results: Any) -> dict[str, Any]:
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
        if hasattr(None, "std_resid") and results.std_resid is not None:
            z = np.asarray(results.std_resid)
            context["residual_stats"] = {
                "mean": float(np.mean(z)),
                "std": float(np.std(z)),
                "skewness": float(self._skewness(z)),
                "kurtosis": float(self._kurtosis(z)),
            }

        return context

    def xǁGARCHTransformerǁtransform__mutmut_146(self, results: Any) -> dict[str, Any]:
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
        if hasattr(results, None) and results.std_resid is not None:
            z = np.asarray(results.std_resid)
            context["residual_stats"] = {
                "mean": float(np.mean(z)),
                "std": float(np.std(z)),
                "skewness": float(self._skewness(z)),
                "kurtosis": float(self._kurtosis(z)),
            }

        return context

    def xǁGARCHTransformerǁtransform__mutmut_147(self, results: Any) -> dict[str, Any]:
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
        if hasattr("std_resid") and results.std_resid is not None:
            z = np.asarray(results.std_resid)
            context["residual_stats"] = {
                "mean": float(np.mean(z)),
                "std": float(np.std(z)),
                "skewness": float(self._skewness(z)),
                "kurtosis": float(self._kurtosis(z)),
            }

        return context

    def xǁGARCHTransformerǁtransform__mutmut_148(self, results: Any) -> dict[str, Any]:
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
        if (
            hasattr(
                results,
            )
            and results.std_resid is not None
        ):
            z = np.asarray(results.std_resid)
            context["residual_stats"] = {
                "mean": float(np.mean(z)),
                "std": float(np.std(z)),
                "skewness": float(self._skewness(z)),
                "kurtosis": float(self._kurtosis(z)),
            }

        return context

    def xǁGARCHTransformerǁtransform__mutmut_149(self, results: Any) -> dict[str, Any]:
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
        if hasattr(results, "XXstd_residXX") and results.std_resid is not None:
            z = np.asarray(results.std_resid)
            context["residual_stats"] = {
                "mean": float(np.mean(z)),
                "std": float(np.std(z)),
                "skewness": float(self._skewness(z)),
                "kurtosis": float(self._kurtosis(z)),
            }

        return context

    def xǁGARCHTransformerǁtransform__mutmut_150(self, results: Any) -> dict[str, Any]:
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
        if hasattr(results, "STD_RESID") and results.std_resid is not None:
            z = np.asarray(results.std_resid)
            context["residual_stats"] = {
                "mean": float(np.mean(z)),
                "std": float(np.std(z)),
                "skewness": float(self._skewness(z)),
                "kurtosis": float(self._kurtosis(z)),
            }

        return context

    def xǁGARCHTransformerǁtransform__mutmut_151(self, results: Any) -> dict[str, Any]:
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
        if hasattr(results, "std_resid") and results.std_resid is None:
            z = np.asarray(results.std_resid)
            context["residual_stats"] = {
                "mean": float(np.mean(z)),
                "std": float(np.std(z)),
                "skewness": float(self._skewness(z)),
                "kurtosis": float(self._kurtosis(z)),
            }

        return context

    def xǁGARCHTransformerǁtransform__mutmut_152(self, results: Any) -> dict[str, Any]:
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
            z = None
            context["residual_stats"] = {
                "mean": float(np.mean(z)),
                "std": float(np.std(z)),
                "skewness": float(self._skewness(z)),
                "kurtosis": float(self._kurtosis(z)),
            }

        return context

    def xǁGARCHTransformerǁtransform__mutmut_153(self, results: Any) -> dict[str, Any]:
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
            z = np.asarray(None)
            context["residual_stats"] = {
                "mean": float(np.mean(z)),
                "std": float(np.std(z)),
                "skewness": float(self._skewness(z)),
                "kurtosis": float(self._kurtosis(z)),
            }

        return context

    def xǁGARCHTransformerǁtransform__mutmut_154(self, results: Any) -> dict[str, Any]:
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
            context["residual_stats"] = None

        return context

    def xǁGARCHTransformerǁtransform__mutmut_155(self, results: Any) -> dict[str, Any]:
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
            context["XXresidual_statsXX"] = {
                "mean": float(np.mean(z)),
                "std": float(np.std(z)),
                "skewness": float(self._skewness(z)),
                "kurtosis": float(self._kurtosis(z)),
            }

        return context

    def xǁGARCHTransformerǁtransform__mutmut_156(self, results: Any) -> dict[str, Any]:
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
            context["RESIDUAL_STATS"] = {
                "mean": float(np.mean(z)),
                "std": float(np.std(z)),
                "skewness": float(self._skewness(z)),
                "kurtosis": float(self._kurtosis(z)),
            }

        return context

    def xǁGARCHTransformerǁtransform__mutmut_157(self, results: Any) -> dict[str, Any]:
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
                "XXmeanXX": float(np.mean(z)),
                "std": float(np.std(z)),
                "skewness": float(self._skewness(z)),
                "kurtosis": float(self._kurtosis(z)),
            }

        return context

    def xǁGARCHTransformerǁtransform__mutmut_158(self, results: Any) -> dict[str, Any]:
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
                "MEAN": float(np.mean(z)),
                "std": float(np.std(z)),
                "skewness": float(self._skewness(z)),
                "kurtosis": float(self._kurtosis(z)),
            }

        return context

    def xǁGARCHTransformerǁtransform__mutmut_159(self, results: Any) -> dict[str, Any]:
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
                "mean": float(None),
                "std": float(np.std(z)),
                "skewness": float(self._skewness(z)),
                "kurtosis": float(self._kurtosis(z)),
            }

        return context

    def xǁGARCHTransformerǁtransform__mutmut_160(self, results: Any) -> dict[str, Any]:
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
                "mean": float(np.mean(None)),
                "std": float(np.std(z)),
                "skewness": float(self._skewness(z)),
                "kurtosis": float(self._kurtosis(z)),
            }

        return context

    def xǁGARCHTransformerǁtransform__mutmut_161(self, results: Any) -> dict[str, Any]:
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
                "XXstdXX": float(np.std(z)),
                "skewness": float(self._skewness(z)),
                "kurtosis": float(self._kurtosis(z)),
            }

        return context

    def xǁGARCHTransformerǁtransform__mutmut_162(self, results: Any) -> dict[str, Any]:
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
                "STD": float(np.std(z)),
                "skewness": float(self._skewness(z)),
                "kurtosis": float(self._kurtosis(z)),
            }

        return context

    def xǁGARCHTransformerǁtransform__mutmut_163(self, results: Any) -> dict[str, Any]:
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
                "std": float(None),
                "skewness": float(self._skewness(z)),
                "kurtosis": float(self._kurtosis(z)),
            }

        return context

    def xǁGARCHTransformerǁtransform__mutmut_164(self, results: Any) -> dict[str, Any]:
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
                "std": float(np.std(None)),
                "skewness": float(self._skewness(z)),
                "kurtosis": float(self._kurtosis(z)),
            }

        return context

    def xǁGARCHTransformerǁtransform__mutmut_165(self, results: Any) -> dict[str, Any]:
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
                "XXskewnessXX": float(self._skewness(z)),
                "kurtosis": float(self._kurtosis(z)),
            }

        return context

    def xǁGARCHTransformerǁtransform__mutmut_166(self, results: Any) -> dict[str, Any]:
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
                "SKEWNESS": float(self._skewness(z)),
                "kurtosis": float(self._kurtosis(z)),
            }

        return context

    def xǁGARCHTransformerǁtransform__mutmut_167(self, results: Any) -> dict[str, Any]:
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
                "skewness": float(None),
                "kurtosis": float(self._kurtosis(z)),
            }

        return context

    def xǁGARCHTransformerǁtransform__mutmut_168(self, results: Any) -> dict[str, Any]:
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
                "skewness": float(self._skewness(None)),
                "kurtosis": float(self._kurtosis(z)),
            }

        return context

    def xǁGARCHTransformerǁtransform__mutmut_169(self, results: Any) -> dict[str, Any]:
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
                "XXkurtosisXX": float(self._kurtosis(z)),
            }

        return context

    def xǁGARCHTransformerǁtransform__mutmut_170(self, results: Any) -> dict[str, Any]:
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
                "KURTOSIS": float(self._kurtosis(z)),
            }

        return context

    def xǁGARCHTransformerǁtransform__mutmut_171(self, results: Any) -> dict[str, Any]:
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
                "kurtosis": float(None),
            }

        return context

    def xǁGARCHTransformerǁtransform__mutmut_172(self, results: Any) -> dict[str, Any]:
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
                "kurtosis": float(self._kurtosis(None)),
            }

        return context

    xǁGARCHTransformerǁtransform__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGARCHTransformerǁtransform__mutmut_1": xǁGARCHTransformerǁtransform__mutmut_1,
        "xǁGARCHTransformerǁtransform__mutmut_2": xǁGARCHTransformerǁtransform__mutmut_2,
        "xǁGARCHTransformerǁtransform__mutmut_3": xǁGARCHTransformerǁtransform__mutmut_3,
        "xǁGARCHTransformerǁtransform__mutmut_4": xǁGARCHTransformerǁtransform__mutmut_4,
        "xǁGARCHTransformerǁtransform__mutmut_5": xǁGARCHTransformerǁtransform__mutmut_5,
        "xǁGARCHTransformerǁtransform__mutmut_6": xǁGARCHTransformerǁtransform__mutmut_6,
        "xǁGARCHTransformerǁtransform__mutmut_7": xǁGARCHTransformerǁtransform__mutmut_7,
        "xǁGARCHTransformerǁtransform__mutmut_8": xǁGARCHTransformerǁtransform__mutmut_8,
        "xǁGARCHTransformerǁtransform__mutmut_9": xǁGARCHTransformerǁtransform__mutmut_9,
        "xǁGARCHTransformerǁtransform__mutmut_10": xǁGARCHTransformerǁtransform__mutmut_10,
        "xǁGARCHTransformerǁtransform__mutmut_11": xǁGARCHTransformerǁtransform__mutmut_11,
        "xǁGARCHTransformerǁtransform__mutmut_12": xǁGARCHTransformerǁtransform__mutmut_12,
        "xǁGARCHTransformerǁtransform__mutmut_13": xǁGARCHTransformerǁtransform__mutmut_13,
        "xǁGARCHTransformerǁtransform__mutmut_14": xǁGARCHTransformerǁtransform__mutmut_14,
        "xǁGARCHTransformerǁtransform__mutmut_15": xǁGARCHTransformerǁtransform__mutmut_15,
        "xǁGARCHTransformerǁtransform__mutmut_16": xǁGARCHTransformerǁtransform__mutmut_16,
        "xǁGARCHTransformerǁtransform__mutmut_17": xǁGARCHTransformerǁtransform__mutmut_17,
        "xǁGARCHTransformerǁtransform__mutmut_18": xǁGARCHTransformerǁtransform__mutmut_18,
        "xǁGARCHTransformerǁtransform__mutmut_19": xǁGARCHTransformerǁtransform__mutmut_19,
        "xǁGARCHTransformerǁtransform__mutmut_20": xǁGARCHTransformerǁtransform__mutmut_20,
        "xǁGARCHTransformerǁtransform__mutmut_21": xǁGARCHTransformerǁtransform__mutmut_21,
        "xǁGARCHTransformerǁtransform__mutmut_22": xǁGARCHTransformerǁtransform__mutmut_22,
        "xǁGARCHTransformerǁtransform__mutmut_23": xǁGARCHTransformerǁtransform__mutmut_23,
        "xǁGARCHTransformerǁtransform__mutmut_24": xǁGARCHTransformerǁtransform__mutmut_24,
        "xǁGARCHTransformerǁtransform__mutmut_25": xǁGARCHTransformerǁtransform__mutmut_25,
        "xǁGARCHTransformerǁtransform__mutmut_26": xǁGARCHTransformerǁtransform__mutmut_26,
        "xǁGARCHTransformerǁtransform__mutmut_27": xǁGARCHTransformerǁtransform__mutmut_27,
        "xǁGARCHTransformerǁtransform__mutmut_28": xǁGARCHTransformerǁtransform__mutmut_28,
        "xǁGARCHTransformerǁtransform__mutmut_29": xǁGARCHTransformerǁtransform__mutmut_29,
        "xǁGARCHTransformerǁtransform__mutmut_30": xǁGARCHTransformerǁtransform__mutmut_30,
        "xǁGARCHTransformerǁtransform__mutmut_31": xǁGARCHTransformerǁtransform__mutmut_31,
        "xǁGARCHTransformerǁtransform__mutmut_32": xǁGARCHTransformerǁtransform__mutmut_32,
        "xǁGARCHTransformerǁtransform__mutmut_33": xǁGARCHTransformerǁtransform__mutmut_33,
        "xǁGARCHTransformerǁtransform__mutmut_34": xǁGARCHTransformerǁtransform__mutmut_34,
        "xǁGARCHTransformerǁtransform__mutmut_35": xǁGARCHTransformerǁtransform__mutmut_35,
        "xǁGARCHTransformerǁtransform__mutmut_36": xǁGARCHTransformerǁtransform__mutmut_36,
        "xǁGARCHTransformerǁtransform__mutmut_37": xǁGARCHTransformerǁtransform__mutmut_37,
        "xǁGARCHTransformerǁtransform__mutmut_38": xǁGARCHTransformerǁtransform__mutmut_38,
        "xǁGARCHTransformerǁtransform__mutmut_39": xǁGARCHTransformerǁtransform__mutmut_39,
        "xǁGARCHTransformerǁtransform__mutmut_40": xǁGARCHTransformerǁtransform__mutmut_40,
        "xǁGARCHTransformerǁtransform__mutmut_41": xǁGARCHTransformerǁtransform__mutmut_41,
        "xǁGARCHTransformerǁtransform__mutmut_42": xǁGARCHTransformerǁtransform__mutmut_42,
        "xǁGARCHTransformerǁtransform__mutmut_43": xǁGARCHTransformerǁtransform__mutmut_43,
        "xǁGARCHTransformerǁtransform__mutmut_44": xǁGARCHTransformerǁtransform__mutmut_44,
        "xǁGARCHTransformerǁtransform__mutmut_45": xǁGARCHTransformerǁtransform__mutmut_45,
        "xǁGARCHTransformerǁtransform__mutmut_46": xǁGARCHTransformerǁtransform__mutmut_46,
        "xǁGARCHTransformerǁtransform__mutmut_47": xǁGARCHTransformerǁtransform__mutmut_47,
        "xǁGARCHTransformerǁtransform__mutmut_48": xǁGARCHTransformerǁtransform__mutmut_48,
        "xǁGARCHTransformerǁtransform__mutmut_49": xǁGARCHTransformerǁtransform__mutmut_49,
        "xǁGARCHTransformerǁtransform__mutmut_50": xǁGARCHTransformerǁtransform__mutmut_50,
        "xǁGARCHTransformerǁtransform__mutmut_51": xǁGARCHTransformerǁtransform__mutmut_51,
        "xǁGARCHTransformerǁtransform__mutmut_52": xǁGARCHTransformerǁtransform__mutmut_52,
        "xǁGARCHTransformerǁtransform__mutmut_53": xǁGARCHTransformerǁtransform__mutmut_53,
        "xǁGARCHTransformerǁtransform__mutmut_54": xǁGARCHTransformerǁtransform__mutmut_54,
        "xǁGARCHTransformerǁtransform__mutmut_55": xǁGARCHTransformerǁtransform__mutmut_55,
        "xǁGARCHTransformerǁtransform__mutmut_56": xǁGARCHTransformerǁtransform__mutmut_56,
        "xǁGARCHTransformerǁtransform__mutmut_57": xǁGARCHTransformerǁtransform__mutmut_57,
        "xǁGARCHTransformerǁtransform__mutmut_58": xǁGARCHTransformerǁtransform__mutmut_58,
        "xǁGARCHTransformerǁtransform__mutmut_59": xǁGARCHTransformerǁtransform__mutmut_59,
        "xǁGARCHTransformerǁtransform__mutmut_60": xǁGARCHTransformerǁtransform__mutmut_60,
        "xǁGARCHTransformerǁtransform__mutmut_61": xǁGARCHTransformerǁtransform__mutmut_61,
        "xǁGARCHTransformerǁtransform__mutmut_62": xǁGARCHTransformerǁtransform__mutmut_62,
        "xǁGARCHTransformerǁtransform__mutmut_63": xǁGARCHTransformerǁtransform__mutmut_63,
        "xǁGARCHTransformerǁtransform__mutmut_64": xǁGARCHTransformerǁtransform__mutmut_64,
        "xǁGARCHTransformerǁtransform__mutmut_65": xǁGARCHTransformerǁtransform__mutmut_65,
        "xǁGARCHTransformerǁtransform__mutmut_66": xǁGARCHTransformerǁtransform__mutmut_66,
        "xǁGARCHTransformerǁtransform__mutmut_67": xǁGARCHTransformerǁtransform__mutmut_67,
        "xǁGARCHTransformerǁtransform__mutmut_68": xǁGARCHTransformerǁtransform__mutmut_68,
        "xǁGARCHTransformerǁtransform__mutmut_69": xǁGARCHTransformerǁtransform__mutmut_69,
        "xǁGARCHTransformerǁtransform__mutmut_70": xǁGARCHTransformerǁtransform__mutmut_70,
        "xǁGARCHTransformerǁtransform__mutmut_71": xǁGARCHTransformerǁtransform__mutmut_71,
        "xǁGARCHTransformerǁtransform__mutmut_72": xǁGARCHTransformerǁtransform__mutmut_72,
        "xǁGARCHTransformerǁtransform__mutmut_73": xǁGARCHTransformerǁtransform__mutmut_73,
        "xǁGARCHTransformerǁtransform__mutmut_74": xǁGARCHTransformerǁtransform__mutmut_74,
        "xǁGARCHTransformerǁtransform__mutmut_75": xǁGARCHTransformerǁtransform__mutmut_75,
        "xǁGARCHTransformerǁtransform__mutmut_76": xǁGARCHTransformerǁtransform__mutmut_76,
        "xǁGARCHTransformerǁtransform__mutmut_77": xǁGARCHTransformerǁtransform__mutmut_77,
        "xǁGARCHTransformerǁtransform__mutmut_78": xǁGARCHTransformerǁtransform__mutmut_78,
        "xǁGARCHTransformerǁtransform__mutmut_79": xǁGARCHTransformerǁtransform__mutmut_79,
        "xǁGARCHTransformerǁtransform__mutmut_80": xǁGARCHTransformerǁtransform__mutmut_80,
        "xǁGARCHTransformerǁtransform__mutmut_81": xǁGARCHTransformerǁtransform__mutmut_81,
        "xǁGARCHTransformerǁtransform__mutmut_82": xǁGARCHTransformerǁtransform__mutmut_82,
        "xǁGARCHTransformerǁtransform__mutmut_83": xǁGARCHTransformerǁtransform__mutmut_83,
        "xǁGARCHTransformerǁtransform__mutmut_84": xǁGARCHTransformerǁtransform__mutmut_84,
        "xǁGARCHTransformerǁtransform__mutmut_85": xǁGARCHTransformerǁtransform__mutmut_85,
        "xǁGARCHTransformerǁtransform__mutmut_86": xǁGARCHTransformerǁtransform__mutmut_86,
        "xǁGARCHTransformerǁtransform__mutmut_87": xǁGARCHTransformerǁtransform__mutmut_87,
        "xǁGARCHTransformerǁtransform__mutmut_88": xǁGARCHTransformerǁtransform__mutmut_88,
        "xǁGARCHTransformerǁtransform__mutmut_89": xǁGARCHTransformerǁtransform__mutmut_89,
        "xǁGARCHTransformerǁtransform__mutmut_90": xǁGARCHTransformerǁtransform__mutmut_90,
        "xǁGARCHTransformerǁtransform__mutmut_91": xǁGARCHTransformerǁtransform__mutmut_91,
        "xǁGARCHTransformerǁtransform__mutmut_92": xǁGARCHTransformerǁtransform__mutmut_92,
        "xǁGARCHTransformerǁtransform__mutmut_93": xǁGARCHTransformerǁtransform__mutmut_93,
        "xǁGARCHTransformerǁtransform__mutmut_94": xǁGARCHTransformerǁtransform__mutmut_94,
        "xǁGARCHTransformerǁtransform__mutmut_95": xǁGARCHTransformerǁtransform__mutmut_95,
        "xǁGARCHTransformerǁtransform__mutmut_96": xǁGARCHTransformerǁtransform__mutmut_96,
        "xǁGARCHTransformerǁtransform__mutmut_97": xǁGARCHTransformerǁtransform__mutmut_97,
        "xǁGARCHTransformerǁtransform__mutmut_98": xǁGARCHTransformerǁtransform__mutmut_98,
        "xǁGARCHTransformerǁtransform__mutmut_99": xǁGARCHTransformerǁtransform__mutmut_99,
        "xǁGARCHTransformerǁtransform__mutmut_100": xǁGARCHTransformerǁtransform__mutmut_100,
        "xǁGARCHTransformerǁtransform__mutmut_101": xǁGARCHTransformerǁtransform__mutmut_101,
        "xǁGARCHTransformerǁtransform__mutmut_102": xǁGARCHTransformerǁtransform__mutmut_102,
        "xǁGARCHTransformerǁtransform__mutmut_103": xǁGARCHTransformerǁtransform__mutmut_103,
        "xǁGARCHTransformerǁtransform__mutmut_104": xǁGARCHTransformerǁtransform__mutmut_104,
        "xǁGARCHTransformerǁtransform__mutmut_105": xǁGARCHTransformerǁtransform__mutmut_105,
        "xǁGARCHTransformerǁtransform__mutmut_106": xǁGARCHTransformerǁtransform__mutmut_106,
        "xǁGARCHTransformerǁtransform__mutmut_107": xǁGARCHTransformerǁtransform__mutmut_107,
        "xǁGARCHTransformerǁtransform__mutmut_108": xǁGARCHTransformerǁtransform__mutmut_108,
        "xǁGARCHTransformerǁtransform__mutmut_109": xǁGARCHTransformerǁtransform__mutmut_109,
        "xǁGARCHTransformerǁtransform__mutmut_110": xǁGARCHTransformerǁtransform__mutmut_110,
        "xǁGARCHTransformerǁtransform__mutmut_111": xǁGARCHTransformerǁtransform__mutmut_111,
        "xǁGARCHTransformerǁtransform__mutmut_112": xǁGARCHTransformerǁtransform__mutmut_112,
        "xǁGARCHTransformerǁtransform__mutmut_113": xǁGARCHTransformerǁtransform__mutmut_113,
        "xǁGARCHTransformerǁtransform__mutmut_114": xǁGARCHTransformerǁtransform__mutmut_114,
        "xǁGARCHTransformerǁtransform__mutmut_115": xǁGARCHTransformerǁtransform__mutmut_115,
        "xǁGARCHTransformerǁtransform__mutmut_116": xǁGARCHTransformerǁtransform__mutmut_116,
        "xǁGARCHTransformerǁtransform__mutmut_117": xǁGARCHTransformerǁtransform__mutmut_117,
        "xǁGARCHTransformerǁtransform__mutmut_118": xǁGARCHTransformerǁtransform__mutmut_118,
        "xǁGARCHTransformerǁtransform__mutmut_119": xǁGARCHTransformerǁtransform__mutmut_119,
        "xǁGARCHTransformerǁtransform__mutmut_120": xǁGARCHTransformerǁtransform__mutmut_120,
        "xǁGARCHTransformerǁtransform__mutmut_121": xǁGARCHTransformerǁtransform__mutmut_121,
        "xǁGARCHTransformerǁtransform__mutmut_122": xǁGARCHTransformerǁtransform__mutmut_122,
        "xǁGARCHTransformerǁtransform__mutmut_123": xǁGARCHTransformerǁtransform__mutmut_123,
        "xǁGARCHTransformerǁtransform__mutmut_124": xǁGARCHTransformerǁtransform__mutmut_124,
        "xǁGARCHTransformerǁtransform__mutmut_125": xǁGARCHTransformerǁtransform__mutmut_125,
        "xǁGARCHTransformerǁtransform__mutmut_126": xǁGARCHTransformerǁtransform__mutmut_126,
        "xǁGARCHTransformerǁtransform__mutmut_127": xǁGARCHTransformerǁtransform__mutmut_127,
        "xǁGARCHTransformerǁtransform__mutmut_128": xǁGARCHTransformerǁtransform__mutmut_128,
        "xǁGARCHTransformerǁtransform__mutmut_129": xǁGARCHTransformerǁtransform__mutmut_129,
        "xǁGARCHTransformerǁtransform__mutmut_130": xǁGARCHTransformerǁtransform__mutmut_130,
        "xǁGARCHTransformerǁtransform__mutmut_131": xǁGARCHTransformerǁtransform__mutmut_131,
        "xǁGARCHTransformerǁtransform__mutmut_132": xǁGARCHTransformerǁtransform__mutmut_132,
        "xǁGARCHTransformerǁtransform__mutmut_133": xǁGARCHTransformerǁtransform__mutmut_133,
        "xǁGARCHTransformerǁtransform__mutmut_134": xǁGARCHTransformerǁtransform__mutmut_134,
        "xǁGARCHTransformerǁtransform__mutmut_135": xǁGARCHTransformerǁtransform__mutmut_135,
        "xǁGARCHTransformerǁtransform__mutmut_136": xǁGARCHTransformerǁtransform__mutmut_136,
        "xǁGARCHTransformerǁtransform__mutmut_137": xǁGARCHTransformerǁtransform__mutmut_137,
        "xǁGARCHTransformerǁtransform__mutmut_138": xǁGARCHTransformerǁtransform__mutmut_138,
        "xǁGARCHTransformerǁtransform__mutmut_139": xǁGARCHTransformerǁtransform__mutmut_139,
        "xǁGARCHTransformerǁtransform__mutmut_140": xǁGARCHTransformerǁtransform__mutmut_140,
        "xǁGARCHTransformerǁtransform__mutmut_141": xǁGARCHTransformerǁtransform__mutmut_141,
        "xǁGARCHTransformerǁtransform__mutmut_142": xǁGARCHTransformerǁtransform__mutmut_142,
        "xǁGARCHTransformerǁtransform__mutmut_143": xǁGARCHTransformerǁtransform__mutmut_143,
        "xǁGARCHTransformerǁtransform__mutmut_144": xǁGARCHTransformerǁtransform__mutmut_144,
        "xǁGARCHTransformerǁtransform__mutmut_145": xǁGARCHTransformerǁtransform__mutmut_145,
        "xǁGARCHTransformerǁtransform__mutmut_146": xǁGARCHTransformerǁtransform__mutmut_146,
        "xǁGARCHTransformerǁtransform__mutmut_147": xǁGARCHTransformerǁtransform__mutmut_147,
        "xǁGARCHTransformerǁtransform__mutmut_148": xǁGARCHTransformerǁtransform__mutmut_148,
        "xǁGARCHTransformerǁtransform__mutmut_149": xǁGARCHTransformerǁtransform__mutmut_149,
        "xǁGARCHTransformerǁtransform__mutmut_150": xǁGARCHTransformerǁtransform__mutmut_150,
        "xǁGARCHTransformerǁtransform__mutmut_151": xǁGARCHTransformerǁtransform__mutmut_151,
        "xǁGARCHTransformerǁtransform__mutmut_152": xǁGARCHTransformerǁtransform__mutmut_152,
        "xǁGARCHTransformerǁtransform__mutmut_153": xǁGARCHTransformerǁtransform__mutmut_153,
        "xǁGARCHTransformerǁtransform__mutmut_154": xǁGARCHTransformerǁtransform__mutmut_154,
        "xǁGARCHTransformerǁtransform__mutmut_155": xǁGARCHTransformerǁtransform__mutmut_155,
        "xǁGARCHTransformerǁtransform__mutmut_156": xǁGARCHTransformerǁtransform__mutmut_156,
        "xǁGARCHTransformerǁtransform__mutmut_157": xǁGARCHTransformerǁtransform__mutmut_157,
        "xǁGARCHTransformerǁtransform__mutmut_158": xǁGARCHTransformerǁtransform__mutmut_158,
        "xǁGARCHTransformerǁtransform__mutmut_159": xǁGARCHTransformerǁtransform__mutmut_159,
        "xǁGARCHTransformerǁtransform__mutmut_160": xǁGARCHTransformerǁtransform__mutmut_160,
        "xǁGARCHTransformerǁtransform__mutmut_161": xǁGARCHTransformerǁtransform__mutmut_161,
        "xǁGARCHTransformerǁtransform__mutmut_162": xǁGARCHTransformerǁtransform__mutmut_162,
        "xǁGARCHTransformerǁtransform__mutmut_163": xǁGARCHTransformerǁtransform__mutmut_163,
        "xǁGARCHTransformerǁtransform__mutmut_164": xǁGARCHTransformerǁtransform__mutmut_164,
        "xǁGARCHTransformerǁtransform__mutmut_165": xǁGARCHTransformerǁtransform__mutmut_165,
        "xǁGARCHTransformerǁtransform__mutmut_166": xǁGARCHTransformerǁtransform__mutmut_166,
        "xǁGARCHTransformerǁtransform__mutmut_167": xǁGARCHTransformerǁtransform__mutmut_167,
        "xǁGARCHTransformerǁtransform__mutmut_168": xǁGARCHTransformerǁtransform__mutmut_168,
        "xǁGARCHTransformerǁtransform__mutmut_169": xǁGARCHTransformerǁtransform__mutmut_169,
        "xǁGARCHTransformerǁtransform__mutmut_170": xǁGARCHTransformerǁtransform__mutmut_170,
        "xǁGARCHTransformerǁtransform__mutmut_171": xǁGARCHTransformerǁtransform__mutmut_171,
        "xǁGARCHTransformerǁtransform__mutmut_172": xǁGARCHTransformerǁtransform__mutmut_172,
    }
    xǁGARCHTransformerǁtransform__mutmut_orig.__name__ = "xǁGARCHTransformerǁtransform"

    def _extract_params_table(self, results: Any) -> list[dict[str, Any]]:
        args = [results]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGARCHTransformerǁ_extract_params_table__mutmut_orig"),
            object.__getattribute__(
                self, "xǁGARCHTransformerǁ_extract_params_table__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_orig(
        self, results: Any
    ) -> list[dict[str, Any]]:
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_1(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = None
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_2(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = None
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_3(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(None, "params", None)
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_4(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, None, None)
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_5(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr("params", None)
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_6(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, None)
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_7(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = results.params
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_8(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "XXparamsXX", None)
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_9(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "PARAMS", None)
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_10(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = None
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_11(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = getattr(None, "param_names", None)
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_12(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = getattr(results, None, None)
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_13(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = getattr("param_names", None)
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_14(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = getattr(results, None)
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_15(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = results.param_names
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_16(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = getattr(results, "XXparam_namesXX", None)
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_17(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = getattr(results, "PARAM_NAMES", None)
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_18(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = getattr(results, "param_names", None)
        std_errors = None
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_19(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = getattr(results, "param_names", None)
        std_errors = getattr(None, "std_errors", None)
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_20(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = getattr(results, "param_names", None)
        std_errors = getattr(results, None, None)
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_21(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = getattr(results, "param_names", None)
        std_errors = getattr("std_errors", None)
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_22(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = getattr(results, "param_names", None)
        std_errors = getattr(results, None)
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_23(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = getattr(results, "param_names", None)
        std_errors = results.std_errors
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_24(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = getattr(results, "param_names", None)
        std_errors = getattr(results, "XXstd_errorsXX", None)
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_25(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = getattr(results, "param_names", None)
        std_errors = getattr(results, "STD_ERRORS", None)
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_26(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = getattr(results, "param_names", None)
        std_errors = getattr(results, "std_errors", None)
        tvalues = None
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_27(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = getattr(results, "param_names", None)
        std_errors = getattr(results, "std_errors", None)
        tvalues = getattr(None, "tvalues", None)
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_28(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = getattr(results, "param_names", None)
        std_errors = getattr(results, "std_errors", None)
        tvalues = getattr(results, None, None)
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_29(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = getattr(results, "param_names", None)
        std_errors = getattr(results, "std_errors", None)
        tvalues = getattr("tvalues", None)
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_30(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = getattr(results, "param_names", None)
        std_errors = getattr(results, "std_errors", None)
        tvalues = getattr(results, None)
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_31(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = getattr(results, "param_names", None)
        std_errors = getattr(results, "std_errors", None)
        tvalues = results.tvalues
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_32(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = getattr(results, "param_names", None)
        std_errors = getattr(results, "std_errors", None)
        tvalues = getattr(results, "XXtvaluesXX", None)
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_33(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = getattr(results, "param_names", None)
        std_errors = getattr(results, "std_errors", None)
        tvalues = getattr(results, "TVALUES", None)
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_34(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = getattr(results, "param_names", None)
        std_errors = getattr(results, "std_errors", None)
        tvalues = getattr(results, "tvalues", None)
        pvalues = None

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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_35(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = getattr(results, "param_names", None)
        std_errors = getattr(results, "std_errors", None)
        tvalues = getattr(results, "tvalues", None)
        pvalues = getattr(None, "pvalues", None)

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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_36(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = getattr(results, "param_names", None)
        std_errors = getattr(results, "std_errors", None)
        tvalues = getattr(results, "tvalues", None)
        pvalues = getattr(results, None, None)

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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_37(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = getattr(results, "param_names", None)
        std_errors = getattr(results, "std_errors", None)
        tvalues = getattr(results, "tvalues", None)
        pvalues = getattr("pvalues", None)

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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_38(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = getattr(results, "param_names", None)
        std_errors = getattr(results, "std_errors", None)
        tvalues = getattr(results, "tvalues", None)
        pvalues = getattr(results, None)

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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_39(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = getattr(results, "param_names", None)
        std_errors = getattr(results, "std_errors", None)
        tvalues = getattr(results, "tvalues", None)
        pvalues = results.pvalues

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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_40(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = getattr(results, "param_names", None)
        std_errors = getattr(results, "std_errors", None)
        tvalues = getattr(results, "tvalues", None)
        pvalues = getattr(results, "XXpvaluesXX", None)

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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_41(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = getattr(results, "param_names", None)
        std_errors = getattr(results, "std_errors", None)
        tvalues = getattr(results, "tvalues", None)
        pvalues = getattr(results, "PVALUES", None)

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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_42(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = getattr(results, "param_names", None)
        std_errors = getattr(results, "std_errors", None)
        tvalues = getattr(results, "tvalues", None)
        pvalues = getattr(results, "pvalues", None)

        if params is not None:
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_43(
        self, results: Any
    ) -> list[dict[str, Any]]:
        """Extract parameter table from results."""
        table = []
        params = getattr(results, "params", None)
        param_names = getattr(results, "param_names", None)
        std_errors = getattr(results, "std_errors", None)
        tvalues = getattr(results, "tvalues", None)
        pvalues = getattr(results, "pvalues", None)

        if params is None:
            return table

        n_params = None
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_44(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
        if param_names is not None:
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_45(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
            param_names = None

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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_46(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
            param_names = [f"param_{i}" for i in range(None)]

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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_47(
        self, results: Any
    ) -> list[dict[str, Any]]:
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

        for i in range(None):
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_48(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
            row: dict[str, Any] = None
            if std_errors is not None and i < len(std_errors):
                row["std_error"] = float(std_errors[i])
            if tvalues is not None and i < len(tvalues):
                row["t_stat"] = float(tvalues[i])
            if pvalues is not None and i < len(pvalues):
                row["p_value"] = float(pvalues[i])
                row["significance"] = self._significance_stars(pvalues[i])
            table.append(row)

        return table

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_49(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
                "XXnameXX": param_names[i] if i < len(param_names) else f"param_{i}",
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_50(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
                "NAME": param_names[i] if i < len(param_names) else f"param_{i}",
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_51(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
                "name": param_names[i] if i <= len(param_names) else f"param_{i}",
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_52(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
                "XXvalueXX": float(params[i]),
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_53(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
                "VALUE": float(params[i]),
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_54(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
                "value": float(None),
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

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_55(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
            if std_errors is not None or i < len(std_errors):
                row["std_error"] = float(std_errors[i])
            if tvalues is not None and i < len(tvalues):
                row["t_stat"] = float(tvalues[i])
            if pvalues is not None and i < len(pvalues):
                row["p_value"] = float(pvalues[i])
                row["significance"] = self._significance_stars(pvalues[i])
            table.append(row)

        return table

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_56(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
            if std_errors is None and i < len(std_errors):
                row["std_error"] = float(std_errors[i])
            if tvalues is not None and i < len(tvalues):
                row["t_stat"] = float(tvalues[i])
            if pvalues is not None and i < len(pvalues):
                row["p_value"] = float(pvalues[i])
                row["significance"] = self._significance_stars(pvalues[i])
            table.append(row)

        return table

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_57(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
            if std_errors is not None and i <= len(std_errors):
                row["std_error"] = float(std_errors[i])
            if tvalues is not None and i < len(tvalues):
                row["t_stat"] = float(tvalues[i])
            if pvalues is not None and i < len(pvalues):
                row["p_value"] = float(pvalues[i])
                row["significance"] = self._significance_stars(pvalues[i])
            table.append(row)

        return table

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_58(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
                row["std_error"] = None
            if tvalues is not None and i < len(tvalues):
                row["t_stat"] = float(tvalues[i])
            if pvalues is not None and i < len(pvalues):
                row["p_value"] = float(pvalues[i])
                row["significance"] = self._significance_stars(pvalues[i])
            table.append(row)

        return table

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_59(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
                row["XXstd_errorXX"] = float(std_errors[i])
            if tvalues is not None and i < len(tvalues):
                row["t_stat"] = float(tvalues[i])
            if pvalues is not None and i < len(pvalues):
                row["p_value"] = float(pvalues[i])
                row["significance"] = self._significance_stars(pvalues[i])
            table.append(row)

        return table

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_60(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
                row["STD_ERROR"] = float(std_errors[i])
            if tvalues is not None and i < len(tvalues):
                row["t_stat"] = float(tvalues[i])
            if pvalues is not None and i < len(pvalues):
                row["p_value"] = float(pvalues[i])
                row["significance"] = self._significance_stars(pvalues[i])
            table.append(row)

        return table

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_61(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
                row["std_error"] = float(None)
            if tvalues is not None and i < len(tvalues):
                row["t_stat"] = float(tvalues[i])
            if pvalues is not None and i < len(pvalues):
                row["p_value"] = float(pvalues[i])
                row["significance"] = self._significance_stars(pvalues[i])
            table.append(row)

        return table

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_62(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
            if tvalues is not None or i < len(tvalues):
                row["t_stat"] = float(tvalues[i])
            if pvalues is not None and i < len(pvalues):
                row["p_value"] = float(pvalues[i])
                row["significance"] = self._significance_stars(pvalues[i])
            table.append(row)

        return table

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_63(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
            if tvalues is None and i < len(tvalues):
                row["t_stat"] = float(tvalues[i])
            if pvalues is not None and i < len(pvalues):
                row["p_value"] = float(pvalues[i])
                row["significance"] = self._significance_stars(pvalues[i])
            table.append(row)

        return table

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_64(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
            if tvalues is not None and i <= len(tvalues):
                row["t_stat"] = float(tvalues[i])
            if pvalues is not None and i < len(pvalues):
                row["p_value"] = float(pvalues[i])
                row["significance"] = self._significance_stars(pvalues[i])
            table.append(row)

        return table

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_65(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
                row["t_stat"] = None
            if pvalues is not None and i < len(pvalues):
                row["p_value"] = float(pvalues[i])
                row["significance"] = self._significance_stars(pvalues[i])
            table.append(row)

        return table

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_66(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
                row["XXt_statXX"] = float(tvalues[i])
            if pvalues is not None and i < len(pvalues):
                row["p_value"] = float(pvalues[i])
                row["significance"] = self._significance_stars(pvalues[i])
            table.append(row)

        return table

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_67(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
                row["T_STAT"] = float(tvalues[i])
            if pvalues is not None and i < len(pvalues):
                row["p_value"] = float(pvalues[i])
                row["significance"] = self._significance_stars(pvalues[i])
            table.append(row)

        return table

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_68(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
                row["t_stat"] = float(None)
            if pvalues is not None and i < len(pvalues):
                row["p_value"] = float(pvalues[i])
                row["significance"] = self._significance_stars(pvalues[i])
            table.append(row)

        return table

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_69(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
            if pvalues is not None or i < len(pvalues):
                row["p_value"] = float(pvalues[i])
                row["significance"] = self._significance_stars(pvalues[i])
            table.append(row)

        return table

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_70(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
            if pvalues is None and i < len(pvalues):
                row["p_value"] = float(pvalues[i])
                row["significance"] = self._significance_stars(pvalues[i])
            table.append(row)

        return table

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_71(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
            if pvalues is not None and i <= len(pvalues):
                row["p_value"] = float(pvalues[i])
                row["significance"] = self._significance_stars(pvalues[i])
            table.append(row)

        return table

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_72(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
                row["p_value"] = None
                row["significance"] = self._significance_stars(pvalues[i])
            table.append(row)

        return table

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_73(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
                row["XXp_valueXX"] = float(pvalues[i])
                row["significance"] = self._significance_stars(pvalues[i])
            table.append(row)

        return table

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_74(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
                row["P_VALUE"] = float(pvalues[i])
                row["significance"] = self._significance_stars(pvalues[i])
            table.append(row)

        return table

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_75(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
                row["p_value"] = float(None)
                row["significance"] = self._significance_stars(pvalues[i])
            table.append(row)

        return table

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_76(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
                row["significance"] = None
            table.append(row)

        return table

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_77(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
                row["XXsignificanceXX"] = self._significance_stars(pvalues[i])
            table.append(row)

        return table

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_78(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
                row["SIGNIFICANCE"] = self._significance_stars(pvalues[i])
            table.append(row)

        return table

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_79(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
                row["significance"] = self._significance_stars(None)
            table.append(row)

        return table

    def xǁGARCHTransformerǁ_extract_params_table__mutmut_80(
        self, results: Any
    ) -> list[dict[str, Any]]:
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
            table.append(None)

        return table

    xǁGARCHTransformerǁ_extract_params_table__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_1": xǁGARCHTransformerǁ_extract_params_table__mutmut_1,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_2": xǁGARCHTransformerǁ_extract_params_table__mutmut_2,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_3": xǁGARCHTransformerǁ_extract_params_table__mutmut_3,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_4": xǁGARCHTransformerǁ_extract_params_table__mutmut_4,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_5": xǁGARCHTransformerǁ_extract_params_table__mutmut_5,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_6": xǁGARCHTransformerǁ_extract_params_table__mutmut_6,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_7": xǁGARCHTransformerǁ_extract_params_table__mutmut_7,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_8": xǁGARCHTransformerǁ_extract_params_table__mutmut_8,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_9": xǁGARCHTransformerǁ_extract_params_table__mutmut_9,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_10": xǁGARCHTransformerǁ_extract_params_table__mutmut_10,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_11": xǁGARCHTransformerǁ_extract_params_table__mutmut_11,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_12": xǁGARCHTransformerǁ_extract_params_table__mutmut_12,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_13": xǁGARCHTransformerǁ_extract_params_table__mutmut_13,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_14": xǁGARCHTransformerǁ_extract_params_table__mutmut_14,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_15": xǁGARCHTransformerǁ_extract_params_table__mutmut_15,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_16": xǁGARCHTransformerǁ_extract_params_table__mutmut_16,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_17": xǁGARCHTransformerǁ_extract_params_table__mutmut_17,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_18": xǁGARCHTransformerǁ_extract_params_table__mutmut_18,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_19": xǁGARCHTransformerǁ_extract_params_table__mutmut_19,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_20": xǁGARCHTransformerǁ_extract_params_table__mutmut_20,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_21": xǁGARCHTransformerǁ_extract_params_table__mutmut_21,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_22": xǁGARCHTransformerǁ_extract_params_table__mutmut_22,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_23": xǁGARCHTransformerǁ_extract_params_table__mutmut_23,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_24": xǁGARCHTransformerǁ_extract_params_table__mutmut_24,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_25": xǁGARCHTransformerǁ_extract_params_table__mutmut_25,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_26": xǁGARCHTransformerǁ_extract_params_table__mutmut_26,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_27": xǁGARCHTransformerǁ_extract_params_table__mutmut_27,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_28": xǁGARCHTransformerǁ_extract_params_table__mutmut_28,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_29": xǁGARCHTransformerǁ_extract_params_table__mutmut_29,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_30": xǁGARCHTransformerǁ_extract_params_table__mutmut_30,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_31": xǁGARCHTransformerǁ_extract_params_table__mutmut_31,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_32": xǁGARCHTransformerǁ_extract_params_table__mutmut_32,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_33": xǁGARCHTransformerǁ_extract_params_table__mutmut_33,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_34": xǁGARCHTransformerǁ_extract_params_table__mutmut_34,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_35": xǁGARCHTransformerǁ_extract_params_table__mutmut_35,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_36": xǁGARCHTransformerǁ_extract_params_table__mutmut_36,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_37": xǁGARCHTransformerǁ_extract_params_table__mutmut_37,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_38": xǁGARCHTransformerǁ_extract_params_table__mutmut_38,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_39": xǁGARCHTransformerǁ_extract_params_table__mutmut_39,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_40": xǁGARCHTransformerǁ_extract_params_table__mutmut_40,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_41": xǁGARCHTransformerǁ_extract_params_table__mutmut_41,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_42": xǁGARCHTransformerǁ_extract_params_table__mutmut_42,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_43": xǁGARCHTransformerǁ_extract_params_table__mutmut_43,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_44": xǁGARCHTransformerǁ_extract_params_table__mutmut_44,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_45": xǁGARCHTransformerǁ_extract_params_table__mutmut_45,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_46": xǁGARCHTransformerǁ_extract_params_table__mutmut_46,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_47": xǁGARCHTransformerǁ_extract_params_table__mutmut_47,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_48": xǁGARCHTransformerǁ_extract_params_table__mutmut_48,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_49": xǁGARCHTransformerǁ_extract_params_table__mutmut_49,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_50": xǁGARCHTransformerǁ_extract_params_table__mutmut_50,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_51": xǁGARCHTransformerǁ_extract_params_table__mutmut_51,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_52": xǁGARCHTransformerǁ_extract_params_table__mutmut_52,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_53": xǁGARCHTransformerǁ_extract_params_table__mutmut_53,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_54": xǁGARCHTransformerǁ_extract_params_table__mutmut_54,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_55": xǁGARCHTransformerǁ_extract_params_table__mutmut_55,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_56": xǁGARCHTransformerǁ_extract_params_table__mutmut_56,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_57": xǁGARCHTransformerǁ_extract_params_table__mutmut_57,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_58": xǁGARCHTransformerǁ_extract_params_table__mutmut_58,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_59": xǁGARCHTransformerǁ_extract_params_table__mutmut_59,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_60": xǁGARCHTransformerǁ_extract_params_table__mutmut_60,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_61": xǁGARCHTransformerǁ_extract_params_table__mutmut_61,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_62": xǁGARCHTransformerǁ_extract_params_table__mutmut_62,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_63": xǁGARCHTransformerǁ_extract_params_table__mutmut_63,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_64": xǁGARCHTransformerǁ_extract_params_table__mutmut_64,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_65": xǁGARCHTransformerǁ_extract_params_table__mutmut_65,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_66": xǁGARCHTransformerǁ_extract_params_table__mutmut_66,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_67": xǁGARCHTransformerǁ_extract_params_table__mutmut_67,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_68": xǁGARCHTransformerǁ_extract_params_table__mutmut_68,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_69": xǁGARCHTransformerǁ_extract_params_table__mutmut_69,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_70": xǁGARCHTransformerǁ_extract_params_table__mutmut_70,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_71": xǁGARCHTransformerǁ_extract_params_table__mutmut_71,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_72": xǁGARCHTransformerǁ_extract_params_table__mutmut_72,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_73": xǁGARCHTransformerǁ_extract_params_table__mutmut_73,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_74": xǁGARCHTransformerǁ_extract_params_table__mutmut_74,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_75": xǁGARCHTransformerǁ_extract_params_table__mutmut_75,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_76": xǁGARCHTransformerǁ_extract_params_table__mutmut_76,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_77": xǁGARCHTransformerǁ_extract_params_table__mutmut_77,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_78": xǁGARCHTransformerǁ_extract_params_table__mutmut_78,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_79": xǁGARCHTransformerǁ_extract_params_table__mutmut_79,
        "xǁGARCHTransformerǁ_extract_params_table__mutmut_80": xǁGARCHTransformerǁ_extract_params_table__mutmut_80,
    }
    xǁGARCHTransformerǁ_extract_params_table__mutmut_orig.__name__ = (
        "xǁGARCHTransformerǁ_extract_params_table"
    )

    def _extract_diagnostics(self, results: Any) -> dict[str, Any]:
        args = [results]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGARCHTransformerǁ_extract_diagnostics__mutmut_orig"),
            object.__getattribute__(
                self, "xǁGARCHTransformerǁ_extract_diagnostics__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )

    def xǁGARCHTransformerǁ_extract_diagnostics__mutmut_orig(self, results: Any) -> dict[str, Any]:
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

    def xǁGARCHTransformerǁ_extract_diagnostics__mutmut_1(self, results: Any) -> dict[str, Any]:
        """Extract diagnostic test results."""
        diag: dict[str, Any] = None

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

    def xǁGARCHTransformerǁ_extract_diagnostics__mutmut_2(self, results: Any) -> dict[str, Any]:
        """Extract diagnostic test results."""
        diag: dict[str, Any] = {}

        # ARCH-LM test
        if hasattr(None, "arch_lm"):
            diag["arch_lm"] = results.arch_lm

        # Ljung-Box on squared residuals
        if hasattr(results, "ljung_box_z2"):
            diag["ljung_box_z2"] = results.ljung_box_z2

        # Sign bias test
        if hasattr(results, "sign_bias"):
            diag["sign_bias"] = results.sign_bias

        return diag

    def xǁGARCHTransformerǁ_extract_diagnostics__mutmut_3(self, results: Any) -> dict[str, Any]:
        """Extract diagnostic test results."""
        diag: dict[str, Any] = {}

        # ARCH-LM test
        if hasattr(results, None):
            diag["arch_lm"] = results.arch_lm

        # Ljung-Box on squared residuals
        if hasattr(results, "ljung_box_z2"):
            diag["ljung_box_z2"] = results.ljung_box_z2

        # Sign bias test
        if hasattr(results, "sign_bias"):
            diag["sign_bias"] = results.sign_bias

        return diag

    def xǁGARCHTransformerǁ_extract_diagnostics__mutmut_4(self, results: Any) -> dict[str, Any]:
        """Extract diagnostic test results."""
        diag: dict[str, Any] = {}

        # ARCH-LM test
        if hasattr("arch_lm"):
            diag["arch_lm"] = results.arch_lm

        # Ljung-Box on squared residuals
        if hasattr(results, "ljung_box_z2"):
            diag["ljung_box_z2"] = results.ljung_box_z2

        # Sign bias test
        if hasattr(results, "sign_bias"):
            diag["sign_bias"] = results.sign_bias

        return diag

    def xǁGARCHTransformerǁ_extract_diagnostics__mutmut_5(self, results: Any) -> dict[str, Any]:
        """Extract diagnostic test results."""
        diag: dict[str, Any] = {}

        # ARCH-LM test
        if hasattr(
            results,
        ):
            diag["arch_lm"] = results.arch_lm

        # Ljung-Box on squared residuals
        if hasattr(results, "ljung_box_z2"):
            diag["ljung_box_z2"] = results.ljung_box_z2

        # Sign bias test
        if hasattr(results, "sign_bias"):
            diag["sign_bias"] = results.sign_bias

        return diag

    def xǁGARCHTransformerǁ_extract_diagnostics__mutmut_6(self, results: Any) -> dict[str, Any]:
        """Extract diagnostic test results."""
        diag: dict[str, Any] = {}

        # ARCH-LM test
        if hasattr(results, "XXarch_lmXX"):
            diag["arch_lm"] = results.arch_lm

        # Ljung-Box on squared residuals
        if hasattr(results, "ljung_box_z2"):
            diag["ljung_box_z2"] = results.ljung_box_z2

        # Sign bias test
        if hasattr(results, "sign_bias"):
            diag["sign_bias"] = results.sign_bias

        return diag

    def xǁGARCHTransformerǁ_extract_diagnostics__mutmut_7(self, results: Any) -> dict[str, Any]:
        """Extract diagnostic test results."""
        diag: dict[str, Any] = {}

        # ARCH-LM test
        if hasattr(results, "ARCH_LM"):
            diag["arch_lm"] = results.arch_lm

        # Ljung-Box on squared residuals
        if hasattr(results, "ljung_box_z2"):
            diag["ljung_box_z2"] = results.ljung_box_z2

        # Sign bias test
        if hasattr(results, "sign_bias"):
            diag["sign_bias"] = results.sign_bias

        return diag

    def xǁGARCHTransformerǁ_extract_diagnostics__mutmut_8(self, results: Any) -> dict[str, Any]:
        """Extract diagnostic test results."""
        diag: dict[str, Any] = {}

        # ARCH-LM test
        if hasattr(results, "arch_lm"):
            diag["arch_lm"] = None

        # Ljung-Box on squared residuals
        if hasattr(results, "ljung_box_z2"):
            diag["ljung_box_z2"] = results.ljung_box_z2

        # Sign bias test
        if hasattr(results, "sign_bias"):
            diag["sign_bias"] = results.sign_bias

        return diag

    def xǁGARCHTransformerǁ_extract_diagnostics__mutmut_9(self, results: Any) -> dict[str, Any]:
        """Extract diagnostic test results."""
        diag: dict[str, Any] = {}

        # ARCH-LM test
        if hasattr(results, "arch_lm"):
            diag["XXarch_lmXX"] = results.arch_lm

        # Ljung-Box on squared residuals
        if hasattr(results, "ljung_box_z2"):
            diag["ljung_box_z2"] = results.ljung_box_z2

        # Sign bias test
        if hasattr(results, "sign_bias"):
            diag["sign_bias"] = results.sign_bias

        return diag

    def xǁGARCHTransformerǁ_extract_diagnostics__mutmut_10(self, results: Any) -> dict[str, Any]:
        """Extract diagnostic test results."""
        diag: dict[str, Any] = {}

        # ARCH-LM test
        if hasattr(results, "arch_lm"):
            diag["ARCH_LM"] = results.arch_lm

        # Ljung-Box on squared residuals
        if hasattr(results, "ljung_box_z2"):
            diag["ljung_box_z2"] = results.ljung_box_z2

        # Sign bias test
        if hasattr(results, "sign_bias"):
            diag["sign_bias"] = results.sign_bias

        return diag

    def xǁGARCHTransformerǁ_extract_diagnostics__mutmut_11(self, results: Any) -> dict[str, Any]:
        """Extract diagnostic test results."""
        diag: dict[str, Any] = {}

        # ARCH-LM test
        if hasattr(results, "arch_lm"):
            diag["arch_lm"] = results.arch_lm

        # Ljung-Box on squared residuals
        if hasattr(None, "ljung_box_z2"):
            diag["ljung_box_z2"] = results.ljung_box_z2

        # Sign bias test
        if hasattr(results, "sign_bias"):
            diag["sign_bias"] = results.sign_bias

        return diag

    def xǁGARCHTransformerǁ_extract_diagnostics__mutmut_12(self, results: Any) -> dict[str, Any]:
        """Extract diagnostic test results."""
        diag: dict[str, Any] = {}

        # ARCH-LM test
        if hasattr(results, "arch_lm"):
            diag["arch_lm"] = results.arch_lm

        # Ljung-Box on squared residuals
        if hasattr(results, None):
            diag["ljung_box_z2"] = results.ljung_box_z2

        # Sign bias test
        if hasattr(results, "sign_bias"):
            diag["sign_bias"] = results.sign_bias

        return diag

    def xǁGARCHTransformerǁ_extract_diagnostics__mutmut_13(self, results: Any) -> dict[str, Any]:
        """Extract diagnostic test results."""
        diag: dict[str, Any] = {}

        # ARCH-LM test
        if hasattr(results, "arch_lm"):
            diag["arch_lm"] = results.arch_lm

        # Ljung-Box on squared residuals
        if hasattr("ljung_box_z2"):
            diag["ljung_box_z2"] = results.ljung_box_z2

        # Sign bias test
        if hasattr(results, "sign_bias"):
            diag["sign_bias"] = results.sign_bias

        return diag

    def xǁGARCHTransformerǁ_extract_diagnostics__mutmut_14(self, results: Any) -> dict[str, Any]:
        """Extract diagnostic test results."""
        diag: dict[str, Any] = {}

        # ARCH-LM test
        if hasattr(results, "arch_lm"):
            diag["arch_lm"] = results.arch_lm

        # Ljung-Box on squared residuals
        if hasattr(
            results,
        ):
            diag["ljung_box_z2"] = results.ljung_box_z2

        # Sign bias test
        if hasattr(results, "sign_bias"):
            diag["sign_bias"] = results.sign_bias

        return diag

    def xǁGARCHTransformerǁ_extract_diagnostics__mutmut_15(self, results: Any) -> dict[str, Any]:
        """Extract diagnostic test results."""
        diag: dict[str, Any] = {}

        # ARCH-LM test
        if hasattr(results, "arch_lm"):
            diag["arch_lm"] = results.arch_lm

        # Ljung-Box on squared residuals
        if hasattr(results, "XXljung_box_z2XX"):
            diag["ljung_box_z2"] = results.ljung_box_z2

        # Sign bias test
        if hasattr(results, "sign_bias"):
            diag["sign_bias"] = results.sign_bias

        return diag

    def xǁGARCHTransformerǁ_extract_diagnostics__mutmut_16(self, results: Any) -> dict[str, Any]:
        """Extract diagnostic test results."""
        diag: dict[str, Any] = {}

        # ARCH-LM test
        if hasattr(results, "arch_lm"):
            diag["arch_lm"] = results.arch_lm

        # Ljung-Box on squared residuals
        if hasattr(results, "LJUNG_BOX_Z2"):
            diag["ljung_box_z2"] = results.ljung_box_z2

        # Sign bias test
        if hasattr(results, "sign_bias"):
            diag["sign_bias"] = results.sign_bias

        return diag

    def xǁGARCHTransformerǁ_extract_diagnostics__mutmut_17(self, results: Any) -> dict[str, Any]:
        """Extract diagnostic test results."""
        diag: dict[str, Any] = {}

        # ARCH-LM test
        if hasattr(results, "arch_lm"):
            diag["arch_lm"] = results.arch_lm

        # Ljung-Box on squared residuals
        if hasattr(results, "ljung_box_z2"):
            diag["ljung_box_z2"] = None

        # Sign bias test
        if hasattr(results, "sign_bias"):
            diag["sign_bias"] = results.sign_bias

        return diag

    def xǁGARCHTransformerǁ_extract_diagnostics__mutmut_18(self, results: Any) -> dict[str, Any]:
        """Extract diagnostic test results."""
        diag: dict[str, Any] = {}

        # ARCH-LM test
        if hasattr(results, "arch_lm"):
            diag["arch_lm"] = results.arch_lm

        # Ljung-Box on squared residuals
        if hasattr(results, "ljung_box_z2"):
            diag["XXljung_box_z2XX"] = results.ljung_box_z2

        # Sign bias test
        if hasattr(results, "sign_bias"):
            diag["sign_bias"] = results.sign_bias

        return diag

    def xǁGARCHTransformerǁ_extract_diagnostics__mutmut_19(self, results: Any) -> dict[str, Any]:
        """Extract diagnostic test results."""
        diag: dict[str, Any] = {}

        # ARCH-LM test
        if hasattr(results, "arch_lm"):
            diag["arch_lm"] = results.arch_lm

        # Ljung-Box on squared residuals
        if hasattr(results, "ljung_box_z2"):
            diag["LJUNG_BOX_Z2"] = results.ljung_box_z2

        # Sign bias test
        if hasattr(results, "sign_bias"):
            diag["sign_bias"] = results.sign_bias

        return diag

    def xǁGARCHTransformerǁ_extract_diagnostics__mutmut_20(self, results: Any) -> dict[str, Any]:
        """Extract diagnostic test results."""
        diag: dict[str, Any] = {}

        # ARCH-LM test
        if hasattr(results, "arch_lm"):
            diag["arch_lm"] = results.arch_lm

        # Ljung-Box on squared residuals
        if hasattr(results, "ljung_box_z2"):
            diag["ljung_box_z2"] = results.ljung_box_z2

        # Sign bias test
        if hasattr(None, "sign_bias"):
            diag["sign_bias"] = results.sign_bias

        return diag

    def xǁGARCHTransformerǁ_extract_diagnostics__mutmut_21(self, results: Any) -> dict[str, Any]:
        """Extract diagnostic test results."""
        diag: dict[str, Any] = {}

        # ARCH-LM test
        if hasattr(results, "arch_lm"):
            diag["arch_lm"] = results.arch_lm

        # Ljung-Box on squared residuals
        if hasattr(results, "ljung_box_z2"):
            diag["ljung_box_z2"] = results.ljung_box_z2

        # Sign bias test
        if hasattr(results, None):
            diag["sign_bias"] = results.sign_bias

        return diag

    def xǁGARCHTransformerǁ_extract_diagnostics__mutmut_22(self, results: Any) -> dict[str, Any]:
        """Extract diagnostic test results."""
        diag: dict[str, Any] = {}

        # ARCH-LM test
        if hasattr(results, "arch_lm"):
            diag["arch_lm"] = results.arch_lm

        # Ljung-Box on squared residuals
        if hasattr(results, "ljung_box_z2"):
            diag["ljung_box_z2"] = results.ljung_box_z2

        # Sign bias test
        if hasattr("sign_bias"):
            diag["sign_bias"] = results.sign_bias

        return diag

    def xǁGARCHTransformerǁ_extract_diagnostics__mutmut_23(self, results: Any) -> dict[str, Any]:
        """Extract diagnostic test results."""
        diag: dict[str, Any] = {}

        # ARCH-LM test
        if hasattr(results, "arch_lm"):
            diag["arch_lm"] = results.arch_lm

        # Ljung-Box on squared residuals
        if hasattr(results, "ljung_box_z2"):
            diag["ljung_box_z2"] = results.ljung_box_z2

        # Sign bias test
        if hasattr(
            results,
        ):
            diag["sign_bias"] = results.sign_bias

        return diag

    def xǁGARCHTransformerǁ_extract_diagnostics__mutmut_24(self, results: Any) -> dict[str, Any]:
        """Extract diagnostic test results."""
        diag: dict[str, Any] = {}

        # ARCH-LM test
        if hasattr(results, "arch_lm"):
            diag["arch_lm"] = results.arch_lm

        # Ljung-Box on squared residuals
        if hasattr(results, "ljung_box_z2"):
            diag["ljung_box_z2"] = results.ljung_box_z2

        # Sign bias test
        if hasattr(results, "XXsign_biasXX"):
            diag["sign_bias"] = results.sign_bias

        return diag

    def xǁGARCHTransformerǁ_extract_diagnostics__mutmut_25(self, results: Any) -> dict[str, Any]:
        """Extract diagnostic test results."""
        diag: dict[str, Any] = {}

        # ARCH-LM test
        if hasattr(results, "arch_lm"):
            diag["arch_lm"] = results.arch_lm

        # Ljung-Box on squared residuals
        if hasattr(results, "ljung_box_z2"):
            diag["ljung_box_z2"] = results.ljung_box_z2

        # Sign bias test
        if hasattr(results, "SIGN_BIAS"):
            diag["sign_bias"] = results.sign_bias

        return diag

    def xǁGARCHTransformerǁ_extract_diagnostics__mutmut_26(self, results: Any) -> dict[str, Any]:
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
            diag["sign_bias"] = None

        return diag

    def xǁGARCHTransformerǁ_extract_diagnostics__mutmut_27(self, results: Any) -> dict[str, Any]:
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
            diag["XXsign_biasXX"] = results.sign_bias

        return diag

    def xǁGARCHTransformerǁ_extract_diagnostics__mutmut_28(self, results: Any) -> dict[str, Any]:
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
            diag["SIGN_BIAS"] = results.sign_bias

        return diag

    xǁGARCHTransformerǁ_extract_diagnostics__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGARCHTransformerǁ_extract_diagnostics__mutmut_1": xǁGARCHTransformerǁ_extract_diagnostics__mutmut_1,
        "xǁGARCHTransformerǁ_extract_diagnostics__mutmut_2": xǁGARCHTransformerǁ_extract_diagnostics__mutmut_2,
        "xǁGARCHTransformerǁ_extract_diagnostics__mutmut_3": xǁGARCHTransformerǁ_extract_diagnostics__mutmut_3,
        "xǁGARCHTransformerǁ_extract_diagnostics__mutmut_4": xǁGARCHTransformerǁ_extract_diagnostics__mutmut_4,
        "xǁGARCHTransformerǁ_extract_diagnostics__mutmut_5": xǁGARCHTransformerǁ_extract_diagnostics__mutmut_5,
        "xǁGARCHTransformerǁ_extract_diagnostics__mutmut_6": xǁGARCHTransformerǁ_extract_diagnostics__mutmut_6,
        "xǁGARCHTransformerǁ_extract_diagnostics__mutmut_7": xǁGARCHTransformerǁ_extract_diagnostics__mutmut_7,
        "xǁGARCHTransformerǁ_extract_diagnostics__mutmut_8": xǁGARCHTransformerǁ_extract_diagnostics__mutmut_8,
        "xǁGARCHTransformerǁ_extract_diagnostics__mutmut_9": xǁGARCHTransformerǁ_extract_diagnostics__mutmut_9,
        "xǁGARCHTransformerǁ_extract_diagnostics__mutmut_10": xǁGARCHTransformerǁ_extract_diagnostics__mutmut_10,
        "xǁGARCHTransformerǁ_extract_diagnostics__mutmut_11": xǁGARCHTransformerǁ_extract_diagnostics__mutmut_11,
        "xǁGARCHTransformerǁ_extract_diagnostics__mutmut_12": xǁGARCHTransformerǁ_extract_diagnostics__mutmut_12,
        "xǁGARCHTransformerǁ_extract_diagnostics__mutmut_13": xǁGARCHTransformerǁ_extract_diagnostics__mutmut_13,
        "xǁGARCHTransformerǁ_extract_diagnostics__mutmut_14": xǁGARCHTransformerǁ_extract_diagnostics__mutmut_14,
        "xǁGARCHTransformerǁ_extract_diagnostics__mutmut_15": xǁGARCHTransformerǁ_extract_diagnostics__mutmut_15,
        "xǁGARCHTransformerǁ_extract_diagnostics__mutmut_16": xǁGARCHTransformerǁ_extract_diagnostics__mutmut_16,
        "xǁGARCHTransformerǁ_extract_diagnostics__mutmut_17": xǁGARCHTransformerǁ_extract_diagnostics__mutmut_17,
        "xǁGARCHTransformerǁ_extract_diagnostics__mutmut_18": xǁGARCHTransformerǁ_extract_diagnostics__mutmut_18,
        "xǁGARCHTransformerǁ_extract_diagnostics__mutmut_19": xǁGARCHTransformerǁ_extract_diagnostics__mutmut_19,
        "xǁGARCHTransformerǁ_extract_diagnostics__mutmut_20": xǁGARCHTransformerǁ_extract_diagnostics__mutmut_20,
        "xǁGARCHTransformerǁ_extract_diagnostics__mutmut_21": xǁGARCHTransformerǁ_extract_diagnostics__mutmut_21,
        "xǁGARCHTransformerǁ_extract_diagnostics__mutmut_22": xǁGARCHTransformerǁ_extract_diagnostics__mutmut_22,
        "xǁGARCHTransformerǁ_extract_diagnostics__mutmut_23": xǁGARCHTransformerǁ_extract_diagnostics__mutmut_23,
        "xǁGARCHTransformerǁ_extract_diagnostics__mutmut_24": xǁGARCHTransformerǁ_extract_diagnostics__mutmut_24,
        "xǁGARCHTransformerǁ_extract_diagnostics__mutmut_25": xǁGARCHTransformerǁ_extract_diagnostics__mutmut_25,
        "xǁGARCHTransformerǁ_extract_diagnostics__mutmut_26": xǁGARCHTransformerǁ_extract_diagnostics__mutmut_26,
        "xǁGARCHTransformerǁ_extract_diagnostics__mutmut_27": xǁGARCHTransformerǁ_extract_diagnostics__mutmut_27,
        "xǁGARCHTransformerǁ_extract_diagnostics__mutmut_28": xǁGARCHTransformerǁ_extract_diagnostics__mutmut_28,
    }
    xǁGARCHTransformerǁ_extract_diagnostics__mutmut_orig.__name__ = (
        "xǁGARCHTransformerǁ_extract_diagnostics"
    )

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
