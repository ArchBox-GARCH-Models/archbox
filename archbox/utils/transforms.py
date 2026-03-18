"""Parameter transformations for constrained optimization.

Transformacoes garantem que os parametros do GARCH satisfacam:
- omega > 0
- alpha_i >= 0
- beta_j >= 0
- sum(alpha_i) + sum(beta_j) < 1 (estacionariedade)
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def positive_transform(x: NDArray[np.float64]) -> NDArray[np.float64]:
    """Transform unconstrained -> positive via exp."""
    return np.exp(x)


def positive_untransform(y: NDArray[np.float64]) -> NDArray[np.float64]:
    """Transform positive -> unconstrained via log."""
    return np.log(y)


def unit_transform(x: NDArray[np.float64]) -> NDArray[np.float64]:
    """Transform unconstrained -> (0, 1) via sigmoid."""
    return 1.0 / (1.0 + np.exp(-x))


def unit_untransform(y: NDArray[np.float64]) -> NDArray[np.float64]:
    """Transform (0, 1) -> unconstrained via logit."""
    return np.log(y / (1.0 - y))


def stationarity_transform(
    alphas: NDArray[np.float64], betas: NDArray[np.float64]
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Ensure sum(alphas) + sum(betas) < 1.

    Aplica sigmoid individual e depois escala para que a soma < 1.
    """
    raw = np.concatenate([alphas, betas])
    individual = 1.0 / (1.0 + np.exp(-raw))
    total = np.sum(individual)
    if total >= 0.9999:
        scale = 0.9999 / total
        individual = individual * scale
    n_alpha = len(alphas)
    return individual[:n_alpha], individual[n_alpha:]
