"""DECO: Dynamic Equicorrelation model (Engle & Kelly, 2012).

R_t = (1 - rho_t) * I_k + rho_t * J_k

Where rho_t is the average off-diagonal element of the DCC-like Q_t.
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


class DECO(MultivariateVolatilityModel):
    """Dynamic Equicorrelation model.

    DECO simplifies DCC by assuming a single scalar equicorrelation rho_t
    for all pairs. This allows scaling to very large k (hundreds of assets).

    R_t = (1 - rho_t) * I_k + rho_t * J_k

    Where:
    - J_k = 1_k * 1_k' (matrix of ones)
    - rho_t = mean off-diagonal of normalized Q_t from DCC dynamics

    Parameters
    ----------
    endog : ndarray
        Array of shape (T, k) with k return series.
    univariate_model : str
        Univariate GARCH variant. Default 'GARCH'.
    univariate_order : tuple[int, int]
        (p, q) order for univariate GARCH. Default (1, 1).

    Examples
    --------
    >>> import numpy as np
    >>> from archbox.multivariate.deco import DECO
    >>> returns = np.random.randn(500, 10) * 0.01
    >>> model = DECO(returns)
    >>> results = model.fit()
    >>> print(results.summary())

    References
    ----------
    Engle, R.F. & Kelly, B.T. (2012). Dynamic Equicorrelation.
    Journal of Business & Economic Statistics, 30(2), 212-228.
    """

    model_name: str = "DECO"

    def __init__(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        args = [endog, univariate_model, univariate_order]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁDECOǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁDECOǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁDECOǁ__init____mutmut_orig(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize DECO model with options."""
        super().__init__(endog, univariate_model, univariate_order)
        self._q_bar: NDArray[np.float64] | None = None
        self._rho_t: NDArray[np.float64] | None = None

    def xǁDECOǁ__init____mutmut_1(
        self,
        endog: Any,
        univariate_model: str = "XXGARCHXX",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize DECO model with options."""
        super().__init__(endog, univariate_model, univariate_order)
        self._q_bar: NDArray[np.float64] | None = None
        self._rho_t: NDArray[np.float64] | None = None

    def xǁDECOǁ__init____mutmut_2(
        self,
        endog: Any,
        univariate_model: str = "garch",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize DECO model with options."""
        super().__init__(endog, univariate_model, univariate_order)
        self._q_bar: NDArray[np.float64] | None = None
        self._rho_t: NDArray[np.float64] | None = None

    def xǁDECOǁ__init____mutmut_3(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize DECO model with options."""
        super().__init__(None, univariate_model, univariate_order)
        self._q_bar: NDArray[np.float64] | None = None
        self._rho_t: NDArray[np.float64] | None = None

    def xǁDECOǁ__init____mutmut_4(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize DECO model with options."""
        super().__init__(endog, None, univariate_order)
        self._q_bar: NDArray[np.float64] | None = None
        self._rho_t: NDArray[np.float64] | None = None

    def xǁDECOǁ__init____mutmut_5(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize DECO model with options."""
        super().__init__(endog, univariate_model, None)
        self._q_bar: NDArray[np.float64] | None = None
        self._rho_t: NDArray[np.float64] | None = None

    def xǁDECOǁ__init____mutmut_6(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize DECO model with options."""
        super().__init__(univariate_model, univariate_order)
        self._q_bar: NDArray[np.float64] | None = None
        self._rho_t: NDArray[np.float64] | None = None

    def xǁDECOǁ__init____mutmut_7(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize DECO model with options."""
        super().__init__(endog, univariate_order)
        self._q_bar: NDArray[np.float64] | None = None
        self._rho_t: NDArray[np.float64] | None = None

    def xǁDECOǁ__init____mutmut_8(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize DECO model with options."""
        super().__init__(
            endog,
            univariate_model,
        )
        self._q_bar: NDArray[np.float64] | None = None
        self._rho_t: NDArray[np.float64] | None = None

    def xǁDECOǁ__init____mutmut_9(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize DECO model with options."""
        super().__init__(endog, univariate_model, univariate_order)
        self._q_bar: NDArray[np.float64] | None = ""
        self._rho_t: NDArray[np.float64] | None = None

    def xǁDECOǁ__init____mutmut_10(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize DECO model with options."""
        super().__init__(endog, univariate_model, univariate_order)
        self._q_bar: NDArray[np.float64] | None = None
        self._rho_t: NDArray[np.float64] | None = ""

    xǁDECOǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁDECOǁ__init____mutmut_1": xǁDECOǁ__init____mutmut_1,
        "xǁDECOǁ__init____mutmut_2": xǁDECOǁ__init____mutmut_2,
        "xǁDECOǁ__init____mutmut_3": xǁDECOǁ__init____mutmut_3,
        "xǁDECOǁ__init____mutmut_4": xǁDECOǁ__init____mutmut_4,
        "xǁDECOǁ__init____mutmut_5": xǁDECOǁ__init____mutmut_5,
        "xǁDECOǁ__init____mutmut_6": xǁDECOǁ__init____mutmut_6,
        "xǁDECOǁ__init____mutmut_7": xǁDECOǁ__init____mutmut_7,
        "xǁDECOǁ__init____mutmut_8": xǁDECOǁ__init____mutmut_8,
        "xǁDECOǁ__init____mutmut_9": xǁDECOǁ__init____mutmut_9,
        "xǁDECOǁ__init____mutmut_10": xǁDECOǁ__init____mutmut_10,
    }
    xǁDECOǁ__init____mutmut_orig.__name__ = "xǁDECOǁ__init__"

    def _correlation_recursion(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        args = [params, std_resids]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁDECOǁ_correlation_recursion__mutmut_orig"),
            object.__getattribute__(self, "xǁDECOǁ_correlation_recursion__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁDECOǁ_correlation_recursion__mutmut_orig(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_1(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = None
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_2(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[1], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_3(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[2]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_4(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = None

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_5(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = None
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_6(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids * n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_7(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = None

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_8(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = None
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_9(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros(None)
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_10(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = None
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_11(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros(None)
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_12(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = None

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_13(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(None)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_14(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = None

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_15(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[1] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_16(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = None
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_17(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(None)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_18(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = None

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_19(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones(None)

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_20(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(None):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_21(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t >= 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_22(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 1:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_23(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = None  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_24(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t + 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_25(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 2 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_26(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = None

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_27(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) - b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_28(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar - a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_29(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) / q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_30(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a + b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_31(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 + a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_32(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (2.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_33(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a / (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_34(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b / q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_35(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t + 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_36(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 2]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_37(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = None
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_38(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(None)
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_39(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(None))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_40(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = None
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_41(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(None, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_42(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, None)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_43(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_44(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(
                d,
            )
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_45(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1.000000000001)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_46(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = None

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_47(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] * np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_48(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(None, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_49(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, None)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_50(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_51(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(
                d,
            )

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_52(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = None

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_53(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) * (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_54(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) + k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_55(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(None) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_56(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k / (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_57(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k + 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_58(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 2))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_59(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = None
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_60(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(None, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_61(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, None, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_62(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, None)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_63(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(-1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_64(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_65(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(
                rho,
                -1.0 / (k - 1) + 1e-6,
            )
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_66(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) - 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_67(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 * (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_68(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, +1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_69(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -2.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_70(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k + 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_71(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 2) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_72(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1.000001, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_73(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 + 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_74(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 2.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_75(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1.000001)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_76(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = None

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_77(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = None

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_78(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k - rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_79(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) / eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_80(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 + rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_81(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (2.0 - rho) * eye_k + rho * ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_82(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho / ones_k

        self._rho_t = rho_t
        return r_mat

    def xǁDECOǁ_correlation_recursion__mutmut_83(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute DECO equicorrelation matrices R_t.

        Uses DCC-like Q_t dynamics to compute mean off-diagonal rho_t,
        then constructs R_t = (1 - rho_t) * I + rho_t * J.

        Parameters
        ----------
        params : ndarray
            DECO parameters [a, b] (same as DCC parameters).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Equicorrelation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar
        q_bar = std_resids.T @ std_resids / n_obs
        self._q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))
        rho_t = np.zeros(n_obs)

        # Initialize
        q_mat[0] = q_bar.copy()

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        for t in range(n_obs):
            if t > 0:
                z = std_resids[t - 1 : t].T  # (k, 1)
                q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize Q_t to correlation
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_dcc = q_mat[t] / np.outer(d, d)

            # Compute average off-diagonal (equicorrelation)
            rho = (np.sum(r_dcc) - k) / (k * (k - 1))

            # Clip to valid range: -1/(k-1) < rho < 1
            rho = np.clip(rho, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)
            rho_t[t] = rho

            # Construct equicorrelation matrix
            r_mat[t] = (1.0 - rho) * eye_k + rho * ones_k

        self._rho_t = None
        return r_mat

    xǁDECOǁ_correlation_recursion__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁDECOǁ_correlation_recursion__mutmut_1": xǁDECOǁ_correlation_recursion__mutmut_1,
        "xǁDECOǁ_correlation_recursion__mutmut_2": xǁDECOǁ_correlation_recursion__mutmut_2,
        "xǁDECOǁ_correlation_recursion__mutmut_3": xǁDECOǁ_correlation_recursion__mutmut_3,
        "xǁDECOǁ_correlation_recursion__mutmut_4": xǁDECOǁ_correlation_recursion__mutmut_4,
        "xǁDECOǁ_correlation_recursion__mutmut_5": xǁDECOǁ_correlation_recursion__mutmut_5,
        "xǁDECOǁ_correlation_recursion__mutmut_6": xǁDECOǁ_correlation_recursion__mutmut_6,
        "xǁDECOǁ_correlation_recursion__mutmut_7": xǁDECOǁ_correlation_recursion__mutmut_7,
        "xǁDECOǁ_correlation_recursion__mutmut_8": xǁDECOǁ_correlation_recursion__mutmut_8,
        "xǁDECOǁ_correlation_recursion__mutmut_9": xǁDECOǁ_correlation_recursion__mutmut_9,
        "xǁDECOǁ_correlation_recursion__mutmut_10": xǁDECOǁ_correlation_recursion__mutmut_10,
        "xǁDECOǁ_correlation_recursion__mutmut_11": xǁDECOǁ_correlation_recursion__mutmut_11,
        "xǁDECOǁ_correlation_recursion__mutmut_12": xǁDECOǁ_correlation_recursion__mutmut_12,
        "xǁDECOǁ_correlation_recursion__mutmut_13": xǁDECOǁ_correlation_recursion__mutmut_13,
        "xǁDECOǁ_correlation_recursion__mutmut_14": xǁDECOǁ_correlation_recursion__mutmut_14,
        "xǁDECOǁ_correlation_recursion__mutmut_15": xǁDECOǁ_correlation_recursion__mutmut_15,
        "xǁDECOǁ_correlation_recursion__mutmut_16": xǁDECOǁ_correlation_recursion__mutmut_16,
        "xǁDECOǁ_correlation_recursion__mutmut_17": xǁDECOǁ_correlation_recursion__mutmut_17,
        "xǁDECOǁ_correlation_recursion__mutmut_18": xǁDECOǁ_correlation_recursion__mutmut_18,
        "xǁDECOǁ_correlation_recursion__mutmut_19": xǁDECOǁ_correlation_recursion__mutmut_19,
        "xǁDECOǁ_correlation_recursion__mutmut_20": xǁDECOǁ_correlation_recursion__mutmut_20,
        "xǁDECOǁ_correlation_recursion__mutmut_21": xǁDECOǁ_correlation_recursion__mutmut_21,
        "xǁDECOǁ_correlation_recursion__mutmut_22": xǁDECOǁ_correlation_recursion__mutmut_22,
        "xǁDECOǁ_correlation_recursion__mutmut_23": xǁDECOǁ_correlation_recursion__mutmut_23,
        "xǁDECOǁ_correlation_recursion__mutmut_24": xǁDECOǁ_correlation_recursion__mutmut_24,
        "xǁDECOǁ_correlation_recursion__mutmut_25": xǁDECOǁ_correlation_recursion__mutmut_25,
        "xǁDECOǁ_correlation_recursion__mutmut_26": xǁDECOǁ_correlation_recursion__mutmut_26,
        "xǁDECOǁ_correlation_recursion__mutmut_27": xǁDECOǁ_correlation_recursion__mutmut_27,
        "xǁDECOǁ_correlation_recursion__mutmut_28": xǁDECOǁ_correlation_recursion__mutmut_28,
        "xǁDECOǁ_correlation_recursion__mutmut_29": xǁDECOǁ_correlation_recursion__mutmut_29,
        "xǁDECOǁ_correlation_recursion__mutmut_30": xǁDECOǁ_correlation_recursion__mutmut_30,
        "xǁDECOǁ_correlation_recursion__mutmut_31": xǁDECOǁ_correlation_recursion__mutmut_31,
        "xǁDECOǁ_correlation_recursion__mutmut_32": xǁDECOǁ_correlation_recursion__mutmut_32,
        "xǁDECOǁ_correlation_recursion__mutmut_33": xǁDECOǁ_correlation_recursion__mutmut_33,
        "xǁDECOǁ_correlation_recursion__mutmut_34": xǁDECOǁ_correlation_recursion__mutmut_34,
        "xǁDECOǁ_correlation_recursion__mutmut_35": xǁDECOǁ_correlation_recursion__mutmut_35,
        "xǁDECOǁ_correlation_recursion__mutmut_36": xǁDECOǁ_correlation_recursion__mutmut_36,
        "xǁDECOǁ_correlation_recursion__mutmut_37": xǁDECOǁ_correlation_recursion__mutmut_37,
        "xǁDECOǁ_correlation_recursion__mutmut_38": xǁDECOǁ_correlation_recursion__mutmut_38,
        "xǁDECOǁ_correlation_recursion__mutmut_39": xǁDECOǁ_correlation_recursion__mutmut_39,
        "xǁDECOǁ_correlation_recursion__mutmut_40": xǁDECOǁ_correlation_recursion__mutmut_40,
        "xǁDECOǁ_correlation_recursion__mutmut_41": xǁDECOǁ_correlation_recursion__mutmut_41,
        "xǁDECOǁ_correlation_recursion__mutmut_42": xǁDECOǁ_correlation_recursion__mutmut_42,
        "xǁDECOǁ_correlation_recursion__mutmut_43": xǁDECOǁ_correlation_recursion__mutmut_43,
        "xǁDECOǁ_correlation_recursion__mutmut_44": xǁDECOǁ_correlation_recursion__mutmut_44,
        "xǁDECOǁ_correlation_recursion__mutmut_45": xǁDECOǁ_correlation_recursion__mutmut_45,
        "xǁDECOǁ_correlation_recursion__mutmut_46": xǁDECOǁ_correlation_recursion__mutmut_46,
        "xǁDECOǁ_correlation_recursion__mutmut_47": xǁDECOǁ_correlation_recursion__mutmut_47,
        "xǁDECOǁ_correlation_recursion__mutmut_48": xǁDECOǁ_correlation_recursion__mutmut_48,
        "xǁDECOǁ_correlation_recursion__mutmut_49": xǁDECOǁ_correlation_recursion__mutmut_49,
        "xǁDECOǁ_correlation_recursion__mutmut_50": xǁDECOǁ_correlation_recursion__mutmut_50,
        "xǁDECOǁ_correlation_recursion__mutmut_51": xǁDECOǁ_correlation_recursion__mutmut_51,
        "xǁDECOǁ_correlation_recursion__mutmut_52": xǁDECOǁ_correlation_recursion__mutmut_52,
        "xǁDECOǁ_correlation_recursion__mutmut_53": xǁDECOǁ_correlation_recursion__mutmut_53,
        "xǁDECOǁ_correlation_recursion__mutmut_54": xǁDECOǁ_correlation_recursion__mutmut_54,
        "xǁDECOǁ_correlation_recursion__mutmut_55": xǁDECOǁ_correlation_recursion__mutmut_55,
        "xǁDECOǁ_correlation_recursion__mutmut_56": xǁDECOǁ_correlation_recursion__mutmut_56,
        "xǁDECOǁ_correlation_recursion__mutmut_57": xǁDECOǁ_correlation_recursion__mutmut_57,
        "xǁDECOǁ_correlation_recursion__mutmut_58": xǁDECOǁ_correlation_recursion__mutmut_58,
        "xǁDECOǁ_correlation_recursion__mutmut_59": xǁDECOǁ_correlation_recursion__mutmut_59,
        "xǁDECOǁ_correlation_recursion__mutmut_60": xǁDECOǁ_correlation_recursion__mutmut_60,
        "xǁDECOǁ_correlation_recursion__mutmut_61": xǁDECOǁ_correlation_recursion__mutmut_61,
        "xǁDECOǁ_correlation_recursion__mutmut_62": xǁDECOǁ_correlation_recursion__mutmut_62,
        "xǁDECOǁ_correlation_recursion__mutmut_63": xǁDECOǁ_correlation_recursion__mutmut_63,
        "xǁDECOǁ_correlation_recursion__mutmut_64": xǁDECOǁ_correlation_recursion__mutmut_64,
        "xǁDECOǁ_correlation_recursion__mutmut_65": xǁDECOǁ_correlation_recursion__mutmut_65,
        "xǁDECOǁ_correlation_recursion__mutmut_66": xǁDECOǁ_correlation_recursion__mutmut_66,
        "xǁDECOǁ_correlation_recursion__mutmut_67": xǁDECOǁ_correlation_recursion__mutmut_67,
        "xǁDECOǁ_correlation_recursion__mutmut_68": xǁDECOǁ_correlation_recursion__mutmut_68,
        "xǁDECOǁ_correlation_recursion__mutmut_69": xǁDECOǁ_correlation_recursion__mutmut_69,
        "xǁDECOǁ_correlation_recursion__mutmut_70": xǁDECOǁ_correlation_recursion__mutmut_70,
        "xǁDECOǁ_correlation_recursion__mutmut_71": xǁDECOǁ_correlation_recursion__mutmut_71,
        "xǁDECOǁ_correlation_recursion__mutmut_72": xǁDECOǁ_correlation_recursion__mutmut_72,
        "xǁDECOǁ_correlation_recursion__mutmut_73": xǁDECOǁ_correlation_recursion__mutmut_73,
        "xǁDECOǁ_correlation_recursion__mutmut_74": xǁDECOǁ_correlation_recursion__mutmut_74,
        "xǁDECOǁ_correlation_recursion__mutmut_75": xǁDECOǁ_correlation_recursion__mutmut_75,
        "xǁDECOǁ_correlation_recursion__mutmut_76": xǁDECOǁ_correlation_recursion__mutmut_76,
        "xǁDECOǁ_correlation_recursion__mutmut_77": xǁDECOǁ_correlation_recursion__mutmut_77,
        "xǁDECOǁ_correlation_recursion__mutmut_78": xǁDECOǁ_correlation_recursion__mutmut_78,
        "xǁDECOǁ_correlation_recursion__mutmut_79": xǁDECOǁ_correlation_recursion__mutmut_79,
        "xǁDECOǁ_correlation_recursion__mutmut_80": xǁDECOǁ_correlation_recursion__mutmut_80,
        "xǁDECOǁ_correlation_recursion__mutmut_81": xǁDECOǁ_correlation_recursion__mutmut_81,
        "xǁDECOǁ_correlation_recursion__mutmut_82": xǁDECOǁ_correlation_recursion__mutmut_82,
        "xǁDECOǁ_correlation_recursion__mutmut_83": xǁDECOǁ_correlation_recursion__mutmut_83,
    }
    xǁDECOǁ_correlation_recursion__mutmut_orig.__name__ = "xǁDECOǁ_correlation_recursion"

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values: a=0.05, b=0.90."""
        return np.array([0.05, 0.90])

    @property
    def param_names(self) -> list[str]:
        """DECO parameter names."""
        return ["a", "b"]

    def _param_bounds(self) -> list[tuple[float, float]]:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁDECOǁ_param_bounds__mutmut_orig"),
            object.__getattribute__(self, "xǁDECOǁ_param_bounds__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁDECOǁ_param_bounds__mutmut_orig(self) -> list[tuple[float, float]]:
        """Parameter bounds: a > 0, b > 0, a+b < 1."""
        return [(1e-6, 0.499), (1e-6, 0.9999)]

    def xǁDECOǁ_param_bounds__mutmut_1(self) -> list[tuple[float, float]]:
        """Parameter bounds: a > 0, b > 0, a+b < 1."""
        return [(1.000001, 0.499), (1e-6, 0.9999)]

    def xǁDECOǁ_param_bounds__mutmut_2(self) -> list[tuple[float, float]]:
        """Parameter bounds: a > 0, b > 0, a+b < 1."""
        return [(1e-6, 1.499), (1e-6, 0.9999)]

    def xǁDECOǁ_param_bounds__mutmut_3(self) -> list[tuple[float, float]]:
        """Parameter bounds: a > 0, b > 0, a+b < 1."""
        return [(1e-6, 0.499), (1.000001, 0.9999)]

    def xǁDECOǁ_param_bounds__mutmut_4(self) -> list[tuple[float, float]]:
        """Parameter bounds: a > 0, b > 0, a+b < 1."""
        return [(1e-6, 0.499), (1e-6, 1.9999)]

    xǁDECOǁ_param_bounds__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁDECOǁ_param_bounds__mutmut_1": xǁDECOǁ_param_bounds__mutmut_1,
        "xǁDECOǁ_param_bounds__mutmut_2": xǁDECOǁ_param_bounds__mutmut_2,
        "xǁDECOǁ_param_bounds__mutmut_3": xǁDECOǁ_param_bounds__mutmut_3,
        "xǁDECOǁ_param_bounds__mutmut_4": xǁDECOǁ_param_bounds__mutmut_4,
    }
    xǁDECOǁ_param_bounds__mutmut_orig.__name__ = "xǁDECOǁ_param_bounds"

    def _estimate_correlation(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        args = [std_resids, disp]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁDECOǁ_estimate_correlation__mutmut_orig"),
            object.__getattribute__(self, "xǁDECOǁ_estimate_correlation__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁDECOǁ_estimate_correlation__mutmut_orig(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_1(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = False,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_2(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = None

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_3(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = None

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_4(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[1], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_5(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[2]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_6(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 and b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_7(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 and a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_8(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a - b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_9(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b > 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_10(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 1.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_11(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a < 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_12(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 1 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_13(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b < 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_14(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 1:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_15(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 10000000001.0

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_16(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = None
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_17(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(None, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_18(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, None)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_19(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_20(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(
                params,
            )
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_21(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = None
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_22(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[1]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_23(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = None

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_24(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 1.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_25(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(None):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_26(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = None
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_27(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = None  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_28(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t - 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_29(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 2].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_30(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = None
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_31(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(None)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_32(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign < 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_33(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 1:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_34(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 10000000001.0
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_35(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = None
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_36(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(None, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_37(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, None)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_38(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_39(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(
                        r_cur,
                    )
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_40(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = None
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_41(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = None
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_42(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll = -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_43(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll -= -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_44(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 / (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_45(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += +0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_46(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -1.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_47(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r + quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_48(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet - quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_49(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 10000000001.0

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_50(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return +ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_51(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = None

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_52(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"XXtypeXX": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_53(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"TYPE": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_54(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "XXineqXX", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_55(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "INEQ", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_56(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "XXfunXX": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_57(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "FUN": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_58(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: None},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_59(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] + p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_60(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 + p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_61(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 1.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_62(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[1] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_63(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[2]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_64(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = None

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_65(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            None,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_66(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            None,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_67(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method=None,
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_68(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=None,
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_69(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=None,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_70(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options=None,
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_71(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_72(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_73(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_74(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_75(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_76(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_77(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="XXSLSQPXX",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_78(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="slsqp",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_79(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"XXmaxiterXX": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_80(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"MAXITER": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_81(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 501, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_82(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "XXdispXX": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_83(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "DISP": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_84(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "XXftolXX": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_85(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "FTOL": 1e-8},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_86(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1.00000001},
        )

        return np.asarray(result.x, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_87(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(None, dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_88(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(result.x, dtype=None)

    def xǁDECOǁ_estimate_correlation__mutmut_89(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(dtype=np.float64)

    def xǁDECOǁ_estimate_correlation__mutmut_90(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DECO parameters (a, b) via MLE.

        Parameters
        ----------
        std_resids : ndarray
            Standardized residuals (T, k).
        disp : bool
            Display optimization progress.

        Returns
        -------
        ndarray
            Estimated parameters [a, b].
        """
        from scipy import optimize

        x0 = self.start_params

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DECO."""
            a, b = params[0], params[1]

            if a + b >= 0.9999 or a <= 0 or b <= 0:
                return 1e10

            r_t = self._correlation_recursion(params, std_resids)
            n_obs = std_resids.shape[0]
            ll = 0.0

            for t in range(n_obs):
                r_cur = r_t[t]
                z = std_resids[t : t + 1].T  # (k, 1)

                try:
                    sign, logdet = np.linalg.slogdet(r_cur)
                    if sign <= 0:
                        return 1e10
                    r_inv_z = np.linalg.solve(r_cur, z)
                    quad_r = (z.T @ r_inv_z).item()
                    quad_i = (z.T @ z).item()
                    ll += -0.5 * (logdet + quad_r - quad_i)
                except np.linalg.LinAlgError:
                    return 1e10

            return -ll

        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        result = optimize.minimize(
            neg_loglike,
            x0,
            method="SLSQP",
            bounds=self._param_bounds(),
            constraints=constraints,
            options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
        )

        return np.asarray(
            result.x,
        )

    xǁDECOǁ_estimate_correlation__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁDECOǁ_estimate_correlation__mutmut_1": xǁDECOǁ_estimate_correlation__mutmut_1,
        "xǁDECOǁ_estimate_correlation__mutmut_2": xǁDECOǁ_estimate_correlation__mutmut_2,
        "xǁDECOǁ_estimate_correlation__mutmut_3": xǁDECOǁ_estimate_correlation__mutmut_3,
        "xǁDECOǁ_estimate_correlation__mutmut_4": xǁDECOǁ_estimate_correlation__mutmut_4,
        "xǁDECOǁ_estimate_correlation__mutmut_5": xǁDECOǁ_estimate_correlation__mutmut_5,
        "xǁDECOǁ_estimate_correlation__mutmut_6": xǁDECOǁ_estimate_correlation__mutmut_6,
        "xǁDECOǁ_estimate_correlation__mutmut_7": xǁDECOǁ_estimate_correlation__mutmut_7,
        "xǁDECOǁ_estimate_correlation__mutmut_8": xǁDECOǁ_estimate_correlation__mutmut_8,
        "xǁDECOǁ_estimate_correlation__mutmut_9": xǁDECOǁ_estimate_correlation__mutmut_9,
        "xǁDECOǁ_estimate_correlation__mutmut_10": xǁDECOǁ_estimate_correlation__mutmut_10,
        "xǁDECOǁ_estimate_correlation__mutmut_11": xǁDECOǁ_estimate_correlation__mutmut_11,
        "xǁDECOǁ_estimate_correlation__mutmut_12": xǁDECOǁ_estimate_correlation__mutmut_12,
        "xǁDECOǁ_estimate_correlation__mutmut_13": xǁDECOǁ_estimate_correlation__mutmut_13,
        "xǁDECOǁ_estimate_correlation__mutmut_14": xǁDECOǁ_estimate_correlation__mutmut_14,
        "xǁDECOǁ_estimate_correlation__mutmut_15": xǁDECOǁ_estimate_correlation__mutmut_15,
        "xǁDECOǁ_estimate_correlation__mutmut_16": xǁDECOǁ_estimate_correlation__mutmut_16,
        "xǁDECOǁ_estimate_correlation__mutmut_17": xǁDECOǁ_estimate_correlation__mutmut_17,
        "xǁDECOǁ_estimate_correlation__mutmut_18": xǁDECOǁ_estimate_correlation__mutmut_18,
        "xǁDECOǁ_estimate_correlation__mutmut_19": xǁDECOǁ_estimate_correlation__mutmut_19,
        "xǁDECOǁ_estimate_correlation__mutmut_20": xǁDECOǁ_estimate_correlation__mutmut_20,
        "xǁDECOǁ_estimate_correlation__mutmut_21": xǁDECOǁ_estimate_correlation__mutmut_21,
        "xǁDECOǁ_estimate_correlation__mutmut_22": xǁDECOǁ_estimate_correlation__mutmut_22,
        "xǁDECOǁ_estimate_correlation__mutmut_23": xǁDECOǁ_estimate_correlation__mutmut_23,
        "xǁDECOǁ_estimate_correlation__mutmut_24": xǁDECOǁ_estimate_correlation__mutmut_24,
        "xǁDECOǁ_estimate_correlation__mutmut_25": xǁDECOǁ_estimate_correlation__mutmut_25,
        "xǁDECOǁ_estimate_correlation__mutmut_26": xǁDECOǁ_estimate_correlation__mutmut_26,
        "xǁDECOǁ_estimate_correlation__mutmut_27": xǁDECOǁ_estimate_correlation__mutmut_27,
        "xǁDECOǁ_estimate_correlation__mutmut_28": xǁDECOǁ_estimate_correlation__mutmut_28,
        "xǁDECOǁ_estimate_correlation__mutmut_29": xǁDECOǁ_estimate_correlation__mutmut_29,
        "xǁDECOǁ_estimate_correlation__mutmut_30": xǁDECOǁ_estimate_correlation__mutmut_30,
        "xǁDECOǁ_estimate_correlation__mutmut_31": xǁDECOǁ_estimate_correlation__mutmut_31,
        "xǁDECOǁ_estimate_correlation__mutmut_32": xǁDECOǁ_estimate_correlation__mutmut_32,
        "xǁDECOǁ_estimate_correlation__mutmut_33": xǁDECOǁ_estimate_correlation__mutmut_33,
        "xǁDECOǁ_estimate_correlation__mutmut_34": xǁDECOǁ_estimate_correlation__mutmut_34,
        "xǁDECOǁ_estimate_correlation__mutmut_35": xǁDECOǁ_estimate_correlation__mutmut_35,
        "xǁDECOǁ_estimate_correlation__mutmut_36": xǁDECOǁ_estimate_correlation__mutmut_36,
        "xǁDECOǁ_estimate_correlation__mutmut_37": xǁDECOǁ_estimate_correlation__mutmut_37,
        "xǁDECOǁ_estimate_correlation__mutmut_38": xǁDECOǁ_estimate_correlation__mutmut_38,
        "xǁDECOǁ_estimate_correlation__mutmut_39": xǁDECOǁ_estimate_correlation__mutmut_39,
        "xǁDECOǁ_estimate_correlation__mutmut_40": xǁDECOǁ_estimate_correlation__mutmut_40,
        "xǁDECOǁ_estimate_correlation__mutmut_41": xǁDECOǁ_estimate_correlation__mutmut_41,
        "xǁDECOǁ_estimate_correlation__mutmut_42": xǁDECOǁ_estimate_correlation__mutmut_42,
        "xǁDECOǁ_estimate_correlation__mutmut_43": xǁDECOǁ_estimate_correlation__mutmut_43,
        "xǁDECOǁ_estimate_correlation__mutmut_44": xǁDECOǁ_estimate_correlation__mutmut_44,
        "xǁDECOǁ_estimate_correlation__mutmut_45": xǁDECOǁ_estimate_correlation__mutmut_45,
        "xǁDECOǁ_estimate_correlation__mutmut_46": xǁDECOǁ_estimate_correlation__mutmut_46,
        "xǁDECOǁ_estimate_correlation__mutmut_47": xǁDECOǁ_estimate_correlation__mutmut_47,
        "xǁDECOǁ_estimate_correlation__mutmut_48": xǁDECOǁ_estimate_correlation__mutmut_48,
        "xǁDECOǁ_estimate_correlation__mutmut_49": xǁDECOǁ_estimate_correlation__mutmut_49,
        "xǁDECOǁ_estimate_correlation__mutmut_50": xǁDECOǁ_estimate_correlation__mutmut_50,
        "xǁDECOǁ_estimate_correlation__mutmut_51": xǁDECOǁ_estimate_correlation__mutmut_51,
        "xǁDECOǁ_estimate_correlation__mutmut_52": xǁDECOǁ_estimate_correlation__mutmut_52,
        "xǁDECOǁ_estimate_correlation__mutmut_53": xǁDECOǁ_estimate_correlation__mutmut_53,
        "xǁDECOǁ_estimate_correlation__mutmut_54": xǁDECOǁ_estimate_correlation__mutmut_54,
        "xǁDECOǁ_estimate_correlation__mutmut_55": xǁDECOǁ_estimate_correlation__mutmut_55,
        "xǁDECOǁ_estimate_correlation__mutmut_56": xǁDECOǁ_estimate_correlation__mutmut_56,
        "xǁDECOǁ_estimate_correlation__mutmut_57": xǁDECOǁ_estimate_correlation__mutmut_57,
        "xǁDECOǁ_estimate_correlation__mutmut_58": xǁDECOǁ_estimate_correlation__mutmut_58,
        "xǁDECOǁ_estimate_correlation__mutmut_59": xǁDECOǁ_estimate_correlation__mutmut_59,
        "xǁDECOǁ_estimate_correlation__mutmut_60": xǁDECOǁ_estimate_correlation__mutmut_60,
        "xǁDECOǁ_estimate_correlation__mutmut_61": xǁDECOǁ_estimate_correlation__mutmut_61,
        "xǁDECOǁ_estimate_correlation__mutmut_62": xǁDECOǁ_estimate_correlation__mutmut_62,
        "xǁDECOǁ_estimate_correlation__mutmut_63": xǁDECOǁ_estimate_correlation__mutmut_63,
        "xǁDECOǁ_estimate_correlation__mutmut_64": xǁDECOǁ_estimate_correlation__mutmut_64,
        "xǁDECOǁ_estimate_correlation__mutmut_65": xǁDECOǁ_estimate_correlation__mutmut_65,
        "xǁDECOǁ_estimate_correlation__mutmut_66": xǁDECOǁ_estimate_correlation__mutmut_66,
        "xǁDECOǁ_estimate_correlation__mutmut_67": xǁDECOǁ_estimate_correlation__mutmut_67,
        "xǁDECOǁ_estimate_correlation__mutmut_68": xǁDECOǁ_estimate_correlation__mutmut_68,
        "xǁDECOǁ_estimate_correlation__mutmut_69": xǁDECOǁ_estimate_correlation__mutmut_69,
        "xǁDECOǁ_estimate_correlation__mutmut_70": xǁDECOǁ_estimate_correlation__mutmut_70,
        "xǁDECOǁ_estimate_correlation__mutmut_71": xǁDECOǁ_estimate_correlation__mutmut_71,
        "xǁDECOǁ_estimate_correlation__mutmut_72": xǁDECOǁ_estimate_correlation__mutmut_72,
        "xǁDECOǁ_estimate_correlation__mutmut_73": xǁDECOǁ_estimate_correlation__mutmut_73,
        "xǁDECOǁ_estimate_correlation__mutmut_74": xǁDECOǁ_estimate_correlation__mutmut_74,
        "xǁDECOǁ_estimate_correlation__mutmut_75": xǁDECOǁ_estimate_correlation__mutmut_75,
        "xǁDECOǁ_estimate_correlation__mutmut_76": xǁDECOǁ_estimate_correlation__mutmut_76,
        "xǁDECOǁ_estimate_correlation__mutmut_77": xǁDECOǁ_estimate_correlation__mutmut_77,
        "xǁDECOǁ_estimate_correlation__mutmut_78": xǁDECOǁ_estimate_correlation__mutmut_78,
        "xǁDECOǁ_estimate_correlation__mutmut_79": xǁDECOǁ_estimate_correlation__mutmut_79,
        "xǁDECOǁ_estimate_correlation__mutmut_80": xǁDECOǁ_estimate_correlation__mutmut_80,
        "xǁDECOǁ_estimate_correlation__mutmut_81": xǁDECOǁ_estimate_correlation__mutmut_81,
        "xǁDECOǁ_estimate_correlation__mutmut_82": xǁDECOǁ_estimate_correlation__mutmut_82,
        "xǁDECOǁ_estimate_correlation__mutmut_83": xǁDECOǁ_estimate_correlation__mutmut_83,
        "xǁDECOǁ_estimate_correlation__mutmut_84": xǁDECOǁ_estimate_correlation__mutmut_84,
        "xǁDECOǁ_estimate_correlation__mutmut_85": xǁDECOǁ_estimate_correlation__mutmut_85,
        "xǁDECOǁ_estimate_correlation__mutmut_86": xǁDECOǁ_estimate_correlation__mutmut_86,
        "xǁDECOǁ_estimate_correlation__mutmut_87": xǁDECOǁ_estimate_correlation__mutmut_87,
        "xǁDECOǁ_estimate_correlation__mutmut_88": xǁDECOǁ_estimate_correlation__mutmut_88,
        "xǁDECOǁ_estimate_correlation__mutmut_89": xǁDECOǁ_estimate_correlation__mutmut_89,
        "xǁDECOǁ_estimate_correlation__mutmut_90": xǁDECOǁ_estimate_correlation__mutmut_90,
    }
    xǁDECOǁ_estimate_correlation__mutmut_orig.__name__ = "xǁDECOǁ_estimate_correlation"

    @property
    def equicorrelation(self) -> NDArray[np.float64] | None:
        """Return the time-varying equicorrelation rho_t."""
        return self._rho_t

    def forecast(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        args = [results, horizon]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁDECOǁforecast__mutmut_orig"),
            object.__getattribute__(self, "xǁDECOǁforecast__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁDECOǁforecast__mutmut_orig(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_1(
        self,
        results: MultivarResults,
        horizon: int = 11,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_2(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_3(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_4(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = None
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_5(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[1], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_6(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[2]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_7(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = None
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_8(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a - b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_9(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = None

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_10(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = None
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_11(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(None)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_12(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = None

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_13(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones(None)

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_14(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = None

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_15(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[+1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_16(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-2]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_17(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = None
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_18(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = None
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_19(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(None)
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_20(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(None))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_21(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = None
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_22(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(None, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_23(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, None)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_24(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_25(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(
            d,
        )
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_26(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1.000000000001)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_27(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = None
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_28(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar * np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_29(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(None, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_30(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, None)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_31(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_32(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(
            d,
        )
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_33(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = None

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_34(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) * (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_35(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) + k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_36(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(None) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_37(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k / (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_38(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k + 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_39(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 2))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_40(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = None
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_41(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros(None)
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_42(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = None

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_43(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros(None)

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_44(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(None, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_45(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, None):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_46(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_47(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(
            1,
        ):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_48(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(2, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_49(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon - 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_50(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 2):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_51(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = None
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_52(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence * h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_53(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = None
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_54(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar - weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_55(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) / rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_56(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 + weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_57(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (2.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_58(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight / rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_59(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = None

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_60(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(None, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_61(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, None, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_62(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, None)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_63(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(-1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_64(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_65(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(
                rho_h,
                -1.0 / (k - 1) + 1e-6,
            )

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_66(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) - 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_67(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 * (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_68(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, +1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_69(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -2.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_70(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k + 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_71(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 2) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_72(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1.000001, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_73(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 + 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_74(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 2.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_75(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1.000001)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_76(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = None
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_77(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k - rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_78(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) / eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_79(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 + rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_80(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (2.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_81(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h / ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_82(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = None

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_83(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h + 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_84(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 2] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_85(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = None
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_86(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(None)
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_87(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[+1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_88(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-2])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_89(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = None

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_90(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h + 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_91(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 2] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_92(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"XXcovarianceXX": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_93(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"COVARIANCE": h_forecast, "correlation": r_forecast}

    def xǁDECOǁforecast__mutmut_94(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "XXcorrelationXX": r_forecast}

    def xǁDECOǁforecast__mutmut_95(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DECO dynamics.

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
        assert self._rho_t is not None
        assert self._q_bar is not None

        a, b = results.params[0], results.params[1]
        persistence = a + b
        k = self.k

        eye_k = np.eye(k)
        ones_k = np.ones((k, k))

        # Last rho
        rho_last = self._rho_t[-1]

        # Long-run rho (from Q_bar)
        q_bar = self._q_bar
        d = np.sqrt(np.diag(q_bar))
        d = np.maximum(d, 1e-12)
        r_bar = q_bar / np.outer(d, d)
        rho_bar = (np.sum(r_bar) - k) / (k * (k - 1))

        r_forecast = np.zeros((horizon, k, k))
        h_forecast = np.zeros((horizon, k, k))

        for h in range(1, horizon + 1):
            # rho converges to rho_bar
            weight = persistence**h
            rho_h = (1.0 - weight) * rho_bar + weight * rho_last
            rho_h = np.clip(rho_h, -1.0 / (k - 1) + 1e-6, 1.0 - 1e-6)

            r_h = (1.0 - rho_h) * eye_k + rho_h * ones_k
            r_forecast[h - 1] = r_h

            # Covariance
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "CORRELATION": r_forecast}

    xǁDECOǁforecast__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁDECOǁforecast__mutmut_1": xǁDECOǁforecast__mutmut_1,
        "xǁDECOǁforecast__mutmut_2": xǁDECOǁforecast__mutmut_2,
        "xǁDECOǁforecast__mutmut_3": xǁDECOǁforecast__mutmut_3,
        "xǁDECOǁforecast__mutmut_4": xǁDECOǁforecast__mutmut_4,
        "xǁDECOǁforecast__mutmut_5": xǁDECOǁforecast__mutmut_5,
        "xǁDECOǁforecast__mutmut_6": xǁDECOǁforecast__mutmut_6,
        "xǁDECOǁforecast__mutmut_7": xǁDECOǁforecast__mutmut_7,
        "xǁDECOǁforecast__mutmut_8": xǁDECOǁforecast__mutmut_8,
        "xǁDECOǁforecast__mutmut_9": xǁDECOǁforecast__mutmut_9,
        "xǁDECOǁforecast__mutmut_10": xǁDECOǁforecast__mutmut_10,
        "xǁDECOǁforecast__mutmut_11": xǁDECOǁforecast__mutmut_11,
        "xǁDECOǁforecast__mutmut_12": xǁDECOǁforecast__mutmut_12,
        "xǁDECOǁforecast__mutmut_13": xǁDECOǁforecast__mutmut_13,
        "xǁDECOǁforecast__mutmut_14": xǁDECOǁforecast__mutmut_14,
        "xǁDECOǁforecast__mutmut_15": xǁDECOǁforecast__mutmut_15,
        "xǁDECOǁforecast__mutmut_16": xǁDECOǁforecast__mutmut_16,
        "xǁDECOǁforecast__mutmut_17": xǁDECOǁforecast__mutmut_17,
        "xǁDECOǁforecast__mutmut_18": xǁDECOǁforecast__mutmut_18,
        "xǁDECOǁforecast__mutmut_19": xǁDECOǁforecast__mutmut_19,
        "xǁDECOǁforecast__mutmut_20": xǁDECOǁforecast__mutmut_20,
        "xǁDECOǁforecast__mutmut_21": xǁDECOǁforecast__mutmut_21,
        "xǁDECOǁforecast__mutmut_22": xǁDECOǁforecast__mutmut_22,
        "xǁDECOǁforecast__mutmut_23": xǁDECOǁforecast__mutmut_23,
        "xǁDECOǁforecast__mutmut_24": xǁDECOǁforecast__mutmut_24,
        "xǁDECOǁforecast__mutmut_25": xǁDECOǁforecast__mutmut_25,
        "xǁDECOǁforecast__mutmut_26": xǁDECOǁforecast__mutmut_26,
        "xǁDECOǁforecast__mutmut_27": xǁDECOǁforecast__mutmut_27,
        "xǁDECOǁforecast__mutmut_28": xǁDECOǁforecast__mutmut_28,
        "xǁDECOǁforecast__mutmut_29": xǁDECOǁforecast__mutmut_29,
        "xǁDECOǁforecast__mutmut_30": xǁDECOǁforecast__mutmut_30,
        "xǁDECOǁforecast__mutmut_31": xǁDECOǁforecast__mutmut_31,
        "xǁDECOǁforecast__mutmut_32": xǁDECOǁforecast__mutmut_32,
        "xǁDECOǁforecast__mutmut_33": xǁDECOǁforecast__mutmut_33,
        "xǁDECOǁforecast__mutmut_34": xǁDECOǁforecast__mutmut_34,
        "xǁDECOǁforecast__mutmut_35": xǁDECOǁforecast__mutmut_35,
        "xǁDECOǁforecast__mutmut_36": xǁDECOǁforecast__mutmut_36,
        "xǁDECOǁforecast__mutmut_37": xǁDECOǁforecast__mutmut_37,
        "xǁDECOǁforecast__mutmut_38": xǁDECOǁforecast__mutmut_38,
        "xǁDECOǁforecast__mutmut_39": xǁDECOǁforecast__mutmut_39,
        "xǁDECOǁforecast__mutmut_40": xǁDECOǁforecast__mutmut_40,
        "xǁDECOǁforecast__mutmut_41": xǁDECOǁforecast__mutmut_41,
        "xǁDECOǁforecast__mutmut_42": xǁDECOǁforecast__mutmut_42,
        "xǁDECOǁforecast__mutmut_43": xǁDECOǁforecast__mutmut_43,
        "xǁDECOǁforecast__mutmut_44": xǁDECOǁforecast__mutmut_44,
        "xǁDECOǁforecast__mutmut_45": xǁDECOǁforecast__mutmut_45,
        "xǁDECOǁforecast__mutmut_46": xǁDECOǁforecast__mutmut_46,
        "xǁDECOǁforecast__mutmut_47": xǁDECOǁforecast__mutmut_47,
        "xǁDECOǁforecast__mutmut_48": xǁDECOǁforecast__mutmut_48,
        "xǁDECOǁforecast__mutmut_49": xǁDECOǁforecast__mutmut_49,
        "xǁDECOǁforecast__mutmut_50": xǁDECOǁforecast__mutmut_50,
        "xǁDECOǁforecast__mutmut_51": xǁDECOǁforecast__mutmut_51,
        "xǁDECOǁforecast__mutmut_52": xǁDECOǁforecast__mutmut_52,
        "xǁDECOǁforecast__mutmut_53": xǁDECOǁforecast__mutmut_53,
        "xǁDECOǁforecast__mutmut_54": xǁDECOǁforecast__mutmut_54,
        "xǁDECOǁforecast__mutmut_55": xǁDECOǁforecast__mutmut_55,
        "xǁDECOǁforecast__mutmut_56": xǁDECOǁforecast__mutmut_56,
        "xǁDECOǁforecast__mutmut_57": xǁDECOǁforecast__mutmut_57,
        "xǁDECOǁforecast__mutmut_58": xǁDECOǁforecast__mutmut_58,
        "xǁDECOǁforecast__mutmut_59": xǁDECOǁforecast__mutmut_59,
        "xǁDECOǁforecast__mutmut_60": xǁDECOǁforecast__mutmut_60,
        "xǁDECOǁforecast__mutmut_61": xǁDECOǁforecast__mutmut_61,
        "xǁDECOǁforecast__mutmut_62": xǁDECOǁforecast__mutmut_62,
        "xǁDECOǁforecast__mutmut_63": xǁDECOǁforecast__mutmut_63,
        "xǁDECOǁforecast__mutmut_64": xǁDECOǁforecast__mutmut_64,
        "xǁDECOǁforecast__mutmut_65": xǁDECOǁforecast__mutmut_65,
        "xǁDECOǁforecast__mutmut_66": xǁDECOǁforecast__mutmut_66,
        "xǁDECOǁforecast__mutmut_67": xǁDECOǁforecast__mutmut_67,
        "xǁDECOǁforecast__mutmut_68": xǁDECOǁforecast__mutmut_68,
        "xǁDECOǁforecast__mutmut_69": xǁDECOǁforecast__mutmut_69,
        "xǁDECOǁforecast__mutmut_70": xǁDECOǁforecast__mutmut_70,
        "xǁDECOǁforecast__mutmut_71": xǁDECOǁforecast__mutmut_71,
        "xǁDECOǁforecast__mutmut_72": xǁDECOǁforecast__mutmut_72,
        "xǁDECOǁforecast__mutmut_73": xǁDECOǁforecast__mutmut_73,
        "xǁDECOǁforecast__mutmut_74": xǁDECOǁforecast__mutmut_74,
        "xǁDECOǁforecast__mutmut_75": xǁDECOǁforecast__mutmut_75,
        "xǁDECOǁforecast__mutmut_76": xǁDECOǁforecast__mutmut_76,
        "xǁDECOǁforecast__mutmut_77": xǁDECOǁforecast__mutmut_77,
        "xǁDECOǁforecast__mutmut_78": xǁDECOǁforecast__mutmut_78,
        "xǁDECOǁforecast__mutmut_79": xǁDECOǁforecast__mutmut_79,
        "xǁDECOǁforecast__mutmut_80": xǁDECOǁforecast__mutmut_80,
        "xǁDECOǁforecast__mutmut_81": xǁDECOǁforecast__mutmut_81,
        "xǁDECOǁforecast__mutmut_82": xǁDECOǁforecast__mutmut_82,
        "xǁDECOǁforecast__mutmut_83": xǁDECOǁforecast__mutmut_83,
        "xǁDECOǁforecast__mutmut_84": xǁDECOǁforecast__mutmut_84,
        "xǁDECOǁforecast__mutmut_85": xǁDECOǁforecast__mutmut_85,
        "xǁDECOǁforecast__mutmut_86": xǁDECOǁforecast__mutmut_86,
        "xǁDECOǁforecast__mutmut_87": xǁDECOǁforecast__mutmut_87,
        "xǁDECOǁforecast__mutmut_88": xǁDECOǁforecast__mutmut_88,
        "xǁDECOǁforecast__mutmut_89": xǁDECOǁforecast__mutmut_89,
        "xǁDECOǁforecast__mutmut_90": xǁDECOǁforecast__mutmut_90,
        "xǁDECOǁforecast__mutmut_91": xǁDECOǁforecast__mutmut_91,
        "xǁDECOǁforecast__mutmut_92": xǁDECOǁforecast__mutmut_92,
        "xǁDECOǁforecast__mutmut_93": xǁDECOǁforecast__mutmut_93,
        "xǁDECOǁforecast__mutmut_94": xǁDECOǁforecast__mutmut_94,
        "xǁDECOǁforecast__mutmut_95": xǁDECOǁforecast__mutmut_95,
    }
    xǁDECOǁforecast__mutmut_orig.__name__ = "xǁDECOǁforecast"
