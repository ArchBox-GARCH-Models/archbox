"""Student-t conditional distribution (Bollerslev, 1987).

f(z; nu) = Gamma((nu+1)/2) / (sqrt(pi*(nu-2)) * Gamma(nu/2)) * (1 + z^2/(nu-2))^{-(nu+1)/2}
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from scipy import stats
from scipy.special import gammaln

from archbox.distributions.base import Distribution


class StudentT(Distribution):
    """Student-t distribution for GARCH models.

    Parameters
    ----------
    nu : float, optional
        Degrees of freedom. Must be > 2. If None, estimated from data.
    """

    name = "Student-t"

    def __init__(self, nu: float | None = None) -> None:
        """Initialize Student-t distribution with optional degrees of freedom."""
        self._fixed_nu = nu

    @property
    def num_params(self) -> int:
        """Number of distribution shape parameters."""
        return 0 if self._fixed_nu is not None else 1

    @property
    def param_names(self) -> list[str]:
        """Distribution parameter names."""
        return [] if self._fixed_nu is not None else ["nu"]

    def start_params(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        if self._fixed_nu is not None:
            return np.array([], dtype=np.float64)
        return np.array([8.0])

    def _get_nu(self, dist_params: NDArray[np.float64] | None = None) -> float:
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and len(dist_params) > 0:
            nu = float(dist_params[0])
        else:
            nu = 8.0
        return max(nu, 2.01)

    def loglikelihood(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals (eps_t).
        sigma2 : ndarray
            Conditional variance (sigma^2_t).
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        z = resids / np.sqrt(sigma2)

        ll = (
            gammaln((nu + 1) / 2)
            - gammaln(nu / 2)
            - 0.5 * np.log(np.pi * (nu - 2))
            - 0.5 * np.log(sigma2)
            - ((nu + 1) / 2) * np.log(1 + z**2 / (nu - 2))
        )
        return ll

    def ppf(self, q: float) -> float:
        """Percent point function for standardized Student-t.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Value x such that P(Z <= x) = q.
        """
        nu = self._get_nu()
        # Standardize: t(nu) has variance nu/(nu-2)
        return float(stats.t.ppf(q, df=nu) / np.sqrt(nu / (nu - 2)))

    def cdf(self, x: float) -> float:
        """CDF for standardized Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        nu = self._get_nu()
        return float(stats.t.cdf(x * np.sqrt(nu / (nu - 2)), df=nu))

    def simulate(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Student-t distribution.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Standardized random variates (zero mean, unit variance).
        """
        nu = self._get_nu(dist_params)
        z = rng.standard_t(nu, size=n)
        z = z / np.sqrt(nu / (nu - 2))
        return z

    def transform_params(self, unconstrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Transform: nu = 2 + exp(x) ensures nu > 2."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        constrained[0] = 2.0 + np.exp(unconstrained[0])
        return constrained

    def untransform_params(self, constrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Inverse transform: x = log(nu - 2)."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0] - 2.0, 1e-6))
        return unconstrained

    def bounds(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        if self._fixed_nu is not None:
            return []
        return [(2.01, 100.0)]
