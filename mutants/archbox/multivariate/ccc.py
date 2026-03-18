"""CCC-GARCH: Constant Conditional Correlation model (Bollerslev, 1990).

H_t = D_t * R * D_t

Where R is constant, estimated as sample correlation of standardized residuals.
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


class CCC(MultivariateVolatilityModel):
    """Constant Conditional Correlation GARCH model.

    The CCC model assumes that the conditional correlation matrix R is constant
    over time. It is estimated as the sample correlation of standardized residuals
    from univariate GARCH models.

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
    >>> from archbox.multivariate.ccc import CCC
    >>> returns = np.random.randn(500, 3) * 0.01
    >>> model = CCC(returns)
    >>> results = model.fit()
    >>> print(results.summary())

    References
    ----------
    Bollerslev, T. (1990). Modelling the Coherence in Short-Run Nominal Exchange Rates:
    A Multivariate Generalized ARCH Model. Review of Economics and Statistics, 72(3), 498-505.
    """

    model_name: str = "CCC-GARCH"

    def __init__(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        args = [endog, univariate_model, univariate_order]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁCCCǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁCCCǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁCCCǁ__init____mutmut_orig(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize CCC-GARCH model with options."""
        super().__init__(endog, univariate_model, univariate_order)
        self._R: NDArray[np.float64] | None = None

    def xǁCCCǁ__init____mutmut_1(
        self,
        endog: Any,
        univariate_model: str = "XXGARCHXX",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize CCC-GARCH model with options."""
        super().__init__(endog, univariate_model, univariate_order)
        self._R: NDArray[np.float64] | None = None

    def xǁCCCǁ__init____mutmut_2(
        self,
        endog: Any,
        univariate_model: str = "garch",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize CCC-GARCH model with options."""
        super().__init__(endog, univariate_model, univariate_order)
        self._R: NDArray[np.float64] | None = None

    def xǁCCCǁ__init____mutmut_3(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize CCC-GARCH model with options."""
        super().__init__(None, univariate_model, univariate_order)
        self._R: NDArray[np.float64] | None = None

    def xǁCCCǁ__init____mutmut_4(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize CCC-GARCH model with options."""
        super().__init__(endog, None, univariate_order)
        self._R: NDArray[np.float64] | None = None

    def xǁCCCǁ__init____mutmut_5(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize CCC-GARCH model with options."""
        super().__init__(endog, univariate_model, None)
        self._R: NDArray[np.float64] | None = None

    def xǁCCCǁ__init____mutmut_6(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize CCC-GARCH model with options."""
        super().__init__(univariate_model, univariate_order)
        self._R: NDArray[np.float64] | None = None

    def xǁCCCǁ__init____mutmut_7(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize CCC-GARCH model with options."""
        super().__init__(endog, univariate_order)
        self._R: NDArray[np.float64] | None = None

    def xǁCCCǁ__init____mutmut_8(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize CCC-GARCH model with options."""
        super().__init__(
            endog,
            univariate_model,
        )
        self._R: NDArray[np.float64] | None = None

    def xǁCCCǁ__init____mutmut_9(
        self,
        endog: Any,
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize CCC-GARCH model with options."""
        super().__init__(endog, univariate_model, univariate_order)
        self._R: NDArray[np.float64] | None = ""

    xǁCCCǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁCCCǁ__init____mutmut_1": xǁCCCǁ__init____mutmut_1,
        "xǁCCCǁ__init____mutmut_2": xǁCCCǁ__init____mutmut_2,
        "xǁCCCǁ__init____mutmut_3": xǁCCCǁ__init____mutmut_3,
        "xǁCCCǁ__init____mutmut_4": xǁCCCǁ__init____mutmut_4,
        "xǁCCCǁ__init____mutmut_5": xǁCCCǁ__init____mutmut_5,
        "xǁCCCǁ__init____mutmut_6": xǁCCCǁ__init____mutmut_6,
        "xǁCCCǁ__init____mutmut_7": xǁCCCǁ__init____mutmut_7,
        "xǁCCCǁ__init____mutmut_8": xǁCCCǁ__init____mutmut_8,
        "xǁCCCǁ__init____mutmut_9": xǁCCCǁ__init____mutmut_9,
    }
    xǁCCCǁ__init____mutmut_orig.__name__ = "xǁCCCǁ__init__"

    def _correlation_recursion(
        self,
        params: NDArray[np.float64],  # noqa: ARG002
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        args = [params, std_resids]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁCCCǁ_correlation_recursion__mutmut_orig"),
            object.__getattribute__(self, "xǁCCCǁ_correlation_recursion__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁCCCǁ_correlation_recursion__mutmut_orig(
        self,
        params: NDArray[np.float64],  # noqa: ARG002
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute constant correlation matrices R_t = R for all t.

        For CCC, params is empty (no parameters). R is computed from
        sample correlation of standardized residuals.

        Parameters
        ----------
        params : ndarray
            Empty array (no correlation parameters for CCC).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Constant correlation matrices, shape (T, k, k).
            R_t = R for all t.
        """
        n_obs, k = std_resids.shape

        # Compute sample correlation of standardized residuals
        corr = np.corrcoef(std_resids.T)  # (k, k)

        # Ensure positive definite
        eigenvalues = np.linalg.eigvalsh(corr)
        if np.any(eigenvalues <= 0):
            from archbox.multivariate.utils import ensure_positive_definite

            corr = ensure_positive_definite(corr)
            # Re-normalize to correlation
            d = np.sqrt(np.diag(corr))
            corr = corr / np.outer(d, d)

        self._R = corr

        # Broadcast to all time periods
        corr_t = np.broadcast_to(corr, (n_obs, k, k)).copy()

        return corr_t

    def xǁCCCǁ_correlation_recursion__mutmut_1(
        self,
        params: NDArray[np.float64],  # noqa: ARG002
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute constant correlation matrices R_t = R for all t.

        For CCC, params is empty (no parameters). R is computed from
        sample correlation of standardized residuals.

        Parameters
        ----------
        params : ndarray
            Empty array (no correlation parameters for CCC).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Constant correlation matrices, shape (T, k, k).
            R_t = R for all t.
        """
        n_obs, k = None

        # Compute sample correlation of standardized residuals
        corr = np.corrcoef(std_resids.T)  # (k, k)

        # Ensure positive definite
        eigenvalues = np.linalg.eigvalsh(corr)
        if np.any(eigenvalues <= 0):
            from archbox.multivariate.utils import ensure_positive_definite

            corr = ensure_positive_definite(corr)
            # Re-normalize to correlation
            d = np.sqrt(np.diag(corr))
            corr = corr / np.outer(d, d)

        self._R = corr

        # Broadcast to all time periods
        corr_t = np.broadcast_to(corr, (n_obs, k, k)).copy()

        return corr_t

    def xǁCCCǁ_correlation_recursion__mutmut_2(
        self,
        params: NDArray[np.float64],  # noqa: ARG002
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute constant correlation matrices R_t = R for all t.

        For CCC, params is empty (no parameters). R is computed from
        sample correlation of standardized residuals.

        Parameters
        ----------
        params : ndarray
            Empty array (no correlation parameters for CCC).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Constant correlation matrices, shape (T, k, k).
            R_t = R for all t.
        """
        n_obs, k = std_resids.shape

        # Compute sample correlation of standardized residuals
        corr = None  # (k, k)

        # Ensure positive definite
        eigenvalues = np.linalg.eigvalsh(corr)
        if np.any(eigenvalues <= 0):
            from archbox.multivariate.utils import ensure_positive_definite

            corr = ensure_positive_definite(corr)
            # Re-normalize to correlation
            d = np.sqrt(np.diag(corr))
            corr = corr / np.outer(d, d)

        self._R = corr

        # Broadcast to all time periods
        corr_t = np.broadcast_to(corr, (n_obs, k, k)).copy()

        return corr_t

    def xǁCCCǁ_correlation_recursion__mutmut_3(
        self,
        params: NDArray[np.float64],  # noqa: ARG002
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute constant correlation matrices R_t = R for all t.

        For CCC, params is empty (no parameters). R is computed from
        sample correlation of standardized residuals.

        Parameters
        ----------
        params : ndarray
            Empty array (no correlation parameters for CCC).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Constant correlation matrices, shape (T, k, k).
            R_t = R for all t.
        """
        n_obs, k = std_resids.shape

        # Compute sample correlation of standardized residuals
        corr = np.corrcoef(None)  # (k, k)

        # Ensure positive definite
        eigenvalues = np.linalg.eigvalsh(corr)
        if np.any(eigenvalues <= 0):
            from archbox.multivariate.utils import ensure_positive_definite

            corr = ensure_positive_definite(corr)
            # Re-normalize to correlation
            d = np.sqrt(np.diag(corr))
            corr = corr / np.outer(d, d)

        self._R = corr

        # Broadcast to all time periods
        corr_t = np.broadcast_to(corr, (n_obs, k, k)).copy()

        return corr_t

    def xǁCCCǁ_correlation_recursion__mutmut_4(
        self,
        params: NDArray[np.float64],  # noqa: ARG002
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute constant correlation matrices R_t = R for all t.

        For CCC, params is empty (no parameters). R is computed from
        sample correlation of standardized residuals.

        Parameters
        ----------
        params : ndarray
            Empty array (no correlation parameters for CCC).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Constant correlation matrices, shape (T, k, k).
            R_t = R for all t.
        """
        n_obs, k = std_resids.shape

        # Compute sample correlation of standardized residuals
        corr = np.corrcoef(std_resids.T)  # (k, k)

        # Ensure positive definite
        eigenvalues = None
        if np.any(eigenvalues <= 0):
            from archbox.multivariate.utils import ensure_positive_definite

            corr = ensure_positive_definite(corr)
            # Re-normalize to correlation
            d = np.sqrt(np.diag(corr))
            corr = corr / np.outer(d, d)

        self._R = corr

        # Broadcast to all time periods
        corr_t = np.broadcast_to(corr, (n_obs, k, k)).copy()

        return corr_t

    def xǁCCCǁ_correlation_recursion__mutmut_5(
        self,
        params: NDArray[np.float64],  # noqa: ARG002
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute constant correlation matrices R_t = R for all t.

        For CCC, params is empty (no parameters). R is computed from
        sample correlation of standardized residuals.

        Parameters
        ----------
        params : ndarray
            Empty array (no correlation parameters for CCC).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Constant correlation matrices, shape (T, k, k).
            R_t = R for all t.
        """
        n_obs, k = std_resids.shape

        # Compute sample correlation of standardized residuals
        corr = np.corrcoef(std_resids.T)  # (k, k)

        # Ensure positive definite
        eigenvalues = np.linalg.eigvalsh(None)
        if np.any(eigenvalues <= 0):
            from archbox.multivariate.utils import ensure_positive_definite

            corr = ensure_positive_definite(corr)
            # Re-normalize to correlation
            d = np.sqrt(np.diag(corr))
            corr = corr / np.outer(d, d)

        self._R = corr

        # Broadcast to all time periods
        corr_t = np.broadcast_to(corr, (n_obs, k, k)).copy()

        return corr_t

    def xǁCCCǁ_correlation_recursion__mutmut_6(
        self,
        params: NDArray[np.float64],  # noqa: ARG002
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute constant correlation matrices R_t = R for all t.

        For CCC, params is empty (no parameters). R is computed from
        sample correlation of standardized residuals.

        Parameters
        ----------
        params : ndarray
            Empty array (no correlation parameters for CCC).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Constant correlation matrices, shape (T, k, k).
            R_t = R for all t.
        """
        n_obs, k = std_resids.shape

        # Compute sample correlation of standardized residuals
        corr = np.corrcoef(std_resids.T)  # (k, k)

        # Ensure positive definite
        eigenvalues = np.linalg.eigvalsh(corr)
        if np.any(None):
            from archbox.multivariate.utils import ensure_positive_definite

            corr = ensure_positive_definite(corr)
            # Re-normalize to correlation
            d = np.sqrt(np.diag(corr))
            corr = corr / np.outer(d, d)

        self._R = corr

        # Broadcast to all time periods
        corr_t = np.broadcast_to(corr, (n_obs, k, k)).copy()

        return corr_t

    def xǁCCCǁ_correlation_recursion__mutmut_7(
        self,
        params: NDArray[np.float64],  # noqa: ARG002
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute constant correlation matrices R_t = R for all t.

        For CCC, params is empty (no parameters). R is computed from
        sample correlation of standardized residuals.

        Parameters
        ----------
        params : ndarray
            Empty array (no correlation parameters for CCC).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Constant correlation matrices, shape (T, k, k).
            R_t = R for all t.
        """
        n_obs, k = std_resids.shape

        # Compute sample correlation of standardized residuals
        corr = np.corrcoef(std_resids.T)  # (k, k)

        # Ensure positive definite
        eigenvalues = np.linalg.eigvalsh(corr)
        if np.any(eigenvalues < 0):
            from archbox.multivariate.utils import ensure_positive_definite

            corr = ensure_positive_definite(corr)
            # Re-normalize to correlation
            d = np.sqrt(np.diag(corr))
            corr = corr / np.outer(d, d)

        self._R = corr

        # Broadcast to all time periods
        corr_t = np.broadcast_to(corr, (n_obs, k, k)).copy()

        return corr_t

    def xǁCCCǁ_correlation_recursion__mutmut_8(
        self,
        params: NDArray[np.float64],  # noqa: ARG002
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute constant correlation matrices R_t = R for all t.

        For CCC, params is empty (no parameters). R is computed from
        sample correlation of standardized residuals.

        Parameters
        ----------
        params : ndarray
            Empty array (no correlation parameters for CCC).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Constant correlation matrices, shape (T, k, k).
            R_t = R for all t.
        """
        n_obs, k = std_resids.shape

        # Compute sample correlation of standardized residuals
        corr = np.corrcoef(std_resids.T)  # (k, k)

        # Ensure positive definite
        eigenvalues = np.linalg.eigvalsh(corr)
        if np.any(eigenvalues <= 1):
            from archbox.multivariate.utils import ensure_positive_definite

            corr = ensure_positive_definite(corr)
            # Re-normalize to correlation
            d = np.sqrt(np.diag(corr))
            corr = corr / np.outer(d, d)

        self._R = corr

        # Broadcast to all time periods
        corr_t = np.broadcast_to(corr, (n_obs, k, k)).copy()

        return corr_t

    def xǁCCCǁ_correlation_recursion__mutmut_9(
        self,
        params: NDArray[np.float64],  # noqa: ARG002
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute constant correlation matrices R_t = R for all t.

        For CCC, params is empty (no parameters). R is computed from
        sample correlation of standardized residuals.

        Parameters
        ----------
        params : ndarray
            Empty array (no correlation parameters for CCC).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Constant correlation matrices, shape (T, k, k).
            R_t = R for all t.
        """
        n_obs, k = std_resids.shape

        # Compute sample correlation of standardized residuals
        corr = np.corrcoef(std_resids.T)  # (k, k)

        # Ensure positive definite
        eigenvalues = np.linalg.eigvalsh(corr)
        if np.any(eigenvalues <= 0):
            corr = None
            # Re-normalize to correlation
            d = np.sqrt(np.diag(corr))
            corr = corr / np.outer(d, d)

        self._R = corr

        # Broadcast to all time periods
        corr_t = np.broadcast_to(corr, (n_obs, k, k)).copy()

        return corr_t

    def xǁCCCǁ_correlation_recursion__mutmut_10(
        self,
        params: NDArray[np.float64],  # noqa: ARG002
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute constant correlation matrices R_t = R for all t.

        For CCC, params is empty (no parameters). R is computed from
        sample correlation of standardized residuals.

        Parameters
        ----------
        params : ndarray
            Empty array (no correlation parameters for CCC).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Constant correlation matrices, shape (T, k, k).
            R_t = R for all t.
        """
        n_obs, k = std_resids.shape

        # Compute sample correlation of standardized residuals
        corr = np.corrcoef(std_resids.T)  # (k, k)

        # Ensure positive definite
        eigenvalues = np.linalg.eigvalsh(corr)
        if np.any(eigenvalues <= 0):
            from archbox.multivariate.utils import ensure_positive_definite

            corr = ensure_positive_definite(None)
            # Re-normalize to correlation
            d = np.sqrt(np.diag(corr))
            corr = corr / np.outer(d, d)

        self._R = corr

        # Broadcast to all time periods
        corr_t = np.broadcast_to(corr, (n_obs, k, k)).copy()

        return corr_t

    def xǁCCCǁ_correlation_recursion__mutmut_11(
        self,
        params: NDArray[np.float64],  # noqa: ARG002
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute constant correlation matrices R_t = R for all t.

        For CCC, params is empty (no parameters). R is computed from
        sample correlation of standardized residuals.

        Parameters
        ----------
        params : ndarray
            Empty array (no correlation parameters for CCC).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Constant correlation matrices, shape (T, k, k).
            R_t = R for all t.
        """
        n_obs, k = std_resids.shape

        # Compute sample correlation of standardized residuals
        corr = np.corrcoef(std_resids.T)  # (k, k)

        # Ensure positive definite
        eigenvalues = np.linalg.eigvalsh(corr)
        if np.any(eigenvalues <= 0):
            from archbox.multivariate.utils import ensure_positive_definite

            corr = ensure_positive_definite(corr)
            # Re-normalize to correlation
            d = None
            corr = corr / np.outer(d, d)

        self._R = corr

        # Broadcast to all time periods
        corr_t = np.broadcast_to(corr, (n_obs, k, k)).copy()

        return corr_t

    def xǁCCCǁ_correlation_recursion__mutmut_12(
        self,
        params: NDArray[np.float64],  # noqa: ARG002
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute constant correlation matrices R_t = R for all t.

        For CCC, params is empty (no parameters). R is computed from
        sample correlation of standardized residuals.

        Parameters
        ----------
        params : ndarray
            Empty array (no correlation parameters for CCC).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Constant correlation matrices, shape (T, k, k).
            R_t = R for all t.
        """
        n_obs, k = std_resids.shape

        # Compute sample correlation of standardized residuals
        corr = np.corrcoef(std_resids.T)  # (k, k)

        # Ensure positive definite
        eigenvalues = np.linalg.eigvalsh(corr)
        if np.any(eigenvalues <= 0):
            from archbox.multivariate.utils import ensure_positive_definite

            corr = ensure_positive_definite(corr)
            # Re-normalize to correlation
            d = np.sqrt(None)
            corr = corr / np.outer(d, d)

        self._R = corr

        # Broadcast to all time periods
        corr_t = np.broadcast_to(corr, (n_obs, k, k)).copy()

        return corr_t

    def xǁCCCǁ_correlation_recursion__mutmut_13(
        self,
        params: NDArray[np.float64],  # noqa: ARG002
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute constant correlation matrices R_t = R for all t.

        For CCC, params is empty (no parameters). R is computed from
        sample correlation of standardized residuals.

        Parameters
        ----------
        params : ndarray
            Empty array (no correlation parameters for CCC).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Constant correlation matrices, shape (T, k, k).
            R_t = R for all t.
        """
        n_obs, k = std_resids.shape

        # Compute sample correlation of standardized residuals
        corr = np.corrcoef(std_resids.T)  # (k, k)

        # Ensure positive definite
        eigenvalues = np.linalg.eigvalsh(corr)
        if np.any(eigenvalues <= 0):
            from archbox.multivariate.utils import ensure_positive_definite

            corr = ensure_positive_definite(corr)
            # Re-normalize to correlation
            d = np.sqrt(np.diag(None))
            corr = corr / np.outer(d, d)

        self._R = corr

        # Broadcast to all time periods
        corr_t = np.broadcast_to(corr, (n_obs, k, k)).copy()

        return corr_t

    def xǁCCCǁ_correlation_recursion__mutmut_14(
        self,
        params: NDArray[np.float64],  # noqa: ARG002
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute constant correlation matrices R_t = R for all t.

        For CCC, params is empty (no parameters). R is computed from
        sample correlation of standardized residuals.

        Parameters
        ----------
        params : ndarray
            Empty array (no correlation parameters for CCC).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Constant correlation matrices, shape (T, k, k).
            R_t = R for all t.
        """
        n_obs, k = std_resids.shape

        # Compute sample correlation of standardized residuals
        corr = np.corrcoef(std_resids.T)  # (k, k)

        # Ensure positive definite
        eigenvalues = np.linalg.eigvalsh(corr)
        if np.any(eigenvalues <= 0):
            from archbox.multivariate.utils import ensure_positive_definite

            corr = ensure_positive_definite(corr)
            # Re-normalize to correlation
            d = np.sqrt(np.diag(corr))
            corr = None

        self._R = corr

        # Broadcast to all time periods
        corr_t = np.broadcast_to(corr, (n_obs, k, k)).copy()

        return corr_t

    def xǁCCCǁ_correlation_recursion__mutmut_15(
        self,
        params: NDArray[np.float64],  # noqa: ARG002
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute constant correlation matrices R_t = R for all t.

        For CCC, params is empty (no parameters). R is computed from
        sample correlation of standardized residuals.

        Parameters
        ----------
        params : ndarray
            Empty array (no correlation parameters for CCC).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Constant correlation matrices, shape (T, k, k).
            R_t = R for all t.
        """
        n_obs, k = std_resids.shape

        # Compute sample correlation of standardized residuals
        corr = np.corrcoef(std_resids.T)  # (k, k)

        # Ensure positive definite
        eigenvalues = np.linalg.eigvalsh(corr)
        if np.any(eigenvalues <= 0):
            from archbox.multivariate.utils import ensure_positive_definite

            corr = ensure_positive_definite(corr)
            # Re-normalize to correlation
            d = np.sqrt(np.diag(corr))
            corr = corr * np.outer(d, d)

        self._R = corr

        # Broadcast to all time periods
        corr_t = np.broadcast_to(corr, (n_obs, k, k)).copy()

        return corr_t

    def xǁCCCǁ_correlation_recursion__mutmut_16(
        self,
        params: NDArray[np.float64],  # noqa: ARG002
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute constant correlation matrices R_t = R for all t.

        For CCC, params is empty (no parameters). R is computed from
        sample correlation of standardized residuals.

        Parameters
        ----------
        params : ndarray
            Empty array (no correlation parameters for CCC).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Constant correlation matrices, shape (T, k, k).
            R_t = R for all t.
        """
        n_obs, k = std_resids.shape

        # Compute sample correlation of standardized residuals
        corr = np.corrcoef(std_resids.T)  # (k, k)

        # Ensure positive definite
        eigenvalues = np.linalg.eigvalsh(corr)
        if np.any(eigenvalues <= 0):
            from archbox.multivariate.utils import ensure_positive_definite

            corr = ensure_positive_definite(corr)
            # Re-normalize to correlation
            d = np.sqrt(np.diag(corr))
            corr = corr / np.outer(None, d)

        self._R = corr

        # Broadcast to all time periods
        corr_t = np.broadcast_to(corr, (n_obs, k, k)).copy()

        return corr_t

    def xǁCCCǁ_correlation_recursion__mutmut_17(
        self,
        params: NDArray[np.float64],  # noqa: ARG002
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute constant correlation matrices R_t = R for all t.

        For CCC, params is empty (no parameters). R is computed from
        sample correlation of standardized residuals.

        Parameters
        ----------
        params : ndarray
            Empty array (no correlation parameters for CCC).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Constant correlation matrices, shape (T, k, k).
            R_t = R for all t.
        """
        n_obs, k = std_resids.shape

        # Compute sample correlation of standardized residuals
        corr = np.corrcoef(std_resids.T)  # (k, k)

        # Ensure positive definite
        eigenvalues = np.linalg.eigvalsh(corr)
        if np.any(eigenvalues <= 0):
            from archbox.multivariate.utils import ensure_positive_definite

            corr = ensure_positive_definite(corr)
            # Re-normalize to correlation
            d = np.sqrt(np.diag(corr))
            corr = corr / np.outer(d, None)

        self._R = corr

        # Broadcast to all time periods
        corr_t = np.broadcast_to(corr, (n_obs, k, k)).copy()

        return corr_t

    def xǁCCCǁ_correlation_recursion__mutmut_18(
        self,
        params: NDArray[np.float64],  # noqa: ARG002
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute constant correlation matrices R_t = R for all t.

        For CCC, params is empty (no parameters). R is computed from
        sample correlation of standardized residuals.

        Parameters
        ----------
        params : ndarray
            Empty array (no correlation parameters for CCC).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Constant correlation matrices, shape (T, k, k).
            R_t = R for all t.
        """
        n_obs, k = std_resids.shape

        # Compute sample correlation of standardized residuals
        corr = np.corrcoef(std_resids.T)  # (k, k)

        # Ensure positive definite
        eigenvalues = np.linalg.eigvalsh(corr)
        if np.any(eigenvalues <= 0):
            from archbox.multivariate.utils import ensure_positive_definite

            corr = ensure_positive_definite(corr)
            # Re-normalize to correlation
            d = np.sqrt(np.diag(corr))
            corr = corr / np.outer(d)

        self._R = corr

        # Broadcast to all time periods
        corr_t = np.broadcast_to(corr, (n_obs, k, k)).copy()

        return corr_t

    def xǁCCCǁ_correlation_recursion__mutmut_19(
        self,
        params: NDArray[np.float64],  # noqa: ARG002
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute constant correlation matrices R_t = R for all t.

        For CCC, params is empty (no parameters). R is computed from
        sample correlation of standardized residuals.

        Parameters
        ----------
        params : ndarray
            Empty array (no correlation parameters for CCC).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Constant correlation matrices, shape (T, k, k).
            R_t = R for all t.
        """
        n_obs, k = std_resids.shape

        # Compute sample correlation of standardized residuals
        corr = np.corrcoef(std_resids.T)  # (k, k)

        # Ensure positive definite
        eigenvalues = np.linalg.eigvalsh(corr)
        if np.any(eigenvalues <= 0):
            from archbox.multivariate.utils import ensure_positive_definite

            corr = ensure_positive_definite(corr)
            # Re-normalize to correlation
            d = np.sqrt(np.diag(corr))
            corr = corr / np.outer(
                d,
            )

        self._R = corr

        # Broadcast to all time periods
        corr_t = np.broadcast_to(corr, (n_obs, k, k)).copy()

        return corr_t

    def xǁCCCǁ_correlation_recursion__mutmut_20(
        self,
        params: NDArray[np.float64],  # noqa: ARG002
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute constant correlation matrices R_t = R for all t.

        For CCC, params is empty (no parameters). R is computed from
        sample correlation of standardized residuals.

        Parameters
        ----------
        params : ndarray
            Empty array (no correlation parameters for CCC).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Constant correlation matrices, shape (T, k, k).
            R_t = R for all t.
        """
        n_obs, k = std_resids.shape

        # Compute sample correlation of standardized residuals
        corr = np.corrcoef(std_resids.T)  # (k, k)

        # Ensure positive definite
        eigenvalues = np.linalg.eigvalsh(corr)
        if np.any(eigenvalues <= 0):
            from archbox.multivariate.utils import ensure_positive_definite

            corr = ensure_positive_definite(corr)
            # Re-normalize to correlation
            d = np.sqrt(np.diag(corr))
            corr = corr / np.outer(d, d)

        self._R = None

        # Broadcast to all time periods
        corr_t = np.broadcast_to(corr, (n_obs, k, k)).copy()

        return corr_t

    def xǁCCCǁ_correlation_recursion__mutmut_21(
        self,
        params: NDArray[np.float64],  # noqa: ARG002
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute constant correlation matrices R_t = R for all t.

        For CCC, params is empty (no parameters). R is computed from
        sample correlation of standardized residuals.

        Parameters
        ----------
        params : ndarray
            Empty array (no correlation parameters for CCC).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Constant correlation matrices, shape (T, k, k).
            R_t = R for all t.
        """
        n_obs, k = std_resids.shape

        # Compute sample correlation of standardized residuals
        corr = np.corrcoef(std_resids.T)  # (k, k)

        # Ensure positive definite
        eigenvalues = np.linalg.eigvalsh(corr)
        if np.any(eigenvalues <= 0):
            from archbox.multivariate.utils import ensure_positive_definite

            corr = ensure_positive_definite(corr)
            # Re-normalize to correlation
            d = np.sqrt(np.diag(corr))
            corr = corr / np.outer(d, d)

        self._R = corr

        # Broadcast to all time periods
        corr_t = None

        return corr_t

    def xǁCCCǁ_correlation_recursion__mutmut_22(
        self,
        params: NDArray[np.float64],  # noqa: ARG002
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute constant correlation matrices R_t = R for all t.

        For CCC, params is empty (no parameters). R is computed from
        sample correlation of standardized residuals.

        Parameters
        ----------
        params : ndarray
            Empty array (no correlation parameters for CCC).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Constant correlation matrices, shape (T, k, k).
            R_t = R for all t.
        """
        n_obs, k = std_resids.shape

        # Compute sample correlation of standardized residuals
        corr = np.corrcoef(std_resids.T)  # (k, k)

        # Ensure positive definite
        eigenvalues = np.linalg.eigvalsh(corr)
        if np.any(eigenvalues <= 0):
            from archbox.multivariate.utils import ensure_positive_definite

            corr = ensure_positive_definite(corr)
            # Re-normalize to correlation
            d = np.sqrt(np.diag(corr))
            corr = corr / np.outer(d, d)

        self._R = corr

        # Broadcast to all time periods
        corr_t = np.broadcast_to(None, (n_obs, k, k)).copy()

        return corr_t

    def xǁCCCǁ_correlation_recursion__mutmut_23(
        self,
        params: NDArray[np.float64],  # noqa: ARG002
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute constant correlation matrices R_t = R for all t.

        For CCC, params is empty (no parameters). R is computed from
        sample correlation of standardized residuals.

        Parameters
        ----------
        params : ndarray
            Empty array (no correlation parameters for CCC).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Constant correlation matrices, shape (T, k, k).
            R_t = R for all t.
        """
        n_obs, k = std_resids.shape

        # Compute sample correlation of standardized residuals
        corr = np.corrcoef(std_resids.T)  # (k, k)

        # Ensure positive definite
        eigenvalues = np.linalg.eigvalsh(corr)
        if np.any(eigenvalues <= 0):
            from archbox.multivariate.utils import ensure_positive_definite

            corr = ensure_positive_definite(corr)
            # Re-normalize to correlation
            d = np.sqrt(np.diag(corr))
            corr = corr / np.outer(d, d)

        self._R = corr

        # Broadcast to all time periods
        corr_t = np.broadcast_to(corr, None).copy()

        return corr_t

    def xǁCCCǁ_correlation_recursion__mutmut_24(
        self,
        params: NDArray[np.float64],  # noqa: ARG002
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute constant correlation matrices R_t = R for all t.

        For CCC, params is empty (no parameters). R is computed from
        sample correlation of standardized residuals.

        Parameters
        ----------
        params : ndarray
            Empty array (no correlation parameters for CCC).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Constant correlation matrices, shape (T, k, k).
            R_t = R for all t.
        """
        n_obs, k = std_resids.shape

        # Compute sample correlation of standardized residuals
        corr = np.corrcoef(std_resids.T)  # (k, k)

        # Ensure positive definite
        eigenvalues = np.linalg.eigvalsh(corr)
        if np.any(eigenvalues <= 0):
            from archbox.multivariate.utils import ensure_positive_definite

            corr = ensure_positive_definite(corr)
            # Re-normalize to correlation
            d = np.sqrt(np.diag(corr))
            corr = corr / np.outer(d, d)

        self._R = corr

        # Broadcast to all time periods
        corr_t = np.broadcast_to((n_obs, k, k)).copy()

        return corr_t

    def xǁCCCǁ_correlation_recursion__mutmut_25(
        self,
        params: NDArray[np.float64],  # noqa: ARG002
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute constant correlation matrices R_t = R for all t.

        For CCC, params is empty (no parameters). R is computed from
        sample correlation of standardized residuals.

        Parameters
        ----------
        params : ndarray
            Empty array (no correlation parameters for CCC).
        std_resids : ndarray
            Standardized residuals (T, k).

        Returns
        -------
        ndarray
            Constant correlation matrices, shape (T, k, k).
            R_t = R for all t.
        """
        n_obs, k = std_resids.shape

        # Compute sample correlation of standardized residuals
        corr = np.corrcoef(std_resids.T)  # (k, k)

        # Ensure positive definite
        eigenvalues = np.linalg.eigvalsh(corr)
        if np.any(eigenvalues <= 0):
            from archbox.multivariate.utils import ensure_positive_definite

            corr = ensure_positive_definite(corr)
            # Re-normalize to correlation
            d = np.sqrt(np.diag(corr))
            corr = corr / np.outer(d, d)

        self._R = corr

        # Broadcast to all time periods
        corr_t = np.broadcast_to(
            corr,
        ).copy()

        return corr_t

    xǁCCCǁ_correlation_recursion__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁCCCǁ_correlation_recursion__mutmut_1": xǁCCCǁ_correlation_recursion__mutmut_1,
        "xǁCCCǁ_correlation_recursion__mutmut_2": xǁCCCǁ_correlation_recursion__mutmut_2,
        "xǁCCCǁ_correlation_recursion__mutmut_3": xǁCCCǁ_correlation_recursion__mutmut_3,
        "xǁCCCǁ_correlation_recursion__mutmut_4": xǁCCCǁ_correlation_recursion__mutmut_4,
        "xǁCCCǁ_correlation_recursion__mutmut_5": xǁCCCǁ_correlation_recursion__mutmut_5,
        "xǁCCCǁ_correlation_recursion__mutmut_6": xǁCCCǁ_correlation_recursion__mutmut_6,
        "xǁCCCǁ_correlation_recursion__mutmut_7": xǁCCCǁ_correlation_recursion__mutmut_7,
        "xǁCCCǁ_correlation_recursion__mutmut_8": xǁCCCǁ_correlation_recursion__mutmut_8,
        "xǁCCCǁ_correlation_recursion__mutmut_9": xǁCCCǁ_correlation_recursion__mutmut_9,
        "xǁCCCǁ_correlation_recursion__mutmut_10": xǁCCCǁ_correlation_recursion__mutmut_10,
        "xǁCCCǁ_correlation_recursion__mutmut_11": xǁCCCǁ_correlation_recursion__mutmut_11,
        "xǁCCCǁ_correlation_recursion__mutmut_12": xǁCCCǁ_correlation_recursion__mutmut_12,
        "xǁCCCǁ_correlation_recursion__mutmut_13": xǁCCCǁ_correlation_recursion__mutmut_13,
        "xǁCCCǁ_correlation_recursion__mutmut_14": xǁCCCǁ_correlation_recursion__mutmut_14,
        "xǁCCCǁ_correlation_recursion__mutmut_15": xǁCCCǁ_correlation_recursion__mutmut_15,
        "xǁCCCǁ_correlation_recursion__mutmut_16": xǁCCCǁ_correlation_recursion__mutmut_16,
        "xǁCCCǁ_correlation_recursion__mutmut_17": xǁCCCǁ_correlation_recursion__mutmut_17,
        "xǁCCCǁ_correlation_recursion__mutmut_18": xǁCCCǁ_correlation_recursion__mutmut_18,
        "xǁCCCǁ_correlation_recursion__mutmut_19": xǁCCCǁ_correlation_recursion__mutmut_19,
        "xǁCCCǁ_correlation_recursion__mutmut_20": xǁCCCǁ_correlation_recursion__mutmut_20,
        "xǁCCCǁ_correlation_recursion__mutmut_21": xǁCCCǁ_correlation_recursion__mutmut_21,
        "xǁCCCǁ_correlation_recursion__mutmut_22": xǁCCCǁ_correlation_recursion__mutmut_22,
        "xǁCCCǁ_correlation_recursion__mutmut_23": xǁCCCǁ_correlation_recursion__mutmut_23,
        "xǁCCCǁ_correlation_recursion__mutmut_24": xǁCCCǁ_correlation_recursion__mutmut_24,
        "xǁCCCǁ_correlation_recursion__mutmut_25": xǁCCCǁ_correlation_recursion__mutmut_25,
    }
    xǁCCCǁ_correlation_recursion__mutmut_orig.__name__ = "xǁCCCǁ_correlation_recursion"

    @property
    def start_params(self) -> NDArray[np.float64]:
        """No parameters to estimate for CCC."""
        return np.array([], dtype=np.float64)

    @property
    def param_names(self) -> list[str]:
        """No parameter names for CCC."""
        return []

    def _param_bounds(self) -> list[tuple[float, float]]:
        """No bounds for CCC (no parameters)."""
        return []

    def fit(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        args = [method, disp]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁCCCǁfit__mutmut_orig"),
            object.__getattribute__(self, "xǁCCCǁfit__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁCCCǁfit__mutmut_orig(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
        )

    def xǁCCCǁfit__mutmut_1(  # noqa: ARG002
        self,
        method: str = "XXtwo_stepXX",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
        )

    def xǁCCCǁfit__mutmut_2(  # noqa: ARG002
        self,
        method: str = "TWO_STEP",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
        )

    def xǁCCCǁfit__mutmut_3(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = False,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
        )

    def xǁCCCǁfit__mutmut_4(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
        )

    def xǁCCCǁfit__mutmut_5(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
        )

    def xǁCCCǁfit__mutmut_6(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
        )

    def xǁCCCǁfit__mutmut_7(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = None
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
        )

    def xǁCCCǁfit__mutmut_8(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = None
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
        )

    def xǁCCCǁfit__mutmut_9(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(None, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
        )

    def xǁCCCǁfit__mutmut_10(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, None)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
        )

    def xǁCCCǁfit__mutmut_11(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
        )

    def xǁCCCǁfit__mutmut_12(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(
            params,
        )
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
        )

    def xǁCCCǁfit__mutmut_13(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = None

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
        )

    def xǁCCCǁfit__mutmut_14(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(None, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
        )

    def xǁCCCǁfit__mutmut_15(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, None)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
        )

    def xǁCCCǁfit__mutmut_16(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
        )

    def xǁCCCǁfit__mutmut_17(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(
            corr_t,
        )

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
        )

    def xǁCCCǁfit__mutmut_18(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = None

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
        )

    def xǁCCCǁfit__mutmut_19(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(None, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
        )

    def xǁCCCǁfit__mutmut_20(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, None, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
        )

    def xǁCCCǁfit__mutmut_21(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, None)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
        )

    def xǁCCCǁfit__mutmut_22(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
        )

    def xǁCCCǁfit__mutmut_23(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
        )

    def xǁCCCǁfit__mutmut_24(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(
            corr_t,
            self._std_resids,
        )

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
        )

    def xǁCCCǁfit__mutmut_25(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = None
        n_total = n_univ_params  # CCC has no correlation parameters

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
        )

    def xǁCCCǁfit__mutmut_26(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(None)
        n_total = n_univ_params  # CCC has no correlation parameters

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
        )

    def xǁCCCǁfit__mutmut_27(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = None  # CCC has no correlation parameters

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
        )

    def xǁCCCǁfit__mutmut_28(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

        aic = None
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
        )

    def xǁCCCǁfit__mutmut_29(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

        aic = -2.0 * loglike - 2.0 * n_total
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
        )

    def xǁCCCǁfit__mutmut_30(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

        aic = -2.0 / loglike + 2.0 * n_total
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
        )

    def xǁCCCǁfit__mutmut_31(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

        aic = +2.0 * loglike + 2.0 * n_total
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
        )

    def xǁCCCǁfit__mutmut_32(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

        aic = -3.0 * loglike + 2.0 * n_total
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
        )

    def xǁCCCǁfit__mutmut_33(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

        aic = -2.0 * loglike + 2.0 / n_total
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
        )

    def xǁCCCǁfit__mutmut_34(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

        aic = -2.0 * loglike + 3.0 * n_total
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
        )

    def xǁCCCǁfit__mutmut_35(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

        aic = -2.0 * loglike + 2.0 * n_total
        bic = None

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
        )

    def xǁCCCǁfit__mutmut_36(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike - np.log(self.T) * n_total

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
        )

    def xǁCCCǁfit__mutmut_37(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 / loglike + np.log(self.T) * n_total

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
        )

    def xǁCCCǁfit__mutmut_38(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

        aic = -2.0 * loglike + 2.0 * n_total
        bic = +2.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁCCCǁfit__mutmut_39(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -3.0 * loglike + np.log(self.T) * n_total

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
        )

    def xǁCCCǁfit__mutmut_40(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) / n_total

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
        )

    def xǁCCCǁfit__mutmut_41(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(None) * n_total

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
        )

    def xǁCCCǁfit__mutmut_42(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = None

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
        )

    def xǁCCCǁfit__mutmut_43(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = False

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
        )

    def xǁCCCǁfit__mutmut_44(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=None,
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
        )

    def xǁCCCǁfit__mutmut_45(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=None,
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
        )

    def xǁCCCǁfit__mutmut_46(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=None,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁCCCǁfit__mutmut_47(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=None,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁCCCǁfit__mutmut_48(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=None,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁCCCǁfit__mutmut_49(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=None,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁCCCǁfit__mutmut_50(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
            std_resids=None,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁCCCǁfit__mutmut_51(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
            loglike=None,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁCCCǁfit__mutmut_52(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
            aic=None,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁCCCǁfit__mutmut_53(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
            bic=None,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁCCCǁfit__mutmut_54(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
            n_obs=None,
            n_series=self.k,
        )

    def xǁCCCǁfit__mutmut_55(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
            n_series=None,
        )

    def xǁCCCǁfit__mutmut_56(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
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
        )

    def xǁCCCǁfit__mutmut_57(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
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
        )

    def xǁCCCǁfit__mutmut_58(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁCCCǁfit__mutmut_59(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_covariance=cov_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁCCCǁfit__mutmut_60(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            conditional_volatility=self._conditional_volatility,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁCCCǁfit__mutmut_61(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

        aic = -2.0 * loglike + 2.0 * n_total
        bic = -2.0 * loglike + np.log(self.T) * n_total

        self._is_fitted = True

        return MultivarResults(
            model=self,
            univariate_results=self._univariate_results,
            params=params,
            dynamic_correlation=corr_t,
            dynamic_covariance=cov_t,
            std_resids=self._std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁCCCǁfit__mutmut_62(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁCCCǁfit__mutmut_63(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁCCCǁfit__mutmut_64(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁCCCǁfit__mutmut_65(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁCCCǁfit__mutmut_66(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
            n_series=self.k,
        )

    def xǁCCCǁfit__mutmut_67(  # noqa: ARG002
        self,
        method: str = "two_step",
        disp: bool = True,
    ) -> MultivarResults:
        """Fit the CCC-GARCH model.

        Parameters
        ----------
        method : str
            Estimation method. Only 'two_step' supported.
        disp : bool
            Display progress.

        Returns
        -------
        MultivarResults
            Fitted model results.
        """
        # Step 1: fit univariate GARCH models
        self._fit_univariate()
        assert self._std_resids is not None
        assert self._conditional_volatility is not None
        assert self._univariate_results is not None

        # Step 2: compute constant correlation (no optimization needed)
        params = self.start_params
        corr_t = self._correlation_recursion(params, self._std_resids)
        cov_t = self._compute_covariance(corr_t, self._conditional_volatility)

        # Compute log-likelihood
        loglike = self._loglikelihood(corr_t, self._std_resids, self._conditional_volatility)

        # Count parameters
        n_univ_params = sum(len(r.params) for r in self._univariate_results)
        n_total = n_univ_params  # CCC has no correlation parameters

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
        )

    xǁCCCǁfit__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁCCCǁfit__mutmut_1": xǁCCCǁfit__mutmut_1,
        "xǁCCCǁfit__mutmut_2": xǁCCCǁfit__mutmut_2,
        "xǁCCCǁfit__mutmut_3": xǁCCCǁfit__mutmut_3,
        "xǁCCCǁfit__mutmut_4": xǁCCCǁfit__mutmut_4,
        "xǁCCCǁfit__mutmut_5": xǁCCCǁfit__mutmut_5,
        "xǁCCCǁfit__mutmut_6": xǁCCCǁfit__mutmut_6,
        "xǁCCCǁfit__mutmut_7": xǁCCCǁfit__mutmut_7,
        "xǁCCCǁfit__mutmut_8": xǁCCCǁfit__mutmut_8,
        "xǁCCCǁfit__mutmut_9": xǁCCCǁfit__mutmut_9,
        "xǁCCCǁfit__mutmut_10": xǁCCCǁfit__mutmut_10,
        "xǁCCCǁfit__mutmut_11": xǁCCCǁfit__mutmut_11,
        "xǁCCCǁfit__mutmut_12": xǁCCCǁfit__mutmut_12,
        "xǁCCCǁfit__mutmut_13": xǁCCCǁfit__mutmut_13,
        "xǁCCCǁfit__mutmut_14": xǁCCCǁfit__mutmut_14,
        "xǁCCCǁfit__mutmut_15": xǁCCCǁfit__mutmut_15,
        "xǁCCCǁfit__mutmut_16": xǁCCCǁfit__mutmut_16,
        "xǁCCCǁfit__mutmut_17": xǁCCCǁfit__mutmut_17,
        "xǁCCCǁfit__mutmut_18": xǁCCCǁfit__mutmut_18,
        "xǁCCCǁfit__mutmut_19": xǁCCCǁfit__mutmut_19,
        "xǁCCCǁfit__mutmut_20": xǁCCCǁfit__mutmut_20,
        "xǁCCCǁfit__mutmut_21": xǁCCCǁfit__mutmut_21,
        "xǁCCCǁfit__mutmut_22": xǁCCCǁfit__mutmut_22,
        "xǁCCCǁfit__mutmut_23": xǁCCCǁfit__mutmut_23,
        "xǁCCCǁfit__mutmut_24": xǁCCCǁfit__mutmut_24,
        "xǁCCCǁfit__mutmut_25": xǁCCCǁfit__mutmut_25,
        "xǁCCCǁfit__mutmut_26": xǁCCCǁfit__mutmut_26,
        "xǁCCCǁfit__mutmut_27": xǁCCCǁfit__mutmut_27,
        "xǁCCCǁfit__mutmut_28": xǁCCCǁfit__mutmut_28,
        "xǁCCCǁfit__mutmut_29": xǁCCCǁfit__mutmut_29,
        "xǁCCCǁfit__mutmut_30": xǁCCCǁfit__mutmut_30,
        "xǁCCCǁfit__mutmut_31": xǁCCCǁfit__mutmut_31,
        "xǁCCCǁfit__mutmut_32": xǁCCCǁfit__mutmut_32,
        "xǁCCCǁfit__mutmut_33": xǁCCCǁfit__mutmut_33,
        "xǁCCCǁfit__mutmut_34": xǁCCCǁfit__mutmut_34,
        "xǁCCCǁfit__mutmut_35": xǁCCCǁfit__mutmut_35,
        "xǁCCCǁfit__mutmut_36": xǁCCCǁfit__mutmut_36,
        "xǁCCCǁfit__mutmut_37": xǁCCCǁfit__mutmut_37,
        "xǁCCCǁfit__mutmut_38": xǁCCCǁfit__mutmut_38,
        "xǁCCCǁfit__mutmut_39": xǁCCCǁfit__mutmut_39,
        "xǁCCCǁfit__mutmut_40": xǁCCCǁfit__mutmut_40,
        "xǁCCCǁfit__mutmut_41": xǁCCCǁfit__mutmut_41,
        "xǁCCCǁfit__mutmut_42": xǁCCCǁfit__mutmut_42,
        "xǁCCCǁfit__mutmut_43": xǁCCCǁfit__mutmut_43,
        "xǁCCCǁfit__mutmut_44": xǁCCCǁfit__mutmut_44,
        "xǁCCCǁfit__mutmut_45": xǁCCCǁfit__mutmut_45,
        "xǁCCCǁfit__mutmut_46": xǁCCCǁfit__mutmut_46,
        "xǁCCCǁfit__mutmut_47": xǁCCCǁfit__mutmut_47,
        "xǁCCCǁfit__mutmut_48": xǁCCCǁfit__mutmut_48,
        "xǁCCCǁfit__mutmut_49": xǁCCCǁfit__mutmut_49,
        "xǁCCCǁfit__mutmut_50": xǁCCCǁfit__mutmut_50,
        "xǁCCCǁfit__mutmut_51": xǁCCCǁfit__mutmut_51,
        "xǁCCCǁfit__mutmut_52": xǁCCCǁfit__mutmut_52,
        "xǁCCCǁfit__mutmut_53": xǁCCCǁfit__mutmut_53,
        "xǁCCCǁfit__mutmut_54": xǁCCCǁfit__mutmut_54,
        "xǁCCCǁfit__mutmut_55": xǁCCCǁfit__mutmut_55,
        "xǁCCCǁfit__mutmut_56": xǁCCCǁfit__mutmut_56,
        "xǁCCCǁfit__mutmut_57": xǁCCCǁfit__mutmut_57,
        "xǁCCCǁfit__mutmut_58": xǁCCCǁfit__mutmut_58,
        "xǁCCCǁfit__mutmut_59": xǁCCCǁfit__mutmut_59,
        "xǁCCCǁfit__mutmut_60": xǁCCCǁfit__mutmut_60,
        "xǁCCCǁfit__mutmut_61": xǁCCCǁfit__mutmut_61,
        "xǁCCCǁfit__mutmut_62": xǁCCCǁfit__mutmut_62,
        "xǁCCCǁfit__mutmut_63": xǁCCCǁfit__mutmut_63,
        "xǁCCCǁfit__mutmut_64": xǁCCCǁfit__mutmut_64,
        "xǁCCCǁfit__mutmut_65": xǁCCCǁfit__mutmut_65,
        "xǁCCCǁfit__mutmut_66": xǁCCCǁfit__mutmut_66,
        "xǁCCCǁfit__mutmut_67": xǁCCCǁfit__mutmut_67,
    }
    xǁCCCǁfit__mutmut_orig.__name__ = "xǁCCCǁfit"

    @property
    def constant_correlation(self) -> NDArray[np.float64] | None:
        """Return the estimated constant correlation matrix R."""
        return self._R

    def forecast(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        args = [results, horizon]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁCCCǁforecast__mutmut_orig"),
            object.__getattribute__(self, "xǁCCCǁforecast__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁCCCǁforecast__mutmut_orig(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for CCC.

        For CCC, the correlation forecast is simply R (constant).
        The covariance forecast uses univariate GARCH variance forecasts.

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
        assert self._R is not None

        corr_forecast = np.zeros((horizon, self.k, self.k))
        cov_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            corr_forecast[h] = self._R
            # Use last conditional volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            cov_forecast[h] = d_mat @ self._R @ d_mat

        return {"covariance": cov_forecast, "correlation": corr_forecast}

    def xǁCCCǁforecast__mutmut_1(
        self,
        results: MultivarResults,
        horizon: int = 11,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for CCC.

        For CCC, the correlation forecast is simply R (constant).
        The covariance forecast uses univariate GARCH variance forecasts.

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
        assert self._R is not None

        corr_forecast = np.zeros((horizon, self.k, self.k))
        cov_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            corr_forecast[h] = self._R
            # Use last conditional volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            cov_forecast[h] = d_mat @ self._R @ d_mat

        return {"covariance": cov_forecast, "correlation": corr_forecast}

    def xǁCCCǁforecast__mutmut_2(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for CCC.

        For CCC, the correlation forecast is simply R (constant).
        The covariance forecast uses univariate GARCH variance forecasts.

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
        assert self._R is None

        corr_forecast = np.zeros((horizon, self.k, self.k))
        cov_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            corr_forecast[h] = self._R
            # Use last conditional volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            cov_forecast[h] = d_mat @ self._R @ d_mat

        return {"covariance": cov_forecast, "correlation": corr_forecast}

    def xǁCCCǁforecast__mutmut_3(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for CCC.

        For CCC, the correlation forecast is simply R (constant).
        The covariance forecast uses univariate GARCH variance forecasts.

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
        assert self._R is not None

        corr_forecast = None
        cov_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            corr_forecast[h] = self._R
            # Use last conditional volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            cov_forecast[h] = d_mat @ self._R @ d_mat

        return {"covariance": cov_forecast, "correlation": corr_forecast}

    def xǁCCCǁforecast__mutmut_4(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for CCC.

        For CCC, the correlation forecast is simply R (constant).
        The covariance forecast uses univariate GARCH variance forecasts.

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
        assert self._R is not None

        corr_forecast = np.zeros(None)
        cov_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            corr_forecast[h] = self._R
            # Use last conditional volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            cov_forecast[h] = d_mat @ self._R @ d_mat

        return {"covariance": cov_forecast, "correlation": corr_forecast}

    def xǁCCCǁforecast__mutmut_5(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for CCC.

        For CCC, the correlation forecast is simply R (constant).
        The covariance forecast uses univariate GARCH variance forecasts.

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
        assert self._R is not None

        corr_forecast = np.zeros((horizon, self.k, self.k))
        cov_forecast = None

        for h in range(horizon):
            corr_forecast[h] = self._R
            # Use last conditional volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            cov_forecast[h] = d_mat @ self._R @ d_mat

        return {"covariance": cov_forecast, "correlation": corr_forecast}

    def xǁCCCǁforecast__mutmut_6(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for CCC.

        For CCC, the correlation forecast is simply R (constant).
        The covariance forecast uses univariate GARCH variance forecasts.

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
        assert self._R is not None

        corr_forecast = np.zeros((horizon, self.k, self.k))
        cov_forecast = np.zeros(None)

        for h in range(horizon):
            corr_forecast[h] = self._R
            # Use last conditional volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            cov_forecast[h] = d_mat @ self._R @ d_mat

        return {"covariance": cov_forecast, "correlation": corr_forecast}

    def xǁCCCǁforecast__mutmut_7(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for CCC.

        For CCC, the correlation forecast is simply R (constant).
        The covariance forecast uses univariate GARCH variance forecasts.

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
        assert self._R is not None

        corr_forecast = np.zeros((horizon, self.k, self.k))
        cov_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(None):
            corr_forecast[h] = self._R
            # Use last conditional volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            cov_forecast[h] = d_mat @ self._R @ d_mat

        return {"covariance": cov_forecast, "correlation": corr_forecast}

    def xǁCCCǁforecast__mutmut_8(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for CCC.

        For CCC, the correlation forecast is simply R (constant).
        The covariance forecast uses univariate GARCH variance forecasts.

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
        assert self._R is not None

        corr_forecast = np.zeros((horizon, self.k, self.k))
        cov_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            corr_forecast[h] = None
            # Use last conditional volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            cov_forecast[h] = d_mat @ self._R @ d_mat

        return {"covariance": cov_forecast, "correlation": corr_forecast}

    def xǁCCCǁforecast__mutmut_9(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for CCC.

        For CCC, the correlation forecast is simply R (constant).
        The covariance forecast uses univariate GARCH variance forecasts.

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
        assert self._R is not None

        corr_forecast = np.zeros((horizon, self.k, self.k))
        cov_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            corr_forecast[h] = self._R
            # Use last conditional volatility as naive forecast
            d_mat = None
            cov_forecast[h] = d_mat @ self._R @ d_mat

        return {"covariance": cov_forecast, "correlation": corr_forecast}

    def xǁCCCǁforecast__mutmut_10(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for CCC.

        For CCC, the correlation forecast is simply R (constant).
        The covariance forecast uses univariate GARCH variance forecasts.

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
        assert self._R is not None

        corr_forecast = np.zeros((horizon, self.k, self.k))
        cov_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            corr_forecast[h] = self._R
            # Use last conditional volatility as naive forecast
            d_mat = np.diag(None)
            cov_forecast[h] = d_mat @ self._R @ d_mat

        return {"covariance": cov_forecast, "correlation": corr_forecast}

    def xǁCCCǁforecast__mutmut_11(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for CCC.

        For CCC, the correlation forecast is simply R (constant).
        The covariance forecast uses univariate GARCH variance forecasts.

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
        assert self._R is not None

        corr_forecast = np.zeros((horizon, self.k, self.k))
        cov_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            corr_forecast[h] = self._R
            # Use last conditional volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[+1])
            cov_forecast[h] = d_mat @ self._R @ d_mat

        return {"covariance": cov_forecast, "correlation": corr_forecast}

    def xǁCCCǁforecast__mutmut_12(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for CCC.

        For CCC, the correlation forecast is simply R (constant).
        The covariance forecast uses univariate GARCH variance forecasts.

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
        assert self._R is not None

        corr_forecast = np.zeros((horizon, self.k, self.k))
        cov_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            corr_forecast[h] = self._R
            # Use last conditional volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-2])
            cov_forecast[h] = d_mat @ self._R @ d_mat

        return {"covariance": cov_forecast, "correlation": corr_forecast}

    def xǁCCCǁforecast__mutmut_13(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for CCC.

        For CCC, the correlation forecast is simply R (constant).
        The covariance forecast uses univariate GARCH variance forecasts.

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
        assert self._R is not None

        corr_forecast = np.zeros((horizon, self.k, self.k))
        cov_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            corr_forecast[h] = self._R
            # Use last conditional volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            cov_forecast[h] = None

        return {"covariance": cov_forecast, "correlation": corr_forecast}

    def xǁCCCǁforecast__mutmut_14(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for CCC.

        For CCC, the correlation forecast is simply R (constant).
        The covariance forecast uses univariate GARCH variance forecasts.

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
        assert self._R is not None

        corr_forecast = np.zeros((horizon, self.k, self.k))
        cov_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            corr_forecast[h] = self._R
            # Use last conditional volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            cov_forecast[h] = d_mat @ self._R @ d_mat

        return {"XXcovarianceXX": cov_forecast, "correlation": corr_forecast}

    def xǁCCCǁforecast__mutmut_15(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for CCC.

        For CCC, the correlation forecast is simply R (constant).
        The covariance forecast uses univariate GARCH variance forecasts.

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
        assert self._R is not None

        corr_forecast = np.zeros((horizon, self.k, self.k))
        cov_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            corr_forecast[h] = self._R
            # Use last conditional volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            cov_forecast[h] = d_mat @ self._R @ d_mat

        return {"COVARIANCE": cov_forecast, "correlation": corr_forecast}

    def xǁCCCǁforecast__mutmut_16(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for CCC.

        For CCC, the correlation forecast is simply R (constant).
        The covariance forecast uses univariate GARCH variance forecasts.

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
        assert self._R is not None

        corr_forecast = np.zeros((horizon, self.k, self.k))
        cov_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            corr_forecast[h] = self._R
            # Use last conditional volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            cov_forecast[h] = d_mat @ self._R @ d_mat

        return {"covariance": cov_forecast, "XXcorrelationXX": corr_forecast}

    def xǁCCCǁforecast__mutmut_17(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        """Forecast H_{T+h} for CCC.

        For CCC, the correlation forecast is simply R (constant).
        The covariance forecast uses univariate GARCH variance forecasts.

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
        assert self._R is not None

        corr_forecast = np.zeros((horizon, self.k, self.k))
        cov_forecast = np.zeros((horizon, self.k, self.k))

        for h in range(horizon):
            corr_forecast[h] = self._R
            # Use last conditional volatility as naive forecast
            d_mat = np.diag(results.conditional_volatility[-1])
            cov_forecast[h] = d_mat @ self._R @ d_mat

        return {"covariance": cov_forecast, "CORRELATION": corr_forecast}

    xǁCCCǁforecast__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁCCCǁforecast__mutmut_1": xǁCCCǁforecast__mutmut_1,
        "xǁCCCǁforecast__mutmut_2": xǁCCCǁforecast__mutmut_2,
        "xǁCCCǁforecast__mutmut_3": xǁCCCǁforecast__mutmut_3,
        "xǁCCCǁforecast__mutmut_4": xǁCCCǁforecast__mutmut_4,
        "xǁCCCǁforecast__mutmut_5": xǁCCCǁforecast__mutmut_5,
        "xǁCCCǁforecast__mutmut_6": xǁCCCǁforecast__mutmut_6,
        "xǁCCCǁforecast__mutmut_7": xǁCCCǁforecast__mutmut_7,
        "xǁCCCǁforecast__mutmut_8": xǁCCCǁforecast__mutmut_8,
        "xǁCCCǁforecast__mutmut_9": xǁCCCǁforecast__mutmut_9,
        "xǁCCCǁforecast__mutmut_10": xǁCCCǁforecast__mutmut_10,
        "xǁCCCǁforecast__mutmut_11": xǁCCCǁforecast__mutmut_11,
        "xǁCCCǁforecast__mutmut_12": xǁCCCǁforecast__mutmut_12,
        "xǁCCCǁforecast__mutmut_13": xǁCCCǁforecast__mutmut_13,
        "xǁCCCǁforecast__mutmut_14": xǁCCCǁforecast__mutmut_14,
        "xǁCCCǁforecast__mutmut_15": xǁCCCǁforecast__mutmut_15,
        "xǁCCCǁforecast__mutmut_16": xǁCCCǁforecast__mutmut_16,
        "xǁCCCǁforecast__mutmut_17": xǁCCCǁforecast__mutmut_17,
    }
    xǁCCCǁforecast__mutmut_orig.__name__ = "xǁCCCǁforecast"
