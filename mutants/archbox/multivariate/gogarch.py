"""GO-GARCH: Generalized Orthogonal GARCH (van der Weide, 2002).

eps_t = Z * f_t
f_{i,t} ~ GARCH(1,1) (independent factors)
H_t = Z * diag(h_{1,t}, ..., h_{k,t}) * Z'
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Annotated, Any, ClassVar

import numpy as np
from numpy.typing import NDArray

from archbox.multivariate.base import MultivariateVolatilityModel, MultivarResults

MutantDict = Annotated[dict[str, Callable], "Mutant"]  # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):  # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os  # type: ignore

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]  # type: ignore
    if mutant_under_test == "fail":  # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException  # type: ignore

        raise MutmutProgrammaticFailException("Failed programmatically")  # type: ignore
    elif mutant_under_test == "stats":  # type: ignore
        from mutmut.__main__ import record_trampoline_hit  # type: ignore

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)  # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs)  # type: ignore
        return result  # type: ignore
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"  # type: ignore
    if not mutant_under_test.startswith(prefix):  # type: ignore
        result = orig(*call_args, **call_kwargs)  # type: ignore
        return result  # type: ignore
    mutant_name = mutant_under_test.rpartition(".")[-1]  # type: ignore
    if self_arg is not None:  # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)  # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)  # type: ignore
    return result  # type: ignore


class GOGARCH(MultivariateVolatilityModel):
    """Generalized Orthogonal GARCH model.

    GO-GARCH uses ICA to find independent factors, then fits univariate
    GARCH on each factor. The covariance is reconstructed as:
        H_t = Z * diag(h_{1,t}, ..., h_{k,t}) * Z'

    Parameters
    ----------
    endog : ndarray
        Array of shape (T, k) with k return series.
    n_components : int or None
        Number of ICA components. Default None (= k).
    univariate_model : str
        Univariate GARCH variant for factors. Default 'GARCH'.
    univariate_order : tuple[int, int]
        (p, q) order for univariate GARCH. Default (1, 1).

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
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        args = [endog, n_components, univariate_model, univariate_order]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGOGARCHǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁGOGARCHǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGOGARCHǁ__init____mutmut_orig(
        self,
        endog: Any,
        n_components: int | None = None,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize GO-GARCH model with options."""
        super().__init__(endog, univariate_model, univariate_order)
        self.n_components = n_components or self.k
        self._mixing_matrix: NDArray[np.float64] | None = None
        self._factors: NDArray[np.float64] | None = None

    def xǁGOGARCHǁ__init____mutmut_1(
        self,
        endog: Any,
        n_components: int | None = None,
        univariate_model: str = "XXGARCHXX",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize GO-GARCH model with options."""
        super().__init__(endog, univariate_model, univariate_order)
        self.n_components = n_components or self.k
        self._mixing_matrix: NDArray[np.float64] | None = None
        self._factors: NDArray[np.float64] | None = None

    def xǁGOGARCHǁ__init____mutmut_2(
        self,
        endog: Any,
        n_components: int | None = None,
        univariate_model: str = "garch",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize GO-GARCH model with options."""
        super().__init__(endog, univariate_model, univariate_order)
        self.n_components = n_components or self.k
        self._mixing_matrix: NDArray[np.float64] | None = None
        self._factors: NDArray[np.float64] | None = None

    def xǁGOGARCHǁ__init____mutmut_3(
        self,
        endog: Any,
        n_components: int | None = None,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize GO-GARCH model with options."""
        super().__init__(None, univariate_model, univariate_order)
        self.n_components = n_components or self.k
        self._mixing_matrix: NDArray[np.float64] | None = None
        self._factors: NDArray[np.float64] | None = None

    def xǁGOGARCHǁ__init____mutmut_4(
        self,
        endog: Any,
        n_components: int | None = None,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize GO-GARCH model with options."""
        super().__init__(endog, None, univariate_order)
        self.n_components = n_components or self.k
        self._mixing_matrix: NDArray[np.float64] | None = None
        self._factors: NDArray[np.float64] | None = None

    def xǁGOGARCHǁ__init____mutmut_5(
        self,
        endog: Any,
        n_components: int | None = None,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize GO-GARCH model with options."""
        super().__init__(endog, univariate_model, None)
        self.n_components = n_components or self.k
        self._mixing_matrix: NDArray[np.float64] | None = None
        self._factors: NDArray[np.float64] | None = None

    def xǁGOGARCHǁ__init____mutmut_6(
        self,
        endog: Any,
        n_components: int | None = None,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize GO-GARCH model with options."""
        super().__init__(univariate_model, univariate_order)
        self.n_components = n_components or self.k
        self._mixing_matrix: NDArray[np.float64] | None = None
        self._factors: NDArray[np.float64] | None = None

    def xǁGOGARCHǁ__init____mutmut_7(
        self,
        endog: Any,
        n_components: int | None = None,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize GO-GARCH model with options."""
        super().__init__(endog, univariate_order)
        self.n_components = n_components or self.k
        self._mixing_matrix: NDArray[np.float64] | None = None
        self._factors: NDArray[np.float64] | None = None

    def xǁGOGARCHǁ__init____mutmut_8(
        self,
        endog: Any,
        n_components: int | None = None,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize GO-GARCH model with options."""
        super().__init__(
            endog,
            univariate_model,
        )
        self.n_components = n_components or self.k
        self._mixing_matrix: NDArray[np.float64] | None = None
        self._factors: NDArray[np.float64] | None = None

    def xǁGOGARCHǁ__init____mutmut_9(
        self,
        endog: Any,
        n_components: int | None = None,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize GO-GARCH model with options."""
        super().__init__(endog, univariate_model, univariate_order)
        self.n_components = None
        self._mixing_matrix: NDArray[np.float64] | None = None
        self._factors: NDArray[np.float64] | None = None

    def xǁGOGARCHǁ__init____mutmut_10(
        self,
        endog: Any,
        n_components: int | None = None,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize GO-GARCH model with options."""
        super().__init__(endog, univariate_model, univariate_order)
        self.n_components = n_components and self.k
        self._mixing_matrix: NDArray[np.float64] | None = None
        self._factors: NDArray[np.float64] | None = None

    def xǁGOGARCHǁ__init____mutmut_11(
        self,
        endog: Any,
        n_components: int | None = None,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize GO-GARCH model with options."""
        super().__init__(endog, univariate_model, univariate_order)
        self.n_components = n_components or self.k
        self._mixing_matrix: NDArray[np.float64] | None = ""
        self._factors: NDArray[np.float64] | None = None

    def xǁGOGARCHǁ__init____mutmut_12(
        self,
        endog: Any,
        n_components: int | None = None,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize GO-GARCH model with options."""
        super().__init__(endog, univariate_model, univariate_order)
        self.n_components = n_components or self.k
        self._mixing_matrix: NDArray[np.float64] | None = None
        self._factors: NDArray[np.float64] | None = ""

    xǁGOGARCHǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGOGARCHǁ__init____mutmut_1": xǁGOGARCHǁ__init____mutmut_1,
        "xǁGOGARCHǁ__init____mutmut_2": xǁGOGARCHǁ__init____mutmut_2,
        "xǁGOGARCHǁ__init____mutmut_3": xǁGOGARCHǁ__init____mutmut_3,
        "xǁGOGARCHǁ__init____mutmut_4": xǁGOGARCHǁ__init____mutmut_4,
        "xǁGOGARCHǁ__init____mutmut_5": xǁGOGARCHǁ__init____mutmut_5,
        "xǁGOGARCHǁ__init____mutmut_6": xǁGOGARCHǁ__init____mutmut_6,
        "xǁGOGARCHǁ__init____mutmut_7": xǁGOGARCHǁ__init____mutmut_7,
        "xǁGOGARCHǁ__init____mutmut_8": xǁGOGARCHǁ__init____mutmut_8,
        "xǁGOGARCHǁ__init____mutmut_9": xǁGOGARCHǁ__init____mutmut_9,
        "xǁGOGARCHǁ__init____mutmut_10": xǁGOGARCHǁ__init____mutmut_10,
        "xǁGOGARCHǁ__init____mutmut_11": xǁGOGARCHǁ__init____mutmut_11,
        "xǁGOGARCHǁ__init____mutmut_12": xǁGOGARCHǁ__init____mutmut_12,
    }
    xǁGOGARCHǁ__init____mutmut_orig.__name__ = "xǁGOGARCHǁ__init__"

    def _correlation_recursion(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        args = [params, std_resids]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGOGARCHǁ_correlation_recursion__mutmut_orig"),
            object.__getattribute__(self, "xǁGOGARCHǁ_correlation_recursion__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGOGARCHǁ_correlation_recursion__mutmut_orig(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Not directly used for GO-GARCH (correlation derived from H_t).

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
        r_mat = np.zeros((n_obs, k, k))
        for t in range(n_obs):
            r_mat[t] = np.eye(k)
        return r_mat

    def xǁGOGARCHǁ_correlation_recursion__mutmut_1(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Not directly used for GO-GARCH (correlation derived from H_t).

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
        n_obs, k = None
        r_mat = np.zeros((n_obs, k, k))
        for t in range(n_obs):
            r_mat[t] = np.eye(k)
        return r_mat

    def xǁGOGARCHǁ_correlation_recursion__mutmut_2(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Not directly used for GO-GARCH (correlation derived from H_t).

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
        r_mat = None
        for t in range(n_obs):
            r_mat[t] = np.eye(k)
        return r_mat

    def xǁGOGARCHǁ_correlation_recursion__mutmut_3(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Not directly used for GO-GARCH (correlation derived from H_t).

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
        r_mat = np.zeros(None)
        for t in range(n_obs):
            r_mat[t] = np.eye(k)
        return r_mat

    def xǁGOGARCHǁ_correlation_recursion__mutmut_4(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Not directly used for GO-GARCH (correlation derived from H_t).

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
        r_mat = np.zeros((n_obs, k, k))
        for t in range(None):
            r_mat[t] = np.eye(k)
        return r_mat

    def xǁGOGARCHǁ_correlation_recursion__mutmut_5(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Not directly used for GO-GARCH (correlation derived from H_t).

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
        r_mat = np.zeros((n_obs, k, k))
        for t in range(n_obs):
            r_mat[t] = None
        return r_mat

    def xǁGOGARCHǁ_correlation_recursion__mutmut_6(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Not directly used for GO-GARCH (correlation derived from H_t).

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
        r_mat = np.zeros((n_obs, k, k))
        for t in range(n_obs):
            r_mat[t] = np.eye(None)
        return r_mat

    xǁGOGARCHǁ_correlation_recursion__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGOGARCHǁ_correlation_recursion__mutmut_1": xǁGOGARCHǁ_correlation_recursion__mutmut_1,
        "xǁGOGARCHǁ_correlation_recursion__mutmut_2": xǁGOGARCHǁ_correlation_recursion__mutmut_2,
        "xǁGOGARCHǁ_correlation_recursion__mutmut_3": xǁGOGARCHǁ_correlation_recursion__mutmut_3,
        "xǁGOGARCHǁ_correlation_recursion__mutmut_4": xǁGOGARCHǁ_correlation_recursion__mutmut_4,
        "xǁGOGARCHǁ_correlation_recursion__mutmut_5": xǁGOGARCHǁ_correlation_recursion__mutmut_5,
        "xǁGOGARCHǁ_correlation_recursion__mutmut_6": xǁGOGARCHǁ_correlation_recursion__mutmut_6,
    }
    xǁGOGARCHǁ_correlation_recursion__mutmut_orig.__name__ = "xǁGOGARCHǁ_correlation_recursion"

    @property
    def start_params(self) -> NDArray[np.float64]:
        """No separate correlation parameters for GO-GARCH."""
        return np.array([], dtype=np.float64)

    @property
    def param_names(self) -> list[str]:
        """No correlation parameter names."""
        return []

    def fit(self, method: str = "two_step", disp: bool = True) -> MultivarResults:
        args = [method, disp]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGOGARCHǁfit__mutmut_orig"),
            object.__getattribute__(self, "xǁGOGARCHǁfit__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGOGARCHǁfit__mutmut_orig(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_1(
        self, method: str = "XXtwo_stepXX", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_2(
        self, method: str = "TWO_STEP", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_3(
        self, method: str = "two_step", disp: bool = False
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_4(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = None
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_5(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(None, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_6(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=None)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_7(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_8(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(
            self.endog,
        )
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_9(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=1)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_10(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = None

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_11(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog + mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_12(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = None
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_13(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=None,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_14(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=None,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_15(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=None,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_16(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=None,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_17(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_18(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_19(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_20(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_21(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=43,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_22(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=501,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_23(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1.0001,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_24(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = None  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_25(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            None, dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_26(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=None
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_27(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(dtype=np.float64)  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_28(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids),
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_29(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(None), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_30(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = None  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_31(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            None, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_32(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=None
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_33(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_34(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_,
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_35(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = None
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_36(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = None

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_37(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = None
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_38(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = None
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_39(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = None

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_40(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros(None)

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_41(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(None):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_42(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = None
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_43(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = None
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_44(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(None, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_45(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=None, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_46(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=None, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_47(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean=None)
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_48(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_49(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_50(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_51(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(
                factor_series,
                p=p,
                q=q,
            )
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_52(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="XXzeroXX")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_53(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="ZERO")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_54(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = None
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_55(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=None)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_56(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=True)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_57(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(None)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_58(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = None

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_59(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility * 2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_60(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**3

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_61(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = None
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_62(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros(None)
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_63(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = None
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_64(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros(None)
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_65(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = None

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_66(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros(None)

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_67(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(None):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_68(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = None
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_69(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(None)
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_70(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = None
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_71(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = None  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_72(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) * 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_73(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] - h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_74(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 3.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_75(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = None
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_76(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(None)
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_77(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(None, 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_78(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), None))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_79(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_80(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(
                np.maximum(
                    np.diag(h_t[t]),
                )
            )
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_81(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(None), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_82(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1.000000000001))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_83(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = None
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_84(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = None

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_85(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] * np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_86(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(None, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_87(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, None)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_88(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_89(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(
                d,
            )

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_90(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = None
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_91(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros(None)
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_92(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(None):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_93(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = None

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_94(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] * cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_95(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = None

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_96(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(None, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_97(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, None, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_98(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, None)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_99(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_100(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_101(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(
            r_t,
            std_resids,
        )

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_102(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = None
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_103(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(None)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_104(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = None

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_105(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = None
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_106(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike - 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_107(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 / loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_108(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = +2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_109(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -3.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_110(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 / n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_111(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 3.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_112(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = None

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
        )

    def xǁGOGARCHǁfit__mutmut_113(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike - np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_114(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 / loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_115(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = +2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_116(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -3.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_117(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) / n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_118(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(None) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_119(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = None

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
        )

    def xǁGOGARCHǁfit__mutmut_120(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = False

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
        )

    def xǁGOGARCHǁfit__mutmut_121(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=None,
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
        )

    def xǁGOGARCHǁfit__mutmut_122(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=None,
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
        )

    def xǁGOGARCHǁfit__mutmut_123(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=factor_results,
            params=None,
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

    def xǁGOGARCHǁfit__mutmut_124(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=factor_results,
            params=np.array([], dtype=np.float64),
            dynamic_correlation=None,
            dynamic_covariance=h_t,
            conditional_volatility=cond_vol,
            std_resids=std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁGOGARCHǁfit__mutmut_125(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=factor_results,
            params=np.array([], dtype=np.float64),
            dynamic_correlation=r_t,
            dynamic_covariance=None,
            conditional_volatility=cond_vol,
            std_resids=std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁGOGARCHǁfit__mutmut_126(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=factor_results,
            params=np.array([], dtype=np.float64),
            dynamic_correlation=r_t,
            dynamic_covariance=h_t,
            conditional_volatility=None,
            std_resids=std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁGOGARCHǁfit__mutmut_127(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=factor_results,
            params=np.array([], dtype=np.float64),
            dynamic_correlation=r_t,
            dynamic_covariance=h_t,
            conditional_volatility=cond_vol,
            std_resids=None,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁGOGARCHǁfit__mutmut_128(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=factor_results,
            params=np.array([], dtype=np.float64),
            dynamic_correlation=r_t,
            dynamic_covariance=h_t,
            conditional_volatility=cond_vol,
            std_resids=std_resids,
            loglike=None,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁGOGARCHǁfit__mutmut_129(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
            aic=None,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁGOGARCHǁfit__mutmut_130(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
            bic=None,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁGOGARCHǁfit__mutmut_131(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
            n_obs=None,
            n_series=self.k,
        )

    def xǁGOGARCHǁfit__mutmut_132(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
            n_series=None,
        )

    def xǁGOGARCHǁfit__mutmut_133(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
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
        )

    def xǁGOGARCHǁfit__mutmut_134(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
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
        )

    def xǁGOGARCHǁfit__mutmut_135(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=factor_results,
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

    def xǁGOGARCHǁfit__mutmut_136(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=factor_results,
            params=np.array([], dtype=np.float64),
            dynamic_covariance=h_t,
            conditional_volatility=cond_vol,
            std_resids=std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁGOGARCHǁfit__mutmut_137(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=factor_results,
            params=np.array([], dtype=np.float64),
            dynamic_correlation=r_t,
            conditional_volatility=cond_vol,
            std_resids=std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁGOGARCHǁfit__mutmut_138(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=factor_results,
            params=np.array([], dtype=np.float64),
            dynamic_correlation=r_t,
            dynamic_covariance=h_t,
            std_resids=std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁGOGARCHǁfit__mutmut_139(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=factor_results,
            params=np.array([], dtype=np.float64),
            dynamic_correlation=r_t,
            dynamic_covariance=h_t,
            conditional_volatility=cond_vol,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁGOGARCHǁfit__mutmut_140(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=factor_results,
            params=np.array([], dtype=np.float64),
            dynamic_correlation=r_t,
            dynamic_covariance=h_t,
            conditional_volatility=cond_vol,
            std_resids=std_resids,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁGOGARCHǁfit__mutmut_141(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁGOGARCHǁfit__mutmut_142(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁGOGARCHǁfit__mutmut_143(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
            n_series=self.k,
        )

    def xǁGOGARCHǁfit__mutmut_144(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁGOGARCHǁfit__mutmut_145(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=factor_results,
            params=np.array(None, dtype=np.float64),
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

    def xǁGOGARCHǁfit__mutmut_146(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=factor_results,
            params=np.array([], dtype=None),
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

    def xǁGOGARCHǁfit__mutmut_147(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=factor_results,
            params=np.array(dtype=np.float64),
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

    def xǁGOGARCHǁfit__mutmut_148(
        self, method: str = "two_step", disp: bool = True
    ) -> MultivarResults:
        """Fit the GO-GARCH model.

        Steps:
        1. Estimate mixing matrix Z via ICA (FastICA)
        2. Compute factors f_t = Z^{-1} * eps_t
        3. Fit univariate GARCH on each factor
        4. Reconstruct H_t = Z * diag(h_t) * Z'

        Parameters
        ----------
        method : str
            Estimation method. Default 'two_step'.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        from sklearn.decomposition import FastICA

        from archbox.models.garch import GARCH

        # Demean returns
        mu = np.mean(self.endog, axis=0)
        resids = self.endog - mu

        # Step 1: ICA to find mixing matrix Z
        ica = FastICA(
            n_components=self.n_components,
            random_state=42,
            max_iter=500,
            tol=1e-4,
        )
        factors: NDArray[np.float64] = np.asarray(
            ica.fit_transform(resids), dtype=np.float64
        )  # (T, k) - independent factors
        mix_mat: NDArray[np.float64] = np.asarray(
            ica.mixing_, dtype=np.float64
        )  # (k, k) - mixing matrix: eps_t = Z * f_t

        self._mixing_matrix = mix_mat
        self._factors = factors

        # Step 2: Fit univariate GARCH on each factor
        p, q = self.univariate_order
        factor_results = []
        factor_variances = np.zeros((self.T, self.k))

        for i in range(self.k):
            factor_series: NDArray[np.float64] = factors[:, i]
            model = GARCH(factor_series, p=p, q=q, mean="zero")
            res = model.fit(disp=False)
            factor_results.append(res)
            factor_variances[:, i] = res.conditional_volatility**2

        # Step 3: Reconstruct H_t = Z * diag(h_t) * Z'
        h_t = np.zeros((self.T, self.k, self.k))
        r_t = np.zeros((self.T, self.k, self.k))
        cond_vol = np.zeros((self.T, self.k))

        for t in range(self.T):
            d_f = np.diag(factor_variances[t])
            h_t[t] = mix_mat @ d_f @ mix_mat.T
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0  # Ensure symmetry

            # Derive R_t and volatilities from H_t
            d = np.sqrt(np.maximum(np.diag(h_t[t]), 1e-12))
            cond_vol[t] = d
            r_t[t] = h_t[t] / np.outer(d, d)

        # Compute standardized residuals
        std_resids = np.zeros((self.T, self.k))
        for t in range(self.T):
            std_resids[t] = resids[t] / cond_vol[t]

        # Compute log-likelihood
        loglike = self._loglikelihood(r_t, std_resids, cond_vol)

        # Count parameters: k GARCH models (each ~3 params)
        n_univ_params = sum(len(r.params) for r in factor_results)
        n_total = n_univ_params

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=factor_results,
            params=np.array(
                [],
            ),
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

    xǁGOGARCHǁfit__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGOGARCHǁfit__mutmut_1": xǁGOGARCHǁfit__mutmut_1,
        "xǁGOGARCHǁfit__mutmut_2": xǁGOGARCHǁfit__mutmut_2,
        "xǁGOGARCHǁfit__mutmut_3": xǁGOGARCHǁfit__mutmut_3,
        "xǁGOGARCHǁfit__mutmut_4": xǁGOGARCHǁfit__mutmut_4,
        "xǁGOGARCHǁfit__mutmut_5": xǁGOGARCHǁfit__mutmut_5,
        "xǁGOGARCHǁfit__mutmut_6": xǁGOGARCHǁfit__mutmut_6,
        "xǁGOGARCHǁfit__mutmut_7": xǁGOGARCHǁfit__mutmut_7,
        "xǁGOGARCHǁfit__mutmut_8": xǁGOGARCHǁfit__mutmut_8,
        "xǁGOGARCHǁfit__mutmut_9": xǁGOGARCHǁfit__mutmut_9,
        "xǁGOGARCHǁfit__mutmut_10": xǁGOGARCHǁfit__mutmut_10,
        "xǁGOGARCHǁfit__mutmut_11": xǁGOGARCHǁfit__mutmut_11,
        "xǁGOGARCHǁfit__mutmut_12": xǁGOGARCHǁfit__mutmut_12,
        "xǁGOGARCHǁfit__mutmut_13": xǁGOGARCHǁfit__mutmut_13,
        "xǁGOGARCHǁfit__mutmut_14": xǁGOGARCHǁfit__mutmut_14,
        "xǁGOGARCHǁfit__mutmut_15": xǁGOGARCHǁfit__mutmut_15,
        "xǁGOGARCHǁfit__mutmut_16": xǁGOGARCHǁfit__mutmut_16,
        "xǁGOGARCHǁfit__mutmut_17": xǁGOGARCHǁfit__mutmut_17,
        "xǁGOGARCHǁfit__mutmut_18": xǁGOGARCHǁfit__mutmut_18,
        "xǁGOGARCHǁfit__mutmut_19": xǁGOGARCHǁfit__mutmut_19,
        "xǁGOGARCHǁfit__mutmut_20": xǁGOGARCHǁfit__mutmut_20,
        "xǁGOGARCHǁfit__mutmut_21": xǁGOGARCHǁfit__mutmut_21,
        "xǁGOGARCHǁfit__mutmut_22": xǁGOGARCHǁfit__mutmut_22,
        "xǁGOGARCHǁfit__mutmut_23": xǁGOGARCHǁfit__mutmut_23,
        "xǁGOGARCHǁfit__mutmut_24": xǁGOGARCHǁfit__mutmut_24,
        "xǁGOGARCHǁfit__mutmut_25": xǁGOGARCHǁfit__mutmut_25,
        "xǁGOGARCHǁfit__mutmut_26": xǁGOGARCHǁfit__mutmut_26,
        "xǁGOGARCHǁfit__mutmut_27": xǁGOGARCHǁfit__mutmut_27,
        "xǁGOGARCHǁfit__mutmut_28": xǁGOGARCHǁfit__mutmut_28,
        "xǁGOGARCHǁfit__mutmut_29": xǁGOGARCHǁfit__mutmut_29,
        "xǁGOGARCHǁfit__mutmut_30": xǁGOGARCHǁfit__mutmut_30,
        "xǁGOGARCHǁfit__mutmut_31": xǁGOGARCHǁfit__mutmut_31,
        "xǁGOGARCHǁfit__mutmut_32": xǁGOGARCHǁfit__mutmut_32,
        "xǁGOGARCHǁfit__mutmut_33": xǁGOGARCHǁfit__mutmut_33,
        "xǁGOGARCHǁfit__mutmut_34": xǁGOGARCHǁfit__mutmut_34,
        "xǁGOGARCHǁfit__mutmut_35": xǁGOGARCHǁfit__mutmut_35,
        "xǁGOGARCHǁfit__mutmut_36": xǁGOGARCHǁfit__mutmut_36,
        "xǁGOGARCHǁfit__mutmut_37": xǁGOGARCHǁfit__mutmut_37,
        "xǁGOGARCHǁfit__mutmut_38": xǁGOGARCHǁfit__mutmut_38,
        "xǁGOGARCHǁfit__mutmut_39": xǁGOGARCHǁfit__mutmut_39,
        "xǁGOGARCHǁfit__mutmut_40": xǁGOGARCHǁfit__mutmut_40,
        "xǁGOGARCHǁfit__mutmut_41": xǁGOGARCHǁfit__mutmut_41,
        "xǁGOGARCHǁfit__mutmut_42": xǁGOGARCHǁfit__mutmut_42,
        "xǁGOGARCHǁfit__mutmut_43": xǁGOGARCHǁfit__mutmut_43,
        "xǁGOGARCHǁfit__mutmut_44": xǁGOGARCHǁfit__mutmut_44,
        "xǁGOGARCHǁfit__mutmut_45": xǁGOGARCHǁfit__mutmut_45,
        "xǁGOGARCHǁfit__mutmut_46": xǁGOGARCHǁfit__mutmut_46,
        "xǁGOGARCHǁfit__mutmut_47": xǁGOGARCHǁfit__mutmut_47,
        "xǁGOGARCHǁfit__mutmut_48": xǁGOGARCHǁfit__mutmut_48,
        "xǁGOGARCHǁfit__mutmut_49": xǁGOGARCHǁfit__mutmut_49,
        "xǁGOGARCHǁfit__mutmut_50": xǁGOGARCHǁfit__mutmut_50,
        "xǁGOGARCHǁfit__mutmut_51": xǁGOGARCHǁfit__mutmut_51,
        "xǁGOGARCHǁfit__mutmut_52": xǁGOGARCHǁfit__mutmut_52,
        "xǁGOGARCHǁfit__mutmut_53": xǁGOGARCHǁfit__mutmut_53,
        "xǁGOGARCHǁfit__mutmut_54": xǁGOGARCHǁfit__mutmut_54,
        "xǁGOGARCHǁfit__mutmut_55": xǁGOGARCHǁfit__mutmut_55,
        "xǁGOGARCHǁfit__mutmut_56": xǁGOGARCHǁfit__mutmut_56,
        "xǁGOGARCHǁfit__mutmut_57": xǁGOGARCHǁfit__mutmut_57,
        "xǁGOGARCHǁfit__mutmut_58": xǁGOGARCHǁfit__mutmut_58,
        "xǁGOGARCHǁfit__mutmut_59": xǁGOGARCHǁfit__mutmut_59,
        "xǁGOGARCHǁfit__mutmut_60": xǁGOGARCHǁfit__mutmut_60,
        "xǁGOGARCHǁfit__mutmut_61": xǁGOGARCHǁfit__mutmut_61,
        "xǁGOGARCHǁfit__mutmut_62": xǁGOGARCHǁfit__mutmut_62,
        "xǁGOGARCHǁfit__mutmut_63": xǁGOGARCHǁfit__mutmut_63,
        "xǁGOGARCHǁfit__mutmut_64": xǁGOGARCHǁfit__mutmut_64,
        "xǁGOGARCHǁfit__mutmut_65": xǁGOGARCHǁfit__mutmut_65,
        "xǁGOGARCHǁfit__mutmut_66": xǁGOGARCHǁfit__mutmut_66,
        "xǁGOGARCHǁfit__mutmut_67": xǁGOGARCHǁfit__mutmut_67,
        "xǁGOGARCHǁfit__mutmut_68": xǁGOGARCHǁfit__mutmut_68,
        "xǁGOGARCHǁfit__mutmut_69": xǁGOGARCHǁfit__mutmut_69,
        "xǁGOGARCHǁfit__mutmut_70": xǁGOGARCHǁfit__mutmut_70,
        "xǁGOGARCHǁfit__mutmut_71": xǁGOGARCHǁfit__mutmut_71,
        "xǁGOGARCHǁfit__mutmut_72": xǁGOGARCHǁfit__mutmut_72,
        "xǁGOGARCHǁfit__mutmut_73": xǁGOGARCHǁfit__mutmut_73,
        "xǁGOGARCHǁfit__mutmut_74": xǁGOGARCHǁfit__mutmut_74,
        "xǁGOGARCHǁfit__mutmut_75": xǁGOGARCHǁfit__mutmut_75,
        "xǁGOGARCHǁfit__mutmut_76": xǁGOGARCHǁfit__mutmut_76,
        "xǁGOGARCHǁfit__mutmut_77": xǁGOGARCHǁfit__mutmut_77,
        "xǁGOGARCHǁfit__mutmut_78": xǁGOGARCHǁfit__mutmut_78,
        "xǁGOGARCHǁfit__mutmut_79": xǁGOGARCHǁfit__mutmut_79,
        "xǁGOGARCHǁfit__mutmut_80": xǁGOGARCHǁfit__mutmut_80,
        "xǁGOGARCHǁfit__mutmut_81": xǁGOGARCHǁfit__mutmut_81,
        "xǁGOGARCHǁfit__mutmut_82": xǁGOGARCHǁfit__mutmut_82,
        "xǁGOGARCHǁfit__mutmut_83": xǁGOGARCHǁfit__mutmut_83,
        "xǁGOGARCHǁfit__mutmut_84": xǁGOGARCHǁfit__mutmut_84,
        "xǁGOGARCHǁfit__mutmut_85": xǁGOGARCHǁfit__mutmut_85,
        "xǁGOGARCHǁfit__mutmut_86": xǁGOGARCHǁfit__mutmut_86,
        "xǁGOGARCHǁfit__mutmut_87": xǁGOGARCHǁfit__mutmut_87,
        "xǁGOGARCHǁfit__mutmut_88": xǁGOGARCHǁfit__mutmut_88,
        "xǁGOGARCHǁfit__mutmut_89": xǁGOGARCHǁfit__mutmut_89,
        "xǁGOGARCHǁfit__mutmut_90": xǁGOGARCHǁfit__mutmut_90,
        "xǁGOGARCHǁfit__mutmut_91": xǁGOGARCHǁfit__mutmut_91,
        "xǁGOGARCHǁfit__mutmut_92": xǁGOGARCHǁfit__mutmut_92,
        "xǁGOGARCHǁfit__mutmut_93": xǁGOGARCHǁfit__mutmut_93,
        "xǁGOGARCHǁfit__mutmut_94": xǁGOGARCHǁfit__mutmut_94,
        "xǁGOGARCHǁfit__mutmut_95": xǁGOGARCHǁfit__mutmut_95,
        "xǁGOGARCHǁfit__mutmut_96": xǁGOGARCHǁfit__mutmut_96,
        "xǁGOGARCHǁfit__mutmut_97": xǁGOGARCHǁfit__mutmut_97,
        "xǁGOGARCHǁfit__mutmut_98": xǁGOGARCHǁfit__mutmut_98,
        "xǁGOGARCHǁfit__mutmut_99": xǁGOGARCHǁfit__mutmut_99,
        "xǁGOGARCHǁfit__mutmut_100": xǁGOGARCHǁfit__mutmut_100,
        "xǁGOGARCHǁfit__mutmut_101": xǁGOGARCHǁfit__mutmut_101,
        "xǁGOGARCHǁfit__mutmut_102": xǁGOGARCHǁfit__mutmut_102,
        "xǁGOGARCHǁfit__mutmut_103": xǁGOGARCHǁfit__mutmut_103,
        "xǁGOGARCHǁfit__mutmut_104": xǁGOGARCHǁfit__mutmut_104,
        "xǁGOGARCHǁfit__mutmut_105": xǁGOGARCHǁfit__mutmut_105,
        "xǁGOGARCHǁfit__mutmut_106": xǁGOGARCHǁfit__mutmut_106,
        "xǁGOGARCHǁfit__mutmut_107": xǁGOGARCHǁfit__mutmut_107,
        "xǁGOGARCHǁfit__mutmut_108": xǁGOGARCHǁfit__mutmut_108,
        "xǁGOGARCHǁfit__mutmut_109": xǁGOGARCHǁfit__mutmut_109,
        "xǁGOGARCHǁfit__mutmut_110": xǁGOGARCHǁfit__mutmut_110,
        "xǁGOGARCHǁfit__mutmut_111": xǁGOGARCHǁfit__mutmut_111,
        "xǁGOGARCHǁfit__mutmut_112": xǁGOGARCHǁfit__mutmut_112,
        "xǁGOGARCHǁfit__mutmut_113": xǁGOGARCHǁfit__mutmut_113,
        "xǁGOGARCHǁfit__mutmut_114": xǁGOGARCHǁfit__mutmut_114,
        "xǁGOGARCHǁfit__mutmut_115": xǁGOGARCHǁfit__mutmut_115,
        "xǁGOGARCHǁfit__mutmut_116": xǁGOGARCHǁfit__mutmut_116,
        "xǁGOGARCHǁfit__mutmut_117": xǁGOGARCHǁfit__mutmut_117,
        "xǁGOGARCHǁfit__mutmut_118": xǁGOGARCHǁfit__mutmut_118,
        "xǁGOGARCHǁfit__mutmut_119": xǁGOGARCHǁfit__mutmut_119,
        "xǁGOGARCHǁfit__mutmut_120": xǁGOGARCHǁfit__mutmut_120,
        "xǁGOGARCHǁfit__mutmut_121": xǁGOGARCHǁfit__mutmut_121,
        "xǁGOGARCHǁfit__mutmut_122": xǁGOGARCHǁfit__mutmut_122,
        "xǁGOGARCHǁfit__mutmut_123": xǁGOGARCHǁfit__mutmut_123,
        "xǁGOGARCHǁfit__mutmut_124": xǁGOGARCHǁfit__mutmut_124,
        "xǁGOGARCHǁfit__mutmut_125": xǁGOGARCHǁfit__mutmut_125,
        "xǁGOGARCHǁfit__mutmut_126": xǁGOGARCHǁfit__mutmut_126,
        "xǁGOGARCHǁfit__mutmut_127": xǁGOGARCHǁfit__mutmut_127,
        "xǁGOGARCHǁfit__mutmut_128": xǁGOGARCHǁfit__mutmut_128,
        "xǁGOGARCHǁfit__mutmut_129": xǁGOGARCHǁfit__mutmut_129,
        "xǁGOGARCHǁfit__mutmut_130": xǁGOGARCHǁfit__mutmut_130,
        "xǁGOGARCHǁfit__mutmut_131": xǁGOGARCHǁfit__mutmut_131,
        "xǁGOGARCHǁfit__mutmut_132": xǁGOGARCHǁfit__mutmut_132,
        "xǁGOGARCHǁfit__mutmut_133": xǁGOGARCHǁfit__mutmut_133,
        "xǁGOGARCHǁfit__mutmut_134": xǁGOGARCHǁfit__mutmut_134,
        "xǁGOGARCHǁfit__mutmut_135": xǁGOGARCHǁfit__mutmut_135,
        "xǁGOGARCHǁfit__mutmut_136": xǁGOGARCHǁfit__mutmut_136,
        "xǁGOGARCHǁfit__mutmut_137": xǁGOGARCHǁfit__mutmut_137,
        "xǁGOGARCHǁfit__mutmut_138": xǁGOGARCHǁfit__mutmut_138,
        "xǁGOGARCHǁfit__mutmut_139": xǁGOGARCHǁfit__mutmut_139,
        "xǁGOGARCHǁfit__mutmut_140": xǁGOGARCHǁfit__mutmut_140,
        "xǁGOGARCHǁfit__mutmut_141": xǁGOGARCHǁfit__mutmut_141,
        "xǁGOGARCHǁfit__mutmut_142": xǁGOGARCHǁfit__mutmut_142,
        "xǁGOGARCHǁfit__mutmut_143": xǁGOGARCHǁfit__mutmut_143,
        "xǁGOGARCHǁfit__mutmut_144": xǁGOGARCHǁfit__mutmut_144,
        "xǁGOGARCHǁfit__mutmut_145": xǁGOGARCHǁfit__mutmut_145,
        "xǁGOGARCHǁfit__mutmut_146": xǁGOGARCHǁfit__mutmut_146,
        "xǁGOGARCHǁfit__mutmut_147": xǁGOGARCHǁfit__mutmut_147,
        "xǁGOGARCHǁfit__mutmut_148": xǁGOGARCHǁfit__mutmut_148,
    }
    xǁGOGARCHǁfit__mutmut_orig.__name__ = "xǁGOGARCHǁfit"

    @property
    def mixing_matrix(self) -> NDArray[np.float64] | None:
        """Return the ICA mixing matrix Z."""
        return self._mixing_matrix

    @property
    def factors(self) -> NDArray[np.float64] | None:
        """Return the independent factors."""
        return self._factors

    def forecast(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        args = [results, horizon]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁGOGARCHǁforecast__mutmut_orig"),
            object.__getattribute__(self, "xǁGOGARCHǁforecast__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁGOGARCHǁforecast__mutmut_orig(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), 1e-12))
            r_forecast[h] = h_h / np.outer(d, d)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_1(
        self,
        results: MultivarResults,
        horizon: int = 11,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), 1e-12))
            r_forecast[h] = h_h / np.outer(d, d)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_2(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), 1e-12))
            r_forecast[h] = h_h / np.outer(d, d)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_3(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = None

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), 1e-12))
            r_forecast[h] = h_h / np.outer(d, d)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_4(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = None
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), 1e-12))
            r_forecast[h] = h_h / np.outer(d, d)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_5(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros(None)
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), 1e-12))
            r_forecast[h] = h_h / np.outer(d, d)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_6(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = None

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), 1e-12))
            r_forecast[h] = h_h / np.outer(d, d)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_7(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros(None)

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), 1e-12))
            r_forecast[h] = h_h / np.outer(d, d)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_8(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(None):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), 1e-12))
            r_forecast[h] = h_h / np.outer(d, d)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_9(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = None
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), 1e-12))
            r_forecast[h] = h_h / np.outer(d, d)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_10(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(None)
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), 1e-12))
            r_forecast[h] = h_h / np.outer(d, d)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_11(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] * 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), 1e-12))
            r_forecast[h] = h_h / np.outer(d, d)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_12(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[+1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), 1e-12))
            r_forecast[h] = h_h / np.outer(d, d)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_13(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-2] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), 1e-12))
            r_forecast[h] = h_h / np.outer(d, d)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_14(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 3 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), 1e-12))
            r_forecast[h] = h_h / np.outer(d, d)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_15(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = None
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), 1e-12))
            r_forecast[h] = h_h / np.outer(d, d)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_16(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(None)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), 1e-12))
            r_forecast[h] = h_h / np.outer(d, d)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_17(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = None
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), 1e-12))
            r_forecast[h] = h_h / np.outer(d, d)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_18(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = None
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), 1e-12))
            r_forecast[h] = h_h / np.outer(d, d)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_19(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) * 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), 1e-12))
            r_forecast[h] = h_h / np.outer(d, d)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_20(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h - h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), 1e-12))
            r_forecast[h] = h_h / np.outer(d, d)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_21(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 3.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), 1e-12))
            r_forecast[h] = h_h / np.outer(d, d)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_22(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = None

            d = np.sqrt(np.maximum(np.diag(h_h), 1e-12))
            r_forecast[h] = h_h / np.outer(d, d)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_23(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = None
            r_forecast[h] = h_h / np.outer(d, d)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_24(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(None)
            r_forecast[h] = h_h / np.outer(d, d)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_25(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(None, 1e-12))
            r_forecast[h] = h_h / np.outer(d, d)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_26(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), None))
            r_forecast[h] = h_h / np.outer(d, d)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_27(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(1e-12))
            r_forecast[h] = h_h / np.outer(d, d)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_28(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(
                np.maximum(
                    np.diag(h_h),
                )
            )
            r_forecast[h] = h_h / np.outer(d, d)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_29(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(None), 1e-12))
            r_forecast[h] = h_h / np.outer(d, d)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_30(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), 1.000000000001))
            r_forecast[h] = h_h / np.outer(d, d)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_31(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), 1e-12))
            r_forecast[h] = None

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_32(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), 1e-12))
            r_forecast[h] = h_h * np.outer(d, d)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_33(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), 1e-12))
            r_forecast[h] = h_h / np.outer(None, d)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_34(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), 1e-12))
            r_forecast[h] = h_h / np.outer(d, None)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_35(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), 1e-12))
            r_forecast[h] = h_h / np.outer(d)

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_36(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), 1e-12))
            r_forecast[h] = h_h / np.outer(
                d,
            )

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_37(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), 1e-12))
            r_forecast[h] = h_h / np.outer(d, d)

        return {"XXcovarianceXX": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_38(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), 1e-12))
            r_forecast[h] = h_h / np.outer(d, d)

        return {"COVARIANCE": h_forecast, "correlation": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_39(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), 1e-12))
            r_forecast[h] = h_h / np.outer(d, d)

        return {"covariance": h_forecast, "XXcorrelationXX": r_forecast}

    def xǁGOGARCHǁforecast__mutmut_40(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using GO-GARCH structure.

        H_{T+h} = Z * diag(h_{1,T+h}, ..., h_{k,T+h}) * Z'

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
        assert self._mixing_matrix is not None
        mix_mat = self._mixing_matrix

        h_forecast = np.zeros((horizon, self.k, self.k))
        r_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            # Naive: use last conditional variance of each factor
            h_f = np.array(
                [res.conditional_volatility[-1] ** 2 for res in results.univariate_results]
            )
            d_f = np.diag(h_f)
            h_h = mix_mat @ d_f @ mix_mat.T
            h_h = (h_h + h_h.T) / 2.0
            h_forecast[h] = h_h

            d = np.sqrt(np.maximum(np.diag(h_h), 1e-12))
            r_forecast[h] = h_h / np.outer(d, d)

        return {"covariance": h_forecast, "CORRELATION": r_forecast}

    xǁGOGARCHǁforecast__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁGOGARCHǁforecast__mutmut_1": xǁGOGARCHǁforecast__mutmut_1,
        "xǁGOGARCHǁforecast__mutmut_2": xǁGOGARCHǁforecast__mutmut_2,
        "xǁGOGARCHǁforecast__mutmut_3": xǁGOGARCHǁforecast__mutmut_3,
        "xǁGOGARCHǁforecast__mutmut_4": xǁGOGARCHǁforecast__mutmut_4,
        "xǁGOGARCHǁforecast__mutmut_5": xǁGOGARCHǁforecast__mutmut_5,
        "xǁGOGARCHǁforecast__mutmut_6": xǁGOGARCHǁforecast__mutmut_6,
        "xǁGOGARCHǁforecast__mutmut_7": xǁGOGARCHǁforecast__mutmut_7,
        "xǁGOGARCHǁforecast__mutmut_8": xǁGOGARCHǁforecast__mutmut_8,
        "xǁGOGARCHǁforecast__mutmut_9": xǁGOGARCHǁforecast__mutmut_9,
        "xǁGOGARCHǁforecast__mutmut_10": xǁGOGARCHǁforecast__mutmut_10,
        "xǁGOGARCHǁforecast__mutmut_11": xǁGOGARCHǁforecast__mutmut_11,
        "xǁGOGARCHǁforecast__mutmut_12": xǁGOGARCHǁforecast__mutmut_12,
        "xǁGOGARCHǁforecast__mutmut_13": xǁGOGARCHǁforecast__mutmut_13,
        "xǁGOGARCHǁforecast__mutmut_14": xǁGOGARCHǁforecast__mutmut_14,
        "xǁGOGARCHǁforecast__mutmut_15": xǁGOGARCHǁforecast__mutmut_15,
        "xǁGOGARCHǁforecast__mutmut_16": xǁGOGARCHǁforecast__mutmut_16,
        "xǁGOGARCHǁforecast__mutmut_17": xǁGOGARCHǁforecast__mutmut_17,
        "xǁGOGARCHǁforecast__mutmut_18": xǁGOGARCHǁforecast__mutmut_18,
        "xǁGOGARCHǁforecast__mutmut_19": xǁGOGARCHǁforecast__mutmut_19,
        "xǁGOGARCHǁforecast__mutmut_20": xǁGOGARCHǁforecast__mutmut_20,
        "xǁGOGARCHǁforecast__mutmut_21": xǁGOGARCHǁforecast__mutmut_21,
        "xǁGOGARCHǁforecast__mutmut_22": xǁGOGARCHǁforecast__mutmut_22,
        "xǁGOGARCHǁforecast__mutmut_23": xǁGOGARCHǁforecast__mutmut_23,
        "xǁGOGARCHǁforecast__mutmut_24": xǁGOGARCHǁforecast__mutmut_24,
        "xǁGOGARCHǁforecast__mutmut_25": xǁGOGARCHǁforecast__mutmut_25,
        "xǁGOGARCHǁforecast__mutmut_26": xǁGOGARCHǁforecast__mutmut_26,
        "xǁGOGARCHǁforecast__mutmut_27": xǁGOGARCHǁforecast__mutmut_27,
        "xǁGOGARCHǁforecast__mutmut_28": xǁGOGARCHǁforecast__mutmut_28,
        "xǁGOGARCHǁforecast__mutmut_29": xǁGOGARCHǁforecast__mutmut_29,
        "xǁGOGARCHǁforecast__mutmut_30": xǁGOGARCHǁforecast__mutmut_30,
        "xǁGOGARCHǁforecast__mutmut_31": xǁGOGARCHǁforecast__mutmut_31,
        "xǁGOGARCHǁforecast__mutmut_32": xǁGOGARCHǁforecast__mutmut_32,
        "xǁGOGARCHǁforecast__mutmut_33": xǁGOGARCHǁforecast__mutmut_33,
        "xǁGOGARCHǁforecast__mutmut_34": xǁGOGARCHǁforecast__mutmut_34,
        "xǁGOGARCHǁforecast__mutmut_35": xǁGOGARCHǁforecast__mutmut_35,
        "xǁGOGARCHǁforecast__mutmut_36": xǁGOGARCHǁforecast__mutmut_36,
        "xǁGOGARCHǁforecast__mutmut_37": xǁGOGARCHǁforecast__mutmut_37,
        "xǁGOGARCHǁforecast__mutmut_38": xǁGOGARCHǁforecast__mutmut_38,
        "xǁGOGARCHǁforecast__mutmut_39": xǁGOGARCHǁforecast__mutmut_39,
        "xǁGOGARCHǁforecast__mutmut_40": xǁGOGARCHǁforecast__mutmut_40,
    }
    xǁGOGARCHǁforecast__mutmut_orig.__name__ = "xǁGOGARCHǁforecast"
