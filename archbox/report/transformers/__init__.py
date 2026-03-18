"""Result transformers for report generation.

Each transformer extracts relevant data from fitted model results
and formats it as a template context dictionary.
"""

from archbox.report.transformers.garch import GARCHTransformer
from archbox.report.transformers.multivariate import MultivariateTransformer
from archbox.report.transformers.regime import RegimeTransformer
from archbox.report.transformers.risk import RiskTransformer

__all__ = [
    "GARCHTransformer",
    "MultivariateTransformer",
    "RegimeTransformer",
    "RiskTransformer",
]
