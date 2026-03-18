"""Markov-Switching GARCH model (Gray, 1996).

Implements GARCH with regime-switching parameters using the Gray (1996)
collapsing approach to handle path-dependence.

References
----------
Gray, S.F. (1996). Modeling the Conditional Distribution of Interest Rates
as a Regime-Switching Process. Journal of Financial Economics, 42(1), 27-62.

Haas, M., Mittnik, S. & Paolella, M.S. (2004). A New Approach to
Markov-Switching GARCH Models. Journal of Financial Econometrics, 2(4), 493-530.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray

from archbox.regime.base import MarkovSwitchingModel


class MarkovSwitchingGARCH(MarkovSwitchingModel):
    """Markov-Switching GARCH model (Gray, 1996).

    sigma^2_t(s) = omega_s + alpha_s * eps^2_{t-1} + beta_s * h_{t-1}
    h_{t-1} = sum_j P(S_{t-1}=j | Y_{t-1}) * sigma^2_{t-1}(j)

    Parameters
    ----------
    endog : array-like
        Time series of returns, shape (T,).
    k_regimes : int
        Number of regimes. Default is 2.
    p : int
        GARCH order (number of lagged variances). Default is 1.
    q : int
        ARCH order (number of lagged squared residuals). Default is 1.
    method : str
        Collapsing method: 'gray' (default) or 'haas'.

    Examples
    --------
    >>> import numpy as np
    >>> from archbox.regime.ms_garch import MarkovSwitchingGARCH
    >>> returns = np.random.randn(500) * 0.01
    >>> model = MarkovSwitchingGARCH(returns, k_regimes=2, p=1, q=1)
    >>> results = model.fit()
    >>> print(results.summary())
    """

    model_name: str = "MS-GARCH"

    def __init__(
        self,
        endog: Any,
        k_regimes: int = 2,
        p: int = 1,
        q: int = 1,
        method: str = "gray",
    ) -> None:
        """Initialize Markov-Switching GARCH model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=max(p, q),
            switching_mean=False,
            switching_variance=True,
            switching_ar=False,
        )
        self.p_garch = p
        self.q_arch = q
        self.method = method

        # Pre-computed conditional variances per regime, updated during EM
        self._sigma2: NDArray[np.float64] | None = None
        self._h_collapsed: NDArray[np.float64] | None = None
        self._filtered_probs_cache: NDArray[np.float64] | None = None

    def _regime_loglike(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def _unpack_garch_params(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        """Unpack GARCH parameters for a specific regime.

        Parameter layout:
        [omega_0, alpha_0, beta_0, omega_1, alpha_1, beta_1, ..., trans_params]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (omega, alpha, beta) for the regime.
        """
        base = regime * 3  # 3 GARCH params per regime
        omega = max(abs(float(params[base])), 1e-8)
        alpha = max(abs(float(params[base + 1])), 1e-8)
        beta = max(abs(float(params[base + 2])), 0.0)
        return omega, alpha, beta

    def update_collapsed_variance(
        self,
        filtered_probs: NDArray[np.float64],
    ) -> None:
        """Update the collapsed conditional variance h_{t-1}.

        h_{t-1} = sum_j P(S_{t-1}=j | Y_{t-1}) * sigma^2_{t-1}(j)

        Parameters
        ----------
        filtered_probs : ndarray
            Filtered probabilities, shape (T, k).
        """
        if self._sigma2 is None:
            return

        n_obs, k = filtered_probs.shape
        self._h_collapsed = np.zeros(n_obs)
        for t in range(n_obs):
            for s in range(k):
                self._h_collapsed[t] += filtered_probs[t, s] * self._sigma2[t, s]
            self._h_collapsed[t] = max(self._h_collapsed[t], 1e-12)

        self._filtered_probs_cache = filtered_probs.copy()

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values.

        Returns
        -------
        ndarray
            [omega_0, alpha_0, beta_0, ..., omega_{k-1}, alpha_{k-1}, beta_{k-1}, trans_params].
        """
        k = self.k_regimes
        y = self.endog
        var_y = float(np.var(y))
        params_list: list[float] = []

        for s in range(k):
            # Different initial GARCH params per regime
            scale = 0.5 + s * 1.0  # regime 0: low vol, regime 1: high vol
            omega = var_y * 0.05 * scale
            alpha = 0.05 + s * 0.05
            beta = 0.85 - s * 0.10
            params_list.extend([omega, alpha, beta])

        # Transition params
        n_trans = k * (k - 1)
        params_list.extend([0.0] * n_trans)

        return np.array(params_list)

    @property
    def param_names(self) -> list[str]:
        """Parameter names."""
        k = self.k_regimes
        names: list[str] = []
        for s in range(k):
            names.extend([f"omega_{s}", f"alpha_{s}", f"beta_{s}"])
        names.extend([f"p_{i}{j}" for i in range(k) for j in range(k) if i != j])
        return names

    def _m_step_update(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def _extract_regime_params(self, params: NDArray[np.float64]) -> dict[int, dict[str, float]]:
        """Extract regime-specific GARCH parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            omega, alpha, beta = self._unpack_garch_params(params, s)
            regime_params[s] = {
                "omega": omega,
                "alpha": alpha,
                "beta": beta,
                "persistence": alpha + beta,
            }
        return regime_params
