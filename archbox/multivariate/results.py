"""Multivariate GARCH results - re-exported from base module.

The MultivarResults class is defined in base.py for circular import reasons.
This module re-exports it for convenience.
"""

from archbox.multivariate.base import MultivarResults

__all__ = ["MultivarResults"]
