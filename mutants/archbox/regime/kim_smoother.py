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

from collections.abc import Callable
from typing import Annotated, ClassVar

import numpy as np
from numpy.typing import NDArray

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
        args = [filtered_probs, predicted_probs, transition_matrix]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁKimSmootherǁsmooth__mutmut_orig"),
            object.__getattribute__(self, "xǁKimSmootherǁsmooth__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁKimSmootherǁsmooth__mutmut_orig(
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

    def xǁKimSmootherǁsmooth__mutmut_1(
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
        n_obs, k = None
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

    def xǁKimSmootherǁsmooth__mutmut_2(
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
        trans = None
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

    def xǁKimSmootherǁsmooth__mutmut_3(
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
        smoothed = None

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

    def xǁKimSmootherǁsmooth__mutmut_4(
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
        smoothed = np.zeros(None)

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

    def xǁKimSmootherǁsmooth__mutmut_5(
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
        smoothed[-1] = None

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

    def xǁKimSmootherǁsmooth__mutmut_6(
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
        smoothed[+1] = filtered_probs[-1]

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

    def xǁKimSmootherǁsmooth__mutmut_7(
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
        smoothed[-2] = filtered_probs[-1]

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

    def xǁKimSmootherǁsmooth__mutmut_8(
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
        smoothed[-1] = filtered_probs[+1]

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

    def xǁKimSmootherǁsmooth__mutmut_9(
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
        smoothed[-1] = filtered_probs[-2]

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

    def xǁKimSmootherǁsmooth__mutmut_10(
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
        for t in range(None, -1, -1):
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

    def xǁKimSmootherǁsmooth__mutmut_11(
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
        for t in range(n_obs - 2, None, -1):
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

    def xǁKimSmootherǁsmooth__mutmut_12(
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
        for t in range(n_obs - 2, -1, None):
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

    def xǁKimSmootherǁsmooth__mutmut_13(
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
        for t in range(-1, -1):
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

    def xǁKimSmootherǁsmooth__mutmut_14(
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
        for t in range(n_obs - 2, -1):
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

    def xǁKimSmootherǁsmooth__mutmut_15(
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
        for t in range(
            n_obs - 2,
            -1,
        ):
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

    def xǁKimSmootherǁsmooth__mutmut_16(
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
        for t in range(n_obs + 2, -1, -1):
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

    def xǁKimSmootherǁsmooth__mutmut_17(
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
        for t in range(n_obs - 3, -1, -1):
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

    def xǁKimSmootherǁsmooth__mutmut_18(
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
        for t in range(n_obs - 2, +1, -1):
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

    def xǁKimSmootherǁsmooth__mutmut_19(
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
        for t in range(n_obs - 2, -2, -1):
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

    def xǁKimSmootherǁsmooth__mutmut_20(
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
        for t in range(n_obs - 2, -1, +1):
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

    def xǁKimSmootherǁsmooth__mutmut_21(
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
        for t in range(n_obs - 2, -1, -2):
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

    def xǁKimSmootherǁsmooth__mutmut_22(
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
            for i in range(None):
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

    def xǁKimSmootherǁsmooth__mutmut_23(
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
                s = None
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

    def xǁKimSmootherǁsmooth__mutmut_24(
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
                s = 1.0
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

    def xǁKimSmootherǁsmooth__mutmut_25(
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
                for j in range(None):
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

    def xǁKimSmootherǁsmooth__mutmut_26(
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
                    pred_j = None
                    s += filtered_probs[t, i] * trans[i, j] * smoothed[t + 1, j] / pred_j
                smoothed[t, i] = s

            # Ensure valid probabilities
            row_sum = smoothed[t].sum()
            if row_sum > 0:
                smoothed[t] /= row_sum
            else:
                smoothed[t] = np.ones(k) / k

        return smoothed

    def xǁKimSmootherǁsmooth__mutmut_27(
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
                    pred_j = max(None, 1e-300)
                    s += filtered_probs[t, i] * trans[i, j] * smoothed[t + 1, j] / pred_j
                smoothed[t, i] = s

            # Ensure valid probabilities
            row_sum = smoothed[t].sum()
            if row_sum > 0:
                smoothed[t] /= row_sum
            else:
                smoothed[t] = np.ones(k) / k

        return smoothed

    def xǁKimSmootherǁsmooth__mutmut_28(
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
                    pred_j = max(predicted_probs[t + 1, j], None)
                    s += filtered_probs[t, i] * trans[i, j] * smoothed[t + 1, j] / pred_j
                smoothed[t, i] = s

            # Ensure valid probabilities
            row_sum = smoothed[t].sum()
            if row_sum > 0:
                smoothed[t] /= row_sum
            else:
                smoothed[t] = np.ones(k) / k

        return smoothed

    def xǁKimSmootherǁsmooth__mutmut_29(
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
                    pred_j = max(1e-300)
                    s += filtered_probs[t, i] * trans[i, j] * smoothed[t + 1, j] / pred_j
                smoothed[t, i] = s

            # Ensure valid probabilities
            row_sum = smoothed[t].sum()
            if row_sum > 0:
                smoothed[t] /= row_sum
            else:
                smoothed[t] = np.ones(k) / k

        return smoothed

    def xǁKimSmootherǁsmooth__mutmut_30(
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
                    pred_j = max(
                        predicted_probs[t + 1, j],
                    )
                    s += filtered_probs[t, i] * trans[i, j] * smoothed[t + 1, j] / pred_j
                smoothed[t, i] = s

            # Ensure valid probabilities
            row_sum = smoothed[t].sum()
            if row_sum > 0:
                smoothed[t] /= row_sum
            else:
                smoothed[t] = np.ones(k) / k

        return smoothed

    def xǁKimSmootherǁsmooth__mutmut_31(
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
                    pred_j = max(predicted_probs[t - 1, j], 1e-300)
                    s += filtered_probs[t, i] * trans[i, j] * smoothed[t + 1, j] / pred_j
                smoothed[t, i] = s

            # Ensure valid probabilities
            row_sum = smoothed[t].sum()
            if row_sum > 0:
                smoothed[t] /= row_sum
            else:
                smoothed[t] = np.ones(k) / k

        return smoothed

    def xǁKimSmootherǁsmooth__mutmut_32(
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
                    pred_j = max(predicted_probs[t + 2, j], 1e-300)
                    s += filtered_probs[t, i] * trans[i, j] * smoothed[t + 1, j] / pred_j
                smoothed[t, i] = s

            # Ensure valid probabilities
            row_sum = smoothed[t].sum()
            if row_sum > 0:
                smoothed[t] /= row_sum
            else:
                smoothed[t] = np.ones(k) / k

        return smoothed

    def xǁKimSmootherǁsmooth__mutmut_33(
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
                    pred_j = max(predicted_probs[t + 1, j], 1.0)
                    s += filtered_probs[t, i] * trans[i, j] * smoothed[t + 1, j] / pred_j
                smoothed[t, i] = s

            # Ensure valid probabilities
            row_sum = smoothed[t].sum()
            if row_sum > 0:
                smoothed[t] /= row_sum
            else:
                smoothed[t] = np.ones(k) / k

        return smoothed

    def xǁKimSmootherǁsmooth__mutmut_34(
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
                    s = filtered_probs[t, i] * trans[i, j] * smoothed[t + 1, j] / pred_j
                smoothed[t, i] = s

            # Ensure valid probabilities
            row_sum = smoothed[t].sum()
            if row_sum > 0:
                smoothed[t] /= row_sum
            else:
                smoothed[t] = np.ones(k) / k

        return smoothed

    def xǁKimSmootherǁsmooth__mutmut_35(
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
                    s -= filtered_probs[t, i] * trans[i, j] * smoothed[t + 1, j] / pred_j
                smoothed[t, i] = s

            # Ensure valid probabilities
            row_sum = smoothed[t].sum()
            if row_sum > 0:
                smoothed[t] /= row_sum
            else:
                smoothed[t] = np.ones(k) / k

        return smoothed

    def xǁKimSmootherǁsmooth__mutmut_36(
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
                    s += filtered_probs[t, i] * trans[i, j] * smoothed[t + 1, j] * pred_j
                smoothed[t, i] = s

            # Ensure valid probabilities
            row_sum = smoothed[t].sum()
            if row_sum > 0:
                smoothed[t] /= row_sum
            else:
                smoothed[t] = np.ones(k) / k

        return smoothed

    def xǁKimSmootherǁsmooth__mutmut_37(
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
                    s += filtered_probs[t, i] * trans[i, j] / smoothed[t + 1, j] / pred_j
                smoothed[t, i] = s

            # Ensure valid probabilities
            row_sum = smoothed[t].sum()
            if row_sum > 0:
                smoothed[t] /= row_sum
            else:
                smoothed[t] = np.ones(k) / k

        return smoothed

    def xǁKimSmootherǁsmooth__mutmut_38(
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
                    s += filtered_probs[t, i] / trans[i, j] * smoothed[t + 1, j] / pred_j
                smoothed[t, i] = s

            # Ensure valid probabilities
            row_sum = smoothed[t].sum()
            if row_sum > 0:
                smoothed[t] /= row_sum
            else:
                smoothed[t] = np.ones(k) / k

        return smoothed

    def xǁKimSmootherǁsmooth__mutmut_39(
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
                    s += filtered_probs[t, i] * trans[i, j] * smoothed[t - 1, j] / pred_j
                smoothed[t, i] = s

            # Ensure valid probabilities
            row_sum = smoothed[t].sum()
            if row_sum > 0:
                smoothed[t] /= row_sum
            else:
                smoothed[t] = np.ones(k) / k

        return smoothed

    def xǁKimSmootherǁsmooth__mutmut_40(
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
                    s += filtered_probs[t, i] * trans[i, j] * smoothed[t + 2, j] / pred_j
                smoothed[t, i] = s

            # Ensure valid probabilities
            row_sum = smoothed[t].sum()
            if row_sum > 0:
                smoothed[t] /= row_sum
            else:
                smoothed[t] = np.ones(k) / k

        return smoothed

    def xǁKimSmootherǁsmooth__mutmut_41(
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
                smoothed[t, i] = None

            # Ensure valid probabilities
            row_sum = smoothed[t].sum()
            if row_sum > 0:
                smoothed[t] /= row_sum
            else:
                smoothed[t] = np.ones(k) / k

        return smoothed

    def xǁKimSmootherǁsmooth__mutmut_42(
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
            row_sum = None
            if row_sum > 0:
                smoothed[t] /= row_sum
            else:
                smoothed[t] = np.ones(k) / k

        return smoothed

    def xǁKimSmootherǁsmooth__mutmut_43(
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
            if row_sum >= 0:
                smoothed[t] /= row_sum
            else:
                smoothed[t] = np.ones(k) / k

        return smoothed

    def xǁKimSmootherǁsmooth__mutmut_44(
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
            if row_sum > 1:
                smoothed[t] /= row_sum
            else:
                smoothed[t] = np.ones(k) / k

        return smoothed

    def xǁKimSmootherǁsmooth__mutmut_45(
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
                smoothed[t] = row_sum
            else:
                smoothed[t] = np.ones(k) / k

        return smoothed

    def xǁKimSmootherǁsmooth__mutmut_46(
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
                smoothed[t] *= row_sum
            else:
                smoothed[t] = np.ones(k) / k

        return smoothed

    def xǁKimSmootherǁsmooth__mutmut_47(
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
                smoothed[t] = None

        return smoothed

    def xǁKimSmootherǁsmooth__mutmut_48(
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
                smoothed[t] = np.ones(k) * k

        return smoothed

    def xǁKimSmootherǁsmooth__mutmut_49(
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
                smoothed[t] = np.ones(None) / k

        return smoothed

    xǁKimSmootherǁsmooth__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁKimSmootherǁsmooth__mutmut_1": xǁKimSmootherǁsmooth__mutmut_1,
        "xǁKimSmootherǁsmooth__mutmut_2": xǁKimSmootherǁsmooth__mutmut_2,
        "xǁKimSmootherǁsmooth__mutmut_3": xǁKimSmootherǁsmooth__mutmut_3,
        "xǁKimSmootherǁsmooth__mutmut_4": xǁKimSmootherǁsmooth__mutmut_4,
        "xǁKimSmootherǁsmooth__mutmut_5": xǁKimSmootherǁsmooth__mutmut_5,
        "xǁKimSmootherǁsmooth__mutmut_6": xǁKimSmootherǁsmooth__mutmut_6,
        "xǁKimSmootherǁsmooth__mutmut_7": xǁKimSmootherǁsmooth__mutmut_7,
        "xǁKimSmootherǁsmooth__mutmut_8": xǁKimSmootherǁsmooth__mutmut_8,
        "xǁKimSmootherǁsmooth__mutmut_9": xǁKimSmootherǁsmooth__mutmut_9,
        "xǁKimSmootherǁsmooth__mutmut_10": xǁKimSmootherǁsmooth__mutmut_10,
        "xǁKimSmootherǁsmooth__mutmut_11": xǁKimSmootherǁsmooth__mutmut_11,
        "xǁKimSmootherǁsmooth__mutmut_12": xǁKimSmootherǁsmooth__mutmut_12,
        "xǁKimSmootherǁsmooth__mutmut_13": xǁKimSmootherǁsmooth__mutmut_13,
        "xǁKimSmootherǁsmooth__mutmut_14": xǁKimSmootherǁsmooth__mutmut_14,
        "xǁKimSmootherǁsmooth__mutmut_15": xǁKimSmootherǁsmooth__mutmut_15,
        "xǁKimSmootherǁsmooth__mutmut_16": xǁKimSmootherǁsmooth__mutmut_16,
        "xǁKimSmootherǁsmooth__mutmut_17": xǁKimSmootherǁsmooth__mutmut_17,
        "xǁKimSmootherǁsmooth__mutmut_18": xǁKimSmootherǁsmooth__mutmut_18,
        "xǁKimSmootherǁsmooth__mutmut_19": xǁKimSmootherǁsmooth__mutmut_19,
        "xǁKimSmootherǁsmooth__mutmut_20": xǁKimSmootherǁsmooth__mutmut_20,
        "xǁKimSmootherǁsmooth__mutmut_21": xǁKimSmootherǁsmooth__mutmut_21,
        "xǁKimSmootherǁsmooth__mutmut_22": xǁKimSmootherǁsmooth__mutmut_22,
        "xǁKimSmootherǁsmooth__mutmut_23": xǁKimSmootherǁsmooth__mutmut_23,
        "xǁKimSmootherǁsmooth__mutmut_24": xǁKimSmootherǁsmooth__mutmut_24,
        "xǁKimSmootherǁsmooth__mutmut_25": xǁKimSmootherǁsmooth__mutmut_25,
        "xǁKimSmootherǁsmooth__mutmut_26": xǁKimSmootherǁsmooth__mutmut_26,
        "xǁKimSmootherǁsmooth__mutmut_27": xǁKimSmootherǁsmooth__mutmut_27,
        "xǁKimSmootherǁsmooth__mutmut_28": xǁKimSmootherǁsmooth__mutmut_28,
        "xǁKimSmootherǁsmooth__mutmut_29": xǁKimSmootherǁsmooth__mutmut_29,
        "xǁKimSmootherǁsmooth__mutmut_30": xǁKimSmootherǁsmooth__mutmut_30,
        "xǁKimSmootherǁsmooth__mutmut_31": xǁKimSmootherǁsmooth__mutmut_31,
        "xǁKimSmootherǁsmooth__mutmut_32": xǁKimSmootherǁsmooth__mutmut_32,
        "xǁKimSmootherǁsmooth__mutmut_33": xǁKimSmootherǁsmooth__mutmut_33,
        "xǁKimSmootherǁsmooth__mutmut_34": xǁKimSmootherǁsmooth__mutmut_34,
        "xǁKimSmootherǁsmooth__mutmut_35": xǁKimSmootherǁsmooth__mutmut_35,
        "xǁKimSmootherǁsmooth__mutmut_36": xǁKimSmootherǁsmooth__mutmut_36,
        "xǁKimSmootherǁsmooth__mutmut_37": xǁKimSmootherǁsmooth__mutmut_37,
        "xǁKimSmootherǁsmooth__mutmut_38": xǁKimSmootherǁsmooth__mutmut_38,
        "xǁKimSmootherǁsmooth__mutmut_39": xǁKimSmootherǁsmooth__mutmut_39,
        "xǁKimSmootherǁsmooth__mutmut_40": xǁKimSmootherǁsmooth__mutmut_40,
        "xǁKimSmootherǁsmooth__mutmut_41": xǁKimSmootherǁsmooth__mutmut_41,
        "xǁKimSmootherǁsmooth__mutmut_42": xǁKimSmootherǁsmooth__mutmut_42,
        "xǁKimSmootherǁsmooth__mutmut_43": xǁKimSmootherǁsmooth__mutmut_43,
        "xǁKimSmootherǁsmooth__mutmut_44": xǁKimSmootherǁsmooth__mutmut_44,
        "xǁKimSmootherǁsmooth__mutmut_45": xǁKimSmootherǁsmooth__mutmut_45,
        "xǁKimSmootherǁsmooth__mutmut_46": xǁKimSmootherǁsmooth__mutmut_46,
        "xǁKimSmootherǁsmooth__mutmut_47": xǁKimSmootherǁsmooth__mutmut_47,
        "xǁKimSmootherǁsmooth__mutmut_48": xǁKimSmootherǁsmooth__mutmut_48,
        "xǁKimSmootherǁsmooth__mutmut_49": xǁKimSmootherǁsmooth__mutmut_49,
    }
    xǁKimSmootherǁsmooth__mutmut_orig.__name__ = "xǁKimSmootherǁsmooth"

    def smooth_vectorized(
        self,
        filtered_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        transition_matrix: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        args = [filtered_probs, predicted_probs, transition_matrix]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁKimSmootherǁsmooth_vectorized__mutmut_orig"),
            object.__getattribute__(self, "xǁKimSmootherǁsmooth_vectorized__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁKimSmootherǁsmooth_vectorized__mutmut_orig(
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

    def xǁKimSmootherǁsmooth_vectorized__mutmut_1(
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
        n_obs, k = None
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

    def xǁKimSmootherǁsmooth_vectorized__mutmut_2(
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
        trans = None
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

    def xǁKimSmootherǁsmooth_vectorized__mutmut_3(
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
        smoothed = None
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

    def xǁKimSmootherǁsmooth_vectorized__mutmut_4(
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
        smoothed = np.zeros(None)
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

    def xǁKimSmootherǁsmooth_vectorized__mutmut_5(
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
        smoothed[-1] = None

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

    def xǁKimSmootherǁsmooth_vectorized__mutmut_6(
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
        smoothed[+1] = filtered_probs[-1]

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

    def xǁKimSmootherǁsmooth_vectorized__mutmut_7(
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
        smoothed[-2] = filtered_probs[-1]

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

    def xǁKimSmootherǁsmooth_vectorized__mutmut_8(
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
        smoothed[-1] = filtered_probs[+1]

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

    def xǁKimSmootherǁsmooth_vectorized__mutmut_9(
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
        smoothed[-1] = filtered_probs[-2]

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

    def xǁKimSmootherǁsmooth_vectorized__mutmut_10(
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

        for t in range(None, -1, -1):
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

    def xǁKimSmootherǁsmooth_vectorized__mutmut_11(
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

        for t in range(n_obs - 2, None, -1):
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

    def xǁKimSmootherǁsmooth_vectorized__mutmut_12(
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

        for t in range(n_obs - 2, -1, None):
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

    def xǁKimSmootherǁsmooth_vectorized__mutmut_13(
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

        for t in range(-1, -1):
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

    def xǁKimSmootherǁsmooth_vectorized__mutmut_14(
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

        for t in range(n_obs - 2, -1):
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

    def xǁKimSmootherǁsmooth_vectorized__mutmut_15(
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

        for t in range(
            n_obs - 2,
            -1,
        ):
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

    def xǁKimSmootherǁsmooth_vectorized__mutmut_16(
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

        for t in range(n_obs + 2, -1, -1):
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

    def xǁKimSmootherǁsmooth_vectorized__mutmut_17(
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

        for t in range(n_obs - 3, -1, -1):
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

    def xǁKimSmootherǁsmooth_vectorized__mutmut_18(
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

        for t in range(n_obs - 2, +1, -1):
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

    def xǁKimSmootherǁsmooth_vectorized__mutmut_19(
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

        for t in range(n_obs - 2, -2, -1):
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

    def xǁKimSmootherǁsmooth_vectorized__mutmut_20(
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

        for t in range(n_obs - 2, -1, +1):
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

    def xǁKimSmootherǁsmooth_vectorized__mutmut_21(
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

        for t in range(n_obs - 2, -1, -2):
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

    def xǁKimSmootherǁsmooth_vectorized__mutmut_22(
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
            pred_safe = None
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

    def xǁKimSmootherǁsmooth_vectorized__mutmut_23(
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
            pred_safe = np.maximum(None, 1e-300)
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

    def xǁKimSmootherǁsmooth_vectorized__mutmut_24(
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
            pred_safe = np.maximum(predicted_probs[t + 1], None)
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

    def xǁKimSmootherǁsmooth_vectorized__mutmut_25(
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
            pred_safe = np.maximum(1e-300)
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

    def xǁKimSmootherǁsmooth_vectorized__mutmut_26(
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
            pred_safe = np.maximum(
                predicted_probs[t + 1],
            )
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

    def xǁKimSmootherǁsmooth_vectorized__mutmut_27(
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
            pred_safe = np.maximum(predicted_probs[t - 1], 1e-300)
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

    def xǁKimSmootherǁsmooth_vectorized__mutmut_28(
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
            pred_safe = np.maximum(predicted_probs[t + 2], 1e-300)
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

    def xǁKimSmootherǁsmooth_vectorized__mutmut_29(
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
            pred_safe = np.maximum(predicted_probs[t + 1], 1.0)
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

    def xǁKimSmootherǁsmooth_vectorized__mutmut_30(
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
            ratio = None  # (k,)

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

    def xǁKimSmootherǁsmooth_vectorized__mutmut_31(
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
            ratio = smoothed[t + 1] * pred_safe  # (k,)

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

    def xǁKimSmootherǁsmooth_vectorized__mutmut_32(
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
            ratio = smoothed[t - 1] / pred_safe  # (k,)

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

    def xǁKimSmootherǁsmooth_vectorized__mutmut_33(
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
            ratio = smoothed[t + 2] / pred_safe  # (k,)

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

    def xǁKimSmootherǁsmooth_vectorized__mutmut_34(
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
            correction = None  # (k,)
            smoothed[t] = filtered_probs[t] * correction

            # Normalize
            row_sum = smoothed[t].sum()
            if row_sum > 0:
                smoothed[t] /= row_sum
            else:
                smoothed[t] = np.ones(k) / k

        return smoothed

    def xǁKimSmootherǁsmooth_vectorized__mutmut_35(
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
            smoothed[t] = None

            # Normalize
            row_sum = smoothed[t].sum()
            if row_sum > 0:
                smoothed[t] /= row_sum
            else:
                smoothed[t] = np.ones(k) / k

        return smoothed

    def xǁKimSmootherǁsmooth_vectorized__mutmut_36(
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
            smoothed[t] = filtered_probs[t] / correction

            # Normalize
            row_sum = smoothed[t].sum()
            if row_sum > 0:
                smoothed[t] /= row_sum
            else:
                smoothed[t] = np.ones(k) / k

        return smoothed

    def xǁKimSmootherǁsmooth_vectorized__mutmut_37(
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
            row_sum = None
            if row_sum > 0:
                smoothed[t] /= row_sum
            else:
                smoothed[t] = np.ones(k) / k

        return smoothed

    def xǁKimSmootherǁsmooth_vectorized__mutmut_38(
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
            if row_sum >= 0:
                smoothed[t] /= row_sum
            else:
                smoothed[t] = np.ones(k) / k

        return smoothed

    def xǁKimSmootherǁsmooth_vectorized__mutmut_39(
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
            if row_sum > 1:
                smoothed[t] /= row_sum
            else:
                smoothed[t] = np.ones(k) / k

        return smoothed

    def xǁKimSmootherǁsmooth_vectorized__mutmut_40(
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
                smoothed[t] = row_sum
            else:
                smoothed[t] = np.ones(k) / k

        return smoothed

    def xǁKimSmootherǁsmooth_vectorized__mutmut_41(
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
                smoothed[t] *= row_sum
            else:
                smoothed[t] = np.ones(k) / k

        return smoothed

    def xǁKimSmootherǁsmooth_vectorized__mutmut_42(
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
                smoothed[t] = None

        return smoothed

    def xǁKimSmootherǁsmooth_vectorized__mutmut_43(
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
                smoothed[t] = np.ones(k) * k

        return smoothed

    def xǁKimSmootherǁsmooth_vectorized__mutmut_44(
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
                smoothed[t] = np.ones(None) / k

        return smoothed

    xǁKimSmootherǁsmooth_vectorized__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁKimSmootherǁsmooth_vectorized__mutmut_1": xǁKimSmootherǁsmooth_vectorized__mutmut_1,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_2": xǁKimSmootherǁsmooth_vectorized__mutmut_2,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_3": xǁKimSmootherǁsmooth_vectorized__mutmut_3,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_4": xǁKimSmootherǁsmooth_vectorized__mutmut_4,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_5": xǁKimSmootherǁsmooth_vectorized__mutmut_5,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_6": xǁKimSmootherǁsmooth_vectorized__mutmut_6,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_7": xǁKimSmootherǁsmooth_vectorized__mutmut_7,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_8": xǁKimSmootherǁsmooth_vectorized__mutmut_8,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_9": xǁKimSmootherǁsmooth_vectorized__mutmut_9,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_10": xǁKimSmootherǁsmooth_vectorized__mutmut_10,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_11": xǁKimSmootherǁsmooth_vectorized__mutmut_11,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_12": xǁKimSmootherǁsmooth_vectorized__mutmut_12,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_13": xǁKimSmootherǁsmooth_vectorized__mutmut_13,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_14": xǁKimSmootherǁsmooth_vectorized__mutmut_14,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_15": xǁKimSmootherǁsmooth_vectorized__mutmut_15,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_16": xǁKimSmootherǁsmooth_vectorized__mutmut_16,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_17": xǁKimSmootherǁsmooth_vectorized__mutmut_17,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_18": xǁKimSmootherǁsmooth_vectorized__mutmut_18,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_19": xǁKimSmootherǁsmooth_vectorized__mutmut_19,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_20": xǁKimSmootherǁsmooth_vectorized__mutmut_20,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_21": xǁKimSmootherǁsmooth_vectorized__mutmut_21,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_22": xǁKimSmootherǁsmooth_vectorized__mutmut_22,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_23": xǁKimSmootherǁsmooth_vectorized__mutmut_23,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_24": xǁKimSmootherǁsmooth_vectorized__mutmut_24,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_25": xǁKimSmootherǁsmooth_vectorized__mutmut_25,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_26": xǁKimSmootherǁsmooth_vectorized__mutmut_26,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_27": xǁKimSmootherǁsmooth_vectorized__mutmut_27,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_28": xǁKimSmootherǁsmooth_vectorized__mutmut_28,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_29": xǁKimSmootherǁsmooth_vectorized__mutmut_29,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_30": xǁKimSmootherǁsmooth_vectorized__mutmut_30,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_31": xǁKimSmootherǁsmooth_vectorized__mutmut_31,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_32": xǁKimSmootherǁsmooth_vectorized__mutmut_32,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_33": xǁKimSmootherǁsmooth_vectorized__mutmut_33,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_34": xǁKimSmootherǁsmooth_vectorized__mutmut_34,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_35": xǁKimSmootherǁsmooth_vectorized__mutmut_35,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_36": xǁKimSmootherǁsmooth_vectorized__mutmut_36,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_37": xǁKimSmootherǁsmooth_vectorized__mutmut_37,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_38": xǁKimSmootherǁsmooth_vectorized__mutmut_38,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_39": xǁKimSmootherǁsmooth_vectorized__mutmut_39,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_40": xǁKimSmootherǁsmooth_vectorized__mutmut_40,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_41": xǁKimSmootherǁsmooth_vectorized__mutmut_41,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_42": xǁKimSmootherǁsmooth_vectorized__mutmut_42,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_43": xǁKimSmootherǁsmooth_vectorized__mutmut_43,
        "xǁKimSmootherǁsmooth_vectorized__mutmut_44": xǁKimSmootherǁsmooth_vectorized__mutmut_44,
    }
    xǁKimSmootherǁsmooth_vectorized__mutmut_orig.__name__ = "xǁKimSmootherǁsmooth_vectorized"

    def joint_smoothed(
        self,
        filtered_probs: NDArray[np.float64],
        predicted_probs: NDArray[np.float64],
        smoothed_probs: NDArray[np.float64],
        transition_matrix: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        args = [filtered_probs, predicted_probs, smoothed_probs, transition_matrix]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁKimSmootherǁjoint_smoothed__mutmut_orig"),
            object.__getattribute__(self, "xǁKimSmootherǁjoint_smoothed__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁKimSmootherǁjoint_smoothed__mutmut_orig(
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

    def xǁKimSmootherǁjoint_smoothed__mutmut_1(
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
        n_obs, k = None
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

    def xǁKimSmootherǁjoint_smoothed__mutmut_2(
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
        trans = None
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

    def xǁKimSmootherǁjoint_smoothed__mutmut_3(
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
        joint = None

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

    def xǁKimSmootherǁjoint_smoothed__mutmut_4(
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
        joint = np.zeros(None)

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

    def xǁKimSmootherǁjoint_smoothed__mutmut_5(
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
        joint = np.zeros((n_obs + 1, k, k))

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

    def xǁKimSmootherǁjoint_smoothed__mutmut_6(
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
        joint = np.zeros((n_obs - 2, k, k))

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

    def xǁKimSmootherǁjoint_smoothed__mutmut_7(
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

        for t in range(None):
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

    def xǁKimSmootherǁjoint_smoothed__mutmut_8(
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

        for t in range(n_obs + 1):
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

    def xǁKimSmootherǁjoint_smoothed__mutmut_9(
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

        for t in range(n_obs - 2):
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

    def xǁKimSmootherǁjoint_smoothed__mutmut_10(
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
            for i in range(None):
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

    def xǁKimSmootherǁjoint_smoothed__mutmut_11(
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
                for j in range(None):
                    pred_j = max(predicted_probs[t + 1, j], 1e-300)
                    joint[t, i, j] = (
                        filtered_probs[t, i] * trans[i, j] * smoothed_probs[t + 1, j] / pred_j
                    )

            # Normalize so that sum over i,j = 1
            total = joint[t].sum()
            if total > 0:
                joint[t] /= total

        return joint

    def xǁKimSmootherǁjoint_smoothed__mutmut_12(
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
                    pred_j = None
                    joint[t, i, j] = (
                        filtered_probs[t, i] * trans[i, j] * smoothed_probs[t + 1, j] / pred_j
                    )

            # Normalize so that sum over i,j = 1
            total = joint[t].sum()
            if total > 0:
                joint[t] /= total

        return joint

    def xǁKimSmootherǁjoint_smoothed__mutmut_13(
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
                    pred_j = max(None, 1e-300)
                    joint[t, i, j] = (
                        filtered_probs[t, i] * trans[i, j] * smoothed_probs[t + 1, j] / pred_j
                    )

            # Normalize so that sum over i,j = 1
            total = joint[t].sum()
            if total > 0:
                joint[t] /= total

        return joint

    def xǁKimSmootherǁjoint_smoothed__mutmut_14(
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
                    pred_j = max(predicted_probs[t + 1, j], None)
                    joint[t, i, j] = (
                        filtered_probs[t, i] * trans[i, j] * smoothed_probs[t + 1, j] / pred_j
                    )

            # Normalize so that sum over i,j = 1
            total = joint[t].sum()
            if total > 0:
                joint[t] /= total

        return joint

    def xǁKimSmootherǁjoint_smoothed__mutmut_15(
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
                    pred_j = max(1e-300)
                    joint[t, i, j] = (
                        filtered_probs[t, i] * trans[i, j] * smoothed_probs[t + 1, j] / pred_j
                    )

            # Normalize so that sum over i,j = 1
            total = joint[t].sum()
            if total > 0:
                joint[t] /= total

        return joint

    def xǁKimSmootherǁjoint_smoothed__mutmut_16(
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
                    pred_j = max(
                        predicted_probs[t + 1, j],
                    )
                    joint[t, i, j] = (
                        filtered_probs[t, i] * trans[i, j] * smoothed_probs[t + 1, j] / pred_j
                    )

            # Normalize so that sum over i,j = 1
            total = joint[t].sum()
            if total > 0:
                joint[t] /= total

        return joint

    def xǁKimSmootherǁjoint_smoothed__mutmut_17(
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
                    pred_j = max(predicted_probs[t - 1, j], 1e-300)
                    joint[t, i, j] = (
                        filtered_probs[t, i] * trans[i, j] * smoothed_probs[t + 1, j] / pred_j
                    )

            # Normalize so that sum over i,j = 1
            total = joint[t].sum()
            if total > 0:
                joint[t] /= total

        return joint

    def xǁKimSmootherǁjoint_smoothed__mutmut_18(
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
                    pred_j = max(predicted_probs[t + 2, j], 1e-300)
                    joint[t, i, j] = (
                        filtered_probs[t, i] * trans[i, j] * smoothed_probs[t + 1, j] / pred_j
                    )

            # Normalize so that sum over i,j = 1
            total = joint[t].sum()
            if total > 0:
                joint[t] /= total

        return joint

    def xǁKimSmootherǁjoint_smoothed__mutmut_19(
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
                    pred_j = max(predicted_probs[t + 1, j], 1.0)
                    joint[t, i, j] = (
                        filtered_probs[t, i] * trans[i, j] * smoothed_probs[t + 1, j] / pred_j
                    )

            # Normalize so that sum over i,j = 1
            total = joint[t].sum()
            if total > 0:
                joint[t] /= total

        return joint

    def xǁKimSmootherǁjoint_smoothed__mutmut_20(
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
                    joint[t, i, j] = None

            # Normalize so that sum over i,j = 1
            total = joint[t].sum()
            if total > 0:
                joint[t] /= total

        return joint

    def xǁKimSmootherǁjoint_smoothed__mutmut_21(
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
                        filtered_probs[t, i] * trans[i, j] * smoothed_probs[t + 1, j] * pred_j
                    )

            # Normalize so that sum over i,j = 1
            total = joint[t].sum()
            if total > 0:
                joint[t] /= total

        return joint

    def xǁKimSmootherǁjoint_smoothed__mutmut_22(
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
                        filtered_probs[t, i] * trans[i, j] / smoothed_probs[t + 1, j] / pred_j
                    )

            # Normalize so that sum over i,j = 1
            total = joint[t].sum()
            if total > 0:
                joint[t] /= total

        return joint

    def xǁKimSmootherǁjoint_smoothed__mutmut_23(
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
                        filtered_probs[t, i] / trans[i, j] * smoothed_probs[t + 1, j] / pred_j
                    )

            # Normalize so that sum over i,j = 1
            total = joint[t].sum()
            if total > 0:
                joint[t] /= total

        return joint

    def xǁKimSmootherǁjoint_smoothed__mutmut_24(
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
                        filtered_probs[t, i] * trans[i, j] * smoothed_probs[t - 1, j] / pred_j
                    )

            # Normalize so that sum over i,j = 1
            total = joint[t].sum()
            if total > 0:
                joint[t] /= total

        return joint

    def xǁKimSmootherǁjoint_smoothed__mutmut_25(
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
                        filtered_probs[t, i] * trans[i, j] * smoothed_probs[t + 2, j] / pred_j
                    )

            # Normalize so that sum over i,j = 1
            total = joint[t].sum()
            if total > 0:
                joint[t] /= total

        return joint

    def xǁKimSmootherǁjoint_smoothed__mutmut_26(
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
            total = None
            if total > 0:
                joint[t] /= total

        return joint

    def xǁKimSmootherǁjoint_smoothed__mutmut_27(
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
            if total >= 0:
                joint[t] /= total

        return joint

    def xǁKimSmootherǁjoint_smoothed__mutmut_28(
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
            if total > 1:
                joint[t] /= total

        return joint

    def xǁKimSmootherǁjoint_smoothed__mutmut_29(
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
                joint[t] = total

        return joint

    def xǁKimSmootherǁjoint_smoothed__mutmut_30(
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
                joint[t] *= total

        return joint

    xǁKimSmootherǁjoint_smoothed__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁKimSmootherǁjoint_smoothed__mutmut_1": xǁKimSmootherǁjoint_smoothed__mutmut_1,
        "xǁKimSmootherǁjoint_smoothed__mutmut_2": xǁKimSmootherǁjoint_smoothed__mutmut_2,
        "xǁKimSmootherǁjoint_smoothed__mutmut_3": xǁKimSmootherǁjoint_smoothed__mutmut_3,
        "xǁKimSmootherǁjoint_smoothed__mutmut_4": xǁKimSmootherǁjoint_smoothed__mutmut_4,
        "xǁKimSmootherǁjoint_smoothed__mutmut_5": xǁKimSmootherǁjoint_smoothed__mutmut_5,
        "xǁKimSmootherǁjoint_smoothed__mutmut_6": xǁKimSmootherǁjoint_smoothed__mutmut_6,
        "xǁKimSmootherǁjoint_smoothed__mutmut_7": xǁKimSmootherǁjoint_smoothed__mutmut_7,
        "xǁKimSmootherǁjoint_smoothed__mutmut_8": xǁKimSmootherǁjoint_smoothed__mutmut_8,
        "xǁKimSmootherǁjoint_smoothed__mutmut_9": xǁKimSmootherǁjoint_smoothed__mutmut_9,
        "xǁKimSmootherǁjoint_smoothed__mutmut_10": xǁKimSmootherǁjoint_smoothed__mutmut_10,
        "xǁKimSmootherǁjoint_smoothed__mutmut_11": xǁKimSmootherǁjoint_smoothed__mutmut_11,
        "xǁKimSmootherǁjoint_smoothed__mutmut_12": xǁKimSmootherǁjoint_smoothed__mutmut_12,
        "xǁKimSmootherǁjoint_smoothed__mutmut_13": xǁKimSmootherǁjoint_smoothed__mutmut_13,
        "xǁKimSmootherǁjoint_smoothed__mutmut_14": xǁKimSmootherǁjoint_smoothed__mutmut_14,
        "xǁKimSmootherǁjoint_smoothed__mutmut_15": xǁKimSmootherǁjoint_smoothed__mutmut_15,
        "xǁKimSmootherǁjoint_smoothed__mutmut_16": xǁKimSmootherǁjoint_smoothed__mutmut_16,
        "xǁKimSmootherǁjoint_smoothed__mutmut_17": xǁKimSmootherǁjoint_smoothed__mutmut_17,
        "xǁKimSmootherǁjoint_smoothed__mutmut_18": xǁKimSmootherǁjoint_smoothed__mutmut_18,
        "xǁKimSmootherǁjoint_smoothed__mutmut_19": xǁKimSmootherǁjoint_smoothed__mutmut_19,
        "xǁKimSmootherǁjoint_smoothed__mutmut_20": xǁKimSmootherǁjoint_smoothed__mutmut_20,
        "xǁKimSmootherǁjoint_smoothed__mutmut_21": xǁKimSmootherǁjoint_smoothed__mutmut_21,
        "xǁKimSmootherǁjoint_smoothed__mutmut_22": xǁKimSmootherǁjoint_smoothed__mutmut_22,
        "xǁKimSmootherǁjoint_smoothed__mutmut_23": xǁKimSmootherǁjoint_smoothed__mutmut_23,
        "xǁKimSmootherǁjoint_smoothed__mutmut_24": xǁKimSmootherǁjoint_smoothed__mutmut_24,
        "xǁKimSmootherǁjoint_smoothed__mutmut_25": xǁKimSmootherǁjoint_smoothed__mutmut_25,
        "xǁKimSmootherǁjoint_smoothed__mutmut_26": xǁKimSmootherǁjoint_smoothed__mutmut_26,
        "xǁKimSmootherǁjoint_smoothed__mutmut_27": xǁKimSmootherǁjoint_smoothed__mutmut_27,
        "xǁKimSmootherǁjoint_smoothed__mutmut_28": xǁKimSmootherǁjoint_smoothed__mutmut_28,
        "xǁKimSmootherǁjoint_smoothed__mutmut_29": xǁKimSmootherǁjoint_smoothed__mutmut_29,
        "xǁKimSmootherǁjoint_smoothed__mutmut_30": xǁKimSmootherǁjoint_smoothed__mutmut_30,
    }
    xǁKimSmootherǁjoint_smoothed__mutmut_orig.__name__ = "xǁKimSmootherǁjoint_smoothed"
