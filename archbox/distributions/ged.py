"""GED - Generalized Error Distribution (Nelson, 1991).

f(z; nu) = nu / (lambda * 2^{1+1/nu} * Gamma(1/nu)) * exp(-0.5 * |z/lambda|^nu)

lambda = sqrt(2^{-2/nu} * Gamma(1/nu) / Gamma(3/nu))

Special cases: nu=2 (Normal), nu=1 (Laplace).
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy.special import gammainc, gammaincinv, gammaln

from archbox.distributions.base import Distribution, as_scalar_or_array


class GeneralizedError(Distribution):
    """Generalized Error Distribution for GARCH models.

    Parameters
    ----------
    nu : float, optional
        Shape parameter. Must be > 0. If None, estimated from data.
        nu=2 is Normal, nu=1 is Laplace.
    """

    name = "GED"

    #: Bounds of the shape parameter; ``transform_params`` maps onto this open
    #: interval and ``_get_nu`` clamps to it, so transform, clamp and
    #: ``bounds()`` are mutually consistent.
    NU_MIN: float = 0.1
    NU_MAX: float = 20.0

    def __init__(self, nu: float | None = None) -> None:
        """Initialize GED distribution with optional shape parameter."""
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
        return np.array([1.5])  # between Laplace and Normal

    def _get_nu(self, dist_params: NDArray[np.float64] | None = None) -> float:
        """Extract nu from ``dist_params`` or the fixed value.

        An estimated nu is clamped to the declared ``bounds()``; a nu fixed by
        the user only has to stay in the validity domain ``nu > 0``.
        """
        if self._fixed_nu is not None:
            return max(float(self._fixed_nu), 1e-3)
        has_params = dist_params is not None and len(dist_params) > 0
        nu = float(dist_params[0]) if has_params and dist_params is not None else 1.5
        return float(np.clip(nu, self.NU_MIN, self.NU_MAX))

    @staticmethod
    def _lambda_ged(nu: float) -> float:
        """Compute the GED scale parameter lambda.

        lambda = sqrt(2^{-2/nu} * Gamma(1/nu) / Gamma(3/nu))
        """
        return float(np.sqrt(2 ** (-2.0 / nu) * np.exp(gammaln(1.0 / nu) - gammaln(3.0 / nu))))

    def loglikelihood(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under GED.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)
        z = resids / np.sqrt(sigma2)

        # loglike = log(nu) - log(lambda) - (1+1/nu)*log(2) - gammaln(1/nu)
        #           - 0.5 * |z/lambda|^nu - 0.5 * log(sigma2)
        ll = (
            np.log(nu)
            - np.log(lam)
            - (1 + 1.0 / nu) * np.log(2)
            - gammaln(1.0 / nu)
            - 0.5 * np.abs(z / lam) ** nu
            - 0.5 * np.log(sigma2)
        )
        return ll

    def ppf(self, q: float | NDArray[np.float64]) -> Any:
        """Percent point function for standardized GED.

        Uses the symmetry ``P(|Z| <= x) = gammainc(1/nu, 0.5 (x/lam)^nu)``:
        ``x = lam (2 gammaincinv(1/nu, |2q - 1|))^(1/nu)`` with the sign of
        ``q - 0.5``.

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
        lam = self._lambda_ged(nu)

        q_arr = np.asarray(q, dtype=np.float64)
        tail = np.abs(2.0 * q_arr - 1.0)
        val = np.asarray(gammaincinv(1.0 / nu, tail), dtype=np.float64)
        magnitude = lam * (2.0 * val) ** (1.0 / nu)
        values = np.sign(q_arr - 0.5) * magnitude
        return as_scalar_or_array(values, q)

    def cdf(self, x: float | NDArray[np.float64]) -> Any:
        """CDF for standardized GED.

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
        lam = self._lambda_ged(nu)

        x_arr = np.asarray(x, dtype=np.float64)
        u = 0.5 * np.abs(x_arr / lam) ** nu
        g = np.asarray(gammainc(1.0 / nu, u), dtype=np.float64)
        values = np.where(x_arr >= 0.0, 0.5 * (1.0 + g), 0.5 * (1.0 - g))
        return as_scalar_or_array(values, x)

    def simulate(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized GED.

        Uses the representation: if U ~ Gamma(1/nu, 1), then
        X = sign(V) * (2*U)^{1/nu} * lambda has GED(nu) distribution.

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
            Standardized random variates.
        """
        nu = self._get_nu(dist_params)
        lam = self._lambda_ged(nu)

        # Generate using gamma distribution
        u = rng.gamma(1.0 / nu, scale=1.0, size=n)
        signs = 2 * rng.integers(0, 2, size=n) - 1
        z = signs * (2 * u) ** (1.0 / nu) * lam

        return z

    def transform_params(self, unconstrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Transform x -> nu in the open interval ``(NU_MIN, NU_MAX)``.

        The scaled logistic keeps the optimum interior to the declared
        ``bounds()``, so the clamp in ``_get_nu`` never bites at the optimum.
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
