"""BEKK-GARCH: Baba-Engle-Kraft-Kroner model (Engle & Kroner, 1995).

H_t = C*C' + A'*eps_{t-1}*eps'_{t-1}*A + B'*H_{t-1}*B

Guarantees positive definite H_t by construction.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import numpy as np
from numpy.typing import NDArray

from archbox.core.exceptions import ConvergenceError
from archbox.multivariate.base import PENALTY, MultivariateVolatilityModel
from archbox.multivariate.results import MultivarResults
from archbox.multivariate.utils import (
    cov_to_corr,
    is_positive_definite,
    numerical_hessian,
    standard_errors_from_hessian,
)


class BEKK(MultivariateVolatilityModel):
    """BEKK-GARCH multivariate volatility model.

    The BEKK model parametrizes the conditional covariance directly,
    guaranteeing positive definiteness by construction.

    Parameters
    ----------
    endog : array-like
        Array or DataFrame of shape (T, k) with k return series.
    variant : str
        'full' for full BEKK, 'diagonal' for diagonal BEKK. Default 'diagonal'.
    univariate_model : str or type or callable
        Not used directly (BEKK uses full MLE). Default 'GARCH'.
    univariate_order : tuple[int, int]
        Not used directly. Default (1, 1).
    univariate_dist : str
        Not used directly. Default 'normal'.

    Examples
    --------
    >>> import numpy as np
    >>> from archbox.multivariate.bekk import BEKK
    >>> returns = np.random.randn(500, 2) * 0.01
    >>> model = BEKK(returns, variant='diagonal')
    >>> results = model.fit()
    >>> print(results.summary())

    References
    ----------
    Engle, R.F. & Kroner, K.F. (1995). Multivariate Simultaneous Generalized ARCH.
    Econometric Theory, 11(1), 122-150.
    """

    model_name: str = "BEKK-GARCH"
    supported_methods: tuple[str, ...] = ("mle",)

    def __init__(
        self,
        endog: Any,
        variant: str = "diagonal",
        univariate_model: str | type | Callable[..., Any] = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
        univariate_dist: str = "normal",
    ) -> None:
        """Initialize BEKK-GARCH model with variant and options."""
        super().__init__(endog, univariate_model, univariate_order, univariate_dist)
        if variant not in ("full", "diagonal"):
            msg = f"variant must be 'full' or 'diagonal', got '{variant}'"
            raise ValueError(msg)
        self.variant = variant
        self.model_name = f"BEKK-GARCH ({variant})"
        self._mu: NDArray[np.float64] | None = None

    # --- Parameter bookkeeping ---

    @property
    def _n_c_params(self) -> int:
        """Number of parameters in lower-triangular C."""
        return self.k * (self.k + 1) // 2

    @property
    def _n_a_params(self) -> int:
        """Number of parameters in A."""
        if self.variant == "diagonal":
            return self.k
        return self.k * self.k

    @property
    def _n_b_params(self) -> int:
        """Number of parameters in B."""
        if self.variant == "diagonal":
            return self.k
        return self.k * self.k

    @property
    def num_params(self) -> int:
        """Total number of covariance parameters (C, A and B; excludes the mean)."""
        return self._n_c_params + self._n_a_params + self._n_b_params

    @property
    def num_mean_params(self) -> int:
        """Number of mean parameters estimated by demeaning the returns."""
        return self.k

    def _unpack_params(
        self, params: NDArray[np.float64]
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """Unpack parameter vector into C, A, B matrices.

        Parameters
        ----------
        params : ndarray
            Flat parameter vector.

        Returns
        -------
        tuple[ndarray, ndarray, ndarray]
            (c_mat, a_mat, b_mat) matrices, each (k, k).
        """
        k = self.k
        idx = 0

        c_mat = np.zeros((k, k))
        rows, cols = np.tril_indices(k)
        c_mat[rows, cols] = params[idx : idx + self._n_c_params]
        idx += self._n_c_params

        if self.variant == "diagonal":
            a_mat = np.diag(np.asarray(params[idx : idx + k], dtype=np.float64))
            idx += k
            b_mat = np.diag(np.asarray(params[idx : idx + k], dtype=np.float64))
            idx += k
        else:
            a_mat = np.asarray(params[idx : idx + k * k], dtype=np.float64).reshape(k, k)
            idx += k * k
            b_mat = np.asarray(params[idx : idx + k * k], dtype=np.float64).reshape(k, k)
            idx += k * k

        return c_mat, a_mat, b_mat

    def _pack_params(
        self,
        c_mat: NDArray[np.float64],
        a_mat: NDArray[np.float64],
        b_mat: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Pack C, A, B matrices into a flat parameter vector.

        Parameters
        ----------
        c_mat : ndarray
            Lower triangular matrix (k, k).
        a_mat : ndarray
            ARCH parameter matrix (k, k).
        b_mat : ndarray
            GARCH parameter matrix (k, k).

        Returns
        -------
        ndarray
            Flat parameter vector.
        """
        k = self.k
        rows, cols = np.tril_indices(k)
        parts: list[NDArray[np.float64]] = [c_mat[rows, cols]]
        if self.variant == "diagonal":
            parts.append(np.diag(a_mat))
            parts.append(np.diag(b_mat))
        else:
            parts.append(a_mat.ravel())
            parts.append(b_mat.ravel())
        return np.concatenate(parts).astype(np.float64)

    @property
    def param_names(self) -> list[str]:
        """Parameter names."""
        k = self.k
        names: list[str] = []
        for i in range(k):
            for j in range(i + 1):
                names.append(f"C[{i},{j}]")
        if self.variant == "diagonal":
            names.extend(f"A[{i},{i}]" for i in range(k))
            names.extend(f"B[{i},{i}]" for i in range(k))
        else:
            names.extend(f"A[{i},{j}]" for i in range(k) for j in range(k))
            names.extend(f"B[{i},{j}]" for i in range(k) for j in range(k))
        return names

    # --- Recursion / likelihood ---

    def _bekk_recursion(
        self,
        c_mat: NDArray[np.float64],
        a_mat: NDArray[np.float64],
        b_mat: NDArray[np.float64],
        resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute the BEKK covariance recursion.

        h_t = C C' + A' eps_{t-1} eps'_{t-1} A + B' h_{t-1} B

        Parameters
        ----------
        c_mat : ndarray
            Lower triangular matrix (k, k).
        a_mat : ndarray
            ARCH parameter matrix (k, k).
        b_mat : ndarray
            GARCH parameter matrix (k, k).
        resids : ndarray
            Residuals (T, k).

        Returns
        -------
        ndarray
            Conditional covariance matrices (T, k, k).
        """
        n_obs, k = resids.shape
        h_t = np.empty((n_obs, k, k))
        cc = c_mat @ c_mat.T

        h_0 = np.cov(resids.T)
        if not is_positive_definite(h_0):
            h_0 = cc + np.eye(k) * 1e-6
        h_t[0] = h_0

        outer = resids[:, :, None] * resids[:, None, :]
        h_prev = h_0
        for t in range(1, n_obs):
            h_prev = cc + a_mat.T @ outer[t - 1] @ a_mat + b_mat.T @ h_prev @ b_mat
            h_prev = 0.5 * (h_prev + h_prev.T)
            h_t[t] = h_prev

        return h_t

    @staticmethod
    def _gaussian_loglike(
        h_t: NDArray[np.float64],
        resids: NDArray[np.float64],
    ) -> float:
        """Full Gaussian log-likelihood of ``resids`` under the H_t path.

        Parameters
        ----------
        h_t : ndarray
            Conditional covariance matrices (T, k, k).
        resids : ndarray
            Residuals (T, k).

        Returns
        -------
        float
            Log-likelihood, or ``-inf`` when some H_t is not positive definite.
        """
        n_obs, k = resids.shape
        if not np.all(np.isfinite(h_t)):
            return -np.inf
        sign, logdet = np.linalg.slogdet(h_t)
        if np.any(sign <= 0.0) or not np.all(np.isfinite(logdet)):
            return -np.inf
        try:
            solved = np.linalg.solve(h_t, resids[:, :, None])[:, :, 0]
        except np.linalg.LinAlgError:
            return -np.inf
        quad = np.einsum("tk,tk->t", resids, solved)
        total = float(np.sum(logdet + quad)) + n_obs * k * np.log(2.0 * np.pi)
        if not np.isfinite(total):
            return -np.inf
        return -0.5 * total

    def _neg_loglike(
        self,
        params: NDArray[np.float64],
        resids: NDArray[np.float64],
    ) -> float:
        """Negative BEKK log-likelihood, ``inf`` when the parameters are infeasible."""
        c_mat, a_mat, b_mat = self._unpack_params(np.asarray(params, dtype=np.float64))
        if self.stationarity_measure(a_mat, b_mat) >= 1.0:
            return float(np.inf)
        with np.errstate(over="ignore", invalid="ignore"):
            h_t = self._bekk_recursion(c_mat, a_mat, b_mat, resids)
            ll = self._gaussian_loglike(h_t, resids)
        if not np.isfinite(ll):
            return float(np.inf)
        return -ll

    # --- Constraints ---

    @staticmethod
    def stationarity_measure(
        a_mat: NDArray[np.float64],
        b_mat: NDArray[np.float64],
    ) -> float:
        """Spectral radius of (A' kron A') + (B' kron B').

        The BEKK covariance process is covariance stationary iff this value is
        strictly below 1 (Engle & Kroner, 1995, Prop. 2.7).

        Parameters
        ----------
        a_mat : ndarray
            ARCH parameter matrix (k, k).
        b_mat : ndarray
            GARCH parameter matrix (k, k).

        Returns
        -------
        float
            Spectral radius, or ``inf`` if it cannot be computed.
        """
        companion = np.kron(a_mat.T, a_mat.T) + np.kron(b_mat.T, b_mat.T)
        if not np.all(np.isfinite(companion)):
            return float(np.inf)
        try:
            eigvals = np.linalg.eigvals(companion)
        except np.linalg.LinAlgError:  # pragma: no cover - defensive
            return float(np.inf)
        return float(np.max(np.abs(eigvals)))

    def _stationarity_slack(self, params: NDArray[np.float64]) -> float:
        """Inequality-constraint slack: positive iff the process is stationary."""
        _c_mat, a_mat, b_mat = self._unpack_params(np.asarray(params, dtype=np.float64))
        return 1.0 - 1e-6 - self.stationarity_measure(a_mat, b_mat)

    def _param_bounds(self) -> list[tuple[float, float]]:
        """Box bounds for (C, A, B).

        The diagonal of C is kept strictly positive (C C' identifiable and PD)
        and all entries are bounded on the scale of the data; A and B entries
        are bounded well inside the region where the spectral-radius constraint
        can still bind.
        """
        scale = float(np.sqrt(np.mean(np.diag(np.atleast_2d(np.cov(self.endog.T))))))
        scale = max(scale, 1e-8)
        bounds: list[tuple[float, float]] = []
        for i in range(self.k):
            for j in range(i + 1):
                if i == j:
                    bounds.append((1e-8 * scale, 10.0 * scale))
                else:
                    bounds.append((-10.0 * scale, 10.0 * scale))
        limit = 0.999 if self.variant == "diagonal" else 1.5
        bounds.extend([(-limit, limit)] * self._n_a_params)
        bounds.extend([(-limit, limit)] * self._n_b_params)
        return bounds

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Starting parameter values.

        C: Cholesky of (sample_covariance * 0.05); A: diag(0.2); B: diag(0.8).
        """
        return self._starting_points()[0]

    def _c_start(self, weight: float) -> NDArray[np.float64]:
        """Cholesky factor of ``weight`` times the sample covariance."""
        sample_cov = np.atleast_2d(np.cov(self.endog.T))
        try:
            return np.linalg.cholesky(sample_cov * weight).astype(np.float64)
        except np.linalg.LinAlgError:
            return np.eye(self.k) * np.sqrt(weight * np.mean(np.diag(sample_cov)))

    def _starting_points(self) -> list[NDArray[np.float64]]:
        """Several (C, A, B) starts, all inside the stationarity region."""
        specs = [(0.05, 0.2, 0.8), (0.20, 0.1, 0.5), (0.10, 0.3, 0.7), (0.50, 0.15, 0.2)]
        return [
            self._pack_params(
                self._c_start(weight),
                np.eye(self.k) * a,
                np.eye(self.k) * b,
            )
            for weight, a, b in specs
        ]

    def _correlation_recursion(
        self,
        params: NDArray[np.float64],  # noqa: ARG002
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Not used for BEKK (it models H_t directly, not R_t).

        Required by the ABC; BEKK overrides ``fit`` and works with H_t.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Identity correlation matrices, shape (T, k, k).
        """
        n_obs, k = std_resids.shape
        return np.broadcast_to(np.eye(k), (n_obs, k, k)).copy()

    # --- Fit ---

    def fit(self, method: str = "mle", disp: bool = True) -> MultivarResults:
        """Fit the BEKK-GARCH model via full MLE.

        Parameters
        ----------
        method : str
            Estimation method. Only 'mle' is supported for BEKK.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.

        Raises
        ------
        ConvergenceError
            If no starting point yields a finite log-likelihood.
        """
        self._check_method(method)

        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu
        self._mu = mu

        def objective(params: NDArray[np.float64]) -> float:
            value = self._neg_loglike(params, resids)
            return PENALTY if not np.isfinite(value) else value

        outcome = self._run_multistart(
            objective=objective,
            starting_points=self._starting_points(),
            bounds=self._param_bounds(),
            constraints=[{"type": "ineq", "fun": self._stationarity_slack}],
            disp=disp,
            maxiter=1000,
        )
        self._warn_if_not_converged(outcome)

        opt_params = outcome.params
        c_mat, a_mat, b_mat = self._unpack_params(opt_params)
        h_t = self._bekk_recursion(c_mat, a_mat, b_mat, resids)
        loglike = self._gaussian_loglike(h_t, resids)
        if not np.isfinite(loglike):
            msg = (
                f"{self.model_name}: no starting point produced a finite "
                "log-likelihood; the model failed to converge."
            )
            raise ConvergenceError(msg)

        cond_vol = np.sqrt(np.maximum(np.diagonal(h_t, axis1=1, axis2=2), 1e-24))
        r_t = cov_to_corr(h_t)
        std_resids = resids / cond_vol

        # AIC/BIC count the k mean parameters removed by demeaning.
        n_params = len(opt_params) + self.num_mean_params
        aic = -2.0 * loglike + 2.0 * n_params
        bic = -2.0 * loglike + np.log(self.T) * n_params

        std_errors = standard_errors_from_hessian(
            numerical_hessian(lambda p: self._neg_loglike(p, resids), opt_params)
        )

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=[],  # BEKK does not use a univariate step
            params=opt_params,
            dynamic_correlation=r_t,
            dynamic_covariance=h_t,
            conditional_volatility=cond_vol,
            std_resids=std_resids,
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
            extras={"mu": mu, "resid_last": resids[-1].copy(), "variant": self.variant},
        )

    # --- Forecast ---

    def forecast(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using BEKK dynamics.

        The one-step forecast is the in-sample recursion applied one step ahead,

            H_{T+1} = C C' + A' eps_T eps_T' A + B' H_T B,

        and for h > 1 the unknown eps eps' is replaced by its conditional
        expectation H_{T+h-1}:

            H_{T+h} = C C' + A' H_{T+h-1} A + B' H_{T+h-1} B.

        Parameters
        ----------
        results : MultivarResults
            Fitted model results.
        horizon : int
            Number of steps ahead.

        Returns
        -------
        dict
            Dictionary with 'covariance' and 'correlation' forecasts.
        """
        if horizon < 1:
            msg = f"horizon must be >= 1, got {horizon}"
            raise ValueError(msg)

        c_mat, a_mat, b_mat = self._unpack_params(results.params)
        cc = c_mat @ c_mat.T
        eps_last = np.asarray(results.extras["resid_last"], dtype=np.float64)

        h_forecast = np.zeros((horizon, self.k, self.k))
        h_prev = np.asarray(results.dynamic_covariance[-1], dtype=np.float64)

        for h in range(horizon):
            shock = np.outer(eps_last, eps_last) if h == 0 else h_prev
            h_next = cc + a_mat.T @ shock @ a_mat + b_mat.T @ h_prev @ b_mat
            h_next = 0.5 * (h_next + h_next.T)
            h_forecast[h] = h_next
            h_prev = h_next

        return {"covariance": h_forecast, "correlation": cov_to_corr(h_forecast)}
