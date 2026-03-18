"""Markov-Switching GARCH model (Gray, 1996).

Implements GARCH with regime-switching parameters using the Gray (1996)
collapsing approach to handle path-dependence.

References
----------
Gray, S.F. (1996). Modeling the Conditional Distribution of Interest Rates
as a Regime-Switching Process. Journal of Financial Economics, 42(1), 27-62.

Haas, M., Mittnik, S. & Paolella, M.S. (2004). A New Approach to
Markov-Switching GARCH Models. Journal of Financial Econometrics, 2(4), 493-530.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Annotated, Any, ClassVar

import numpy as np
from numpy.typing import NDArray

from archbox.regime.base import MarkovSwitchingModel

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


class MarkovSwitchingGARCH(MarkovSwitchingModel):
    """Markov-Switching GARCH model (Gray, 1996).

    sigma^2_t(s) = omega_s + alpha_s * eps^2_{t-1} + beta_s * h_{t-1}
    h_{t-1} = sum_j P(S_{t-1}=j | Y_{t-1}) * sigma^2_{t-1}(j)

    Parameters
    ----------
    endog : array-like
        Time series of returns, shape (T,).
    k_regimes : int
        Number of regimes. Default is 2.
    p : int
        GARCH order (number of lagged variances). Default is 1.
    q : int
        ARCH order (number of lagged squared residuals). Default is 1.
    method : str
        Collapsing method: 'gray' (default) or 'haas'.

    Examples
    --------
    >>> import numpy as np
    >>> from archbox.regime.ms_garch import MarkovSwitchingGARCH
    >>> returns = np.random.randn(500) * 0.01
    >>> model = MarkovSwitchingGARCH(returns, k_regimes=2, p=1, q=1)
    >>> results = model.fit()
    >>> print(results.summary())
    """

    model_name: str = "MS-GARCH"

    def __init__(
        self,
        endog: Any,
        k_regimes: int = 2,
        p: int = 1,
        q: int = 1,
        method: str = "gray",
    ) -> None:
        args = [endog, k_regimes, p, q, method]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMarkovSwitchingGARCHǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁMarkovSwitchingGARCHǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMarkovSwitchingGARCHǁ__init____mutmut_orig(
        self,
        endog: Any,
        k_regimes: int = 2,
        p: int = 1,
        q: int = 1,
        method: str = "gray",
    ) -> None:
        """Initialize Markov-Switching GARCH model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=max(p, q),
            switching_mean=False,
            switching_variance=True,
            switching_ar=False,
        )
        self.p_garch = p
        self.q_arch = q
        self.method = method

        # Pre-computed conditional variances per regime, updated during EM
        self._sigma2: NDArray[np.float64] | None = None
        self._h_collapsed: NDArray[np.float64] | None = None
        self._filtered_probs_cache: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingGARCHǁ__init____mutmut_1(
        self,
        endog: Any,
        k_regimes: int = 3,
        p: int = 1,
        q: int = 1,
        method: str = "gray",
    ) -> None:
        """Initialize Markov-Switching GARCH model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=max(p, q),
            switching_mean=False,
            switching_variance=True,
            switching_ar=False,
        )
        self.p_garch = p
        self.q_arch = q
        self.method = method

        # Pre-computed conditional variances per regime, updated during EM
        self._sigma2: NDArray[np.float64] | None = None
        self._h_collapsed: NDArray[np.float64] | None = None
        self._filtered_probs_cache: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingGARCHǁ__init____mutmut_2(
        self,
        endog: Any,
        k_regimes: int = 2,
        p: int = 2,
        q: int = 1,
        method: str = "gray",
    ) -> None:
        """Initialize Markov-Switching GARCH model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=max(p, q),
            switching_mean=False,
            switching_variance=True,
            switching_ar=False,
        )
        self.p_garch = p
        self.q_arch = q
        self.method = method

        # Pre-computed conditional variances per regime, updated during EM
        self._sigma2: NDArray[np.float64] | None = None
        self._h_collapsed: NDArray[np.float64] | None = None
        self._filtered_probs_cache: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingGARCHǁ__init____mutmut_3(
        self,
        endog: Any,
        k_regimes: int = 2,
        p: int = 1,
        q: int = 2,
        method: str = "gray",
    ) -> None:
        """Initialize Markov-Switching GARCH model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=max(p, q),
            switching_mean=False,
            switching_variance=True,
            switching_ar=False,
        )
        self.p_garch = p
        self.q_arch = q
        self.method = method

        # Pre-computed conditional variances per regime, updated during EM
        self._sigma2: NDArray[np.float64] | None = None
        self._h_collapsed: NDArray[np.float64] | None = None
        self._filtered_probs_cache: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingGARCHǁ__init____mutmut_4(
        self,
        endog: Any,
        k_regimes: int = 2,
        p: int = 1,
        q: int = 1,
        method: str = "XXgrayXX",
    ) -> None:
        """Initialize Markov-Switching GARCH model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=max(p, q),
            switching_mean=False,
            switching_variance=True,
            switching_ar=False,
        )
        self.p_garch = p
        self.q_arch = q
        self.method = method

        # Pre-computed conditional variances per regime, updated during EM
        self._sigma2: NDArray[np.float64] | None = None
        self._h_collapsed: NDArray[np.float64] | None = None
        self._filtered_probs_cache: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingGARCHǁ__init____mutmut_5(
        self,
        endog: Any,
        k_regimes: int = 2,
        p: int = 1,
        q: int = 1,
        method: str = "GRAY",
    ) -> None:
        """Initialize Markov-Switching GARCH model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=max(p, q),
            switching_mean=False,
            switching_variance=True,
            switching_ar=False,
        )
        self.p_garch = p
        self.q_arch = q
        self.method = method

        # Pre-computed conditional variances per regime, updated during EM
        self._sigma2: NDArray[np.float64] | None = None
        self._h_collapsed: NDArray[np.float64] | None = None
        self._filtered_probs_cache: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingGARCHǁ__init____mutmut_6(
        self,
        endog: Any,
        k_regimes: int = 2,
        p: int = 1,
        q: int = 1,
        method: str = "gray",
    ) -> None:
        """Initialize Markov-Switching GARCH model with regime configuration."""
        super().__init__(
            None,
            k_regimes=k_regimes,
            order=max(p, q),
            switching_mean=False,
            switching_variance=True,
            switching_ar=False,
        )
        self.p_garch = p
        self.q_arch = q
        self.method = method

        # Pre-computed conditional variances per regime, updated during EM
        self._sigma2: NDArray[np.float64] | None = None
        self._h_collapsed: NDArray[np.float64] | None = None
        self._filtered_probs_cache: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingGARCHǁ__init____mutmut_7(
        self,
        endog: Any,
        k_regimes: int = 2,
        p: int = 1,
        q: int = 1,
        method: str = "gray",
    ) -> None:
        """Initialize Markov-Switching GARCH model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=None,
            order=max(p, q),
            switching_mean=False,
            switching_variance=True,
            switching_ar=False,
        )
        self.p_garch = p
        self.q_arch = q
        self.method = method

        # Pre-computed conditional variances per regime, updated during EM
        self._sigma2: NDArray[np.float64] | None = None
        self._h_collapsed: NDArray[np.float64] | None = None
        self._filtered_probs_cache: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingGARCHǁ__init____mutmut_8(
        self,
        endog: Any,
        k_regimes: int = 2,
        p: int = 1,
        q: int = 1,
        method: str = "gray",
    ) -> None:
        """Initialize Markov-Switching GARCH model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=None,
            switching_mean=False,
            switching_variance=True,
            switching_ar=False,
        )
        self.p_garch = p
        self.q_arch = q
        self.method = method

        # Pre-computed conditional variances per regime, updated during EM
        self._sigma2: NDArray[np.float64] | None = None
        self._h_collapsed: NDArray[np.float64] | None = None
        self._filtered_probs_cache: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingGARCHǁ__init____mutmut_9(
        self,
        endog: Any,
        k_regimes: int = 2,
        p: int = 1,
        q: int = 1,
        method: str = "gray",
    ) -> None:
        """Initialize Markov-Switching GARCH model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=max(p, q),
            switching_mean=None,
            switching_variance=True,
            switching_ar=False,
        )
        self.p_garch = p
        self.q_arch = q
        self.method = method

        # Pre-computed conditional variances per regime, updated during EM
        self._sigma2: NDArray[np.float64] | None = None
        self._h_collapsed: NDArray[np.float64] | None = None
        self._filtered_probs_cache: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingGARCHǁ__init____mutmut_10(
        self,
        endog: Any,
        k_regimes: int = 2,
        p: int = 1,
        q: int = 1,
        method: str = "gray",
    ) -> None:
        """Initialize Markov-Switching GARCH model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=max(p, q),
            switching_mean=False,
            switching_variance=None,
            switching_ar=False,
        )
        self.p_garch = p
        self.q_arch = q
        self.method = method

        # Pre-computed conditional variances per regime, updated during EM
        self._sigma2: NDArray[np.float64] | None = None
        self._h_collapsed: NDArray[np.float64] | None = None
        self._filtered_probs_cache: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingGARCHǁ__init____mutmut_11(
        self,
        endog: Any,
        k_regimes: int = 2,
        p: int = 1,
        q: int = 1,
        method: str = "gray",
    ) -> None:
        """Initialize Markov-Switching GARCH model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=max(p, q),
            switching_mean=False,
            switching_variance=True,
            switching_ar=None,
        )
        self.p_garch = p
        self.q_arch = q
        self.method = method

        # Pre-computed conditional variances per regime, updated during EM
        self._sigma2: NDArray[np.float64] | None = None
        self._h_collapsed: NDArray[np.float64] | None = None
        self._filtered_probs_cache: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingGARCHǁ__init____mutmut_12(
        self,
        endog: Any,
        k_regimes: int = 2,
        p: int = 1,
        q: int = 1,
        method: str = "gray",
    ) -> None:
        """Initialize Markov-Switching GARCH model with regime configuration."""
        super().__init__(
            k_regimes=k_regimes,
            order=max(p, q),
            switching_mean=False,
            switching_variance=True,
            switching_ar=False,
        )
        self.p_garch = p
        self.q_arch = q
        self.method = method

        # Pre-computed conditional variances per regime, updated during EM
        self._sigma2: NDArray[np.float64] | None = None
        self._h_collapsed: NDArray[np.float64] | None = None
        self._filtered_probs_cache: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingGARCHǁ__init____mutmut_13(
        self,
        endog: Any,
        k_regimes: int = 2,
        p: int = 1,
        q: int = 1,
        method: str = "gray",
    ) -> None:
        """Initialize Markov-Switching GARCH model with regime configuration."""
        super().__init__(
            endog,
            order=max(p, q),
            switching_mean=False,
            switching_variance=True,
            switching_ar=False,
        )
        self.p_garch = p
        self.q_arch = q
        self.method = method

        # Pre-computed conditional variances per regime, updated during EM
        self._sigma2: NDArray[np.float64] | None = None
        self._h_collapsed: NDArray[np.float64] | None = None
        self._filtered_probs_cache: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingGARCHǁ__init____mutmut_14(
        self,
        endog: Any,
        k_regimes: int = 2,
        p: int = 1,
        q: int = 1,
        method: str = "gray",
    ) -> None:
        """Initialize Markov-Switching GARCH model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            switching_mean=False,
            switching_variance=True,
            switching_ar=False,
        )
        self.p_garch = p
        self.q_arch = q
        self.method = method

        # Pre-computed conditional variances per regime, updated during EM
        self._sigma2: NDArray[np.float64] | None = None
        self._h_collapsed: NDArray[np.float64] | None = None
        self._filtered_probs_cache: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingGARCHǁ__init____mutmut_15(
        self,
        endog: Any,
        k_regimes: int = 2,
        p: int = 1,
        q: int = 1,
        method: str = "gray",
    ) -> None:
        """Initialize Markov-Switching GARCH model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=max(p, q),
            switching_variance=True,
            switching_ar=False,
        )
        self.p_garch = p
        self.q_arch = q
        self.method = method

        # Pre-computed conditional variances per regime, updated during EM
        self._sigma2: NDArray[np.float64] | None = None
        self._h_collapsed: NDArray[np.float64] | None = None
        self._filtered_probs_cache: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingGARCHǁ__init____mutmut_16(
        self,
        endog: Any,
        k_regimes: int = 2,
        p: int = 1,
        q: int = 1,
        method: str = "gray",
    ) -> None:
        """Initialize Markov-Switching GARCH model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=max(p, q),
            switching_mean=False,
            switching_ar=False,
        )
        self.p_garch = p
        self.q_arch = q
        self.method = method

        # Pre-computed conditional variances per regime, updated during EM
        self._sigma2: NDArray[np.float64] | None = None
        self._h_collapsed: NDArray[np.float64] | None = None
        self._filtered_probs_cache: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingGARCHǁ__init____mutmut_17(
        self,
        endog: Any,
        k_regimes: int = 2,
        p: int = 1,
        q: int = 1,
        method: str = "gray",
    ) -> None:
        """Initialize Markov-Switching GARCH model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=max(p, q),
            switching_mean=False,
            switching_variance=True,
        )
        self.p_garch = p
        self.q_arch = q
        self.method = method

        # Pre-computed conditional variances per regime, updated during EM
        self._sigma2: NDArray[np.float64] | None = None
        self._h_collapsed: NDArray[np.float64] | None = None
        self._filtered_probs_cache: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingGARCHǁ__init____mutmut_18(
        self,
        endog: Any,
        k_regimes: int = 2,
        p: int = 1,
        q: int = 1,
        method: str = "gray",
    ) -> None:
        """Initialize Markov-Switching GARCH model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=max(None, q),
            switching_mean=False,
            switching_variance=True,
            switching_ar=False,
        )
        self.p_garch = p
        self.q_arch = q
        self.method = method

        # Pre-computed conditional variances per regime, updated during EM
        self._sigma2: NDArray[np.float64] | None = None
        self._h_collapsed: NDArray[np.float64] | None = None
        self._filtered_probs_cache: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingGARCHǁ__init____mutmut_19(
        self,
        endog: Any,
        k_regimes: int = 2,
        p: int = 1,
        q: int = 1,
        method: str = "gray",
    ) -> None:
        """Initialize Markov-Switching GARCH model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=max(p, None),
            switching_mean=False,
            switching_variance=True,
            switching_ar=False,
        )
        self.p_garch = p
        self.q_arch = q
        self.method = method

        # Pre-computed conditional variances per regime, updated during EM
        self._sigma2: NDArray[np.float64] | None = None
        self._h_collapsed: NDArray[np.float64] | None = None
        self._filtered_probs_cache: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingGARCHǁ__init____mutmut_20(
        self,
        endog: Any,
        k_regimes: int = 2,
        p: int = 1,
        q: int = 1,
        method: str = "gray",
    ) -> None:
        """Initialize Markov-Switching GARCH model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=max(q),
            switching_mean=False,
            switching_variance=True,
            switching_ar=False,
        )
        self.p_garch = p
        self.q_arch = q
        self.method = method

        # Pre-computed conditional variances per regime, updated during EM
        self._sigma2: NDArray[np.float64] | None = None
        self._h_collapsed: NDArray[np.float64] | None = None
        self._filtered_probs_cache: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingGARCHǁ__init____mutmut_21(
        self,
        endog: Any,
        k_regimes: int = 2,
        p: int = 1,
        q: int = 1,
        method: str = "gray",
    ) -> None:
        """Initialize Markov-Switching GARCH model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=max(
                p,
            ),
            switching_mean=False,
            switching_variance=True,
            switching_ar=False,
        )
        self.p_garch = p
        self.q_arch = q
        self.method = method

        # Pre-computed conditional variances per regime, updated during EM
        self._sigma2: NDArray[np.float64] | None = None
        self._h_collapsed: NDArray[np.float64] | None = None
        self._filtered_probs_cache: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingGARCHǁ__init____mutmut_22(
        self,
        endog: Any,
        k_regimes: int = 2,
        p: int = 1,
        q: int = 1,
        method: str = "gray",
    ) -> None:
        """Initialize Markov-Switching GARCH model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=max(p, q),
            switching_mean=True,
            switching_variance=True,
            switching_ar=False,
        )
        self.p_garch = p
        self.q_arch = q
        self.method = method

        # Pre-computed conditional variances per regime, updated during EM
        self._sigma2: NDArray[np.float64] | None = None
        self._h_collapsed: NDArray[np.float64] | None = None
        self._filtered_probs_cache: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingGARCHǁ__init____mutmut_23(
        self,
        endog: Any,
        k_regimes: int = 2,
        p: int = 1,
        q: int = 1,
        method: str = "gray",
    ) -> None:
        """Initialize Markov-Switching GARCH model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=max(p, q),
            switching_mean=False,
            switching_variance=False,
            switching_ar=False,
        )
        self.p_garch = p
        self.q_arch = q
        self.method = method

        # Pre-computed conditional variances per regime, updated during EM
        self._sigma2: NDArray[np.float64] | None = None
        self._h_collapsed: NDArray[np.float64] | None = None
        self._filtered_probs_cache: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingGARCHǁ__init____mutmut_24(
        self,
        endog: Any,
        k_regimes: int = 2,
        p: int = 1,
        q: int = 1,
        method: str = "gray",
    ) -> None:
        """Initialize Markov-Switching GARCH model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=max(p, q),
            switching_mean=False,
            switching_variance=True,
            switching_ar=True,
        )
        self.p_garch = p
        self.q_arch = q
        self.method = method

        # Pre-computed conditional variances per regime, updated during EM
        self._sigma2: NDArray[np.float64] | None = None
        self._h_collapsed: NDArray[np.float64] | None = None
        self._filtered_probs_cache: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingGARCHǁ__init____mutmut_25(
        self,
        endog: Any,
        k_regimes: int = 2,
        p: int = 1,
        q: int = 1,
        method: str = "gray",
    ) -> None:
        """Initialize Markov-Switching GARCH model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=max(p, q),
            switching_mean=False,
            switching_variance=True,
            switching_ar=False,
        )
        self.p_garch = None
        self.q_arch = q
        self.method = method

        # Pre-computed conditional variances per regime, updated during EM
        self._sigma2: NDArray[np.float64] | None = None
        self._h_collapsed: NDArray[np.float64] | None = None
        self._filtered_probs_cache: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingGARCHǁ__init____mutmut_26(
        self,
        endog: Any,
        k_regimes: int = 2,
        p: int = 1,
        q: int = 1,
        method: str = "gray",
    ) -> None:
        """Initialize Markov-Switching GARCH model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=max(p, q),
            switching_mean=False,
            switching_variance=True,
            switching_ar=False,
        )
        self.p_garch = p
        self.q_arch = None
        self.method = method

        # Pre-computed conditional variances per regime, updated during EM
        self._sigma2: NDArray[np.float64] | None = None
        self._h_collapsed: NDArray[np.float64] | None = None
        self._filtered_probs_cache: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingGARCHǁ__init____mutmut_27(
        self,
        endog: Any,
        k_regimes: int = 2,
        p: int = 1,
        q: int = 1,
        method: str = "gray",
    ) -> None:
        """Initialize Markov-Switching GARCH model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=max(p, q),
            switching_mean=False,
            switching_variance=True,
            switching_ar=False,
        )
        self.p_garch = p
        self.q_arch = q
        self.method = None

        # Pre-computed conditional variances per regime, updated during EM
        self._sigma2: NDArray[np.float64] | None = None
        self._h_collapsed: NDArray[np.float64] | None = None
        self._filtered_probs_cache: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingGARCHǁ__init____mutmut_28(
        self,
        endog: Any,
        k_regimes: int = 2,
        p: int = 1,
        q: int = 1,
        method: str = "gray",
    ) -> None:
        """Initialize Markov-Switching GARCH model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=max(p, q),
            switching_mean=False,
            switching_variance=True,
            switching_ar=False,
        )
        self.p_garch = p
        self.q_arch = q
        self.method = method

        # Pre-computed conditional variances per regime, updated during EM
        self._sigma2: NDArray[np.float64] | None = ""
        self._h_collapsed: NDArray[np.float64] | None = None
        self._filtered_probs_cache: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingGARCHǁ__init____mutmut_29(
        self,
        endog: Any,
        k_regimes: int = 2,
        p: int = 1,
        q: int = 1,
        method: str = "gray",
    ) -> None:
        """Initialize Markov-Switching GARCH model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=max(p, q),
            switching_mean=False,
            switching_variance=True,
            switching_ar=False,
        )
        self.p_garch = p
        self.q_arch = q
        self.method = method

        # Pre-computed conditional variances per regime, updated during EM
        self._sigma2: NDArray[np.float64] | None = None
        self._h_collapsed: NDArray[np.float64] | None = ""
        self._filtered_probs_cache: NDArray[np.float64] | None = None

    def xǁMarkovSwitchingGARCHǁ__init____mutmut_30(
        self,
        endog: Any,
        k_regimes: int = 2,
        p: int = 1,
        q: int = 1,
        method: str = "gray",
    ) -> None:
        """Initialize Markov-Switching GARCH model with regime configuration."""
        super().__init__(
            endog,
            k_regimes=k_regimes,
            order=max(p, q),
            switching_mean=False,
            switching_variance=True,
            switching_ar=False,
        )
        self.p_garch = p
        self.q_arch = q
        self.method = method

        # Pre-computed conditional variances per regime, updated during EM
        self._sigma2: NDArray[np.float64] | None = None
        self._h_collapsed: NDArray[np.float64] | None = None
        self._filtered_probs_cache: NDArray[np.float64] | None = ""

    xǁMarkovSwitchingGARCHǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingGARCHǁ__init____mutmut_1": xǁMarkovSwitchingGARCHǁ__init____mutmut_1,
        "xǁMarkovSwitchingGARCHǁ__init____mutmut_2": xǁMarkovSwitchingGARCHǁ__init____mutmut_2,
        "xǁMarkovSwitchingGARCHǁ__init____mutmut_3": xǁMarkovSwitchingGARCHǁ__init____mutmut_3,
        "xǁMarkovSwitchingGARCHǁ__init____mutmut_4": xǁMarkovSwitchingGARCHǁ__init____mutmut_4,
        "xǁMarkovSwitchingGARCHǁ__init____mutmut_5": xǁMarkovSwitchingGARCHǁ__init____mutmut_5,
        "xǁMarkovSwitchingGARCHǁ__init____mutmut_6": xǁMarkovSwitchingGARCHǁ__init____mutmut_6,
        "xǁMarkovSwitchingGARCHǁ__init____mutmut_7": xǁMarkovSwitchingGARCHǁ__init____mutmut_7,
        "xǁMarkovSwitchingGARCHǁ__init____mutmut_8": xǁMarkovSwitchingGARCHǁ__init____mutmut_8,
        "xǁMarkovSwitchingGARCHǁ__init____mutmut_9": xǁMarkovSwitchingGARCHǁ__init____mutmut_9,
        "xǁMarkovSwitchingGARCHǁ__init____mutmut_10": xǁMarkovSwitchingGARCHǁ__init____mutmut_10,
        "xǁMarkovSwitchingGARCHǁ__init____mutmut_11": xǁMarkovSwitchingGARCHǁ__init____mutmut_11,
        "xǁMarkovSwitchingGARCHǁ__init____mutmut_12": xǁMarkovSwitchingGARCHǁ__init____mutmut_12,
        "xǁMarkovSwitchingGARCHǁ__init____mutmut_13": xǁMarkovSwitchingGARCHǁ__init____mutmut_13,
        "xǁMarkovSwitchingGARCHǁ__init____mutmut_14": xǁMarkovSwitchingGARCHǁ__init____mutmut_14,
        "xǁMarkovSwitchingGARCHǁ__init____mutmut_15": xǁMarkovSwitchingGARCHǁ__init____mutmut_15,
        "xǁMarkovSwitchingGARCHǁ__init____mutmut_16": xǁMarkovSwitchingGARCHǁ__init____mutmut_16,
        "xǁMarkovSwitchingGARCHǁ__init____mutmut_17": xǁMarkovSwitchingGARCHǁ__init____mutmut_17,
        "xǁMarkovSwitchingGARCHǁ__init____mutmut_18": xǁMarkovSwitchingGARCHǁ__init____mutmut_18,
        "xǁMarkovSwitchingGARCHǁ__init____mutmut_19": xǁMarkovSwitchingGARCHǁ__init____mutmut_19,
        "xǁMarkovSwitchingGARCHǁ__init____mutmut_20": xǁMarkovSwitchingGARCHǁ__init____mutmut_20,
        "xǁMarkovSwitchingGARCHǁ__init____mutmut_21": xǁMarkovSwitchingGARCHǁ__init____mutmut_21,
        "xǁMarkovSwitchingGARCHǁ__init____mutmut_22": xǁMarkovSwitchingGARCHǁ__init____mutmut_22,
        "xǁMarkovSwitchingGARCHǁ__init____mutmut_23": xǁMarkovSwitchingGARCHǁ__init____mutmut_23,
        "xǁMarkovSwitchingGARCHǁ__init____mutmut_24": xǁMarkovSwitchingGARCHǁ__init____mutmut_24,
        "xǁMarkovSwitchingGARCHǁ__init____mutmut_25": xǁMarkovSwitchingGARCHǁ__init____mutmut_25,
        "xǁMarkovSwitchingGARCHǁ__init____mutmut_26": xǁMarkovSwitchingGARCHǁ__init____mutmut_26,
        "xǁMarkovSwitchingGARCHǁ__init____mutmut_27": xǁMarkovSwitchingGARCHǁ__init____mutmut_27,
        "xǁMarkovSwitchingGARCHǁ__init____mutmut_28": xǁMarkovSwitchingGARCHǁ__init____mutmut_28,
        "xǁMarkovSwitchingGARCHǁ__init____mutmut_29": xǁMarkovSwitchingGARCHǁ__init____mutmut_29,
        "xǁMarkovSwitchingGARCHǁ__init____mutmut_30": xǁMarkovSwitchingGARCHǁ__init____mutmut_30,
    }
    xǁMarkovSwitchingGARCHǁ__init____mutmut_orig.__name__ = "xǁMarkovSwitchingGARCHǁ__init__"

    def _regime_loglike(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        args = [params, regime]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_orig"),
            object.__getattribute__(self, "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_orig(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_1(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = None
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_2(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = None
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_3(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = None

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_4(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = None

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_5(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(None, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_6(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, None)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_7(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_8(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(
            params,
        )

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_9(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = None
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_10(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(None)
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_11(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(None))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_12(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = None  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_13(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(None, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_14(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, None)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_15(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_16(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(
            n_obs,
        )  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_17(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = None
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_18(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is not None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_19(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = None

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_20(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(None, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_21(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, None)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_22(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_23(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(
                n_obs,
            )

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_24(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(None, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_25(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, None):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_26(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_27(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(
            1,
        ):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_28(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(2, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_29(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = None
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_30(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 - beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_31(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega - alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_32(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha / y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_33(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] * 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_34(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t + 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_35(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 2] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_36(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 3 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_37(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta / h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_38(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t + 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_39(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 2]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_40(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = None

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_41(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(None, 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_42(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], None)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_43(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_44(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(
                sigma2[t],
            )

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_45(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1.000000000001)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_46(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = None

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_47(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) + 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_48(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) + 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_49(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 / np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_50(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = +0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_51(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -1.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_52(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(None) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_53(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 / np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_54(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(3.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_55(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 / np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_56(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 1.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_57(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(None) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_58(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 * sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_59(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 / y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_60(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 1.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_61(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y * 2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_62(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**3 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_63(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is not None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_64(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = None
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_65(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros(None)
        self._sigma2[:, regime] = sigma2

        return ll

    def xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_66(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> NDArray[np.float64]:
        """Compute log f(y_t | S_t=regime, Y_{t-1}) for all t.

        Uses the Gray (1996) collapsing approach.

        Parameters
        ----------
        params : ndarray
            Parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        ndarray
            Log-likelihood per observation, shape (T,).
        """
        k = self.k_regimes
        n_obs = self.nobs
        y = self.endog

        # Extract GARCH parameters for this regime
        omega, alpha, beta = self._unpack_garch_params(params, regime)

        # Compute conditional variances
        var_y = float(np.var(y))
        sigma2 = np.full(n_obs, var_y)  # Initialize with sample variance

        # If we have cached collapsed h, use it; otherwise use sample variance
        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, var_y)

        for t in range(1, n_obs):
            sigma2[t] = omega + alpha * y[t - 1] ** 2 + beta * h_collapsed[t - 1]
            sigma2[t] = max(sigma2[t], 1e-12)

        # Log-likelihood (zero-mean Gaussian)
        ll = -0.5 * np.log(2.0 * np.pi) - 0.5 * np.log(sigma2) - 0.5 * y**2 / sigma2

        # Store sigma2 for collapsing in next iteration
        if self._sigma2 is None:
            self._sigma2 = np.zeros((n_obs, k))
        self._sigma2[:, regime] = None

        return ll

    xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_1": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_1,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_2": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_2,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_3": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_3,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_4": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_4,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_5": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_5,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_6": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_6,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_7": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_7,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_8": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_8,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_9": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_9,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_10": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_10,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_11": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_11,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_12": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_12,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_13": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_13,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_14": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_14,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_15": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_15,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_16": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_16,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_17": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_17,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_18": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_18,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_19": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_19,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_20": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_20,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_21": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_21,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_22": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_22,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_23": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_23,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_24": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_24,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_25": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_25,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_26": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_26,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_27": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_27,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_28": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_28,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_29": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_29,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_30": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_30,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_31": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_31,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_32": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_32,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_33": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_33,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_34": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_34,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_35": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_35,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_36": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_36,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_37": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_37,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_38": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_38,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_39": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_39,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_40": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_40,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_41": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_41,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_42": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_42,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_43": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_43,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_44": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_44,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_45": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_45,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_46": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_46,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_47": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_47,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_48": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_48,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_49": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_49,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_50": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_50,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_51": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_51,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_52": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_52,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_53": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_53,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_54": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_54,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_55": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_55,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_56": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_56,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_57": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_57,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_58": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_58,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_59": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_59,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_60": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_60,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_61": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_61,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_62": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_62,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_63": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_63,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_64": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_64,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_65": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_65,
        "xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_66": xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_66,
    }
    xǁMarkovSwitchingGARCHǁ_regime_loglike__mutmut_orig.__name__ = (
        "xǁMarkovSwitchingGARCHǁ_regime_loglike"
    )

    def _unpack_garch_params(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        args = [params, regime]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )

    def xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_orig(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        """Unpack GARCH parameters for a specific regime.

        Parameter layout:
        [omega_0, alpha_0, beta_0, omega_1, alpha_1, beta_1, ..., trans_params]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (omega, alpha, beta) for the regime.
        """
        base = regime * 3  # 3 GARCH params per regime
        omega = max(abs(float(params[base])), 1e-8)
        alpha = max(abs(float(params[base + 1])), 1e-8)
        beta = max(abs(float(params[base + 2])), 0.0)
        return omega, alpha, beta

    def xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_1(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        """Unpack GARCH parameters for a specific regime.

        Parameter layout:
        [omega_0, alpha_0, beta_0, omega_1, alpha_1, beta_1, ..., trans_params]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (omega, alpha, beta) for the regime.
        """
        base = None  # 3 GARCH params per regime
        omega = max(abs(float(params[base])), 1e-8)
        alpha = max(abs(float(params[base + 1])), 1e-8)
        beta = max(abs(float(params[base + 2])), 0.0)
        return omega, alpha, beta

    def xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_2(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        """Unpack GARCH parameters for a specific regime.

        Parameter layout:
        [omega_0, alpha_0, beta_0, omega_1, alpha_1, beta_1, ..., trans_params]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (omega, alpha, beta) for the regime.
        """
        base = regime / 3  # 3 GARCH params per regime
        omega = max(abs(float(params[base])), 1e-8)
        alpha = max(abs(float(params[base + 1])), 1e-8)
        beta = max(abs(float(params[base + 2])), 0.0)
        return omega, alpha, beta

    def xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_3(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        """Unpack GARCH parameters for a specific regime.

        Parameter layout:
        [omega_0, alpha_0, beta_0, omega_1, alpha_1, beta_1, ..., trans_params]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (omega, alpha, beta) for the regime.
        """
        base = regime * 4  # 3 GARCH params per regime
        omega = max(abs(float(params[base])), 1e-8)
        alpha = max(abs(float(params[base + 1])), 1e-8)
        beta = max(abs(float(params[base + 2])), 0.0)
        return omega, alpha, beta

    def xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_4(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        """Unpack GARCH parameters for a specific regime.

        Parameter layout:
        [omega_0, alpha_0, beta_0, omega_1, alpha_1, beta_1, ..., trans_params]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (omega, alpha, beta) for the regime.
        """
        base = regime * 3  # 3 GARCH params per regime
        omega = None
        alpha = max(abs(float(params[base + 1])), 1e-8)
        beta = max(abs(float(params[base + 2])), 0.0)
        return omega, alpha, beta

    def xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_5(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        """Unpack GARCH parameters for a specific regime.

        Parameter layout:
        [omega_0, alpha_0, beta_0, omega_1, alpha_1, beta_1, ..., trans_params]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (omega, alpha, beta) for the regime.
        """
        base = regime * 3  # 3 GARCH params per regime
        omega = max(None, 1e-8)
        alpha = max(abs(float(params[base + 1])), 1e-8)
        beta = max(abs(float(params[base + 2])), 0.0)
        return omega, alpha, beta

    def xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_6(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        """Unpack GARCH parameters for a specific regime.

        Parameter layout:
        [omega_0, alpha_0, beta_0, omega_1, alpha_1, beta_1, ..., trans_params]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (omega, alpha, beta) for the regime.
        """
        base = regime * 3  # 3 GARCH params per regime
        omega = max(abs(float(params[base])), None)
        alpha = max(abs(float(params[base + 1])), 1e-8)
        beta = max(abs(float(params[base + 2])), 0.0)
        return omega, alpha, beta

    def xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_7(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        """Unpack GARCH parameters for a specific regime.

        Parameter layout:
        [omega_0, alpha_0, beta_0, omega_1, alpha_1, beta_1, ..., trans_params]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (omega, alpha, beta) for the regime.
        """
        base = regime * 3  # 3 GARCH params per regime
        omega = max(1e-8)
        alpha = max(abs(float(params[base + 1])), 1e-8)
        beta = max(abs(float(params[base + 2])), 0.0)
        return omega, alpha, beta

    def xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_8(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        """Unpack GARCH parameters for a specific regime.

        Parameter layout:
        [omega_0, alpha_0, beta_0, omega_1, alpha_1, beta_1, ..., trans_params]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (omega, alpha, beta) for the regime.
        """
        base = regime * 3  # 3 GARCH params per regime
        omega = max(
            abs(float(params[base])),
        )
        alpha = max(abs(float(params[base + 1])), 1e-8)
        beta = max(abs(float(params[base + 2])), 0.0)
        return omega, alpha, beta

    def xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_9(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        """Unpack GARCH parameters for a specific regime.

        Parameter layout:
        [omega_0, alpha_0, beta_0, omega_1, alpha_1, beta_1, ..., trans_params]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (omega, alpha, beta) for the regime.
        """
        base = regime * 3  # 3 GARCH params per regime
        omega = max(abs(None), 1e-8)
        alpha = max(abs(float(params[base + 1])), 1e-8)
        beta = max(abs(float(params[base + 2])), 0.0)
        return omega, alpha, beta

    def xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_10(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        """Unpack GARCH parameters for a specific regime.

        Parameter layout:
        [omega_0, alpha_0, beta_0, omega_1, alpha_1, beta_1, ..., trans_params]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (omega, alpha, beta) for the regime.
        """
        base = regime * 3  # 3 GARCH params per regime
        omega = max(abs(float(None)), 1e-8)
        alpha = max(abs(float(params[base + 1])), 1e-8)
        beta = max(abs(float(params[base + 2])), 0.0)
        return omega, alpha, beta

    def xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_11(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        """Unpack GARCH parameters for a specific regime.

        Parameter layout:
        [omega_0, alpha_0, beta_0, omega_1, alpha_1, beta_1, ..., trans_params]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (omega, alpha, beta) for the regime.
        """
        base = regime * 3  # 3 GARCH params per regime
        omega = max(abs(float(params[base])), 1.00000001)
        alpha = max(abs(float(params[base + 1])), 1e-8)
        beta = max(abs(float(params[base + 2])), 0.0)
        return omega, alpha, beta

    def xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_12(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        """Unpack GARCH parameters for a specific regime.

        Parameter layout:
        [omega_0, alpha_0, beta_0, omega_1, alpha_1, beta_1, ..., trans_params]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (omega, alpha, beta) for the regime.
        """
        base = regime * 3  # 3 GARCH params per regime
        omega = max(abs(float(params[base])), 1e-8)
        alpha = None
        beta = max(abs(float(params[base + 2])), 0.0)
        return omega, alpha, beta

    def xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_13(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        """Unpack GARCH parameters for a specific regime.

        Parameter layout:
        [omega_0, alpha_0, beta_0, omega_1, alpha_1, beta_1, ..., trans_params]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (omega, alpha, beta) for the regime.
        """
        base = regime * 3  # 3 GARCH params per regime
        omega = max(abs(float(params[base])), 1e-8)
        alpha = max(None, 1e-8)
        beta = max(abs(float(params[base + 2])), 0.0)
        return omega, alpha, beta

    def xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_14(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        """Unpack GARCH parameters for a specific regime.

        Parameter layout:
        [omega_0, alpha_0, beta_0, omega_1, alpha_1, beta_1, ..., trans_params]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (omega, alpha, beta) for the regime.
        """
        base = regime * 3  # 3 GARCH params per regime
        omega = max(abs(float(params[base])), 1e-8)
        alpha = max(abs(float(params[base + 1])), None)
        beta = max(abs(float(params[base + 2])), 0.0)
        return omega, alpha, beta

    def xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_15(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        """Unpack GARCH parameters for a specific regime.

        Parameter layout:
        [omega_0, alpha_0, beta_0, omega_1, alpha_1, beta_1, ..., trans_params]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (omega, alpha, beta) for the regime.
        """
        base = regime * 3  # 3 GARCH params per regime
        omega = max(abs(float(params[base])), 1e-8)
        alpha = max(1e-8)
        beta = max(abs(float(params[base + 2])), 0.0)
        return omega, alpha, beta

    def xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_16(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        """Unpack GARCH parameters for a specific regime.

        Parameter layout:
        [omega_0, alpha_0, beta_0, omega_1, alpha_1, beta_1, ..., trans_params]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (omega, alpha, beta) for the regime.
        """
        base = regime * 3  # 3 GARCH params per regime
        omega = max(abs(float(params[base])), 1e-8)
        alpha = max(
            abs(float(params[base + 1])),
        )
        beta = max(abs(float(params[base + 2])), 0.0)
        return omega, alpha, beta

    def xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_17(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        """Unpack GARCH parameters for a specific regime.

        Parameter layout:
        [omega_0, alpha_0, beta_0, omega_1, alpha_1, beta_1, ..., trans_params]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (omega, alpha, beta) for the regime.
        """
        base = regime * 3  # 3 GARCH params per regime
        omega = max(abs(float(params[base])), 1e-8)
        alpha = max(abs(None), 1e-8)
        beta = max(abs(float(params[base + 2])), 0.0)
        return omega, alpha, beta

    def xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_18(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        """Unpack GARCH parameters for a specific regime.

        Parameter layout:
        [omega_0, alpha_0, beta_0, omega_1, alpha_1, beta_1, ..., trans_params]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (omega, alpha, beta) for the regime.
        """
        base = regime * 3  # 3 GARCH params per regime
        omega = max(abs(float(params[base])), 1e-8)
        alpha = max(abs(float(None)), 1e-8)
        beta = max(abs(float(params[base + 2])), 0.0)
        return omega, alpha, beta

    def xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_19(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        """Unpack GARCH parameters for a specific regime.

        Parameter layout:
        [omega_0, alpha_0, beta_0, omega_1, alpha_1, beta_1, ..., trans_params]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (omega, alpha, beta) for the regime.
        """
        base = regime * 3  # 3 GARCH params per regime
        omega = max(abs(float(params[base])), 1e-8)
        alpha = max(abs(float(params[base - 1])), 1e-8)
        beta = max(abs(float(params[base + 2])), 0.0)
        return omega, alpha, beta

    def xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_20(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        """Unpack GARCH parameters for a specific regime.

        Parameter layout:
        [omega_0, alpha_0, beta_0, omega_1, alpha_1, beta_1, ..., trans_params]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (omega, alpha, beta) for the regime.
        """
        base = regime * 3  # 3 GARCH params per regime
        omega = max(abs(float(params[base])), 1e-8)
        alpha = max(abs(float(params[base + 2])), 1e-8)
        beta = max(abs(float(params[base + 2])), 0.0)
        return omega, alpha, beta

    def xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_21(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        """Unpack GARCH parameters for a specific regime.

        Parameter layout:
        [omega_0, alpha_0, beta_0, omega_1, alpha_1, beta_1, ..., trans_params]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (omega, alpha, beta) for the regime.
        """
        base = regime * 3  # 3 GARCH params per regime
        omega = max(abs(float(params[base])), 1e-8)
        alpha = max(abs(float(params[base + 1])), 1.00000001)
        beta = max(abs(float(params[base + 2])), 0.0)
        return omega, alpha, beta

    def xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_22(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        """Unpack GARCH parameters for a specific regime.

        Parameter layout:
        [omega_0, alpha_0, beta_0, omega_1, alpha_1, beta_1, ..., trans_params]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (omega, alpha, beta) for the regime.
        """
        base = regime * 3  # 3 GARCH params per regime
        omega = max(abs(float(params[base])), 1e-8)
        alpha = max(abs(float(params[base + 1])), 1e-8)
        beta = None
        return omega, alpha, beta

    def xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_23(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        """Unpack GARCH parameters for a specific regime.

        Parameter layout:
        [omega_0, alpha_0, beta_0, omega_1, alpha_1, beta_1, ..., trans_params]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (omega, alpha, beta) for the regime.
        """
        base = regime * 3  # 3 GARCH params per regime
        omega = max(abs(float(params[base])), 1e-8)
        alpha = max(abs(float(params[base + 1])), 1e-8)
        beta = max(None, 0.0)
        return omega, alpha, beta

    def xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_24(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        """Unpack GARCH parameters for a specific regime.

        Parameter layout:
        [omega_0, alpha_0, beta_0, omega_1, alpha_1, beta_1, ..., trans_params]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (omega, alpha, beta) for the regime.
        """
        base = regime * 3  # 3 GARCH params per regime
        omega = max(abs(float(params[base])), 1e-8)
        alpha = max(abs(float(params[base + 1])), 1e-8)
        beta = max(abs(float(params[base + 2])), None)
        return omega, alpha, beta

    def xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_25(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        """Unpack GARCH parameters for a specific regime.

        Parameter layout:
        [omega_0, alpha_0, beta_0, omega_1, alpha_1, beta_1, ..., trans_params]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (omega, alpha, beta) for the regime.
        """
        base = regime * 3  # 3 GARCH params per regime
        omega = max(abs(float(params[base])), 1e-8)
        alpha = max(abs(float(params[base + 1])), 1e-8)
        beta = max(0.0)
        return omega, alpha, beta

    def xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_26(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        """Unpack GARCH parameters for a specific regime.

        Parameter layout:
        [omega_0, alpha_0, beta_0, omega_1, alpha_1, beta_1, ..., trans_params]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (omega, alpha, beta) for the regime.
        """
        base = regime * 3  # 3 GARCH params per regime
        omega = max(abs(float(params[base])), 1e-8)
        alpha = max(abs(float(params[base + 1])), 1e-8)
        beta = max(
            abs(float(params[base + 2])),
        )
        return omega, alpha, beta

    def xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_27(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        """Unpack GARCH parameters for a specific regime.

        Parameter layout:
        [omega_0, alpha_0, beta_0, omega_1, alpha_1, beta_1, ..., trans_params]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (omega, alpha, beta) for the regime.
        """
        base = regime * 3  # 3 GARCH params per regime
        omega = max(abs(float(params[base])), 1e-8)
        alpha = max(abs(float(params[base + 1])), 1e-8)
        beta = max(abs(None), 0.0)
        return omega, alpha, beta

    def xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_28(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        """Unpack GARCH parameters for a specific regime.

        Parameter layout:
        [omega_0, alpha_0, beta_0, omega_1, alpha_1, beta_1, ..., trans_params]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (omega, alpha, beta) for the regime.
        """
        base = regime * 3  # 3 GARCH params per regime
        omega = max(abs(float(params[base])), 1e-8)
        alpha = max(abs(float(params[base + 1])), 1e-8)
        beta = max(abs(float(None)), 0.0)
        return omega, alpha, beta

    def xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_29(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        """Unpack GARCH parameters for a specific regime.

        Parameter layout:
        [omega_0, alpha_0, beta_0, omega_1, alpha_1, beta_1, ..., trans_params]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (omega, alpha, beta) for the regime.
        """
        base = regime * 3  # 3 GARCH params per regime
        omega = max(abs(float(params[base])), 1e-8)
        alpha = max(abs(float(params[base + 1])), 1e-8)
        beta = max(abs(float(params[base - 2])), 0.0)
        return omega, alpha, beta

    def xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_30(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        """Unpack GARCH parameters for a specific regime.

        Parameter layout:
        [omega_0, alpha_0, beta_0, omega_1, alpha_1, beta_1, ..., trans_params]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (omega, alpha, beta) for the regime.
        """
        base = regime * 3  # 3 GARCH params per regime
        omega = max(abs(float(params[base])), 1e-8)
        alpha = max(abs(float(params[base + 1])), 1e-8)
        beta = max(abs(float(params[base + 3])), 0.0)
        return omega, alpha, beta

    def xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_31(
        self,
        params: NDArray[np.float64],
        regime: int,
    ) -> tuple[float, float, float]:
        """Unpack GARCH parameters for a specific regime.

        Parameter layout:
        [omega_0, alpha_0, beta_0, omega_1, alpha_1, beta_1, ..., trans_params]

        Parameters
        ----------
        params : ndarray
            Full parameter vector.
        regime : int
            Regime index.

        Returns
        -------
        tuple
            (omega, alpha, beta) for the regime.
        """
        base = regime * 3  # 3 GARCH params per regime
        omega = max(abs(float(params[base])), 1e-8)
        alpha = max(abs(float(params[base + 1])), 1e-8)
        beta = max(abs(float(params[base + 2])), 1.0)
        return omega, alpha, beta

    xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_1": xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_1,
        "xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_2": xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_2,
        "xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_3": xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_3,
        "xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_4": xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_4,
        "xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_5": xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_5,
        "xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_6": xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_6,
        "xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_7": xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_7,
        "xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_8": xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_8,
        "xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_9": xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_9,
        "xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_10": xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_10,
        "xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_11": xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_11,
        "xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_12": xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_12,
        "xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_13": xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_13,
        "xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_14": xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_14,
        "xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_15": xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_15,
        "xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_16": xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_16,
        "xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_17": xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_17,
        "xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_18": xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_18,
        "xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_19": xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_19,
        "xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_20": xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_20,
        "xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_21": xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_21,
        "xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_22": xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_22,
        "xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_23": xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_23,
        "xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_24": xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_24,
        "xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_25": xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_25,
        "xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_26": xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_26,
        "xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_27": xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_27,
        "xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_28": xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_28,
        "xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_29": xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_29,
        "xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_30": xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_30,
        "xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_31": xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_31,
    }
    xǁMarkovSwitchingGARCHǁ_unpack_garch_params__mutmut_orig.__name__ = (
        "xǁMarkovSwitchingGARCHǁ_unpack_garch_params"
    )

    def update_collapsed_variance(
        self,
        filtered_probs: NDArray[np.float64],
    ) -> None:
        args = [filtered_probs]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )

    def xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_orig(
        self,
        filtered_probs: NDArray[np.float64],
    ) -> None:
        """Update the collapsed conditional variance h_{t-1}.

        h_{t-1} = sum_j P(S_{t-1}=j | Y_{t-1}) * sigma^2_{t-1}(j)

        Parameters
        ----------
        filtered_probs : ndarray
            Filtered probabilities, shape (T, k).
        """
        if self._sigma2 is None:
            return

        n_obs, k = filtered_probs.shape
        self._h_collapsed = np.zeros(n_obs)
        for t in range(n_obs):
            for s in range(k):
                self._h_collapsed[t] += filtered_probs[t, s] * self._sigma2[t, s]
            self._h_collapsed[t] = max(self._h_collapsed[t], 1e-12)

        self._filtered_probs_cache = filtered_probs.copy()

    def xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_1(
        self,
        filtered_probs: NDArray[np.float64],
    ) -> None:
        """Update the collapsed conditional variance h_{t-1}.

        h_{t-1} = sum_j P(S_{t-1}=j | Y_{t-1}) * sigma^2_{t-1}(j)

        Parameters
        ----------
        filtered_probs : ndarray
            Filtered probabilities, shape (T, k).
        """
        if self._sigma2 is not None:
            return

        n_obs, k = filtered_probs.shape
        self._h_collapsed = np.zeros(n_obs)
        for t in range(n_obs):
            for s in range(k):
                self._h_collapsed[t] += filtered_probs[t, s] * self._sigma2[t, s]
            self._h_collapsed[t] = max(self._h_collapsed[t], 1e-12)

        self._filtered_probs_cache = filtered_probs.copy()

    def xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_2(
        self,
        filtered_probs: NDArray[np.float64],
    ) -> None:
        """Update the collapsed conditional variance h_{t-1}.

        h_{t-1} = sum_j P(S_{t-1}=j | Y_{t-1}) * sigma^2_{t-1}(j)

        Parameters
        ----------
        filtered_probs : ndarray
            Filtered probabilities, shape (T, k).
        """
        if self._sigma2 is None:
            return

        n_obs, k = None
        self._h_collapsed = np.zeros(n_obs)
        for t in range(n_obs):
            for s in range(k):
                self._h_collapsed[t] += filtered_probs[t, s] * self._sigma2[t, s]
            self._h_collapsed[t] = max(self._h_collapsed[t], 1e-12)

        self._filtered_probs_cache = filtered_probs.copy()

    def xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_3(
        self,
        filtered_probs: NDArray[np.float64],
    ) -> None:
        """Update the collapsed conditional variance h_{t-1}.

        h_{t-1} = sum_j P(S_{t-1}=j | Y_{t-1}) * sigma^2_{t-1}(j)

        Parameters
        ----------
        filtered_probs : ndarray
            Filtered probabilities, shape (T, k).
        """
        if self._sigma2 is None:
            return

        n_obs, k = filtered_probs.shape
        self._h_collapsed = None
        for t in range(n_obs):
            for s in range(k):
                self._h_collapsed[t] += filtered_probs[t, s] * self._sigma2[t, s]
            self._h_collapsed[t] = max(self._h_collapsed[t], 1e-12)

        self._filtered_probs_cache = filtered_probs.copy()

    def xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_4(
        self,
        filtered_probs: NDArray[np.float64],
    ) -> None:
        """Update the collapsed conditional variance h_{t-1}.

        h_{t-1} = sum_j P(S_{t-1}=j | Y_{t-1}) * sigma^2_{t-1}(j)

        Parameters
        ----------
        filtered_probs : ndarray
            Filtered probabilities, shape (T, k).
        """
        if self._sigma2 is None:
            return

        n_obs, k = filtered_probs.shape
        self._h_collapsed = np.zeros(None)
        for t in range(n_obs):
            for s in range(k):
                self._h_collapsed[t] += filtered_probs[t, s] * self._sigma2[t, s]
            self._h_collapsed[t] = max(self._h_collapsed[t], 1e-12)

        self._filtered_probs_cache = filtered_probs.copy()

    def xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_5(
        self,
        filtered_probs: NDArray[np.float64],
    ) -> None:
        """Update the collapsed conditional variance h_{t-1}.

        h_{t-1} = sum_j P(S_{t-1}=j | Y_{t-1}) * sigma^2_{t-1}(j)

        Parameters
        ----------
        filtered_probs : ndarray
            Filtered probabilities, shape (T, k).
        """
        if self._sigma2 is None:
            return

        n_obs, k = filtered_probs.shape
        self._h_collapsed = np.zeros(n_obs)
        for t in range(None):
            for s in range(k):
                self._h_collapsed[t] += filtered_probs[t, s] * self._sigma2[t, s]
            self._h_collapsed[t] = max(self._h_collapsed[t], 1e-12)

        self._filtered_probs_cache = filtered_probs.copy()

    def xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_6(
        self,
        filtered_probs: NDArray[np.float64],
    ) -> None:
        """Update the collapsed conditional variance h_{t-1}.

        h_{t-1} = sum_j P(S_{t-1}=j | Y_{t-1}) * sigma^2_{t-1}(j)

        Parameters
        ----------
        filtered_probs : ndarray
            Filtered probabilities, shape (T, k).
        """
        if self._sigma2 is None:
            return

        n_obs, k = filtered_probs.shape
        self._h_collapsed = np.zeros(n_obs)
        for t in range(n_obs):
            for s in range(None):
                self._h_collapsed[t] += filtered_probs[t, s] * self._sigma2[t, s]
            self._h_collapsed[t] = max(self._h_collapsed[t], 1e-12)

        self._filtered_probs_cache = filtered_probs.copy()

    def xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_7(
        self,
        filtered_probs: NDArray[np.float64],
    ) -> None:
        """Update the collapsed conditional variance h_{t-1}.

        h_{t-1} = sum_j P(S_{t-1}=j | Y_{t-1}) * sigma^2_{t-1}(j)

        Parameters
        ----------
        filtered_probs : ndarray
            Filtered probabilities, shape (T, k).
        """
        if self._sigma2 is None:
            return

        n_obs, k = filtered_probs.shape
        self._h_collapsed = np.zeros(n_obs)
        for t in range(n_obs):
            for s in range(k):
                self._h_collapsed[t] = filtered_probs[t, s] * self._sigma2[t, s]
            self._h_collapsed[t] = max(self._h_collapsed[t], 1e-12)

        self._filtered_probs_cache = filtered_probs.copy()

    def xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_8(
        self,
        filtered_probs: NDArray[np.float64],
    ) -> None:
        """Update the collapsed conditional variance h_{t-1}.

        h_{t-1} = sum_j P(S_{t-1}=j | Y_{t-1}) * sigma^2_{t-1}(j)

        Parameters
        ----------
        filtered_probs : ndarray
            Filtered probabilities, shape (T, k).
        """
        if self._sigma2 is None:
            return

        n_obs, k = filtered_probs.shape
        self._h_collapsed = np.zeros(n_obs)
        for t in range(n_obs):
            for s in range(k):
                self._h_collapsed[t] -= filtered_probs[t, s] * self._sigma2[t, s]
            self._h_collapsed[t] = max(self._h_collapsed[t], 1e-12)

        self._filtered_probs_cache = filtered_probs.copy()

    def xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_9(
        self,
        filtered_probs: NDArray[np.float64],
    ) -> None:
        """Update the collapsed conditional variance h_{t-1}.

        h_{t-1} = sum_j P(S_{t-1}=j | Y_{t-1}) * sigma^2_{t-1}(j)

        Parameters
        ----------
        filtered_probs : ndarray
            Filtered probabilities, shape (T, k).
        """
        if self._sigma2 is None:
            return

        n_obs, k = filtered_probs.shape
        self._h_collapsed = np.zeros(n_obs)
        for t in range(n_obs):
            for s in range(k):
                self._h_collapsed[t] += filtered_probs[t, s] / self._sigma2[t, s]
            self._h_collapsed[t] = max(self._h_collapsed[t], 1e-12)

        self._filtered_probs_cache = filtered_probs.copy()

    def xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_10(
        self,
        filtered_probs: NDArray[np.float64],
    ) -> None:
        """Update the collapsed conditional variance h_{t-1}.

        h_{t-1} = sum_j P(S_{t-1}=j | Y_{t-1}) * sigma^2_{t-1}(j)

        Parameters
        ----------
        filtered_probs : ndarray
            Filtered probabilities, shape (T, k).
        """
        if self._sigma2 is None:
            return

        n_obs, k = filtered_probs.shape
        self._h_collapsed = np.zeros(n_obs)
        for t in range(n_obs):
            for s in range(k):
                self._h_collapsed[t] += filtered_probs[t, s] * self._sigma2[t, s]
            self._h_collapsed[t] = None

        self._filtered_probs_cache = filtered_probs.copy()

    def xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_11(
        self,
        filtered_probs: NDArray[np.float64],
    ) -> None:
        """Update the collapsed conditional variance h_{t-1}.

        h_{t-1} = sum_j P(S_{t-1}=j | Y_{t-1}) * sigma^2_{t-1}(j)

        Parameters
        ----------
        filtered_probs : ndarray
            Filtered probabilities, shape (T, k).
        """
        if self._sigma2 is None:
            return

        n_obs, k = filtered_probs.shape
        self._h_collapsed = np.zeros(n_obs)
        for t in range(n_obs):
            for s in range(k):
                self._h_collapsed[t] += filtered_probs[t, s] * self._sigma2[t, s]
            self._h_collapsed[t] = max(None, 1e-12)

        self._filtered_probs_cache = filtered_probs.copy()

    def xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_12(
        self,
        filtered_probs: NDArray[np.float64],
    ) -> None:
        """Update the collapsed conditional variance h_{t-1}.

        h_{t-1} = sum_j P(S_{t-1}=j | Y_{t-1}) * sigma^2_{t-1}(j)

        Parameters
        ----------
        filtered_probs : ndarray
            Filtered probabilities, shape (T, k).
        """
        if self._sigma2 is None:
            return

        n_obs, k = filtered_probs.shape
        self._h_collapsed = np.zeros(n_obs)
        for t in range(n_obs):
            for s in range(k):
                self._h_collapsed[t] += filtered_probs[t, s] * self._sigma2[t, s]
            self._h_collapsed[t] = max(self._h_collapsed[t], None)

        self._filtered_probs_cache = filtered_probs.copy()

    def xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_13(
        self,
        filtered_probs: NDArray[np.float64],
    ) -> None:
        """Update the collapsed conditional variance h_{t-1}.

        h_{t-1} = sum_j P(S_{t-1}=j | Y_{t-1}) * sigma^2_{t-1}(j)

        Parameters
        ----------
        filtered_probs : ndarray
            Filtered probabilities, shape (T, k).
        """
        if self._sigma2 is None:
            return

        n_obs, k = filtered_probs.shape
        self._h_collapsed = np.zeros(n_obs)
        for t in range(n_obs):
            for s in range(k):
                self._h_collapsed[t] += filtered_probs[t, s] * self._sigma2[t, s]
            self._h_collapsed[t] = max(1e-12)

        self._filtered_probs_cache = filtered_probs.copy()

    def xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_14(
        self,
        filtered_probs: NDArray[np.float64],
    ) -> None:
        """Update the collapsed conditional variance h_{t-1}.

        h_{t-1} = sum_j P(S_{t-1}=j | Y_{t-1}) * sigma^2_{t-1}(j)

        Parameters
        ----------
        filtered_probs : ndarray
            Filtered probabilities, shape (T, k).
        """
        if self._sigma2 is None:
            return

        n_obs, k = filtered_probs.shape
        self._h_collapsed = np.zeros(n_obs)
        for t in range(n_obs):
            for s in range(k):
                self._h_collapsed[t] += filtered_probs[t, s] * self._sigma2[t, s]
            self._h_collapsed[t] = max(
                self._h_collapsed[t],
            )

        self._filtered_probs_cache = filtered_probs.copy()

    def xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_15(
        self,
        filtered_probs: NDArray[np.float64],
    ) -> None:
        """Update the collapsed conditional variance h_{t-1}.

        h_{t-1} = sum_j P(S_{t-1}=j | Y_{t-1}) * sigma^2_{t-1}(j)

        Parameters
        ----------
        filtered_probs : ndarray
            Filtered probabilities, shape (T, k).
        """
        if self._sigma2 is None:
            return

        n_obs, k = filtered_probs.shape
        self._h_collapsed = np.zeros(n_obs)
        for t in range(n_obs):
            for s in range(k):
                self._h_collapsed[t] += filtered_probs[t, s] * self._sigma2[t, s]
            self._h_collapsed[t] = max(self._h_collapsed[t], 1.000000000001)

        self._filtered_probs_cache = filtered_probs.copy()

    def xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_16(
        self,
        filtered_probs: NDArray[np.float64],
    ) -> None:
        """Update the collapsed conditional variance h_{t-1}.

        h_{t-1} = sum_j P(S_{t-1}=j | Y_{t-1}) * sigma^2_{t-1}(j)

        Parameters
        ----------
        filtered_probs : ndarray
            Filtered probabilities, shape (T, k).
        """
        if self._sigma2 is None:
            return

        n_obs, k = filtered_probs.shape
        self._h_collapsed = np.zeros(n_obs)
        for t in range(n_obs):
            for s in range(k):
                self._h_collapsed[t] += filtered_probs[t, s] * self._sigma2[t, s]
            self._h_collapsed[t] = max(self._h_collapsed[t], 1e-12)

        self._filtered_probs_cache = None

    xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_1": xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_1,
        "xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_2": xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_2,
        "xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_3": xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_3,
        "xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_4": xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_4,
        "xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_5": xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_5,
        "xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_6": xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_6,
        "xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_7": xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_7,
        "xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_8": xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_8,
        "xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_9": xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_9,
        "xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_10": xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_10,
        "xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_11": xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_11,
        "xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_12": xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_12,
        "xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_13": xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_13,
        "xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_14": xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_14,
        "xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_15": xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_15,
        "xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_16": xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_16,
    }
    xǁMarkovSwitchingGARCHǁupdate_collapsed_variance__mutmut_orig.__name__ = (
        "xǁMarkovSwitchingGARCHǁupdate_collapsed_variance"
    )

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameter values.

        Returns
        -------
        ndarray
            [omega_0, alpha_0, beta_0, ..., omega_{k-1}, alpha_{k-1}, beta_{k-1}, trans_params].
        """
        k = self.k_regimes
        y = self.endog
        var_y = float(np.var(y))
        params_list: list[float] = []

        for s in range(k):
            # Different initial GARCH params per regime
            scale = 0.5 + s * 1.0  # regime 0: low vol, regime 1: high vol
            omega = var_y * 0.05 * scale
            alpha = 0.05 + s * 0.05
            beta = 0.85 - s * 0.10
            params_list.extend([omega, alpha, beta])

        # Transition params
        n_trans = k * (k - 1)
        params_list.extend([0.0] * n_trans)

        return np.array(params_list)

    @property
    def param_names(self) -> list[str]:
        """Parameter names."""
        k = self.k_regimes
        names: list[str] = []
        for s in range(k):
            names.extend([f"omega_{s}", f"alpha_{s}", f"beta_{s}"])
        names.extend([f"p_{i}{j}" for i in range(k) for j in range(k) if i != j])
        return names

    def _m_step_update(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        args = [params, smoothed, joint_smoothed]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_orig"),
            object.__getattribute__(self, "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_orig(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_1(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = None
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_2(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = None
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_3(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = None
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_4(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = None

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_5(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(None)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_6(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = None
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_7(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is not None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_8(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = None

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_9(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(None, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_10(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, None)

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_11(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_12(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(
                n_obs,
            )

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_13(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(None))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_14(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(None)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_15(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(None):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_16(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = None  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_17(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[2:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_18(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = None

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_19(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(None)

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_20(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 or self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_21(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum >= 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_22(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1.000000000001 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_23(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_24(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = None

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_25(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[2:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_26(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = None
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_27(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] * 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_28(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:+1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_29(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-2] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_30(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 3
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_31(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = None

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_32(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:+1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_33(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-2]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_34(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = None
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_35(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack(None)
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_36(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(None), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_37(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs + 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_38(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 2), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_39(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = None

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_40(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(None)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_41(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = None
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_42(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat - 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_43(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 / np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_44(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1.00000001 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_45(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(None)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_46(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(4)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_47(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = None
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_48(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = None

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_49(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(None, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_50(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, None)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_51(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_52(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(
                        xwx,
                    )

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_53(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = None
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_54(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s / 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_55(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 4
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_56(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = None  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_57(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(None, 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_58(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], None)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_59(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_60(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(
                        coeffs[0],
                    )  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_61(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[1], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_62(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1.00000001)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_63(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = None  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_64(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base - 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_65(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 2] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_66(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(None, 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_67(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], None)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_68(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_69(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(
                        coeffs[1],
                    )  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_70(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[2], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_71(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1.00000001)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_72(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = None  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_73(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base - 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_74(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 3] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_75(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(None, 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_76(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], None)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_77(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_78(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(
                        coeffs[2],
                    )  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_79(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[3], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_80(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 1.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_81(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = None
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_82(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] - new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_83(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base - 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_84(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 2] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_85(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base - 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_86(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 3]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_87(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence > 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_88(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 1.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_89(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = None
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_90(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 * persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_91(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 1.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_92(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] = scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_93(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] /= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_94(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base - 1] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_95(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 2] *= scale
                        new_params[base + 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_96(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] = scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_97(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 2] /= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_98(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base - 2] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    def xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_99(
        self,
        params: NDArray[np.float64],
        smoothed: NDArray[np.float64],
        joint_smoothed: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Custom M-step for MS-GARCH.

        Updates GARCH parameters using weighted quasi-MLE.

        Parameters
        ----------
        params : ndarray
            Current parameters.
        smoothed : ndarray
            Smoothed probabilities, shape (T, k).
        joint_smoothed : ndarray
            Joint smoothed probabilities, shape (T-1, k, k).

        Returns
        -------
        ndarray
            Updated parameters.
        """
        k = self.k_regimes
        y = self.endog
        n_obs = self.nobs
        new_params = params.copy()

        # Update collapsed variance using smoothed probs for next iteration
        self.update_collapsed_variance(smoothed)

        h_collapsed = self._h_collapsed
        if h_collapsed is None:
            h_collapsed = np.full(n_obs, float(np.var(y)))

        for s in range(k):
            weights = smoothed[1:, s]  # t = 1, ..., T-1
            w_sum = float(weights.sum())

            if w_sum > 1e-12 and self._sigma2 is not None:
                # Target: sigma^2_t(s) for t=1..T-1
                target = self._sigma2[1:, s]

                # Regressors
                y2_lag = y[:-1] ** 2
                h_lag = h_collapsed[:-1]

                # Weighted least squares
                x_mat = np.column_stack([np.ones(n_obs - 1), y2_lag, h_lag])
                w_diag = np.diag(weights)

                try:
                    xwx = x_mat.T @ w_diag @ x_mat + 1e-8 * np.eye(3)
                    xwy = x_mat.T @ w_diag @ target
                    coeffs = np.linalg.solve(xwx, xwy)

                    base = s * 3
                    new_params[base] = max(coeffs[0], 1e-8)  # omega
                    new_params[base + 1] = max(coeffs[1], 1e-8)  # alpha
                    new_params[base + 2] = max(coeffs[2], 0.0)  # beta

                    # Ensure stationarity: alpha + beta < 1
                    persistence = new_params[base + 1] + new_params[base + 2]
                    if persistence >= 0.999:
                        scale = 0.998 / persistence
                        new_params[base + 1] *= scale
                        new_params[base + 3] *= scale
                except np.linalg.LinAlgError:
                    pass

        return new_params

    xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_1": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_1,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_2": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_2,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_3": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_3,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_4": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_4,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_5": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_5,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_6": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_6,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_7": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_7,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_8": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_8,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_9": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_9,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_10": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_10,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_11": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_11,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_12": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_12,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_13": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_13,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_14": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_14,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_15": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_15,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_16": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_16,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_17": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_17,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_18": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_18,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_19": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_19,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_20": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_20,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_21": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_21,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_22": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_22,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_23": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_23,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_24": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_24,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_25": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_25,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_26": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_26,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_27": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_27,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_28": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_28,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_29": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_29,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_30": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_30,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_31": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_31,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_32": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_32,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_33": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_33,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_34": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_34,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_35": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_35,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_36": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_36,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_37": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_37,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_38": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_38,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_39": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_39,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_40": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_40,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_41": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_41,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_42": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_42,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_43": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_43,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_44": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_44,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_45": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_45,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_46": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_46,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_47": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_47,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_48": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_48,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_49": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_49,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_50": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_50,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_51": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_51,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_52": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_52,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_53": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_53,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_54": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_54,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_55": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_55,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_56": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_56,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_57": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_57,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_58": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_58,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_59": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_59,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_60": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_60,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_61": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_61,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_62": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_62,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_63": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_63,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_64": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_64,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_65": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_65,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_66": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_66,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_67": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_67,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_68": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_68,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_69": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_69,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_70": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_70,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_71": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_71,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_72": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_72,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_73": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_73,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_74": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_74,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_75": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_75,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_76": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_76,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_77": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_77,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_78": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_78,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_79": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_79,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_80": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_80,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_81": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_81,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_82": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_82,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_83": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_83,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_84": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_84,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_85": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_85,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_86": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_86,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_87": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_87,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_88": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_88,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_89": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_89,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_90": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_90,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_91": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_91,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_92": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_92,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_93": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_93,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_94": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_94,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_95": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_95,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_96": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_96,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_97": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_97,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_98": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_98,
        "xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_99": xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_99,
    }
    xǁMarkovSwitchingGARCHǁ_m_step_update__mutmut_orig.__name__ = (
        "xǁMarkovSwitchingGARCHǁ_m_step_update"
    )

    def _extract_regime_params(self, params: NDArray[np.float64]) -> dict[int, dict[str, float]]:
        args = [params]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )

    def xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_orig(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific GARCH parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            omega, alpha, beta = self._unpack_garch_params(params, s)
            regime_params[s] = {
                "omega": omega,
                "alpha": alpha,
                "beta": beta,
                "persistence": alpha + beta,
            }
        return regime_params

    def xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_1(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific GARCH parameters."""
        k = None
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            omega, alpha, beta = self._unpack_garch_params(params, s)
            regime_params[s] = {
                "omega": omega,
                "alpha": alpha,
                "beta": beta,
                "persistence": alpha + beta,
            }
        return regime_params

    def xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_2(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific GARCH parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, float]] = None
        for s in range(k):
            omega, alpha, beta = self._unpack_garch_params(params, s)
            regime_params[s] = {
                "omega": omega,
                "alpha": alpha,
                "beta": beta,
                "persistence": alpha + beta,
            }
        return regime_params

    def xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_3(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific GARCH parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(None):
            omega, alpha, beta = self._unpack_garch_params(params, s)
            regime_params[s] = {
                "omega": omega,
                "alpha": alpha,
                "beta": beta,
                "persistence": alpha + beta,
            }
        return regime_params

    def xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_4(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific GARCH parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            omega, alpha, beta = None
            regime_params[s] = {
                "omega": omega,
                "alpha": alpha,
                "beta": beta,
                "persistence": alpha + beta,
            }
        return regime_params

    def xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_5(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific GARCH parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            omega, alpha, beta = self._unpack_garch_params(None, s)
            regime_params[s] = {
                "omega": omega,
                "alpha": alpha,
                "beta": beta,
                "persistence": alpha + beta,
            }
        return regime_params

    def xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_6(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific GARCH parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            omega, alpha, beta = self._unpack_garch_params(params, None)
            regime_params[s] = {
                "omega": omega,
                "alpha": alpha,
                "beta": beta,
                "persistence": alpha + beta,
            }
        return regime_params

    def xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_7(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific GARCH parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            omega, alpha, beta = self._unpack_garch_params(s)
            regime_params[s] = {
                "omega": omega,
                "alpha": alpha,
                "beta": beta,
                "persistence": alpha + beta,
            }
        return regime_params

    def xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_8(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific GARCH parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            omega, alpha, beta = self._unpack_garch_params(
                params,
            )
            regime_params[s] = {
                "omega": omega,
                "alpha": alpha,
                "beta": beta,
                "persistence": alpha + beta,
            }
        return regime_params

    def xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_9(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific GARCH parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            omega, alpha, beta = self._unpack_garch_params(params, s)
            regime_params[s] = None
        return regime_params

    def xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_10(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific GARCH parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            omega, alpha, beta = self._unpack_garch_params(params, s)
            regime_params[s] = {
                "XXomegaXX": omega,
                "alpha": alpha,
                "beta": beta,
                "persistence": alpha + beta,
            }
        return regime_params

    def xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_11(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific GARCH parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            omega, alpha, beta = self._unpack_garch_params(params, s)
            regime_params[s] = {
                "OMEGA": omega,
                "alpha": alpha,
                "beta": beta,
                "persistence": alpha + beta,
            }
        return regime_params

    def xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_12(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific GARCH parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            omega, alpha, beta = self._unpack_garch_params(params, s)
            regime_params[s] = {
                "omega": omega,
                "XXalphaXX": alpha,
                "beta": beta,
                "persistence": alpha + beta,
            }
        return regime_params

    def xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_13(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific GARCH parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            omega, alpha, beta = self._unpack_garch_params(params, s)
            regime_params[s] = {
                "omega": omega,
                "ALPHA": alpha,
                "beta": beta,
                "persistence": alpha + beta,
            }
        return regime_params

    def xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_14(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific GARCH parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            omega, alpha, beta = self._unpack_garch_params(params, s)
            regime_params[s] = {
                "omega": omega,
                "alpha": alpha,
                "XXbetaXX": beta,
                "persistence": alpha + beta,
            }
        return regime_params

    def xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_15(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific GARCH parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            omega, alpha, beta = self._unpack_garch_params(params, s)
            regime_params[s] = {
                "omega": omega,
                "alpha": alpha,
                "BETA": beta,
                "persistence": alpha + beta,
            }
        return regime_params

    def xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_16(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific GARCH parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            omega, alpha, beta = self._unpack_garch_params(params, s)
            regime_params[s] = {
                "omega": omega,
                "alpha": alpha,
                "beta": beta,
                "XXpersistenceXX": alpha + beta,
            }
        return regime_params

    def xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_17(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific GARCH parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            omega, alpha, beta = self._unpack_garch_params(params, s)
            regime_params[s] = {
                "omega": omega,
                "alpha": alpha,
                "beta": beta,
                "PERSISTENCE": alpha + beta,
            }
        return regime_params

    def xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_18(
        self, params: NDArray[np.float64]
    ) -> dict[int, dict[str, float]]:
        """Extract regime-specific GARCH parameters."""
        k = self.k_regimes
        regime_params: dict[int, dict[str, float]] = {}
        for s in range(k):
            omega, alpha, beta = self._unpack_garch_params(params, s)
            regime_params[s] = {
                "omega": omega,
                "alpha": alpha,
                "beta": beta,
                "persistence": alpha - beta,
            }
        return regime_params

    xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_1": xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_1,
        "xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_2": xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_2,
        "xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_3": xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_3,
        "xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_4": xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_4,
        "xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_5": xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_5,
        "xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_6": xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_6,
        "xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_7": xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_7,
        "xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_8": xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_8,
        "xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_9": xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_9,
        "xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_10": xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_10,
        "xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_11": xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_11,
        "xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_12": xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_12,
        "xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_13": xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_13,
        "xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_14": xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_14,
        "xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_15": xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_15,
        "xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_16": xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_16,
        "xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_17": xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_17,
        "xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_18": xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_18,
    }
    xǁMarkovSwitchingGARCHǁ_extract_regime_params__mutmut_orig.__name__ = (
        "xǁMarkovSwitchingGARCHǁ_extract_regime_params"
    )
