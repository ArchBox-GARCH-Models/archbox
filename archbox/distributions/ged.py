"""GED - Generalized Error Distribution (Nelson, 1991).

f(z; nu) = nu / (lambda * 2^{1+1/nu} * Gamma(1/nu)) * exp(-0.5 * |z/lambda|^nu)

lambda = sqrt(2^{-2/nu} * Gamma(1/nu) / Gamma(3/nu))

Special cases: nu=2 (Normal), nu=1 (Laplace).
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from scipy.special import gammainc, gammaincinv, gammaln

from archbox.distributions.base import Distribution


class GeneralizedError(Distribution):
    """Generalized Error Distribution for GARCH models.

    Parameters
    ----------
    nu : float, optional
        Shape parameter. Must be > 0. If None, estimated from data.
        nu=2 is Normal, nu=1 is Laplace.
    """

    name = "GED"

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
        """Extract nu from dist_params or fixed value."""
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and len(dist_params) > 0:
            nu = float(dist_params[0])
        else:
            nu = 1.5
        return max(nu, 0.1)

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

    def ppf(self, q: float) -> float:
        """Percent point function for standardized GED.

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
        lam = self._lambda_ged(nu)

        if q < 0.5:
            # Use symmetry: ppf(q) = -ppf(1-q)
            p = 1.0 - 2.0 * q
            # P(|Z| <= x) = gammainc(1/nu, 0.5*(x/lam)^nu)
            # We need P(Z <= x) = q, so P(Z > -x) = q => P(|Z| <= x) = 1 - 2q
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return -x
        elif q > 0.5:
            p = 2.0 * q - 1.0
            val = float(gammaincinv(1.0 / nu, p))
            x = lam * (2.0 * val) ** (1.0 / nu)
            return float(x)
        else:
            return 0.0

    def cdf(self, x: float) -> float:
        """CDF for standardized GED.

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
        lam = self._lambda_ged(nu)

        # CDF using incomplete gamma
        u = 0.5 * np.abs(x / lam) ** nu
        g = float(gammainc(1.0 / nu, u))

        if x >= 0:
            return 0.5 * (1.0 + g)
        else:
            return 0.5 * (1.0 - g)

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
        """Transform: nu = exp(x) ensures nu > 0."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        constrained[0] = np.exp(unconstrained[0])
        return constrained

    def untransform_params(self, constrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Inverse transform: x = log(nu)."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        unconstrained[0] = np.log(max(constrained[0], 1e-6))
        return unconstrained

    def bounds(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        if self._fixed_nu is not None:
            return []
        return [(0.1, 20.0)]
