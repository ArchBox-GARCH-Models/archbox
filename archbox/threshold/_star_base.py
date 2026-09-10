"""Shared estimation machinery for smooth transition AR models (LSTAR, ESTAR).

Both models are estimated by concentrated non-linear least squares: for a
given pair (gamma, c) the AR coefficients of the two regimes follow from OLS,
so only the two transition parameters are searched over.

Following Terasvirta (1994), the smoothness parameter gamma is made scale-free
by expressing it in units of the (power of the) standard deviation of the
transition variable: the grid and the upper bound are divided by
``std(s) ** scale_power`` (power 1 for the logistic transition, 2 for the
exponential one, matching the power of (s - c) in the exponent). Estimates are
therefore invariant to rescaling of the data, and no fixed numeric cap on
gamma is needed.

References
----------
- Terasvirta, T. (1994). Specification, Estimation, and Evaluation of
  Smooth Transition Autoregressive Models. JASA, 89(425), 208-218.
"""

from __future__ import annotations

import warnings
from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy import optimize

from archbox.threshold.base import ThresholdModel, count_params
from archbox.threshold.results import ThresholdResults
from archbox.threshold.tests_linearity import linearity_test_from_parts


class SmoothTransitionModel(ThresholdModel):
    """Base class for two-regime smooth transition autoregressive models.

    Subclasses provide :meth:`_transition` and the class attributes
    ``scale_power`` (power of std(s) used to scale gamma) and ``model_name``.
    """

    #: Largest smoothness allowed, in standardized units (gamma * std(s)^power).
    gamma_max_std: float = 500.0
    #: Power of std(s) used to scale gamma (1 for logistic, 2 for exponential).
    scale_power: int = 1

    def __init__(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        """Initialize the STAR model with grid search configuration."""
        super().__init__(endog, order=order, delay=delay, n_regimes=2)
        self.gamma_grid = gamma_grid
        self.c_grid = c_grid
        self.refine = refine

    # --- Subclass hook ---

    def _transition(self, s: NDArray[np.float64], gamma: float, c: float) -> NDArray[np.float64]:
        """Transition function G(s; gamma, c) (implemented by the subclass)."""
        raise NotImplementedError

    def _transition_function(
        self, s: NDArray[np.float64], params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Transition function with parameters packed as [gamma, c]."""
        return self._transition(s, float(params[0]), float(params[1]))

    # --- Scaling ---

    @property
    def gamma_scale(self) -> float:
        """``std(s) ** scale_power``: the scale gamma is expressed in."""
        sd = float(np.std(self._s))
        if not np.isfinite(sd) or sd <= 0.0:
            sd = 1.0
        return sd**self.scale_power

    @property
    def gamma_max(self) -> float:
        """Upper bound for gamma in the units of the data."""
        return self.gamma_max_std / self.gamma_scale

    @property
    def param_names(self) -> list[str]:
        """Parameter names."""
        names = ["gamma", "c"]
        for regime in range(1, 3):
            names.append(f"phi_0_regime{regime}")
            for lag in range(1, self.order + 1):
                names.append(f"phi_{lag}_regime{regime}")
        names.append("sigma2")
        return names

    # --- Estimation ---

    def _concentrated_ols(
        self,
        gamma: float,
        c: float,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        """OLS concentrated on (gamma, c).

        For given gamma and c, compute G(s; gamma, c), then solve
        y = x1 * phi^{(1)} + x2 * phi^{(2)} + error, where x1 = x_mat * (1 - G)
        and x2 = x_mat * G.

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
        g = self._transition(s, gamma, c)
        x_full = np.hstack([x_mat * (1.0 - g)[:, np.newaxis], x_mat * g[:, np.newaxis]])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0].astype(np.float64)
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def _gamma_values(self) -> NDArray[np.float64]:
        """Grid of gamma values, log-spaced in standardized units."""
        return np.logspace(-1.0, 2.0, self.gamma_grid) / self.gamma_scale

    def _c_values(self, s: NDArray[np.float64]) -> NDArray[np.float64]:
        """Grid of location values between the 15% and 85% quantiles of s."""
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo, hi = 0, n - 1
        return np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

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
        best_rss = np.inf
        best_gamma = 1.0 / self.gamma_scale
        best_c = float(np.median(s))

        for gamma in self._gamma_values():
            for c_val in self._c_values(s):
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                except np.linalg.LinAlgError:
                    continue
                if rss < best_rss:
                    best_rss = rss
                    best_gamma = float(gamma)
                    best_c = float(c_val)

        return best_gamma, best_c, float(best_rss)

    def _nls_objective(
        self,
        transition_params: NDArray[np.float64],
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> float:
        """NLS objective: RSS as a function of (log gamma, c).

        Parameters
        ----------
        transition_params : ndarray
            [log_gamma, c] - log_gamma keeps gamma > 0.
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
        gamma = min(float(np.exp(log_gamma)), self.gamma_max)

        try:
            _, _, rss = self._concentrated_ols(gamma, c, y, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def _fit_cls(self) -> ThresholdResults:
        """Fit the STAR model by concentrated non-linear least squares.

        Returns
        -------
        ThresholdResults
        """
        y, x_mat, s = self._y, self._X, self._s

        gamma_init, c_init, rss_init = self._grid_search(y, x_mat, s)
        best_gamma, best_c = gamma_init, c_init
        converged = True

        if self.refine:
            x0 = np.array([np.log(max(gamma_init, 1e-8)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            converged = bool(result.success)
            if not converged:
                warnings.warn(
                    f"{self.model_name}: Nelder-Mead refinement did not converge "
                    f"({result.message}); grid-search values are used when they fit "
                    "better.",
                    UserWarning,
                    stacklevel=3,
                )
            gamma_ref = min(float(np.exp(result.x[0])), self.gamma_max)
            c_ref = float(result.x[1])
            if float(result.fun) <= rss_init:
                best_gamma, best_c = gamma_ref, c_ref

        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = self._transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1, beta2 = beta[:k], beta[k:]

        t_eff = len(y)
        sigma2 = max(rss / t_eff, 1e-12)
        loglike = self.loglike([beta1, beta2], [sigma2, sigma2], g)

        # 2 * (p + 1) AR coefficients + gamma + c + one innovation variance
        n_params = count_params(2, self.order, n_transition=2, n_variances=1)
        aic = -2.0 * loglike + 2.0 * n_params
        bic = -2.0 * loglike + np.log(t_eff) * n_params

        # Variance by dominant regime (descriptive only; the likelihood above is
        # homoskedastic).
        mask_r1 = g < 0.5
        mask_r2 = ~mask_r1
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=float(best_c),
            delay=self.delay,
            transition_params={"gamma": float(best_gamma), "c": float(best_c)},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regimes=[beta1, beta2],
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=loglike,
            aic=float(aic),
            bic=float(bic),
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            linearity_test=linearity_test_from_parts(y, x_mat, s),
            converged=converged,
            param_names=self.param_names,
            _model=self,
        )
