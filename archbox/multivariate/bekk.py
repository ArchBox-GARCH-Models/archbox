"""BEKK-GARCH: Baba-Engle-Kraft-Kroner model (Engle & Kroner, 1995).

H_t = C*C' + A'*eps_{t-1}*eps'_{t-1}*A + B'*H_{t-1}*B

Guarantees positive definite H_t by construction.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy import optimize

from archbox.multivariate.base import MultivariateVolatilityModel, MultivarResults
from archbox.multivariate.utils import is_positive_definite


class BEKK(MultivariateVolatilityModel):
    """BEKK-GARCH multivariate volatility model.

    The BEKK model parametrizes the conditional covariance directly,
    guaranteeing positive definiteness by construction.

    Parameters
    ----------
    endog : ndarray
        Array of shape (T, k) with k return series.
    variant : str
        'full' for full BEKK, 'diagonal' for diagonal BEKK. Default 'diagonal'.
    univariate_model : str
        Not used directly (BEKK uses full MLE). Default 'GARCH'.
    univariate_order : tuple[int, int]
        Not used directly. Default (1, 1).

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

    def __init__(
        self,
        endog: Any,
        variant: str = "diagonal",
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize BEKK-GARCH model with variant and options."""
        super().__init__(endog, univariate_model, univariate_order)
        if variant not in ("full", "diagonal"):
            msg = f"variant must be 'full' or 'diagonal', got '{variant}'"
            raise ValueError(msg)
        self.variant = variant
        self.model_name = f"BEKK-GARCH ({variant})"

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
        """Total number of model parameters."""
        return self._n_c_params + self._n_a_params + self._n_b_params

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

        # c_mat: lower triangular
        c_mat = np.zeros((k, k))
        for i in range(k):
            for j in range(i + 1):
                c_mat[i, j] = params[idx]
                idx += 1

        # a_mat
        if self.variant == "diagonal":
            a_mat = np.diag(params[idx : idx + k])
            idx += k
        else:
            a_mat = params[idx : idx + k * k].reshape(k, k)
            idx += k * k

        # b_mat
        if self.variant == "diagonal":
            b_mat = np.diag(params[idx : idx + k])
            idx += k
        else:
            b_mat = params[idx : idx + k * k].reshape(k, k)
            idx += k * k

        return c_mat, a_mat, b_mat

    def _pack_params(
        self,
        c_mat: NDArray[np.float64],
        a_mat: NDArray[np.float64],
        b_mat: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Pack C, A, B matrices into flat parameter vector.

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
        params_list: list[float] = []

        # c_mat: lower triangular elements
        for i in range(k):
            for j in range(i + 1):
                params_list.append(c_mat[i, j])

        # a_mat
        if self.variant == "diagonal":
            params_list.extend(np.diag(a_mat).tolist())
        else:
            params_list.extend(a_mat.ravel().tolist())

        # b_mat
        if self.variant == "diagonal":
            params_list.extend(np.diag(b_mat).tolist())
        else:
            params_list.extend(b_mat.ravel().tolist())

        return np.array(params_list, dtype=np.float64)

    def _bekk_recursion(
        self,
        c_mat: NDArray[np.float64],
        a_mat: NDArray[np.float64],
        b_mat: NDArray[np.float64],
        resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute BEKK covariance recursion.

        h_t = c_mat @ c_mat' + a_mat' @ eps_{t-1} @ eps'_{t-1} @ a_mat
              + b_mat' @ h_{t-1} @ b_mat

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
        h_t = np.zeros((n_obs, k, k))
        cc = c_mat @ c_mat.T

        # Initialize h_0 with sample covariance
        h_t[0] = np.cov(resids.T)
        if not is_positive_definite(h_t[0]):
            h_t[0] = cc + np.eye(k) * 1e-6

        for t in range(1, n_obs):
            eps = resids[t - 1 : t].T  # (k, 1)
            h_t[t] = cc + a_mat.T @ (eps @ eps.T) @ a_mat + b_mat.T @ h_t[t - 1] @ b_mat

            # Ensure symmetry
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0

        return h_t

    def _correlation_recursion(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Not used for BEKK (BEKK models H_t directly, not R_t).

        This method is required by the ABC but BEKK overrides fit() directly.
        Returns identity correlation matrices as placeholder.

        Parameters
        ----------
        params : ndarray
            Model parameters.
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Correlation matrices derived from H_t, shape (T, k, k).
        """
        n_obs, k = std_resids.shape
        r_t = np.zeros((n_obs, k, k))
        for t in range(n_obs):
            r_t[t] = np.eye(k)
        return r_t

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Starting parameter values.

        C: Cholesky of (sample_covariance * 0.05)
        A: diag(0.2)
        B: diag(0.8)
        """
        sample_cov = np.cov(self.endog.T)
        try:
            c_mat = np.linalg.cholesky(sample_cov * 0.05)
        except np.linalg.LinAlgError:
            c_mat = np.eye(self.k) * np.sqrt(0.05 * np.mean(np.diag(sample_cov)))

        a_mat = np.eye(self.k) * 0.2
        b_mat = np.eye(self.k) * 0.8

        return self._pack_params(c_mat, a_mat, b_mat)

    @property
    def param_names(self) -> list[str]:
        """Parameter names."""
        k = self.k
        names: list[str] = []

        # C params
        for i in range(k):
            for j in range(i + 1):
                names.append(f"C[{i},{j}]")

        # A params
        if self.variant == "diagonal":
            for i in range(k):
                names.append(f"A[{i},{i}]")
        else:
            for i in range(k):
                for j in range(k):
                    names.append(f"A[{i},{j}]")

        # B params
        if self.variant == "diagonal":
            for i in range(k):
                names.append(f"B[{i},{i}]")
        else:
            for i in range(k):
                for j in range(k):
                    names.append(f"B[{i},{j}]")

        return names

    def fit(self, method: str = "mle", disp: bool = True) -> MultivarResults:
        """Fit the BEKK-GARCH model via full MLE.

        Parameters
        ----------
        method : str
            Estimation method. Only 'mle' supported for BEKK.
        disp : bool
            Display optimization progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative log-likelihood for BEKK optimization."""
            c_mat, a_mat, b_mat = self._unpack_params(params)
            h_t = self._bekk_recursion(c_mat, a_mat, b_mat, resids)

            n_obs, k = resids.shape
            ll = 0.0
            const = k * np.log(2.0 * np.pi)

            for t in range(n_obs):
                if not is_positive_definite(h_t[t]):
                    return 1e10
                try:
                    sign, logdet = np.linalg.slogdet(h_t[t])
                    if sign <= 0:
                        return 1e10
                    eps = resids[t : t + 1].T  # (k, 1)
                    h_inv_eps = np.linalg.solve(h_t[t], eps)
                    quad = float((eps.T @ h_inv_eps).item())
                    ll += -0.5 * (const + logdet + quad)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            options={"maxiter": 1000, "disp": disp, "ftol": 1e-8},
        )

        opt_params = result.x
        c_mat, a_mat, b_mat = self._unpack_params(opt_params)
        h_t = self._bekk_recursion(c_mat, a_mat, b_mat, resids)

        # Derive r_t from h_t
        r_t = np.zeros_like(h_t)
        cond_vol = np.zeros((self.T, self.k))
        for t in range(self.T):
            d = np.sqrt(np.diag(h_t[t]))
            d = np.maximum(d, 1e-12)
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        loglike = -result.fun

        n_params = len(opt_params)
        aic = -2.0 * loglike + 2.0 * n_params
        bic = -2.0 * loglike + np.log(self.T) * n_params

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=[],  # BEKK does not use univariate step
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
        )

    def forecast(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using BEKK dynamics.

        H_{T+h} converges to unconditional covariance H_bar.

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
        c_mat, a_mat, b_mat = self._unpack_params(results.params)
        cc = c_mat @ c_mat.T

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        # For forecast, use E[eps*eps'] = H_T (last estimated)
        h_prev = results.dynamic_covariance[-1].copy()

        for h in range(horizon):
            # E[H_{T+h}] = cc + a_mat' H_{T+h-1} a_mat + b_mat' H_{T+h-1} b_mat
            h_next = cc + a_mat.T @ h_prev @ a_mat + b_mat.T @ h_prev @ b_mat
            h_next = (h_next + h_next.T) / 2.0
            h_forecast[h] = h_next

            # Derive R from H
            d = np.sqrt(np.diag(h_next))
            d = np.maximum(d, 1e-12)
            r_forecast[h] = h_next / np.outer(d, d)

            h_prev = h_next

        return {"covariance": h_forecast, "correlation": r_forecast}
