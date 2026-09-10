"""Base class for conditional distributions."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import numpy as np
from numpy.typing import NDArray


def as_scalar_or_array(values: NDArray[np.float64], like: float | NDArray[np.float64]) -> Any:
    """Shape a computed result like its input.

    ``ppf`` and ``cdf`` accept either a scalar or an array; this returns a
    Python ``float`` when the caller passed a scalar (or a 0-d array) and an
    ``ndarray`` when the caller passed an array, so both call styles work.

    Parameters
    ----------
    values : ndarray
        Computed values (always an array internally).
    like : float or ndarray
        The original input.

    Returns
    -------
    float or ndarray
        ``values`` reshaped to match ``like``.
    """
    arr = np.asarray(values, dtype=np.float64)
    if isinstance(like, np.ndarray) and like.ndim > 0:
        return arr
    return float(arr.reshape(-1)[0])


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
    def ppf(self, q: float | NDArray[np.float64]) -> Any:
        """Percent point function (inverse CDF).

        Parameters
        ----------
        q : float or ndarray
            Quantile(s) in (0, 1).

        Returns
        -------
        float or ndarray
            Value x such that P(Z <= x) = q; a float for scalar input, an
            array (same shape) for array input.
        """

    @abstractmethod
    def cdf(self, x: float | NDArray[np.float64]) -> Any:
        """Cumulative distribution function.

        Parameters
        ----------
        x : float or ndarray
            Value(s).

        Returns
        -------
        float or ndarray
            P(Z <= x); a float for scalar input, an array for array input.
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
