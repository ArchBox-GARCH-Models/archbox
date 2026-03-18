"""Normal (Gaussian) conditional distribution."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from scipy import stats

from archbox.distributions.base import Distribution

_LOG_2PI = np.log(2.0 * np.pi)


class Normal(Distribution):
    """Standard Normal distribution for GARCH innovations.

    The log-likelihood per observation is:
        ll_t = -0.5 * (log(2*pi) + log(sigma^2_t) + eps^2_t / sigma^2_t)

    No additional parameters.
    """

    name: str = "Normal"

    def loglikelihood(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute per-observation Normal log-likelihood.

        Parameters
        ----------
        resids : ndarray
            Residuals eps_t, shape (T,).
        sigma2 : ndarray
            Conditional variance sigma^2_t, shape (T,).

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        return -0.5 * (_LOG_2PI + np.log(sigma2) + resids**2 / sigma2)

    def ppf(self, q: float) -> float:
        """Normal percent point function.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Value x such that Phi(x) = q.
        """
        return float(stats.norm.ppf(q))

    def cdf(self, x: float) -> float:
        """Normal CDF.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            Phi(x).
        """
        return float(stats.norm.cdf(x))

    def simulate(self, n: int, rng: np.random.Generator) -> NDArray[np.float64]:
        """Simulate n standard normal draws.

        Parameters
        ----------
        n : int
            Number of draws.
        rng : np.random.Generator
            Random number generator.

        Returns
        -------
        ndarray
            z_t ~ N(0,1), shape (n,).
        """
        return rng.standard_normal(n)

    @property
    def num_params(self) -> int:
        """Normal has no additional parameters."""
        return 0

    @property
    def param_names(self) -> list[str]:
        """No parameter names."""
        return []

    def start_params(self) -> NDArray[np.float64]:
        """Empty array (no parameters)."""
        return np.array([], dtype=np.float64)

    def bounds(self) -> list[tuple[float, float]]:
        """Empty list (no parameters)."""
        return []
