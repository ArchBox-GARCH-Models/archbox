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
        args = [endog, regime_loglike_fn, transition_matrix, init_probs]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁHamiltonFilterǁfilter__mutmut_orig"),
            object.__getattribute__(self, "xǁHamiltonFilterǁfilter__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁHamiltonFilterǁfilter__mutmut_orig(
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

    def xǁHamiltonFilterǁfilter__mutmut_1(
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
        n_obs = None
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

    def xǁHamiltonFilterǁfilter__mutmut_2(
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
        n_obs = len(endog) if endog.ndim != 1 else endog.shape[0]
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

    def xǁHamiltonFilterǁfilter__mutmut_3(
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
        n_obs = len(endog) if endog.ndim == 2 else endog.shape[0]
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

    def xǁHamiltonFilterǁfilter__mutmut_4(
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
        n_obs = len(endog) if endog.ndim == 1 else endog.shape[1]
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

    def xǁHamiltonFilterǁfilter__mutmut_5(
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
        k = None
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

    def xǁHamiltonFilterǁfilter__mutmut_6(
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
        k = transition_matrix.shape[1]
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

    def xǁHamiltonFilterǁfilter__mutmut_7(
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
        trans = None

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

    def xǁHamiltonFilterǁfilter__mutmut_8(
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

        if init_probs is not None:
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

    def xǁHamiltonFilterǁfilter__mutmut_9(
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
            init_probs = None

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

    def xǁHamiltonFilterǁfilter__mutmut_10(
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
            init_probs = self.ergodic_probabilities(None)

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

    def xǁHamiltonFilterǁfilter__mutmut_11(
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

        filtered = None
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

    def xǁHamiltonFilterǁfilter__mutmut_12(
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

        filtered = np.zeros(None)
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

    def xǁHamiltonFilterǁfilter__mutmut_13(
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
        predicted = None
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

    def xǁHamiltonFilterǁfilter__mutmut_14(
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
        predicted = np.zeros(None)
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

    def xǁHamiltonFilterǁfilter__mutmut_15(
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
        marginal_ll = None

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

    def xǁHamiltonFilterǁfilter__mutmut_16(
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
        marginal_ll = np.zeros(None)

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

    def xǁHamiltonFilterǁfilter__mutmut_17(
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

        xi = None

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

    def xǁHamiltonFilterǁfilter__mutmut_18(
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

        for t in range(None):
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

    def xǁHamiltonFilterǁfilter__mutmut_19(
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
            xi_pred = None
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

    def xǁHamiltonFilterǁfilter__mutmut_20(
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
            xi_pred = None
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

    def xǁHamiltonFilterǁfilter__mutmut_21(
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
            xi_pred = np.maximum(None, 1e-300)
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

    def xǁHamiltonFilterǁfilter__mutmut_22(
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
            xi_pred = np.maximum(xi_pred, None)
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

    def xǁHamiltonFilterǁfilter__mutmut_23(
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
            xi_pred = np.maximum(1e-300)
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

    def xǁHamiltonFilterǁfilter__mutmut_24(
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
            xi_pred = np.maximum(
                xi_pred,
            )
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

    def xǁHamiltonFilterǁfilter__mutmut_25(
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
            xi_pred = np.maximum(xi_pred, 1.0)
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

    def xǁHamiltonFilterǁfilter__mutmut_26(
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
            xi_pred = xi_pred.sum()
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

    def xǁHamiltonFilterǁfilter__mutmut_27(
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
            xi_pred *= xi_pred.sum()
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

    def xǁHamiltonFilterǁfilter__mutmut_28(
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
            predicted[t] = None

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

    def xǁHamiltonFilterǁfilter__mutmut_29(
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
            log_eta = None

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

    def xǁHamiltonFilterǁfilter__mutmut_30(
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
            log_eta = np.array(None)

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

    def xǁHamiltonFilterǁfilter__mutmut_31(
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
            log_eta = np.array([regime_loglike_fn(None, s) for s in range(k)])

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

    def xǁHamiltonFilterǁfilter__mutmut_32(
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
            log_eta = np.array([regime_loglike_fn(t, None) for s in range(k)])

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

    def xǁHamiltonFilterǁfilter__mutmut_33(
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
            log_eta = np.array([regime_loglike_fn(s) for s in range(k)])

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

    def xǁHamiltonFilterǁfilter__mutmut_34(
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
            log_eta = np.array(
                [
                    regime_loglike_fn(
                        t,
                    )
                    for s in range(k)
                ]
            )

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

    def xǁHamiltonFilterǁfilter__mutmut_35(
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
            log_eta = np.array([regime_loglike_fn(t, s) for s in range(None)])

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

    def xǁHamiltonFilterǁfilter__mutmut_36(
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
            max_log_eta = None
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

    def xǁHamiltonFilterǁfilter__mutmut_37(
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
            max_log_eta = np.max(None)
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

    def xǁHamiltonFilterǁfilter__mutmut_38(
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
            eta = None

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

    def xǁHamiltonFilterǁfilter__mutmut_39(
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
            eta = np.exp(None)

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

    def xǁHamiltonFilterǁfilter__mutmut_40(
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
            eta = np.exp(log_eta + max_log_eta)

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

    def xǁHamiltonFilterǁfilter__mutmut_41(
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
            num = None
            f_t = num.sum()

            xi = np.ones(k) / k if f_t < 1e-300 else num / f_t

            filtered[t] = xi
            # log(f_t) = log(sum(xi_pred * exp(log_eta)))
            # = max_log_eta + log(sum(xi_pred * exp(log_eta - max_log_eta)))
            marginal_ll[t] = max_log_eta + np.log(max(f_t, 1e-300))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter__mutmut_42(
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
            num = xi_pred / eta
            f_t = num.sum()

            xi = np.ones(k) / k if f_t < 1e-300 else num / f_t

            filtered[t] = xi
            # log(f_t) = log(sum(xi_pred * exp(log_eta)))
            # = max_log_eta + log(sum(xi_pred * exp(log_eta - max_log_eta)))
            marginal_ll[t] = max_log_eta + np.log(max(f_t, 1e-300))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter__mutmut_43(
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
            f_t = None

            xi = np.ones(k) / k if f_t < 1e-300 else num / f_t

            filtered[t] = xi
            # log(f_t) = log(sum(xi_pred * exp(log_eta)))
            # = max_log_eta + log(sum(xi_pred * exp(log_eta - max_log_eta)))
            marginal_ll[t] = max_log_eta + np.log(max(f_t, 1e-300))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter__mutmut_44(
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

            xi = None

            filtered[t] = xi
            # log(f_t) = log(sum(xi_pred * exp(log_eta)))
            # = max_log_eta + log(sum(xi_pred * exp(log_eta - max_log_eta)))
            marginal_ll[t] = max_log_eta + np.log(max(f_t, 1e-300))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter__mutmut_45(
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

            xi = np.ones(k) * k if f_t < 1e-300 else num / f_t

            filtered[t] = xi
            # log(f_t) = log(sum(xi_pred * exp(log_eta)))
            # = max_log_eta + log(sum(xi_pred * exp(log_eta - max_log_eta)))
            marginal_ll[t] = max_log_eta + np.log(max(f_t, 1e-300))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter__mutmut_46(
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

            xi = np.ones(None) / k if f_t < 1e-300 else num / f_t

            filtered[t] = xi
            # log(f_t) = log(sum(xi_pred * exp(log_eta)))
            # = max_log_eta + log(sum(xi_pred * exp(log_eta - max_log_eta)))
            marginal_ll[t] = max_log_eta + np.log(max(f_t, 1e-300))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter__mutmut_47(
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

            xi = np.ones(k) / k if f_t <= 1e-300 else num / f_t

            filtered[t] = xi
            # log(f_t) = log(sum(xi_pred * exp(log_eta)))
            # = max_log_eta + log(sum(xi_pred * exp(log_eta - max_log_eta)))
            marginal_ll[t] = max_log_eta + np.log(max(f_t, 1e-300))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter__mutmut_48(
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

            xi = np.ones(k) / k if f_t < 1.0 else num / f_t

            filtered[t] = xi
            # log(f_t) = log(sum(xi_pred * exp(log_eta)))
            # = max_log_eta + log(sum(xi_pred * exp(log_eta - max_log_eta)))
            marginal_ll[t] = max_log_eta + np.log(max(f_t, 1e-300))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter__mutmut_49(
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

            xi = np.ones(k) / k if f_t < 1e-300 else num * f_t

            filtered[t] = xi
            # log(f_t) = log(sum(xi_pred * exp(log_eta)))
            # = max_log_eta + log(sum(xi_pred * exp(log_eta - max_log_eta)))
            marginal_ll[t] = max_log_eta + np.log(max(f_t, 1e-300))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter__mutmut_50(
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

            filtered[t] = None
            # log(f_t) = log(sum(xi_pred * exp(log_eta)))
            # = max_log_eta + log(sum(xi_pred * exp(log_eta - max_log_eta)))
            marginal_ll[t] = max_log_eta + np.log(max(f_t, 1e-300))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter__mutmut_51(
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
            marginal_ll[t] = None

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter__mutmut_52(
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
            marginal_ll[t] = max_log_eta - np.log(max(f_t, 1e-300))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter__mutmut_53(
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
            marginal_ll[t] = max_log_eta + np.log(None)

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter__mutmut_54(
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
            marginal_ll[t] = max_log_eta + np.log(max(None, 1e-300))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter__mutmut_55(
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
            marginal_ll[t] = max_log_eta + np.log(max(f_t, None))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter__mutmut_56(
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
            marginal_ll[t] = max_log_eta + np.log(max(1e-300))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter__mutmut_57(
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
            marginal_ll[t] = max_log_eta + np.log(
                max(
                    f_t,
                )
            )

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter__mutmut_58(
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
            marginal_ll[t] = max_log_eta + np.log(max(f_t, 1.0))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter__mutmut_59(
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

        total_loglike = None
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter__mutmut_60(
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

        total_loglike = float(None)
        return filtered, predicted, total_loglike, marginal_ll

    xǁHamiltonFilterǁfilter__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁHamiltonFilterǁfilter__mutmut_1": xǁHamiltonFilterǁfilter__mutmut_1,
        "xǁHamiltonFilterǁfilter__mutmut_2": xǁHamiltonFilterǁfilter__mutmut_2,
        "xǁHamiltonFilterǁfilter__mutmut_3": xǁHamiltonFilterǁfilter__mutmut_3,
        "xǁHamiltonFilterǁfilter__mutmut_4": xǁHamiltonFilterǁfilter__mutmut_4,
        "xǁHamiltonFilterǁfilter__mutmut_5": xǁHamiltonFilterǁfilter__mutmut_5,
        "xǁHamiltonFilterǁfilter__mutmut_6": xǁHamiltonFilterǁfilter__mutmut_6,
        "xǁHamiltonFilterǁfilter__mutmut_7": xǁHamiltonFilterǁfilter__mutmut_7,
        "xǁHamiltonFilterǁfilter__mutmut_8": xǁHamiltonFilterǁfilter__mutmut_8,
        "xǁHamiltonFilterǁfilter__mutmut_9": xǁHamiltonFilterǁfilter__mutmut_9,
        "xǁHamiltonFilterǁfilter__mutmut_10": xǁHamiltonFilterǁfilter__mutmut_10,
        "xǁHamiltonFilterǁfilter__mutmut_11": xǁHamiltonFilterǁfilter__mutmut_11,
        "xǁHamiltonFilterǁfilter__mutmut_12": xǁHamiltonFilterǁfilter__mutmut_12,
        "xǁHamiltonFilterǁfilter__mutmut_13": xǁHamiltonFilterǁfilter__mutmut_13,
        "xǁHamiltonFilterǁfilter__mutmut_14": xǁHamiltonFilterǁfilter__mutmut_14,
        "xǁHamiltonFilterǁfilter__mutmut_15": xǁHamiltonFilterǁfilter__mutmut_15,
        "xǁHamiltonFilterǁfilter__mutmut_16": xǁHamiltonFilterǁfilter__mutmut_16,
        "xǁHamiltonFilterǁfilter__mutmut_17": xǁHamiltonFilterǁfilter__mutmut_17,
        "xǁHamiltonFilterǁfilter__mutmut_18": xǁHamiltonFilterǁfilter__mutmut_18,
        "xǁHamiltonFilterǁfilter__mutmut_19": xǁHamiltonFilterǁfilter__mutmut_19,
        "xǁHamiltonFilterǁfilter__mutmut_20": xǁHamiltonFilterǁfilter__mutmut_20,
        "xǁHamiltonFilterǁfilter__mutmut_21": xǁHamiltonFilterǁfilter__mutmut_21,
        "xǁHamiltonFilterǁfilter__mutmut_22": xǁHamiltonFilterǁfilter__mutmut_22,
        "xǁHamiltonFilterǁfilter__mutmut_23": xǁHamiltonFilterǁfilter__mutmut_23,
        "xǁHamiltonFilterǁfilter__mutmut_24": xǁHamiltonFilterǁfilter__mutmut_24,
        "xǁHamiltonFilterǁfilter__mutmut_25": xǁHamiltonFilterǁfilter__mutmut_25,
        "xǁHamiltonFilterǁfilter__mutmut_26": xǁHamiltonFilterǁfilter__mutmut_26,
        "xǁHamiltonFilterǁfilter__mutmut_27": xǁHamiltonFilterǁfilter__mutmut_27,
        "xǁHamiltonFilterǁfilter__mutmut_28": xǁHamiltonFilterǁfilter__mutmut_28,
        "xǁHamiltonFilterǁfilter__mutmut_29": xǁHamiltonFilterǁfilter__mutmut_29,
        "xǁHamiltonFilterǁfilter__mutmut_30": xǁHamiltonFilterǁfilter__mutmut_30,
        "xǁHamiltonFilterǁfilter__mutmut_31": xǁHamiltonFilterǁfilter__mutmut_31,
        "xǁHamiltonFilterǁfilter__mutmut_32": xǁHamiltonFilterǁfilter__mutmut_32,
        "xǁHamiltonFilterǁfilter__mutmut_33": xǁHamiltonFilterǁfilter__mutmut_33,
        "xǁHamiltonFilterǁfilter__mutmut_34": xǁHamiltonFilterǁfilter__mutmut_34,
        "xǁHamiltonFilterǁfilter__mutmut_35": xǁHamiltonFilterǁfilter__mutmut_35,
        "xǁHamiltonFilterǁfilter__mutmut_36": xǁHamiltonFilterǁfilter__mutmut_36,
        "xǁHamiltonFilterǁfilter__mutmut_37": xǁHamiltonFilterǁfilter__mutmut_37,
        "xǁHamiltonFilterǁfilter__mutmut_38": xǁHamiltonFilterǁfilter__mutmut_38,
        "xǁHamiltonFilterǁfilter__mutmut_39": xǁHamiltonFilterǁfilter__mutmut_39,
        "xǁHamiltonFilterǁfilter__mutmut_40": xǁHamiltonFilterǁfilter__mutmut_40,
        "xǁHamiltonFilterǁfilter__mutmut_41": xǁHamiltonFilterǁfilter__mutmut_41,
        "xǁHamiltonFilterǁfilter__mutmut_42": xǁHamiltonFilterǁfilter__mutmut_42,
        "xǁHamiltonFilterǁfilter__mutmut_43": xǁHamiltonFilterǁfilter__mutmut_43,
        "xǁHamiltonFilterǁfilter__mutmut_44": xǁHamiltonFilterǁfilter__mutmut_44,
        "xǁHamiltonFilterǁfilter__mutmut_45": xǁHamiltonFilterǁfilter__mutmut_45,
        "xǁHamiltonFilterǁfilter__mutmut_46": xǁHamiltonFilterǁfilter__mutmut_46,
        "xǁHamiltonFilterǁfilter__mutmut_47": xǁHamiltonFilterǁfilter__mutmut_47,
        "xǁHamiltonFilterǁfilter__mutmut_48": xǁHamiltonFilterǁfilter__mutmut_48,
        "xǁHamiltonFilterǁfilter__mutmut_49": xǁHamiltonFilterǁfilter__mutmut_49,
        "xǁHamiltonFilterǁfilter__mutmut_50": xǁHamiltonFilterǁfilter__mutmut_50,
        "xǁHamiltonFilterǁfilter__mutmut_51": xǁHamiltonFilterǁfilter__mutmut_51,
        "xǁHamiltonFilterǁfilter__mutmut_52": xǁHamiltonFilterǁfilter__mutmut_52,
        "xǁHamiltonFilterǁfilter__mutmut_53": xǁHamiltonFilterǁfilter__mutmut_53,
        "xǁHamiltonFilterǁfilter__mutmut_54": xǁHamiltonFilterǁfilter__mutmut_54,
        "xǁHamiltonFilterǁfilter__mutmut_55": xǁHamiltonFilterǁfilter__mutmut_55,
        "xǁHamiltonFilterǁfilter__mutmut_56": xǁHamiltonFilterǁfilter__mutmut_56,
        "xǁHamiltonFilterǁfilter__mutmut_57": xǁHamiltonFilterǁfilter__mutmut_57,
        "xǁHamiltonFilterǁfilter__mutmut_58": xǁHamiltonFilterǁfilter__mutmut_58,
        "xǁHamiltonFilterǁfilter__mutmut_59": xǁHamiltonFilterǁfilter__mutmut_59,
        "xǁHamiltonFilterǁfilter__mutmut_60": xǁHamiltonFilterǁfilter__mutmut_60,
    }
    xǁHamiltonFilterǁfilter__mutmut_orig.__name__ = "xǁHamiltonFilterǁfilter"

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
        args = [regime_loglikes, transition_matrix, init_probs]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁHamiltonFilterǁfilter_vectorized__mutmut_orig"),
            object.__getattribute__(self, "xǁHamiltonFilterǁfilter_vectorized__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_orig(
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

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_1(
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
        n_obs, k = None
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

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_2(
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
        trans = None

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

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_3(
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

        if init_probs is not None:
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

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_4(
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
            init_probs = None

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

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_5(
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
            init_probs = self.ergodic_probabilities(None)

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

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_6(
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

        filtered = None
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

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_7(
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

        filtered = np.zeros(None)
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

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_8(
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
        predicted = None
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

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_9(
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
        predicted = np.zeros(None)
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

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_10(
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
        marginal_ll = None

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

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_11(
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
        marginal_ll = np.zeros(None)

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

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_12(
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

        xi = None

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

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_13(
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

        for t in range(None):
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

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_14(
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
            xi_pred = None
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

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_15(
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
            xi_pred = None
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

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_16(
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
            xi_pred = np.maximum(None, 1e-300)
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

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_17(
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
            xi_pred = np.maximum(xi_pred, None)
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

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_18(
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
            xi_pred = np.maximum(1e-300)
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

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_19(
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
            xi_pred = np.maximum(
                xi_pred,
            )
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

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_20(
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
            xi_pred = np.maximum(xi_pred, 1.0)
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

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_21(
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
            xi_pred = xi_pred.sum()
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

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_22(
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
            xi_pred *= xi_pred.sum()
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

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_23(
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
            predicted[t] = None

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

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_24(
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
            log_eta = None
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

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_25(
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
            max_log_eta = None
            eta = np.exp(log_eta - max_log_eta)

            # Update
            num = xi_pred * eta
            f_t = num.sum()

            xi = np.ones(k) / k if f_t < 1e-300 else num / f_t

            filtered[t] = xi
            marginal_ll[t] = max_log_eta + np.log(max(f_t, 1e-300))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_26(
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
            max_log_eta = np.max(None)
            eta = np.exp(log_eta - max_log_eta)

            # Update
            num = xi_pred * eta
            f_t = num.sum()

            xi = np.ones(k) / k if f_t < 1e-300 else num / f_t

            filtered[t] = xi
            marginal_ll[t] = max_log_eta + np.log(max(f_t, 1e-300))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_27(
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
            eta = None

            # Update
            num = xi_pred * eta
            f_t = num.sum()

            xi = np.ones(k) / k if f_t < 1e-300 else num / f_t

            filtered[t] = xi
            marginal_ll[t] = max_log_eta + np.log(max(f_t, 1e-300))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_28(
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
            eta = np.exp(None)

            # Update
            num = xi_pred * eta
            f_t = num.sum()

            xi = np.ones(k) / k if f_t < 1e-300 else num / f_t

            filtered[t] = xi
            marginal_ll[t] = max_log_eta + np.log(max(f_t, 1e-300))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_29(
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
            eta = np.exp(log_eta + max_log_eta)

            # Update
            num = xi_pred * eta
            f_t = num.sum()

            xi = np.ones(k) / k if f_t < 1e-300 else num / f_t

            filtered[t] = xi
            marginal_ll[t] = max_log_eta + np.log(max(f_t, 1e-300))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_30(
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
            num = None
            f_t = num.sum()

            xi = np.ones(k) / k if f_t < 1e-300 else num / f_t

            filtered[t] = xi
            marginal_ll[t] = max_log_eta + np.log(max(f_t, 1e-300))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_31(
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
            num = xi_pred / eta
            f_t = num.sum()

            xi = np.ones(k) / k if f_t < 1e-300 else num / f_t

            filtered[t] = xi
            marginal_ll[t] = max_log_eta + np.log(max(f_t, 1e-300))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_32(
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
            f_t = None

            xi = np.ones(k) / k if f_t < 1e-300 else num / f_t

            filtered[t] = xi
            marginal_ll[t] = max_log_eta + np.log(max(f_t, 1e-300))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_33(
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

            xi = None

            filtered[t] = xi
            marginal_ll[t] = max_log_eta + np.log(max(f_t, 1e-300))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_34(
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

            xi = np.ones(k) * k if f_t < 1e-300 else num / f_t

            filtered[t] = xi
            marginal_ll[t] = max_log_eta + np.log(max(f_t, 1e-300))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_35(
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

            xi = np.ones(None) / k if f_t < 1e-300 else num / f_t

            filtered[t] = xi
            marginal_ll[t] = max_log_eta + np.log(max(f_t, 1e-300))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_36(
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

            xi = np.ones(k) / k if f_t <= 1e-300 else num / f_t

            filtered[t] = xi
            marginal_ll[t] = max_log_eta + np.log(max(f_t, 1e-300))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_37(
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

            xi = np.ones(k) / k if f_t < 1.0 else num / f_t

            filtered[t] = xi
            marginal_ll[t] = max_log_eta + np.log(max(f_t, 1e-300))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_38(
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

            xi = np.ones(k) / k if f_t < 1e-300 else num * f_t

            filtered[t] = xi
            marginal_ll[t] = max_log_eta + np.log(max(f_t, 1e-300))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_39(
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

            filtered[t] = None
            marginal_ll[t] = max_log_eta + np.log(max(f_t, 1e-300))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_40(
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
            marginal_ll[t] = None

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_41(
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
            marginal_ll[t] = max_log_eta - np.log(max(f_t, 1e-300))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_42(
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
            marginal_ll[t] = max_log_eta + np.log(None)

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_43(
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
            marginal_ll[t] = max_log_eta + np.log(max(None, 1e-300))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_44(
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
            marginal_ll[t] = max_log_eta + np.log(max(f_t, None))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_45(
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
            marginal_ll[t] = max_log_eta + np.log(max(1e-300))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_46(
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
            marginal_ll[t] = max_log_eta + np.log(
                max(
                    f_t,
                )
            )

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_47(
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
            marginal_ll[t] = max_log_eta + np.log(max(f_t, 1.0))

        total_loglike = float(marginal_ll.sum())
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_48(
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

        total_loglike = None
        return filtered, predicted, total_loglike, marginal_ll

    def xǁHamiltonFilterǁfilter_vectorized__mutmut_49(
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

        total_loglike = float(None)
        return filtered, predicted, total_loglike, marginal_ll

    xǁHamiltonFilterǁfilter_vectorized__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_1": xǁHamiltonFilterǁfilter_vectorized__mutmut_1,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_2": xǁHamiltonFilterǁfilter_vectorized__mutmut_2,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_3": xǁHamiltonFilterǁfilter_vectorized__mutmut_3,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_4": xǁHamiltonFilterǁfilter_vectorized__mutmut_4,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_5": xǁHamiltonFilterǁfilter_vectorized__mutmut_5,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_6": xǁHamiltonFilterǁfilter_vectorized__mutmut_6,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_7": xǁHamiltonFilterǁfilter_vectorized__mutmut_7,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_8": xǁHamiltonFilterǁfilter_vectorized__mutmut_8,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_9": xǁHamiltonFilterǁfilter_vectorized__mutmut_9,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_10": xǁHamiltonFilterǁfilter_vectorized__mutmut_10,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_11": xǁHamiltonFilterǁfilter_vectorized__mutmut_11,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_12": xǁHamiltonFilterǁfilter_vectorized__mutmut_12,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_13": xǁHamiltonFilterǁfilter_vectorized__mutmut_13,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_14": xǁHamiltonFilterǁfilter_vectorized__mutmut_14,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_15": xǁHamiltonFilterǁfilter_vectorized__mutmut_15,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_16": xǁHamiltonFilterǁfilter_vectorized__mutmut_16,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_17": xǁHamiltonFilterǁfilter_vectorized__mutmut_17,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_18": xǁHamiltonFilterǁfilter_vectorized__mutmut_18,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_19": xǁHamiltonFilterǁfilter_vectorized__mutmut_19,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_20": xǁHamiltonFilterǁfilter_vectorized__mutmut_20,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_21": xǁHamiltonFilterǁfilter_vectorized__mutmut_21,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_22": xǁHamiltonFilterǁfilter_vectorized__mutmut_22,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_23": xǁHamiltonFilterǁfilter_vectorized__mutmut_23,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_24": xǁHamiltonFilterǁfilter_vectorized__mutmut_24,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_25": xǁHamiltonFilterǁfilter_vectorized__mutmut_25,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_26": xǁHamiltonFilterǁfilter_vectorized__mutmut_26,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_27": xǁHamiltonFilterǁfilter_vectorized__mutmut_27,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_28": xǁHamiltonFilterǁfilter_vectorized__mutmut_28,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_29": xǁHamiltonFilterǁfilter_vectorized__mutmut_29,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_30": xǁHamiltonFilterǁfilter_vectorized__mutmut_30,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_31": xǁHamiltonFilterǁfilter_vectorized__mutmut_31,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_32": xǁHamiltonFilterǁfilter_vectorized__mutmut_32,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_33": xǁHamiltonFilterǁfilter_vectorized__mutmut_33,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_34": xǁHamiltonFilterǁfilter_vectorized__mutmut_34,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_35": xǁHamiltonFilterǁfilter_vectorized__mutmut_35,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_36": xǁHamiltonFilterǁfilter_vectorized__mutmut_36,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_37": xǁHamiltonFilterǁfilter_vectorized__mutmut_37,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_38": xǁHamiltonFilterǁfilter_vectorized__mutmut_38,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_39": xǁHamiltonFilterǁfilter_vectorized__mutmut_39,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_40": xǁHamiltonFilterǁfilter_vectorized__mutmut_40,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_41": xǁHamiltonFilterǁfilter_vectorized__mutmut_41,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_42": xǁHamiltonFilterǁfilter_vectorized__mutmut_42,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_43": xǁHamiltonFilterǁfilter_vectorized__mutmut_43,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_44": xǁHamiltonFilterǁfilter_vectorized__mutmut_44,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_45": xǁHamiltonFilterǁfilter_vectorized__mutmut_45,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_46": xǁHamiltonFilterǁfilter_vectorized__mutmut_46,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_47": xǁHamiltonFilterǁfilter_vectorized__mutmut_47,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_48": xǁHamiltonFilterǁfilter_vectorized__mutmut_48,
        "xǁHamiltonFilterǁfilter_vectorized__mutmut_49": xǁHamiltonFilterǁfilter_vectorized__mutmut_49,
    }
    xǁHamiltonFilterǁfilter_vectorized__mutmut_orig.__name__ = "xǁHamiltonFilterǁfilter_vectorized"

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
