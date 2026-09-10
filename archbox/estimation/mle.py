"""Maximum Likelihood Estimation for volatility models.

Optimization strategy
---------------------
Models are optimized in their **unconstrained** parameterisation: the search
vector is mapped through ``model.full_transform_params`` (exp/logit/tanh maps
that already encode positivity and stationarity), so scipy always sees an
unbounded problem.  The bounds declared by ``model.bounds()`` /
``dist.bounds()`` are honoured on top of that by projecting every candidate
onto the declared box before the likelihood is evaluated, and again on the
returned estimates - so e.g. an APARCH ``delta`` can never leave ``(0.01, 10)``
and a Student-t ``nu`` can never leave ``(2.01, 100)``.  This is the coherent
alternative to handing ``bounds=`` to scipy, which would be meaningless in the
unconstrained space, and it is why no ``bounds`` argument appears below.
"""

from __future__ import annotations

import math
import warnings
from collections.abc import Callable
from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from scipy import optimize

from archbox._logging import get_logger
from archbox.core.exceptions import ConvergenceWarning, StandardErrorWarning
from archbox.core.results import ArchResults

if TYPE_CHECKING:
    from archbox.core.volatility_model import VolatilityModel

logger = get_logger("estimation.mle")

#: Largest persistence variance targeting will reconstruct omega from.
_MAX_TARGET_PERSISTENCE = 0.9999

#: Relative step for numerical derivatives, with a floor on the parameter scale
#: so that a parameter at (or near) zero still gets a usable perturbation.
_FD_EPS = 1e-5
_FD_MIN_SCALE = 1e-3

#: Weight of the quadratic penalty applied to a candidate that leaves the
#: declared bounds, and the cap on the (relative) violation that feeds it.
_BOUND_PENALTY = 1e4
_MAX_REL_VIOLATION = 1e6


def _fd_step(value: float) -> float:
    """Finite-difference step for a parameter with the given value.

    Uses ``eps * max(|theta|, 1e-3)`` so parameters sitting at zero (a GJR
    ``gamma``, an APARCH ``gamma``) get a step of 1e-8 instead of collapsing to
    the ``eps * 1e-8 = 1e-13`` of a pure relative rule, which is below the
    resolution of the log-likelihood and produces pure noise.

    Parameters
    ----------
    value : float
        Current parameter value.

    Returns
    -------
    float
        Step size, strictly positive.
    """
    return _FD_EPS * max(abs(float(value)), _FD_MIN_SCALE)


