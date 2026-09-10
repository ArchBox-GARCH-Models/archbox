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

The search over gamma is carried out in units of 1 / std(s_t) (Terasvirta's
convention), so the estimates do not depend on the scale of the data.

References
----------
- Terasvirta, T. (1994). Specification, Estimation, and Evaluation of
  Smooth Transition Autoregressive Models. JASA, 89(425), 208-218.
- van Dijk, D., Terasvirta, T. & Franses, P.H. (2002). Smooth Transition
  Autoregressive Models - A Survey. Econometric Reviews, 21(1), 1-47.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from archbox.threshold._star_base import SmoothTransitionModel
from archbox.threshold.transition import logistic_transition


class LSTAR(SmoothTransitionModel):
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
    scale_power: int = 1

    def _transition(self, s: NDArray[np.float64], gamma: float, c: float) -> NDArray[np.float64]:
        """Logistic transition: G(s; gamma, c) = 1/(1+exp(-gamma*(s-c))).

        Parameters
        ----------
        s : ndarray
            Transition variable values.
        gamma : float
            Speed of transition.
        c : float
            Location of transition.

        Returns
        -------
        ndarray
            Transition values in [0, 1].
        """
        return logistic_transition(np.asarray(s, dtype=np.float64), gamma, c)
