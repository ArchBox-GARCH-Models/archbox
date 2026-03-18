"""EWMA / RiskMetrics volatility model.

The Exponentially Weighted Moving Average model from JP Morgan's
RiskMetrics (1996). Equivalent to IGARCH(1,1) with omega=0.

Parameters:
    lambda = 0.94 (daily) or 0.97 (monthly)

References
----------
- JP Morgan (1996). RiskMetrics Technical Document. 4th ed.
- Francq, C. & Zakoian, J.-M. (2019). GARCH Models. 2nd ed. Wiley. Cap. 2.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from numpy.typing import NDArray


@dataclass
class EWMAResult:
    """Container for EWMA fit results.

    Attributes
    ----------
    conditional_volatility : NDArray[np.float64]
        Conditional volatility series sigma_t.
    conditional_variance : NDArray[np.float64]
        Conditional variance series sigma^2_t.
    returns : NDArray[np.float64]
        The input return series.
    lam : float
        The decay factor lambda.
    resids : NDArray[np.float64]
        Residuals (same as returns for zero-mean model).
    mu : float
        Mean (always 0 for EWMA).
    params : NDArray[np.float64]
        Parameters [omega=0, alpha=1-lambda, beta=lambda].
    p : int
        GARCH order (always 1).
    q : int
        ARCH order (always 1).
    """

    conditional_volatility: NDArray[np.float64]
    conditional_variance: NDArray[np.float64]
    returns: NDArray[np.float64]
    lam: float
    resids: NDArray[np.float64] = field(init=False)
    mu: float = 0.0
    params: NDArray[np.float64] = field(init=False)
    p: int = 1
    q: int = 1

    def __post_init__(self) -> None:
        """Compute derived attributes after dataclass initialization."""
        self.resids = self.returns.copy()
        self.params = np.array([0.0, 1.0 - self.lam, self.lam])


class EWMA:
    """EWMA / RiskMetrics volatility model.

    Parameters
    ----------
    returns : array-like
        Time series of returns (1D).
    lam : float
        Decay factor lambda. Default is 0.94 (daily).
        Use 0.97 for monthly data.

    Attributes
    ----------
    returns : NDArray[np.float64]
        Returns array.
    lam : float
        Decay factor.
    """

    def __init__(self, returns: object, lam: float = 0.94) -> None:
        """Initialize EWMA model with returns and decay factor."""
        self.returns = np.asarray(returns, dtype=np.float64).ravel()
        if not 0 < lam < 1:
            msg = f"lambda must be in (0, 1), got {lam}"
            raise ValueError(msg)
        self.lam = lam

    def fit(self) -> EWMAResult:
        """Compute EWMA volatility.

        Returns
        -------
        EWMAResult
            Result container with conditional_volatility and conditional_variance.

        Notes
        -----
        sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}

        Initial value: sigma^2_0 = sample variance of first 25 observations
        (or all observations if fewer than 25).
        """
        n_obs = len(self.returns)
        sigma2 = np.empty(n_obs)

        # Initial variance from first observations
        init_window = min(25, n_obs)
        sigma2[0] = np.var(self.returns[:init_window])
        if sigma2[0] < 1e-12:
            sigma2[0] = 1e-6

        for t in range(1, n_obs):
            sigma2[t] = self.lam * sigma2[t - 1] + (1 - self.lam) * self.returns[t - 1] ** 2

        sigma = np.sqrt(np.maximum(sigma2, 1e-12))

        return EWMAResult(
            conditional_volatility=sigma,
            conditional_variance=sigma2,
            returns=self.returns,
            lam=self.lam,
        )

    def covariance(self, returns_matrix: object) -> NDArray[np.float64]:
        """Compute multivariate EWMA covariance matrices.

        Parameters
        ----------
        returns_matrix : array-like
            Matrix of returns, shape (T, k) where k is the number of assets.

        Returns
        -------
        NDArray[np.float64]
            Array of covariance matrices, shape (T, k, k).

        Notes
        -----
        H_t = lambda * H_{t-1} + (1 - lambda) * r_{t-1} * r'_{t-1}

        The initial covariance H_0 is the sample covariance of the first
        25 observations.
        """
        ret = np.asarray(returns_matrix, dtype=np.float64)
        if ret.ndim != 2:
            msg = f"returns_matrix must be 2D, got {ret.ndim}D"
            raise ValueError(msg)

        n_obs, k = ret.shape
        h_cov = np.empty((n_obs, k, k))

        # Initial covariance from first observations
        init_window = min(25, n_obs)
        h_cov[0] = np.cov(ret[:init_window].T)
        if np.any(np.isnan(h_cov[0])):
            h_cov[0] = np.eye(k) * np.var(ret[:init_window])

        for t in range(1, n_obs):
            r_prev = ret[t - 1 : t].T  # (k, 1)
            outer = r_prev @ r_prev.T  # (k, k)
            h_cov[t] = self.lam * h_cov[t - 1] + (1 - self.lam) * outer

        return h_cov
