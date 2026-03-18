"""Multivariate GARCH model implementations.

Available models:
- CCC: Constant Conditional Correlation (Bollerslev, 1990)
- DCC: Dynamic Conditional Correlation (Engle, 2002)
- BEKK: Baba-Engle-Kraft-Kroner (Engle & Kroner, 1995)
- GOGARCH: Generalized Orthogonal GARCH (van der Weide, 2002)
- DECO: Dynamic Equicorrelation (Engle & Kelly, 2012)
"""

from archbox.multivariate.base import MultivariateVolatilityModel, MultivarResults
from archbox.multivariate.bekk import BEKK
from archbox.multivariate.ccc import CCC
from archbox.multivariate.dcc import DCC
from archbox.multivariate.deco import DECO
from archbox.multivariate.gogarch import GOGARCH
from archbox.multivariate.portfolio import (
    marginal_risk_contribution,
    minimum_variance_weights,
    minimum_variance_weights_dynamic,
    portfolio_variance,
    portfolio_volatility,
    risk_contribution,
    risk_decomposition,
)

__all__ = [
    # Base
    "MultivariateVolatilityModel",
    "MultivarResults",
    # Models
    "BEKK",
    "CCC",
    "DCC",
    "DECO",
    "GOGARCH",
    # Portfolio utilities
    "marginal_risk_contribution",
    "minimum_variance_weights",
    "minimum_variance_weights_dynamic",
    "portfolio_variance",
    "portfolio_volatility",
    "risk_contribution",
    "risk_decomposition",
]
