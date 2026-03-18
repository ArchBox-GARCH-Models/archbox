"""Mixture Normal distribution (Haas, Mittnik & Paolella, 2004).

f(z) = p * N(0, sigma1^2) + (1-p) * N(0, sigma2^2)

Unit variance constraint: p * sigma1^2 + (1-p) * sigma2^2 = 1
=> sigma2^2 = (1 - p * sigma1^2) / (1 - p)
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from scipy import stats

from archbox.distributions.base import Distribution


class MixtureNormal(Distribution):
    """Mixture of two Normal distributions for GARCH models.

    The unit variance constraint ensures:
    p * sigma1^2 + (1-p) * sigma2^2 = 1

    Parameters
    ----------
    p : float, optional
        Mixing probability. Must be in (0, 1).
    sigma1 : float, optional
        Standard deviation of first component. Must be > 0.
    """

    name = "Mixture Normal"

    def __init__(self, p: float | None = None, sigma1: float | None = None) -> None:
        """Initialize Mixture Normal distribution with optional parameters."""
        self._fixed_p = p
        self._fixed_sigma1 = sigma1

    @property
    def num_params(self) -> int:
        """Number of distribution shape parameters."""
        count = 0
        if self._fixed_p is None:
            count += 1
        if self._fixed_sigma1 is None:
            count += 1
        return count

    @property
    def param_names(self) -> list[str]:
        """Distribution parameter names."""
        names: list[str] = []
        if self._fixed_p is None:
            names.append("p")
        if self._fixed_sigma1 is None:
            names.append("sigma1")
        return names

    def start_params(self) -> NDArray[np.float64]:
        """Starting values for distribution parameters."""
        params: list[float] = []
        if self._fixed_p is None:
            params.append(0.5)
        if self._fixed_sigma1 is None:
            params.append(0.5)  # smaller than 1 for first component
        return np.array(params, dtype=np.float64) if params else np.array([], dtype=np.float64)

    def _get_p_sigma1(self, dist_params: NDArray[np.float64] | None = None) -> tuple[float, float]:
        """Extract p and sigma1 from dist_params or fixed values."""
        idx = 0
        if self._fixed_p is not None:
            p = self._fixed_p
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        if self._fixed_sigma1 is not None:
            sigma1 = self._fixed_sigma1
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        p = float(np.clip(p, 0.01, 0.99))
        sigma1 = max(sigma1, 0.01)
        return p, sigma1

    @staticmethod
    def _compute_sigma2(p: float, sigma1: float) -> float:
        """Compute sigma2 from unit variance constraint.

        sigma2^2 = (1 - p * sigma1^2) / (1 - p)

        Parameters
        ----------
        p : float
            Mixing probability.
        sigma1 : float
            Std dev of first component.

        Returns
        -------
        float
            sigma2 (std dev of second component).
        """
        numerator = 1.0 - p * sigma1**2
        denominator = 1.0 - p
        if numerator <= 0 or denominator <= 0:
            return 1.0  # fallback
        return float(np.sqrt(numerator / denominator))

    def loglikelihood(
        self,
        resids: NDArray[np.float64],
        sigma2: NDArray[np.float64],
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Compute per-observation log-likelihood under Mixture Normal.

        Parameters
        ----------
        resids : ndarray
            Residuals.
        sigma2 : ndarray
            Conditional variance.
        dist_params : ndarray, optional
            Distribution parameters [p, sigma1].

        Returns
        -------
        ndarray
            Log-likelihood per observation.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        z = resids / np.sqrt(sigma2)

        # Component 1: p * N(0, sigma1^2)
        comp1 = p * (1.0 / (np.sqrt(2 * np.pi) * sigma1)) * np.exp(-(z**2) / (2 * sigma1**2))
        # Component 2: (1-p) * N(0, sigma2^2)
        comp2 = (
            (1 - p)
            * (1.0 / (np.sqrt(2 * np.pi) * sigma2_comp))
            * np.exp(-(z**2) / (2 * sigma2_comp**2))
        )

        mixture_density = comp1 + comp2
        mixture_density = np.maximum(mixture_density, 1e-300)

        ll = -0.5 * np.log(sigma2) + np.log(mixture_density)
        return ll

    def ppf(self, q: float) -> float:
        """Percent point function for Mixture Normal.

        Uses numerical inversion via Brent's method.

        Parameters
        ----------
        q : float
            Quantile in (0, 1).

        Returns
        -------
        float
            Value x such that P(Z <= x) = q.
        """
        from scipy.optimize import brentq

        def _cdf_minus_q(x: float) -> float:
            """Compute CDF(x) - q for root finding."""
            return self.cdf(x) - q

        result: float = brentq(_cdf_minus_q, -50.0, 50.0)  # type: ignore[assignment]
        return result

    def cdf(self, x: float) -> float:
        """CDF for Mixture Normal.

        Parameters
        ----------
        x : float
            Value.

        Returns
        -------
        float
            P(Z <= x).
        """
        p, sigma1 = self._get_p_sigma1()
        sigma2_comp = self._compute_sigma2(p, sigma1)

        return float(
            p * stats.norm.cdf(x, scale=sigma1) + (1 - p) * stats.norm.cdf(x, scale=sigma2_comp)
        )

    def simulate(
        self,
        n: int,
        rng: np.random.Generator,
        dist_params: NDArray[np.float64] | None = None,
    ) -> NDArray[np.float64]:
        """Simulate from Mixture Normal distribution.

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
            Random variates with unit variance.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        # Select component
        component = rng.uniform(size=n) < p
        z = np.where(
            component,
            rng.normal(0, sigma1, size=n),
            rng.normal(0, sigma2_comp, size=n),
        )
        return z

    def transform_params(self, unconstrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Transform: p = sigmoid(x), sigma1 = exp(x)."""
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_p is None:
            constrained[idx] = 1.0 / (1.0 + np.exp(-unconstrained[idx]))
            idx += 1
        if self._fixed_sigma1 is None:
            constrained[idx] = np.exp(unconstrained[idx])
        return constrained

    def untransform_params(self, constrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Inverse transform distribution parameters."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_p is None:
            p = float(np.clip(constrained[idx], 1e-6, 1 - 1e-6))
            unconstrained[idx] = np.log(p / (1.0 - p))
            idx += 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = np.log(max(constrained[idx], 1e-6))
        return unconstrained

    def bounds(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        if self._fixed_p is None:
            bnds.append((0.01, 0.99))
        if self._fixed_sigma1 is None:
            bnds.append((0.01, 5.0))
        return bnds
