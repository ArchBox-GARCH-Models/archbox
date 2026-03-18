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
