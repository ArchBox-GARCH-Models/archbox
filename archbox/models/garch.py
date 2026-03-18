"""GARCH(p,q) volatility model - Bollerslev (1986)."""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray

from archbox.core.volatility_model import VolatilityModel
from archbox.utils.validation import validate_positive_integer


class GARCH(VolatilityModel):
    """GARCH(p,q) model.

    sigma^2_t = omega + sum_{i=1}^q alpha_i * eps^2_{t-i}
                      + sum_{j=1}^p beta_j * sigma^2_{t-j}

    Parameters
    ----------
    endog : array-like
        Time series of returns.
    p : int
        Number of GARCH (lagged variance) terms. Default 1.
    q : int
        Number of ARCH (lagged squared residual) terms. Default 1.
    mean : str
        Mean model: 'constant' or 'zero'.
    dist : str
        Conditional distribution: 'normal'.

    Examples
    --------
    >>> from archbox import GARCH
    >>> from archbox.datasets import load_dataset
    >>> sp500 = load_dataset('sp500')
    >>> model = GARCH(sp500['returns'], p=1, q=1)
    >>> results = model.fit()
    >>> print(results.summary())
    """

    volatility_process: str = "GARCH"

    def __init__(
        self,
        endog: Any,
        p: int = 1,
        q: int = 1,
        mean: str = "constant",
        dist: str = "normal",
    ) -> None:
        """Initialize GARCH model with lag orders and options."""
        self.p = validate_positive_integer(p, "p")
        self.q = validate_positive_integer(q, "q")
        super().__init__(endog, mean=mean, dist=dist)

    def _variance_recursion(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute conditional variance series using numba-accelerated recursion.

        Parameters
        ----------
        params : ndarray
            [omega, alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        resids : ndarray
            Residuals eps_t.
        backcast : float
            Initial variance value.

        Returns
        -------
        ndarray
            Conditional variance sigma^2_t.
        """
        from archbox.utils.backend import get_garch_recursion

        omega = params[0]
        alphas = params[1 : 1 + self.q]
        betas = params[1 + self.q : 1 + self.q + self.p]

        T = len(resids)
        sigma2 = np.empty(T)

        recursion_fn = get_garch_recursion()
        return recursion_fn(resids, sigma2, omega, alphas, betas, self.p, self.q, backcast)

    def _one_step_variance(
        self, eps: float, sigma2_prev: float, params: NDArray[np.float64]
    ) -> float:
        """Compute one-step variance for news impact curve."""
        omega = params[0]
        alpha = params[1]
        beta = params[1 + self.q]
        sigma2 = omega + alpha * eps**2 + beta * sigma2_prev
        return float(max(sigma2, 1e-12))

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameters via variance targeting.

        Sets alpha=0.08, beta=0.88, and derives omega from
        the sample variance.
        """
        target_var = float(np.var(self.endog))
        alpha_init = 0.08
        beta_init = 0.88
        omega_init = target_var * (1 - alpha_init * self.q - beta_init * self.p)
        omega_init = max(omega_init, 1e-10)
        return np.array([omega_init] + [alpha_init] * self.q + [beta_init] * self.p)

    @property
    def param_names(self) -> list[str]:
        """Parameter names: omega, alpha[1], ..., beta[1], ..."""
        names = ["omega"]
        names.extend(f"alpha[{i + 1}]" for i in range(self.q))
        names.extend(f"beta[{j + 1}]" for j in range(self.p))
        return names

    def transform_params(self, unconstrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Transform unconstrained -> constrained parameters.

        - omega: exp(x) to ensure > 0 (clamped to avoid overflow)
        - alpha, beta: sigmoid to ensure >= 0, scaled so sum < 1
        """
        constrained = np.empty_like(unconstrained)
        constrained[0] = np.exp(np.clip(unconstrained[0], -50.0, 50.0))

        # alpha and beta: individual sigmoid then scale so sum < 0.9999
        raw = 1.0 / (1.0 + np.exp(-unconstrained[1:]))  # each in (0, 1)
        total = np.sum(raw)
        if total >= 0.9999:
            raw = raw * (0.9999 / total)
        constrained[1:] = raw

        return constrained

    def untransform_params(self, constrained: NDArray[np.float64]) -> NDArray[np.float64]:
        """Transform constrained -> unconstrained parameters."""
        unconstrained = np.empty_like(constrained)
        unconstrained[0] = np.log(constrained[0])  # log(omega)
        # inverse sigmoid: log(p / (1 - p))
        ab = np.clip(constrained[1:], 1e-8, 1.0 - 1e-8)
        unconstrained[1:] = np.log(ab / (1.0 - ab))
        return unconstrained

    def bounds(self) -> list[tuple[float, float]]:
        """Parameter bounds."""
        b: list[tuple[float, float]] = [(1e-12, 10.0)]  # omega
        b.extend((0.0, 1.0) for _ in range(self.q))  # alphas
        b.extend((0.0, 1.0) for _ in range(self.p))  # betas
        return b

    @property
    def num_params(self) -> int:
        """Number of parameters: 1 + q + p."""
        return 1 + self.q + self.p

    def __repr__(self) -> str:
        """Return string representation of the GARCH model."""
        return f"GARCH(p={self.p}, q={self.q}, nobs={self.nobs})"
