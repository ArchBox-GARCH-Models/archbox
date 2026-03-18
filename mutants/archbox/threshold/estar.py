"""ESTAR - Exponential Smooth Transition Autoregressive Model (Terasvirta, 1994).

The ESTAR model uses an exponential transition function for symmetric
smooth regime switching:

    y_t = phi^{(1)}'x_t * (1 - G(s_t; gamma, c))
        + phi^{(2)}'x_t * G(s_t; gamma, c)
        + eps_t

    G(s_t; gamma, c) = 1 - exp(-gamma * (s_t - c)^2)

Key difference from LSTAR:
- LSTAR: asymmetric (regime depends on direction of shock)
- ESTAR: symmetric (regime depends on magnitude of shock)

Properties:
- Symmetric around c: G(c - delta) == G(c + delta)
- gamma -> 0: linear model (G -> 0)
- gamma -> inf: G -> 1 except at s_t = c exactly

References
----------
- Terasvirta, T. (1994). Specification, Estimation, and Evaluation of
  Smooth Transition Autoregressive Models. JASA, 89(425), 208-218.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Annotated, Any, ClassVar

import numpy as np
from numpy.typing import NDArray
from scipy import optimize

from archbox.threshold.base import ThresholdModel
from archbox.threshold.results import ThresholdResults
from archbox.threshold.transition import exponential_transition

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


class ESTAR(ThresholdModel):
    """Exponential Smooth Transition Autoregressive model (Terasvirta, 1994).

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
    >>> from archbox.threshold.estar import ESTAR
    >>> rng = np.random.default_rng(42)
    >>> n = 1000
    >>> y = np.zeros(n)
    >>> gamma_true, c_true = 3.0, 0.0
    >>> for t in range(1, n):
    ...     s = y[t-1]
    ...     G = 1 - np.exp(-gamma_true * (s - c_true)**2)
    ...     y[t] = (0.5 + 0.3 * y[t-1]) * (1 - G) + (-0.2 + 0.8 * y[t-1]) * G
    ...     y[t] += rng.standard_normal() * 0.5
    >>> model = ESTAR(y, order=1, delay=1)
    >>> results = model.fit()
    """

    model_name: str = "ESTAR"

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
            object.__getattribute__(self, "xǁESTARǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁESTARǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁESTARǁ__init____mutmut_orig(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        """Initialize ESTAR model with grid search configuration."""
        super().__init__(endog, order=order, delay=delay, n_regimes=2)
        self.gamma_grid = gamma_grid
        self.c_grid = c_grid
        self.refine = refine

    def xǁESTARǁ__init____mutmut_1(
        self,
        endog: Any,
        order: int = 2,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        """Initialize ESTAR model with grid search configuration."""
        super().__init__(endog, order=order, delay=delay, n_regimes=2)
        self.gamma_grid = gamma_grid
        self.c_grid = c_grid
        self.refine = refine

    def xǁESTARǁ__init____mutmut_2(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 2,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        """Initialize ESTAR model with grid search configuration."""
        super().__init__(endog, order=order, delay=delay, n_regimes=2)
        self.gamma_grid = gamma_grid
        self.c_grid = c_grid
        self.refine = refine

    def xǁESTARǁ__init____mutmut_3(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 51,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        """Initialize ESTAR model with grid search configuration."""
        super().__init__(endog, order=order, delay=delay, n_regimes=2)
        self.gamma_grid = gamma_grid
        self.c_grid = c_grid
        self.refine = refine

    def xǁESTARǁ__init____mutmut_4(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 51,
        refine: bool = True,
    ) -> None:
        """Initialize ESTAR model with grid search configuration."""
        super().__init__(endog, order=order, delay=delay, n_regimes=2)
        self.gamma_grid = gamma_grid
        self.c_grid = c_grid
        self.refine = refine

    def xǁESTARǁ__init____mutmut_5(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = False,
    ) -> None:
        """Initialize ESTAR model with grid search configuration."""
        super().__init__(endog, order=order, delay=delay, n_regimes=2)
        self.gamma_grid = gamma_grid
        self.c_grid = c_grid
        self.refine = refine

    def xǁESTARǁ__init____mutmut_6(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        """Initialize ESTAR model with grid search configuration."""
        super().__init__(None, order=order, delay=delay, n_regimes=2)
        self.gamma_grid = gamma_grid
        self.c_grid = c_grid
        self.refine = refine

    def xǁESTARǁ__init____mutmut_7(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        """Initialize ESTAR model with grid search configuration."""
        super().__init__(endog, order=None, delay=delay, n_regimes=2)
        self.gamma_grid = gamma_grid
        self.c_grid = c_grid
        self.refine = refine

    def xǁESTARǁ__init____mutmut_8(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        """Initialize ESTAR model with grid search configuration."""
        super().__init__(endog, order=order, delay=None, n_regimes=2)
        self.gamma_grid = gamma_grid
        self.c_grid = c_grid
        self.refine = refine

    def xǁESTARǁ__init____mutmut_9(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        """Initialize ESTAR model with grid search configuration."""
        super().__init__(endog, order=order, delay=delay, n_regimes=None)
        self.gamma_grid = gamma_grid
        self.c_grid = c_grid
        self.refine = refine

    def xǁESTARǁ__init____mutmut_10(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        """Initialize ESTAR model with grid search configuration."""
        super().__init__(order=order, delay=delay, n_regimes=2)
        self.gamma_grid = gamma_grid
        self.c_grid = c_grid
        self.refine = refine

    def xǁESTARǁ__init____mutmut_11(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        """Initialize ESTAR model with grid search configuration."""
        super().__init__(endog, delay=delay, n_regimes=2)
        self.gamma_grid = gamma_grid
        self.c_grid = c_grid
        self.refine = refine

    def xǁESTARǁ__init____mutmut_12(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        """Initialize ESTAR model with grid search configuration."""
        super().__init__(endog, order=order, n_regimes=2)
        self.gamma_grid = gamma_grid
        self.c_grid = c_grid
        self.refine = refine

    def xǁESTARǁ__init____mutmut_13(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        """Initialize ESTAR model with grid search configuration."""
        super().__init__(
            endog,
            order=order,
            delay=delay,
        )
        self.gamma_grid = gamma_grid
        self.c_grid = c_grid
        self.refine = refine

    def xǁESTARǁ__init____mutmut_14(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        """Initialize ESTAR model with grid search configuration."""
        super().__init__(endog, order=order, delay=delay, n_regimes=3)
        self.gamma_grid = gamma_grid
        self.c_grid = c_grid
        self.refine = refine

    def xǁESTARǁ__init____mutmut_15(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        """Initialize ESTAR model with grid search configuration."""
        super().__init__(endog, order=order, delay=delay, n_regimes=2)
        self.gamma_grid = None
        self.c_grid = c_grid
        self.refine = refine

    def xǁESTARǁ__init____mutmut_16(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        """Initialize ESTAR model with grid search configuration."""
        super().__init__(endog, order=order, delay=delay, n_regimes=2)
        self.gamma_grid = gamma_grid
        self.c_grid = None
        self.refine = refine

    def xǁESTARǁ__init____mutmut_17(
        self,
        endog: Any,
        order: int = 1,
        delay: int = 1,
        gamma_grid: int = 50,
        c_grid: int = 50,
        refine: bool = True,
    ) -> None:
        """Initialize ESTAR model with grid search configuration."""
        super().__init__(endog, order=order, delay=delay, n_regimes=2)
        self.gamma_grid = gamma_grid
        self.c_grid = c_grid
        self.refine = None

    xǁESTARǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁESTARǁ__init____mutmut_1": xǁESTARǁ__init____mutmut_1,
        "xǁESTARǁ__init____mutmut_2": xǁESTARǁ__init____mutmut_2,
        "xǁESTARǁ__init____mutmut_3": xǁESTARǁ__init____mutmut_3,
        "xǁESTARǁ__init____mutmut_4": xǁESTARǁ__init____mutmut_4,
        "xǁESTARǁ__init____mutmut_5": xǁESTARǁ__init____mutmut_5,
        "xǁESTARǁ__init____mutmut_6": xǁESTARǁ__init____mutmut_6,
        "xǁESTARǁ__init____mutmut_7": xǁESTARǁ__init____mutmut_7,
        "xǁESTARǁ__init____mutmut_8": xǁESTARǁ__init____mutmut_8,
        "xǁESTARǁ__init____mutmut_9": xǁESTARǁ__init____mutmut_9,
        "xǁESTARǁ__init____mutmut_10": xǁESTARǁ__init____mutmut_10,
        "xǁESTARǁ__init____mutmut_11": xǁESTARǁ__init____mutmut_11,
        "xǁESTARǁ__init____mutmut_12": xǁESTARǁ__init____mutmut_12,
        "xǁESTARǁ__init____mutmut_13": xǁESTARǁ__init____mutmut_13,
        "xǁESTARǁ__init____mutmut_14": xǁESTARǁ__init____mutmut_14,
        "xǁESTARǁ__init____mutmut_15": xǁESTARǁ__init____mutmut_15,
        "xǁESTARǁ__init____mutmut_16": xǁESTARǁ__init____mutmut_16,
        "xǁESTARǁ__init____mutmut_17": xǁESTARǁ__init____mutmut_17,
    }
    xǁESTARǁ__init____mutmut_orig.__name__ = "xǁESTARǁ__init__"

    def _transition_function(
        self, s: NDArray[np.float64], params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        args = [s, params]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁESTARǁ_transition_function__mutmut_orig"),
            object.__getattribute__(self, "xǁESTARǁ_transition_function__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁESTARǁ_transition_function__mutmut_orig(
        self, s: NDArray[np.float64], params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Exponential transition: G(s; gamma, c) = 1 - exp(-gamma*(s-c)^2).

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
        return exponential_transition(s, gamma, c)

    def xǁESTARǁ_transition_function__mutmut_1(
        self, s: NDArray[np.float64], params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Exponential transition: G(s; gamma, c) = 1 - exp(-gamma*(s-c)^2).

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
        return exponential_transition(s, gamma, c)

    def xǁESTARǁ_transition_function__mutmut_2(
        self, s: NDArray[np.float64], params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Exponential transition: G(s; gamma, c) = 1 - exp(-gamma*(s-c)^2).

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
        return exponential_transition(s, gamma, c)

    def xǁESTARǁ_transition_function__mutmut_3(
        self, s: NDArray[np.float64], params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Exponential transition: G(s; gamma, c) = 1 - exp(-gamma*(s-c)^2).

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
        return exponential_transition(s, gamma, c)

    def xǁESTARǁ_transition_function__mutmut_4(
        self, s: NDArray[np.float64], params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Exponential transition: G(s; gamma, c) = 1 - exp(-gamma*(s-c)^2).

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
        return exponential_transition(None, gamma, c)

    def xǁESTARǁ_transition_function__mutmut_5(
        self, s: NDArray[np.float64], params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Exponential transition: G(s; gamma, c) = 1 - exp(-gamma*(s-c)^2).

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
        return exponential_transition(s, None, c)

    def xǁESTARǁ_transition_function__mutmut_6(
        self, s: NDArray[np.float64], params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Exponential transition: G(s; gamma, c) = 1 - exp(-gamma*(s-c)^2).

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
        return exponential_transition(s, gamma, None)

    def xǁESTARǁ_transition_function__mutmut_7(
        self, s: NDArray[np.float64], params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Exponential transition: G(s; gamma, c) = 1 - exp(-gamma*(s-c)^2).

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
        return exponential_transition(gamma, c)

    def xǁESTARǁ_transition_function__mutmut_8(
        self, s: NDArray[np.float64], params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Exponential transition: G(s; gamma, c) = 1 - exp(-gamma*(s-c)^2).

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
        return exponential_transition(s, c)

    def xǁESTARǁ_transition_function__mutmut_9(
        self, s: NDArray[np.float64], params: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Exponential transition: G(s; gamma, c) = 1 - exp(-gamma*(s-c)^2).

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
        return exponential_transition(
            s,
            gamma,
        )

    xǁESTARǁ_transition_function__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁESTARǁ_transition_function__mutmut_1": xǁESTARǁ_transition_function__mutmut_1,
        "xǁESTARǁ_transition_function__mutmut_2": xǁESTARǁ_transition_function__mutmut_2,
        "xǁESTARǁ_transition_function__mutmut_3": xǁESTARǁ_transition_function__mutmut_3,
        "xǁESTARǁ_transition_function__mutmut_4": xǁESTARǁ_transition_function__mutmut_4,
        "xǁESTARǁ_transition_function__mutmut_5": xǁESTARǁ_transition_function__mutmut_5,
        "xǁESTARǁ_transition_function__mutmut_6": xǁESTARǁ_transition_function__mutmut_6,
        "xǁESTARǁ_transition_function__mutmut_7": xǁESTARǁ_transition_function__mutmut_7,
        "xǁESTARǁ_transition_function__mutmut_8": xǁESTARǁ_transition_function__mutmut_8,
        "xǁESTARǁ_transition_function__mutmut_9": xǁESTARǁ_transition_function__mutmut_9,
    }
    xǁESTARǁ_transition_function__mutmut_orig.__name__ = "xǁESTARǁ_transition_function"

    @property
    def start_params(self) -> NDArray[np.float64]:
        """Initial parameters: [gamma=1, c=mean(s)]."""
        return np.array([1.0, np.mean(self._s)])

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
            object.__getattribute__(self, "xǁESTARǁ_concentrated_ols__mutmut_orig"),
            object.__getattribute__(self, "xǁESTARǁ_concentrated_ols__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁESTARǁ_concentrated_ols__mutmut_orig(
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
            Center of symmetry.
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
        g = exponential_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁESTARǁ_concentrated_ols__mutmut_1(
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
            Center of symmetry.
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

    def xǁESTARǁ_concentrated_ols__mutmut_2(
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
            Center of symmetry.
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
        g = exponential_transition(None, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁESTARǁ_concentrated_ols__mutmut_3(
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
            Center of symmetry.
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
        g = exponential_transition(s, None, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁESTARǁ_concentrated_ols__mutmut_4(
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
            Center of symmetry.
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
        g = exponential_transition(s, gamma, None)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁESTARǁ_concentrated_ols__mutmut_5(
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
            Center of symmetry.
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
        g = exponential_transition(gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁESTARǁ_concentrated_ols__mutmut_6(
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
            Center of symmetry.
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
        g = exponential_transition(s, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁESTARǁ_concentrated_ols__mutmut_7(
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
            Center of symmetry.
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
        g = exponential_transition(
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

    def xǁESTARǁ_concentrated_ols__mutmut_8(
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
            Center of symmetry.
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
        g = exponential_transition(s, gamma, c)
        x1 = None
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁESTARǁ_concentrated_ols__mutmut_9(
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
            Center of symmetry.
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
        g = exponential_transition(s, gamma, c)
        x1 = x_mat / (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁESTARǁ_concentrated_ols__mutmut_10(
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
            Center of symmetry.
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
        g = exponential_transition(s, gamma, c)
        x1 = x_mat * (1 + g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁESTARǁ_concentrated_ols__mutmut_11(
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
            Center of symmetry.
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
        g = exponential_transition(s, gamma, c)
        x1 = x_mat * (2 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁESTARǁ_concentrated_ols__mutmut_12(
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
            Center of symmetry.
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
        g = exponential_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = None
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁESTARǁ_concentrated_ols__mutmut_13(
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
            Center of symmetry.
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
        g = exponential_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat / g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁESTARǁ_concentrated_ols__mutmut_14(
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
            Center of symmetry.
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
        g = exponential_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = None

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁESTARǁ_concentrated_ols__mutmut_15(
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
            Center of symmetry.
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
        g = exponential_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack(None)

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁESTARǁ_concentrated_ols__mutmut_16(
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
            Center of symmetry.
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
        g = exponential_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = None
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁESTARǁ_concentrated_ols__mutmut_17(
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
            Center of symmetry.
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
        g = exponential_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(None, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁESTARǁ_concentrated_ols__mutmut_18(
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
            Center of symmetry.
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
        g = exponential_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, None, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁESTARǁ_concentrated_ols__mutmut_19(
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
            Center of symmetry.
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
        g = exponential_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁESTARǁ_concentrated_ols__mutmut_20(
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
            Center of symmetry.
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
        g = exponential_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁESTARǁ_concentrated_ols__mutmut_21(
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
            Center of symmetry.
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
        g = exponential_transition(s, gamma, c)
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

    def xǁESTARǁ_concentrated_ols__mutmut_22(
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
            Center of symmetry.
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
        g = exponential_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[1]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁESTARǁ_concentrated_ols__mutmut_23(
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
            Center of symmetry.
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
        g = exponential_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = None
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁESTARǁ_concentrated_ols__mutmut_24(
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
            Center of symmetry.
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
        g = exponential_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y + x_full @ beta
        rss = float(np.sum(resid**2))
        return beta, resid, rss

    def xǁESTARǁ_concentrated_ols__mutmut_25(
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
            Center of symmetry.
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
        g = exponential_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = None
        return beta, resid, rss

    def xǁESTARǁ_concentrated_ols__mutmut_26(
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
            Center of symmetry.
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
        g = exponential_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(None)
        return beta, resid, rss

    def xǁESTARǁ_concentrated_ols__mutmut_27(
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
            Center of symmetry.
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
        g = exponential_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(None))
        return beta, resid, rss

    def xǁESTARǁ_concentrated_ols__mutmut_28(
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
            Center of symmetry.
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
        g = exponential_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid * 2))
        return beta, resid, rss

    def xǁESTARǁ_concentrated_ols__mutmut_29(
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
            Center of symmetry.
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
        g = exponential_transition(s, gamma, c)
        x1 = x_mat * (1 - g)[:, np.newaxis]
        x2 = x_mat * g[:, np.newaxis]
        x_full = np.hstack([x1, x2])

        beta = np.linalg.lstsq(x_full, y, rcond=None)[0]
        resid = y - x_full @ beta
        rss = float(np.sum(resid**3))
        return beta, resid, rss

    xǁESTARǁ_concentrated_ols__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁESTARǁ_concentrated_ols__mutmut_1": xǁESTARǁ_concentrated_ols__mutmut_1,
        "xǁESTARǁ_concentrated_ols__mutmut_2": xǁESTARǁ_concentrated_ols__mutmut_2,
        "xǁESTARǁ_concentrated_ols__mutmut_3": xǁESTARǁ_concentrated_ols__mutmut_3,
        "xǁESTARǁ_concentrated_ols__mutmut_4": xǁESTARǁ_concentrated_ols__mutmut_4,
        "xǁESTARǁ_concentrated_ols__mutmut_5": xǁESTARǁ_concentrated_ols__mutmut_5,
        "xǁESTARǁ_concentrated_ols__mutmut_6": xǁESTARǁ_concentrated_ols__mutmut_6,
        "xǁESTARǁ_concentrated_ols__mutmut_7": xǁESTARǁ_concentrated_ols__mutmut_7,
        "xǁESTARǁ_concentrated_ols__mutmut_8": xǁESTARǁ_concentrated_ols__mutmut_8,
        "xǁESTARǁ_concentrated_ols__mutmut_9": xǁESTARǁ_concentrated_ols__mutmut_9,
        "xǁESTARǁ_concentrated_ols__mutmut_10": xǁESTARǁ_concentrated_ols__mutmut_10,
        "xǁESTARǁ_concentrated_ols__mutmut_11": xǁESTARǁ_concentrated_ols__mutmut_11,
        "xǁESTARǁ_concentrated_ols__mutmut_12": xǁESTARǁ_concentrated_ols__mutmut_12,
        "xǁESTARǁ_concentrated_ols__mutmut_13": xǁESTARǁ_concentrated_ols__mutmut_13,
        "xǁESTARǁ_concentrated_ols__mutmut_14": xǁESTARǁ_concentrated_ols__mutmut_14,
        "xǁESTARǁ_concentrated_ols__mutmut_15": xǁESTARǁ_concentrated_ols__mutmut_15,
        "xǁESTARǁ_concentrated_ols__mutmut_16": xǁESTARǁ_concentrated_ols__mutmut_16,
        "xǁESTARǁ_concentrated_ols__mutmut_17": xǁESTARǁ_concentrated_ols__mutmut_17,
        "xǁESTARǁ_concentrated_ols__mutmut_18": xǁESTARǁ_concentrated_ols__mutmut_18,
        "xǁESTARǁ_concentrated_ols__mutmut_19": xǁESTARǁ_concentrated_ols__mutmut_19,
        "xǁESTARǁ_concentrated_ols__mutmut_20": xǁESTARǁ_concentrated_ols__mutmut_20,
        "xǁESTARǁ_concentrated_ols__mutmut_21": xǁESTARǁ_concentrated_ols__mutmut_21,
        "xǁESTARǁ_concentrated_ols__mutmut_22": xǁESTARǁ_concentrated_ols__mutmut_22,
        "xǁESTARǁ_concentrated_ols__mutmut_23": xǁESTARǁ_concentrated_ols__mutmut_23,
        "xǁESTARǁ_concentrated_ols__mutmut_24": xǁESTARǁ_concentrated_ols__mutmut_24,
        "xǁESTARǁ_concentrated_ols__mutmut_25": xǁESTARǁ_concentrated_ols__mutmut_25,
        "xǁESTARǁ_concentrated_ols__mutmut_26": xǁESTARǁ_concentrated_ols__mutmut_26,
        "xǁESTARǁ_concentrated_ols__mutmut_27": xǁESTARǁ_concentrated_ols__mutmut_27,
        "xǁESTARǁ_concentrated_ols__mutmut_28": xǁESTARǁ_concentrated_ols__mutmut_28,
        "xǁESTARǁ_concentrated_ols__mutmut_29": xǁESTARǁ_concentrated_ols__mutmut_29,
    }
    xǁESTARǁ_concentrated_ols__mutmut_orig.__name__ = "xǁESTARǁ_concentrated_ols"

    def _grid_search(
        self,
        y: NDArray[np.float64],
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
    ) -> tuple[float, float, float]:
        args = [y, x_mat, s]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁESTARǁ_grid_search__mutmut_orig"),
            object.__getattribute__(self, "xǁESTARǁ_grid_search__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁESTARǁ_grid_search__mutmut_orig(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_1(
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
        gamma_vals = None

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_2(
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
        gamma_vals = np.logspace(None, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_3(
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
        gamma_vals = np.logspace(-1, None, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_4(
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
        gamma_vals = np.logspace(-1, 2, None)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_5(
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
        gamma_vals = np.logspace(2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_6(
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
        gamma_vals = np.logspace(-1, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_7(
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
        gamma_vals = np.logspace(
            -1,
            2,
        )

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_8(
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
        gamma_vals = np.logspace(+1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_9(
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
        gamma_vals = np.logspace(-2, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_10(
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
        gamma_vals = np.logspace(-1, 3, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_11(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_12(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_13(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_14(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_15(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_16(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_17(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_18(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_19(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_20(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_21(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_22(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_23(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_24(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_25(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_26(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_27(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_28(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_29(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_30(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_31(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_32(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_33(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_34(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_35(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_36(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_37(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_38(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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

    def xǁESTARǁ_grid_search__mutmut_39(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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

    def xǁESTARǁ_grid_search__mutmut_40(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(None))

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

    def xǁESTARǁ_grid_search__mutmut_41(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_42(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_43(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_44(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_45(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_46(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_47(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_48(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_49(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_50(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_51(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_52(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_53(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_54(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_55(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_56(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_57(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    def xǁESTARǁ_grid_search__mutmut_58(
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
        gamma_vals = np.logspace(-1, 2, self.gamma_grid)

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
        best_c = float(np.mean(s))

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

    xǁESTARǁ_grid_search__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁESTARǁ_grid_search__mutmut_1": xǁESTARǁ_grid_search__mutmut_1,
        "xǁESTARǁ_grid_search__mutmut_2": xǁESTARǁ_grid_search__mutmut_2,
        "xǁESTARǁ_grid_search__mutmut_3": xǁESTARǁ_grid_search__mutmut_3,
        "xǁESTARǁ_grid_search__mutmut_4": xǁESTARǁ_grid_search__mutmut_4,
        "xǁESTARǁ_grid_search__mutmut_5": xǁESTARǁ_grid_search__mutmut_5,
        "xǁESTARǁ_grid_search__mutmut_6": xǁESTARǁ_grid_search__mutmut_6,
        "xǁESTARǁ_grid_search__mutmut_7": xǁESTARǁ_grid_search__mutmut_7,
        "xǁESTARǁ_grid_search__mutmut_8": xǁESTARǁ_grid_search__mutmut_8,
        "xǁESTARǁ_grid_search__mutmut_9": xǁESTARǁ_grid_search__mutmut_9,
        "xǁESTARǁ_grid_search__mutmut_10": xǁESTARǁ_grid_search__mutmut_10,
        "xǁESTARǁ_grid_search__mutmut_11": xǁESTARǁ_grid_search__mutmut_11,
        "xǁESTARǁ_grid_search__mutmut_12": xǁESTARǁ_grid_search__mutmut_12,
        "xǁESTARǁ_grid_search__mutmut_13": xǁESTARǁ_grid_search__mutmut_13,
        "xǁESTARǁ_grid_search__mutmut_14": xǁESTARǁ_grid_search__mutmut_14,
        "xǁESTARǁ_grid_search__mutmut_15": xǁESTARǁ_grid_search__mutmut_15,
        "xǁESTARǁ_grid_search__mutmut_16": xǁESTARǁ_grid_search__mutmut_16,
        "xǁESTARǁ_grid_search__mutmut_17": xǁESTARǁ_grid_search__mutmut_17,
        "xǁESTARǁ_grid_search__mutmut_18": xǁESTARǁ_grid_search__mutmut_18,
        "xǁESTARǁ_grid_search__mutmut_19": xǁESTARǁ_grid_search__mutmut_19,
        "xǁESTARǁ_grid_search__mutmut_20": xǁESTARǁ_grid_search__mutmut_20,
        "xǁESTARǁ_grid_search__mutmut_21": xǁESTARǁ_grid_search__mutmut_21,
        "xǁESTARǁ_grid_search__mutmut_22": xǁESTARǁ_grid_search__mutmut_22,
        "xǁESTARǁ_grid_search__mutmut_23": xǁESTARǁ_grid_search__mutmut_23,
        "xǁESTARǁ_grid_search__mutmut_24": xǁESTARǁ_grid_search__mutmut_24,
        "xǁESTARǁ_grid_search__mutmut_25": xǁESTARǁ_grid_search__mutmut_25,
        "xǁESTARǁ_grid_search__mutmut_26": xǁESTARǁ_grid_search__mutmut_26,
        "xǁESTARǁ_grid_search__mutmut_27": xǁESTARǁ_grid_search__mutmut_27,
        "xǁESTARǁ_grid_search__mutmut_28": xǁESTARǁ_grid_search__mutmut_28,
        "xǁESTARǁ_grid_search__mutmut_29": xǁESTARǁ_grid_search__mutmut_29,
        "xǁESTARǁ_grid_search__mutmut_30": xǁESTARǁ_grid_search__mutmut_30,
        "xǁESTARǁ_grid_search__mutmut_31": xǁESTARǁ_grid_search__mutmut_31,
        "xǁESTARǁ_grid_search__mutmut_32": xǁESTARǁ_grid_search__mutmut_32,
        "xǁESTARǁ_grid_search__mutmut_33": xǁESTARǁ_grid_search__mutmut_33,
        "xǁESTARǁ_grid_search__mutmut_34": xǁESTARǁ_grid_search__mutmut_34,
        "xǁESTARǁ_grid_search__mutmut_35": xǁESTARǁ_grid_search__mutmut_35,
        "xǁESTARǁ_grid_search__mutmut_36": xǁESTARǁ_grid_search__mutmut_36,
        "xǁESTARǁ_grid_search__mutmut_37": xǁESTARǁ_grid_search__mutmut_37,
        "xǁESTARǁ_grid_search__mutmut_38": xǁESTARǁ_grid_search__mutmut_38,
        "xǁESTARǁ_grid_search__mutmut_39": xǁESTARǁ_grid_search__mutmut_39,
        "xǁESTARǁ_grid_search__mutmut_40": xǁESTARǁ_grid_search__mutmut_40,
        "xǁESTARǁ_grid_search__mutmut_41": xǁESTARǁ_grid_search__mutmut_41,
        "xǁESTARǁ_grid_search__mutmut_42": xǁESTARǁ_grid_search__mutmut_42,
        "xǁESTARǁ_grid_search__mutmut_43": xǁESTARǁ_grid_search__mutmut_43,
        "xǁESTARǁ_grid_search__mutmut_44": xǁESTARǁ_grid_search__mutmut_44,
        "xǁESTARǁ_grid_search__mutmut_45": xǁESTARǁ_grid_search__mutmut_45,
        "xǁESTARǁ_grid_search__mutmut_46": xǁESTARǁ_grid_search__mutmut_46,
        "xǁESTARǁ_grid_search__mutmut_47": xǁESTARǁ_grid_search__mutmut_47,
        "xǁESTARǁ_grid_search__mutmut_48": xǁESTARǁ_grid_search__mutmut_48,
        "xǁESTARǁ_grid_search__mutmut_49": xǁESTARǁ_grid_search__mutmut_49,
        "xǁESTARǁ_grid_search__mutmut_50": xǁESTARǁ_grid_search__mutmut_50,
        "xǁESTARǁ_grid_search__mutmut_51": xǁESTARǁ_grid_search__mutmut_51,
        "xǁESTARǁ_grid_search__mutmut_52": xǁESTARǁ_grid_search__mutmut_52,
        "xǁESTARǁ_grid_search__mutmut_53": xǁESTARǁ_grid_search__mutmut_53,
        "xǁESTARǁ_grid_search__mutmut_54": xǁESTARǁ_grid_search__mutmut_54,
        "xǁESTARǁ_grid_search__mutmut_55": xǁESTARǁ_grid_search__mutmut_55,
        "xǁESTARǁ_grid_search__mutmut_56": xǁESTARǁ_grid_search__mutmut_56,
        "xǁESTARǁ_grid_search__mutmut_57": xǁESTARǁ_grid_search__mutmut_57,
        "xǁESTARǁ_grid_search__mutmut_58": xǁESTARǁ_grid_search__mutmut_58,
    }
    xǁESTARǁ_grid_search__mutmut_orig.__name__ = "xǁESTARǁ_grid_search"

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
            object.__getattribute__(self, "xǁESTARǁ_nls_objective__mutmut_orig"),
            object.__getattribute__(self, "xǁESTARǁ_nls_objective__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁESTARǁ_nls_objective__mutmut_orig(
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
        gamma = min(gamma, 500.0)

        try:
            _, _, rss = self._concentrated_ols(gamma, c, y, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁESTARǁ_nls_objective__mutmut_1(
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
        gamma = min(gamma, 500.0)

        try:
            _, _, rss = self._concentrated_ols(gamma, c, y, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁESTARǁ_nls_objective__mutmut_2(
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
        gamma = min(gamma, 500.0)

        try:
            _, _, rss = self._concentrated_ols(gamma, c, y, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁESTARǁ_nls_objective__mutmut_3(
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
        gamma = min(gamma, 500.0)

        try:
            _, _, rss = self._concentrated_ols(gamma, c, y, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁESTARǁ_nls_objective__mutmut_4(
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
        gamma = None

        try:
            _, _, rss = self._concentrated_ols(gamma, c, y, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁESTARǁ_nls_objective__mutmut_5(
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
        gamma = min(None, 500.0)

        try:
            _, _, rss = self._concentrated_ols(gamma, c, y, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁESTARǁ_nls_objective__mutmut_6(
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
        gamma = min(gamma, None)

        try:
            _, _, rss = self._concentrated_ols(gamma, c, y, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁESTARǁ_nls_objective__mutmut_7(
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
        gamma = min(500.0)

        try:
            _, _, rss = self._concentrated_ols(gamma, c, y, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁESTARǁ_nls_objective__mutmut_8(
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
        )

        try:
            _, _, rss = self._concentrated_ols(gamma, c, y, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁESTARǁ_nls_objective__mutmut_9(
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
        gamma = min(gamma, 501.0)

        try:
            _, _, rss = self._concentrated_ols(gamma, c, y, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁESTARǁ_nls_objective__mutmut_10(
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
        gamma = min(gamma, 500.0)

        try:
            _, _, rss = None
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁESTARǁ_nls_objective__mutmut_11(
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
        gamma = min(gamma, 500.0)

        try:
            _, _, rss = self._concentrated_ols(None, c, y, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁESTARǁ_nls_objective__mutmut_12(
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
        gamma = min(gamma, 500.0)

        try:
            _, _, rss = self._concentrated_ols(gamma, None, y, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁESTARǁ_nls_objective__mutmut_13(
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
        gamma = min(gamma, 500.0)

        try:
            _, _, rss = self._concentrated_ols(gamma, c, None, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁESTARǁ_nls_objective__mutmut_14(
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
        gamma = min(gamma, 500.0)

        try:
            _, _, rss = self._concentrated_ols(gamma, c, y, None, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁESTARǁ_nls_objective__mutmut_15(
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
        gamma = min(gamma, 500.0)

        try:
            _, _, rss = self._concentrated_ols(gamma, c, y, x_mat, None)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁESTARǁ_nls_objective__mutmut_16(
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
        gamma = min(gamma, 500.0)

        try:
            _, _, rss = self._concentrated_ols(c, y, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁESTARǁ_nls_objective__mutmut_17(
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
        gamma = min(gamma, 500.0)

        try:
            _, _, rss = self._concentrated_ols(gamma, y, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁESTARǁ_nls_objective__mutmut_18(
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
        gamma = min(gamma, 500.0)

        try:
            _, _, rss = self._concentrated_ols(gamma, c, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁESTARǁ_nls_objective__mutmut_19(
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
        gamma = min(gamma, 500.0)

        try:
            _, _, rss = self._concentrated_ols(gamma, c, y, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1e15
        return rss

    def xǁESTARǁ_nls_objective__mutmut_20(
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
        gamma = min(gamma, 500.0)

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

    def xǁESTARǁ_nls_objective__mutmut_21(
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
        gamma = min(gamma, 500.0)

        try:
            _, _, rss = self._concentrated_ols(gamma, c, y, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = None
        return rss

    def xǁESTARǁ_nls_objective__mutmut_22(
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
        gamma = min(gamma, 500.0)

        try:
            _, _, rss = self._concentrated_ols(gamma, c, y, x_mat, s)
        except (np.linalg.LinAlgError, ValueError):
            rss = 1000000000000001.0
        return rss

    xǁESTARǁ_nls_objective__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁESTARǁ_nls_objective__mutmut_1": xǁESTARǁ_nls_objective__mutmut_1,
        "xǁESTARǁ_nls_objective__mutmut_2": xǁESTARǁ_nls_objective__mutmut_2,
        "xǁESTARǁ_nls_objective__mutmut_3": xǁESTARǁ_nls_objective__mutmut_3,
        "xǁESTARǁ_nls_objective__mutmut_4": xǁESTARǁ_nls_objective__mutmut_4,
        "xǁESTARǁ_nls_objective__mutmut_5": xǁESTARǁ_nls_objective__mutmut_5,
        "xǁESTARǁ_nls_objective__mutmut_6": xǁESTARǁ_nls_objective__mutmut_6,
        "xǁESTARǁ_nls_objective__mutmut_7": xǁESTARǁ_nls_objective__mutmut_7,
        "xǁESTARǁ_nls_objective__mutmut_8": xǁESTARǁ_nls_objective__mutmut_8,
        "xǁESTARǁ_nls_objective__mutmut_9": xǁESTARǁ_nls_objective__mutmut_9,
        "xǁESTARǁ_nls_objective__mutmut_10": xǁESTARǁ_nls_objective__mutmut_10,
        "xǁESTARǁ_nls_objective__mutmut_11": xǁESTARǁ_nls_objective__mutmut_11,
        "xǁESTARǁ_nls_objective__mutmut_12": xǁESTARǁ_nls_objective__mutmut_12,
        "xǁESTARǁ_nls_objective__mutmut_13": xǁESTARǁ_nls_objective__mutmut_13,
        "xǁESTARǁ_nls_objective__mutmut_14": xǁESTARǁ_nls_objective__mutmut_14,
        "xǁESTARǁ_nls_objective__mutmut_15": xǁESTARǁ_nls_objective__mutmut_15,
        "xǁESTARǁ_nls_objective__mutmut_16": xǁESTARǁ_nls_objective__mutmut_16,
        "xǁESTARǁ_nls_objective__mutmut_17": xǁESTARǁ_nls_objective__mutmut_17,
        "xǁESTARǁ_nls_objective__mutmut_18": xǁESTARǁ_nls_objective__mutmut_18,
        "xǁESTARǁ_nls_objective__mutmut_19": xǁESTARǁ_nls_objective__mutmut_19,
        "xǁESTARǁ_nls_objective__mutmut_20": xǁESTARǁ_nls_objective__mutmut_20,
        "xǁESTARǁ_nls_objective__mutmut_21": xǁESTARǁ_nls_objective__mutmut_21,
        "xǁESTARǁ_nls_objective__mutmut_22": xǁESTARǁ_nls_objective__mutmut_22,
    }
    xǁESTARǁ_nls_objective__mutmut_orig.__name__ = "xǁESTARǁ_nls_objective"

    def _fit_cls(self) -> ThresholdResults:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁESTARǁ_fit_cls__mutmut_orig"),
            object.__getattribute__(self, "xǁESTARǁ_fit_cls__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁESTARǁ_fit_cls__mutmut_orig(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_1(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_2(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_3(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_4(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_5(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_6(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_7(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_8(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_9(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_10(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_11(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_12(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_13(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_14(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_15(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_16(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_17(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_18(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_19(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_20(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_21(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_22(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_23(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_24(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_25(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_26(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_27(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_28(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_29(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_30(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_31(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_32(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_33(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_34(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_35(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_36(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_37(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_38(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_39(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_40(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_41(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_42(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_43(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_44(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_45(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_46(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_47(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_48(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_49(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_50(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_51(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_52(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_53(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_54(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_55(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_56(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_57(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_58(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_59(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_60(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_61(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_62(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_63(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_64(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_65(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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

    def xǁESTARǁ_fit_cls__mutmut_66(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(None, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_67(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, None, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_68(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, None)

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

    def xǁESTARǁ_fit_cls__mutmut_69(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_70(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_71(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(
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

    def xǁESTARǁ_fit_cls__mutmut_72(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_73(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_74(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_75(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_76(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_77(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_78(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_79(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_80(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_81(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_82(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_83(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_84(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_85(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_86(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_87(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_88(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_89(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_90(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_91(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_92(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_93(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_94(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_95(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_96(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_97(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_98(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_99(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_100(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_101(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_102(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_103(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_104(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_105(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_106(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_107(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_108(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_109(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_110(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_111(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_112(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_113(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_114(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_115(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_116(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_117(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_118(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_119(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_120(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_121(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_122(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_123(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_124(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_125(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_126(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_127(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_128(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_129(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_130(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_131(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_132(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_133(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_134(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_135(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_136(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_137(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_138(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_139(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_140(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_141(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_142(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_143(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_144(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_145(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_146(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_147(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_148(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_149(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_150(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_151(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_152(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_153(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_154(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_155(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_156(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_157(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_158(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_159(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_160(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_161(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_162(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_163(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_164(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_165(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_166(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_167(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_168(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_169(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_170(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_171(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_172(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_173(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_174(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_175(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_176(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_177(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_178(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_179(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_180(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_181(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_182(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_183(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_184(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_185(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_186(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_187(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_188(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_189(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_190(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_191(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_192(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_193(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_194(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_195(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_196(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    def xǁESTARǁ_fit_cls__mutmut_197(self) -> ThresholdResults:
        """Fit ESTAR via Conditional Least Squares (NLS).

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
        g = exponential_transition(s, best_gamma, best_c)

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

    xǁESTARǁ_fit_cls__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁESTARǁ_fit_cls__mutmut_1": xǁESTARǁ_fit_cls__mutmut_1,
        "xǁESTARǁ_fit_cls__mutmut_2": xǁESTARǁ_fit_cls__mutmut_2,
        "xǁESTARǁ_fit_cls__mutmut_3": xǁESTARǁ_fit_cls__mutmut_3,
        "xǁESTARǁ_fit_cls__mutmut_4": xǁESTARǁ_fit_cls__mutmut_4,
        "xǁESTARǁ_fit_cls__mutmut_5": xǁESTARǁ_fit_cls__mutmut_5,
        "xǁESTARǁ_fit_cls__mutmut_6": xǁESTARǁ_fit_cls__mutmut_6,
        "xǁESTARǁ_fit_cls__mutmut_7": xǁESTARǁ_fit_cls__mutmut_7,
        "xǁESTARǁ_fit_cls__mutmut_8": xǁESTARǁ_fit_cls__mutmut_8,
        "xǁESTARǁ_fit_cls__mutmut_9": xǁESTARǁ_fit_cls__mutmut_9,
        "xǁESTARǁ_fit_cls__mutmut_10": xǁESTARǁ_fit_cls__mutmut_10,
        "xǁESTARǁ_fit_cls__mutmut_11": xǁESTARǁ_fit_cls__mutmut_11,
        "xǁESTARǁ_fit_cls__mutmut_12": xǁESTARǁ_fit_cls__mutmut_12,
        "xǁESTARǁ_fit_cls__mutmut_13": xǁESTARǁ_fit_cls__mutmut_13,
        "xǁESTARǁ_fit_cls__mutmut_14": xǁESTARǁ_fit_cls__mutmut_14,
        "xǁESTARǁ_fit_cls__mutmut_15": xǁESTARǁ_fit_cls__mutmut_15,
        "xǁESTARǁ_fit_cls__mutmut_16": xǁESTARǁ_fit_cls__mutmut_16,
        "xǁESTARǁ_fit_cls__mutmut_17": xǁESTARǁ_fit_cls__mutmut_17,
        "xǁESTARǁ_fit_cls__mutmut_18": xǁESTARǁ_fit_cls__mutmut_18,
        "xǁESTARǁ_fit_cls__mutmut_19": xǁESTARǁ_fit_cls__mutmut_19,
        "xǁESTARǁ_fit_cls__mutmut_20": xǁESTARǁ_fit_cls__mutmut_20,
        "xǁESTARǁ_fit_cls__mutmut_21": xǁESTARǁ_fit_cls__mutmut_21,
        "xǁESTARǁ_fit_cls__mutmut_22": xǁESTARǁ_fit_cls__mutmut_22,
        "xǁESTARǁ_fit_cls__mutmut_23": xǁESTARǁ_fit_cls__mutmut_23,
        "xǁESTARǁ_fit_cls__mutmut_24": xǁESTARǁ_fit_cls__mutmut_24,
        "xǁESTARǁ_fit_cls__mutmut_25": xǁESTARǁ_fit_cls__mutmut_25,
        "xǁESTARǁ_fit_cls__mutmut_26": xǁESTARǁ_fit_cls__mutmut_26,
        "xǁESTARǁ_fit_cls__mutmut_27": xǁESTARǁ_fit_cls__mutmut_27,
        "xǁESTARǁ_fit_cls__mutmut_28": xǁESTARǁ_fit_cls__mutmut_28,
        "xǁESTARǁ_fit_cls__mutmut_29": xǁESTARǁ_fit_cls__mutmut_29,
        "xǁESTARǁ_fit_cls__mutmut_30": xǁESTARǁ_fit_cls__mutmut_30,
        "xǁESTARǁ_fit_cls__mutmut_31": xǁESTARǁ_fit_cls__mutmut_31,
        "xǁESTARǁ_fit_cls__mutmut_32": xǁESTARǁ_fit_cls__mutmut_32,
        "xǁESTARǁ_fit_cls__mutmut_33": xǁESTARǁ_fit_cls__mutmut_33,
        "xǁESTARǁ_fit_cls__mutmut_34": xǁESTARǁ_fit_cls__mutmut_34,
        "xǁESTARǁ_fit_cls__mutmut_35": xǁESTARǁ_fit_cls__mutmut_35,
        "xǁESTARǁ_fit_cls__mutmut_36": xǁESTARǁ_fit_cls__mutmut_36,
        "xǁESTARǁ_fit_cls__mutmut_37": xǁESTARǁ_fit_cls__mutmut_37,
        "xǁESTARǁ_fit_cls__mutmut_38": xǁESTARǁ_fit_cls__mutmut_38,
        "xǁESTARǁ_fit_cls__mutmut_39": xǁESTARǁ_fit_cls__mutmut_39,
        "xǁESTARǁ_fit_cls__mutmut_40": xǁESTARǁ_fit_cls__mutmut_40,
        "xǁESTARǁ_fit_cls__mutmut_41": xǁESTARǁ_fit_cls__mutmut_41,
        "xǁESTARǁ_fit_cls__mutmut_42": xǁESTARǁ_fit_cls__mutmut_42,
        "xǁESTARǁ_fit_cls__mutmut_43": xǁESTARǁ_fit_cls__mutmut_43,
        "xǁESTARǁ_fit_cls__mutmut_44": xǁESTARǁ_fit_cls__mutmut_44,
        "xǁESTARǁ_fit_cls__mutmut_45": xǁESTARǁ_fit_cls__mutmut_45,
        "xǁESTARǁ_fit_cls__mutmut_46": xǁESTARǁ_fit_cls__mutmut_46,
        "xǁESTARǁ_fit_cls__mutmut_47": xǁESTARǁ_fit_cls__mutmut_47,
        "xǁESTARǁ_fit_cls__mutmut_48": xǁESTARǁ_fit_cls__mutmut_48,
        "xǁESTARǁ_fit_cls__mutmut_49": xǁESTARǁ_fit_cls__mutmut_49,
        "xǁESTARǁ_fit_cls__mutmut_50": xǁESTARǁ_fit_cls__mutmut_50,
        "xǁESTARǁ_fit_cls__mutmut_51": xǁESTARǁ_fit_cls__mutmut_51,
        "xǁESTARǁ_fit_cls__mutmut_52": xǁESTARǁ_fit_cls__mutmut_52,
        "xǁESTARǁ_fit_cls__mutmut_53": xǁESTARǁ_fit_cls__mutmut_53,
        "xǁESTARǁ_fit_cls__mutmut_54": xǁESTARǁ_fit_cls__mutmut_54,
        "xǁESTARǁ_fit_cls__mutmut_55": xǁESTARǁ_fit_cls__mutmut_55,
        "xǁESTARǁ_fit_cls__mutmut_56": xǁESTARǁ_fit_cls__mutmut_56,
        "xǁESTARǁ_fit_cls__mutmut_57": xǁESTARǁ_fit_cls__mutmut_57,
        "xǁESTARǁ_fit_cls__mutmut_58": xǁESTARǁ_fit_cls__mutmut_58,
        "xǁESTARǁ_fit_cls__mutmut_59": xǁESTARǁ_fit_cls__mutmut_59,
        "xǁESTARǁ_fit_cls__mutmut_60": xǁESTARǁ_fit_cls__mutmut_60,
        "xǁESTARǁ_fit_cls__mutmut_61": xǁESTARǁ_fit_cls__mutmut_61,
        "xǁESTARǁ_fit_cls__mutmut_62": xǁESTARǁ_fit_cls__mutmut_62,
        "xǁESTARǁ_fit_cls__mutmut_63": xǁESTARǁ_fit_cls__mutmut_63,
        "xǁESTARǁ_fit_cls__mutmut_64": xǁESTARǁ_fit_cls__mutmut_64,
        "xǁESTARǁ_fit_cls__mutmut_65": xǁESTARǁ_fit_cls__mutmut_65,
        "xǁESTARǁ_fit_cls__mutmut_66": xǁESTARǁ_fit_cls__mutmut_66,
        "xǁESTARǁ_fit_cls__mutmut_67": xǁESTARǁ_fit_cls__mutmut_67,
        "xǁESTARǁ_fit_cls__mutmut_68": xǁESTARǁ_fit_cls__mutmut_68,
        "xǁESTARǁ_fit_cls__mutmut_69": xǁESTARǁ_fit_cls__mutmut_69,
        "xǁESTARǁ_fit_cls__mutmut_70": xǁESTARǁ_fit_cls__mutmut_70,
        "xǁESTARǁ_fit_cls__mutmut_71": xǁESTARǁ_fit_cls__mutmut_71,
        "xǁESTARǁ_fit_cls__mutmut_72": xǁESTARǁ_fit_cls__mutmut_72,
        "xǁESTARǁ_fit_cls__mutmut_73": xǁESTARǁ_fit_cls__mutmut_73,
        "xǁESTARǁ_fit_cls__mutmut_74": xǁESTARǁ_fit_cls__mutmut_74,
        "xǁESTARǁ_fit_cls__mutmut_75": xǁESTARǁ_fit_cls__mutmut_75,
        "xǁESTARǁ_fit_cls__mutmut_76": xǁESTARǁ_fit_cls__mutmut_76,
        "xǁESTARǁ_fit_cls__mutmut_77": xǁESTARǁ_fit_cls__mutmut_77,
        "xǁESTARǁ_fit_cls__mutmut_78": xǁESTARǁ_fit_cls__mutmut_78,
        "xǁESTARǁ_fit_cls__mutmut_79": xǁESTARǁ_fit_cls__mutmut_79,
        "xǁESTARǁ_fit_cls__mutmut_80": xǁESTARǁ_fit_cls__mutmut_80,
        "xǁESTARǁ_fit_cls__mutmut_81": xǁESTARǁ_fit_cls__mutmut_81,
        "xǁESTARǁ_fit_cls__mutmut_82": xǁESTARǁ_fit_cls__mutmut_82,
        "xǁESTARǁ_fit_cls__mutmut_83": xǁESTARǁ_fit_cls__mutmut_83,
        "xǁESTARǁ_fit_cls__mutmut_84": xǁESTARǁ_fit_cls__mutmut_84,
        "xǁESTARǁ_fit_cls__mutmut_85": xǁESTARǁ_fit_cls__mutmut_85,
        "xǁESTARǁ_fit_cls__mutmut_86": xǁESTARǁ_fit_cls__mutmut_86,
        "xǁESTARǁ_fit_cls__mutmut_87": xǁESTARǁ_fit_cls__mutmut_87,
        "xǁESTARǁ_fit_cls__mutmut_88": xǁESTARǁ_fit_cls__mutmut_88,
        "xǁESTARǁ_fit_cls__mutmut_89": xǁESTARǁ_fit_cls__mutmut_89,
        "xǁESTARǁ_fit_cls__mutmut_90": xǁESTARǁ_fit_cls__mutmut_90,
        "xǁESTARǁ_fit_cls__mutmut_91": xǁESTARǁ_fit_cls__mutmut_91,
        "xǁESTARǁ_fit_cls__mutmut_92": xǁESTARǁ_fit_cls__mutmut_92,
        "xǁESTARǁ_fit_cls__mutmut_93": xǁESTARǁ_fit_cls__mutmut_93,
        "xǁESTARǁ_fit_cls__mutmut_94": xǁESTARǁ_fit_cls__mutmut_94,
        "xǁESTARǁ_fit_cls__mutmut_95": xǁESTARǁ_fit_cls__mutmut_95,
        "xǁESTARǁ_fit_cls__mutmut_96": xǁESTARǁ_fit_cls__mutmut_96,
        "xǁESTARǁ_fit_cls__mutmut_97": xǁESTARǁ_fit_cls__mutmut_97,
        "xǁESTARǁ_fit_cls__mutmut_98": xǁESTARǁ_fit_cls__mutmut_98,
        "xǁESTARǁ_fit_cls__mutmut_99": xǁESTARǁ_fit_cls__mutmut_99,
        "xǁESTARǁ_fit_cls__mutmut_100": xǁESTARǁ_fit_cls__mutmut_100,
        "xǁESTARǁ_fit_cls__mutmut_101": xǁESTARǁ_fit_cls__mutmut_101,
        "xǁESTARǁ_fit_cls__mutmut_102": xǁESTARǁ_fit_cls__mutmut_102,
        "xǁESTARǁ_fit_cls__mutmut_103": xǁESTARǁ_fit_cls__mutmut_103,
        "xǁESTARǁ_fit_cls__mutmut_104": xǁESTARǁ_fit_cls__mutmut_104,
        "xǁESTARǁ_fit_cls__mutmut_105": xǁESTARǁ_fit_cls__mutmut_105,
        "xǁESTARǁ_fit_cls__mutmut_106": xǁESTARǁ_fit_cls__mutmut_106,
        "xǁESTARǁ_fit_cls__mutmut_107": xǁESTARǁ_fit_cls__mutmut_107,
        "xǁESTARǁ_fit_cls__mutmut_108": xǁESTARǁ_fit_cls__mutmut_108,
        "xǁESTARǁ_fit_cls__mutmut_109": xǁESTARǁ_fit_cls__mutmut_109,
        "xǁESTARǁ_fit_cls__mutmut_110": xǁESTARǁ_fit_cls__mutmut_110,
        "xǁESTARǁ_fit_cls__mutmut_111": xǁESTARǁ_fit_cls__mutmut_111,
        "xǁESTARǁ_fit_cls__mutmut_112": xǁESTARǁ_fit_cls__mutmut_112,
        "xǁESTARǁ_fit_cls__mutmut_113": xǁESTARǁ_fit_cls__mutmut_113,
        "xǁESTARǁ_fit_cls__mutmut_114": xǁESTARǁ_fit_cls__mutmut_114,
        "xǁESTARǁ_fit_cls__mutmut_115": xǁESTARǁ_fit_cls__mutmut_115,
        "xǁESTARǁ_fit_cls__mutmut_116": xǁESTARǁ_fit_cls__mutmut_116,
        "xǁESTARǁ_fit_cls__mutmut_117": xǁESTARǁ_fit_cls__mutmut_117,
        "xǁESTARǁ_fit_cls__mutmut_118": xǁESTARǁ_fit_cls__mutmut_118,
        "xǁESTARǁ_fit_cls__mutmut_119": xǁESTARǁ_fit_cls__mutmut_119,
        "xǁESTARǁ_fit_cls__mutmut_120": xǁESTARǁ_fit_cls__mutmut_120,
        "xǁESTARǁ_fit_cls__mutmut_121": xǁESTARǁ_fit_cls__mutmut_121,
        "xǁESTARǁ_fit_cls__mutmut_122": xǁESTARǁ_fit_cls__mutmut_122,
        "xǁESTARǁ_fit_cls__mutmut_123": xǁESTARǁ_fit_cls__mutmut_123,
        "xǁESTARǁ_fit_cls__mutmut_124": xǁESTARǁ_fit_cls__mutmut_124,
        "xǁESTARǁ_fit_cls__mutmut_125": xǁESTARǁ_fit_cls__mutmut_125,
        "xǁESTARǁ_fit_cls__mutmut_126": xǁESTARǁ_fit_cls__mutmut_126,
        "xǁESTARǁ_fit_cls__mutmut_127": xǁESTARǁ_fit_cls__mutmut_127,
        "xǁESTARǁ_fit_cls__mutmut_128": xǁESTARǁ_fit_cls__mutmut_128,
        "xǁESTARǁ_fit_cls__mutmut_129": xǁESTARǁ_fit_cls__mutmut_129,
        "xǁESTARǁ_fit_cls__mutmut_130": xǁESTARǁ_fit_cls__mutmut_130,
        "xǁESTARǁ_fit_cls__mutmut_131": xǁESTARǁ_fit_cls__mutmut_131,
        "xǁESTARǁ_fit_cls__mutmut_132": xǁESTARǁ_fit_cls__mutmut_132,
        "xǁESTARǁ_fit_cls__mutmut_133": xǁESTARǁ_fit_cls__mutmut_133,
        "xǁESTARǁ_fit_cls__mutmut_134": xǁESTARǁ_fit_cls__mutmut_134,
        "xǁESTARǁ_fit_cls__mutmut_135": xǁESTARǁ_fit_cls__mutmut_135,
        "xǁESTARǁ_fit_cls__mutmut_136": xǁESTARǁ_fit_cls__mutmut_136,
        "xǁESTARǁ_fit_cls__mutmut_137": xǁESTARǁ_fit_cls__mutmut_137,
        "xǁESTARǁ_fit_cls__mutmut_138": xǁESTARǁ_fit_cls__mutmut_138,
        "xǁESTARǁ_fit_cls__mutmut_139": xǁESTARǁ_fit_cls__mutmut_139,
        "xǁESTARǁ_fit_cls__mutmut_140": xǁESTARǁ_fit_cls__mutmut_140,
        "xǁESTARǁ_fit_cls__mutmut_141": xǁESTARǁ_fit_cls__mutmut_141,
        "xǁESTARǁ_fit_cls__mutmut_142": xǁESTARǁ_fit_cls__mutmut_142,
        "xǁESTARǁ_fit_cls__mutmut_143": xǁESTARǁ_fit_cls__mutmut_143,
        "xǁESTARǁ_fit_cls__mutmut_144": xǁESTARǁ_fit_cls__mutmut_144,
        "xǁESTARǁ_fit_cls__mutmut_145": xǁESTARǁ_fit_cls__mutmut_145,
        "xǁESTARǁ_fit_cls__mutmut_146": xǁESTARǁ_fit_cls__mutmut_146,
        "xǁESTARǁ_fit_cls__mutmut_147": xǁESTARǁ_fit_cls__mutmut_147,
        "xǁESTARǁ_fit_cls__mutmut_148": xǁESTARǁ_fit_cls__mutmut_148,
        "xǁESTARǁ_fit_cls__mutmut_149": xǁESTARǁ_fit_cls__mutmut_149,
        "xǁESTARǁ_fit_cls__mutmut_150": xǁESTARǁ_fit_cls__mutmut_150,
        "xǁESTARǁ_fit_cls__mutmut_151": xǁESTARǁ_fit_cls__mutmut_151,
        "xǁESTARǁ_fit_cls__mutmut_152": xǁESTARǁ_fit_cls__mutmut_152,
        "xǁESTARǁ_fit_cls__mutmut_153": xǁESTARǁ_fit_cls__mutmut_153,
        "xǁESTARǁ_fit_cls__mutmut_154": xǁESTARǁ_fit_cls__mutmut_154,
        "xǁESTARǁ_fit_cls__mutmut_155": xǁESTARǁ_fit_cls__mutmut_155,
        "xǁESTARǁ_fit_cls__mutmut_156": xǁESTARǁ_fit_cls__mutmut_156,
        "xǁESTARǁ_fit_cls__mutmut_157": xǁESTARǁ_fit_cls__mutmut_157,
        "xǁESTARǁ_fit_cls__mutmut_158": xǁESTARǁ_fit_cls__mutmut_158,
        "xǁESTARǁ_fit_cls__mutmut_159": xǁESTARǁ_fit_cls__mutmut_159,
        "xǁESTARǁ_fit_cls__mutmut_160": xǁESTARǁ_fit_cls__mutmut_160,
        "xǁESTARǁ_fit_cls__mutmut_161": xǁESTARǁ_fit_cls__mutmut_161,
        "xǁESTARǁ_fit_cls__mutmut_162": xǁESTARǁ_fit_cls__mutmut_162,
        "xǁESTARǁ_fit_cls__mutmut_163": xǁESTARǁ_fit_cls__mutmut_163,
        "xǁESTARǁ_fit_cls__mutmut_164": xǁESTARǁ_fit_cls__mutmut_164,
        "xǁESTARǁ_fit_cls__mutmut_165": xǁESTARǁ_fit_cls__mutmut_165,
        "xǁESTARǁ_fit_cls__mutmut_166": xǁESTARǁ_fit_cls__mutmut_166,
        "xǁESTARǁ_fit_cls__mutmut_167": xǁESTARǁ_fit_cls__mutmut_167,
        "xǁESTARǁ_fit_cls__mutmut_168": xǁESTARǁ_fit_cls__mutmut_168,
        "xǁESTARǁ_fit_cls__mutmut_169": xǁESTARǁ_fit_cls__mutmut_169,
        "xǁESTARǁ_fit_cls__mutmut_170": xǁESTARǁ_fit_cls__mutmut_170,
        "xǁESTARǁ_fit_cls__mutmut_171": xǁESTARǁ_fit_cls__mutmut_171,
        "xǁESTARǁ_fit_cls__mutmut_172": xǁESTARǁ_fit_cls__mutmut_172,
        "xǁESTARǁ_fit_cls__mutmut_173": xǁESTARǁ_fit_cls__mutmut_173,
        "xǁESTARǁ_fit_cls__mutmut_174": xǁESTARǁ_fit_cls__mutmut_174,
        "xǁESTARǁ_fit_cls__mutmut_175": xǁESTARǁ_fit_cls__mutmut_175,
        "xǁESTARǁ_fit_cls__mutmut_176": xǁESTARǁ_fit_cls__mutmut_176,
        "xǁESTARǁ_fit_cls__mutmut_177": xǁESTARǁ_fit_cls__mutmut_177,
        "xǁESTARǁ_fit_cls__mutmut_178": xǁESTARǁ_fit_cls__mutmut_178,
        "xǁESTARǁ_fit_cls__mutmut_179": xǁESTARǁ_fit_cls__mutmut_179,
        "xǁESTARǁ_fit_cls__mutmut_180": xǁESTARǁ_fit_cls__mutmut_180,
        "xǁESTARǁ_fit_cls__mutmut_181": xǁESTARǁ_fit_cls__mutmut_181,
        "xǁESTARǁ_fit_cls__mutmut_182": xǁESTARǁ_fit_cls__mutmut_182,
        "xǁESTARǁ_fit_cls__mutmut_183": xǁESTARǁ_fit_cls__mutmut_183,
        "xǁESTARǁ_fit_cls__mutmut_184": xǁESTARǁ_fit_cls__mutmut_184,
        "xǁESTARǁ_fit_cls__mutmut_185": xǁESTARǁ_fit_cls__mutmut_185,
        "xǁESTARǁ_fit_cls__mutmut_186": xǁESTARǁ_fit_cls__mutmut_186,
        "xǁESTARǁ_fit_cls__mutmut_187": xǁESTARǁ_fit_cls__mutmut_187,
        "xǁESTARǁ_fit_cls__mutmut_188": xǁESTARǁ_fit_cls__mutmut_188,
        "xǁESTARǁ_fit_cls__mutmut_189": xǁESTARǁ_fit_cls__mutmut_189,
        "xǁESTARǁ_fit_cls__mutmut_190": xǁESTARǁ_fit_cls__mutmut_190,
        "xǁESTARǁ_fit_cls__mutmut_191": xǁESTARǁ_fit_cls__mutmut_191,
        "xǁESTARǁ_fit_cls__mutmut_192": xǁESTARǁ_fit_cls__mutmut_192,
        "xǁESTARǁ_fit_cls__mutmut_193": xǁESTARǁ_fit_cls__mutmut_193,
        "xǁESTARǁ_fit_cls__mutmut_194": xǁESTARǁ_fit_cls__mutmut_194,
        "xǁESTARǁ_fit_cls__mutmut_195": xǁESTARǁ_fit_cls__mutmut_195,
        "xǁESTARǁ_fit_cls__mutmut_196": xǁESTARǁ_fit_cls__mutmut_196,
        "xǁESTARǁ_fit_cls__mutmut_197": xǁESTARǁ_fit_cls__mutmut_197,
    }
    xǁESTARǁ_fit_cls__mutmut_orig.__name__ = "xǁESTARǁ_fit_cls"
