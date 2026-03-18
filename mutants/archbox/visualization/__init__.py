"""Visualization module for archbox.

Provides professional-quality charts for volatility models, diagnostics,
regime-switching, correlations, distributions, and risk analysis.

Usage:
    from archbox.visualization import plot_volatility, plot_diagnostics
    from archbox.visualization.themes import get_theme
    from archbox.visualization.export import export_png
"""

from archbox.visualization.correlation_plot import (
    plot_correlation_heatmap,
    plot_covariance_decomposition,
    plot_dynamic_correlation,
)
from archbox.visualization.diagnostics_plot import plot_diagnostics
from archbox.visualization.distribution_plot import plot_distribution_fit
from archbox.visualization.news_impact_plot import plot_news_impact, plot_news_impact_comparison
from archbox.visualization.regime_plot import plot_regimes, plot_transition_matrix
from archbox.visualization.risk_plot import (
    plot_traffic_light,
    plot_var_backtest,
    plot_var_comparison,
)
from archbox.visualization.transition_plot import plot_phase_diagram, plot_transition_function
from archbox.visualization.volatility_plot import plot_variance_persistence, plot_volatility

__all__ = [
    # Volatility
    "plot_volatility",
    "plot_variance_persistence",
    # News Impact
    "plot_news_impact",
    "plot_news_impact_comparison",
    # Diagnostics
    "plot_diagnostics",
    # Regime
    "plot_regimes",
    "plot_transition_matrix",
    # Transition
    "plot_transition_function",
    "plot_phase_diagram",
    # Correlation
    "plot_dynamic_correlation",
    "plot_correlation_heatmap",
    "plot_covariance_decomposition",
    # Distribution
    "plot_distribution_fit",
    # Risk
    "plot_var_backtest",
    "plot_traffic_light",
    "plot_var_comparison",
]
from collections.abc import Callable
from typing import Annotated, ClassVar

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
