"""BEKK-GARCH: Baba-Engle-Kraft-Kroner model (Engle & Kroner, 1995).

H_t = C*C' + A'*eps_{t-1}*eps'_{t-1}*A + B'*H_{t-1}*B

Guarantees positive definite H_t by construction.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Annotated, Any, ClassVar

import numpy as np
from numpy.typing import NDArray
from scipy import optimize

from archbox.multivariate.base import MultivariateVolatilityModel, MultivarResults
from archbox.multivariate.utils import is_positive_definite

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
        args = [endog, variant, univariate_model, univariate_order]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁBEKKǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁBEKKǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁBEKKǁ__init____mutmut_orig(
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

    def xǁBEKKǁ__init____mutmut_1(
        self,
        endog: Any,
        variant: str = "XXdiagonalXX",
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

    def xǁBEKKǁ__init____mutmut_2(
        self,
        endog: Any,
        variant: str = "DIAGONAL",
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

    def xǁBEKKǁ__init____mutmut_3(
        self,
        endog: Any,
        variant: str = "diagonal",
        univariate_model: str = "XXGARCHXX",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize BEKK-GARCH model with variant and options."""
        super().__init__(endog, univariate_model, univariate_order)
        if variant not in ("full", "diagonal"):
            msg = f"variant must be 'full' or 'diagonal', got '{variant}'"
            raise ValueError(msg)
        self.variant = variant
        self.model_name = f"BEKK-GARCH ({variant})"

    def xǁBEKKǁ__init____mutmut_4(
        self,
        endog: Any,
        variant: str = "diagonal",
        univariate_model: str = "garch",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize BEKK-GARCH model with variant and options."""
        super().__init__(endog, univariate_model, univariate_order)
        if variant not in ("full", "diagonal"):
            msg = f"variant must be 'full' or 'diagonal', got '{variant}'"
            raise ValueError(msg)
        self.variant = variant
        self.model_name = f"BEKK-GARCH ({variant})"

    def xǁBEKKǁ__init____mutmut_5(
        self,
        endog: Any,
        variant: str = "diagonal",
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize BEKK-GARCH model with variant and options."""
        super().__init__(None, univariate_model, univariate_order)
        if variant not in ("full", "diagonal"):
            msg = f"variant must be 'full' or 'diagonal', got '{variant}'"
            raise ValueError(msg)
        self.variant = variant
        self.model_name = f"BEKK-GARCH ({variant})"

    def xǁBEKKǁ__init____mutmut_6(
        self,
        endog: Any,
        variant: str = "diagonal",
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize BEKK-GARCH model with variant and options."""
        super().__init__(endog, None, univariate_order)
        if variant not in ("full", "diagonal"):
            msg = f"variant must be 'full' or 'diagonal', got '{variant}'"
            raise ValueError(msg)
        self.variant = variant
        self.model_name = f"BEKK-GARCH ({variant})"

    def xǁBEKKǁ__init____mutmut_7(
        self,
        endog: Any,
        variant: str = "diagonal",
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize BEKK-GARCH model with variant and options."""
        super().__init__(endog, univariate_model, None)
        if variant not in ("full", "diagonal"):
            msg = f"variant must be 'full' or 'diagonal', got '{variant}'"
            raise ValueError(msg)
        self.variant = variant
        self.model_name = f"BEKK-GARCH ({variant})"

    def xǁBEKKǁ__init____mutmut_8(
        self,
        endog: Any,
        variant: str = "diagonal",
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize BEKK-GARCH model with variant and options."""
        super().__init__(univariate_model, univariate_order)
        if variant not in ("full", "diagonal"):
            msg = f"variant must be 'full' or 'diagonal', got '{variant}'"
            raise ValueError(msg)
        self.variant = variant
        self.model_name = f"BEKK-GARCH ({variant})"

    def xǁBEKKǁ__init____mutmut_9(
        self,
        endog: Any,
        variant: str = "diagonal",
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize BEKK-GARCH model with variant and options."""
        super().__init__(endog, univariate_order)
        if variant not in ("full", "diagonal"):
            msg = f"variant must be 'full' or 'diagonal', got '{variant}'"
            raise ValueError(msg)
        self.variant = variant
        self.model_name = f"BEKK-GARCH ({variant})"

    def xǁBEKKǁ__init____mutmut_10(
        self,
        endog: Any,
        variant: str = "diagonal",
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize BEKK-GARCH model with variant and options."""
        super().__init__(
            endog,
            univariate_model,
        )
        if variant not in ("full", "diagonal"):
            msg = f"variant must be 'full' or 'diagonal', got '{variant}'"
            raise ValueError(msg)
        self.variant = variant
        self.model_name = f"BEKK-GARCH ({variant})"

    def xǁBEKKǁ__init____mutmut_11(
        self,
        endog: Any,
        variant: str = "diagonal",
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize BEKK-GARCH model with variant and options."""
        super().__init__(endog, univariate_model, univariate_order)
        if variant in ("full", "diagonal"):
            msg = f"variant must be 'full' or 'diagonal', got '{variant}'"
            raise ValueError(msg)
        self.variant = variant
        self.model_name = f"BEKK-GARCH ({variant})"

    def xǁBEKKǁ__init____mutmut_12(
        self,
        endog: Any,
        variant: str = "diagonal",
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize BEKK-GARCH model with variant and options."""
        super().__init__(endog, univariate_model, univariate_order)
        if variant not in ("XXfullXX", "diagonal"):
            msg = f"variant must be 'full' or 'diagonal', got '{variant}'"
            raise ValueError(msg)
        self.variant = variant
        self.model_name = f"BEKK-GARCH ({variant})"

    def xǁBEKKǁ__init____mutmut_13(
        self,
        endog: Any,
        variant: str = "diagonal",
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize BEKK-GARCH model with variant and options."""
        super().__init__(endog, univariate_model, univariate_order)
        if variant not in ("FULL", "diagonal"):
            msg = f"variant must be 'full' or 'diagonal', got '{variant}'"
            raise ValueError(msg)
        self.variant = variant
        self.model_name = f"BEKK-GARCH ({variant})"

    def xǁBEKKǁ__init____mutmut_14(
        self,
        endog: Any,
        variant: str = "diagonal",
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize BEKK-GARCH model with variant and options."""
        super().__init__(endog, univariate_model, univariate_order)
        if variant not in ("full", "XXdiagonalXX"):
            msg = f"variant must be 'full' or 'diagonal', got '{variant}'"
            raise ValueError(msg)
        self.variant = variant
        self.model_name = f"BEKK-GARCH ({variant})"

    def xǁBEKKǁ__init____mutmut_15(
        self,
        endog: Any,
        variant: str = "diagonal",
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize BEKK-GARCH model with variant and options."""
        super().__init__(endog, univariate_model, univariate_order)
        if variant not in ("full", "DIAGONAL"):
            msg = f"variant must be 'full' or 'diagonal', got '{variant}'"
            raise ValueError(msg)
        self.variant = variant
        self.model_name = f"BEKK-GARCH ({variant})"

    def xǁBEKKǁ__init____mutmut_16(
        self,
        endog: Any,
        variant: str = "diagonal",
        univariate_model: str = "GARCH",
        univariate_order: tuple[int, int] = (1, 1),
    ) -> None:
        """Initialize BEKK-GARCH model with variant and options."""
        super().__init__(endog, univariate_model, univariate_order)
        if variant not in ("full", "diagonal"):
            msg = None
            raise ValueError(msg)
        self.variant = variant
        self.model_name = f"BEKK-GARCH ({variant})"

    def xǁBEKKǁ__init____mutmut_17(
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
            raise ValueError(None)
        self.variant = variant
        self.model_name = f"BEKK-GARCH ({variant})"

    def xǁBEKKǁ__init____mutmut_18(
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
        self.variant = None
        self.model_name = f"BEKK-GARCH ({variant})"

    def xǁBEKKǁ__init____mutmut_19(
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
        self.model_name = None

    xǁBEKKǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁBEKKǁ__init____mutmut_1": xǁBEKKǁ__init____mutmut_1,
        "xǁBEKKǁ__init____mutmut_2": xǁBEKKǁ__init____mutmut_2,
        "xǁBEKKǁ__init____mutmut_3": xǁBEKKǁ__init____mutmut_3,
        "xǁBEKKǁ__init____mutmut_4": xǁBEKKǁ__init____mutmut_4,
        "xǁBEKKǁ__init____mutmut_5": xǁBEKKǁ__init____mutmut_5,
        "xǁBEKKǁ__init____mutmut_6": xǁBEKKǁ__init____mutmut_6,
        "xǁBEKKǁ__init____mutmut_7": xǁBEKKǁ__init____mutmut_7,
        "xǁBEKKǁ__init____mutmut_8": xǁBEKKǁ__init____mutmut_8,
        "xǁBEKKǁ__init____mutmut_9": xǁBEKKǁ__init____mutmut_9,
        "xǁBEKKǁ__init____mutmut_10": xǁBEKKǁ__init____mutmut_10,
        "xǁBEKKǁ__init____mutmut_11": xǁBEKKǁ__init____mutmut_11,
        "xǁBEKKǁ__init____mutmut_12": xǁBEKKǁ__init____mutmut_12,
        "xǁBEKKǁ__init____mutmut_13": xǁBEKKǁ__init____mutmut_13,
        "xǁBEKKǁ__init____mutmut_14": xǁBEKKǁ__init____mutmut_14,
        "xǁBEKKǁ__init____mutmut_15": xǁBEKKǁ__init____mutmut_15,
        "xǁBEKKǁ__init____mutmut_16": xǁBEKKǁ__init____mutmut_16,
        "xǁBEKKǁ__init____mutmut_17": xǁBEKKǁ__init____mutmut_17,
        "xǁBEKKǁ__init____mutmut_18": xǁBEKKǁ__init____mutmut_18,
        "xǁBEKKǁ__init____mutmut_19": xǁBEKKǁ__init____mutmut_19,
    }
    xǁBEKKǁ__init____mutmut_orig.__name__ = "xǁBEKKǁ__init__"

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
        args = [params]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁBEKKǁ_unpack_params__mutmut_orig"),
            object.__getattribute__(self, "xǁBEKKǁ_unpack_params__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁBEKKǁ_unpack_params__mutmut_orig(
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

    def xǁBEKKǁ_unpack_params__mutmut_1(
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
        k = None
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

    def xǁBEKKǁ_unpack_params__mutmut_2(
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
        idx = None

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

    def xǁBEKKǁ_unpack_params__mutmut_3(
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
        idx = 1

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

    def xǁBEKKǁ_unpack_params__mutmut_4(
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
        c_mat = None
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

    def xǁBEKKǁ_unpack_params__mutmut_5(
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
        c_mat = np.zeros(None)
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

    def xǁBEKKǁ_unpack_params__mutmut_6(
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
        for i in range(None):
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

    def xǁBEKKǁ_unpack_params__mutmut_7(
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
            for j in range(None):
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

    def xǁBEKKǁ_unpack_params__mutmut_8(
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
            for j in range(i - 1):
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

    def xǁBEKKǁ_unpack_params__mutmut_9(
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
            for j in range(i + 2):
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

    def xǁBEKKǁ_unpack_params__mutmut_10(
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
                c_mat[i, j] = None
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

    def xǁBEKKǁ_unpack_params__mutmut_11(
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
                idx = 1

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

    def xǁBEKKǁ_unpack_params__mutmut_12(
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
                idx -= 1

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

    def xǁBEKKǁ_unpack_params__mutmut_13(
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
                idx += 2

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

    def xǁBEKKǁ_unpack_params__mutmut_14(
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
        if self.variant != "diagonal":
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

    def xǁBEKKǁ_unpack_params__mutmut_15(
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
        if self.variant == "XXdiagonalXX":
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

    def xǁBEKKǁ_unpack_params__mutmut_16(
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
        if self.variant == "DIAGONAL":
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

    def xǁBEKKǁ_unpack_params__mutmut_17(
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
            a_mat = None
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

    def xǁBEKKǁ_unpack_params__mutmut_18(
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
            a_mat = np.diag(None)
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

    def xǁBEKKǁ_unpack_params__mutmut_19(
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
            a_mat = np.diag(params[idx : idx - k])
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

    def xǁBEKKǁ_unpack_params__mutmut_20(
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
            idx = k
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

    def xǁBEKKǁ_unpack_params__mutmut_21(
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
            idx -= k
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

    def xǁBEKKǁ_unpack_params__mutmut_22(
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
            a_mat = None
            idx += k * k

        # b_mat
        if self.variant == "diagonal":
            b_mat = np.diag(params[idx : idx + k])
            idx += k
        else:
            b_mat = params[idx : idx + k * k].reshape(k, k)
            idx += k * k

        return c_mat, a_mat, b_mat

    def xǁBEKKǁ_unpack_params__mutmut_23(
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
            a_mat = params[idx : idx + k * k].reshape(None, k)
            idx += k * k

        # b_mat
        if self.variant == "diagonal":
            b_mat = np.diag(params[idx : idx + k])
            idx += k
        else:
            b_mat = params[idx : idx + k * k].reshape(k, k)
            idx += k * k

        return c_mat, a_mat, b_mat

    def xǁBEKKǁ_unpack_params__mutmut_24(
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
            a_mat = params[idx : idx + k * k].reshape(k, None)
            idx += k * k

        # b_mat
        if self.variant == "diagonal":
            b_mat = np.diag(params[idx : idx + k])
            idx += k
        else:
            b_mat = params[idx : idx + k * k].reshape(k, k)
            idx += k * k

        return c_mat, a_mat, b_mat

    def xǁBEKKǁ_unpack_params__mutmut_25(
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
            a_mat = params[idx : idx + k * k].reshape(k)
            idx += k * k

        # b_mat
        if self.variant == "diagonal":
            b_mat = np.diag(params[idx : idx + k])
            idx += k
        else:
            b_mat = params[idx : idx + k * k].reshape(k, k)
            idx += k * k

        return c_mat, a_mat, b_mat

    def xǁBEKKǁ_unpack_params__mutmut_26(
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
            a_mat = params[idx : idx + k * k].reshape(
                k,
            )
            idx += k * k

        # b_mat
        if self.variant == "diagonal":
            b_mat = np.diag(params[idx : idx + k])
            idx += k
        else:
            b_mat = params[idx : idx + k * k].reshape(k, k)
            idx += k * k

        return c_mat, a_mat, b_mat

    def xǁBEKKǁ_unpack_params__mutmut_27(
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
            a_mat = params[idx : idx - k * k].reshape(k, k)
            idx += k * k

        # b_mat
        if self.variant == "diagonal":
            b_mat = np.diag(params[idx : idx + k])
            idx += k
        else:
            b_mat = params[idx : idx + k * k].reshape(k, k)
            idx += k * k

        return c_mat, a_mat, b_mat

    def xǁBEKKǁ_unpack_params__mutmut_28(
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
            a_mat = params[idx : idx + k / k].reshape(k, k)
            idx += k * k

        # b_mat
        if self.variant == "diagonal":
            b_mat = np.diag(params[idx : idx + k])
            idx += k
        else:
            b_mat = params[idx : idx + k * k].reshape(k, k)
            idx += k * k

        return c_mat, a_mat, b_mat

    def xǁBEKKǁ_unpack_params__mutmut_29(
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
            idx = k * k

        # b_mat
        if self.variant == "diagonal":
            b_mat = np.diag(params[idx : idx + k])
            idx += k
        else:
            b_mat = params[idx : idx + k * k].reshape(k, k)
            idx += k * k

        return c_mat, a_mat, b_mat

    def xǁBEKKǁ_unpack_params__mutmut_30(
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
            idx -= k * k

        # b_mat
        if self.variant == "diagonal":
            b_mat = np.diag(params[idx : idx + k])
            idx += k
        else:
            b_mat = params[idx : idx + k * k].reshape(k, k)
            idx += k * k

        return c_mat, a_mat, b_mat

    def xǁBEKKǁ_unpack_params__mutmut_31(
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
            idx += k / k

        # b_mat
        if self.variant == "diagonal":
            b_mat = np.diag(params[idx : idx + k])
            idx += k
        else:
            b_mat = params[idx : idx + k * k].reshape(k, k)
            idx += k * k

        return c_mat, a_mat, b_mat

    def xǁBEKKǁ_unpack_params__mutmut_32(
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
        if self.variant != "diagonal":
            b_mat = np.diag(params[idx : idx + k])
            idx += k
        else:
            b_mat = params[idx : idx + k * k].reshape(k, k)
            idx += k * k

        return c_mat, a_mat, b_mat

    def xǁBEKKǁ_unpack_params__mutmut_33(
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
        if self.variant == "XXdiagonalXX":
            b_mat = np.diag(params[idx : idx + k])
            idx += k
        else:
            b_mat = params[idx : idx + k * k].reshape(k, k)
            idx += k * k

        return c_mat, a_mat, b_mat

    def xǁBEKKǁ_unpack_params__mutmut_34(
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
        if self.variant == "DIAGONAL":
            b_mat = np.diag(params[idx : idx + k])
            idx += k
        else:
            b_mat = params[idx : idx + k * k].reshape(k, k)
            idx += k * k

        return c_mat, a_mat, b_mat

    def xǁBEKKǁ_unpack_params__mutmut_35(
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
            b_mat = None
            idx += k
        else:
            b_mat = params[idx : idx + k * k].reshape(k, k)
            idx += k * k

        return c_mat, a_mat, b_mat

    def xǁBEKKǁ_unpack_params__mutmut_36(
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
            b_mat = np.diag(None)
            idx += k
        else:
            b_mat = params[idx : idx + k * k].reshape(k, k)
            idx += k * k

        return c_mat, a_mat, b_mat

    def xǁBEKKǁ_unpack_params__mutmut_37(
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
            b_mat = np.diag(params[idx : idx - k])
            idx += k
        else:
            b_mat = params[idx : idx + k * k].reshape(k, k)
            idx += k * k

        return c_mat, a_mat, b_mat

    def xǁBEKKǁ_unpack_params__mutmut_38(
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
            idx = k
        else:
            b_mat = params[idx : idx + k * k].reshape(k, k)
            idx += k * k

        return c_mat, a_mat, b_mat

    def xǁBEKKǁ_unpack_params__mutmut_39(
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
            idx -= k
        else:
            b_mat = params[idx : idx + k * k].reshape(k, k)
            idx += k * k

        return c_mat, a_mat, b_mat

    def xǁBEKKǁ_unpack_params__mutmut_40(
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
            b_mat = None
            idx += k * k

        return c_mat, a_mat, b_mat

    def xǁBEKKǁ_unpack_params__mutmut_41(
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
            b_mat = params[idx : idx + k * k].reshape(None, k)
            idx += k * k

        return c_mat, a_mat, b_mat

    def xǁBEKKǁ_unpack_params__mutmut_42(
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
            b_mat = params[idx : idx + k * k].reshape(k, None)
            idx += k * k

        return c_mat, a_mat, b_mat

    def xǁBEKKǁ_unpack_params__mutmut_43(
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
            b_mat = params[idx : idx + k * k].reshape(k)
            idx += k * k

        return c_mat, a_mat, b_mat

    def xǁBEKKǁ_unpack_params__mutmut_44(
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
            b_mat = params[idx : idx + k * k].reshape(
                k,
            )
            idx += k * k

        return c_mat, a_mat, b_mat

    def xǁBEKKǁ_unpack_params__mutmut_45(
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
            b_mat = params[idx : idx - k * k].reshape(k, k)
            idx += k * k

        return c_mat, a_mat, b_mat

    def xǁBEKKǁ_unpack_params__mutmut_46(
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
            b_mat = params[idx : idx + k / k].reshape(k, k)
            idx += k * k

        return c_mat, a_mat, b_mat

    def xǁBEKKǁ_unpack_params__mutmut_47(
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
            idx = k * k

        return c_mat, a_mat, b_mat

    def xǁBEKKǁ_unpack_params__mutmut_48(
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
            idx -= k * k

        return c_mat, a_mat, b_mat

    def xǁBEKKǁ_unpack_params__mutmut_49(
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
            idx += k / k

        return c_mat, a_mat, b_mat

    xǁBEKKǁ_unpack_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁBEKKǁ_unpack_params__mutmut_1": xǁBEKKǁ_unpack_params__mutmut_1,
        "xǁBEKKǁ_unpack_params__mutmut_2": xǁBEKKǁ_unpack_params__mutmut_2,
        "xǁBEKKǁ_unpack_params__mutmut_3": xǁBEKKǁ_unpack_params__mutmut_3,
        "xǁBEKKǁ_unpack_params__mutmut_4": xǁBEKKǁ_unpack_params__mutmut_4,
        "xǁBEKKǁ_unpack_params__mutmut_5": xǁBEKKǁ_unpack_params__mutmut_5,
        "xǁBEKKǁ_unpack_params__mutmut_6": xǁBEKKǁ_unpack_params__mutmut_6,
        "xǁBEKKǁ_unpack_params__mutmut_7": xǁBEKKǁ_unpack_params__mutmut_7,
        "xǁBEKKǁ_unpack_params__mutmut_8": xǁBEKKǁ_unpack_params__mutmut_8,
        "xǁBEKKǁ_unpack_params__mutmut_9": xǁBEKKǁ_unpack_params__mutmut_9,
        "xǁBEKKǁ_unpack_params__mutmut_10": xǁBEKKǁ_unpack_params__mutmut_10,
        "xǁBEKKǁ_unpack_params__mutmut_11": xǁBEKKǁ_unpack_params__mutmut_11,
        "xǁBEKKǁ_unpack_params__mutmut_12": xǁBEKKǁ_unpack_params__mutmut_12,
        "xǁBEKKǁ_unpack_params__mutmut_13": xǁBEKKǁ_unpack_params__mutmut_13,
        "xǁBEKKǁ_unpack_params__mutmut_14": xǁBEKKǁ_unpack_params__mutmut_14,
        "xǁBEKKǁ_unpack_params__mutmut_15": xǁBEKKǁ_unpack_params__mutmut_15,
        "xǁBEKKǁ_unpack_params__mutmut_16": xǁBEKKǁ_unpack_params__mutmut_16,
        "xǁBEKKǁ_unpack_params__mutmut_17": xǁBEKKǁ_unpack_params__mutmut_17,
        "xǁBEKKǁ_unpack_params__mutmut_18": xǁBEKKǁ_unpack_params__mutmut_18,
        "xǁBEKKǁ_unpack_params__mutmut_19": xǁBEKKǁ_unpack_params__mutmut_19,
        "xǁBEKKǁ_unpack_params__mutmut_20": xǁBEKKǁ_unpack_params__mutmut_20,
        "xǁBEKKǁ_unpack_params__mutmut_21": xǁBEKKǁ_unpack_params__mutmut_21,
        "xǁBEKKǁ_unpack_params__mutmut_22": xǁBEKKǁ_unpack_params__mutmut_22,
        "xǁBEKKǁ_unpack_params__mutmut_23": xǁBEKKǁ_unpack_params__mutmut_23,
        "xǁBEKKǁ_unpack_params__mutmut_24": xǁBEKKǁ_unpack_params__mutmut_24,
        "xǁBEKKǁ_unpack_params__mutmut_25": xǁBEKKǁ_unpack_params__mutmut_25,
        "xǁBEKKǁ_unpack_params__mutmut_26": xǁBEKKǁ_unpack_params__mutmut_26,
        "xǁBEKKǁ_unpack_params__mutmut_27": xǁBEKKǁ_unpack_params__mutmut_27,
        "xǁBEKKǁ_unpack_params__mutmut_28": xǁBEKKǁ_unpack_params__mutmut_28,
        "xǁBEKKǁ_unpack_params__mutmut_29": xǁBEKKǁ_unpack_params__mutmut_29,
        "xǁBEKKǁ_unpack_params__mutmut_30": xǁBEKKǁ_unpack_params__mutmut_30,
        "xǁBEKKǁ_unpack_params__mutmut_31": xǁBEKKǁ_unpack_params__mutmut_31,
        "xǁBEKKǁ_unpack_params__mutmut_32": xǁBEKKǁ_unpack_params__mutmut_32,
        "xǁBEKKǁ_unpack_params__mutmut_33": xǁBEKKǁ_unpack_params__mutmut_33,
        "xǁBEKKǁ_unpack_params__mutmut_34": xǁBEKKǁ_unpack_params__mutmut_34,
        "xǁBEKKǁ_unpack_params__mutmut_35": xǁBEKKǁ_unpack_params__mutmut_35,
        "xǁBEKKǁ_unpack_params__mutmut_36": xǁBEKKǁ_unpack_params__mutmut_36,
        "xǁBEKKǁ_unpack_params__mutmut_37": xǁBEKKǁ_unpack_params__mutmut_37,
        "xǁBEKKǁ_unpack_params__mutmut_38": xǁBEKKǁ_unpack_params__mutmut_38,
        "xǁBEKKǁ_unpack_params__mutmut_39": xǁBEKKǁ_unpack_params__mutmut_39,
        "xǁBEKKǁ_unpack_params__mutmut_40": xǁBEKKǁ_unpack_params__mutmut_40,
        "xǁBEKKǁ_unpack_params__mutmut_41": xǁBEKKǁ_unpack_params__mutmut_41,
        "xǁBEKKǁ_unpack_params__mutmut_42": xǁBEKKǁ_unpack_params__mutmut_42,
        "xǁBEKKǁ_unpack_params__mutmut_43": xǁBEKKǁ_unpack_params__mutmut_43,
        "xǁBEKKǁ_unpack_params__mutmut_44": xǁBEKKǁ_unpack_params__mutmut_44,
        "xǁBEKKǁ_unpack_params__mutmut_45": xǁBEKKǁ_unpack_params__mutmut_45,
        "xǁBEKKǁ_unpack_params__mutmut_46": xǁBEKKǁ_unpack_params__mutmut_46,
        "xǁBEKKǁ_unpack_params__mutmut_47": xǁBEKKǁ_unpack_params__mutmut_47,
        "xǁBEKKǁ_unpack_params__mutmut_48": xǁBEKKǁ_unpack_params__mutmut_48,
        "xǁBEKKǁ_unpack_params__mutmut_49": xǁBEKKǁ_unpack_params__mutmut_49,
    }
    xǁBEKKǁ_unpack_params__mutmut_orig.__name__ = "xǁBEKKǁ_unpack_params"

    def _pack_params(
        self,
        c_mat: NDArray[np.float64],
        a_mat: NDArray[np.float64],
        b_mat: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        args = [c_mat, a_mat, b_mat]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁBEKKǁ_pack_params__mutmut_orig"),
            object.__getattribute__(self, "xǁBEKKǁ_pack_params__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁBEKKǁ_pack_params__mutmut_orig(
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

    def xǁBEKKǁ_pack_params__mutmut_1(
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
        k = None
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

    def xǁBEKKǁ_pack_params__mutmut_2(
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
        params_list: list[float] = None

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

    def xǁBEKKǁ_pack_params__mutmut_3(
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
        for i in range(None):
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

    def xǁBEKKǁ_pack_params__mutmut_4(
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
            for j in range(None):
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

    def xǁBEKKǁ_pack_params__mutmut_5(
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
            for j in range(i - 1):
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

    def xǁBEKKǁ_pack_params__mutmut_6(
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
            for j in range(i + 2):
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

    def xǁBEKKǁ_pack_params__mutmut_7(
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
                params_list.append(None)

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

    def xǁBEKKǁ_pack_params__mutmut_8(
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
        if self.variant != "diagonal":
            params_list.extend(np.diag(a_mat).tolist())
        else:
            params_list.extend(a_mat.ravel().tolist())

        # b_mat
        if self.variant == "diagonal":
            params_list.extend(np.diag(b_mat).tolist())
        else:
            params_list.extend(b_mat.ravel().tolist())

        return np.array(params_list, dtype=np.float64)

    def xǁBEKKǁ_pack_params__mutmut_9(
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
        if self.variant == "XXdiagonalXX":
            params_list.extend(np.diag(a_mat).tolist())
        else:
            params_list.extend(a_mat.ravel().tolist())

        # b_mat
        if self.variant == "diagonal":
            params_list.extend(np.diag(b_mat).tolist())
        else:
            params_list.extend(b_mat.ravel().tolist())

        return np.array(params_list, dtype=np.float64)

    def xǁBEKKǁ_pack_params__mutmut_10(
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
        if self.variant == "DIAGONAL":
            params_list.extend(np.diag(a_mat).tolist())
        else:
            params_list.extend(a_mat.ravel().tolist())

        # b_mat
        if self.variant == "diagonal":
            params_list.extend(np.diag(b_mat).tolist())
        else:
            params_list.extend(b_mat.ravel().tolist())

        return np.array(params_list, dtype=np.float64)

    def xǁBEKKǁ_pack_params__mutmut_11(
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
            params_list.extend(None)
        else:
            params_list.extend(a_mat.ravel().tolist())

        # b_mat
        if self.variant == "diagonal":
            params_list.extend(np.diag(b_mat).tolist())
        else:
            params_list.extend(b_mat.ravel().tolist())

        return np.array(params_list, dtype=np.float64)

    def xǁBEKKǁ_pack_params__mutmut_12(
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
            params_list.extend(np.diag(None).tolist())
        else:
            params_list.extend(a_mat.ravel().tolist())

        # b_mat
        if self.variant == "diagonal":
            params_list.extend(np.diag(b_mat).tolist())
        else:
            params_list.extend(b_mat.ravel().tolist())

        return np.array(params_list, dtype=np.float64)

    def xǁBEKKǁ_pack_params__mutmut_13(
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
            params_list.extend(None)

        # b_mat
        if self.variant == "diagonal":
            params_list.extend(np.diag(b_mat).tolist())
        else:
            params_list.extend(b_mat.ravel().tolist())

        return np.array(params_list, dtype=np.float64)

    def xǁBEKKǁ_pack_params__mutmut_14(
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
        if self.variant != "diagonal":
            params_list.extend(np.diag(b_mat).tolist())
        else:
            params_list.extend(b_mat.ravel().tolist())

        return np.array(params_list, dtype=np.float64)

    def xǁBEKKǁ_pack_params__mutmut_15(
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
        if self.variant == "XXdiagonalXX":
            params_list.extend(np.diag(b_mat).tolist())
        else:
            params_list.extend(b_mat.ravel().tolist())

        return np.array(params_list, dtype=np.float64)

    def xǁBEKKǁ_pack_params__mutmut_16(
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
        if self.variant == "DIAGONAL":
            params_list.extend(np.diag(b_mat).tolist())
        else:
            params_list.extend(b_mat.ravel().tolist())

        return np.array(params_list, dtype=np.float64)

    def xǁBEKKǁ_pack_params__mutmut_17(
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
            params_list.extend(None)
        else:
            params_list.extend(b_mat.ravel().tolist())

        return np.array(params_list, dtype=np.float64)

    def xǁBEKKǁ_pack_params__mutmut_18(
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
            params_list.extend(np.diag(None).tolist())
        else:
            params_list.extend(b_mat.ravel().tolist())

        return np.array(params_list, dtype=np.float64)

    def xǁBEKKǁ_pack_params__mutmut_19(
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
            params_list.extend(None)

        return np.array(params_list, dtype=np.float64)

    def xǁBEKKǁ_pack_params__mutmut_20(
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

        return np.array(None, dtype=np.float64)

    def xǁBEKKǁ_pack_params__mutmut_21(
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

        return np.array(params_list, dtype=None)

    def xǁBEKKǁ_pack_params__mutmut_22(
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

        return np.array(dtype=np.float64)

    def xǁBEKKǁ_pack_params__mutmut_23(
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

        return np.array(
            params_list,
        )

    xǁBEKKǁ_pack_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁBEKKǁ_pack_params__mutmut_1": xǁBEKKǁ_pack_params__mutmut_1,
        "xǁBEKKǁ_pack_params__mutmut_2": xǁBEKKǁ_pack_params__mutmut_2,
        "xǁBEKKǁ_pack_params__mutmut_3": xǁBEKKǁ_pack_params__mutmut_3,
        "xǁBEKKǁ_pack_params__mutmut_4": xǁBEKKǁ_pack_params__mutmut_4,
        "xǁBEKKǁ_pack_params__mutmut_5": xǁBEKKǁ_pack_params__mutmut_5,
        "xǁBEKKǁ_pack_params__mutmut_6": xǁBEKKǁ_pack_params__mutmut_6,
        "xǁBEKKǁ_pack_params__mutmut_7": xǁBEKKǁ_pack_params__mutmut_7,
        "xǁBEKKǁ_pack_params__mutmut_8": xǁBEKKǁ_pack_params__mutmut_8,
        "xǁBEKKǁ_pack_params__mutmut_9": xǁBEKKǁ_pack_params__mutmut_9,
        "xǁBEKKǁ_pack_params__mutmut_10": xǁBEKKǁ_pack_params__mutmut_10,
        "xǁBEKKǁ_pack_params__mutmut_11": xǁBEKKǁ_pack_params__mutmut_11,
        "xǁBEKKǁ_pack_params__mutmut_12": xǁBEKKǁ_pack_params__mutmut_12,
        "xǁBEKKǁ_pack_params__mutmut_13": xǁBEKKǁ_pack_params__mutmut_13,
        "xǁBEKKǁ_pack_params__mutmut_14": xǁBEKKǁ_pack_params__mutmut_14,
        "xǁBEKKǁ_pack_params__mutmut_15": xǁBEKKǁ_pack_params__mutmut_15,
        "xǁBEKKǁ_pack_params__mutmut_16": xǁBEKKǁ_pack_params__mutmut_16,
        "xǁBEKKǁ_pack_params__mutmut_17": xǁBEKKǁ_pack_params__mutmut_17,
        "xǁBEKKǁ_pack_params__mutmut_18": xǁBEKKǁ_pack_params__mutmut_18,
        "xǁBEKKǁ_pack_params__mutmut_19": xǁBEKKǁ_pack_params__mutmut_19,
        "xǁBEKKǁ_pack_params__mutmut_20": xǁBEKKǁ_pack_params__mutmut_20,
        "xǁBEKKǁ_pack_params__mutmut_21": xǁBEKKǁ_pack_params__mutmut_21,
        "xǁBEKKǁ_pack_params__mutmut_22": xǁBEKKǁ_pack_params__mutmut_22,
        "xǁBEKKǁ_pack_params__mutmut_23": xǁBEKKǁ_pack_params__mutmut_23,
    }
    xǁBEKKǁ_pack_params__mutmut_orig.__name__ = "xǁBEKKǁ_pack_params"

    def _bekk_recursion(
        self,
        c_mat: NDArray[np.float64],
        a_mat: NDArray[np.float64],
        b_mat: NDArray[np.float64],
        resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        args = [c_mat, a_mat, b_mat, resids]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁBEKKǁ_bekk_recursion__mutmut_orig"),
            object.__getattribute__(self, "xǁBEKKǁ_bekk_recursion__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁBEKKǁ_bekk_recursion__mutmut_orig(
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

    def xǁBEKKǁ_bekk_recursion__mutmut_1(
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
        n_obs, k = None
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

    def xǁBEKKǁ_bekk_recursion__mutmut_2(
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
        h_t = None
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

    def xǁBEKKǁ_bekk_recursion__mutmut_3(
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
        h_t = np.zeros(None)
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

    def xǁBEKKǁ_bekk_recursion__mutmut_4(
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
        cc = None

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

    def xǁBEKKǁ_bekk_recursion__mutmut_5(
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
        h_t[0] = None
        if not is_positive_definite(h_t[0]):
            h_t[0] = cc + np.eye(k) * 1e-6

        for t in range(1, n_obs):
            eps = resids[t - 1 : t].T  # (k, 1)
            h_t[t] = cc + a_mat.T @ (eps @ eps.T) @ a_mat + b_mat.T @ h_t[t - 1] @ b_mat

            # Ensure symmetry
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0

        return h_t

    def xǁBEKKǁ_bekk_recursion__mutmut_6(
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
        h_t[1] = np.cov(resids.T)
        if not is_positive_definite(h_t[0]):
            h_t[0] = cc + np.eye(k) * 1e-6

        for t in range(1, n_obs):
            eps = resids[t - 1 : t].T  # (k, 1)
            h_t[t] = cc + a_mat.T @ (eps @ eps.T) @ a_mat + b_mat.T @ h_t[t - 1] @ b_mat

            # Ensure symmetry
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0

        return h_t

    def xǁBEKKǁ_bekk_recursion__mutmut_7(
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
        h_t[0] = np.cov(None)
        if not is_positive_definite(h_t[0]):
            h_t[0] = cc + np.eye(k) * 1e-6

        for t in range(1, n_obs):
            eps = resids[t - 1 : t].T  # (k, 1)
            h_t[t] = cc + a_mat.T @ (eps @ eps.T) @ a_mat + b_mat.T @ h_t[t - 1] @ b_mat

            # Ensure symmetry
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0

        return h_t

    def xǁBEKKǁ_bekk_recursion__mutmut_8(
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
        if is_positive_definite(h_t[0]):
            h_t[0] = cc + np.eye(k) * 1e-6

        for t in range(1, n_obs):
            eps = resids[t - 1 : t].T  # (k, 1)
            h_t[t] = cc + a_mat.T @ (eps @ eps.T) @ a_mat + b_mat.T @ h_t[t - 1] @ b_mat

            # Ensure symmetry
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0

        return h_t

    def xǁBEKKǁ_bekk_recursion__mutmut_9(
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
        if not is_positive_definite(None):
            h_t[0] = cc + np.eye(k) * 1e-6

        for t in range(1, n_obs):
            eps = resids[t - 1 : t].T  # (k, 1)
            h_t[t] = cc + a_mat.T @ (eps @ eps.T) @ a_mat + b_mat.T @ h_t[t - 1] @ b_mat

            # Ensure symmetry
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0

        return h_t

    def xǁBEKKǁ_bekk_recursion__mutmut_10(
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
        if not is_positive_definite(h_t[1]):
            h_t[0] = cc + np.eye(k) * 1e-6

        for t in range(1, n_obs):
            eps = resids[t - 1 : t].T  # (k, 1)
            h_t[t] = cc + a_mat.T @ (eps @ eps.T) @ a_mat + b_mat.T @ h_t[t - 1] @ b_mat

            # Ensure symmetry
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0

        return h_t

    def xǁBEKKǁ_bekk_recursion__mutmut_11(
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
            h_t[0] = None

        for t in range(1, n_obs):
            eps = resids[t - 1 : t].T  # (k, 1)
            h_t[t] = cc + a_mat.T @ (eps @ eps.T) @ a_mat + b_mat.T @ h_t[t - 1] @ b_mat

            # Ensure symmetry
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0

        return h_t

    def xǁBEKKǁ_bekk_recursion__mutmut_12(
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
            h_t[1] = cc + np.eye(k) * 1e-6

        for t in range(1, n_obs):
            eps = resids[t - 1 : t].T  # (k, 1)
            h_t[t] = cc + a_mat.T @ (eps @ eps.T) @ a_mat + b_mat.T @ h_t[t - 1] @ b_mat

            # Ensure symmetry
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0

        return h_t

    def xǁBEKKǁ_bekk_recursion__mutmut_13(
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
            h_t[0] = cc - np.eye(k) * 1e-6

        for t in range(1, n_obs):
            eps = resids[t - 1 : t].T  # (k, 1)
            h_t[t] = cc + a_mat.T @ (eps @ eps.T) @ a_mat + b_mat.T @ h_t[t - 1] @ b_mat

            # Ensure symmetry
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0

        return h_t

    def xǁBEKKǁ_bekk_recursion__mutmut_14(
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
            h_t[0] = cc + np.eye(k) / 1e-6

        for t in range(1, n_obs):
            eps = resids[t - 1 : t].T  # (k, 1)
            h_t[t] = cc + a_mat.T @ (eps @ eps.T) @ a_mat + b_mat.T @ h_t[t - 1] @ b_mat

            # Ensure symmetry
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0

        return h_t

    def xǁBEKKǁ_bekk_recursion__mutmut_15(
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
            h_t[0] = cc + np.eye(None) * 1e-6

        for t in range(1, n_obs):
            eps = resids[t - 1 : t].T  # (k, 1)
            h_t[t] = cc + a_mat.T @ (eps @ eps.T) @ a_mat + b_mat.T @ h_t[t - 1] @ b_mat

            # Ensure symmetry
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0

        return h_t

    def xǁBEKKǁ_bekk_recursion__mutmut_16(
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
            h_t[0] = cc + np.eye(k) * 1.000001

        for t in range(1, n_obs):
            eps = resids[t - 1 : t].T  # (k, 1)
            h_t[t] = cc + a_mat.T @ (eps @ eps.T) @ a_mat + b_mat.T @ h_t[t - 1] @ b_mat

            # Ensure symmetry
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0

        return h_t

    def xǁBEKKǁ_bekk_recursion__mutmut_17(
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

        for t in range(None, n_obs):
            eps = resids[t - 1 : t].T  # (k, 1)
            h_t[t] = cc + a_mat.T @ (eps @ eps.T) @ a_mat + b_mat.T @ h_t[t - 1] @ b_mat

            # Ensure symmetry
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0

        return h_t

    def xǁBEKKǁ_bekk_recursion__mutmut_18(
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

        for t in range(1, None):
            eps = resids[t - 1 : t].T  # (k, 1)
            h_t[t] = cc + a_mat.T @ (eps @ eps.T) @ a_mat + b_mat.T @ h_t[t - 1] @ b_mat

            # Ensure symmetry
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0

        return h_t

    def xǁBEKKǁ_bekk_recursion__mutmut_19(
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

        for t in range(n_obs):
            eps = resids[t - 1 : t].T  # (k, 1)
            h_t[t] = cc + a_mat.T @ (eps @ eps.T) @ a_mat + b_mat.T @ h_t[t - 1] @ b_mat

            # Ensure symmetry
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0

        return h_t

    def xǁBEKKǁ_bekk_recursion__mutmut_20(
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

        for t in range(
            1,
        ):
            eps = resids[t - 1 : t].T  # (k, 1)
            h_t[t] = cc + a_mat.T @ (eps @ eps.T) @ a_mat + b_mat.T @ h_t[t - 1] @ b_mat

            # Ensure symmetry
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0

        return h_t

    def xǁBEKKǁ_bekk_recursion__mutmut_21(
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

        for t in range(2, n_obs):
            eps = resids[t - 1 : t].T  # (k, 1)
            h_t[t] = cc + a_mat.T @ (eps @ eps.T) @ a_mat + b_mat.T @ h_t[t - 1] @ b_mat

            # Ensure symmetry
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0

        return h_t

    def xǁBEKKǁ_bekk_recursion__mutmut_22(
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
            eps = None  # (k, 1)
            h_t[t] = cc + a_mat.T @ (eps @ eps.T) @ a_mat + b_mat.T @ h_t[t - 1] @ b_mat

            # Ensure symmetry
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0

        return h_t

    def xǁBEKKǁ_bekk_recursion__mutmut_23(
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
            eps = resids[t + 1 : t].T  # (k, 1)
            h_t[t] = cc + a_mat.T @ (eps @ eps.T) @ a_mat + b_mat.T @ h_t[t - 1] @ b_mat

            # Ensure symmetry
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0

        return h_t

    def xǁBEKKǁ_bekk_recursion__mutmut_24(
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
            eps = resids[t - 2 : t].T  # (k, 1)
            h_t[t] = cc + a_mat.T @ (eps @ eps.T) @ a_mat + b_mat.T @ h_t[t - 1] @ b_mat

            # Ensure symmetry
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0

        return h_t

    def xǁBEKKǁ_bekk_recursion__mutmut_25(
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
            h_t[t] = None

            # Ensure symmetry
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0

        return h_t

    def xǁBEKKǁ_bekk_recursion__mutmut_26(
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
            h_t[t] = cc + a_mat.T @ (eps @ eps.T) @ a_mat - b_mat.T @ h_t[t - 1] @ b_mat

            # Ensure symmetry
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0

        return h_t

    def xǁBEKKǁ_bekk_recursion__mutmut_27(
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
            h_t[t] = cc - a_mat.T @ (eps @ eps.T) @ a_mat + b_mat.T @ h_t[t - 1] @ b_mat

            # Ensure symmetry
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0

        return h_t

    def xǁBEKKǁ_bekk_recursion__mutmut_28(
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
            h_t[t] = cc + a_mat.T @ (eps @ eps.T) @ a_mat + b_mat.T @ h_t[t + 1] @ b_mat

            # Ensure symmetry
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0

        return h_t

    def xǁBEKKǁ_bekk_recursion__mutmut_29(
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
            h_t[t] = cc + a_mat.T @ (eps @ eps.T) @ a_mat + b_mat.T @ h_t[t - 2] @ b_mat

            # Ensure symmetry
            h_t[t] = (h_t[t] + h_t[t].T) / 2.0

        return h_t

    def xǁBEKKǁ_bekk_recursion__mutmut_30(
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
            h_t[t] = None

        return h_t

    def xǁBEKKǁ_bekk_recursion__mutmut_31(
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
            h_t[t] = (h_t[t] + h_t[t].T) * 2.0

        return h_t

    def xǁBEKKǁ_bekk_recursion__mutmut_32(
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
            h_t[t] = (h_t[t] - h_t[t].T) / 2.0

        return h_t

    def xǁBEKKǁ_bekk_recursion__mutmut_33(
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
            h_t[t] = (h_t[t] + h_t[t].T) / 3.0

        return h_t

    xǁBEKKǁ_bekk_recursion__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁBEKKǁ_bekk_recursion__mutmut_1": xǁBEKKǁ_bekk_recursion__mutmut_1,
        "xǁBEKKǁ_bekk_recursion__mutmut_2": xǁBEKKǁ_bekk_recursion__mutmut_2,
        "xǁBEKKǁ_bekk_recursion__mutmut_3": xǁBEKKǁ_bekk_recursion__mutmut_3,
        "xǁBEKKǁ_bekk_recursion__mutmut_4": xǁBEKKǁ_bekk_recursion__mutmut_4,
        "xǁBEKKǁ_bekk_recursion__mutmut_5": xǁBEKKǁ_bekk_recursion__mutmut_5,
        "xǁBEKKǁ_bekk_recursion__mutmut_6": xǁBEKKǁ_bekk_recursion__mutmut_6,
        "xǁBEKKǁ_bekk_recursion__mutmut_7": xǁBEKKǁ_bekk_recursion__mutmut_7,
        "xǁBEKKǁ_bekk_recursion__mutmut_8": xǁBEKKǁ_bekk_recursion__mutmut_8,
        "xǁBEKKǁ_bekk_recursion__mutmut_9": xǁBEKKǁ_bekk_recursion__mutmut_9,
        "xǁBEKKǁ_bekk_recursion__mutmut_10": xǁBEKKǁ_bekk_recursion__mutmut_10,
        "xǁBEKKǁ_bekk_recursion__mutmut_11": xǁBEKKǁ_bekk_recursion__mutmut_11,
        "xǁBEKKǁ_bekk_recursion__mutmut_12": xǁBEKKǁ_bekk_recursion__mutmut_12,
        "xǁBEKKǁ_bekk_recursion__mutmut_13": xǁBEKKǁ_bekk_recursion__mutmut_13,
        "xǁBEKKǁ_bekk_recursion__mutmut_14": xǁBEKKǁ_bekk_recursion__mutmut_14,
        "xǁBEKKǁ_bekk_recursion__mutmut_15": xǁBEKKǁ_bekk_recursion__mutmut_15,
        "xǁBEKKǁ_bekk_recursion__mutmut_16": xǁBEKKǁ_bekk_recursion__mutmut_16,
        "xǁBEKKǁ_bekk_recursion__mutmut_17": xǁBEKKǁ_bekk_recursion__mutmut_17,
        "xǁBEKKǁ_bekk_recursion__mutmut_18": xǁBEKKǁ_bekk_recursion__mutmut_18,
        "xǁBEKKǁ_bekk_recursion__mutmut_19": xǁBEKKǁ_bekk_recursion__mutmut_19,
        "xǁBEKKǁ_bekk_recursion__mutmut_20": xǁBEKKǁ_bekk_recursion__mutmut_20,
        "xǁBEKKǁ_bekk_recursion__mutmut_21": xǁBEKKǁ_bekk_recursion__mutmut_21,
        "xǁBEKKǁ_bekk_recursion__mutmut_22": xǁBEKKǁ_bekk_recursion__mutmut_22,
        "xǁBEKKǁ_bekk_recursion__mutmut_23": xǁBEKKǁ_bekk_recursion__mutmut_23,
        "xǁBEKKǁ_bekk_recursion__mutmut_24": xǁBEKKǁ_bekk_recursion__mutmut_24,
        "xǁBEKKǁ_bekk_recursion__mutmut_25": xǁBEKKǁ_bekk_recursion__mutmut_25,
        "xǁBEKKǁ_bekk_recursion__mutmut_26": xǁBEKKǁ_bekk_recursion__mutmut_26,
        "xǁBEKKǁ_bekk_recursion__mutmut_27": xǁBEKKǁ_bekk_recursion__mutmut_27,
        "xǁBEKKǁ_bekk_recursion__mutmut_28": xǁBEKKǁ_bekk_recursion__mutmut_28,
        "xǁBEKKǁ_bekk_recursion__mutmut_29": xǁBEKKǁ_bekk_recursion__mutmut_29,
        "xǁBEKKǁ_bekk_recursion__mutmut_30": xǁBEKKǁ_bekk_recursion__mutmut_30,
        "xǁBEKKǁ_bekk_recursion__mutmut_31": xǁBEKKǁ_bekk_recursion__mutmut_31,
        "xǁBEKKǁ_bekk_recursion__mutmut_32": xǁBEKKǁ_bekk_recursion__mutmut_32,
        "xǁBEKKǁ_bekk_recursion__mutmut_33": xǁBEKKǁ_bekk_recursion__mutmut_33,
    }
    xǁBEKKǁ_bekk_recursion__mutmut_orig.__name__ = "xǁBEKKǁ_bekk_recursion"

    def _correlation_recursion(
        self,
        params: NDArray[np.float64],
        std_resids: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        args = [params, std_resids]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁBEKKǁ_correlation_recursion__mutmut_orig"),
            object.__getattribute__(self, "xǁBEKKǁ_correlation_recursion__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁBEKKǁ_correlation_recursion__mutmut_orig(
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

    def xǁBEKKǁ_correlation_recursion__mutmut_1(
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
        n_obs, k = None
        r_t = np.zeros((n_obs, k, k))
        for t in range(n_obs):
            r_t[t] = np.eye(k)
        return r_t

    def xǁBEKKǁ_correlation_recursion__mutmut_2(
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
        r_t = None
        for t in range(n_obs):
            r_t[t] = np.eye(k)
        return r_t

    def xǁBEKKǁ_correlation_recursion__mutmut_3(
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
        r_t = np.zeros(None)
        for t in range(n_obs):
            r_t[t] = np.eye(k)
        return r_t

    def xǁBEKKǁ_correlation_recursion__mutmut_4(
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
        for t in range(None):
            r_t[t] = np.eye(k)
        return r_t

    def xǁBEKKǁ_correlation_recursion__mutmut_5(
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
            r_t[t] = None
        return r_t

    def xǁBEKKǁ_correlation_recursion__mutmut_6(
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
            r_t[t] = np.eye(None)
        return r_t

    xǁBEKKǁ_correlation_recursion__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁBEKKǁ_correlation_recursion__mutmut_1": xǁBEKKǁ_correlation_recursion__mutmut_1,
        "xǁBEKKǁ_correlation_recursion__mutmut_2": xǁBEKKǁ_correlation_recursion__mutmut_2,
        "xǁBEKKǁ_correlation_recursion__mutmut_3": xǁBEKKǁ_correlation_recursion__mutmut_3,
        "xǁBEKKǁ_correlation_recursion__mutmut_4": xǁBEKKǁ_correlation_recursion__mutmut_4,
        "xǁBEKKǁ_correlation_recursion__mutmut_5": xǁBEKKǁ_correlation_recursion__mutmut_5,
        "xǁBEKKǁ_correlation_recursion__mutmut_6": xǁBEKKǁ_correlation_recursion__mutmut_6,
    }
    xǁBEKKǁ_correlation_recursion__mutmut_orig.__name__ = "xǁBEKKǁ_correlation_recursion"

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
        args = [method, disp]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁBEKKǁfit__mutmut_orig"),
            object.__getattribute__(self, "xǁBEKKǁfit__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁBEKKǁfit__mutmut_orig(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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

    def xǁBEKKǁfit__mutmut_1(self, method: str = "XXmleXX", disp: bool = True) -> MultivarResults:
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

    def xǁBEKKǁfit__mutmut_2(self, method: str = "MLE", disp: bool = True) -> MultivarResults:
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

    def xǁBEKKǁfit__mutmut_3(self, method: str = "mle", disp: bool = False) -> MultivarResults:
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

    def xǁBEKKǁfit__mutmut_4(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        mu = None
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

    def xǁBEKKǁfit__mutmut_5(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        mu = np.mean(None, axis=0)
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

    def xǁBEKKǁfit__mutmut_6(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        mu = np.mean(self.endog, axis=None)
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

    def xǁBEKKǁfit__mutmut_7(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        mu = np.mean(axis=0)
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

    def xǁBEKKǁfit__mutmut_8(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        mu = np.mean(
            self.endog,
        )
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

    def xǁBEKKǁfit__mutmut_9(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        mu = np.mean(self.endog, axis=1)
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

    def xǁBEKKǁfit__mutmut_10(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        resids = None

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

    def xǁBEKKǁfit__mutmut_11(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        resids = self.endog + mu

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

    def xǁBEKKǁfit__mutmut_12(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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

        x0 = None

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

    def xǁBEKKǁfit__mutmut_13(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            c_mat, a_mat, b_mat = None
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

    def xǁBEKKǁfit__mutmut_14(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            c_mat, a_mat, b_mat = self._unpack_params(None)
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

    def xǁBEKKǁfit__mutmut_15(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            h_t = None

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

    def xǁBEKKǁfit__mutmut_16(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            h_t = self._bekk_recursion(None, a_mat, b_mat, resids)

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

    def xǁBEKKǁfit__mutmut_17(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            h_t = self._bekk_recursion(c_mat, None, b_mat, resids)

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

    def xǁBEKKǁfit__mutmut_18(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            h_t = self._bekk_recursion(c_mat, a_mat, None, resids)

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

    def xǁBEKKǁfit__mutmut_19(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            h_t = self._bekk_recursion(c_mat, a_mat, b_mat, None)

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

    def xǁBEKKǁfit__mutmut_20(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            h_t = self._bekk_recursion(a_mat, b_mat, resids)

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

    def xǁBEKKǁfit__mutmut_21(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            h_t = self._bekk_recursion(c_mat, b_mat, resids)

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

    def xǁBEKKǁfit__mutmut_22(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            h_t = self._bekk_recursion(c_mat, a_mat, resids)

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

    def xǁBEKKǁfit__mutmut_23(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            h_t = self._bekk_recursion(
                c_mat,
                a_mat,
                b_mat,
            )

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

    def xǁBEKKǁfit__mutmut_24(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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

            n_obs, k = None
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

    def xǁBEKKǁfit__mutmut_25(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            ll = None
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

    def xǁBEKKǁfit__mutmut_26(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            ll = 1.0
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

    def xǁBEKKǁfit__mutmut_27(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            const = None

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

    def xǁBEKKǁfit__mutmut_28(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            const = k / np.log(2.0 * np.pi)

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

    def xǁBEKKǁfit__mutmut_29(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            const = k * np.log(None)

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

    def xǁBEKKǁfit__mutmut_30(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            const = k * np.log(2.0 / np.pi)

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

    def xǁBEKKǁfit__mutmut_31(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            const = k * np.log(3.0 * np.pi)

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

    def xǁBEKKǁfit__mutmut_32(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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

            for t in range(None):
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

    def xǁBEKKǁfit__mutmut_33(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
                if is_positive_definite(h_t[t]):
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

    def xǁBEKKǁfit__mutmut_34(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
                if not is_positive_definite(None):
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

    def xǁBEKKǁfit__mutmut_35(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
                    return 10000000001.0
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

    def xǁBEKKǁfit__mutmut_36(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
                    sign, logdet = None
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

    def xǁBEKKǁfit__mutmut_37(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
                    sign, logdet = np.linalg.slogdet(None)
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

    def xǁBEKKǁfit__mutmut_38(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
                    if sign < 0:
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

    def xǁBEKKǁfit__mutmut_39(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
                    if sign <= 1:
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

    def xǁBEKKǁfit__mutmut_40(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
                        return 10000000001.0
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

    def xǁBEKKǁfit__mutmut_41(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
                    eps = None  # (k, 1)
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

    def xǁBEKKǁfit__mutmut_42(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
                    eps = resids[t : t - 1].T  # (k, 1)
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

    def xǁBEKKǁfit__mutmut_43(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
                    eps = resids[t : t + 2].T  # (k, 1)
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

    def xǁBEKKǁfit__mutmut_44(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
                    h_inv_eps = None
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

    def xǁBEKKǁfit__mutmut_45(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
                    h_inv_eps = np.linalg.solve(None, eps)
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

    def xǁBEKKǁfit__mutmut_46(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
                    h_inv_eps = np.linalg.solve(h_t[t], None)
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

    def xǁBEKKǁfit__mutmut_47(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
                    h_inv_eps = np.linalg.solve(eps)
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

    def xǁBEKKǁfit__mutmut_48(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
                    h_inv_eps = np.linalg.solve(
                        h_t[t],
                    )
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

    def xǁBEKKǁfit__mutmut_49(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
                    quad = None
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

    def xǁBEKKǁfit__mutmut_50(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
                    quad = float(None)
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

    def xǁBEKKǁfit__mutmut_51(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
                    ll = -0.5 * (const + logdet + quad)
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

    def xǁBEKKǁfit__mutmut_52(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
                    ll -= -0.5 * (const + logdet + quad)
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

    def xǁBEKKǁfit__mutmut_53(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
                    ll += -0.5 / (const + logdet + quad)
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

    def xǁBEKKǁfit__mutmut_54(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
                    ll += +0.5 * (const + logdet + quad)
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

    def xǁBEKKǁfit__mutmut_55(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
                    ll += -1.5 * (const + logdet + quad)
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

    def xǁBEKKǁfit__mutmut_56(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
                    ll += -0.5 * (const + logdet - quad)
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

    def xǁBEKKǁfit__mutmut_57(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
                    ll += -0.5 * (const - logdet + quad)
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

    def xǁBEKKǁfit__mutmut_58(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
                    return 10000000001.0

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

    def xǁBEKKǁfit__mutmut_59(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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

            return +ll

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

    def xǁBEKKǁfit__mutmut_60(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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

        result = None

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

    def xǁBEKKǁfit__mutmut_61(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            None,
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

    def xǁBEKKǁfit__mutmut_62(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            None,
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

    def xǁBEKKǁfit__mutmut_63(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            method=None,
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

    def xǁBEKKǁfit__mutmut_64(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            options=None,
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

    def xǁBEKKǁfit__mutmut_65(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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

    def xǁBEKKǁfit__mutmut_66(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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

    def xǁBEKKǁfit__mutmut_67(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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

    def xǁBEKKǁfit__mutmut_68(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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

    def xǁBEKKǁfit__mutmut_69(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            method="XXSLSQPXX",
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

    def xǁBEKKǁfit__mutmut_70(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            method="slsqp",
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

    def xǁBEKKǁfit__mutmut_71(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            options={"XXmaxiterXX": 1000, "disp": disp, "ftol": 1e-8},
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

    def xǁBEKKǁfit__mutmut_72(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            options={"MAXITER": 1000, "disp": disp, "ftol": 1e-8},
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

    def xǁBEKKǁfit__mutmut_73(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            options={"maxiter": 1001, "disp": disp, "ftol": 1e-8},
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

    def xǁBEKKǁfit__mutmut_74(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            options={"maxiter": 1000, "XXdispXX": disp, "ftol": 1e-8},
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

    def xǁBEKKǁfit__mutmut_75(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            options={"maxiter": 1000, "DISP": disp, "ftol": 1e-8},
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

    def xǁBEKKǁfit__mutmut_76(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            options={"maxiter": 1000, "disp": disp, "XXftolXX": 1e-8},
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

    def xǁBEKKǁfit__mutmut_77(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            options={"maxiter": 1000, "disp": disp, "FTOL": 1e-8},
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

    def xǁBEKKǁfit__mutmut_78(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            options={"maxiter": 1000, "disp": disp, "ftol": 1.00000001},
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

    def xǁBEKKǁfit__mutmut_79(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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

        opt_params = None
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

    def xǁBEKKǁfit__mutmut_80(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        c_mat, a_mat, b_mat = None
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

    def xǁBEKKǁfit__mutmut_81(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        c_mat, a_mat, b_mat = self._unpack_params(None)
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

    def xǁBEKKǁfit__mutmut_82(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        h_t = None

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

    def xǁBEKKǁfit__mutmut_83(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        h_t = self._bekk_recursion(None, a_mat, b_mat, resids)

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

    def xǁBEKKǁfit__mutmut_84(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        h_t = self._bekk_recursion(c_mat, None, b_mat, resids)

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

    def xǁBEKKǁfit__mutmut_85(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        h_t = self._bekk_recursion(c_mat, a_mat, None, resids)

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

    def xǁBEKKǁfit__mutmut_86(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        h_t = self._bekk_recursion(c_mat, a_mat, b_mat, None)

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

    def xǁBEKKǁfit__mutmut_87(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        h_t = self._bekk_recursion(a_mat, b_mat, resids)

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

    def xǁBEKKǁfit__mutmut_88(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        h_t = self._bekk_recursion(c_mat, b_mat, resids)

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

    def xǁBEKKǁfit__mutmut_89(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        h_t = self._bekk_recursion(c_mat, a_mat, resids)

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

    def xǁBEKKǁfit__mutmut_90(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        h_t = self._bekk_recursion(
            c_mat,
            a_mat,
            b_mat,
        )

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

    def xǁBEKKǁfit__mutmut_91(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        r_t = None
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

    def xǁBEKKǁfit__mutmut_92(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        r_t = np.zeros_like(None)
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

    def xǁBEKKǁfit__mutmut_93(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        cond_vol = None
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

    def xǁBEKKǁfit__mutmut_94(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        cond_vol = np.zeros(None)
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

    def xǁBEKKǁfit__mutmut_95(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        for t in range(None):
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

    def xǁBEKKǁfit__mutmut_96(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            d = None
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

    def xǁBEKKǁfit__mutmut_97(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            d = np.sqrt(None)
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

    def xǁBEKKǁfit__mutmut_98(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            d = np.sqrt(np.diag(None))
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

    def xǁBEKKǁfit__mutmut_99(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            d = None
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

    def xǁBEKKǁfit__mutmut_100(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            d = np.maximum(None, 1e-12)
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

    def xǁBEKKǁfit__mutmut_101(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            d = np.maximum(d, None)
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

    def xǁBEKKǁfit__mutmut_102(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            d = np.maximum(1e-12)
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

    def xǁBEKKǁfit__mutmut_103(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            d = np.maximum(
                d,
            )
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

    def xǁBEKKǁfit__mutmut_104(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            d = np.maximum(d, 1.000000000001)
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

    def xǁBEKKǁfit__mutmut_105(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            cond_vol[t] = None
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

    def xǁBEKKǁfit__mutmut_106(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            r_t[t] = None

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

    def xǁBEKKǁfit__mutmut_107(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            r_t[t] = h_t[t] * np.outer(d, d)

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

    def xǁBEKKǁfit__mutmut_108(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            r_t[t] = h_t[t] / np.outer(None, d)

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

    def xǁBEKKǁfit__mutmut_109(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            r_t[t] = h_t[t] / np.outer(d, None)

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

    def xǁBEKKǁfit__mutmut_110(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            r_t[t] = h_t[t] / np.outer(d)

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

    def xǁBEKKǁfit__mutmut_111(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            r_t[t] = h_t[t] / np.outer(
                d,
            )

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

    def xǁBEKKǁfit__mutmut_112(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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

        loglike = None

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

    def xǁBEKKǁfit__mutmut_113(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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

        loglike = +result.fun

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

    def xǁBEKKǁfit__mutmut_114(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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

        n_params = None
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

    def xǁBEKKǁfit__mutmut_115(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        aic = None
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

    def xǁBEKKǁfit__mutmut_116(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        aic = -2.0 * loglike - 2.0 * n_params
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

    def xǁBEKKǁfit__mutmut_117(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        aic = -2.0 / loglike + 2.0 * n_params
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

    def xǁBEKKǁfit__mutmut_118(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        aic = +2.0 * loglike + 2.0 * n_params
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

    def xǁBEKKǁfit__mutmut_119(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        aic = -3.0 * loglike + 2.0 * n_params
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

    def xǁBEKKǁfit__mutmut_120(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        aic = -2.0 * loglike + 2.0 / n_params
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

    def xǁBEKKǁfit__mutmut_121(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        aic = -2.0 * loglike + 3.0 * n_params
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

    def xǁBEKKǁfit__mutmut_122(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        bic = None

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

    def xǁBEKKǁfit__mutmut_123(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        bic = -2.0 * loglike - np.log(self.T) * n_params

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

    def xǁBEKKǁfit__mutmut_124(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        bic = -2.0 / loglike + np.log(self.T) * n_params

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

    def xǁBEKKǁfit__mutmut_125(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        bic = +2.0 * loglike + np.log(self.T) * n_params

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

    def xǁBEKKǁfit__mutmut_126(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        bic = -3.0 * loglike + np.log(self.T) * n_params

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

    def xǁBEKKǁfit__mutmut_127(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        bic = -2.0 * loglike + np.log(self.T) / n_params

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

    def xǁBEKKǁfit__mutmut_128(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        bic = -2.0 * loglike + np.log(None) * n_params

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

    def xǁBEKKǁfit__mutmut_129(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        std_resids = None
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

    def xǁBEKKǁfit__mutmut_130(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        std_resids = np.zeros(None)
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

    def xǁBEKKǁfit__mutmut_131(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        for t in range(None):
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

    def xǁBEKKǁfit__mutmut_132(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            std_resids[t] = None

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

    def xǁBEKKǁfit__mutmut_133(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            std_resids[t] = resids[t] * cond_vol[t]

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

    def xǁBEKKǁfit__mutmut_134(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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

        self._is_fitted = None

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

    def xǁBEKKǁfit__mutmut_135(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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

        self._is_fitted = False

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

    def xǁBEKKǁfit__mutmut_136(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            model=None,
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

    def xǁBEKKǁfit__mutmut_137(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            univariate_results=None,  # BEKK does not use univariate step
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

    def xǁBEKKǁfit__mutmut_138(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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

    def xǁBEKKǁfit__mutmut_139(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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

    def xǁBEKKǁfit__mutmut_140(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            dynamic_covariance=None,
            conditional_volatility=cond_vol,
            std_resids=std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁBEKKǁfit__mutmut_141(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            conditional_volatility=None,
            std_resids=std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁBEKKǁfit__mutmut_142(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            std_resids=None,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁBEKKǁfit__mutmut_143(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            loglike=None,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁBEKKǁfit__mutmut_144(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            aic=None,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁBEKKǁfit__mutmut_145(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            bic=None,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁBEKKǁfit__mutmut_146(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            n_obs=None,
            n_series=self.k,
        )

    def xǁBEKKǁfit__mutmut_147(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            n_series=None,
        )

    def xǁBEKKǁfit__mutmut_148(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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

    def xǁBEKKǁfit__mutmut_149(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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

    def xǁBEKKǁfit__mutmut_150(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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

    def xǁBEKKǁfit__mutmut_151(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            dynamic_covariance=h_t,
            conditional_volatility=cond_vol,
            std_resids=std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁBEKKǁfit__mutmut_152(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            conditional_volatility=cond_vol,
            std_resids=std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁBEKKǁfit__mutmut_153(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            std_resids=std_resids,
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁBEKKǁfit__mutmut_154(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            loglike=loglike,
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁBEKKǁfit__mutmut_155(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            aic=aic,
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁBEKKǁfit__mutmut_156(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            bic=bic,
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁBEKKǁfit__mutmut_157(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            n_obs=self.T,
            n_series=self.k,
        )

    def xǁBEKKǁfit__mutmut_158(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
            n_series=self.k,
        )

    def xǁBEKKǁfit__mutmut_159(self, method: str = "mle", disp: bool = True) -> MultivarResults:
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
        )

    xǁBEKKǁfit__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁBEKKǁfit__mutmut_1": xǁBEKKǁfit__mutmut_1,
        "xǁBEKKǁfit__mutmut_2": xǁBEKKǁfit__mutmut_2,
        "xǁBEKKǁfit__mutmut_3": xǁBEKKǁfit__mutmut_3,
        "xǁBEKKǁfit__mutmut_4": xǁBEKKǁfit__mutmut_4,
        "xǁBEKKǁfit__mutmut_5": xǁBEKKǁfit__mutmut_5,
        "xǁBEKKǁfit__mutmut_6": xǁBEKKǁfit__mutmut_6,
        "xǁBEKKǁfit__mutmut_7": xǁBEKKǁfit__mutmut_7,
        "xǁBEKKǁfit__mutmut_8": xǁBEKKǁfit__mutmut_8,
        "xǁBEKKǁfit__mutmut_9": xǁBEKKǁfit__mutmut_9,
        "xǁBEKKǁfit__mutmut_10": xǁBEKKǁfit__mutmut_10,
        "xǁBEKKǁfit__mutmut_11": xǁBEKKǁfit__mutmut_11,
        "xǁBEKKǁfit__mutmut_12": xǁBEKKǁfit__mutmut_12,
        "xǁBEKKǁfit__mutmut_13": xǁBEKKǁfit__mutmut_13,
        "xǁBEKKǁfit__mutmut_14": xǁBEKKǁfit__mutmut_14,
        "xǁBEKKǁfit__mutmut_15": xǁBEKKǁfit__mutmut_15,
        "xǁBEKKǁfit__mutmut_16": xǁBEKKǁfit__mutmut_16,
        "xǁBEKKǁfit__mutmut_17": xǁBEKKǁfit__mutmut_17,
        "xǁBEKKǁfit__mutmut_18": xǁBEKKǁfit__mutmut_18,
        "xǁBEKKǁfit__mutmut_19": xǁBEKKǁfit__mutmut_19,
        "xǁBEKKǁfit__mutmut_20": xǁBEKKǁfit__mutmut_20,
        "xǁBEKKǁfit__mutmut_21": xǁBEKKǁfit__mutmut_21,
        "xǁBEKKǁfit__mutmut_22": xǁBEKKǁfit__mutmut_22,
        "xǁBEKKǁfit__mutmut_23": xǁBEKKǁfit__mutmut_23,
        "xǁBEKKǁfit__mutmut_24": xǁBEKKǁfit__mutmut_24,
        "xǁBEKKǁfit__mutmut_25": xǁBEKKǁfit__mutmut_25,
        "xǁBEKKǁfit__mutmut_26": xǁBEKKǁfit__mutmut_26,
        "xǁBEKKǁfit__mutmut_27": xǁBEKKǁfit__mutmut_27,
        "xǁBEKKǁfit__mutmut_28": xǁBEKKǁfit__mutmut_28,
        "xǁBEKKǁfit__mutmut_29": xǁBEKKǁfit__mutmut_29,
        "xǁBEKKǁfit__mutmut_30": xǁBEKKǁfit__mutmut_30,
        "xǁBEKKǁfit__mutmut_31": xǁBEKKǁfit__mutmut_31,
        "xǁBEKKǁfit__mutmut_32": xǁBEKKǁfit__mutmut_32,
        "xǁBEKKǁfit__mutmut_33": xǁBEKKǁfit__mutmut_33,
        "xǁBEKKǁfit__mutmut_34": xǁBEKKǁfit__mutmut_34,
        "xǁBEKKǁfit__mutmut_35": xǁBEKKǁfit__mutmut_35,
        "xǁBEKKǁfit__mutmut_36": xǁBEKKǁfit__mutmut_36,
        "xǁBEKKǁfit__mutmut_37": xǁBEKKǁfit__mutmut_37,
        "xǁBEKKǁfit__mutmut_38": xǁBEKKǁfit__mutmut_38,
        "xǁBEKKǁfit__mutmut_39": xǁBEKKǁfit__mutmut_39,
        "xǁBEKKǁfit__mutmut_40": xǁBEKKǁfit__mutmut_40,
        "xǁBEKKǁfit__mutmut_41": xǁBEKKǁfit__mutmut_41,
        "xǁBEKKǁfit__mutmut_42": xǁBEKKǁfit__mutmut_42,
        "xǁBEKKǁfit__mutmut_43": xǁBEKKǁfit__mutmut_43,
        "xǁBEKKǁfit__mutmut_44": xǁBEKKǁfit__mutmut_44,
        "xǁBEKKǁfit__mutmut_45": xǁBEKKǁfit__mutmut_45,
        "xǁBEKKǁfit__mutmut_46": xǁBEKKǁfit__mutmut_46,
        "xǁBEKKǁfit__mutmut_47": xǁBEKKǁfit__mutmut_47,
        "xǁBEKKǁfit__mutmut_48": xǁBEKKǁfit__mutmut_48,
        "xǁBEKKǁfit__mutmut_49": xǁBEKKǁfit__mutmut_49,
        "xǁBEKKǁfit__mutmut_50": xǁBEKKǁfit__mutmut_50,
        "xǁBEKKǁfit__mutmut_51": xǁBEKKǁfit__mutmut_51,
        "xǁBEKKǁfit__mutmut_52": xǁBEKKǁfit__mutmut_52,
        "xǁBEKKǁfit__mutmut_53": xǁBEKKǁfit__mutmut_53,
        "xǁBEKKǁfit__mutmut_54": xǁBEKKǁfit__mutmut_54,
        "xǁBEKKǁfit__mutmut_55": xǁBEKKǁfit__mutmut_55,
        "xǁBEKKǁfit__mutmut_56": xǁBEKKǁfit__mutmut_56,
        "xǁBEKKǁfit__mutmut_57": xǁBEKKǁfit__mutmut_57,
        "xǁBEKKǁfit__mutmut_58": xǁBEKKǁfit__mutmut_58,
        "xǁBEKKǁfit__mutmut_59": xǁBEKKǁfit__mutmut_59,
        "xǁBEKKǁfit__mutmut_60": xǁBEKKǁfit__mutmut_60,
        "xǁBEKKǁfit__mutmut_61": xǁBEKKǁfit__mutmut_61,
        "xǁBEKKǁfit__mutmut_62": xǁBEKKǁfit__mutmut_62,
        "xǁBEKKǁfit__mutmut_63": xǁBEKKǁfit__mutmut_63,
        "xǁBEKKǁfit__mutmut_64": xǁBEKKǁfit__mutmut_64,
        "xǁBEKKǁfit__mutmut_65": xǁBEKKǁfit__mutmut_65,
        "xǁBEKKǁfit__mutmut_66": xǁBEKKǁfit__mutmut_66,
        "xǁBEKKǁfit__mutmut_67": xǁBEKKǁfit__mutmut_67,
        "xǁBEKKǁfit__mutmut_68": xǁBEKKǁfit__mutmut_68,
        "xǁBEKKǁfit__mutmut_69": xǁBEKKǁfit__mutmut_69,
        "xǁBEKKǁfit__mutmut_70": xǁBEKKǁfit__mutmut_70,
        "xǁBEKKǁfit__mutmut_71": xǁBEKKǁfit__mutmut_71,
        "xǁBEKKǁfit__mutmut_72": xǁBEKKǁfit__mutmut_72,
        "xǁBEKKǁfit__mutmut_73": xǁBEKKǁfit__mutmut_73,
        "xǁBEKKǁfit__mutmut_74": xǁBEKKǁfit__mutmut_74,
        "xǁBEKKǁfit__mutmut_75": xǁBEKKǁfit__mutmut_75,
        "xǁBEKKǁfit__mutmut_76": xǁBEKKǁfit__mutmut_76,
        "xǁBEKKǁfit__mutmut_77": xǁBEKKǁfit__mutmut_77,
        "xǁBEKKǁfit__mutmut_78": xǁBEKKǁfit__mutmut_78,
        "xǁBEKKǁfit__mutmut_79": xǁBEKKǁfit__mutmut_79,
        "xǁBEKKǁfit__mutmut_80": xǁBEKKǁfit__mutmut_80,
        "xǁBEKKǁfit__mutmut_81": xǁBEKKǁfit__mutmut_81,
        "xǁBEKKǁfit__mutmut_82": xǁBEKKǁfit__mutmut_82,
        "xǁBEKKǁfit__mutmut_83": xǁBEKKǁfit__mutmut_83,
        "xǁBEKKǁfit__mutmut_84": xǁBEKKǁfit__mutmut_84,
        "xǁBEKKǁfit__mutmut_85": xǁBEKKǁfit__mutmut_85,
        "xǁBEKKǁfit__mutmut_86": xǁBEKKǁfit__mutmut_86,
        "xǁBEKKǁfit__mutmut_87": xǁBEKKǁfit__mutmut_87,
        "xǁBEKKǁfit__mutmut_88": xǁBEKKǁfit__mutmut_88,
        "xǁBEKKǁfit__mutmut_89": xǁBEKKǁfit__mutmut_89,
        "xǁBEKKǁfit__mutmut_90": xǁBEKKǁfit__mutmut_90,
        "xǁBEKKǁfit__mutmut_91": xǁBEKKǁfit__mutmut_91,
        "xǁBEKKǁfit__mutmut_92": xǁBEKKǁfit__mutmut_92,
        "xǁBEKKǁfit__mutmut_93": xǁBEKKǁfit__mutmut_93,
        "xǁBEKKǁfit__mutmut_94": xǁBEKKǁfit__mutmut_94,
        "xǁBEKKǁfit__mutmut_95": xǁBEKKǁfit__mutmut_95,
        "xǁBEKKǁfit__mutmut_96": xǁBEKKǁfit__mutmut_96,
        "xǁBEKKǁfit__mutmut_97": xǁBEKKǁfit__mutmut_97,
        "xǁBEKKǁfit__mutmut_98": xǁBEKKǁfit__mutmut_98,
        "xǁBEKKǁfit__mutmut_99": xǁBEKKǁfit__mutmut_99,
        "xǁBEKKǁfit__mutmut_100": xǁBEKKǁfit__mutmut_100,
        "xǁBEKKǁfit__mutmut_101": xǁBEKKǁfit__mutmut_101,
        "xǁBEKKǁfit__mutmut_102": xǁBEKKǁfit__mutmut_102,
        "xǁBEKKǁfit__mutmut_103": xǁBEKKǁfit__mutmut_103,
        "xǁBEKKǁfit__mutmut_104": xǁBEKKǁfit__mutmut_104,
        "xǁBEKKǁfit__mutmut_105": xǁBEKKǁfit__mutmut_105,
        "xǁBEKKǁfit__mutmut_106": xǁBEKKǁfit__mutmut_106,
        "xǁBEKKǁfit__mutmut_107": xǁBEKKǁfit__mutmut_107,
        "xǁBEKKǁfit__mutmut_108": xǁBEKKǁfit__mutmut_108,
        "xǁBEKKǁfit__mutmut_109": xǁBEKKǁfit__mutmut_109,
        "xǁBEKKǁfit__mutmut_110": xǁBEKKǁfit__mutmut_110,
        "xǁBEKKǁfit__mutmut_111": xǁBEKKǁfit__mutmut_111,
        "xǁBEKKǁfit__mutmut_112": xǁBEKKǁfit__mutmut_112,
        "xǁBEKKǁfit__mutmut_113": xǁBEKKǁfit__mutmut_113,
        "xǁBEKKǁfit__mutmut_114": xǁBEKKǁfit__mutmut_114,
        "xǁBEKKǁfit__mutmut_115": xǁBEKKǁfit__mutmut_115,
        "xǁBEKKǁfit__mutmut_116": xǁBEKKǁfit__mutmut_116,
        "xǁBEKKǁfit__mutmut_117": xǁBEKKǁfit__mutmut_117,
        "xǁBEKKǁfit__mutmut_118": xǁBEKKǁfit__mutmut_118,
        "xǁBEKKǁfit__mutmut_119": xǁBEKKǁfit__mutmut_119,
        "xǁBEKKǁfit__mutmut_120": xǁBEKKǁfit__mutmut_120,
        "xǁBEKKǁfit__mutmut_121": xǁBEKKǁfit__mutmut_121,
        "xǁBEKKǁfit__mutmut_122": xǁBEKKǁfit__mutmut_122,
        "xǁBEKKǁfit__mutmut_123": xǁBEKKǁfit__mutmut_123,
        "xǁBEKKǁfit__mutmut_124": xǁBEKKǁfit__mutmut_124,
        "xǁBEKKǁfit__mutmut_125": xǁBEKKǁfit__mutmut_125,
        "xǁBEKKǁfit__mutmut_126": xǁBEKKǁfit__mutmut_126,
        "xǁBEKKǁfit__mutmut_127": xǁBEKKǁfit__mutmut_127,
        "xǁBEKKǁfit__mutmut_128": xǁBEKKǁfit__mutmut_128,
        "xǁBEKKǁfit__mutmut_129": xǁBEKKǁfit__mutmut_129,
        "xǁBEKKǁfit__mutmut_130": xǁBEKKǁfit__mutmut_130,
        "xǁBEKKǁfit__mutmut_131": xǁBEKKǁfit__mutmut_131,
        "xǁBEKKǁfit__mutmut_132": xǁBEKKǁfit__mutmut_132,
        "xǁBEKKǁfit__mutmut_133": xǁBEKKǁfit__mutmut_133,
        "xǁBEKKǁfit__mutmut_134": xǁBEKKǁfit__mutmut_134,
        "xǁBEKKǁfit__mutmut_135": xǁBEKKǁfit__mutmut_135,
        "xǁBEKKǁfit__mutmut_136": xǁBEKKǁfit__mutmut_136,
        "xǁBEKKǁfit__mutmut_137": xǁBEKKǁfit__mutmut_137,
        "xǁBEKKǁfit__mutmut_138": xǁBEKKǁfit__mutmut_138,
        "xǁBEKKǁfit__mutmut_139": xǁBEKKǁfit__mutmut_139,
        "xǁBEKKǁfit__mutmut_140": xǁBEKKǁfit__mutmut_140,
        "xǁBEKKǁfit__mutmut_141": xǁBEKKǁfit__mutmut_141,
        "xǁBEKKǁfit__mutmut_142": xǁBEKKǁfit__mutmut_142,
        "xǁBEKKǁfit__mutmut_143": xǁBEKKǁfit__mutmut_143,
        "xǁBEKKǁfit__mutmut_144": xǁBEKKǁfit__mutmut_144,
        "xǁBEKKǁfit__mutmut_145": xǁBEKKǁfit__mutmut_145,
        "xǁBEKKǁfit__mutmut_146": xǁBEKKǁfit__mutmut_146,
        "xǁBEKKǁfit__mutmut_147": xǁBEKKǁfit__mutmut_147,
        "xǁBEKKǁfit__mutmut_148": xǁBEKKǁfit__mutmut_148,
        "xǁBEKKǁfit__mutmut_149": xǁBEKKǁfit__mutmut_149,
        "xǁBEKKǁfit__mutmut_150": xǁBEKKǁfit__mutmut_150,
        "xǁBEKKǁfit__mutmut_151": xǁBEKKǁfit__mutmut_151,
        "xǁBEKKǁfit__mutmut_152": xǁBEKKǁfit__mutmut_152,
        "xǁBEKKǁfit__mutmut_153": xǁBEKKǁfit__mutmut_153,
        "xǁBEKKǁfit__mutmut_154": xǁBEKKǁfit__mutmut_154,
        "xǁBEKKǁfit__mutmut_155": xǁBEKKǁfit__mutmut_155,
        "xǁBEKKǁfit__mutmut_156": xǁBEKKǁfit__mutmut_156,
        "xǁBEKKǁfit__mutmut_157": xǁBEKKǁfit__mutmut_157,
        "xǁBEKKǁfit__mutmut_158": xǁBEKKǁfit__mutmut_158,
        "xǁBEKKǁfit__mutmut_159": xǁBEKKǁfit__mutmut_159,
    }
    xǁBEKKǁfit__mutmut_orig.__name__ = "xǁBEKKǁfit"

    def forecast(
        self,
        results: MultivarResults,
        horizon: int = 10,
    ) -> dict[str, NDArray[np.float64]]:
        args = [results, horizon]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁBEKKǁforecast__mutmut_orig"),
            object.__getattribute__(self, "xǁBEKKǁforecast__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁBEKKǁforecast__mutmut_orig(
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

    def xǁBEKKǁforecast__mutmut_1(
        self,
        results: MultivarResults,
        horizon: int = 11,
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

    def xǁBEKKǁforecast__mutmut_2(
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
        c_mat, a_mat, b_mat = None
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

    def xǁBEKKǁforecast__mutmut_3(
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
        c_mat, a_mat, b_mat = self._unpack_params(None)
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

    def xǁBEKKǁforecast__mutmut_4(
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
        cc = None

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

    def xǁBEKKǁforecast__mutmut_5(
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

        h_forecast = None
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

    def xǁBEKKǁforecast__mutmut_6(
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

        h_forecast = np.zeros(None)
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

    def xǁBEKKǁforecast__mutmut_7(
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
        r_forecast = None

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

    def xǁBEKKǁforecast__mutmut_8(
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
        r_forecast = np.zeros(None)

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

    def xǁBEKKǁforecast__mutmut_9(
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
        h_prev = None

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

    def xǁBEKKǁforecast__mutmut_10(
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
        h_prev = results.dynamic_covariance[+1].copy()

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

    def xǁBEKKǁforecast__mutmut_11(
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
        h_prev = results.dynamic_covariance[-2].copy()

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

    def xǁBEKKǁforecast__mutmut_12(
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

        for h in range(None):
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

    def xǁBEKKǁforecast__mutmut_13(
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
            h_next = None
            h_next = (h_next + h_next.T) / 2.0
            h_forecast[h] = h_next

            # Derive R from H
            d = np.sqrt(np.diag(h_next))
            d = np.maximum(d, 1e-12)
            r_forecast[h] = h_next / np.outer(d, d)

            h_prev = h_next

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁBEKKǁforecast__mutmut_14(
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
            h_next = cc + a_mat.T @ h_prev @ a_mat - b_mat.T @ h_prev @ b_mat
            h_next = (h_next + h_next.T) / 2.0
            h_forecast[h] = h_next

            # Derive R from H
            d = np.sqrt(np.diag(h_next))
            d = np.maximum(d, 1e-12)
            r_forecast[h] = h_next / np.outer(d, d)

            h_prev = h_next

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁBEKKǁforecast__mutmut_15(
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
            h_next = cc - a_mat.T @ h_prev @ a_mat + b_mat.T @ h_prev @ b_mat
            h_next = (h_next + h_next.T) / 2.0
            h_forecast[h] = h_next

            # Derive R from H
            d = np.sqrt(np.diag(h_next))
            d = np.maximum(d, 1e-12)
            r_forecast[h] = h_next / np.outer(d, d)

            h_prev = h_next

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁBEKKǁforecast__mutmut_16(
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
            h_next = None
            h_forecast[h] = h_next

            # Derive R from H
            d = np.sqrt(np.diag(h_next))
            d = np.maximum(d, 1e-12)
            r_forecast[h] = h_next / np.outer(d, d)

            h_prev = h_next

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁBEKKǁforecast__mutmut_17(
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
            h_next = (h_next + h_next.T) * 2.0
            h_forecast[h] = h_next

            # Derive R from H
            d = np.sqrt(np.diag(h_next))
            d = np.maximum(d, 1e-12)
            r_forecast[h] = h_next / np.outer(d, d)

            h_prev = h_next

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁBEKKǁforecast__mutmut_18(
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
            h_next = (h_next - h_next.T) / 2.0
            h_forecast[h] = h_next

            # Derive R from H
            d = np.sqrt(np.diag(h_next))
            d = np.maximum(d, 1e-12)
            r_forecast[h] = h_next / np.outer(d, d)

            h_prev = h_next

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁBEKKǁforecast__mutmut_19(
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
            h_next = (h_next + h_next.T) / 3.0
            h_forecast[h] = h_next

            # Derive R from H
            d = np.sqrt(np.diag(h_next))
            d = np.maximum(d, 1e-12)
            r_forecast[h] = h_next / np.outer(d, d)

            h_prev = h_next

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁBEKKǁforecast__mutmut_20(
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
            h_forecast[h] = None

            # Derive R from H
            d = np.sqrt(np.diag(h_next))
            d = np.maximum(d, 1e-12)
            r_forecast[h] = h_next / np.outer(d, d)

            h_prev = h_next

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁBEKKǁforecast__mutmut_21(
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
            d = None
            d = np.maximum(d, 1e-12)
            r_forecast[h] = h_next / np.outer(d, d)

            h_prev = h_next

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁBEKKǁforecast__mutmut_22(
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
            d = np.sqrt(None)
            d = np.maximum(d, 1e-12)
            r_forecast[h] = h_next / np.outer(d, d)

            h_prev = h_next

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁBEKKǁforecast__mutmut_23(
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
            d = np.sqrt(np.diag(None))
            d = np.maximum(d, 1e-12)
            r_forecast[h] = h_next / np.outer(d, d)

            h_prev = h_next

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁBEKKǁforecast__mutmut_24(
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
            d = None
            r_forecast[h] = h_next / np.outer(d, d)

            h_prev = h_next

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁBEKKǁforecast__mutmut_25(
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
            d = np.maximum(None, 1e-12)
            r_forecast[h] = h_next / np.outer(d, d)

            h_prev = h_next

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁBEKKǁforecast__mutmut_26(
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
            d = np.maximum(d, None)
            r_forecast[h] = h_next / np.outer(d, d)

            h_prev = h_next

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁBEKKǁforecast__mutmut_27(
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
            d = np.maximum(1e-12)
            r_forecast[h] = h_next / np.outer(d, d)

            h_prev = h_next

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁBEKKǁforecast__mutmut_28(
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
            d = np.maximum(
                d,
            )
            r_forecast[h] = h_next / np.outer(d, d)

            h_prev = h_next

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁBEKKǁforecast__mutmut_29(
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
            d = np.maximum(d, 1.000000000001)
            r_forecast[h] = h_next / np.outer(d, d)

            h_prev = h_next

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁBEKKǁforecast__mutmut_30(
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
            r_forecast[h] = None

            h_prev = h_next

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁBEKKǁforecast__mutmut_31(
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
            r_forecast[h] = h_next * np.outer(d, d)

            h_prev = h_next

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁBEKKǁforecast__mutmut_32(
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
            r_forecast[h] = h_next / np.outer(None, d)

            h_prev = h_next

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁBEKKǁforecast__mutmut_33(
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
            r_forecast[h] = h_next / np.outer(d, None)

            h_prev = h_next

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁBEKKǁforecast__mutmut_34(
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
            r_forecast[h] = h_next / np.outer(d)

            h_prev = h_next

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁBEKKǁforecast__mutmut_35(
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
            r_forecast[h] = h_next / np.outer(
                d,
            )

            h_prev = h_next

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁBEKKǁforecast__mutmut_36(
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

            h_prev = None

        return {"covariance": h_forecast, "correlation": r_forecast}

    def xǁBEKKǁforecast__mutmut_37(
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

        return {"XXcovarianceXX": h_forecast, "correlation": r_forecast}

    def xǁBEKKǁforecast__mutmut_38(
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

        return {"COVARIANCE": h_forecast, "correlation": r_forecast}

    def xǁBEKKǁforecast__mutmut_39(
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

        return {"covariance": h_forecast, "XXcorrelationXX": r_forecast}

    def xǁBEKKǁforecast__mutmut_40(
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

        return {"covariance": h_forecast, "CORRELATION": r_forecast}

    xǁBEKKǁforecast__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁBEKKǁforecast__mutmut_1": xǁBEKKǁforecast__mutmut_1,
        "xǁBEKKǁforecast__mutmut_2": xǁBEKKǁforecast__mutmut_2,
        "xǁBEKKǁforecast__mutmut_3": xǁBEKKǁforecast__mutmut_3,
        "xǁBEKKǁforecast__mutmut_4": xǁBEKKǁforecast__mutmut_4,
        "xǁBEKKǁforecast__mutmut_5": xǁBEKKǁforecast__mutmut_5,
        "xǁBEKKǁforecast__mutmut_6": xǁBEKKǁforecast__mutmut_6,
        "xǁBEKKǁforecast__mutmut_7": xǁBEKKǁforecast__mutmut_7,
        "xǁBEKKǁforecast__mutmut_8": xǁBEKKǁforecast__mutmut_8,
        "xǁBEKKǁforecast__mutmut_9": xǁBEKKǁforecast__mutmut_9,
        "xǁBEKKǁforecast__mutmut_10": xǁBEKKǁforecast__mutmut_10,
        "xǁBEKKǁforecast__mutmut_11": xǁBEKKǁforecast__mutmut_11,
        "xǁBEKKǁforecast__mutmut_12": xǁBEKKǁforecast__mutmut_12,
        "xǁBEKKǁforecast__mutmut_13": xǁBEKKǁforecast__mutmut_13,
        "xǁBEKKǁforecast__mutmut_14": xǁBEKKǁforecast__mutmut_14,
        "xǁBEKKǁforecast__mutmut_15": xǁBEKKǁforecast__mutmut_15,
        "xǁBEKKǁforecast__mutmut_16": xǁBEKKǁforecast__mutmut_16,
        "xǁBEKKǁforecast__mutmut_17": xǁBEKKǁforecast__mutmut_17,
        "xǁBEKKǁforecast__mutmut_18": xǁBEKKǁforecast__mutmut_18,
        "xǁBEKKǁforecast__mutmut_19": xǁBEKKǁforecast__mutmut_19,
        "xǁBEKKǁforecast__mutmut_20": xǁBEKKǁforecast__mutmut_20,
        "xǁBEKKǁforecast__mutmut_21": xǁBEKKǁforecast__mutmut_21,
        "xǁBEKKǁforecast__mutmut_22": xǁBEKKǁforecast__mutmut_22,
        "xǁBEKKǁforecast__mutmut_23": xǁBEKKǁforecast__mutmut_23,
        "xǁBEKKǁforecast__mutmut_24": xǁBEKKǁforecast__mutmut_24,
        "xǁBEKKǁforecast__mutmut_25": xǁBEKKǁforecast__mutmut_25,
        "xǁBEKKǁforecast__mutmut_26": xǁBEKKǁforecast__mutmut_26,
        "xǁBEKKǁforecast__mutmut_27": xǁBEKKǁforecast__mutmut_27,
        "xǁBEKKǁforecast__mutmut_28": xǁBEKKǁforecast__mutmut_28,
        "xǁBEKKǁforecast__mutmut_29": xǁBEKKǁforecast__mutmut_29,
        "xǁBEKKǁforecast__mutmut_30": xǁBEKKǁforecast__mutmut_30,
        "xǁBEKKǁforecast__mutmut_31": xǁBEKKǁforecast__mutmut_31,
        "xǁBEKKǁforecast__mutmut_32": xǁBEKKǁforecast__mutmut_32,
        "xǁBEKKǁforecast__mutmut_33": xǁBEKKǁforecast__mutmut_33,
        "xǁBEKKǁforecast__mutmut_34": xǁBEKKǁforecast__mutmut_34,
        "xǁBEKKǁforecast__mutmut_35": xǁBEKKǁforecast__mutmut_35,
        "xǁBEKKǁforecast__mutmut_36": xǁBEKKǁforecast__mutmut_36,
        "xǁBEKKǁforecast__mutmut_37": xǁBEKKǁforecast__mutmut_37,
        "xǁBEKKǁforecast__mutmut_38": xǁBEKKǁforecast__mutmut_38,
        "xǁBEKKǁforecast__mutmut_39": xǁBEKKǁforecast__mutmut_39,
        "xǁBEKKǁforecast__mutmut_40": xǁBEKKǁforecast__mutmut_40,
    }
    xǁBEKKǁforecast__mutmut_orig.__name__ = "xǁBEKKǁforecast"
