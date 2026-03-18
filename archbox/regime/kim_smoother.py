"""Kim Smoother for Markov-Switching models.

Implements the backward smoothing algorithm from Kim (1994) for computing
smoothed probabilities P(S_t=j | Y_T) using the full sample.

References
----------
Kim, C.-J. (1994). Dynamic Linear Models with Markov-Switching.
Journal of Econometrics, 60(1-2), 1-22.

Kim, C.-J. & Nelson, C.R. (1999). State-Space Models with Regime Switching.
MIT Press.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


class KimSmoother:
    """Kim Smoother for Markov-Switching models.

    Computes smoothed probabilities P(S_t=j | Y_T) via backward recursion
    from filtered and predicted probabilities.
    """

    def smooth(
        self,
        filtered_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        transition_matrix: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute smoothed probabilities via backward recursion.

        Parameters
        ----------
        filtered_probs : ndarray
            Filtered probabilities P(S_t=j | Y_t), shape (T, k).
        predicted_probs : ndarray
            Predicted probabilities P(S_t=j | Y_{t-1}), shape (T, k).
        transition_matrix : ndarray
            Transition matrix P, shape (k, k).
            P[i, j] = P(S_t=j | S_{t-1}=i).

        Returns
        -------
        ndarray
            Smoothed probabilities P(S_t=j | Y_T), shape (T, k).
        """
        n_obs, k = filtered_probs.shape
        trans = transition_matrix
        smoothed = np.zeros((n_obs, k))

        # Last point: smoothed = filtered
        smoothed[-1] = filtered_probs[-1]

        # Backward recursion: t = T-2, T-3, ..., 0
        for t in range(n_obs - 2, -1, -1):
            for i in range(k):
                s = 0.0
                for j in range(k):
                    pred_j = max(predicted_probs[t + 1, j], 1e-300)
                    s += filtered_probs[t, i] * trans[i, j] * smoothed[t + 1, j] / pred_j
                smoothed[t, i] = s

            # Ensure valid probabilities
            row_sum = smoothed[t].sum()
            if row_sum > 0:
                smoothed[t] /= row_sum
            else:
                smoothed[t] = np.ones(k) / k

        return smoothed

    def smooth_vectorized(
        self,
        filtered_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        transition_matrix: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute smoothed probabilities (vectorized version).

        Same algorithm as smooth() but using matrix operations
        instead of explicit loops over regimes.

        Parameters
        ----------
        filtered_probs : ndarray
            Shape (T, k).
        predicted_probs : ndarray
            Shape (T, k).
        transition_matrix : ndarray
            Shape (k, k).

        Returns
        -------
        ndarray
            Smoothed probabilities, shape (T, k).
        """
        n_obs, k = filtered_probs.shape
        trans = transition_matrix
        smoothed = np.zeros((n_obs, k))
        smoothed[-1] = filtered_probs[-1]

        for t in range(n_obs - 2, -1, -1):
            # ratio(j) = smoothed[t+1, j] / predicted[t+1, j]
            pred_safe = np.maximum(predicted_probs[t + 1], 1e-300)
            ratio = smoothed[t + 1] / pred_safe  # (k,)

            # smoothed[t, i] = filtered[t, i] * sum_j(P[i,j] * ratio[j])
            correction = trans @ ratio  # (k,)
            smoothed[t] = filtered_probs[t] * correction

            # Normalize
            row_sum = smoothed[t].sum()
            if row_sum > 0:
                smoothed[t] /= row_sum
            else:
                smoothed[t] = np.ones(k) / k

        return smoothed

    def joint_smoothed(
        self,
        filtered_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        transition_matrix: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Compute joint smoothed probabilities P(S_t=i, S_{t+1}=j | Y_T).

        Needed for the M-step of EM to update the transition matrix.

        Parameters
        ----------
        filtered_probs : ndarray
            Shape (T, k).
        predicted_probs : ndarray
            Shape (T, k).
        smoothed_probs : ndarray
            Shape (T, k).
        transition_matrix : ndarray
            Shape (k, k).

        Returns
        -------
        ndarray
            Joint smoothed probabilities, shape (T-1, k, k).
            joint[t, i, j] = P(S_t=i, S_{t+1}=j | Y_T) for t=0..T-2.
        """
        n_obs, k = filtered_probs.shape
        trans = transition_matrix
        joint = np.zeros((n_obs - 1, k, k))

        for t in range(n_obs - 1):
            for i in range(k):
                for j in range(k):
                    pred_j = max(predicted_probs[t + 1, j], 1e-300)
                    joint[t, i, j] = (
                        filtered_probs[t, i] * trans[i, j] * smoothed_probs[t + 1, j] / pred_j
                    )

            # Normalize so that sum over i,j = 1
            total = joint[t].sum()
            if total > 0:
                joint[t] /= total

        return joint
