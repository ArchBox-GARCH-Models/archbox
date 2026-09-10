"""Multivariate GARCH model implementations.

Available models:
- CCC: Constant Conditional Correlation (Bollerslev, 1990)
- DCC: Dynamic Conditional Correlation (Engle, 2002)
- BEKK: Baba-Engle-Kraft-Kroner (Engle & Kroner, 1995)
- GOGARCH: Generalized Orthogonal GARCH (van der Weide, 2002)
- DECO: Dynamic Equicorrelation (Engle & Kelly, 2012)
"""

from archbox.multivariate.base import (
    MultivariateVolatilityModel,
    OptimOutcome,
    correlation_loglike,
)
from archbox.multivariate.bekk import BEKK
from archbox.multivariate.ccc import CCC
from archbox.multivariate.dcc import DCC
from archbox.multivariate.deco import DECO, equicorrelation_loglike
from archbox.multivariate.gogarch import GOGARCH, fast_ica, pca_whiten
from archbox.multivariate.portfolio import (
    marginal_risk_contribution,
    minimum_variance_weights,
    minimum_variance_weights_dynamic,
    portfolio_variance,
    portfolio_volatility,
    risk_contribution,
    risk_decomposition,
)
from archbox.multivariate.results import MultivarResults
from archbox.multivariate.utils import (
    corr_to_cov,
    cov_to_corr,
    ensure_positive_definite,
    is_positive_definite,
    numerical_hessian,
    standard_errors_from_hessian,
    validate_multivariate_returns,
)

__all__ = [
    # Base
    "MultivariateVolatilityModel",
    "MultivarResults",
    "OptimOutcome",
    "correlation_loglike",
    "equicorrelation_loglike",
    # Models
    "BEKK",
    "CCC",
    "DCC",
    "DECO",
    "GOGARCH",
    # Factor extraction
    "fast_ica",
    "pca_whiten",
    # Portfolio utilities
    "marginal_risk_contribution",
    "minimum_variance_weights",
    "minimum_variance_weights_dynamic",
    "portfolio_variance",
    "portfolio_volatility",
    "risk_contribution",
    "risk_decomposition",
    # Matrix utilities
    "corr_to_cov",
    "cov_to_corr",
    "ensure_positive_definite",
    "is_positive_definite",
    "numerical_hessian",
    "standard_errors_from_hessian",
    "validate_multivariate_returns",
]
