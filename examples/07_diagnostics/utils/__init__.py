"""Utility functions for diagnostics examples."""

from .data_generator import (
    generate_misspecified_data,
    generate_sp500_returns,
    generate_structural_break_data,
)
from .plot_helpers import (
    plot_news_impact_curve,
    plot_nyblom_recursive,
    plot_residual_diagnostics,
    plot_sign_bias_scatter,
    plot_standardized_residuals,
)
