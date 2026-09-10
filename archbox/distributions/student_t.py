"""Student-t conditional distribution (Bollerslev, 1987).

f(z; nu) = Gamma((nu+1)/2) / (sqrt(pi*(nu-2)) * Gamma(nu/2)) * (1 + z^2/(nu-2))^{-(nu+1)/2}
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy import stats
from scipy.special import gammaln

from archbox.distributions.base import Distribution, as_scalar_or_array


class StudentT(Distribution):
    """Student-t distribution for GARCH models.

    Parameters
    ----------
    nu : float, optional
        Degrees of freedom. Must be > 2. If None, estimated from data.
    """

    name = "Student-t"

    #: Bounds of the shape parameter. ``transform_params`` maps the whole real
    #: line onto this open interval and ``_get_nu`` clamps to it, so the
    #: declared ``bounds()``, the transform and the likelihood always agree.
    NU_MIN: float = 2.01
    NU_MAX: float = 100.0

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
        """Extract nu from ``dist_params`` or the fixed value.

        An *estimated* nu is clamped to the declared ``bounds()`` (the same
        interval ``transform_params`` maps onto, so the clamp never bites at the
        optimum). A nu fixed by the user is only clamped to the validity domain
        ``nu > 2``: pinning ``nu = 200`` is a legitimate choice, not an
        optimizer excursion.
        """
        if self._fixed_nu is not None:
            return max(float(self._fixed_nu), self.NU_MIN)
        has_params = dist_params is not None and len(dist_params) > 0
        nu = float(dist_params[0]) if has_params and dist_params is not None else 8.0
        return float(np.clip(nu, self.NU_MIN, self.NU_MAX))

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

    def ppf(self, q: float | NDArray[np.float64]) -> Any:
        """Percent point function for standardized Student-t.

        Parameters
        ----------
        q : float or ndarray
            Quantile(s) in (0, 1).

        Returns
        -------
        float or ndarray
            Value x such that P(Z <= x) = q.
        """
        nu = self._get_nu()
        # Standardize: t(nu) has variance nu/(nu-2)
        values = np.asarray(stats.t.ppf(q, df=nu), dtype=np.float64) / np.sqrt(nu / (nu - 2))
        return as_scalar_or_array(values, q)

    def cdf(self, x: float | NDArray[np.float64]) -> Any:
        """CDF for standardized Student-t.

        Parameters
        ----------
        x : float or ndarray
            Value(s).

        Returns
        -------
        float or ndarray
            P(Z <= x).
        """
        nu = self._get_nu()
        scaled = np.asarray(x, dtype=np.float64) * np.sqrt(nu / (nu - 2))
        return as_scalar_or_array(np.asarray(stats.t.cdf(scaled, df=nu), dtype=np.float64), x)

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
        """Transform x -> nu in the open interval ``(NU_MIN, NU_MAX)``.

        The scaled logistic keeps the optimum interior to the declared
        ``bounds()``, so the clamp in ``_get_nu`` never truncates the value the
        optimizer is actually exploring.
        """
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        span = self.NU_MAX - self.NU_MIN
        weight = 1.0 / (1.0 + np.exp(-np.clip(unconstrained[0], -50.0, 50.0)))
        constrained[0] = self.NU_MIN + span * weight
        return constrained

    def untransform_params(self, constrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Inverse of :meth:`transform_params` (logit of the rescaled nu)."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        span = self.NU_MAX - self.NU_MIN
        weight = (float(constrained[0]) - self.NU_MIN) / span
        weight = float(np.clip(weight, 1e-8, 1.0 - 1e-8))
        unconstrained[0] = np.log(weight / (1.0 - weight))
        return unconstrained

    def bounds(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        if self._fixed_nu is not None:
            return []
        return [(self.NU_MIN, self.NU_MAX)]
