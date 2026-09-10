"""Mixture Normal distribution (Haas, Mittnik & Paolella, 2004).

f(z) = p * N(0, sigma1^2) + (1-p) * N(0, sigma2^2)

Unit variance constraint: p * sigma1^2 + (1-p) * sigma2^2 = 1
=> sigma2^2 = (1 - p * sigma1^2) / (1 - p)
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy import stats

from archbox.distributions.base import Distribution, as_scalar_or_array


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

    #: Shape-parameter bounds. ``transform_params`` maps onto these open
    #: intervals and ``_get_p_sigma1`` clamps to them, so transform, clamp and
    #: ``bounds()`` agree and the optimum stays interior.
    P_MIN: float = 0.01
    P_MAX: float = 0.99
    SIGMA1_MIN: float = 0.01
    SIGMA1_MAX: float = 5.0

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
        """Extract p and sigma1 from ``dist_params`` or the fixed values.

        Estimated parameters are clamped to the declared ``bounds()`` (the
        intervals ``transform_params`` maps onto); parameters fixed by the user
        are only clamped to the validity domain (``0 < p < 1``, ``sigma1 > 0``).
        """
        idx = 0
        p_fixed = self._fixed_p is not None
        if self._fixed_p is not None:
            p = float(self._fixed_p)
        elif dist_params is not None and idx < len(dist_params):
            p = float(dist_params[idx])
            idx += 1
        else:
            p = 0.5

        sigma1_fixed = self._fixed_sigma1 is not None
        if self._fixed_sigma1 is not None:
            sigma1 = float(self._fixed_sigma1)
        elif dist_params is not None and idx < len(dist_params):
            sigma1 = float(dist_params[idx])
        else:
            sigma1 = 0.5

        if p_fixed:
            p = float(np.clip(p, 1e-6, 1.0 - 1e-6))
        else:
            p = float(np.clip(p, self.P_MIN, self.P_MAX))
        if sigma1_fixed:
            sigma1 = max(sigma1, 1e-6)
        else:
            sigma1 = float(np.clip(sigma1, self.SIGMA1_MIN, self.SIGMA1_MAX))
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

    def _ppf_scalar(self, q: float) -> float:
        """Invert the mixture CDF at a single probability.

        The bracket starts at the widest component scale and **expands
        geometrically** until it straddles the root, so quantiles deep in the
        tails (small ``q``) work for any admissible ``(p, sigma1)`` instead of
        failing on a hard-coded [-50, 50] window.

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

        if not 0.0 < q < 1.0:
            msg = f"q must be in (0, 1), got {q}."
            raise ValueError(msg)

        p, sigma1 = self._get_p_sigma1()
        sigma2_comp = self._compute_sigma2(p, sigma1)
        scale = max(sigma1, sigma2_comp, 1.0)

        def _cdf_minus_q(x: float) -> float:
            """Compute CDF(x) - q for root finding."""
            return float(self.cdf(x)) - q

        lo = -10.0 * scale
        hi = 10.0 * scale
        for _ in range(60):
            if _cdf_minus_q(lo) < 0.0 < _cdf_minus_q(hi):
                break
            lo *= 2.0
            hi *= 2.0
        else:  # pragma: no cover - only reachable for degenerate parameters
            msg = f"Could not bracket the mixture-normal quantile for q={q}."
            raise ValueError(msg)

        root: float = brentq(_cdf_minus_q, lo, hi)  # type: ignore[assignment]
        return float(root)

    def ppf(self, q: float | NDArray[np.float64]) -> Any:
        """Percent point function for Mixture Normal.

        Uses numerical inversion via Brent's method with an adaptive bracket.

        Parameters
        ----------
        q : float or ndarray
            Quantile(s) in (0, 1).

        Returns
        -------
        float or ndarray
            Value x such that P(Z <= x) = q.
        """
        q_arr = np.asarray(q, dtype=np.float64)
        values = np.array([self._ppf_scalar(float(v)) for v in q_arr.ravel()], dtype=np.float64)
        return as_scalar_or_array(values.reshape(q_arr.shape), q)

    def cdf(self, x: float | NDArray[np.float64]) -> Any:
        """CDF for Mixture Normal.

        Parameters
        ----------
        x : float or ndarray
            Value(s).

        Returns
        -------
        float or ndarray
            P(Z <= x).
        """
        p, sigma1 = self._get_p_sigma1()
        sigma2_comp = self._compute_sigma2(p, sigma1)

        x_arr = np.asarray(x, dtype=np.float64)
        values = p * np.asarray(stats.norm.cdf(x_arr, scale=sigma1), dtype=np.float64) + (
            1 - p
        ) * np.asarray(stats.norm.cdf(x_arr, scale=sigma2_comp), dtype=np.float64)
        return as_scalar_or_array(values, x)

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
            Random variates with mean 0 and unit variance.
        """
        p, sigma1 = self._get_p_sigma1(dist_params)
        sigma2_comp = self._compute_sigma2(p, sigma1)

        # One standard normal per draw, scaled by the selected component's
        # standard deviation: exactly the density used by `loglikelihood`
        # (symmetric, so the empirical CDF at 0 matches cdf(0) = 0.5).
        component = rng.uniform(size=n) < p
        scales = np.where(component, sigma1, sigma2_comp)
        return np.asarray(rng.standard_normal(n) * scales, dtype=np.float64)

    @staticmethod
    def _logistic(x: float, low: float, high: float) -> float:
        """Map the real line onto the open interval ``(low, high)``."""
        weight = 1.0 / (1.0 + np.exp(-np.clip(x, -50.0, 50.0)))
        return float(low + (high - low) * weight)

    @staticmethod
    def _logit(value: float, low: float, high: float) -> float:
        """Inverse of :meth:`_logistic`."""
        weight = (value - low) / (high - low)
        weight = float(np.clip(weight, 1e-8, 1.0 - 1e-8))
        return float(np.log(weight / (1.0 - weight)))

    def transform_params(self, unconstrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Map to ``p`` in ``(P_MIN, P_MAX)`` and ``sigma1`` in ``(SIGMA1_MIN, SIGMA1_MAX)``.

        Both land strictly inside the declared ``bounds()``, matching the
        clamps applied in ``_get_p_sigma1``.
        """
        if len(unconstrained) == 0:
            return unconstrained
        constrained = unconstrained.copy()
        idx = 0
        if self._fixed_p is None:
            constrained[idx] = self._logistic(float(unconstrained[idx]), self.P_MIN, self.P_MAX)
            idx += 1
        if self._fixed_sigma1 is None:
            constrained[idx] = self._logistic(
                float(unconstrained[idx]), self.SIGMA1_MIN, self.SIGMA1_MAX
            )
        return constrained

    def untransform_params(self, constrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Inverse of :meth:`transform_params`."""
        if len(constrained) == 0:
            return constrained
        unconstrained = constrained.copy()
        idx = 0
        if self._fixed_p is None:
            unconstrained[idx] = self._logit(float(constrained[idx]), self.P_MIN, self.P_MAX)
            idx += 1
        if self._fixed_sigma1 is None:
            unconstrained[idx] = self._logit(
                float(constrained[idx]), self.SIGMA1_MIN, self.SIGMA1_MAX
            )
        return unconstrained

    def bounds(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        bnds: list[tuple[float, float]] = []
        if self._fixed_p is None:
            bnds.append((self.P_MIN, self.P_MAX))
        if self._fixed_sigma1 is None:
            bnds.append((self.SIGMA1_MIN, self.SIGMA1_MAX))
        return bnds
