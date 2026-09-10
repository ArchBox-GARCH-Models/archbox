"""Base class for multivariate volatility models."""

from __future__ import annotations

import warnings
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

import numpy as np
import pandas as pd
from numpy.typing import NDArray
from scipy import optimize

from archbox.core.exceptions import ConvergenceError, ConvergenceWarning
from archbox.multivariate.results import MultivarResults
from archbox.multivariate.utils import (
    corr_to_cov,
    numerical_hessian,
    standard_errors_from_hessian,
    validate_multivariate_returns,
)

#: Value returned to the optimizer when the objective cannot be evaluated.
PENALTY = 1e10


def correlation_loglike(
    corr_t: NDArray[np.float64],
    std_resids: NDArray[np.float64],
) -> float:
    """Correlation part of the Gaussian log-likelihood, vectorised over time.

    Computes ``-0.5 * sum_t [log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t]`` with a
    single batched ``slogdet``/``solve`` instead of a Python loop over t.

    Parameters
    ----------
    corr_t : ndarray
        Dynamic correlation matrices (T, k, k).
    std_resids : ndarray
        Standardized residuals (T, k).

    Returns
    -------
    float
        The correlation log-likelihood, or ``-inf`` if any R_t is not positive
        definite or the linear solve fails.
    """
    sign, logdet = np.linalg.slogdet(corr_t)
    if np.any(sign <= 0.0) or not np.all(np.isfinite(logdet)):
        return -np.inf
    try:
        solved = np.linalg.solve(corr_t, std_resids[:, :, None])[:, :, 0]
    except np.linalg.LinAlgError:
        return -np.inf
    quad_r = np.einsum("tk,tk->t", std_resids, solved)
    quad_i = np.einsum("tk,tk->t", std_resids, std_resids)
    total = float(np.sum(logdet + quad_r - quad_i))
    if not np.isfinite(total):
        return -np.inf
    return -0.5 * total


@dataclass
class OptimOutcome:
    """Outcome of a (multi-start) numerical optimization.

    Attributes
    ----------
    params : ndarray
        Best parameter vector found.
    fun : float
        Objective value (a *negative* log-likelihood) at ``params``.
    converged : bool
        True when at least one start reported success.
    n_success : int
        How many starting points converged.
    messages : list of str
        Optimizer messages, one per starting point.
    """

    params: NDArray[np.float64]
    fun: float
    converged: bool
    n_success: int = 0
    messages: list[str] = field(default_factory=list)


def _resolve_univariate_factory(
    univariate_model: str | type | Callable[..., Any],
) -> Callable[..., Any]:
    """Turn the ``univariate_model`` argument into a model factory.

    Accepts a model name (``'GARCH'``, ``'EGARCH'``, ...), a
    ``VolatilityModel`` subclass, or a callable factory taking the series (and
    optionally ``p``/``q``/``mean``/``dist`` keywords).

    Parameters
    ----------
    univariate_model : str or type or callable
        Specification of the univariate model.

    Returns
    -------
    callable
        A factory ``f(series, p=..., q=..., mean=..., dist=...)``.

    Raises
    ------
    ValueError
        If the string does not name a known univariate model.
    TypeError
        If the object is neither a string, a class, nor a callable.
    """
    if isinstance(univariate_model, str):
        from archbox import models as _models

        key = univariate_model.strip().upper().replace("-", "").replace("_", "")
        registry = {
            "GARCH": _models.GARCH,
            "EGARCH": _models.EGARCH,
            "GJRGARCH": _models.GJRGARCH,
            "GJR": _models.GJRGARCH,
            "APARCH": _models.APARCH,
            "IGARCH": _models.IGARCH,
            "FIGARCH": _models.FIGARCH,
            "GARCHM": _models.GARCHM,
            "COMPONENTGARCH": _models.ComponentGARCH,
        }
        if key not in registry:
            msg = (
                f"Unknown univariate_model {univariate_model!r}. "
                f"Choose one of {sorted(registry)} or pass a model class/factory."
            )
            raise ValueError(msg)
        return registry[key]
    if isinstance(univariate_model, type) or callable(univariate_model):
        return univariate_model
    msg = (
        "univariate_model must be a model name, a VolatilityModel subclass, "
        f"or a callable factory, got {type(univariate_model).__name__}"
    )
    raise TypeError(msg)


