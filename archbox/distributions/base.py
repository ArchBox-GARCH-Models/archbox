"""Base class for conditional distributions."""

from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np
from numpy.typing import NDArray


class Distribution(ABC):
    """Abstract base class for conditional distributions.

    The distribution defines the shape of the log-likelihood and provides
    simulation capabilities for z_t ~ D(0,1).
    """

    name: str = "Unknown"

    @abstractmethod
    def loglikelihood(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood.

        Parameters
        ----------
        resids : ndarray
            Residuals eps_t = r_t - mu, shape (T,).
        sigma2 : ndarray
            Conditional variance sigma^2_t, shape (T,).
        dist_params : ndarray, optional
            Distribution shape parameters.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """

    def transform_params(self, unconstrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Transform unconstrained distribution params to constrained space.

        Default is a no-op (for distributions with no shape parameters).
        """
        return unconstrained

    def untransform_params(self, constrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Transform constrained distribution params to unconstrained space.

        Default is a no-op (for distributions with no shape parameters).
        """
        return constrained

    @abstractmethod
    def ppf(self, q: float) -> float:
        """Percent point function (inverse CDF).

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Value x such that P(Z <= x) = q.
        """

    @abstractmethod
    def cdf(self, x: float) -> float:
        """Cumulative distribution function.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """

    @abstractmethod
    def simulate(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate n draws from D(0, 1).

        Parameters
        ----------
        n : int
            Number of draws.
        rng : np.random.Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution shape parameters (ignored by parameter-free distributions).

        Returns
        -------
        ndarray
            Simulated innovations z_t, shape (n,).
        """

    @property
    @abstractmethod
    def num_params(self) -> int:
        """Number of distribution parameters (0 for Normal)."""

    @property
    @abstractmethod
    def param_names(self) -> list[str]:
        """Distribution parameter names."""

    @abstractmethod
    def start_params(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""

    @abstractmethod
    def bounds(self) -> list[tuple[float, float]]:
        """Bounds for distribution parameters."""