class MLEstimator:
    """Maximum Likelihood Estimator for ARCH/GARCH models.

    Minimizes the negative log-likelihood using scipy.optimize.minimize,
    then computes standard errors via numerical Hessian.
    """

    # --- Bounds handling ---

    @staticmethod
    def _bounds_box(
        bounds: list[tuple[float, float]], k: int
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Turn a declared bounds list into (lower, upper) arrays of length k.

        ``None`` entries (and a bounds list whose length does not match the
        parameter vector) are treated as unbounded.

        Parameters
        ----------
        bounds : list of tuple
            Declared bounds, ``[(lo, hi), ...]``.
        k : int
            Number of parameters.

        Returns
        -------
        tuple[ndarray, ndarray]
            Lower and upper bound arrays.
        """
        lower = np.full(k, -np.inf, dtype=np.float64)
        upper = np.full(k, np.inf, dtype=np.float64)
        if len(bounds) != k:
            logger.warning(
                "Model declared %d bounds for %d parameters; bounds are ignored.",
                len(bounds),
                k,
            )
            return lower, upper
        for i, (lo, hi) in enumerate(bounds):
            # `None` is accepted (and treated as unbounded) for models that
            # declare open-ended bounds the scipy way.
            if lo is not None and math.isfinite(lo):  # pyright: ignore[reportUnnecessaryComparison]
                lower[i] = float(lo)
            if hi is not None and math.isfinite(hi):  # pyright: ignore[reportUnnecessaryComparison]
                upper[i] = float(hi)
        return lower, upper

    def _project(
        self, params: NDArray[np.float64], bounds: list[tuple[float, float]]
    ) -> NDArray[np.float64]:
        """Clip a constrained parameter vector onto the declared bounds.

        Parameters
        ----------
        params : ndarray
            Constrained parameters.
        bounds : list of tuple
            Declared bounds.

        Returns
        -------
        ndarray
            Parameters guaranteed to satisfy ``bounds``.
        """
        arr = np.asarray(params, dtype=np.float64)
        lower, upper = self._bounds_box(bounds, len(arr))
        return np.clip(arr, lower, upper)

    @staticmethod
    def _bound_penalty(raw: NDArray[np.float64], projected: NDArray[np.float64]) -> float:
        """Quadratic penalty for the distance between a candidate and its projection.

        Clipping alone would make the objective flat outside the box, and a
        finite-difference optimizer can then simply stop on the bound. Adding
        the (relative, squared) violation restores a gradient that points back
        inside, so the likelihood is still only ever evaluated at feasible
        parameters but the search is pushed into the interior.

        Parameters
        ----------
        raw : ndarray
            Candidate produced by the transform.
        projected : ndarray
            The same candidate clipped onto the declared bounds.

        Returns
        -------
        float
            Penalty to add to the negative log-likelihood (0 when feasible).
        """
        violation = np.abs(raw - projected)
        if not np.any(violation > 0.0):
            return 0.0
        scale = np.maximum(np.abs(projected), 1e-8)
        relative = np.minimum(violation / scale, _MAX_REL_VIOLATION)
        return float(_BOUND_PENALTY * np.sum(relative**2))

    def _constrain_full(
        self, model: VolatilityModel, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Map the search vector to bounded constrained [variance, dist] params."""
        return self._project(
            model.full_transform_params(np.asarray(unconstrained, dtype=np.float64)),
            model.full_bounds(),
        )

    def _constrain_var(
        self, model: VolatilityModel, unconstrained: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Map a variance-block search vector to bounded constrained params."""
        return self._project(
            model.transform_params(np.asarray(unconstrained, dtype=np.float64)),
            model.bounds(),
        )

    def _make_objective(
        self,
        model: VolatilityModel,
        backcast: float,
        fixed_tail: NDArray[np.float64] | None = None,
    ) -> Callable[[NDArray[np.float64]], float]:
        """Build the penalized objective, with the bounds box resolved once.

        The returned closure maps the search vector to constrained parameters,
        projects them onto the declared bounds, evaluates the likelihood there
        and adds :meth:`_bound_penalty`. Resolving the bounds up front keeps the
        per-evaluation cost down (the objective is called thousands of times).

        Parameters
        ----------
        model : VolatilityModel
            Model being fitted.
        backcast : float
            Initial variance.
        fixed_tail : ndarray, optional
            Distribution parameters held fixed; when given, the search vector
            covers only the variance block (warm-start phase).

        Returns
        -------
        callable
            Objective suitable for ``scipy.optimize.minimize``.
        """
        if fixed_tail is None:
            transform = model.full_transform_params
            lower, upper = self._bounds_box(model.full_bounds(), model.n_total_params)
        else:
            transform = model.transform_params
            lower, upper = self._bounds_box(model.bounds(), model.num_params)

        def objective(unconstrained: NDArray[np.float64]) -> float:
            """Penalized negative log-likelihood at a candidate vector."""
            raw = transform(unconstrained)
            projected = np.clip(raw, lower, upper)
            full = projected if fixed_tail is None else np.concatenate([projected, fixed_tail])
            value = -model.loglike(full, backcast)
            if not np.array_equal(projected, raw):
                value += self._bound_penalty(raw, projected)
            return value

        return objective

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
            Fix omega via variance targeting. Only allowed for models that set
            ``supports_variance_targeting = True`` (the plain GARCH layout).
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

        Raises
        ------
        ValueError
            If ``variance_targeting`` is requested for a model that does not
            support it, or if the sample variance is not strictly positive.
        """
        backcast = model._backcast(model.endog)

        if starting_values is not None:
            x0_constrained = np.asarray(starting_values, dtype=np.float64).copy()
        else:
            x0_constrained = model.full_start_params()

        if variance_targeting:
            if not getattr(model, "supports_variance_targeting", False):
                msg = (
                    f"Variance targeting is not supported for "
                    f"{type(model).__name__}: rebuilding omega as "
                    "var * (1 - persistence) assumes the plain GARCH layout "
                    "[omega, alpha_1..q, beta_1..p]. Set "
                    "supports_variance_targeting = True on the model if that layout "
                    "applies, or fit with variance_targeting=False."
                )
                raise ValueError(msg)
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

    @staticmethod
    def _report_failure(message: str) -> None:
        """Log and warn (never raise) when the optimizer does not converge."""
        text = f"Optimization did not converge: {message}"
        logger.warning(text)
        warnings.warn(text, ConvergenceWarning, stacklevel=3)

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
        nv = model.num_params
        n_dist = model.dist.num_params

        # Warm-start: when shape parameters are present, the joint surface is
        # very flat along the shape direction and the optimizer can settle in a
        # poor region of the variance block. Refine the variance block first
        # (holding shape params at their starting values), then optimize jointly.
        if n_dist > 0:
            x0_var_unc = model.untransform_params(x0_constrained[:nv])

            neg_loglike_var = self._make_objective(model, backcast, x0_constrained[nv:])

            var_result = optimize.minimize(
                neg_loglike_var,
                x0_var_unc,
                method=optimizer,
                options={"maxiter": maxiter, "disp": False, "ftol": 1e-10},
            )
            warm_var = self._constrain_var(model, var_result.x)
            x0_constrained = np.concatenate([warm_var, x0_constrained[nv:]])

        x0 = model.full_untransform_params(x0_constrained)

        neg_loglike = self._make_objective(model, backcast)

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        if not result.success:
            self._report_failure(str(result.message))

        params_opt = self._constrain_full(model, result.x)
        # -result.fun would include the bound penalty; report the likelihood
        # actually attained at the (feasible) reported parameters.
        loglike_val = model.loglike(params_opt, backcast)

        # Use the model-level path so models with a non-standard mapping from
        # returns to residuals (e.g. GARCH-M) report the sigma2 the likelihood used.
        sigma2 = model.conditional_variance(params_opt, backcast)

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
            convergence=bool(result.success),
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
        """MLE fit with variance targeting (omega fixed).

        ``omega = var * (1 - sum(alpha) - sum(beta))`` is rebuilt at every
        evaluation, so only the GARCH layout is admissible (enforced by
        ``fit``). The reconstruction is guarded on both sides: persistence is
        capped strictly below one and the resulting ``omega`` is always
        strictly positive - a candidate that would violate either is rejected
        by the objective, and the final fallback rescales instead of silently
        returning ``omega <= 0``.
        """
        sample_var = float(np.var(model.endog))
        if not np.isfinite(sample_var) or sample_var <= 0.0:
            msg = (
                "Variance targeting requires a strictly positive sample variance, "
                f"got {sample_var!r}."
            )
            raise ValueError(msg)

        nv = model.num_params
        dist = model.dist

        # Split constrained start values into variance and distribution blocks.
        var_constrained = x0_constrained[:nv]
        dist_constrained = x0_constrained[nv:]

        # Free variance params (exclude omega), optimized in log space.
        x0_free = np.maximum(var_constrained[1:], 1e-8)
        x0_free_unc = np.log(x0_free)
        # Distribution params optimized in their own unconstrained space.
        x0_dist_unc = dist.untransform_params(dist_constrained)
        x0_combined = np.concatenate([x0_free_unc, x0_dist_unc])
        n_free_var = len(x0_free_unc)

        def _rebuild(
            unconstrained: NDArray[np.float64], rescale: bool
        ) -> NDArray[np.float64] | None:
            """Reconstruct full constrained params from the targeting vector.

            With ``rescale=False`` an infeasible candidate returns ``None`` (so
            the objective can reject it); with ``rescale=True`` the free
            parameters are shrunk until persistence is admissible, which
            guarantees ``omega > 0``.
            """
            free_var = np.exp(np.clip(unconstrained[:n_free_var], -50.0, 50.0))
            persistence = float(np.sum(free_var))
            if persistence >= _MAX_TARGET_PERSISTENCE:
                if not rescale:
                    return None
                free_var = free_var * (_MAX_TARGET_PERSISTENCE / persistence)
                persistence = _MAX_TARGET_PERSISTENCE
            omega = sample_var * (1.0 - persistence)
            if omega <= 0.0:
                if not rescale:
                    return None
                omega = sample_var * (1.0 - _MAX_TARGET_PERSISTENCE)
            dist_params = dist.transform_params(unconstrained[n_free_var:])
            full = np.concatenate([[omega], free_var, dist_params])
            return self._project(full, model.full_bounds())

        def neg_loglike_targeted(unconstrained: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood with variance targeting."""
            full_params = _rebuild(unconstrained, rescale=False)
            if full_params is None:
                return 1e10
            ll = model.loglike(full_params, backcast)
            return -ll

        result = optimize.minimize(
            neg_loglike_targeted,
            x0_combined,
            method=optimizer,
            options={"maxiter": maxiter, "disp": disp, "ftol": 1e-10},
        )

        converged = bool(result.success)
        if not converged:
            self._report_failure(str(result.message))

        params_opt = _rebuild(result.x, rescale=False)
        if params_opt is None:
            # The optimizer ended on an infeasible point: rescale to the
            # stationarity cap rather than emitting a non-positive omega.
            converged = False
            rescued = _rebuild(result.x, rescale=True)
            if rescued is None:  # pragma: no cover - rescale=True always succeeds
                msg = "Variance targeting could not rebuild a feasible parameter vector."
                raise ValueError(msg)
            params_opt = rescued
            text = (
                "Variance targeting ended on a non-stationary point; parameters "
                f"were rescaled to persistence {_MAX_TARGET_PERSISTENCE}."
            )
            logger.warning(text)
            warnings.warn(text, ConvergenceWarning, stacklevel=3)

        loglike_val = model.loglike(params_opt, backcast)

        sigma2 = model.conditional_variance(params_opt, backcast)

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
            convergence=converged,
        )

    # --- Standard errors ---

    @staticmethod
    def _se_from_variance(
        variances: NDArray[np.float64],
        names: list[str],
        label: str,
    ) -> NDArray[np.float64]:
        """Square-root the diagonal of a covariance matrix, NaN where invalid.

        A non positive-definite Hessian (or a sandwich built from one) produces
        non-positive variances. Those entries become ``NaN`` - never
        ``sqrt(|.|)``, which would report a confident-looking standard error
        for a direction in which the likelihood is not even locally concave.

        Parameters
        ----------
        variances : ndarray
            Diagonal of the estimated covariance matrix.
        names : list of str
            Parameter names, used in the warning message.
        label : str
            'robust' or 'non-robust', used in the warning message.

        Returns
        -------
        ndarray
            Standard errors, ``NaN`` for invalid entries.
        """
        diag = np.asarray(variances, dtype=np.float64)
        valid = np.isfinite(diag) & (diag > 0.0)
        if not np.all(valid):
            bad = [names[i] if i < len(names) else str(i) for i in np.flatnonzero(~valid)]
            text = (
                f"Could not compute {label} standard errors for {bad}: the estimated "
                "covariance is not positive definite (the optimum may not be a proper "
                "interior maximum). Reporting NaN."
            )
            logger.warning(text)
            warnings.warn(text, StandardErrorWarning, stacklevel=3)
        return np.where(valid, np.sqrt(np.where(valid, diag, 1.0)), np.nan)

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
            (se_robust, se_nonrobust); entries are ``NaN`` when the Hessian is
            not positive definite.
        """
        k = len(params)
        names = list(model.full_param_names()) if hasattr(model, "full_param_names") else []

        try:
            hessian = self._compute_hessian(model, params, backcast)
            h_inv = np.linalg.inv(hessian)
        except (np.linalg.LinAlgError, ValueError):
            text = "Failed to invert the numerical Hessian; standard errors are reported as NaN."
            logger.warning(text)
            warnings.warn(text, StandardErrorWarning, stacklevel=2)
            return np.full(k, np.nan), np.full(k, np.nan)

        se_nonrobust = self._se_from_variance(
            np.asarray(np.diag(h_inv), dtype=np.float64), names, "non-robust"
        )

        try:
            opg = self._compute_opg(model, params, backcast)
            sandwich = h_inv @ opg @ h_inv
        except (np.linalg.LinAlgError, ValueError):
            text = "Failed to compute the OPG matrix; robust standard errors are NaN."
            logger.warning(text)
            warnings.warn(text, StandardErrorWarning, stacklevel=2)
            return np.full(k, np.nan), se_nonrobust

        se_robust = self._se_from_variance(
            np.asarray(np.diag(sandwich), dtype=np.float64), names, "robust"
        )
        return se_robust, se_nonrobust

    def _compute_hessian(
        self,
        model: VolatilityModel,
        params: NDArray[np.float64],
        backcast: float,
    ) -> NDArray[np.float64]:
        """Compute numerical Hessian of negative log-likelihood.

        Uses second-order central differences with the step of :func:`_fd_step`.

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

        def neg_ll(p: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for Hessian computation."""
            return -model.loglike(p, backcast)

        steps = np.array([_fd_step(float(params[i])) for i in range(k)], dtype=np.float64)
        hessian = np.zeros((k, k))

        for i in range(k):
            for j in range(i, k):
                ei = np.zeros(k)
                ej = np.zeros(k)
                ei[i] = steps[i]
                ej[j] = steps[j]

                fpp = neg_ll(params + ei + ej)
                fpm = neg_ll(params + ei - ej)
                fmp = neg_ll(params - ei + ej)
                fmm = neg_ll(params - ei - ej)

                hessian[i, j] = (fpp - fpm - fmp + fmm) / (4.0 * steps[i] * steps[j])
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

        ll_base = model.loglike_per_obs(params, backcast)
        n_obs = len(ll_base)

        # Compute gradient per observation via finite differences
        gradients = np.zeros((n_obs, k))
        for j in range(k):
            step = _fd_step(float(params[j]))
            ej = np.zeros(k)
            ej[j] = step

            ll_plus = model.loglike_per_obs(params + ej, backcast)
            ll_minus = model.loglike_per_obs(params - ej, backcast)
            gradients[:, j] = (ll_plus - ll_minus) / (2.0 * step)

        # OPG = sum(g_t * g_t')
        return gradients.T @ gradients
