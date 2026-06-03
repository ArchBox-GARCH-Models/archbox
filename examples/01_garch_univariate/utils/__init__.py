"""Utility functions for GARCH univariate examples."""

from .data_generator import (
    generate_bitcoin_returns,
    generate_ibovespa_returns,
    generate_sp500_returns,
)
from .plot_helpers import (
    plot_acf_pacf,
    plot_model_comparison,
    plot_news_impact,
    plot_qq,
    plot_returns,
    plot_volatility,
)
