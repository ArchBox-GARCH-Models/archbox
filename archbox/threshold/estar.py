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

The search over gamma is carried out in units of 1 / var(s_t) (Terasvirta's
convention for the exponential transition, whose exponent is quadratic in
s_t - c), so the estimates do not depend on the scale of the data.

References
----------
- Terasvirta, T. (1994). Specification, Estimation, and Evaluation of
  Smooth Transition Autoregressive Models. JASA, 89(425), 208-218.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from archbox.threshold._star_base import SmoothTransitionModel
from archbox.threshold.transition import exponential_transition


class ESTAR(SmoothTransitionModel):
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
    scale_power: int = 2

    def _transition(self, s: NDArray[np.float64], gamma: float, c: float) -> NDArray[np.float64]:
        """Exponential transition: G(s; gamma, c) = 1 - exp(-gamma*(s-c)^2).

        Parameters
        ----------
        s : ndarray
            Transition variable values.
        gamma : float
            Speed of transition.
        c : float
            Center of symmetry.

        Returns
        -------
        ndarray
            Transition values in [0, 1].
        """
        return exponential_transition(np.asarray(s, dtype=np.float64), gamma, c)
