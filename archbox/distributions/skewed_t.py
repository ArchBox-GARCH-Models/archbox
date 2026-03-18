"""Skewed Student-t distribution (Hansen, 1994).

f(z; nu, lambda) = {
    b*c*(1 + 1/(nu-2) * ((b*z+a)/(1-lambda))^2)^{-(nu+1)/2}  if z < -a/b
    b*c*(1 + 1/(nu-2) * ((b*z+a)/(1+lambda))^2)^{-(nu+1)/2}  if z >= -a/b
}

where:
    a = 4*lambda*c*(nu-2)/(nu-1)
    b^2 = 1 + 3*lambda^2 - a^2
    c = Gamma((nu+1)/2) / (sqrt(pi*(nu-2)) * Gamma(nu/2))
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from scipy.special import gammaln

from archbox.distributions.base import Distribution


class SkewedT(Distribution):
    """Skewed Student-t distribution for GARCH models.

    Parameters
    ----------
    nu : float, optional
        Degrees of freedom. Must be > 2.
    lam : float, optional
        Skewness parameter. Must be in (-1, 1).
    """

    name = "Skewed Student-t"

    def __init__(self, nu: float | None = None, lam: float | None = None) -> None:
        """Initialize Skewed Student-t distribution with optional parameters."""
        self._fixed_nu = nu
        self._fixed_lam = lam

    @property
    def num_params(self) -> int:
        """Number of distribution shape parameters."""
        count = 0
        if self._fixed_nu is None:
            count += 1
        if self._fixed_lam is None:
            count += 1
        return count

    @property
    def param_names(self) -> list[str]:
        """Distribution parameter names."""
        names: list[str] = []
        if self._fixed_nu is None:
            names.append("nu")
        if self._fixed_lam is None:
            names.append("lambda")
        return names

    def start_params(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = []
        if self._fixed_nu is None:
            params.append(8.0)
        if self._fixed_lam is None:
            params.append(-0.1)
        return np.array(params, dtype=np.float64) if params else np.array([], dtype=np.float64)

    def _get_nu_lam(self, dist_params: NDArray[np.float64] | None = None) -> tuple[float, float]:
        """Extract nu and lambda from dist_params or fixed values."""
        idx = 0
        if self._fixed_nu is not None:
            nu = self._fixed_nu
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = self._fixed_lam
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, 2.01)
        lam = float(np.clip(lam, -0.999, 0.999))
        return nu, lam

    @staticmethod
    def _compute_abc(nu: float, lam: float) -> tuple[float, float, float]:
        """Compute Hansen's a, b, c constants.

        Parameters
        ----------
        nu : float
            Degrees of freedom.
        lam : float
            Skewness parameter.

        Returns
        -------
        tuple[float, float, float]
            (a, b, c) constants.
        """
        c = float(np.exp(gammaln((nu + 1) / 2) - gammaln(nu / 2) - 0.5 * np.log(np.pi * (nu - 2))))
        a = 4 * lam * c * (nu - 2) / (nu - 1)
        b2 = 1 + 3 * lam**2 - a**2
        b = float(np.sqrt(max(b2, 1e-12)))
        return a, b, c

    def loglikelihood(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Skewed Student-t.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only non-fixed params).

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        z = resids / np.sqrt(sigma2)
        threshold = -a / b

        log_bc = np.log(b) + np.log(c)

        # Vectorized computation
        left_mask = z < threshold
        eta = np.where(left_mask, (b * z + a) / (1 - lam), (b * z + a) / (1 + lam))

        ll = log_bc - 0.5 * np.log(sigma2) - ((nu + 1) / 2) * np.log(1 + eta**2 / (nu - 2))
        return ll

    def ppf(self, q: float) -> float:
        """Percent point function for Skewed Student-t.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Approximate quantile value.
        """
        from scipy.optimize import brentq

        def _cdf_minus_q(x: float) -> float:
            """Compute CDF(x) - q for root finding."""
            return self.cdf(x) - q

        result: float = brentq(_cdf_minus_q, -50.0, 50.0)  # type: ignore[assignment]
        return result

    def cdf(self, x: float) -> float:
        """CDF for Skewed Student-t.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        from scipy import stats as sp_stats

        nu, lam = self._get_nu_lam()
        a, b, c = self._compute_abc(nu, lam)
        threshold = -a / b

        if x < threshold:
            eta = (b * x + a) / (1 - lam)
            # Scale to standard t
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 - lam) * p)
        else:
            eta = (b * x + a) / (1 + lam)
            p = sp_stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu)
            return float((1 + lam) * p - lam)

    def simulate(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from standardized Skewed Student-t.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters.

        Returns
        -------
        ndarray
            Standardized random variates.
        """
        nu, lam = self._get_nu_lam(dist_params)
        a, b, c = self._compute_abc(nu, lam)

        # Standardized t draws
        t_samples = rng.standard_t(nu, size=n) / np.sqrt(nu / (nu - 2))

        # Apply skewness
        u = rng.uniform(size=n)
        threshold = (1 - lam) / 2

        z = np.where(
            u < threshold,
            ((1 - lam) / b) * t_samples - a / b,
            ((1 + lam) / b) * t_samples - a / b,
        )
        return z

    def transform_params(self, unconstrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Transform: nu = 2 + exp(x), lambda = tanh(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_nu is None:
            constrained[idx] = 2.0 + np.exp(unconstrained[idx])
            idx += 1
        if self._fixed_lam is None:
            constrained[idx] = np.tanh(unconstrained[idx])
        return constrained

    def untransform_params(self, constrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_nu is None:
            unconstrained[idx] = np.log(max(constrained[idx] - 2.0, 1e-6))
            idx += 1
        if self._fixed_lam is None:
            unconstrained[idx] = np.arctanh(np.clip(constrained[idx], -0.999, 0.999))
        return unconstrained

    def bounds(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        if self._fixed_nu is None:
            bnds.append((2.01, 100.0))
        if self._fixed_lam is None:
            bnds.append((-0.999, 0.999))
        return bnds
