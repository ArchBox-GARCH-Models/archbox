"""GO-GARCH: Generalized Orthogonal GARCH (van der Weide, 2002).

eps_t = Z * f_t
f_{i,t} ~ GARCH(1,1) (independent factors)
H_t = Z * diag(h_{1,t}, ..., h_{m,t}) * Z' + diag(psi)

The factor extraction is pure numpy: a PCA whitening via the eigendecomposition
of the sample covariance, followed by a small symmetric FastICA rotation. No
scikit-learn dependency, and the result is reproducible from an explicit seed.
"""

from __future__ import annotations

import warnings
from collections.abc import Callable
from typing import Any

import numpy as np
from numpy.typing import NDArray

from archbox.core.exceptions import ConvergenceWarning
from archbox.multivariate.base import MultivariateVolatilityModel
from archbox.multivariate.results import MultivarResults
from archbox.multivariate.utils import cov_to_corr


def pca_whiten(
    data: NDArray[np.float64],
    n_components: int,
) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    """Whiten (already demeaned) data with a PCA eigendecomposition.

    Parameters
    ----------
    data : ndarray
        Demeaned data (T, k).
    n_components : int
        Number of principal components to retain, ``1 <= m <= k``.

    Returns
    -------
    tuple[ndarray, ndarray, ndarray]
        ``(whitened, whitening, dewhitening)`` where ``whitened`` is (T, m) with
        identity sample covariance, ``whitening`` is (m, k) with
        ``whitened = data @ whitening.T`` and ``dewhitening`` is (k, m) with
        ``data ~ whitened @ dewhitening.T``.
    """
    n_obs = data.shape[0]
    cov = data.T @ data / n_obs
    eigvals, eigvecs = np.linalg.eigh(cov)  # ascending
    order = np.argsort(eigvals)[::-1][:n_components]
    lam = np.maximum(eigvals[order], 1e-16)
    vecs = eigvecs[:, order]  # (k, m)

    whitening = (vecs / np.sqrt(lam)).T  # (m, k)
    dewhitening = vecs * np.sqrt(lam)  # (k, m)
    whitened = data @ whitening.T  # (T, m)
    return whitened, whitening, dewhitening


def fast_ica(
    whitened: NDArray[np.float64],
    seed: int = 0,
    max_iter: int = 500,
    tol: float = 1e-6,
) -> tuple[NDArray[np.float64], bool]:
    """Symmetric FastICA (logcosh contrast) on whitened data, in numpy.

    Parameters
    ----------
    whitened : ndarray
        Whitened data (T, m) with identity sample covariance.
    seed : int
        Seed for the random orthogonal initialization; makes the result
        reproducible.
    max_iter : int
        Maximum number of fixed-point iterations.
    tol : float
        Convergence tolerance on the rotation.

    Returns
    -------
    tuple[ndarray, bool]
        ``(rotation, converged)`` where ``rotation`` is an orthogonal (m, m)
        matrix such that ``sources = whitened @ rotation.T`` are maximally
        non-Gaussian (and remain uncorrelated with unit variance).
    """
    x = np.asarray(whitened, dtype=np.float64).T  # (m, T)
    m, n_obs = x.shape

    def symmetric_decorrelation(w: NDArray[np.float64]) -> NDArray[np.float64]:
        """Return (W W')^{-1/2} W, the nearest orthogonal matrix to W."""
        eigvals, eigvecs = np.linalg.eigh(w @ w.T)
        eigvals = np.maximum(eigvals, 1e-16)
        return eigvecs @ np.diag(1.0 / np.sqrt(eigvals)) @ eigvecs.T @ w

    rng = np.random.default_rng(seed)
    w_mat = symmetric_decorrelation(rng.standard_normal((m, m)))

    converged = False
    for _ in range(max_iter):
        wx = w_mat @ x  # (m, T)
        g = np.tanh(wx)
        g_prime = 1.0 - g**2
        w_new = (g @ x.T) / n_obs - np.mean(g_prime, axis=1)[:, None] * w_mat
        w_new = symmetric_decorrelation(w_new)
        delta = float(np.max(np.abs(np.abs(np.sum(w_new * w_mat, axis=1)) - 1.0)))
        w_mat = w_new
        if delta < tol:
            converged = True
            break

    return w_mat, converged