class MultivariateVolatilityModel(ABC):
    """Abstract base class for multivariate GARCH models.

    All multivariate models (DCC, CCC, BEKK, GO-GARCH, DECO) inherit from this class.

    Parameters
    ----------
    endog : array-like
        Array or DataFrame of shape (T, k) with k return series. When a pandas
        object is passed, its column names and index are kept and used to label
        the fitted output.
    univariate_model : str or type or callable
        Univariate volatility model used for each series. Either a name
        (``'GARCH'``, ``'EGARCH'``, ``'GJR-GARCH'``, ...), a ``VolatilityModel``
        subclass, or a factory called as ``factory(series, p=, q=, mean=, dist=)``.
        Default ``'GARCH'``.
    univariate_order : tuple[int, int]
        (p, q) order for the univariate model. Default (1, 1).
    univariate_dist : str
        Conditional distribution for the univariate models. Default 'normal'.

    Attributes
    ----------
    endog : NDArray[np.float64]
        Returns array (T, k).
    T : int
        Number of observations.
    k : int
        Number of series.
    series_names : list of str
        Column names (from the input DataFrame, or ``series_0 ... series_{k-1}``).
    """

    model_name: str = "Unknown"

    #: Estimation methods the model accepts in ``fit(method=...)``.
    supported_methods: tuple[str, ...] = ("two_step",)

    def __init__(
        self,
        endog: Any,
        univariate_model: str | type | Callable[..., Any] = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
        univariate_dist: str = "normal",
    ) -> None:
        """Initialize multivariate volatility model with return data."""
        self.series_names: list[str] = []
        self.index: pd.Index | None = None
        if isinstance(endog, pd.DataFrame):
            self.series_names = [str(c) for c in endog.columns]
            self.index = endog.index
            values = endog.to_numpy()
        elif isinstance(endog, pd.Series):
            values = endog.to_numpy()
        else:
            values = endog

        self.endog = np.asarray(values, dtype=np.float64)
        validate_multivariate_returns(self.endog)

        self.T, self.k = self.endog.shape
        if not self.series_names:
            self.series_names = [f"series_{i}" for i in range(self.k)]

        self.univariate_model = univariate_model
        self.univariate_order = univariate_order
        self.univariate_dist = univariate_dist
        # Fails fast on a bad spec instead of at fit() time.
        self._univariate_factory = _resolve_univariate_factory(univariate_model)

        self._is_fitted = False
        self._univariate_results: list[Any] | None = None
        self._std_resids: NDArray[np.float64] | None = None
        self._conditional_volatility: NDArray[np.float64] | None = None

    # --- Abstract methods (subclass MUST implement) ---

    @abstractmethod
    def _correlation_recursion(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t.

        Parameters
        ----------
        params : ndarray
            Correlation model parameters.
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """

    @property
    @abstractmethod
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values for correlation model optimization."""

    @property
    @abstractmethod
    def param_names(self) -> list[str]:
        """Parameter names for the correlation model."""

    # --- Univariate (first) step ---

    def _build_univariate(self, series: NDArray[np.float64]) -> Any:
        """Instantiate the configured univariate model for one series.

        Parameters
        ----------
        series : ndarray
            One return series (T,).

        Returns
        -------
        VolatilityModel
            An unfitted univariate model.
        """
        p, q = self.univariate_order
        factory = self._univariate_factory
        try:
            return factory(series, p=p, q=q, mean="constant", dist=self.univariate_dist)
        except TypeError:
            # A user-supplied factory may only accept the series.
            return factory(series)

    def _fit_univariate(self) -> None:
        """Fit the univariate model to each series (Step 1 of the two-step).

        Populates ``self._univariate_results``, ``self._std_resids`` and
        ``self._conditional_volatility``. The standardized residuals are taken
        straight from ``ArchResults.std_resid`` (``resid`` holds *raw*
        residuals, so dividing it by sigma again would rescale the data twice).
        """
        results_list: list[Any] = []
        std_resids = np.zeros((self.T, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for i in range(self.k):
            model = self._build_univariate(self.endog[:, i])
            res = model.fit(disp=False)
            results_list.append(res)
            # res.resid  -> raw residuals (return scale)
            # res.std_resid -> z_{i,t} = eps_{i,t} / sigma_{i,t}
            std_resids[:, i] = np.asarray(res.std_resid, dtype=np.float64)
            cond_vol[:, i] = np.asarray(res.conditional_volatility, dtype=np.float64)

        self._univariate_results = results_list
        self._std_resids = std_resids
        self._conditional_volatility = cond_vol

    def _univariate_volatility_forecast(
        self,
        results: MultivarResults,
        horizon: int,
    ) -> NDArray[np.float64]:
        """Forecast each series' conditional volatility ``horizon`` steps ahead.

        Uses every univariate ``ArchResults.forecast(horizon)`` rather than
        holding the last in-sample value constant. Falls back to the last
        fitted volatility only when a univariate result cannot forecast.

        Parameters
        ----------
        results : MultivarResults
            Fitted model results.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        ndarray
            Forecast volatilities, shape (horizon, k).
        """
        last = np.asarray(results.conditional_volatility[-1], dtype=np.float64)
        n_series = last.size
        vol = np.tile(last, (horizon, 1))
        for i, res in enumerate(results.univariate_results[:n_series]):
            forecast = getattr(res, "forecast", None)
            if forecast is None:
                continue
            fc = forecast(horizon=horizon)
            variance = np.asarray(fc["variance"], dtype=np.float64).ravel()
            if variance.size < horizon or not np.all(np.isfinite(variance[:horizon])):
                continue
            vol[:, i] = np.sqrt(np.maximum(variance[:horizon], 0.0))
        return vol

    # --- Fit ---

    def _check_method(self, method: str) -> None:
        """Validate the ``method`` argument of ``fit``.

        Parameters
        ----------
        method : str
            Requested estimation method.

        Raises
        ------
        ValueError
            If the method is not supported by this model.
        """
        if method not in self.supported_methods:
            msg = (
                f"{type(self).__name__} does not support method={method!r}; "
                f"supported methods: {list(self.supported_methods)}"
            )
            raise ValueError(msg)

    def fit(self, method: str = "two_step", disp: bool = True) -> MultivarResults:
        """Fit the multivariate GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Must be one of ``supported_methods``.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.

        Raises
        ------
        ConvergenceError
            If the log-likelihood at the estimated parameters is not finite.
        """
        self._check_method(method)

        # Step 1: fit univariate models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: estimate correlation parameters
        outcome = self._estimate_correlation(self._std_resids, disp=disp)
        params = outcome.params
        self._warn_if_not_converged(outcome)

        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)
        if not np.isfinite(loglike):
            msg = (
                f"{self.model_name}: the log-likelihood at the estimated parameters "
                "is not finite; the model did not converge to a usable optimum."
            )
            raise ConvergenceError(msg)

        std_errors = self._correlation_standard_errors(params, self._std_resids)

        # Count total parameters (univariate + correlation)
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params + len(params)

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
            param_names=self.param_names,
            std_errors=std_errors,
            converged=outcome.converged,
            series_names=self.series_names,
            index=self.index,
            extras=self._results_extras(params, self._std_resids),
        )

    def _results_extras(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> dict[str, Any]:
        """State a subclass needs at forecast time, stored on the results.

        Parameters
        ----------
        params : ndarray
            Estimated correlation parameters.
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        dict
            Model-specific extras. Empty by default.
        """
        del params, std_resids
        return {}

    def _warn_if_not_converged(self, outcome: OptimOutcome) -> None:
        """Warn (loudly) when no optimizer start reported success.

        Parameters
        ----------
        outcome : OptimOutcome
            Result of the second-step optimization.
        """
        if outcome.converged or outcome.params.size == 0:
            return
        detail = "; ".join(outcome.messages[:3]) or "no optimizer message"
        msg = (
            f"{self.model_name}: none of the optimizer starting points converged "
            f"({detail}). The reported parameters are the best point found and "
            "results.converged is False."
        )
        warnings.warn(msg, ConvergenceWarning, stacklevel=3)

    # --- Second-step estimation ---

    def _second_step_neg_loglike(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> float:
        """Negative correlation log-likelihood, without any bound penalty.

        Parameters
        ----------
        params : ndarray
            Correlation model parameters.
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        float
            ``-correlation_loglike(R_t(params), z)``; ``inf`` when infeasible.
        """
        corr_t = self._correlation_recursion(params, std_resids)
        ll = correlation_loglike(corr_t, std_resids)
        if not np.isfinite(ll):
            return float(np.inf)
        return -ll

    def _objective(
        self,
        std_resids: NDArray[np.float64],
    ) -> Callable[[NDArray[np.float64]], float]:
        """Build the bounded optimizer objective for the second step."""

        def neg_loglike(params: NDArray[np.float64]) -> float:
            value = self._second_step_neg_loglike(np.asarray(params, dtype=np.float64), std_resids)
            if not np.isfinite(value):
                return PENALTY
            return value

        return neg_loglike

    def _starting_points(self) -> list[NDArray[np.float64]]:
        """Starting points for the multi-start second-step optimization."""
        return [self.start_params]

    def _constraints(self) -> list[dict[str, Any]]:
        """Inequality constraints for the second-step optimization."""
        return []

    def _run_multistart(
        self,
        objective: Callable[[NDArray[np.float64]], float],
        starting_points: list[NDArray[np.float64]],
        bounds: list[tuple[float, float]] | None,
        constraints: list[dict[str, Any]] | None = None,
        disp: bool = False,
        maxiter: int = 500,
    ) -> OptimOutcome:
        """Run SLSQP from several starting points and keep the best result.

        Parameters
        ----------
        objective : callable
            Negative log-likelihood to minimize.
        starting_points : list of ndarray
            Starting parameter vectors.
        bounds : list of tuple or None
            Box bounds.
        constraints : list of dict or None
            SciPy inequality constraints.
        disp : bool
            Display optimizer progress.
        maxiter : int
            Maximum iterations per start.

        Returns
        -------
        OptimOutcome
            Best point found, with a convergence flag.
        """
        best_fun = np.inf
        best_x = np.asarray(starting_points[0], dtype=np.float64)
        best_from_success = False
        n_success = 0
        messages: list[str] = []

        for x0 in starting_points:
            try:
                result = optimize.minimize(
                    objective,
                    np.asarray(x0, dtype=np.float64),
                    method="SLSQP",
                    bounds=bounds,
                    constraints=constraints or (),
                    options={"maxiter": maxiter, "disp": disp, "ftol": 1e-8},
                )
            except (ValueError, np.linalg.LinAlgError) as exc:  # pragma: no cover - defensive
                messages.append(f"start {np.round(x0, 4).tolist()}: {exc}")
                continue

            messages.append(f"start {np.round(x0, 4).tolist()}: {result.message}")
            fun = float(result.fun)
            success = bool(result.success) and np.isfinite(fun) and fun < PENALTY
            if success:
                n_success += 1
            # A converged point always beats a non-converged one; among equals,
            # the lower objective wins.
            better = (success and not best_from_success) or (
                success == best_from_success and fun < best_fun
            )
            if better and np.isfinite(fun):
                best_fun = fun
                best_x = np.asarray(result.x, dtype=np.float64)
                best_from_success = success

        return OptimOutcome(
            params=best_x,
            fun=best_fun,
            converged=n_success > 0,
            n_success=n_success,
            messages=messages,
        )

    def _estimate_correlation(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> OptimOutcome:
        """Estimate correlation model parameters via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        OptimOutcome
            Estimated correlation parameters and convergence information.
        """
        x0 = self.start_params
        if len(x0) == 0:
            # No parameters to estimate (e.g. CCC, GO-GARCH).
            return OptimOutcome(params=x0, fun=0.0, converged=True, n_success=0)

        return self._run_multistart(
            objective=self._objective(std_resids),
            starting_points=self._starting_points(),
            bounds=self._param_bounds(),
            constraints=self._constraints(),
            disp=disp,
        )

    def _correlation_standard_errors(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Standard errors from the numerical Hessian of the second-step likelihood.

        Parameters
        ----------
        params : ndarray
            Estimated correlation parameters.
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Standard errors, shape ``params.shape``; ``nan`` when the Hessian is
            not positive definite (the optimum sits on a bound, or the surface is
            flat).
        """
        params = np.asarray(params, dtype=np.float64)
        if params.size == 0:
            return np.zeros(0)
        hess = numerical_hessian(
            lambda p: self._second_step_neg_loglike(p, std_resids),
            params,
        )
        return standard_errors_from_hessian(hess)

    def _param_bounds(self) -> list[tuple[float, float]]:
        """Default parameter bounds. Override in subclasses."""
        return [(1e-6, 0.999)] * len(self.start_params)

    # --- Covariance / likelihood helpers ---

    def _compute_covariance(
        self,
        corr_t: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute H_t = D_t * R_t * D_t.

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        ndarray
            Dynamic covariance matrices (T, k, k).
        """
        return corr_to_cov(corr_t, cond_vol)

    def _loglikelihood(
        self,
        corr_t: NDArray[np.float64],
        std_resids: NDArray[np.float64],
        cond_vol: NDArray[np.float64],
    ) -> float:
        """Compute the full multivariate normal log-likelihood.

        loglike = -0.5 * sum_t [ k*log(2*pi) + 2*log|D_t| + log|R_t| + z_t' R_t^{-1} z_t ]

        Parameters
        ----------
        corr_t : ndarray
            Dynamic correlation matrices (T, k, k).
        std_resids : ndarray
            Standardized residuals (T, k).
        cond_vol : ndarray
            Conditional volatilities (T, k).

        Returns
        -------
        float
            Total log-likelihood, or ``-inf`` when some R_t is not usable.
        """
        n_obs, n_k = std_resids.shape
        const = n_k * np.log(2.0 * np.pi)

        sign, logdet_r = np.linalg.slogdet(corr_t)
        if np.any(sign <= 0.0) or not np.all(np.isfinite(logdet_r)):
            return -np.inf
        try:
            solved = np.linalg.solve(corr_t, std_resids[:, :, None])[:, :, 0]
        except np.linalg.LinAlgError:
            return -np.inf

        quad = np.einsum("tk,tk->t", std_resids, solved)
        log_det_d = np.sum(np.log(cond_vol), axis=1)
        total = float(np.sum(2.0 * log_det_d + logdet_r + quad)) + const * n_obs
        ll = -0.5 * total
        if not np.isfinite(ll):
            return -np.inf
        return ll

    def portfolio_variance(
        self,
        weights: NDArray[np.float64],
        cov_t: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute portfolio variance w' H_t w for all t.

        Parameters
        ----------
        weights : ndarray
            Portfolio weights (k,).
        cov_t : ndarray
            Dynamic covariance matrices (T, k, k).

        Returns
        -------
        ndarray
            Portfolio variance series (T,).
        """
        w = np.asarray(weights, dtype=np.float64)
        return np.einsum("i,tij,j->t", w, np.asarray(cov_t, dtype=np.float64), w)

    def forecast(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for h = 1, ..., ``horizon``.

        The default holds the correlation at its last in-sample value and takes
        the variances from each univariate ``ArchResults.forecast(horizon)``.
        Subclasses with correlation dynamics override this.

        Parameters
        ----------
        results : MultivarResults
            Fitted model results.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'covariance' (horizon, k, k) and 'correlation'
            (horizon, k, k).
        """
        if horizon < 1:
            msg = f"horizon must be >= 1, got {horizon}"
            raise ValueError(msg)
        corr_forecast = np.tile(results.dynamic_correlation[-1], (horizon, 1, 1))
        vol = self._univariate_volatility_forecast(results, horizon)
        cov_forecast = corr_to_cov(corr_forecast, vol)
        return {"covariance": cov_forecast, "correlation": corr_forecast}


__all__ = [
    "MultivariateVolatilityModel",
    "MultivarResults",
    "OptimOutcome",
    "correlation_loglike",
]
