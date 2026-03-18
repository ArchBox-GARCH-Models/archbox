"""LSTAR - Logistic Smooth Transition Autoregressive Model (Terasvirta, 1994).

The LSTAR model uses a logistic transition function for smooth regime switching:

    y_t = phi^{(1)}'x_t * (1 - G(s_t; gamma, c))
        + phi^{(2)}'x_t * G(s_t; gamma, c)
        + eps_t

    G(s_t; gamma, c) = 1 / (1 + exp(-gamma * (s_t - c)))

Properties:
- gamma -> 0: linear model (G -> 0.5)
- gamma -> inf: LSTAR -> SETAR (abrupt transition)
- G(c; gamma, c) = 0.5 (midpoint of transition)

References
----------
- Terasvirta, T. (1994). Specification, Estimation, and Evaluation of
  Smooth Transition Autoregressive Models. JASA, 89(425), 208-218.
- van Dijk, D., Terasvirta, T. & Franses, P.H. (2002). Smooth Transition
  Autoregressive Models - A Survey. Econometric Reviews, 21(1), 1-47.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Annotated, Any, ClassVar

import numpy as np
from numpy.typing import NDArray
from scipy import optimize

from archbox.threshold.base import ThresholdModel
from archbox.threshold.results import ThresholdResults
from archbox.threshold.transition import logistic_transition

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


class LSTAR(ThresholdModel):
    """Logistic Smooth Transition Autoregressive model (Terasvirta, 1994).

    Parameters
    ----------
    endog : array-like
        Endogenous time series.
    order : int
        AR order p (default 1).
    delay : int
        Delay parameter d (default 1).
    gamma_grid : int
        Number of gamma values in grid search (default 50).
    c_grid : int
        Number of c values in grid search (default 50).
    refine : bool
        Whether to refine via NLS after grid search (default True).

    Examples
    --------
    >>> import numpy as np
    >>> from archbox.threshold.lstar import LSTAR
    >>> rng = np.random.default_rng(42)
    >>> n = 1000
    >>> y = np.zeros(n)
    >>> gamma_true, c_true = 5.0, 0.0
    >>> for t in range(1, n):
    ...     s = y[t-1]
    ...     G = 1 / (1 + np.exp(-gamma_true * (s - c_true)))
    ...     y[t] = (0.5 + 0.3 * y[t-1]) * (1 - G) + (-0.2 + 0.8 * y[t-1]) * G
    ...     y[t] += rng.standard_normal() * 0.5
    >>> model = LSTAR(y, order=1, delay=1)
    >>> results = model.fit()
    >>> results.plot_transition()  # doctest: +SKIP
    """

    model_name: str = "LSTAR"

    def __init__(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        args = [endog, order, delay, gamma_grid, c_grid, refine]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁLSTARǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁLSTARǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁLSTARǁ__init____mutmut_orig(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        """Initialize LSTAR model with grid search configuration."""
        super().__init__(endog, order=order, delay=delay, n_regimes=2)
        self.gamma_grid = gamma_grid
        self.c_grid = c_grid
        self.refine = refine

    def xǁLSTARǁ__init____mutmut_1(
        self,
        endog: Any,
        order: int = 2,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        """Initialize LSTAR model with grid search configuration."""
        super().__init__(endog, order=order, delay=delay, n_regimes=2)
        self.gamma_grid = gamma_grid
        self.c_grid = c_grid
        self.refine = refine

    def xǁLSTARǁ__init____mutmut_2(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 2,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        """Initialize LSTAR model with grid search configuration."""
        super().__init__(endog, order=order, delay=delay, n_regimes=2)
        self.gamma_grid = gamma_grid
        self.c_grid = c_grid
        self.refine = refine

    def xǁLSTARǁ__init____mutmut_3(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 51,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        """Initialize LSTAR model with grid search configuration."""
        super().__init__(endog, order=order, delay=delay, n_regimes=2)
        self.gamma_grid = gamma_grid
        self.c_grid = c_grid
        self.refine = refine

    def xǁLSTARǁ__init____mutmut_4(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 51,
        refine: bool = True,
    ) -> None:
        """Initialize LSTAR model with grid search configuration."""
        super().__init__(endog, order=order, delay=delay, n_regimes=2)
        self.gamma_grid = gamma_grid
        self.c_grid = c_grid
        self.refine = refine

    def xǁLSTARǁ__init____mutmut_5(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = False,
    ) -> None:
        """Initialize LSTAR model with grid search configuration."""
        super().__init__(endog, order=order, delay=delay, n_regimes=2)
        self.gamma_grid = gamma_grid
        self.c_grid = c_grid
        self.refine = refine

    def xǁLSTARǁ__init____mutmut_6(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        """Initialize LSTAR model with grid search configuration."""
        super().__init__(None, order=order, delay=delay, n_regimes=2)
        self.gamma_grid = gamma_grid
        self.c_grid = c_grid
        self.refine = refine

    def xǁLSTARǁ__init____mutmut_7(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        """Initialize LSTAR model with grid search configuration."""
        super().__init__(endog, order=None, delay=delay, n_regimes=2)
        self.gamma_grid = gamma_grid
        self.c_grid = c_grid
        self.refine = refine

    def xǁLSTARǁ__init____mutmut_8(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        """Initialize LSTAR model with grid search configuration."""
        super().__init__(endog, order=order, delay=None, n_regimes=2)
        self.gamma_grid = gamma_grid
        self.c_grid = c_grid
        self.refine = refine

    def xǁLSTARǁ__init____mutmut_9(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        """Initialize LSTAR model with grid search configuration."""
        super().__init__(endog, order=order, delay=delay, n_regimes=None)
        self.gamma_grid = gamma_grid
        self.c_grid = c_grid
        self.refine = refine

    def xǁLSTARǁ__init____mutmut_10(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        """Initialize LSTAR model with grid search configuration."""
        super().__init__(order=order, delay=delay, n_regimes=2)
        self.gamma_grid = gamma_grid
        self.c_grid = c_grid
        self.refine = refine

    def xǁLSTARǁ__init____mutmut_11(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        """Initialize LSTAR model with grid search configuration."""
        super().__init__(endog, delay=delay, n_regimes=2)
        self.gamma_grid = gamma_grid
        self.c_grid = c_grid
        self.refine = refine

    def xǁLSTARǁ__init____mutmut_12(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        """Initialize LSTAR model with grid search configuration."""
        super().__init__(endog, order=order, n_regimes=2)
        self.gamma_grid = gamma_grid
        self.c_grid = c_grid
        self.refine = refine

    def xǁLSTARǁ__init____mutmut_13(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        """Initialize LSTAR model with grid search configuration."""
        super().__init__(
            endog,
            order=order,
            delay=delay,
        )
        self.gamma_grid = gamma_grid
        self.c_grid = c_grid
        self.refine = refine

    def xǁLSTARǁ__init____mutmut_14(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        """Initialize LSTAR model with grid search configuration."""
        super().__init__(endog, order=order, delay=delay, n_regimes=3)
        self.gamma_grid = gamma_grid
        self.c_grid = c_grid
        self.refine = refine

    def xǁLSTARǁ__init____mutmut_15(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        """Initialize LSTAR model with grid search configuration."""
        super().__init__(endog, order=order, delay=delay, n_regimes=2)
        self.gamma_grid = None
        self.c_grid = c_grid
        self.refine = refine

    def xǁLSTARǁ__init____mutmut_16(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        """Initialize LSTAR model with grid search configuration."""
        super().__init__(endog, order=order, delay=delay, n_regimes=2)
        self.gamma_grid = gamma_grid
        self.c_grid = None
        self.refine = refine

    def xǁLSTARǁ__init____mutmut_17(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        """Initialize LSTAR model with grid search configuration."""
        super().__init__(endog, order=order, delay=delay, n_regimes=2)
        self.gamma_grid = gamma_grid
        self.c_grid = c_grid
        self.refine = None

    xǁLSTARǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁLSTARǁ__init____mutmut_1": xǁLSTARǁ__init____mutmut_1,
        "xǁLSTARǁ__init____mutmut_2": xǁLSTARǁ__init____mutmut_2,
        "xǁLSTARǁ__init____mutmut_3": xǁLSTARǁ__init____mutmut_3,
        "xǁLSTARǁ__init____mutmut_4": xǁLSTARǁ__init____mutmut_4,
        "xǁLSTARǁ__init____mutmut_5": xǁLSTARǁ__init____mutmut_5,
        "xǁLSTARǁ__init____mutmut_6": xǁLSTARǁ__init____mutmut_6,
        "xǁLSTARǁ__init____mutmut_7": xǁLSTARǁ__init____mutmut_7,
        "xǁLSTARǁ__init____mutmut_8": xǁLSTARǁ__init____mutmut_8,
        "xǁLSTARǁ__init____mutmut_9": xǁLSTARǁ__init____mutmut_9,
        "xǁLSTARǁ__init____mutmut_10": xǁLSTARǁ__init____mutmut_10,
        "xǁLSTARǁ__init____mutmut_11": xǁLSTARǁ__init____mutmut_11,
        "xǁLSTARǁ__init____mutmut_12": xǁLSTARǁ__init____mutmut_12,
        "xǁLSTARǁ__init____mutmut_13": xǁLSTARǁ__init____mutmut_13,
        "xǁLSTARǁ__init____mutmut_14": xǁLSTARǁ__init____mutmut_14,
        "xǁLSTARǁ__init____mutmut_15": xǁLSTARǁ__init____mutmut_15,
        "xǁLSTARǁ__init____mutmut_16": xǁLSTARǁ__init____mutmut_16,
        "xǁLSTARǁ__init____mutmut_17": xǁLSTARǁ__init____mutmut_17,
    }
    xǁLSTARǁ__init____mutmut_orig.__name__ = "xǁLSTARǁ__init__"

    def _transition_function(
        self, s: NDArray[np.float64], params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        args = [s, params]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁLSTARǁ_transition_function__mutmut_orig"),
            object.__getattribute__(self, "xǁLSTARǁ_transition_function__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁLSTARǁ_transition_function__mutmut_orig(
        self, s: NDArray[np.float64], params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Logistic transition: G(s; gamma, c) = 1/(1+exp(-gamma*(s-c))).

        Parameters
        ----------
        s : ndarray
            Transition variable values.
        params : ndarray
            Array with [gamma, c].

        Returns
        -------
        ndarray
            Transition values in [0, 1].
        """
        gamma, c = params[0], params[1]
        return logistic_transition(s, gamma, c)

    def xǁLSTARǁ_transition_function__mutmut_1(
        self, s: NDArray[np.float64], params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Logistic transition: G(s; gamma, c) = 1/(1+exp(-gamma*(s-c))).

        Parameters
        ----------
        s : ndarray
            Transition variable values.
        params : ndarray
            Array with [gamma, c].

        Returns
        -------
        ndarray
            Transition values in [0, 1].
        """
        gamma, c = None
        return logistic_transition(s, gamma, c)

    def xǁLSTARǁ_transition_function__mutmut_2(
        self, s: NDArray[np.float64], params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Logistic transition: G(s; gamma, c) = 1/(1+exp(-gamma*(s-c))).

        Parameters
        ----------
        s : ndarray
            Transition variable values.
        params : ndarray
            Array with [gamma, c].

        Returns
        -------
        ndarray
            Transition values in [0, 1].
        """
        gamma, c = params[1], params[1]
        return logistic_transition(s, gamma, c)

    def xǁLSTARǁ_transition_function__mutmut_3(
        self, s: NDArray[np.float64], params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Logistic transition: G(s; gamma, c) = 1/(1+exp(-gamma*(s-c))).

        Parameters
        ----------
        s : ndarray
            Transition variable values.
        params : ndarray
            Array with [gamma, c].

        Returns
        -------
        ndarray
            Transition values in [0, 1].
        """
        gamma, c = params[0], params[2]
        return logistic_transition(s, gamma, c)

    def xǁLSTARǁ_transition_function__mutmut_4(
        self, s: NDArray[np.float64], params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Logistic transition: G(s; gamma, c) = 1/(1+exp(-gamma*(s-c))).

        Parameters
        ----------
        s : ndarray
            Transition variable values.
        params : ndarray
            Array with [gamma, c].

        Returns
        -------
        ndarray
            Transition values in [0, 1].
        """
        gamma, c = params[0], params[1]
        return logistic_transition(None, gamma, c)

    def xǁLSTARǁ_transition_function__mutmut_5(
        self, s: NDArray[np.float64], params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Logistic transition: G(s; gamma, c) = 1/(1+exp(-gamma*(s-c))).

        Parameters
        ----------
        s : ndarray
            Transition variable values.
        params : ndarray
            Array with [gamma, c].

        Returns
        -------
        ndarray
            Transition values in [0, 1].
        """
        gamma, c = params[0], params[1]
        return logistic_transition(s, None, c)

    def xǁLSTARǁ_transition_function__mutmut_6(
        self, s: NDArray[np.float64], params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Logistic transition: G(s; gamma, c) = 1/(1+exp(-gamma*(s-c))).

        Parameters
        ----------
        s : ndarray
            Transition variable values.
        params : ndarray
            Array with [gamma, c].

        Returns
        -------
        ndarray
            Transition values in [0, 1].
        """
        gamma, c = params[0], params[1]
        return logistic_transition(s, gamma, None)

    def xǁLSTARǁ_transition_function__mutmut_7(
        self, s: NDArray[np.float64], params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Logistic transition: G(s; gamma, c) = 1/(1+exp(-gamma*(s-c))).

        Parameters
        ----------
        s : ndarray
            Transition variable values.
        params : ndarray
            Array with [gamma, c].

        Returns
        -------
        ndarray
            Transition values in [0, 1].
        """
        gamma, c = params[0], params[1]
        return logistic_transition(gamma, c)

    def xǁLSTARǁ_transition_function__mutmut_8(
        self, s: NDArray[np.float64], params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Logistic transition: G(s; gamma, c) = 1/(1+exp(-gamma*(s-c))).

        Parameters
        ----------
        s : ndarray
            Transition variable values.
        params : ndarray
            Array with [gamma, c].

        Returns
        -------
        ndarray
            Transition values in [0, 1].
        """
        gamma, c = params[0], params[1]
        return logistic_transition(s, c)

    def xǁLSTARǁ_transition_function__mutmut_9(
        self, s: NDArray[np.float64], params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Logistic transition: G(s; gamma, c) = 1/(1+exp(-gamma*(s-c))).

        Parameters
        ----------
        s : ndarray
            Transition variable values.
        params : ndarray
            Array with [gamma, c].

        Returns
        -------
        ndarray
            Transition values in [0, 1].
        """
        gamma, c = params[0], params[1]
        return logistic_transition(
            s,
            gamma,
        )

    xǁLSTARǁ_transition_function__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁLSTARǁ_transition_function__mutmut_1": xǁLSTARǁ_transition_function__mutmut_1,
        "xǁLSTARǁ_transition_function__mutmut_2": xǁLSTARǁ_transition_function__mutmut_2,
        "xǁLSTARǁ_transition_function__mutmut_3": xǁLSTARǁ_transition_function__mutmut_3,
        "xǁLSTARǁ_transition_function__mutmut_4": xǁLSTARǁ_transition_function__mutmut_4,
        "xǁLSTARǁ_transition_function__mutmut_5": xǁLSTARǁ_transition_function__mutmut_5,
        "xǁLSTARǁ_transition_function__mutmut_6": xǁLSTARǁ_transition_function__mutmut_6,
        "xǁLSTARǁ_transition_function__mutmut_7": xǁLSTARǁ_transition_function__mutmut_7,
        "xǁLSTARǁ_transition_function__mutmut_8": xǁLSTARǁ_transition_function__mutmut_8,
        "xǁLSTARǁ_transition_function__mutmut_9": xǁLSTARǁ_transition_function__mutmut_9,
    }
    xǁLSTARǁ_transition_function__mutmut_orig.__name__ = "xǁLSTARǁ_transition_function"

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameters: [gamma=1, c=median(s)]."""
        return np.array([1.0, np.median(self._s)])

    @property
    def param_names(self) -> list[str]:
        """Parameter names."""
        names = ["gamma", "c"]
        for regime in range(1, 3):
            names.append(f"phi_0_regime{regime}")
            for lag in range(1, self.order + 1):
                names.append(f"phi_{lag}_regime{regime}")
        return names

    def _concentrated_ols(
        self,
        gamma: float,
        c: float,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        args = [gamma, c, y, x_mat, s]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁLSTARǁ_concentrated_ols__mutmut_orig"),
            object.__getattribute__(self, "xǁLSTARǁ_concentrated_ols__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁLSTARǁ_concentrated_ols__mutmut_orig(
        self,
        gamma: float,
        c: float,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        """OLS concentrated on (gamma, c).

        For given gamma and c, compute G(s; gamma, c), then solve:
        y = x1 * phi^{(1)} + x2 * phi^{(2)} + error

        where x1 = x_mat * (1 - G), x2 = x_mat * G.

        Parameters
        ----------
        gamma : float
            Speed of transition.
        c : float
            Location of transition.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        beta : ndarray
            Concatenated [phi^{(1)}, phi^{(2)}].
        resid : ndarray
            Residuals.
        rss : float
            Residual sum of squares.
        """
        g = logistic_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁLSTARǁ_concentrated_ols__mutmut_1(
        self,
        gamma: float,
        c: float,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        """OLS concentrated on (gamma, c).

        For given gamma and c, compute G(s; gamma, c), then solve:
        y = x1 * phi^{(1)} + x2 * phi^{(2)} + error

        where x1 = x_mat * (1 - G), x2 = x_mat * G.

        Parameters
        ----------
        gamma : float
            Speed of transition.
        c : float
            Location of transition.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        beta : ndarray
            Concatenated [phi^{(1)}, phi^{(2)}].
        resid : ndarray
            Residuals.
        rss : float
            Residual sum of squares.
        """
        g = None
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁLSTARǁ_concentrated_ols__mutmut_2(
        self,
        gamma: float,
        c: float,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        """OLS concentrated on (gamma, c).

        For given gamma and c, compute G(s; gamma, c), then solve:
        y = x1 * phi^{(1)} + x2 * phi^{(2)} + error

        where x1 = x_mat * (1 - G), x2 = x_mat * G.

        Parameters
        ----------
        gamma : float
            Speed of transition.
        c : float
            Location of transition.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        beta : ndarray
            Concatenated [phi^{(1)}, phi^{(2)}].
        resid : ndarray
            Residuals.
        rss : float
            Residual sum of squares.
        """
        g = logistic_transition(None, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁLSTARǁ_concentrated_ols__mutmut_3(
        self,
        gamma: float,
        c: float,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        """OLS concentrated on (gamma, c).

        For given gamma and c, compute G(s; gamma, c), then solve:
        y = x1 * phi^{(1)} + x2 * phi^{(2)} + error

        where x1 = x_mat * (1 - G), x2 = x_mat * G.

        Parameters
        ----------
        gamma : float
            Speed of transition.
        c : float
            Location of transition.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        beta : ndarray
            Concatenated [phi^{(1)}, phi^{(2)}].
        resid : ndarray
            Residuals.
        rss : float
            Residual sum of squares.
        """
        g = logistic_transition(s, None, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁLSTARǁ_concentrated_ols__mutmut_4(
        self,
        gamma: float,
        c: float,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        """OLS concentrated on (gamma, c).

        For given gamma and c, compute G(s; gamma, c), then solve:
        y = x1 * phi^{(1)} + x2 * phi^{(2)} + error

        where x1 = x_mat * (1 - G), x2 = x_mat * G.

        Parameters
        ----------
        gamma : float
            Speed of transition.
        c : float
            Location of transition.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        beta : ndarray
            Concatenated [phi^{(1)}, phi^{(2)}].
        resid : ndarray
            Residuals.
        rss : float
            Residual sum of squares.
        """
        g = logistic_transition(s, gamma, None)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁLSTARǁ_concentrated_ols__mutmut_5(
        self,
        gamma: float,
        c: float,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        """OLS concentrated on (gamma, c).

        For given gamma and c, compute G(s; gamma, c), then solve:
        y = x1 * phi^{(1)} + x2 * phi^{(2)} + error

        where x1 = x_mat * (1 - G), x2 = x_mat * G.

        Parameters
        ----------
        gamma : float
            Speed of transition.
        c : float
            Location of transition.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        beta : ndarray
            Concatenated [phi^{(1)}, phi^{(2)}].
        resid : ndarray
            Residuals.
        rss : float
            Residual sum of squares.
        """
        g = logistic_transition(gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁLSTARǁ_concentrated_ols__mutmut_6(
        self,
        gamma: float,
        c: float,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        """OLS concentrated on (gamma, c).

        For given gamma and c, compute G(s; gamma, c), then solve:
        y = x1 * phi^{(1)} + x2 * phi^{(2)} + error

        where x1 = x_mat * (1 - G), x2 = x_mat * G.

        Parameters
        ----------
        gamma : float
            Speed of transition.
        c : float
            Location of transition.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        beta : ndarray
            Concatenated [phi^{(1)}, phi^{(2)}].
        resid : ndarray
            Residuals.
        rss : float
            Residual sum of squares.
        """
        g = logistic_transition(s, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁLSTARǁ_concentrated_ols__mutmut_7(
        self,
        gamma: float,
        c: float,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        """OLS concentrated on (gamma, c).

        For given gamma and c, compute G(s; gamma, c), then solve:
        y = x1 * phi^{(1)} + x2 * phi^{(2)} + error

        where x1 = x_mat * (1 - G), x2 = x_mat * G.

        Parameters
        ----------
        gamma : float
            Speed of transition.
        c : float
            Location of transition.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        beta : ndarray
            Concatenated [phi^{(1)}, phi^{(2)}].
        resid : ndarray
            Residuals.
        rss : float
            Residual sum of squares.
        """
        g = logistic_transition(
            s,
            gamma,
        )
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁLSTARǁ_concentrated_ols__mutmut_8(
        self,
        gamma: float,
        c: float,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        """OLS concentrated on (gamma, c).

        For given gamma and c, compute G(s; gamma, c), then solve:
        y = x1 * phi^{(1)} + x2 * phi^{(2)} + error

        where x1 = x_mat * (1 - G), x2 = x_mat * G.

        Parameters
        ----------
        gamma : float
            Speed of transition.
        c : float
            Location of transition.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        beta : ndarray
            Concatenated [phi^{(1)}, phi^{(2)}].
        resid : ndarray
            Residuals.
        rss : float
            Residual sum of squares.
        """
        g = logistic_transition(s, gamma, c)
        x1 = None
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁLSTARǁ_concentrated_ols__mutmut_9(
        self,
        gamma: float,
        c: float,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        """OLS concentrated on (gamma, c).

        For given gamma and c, compute G(s; gamma, c), then solve:
        y = x1 * phi^{(1)} + x2 * phi^{(2)} + error

        where x1 = x_mat * (1 - G), x2 = x_mat * G.

        Parameters
        ----------
        gamma : float
            Speed of transition.
        c : float
            Location of transition.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        beta : ndarray
            Concatenated [phi^{(1)}, phi^{(2)}].
        resid : ndarray
            Residuals.
        rss : float
            Residual sum of squares.
        """
        g = logistic_transition(s, gamma, c)
        x1 = x_mat / (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁLSTARǁ_concentrated_ols__mutmut_10(
        self,
        gamma: float,
        c: float,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        """OLS concentrated on (gamma, c).

        For given gamma and c, compute G(s; gamma, c), then solve:
        y = x1 * phi^{(1)} + x2 * phi^{(2)} + error

        where x1 = x_mat * (1 - G), x2 = x_mat * G.

        Parameters
        ----------
        gamma : float
            Speed of transition.
        c : float
            Location of transition.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        beta : ndarray
            Concatenated [phi^{(1)}, phi^{(2)}].
        resid : ndarray
            Residuals.
        rss : float
            Residual sum of squares.
        """
        g = logistic_transition(s, gamma, c)
        x1 = x_mat * (1 + g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁLSTARǁ_concentrated_ols__mutmut_11(
        self,
        gamma: float,
        c: float,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        """OLS concentrated on (gamma, c).

        For given gamma and c, compute G(s; gamma, c), then solve:
        y = x1 * phi^{(1)} + x2 * phi^{(2)} + error

        where x1 = x_mat * (1 - G), x2 = x_mat * G.

        Parameters
        ----------
        gamma : float
            Speed of transition.
        c : float
            Location of transition.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        beta : ndarray
            Concatenated [phi^{(1)}, phi^{(2)}].
        resid : ndarray
            Residuals.
        rss : float
            Residual sum of squares.
        """
        g = logistic_transition(s, gamma, c)
        x1 = x_mat * (2 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁLSTARǁ_concentrated_ols__mutmut_12(
        self,
        gamma: float,
        c: float,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        """OLS concentrated on (gamma, c).

        For given gamma and c, compute G(s; gamma, c), then solve:
        y = x1 * phi^{(1)} + x2 * phi^{(2)} + error

        where x1 = x_mat * (1 - G), x2 = x_mat * G.

        Parameters
        ----------
        gamma : float
            Speed of transition.
        c : float
            Location of transition.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        beta : ndarray
            Concatenated [phi^{(1)}, phi^{(2)}].
        resid : ndarray
            Residuals.
        rss : float
            Residual sum of squares.
        """
        g = logistic_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = None
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁLSTARǁ_concentrated_ols__mutmut_13(
        self,
        gamma: float,
        c: float,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        """OLS concentrated on (gamma, c).

        For given gamma and c, compute G(s; gamma, c), then solve:
        y = x1 * phi^{(1)} + x2 * phi^{(2)} + error

        where x1 = x_mat * (1 - G), x2 = x_mat * G.

        Parameters
        ----------
        gamma : float
            Speed of transition.
        c : float
            Location of transition.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        beta : ndarray
            Concatenated [phi^{(1)}, phi^{(2)}].
        resid : ndarray
            Residuals.
        rss : float
            Residual sum of squares.
        """
        g = logistic_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat / g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁLSTARǁ_concentrated_ols__mutmut_14(
        self,
        gamma: float,
        c: float,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        """OLS concentrated on (gamma, c).

        For given gamma and c, compute G(s; gamma, c), then solve:
        y = x1 * phi^{(1)} + x2 * phi^{(2)} + error

        where x1 = x_mat * (1 - G), x2 = x_mat * G.

        Parameters
        ----------
        gamma : float
            Speed of transition.
        c : float
            Location of transition.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        beta : ndarray
            Concatenated [phi^{(1)}, phi^{(2)}].
        resid : ndarray
            Residuals.
        rss : float
            Residual sum of squares.
        """
        g = logistic_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = None

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁLSTARǁ_concentrated_ols__mutmut_15(
        self,
        gamma: float,
        c: float,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        """OLS concentrated on (gamma, c).

        For given gamma and c, compute G(s; gamma, c), then solve:
        y = x1 * phi^{(1)} + x2 * phi^{(2)} + error

        where x1 = x_mat * (1 - G), x2 = x_mat * G.

        Parameters
        ----------
        gamma : float
            Speed of transition.
        c : float
            Location of transition.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        beta : ndarray
            Concatenated [phi^{(1)}, phi^{(2)}].
        resid : ndarray
            Residuals.
        rss : float
            Residual sum of squares.
        """
        g = logistic_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack(None)

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁLSTARǁ_concentrated_ols__mutmut_16(
        self,
        gamma: float,
        c: float,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        """OLS concentrated on (gamma, c).

        For given gamma and c, compute G(s; gamma, c), then solve:
        y = x1 * phi^{(1)} + x2 * phi^{(2)} + error

        where x1 = x_mat * (1 - G), x2 = x_mat * G.

        Parameters
        ----------
        gamma : float
            Speed of transition.
        c : float
            Location of transition.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        beta : ndarray
            Concatenated [phi^{(1)}, phi^{(2)}].
        resid : ndarray
            Residuals.
        rss : float
            Residual sum of squares.
        """
        g = logistic_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = None
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁLSTARǁ_concentrated_ols__mutmut_17(
        self,
        gamma: float,
        c: float,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        """OLS concentrated on (gamma, c).

        For given gamma and c, compute G(s; gamma, c), then solve:
        y = x1 * phi^{(1)} + x2 * phi^{(2)} + error

        where x1 = x_mat * (1 - G), x2 = x_mat * G.

        Parameters
        ----------
        gamma : float
            Speed of transition.
        c : float
            Location of transition.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        beta : ndarray
            Concatenated [phi^{(1)}, phi^{(2)}].
        resid : ndarray
            Residuals.
        rss : float
            Residual sum of squares.
        """
        g = logistic_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(None, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁLSTARǁ_concentrated_ols__mutmut_18(
        self,
        gamma: float,
        c: float,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        """OLS concentrated on (gamma, c).

        For given gamma and c, compute G(s; gamma, c), then solve:
        y = x1 * phi^{(1)} + x2 * phi^{(2)} + error

        where x1 = x_mat * (1 - G), x2 = x_mat * G.

        Parameters
        ----------
        gamma : float
            Speed of transition.
        c : float
            Location of transition.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        beta : ndarray
            Concatenated [phi^{(1)}, phi^{(2)}].
        resid : ndarray
            Residuals.
        rss : float
            Residual sum of squares.
        """
        g = logistic_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, None, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁLSTARǁ_concentrated_ols__mutmut_19(
        self,
        gamma: float,
        c: float,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        """OLS concentrated on (gamma, c).

        For given gamma and c, compute G(s; gamma, c), then solve:
        y = x1 * phi^{(1)} + x2 * phi^{(2)} + error

        where x1 = x_mat * (1 - G), x2 = x_mat * G.

        Parameters
        ----------
        gamma : float
            Speed of transition.
        c : float
            Location of transition.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        beta : ndarray
            Concatenated [phi^{(1)}, phi^{(2)}].
        resid : ndarray
            Residuals.
        rss : float
            Residual sum of squares.
        """
        g = logistic_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁLSTARǁ_concentrated_ols__mutmut_20(
        self,
        gamma: float,
        c: float,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        """OLS concentrated on (gamma, c).

        For given gamma and c, compute G(s; gamma, c), then solve:
        y = x1 * phi^{(1)} + x2 * phi^{(2)} + error

        where x1 = x_mat * (1 - G), x2 = x_mat * G.

        Parameters
        ----------
        gamma : float
            Speed of transition.
        c : float
            Location of transition.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        beta : ndarray
            Concatenated [phi^{(1)}, phi^{(2)}].
        resid : ndarray
            Residuals.
        rss : float
            Residual sum of squares.
        """
        g = logistic_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁLSTARǁ_concentrated_ols__mutmut_21(
        self,
        gamma: float,
        c: float,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        """OLS concentrated on (gamma, c).

        For given gamma and c, compute G(s; gamma, c), then solve:
        y = x1 * phi^{(1)} + x2 * phi^{(2)} + error

        where x1 = x_mat * (1 - G), x2 = x_mat * G.

        Parameters
        ----------
        gamma : float
            Speed of transition.
        c : float
            Location of transition.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        beta : ndarray
            Concatenated [phi^{(1)}, phi^{(2)}].
        resid : ndarray
            Residuals.
        rss : float
            Residual sum of squares.
        """
        g = logistic_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(
            x_full,
            y,
        )[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁLSTARǁ_concentrated_ols__mutmut_22(
        self,
        gamma: float,
        c: float,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        """OLS concentrated on (gamma, c).

        For given gamma and c, compute G(s; gamma, c), then solve:
        y = x1 * phi^{(1)} + x2 * phi^{(2)} + error

        where x1 = x_mat * (1 - G), x2 = x_mat * G.

        Parameters
        ----------
        gamma : float
            Speed of transition.
        c : float
            Location of transition.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        beta : ndarray
            Concatenated [phi^{(1)}, phi^{(2)}].
        resid : ndarray
            Residuals.
        rss : float
            Residual sum of squares.
        """
        g = logistic_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[1]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁLSTARǁ_concentrated_ols__mutmut_23(
        self,
        gamma: float,
        c: float,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        """OLS concentrated on (gamma, c).

        For given gamma and c, compute G(s; gamma, c), then solve:
        y = x1 * phi^{(1)} + x2 * phi^{(2)} + error

        where x1 = x_mat * (1 - G), x2 = x_mat * G.

        Parameters
        ----------
        gamma : float
            Speed of transition.
        c : float
            Location of transition.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        beta : ndarray
            Concatenated [phi^{(1)}, phi^{(2)}].
        resid : ndarray
            Residuals.
        rss : float
            Residual sum of squares.
        """
        g = logistic_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = None
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁLSTARǁ_concentrated_ols__mutmut_24(
        self,
        gamma: float,
        c: float,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        """OLS concentrated on (gamma, c).

        For given gamma and c, compute G(s; gamma, c), then solve:
        y = x1 * phi^{(1)} + x2 * phi^{(2)} + error

        where x1 = x_mat * (1 - G), x2 = x_mat * G.

        Parameters
        ----------
        gamma : float
            Speed of transition.
        c : float
            Location of transition.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        beta : ndarray
            Concatenated [phi^{(1)}, phi^{(2)}].
        resid : ndarray
            Residuals.
        rss : float
            Residual sum of squares.
        """
        g = logistic_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y + x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁLSTARǁ_concentrated_ols__mutmut_25(
        self,
        gamma: float,
        c: float,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        """OLS concentrated on (gamma, c).

        For given gamma and c, compute G(s; gamma, c), then solve:
        y = x1 * phi^{(1)} + x2 * phi^{(2)} + error

        where x1 = x_mat * (1 - G), x2 = x_mat * G.

        Parameters
        ----------
        gamma : float
            Speed of transition.
        c : float
            Location of transition.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        beta : ndarray
            Concatenated [phi^{(1)}, phi^{(2)}].
        resid : ndarray
            Residuals.
        rss : float
            Residual sum of squares.
        """
        g = logistic_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = None
        return beta, resid, rss

    def xǁLSTARǁ_concentrated_ols__mutmut_26(
        self,
        gamma: float,
        c: float,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        """OLS concentrated on (gamma, c).

        For given gamma and c, compute G(s; gamma, c), then solve:
        y = x1 * phi^{(1)} + x2 * phi^{(2)} + error

        where x1 = x_mat * (1 - G), x2 = x_mat * G.

        Parameters
        ----------
        gamma : float
            Speed of transition.
        c : float
            Location of transition.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        beta : ndarray
            Concatenated [phi^{(1)}, phi^{(2)}].
        resid : ndarray
            Residuals.
        rss : float
            Residual sum of squares.
        """
        g = logistic_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(None)
        return beta, resid, rss

    def xǁLSTARǁ_concentrated_ols__mutmut_27(
        self,
        gamma: float,
        c: float,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        """OLS concentrated on (gamma, c).

        For given gamma and c, compute G(s; gamma, c), then solve:
        y = x1 * phi^{(1)} + x2 * phi^{(2)} + error

        where x1 = x_mat * (1 - G), x2 = x_mat * G.

        Parameters
        ----------
        gamma : float
            Speed of transition.
        c : float
            Location of transition.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        beta : ndarray
            Concatenated [phi^{(1)}, phi^{(2)}].
        resid : ndarray
            Residuals.
        rss : float
            Residual sum of squares.
        """
        g = logistic_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(None))
        return beta, resid, rss

    def xǁLSTARǁ_concentrated_ols__mutmut_28(
        self,
        gamma: float,
        c: float,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        """OLS concentrated on (gamma, c).

        For given gamma and c, compute G(s; gamma, c), then solve:
        y = x1 * phi^{(1)} + x2 * phi^{(2)} + error

        where x1 = x_mat * (1 - G), x2 = x_mat * G.

        Parameters
        ----------
        gamma : float
            Speed of transition.
        c : float
            Location of transition.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        beta : ndarray
            Concatenated [phi^{(1)}, phi^{(2)}].
        resid : ndarray
            Residuals.
        rss : float
            Residual sum of squares.
        """
        g = logistic_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid * 2))
        return beta, resid, rss

    def xǁLSTARǁ_concentrated_ols__mutmut_29(
        self,
        gamma: float,
        c: float,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], float]:
        """OLS concentrated on (gamma, c).

        For given gamma and c, compute G(s; gamma, c), then solve:
        y = x1 * phi^{(1)} + x2 * phi^{(2)} + error

        where x1 = x_mat * (1 - G), x2 = x_mat * G.

        Parameters
        ----------
        gamma : float
            Speed of transition.
        c : float
            Location of transition.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        beta : ndarray
            Concatenated [phi^{(1)}, phi^{(2)}].
        resid : ndarray
            Residuals.
        rss : float
            Residual sum of squares.
        """
        g = logistic_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**3))
        return beta, resid, rss

    xǁLSTARǁ_concentrated_ols__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁLSTARǁ_concentrated_ols__mutmut_1": xǁLSTARǁ_concentrated_ols__mutmut_1,
        "xǁLSTARǁ_concentrated_ols__mutmut_2": xǁLSTARǁ_concentrated_ols__mutmut_2,
        "xǁLSTARǁ_concentrated_ols__mutmut_3": xǁLSTARǁ_concentrated_ols__mutmut_3,
        "xǁLSTARǁ_concentrated_ols__mutmut_4": xǁLSTARǁ_concentrated_ols__mutmut_4,
        "xǁLSTARǁ_concentrated_ols__mutmut_5": xǁLSTARǁ_concentrated_ols__mutmut_5,
        "xǁLSTARǁ_concentrated_ols__mutmut_6": xǁLSTARǁ_concentrated_ols__mutmut_6,
        "xǁLSTARǁ_concentrated_ols__mutmut_7": xǁLSTARǁ_concentrated_ols__mutmut_7,
        "xǁLSTARǁ_concentrated_ols__mutmut_8": xǁLSTARǁ_concentrated_ols__mutmut_8,
        "xǁLSTARǁ_concentrated_ols__mutmut_9": xǁLSTARǁ_concentrated_ols__mutmut_9,
        "xǁLSTARǁ_concentrated_ols__mutmut_10": xǁLSTARǁ_concentrated_ols__mutmut_10,
        "xǁLSTARǁ_concentrated_ols__mutmut_11": xǁLSTARǁ_concentrated_ols__mutmut_11,
        "xǁLSTARǁ_concentrated_ols__mutmut_12": xǁLSTARǁ_concentrated_ols__mutmut_12,
        "xǁLSTARǁ_concentrated_ols__mutmut_13": xǁLSTARǁ_concentrated_ols__mutmut_13,
        "xǁLSTARǁ_concentrated_ols__mutmut_14": xǁLSTARǁ_concentrated_ols__mutmut_14,
        "xǁLSTARǁ_concentrated_ols__mutmut_15": xǁLSTARǁ_concentrated_ols__mutmut_15,
        "xǁLSTARǁ_concentrated_ols__mutmut_16": xǁLSTARǁ_concentrated_ols__mutmut_16,
        "xǁLSTARǁ_concentrated_ols__mutmut_17": xǁLSTARǁ_concentrated_ols__mutmut_17,
        "xǁLSTARǁ_concentrated_ols__mutmut_18": xǁLSTARǁ_concentrated_ols__mutmut_18,
        "xǁLSTARǁ_concentrated_ols__mutmut_19": xǁLSTARǁ_concentrated_ols__mutmut_19,
        "xǁLSTARǁ_concentrated_ols__mutmut_20": xǁLSTARǁ_concentrated_ols__mutmut_20,
        "xǁLSTARǁ_concentrated_ols__mutmut_21": xǁLSTARǁ_concentrated_ols__mutmut_21,
        "xǁLSTARǁ_concentrated_ols__mutmut_22": xǁLSTARǁ_concentrated_ols__mutmut_22,
        "xǁLSTARǁ_concentrated_ols__mutmut_23": xǁLSTARǁ_concentrated_ols__mutmut_23,
        "xǁLSTARǁ_concentrated_ols__mutmut_24": xǁLSTARǁ_concentrated_ols__mutmut_24,
        "xǁLSTARǁ_concentrated_ols__mutmut_25": xǁLSTARǁ_concentrated_ols__mutmut_25,
        "xǁLSTARǁ_concentrated_ols__mutmut_26": xǁLSTARǁ_concentrated_ols__mutmut_26,
        "xǁLSTARǁ_concentrated_ols__mutmut_27": xǁLSTARǁ_concentrated_ols__mutmut_27,
        "xǁLSTARǁ_concentrated_ols__mutmut_28": xǁLSTARǁ_concentrated_ols__mutmut_28,
        "xǁLSTARǁ_concentrated_ols__mutmut_29": xǁLSTARǁ_concentrated_ols__mutmut_29,
    }
    xǁLSTARǁ_concentrated_ols__mutmut_orig.__name__ = "xǁLSTARǁ_concentrated_ols"

    def _grid_search(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        args = [y, x_mat, s]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁLSTARǁ_grid_search__mutmut_orig"),
            object.__getattribute__(self, "xǁLSTARǁ_grid_search__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁLSTARǁ_grid_search__mutmut_orig(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_1(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = None

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_2(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(None, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_3(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, None, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_4(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, None)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_5(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_6(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_7(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(
            -1,
            2,
        )

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_8(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(+1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_9(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-2, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_10(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 3, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_11(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = None
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_12(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(None)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_13(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = None
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_14(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = None
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_15(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(None)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_16(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 / n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_17(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(1.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_18(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = None
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_19(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(None)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_20(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 / n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_21(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(1.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_22(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo > hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_23(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = None
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_24(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 1
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_25(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = None
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_26(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n + 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_27(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 2
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_28(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = None

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_29(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(None, s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_30(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], None, self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_31(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], None)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_32(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_33(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_34(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(
            s_sorted[lo],
            s_sorted[hi],
        )

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_35(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = None
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_36(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = None
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_37(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 2.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_38(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = None

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_39(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(None)

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_40(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(None))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_41(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = None
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_42(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(None, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_43(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, None, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_44(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, None, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_45(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, None, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_46(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, None)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_47(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_48(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_49(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_50(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_51(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(
                        gamma,
                        c_val,
                        y,
                        x_mat,
                    )
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_52(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss <= best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_53(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = None
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_54(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = None
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_55(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(None)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_56(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = None
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_57(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(None)
                except np.linalg.LinAlgError:
                    continue

        return best_gamma, best_c, best_rss

    def xǁLSTARǁ_grid_search__mutmut_58(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        """Grid search over (gamma, c) to find starting values.

        Parameters
        ----------
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        best_gamma, best_c, best_rss
        """
        # Gamma grid: log-spaced from 0.1 to 100
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

        # c grid: percentiles 15%-85% of s
        s_sorted = np.sort(s)
        n = len(s)
        lo = int(0.15 * n)
        hi = int(0.85 * n)
        if lo >= hi:
            lo = 0
            hi = n - 1
        c_vals = np.linspace(s_sorted[lo], s_sorted[hi], self.c_grid)

        best_rss = np.inf
        best_gamma = 1.0
        best_c = float(np.median(s))

        for gamma in gamma_vals:
            for c_val in c_vals:
                try:
                    _, _, rss = self._concentrated_ols(gamma, c_val, y, x_mat, s)
                    if rss < best_rss:
                        best_rss = rss
                        best_gamma = float(gamma)
                        best_c = float(c_val)
                except np.linalg.LinAlgError:
                    break

        return best_gamma, best_c, best_rss

    xǁLSTARǁ_grid_search__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁLSTARǁ_grid_search__mutmut_1": xǁLSTARǁ_grid_search__mutmut_1,
        "xǁLSTARǁ_grid_search__mutmut_2": xǁLSTARǁ_grid_search__mutmut_2,
        "xǁLSTARǁ_grid_search__mutmut_3": xǁLSTARǁ_grid_search__mutmut_3,
        "xǁLSTARǁ_grid_search__mutmut_4": xǁLSTARǁ_grid_search__mutmut_4,
        "xǁLSTARǁ_grid_search__mutmut_5": xǁLSTARǁ_grid_search__mutmut_5,
        "xǁLSTARǁ_grid_search__mutmut_6": xǁLSTARǁ_grid_search__mutmut_6,
        "xǁLSTARǁ_grid_search__mutmut_7": xǁLSTARǁ_grid_search__mutmut_7,
        "xǁLSTARǁ_grid_search__mutmut_8": xǁLSTARǁ_grid_search__mutmut_8,
        "xǁLSTARǁ_grid_search__mutmut_9": xǁLSTARǁ_grid_search__mutmut_9,
        "xǁLSTARǁ_grid_search__mutmut_10": xǁLSTARǁ_grid_search__mutmut_10,
        "xǁLSTARǁ_grid_search__mutmut_11": xǁLSTARǁ_grid_search__mutmut_11,
        "xǁLSTARǁ_grid_search__mutmut_12": xǁLSTARǁ_grid_search__mutmut_12,
        "xǁLSTARǁ_grid_search__mutmut_13": xǁLSTARǁ_grid_search__mutmut_13,
        "xǁLSTARǁ_grid_search__mutmut_14": xǁLSTARǁ_grid_search__mutmut_14,
        "xǁLSTARǁ_grid_search__mutmut_15": xǁLSTARǁ_grid_search__mutmut_15,
        "xǁLSTARǁ_grid_search__mutmut_16": xǁLSTARǁ_grid_search__mutmut_16,
        "xǁLSTARǁ_grid_search__mutmut_17": xǁLSTARǁ_grid_search__mutmut_17,
        "xǁLSTARǁ_grid_search__mutmut_18": xǁLSTARǁ_grid_search__mutmut_18,
        "xǁLSTARǁ_grid_search__mutmut_19": xǁLSTARǁ_grid_search__mutmut_19,
        "xǁLSTARǁ_grid_search__mutmut_20": xǁLSTARǁ_grid_search__mutmut_20,
        "xǁLSTARǁ_grid_search__mutmut_21": xǁLSTARǁ_grid_search__mutmut_21,
        "xǁLSTARǁ_grid_search__mutmut_22": xǁLSTARǁ_grid_search__mutmut_22,
        "xǁLSTARǁ_grid_search__mutmut_23": xǁLSTARǁ_grid_search__mutmut_23,
        "xǁLSTARǁ_grid_search__mutmut_24": xǁLSTARǁ_grid_search__mutmut_24,
        "xǁLSTARǁ_grid_search__mutmut_25": xǁLSTARǁ_grid_search__mutmut_25,
        "xǁLSTARǁ_grid_search__mutmut_26": xǁLSTARǁ_grid_search__mutmut_26,
        "xǁLSTARǁ_grid_search__mutmut_27": xǁLSTARǁ_grid_search__mutmut_27,
        "xǁLSTARǁ_grid_search__mutmut_28": xǁLSTARǁ_grid_search__mutmut_28,
        "xǁLSTARǁ_grid_search__mutmut_29": xǁLSTARǁ_grid_search__mutmut_29,
        "xǁLSTARǁ_grid_search__mutmut_30": xǁLSTARǁ_grid_search__mutmut_30,
        "xǁLSTARǁ_grid_search__mutmut_31": xǁLSTARǁ_grid_search__mutmut_31,
        "xǁLSTARǁ_grid_search__mutmut_32": xǁLSTARǁ_grid_search__mutmut_32,
        "xǁLSTARǁ_grid_search__mutmut_33": xǁLSTARǁ_grid_search__mutmut_33,
        "xǁLSTARǁ_grid_search__mutmut_34": xǁLSTARǁ_grid_search__mutmut_34,
        "xǁLSTARǁ_grid_search__mutmut_35": xǁLSTARǁ_grid_search__mutmut_35,
        "xǁLSTARǁ_grid_search__mutmut_36": xǁLSTARǁ_grid_search__mutmut_36,
        "xǁLSTARǁ_grid_search__mutmut_37": xǁLSTARǁ_grid_search__mutmut_37,
        "xǁLSTARǁ_grid_search__mutmut_38": xǁLSTARǁ_grid_search__mutmut_38,
        "xǁLSTARǁ_grid_search__mutmut_39": xǁLSTARǁ_grid_search__mutmut_39,
        "xǁLSTARǁ_grid_search__mutmut_40": xǁLSTARǁ_grid_search__mutmut_40,
        "xǁLSTARǁ_grid_search__mutmut_41": xǁLSTARǁ_grid_search__mutmut_41,
        "xǁLSTARǁ_grid_search__mutmut_42": xǁLSTARǁ_grid_search__mutmut_42,
        "xǁLSTARǁ_grid_search__mutmut_43": xǁLSTARǁ_grid_search__mutmut_43,
        "xǁLSTARǁ_grid_search__mutmut_44": xǁLSTARǁ_grid_search__mutmut_44,
        "xǁLSTARǁ_grid_search__mutmut_45": xǁLSTARǁ_grid_search__mutmut_45,
        "xǁLSTARǁ_grid_search__mutmut_46": xǁLSTARǁ_grid_search__mutmut_46,
        "xǁLSTARǁ_grid_search__mutmut_47": xǁLSTARǁ_grid_search__mutmut_47,
        "xǁLSTARǁ_grid_search__mutmut_48": xǁLSTARǁ_grid_search__mutmut_48,
        "xǁLSTARǁ_grid_search__mutmut_49": xǁLSTARǁ_grid_search__mutmut_49,
        "xǁLSTARǁ_grid_search__mutmut_50": xǁLSTARǁ_grid_search__mutmut_50,
        "xǁLSTARǁ_grid_search__mutmut_51": xǁLSTARǁ_grid_search__mutmut_51,
        "xǁLSTARǁ_grid_search__mutmut_52": xǁLSTARǁ_grid_search__mutmut_52,
        "xǁLSTARǁ_grid_search__mutmut_53": xǁLSTARǁ_grid_search__mutmut_53,
        "xǁLSTARǁ_grid_search__mutmut_54": xǁLSTARǁ_grid_search__mutmut_54,
        "xǁLSTARǁ_grid_search__mutmut_55": xǁLSTARǁ_grid_search__mutmut_55,
        "xǁLSTARǁ_grid_search__mutmut_56": xǁLSTARǁ_grid_search__mutmut_56,
        "xǁLSTARǁ_grid_search__mutmut_57": xǁLSTARǁ_grid_search__mutmut_57,
        "xǁLSTARǁ_grid_search__mutmut_58": xǁLSTARǁ_grid_search__mutmut_58,
    }
    xǁLSTARǁ_grid_search__mutmut_orig.__name__ = "xǁLSTARǁ_grid_search"

    def _nls_objective(
        self,
        transition_params: NDArray[np.float64],
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> float:
        args = [transition_params, y, x_mat, s]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁLSTARǁ_nls_objective__mutmut_orig"),
            object.__getattribute__(self, "xǁLSTARǁ_nls_objective__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁLSTARǁ_nls_objective__mutmut_orig(
        self,
        transition_params: NDArray[np.float64],
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> float:
        """NLS objective: RSS as function of (gamma, c).

        Parameters
        ----------
        transition_params : ndarray
            [log_gamma, c] - log_gamma to ensure gamma > 0.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        float
            RSS.
        """
        log_gamma, c = transition_params
        gamma = np.exp(log_gamma)
        gamma = min(gamma, 500.0)  # cap gamma

        try:
            _, _, rss = self._concentrated_ols(gamma, c, y, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁLSTARǁ_nls_objective__mutmut_1(
        self,
        transition_params: NDArray[np.float64],
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> float:
        """NLS objective: RSS as function of (gamma, c).

        Parameters
        ----------
        transition_params : ndarray
            [log_gamma, c] - log_gamma to ensure gamma > 0.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        float
            RSS.
        """
        log_gamma, c = None
        gamma = np.exp(log_gamma)
        gamma = min(gamma, 500.0)  # cap gamma

        try:
            _, _, rss = self._concentrated_ols(gamma, c, y, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁLSTARǁ_nls_objective__mutmut_2(
        self,
        transition_params: NDArray[np.float64],
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> float:
        """NLS objective: RSS as function of (gamma, c).

        Parameters
        ----------
        transition_params : ndarray
            [log_gamma, c] - log_gamma to ensure gamma > 0.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        float
            RSS.
        """
        log_gamma, c = transition_params
        gamma = None
        gamma = min(gamma, 500.0)  # cap gamma

        try:
            _, _, rss = self._concentrated_ols(gamma, c, y, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁLSTARǁ_nls_objective__mutmut_3(
        self,
        transition_params: NDArray[np.float64],
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> float:
        """NLS objective: RSS as function of (gamma, c).

        Parameters
        ----------
        transition_params : ndarray
            [log_gamma, c] - log_gamma to ensure gamma > 0.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        float
            RSS.
        """
        log_gamma, c = transition_params
        gamma = np.exp(None)
        gamma = min(gamma, 500.0)  # cap gamma

        try:
            _, _, rss = self._concentrated_ols(gamma, c, y, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁLSTARǁ_nls_objective__mutmut_4(
        self,
        transition_params: NDArray[np.float64],
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> float:
        """NLS objective: RSS as function of (gamma, c).

        Parameters
        ----------
        transition_params : ndarray
            [log_gamma, c] - log_gamma to ensure gamma > 0.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        float
            RSS.
        """
        log_gamma, c = transition_params
        gamma = np.exp(log_gamma)
        gamma = None  # cap gamma

        try:
            _, _, rss = self._concentrated_ols(gamma, c, y, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁLSTARǁ_nls_objective__mutmut_5(
        self,
        transition_params: NDArray[np.float64],
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> float:
        """NLS objective: RSS as function of (gamma, c).

        Parameters
        ----------
        transition_params : ndarray
            [log_gamma, c] - log_gamma to ensure gamma > 0.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        float
            RSS.
        """
        log_gamma, c = transition_params
        gamma = np.exp(log_gamma)
        gamma = min(None, 500.0)  # cap gamma

        try:
            _, _, rss = self._concentrated_ols(gamma, c, y, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁLSTARǁ_nls_objective__mutmut_6(
        self,
        transition_params: NDArray[np.float64],
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> float:
        """NLS objective: RSS as function of (gamma, c).

        Parameters
        ----------
        transition_params : ndarray
            [log_gamma, c] - log_gamma to ensure gamma > 0.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        float
            RSS.
        """
        log_gamma, c = transition_params
        gamma = np.exp(log_gamma)
        gamma = min(gamma, None)  # cap gamma

        try:
            _, _, rss = self._concentrated_ols(gamma, c, y, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁLSTARǁ_nls_objective__mutmut_7(
        self,
        transition_params: NDArray[np.float64],
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> float:
        """NLS objective: RSS as function of (gamma, c).

        Parameters
        ----------
        transition_params : ndarray
            [log_gamma, c] - log_gamma to ensure gamma > 0.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        float
            RSS.
        """
        log_gamma, c = transition_params
        gamma = np.exp(log_gamma)
        gamma = min(500.0)  # cap gamma

        try:
            _, _, rss = self._concentrated_ols(gamma, c, y, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁLSTARǁ_nls_objective__mutmut_8(
        self,
        transition_params: NDArray[np.float64],
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> float:
        """NLS objective: RSS as function of (gamma, c).

        Parameters
        ----------
        transition_params : ndarray
            [log_gamma, c] - log_gamma to ensure gamma > 0.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        float
            RSS.
        """
        log_gamma, c = transition_params
        gamma = np.exp(log_gamma)
        gamma = min(
            gamma,
        )  # cap gamma

        try:
            _, _, rss = self._concentrated_ols(gamma, c, y, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁLSTARǁ_nls_objective__mutmut_9(
        self,
        transition_params: NDArray[np.float64],
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> float:
        """NLS objective: RSS as function of (gamma, c).

        Parameters
        ----------
        transition_params : ndarray
            [log_gamma, c] - log_gamma to ensure gamma > 0.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        float
            RSS.
        """
        log_gamma, c = transition_params
        gamma = np.exp(log_gamma)
        gamma = min(gamma, 501.0)  # cap gamma

        try:
            _, _, rss = self._concentrated_ols(gamma, c, y, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁLSTARǁ_nls_objective__mutmut_10(
        self,
        transition_params: NDArray[np.float64],
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> float:
        """NLS objective: RSS as function of (gamma, c).

        Parameters
        ----------
        transition_params : ndarray
            [log_gamma, c] - log_gamma to ensure gamma > 0.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        float
            RSS.
        """
        log_gamma, c = transition_params
        gamma = np.exp(log_gamma)
        gamma = min(gamma, 500.0)  # cap gamma

        try:
            _, _, rss = None
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁLSTARǁ_nls_objective__mutmut_11(
        self,
        transition_params: NDArray[np.float64],
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> float:
        """NLS objective: RSS as function of (gamma, c).

        Parameters
        ----------
        transition_params : ndarray
            [log_gamma, c] - log_gamma to ensure gamma > 0.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        float
            RSS.
        """
        log_gamma, c = transition_params
        gamma = np.exp(log_gamma)
        gamma = min(gamma, 500.0)  # cap gamma

        try:
            _, _, rss = self._concentrated_ols(None, c, y, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁLSTARǁ_nls_objective__mutmut_12(
        self,
        transition_params: NDArray[np.float64],
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> float:
        """NLS objective: RSS as function of (gamma, c).

        Parameters
        ----------
        transition_params : ndarray
            [log_gamma, c] - log_gamma to ensure gamma > 0.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        float
            RSS.
        """
        log_gamma, c = transition_params
        gamma = np.exp(log_gamma)
        gamma = min(gamma, 500.0)  # cap gamma

        try:
            _, _, rss = self._concentrated_ols(gamma, None, y, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁLSTARǁ_nls_objective__mutmut_13(
        self,
        transition_params: NDArray[np.float64],
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> float:
        """NLS objective: RSS as function of (gamma, c).

        Parameters
        ----------
        transition_params : ndarray
            [log_gamma, c] - log_gamma to ensure gamma > 0.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        float
            RSS.
        """
        log_gamma, c = transition_params
        gamma = np.exp(log_gamma)
        gamma = min(gamma, 500.0)  # cap gamma

        try:
            _, _, rss = self._concentrated_ols(gamma, c, None, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁLSTARǁ_nls_objective__mutmut_14(
        self,
        transition_params: NDArray[np.float64],
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> float:
        """NLS objective: RSS as function of (gamma, c).

        Parameters
        ----------
        transition_params : ndarray
            [log_gamma, c] - log_gamma to ensure gamma > 0.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        float
            RSS.
        """
        log_gamma, c = transition_params
        gamma = np.exp(log_gamma)
        gamma = min(gamma, 500.0)  # cap gamma

        try:
            _, _, rss = self._concentrated_ols(gamma, c, y, None, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁLSTARǁ_nls_objective__mutmut_15(
        self,
        transition_params: NDArray[np.float64],
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> float:
        """NLS objective: RSS as function of (gamma, c).

        Parameters
        ----------
        transition_params : ndarray
            [log_gamma, c] - log_gamma to ensure gamma > 0.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        float
            RSS.
        """
        log_gamma, c = transition_params
        gamma = np.exp(log_gamma)
        gamma = min(gamma, 500.0)  # cap gamma

        try:
            _, _, rss = self._concentrated_ols(gamma, c, y, x_mat, None)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁLSTARǁ_nls_objective__mutmut_16(
        self,
        transition_params: NDArray[np.float64],
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> float:
        """NLS objective: RSS as function of (gamma, c).

        Parameters
        ----------
        transition_params : ndarray
            [log_gamma, c] - log_gamma to ensure gamma > 0.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        float
            RSS.
        """
        log_gamma, c = transition_params
        gamma = np.exp(log_gamma)
        gamma = min(gamma, 500.0)  # cap gamma

        try:
            _, _, rss = self._concentrated_ols(c, y, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁLSTARǁ_nls_objective__mutmut_17(
        self,
        transition_params: NDArray[np.float64],
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> float:
        """NLS objective: RSS as function of (gamma, c).

        Parameters
        ----------
        transition_params : ndarray
            [log_gamma, c] - log_gamma to ensure gamma > 0.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        float
            RSS.
        """
        log_gamma, c = transition_params
        gamma = np.exp(log_gamma)
        gamma = min(gamma, 500.0)  # cap gamma

        try:
            _, _, rss = self._concentrated_ols(gamma, y, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁLSTARǁ_nls_objective__mutmut_18(
        self,
        transition_params: NDArray[np.float64],
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> float:
        """NLS objective: RSS as function of (gamma, c).

        Parameters
        ----------
        transition_params : ndarray
            [log_gamma, c] - log_gamma to ensure gamma > 0.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        float
            RSS.
        """
        log_gamma, c = transition_params
        gamma = np.exp(log_gamma)
        gamma = min(gamma, 500.0)  # cap gamma

        try:
            _, _, rss = self._concentrated_ols(gamma, c, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁLSTARǁ_nls_objective__mutmut_19(
        self,
        transition_params: NDArray[np.float64],
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> float:
        """NLS objective: RSS as function of (gamma, c).

        Parameters
        ----------
        transition_params : ndarray
            [log_gamma, c] - log_gamma to ensure gamma > 0.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        float
            RSS.
        """
        log_gamma, c = transition_params
        gamma = np.exp(log_gamma)
        gamma = min(gamma, 500.0)  # cap gamma

        try:
            _, _, rss = self._concentrated_ols(gamma, c, y, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁLSTARǁ_nls_objective__mutmut_20(
        self,
        transition_params: NDArray[np.float64],
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> float:
        """NLS objective: RSS as function of (gamma, c).

        Parameters
        ----------
        transition_params : ndarray
            [log_gamma, c] - log_gamma to ensure gamma > 0.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        float
            RSS.
        """
        log_gamma, c = transition_params
        gamma = np.exp(log_gamma)
        gamma = min(gamma, 500.0)  # cap gamma

        try:
            _, _, rss = self._concentrated_ols(
                gamma,
                c,
                y,
                x_mat,
            )
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁLSTARǁ_nls_objective__mutmut_21(
        self,
        transition_params: NDArray[np.float64],
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> float:
        """NLS objective: RSS as function of (gamma, c).

        Parameters
        ----------
        transition_params : ndarray
            [log_gamma, c] - log_gamma to ensure gamma > 0.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        float
            RSS.
        """
        log_gamma, c = transition_params
        gamma = np.exp(log_gamma)
        gamma = min(gamma, 500.0)  # cap gamma

        try:
            _, _, rss = self._concentrated_ols(gamma, c, y, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = None
        return rss

    def xǁLSTARǁ_nls_objective__mutmut_22(
        self,
        transition_params: NDArray[np.float64],
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> float:
        """NLS objective: RSS as function of (gamma, c).

        Parameters
        ----------
        transition_params : ndarray
            [log_gamma, c] - log_gamma to ensure gamma > 0.
        y : ndarray
            Dependent variable.
        x_mat : ndarray
            Design matrix.
        s : ndarray
            Transition variable.

        Returns
        -------
        float
            RSS.
        """
        log_gamma, c = transition_params
        gamma = np.exp(log_gamma)
        gamma = min(gamma, 500.0)  # cap gamma

        try:
            _, _, rss = self._concentrated_ols(gamma, c, y, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1000000000000001.0
        return rss

    xǁLSTARǁ_nls_objective__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁLSTARǁ_nls_objective__mutmut_1": xǁLSTARǁ_nls_objective__mutmut_1,
        "xǁLSTARǁ_nls_objective__mutmut_2": xǁLSTARǁ_nls_objective__mutmut_2,
        "xǁLSTARǁ_nls_objective__mutmut_3": xǁLSTARǁ_nls_objective__mutmut_3,
        "xǁLSTARǁ_nls_objective__mutmut_4": xǁLSTARǁ_nls_objective__mutmut_4,
        "xǁLSTARǁ_nls_objective__mutmut_5": xǁLSTARǁ_nls_objective__mutmut_5,
        "xǁLSTARǁ_nls_objective__mutmut_6": xǁLSTARǁ_nls_objective__mutmut_6,
        "xǁLSTARǁ_nls_objective__mutmut_7": xǁLSTARǁ_nls_objective__mutmut_7,
        "xǁLSTARǁ_nls_objective__mutmut_8": xǁLSTARǁ_nls_objective__mutmut_8,
        "xǁLSTARǁ_nls_objective__mutmut_9": xǁLSTARǁ_nls_objective__mutmut_9,
        "xǁLSTARǁ_nls_objective__mutmut_10": xǁLSTARǁ_nls_objective__mutmut_10,
        "xǁLSTARǁ_nls_objective__mutmut_11": xǁLSTARǁ_nls_objective__mutmut_11,
        "xǁLSTARǁ_nls_objective__mutmut_12": xǁLSTARǁ_nls_objective__mutmut_12,
        "xǁLSTARǁ_nls_objective__mutmut_13": xǁLSTARǁ_nls_objective__mutmut_13,
        "xǁLSTARǁ_nls_objective__mutmut_14": xǁLSTARǁ_nls_objective__mutmut_14,
        "xǁLSTARǁ_nls_objective__mutmut_15": xǁLSTARǁ_nls_objective__mutmut_15,
        "xǁLSTARǁ_nls_objective__mutmut_16": xǁLSTARǁ_nls_objective__mutmut_16,
        "xǁLSTARǁ_nls_objective__mutmut_17": xǁLSTARǁ_nls_objective__mutmut_17,
        "xǁLSTARǁ_nls_objective__mutmut_18": xǁLSTARǁ_nls_objective__mutmut_18,
        "xǁLSTARǁ_nls_objective__mutmut_19": xǁLSTARǁ_nls_objective__mutmut_19,
        "xǁLSTARǁ_nls_objective__mutmut_20": xǁLSTARǁ_nls_objective__mutmut_20,
        "xǁLSTARǁ_nls_objective__mutmut_21": xǁLSTARǁ_nls_objective__mutmut_21,
        "xǁLSTARǁ_nls_objective__mutmut_22": xǁLSTARǁ_nls_objective__mutmut_22,
    }
    xǁLSTARǁ_nls_objective__mutmut_orig.__name__ = "xǁLSTARǁ_nls_objective"

    def _fit_cls(self) -> ThresholdResults:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁLSTARǁ_fit_cls__mutmut_orig"),
            object.__getattribute__(self, "xǁLSTARǁ_fit_cls__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_orig(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_1(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = None
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_2(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = None
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_3(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = None

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_4(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = None

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_5(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(None, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_6(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, None, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_7(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, None)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_8(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_9(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_10(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(
            y,
            x_mat,
        )

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_11(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = None
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_12(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array(None)
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_13(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(None), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_14(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(None, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_15(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, None)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_16(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_17(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array(
                [
                    np.log(
                        max(
                            gamma_init,
                        )
                    ),
                    c_init,
                ]
            )
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_18(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 1.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_19(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = None
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_20(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                None,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_21(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                None,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_22(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=None,
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_23(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method=None,
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_24(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options=None,
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_25(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_26(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_27(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_28(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_29(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_30(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="XXNelder-MeadXX",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_31(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="nelder-mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_32(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="NELDER-MEAD",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_33(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"XXmaxiterXX": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_34(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"MAXITER": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_35(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5001, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_36(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "XXxatolXX": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_37(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "XATOL": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_38(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1.000001, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_39(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "XXfatolXX": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_40(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "FATOL": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_41(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1.000001},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_42(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = None
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_43(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(None, 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_44(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), None)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_45(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_46(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(
                np.exp(result.x[0]),
            )
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_47(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(None), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_48(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[1]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_49(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 501.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_50(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = None
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_51(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[2]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_52(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = None
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_53(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = None

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_54(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = None
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_55(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(None, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_56(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, None, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_57(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, None, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_58(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, None, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_59(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, None)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_60(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_61(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_62(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_63(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_64(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(
            best_gamma,
            best_c,
            y,
            x_mat,
        )
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_65(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = None

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_66(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(None, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_67(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, None, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_68(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, None)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_69(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_70(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_71(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(
            s,
            best_gamma,
        )

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_72(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = None
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_73(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order - 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_74(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 2
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_75(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = None
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_76(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = None

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_77(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = None
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_78(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = None

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_79(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss * t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_80(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = None

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_81(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) + rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_82(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff / (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_83(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 / t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_84(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = +0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_85(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -1.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_86(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) - np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_87(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(None) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_88(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 / np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_89(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(3 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_90(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(None)) - rss / (2 * max(sigma2, 1e-12))

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_91(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(None, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_92(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, None))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_93(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_94(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (
            np.log(2 * np.pi)
            + np.log(
                max(
                    sigma2,
                )
            )
        ) - rss / (2 * max(sigma2, 1e-12))

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_95(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1.000000000001))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_96(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss * (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_97(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 / max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_98(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            3 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_99(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(None, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_100(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, None)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_101(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_102(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2
            * max(
                sigma2,
            )
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_103(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1.000000000001)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_104(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = None
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_105(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) - 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_106(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 / (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_107(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 3 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_108(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order - 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_109(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 2) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_110(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 3
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_111(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = None
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_112(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll - 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_113(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 / ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_114(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = +2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_115(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -3 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_116(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 / n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_117(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 3 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_118(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = None

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_119(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll - np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_120(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 / ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_121(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = +2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_122(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -3 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_123(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) / n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_124(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(None) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_125(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = None
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_126(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g <= 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_127(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 1.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_128(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = None
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_129(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g > 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_130(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 1.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_131(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = None
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_132(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(None) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_133(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(None)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_134(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] * 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_135(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 3)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_136(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() >= 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_137(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 1 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_138(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = None

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_139(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(None) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_140(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(None)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_141(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] * 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_142(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 3)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_143(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() >= 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_144(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 1 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_145(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=None,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_146(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params=None,
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_147(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=None,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_148(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=None,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_149(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params=None,
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_150(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=None,
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_151(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=None,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_152(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=None,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_153(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=None,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_154(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=None,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_155(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=None,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_156(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2=None,
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_157(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=None,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_158(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=None,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_159(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=None,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_160(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=None,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_161(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=None,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_162(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=None,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_163(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=None,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_164(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=None,
        )

    def xǁLSTARǁ_fit_cls__mutmut_165(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_166(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_167(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_168(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_169(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_170(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_171(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_172(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_173(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_174(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_175(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_176(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_177(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_178(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_179(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_180(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_181(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_182(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_183(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_184(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
        )

    def xǁLSTARǁ_fit_cls__mutmut_185(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"XXregime_1XX": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_186(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"REGIME_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_187(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "XXregime_2XX": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_188(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "REGIME_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_189(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"XXgammaXX": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_190(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"GAMMA": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_191(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "XXcXX": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_192(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "C": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_193(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array(None),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_194(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"XXregime_1XX": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_195(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"REGIME_1": sigma2_1, "regime_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_196(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "XXregime_2XX": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    def xǁLSTARǁ_fit_cls__mutmut_197(self) -> ThresholdResults:
        """Fit LSTAR via Conditional Least Squares (NLS).

        Returns
        -------
        ThresholdResults
        """
        y = self._y
        x_mat = self._X
        s = self._s

        # Grid search for starting values
        gamma_init, c_init, _ = self._grid_search(y, x_mat, s)

        if self.refine:
            # Refine via NLS (optimize over log(gamma) and c)
            x0 = np.array([np.log(max(gamma_init, 0.01)), c_init])
            result = optimize.minimize(
                self._nls_objective,
                x0,
                args=(y, x_mat, s),
                method="Nelder-Mead",
                options={"maxiter": 5000, "xatol": 1e-6, "fatol": 1e-6},
            )
            best_gamma = min(np.exp(result.x[0]), 500.0)
            best_c = result.x[1]
        else:
            best_gamma = gamma_init
            best_c = c_init

        # Final estimation with best (gamma, c)
        beta, resid, rss = self._concentrated_ols(best_gamma, best_c, y, x_mat, s)
        g = logistic_transition(s, best_gamma, best_c)

        k = self.order + 1
        beta1 = beta[:k]
        beta2 = beta[k:]

        t_eff = len(y)
        sigma2 = rss / t_eff

        # Log-likelihood (assuming normal errors)
        ll = -0.5 * t_eff * (np.log(2 * np.pi) + np.log(max(sigma2, 1e-12))) - rss / (
            2 * max(sigma2, 1e-12)
        )

        # Number of parameters: 2*(p+1) AR + gamma + c
        n_params = 2 * (self.order + 1) + 2
        aic = -2 * ll + 2 * n_params
        bic = -2 * ll + np.log(t_eff) * n_params

        # Variance per regime (approximate)
        mask_r1 = g < 0.5
        mask_r2 = g >= 0.5
        sigma2_1 = float(np.mean(resid[mask_r1] ** 2)) if mask_r1.sum() > 0 else sigma2
        sigma2_2 = float(np.mean(resid[mask_r2] ** 2)) if mask_r2.sum() > 0 else sigma2

        return ThresholdResults(
            model_name=self.model_name,
            params={"regime_1": beta1, "regime_2": beta2},
            threshold=best_c,
            delay=self.delay,
            transition_params={"gamma": best_gamma, "c": best_c},
            transition_params_array=np.array([best_gamma, best_c]),
            params_regime1=beta1,
            params_regime2=beta2,
            regime_assignments=g,
            transition_values=g,
            resid=resid,
            sigma2={"regime_1": sigma2_1, "REGIME_2": sigma2_2},
            loglike=ll,
            aic=aic,
            bic=bic,
            nobs=t_eff,
            order=self.order,
            n_regimes=self.n_regimes,
            endog=self.endog,
            _model=self,
        )

    xǁLSTARǁ_fit_cls__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁLSTARǁ_fit_cls__mutmut_1": xǁLSTARǁ_fit_cls__mutmut_1,
        "xǁLSTARǁ_fit_cls__mutmut_2": xǁLSTARǁ_fit_cls__mutmut_2,
        "xǁLSTARǁ_fit_cls__mutmut_3": xǁLSTARǁ_fit_cls__mutmut_3,
        "xǁLSTARǁ_fit_cls__mutmut_4": xǁLSTARǁ_fit_cls__mutmut_4,
        "xǁLSTARǁ_fit_cls__mutmut_5": xǁLSTARǁ_fit_cls__mutmut_5,
        "xǁLSTARǁ_fit_cls__mutmut_6": xǁLSTARǁ_fit_cls__mutmut_6,
        "xǁLSTARǁ_fit_cls__mutmut_7": xǁLSTARǁ_fit_cls__mutmut_7,
        "xǁLSTARǁ_fit_cls__mutmut_8": xǁLSTARǁ_fit_cls__mutmut_8,
        "xǁLSTARǁ_fit_cls__mutmut_9": xǁLSTARǁ_fit_cls__mutmut_9,
        "xǁLSTARǁ_fit_cls__mutmut_10": xǁLSTARǁ_fit_cls__mutmut_10,
        "xǁLSTARǁ_fit_cls__mutmut_11": xǁLSTARǁ_fit_cls__mutmut_11,
        "xǁLSTARǁ_fit_cls__mutmut_12": xǁLSTARǁ_fit_cls__mutmut_12,
        "xǁLSTARǁ_fit_cls__mutmut_13": xǁLSTARǁ_fit_cls__mutmut_13,
        "xǁLSTARǁ_fit_cls__mutmut_14": xǁLSTARǁ_fit_cls__mutmut_14,
        "xǁLSTARǁ_fit_cls__mutmut_15": xǁLSTARǁ_fit_cls__mutmut_15,
        "xǁLSTARǁ_fit_cls__mutmut_16": xǁLSTARǁ_fit_cls__mutmut_16,
        "xǁLSTARǁ_fit_cls__mutmut_17": xǁLSTARǁ_fit_cls__mutmut_17,
        "xǁLSTARǁ_fit_cls__mutmut_18": xǁLSTARǁ_fit_cls__mutmut_18,
        "xǁLSTARǁ_fit_cls__mutmut_19": xǁLSTARǁ_fit_cls__mutmut_19,
        "xǁLSTARǁ_fit_cls__mutmut_20": xǁLSTARǁ_fit_cls__mutmut_20,
        "xǁLSTARǁ_fit_cls__mutmut_21": xǁLSTARǁ_fit_cls__mutmut_21,
        "xǁLSTARǁ_fit_cls__mutmut_22": xǁLSTARǁ_fit_cls__mutmut_22,
        "xǁLSTARǁ_fit_cls__mutmut_23": xǁLSTARǁ_fit_cls__mutmut_23,
        "xǁLSTARǁ_fit_cls__mutmut_24": xǁLSTARǁ_fit_cls__mutmut_24,
        "xǁLSTARǁ_fit_cls__mutmut_25": xǁLSTARǁ_fit_cls__mutmut_25,
        "xǁLSTARǁ_fit_cls__mutmut_26": xǁLSTARǁ_fit_cls__mutmut_26,
        "xǁLSTARǁ_fit_cls__mutmut_27": xǁLSTARǁ_fit_cls__mutmut_27,
        "xǁLSTARǁ_fit_cls__mutmut_28": xǁLSTARǁ_fit_cls__mutmut_28,
        "xǁLSTARǁ_fit_cls__mutmut_29": xǁLSTARǁ_fit_cls__mutmut_29,
        "xǁLSTARǁ_fit_cls__mutmut_30": xǁLSTARǁ_fit_cls__mutmut_30,
        "xǁLSTARǁ_fit_cls__mutmut_31": xǁLSTARǁ_fit_cls__mutmut_31,
        "xǁLSTARǁ_fit_cls__mutmut_32": xǁLSTARǁ_fit_cls__mutmut_32,
        "xǁLSTARǁ_fit_cls__mutmut_33": xǁLSTARǁ_fit_cls__mutmut_33,
        "xǁLSTARǁ_fit_cls__mutmut_34": xǁLSTARǁ_fit_cls__mutmut_34,
        "xǁLSTARǁ_fit_cls__mutmut_35": xǁLSTARǁ_fit_cls__mutmut_35,
        "xǁLSTARǁ_fit_cls__mutmut_36": xǁLSTARǁ_fit_cls__mutmut_36,
        "xǁLSTARǁ_fit_cls__mutmut_37": xǁLSTARǁ_fit_cls__mutmut_37,
        "xǁLSTARǁ_fit_cls__mutmut_38": xǁLSTARǁ_fit_cls__mutmut_38,
        "xǁLSTARǁ_fit_cls__mutmut_39": xǁLSTARǁ_fit_cls__mutmut_39,
        "xǁLSTARǁ_fit_cls__mutmut_40": xǁLSTARǁ_fit_cls__mutmut_40,
        "xǁLSTARǁ_fit_cls__mutmut_41": xǁLSTARǁ_fit_cls__mutmut_41,
        "xǁLSTARǁ_fit_cls__mutmut_42": xǁLSTARǁ_fit_cls__mutmut_42,
        "xǁLSTARǁ_fit_cls__mutmut_43": xǁLSTARǁ_fit_cls__mutmut_43,
        "xǁLSTARǁ_fit_cls__mutmut_44": xǁLSTARǁ_fit_cls__mutmut_44,
        "xǁLSTARǁ_fit_cls__mutmut_45": xǁLSTARǁ_fit_cls__mutmut_45,
        "xǁLSTARǁ_fit_cls__mutmut_46": xǁLSTARǁ_fit_cls__mutmut_46,
        "xǁLSTARǁ_fit_cls__mutmut_47": xǁLSTARǁ_fit_cls__mutmut_47,
        "xǁLSTARǁ_fit_cls__mutmut_48": xǁLSTARǁ_fit_cls__mutmut_48,
        "xǁLSTARǁ_fit_cls__mutmut_49": xǁLSTARǁ_fit_cls__mutmut_49,
        "xǁLSTARǁ_fit_cls__mutmut_50": xǁLSTARǁ_fit_cls__mutmut_50,
        "xǁLSTARǁ_fit_cls__mutmut_51": xǁLSTARǁ_fit_cls__mutmut_51,
        "xǁLSTARǁ_fit_cls__mutmut_52": xǁLSTARǁ_fit_cls__mutmut_52,
        "xǁLSTARǁ_fit_cls__mutmut_53": xǁLSTARǁ_fit_cls__mutmut_53,
        "xǁLSTARǁ_fit_cls__mutmut_54": xǁLSTARǁ_fit_cls__mutmut_54,
        "xǁLSTARǁ_fit_cls__mutmut_55": xǁLSTARǁ_fit_cls__mutmut_55,
        "xǁLSTARǁ_fit_cls__mutmut_56": xǁLSTARǁ_fit_cls__mutmut_56,
        "xǁLSTARǁ_fit_cls__mutmut_57": xǁLSTARǁ_fit_cls__mutmut_57,
        "xǁLSTARǁ_fit_cls__mutmut_58": xǁLSTARǁ_fit_cls__mutmut_58,
        "xǁLSTARǁ_fit_cls__mutmut_59": xǁLSTARǁ_fit_cls__mutmut_59,
        "xǁLSTARǁ_fit_cls__mutmut_60": xǁLSTARǁ_fit_cls__mutmut_60,
        "xǁLSTARǁ_fit_cls__mutmut_61": xǁLSTARǁ_fit_cls__mutmut_61,
        "xǁLSTARǁ_fit_cls__mutmut_62": xǁLSTARǁ_fit_cls__mutmut_62,
        "xǁLSTARǁ_fit_cls__mutmut_63": xǁLSTARǁ_fit_cls__mutmut_63,
        "xǁLSTARǁ_fit_cls__mutmut_64": xǁLSTARǁ_fit_cls__mutmut_64,
        "xǁLSTARǁ_fit_cls__mutmut_65": xǁLSTARǁ_fit_cls__mutmut_65,
        "xǁLSTARǁ_fit_cls__mutmut_66": xǁLSTARǁ_fit_cls__mutmut_66,
        "xǁLSTARǁ_fit_cls__mutmut_67": xǁLSTARǁ_fit_cls__mutmut_67,
        "xǁLSTARǁ_fit_cls__mutmut_68": xǁLSTARǁ_fit_cls__mutmut_68,
        "xǁLSTARǁ_fit_cls__mutmut_69": xǁLSTARǁ_fit_cls__mutmut_69,
        "xǁLSTARǁ_fit_cls__mutmut_70": xǁLSTARǁ_fit_cls__mutmut_70,
        "xǁLSTARǁ_fit_cls__mutmut_71": xǁLSTARǁ_fit_cls__mutmut_71,
        "xǁLSTARǁ_fit_cls__mutmut_72": xǁLSTARǁ_fit_cls__mutmut_72,
        "xǁLSTARǁ_fit_cls__mutmut_73": xǁLSTARǁ_fit_cls__mutmut_73,
        "xǁLSTARǁ_fit_cls__mutmut_74": xǁLSTARǁ_fit_cls__mutmut_74,
        "xǁLSTARǁ_fit_cls__mutmut_75": xǁLSTARǁ_fit_cls__mutmut_75,
        "xǁLSTARǁ_fit_cls__mutmut_76": xǁLSTARǁ_fit_cls__mutmut_76,
        "xǁLSTARǁ_fit_cls__mutmut_77": xǁLSTARǁ_fit_cls__mutmut_77,
        "xǁLSTARǁ_fit_cls__mutmut_78": xǁLSTARǁ_fit_cls__mutmut_78,
        "xǁLSTARǁ_fit_cls__mutmut_79": xǁLSTARǁ_fit_cls__mutmut_79,
        "xǁLSTARǁ_fit_cls__mutmut_80": xǁLSTARǁ_fit_cls__mutmut_80,
        "xǁLSTARǁ_fit_cls__mutmut_81": xǁLSTARǁ_fit_cls__mutmut_81,
        "xǁLSTARǁ_fit_cls__mutmut_82": xǁLSTARǁ_fit_cls__mutmut_82,
        "xǁLSTARǁ_fit_cls__mutmut_83": xǁLSTARǁ_fit_cls__mutmut_83,
        "xǁLSTARǁ_fit_cls__mutmut_84": xǁLSTARǁ_fit_cls__mutmut_84,
        "xǁLSTARǁ_fit_cls__mutmut_85": xǁLSTARǁ_fit_cls__mutmut_85,
        "xǁLSTARǁ_fit_cls__mutmut_86": xǁLSTARǁ_fit_cls__mutmut_86,
        "xǁLSTARǁ_fit_cls__mutmut_87": xǁLSTARǁ_fit_cls__mutmut_87,
        "xǁLSTARǁ_fit_cls__mutmut_88": xǁLSTARǁ_fit_cls__mutmut_88,
        "xǁLSTARǁ_fit_cls__mutmut_89": xǁLSTARǁ_fit_cls__mutmut_89,
        "xǁLSTARǁ_fit_cls__mutmut_90": xǁLSTARǁ_fit_cls__mutmut_90,
        "xǁLSTARǁ_fit_cls__mutmut_91": xǁLSTARǁ_fit_cls__mutmut_91,
        "xǁLSTARǁ_fit_cls__mutmut_92": xǁLSTARǁ_fit_cls__mutmut_92,
        "xǁLSTARǁ_fit_cls__mutmut_93": xǁLSTARǁ_fit_cls__mutmut_93,
        "xǁLSTARǁ_fit_cls__mutmut_94": xǁLSTARǁ_fit_cls__mutmut_94,
        "xǁLSTARǁ_fit_cls__mutmut_95": xǁLSTARǁ_fit_cls__mutmut_95,
        "xǁLSTARǁ_fit_cls__mutmut_96": xǁLSTARǁ_fit_cls__mutmut_96,
        "xǁLSTARǁ_fit_cls__mutmut_97": xǁLSTARǁ_fit_cls__mutmut_97,
        "xǁLSTARǁ_fit_cls__mutmut_98": xǁLSTARǁ_fit_cls__mutmut_98,
        "xǁLSTARǁ_fit_cls__mutmut_99": xǁLSTARǁ_fit_cls__mutmut_99,
        "xǁLSTARǁ_fit_cls__mutmut_100": xǁLSTARǁ_fit_cls__mutmut_100,
        "xǁLSTARǁ_fit_cls__mutmut_101": xǁLSTARǁ_fit_cls__mutmut_101,
        "xǁLSTARǁ_fit_cls__mutmut_102": xǁLSTARǁ_fit_cls__mutmut_102,
        "xǁLSTARǁ_fit_cls__mutmut_103": xǁLSTARǁ_fit_cls__mutmut_103,
        "xǁLSTARǁ_fit_cls__mutmut_104": xǁLSTARǁ_fit_cls__mutmut_104,
        "xǁLSTARǁ_fit_cls__mutmut_105": xǁLSTARǁ_fit_cls__mutmut_105,
        "xǁLSTARǁ_fit_cls__mutmut_106": xǁLSTARǁ_fit_cls__mutmut_106,
        "xǁLSTARǁ_fit_cls__mutmut_107": xǁLSTARǁ_fit_cls__mutmut_107,
        "xǁLSTARǁ_fit_cls__mutmut_108": xǁLSTARǁ_fit_cls__mutmut_108,
        "xǁLSTARǁ_fit_cls__mutmut_109": xǁLSTARǁ_fit_cls__mutmut_109,
        "xǁLSTARǁ_fit_cls__mutmut_110": xǁLSTARǁ_fit_cls__mutmut_110,
        "xǁLSTARǁ_fit_cls__mutmut_111": xǁLSTARǁ_fit_cls__mutmut_111,
        "xǁLSTARǁ_fit_cls__mutmut_112": xǁLSTARǁ_fit_cls__mutmut_112,
        "xǁLSTARǁ_fit_cls__mutmut_113": xǁLSTARǁ_fit_cls__mutmut_113,
        "xǁLSTARǁ_fit_cls__mutmut_114": xǁLSTARǁ_fit_cls__mutmut_114,
        "xǁLSTARǁ_fit_cls__mutmut_115": xǁLSTARǁ_fit_cls__mutmut_115,
        "xǁLSTARǁ_fit_cls__mutmut_116": xǁLSTARǁ_fit_cls__mutmut_116,
        "xǁLSTARǁ_fit_cls__mutmut_117": xǁLSTARǁ_fit_cls__mutmut_117,
        "xǁLSTARǁ_fit_cls__mutmut_118": xǁLSTARǁ_fit_cls__mutmut_118,
        "xǁLSTARǁ_fit_cls__mutmut_119": xǁLSTARǁ_fit_cls__mutmut_119,
        "xǁLSTARǁ_fit_cls__mutmut_120": xǁLSTARǁ_fit_cls__mutmut_120,
        "xǁLSTARǁ_fit_cls__mutmut_121": xǁLSTARǁ_fit_cls__mutmut_121,
        "xǁLSTARǁ_fit_cls__mutmut_122": xǁLSTARǁ_fit_cls__mutmut_122,
        "xǁLSTARǁ_fit_cls__mutmut_123": xǁLSTARǁ_fit_cls__mutmut_123,
        "xǁLSTARǁ_fit_cls__mutmut_124": xǁLSTARǁ_fit_cls__mutmut_124,
        "xǁLSTARǁ_fit_cls__mutmut_125": xǁLSTARǁ_fit_cls__mutmut_125,
        "xǁLSTARǁ_fit_cls__mutmut_126": xǁLSTARǁ_fit_cls__mutmut_126,
        "xǁLSTARǁ_fit_cls__mutmut_127": xǁLSTARǁ_fit_cls__mutmut_127,
        "xǁLSTARǁ_fit_cls__mutmut_128": xǁLSTARǁ_fit_cls__mutmut_128,
        "xǁLSTARǁ_fit_cls__mutmut_129": xǁLSTARǁ_fit_cls__mutmut_129,
        "xǁLSTARǁ_fit_cls__mutmut_130": xǁLSTARǁ_fit_cls__mutmut_130,
        "xǁLSTARǁ_fit_cls__mutmut_131": xǁLSTARǁ_fit_cls__mutmut_131,
        "xǁLSTARǁ_fit_cls__mutmut_132": xǁLSTARǁ_fit_cls__mutmut_132,
        "xǁLSTARǁ_fit_cls__mutmut_133": xǁLSTARǁ_fit_cls__mutmut_133,
        "xǁLSTARǁ_fit_cls__mutmut_134": xǁLSTARǁ_fit_cls__mutmut_134,
        "xǁLSTARǁ_fit_cls__mutmut_135": xǁLSTARǁ_fit_cls__mutmut_135,
        "xǁLSTARǁ_fit_cls__mutmut_136": xǁLSTARǁ_fit_cls__mutmut_136,
        "xǁLSTARǁ_fit_cls__mutmut_137": xǁLSTARǁ_fit_cls__mutmut_137,
        "xǁLSTARǁ_fit_cls__mutmut_138": xǁLSTARǁ_fit_cls__mutmut_138,
        "xǁLSTARǁ_fit_cls__mutmut_139": xǁLSTARǁ_fit_cls__mutmut_139,
        "xǁLSTARǁ_fit_cls__mutmut_140": xǁLSTARǁ_fit_cls__mutmut_140,
        "xǁLSTARǁ_fit_cls__mutmut_141": xǁLSTARǁ_fit_cls__mutmut_141,
        "xǁLSTARǁ_fit_cls__mutmut_142": xǁLSTARǁ_fit_cls__mutmut_142,
        "xǁLSTARǁ_fit_cls__mutmut_143": xǁLSTARǁ_fit_cls__mutmut_143,
        "xǁLSTARǁ_fit_cls__mutmut_144": xǁLSTARǁ_fit_cls__mutmut_144,
        "xǁLSTARǁ_fit_cls__mutmut_145": xǁLSTARǁ_fit_cls__mutmut_145,
        "xǁLSTARǁ_fit_cls__mutmut_146": xǁLSTARǁ_fit_cls__mutmut_146,
        "xǁLSTARǁ_fit_cls__mutmut_147": xǁLSTARǁ_fit_cls__mutmut_147,
        "xǁLSTARǁ_fit_cls__mutmut_148": xǁLSTARǁ_fit_cls__mutmut_148,
        "xǁLSTARǁ_fit_cls__mutmut_149": xǁLSTARǁ_fit_cls__mutmut_149,
        "xǁLSTARǁ_fit_cls__mutmut_150": xǁLSTARǁ_fit_cls__mutmut_150,
        "xǁLSTARǁ_fit_cls__mutmut_151": xǁLSTARǁ_fit_cls__mutmut_151,
        "xǁLSTARǁ_fit_cls__mutmut_152": xǁLSTARǁ_fit_cls__mutmut_152,
        "xǁLSTARǁ_fit_cls__mutmut_153": xǁLSTARǁ_fit_cls__mutmut_153,
        "xǁLSTARǁ_fit_cls__mutmut_154": xǁLSTARǁ_fit_cls__mutmut_154,
        "xǁLSTARǁ_fit_cls__mutmut_155": xǁLSTARǁ_fit_cls__mutmut_155,
        "xǁLSTARǁ_fit_cls__mutmut_156": xǁLSTARǁ_fit_cls__mutmut_156,
        "xǁLSTARǁ_fit_cls__mutmut_157": xǁLSTARǁ_fit_cls__mutmut_157,
        "xǁLSTARǁ_fit_cls__mutmut_158": xǁLSTARǁ_fit_cls__mutmut_158,
        "xǁLSTARǁ_fit_cls__mutmut_159": xǁLSTARǁ_fit_cls__mutmut_159,
        "xǁLSTARǁ_fit_cls__mutmut_160": xǁLSTARǁ_fit_cls__mutmut_160,
        "xǁLSTARǁ_fit_cls__mutmut_161": xǁLSTARǁ_fit_cls__mutmut_161,
        "xǁLSTARǁ_fit_cls__mutmut_162": xǁLSTARǁ_fit_cls__mutmut_162,
        "xǁLSTARǁ_fit_cls__mutmut_163": xǁLSTARǁ_fit_cls__mutmut_163,
        "xǁLSTARǁ_fit_cls__mutmut_164": xǁLSTARǁ_fit_cls__mutmut_164,
        "xǁLSTARǁ_fit_cls__mutmut_165": xǁLSTARǁ_fit_cls__mutmut_165,
        "xǁLSTARǁ_fit_cls__mutmut_166": xǁLSTARǁ_fit_cls__mutmut_166,
        "xǁLSTARǁ_fit_cls__mutmut_167": xǁLSTARǁ_fit_cls__mutmut_167,
        "xǁLSTARǁ_fit_cls__mutmut_168": xǁLSTARǁ_fit_cls__mutmut_168,
        "xǁLSTARǁ_fit_cls__mutmut_169": xǁLSTARǁ_fit_cls__mutmut_169,
        "xǁLSTARǁ_fit_cls__mutmut_170": xǁLSTARǁ_fit_cls__mutmut_170,
        "xǁLSTARǁ_fit_cls__mutmut_171": xǁLSTARǁ_fit_cls__mutmut_171,
        "xǁLSTARǁ_fit_cls__mutmut_172": xǁLSTARǁ_fit_cls__mutmut_172,
        "xǁLSTARǁ_fit_cls__mutmut_173": xǁLSTARǁ_fit_cls__mutmut_173,
        "xǁLSTARǁ_fit_cls__mutmut_174": xǁLSTARǁ_fit_cls__mutmut_174,
        "xǁLSTARǁ_fit_cls__mutmut_175": xǁLSTARǁ_fit_cls__mutmut_175,
        "xǁLSTARǁ_fit_cls__mutmut_176": xǁLSTARǁ_fit_cls__mutmut_176,
        "xǁLSTARǁ_fit_cls__mutmut_177": xǁLSTARǁ_fit_cls__mutmut_177,
        "xǁLSTARǁ_fit_cls__mutmut_178": xǁLSTARǁ_fit_cls__mutmut_178,
        "xǁLSTARǁ_fit_cls__mutmut_179": xǁLSTARǁ_fit_cls__mutmut_179,
        "xǁLSTARǁ_fit_cls__mutmut_180": xǁLSTARǁ_fit_cls__mutmut_180,
        "xǁLSTARǁ_fit_cls__mutmut_181": xǁLSTARǁ_fit_cls__mutmut_181,
        "xǁLSTARǁ_fit_cls__mutmut_182": xǁLSTARǁ_fit_cls__mutmut_182,
        "xǁLSTARǁ_fit_cls__mutmut_183": xǁLSTARǁ_fit_cls__mutmut_183,
        "xǁLSTARǁ_fit_cls__mutmut_184": xǁLSTARǁ_fit_cls__mutmut_184,
        "xǁLSTARǁ_fit_cls__mutmut_185": xǁLSTARǁ_fit_cls__mutmut_185,
        "xǁLSTARǁ_fit_cls__mutmut_186": xǁLSTARǁ_fit_cls__mutmut_186,
        "xǁLSTARǁ_fit_cls__mutmut_187": xǁLSTARǁ_fit_cls__mutmut_187,
        "xǁLSTARǁ_fit_cls__mutmut_188": xǁLSTARǁ_fit_cls__mutmut_188,
        "xǁLSTARǁ_fit_cls__mutmut_189": xǁLSTARǁ_fit_cls__mutmut_189,
        "xǁLSTARǁ_fit_cls__mutmut_190": xǁLSTARǁ_fit_cls__mutmut_190,
        "xǁLSTARǁ_fit_cls__mutmut_191": xǁLSTARǁ_fit_cls__mutmut_191,
        "xǁLSTARǁ_fit_cls__mutmut_192": xǁLSTARǁ_fit_cls__mutmut_192,
        "xǁLSTARǁ_fit_cls__mutmut_193": xǁLSTARǁ_fit_cls__mutmut_193,
        "xǁLSTARǁ_fit_cls__mutmut_194": xǁLSTARǁ_fit_cls__mutmut_194,
        "xǁLSTARǁ_fit_cls__mutmut_195": xǁLSTARǁ_fit_cls__mutmut_195,
        "xǁLSTARǁ_fit_cls__mutmut_196": xǁLSTARǁ_fit_cls__mutmut_196,
        "xǁLSTARǁ_fit_cls__mutmut_197": xǁLSTARǁ_fit_cls__mutmut_197,
    }
    xǁLSTARǁ_fit_cls__mutmut_orig.__name__ = "xǁLSTARǁ_fit_cls"
