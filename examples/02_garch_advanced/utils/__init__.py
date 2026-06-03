"""Utility functions for advanced GARCH examples."""

from .data_generator import (
    generate_figarch_returns,
    generate_garchm_returns,
    generate_realized_volatility,
    generate_sp500_returns,
)

__all__ = [
    "generate_figarch_returns",
    "generate_garchm_returns",
    "generate_realized_volatility",
    "generate_sp500_returns",
]
