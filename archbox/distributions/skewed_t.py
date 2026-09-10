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

from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy import stats
from scipy.special import gammaln

from archbox.distributions.base import Distribution, as_scalar_or_array


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

    #: Shape-parameter bounds. ``transform_params`` maps onto these open
    #: intervals and ``_get_nu_lam`` clamps to them, so transform, clamp and
    #: ``bounds()`` agree and the optimum stays interior.
    NU_MIN: float = 2.01
    NU_MAX: float = 100.0
    LAM_MAX: float = 0.999

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
        """Extract nu and lambda from ``dist_params`` or the fixed values.

        Estimated parameters are clamped to the declared ``bounds()`` (the
        intervals ``transform_params`` maps onto); parameters fixed by the user
        are only clamped to the validity domain (``nu > 2``, ``|lambda| < 1``).
        """
        idx = 0
        nu_fixed = self._fixed_nu is not None
        if self._fixed_nu is not None:
            nu = float(self._fixed_nu)
        elif dist_params is not None and idx < len(dist_params):
            nu = float(dist_params[idx])
            idx += 1
        else:
            nu = 8.0

        if self._fixed_lam is not None:
            lam = float(self._fixed_lam)
        elif dist_params is not None and idx < len(dist_params):
            lam = float(dist_params[idx])
        else:
            lam = 0.0

        nu = max(nu, self.NU_MIN) if nu_fixed else float(np.clip(nu, self.NU_MIN, self.NU_MAX))
        lam = float(np.clip(lam, -self.LAM_MAX, self.LAM_MAX))
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

    @classmethod
    def _quantile(
        cls,
        u: NDArray[np.float64],
        nu: float,
        lam: float,
    ) -> NDArray[np.float64]:
        """Inverse CDF of Hansen's skew-t, evaluated elementwise.

        Inverting the two branches of :meth:`cdf` gives, with
        ``s = sqrt((nu-2)/nu) T^-1_nu(.)``,

        ``z = ((1 - lam) s - a) / b``  for ``u < (1 - lam)/2``  (argument ``u/(1-lam)``)
        ``z = ((1 + lam) s - a) / b``  otherwise                (argument ``(u+lam)/(1+lam)``)

        Both branches meet at ``z = -a/b``, so the map is continuous and
        strictly increasing.

        Parameters
        ----------
        u : ndarray
            Probabilities in (0, 1).
        nu : float
            Degrees of freedom.
        lam : float
            Skewness parameter.

        Returns
        -------
        ndarray
            Quantiles of the standardized (mean 0, variance 1) skew-t.
        """
        a, b, _ = cls._compute_abc(nu, lam)
        u_arr = np.clip(np.asarray(u, dtype=np.float64), 1e-14, 1.0 - 1e-14)
        left = u_arr < (1.0 - lam) / 2.0
        inner = np.where(left, u_arr / (1.0 - lam), (u_arr + lam) / (1.0 + lam))
        inner = np.clip(inner, 1e-14, 1.0 - 1e-14)
        scale = np.sqrt((nu - 2.0) / nu)
        t_quantile = np.asarray(stats.t.ppf(inner, df=nu), dtype=np.float64) * scale
        weight = np.where(left, 1.0 - lam, 1.0 + lam)
        return (weight * t_quantile - a) / b

    def ppf(self, q: float | NDArray[np.float64]) -> Any:
        """Percent point function for the standardized Skewed Student-t.

        Closed form (no root finding), so it stays accurate deep in the tails
        and for small ``nu``.

        Parameters
        ----------
        q : float or ndarray
            Quantile(s) in (0, 1).

        Returns
        -------
        float or ndarray
            Value x such that P(Z <= x) = q.
        """
        nu, lam = self._get_nu_lam()
        return as_scalar_or_array(self._quantile(np.asarray(q, dtype=np.float64), nu, lam), q)

    def cdf(self, x: float | NDArray[np.float64]) -> Any:
        """CDF for the standardized Skewed Student-t.

        Parameters
        ----------
        x : float or ndarray
            Value(s).

        Returns
        -------
        float or ndarray
            P(Z <= x).
        """
        nu, lam = self._get_nu_lam()
        a, b, _ = self._compute_abc(nu, lam)
        threshold = -a / b

        x_arr = np.asarray(x, dtype=np.float64)
        left = x_arr < threshold
        weight = np.where(left, 1.0 - lam, 1.0 + lam)
        eta = (b * x_arr + a) / weight
        p = np.asarray(stats.t.cdf(eta * np.sqrt(nu / (nu - 2)), df=nu), dtype=np.float64)
        values = np.where(left, (1.0 - lam) * p, (1.0 + lam) * p - lam)
        return as_scalar_or_array(values, x)

    def simulate(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from the standardized Skewed Student-t (Hansen, 1994).

        Draws are produced by inverse-CDF sampling with :meth:`_quantile`, so
        the sample follows exactly the density used by ``loglikelihood``: mean
        0, variance 1, and ``P(Z <= 0)`` equal to ``cdf(0)``.

        Parameters
        ----------
        n : int
            Number of observations.
        rng : Generator
            Random number generator.
        dist_params : ndarray, optional
            Distribution parameters [nu, lambda] (only the non-fixed ones).

        Returns
        -------
        ndarray
            Standardized random variates, shape (n,).
        """
        nu, lam = self._get_nu_lam(dist_params)
        u = rng.uniform(size=n)
        return self._quantile(u, nu, lam)

    def transform_params(self, unconstrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Transform to ``nu`` in ``(NU_MIN, NU_MAX)`` and ``lambda`` in ``(-LAM_MAX, LAM_MAX)``.

        Both maps land strictly inside the declared ``bounds()``, matching the
        clamps applied in ``_get_nu_lam``.
        """
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_nu is None:
            span = self.NU_MAX - self.NU_MIN
            weight = 1.0 / (1.0 + np.exp(-np.clip(unconstrained[idx], -50.0, 50.0)))
            constrained[idx] = self.NU_MIN + span * weight
            idx += 1
        if self._fixed_lam is None:
            constrained[idx] = self.LAM_MAX * np.tanh(unconstrained[idx])
        return constrained

    def untransform_params(self, constrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Inverse of :meth:`transform_params`."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_nu is None:
            span = self.NU_MAX - self.NU_MIN
            weight = (float(constrained[idx]) - self.NU_MIN) / span
            weight = float(np.clip(weight, 1e-8, 1.0 - 1e-8))
            unconstrained[idx] = np.log(weight / (1.0 - weight))
            idx += 1
        if self._fixed_lam is None:
            ratio = float(constrained[idx]) / self.LAM_MAX
            unconstrained[idx] = np.arctanh(np.clip(ratio, -1.0 + 1e-8, 1.0 - 1e-8))
        return unconstrained

    def bounds(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        if self._fixed_nu is None:
            bnds.append((self.NU_MIN, self.NU_MAX))
        if self._fixed_lam is None:
            bnds.append((-self.LAM_MAX, self.LAM_MAX))
        return bnds