class GOGARCH(MultivariateVolatilityModel):
    """Generalized Orthogonal GARCH model.

    GO-GARCH extracts independent factors (PCA whitening followed by FastICA),
    fits a univariate GARCH to each factor, and reconstructs

        H_t = Z diag(h_{1,t}, ..., h_{m,t}) Z' + diag(psi)

    where ``psi`` is the idiosyncratic variance left over when fewer than ``k``
    components are retained (it is numerically zero when ``m == k``).

    Parameters
    ----------
    endog : array-like
        Array or DataFrame of shape (T, k) with k return series.
    n_components : int or None
        Number of independent components m. Default None (= k). Values below k
        give a reduced-rank factor structure plus idiosyncratic variances.
    univariate_model : str or type or callable
        Univariate volatility model for the factors. Default 'GARCH'.
    univariate_order : tuple[int, int]
        (p, q) order for the univariate model. Default (1, 1).
    univariate_dist : str
        Conditional distribution of the factor models. Default 'normal'.
    seed : int
        Seed for the FastICA initialization; results are deterministic given it.

    Examples
    --------
    >>> import numpy as np
    >>> from archbox.multivariate.gogarch import GOGARCH
    >>> returns = np.random.randn(500, 3) * 0.01
    >>> model = GOGARCH(returns)
    >>> results = model.fit()
    >>> print(results.summary())

    References
    ----------
    van der Weide, R. (2002). GO-GARCH: A Multivariate Generalized Orthogonal
    GARCH Model. Journal of Applied Econometrics, 17(5), 549-564.
    """

    model_name: str = "GO-GARCH"

    def __init__(
        self,
        endog: Any,
        n_components: int | None = None,
        univariate_model: str | type | Callable[..., Any] = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
        univariate_dist: str = "normal",
        seed: int = 0,
    ) -> None:
        """Initialize GO-GARCH model with options."""
        super().__init__(endog, univariate_model, univariate_order, univariate_dist)
        m = self.k if n_components is None else int(n_components)
        if not 1 <= m <= self.k:
            msg = f"n_components must be in [1, {self.k}], got {n_components}"
            raise ValueError(msg)
        self.n_components = m
        self.seed = int(seed)
        self._mixing_matrix: NDArray[np.float64] | None = None
        self._factors: NDArray[np.float64] | None = None
        self._idiosyncratic: NDArray[np.float64] | None = None
        self._mu: NDArray[np.float64] | None = None

    def _correlation_recursion(
        self,
        params: NDArray[np.float64],  # noqa: ARG002
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Not used for GO-GARCH: H_t is modelled directly, not R_t.

        Parameters
        ----------
        params : ndarray
            Empty (no correlation params for GO-GARCH).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Identity correlation matrices, shape (T, k, k).
        """
        n_obs, k = std_resids.shape
        return np.broadcast_to(np.eye(k), (n_obs, k, k)).copy()

    @property
    def start_params(self) -> NDArray[np.float64]:
        """No separate correlation parameters for GO-GARCH."""
        return np.array([], dtype=np.float64)

    @property
    def param_names(self) -> list[str]:
        """No correlation parameter names."""
        return []

    def _build_factor_model(self, series: NDArray[np.float64]) -> Any:
        """Instantiate the univariate model for one (zero-mean) factor."""
        p, q = self.univariate_order
        factory = self._univariate_factory
        try:
            return factory(series, p=p, q=q, mean="zero", dist=self.univariate_dist)
        except TypeError:
            return factory(series)

    def fit(self, method: str = "two_step", disp: bool = True) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Demean the returns and whiten them with a PCA eigendecomposition.
        2. Rotate to independent components with a numpy FastICA.
        3. Fit a univariate GARCH to each factor.
        4. Reconstruct H_t = Z diag(h_t) Z' + diag(psi).

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress (unused; the factor fits are silent).

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        self._check_method(method)
        del disp

        m = self.n_components

        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu
        self._mu = mu

        # Steps 1-2: PCA whitening + FastICA rotation (numpy only).
        whitened, _whitening, dewhitening = pca_whiten(resids, m)
        rotation, ica_converged = fast_ica(whitened, seed=self.seed)
        if not ica_converged:
            warnings.warn(
                f"{self.model_name}: FastICA did not converge within the iteration "
                "limit; the factor rotation may be unreliable.",
                ConvergenceWarning,
                stacklevel=2,
            )

        factors = whitened @ rotation.T  # (T, m), uncorrelated, unit variance
        mix_mat = dewhitening @ rotation.T  # (k, m), eps_t = Z f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Idiosyncratic variance: the part of the returns the retained factors
        # do not span. Zero (to machine precision) when m == k, and what keeps
        # H_t positive definite when m < k.
        residual = resids - factors @ mix_mat.T
        psi = np.maximum(np.var(residual, axis=0), 0.0)
        floor = 1e-12 * float(np.mean(np.var(resids, axis=0)))
        psi = np.maximum(psi, floor)
        self._idiosyncratic = psi

        # Step 3: fit a univariate model to each factor.
        factor_results: list[Any] = []
        factor_variances = np.zeros((self.T, m))
        converged = ica_converged
        for i in range(m):
            model = self._build_factor_model(factors[:, i])
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = np.asarray(res.conditional_volatility, dtype=np.float64) ** 2
            converged = converged and bool(getattr(res, "convergence", True))

        # Step 4: reconstruct H_t (vectorised over t).
        h_t = np.einsum("ki,ti,li->tkl", mix_mat, factor_variances, mix_mat)
        h_t = 0.5 * (h_t + np.transpose(h_t, (0, 2, 1)))
        h_t[:, np.arange(self.k), np.arange(self.k)] += psi

        cond_vol = np.sqrt(np.maximum(np.diagonal(h_t, axis1=1, axis2=2), 1e-24))
        r_t = cov_to_corr(h_t)
        std_resids = resids / cond_vol

        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Parameter count: k mean parameters, the k*m free mixing coefficients,
        # and the factor GARCH parameters.
        n_params = self.k + self.k * m + sum(len(r.params) for r in factor_results)
        aic = -2.0 * loglike + 2.0 * n_params
        bic = -2.0 * loglike + np.log(self.T) * n_params

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=factor_results,
            params=np.array([], dtype=np.float64),
            dynamic_correlation=r_t,
            dynamic_covariance=h_t,
            conditional_volatility=cond_vol,
            std_resids=std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
            param_names=[],
            std_errors=np.zeros(0),
            converged=converged,
            series_names=self.series_names,
            index=self.index,
            extras={
                "mixing_matrix": mix_mat,
                "idiosyncratic": psi,
                "mu": mu,
                "n_components": m,
            },
        )

    @property
    def mixing_matrix(self) -> NDArray[np.float64] | None:
        """Return the mixing matrix Z, shape (k, n_components)."""
        return self._mixing_matrix

    @property
    def factors(self) -> NDArray[np.float64] | None:
        """Return the independent factors, shape (T, n_components)."""
        return self._factors

    @property
    def idiosyncratic_variance(self) -> NDArray[np.float64] | None:
        """Return the idiosyncratic variances psi, shape (k,)."""
        return self._idiosyncratic

    def forecast(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using the GO-GARCH structure.

        H_{T+h} = Z diag(h_{1,T+h}, ..., h_{m,T+h}) Z' + diag(psi), with each
        factor variance taken from its univariate ``ArchResults.forecast``.

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

        mix_mat = np.asarray(results.extras["mixing_matrix"], dtype=np.float64)
        psi = np.asarray(results.extras["idiosyncratic"], dtype=np.float64)
        m = mix_mat.shape[1]

        factor_var = np.zeros((horizon, m))
        for i, res in enumerate(results.univariate_results[:m]):
            fc = res.forecast(horizon=horizon)
            variance = np.asarray(fc["variance"], dtype=np.float64).ravel()
            if variance.size >= horizon and np.all(np.isfinite(variance[:horizon])):
                factor_var[:, i] = np.maximum(variance[:horizon], 0.0)
            else:  # pragma: no cover - defensive
                factor_var[:, i] = float(res.conditional_volatility[-1] ** 2)

        h_forecast = np.einsum("ki,hi,li->hkl", mix_mat, factor_var, mix_mat)
        h_forecast = 0.5 * (h_forecast + np.transpose(h_forecast, (0, 2, 1)))
        h_forecast[:, np.arange(self.k), np.arange(self.k)] += psi
        r_forecast = cov_to_corr(h_forecast)

        return {"covariance": h_forecast, "correlation": r_forecast}
