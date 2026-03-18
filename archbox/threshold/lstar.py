"""LSTAR - Logistic Smooth Transition Autoregressive Model (Terasvirta, 1994).

The LSTAR model uses a logistic transition function for smooth regime switching:

    y_t = phi^{(1)}'x_t * (1 - G(s_t; gamma, c))
        + phi^{(2)}'x_t * G(s_t; gamma, c)
        + eps_t

    G(s_t; gamma, c) = 1 / (1 + exp(-gamma * (s_t - c)))

Properties:
- gamma -> 0: linear model (G -> 0.5)
- gamma -> inf: LSTAR -> SETAR (abrupt transition)
- G(c; gamma, c) = 0.5 (midpoint of transition)

References
----------
- Terasvirta, T. (1994). Specification, Estimation, and Evaluation of
  Smooth Transition Autoregressive Models. JASA, 89(425), 208-218.
- van Dijk, D., Terasvirta, T. & Franses, P.H. (2002). Smooth Transition
  Autoregressive Models - A Survey. Econometric Reviews, 21(1), 1-47.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy import optimize

from archbox.threshold.base import ThresholdModel
from archbox.threshold.results import ThresholdResults
from archbox.threshold.transition import logistic_transition


class LSTAR(ThresholdModel):
    """Logistic Smooth Transition Autoregressive model (Terasvirta, 1994).

    Parameters
    ----------
    endog : array-like
        Endogenous time series.
    order : int
        AR order p (default 1).
    delay : int
        Delay parameter d (default 1).
    gamma_grid : int
        Number of gamma values in grid search (default 50).
    c_grid : int
        Number of c values in grid search (default 50).
    refine : bool
        Whether to refine via NLS after grid search (default True).

    Examples
    --------
    >>> import numpy as np
    >>> from archbox.threshold.lstar import LSTAR
    >>> rng = np.random.default_rng(42)
    >>> n = 1000
    >>> y = np.zeros(n)
    >>> gamma_true, c_true = 5.0, 0.0
    >>> for t in range(1, n):
    ...     s = y[t-1]
    ...     G = 1 / (1 + np.exp(-gamma_true * (s - c_true)))
    ...     y[t] = (0.5 + 0.3 * y[t-1]) * (1 - G) + (-0.2 + 0.8 * y[t-1]) * G
    ...     y[t] += rng.standard_normal() * 0.5
    >>> model = LSTAR(y, order=1, delay=1)
    >>> results = model.fit()
    >>> results.plot_transition()  # doctest: +SKIP
    """

    model_name: str = "LSTAR"

    def __init__(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        """Initialize LSTAR model with grid search configuration."""
        super().__init__(endog, order=order, delay=delay, n_regimes=2)
        self.gamma_grid = gamma_grid
        self.c_grid = c_grid
        self.refine = refine

    def _transition_function(
        self, s: NDArray[np.float64], params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Logistic transition: G(s; gamma, c) = 1/(1+exp(-gamma*(s-c))).

        Parameters
        ----------
        s : ndarray
            Transition variable values.
        params : ndarray
            Array with [gamma, c].

        Returns
        -------
        ndarray
            Transition values in [0, 1].
        """
        gamma, c = params[0], params[1]
        return logistic_transition(s, gamma, c)

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameters: [gamma=1, c=median(s)]."""
        return np.array([1.0, np.median(self._s)])

    @property
    def param_names(self) -> list[str]:
        """Parameter names."""
        names = ["gamma", "c"]
        for regime in range(1, 3):
            names.append(f"phi_0_regime{regime}")
            for lag in range(1, self.order + 1):
                names.append(f"phi_{lag}_regime{regime}")
        return names

    def _concentrated_ols(
        self,
        gamma: float,
        c: float,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        """OLS concentrated on (gamma, c).

        For given gamma and c, compute G(s; gamma, c), then solve:
        y = x1 * phi^{(1)} + x2 * phi^{(2)} + error

        where x1 = x_mat * (1 - G), x2 = x_mat * G.

        Parameters
        ----------
        gamma : float
            Speed of transition.
        c : float
            Location of transition.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        beta : ndarray
            Concatenated [phi^{(1)}, phi^{(2)}].
        resid : ndarray
            Residuals.
        rss : float
            Residual sum of squares.
        """
        g = logistic_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def _grid_search(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def _nls_objective(
        self,
        transition_params: NDArray[np.float64],
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> float:
        """NLS objective: RSS as function of (gamma, c).

        Parameters
        ----------
        transition_params : ndarray
            [log_gamma, c] - log_gamma to ensure gamma > 0.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        float
            RSS.
        """
        log_gamma, c = transition_params
        gamma = np.exp(log_gamma)
        gamma = min(gamma, 500.0)  # cap gamma

        try:
            _, _, rss = self._concentrated_ols(gamma, c, y, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def _fit_cls(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )
