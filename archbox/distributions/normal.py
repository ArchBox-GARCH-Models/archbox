"""Normal (Gaussian) conditional distribution."""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy import stats

from archbox.distributions.base import Distribution, as_scalar_or_array

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
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation Normal log-likelihood.

        Parameters
        ----------
        resids : ndarray
            Residuals eps_t, shape (T,).
        sigma2 : ndarray
            Conditional variance sigma^2_t, shape (T,).
        dist_params : ndarray, optional
            Ignored (Normal has no shape parameters).

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        # Written as in-place updates on two freshly allocated buffers: the
        # optimizer calls this on every likelihood evaluation, and the naive
        # expression allocates five temporaries of length T instead of two.
        # The arithmetic (and its floating-point result) is unchanged.
        out = np.log(sigma2)
        out += _LOG_2PI
        ratio = np.square(resids)
        ratio /= sigma2
        out += ratio
        out *= -0.5
        return out

    def ppf(self, q: float | NDArray[np.float64]) -> Any:
        """Normal percent point function.

        Parameters
        ----------
        q : float or ndarray
            Quantile(s) in (0, 1).

        Returns
        -------
        float or ndarray
            Value x such that Phi(x) = q.
        """
        return as_scalar_or_array(np.asarray(stats.norm.ppf(q), dtype=np.float64), q)

    def cdf(self, x: float | NDArray[np.float64]) -> Any:
        """Normal CDF.

        Parameters
        ----------
        x : float or ndarray
            Value(s).

        Returns
        -------
        float or ndarray
            Phi(x).
        """
        return as_scalar_or_array(np.asarray(stats.norm.cdf(x), dtype=np.float64), x)

    def simulate(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate n standard normal draws.

        Parameters
        ----------
        n : int
            Number of draws.
        rng : np.random.Generator
            Random number generator.
        dist_params : ndarray, optional
            Ignored (Normal has no shape parameters).

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
