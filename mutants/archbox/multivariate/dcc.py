"""DCC-GARCH: Dynamic Conditional Correlation model (Engle, 2002).

H_t = D_t * R_t * D_t

Where R_t evolves dynamically:
    Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
    R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}
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


class DCC(MultivariateVolatilityModel):
    """Dynamic Conditional Correlation GARCH model.

    The DCC model extends CCC by allowing the conditional correlation matrix
    to vary over time, governed by two parameters (a, b).

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
    >>> from archbox.multivariate.dcc import DCC
    >>> returns = np.random.randn(500, 3) * 0.01
    >>> model = DCC(returns)
    >>> results = model.fit()
    >>> print(results.summary())

    References
    ----------
    Engle, R.F. (2002). Dynamic Conditional Correlation: A Simple Class of
    Multivariate Generalized Autoregressive Conditional Heteroskedasticity Models.
    Journal of Business & Economic Statistics, 20(3), 339-350.
    """

    model_name: str = "DCC-GARCH"

    def __init__(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        args = [endog, univariate_model, univariate_order]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁDCCǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁDCCǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁDCCǁ__init____mutmut_orig(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize DCC-GARCH model with options."""
        super().__init__(endog, univariate_model, univariate_order)
        self._Q_bar: NDArray[np.float64] | None = None

    def xǁDCCǁ__init____mutmut_1(
        self,
        endog: Any,
        univariate_model: str = "XXGARCHXX",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize DCC-GARCH model with options."""
        super().__init__(endog, univariate_model, univariate_order)
        self._Q_bar: NDArray[np.float64] | None = None

    def xǁDCCǁ__init____mutmut_2(
        self,
        endog: Any,
        univariate_model: str = "garch",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize DCC-GARCH model with options."""
        super().__init__(endog, univariate_model, univariate_order)
        self._Q_bar: NDArray[np.float64] | None = None

    def xǁDCCǁ__init____mutmut_3(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize DCC-GARCH model with options."""
        super().__init__(None, univariate_model, univariate_order)
        self._Q_bar: NDArray[np.float64] | None = None

    def xǁDCCǁ__init____mutmut_4(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize DCC-GARCH model with options."""
        super().__init__(endog, None, univariate_order)
        self._Q_bar: NDArray[np.float64] | None = None

    def xǁDCCǁ__init____mutmut_5(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize DCC-GARCH model with options."""
        super().__init__(endog, univariate_model, None)
        self._Q_bar: NDArray[np.float64] | None = None

    def xǁDCCǁ__init____mutmut_6(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize DCC-GARCH model with options."""
        super().__init__(univariate_model, univariate_order)
        self._Q_bar: NDArray[np.float64] | None = None

    def xǁDCCǁ__init____mutmut_7(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize DCC-GARCH model with options."""
        super().__init__(endog, univariate_order)
        self._Q_bar: NDArray[np.float64] | None = None

    def xǁDCCǁ__init____mutmut_8(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize DCC-GARCH model with options."""
        super().__init__(
            endog,
            univariate_model,
        )
        self._Q_bar: NDArray[np.float64] | None = None

    def xǁDCCǁ__init____mutmut_9(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize DCC-GARCH model with options."""
        super().__init__(endog, univariate_model, univariate_order)
        self._Q_bar: NDArray[np.float64] | None = ""

    xǁDCCǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁDCCǁ__init____mutmut_1": xǁDCCǁ__init____mutmut_1,
        "xǁDCCǁ__init____mutmut_2": xǁDCCǁ__init____mutmut_2,
        "xǁDCCǁ__init____mutmut_3": xǁDCCǁ__init____mutmut_3,
        "xǁDCCǁ__init____mutmut_4": xǁDCCǁ__init____mutmut_4,
        "xǁDCCǁ__init____mutmut_5": xǁDCCǁ__init____mutmut_5,
        "xǁDCCǁ__init____mutmut_6": xǁDCCǁ__init____mutmut_6,
        "xǁDCCǁ__init____mutmut_7": xǁDCCǁ__init____mutmut_7,
        "xǁDCCǁ__init____mutmut_8": xǁDCCǁ__init____mutmut_8,
        "xǁDCCǁ__init____mutmut_9": xǁDCCǁ__init____mutmut_9,
    }
    xǁDCCǁ__init____mutmut_orig.__name__ = "xǁDCCǁ__init__"

    def _correlation_recursion(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        args = [params, std_resids]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁDCCǁ_correlation_recursion__mutmut_orig"),
            object.__getattribute__(self, "xǁDCCǁ_correlation_recursion__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁDCCǁ_correlation_recursion__mutmut_orig(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_1(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = None
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_2(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[1], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_3(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[2]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_4(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = None

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_5(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = None
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_6(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids * n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_7(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = None

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_8(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = None
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_9(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros(None)
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_10(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = None

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_11(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros(None)

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_12(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = None

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_13(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[1] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_14(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = None
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_15(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(None)
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_16(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(None))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_17(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[1]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_18(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = None
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_19(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(None, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_20(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, None)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_21(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_22(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(
            d,
        )
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_23(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1.000000000001)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_24(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = None

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_25(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[1] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_26(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] * np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_27(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[1] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_28(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(None, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_29(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, None)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_30(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_31(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(
            d,
        )

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_32(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(None, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_33(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, None):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_34(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_35(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(
            1,
        ):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_36(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(2, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_37(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = None  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_38(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t + 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_39(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 2 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_40(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = None

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_41(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) - b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_42(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar - a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_43(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) / q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_44(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a + b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_45(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 + a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_46(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (2.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_47(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a / (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_48(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b / q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_49(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t + 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_50(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 2]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_51(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = None
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_52(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(None)
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_53(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(None))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_54(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = None
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_55(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(None, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_56(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, None)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_57(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_58(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(
                d,
            )
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_59(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1.000000000001)
            r_mat[t] = q_mat[t] / np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_60(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = None

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_61(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] * np.outer(d, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_62(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(None, d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_63(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d, None)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_64(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(d)

        return r_mat

    def xǁDCCǁ_correlation_recursion__mutmut_65(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute dynamic correlation matrices R_t via DCC recursion.

        Q_t = (1-a-b)*Q_bar + a*z_{t-1}*z'_{t-1} + b*Q_{t-1}
        R_t = diag(Q_t)^{-1/2} * Q_t * diag(Q_t)^{-1/2}

        Parameters
        ----------
        params : ndarray
            DCC parameters [a, b].
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Dynamic correlation matrices, shape (T, k, k).
        """
        a, b = params[0], params[1]
        n_obs, k = std_resids.shape

        # Compute Q_bar (unconditional correlation of standardized residuals)
        q_bar = std_resids.T @ std_resids / n_obs
        self._Q_bar = q_bar

        q_mat = np.zeros((n_obs, k, k))
        r_mat = np.zeros((n_obs, k, k))

        # Initialize Q_0 = Q_bar
        q_mat[0] = q_bar.copy()

        # Normalize Q_0 to R_0
        d = np.sqrt(np.diag(q_mat[0]))
        d = np.maximum(d, 1e-12)
        r_mat[0] = q_mat[0] / np.outer(d, d)

        for t in range(1, n_obs):
            z = std_resids[t - 1 : t].T  # (k, 1)
            q_mat[t] = (1.0 - a - b) * q_bar + a * (z @ z.T) + b * q_mat[t - 1]

            # Normalize to correlation matrix
            d = np.sqrt(np.diag(q_mat[t]))
            d = np.maximum(d, 1e-12)
            r_mat[t] = q_mat[t] / np.outer(
                d,
            )

        return r_mat

    xǁDCCǁ_correlation_recursion__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁDCCǁ_correlation_recursion__mutmut_1": xǁDCCǁ_correlation_recursion__mutmut_1,
        "xǁDCCǁ_correlation_recursion__mutmut_2": xǁDCCǁ_correlation_recursion__mutmut_2,
        "xǁDCCǁ_correlation_recursion__mutmut_3": xǁDCCǁ_correlation_recursion__mutmut_3,
        "xǁDCCǁ_correlation_recursion__mutmut_4": xǁDCCǁ_correlation_recursion__mutmut_4,
        "xǁDCCǁ_correlation_recursion__mutmut_5": xǁDCCǁ_correlation_recursion__mutmut_5,
        "xǁDCCǁ_correlation_recursion__mutmut_6": xǁDCCǁ_correlation_recursion__mutmut_6,
        "xǁDCCǁ_correlation_recursion__mutmut_7": xǁDCCǁ_correlation_recursion__mutmut_7,
        "xǁDCCǁ_correlation_recursion__mutmut_8": xǁDCCǁ_correlation_recursion__mutmut_8,
        "xǁDCCǁ_correlation_recursion__mutmut_9": xǁDCCǁ_correlation_recursion__mutmut_9,
        "xǁDCCǁ_correlation_recursion__mutmut_10": xǁDCCǁ_correlation_recursion__mutmut_10,
        "xǁDCCǁ_correlation_recursion__mutmut_11": xǁDCCǁ_correlation_recursion__mutmut_11,
        "xǁDCCǁ_correlation_recursion__mutmut_12": xǁDCCǁ_correlation_recursion__mutmut_12,
        "xǁDCCǁ_correlation_recursion__mutmut_13": xǁDCCǁ_correlation_recursion__mutmut_13,
        "xǁDCCǁ_correlation_recursion__mutmut_14": xǁDCCǁ_correlation_recursion__mutmut_14,
        "xǁDCCǁ_correlation_recursion__mutmut_15": xǁDCCǁ_correlation_recursion__mutmut_15,
        "xǁDCCǁ_correlation_recursion__mutmut_16": xǁDCCǁ_correlation_recursion__mutmut_16,
        "xǁDCCǁ_correlation_recursion__mutmut_17": xǁDCCǁ_correlation_recursion__mutmut_17,
        "xǁDCCǁ_correlation_recursion__mutmut_18": xǁDCCǁ_correlation_recursion__mutmut_18,
        "xǁDCCǁ_correlation_recursion__mutmut_19": xǁDCCǁ_correlation_recursion__mutmut_19,
        "xǁDCCǁ_correlation_recursion__mutmut_20": xǁDCCǁ_correlation_recursion__mutmut_20,
        "xǁDCCǁ_correlation_recursion__mutmut_21": xǁDCCǁ_correlation_recursion__mutmut_21,
        "xǁDCCǁ_correlation_recursion__mutmut_22": xǁDCCǁ_correlation_recursion__mutmut_22,
        "xǁDCCǁ_correlation_recursion__mutmut_23": xǁDCCǁ_correlation_recursion__mutmut_23,
        "xǁDCCǁ_correlation_recursion__mutmut_24": xǁDCCǁ_correlation_recursion__mutmut_24,
        "xǁDCCǁ_correlation_recursion__mutmut_25": xǁDCCǁ_correlation_recursion__mutmut_25,
        "xǁDCCǁ_correlation_recursion__mutmut_26": xǁDCCǁ_correlation_recursion__mutmut_26,
        "xǁDCCǁ_correlation_recursion__mutmut_27": xǁDCCǁ_correlation_recursion__mutmut_27,
        "xǁDCCǁ_correlation_recursion__mutmut_28": xǁDCCǁ_correlation_recursion__mutmut_28,
        "xǁDCCǁ_correlation_recursion__mutmut_29": xǁDCCǁ_correlation_recursion__mutmut_29,
        "xǁDCCǁ_correlation_recursion__mutmut_30": xǁDCCǁ_correlation_recursion__mutmut_30,
        "xǁDCCǁ_correlation_recursion__mutmut_31": xǁDCCǁ_correlation_recursion__mutmut_31,
        "xǁDCCǁ_correlation_recursion__mutmut_32": xǁDCCǁ_correlation_recursion__mutmut_32,
        "xǁDCCǁ_correlation_recursion__mutmut_33": xǁDCCǁ_correlation_recursion__mutmut_33,
        "xǁDCCǁ_correlation_recursion__mutmut_34": xǁDCCǁ_correlation_recursion__mutmut_34,
        "xǁDCCǁ_correlation_recursion__mutmut_35": xǁDCCǁ_correlation_recursion__mutmut_35,
        "xǁDCCǁ_correlation_recursion__mutmut_36": xǁDCCǁ_correlation_recursion__mutmut_36,
        "xǁDCCǁ_correlation_recursion__mutmut_37": xǁDCCǁ_correlation_recursion__mutmut_37,
        "xǁDCCǁ_correlation_recursion__mutmut_38": xǁDCCǁ_correlation_recursion__mutmut_38,
        "xǁDCCǁ_correlation_recursion__mutmut_39": xǁDCCǁ_correlation_recursion__mutmut_39,
        "xǁDCCǁ_correlation_recursion__mutmut_40": xǁDCCǁ_correlation_recursion__mutmut_40,
        "xǁDCCǁ_correlation_recursion__mutmut_41": xǁDCCǁ_correlation_recursion__mutmut_41,
        "xǁDCCǁ_correlation_recursion__mutmut_42": xǁDCCǁ_correlation_recursion__mutmut_42,
        "xǁDCCǁ_correlation_recursion__mutmut_43": xǁDCCǁ_correlation_recursion__mutmut_43,
        "xǁDCCǁ_correlation_recursion__mutmut_44": xǁDCCǁ_correlation_recursion__mutmut_44,
        "xǁDCCǁ_correlation_recursion__mutmut_45": xǁDCCǁ_correlation_recursion__mutmut_45,
        "xǁDCCǁ_correlation_recursion__mutmut_46": xǁDCCǁ_correlation_recursion__mutmut_46,
        "xǁDCCǁ_correlation_recursion__mutmut_47": xǁDCCǁ_correlation_recursion__mutmut_47,
        "xǁDCCǁ_correlation_recursion__mutmut_48": xǁDCCǁ_correlation_recursion__mutmut_48,
        "xǁDCCǁ_correlation_recursion__mutmut_49": xǁDCCǁ_correlation_recursion__mutmut_49,
        "xǁDCCǁ_correlation_recursion__mutmut_50": xǁDCCǁ_correlation_recursion__mutmut_50,
        "xǁDCCǁ_correlation_recursion__mutmut_51": xǁDCCǁ_correlation_recursion__mutmut_51,
        "xǁDCCǁ_correlation_recursion__mutmut_52": xǁDCCǁ_correlation_recursion__mutmut_52,
        "xǁDCCǁ_correlation_recursion__mutmut_53": xǁDCCǁ_correlation_recursion__mutmut_53,
        "xǁDCCǁ_correlation_recursion__mutmut_54": xǁDCCǁ_correlation_recursion__mutmut_54,
        "xǁDCCǁ_correlation_recursion__mutmut_55": xǁDCCǁ_correlation_recursion__mutmut_55,
        "xǁDCCǁ_correlation_recursion__mutmut_56": xǁDCCǁ_correlation_recursion__mutmut_56,
        "xǁDCCǁ_correlation_recursion__mutmut_57": xǁDCCǁ_correlation_recursion__mutmut_57,
        "xǁDCCǁ_correlation_recursion__mutmut_58": xǁDCCǁ_correlation_recursion__mutmut_58,
        "xǁDCCǁ_correlation_recursion__mutmut_59": xǁDCCǁ_correlation_recursion__mutmut_59,
        "xǁDCCǁ_correlation_recursion__mutmut_60": xǁDCCǁ_correlation_recursion__mutmut_60,
        "xǁDCCǁ_correlation_recursion__mutmut_61": xǁDCCǁ_correlation_recursion__mutmut_61,
        "xǁDCCǁ_correlation_recursion__mutmut_62": xǁDCCǁ_correlation_recursion__mutmut_62,
        "xǁDCCǁ_correlation_recursion__mutmut_63": xǁDCCǁ_correlation_recursion__mutmut_63,
        "xǁDCCǁ_correlation_recursion__mutmut_64": xǁDCCǁ_correlation_recursion__mutmut_64,
        "xǁDCCǁ_correlation_recursion__mutmut_65": xǁDCCǁ_correlation_recursion__mutmut_65,
    }
    xǁDCCǁ_correlation_recursion__mutmut_orig.__name__ = "xǁDCCǁ_correlation_recursion"

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values: a=0.05, b=0.90."""
        return np.array([0.05, 0.90])

    @property
    def param_names(self) -> list[str]:
        """DCC parameter names."""
        return ["a", "b"]

    def _param_bounds(self) -> list[tuple[float, float]]:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁDCCǁ_param_bounds__mutmut_orig"),
            object.__getattribute__(self, "xǁDCCǁ_param_bounds__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁDCCǁ_param_bounds__mutmut_orig(self) -> list[tuple[float, float]]:
        """Parameter bounds: a > 0, b > 0, a+b < 1."""
        return [(1e-6, 0.499), (1e-6, 0.9999)]

    def xǁDCCǁ_param_bounds__mutmut_1(self) -> list[tuple[float, float]]:
        """Parameter bounds: a > 0, b > 0, a+b < 1."""
        return [(1.000001, 0.499), (1e-6, 0.9999)]

    def xǁDCCǁ_param_bounds__mutmut_2(self) -> list[tuple[float, float]]:
        """Parameter bounds: a > 0, b > 0, a+b < 1."""
        return [(1e-6, 1.499), (1e-6, 0.9999)]

    def xǁDCCǁ_param_bounds__mutmut_3(self) -> list[tuple[float, float]]:
        """Parameter bounds: a > 0, b > 0, a+b < 1."""
        return [(1e-6, 0.499), (1.000001, 0.9999)]

    def xǁDCCǁ_param_bounds__mutmut_4(self) -> list[tuple[float, float]]:
        """Parameter bounds: a > 0, b > 0, a+b < 1."""
        return [(1e-6, 0.499), (1e-6, 1.9999)]

    xǁDCCǁ_param_bounds__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁDCCǁ_param_bounds__mutmut_1": xǁDCCǁ_param_bounds__mutmut_1,
        "xǁDCCǁ_param_bounds__mutmut_2": xǁDCCǁ_param_bounds__mutmut_2,
        "xǁDCCǁ_param_bounds__mutmut_3": xǁDCCǁ_param_bounds__mutmut_3,
        "xǁDCCǁ_param_bounds__mutmut_4": xǁDCCǁ_param_bounds__mutmut_4,
    }
    xǁDCCǁ_param_bounds__mutmut_orig.__name__ = "xǁDCCǁ_param_bounds"

    def _estimate_correlation(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        args = [std_resids, disp]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁDCCǁ_estimate_correlation__mutmut_orig"),
            object.__getattribute__(self, "xǁDCCǁ_estimate_correlation__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁDCCǁ_estimate_correlation__mutmut_orig(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_1(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = False,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_2(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = None

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_3(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[1], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_4(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[2]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_5(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_6(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_7(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_8(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_9(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_10(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_11(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_12(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_13(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_14(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_15(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_16(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_17(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_18(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_19(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_20(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_21(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_22(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_23(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_24(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_25(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_26(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_27(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_28(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_29(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_30(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_31(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_32(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_33(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_34(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_35(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_36(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_37(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_38(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_39(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_40(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_41(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_42(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_43(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_44(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_45(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_46(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_47(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_48(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_49(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_50(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = None

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_51(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"XXtypeXX": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_52(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"TYPE": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_53(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "XXineqXX", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_54(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "INEQ", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_55(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "XXfunXX": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_56(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "FUN": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_57(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: None},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_58(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] + p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_59(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 + p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_60(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 1.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_61(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[1] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_62(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[2]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_63(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = None

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_64(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = None

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_65(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array(None),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_66(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1.000001, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_67(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1.000001]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_68(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array(None),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_69(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([1.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_70(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 1.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_71(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array(None),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_72(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([1.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_73(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 1.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_74(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array(None),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_75(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([1.1, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_76(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 1.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_77(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = None
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_78(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = None

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_79(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = None
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_80(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                None,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_81(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                None,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_82(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method=None,
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_83(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=None,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_84(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=None,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_85(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options=None,
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_86(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_87(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_88(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_89(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_90(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_91(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_92(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="XXSLSQPXX",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_93(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="slsqp",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_94(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"XXmaxiterXX": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_95(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"MAXITER": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_96(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 501, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_97(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "XXdispXX": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_98(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "DISP": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_99(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "XXftolXX": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_100(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "FTOL": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_101(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1.00000001},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_102(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun <= best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_103(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = None
                best_x = result.x

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_104(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = None

        return np.asarray(best_x, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_105(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(None, dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_106(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(best_x, dtype=None)

    def xǁDCCǁ_estimate_correlation__mutmut_107(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(dtype=np.float64)

    def xǁDCCǁ_estimate_correlation__mutmut_108(
        self,
        std_resids: NDArray[np.float64],
        disp: bool = True,
    ) -> NDArray[np.float64]:
        """Estimate DCC parameters (a, b) via MLE.

        Maximizes the DCC part of the log-likelihood:
        loglike_DCC = -0.5 * sum_t [ log|R_t| + z_t' R_t^{-1} z_t - z_t' z_t ]

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

        def neg_loglike(params: NDArray[np.float64]) -> float:
            """Compute negative correlation log-likelihood for DCC."""
            a, b = params[0], params[1]

            # Enforce a + b < 1
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

        # Constraint: a + b < 1
        constraints: list[dict[str, Any]] = [
            {"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]},
        ]

        bounds = self._param_bounds()

        # Try multiple starting points and keep the best
        starting_points = [
            self.start_params,
            np.array([1e-6, 1e-6]),  # Near CCC (a~0, b~0)
            np.array([0.01, 0.01]),
            np.array([0.02, 0.95]),
            np.array([0.10, 0.85]),
        ]

        best_val = np.inf
        best_x = self.start_params

        for x0 in starting_points:
            result = optimize.minimize(
                neg_loglike,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 500, "disp": disp, "ftol": 1e-8},
            )
            if result.fun < best_val:
                best_val = result.fun
                best_x = result.x

        return np.asarray(
            best_x,
        )

    xǁDCCǁ_estimate_correlation__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁDCCǁ_estimate_correlation__mutmut_1": xǁDCCǁ_estimate_correlation__mutmut_1,
        "xǁDCCǁ_estimate_correlation__mutmut_2": xǁDCCǁ_estimate_correlation__mutmut_2,
        "xǁDCCǁ_estimate_correlation__mutmut_3": xǁDCCǁ_estimate_correlation__mutmut_3,
        "xǁDCCǁ_estimate_correlation__mutmut_4": xǁDCCǁ_estimate_correlation__mutmut_4,
        "xǁDCCǁ_estimate_correlation__mutmut_5": xǁDCCǁ_estimate_correlation__mutmut_5,
        "xǁDCCǁ_estimate_correlation__mutmut_6": xǁDCCǁ_estimate_correlation__mutmut_6,
        "xǁDCCǁ_estimate_correlation__mutmut_7": xǁDCCǁ_estimate_correlation__mutmut_7,
        "xǁDCCǁ_estimate_correlation__mutmut_8": xǁDCCǁ_estimate_correlation__mutmut_8,
        "xǁDCCǁ_estimate_correlation__mutmut_9": xǁDCCǁ_estimate_correlation__mutmut_9,
        "xǁDCCǁ_estimate_correlation__mutmut_10": xǁDCCǁ_estimate_correlation__mutmut_10,
        "xǁDCCǁ_estimate_correlation__mutmut_11": xǁDCCǁ_estimate_correlation__mutmut_11,
        "xǁDCCǁ_estimate_correlation__mutmut_12": xǁDCCǁ_estimate_correlation__mutmut_12,
        "xǁDCCǁ_estimate_correlation__mutmut_13": xǁDCCǁ_estimate_correlation__mutmut_13,
        "xǁDCCǁ_estimate_correlation__mutmut_14": xǁDCCǁ_estimate_correlation__mutmut_14,
        "xǁDCCǁ_estimate_correlation__mutmut_15": xǁDCCǁ_estimate_correlation__mutmut_15,
        "xǁDCCǁ_estimate_correlation__mutmut_16": xǁDCCǁ_estimate_correlation__mutmut_16,
        "xǁDCCǁ_estimate_correlation__mutmut_17": xǁDCCǁ_estimate_correlation__mutmut_17,
        "xǁDCCǁ_estimate_correlation__mutmut_18": xǁDCCǁ_estimate_correlation__mutmut_18,
        "xǁDCCǁ_estimate_correlation__mutmut_19": xǁDCCǁ_estimate_correlation__mutmut_19,
        "xǁDCCǁ_estimate_correlation__mutmut_20": xǁDCCǁ_estimate_correlation__mutmut_20,
        "xǁDCCǁ_estimate_correlation__mutmut_21": xǁDCCǁ_estimate_correlation__mutmut_21,
        "xǁDCCǁ_estimate_correlation__mutmut_22": xǁDCCǁ_estimate_correlation__mutmut_22,
        "xǁDCCǁ_estimate_correlation__mutmut_23": xǁDCCǁ_estimate_correlation__mutmut_23,
        "xǁDCCǁ_estimate_correlation__mutmut_24": xǁDCCǁ_estimate_correlation__mutmut_24,
        "xǁDCCǁ_estimate_correlation__mutmut_25": xǁDCCǁ_estimate_correlation__mutmut_25,
        "xǁDCCǁ_estimate_correlation__mutmut_26": xǁDCCǁ_estimate_correlation__mutmut_26,
        "xǁDCCǁ_estimate_correlation__mutmut_27": xǁDCCǁ_estimate_correlation__mutmut_27,
        "xǁDCCǁ_estimate_correlation__mutmut_28": xǁDCCǁ_estimate_correlation__mutmut_28,
        "xǁDCCǁ_estimate_correlation__mutmut_29": xǁDCCǁ_estimate_correlation__mutmut_29,
        "xǁDCCǁ_estimate_correlation__mutmut_30": xǁDCCǁ_estimate_correlation__mutmut_30,
        "xǁDCCǁ_estimate_correlation__mutmut_31": xǁDCCǁ_estimate_correlation__mutmut_31,
        "xǁDCCǁ_estimate_correlation__mutmut_32": xǁDCCǁ_estimate_correlation__mutmut_32,
        "xǁDCCǁ_estimate_correlation__mutmut_33": xǁDCCǁ_estimate_correlation__mutmut_33,
        "xǁDCCǁ_estimate_correlation__mutmut_34": xǁDCCǁ_estimate_correlation__mutmut_34,
        "xǁDCCǁ_estimate_correlation__mutmut_35": xǁDCCǁ_estimate_correlation__mutmut_35,
        "xǁDCCǁ_estimate_correlation__mutmut_36": xǁDCCǁ_estimate_correlation__mutmut_36,
        "xǁDCCǁ_estimate_correlation__mutmut_37": xǁDCCǁ_estimate_correlation__mutmut_37,
        "xǁDCCǁ_estimate_correlation__mutmut_38": xǁDCCǁ_estimate_correlation__mutmut_38,
        "xǁDCCǁ_estimate_correlation__mutmut_39": xǁDCCǁ_estimate_correlation__mutmut_39,
        "xǁDCCǁ_estimate_correlation__mutmut_40": xǁDCCǁ_estimate_correlation__mutmut_40,
        "xǁDCCǁ_estimate_correlation__mutmut_41": xǁDCCǁ_estimate_correlation__mutmut_41,
        "xǁDCCǁ_estimate_correlation__mutmut_42": xǁDCCǁ_estimate_correlation__mutmut_42,
        "xǁDCCǁ_estimate_correlation__mutmut_43": xǁDCCǁ_estimate_correlation__mutmut_43,
        "xǁDCCǁ_estimate_correlation__mutmut_44": xǁDCCǁ_estimate_correlation__mutmut_44,
        "xǁDCCǁ_estimate_correlation__mutmut_45": xǁDCCǁ_estimate_correlation__mutmut_45,
        "xǁDCCǁ_estimate_correlation__mutmut_46": xǁDCCǁ_estimate_correlation__mutmut_46,
        "xǁDCCǁ_estimate_correlation__mutmut_47": xǁDCCǁ_estimate_correlation__mutmut_47,
        "xǁDCCǁ_estimate_correlation__mutmut_48": xǁDCCǁ_estimate_correlation__mutmut_48,
        "xǁDCCǁ_estimate_correlation__mutmut_49": xǁDCCǁ_estimate_correlation__mutmut_49,
        "xǁDCCǁ_estimate_correlation__mutmut_50": xǁDCCǁ_estimate_correlation__mutmut_50,
        "xǁDCCǁ_estimate_correlation__mutmut_51": xǁDCCǁ_estimate_correlation__mutmut_51,
        "xǁDCCǁ_estimate_correlation__mutmut_52": xǁDCCǁ_estimate_correlation__mutmut_52,
        "xǁDCCǁ_estimate_correlation__mutmut_53": xǁDCCǁ_estimate_correlation__mutmut_53,
        "xǁDCCǁ_estimate_correlation__mutmut_54": xǁDCCǁ_estimate_correlation__mutmut_54,
        "xǁDCCǁ_estimate_correlation__mutmut_55": xǁDCCǁ_estimate_correlation__mutmut_55,
        "xǁDCCǁ_estimate_correlation__mutmut_56": xǁDCCǁ_estimate_correlation__mutmut_56,
        "xǁDCCǁ_estimate_correlation__mutmut_57": xǁDCCǁ_estimate_correlation__mutmut_57,
        "xǁDCCǁ_estimate_correlation__mutmut_58": xǁDCCǁ_estimate_correlation__mutmut_58,
        "xǁDCCǁ_estimate_correlation__mutmut_59": xǁDCCǁ_estimate_correlation__mutmut_59,
        "xǁDCCǁ_estimate_correlation__mutmut_60": xǁDCCǁ_estimate_correlation__mutmut_60,
        "xǁDCCǁ_estimate_correlation__mutmut_61": xǁDCCǁ_estimate_correlation__mutmut_61,
        "xǁDCCǁ_estimate_correlation__mutmut_62": xǁDCCǁ_estimate_correlation__mutmut_62,
        "xǁDCCǁ_estimate_correlation__mutmut_63": xǁDCCǁ_estimate_correlation__mutmut_63,
        "xǁDCCǁ_estimate_correlation__mutmut_64": xǁDCCǁ_estimate_correlation__mutmut_64,
        "xǁDCCǁ_estimate_correlation__mutmut_65": xǁDCCǁ_estimate_correlation__mutmut_65,
        "xǁDCCǁ_estimate_correlation__mutmut_66": xǁDCCǁ_estimate_correlation__mutmut_66,
        "xǁDCCǁ_estimate_correlation__mutmut_67": xǁDCCǁ_estimate_correlation__mutmut_67,
        "xǁDCCǁ_estimate_correlation__mutmut_68": xǁDCCǁ_estimate_correlation__mutmut_68,
        "xǁDCCǁ_estimate_correlation__mutmut_69": xǁDCCǁ_estimate_correlation__mutmut_69,
        "xǁDCCǁ_estimate_correlation__mutmut_70": xǁDCCǁ_estimate_correlation__mutmut_70,
        "xǁDCCǁ_estimate_correlation__mutmut_71": xǁDCCǁ_estimate_correlation__mutmut_71,
        "xǁDCCǁ_estimate_correlation__mutmut_72": xǁDCCǁ_estimate_correlation__mutmut_72,
        "xǁDCCǁ_estimate_correlation__mutmut_73": xǁDCCǁ_estimate_correlation__mutmut_73,
        "xǁDCCǁ_estimate_correlation__mutmut_74": xǁDCCǁ_estimate_correlation__mutmut_74,
        "xǁDCCǁ_estimate_correlation__mutmut_75": xǁDCCǁ_estimate_correlation__mutmut_75,
        "xǁDCCǁ_estimate_correlation__mutmut_76": xǁDCCǁ_estimate_correlation__mutmut_76,
        "xǁDCCǁ_estimate_correlation__mutmut_77": xǁDCCǁ_estimate_correlation__mutmut_77,
        "xǁDCCǁ_estimate_correlation__mutmut_78": xǁDCCǁ_estimate_correlation__mutmut_78,
        "xǁDCCǁ_estimate_correlation__mutmut_79": xǁDCCǁ_estimate_correlation__mutmut_79,
        "xǁDCCǁ_estimate_correlation__mutmut_80": xǁDCCǁ_estimate_correlation__mutmut_80,
        "xǁDCCǁ_estimate_correlation__mutmut_81": xǁDCCǁ_estimate_correlation__mutmut_81,
        "xǁDCCǁ_estimate_correlation__mutmut_82": xǁDCCǁ_estimate_correlation__mutmut_82,
        "xǁDCCǁ_estimate_correlation__mutmut_83": xǁDCCǁ_estimate_correlation__mutmut_83,
        "xǁDCCǁ_estimate_correlation__mutmut_84": xǁDCCǁ_estimate_correlation__mutmut_84,
        "xǁDCCǁ_estimate_correlation__mutmut_85": xǁDCCǁ_estimate_correlation__mutmut_85,
        "xǁDCCǁ_estimate_correlation__mutmut_86": xǁDCCǁ_estimate_correlation__mutmut_86,
        "xǁDCCǁ_estimate_correlation__mutmut_87": xǁDCCǁ_estimate_correlation__mutmut_87,
        "xǁDCCǁ_estimate_correlation__mutmut_88": xǁDCCǁ_estimate_correlation__mutmut_88,
        "xǁDCCǁ_estimate_correlation__mutmut_89": xǁDCCǁ_estimate_correlation__mutmut_89,
        "xǁDCCǁ_estimate_correlation__mutmut_90": xǁDCCǁ_estimate_correlation__mutmut_90,
        "xǁDCCǁ_estimate_correlation__mutmut_91": xǁDCCǁ_estimate_correlation__mutmut_91,
        "xǁDCCǁ_estimate_correlation__mutmut_92": xǁDCCǁ_estimate_correlation__mutmut_92,
        "xǁDCCǁ_estimate_correlation__mutmut_93": xǁDCCǁ_estimate_correlation__mutmut_93,
        "xǁDCCǁ_estimate_correlation__mutmut_94": xǁDCCǁ_estimate_correlation__mutmut_94,
        "xǁDCCǁ_estimate_correlation__mutmut_95": xǁDCCǁ_estimate_correlation__mutmut_95,
        "xǁDCCǁ_estimate_correlation__mutmut_96": xǁDCCǁ_estimate_correlation__mutmut_96,
        "xǁDCCǁ_estimate_correlation__mutmut_97": xǁDCCǁ_estimate_correlation__mutmut_97,
        "xǁDCCǁ_estimate_correlation__mutmut_98": xǁDCCǁ_estimate_correlation__mutmut_98,
        "xǁDCCǁ_estimate_correlation__mutmut_99": xǁDCCǁ_estimate_correlation__mutmut_99,
        "xǁDCCǁ_estimate_correlation__mutmut_100": xǁDCCǁ_estimate_correlation__mutmut_100,
        "xǁDCCǁ_estimate_correlation__mutmut_101": xǁDCCǁ_estimate_correlation__mutmut_101,
        "xǁDCCǁ_estimate_correlation__mutmut_102": xǁDCCǁ_estimate_correlation__mutmut_102,
        "xǁDCCǁ_estimate_correlation__mutmut_103": xǁDCCǁ_estimate_correlation__mutmut_103,
        "xǁDCCǁ_estimate_correlation__mutmut_104": xǁDCCǁ_estimate_correlation__mutmut_104,
        "xǁDCCǁ_estimate_correlation__mutmut_105": xǁDCCǁ_estimate_correlation__mutmut_105,
        "xǁDCCǁ_estimate_correlation__mutmut_106": xǁDCCǁ_estimate_correlation__mutmut_106,
        "xǁDCCǁ_estimate_correlation__mutmut_107": xǁDCCǁ_estimate_correlation__mutmut_107,
        "xǁDCCǁ_estimate_correlation__mutmut_108": xǁDCCǁ_estimate_correlation__mutmut_108,
    }
    xǁDCCǁ_estimate_correlation__mutmut_orig.__name__ = "xǁDCCǁ_estimate_correlation"

    def forecast(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        args = [results, horizon]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁDCCǁforecast__mutmut_orig"),
            object.__getattribute__(self, "xǁDCCǁforecast__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁDCCǁforecast__mutmut_orig(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_1(
        self,
        results: MultivarResults,
        horizon: int = 11,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_2(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_3(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = None
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_4(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[1], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_5(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[2]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_6(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = None

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_7(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a - b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_8(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = None
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_9(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = None  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_10(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[+1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_11(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-2].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_12(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = None
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_13(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros(None)
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_14(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = None

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_15(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros(None)

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_16(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(None, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_17(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, None):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_18(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_19(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(
            1,
        ):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_20(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(2, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_21(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon - 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_22(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 2):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_23(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = None
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_24(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence * h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_25(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = None

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_26(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar - weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_27(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) / q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_28(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 + weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_29(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (2.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_30(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight / q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_31(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = None
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_32(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(None)
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_33(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(None))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_34(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = None
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_35(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(None, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_36(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, None)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_37(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_38(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(
                d,
            )
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_39(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1.000000000001)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_40(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = None
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_41(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h * np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_42(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(None, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_43(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, None)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_44(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_45(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(
                d,
            )
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_46(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = None

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_47(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h + 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_48(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 2] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_49(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = None
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_50(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(None)
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_51(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[+1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_52(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-2])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_53(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = None

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_54(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h + 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_55(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 2] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_56(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"XXcovarianceXX": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_57(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"COVARIANCE": h_forecast, "correlation": r_forecast}

    def xǁDCCǁforecast__mutmut_58(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "XXcorrelationXX": r_forecast}

    def xǁDCCǁforecast__mutmut_59(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} using DCC dynamics.

        Q_{T+h} converges to Q_bar:
            Q_{T+h} = (1 - (a+b)^h) * Q_bar + (a+b)^h * Q_T

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
        assert self._Q_bar is not None
        a, b = results.params[0], results.params[1]
        persistence = a + b

        q_bar = self._Q_bar
        # Last Q_t can be approximated from last R_t and denormalization
        q_last = results.dynamic_correlation[-1].copy()  # Approximate with R_T

        r_forecast = np.zeros((horizon, self.k, self.k))
        h_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(1, horizon + 1):
            # Q_{T+h} converges to Q_bar
            weight = persistence**h
            q_h = (1.0 - weight) * q_bar + weight * q_last

            # Normalize to correlation
            d = np.sqrt(np.diag(q_h))
            d = np.maximum(d, 1e-12)
            r_h = q_h / np.outer(d, d)
            r_forecast[h - 1] = r_h

            # Covariance: use last volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            h_forecast[h - 1] = d_mat @ r_h @ d_mat

        return {"covariance": h_forecast, "CORRELATION": r_forecast}

    xǁDCCǁforecast__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁDCCǁforecast__mutmut_1": xǁDCCǁforecast__mutmut_1,
        "xǁDCCǁforecast__mutmut_2": xǁDCCǁforecast__mutmut_2,
        "xǁDCCǁforecast__mutmut_3": xǁDCCǁforecast__mutmut_3,
        "xǁDCCǁforecast__mutmut_4": xǁDCCǁforecast__mutmut_4,
        "xǁDCCǁforecast__mutmut_5": xǁDCCǁforecast__mutmut_5,
        "xǁDCCǁforecast__mutmut_6": xǁDCCǁforecast__mutmut_6,
        "xǁDCCǁforecast__mutmut_7": xǁDCCǁforecast__mutmut_7,
        "xǁDCCǁforecast__mutmut_8": xǁDCCǁforecast__mutmut_8,
        "xǁDCCǁforecast__mutmut_9": xǁDCCǁforecast__mutmut_9,
        "xǁDCCǁforecast__mutmut_10": xǁDCCǁforecast__mutmut_10,
        "xǁDCCǁforecast__mutmut_11": xǁDCCǁforecast__mutmut_11,
        "xǁDCCǁforecast__mutmut_12": xǁDCCǁforecast__mutmut_12,
        "xǁDCCǁforecast__mutmut_13": xǁDCCǁforecast__mutmut_13,
        "xǁDCCǁforecast__mutmut_14": xǁDCCǁforecast__mutmut_14,
        "xǁDCCǁforecast__mutmut_15": xǁDCCǁforecast__mutmut_15,
        "xǁDCCǁforecast__mutmut_16": xǁDCCǁforecast__mutmut_16,
        "xǁDCCǁforecast__mutmut_17": xǁDCCǁforecast__mutmut_17,
        "xǁDCCǁforecast__mutmut_18": xǁDCCǁforecast__mutmut_18,
        "xǁDCCǁforecast__mutmut_19": xǁDCCǁforecast__mutmut_19,
        "xǁDCCǁforecast__mutmut_20": xǁDCCǁforecast__mutmut_20,
        "xǁDCCǁforecast__mutmut_21": xǁDCCǁforecast__mutmut_21,
        "xǁDCCǁforecast__mutmut_22": xǁDCCǁforecast__mutmut_22,
        "xǁDCCǁforecast__mutmut_23": xǁDCCǁforecast__mutmut_23,
        "xǁDCCǁforecast__mutmut_24": xǁDCCǁforecast__mutmut_24,
        "xǁDCCǁforecast__mutmut_25": xǁDCCǁforecast__mutmut_25,
        "xǁDCCǁforecast__mutmut_26": xǁDCCǁforecast__mutmut_26,
        "xǁDCCǁforecast__mutmut_27": xǁDCCǁforecast__mutmut_27,
        "xǁDCCǁforecast__mutmut_28": xǁDCCǁforecast__mutmut_28,
        "xǁDCCǁforecast__mutmut_29": xǁDCCǁforecast__mutmut_29,
        "xǁDCCǁforecast__mutmut_30": xǁDCCǁforecast__mutmut_30,
        "xǁDCCǁforecast__mutmut_31": xǁDCCǁforecast__mutmut_31,
        "xǁDCCǁforecast__mutmut_32": xǁDCCǁforecast__mutmut_32,
        "xǁDCCǁforecast__mutmut_33": xǁDCCǁforecast__mutmut_33,
        "xǁDCCǁforecast__mutmut_34": xǁDCCǁforecast__mutmut_34,
        "xǁDCCǁforecast__mutmut_35": xǁDCCǁforecast__mutmut_35,
        "xǁDCCǁforecast__mutmut_36": xǁDCCǁforecast__mutmut_36,
        "xǁDCCǁforecast__mutmut_37": xǁDCCǁforecast__mutmut_37,
        "xǁDCCǁforecast__mutmut_38": xǁDCCǁforecast__mutmut_38,
        "xǁDCCǁforecast__mutmut_39": xǁDCCǁforecast__mutmut_39,
        "xǁDCCǁforecast__mutmut_40": xǁDCCǁforecast__mutmut_40,
        "xǁDCCǁforecast__mutmut_41": xǁDCCǁforecast__mutmut_41,
        "xǁDCCǁforecast__mutmut_42": xǁDCCǁforecast__mutmut_42,
        "xǁDCCǁforecast__mutmut_43": xǁDCCǁforecast__mutmut_43,
        "xǁDCCǁforecast__mutmut_44": xǁDCCǁforecast__mutmut_44,
        "xǁDCCǁforecast__mutmut_45": xǁDCCǁforecast__mutmut_45,
        "xǁDCCǁforecast__mutmut_46": xǁDCCǁforecast__mutmut_46,
        "xǁDCCǁforecast__mutmut_47": xǁDCCǁforecast__mutmut_47,
        "xǁDCCǁforecast__mutmut_48": xǁDCCǁforecast__mutmut_48,
        "xǁDCCǁforecast__mutmut_49": xǁDCCǁforecast__mutmut_49,
        "xǁDCCǁforecast__mutmut_50": xǁDCCǁforecast__mutmut_50,
        "xǁDCCǁforecast__mutmut_51": xǁDCCǁforecast__mutmut_51,
        "xǁDCCǁforecast__mutmut_52": xǁDCCǁforecast__mutmut_52,
        "xǁDCCǁforecast__mutmut_53": xǁDCCǁforecast__mutmut_53,
        "xǁDCCǁforecast__mutmut_54": xǁDCCǁforecast__mutmut_54,
        "xǁDCCǁforecast__mutmut_55": xǁDCCǁforecast__mutmut_55,
        "xǁDCCǁforecast__mutmut_56": xǁDCCǁforecast__mutmut_56,
        "xǁDCCǁforecast__mutmut_57": xǁDCCǁforecast__mutmut_57,
        "xǁDCCǁforecast__mutmut_58": xǁDCCǁforecast__mutmut_58,
        "xǁDCCǁforecast__mutmut_59": xǁDCCǁforecast__mutmut_59,
    }
    xǁDCCǁforecast__mutmut_orig.__name__ = "xǁDCCǁforecast"
