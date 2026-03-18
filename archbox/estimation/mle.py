"""Maximum Likelihood Estimation for volatility models."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from scipy import optimize

from archbox._logging import get_logger
from archbox.core.results import ArchResults

if TYPE_CHECKING:
    from archbox.core.volatility_model import VolatilityModel

logger = get_logger("estimation.mle")


class MLEstimator:
    """Maximum Likelihood Estimator for ARCH/GARCH models.

    Minimizes the negative log-likelihood using scipy.optimize.minimize,
    then computes standard errors via numerical Hessian.
    """

    def fit(
        self,
        model: VolatilityModel,
        starting_values: NDArray[np.float64] | None = None,
        variance_targeting: bool = False,
        optimizer: str = "SLSQP",
        maxiter: int = 500,
        disp: bool = True,
    ) -> ArchResults:
        """Fit the model via MLE.

        Parameters
        ----------
        model : VolatilityModel
            Model to fit.
        starting_values : ndarray, optional
            Starting parameter values (in constrained space).
            If None, uses model.start_params.
        variance_targeting : bool
            Fix omega via variance targeting.
        optimizer : str
            Scipy optimizer: 'SLSQP', 'L-BFGS-B'.
        maxiter : int
            Maximum iterations.
        disp : bool
            Display optimization info.

        Returns
        -------
        ArchResults
            Fitted results container.
        """
        backcast = model._backcast(model.endog)

        if starting_values is not None:
            x0_constrained = starting_values.copy()
        else:
            x0_constrained = model.start_params.copy()

        if variance_targeting:
            return self._fit_with_targeting(
                model,
                x0_constrained,
                backcast,
                optimizer,
                maxiter,
                disp,
            )
        return self._fit_standard(
            model,
            x0_constrained,
            backcast,
            optimizer,
            maxiter,
            disp,
        )

    def _fit_standard(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """Standard MLE fit (all parameters free)."""
        x0 = model.untransform_params(x0_constrained)

        def neg_loglike(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for optimization."""
            constrained = model.transform_params(unconstrained)
            ll = model.loglike(constrained, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        params_opt = model.transform_params(result.x)
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def _fit_with_targeting(
        self,
        model: VolatilityModel,
        x0_constrained: NDArray[np.float64],
        backcast: float,
        optimizer: str,
        maxiter: int,
        disp: bool,
    ) -> ArchResults:
        """MLE fit with variance targeting (omega fixed)."""
        sample_var = float(np.var(model.endog))

        # x0 without omega: [alpha_1, ..., alpha_q, beta_1, ..., beta_p]
        x0_free = x0_constrained[1:]
        x0_free_unc = np.log(x0_free)  # simple positive transform

        def neg_loglike_targeted(unconstrained_free: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            free_params = np.exp(unconstrained_free)
            persistence = np.sum(free_params)
            if persistence >= 0.9999:
                return 1e10
            omega = sample_var * (1.0 - persistence)
            if omega <= 0:
                return 1e10
            full_params = np.concatenate([[omega], free_params])
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_free_unc,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            logger.warning("Optimization did not converge: %s", result.message)

        free_params = np.exp(result.x)
        persistence = np.sum(free_params)
        omega = sample_var * (1.0 - persistence)
        params_opt = np.concatenate([[omega], free_params])
        loglike_val = -result.fun

        sigma2 = model._variance_recursion(params_opt, model.endog, backcast)
        sigma2 = np.maximum(sigma2, 1e-12)

        se_robust, se_nonrobust = self._compute_standard_errors(
            model,
            params_opt,
            backcast,
        )

        return ArchResults(
            model=model,
            params=params_opt,
            loglike=loglike_val,
            sigma2=sigma2,
            se_robust=se_robust,
            se_nonrobust=se_nonrobust,
            convergence=result.success,
        )

    def _compute_standard_errors(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute robust and non-robust standard errors.

        Parameters
        ----------
        model : VolatilityModel
            Fitted model.
        params : ndarray
            Estimated parameters (constrained).
        backcast : float
            Backcast value.

        Returns
        -------
        tuple[ndarray, ndarray]
            (se_robust, se_nonrobust).
        """
        k = len(params)

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)

            # Non-robust SE
            se_nonrobust = np.sqrt(np.abs(np.diag(h_inv)))

            # Robust SE (sandwich)
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
            se_robust = np.sqrt(np.abs(np.diag(sandwich)))

        except (np.linalg.LinAlgError, ValueError):
            logger.warning("Failed to compute standard errors, using fallback")
            se_robust = np.full(k, np.nan)
            se_nonrobust = np.full(k, np.nan)

        # Ensure positive
        se_robust = np.maximum(se_robust, 1e-20)
        se_nonrobust = np.maximum(se_nonrobust, 1e-20)

        return se_robust, se_nonrobust

    def _compute_hessian(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order finite differences.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            Hessian matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = eps * max(abs(params[i]), 1e-8)
                ej[j] = eps * max(abs(params[j]), 1e-8)

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * ei[i] * ej[j])
                hessian[j, i] = hessian[i, j]

        return hessian

    def _compute_opg(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute Outer Product of Gradients matrix.

        OPG = sum(g_t * g_t') where g_t is the gradient of ll_t.

        Parameters
        ----------
        model : VolatilityModel
            Model instance.
        params : ndarray
            Parameter values.
        backcast : float
            Backcast value.

        Returns
        -------
        ndarray
            OPG matrix, shape (k, k).
        """
        k = len(params)
        eps = 1e-5

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            ej = np.zeros(k)
            ej[j] = eps * max(abs(params[j]), 1e-8)

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * ej[j])

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients
