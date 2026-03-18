"""Hamilton Filter for Markov-Switching models.

Implements the recursive filter from Hamilton (1989) for computing
filtered probabilities P(S_t=j | Y_t, theta) in Markov-Switching models.

References
----------
Hamilton, J.D. (1989). A New Approach to the Economic Analysis of
Nonstationary Time Series and the Business Cycle.
Econometrica, 57(2), 357-384.
"""

from __future__ import annotations

from collections.abc import Callable

import numpy as np
from numpy.typing import NDArray


class HamiltonFilter:
    """Hamilton Filter for Markov-Switching models.

    Computes filtered probabilities, predicted probabilities,
    and log-likelihood recursively using the prediction-update scheme.
    """

    def filter(
        self,
        endog: NDArray[np.float64],
        regime_loglike_fn: Callable[[int, int], float],
        transition_matrix: NDArray[np.float64],
        init_probs: NDArray[np.float64] | None = None,
    ) -> tuple[
        NDArray[np.float64],
        NDArray[np.float64],
        float,
        NDArray[np.float64],
    ]:
        """Run the Hamilton filter.

        Parameters
        ----------
        endog : ndarray
            Observed data, shape (T,) or (T, n).
        regime_loglike_fn : callable
            Function (t, regime) -> float returning log f(y_t | S_t=regime, Y_{t-1}).
        transition_matrix : ndarray
            Transition matrix P, shape (k, k).
            P[i, j] = P(S_t=j | S_{t-1}=i).
        init_probs : ndarray, optional
            Initial state probabilities. If None, uses ergodic probabilities.

        Returns
        -------
        filtered_probs : ndarray
            Filtered probabilities P(S_t=j | Y_t), shape (T, k).
        predicted_probs : ndarray
            Predicted probabilities P(S_t=j | Y_{t-1}), shape (T, k).
        loglike : float
            Total log-likelihood sum_t log(f_t).
        marginal_loglike : ndarray
            Per-observation marginal log-likelihood log(f_t), shape (T,).
        """
        n_obs = len(endog) if endog.ndim == 1 else endog.shape[0]
        k = transition_matrix.shape[0]
        trans = transition_matrix

        if init_probs is None:
            init_probs = self.ergodic_probabilities(trans)

        filtered = np.zeros((n_obs, k))
        predicted = np.zeros((n_obs, k))
        marginal_ll = np.zeros(n_obs)

        xi = init_probs.copy()

        for t in range(n_obs):
            # --- Prediction step ---
            # xi_{t|t-1} = P' * xi_{t-1|t-1}
            xi_pred = trans.T @ xi
            # Ensure non-negative and sum to 1
            xi_pred = np.maximum(xi_pred, 1e-300)
            xi_pred /= xi_pred.sum()
            predicted[t] = xi_pred

            # --- Regime likelihoods ---
            # eta_t(j) = f(y_t | S_t=j, Y_{t-1})
            log_eta = np.array([regime_loglike_fn(t, s) for s in range(k)])

            # Numerical stability: subtract max before exp
            max_log_eta = np.max(log_eta)
            eta = np.exp(log_eta - max_log_eta)

            # --- Update step ---
            # numerator = xi_{t|t-1} * eta_t
            num = xi_pred * eta
            f_t = num.sum()

            xi = np.ones(k) / k if f_t < 1e-300 else num / f_t

            filtered[t] = xi
            # log(f_t) = log(sum(xi_pred * exp(log_eta)))
            # = max_log_eta + log(sum(xi_pred * exp(log_eta - max_log_eta)))
            marginal_ll[t] = max_log_eta + np.log(max(f_t, 1e-300))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def filter_vectorized(
        self,
        regime_loglikes: NDArray[np.float64],
        transition_matrix: NDArray[np.float64],
        init_probs: NDArray[np.float64] | None = None,
    ) -> tuple[
        NDArray[np.float64],
        NDArray[np.float64],
        float,
        NDArray[np.float64],
    ]:
        """Run the Hamilton filter with pre-computed regime log-likelihoods.

        This is more efficient when all regime log-likelihoods are already
        computed as a (T, k) matrix.

        Parameters
        ----------
        regime_loglikes : ndarray
            Pre-computed log f(y_t | S_t=j), shape (T, k).
        transition_matrix : ndarray
            Transition matrix P, shape (k, k).
        init_probs : ndarray, optional
            Initial state probabilities.

        Returns
        -------
        filtered_probs : ndarray
            Shape (T, k).
        predicted_probs : ndarray
            Shape (T, k).
        loglike : float
            Total log-likelihood.
        marginal_loglike : ndarray
            Shape (T,).
        """
        n_obs, k = regime_loglikes.shape
        trans = transition_matrix

        if init_probs is None:
            init_probs = self.ergodic_probabilities(trans)

        filtered = np.zeros((n_obs, k))
        predicted = np.zeros((n_obs, k))
        marginal_ll = np.zeros(n_obs)

        xi = init_probs.copy()

        for t in range(n_obs):
            # Prediction
            xi_pred = trans.T @ xi
            xi_pred = np.maximum(xi_pred, 1e-300)
            xi_pred /= xi_pred.sum()
            predicted[t] = xi_pred

            # Regime likelihoods
            log_eta = regime_loglikes[t]
            max_log_eta = np.max(log_eta)
            eta = np.exp(log_eta - max_log_eta)

            # Update
            num = xi_pred * eta
            f_t = num.sum()

            xi = np.ones(k) / k if f_t < 1e-300 else num / f_t

            filtered[t] = xi
            marginal_ll[t] = max_log_eta + np.log(max(f_t, 1e-300))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    @staticmethod
    def ergodic_probabilities(
        transition_matrix: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute ergodic (stationary) probabilities of a Markov chain.

        Solves pi = P' * pi with sum(pi) = 1.

        Parameters
        ----------
        transition_matrix : ndarray
            Transition matrix P, shape (k, k).

        Returns
        -------
        ndarray
            Ergodic probabilities, shape (k,).
        """
        k = transition_matrix.shape[0]
        trans = transition_matrix

        # System: (P' - I) * pi = 0, sum(pi) = 1
        # Stack: A = [P' - I; ones], b = [0, ..., 0, 1]
        coeff = np.vstack([trans.T - np.eye(k), np.ones(k)])
        b = np.zeros(k + 1)
        b[-1] = 1.0

        pi = np.linalg.lstsq(coeff, b, rcond=None)[0]

        # Ensure valid probability vector
        pi = np.maximum(pi, 0.0)
        total = pi.sum()
        if total > 0:
            pi /= total
        else:
            pi = np.ones(k) / k

        return pi
