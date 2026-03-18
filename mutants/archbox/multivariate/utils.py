"""Utility functions for multivariate GARCH models."""

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


def ensure_positive_definite(
    matrix: NDArray[np.float64],
    epsilon: float = 1e-8,
) -> NDArray[np.float64]:
    args = [matrix, epsilon]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_ensure_positive_definite__mutmut_orig,
        x_ensure_positive_definite__mutmut_mutants,
        args,
        kwargs,
        None,
    )


def x_ensure_positive_definite__mutmut_orig(
    matrix: NDArray[np.float64],
    epsilon: float = 1e-8,
) -> NDArray[np.float64]:
    """Ensure a matrix is positive definite via eigenvalue clipping.

    Parameters
    ----------
    matrix : ndarray
        Square matrix (k, k).
    epsilon : float
        Minimum eigenvalue.

    Returns
    -------
    ndarray
        Positive definite matrix (k, k).
    """
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    eigenvalues = np.maximum(eigenvalues, epsilon)
    return eigenvectors @ np.diag(eigenvalues) @ eigenvectors.T


def x_ensure_positive_definite__mutmut_1(
    matrix: NDArray[np.float64],
    epsilon: float = 1.00000001,
) -> NDArray[np.float64]:
    """Ensure a matrix is positive definite via eigenvalue clipping.

    Parameters
    ----------
    matrix : ndarray
        Square matrix (k, k).
    epsilon : float
        Minimum eigenvalue.

    Returns
    -------
    ndarray
        Positive definite matrix (k, k).
    """
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    eigenvalues = np.maximum(eigenvalues, epsilon)
    return eigenvectors @ np.diag(eigenvalues) @ eigenvectors.T


def x_ensure_positive_definite__mutmut_2(
    matrix: NDArray[np.float64],
    epsilon: float = 1e-8,
) -> NDArray[np.float64]:
    """Ensure a matrix is positive definite via eigenvalue clipping.

    Parameters
    ----------
    matrix : ndarray
        Square matrix (k, k).
    epsilon : float
        Minimum eigenvalue.

    Returns
    -------
    ndarray
        Positive definite matrix (k, k).
    """
    eigenvalues, eigenvectors = None
    eigenvalues = np.maximum(eigenvalues, epsilon)
    return eigenvectors @ np.diag(eigenvalues) @ eigenvectors.T


def x_ensure_positive_definite__mutmut_3(
    matrix: NDArray[np.float64],
    epsilon: float = 1e-8,
) -> NDArray[np.float64]:
    """Ensure a matrix is positive definite via eigenvalue clipping.

    Parameters
    ----------
    matrix : ndarray
        Square matrix (k, k).
    epsilon : float
        Minimum eigenvalue.

    Returns
    -------
    ndarray
        Positive definite matrix (k, k).
    """
    eigenvalues, eigenvectors = np.linalg.eigh(None)
    eigenvalues = np.maximum(eigenvalues, epsilon)
    return eigenvectors @ np.diag(eigenvalues) @ eigenvectors.T


def x_ensure_positive_definite__mutmut_4(
    matrix: NDArray[np.float64],
    epsilon: float = 1e-8,
) -> NDArray[np.float64]:
    """Ensure a matrix is positive definite via eigenvalue clipping.

    Parameters
    ----------
    matrix : ndarray
        Square matrix (k, k).
    epsilon : float
        Minimum eigenvalue.

    Returns
    -------
    ndarray
        Positive definite matrix (k, k).
    """
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    eigenvalues = None
    return eigenvectors @ np.diag(eigenvalues) @ eigenvectors.T


def x_ensure_positive_definite__mutmut_5(
    matrix: NDArray[np.float64],
    epsilon: float = 1e-8,
) -> NDArray[np.float64]:
    """Ensure a matrix is positive definite via eigenvalue clipping.

    Parameters
    ----------
    matrix : ndarray
        Square matrix (k, k).
    epsilon : float
        Minimum eigenvalue.

    Returns
    -------
    ndarray
        Positive definite matrix (k, k).
    """
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    eigenvalues = np.maximum(None, epsilon)
    return eigenvectors @ np.diag(eigenvalues) @ eigenvectors.T


def x_ensure_positive_definite__mutmut_6(
    matrix: NDArray[np.float64],
    epsilon: float = 1e-8,
) -> NDArray[np.float64]:
    """Ensure a matrix is positive definite via eigenvalue clipping.

    Parameters
    ----------
    matrix : ndarray
        Square matrix (k, k).
    epsilon : float
        Minimum eigenvalue.

    Returns
    -------
    ndarray
        Positive definite matrix (k, k).
    """
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    eigenvalues = np.maximum(eigenvalues, None)
    return eigenvectors @ np.diag(eigenvalues) @ eigenvectors.T


def x_ensure_positive_definite__mutmut_7(
    matrix: NDArray[np.float64],
    epsilon: float = 1e-8,
) -> NDArray[np.float64]:
    """Ensure a matrix is positive definite via eigenvalue clipping.

    Parameters
    ----------
    matrix : ndarray
        Square matrix (k, k).
    epsilon : float
        Minimum eigenvalue.

    Returns
    -------
    ndarray
        Positive definite matrix (k, k).
    """
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    eigenvalues = np.maximum(epsilon)
    return eigenvectors @ np.diag(eigenvalues) @ eigenvectors.T


def x_ensure_positive_definite__mutmut_8(
    matrix: NDArray[np.float64],
    epsilon: float = 1e-8,
) -> NDArray[np.float64]:
    """Ensure a matrix is positive definite via eigenvalue clipping.

    Parameters
    ----------
    matrix : ndarray
        Square matrix (k, k).
    epsilon : float
        Minimum eigenvalue.

    Returns
    -------
    ndarray
        Positive definite matrix (k, k).
    """
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    eigenvalues = np.maximum(
        eigenvalues,
    )
    return eigenvectors @ np.diag(eigenvalues) @ eigenvectors.T


def x_ensure_positive_definite__mutmut_9(
    matrix: NDArray[np.float64],
    epsilon: float = 1e-8,
) -> NDArray[np.float64]:
    """Ensure a matrix is positive definite via eigenvalue clipping.

    Parameters
    ----------
    matrix : ndarray
        Square matrix (k, k).
    epsilon : float
        Minimum eigenvalue.

    Returns
    -------
    ndarray
        Positive definite matrix (k, k).
    """
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    eigenvalues = np.maximum(eigenvalues, epsilon)
    return eigenvectors @ np.diag(None) @ eigenvectors.T


x_ensure_positive_definite__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_ensure_positive_definite__mutmut_1": x_ensure_positive_definite__mutmut_1,
    "x_ensure_positive_definite__mutmut_2": x_ensure_positive_definite__mutmut_2,
    "x_ensure_positive_definite__mutmut_3": x_ensure_positive_definite__mutmut_3,
    "x_ensure_positive_definite__mutmut_4": x_ensure_positive_definite__mutmut_4,
    "x_ensure_positive_definite__mutmut_5": x_ensure_positive_definite__mutmut_5,
    "x_ensure_positive_definite__mutmut_6": x_ensure_positive_definite__mutmut_6,
    "x_ensure_positive_definite__mutmut_7": x_ensure_positive_definite__mutmut_7,
    "x_ensure_positive_definite__mutmut_8": x_ensure_positive_definite__mutmut_8,
    "x_ensure_positive_definite__mutmut_9": x_ensure_positive_definite__mutmut_9,
}
x_ensure_positive_definite__mutmut_orig.__name__ = "x_ensure_positive_definite"


def is_positive_definite(matrix: NDArray[np.float64]) -> bool:
    args = [matrix]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_is_positive_definite__mutmut_orig,
        x_is_positive_definite__mutmut_mutants,
        args,
        kwargs,
        None,
    )


def x_is_positive_definite__mutmut_orig(matrix: NDArray[np.float64]) -> bool:
    """Check if a matrix is positive definite.

    Parameters
    ----------
    matrix : ndarray
        Square matrix (k, k).

    Returns
    -------
    bool
        True if positive definite.
    """
    try:
        eigenvalues = np.linalg.eigvalsh(matrix)
        return bool(np.all(eigenvalues > 0))
    except np.linalg.LinAlgError:
        return False


def x_is_positive_definite__mutmut_1(matrix: NDArray[np.float64]) -> bool:
    """Check if a matrix is positive definite.

    Parameters
    ----------
    matrix : ndarray
        Square matrix (k, k).

    Returns
    -------
    bool
        True if positive definite.
    """
    try:
        eigenvalues = None
        return bool(np.all(eigenvalues > 0))
    except np.linalg.LinAlgError:
        return False


def x_is_positive_definite__mutmut_2(matrix: NDArray[np.float64]) -> bool:
    """Check if a matrix is positive definite.

    Parameters
    ----------
    matrix : ndarray
        Square matrix (k, k).

    Returns
    -------
    bool
        True if positive definite.
    """
    try:
        eigenvalues = np.linalg.eigvalsh(None)
        return bool(np.all(eigenvalues > 0))
    except np.linalg.LinAlgError:
        return False


def x_is_positive_definite__mutmut_3(matrix: NDArray[np.float64]) -> bool:
    """Check if a matrix is positive definite.

    Parameters
    ----------
    matrix : ndarray
        Square matrix (k, k).

    Returns
    -------
    bool
        True if positive definite.
    """
    try:
        eigenvalues = np.linalg.eigvalsh(matrix)
        return bool(None)
    except np.linalg.LinAlgError:
        return False


def x_is_positive_definite__mutmut_4(matrix: NDArray[np.float64]) -> bool:
    """Check if a matrix is positive definite.

    Parameters
    ----------
    matrix : ndarray
        Square matrix (k, k).

    Returns
    -------
    bool
        True if positive definite.
    """
    try:
        eigenvalues = np.linalg.eigvalsh(matrix)
        return bool(np.all(None))
    except np.linalg.LinAlgError:
        return False


def x_is_positive_definite__mutmut_5(matrix: NDArray[np.float64]) -> bool:
    """Check if a matrix is positive definite.

    Parameters
    ----------
    matrix : ndarray
        Square matrix (k, k).

    Returns
    -------
    bool
        True if positive definite.
    """
    try:
        eigenvalues = np.linalg.eigvalsh(matrix)
        return bool(np.all(eigenvalues >= 0))
    except np.linalg.LinAlgError:
        return False


def x_is_positive_definite__mutmut_6(matrix: NDArray[np.float64]) -> bool:
    """Check if a matrix is positive definite.

    Parameters
    ----------
    matrix : ndarray
        Square matrix (k, k).

    Returns
    -------
    bool
        True if positive definite.
    """
    try:
        eigenvalues = np.linalg.eigvalsh(matrix)
        return bool(np.all(eigenvalues > 1))
    except np.linalg.LinAlgError:
        return False


def x_is_positive_definite__mutmut_7(matrix: NDArray[np.float64]) -> bool:
    """Check if a matrix is positive definite.

    Parameters
    ----------
    matrix : ndarray
        Square matrix (k, k).

    Returns
    -------
    bool
        True if positive definite.
    """
    try:
        eigenvalues = np.linalg.eigvalsh(matrix)
        return bool(np.all(eigenvalues > 0))
    except np.linalg.LinAlgError:
        return True


x_is_positive_definite__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_is_positive_definite__mutmut_1": x_is_positive_definite__mutmut_1,
    "x_is_positive_definite__mutmut_2": x_is_positive_definite__mutmut_2,
    "x_is_positive_definite__mutmut_3": x_is_positive_definite__mutmut_3,
    "x_is_positive_definite__mutmut_4": x_is_positive_definite__mutmut_4,
    "x_is_positive_definite__mutmut_5": x_is_positive_definite__mutmut_5,
    "x_is_positive_definite__mutmut_6": x_is_positive_definite__mutmut_6,
    "x_is_positive_definite__mutmut_7": x_is_positive_definite__mutmut_7,
}
x_is_positive_definite__mutmut_orig.__name__ = "x_is_positive_definite"


def cov_to_corr(cov: NDArray[np.float64]) -> NDArray[np.float64]:
    args = [cov]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_cov_to_corr__mutmut_orig, x_cov_to_corr__mutmut_mutants, args, kwargs, None
    )


def x_cov_to_corr__mutmut_orig(cov: NDArray[np.float64]) -> NDArray[np.float64]:
    """Convert covariance matrix to correlation matrix.

    Parameters
    ----------
    cov : ndarray
        Covariance matrix (k, k).

    Returns
    -------
    ndarray
        Correlation matrix (k, k).
    """
    d = np.sqrt(np.diag(cov))
    d_inv = np.where(d > 0, 1.0 / d, 0.0)
    return np.outer(d_inv, d_inv) * cov


def x_cov_to_corr__mutmut_1(cov: NDArray[np.float64]) -> NDArray[np.float64]:
    """Convert covariance matrix to correlation matrix.

    Parameters
    ----------
    cov : ndarray
        Covariance matrix (k, k).

    Returns
    -------
    ndarray
        Correlation matrix (k, k).
    """
    d = None
    d_inv = np.where(d > 0, 1.0 / d, 0.0)
    return np.outer(d_inv, d_inv) * cov


def x_cov_to_corr__mutmut_2(cov: NDArray[np.float64]) -> NDArray[np.float64]:
    """Convert covariance matrix to correlation matrix.

    Parameters
    ----------
    cov : ndarray
        Covariance matrix (k, k).

    Returns
    -------
    ndarray
        Correlation matrix (k, k).
    """
    d = np.sqrt(None)
    d_inv = np.where(d > 0, 1.0 / d, 0.0)
    return np.outer(d_inv, d_inv) * cov


def x_cov_to_corr__mutmut_3(cov: NDArray[np.float64]) -> NDArray[np.float64]:
    """Convert covariance matrix to correlation matrix.

    Parameters
    ----------
    cov : ndarray
        Covariance matrix (k, k).

    Returns
    -------
    ndarray
        Correlation matrix (k, k).
    """
    d = np.sqrt(np.diag(None))
    d_inv = np.where(d > 0, 1.0 / d, 0.0)
    return np.outer(d_inv, d_inv) * cov


def x_cov_to_corr__mutmut_4(cov: NDArray[np.float64]) -> NDArray[np.float64]:
    """Convert covariance matrix to correlation matrix.

    Parameters
    ----------
    cov : ndarray
        Covariance matrix (k, k).

    Returns
    -------
    ndarray
        Correlation matrix (k, k).
    """
    d = np.sqrt(np.diag(cov))
    d_inv = None
    return np.outer(d_inv, d_inv) * cov


def x_cov_to_corr__mutmut_5(cov: NDArray[np.float64]) -> NDArray[np.float64]:
    """Convert covariance matrix to correlation matrix.

    Parameters
    ----------
    cov : ndarray
        Covariance matrix (k, k).

    Returns
    -------
    ndarray
        Correlation matrix (k, k).
    """
    d = np.sqrt(np.diag(cov))
    d_inv = np.where(None, 1.0 / d, 0.0)
    return np.outer(d_inv, d_inv) * cov


def x_cov_to_corr__mutmut_6(cov: NDArray[np.float64]) -> NDArray[np.float64]:
    """Convert covariance matrix to correlation matrix.

    Parameters
    ----------
    cov : ndarray
        Covariance matrix (k, k).

    Returns
    -------
    ndarray
        Correlation matrix (k, k).
    """
    d = np.sqrt(np.diag(cov))
    d_inv = np.where(d > 0, None, 0.0)
    return np.outer(d_inv, d_inv) * cov


def x_cov_to_corr__mutmut_7(cov: NDArray[np.float64]) -> NDArray[np.float64]:
    """Convert covariance matrix to correlation matrix.

    Parameters
    ----------
    cov : ndarray
        Covariance matrix (k, k).

    Returns
    -------
    ndarray
        Correlation matrix (k, k).
    """
    d = np.sqrt(np.diag(cov))
    d_inv = np.where(d > 0, 1.0 / d, None)
    return np.outer(d_inv, d_inv) * cov


def x_cov_to_corr__mutmut_8(cov: NDArray[np.float64]) -> NDArray[np.float64]:
    """Convert covariance matrix to correlation matrix.

    Parameters
    ----------
    cov : ndarray
        Covariance matrix (k, k).

    Returns
    -------
    ndarray
        Correlation matrix (k, k).
    """
    d = np.sqrt(np.diag(cov))
    d_inv = np.where(1.0 / d, 0.0)
    return np.outer(d_inv, d_inv) * cov


def x_cov_to_corr__mutmut_9(cov: NDArray[np.float64]) -> NDArray[np.float64]:
    """Convert covariance matrix to correlation matrix.

    Parameters
    ----------
    cov : ndarray
        Covariance matrix (k, k).

    Returns
    -------
    ndarray
        Correlation matrix (k, k).
    """
    d = np.sqrt(np.diag(cov))
    d_inv = np.where(d > 0, 0.0)
    return np.outer(d_inv, d_inv) * cov


def x_cov_to_corr__mutmut_10(cov: NDArray[np.float64]) -> NDArray[np.float64]:
    """Convert covariance matrix to correlation matrix.

    Parameters
    ----------
    cov : ndarray
        Covariance matrix (k, k).

    Returns
    -------
    ndarray
        Correlation matrix (k, k).
    """
    d = np.sqrt(np.diag(cov))
    d_inv = np.where(
        d > 0,
        1.0 / d,
    )
    return np.outer(d_inv, d_inv) * cov


def x_cov_to_corr__mutmut_11(cov: NDArray[np.float64]) -> NDArray[np.float64]:
    """Convert covariance matrix to correlation matrix.

    Parameters
    ----------
    cov : ndarray
        Covariance matrix (k, k).

    Returns
    -------
    ndarray
        Correlation matrix (k, k).
    """
    d = np.sqrt(np.diag(cov))
    d_inv = np.where(d >= 0, 1.0 / d, 0.0)
    return np.outer(d_inv, d_inv) * cov


def x_cov_to_corr__mutmut_12(cov: NDArray[np.float64]) -> NDArray[np.float64]:
    """Convert covariance matrix to correlation matrix.

    Parameters
    ----------
    cov : ndarray
        Covariance matrix (k, k).

    Returns
    -------
    ndarray
        Correlation matrix (k, k).
    """
    d = np.sqrt(np.diag(cov))
    d_inv = np.where(d > 1, 1.0 / d, 0.0)
    return np.outer(d_inv, d_inv) * cov


def x_cov_to_corr__mutmut_13(cov: NDArray[np.float64]) -> NDArray[np.float64]:
    """Convert covariance matrix to correlation matrix.

    Parameters
    ----------
    cov : ndarray
        Covariance matrix (k, k).

    Returns
    -------
    ndarray
        Correlation matrix (k, k).
    """
    d = np.sqrt(np.diag(cov))
    d_inv = np.where(d > 0, 1.0 * d, 0.0)
    return np.outer(d_inv, d_inv) * cov


def x_cov_to_corr__mutmut_14(cov: NDArray[np.float64]) -> NDArray[np.float64]:
    """Convert covariance matrix to correlation matrix.

    Parameters
    ----------
    cov : ndarray
        Covariance matrix (k, k).

    Returns
    -------
    ndarray
        Correlation matrix (k, k).
    """
    d = np.sqrt(np.diag(cov))
    d_inv = np.where(d > 0, 2.0 / d, 0.0)
    return np.outer(d_inv, d_inv) * cov


def x_cov_to_corr__mutmut_15(cov: NDArray[np.float64]) -> NDArray[np.float64]:
    """Convert covariance matrix to correlation matrix.

    Parameters
    ----------
    cov : ndarray
        Covariance matrix (k, k).

    Returns
    -------
    ndarray
        Correlation matrix (k, k).
    """
    d = np.sqrt(np.diag(cov))
    d_inv = np.where(d > 0, 1.0 / d, 1.0)
    return np.outer(d_inv, d_inv) * cov


def x_cov_to_corr__mutmut_16(cov: NDArray[np.float64]) -> NDArray[np.float64]:
    """Convert covariance matrix to correlation matrix.

    Parameters
    ----------
    cov : ndarray
        Covariance matrix (k, k).

    Returns
    -------
    ndarray
        Correlation matrix (k, k).
    """
    d = np.sqrt(np.diag(cov))
    d_inv = np.where(d > 0, 1.0 / d, 0.0)
    return np.outer(d_inv, d_inv) / cov


def x_cov_to_corr__mutmut_17(cov: NDArray[np.float64]) -> NDArray[np.float64]:
    """Convert covariance matrix to correlation matrix.

    Parameters
    ----------
    cov : ndarray
        Covariance matrix (k, k).

    Returns
    -------
    ndarray
        Correlation matrix (k, k).
    """
    d = np.sqrt(np.diag(cov))
    d_inv = np.where(d > 0, 1.0 / d, 0.0)
    return np.outer(None, d_inv) * cov


def x_cov_to_corr__mutmut_18(cov: NDArray[np.float64]) -> NDArray[np.float64]:
    """Convert covariance matrix to correlation matrix.

    Parameters
    ----------
    cov : ndarray
        Covariance matrix (k, k).

    Returns
    -------
    ndarray
        Correlation matrix (k, k).
    """
    d = np.sqrt(np.diag(cov))
    d_inv = np.where(d > 0, 1.0 / d, 0.0)
    return np.outer(d_inv, None) * cov


def x_cov_to_corr__mutmut_19(cov: NDArray[np.float64]) -> NDArray[np.float64]:
    """Convert covariance matrix to correlation matrix.

    Parameters
    ----------
    cov : ndarray
        Covariance matrix (k, k).

    Returns
    -------
    ndarray
        Correlation matrix (k, k).
    """
    d = np.sqrt(np.diag(cov))
    d_inv = np.where(d > 0, 1.0 / d, 0.0)
    return np.outer(d_inv) * cov


def x_cov_to_corr__mutmut_20(cov: NDArray[np.float64]) -> NDArray[np.float64]:
    """Convert covariance matrix to correlation matrix.

    Parameters
    ----------
    cov : ndarray
        Covariance matrix (k, k).

    Returns
    -------
    ndarray
        Correlation matrix (k, k).
    """
    d = np.sqrt(np.diag(cov))
    d_inv = np.where(d > 0, 1.0 / d, 0.0)
    return (
        np.outer(
            d_inv,
        )
        * cov
    )


x_cov_to_corr__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_cov_to_corr__mutmut_1": x_cov_to_corr__mutmut_1,
    "x_cov_to_corr__mutmut_2": x_cov_to_corr__mutmut_2,
    "x_cov_to_corr__mutmut_3": x_cov_to_corr__mutmut_3,
    "x_cov_to_corr__mutmut_4": x_cov_to_corr__mutmut_4,
    "x_cov_to_corr__mutmut_5": x_cov_to_corr__mutmut_5,
    "x_cov_to_corr__mutmut_6": x_cov_to_corr__mutmut_6,
    "x_cov_to_corr__mutmut_7": x_cov_to_corr__mutmut_7,
    "x_cov_to_corr__mutmut_8": x_cov_to_corr__mutmut_8,
    "x_cov_to_corr__mutmut_9": x_cov_to_corr__mutmut_9,
    "x_cov_to_corr__mutmut_10": x_cov_to_corr__mutmut_10,
    "x_cov_to_corr__mutmut_11": x_cov_to_corr__mutmut_11,
    "x_cov_to_corr__mutmut_12": x_cov_to_corr__mutmut_12,
    "x_cov_to_corr__mutmut_13": x_cov_to_corr__mutmut_13,
    "x_cov_to_corr__mutmut_14": x_cov_to_corr__mutmut_14,
    "x_cov_to_corr__mutmut_15": x_cov_to_corr__mutmut_15,
    "x_cov_to_corr__mutmut_16": x_cov_to_corr__mutmut_16,
    "x_cov_to_corr__mutmut_17": x_cov_to_corr__mutmut_17,
    "x_cov_to_corr__mutmut_18": x_cov_to_corr__mutmut_18,
    "x_cov_to_corr__mutmut_19": x_cov_to_corr__mutmut_19,
    "x_cov_to_corr__mutmut_20": x_cov_to_corr__mutmut_20,
}
x_cov_to_corr__mutmut_orig.__name__ = "x_cov_to_corr"


def corr_to_cov(
    corr: NDArray[np.float64],
    volatilities: NDArray[np.float64],
) -> NDArray[np.float64]:
    args = [corr, volatilities]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_corr_to_cov__mutmut_orig, x_corr_to_cov__mutmut_mutants, args, kwargs, None
    )


def x_corr_to_cov__mutmut_orig(
    corr: NDArray[np.float64],
    volatilities: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Convert correlation matrix + volatilities to covariance matrix.

    Parameters
    ----------
    corr : ndarray
        Correlation matrix (k, k).
    volatilities : ndarray
        Standard deviations (k,).

    Returns
    -------
    ndarray
        Covariance matrix (k, k).
    """
    d_mat = np.diag(volatilities)
    return d_mat @ corr @ d_mat


def x_corr_to_cov__mutmut_1(
    corr: NDArray[np.float64],
    volatilities: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Convert correlation matrix + volatilities to covariance matrix.

    Parameters
    ----------
    corr : ndarray
        Correlation matrix (k, k).
    volatilities : ndarray
        Standard deviations (k,).

    Returns
    -------
    ndarray
        Covariance matrix (k, k).
    """
    d_mat = None
    return d_mat @ corr @ d_mat


def x_corr_to_cov__mutmut_2(
    corr: NDArray[np.float64],
    volatilities: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Convert correlation matrix + volatilities to covariance matrix.

    Parameters
    ----------
    corr : ndarray
        Correlation matrix (k, k).
    volatilities : ndarray
        Standard deviations (k,).

    Returns
    -------
    ndarray
        Covariance matrix (k, k).
    """
    d_mat = np.diag(None)
    return d_mat @ corr @ d_mat


x_corr_to_cov__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_corr_to_cov__mutmut_1": x_corr_to_cov__mutmut_1,
    "x_corr_to_cov__mutmut_2": x_corr_to_cov__mutmut_2,
}
x_corr_to_cov__mutmut_orig.__name__ = "x_corr_to_cov"


def validate_multivariate_returns(endog: NDArray[np.float64]) -> None:
    args = [endog]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_validate_multivariate_returns__mutmut_orig,
        x_validate_multivariate_returns__mutmut_mutants,
        args,
        kwargs,
        None,
    )


def x_validate_multivariate_returns__mutmut_orig(endog: NDArray[np.float64]) -> None:
    """Validate multivariate returns array.

    Parameters
    ----------
    endog : ndarray
        Returns array.

    Raises
    ------
    ValueError
        If validation fails.
    """
    if endog.ndim != 2:
        msg = f"endog must be 2D (T, k), got {endog.ndim}D"
        raise ValueError(msg)
    if endog.shape[1] < 2:
        msg = f"Need at least 2 series, got {endog.shape[1]}"
        raise ValueError(msg)
    if endog.shape[0] < 20:
        msg = f"Need at least 20 observations, got {endog.shape[0]}"
        raise ValueError(msg)
    if np.any(np.isnan(endog)):
        msg = "endog contains NaN values"
        raise ValueError(msg)
    if np.any(np.isinf(endog)):
        msg = "endog contains Inf values"
        raise ValueError(msg)


def x_validate_multivariate_returns__mutmut_1(endog: NDArray[np.float64]) -> None:
    """Validate multivariate returns array.

    Parameters
    ----------
    endog : ndarray
        Returns array.

    Raises
    ------
    ValueError
        If validation fails.
    """
    if endog.ndim == 2:
        msg = f"endog must be 2D (T, k), got {endog.ndim}D"
        raise ValueError(msg)
    if endog.shape[1] < 2:
        msg = f"Need at least 2 series, got {endog.shape[1]}"
        raise ValueError(msg)
    if endog.shape[0] < 20:
        msg = f"Need at least 20 observations, got {endog.shape[0]}"
        raise ValueError(msg)
    if np.any(np.isnan(endog)):
        msg = "endog contains NaN values"
        raise ValueError(msg)
    if np.any(np.isinf(endog)):
        msg = "endog contains Inf values"
        raise ValueError(msg)


def x_validate_multivariate_returns__mutmut_2(endog: NDArray[np.float64]) -> None:
    """Validate multivariate returns array.

    Parameters
    ----------
    endog : ndarray
        Returns array.

    Raises
    ------
    ValueError
        If validation fails.
    """
    if endog.ndim != 3:
        msg = f"endog must be 2D (T, k), got {endog.ndim}D"
        raise ValueError(msg)
    if endog.shape[1] < 2:
        msg = f"Need at least 2 series, got {endog.shape[1]}"
        raise ValueError(msg)
    if endog.shape[0] < 20:
        msg = f"Need at least 20 observations, got {endog.shape[0]}"
        raise ValueError(msg)
    if np.any(np.isnan(endog)):
        msg = "endog contains NaN values"
        raise ValueError(msg)
    if np.any(np.isinf(endog)):
        msg = "endog contains Inf values"
        raise ValueError(msg)


def x_validate_multivariate_returns__mutmut_3(endog: NDArray[np.float64]) -> None:
    """Validate multivariate returns array.

    Parameters
    ----------
    endog : ndarray
        Returns array.

    Raises
    ------
    ValueError
        If validation fails.
    """
    if endog.ndim != 2:
        msg = None
        raise ValueError(msg)
    if endog.shape[1] < 2:
        msg = f"Need at least 2 series, got {endog.shape[1]}"
        raise ValueError(msg)
    if endog.shape[0] < 20:
        msg = f"Need at least 20 observations, got {endog.shape[0]}"
        raise ValueError(msg)
    if np.any(np.isnan(endog)):
        msg = "endog contains NaN values"
        raise ValueError(msg)
    if np.any(np.isinf(endog)):
        msg = "endog contains Inf values"
        raise ValueError(msg)


def x_validate_multivariate_returns__mutmut_4(endog: NDArray[np.float64]) -> None:
    """Validate multivariate returns array.

    Parameters
    ----------
    endog : ndarray
        Returns array.

    Raises
    ------
    ValueError
        If validation fails.
    """
    if endog.ndim != 2:
        msg = f"endog must be 2D (T, k), got {endog.ndim}D"
        raise ValueError(None)
    if endog.shape[1] < 2:
        msg = f"Need at least 2 series, got {endog.shape[1]}"
        raise ValueError(msg)
    if endog.shape[0] < 20:
        msg = f"Need at least 20 observations, got {endog.shape[0]}"
        raise ValueError(msg)
    if np.any(np.isnan(endog)):
        msg = "endog contains NaN values"
        raise ValueError(msg)
    if np.any(np.isinf(endog)):
        msg = "endog contains Inf values"
        raise ValueError(msg)


def x_validate_multivariate_returns__mutmut_5(endog: NDArray[np.float64]) -> None:
    """Validate multivariate returns array.

    Parameters
    ----------
    endog : ndarray
        Returns array.

    Raises
    ------
    ValueError
        If validation fails.
    """
    if endog.ndim != 2:
        msg = f"endog must be 2D (T, k), got {endog.ndim}D"
        raise ValueError(msg)
    if endog.shape[2] < 2:
        msg = f"Need at least 2 series, got {endog.shape[1]}"
        raise ValueError(msg)
    if endog.shape[0] < 20:
        msg = f"Need at least 20 observations, got {endog.shape[0]}"
        raise ValueError(msg)
    if np.any(np.isnan(endog)):
        msg = "endog contains NaN values"
        raise ValueError(msg)
    if np.any(np.isinf(endog)):
        msg = "endog contains Inf values"
        raise ValueError(msg)


def x_validate_multivariate_returns__mutmut_6(endog: NDArray[np.float64]) -> None:
    """Validate multivariate returns array.

    Parameters
    ----------
    endog : ndarray
        Returns array.

    Raises
    ------
    ValueError
        If validation fails.
    """
    if endog.ndim != 2:
        msg = f"endog must be 2D (T, k), got {endog.ndim}D"
        raise ValueError(msg)
    if endog.shape[1] <= 2:
        msg = f"Need at least 2 series, got {endog.shape[1]}"
        raise ValueError(msg)
    if endog.shape[0] < 20:
        msg = f"Need at least 20 observations, got {endog.shape[0]}"
        raise ValueError(msg)
    if np.any(np.isnan(endog)):
        msg = "endog contains NaN values"
        raise ValueError(msg)
    if np.any(np.isinf(endog)):
        msg = "endog contains Inf values"
        raise ValueError(msg)


def x_validate_multivariate_returns__mutmut_7(endog: NDArray[np.float64]) -> None:
    """Validate multivariate returns array.

    Parameters
    ----------
    endog : ndarray
        Returns array.

    Raises
    ------
    ValueError
        If validation fails.
    """
    if endog.ndim != 2:
        msg = f"endog must be 2D (T, k), got {endog.ndim}D"
        raise ValueError(msg)
    if endog.shape[1] < 3:
        msg = f"Need at least 2 series, got {endog.shape[1]}"
        raise ValueError(msg)
    if endog.shape[0] < 20:
        msg = f"Need at least 20 observations, got {endog.shape[0]}"
        raise ValueError(msg)
    if np.any(np.isnan(endog)):
        msg = "endog contains NaN values"
        raise ValueError(msg)
    if np.any(np.isinf(endog)):
        msg = "endog contains Inf values"
        raise ValueError(msg)


def x_validate_multivariate_returns__mutmut_8(endog: NDArray[np.float64]) -> None:
    """Validate multivariate returns array.

    Parameters
    ----------
    endog : ndarray
        Returns array.

    Raises
    ------
    ValueError
        If validation fails.
    """
    if endog.ndim != 2:
        msg = f"endog must be 2D (T, k), got {endog.ndim}D"
        raise ValueError(msg)
    if endog.shape[1] < 2:
        msg = None
        raise ValueError(msg)
    if endog.shape[0] < 20:
        msg = f"Need at least 20 observations, got {endog.shape[0]}"
        raise ValueError(msg)
    if np.any(np.isnan(endog)):
        msg = "endog contains NaN values"
        raise ValueError(msg)
    if np.any(np.isinf(endog)):
        msg = "endog contains Inf values"
        raise ValueError(msg)


def x_validate_multivariate_returns__mutmut_9(endog: NDArray[np.float64]) -> None:
    """Validate multivariate returns array.

    Parameters
    ----------
    endog : ndarray
        Returns array.

    Raises
    ------
    ValueError
        If validation fails.
    """
    if endog.ndim != 2:
        msg = f"endog must be 2D (T, k), got {endog.ndim}D"
        raise ValueError(msg)
    if endog.shape[1] < 2:
        msg = f"Need at least 2 series, got {endog.shape[2]}"
        raise ValueError(msg)
    if endog.shape[0] < 20:
        msg = f"Need at least 20 observations, got {endog.shape[0]}"
        raise ValueError(msg)
    if np.any(np.isnan(endog)):
        msg = "endog contains NaN values"
        raise ValueError(msg)
    if np.any(np.isinf(endog)):
        msg = "endog contains Inf values"
        raise ValueError(msg)


def x_validate_multivariate_returns__mutmut_10(endog: NDArray[np.float64]) -> None:
    """Validate multivariate returns array.

    Parameters
    ----------
    endog : ndarray
        Returns array.

    Raises
    ------
    ValueError
        If validation fails.
    """
    if endog.ndim != 2:
        msg = f"endog must be 2D (T, k), got {endog.ndim}D"
        raise ValueError(msg)
    if endog.shape[1] < 2:
        msg = f"Need at least 2 series, got {endog.shape[1]}"
        raise ValueError(None)
    if endog.shape[0] < 20:
        msg = f"Need at least 20 observations, got {endog.shape[0]}"
        raise ValueError(msg)
    if np.any(np.isnan(endog)):
        msg = "endog contains NaN values"
        raise ValueError(msg)
    if np.any(np.isinf(endog)):
        msg = "endog contains Inf values"
        raise ValueError(msg)


def x_validate_multivariate_returns__mutmut_11(endog: NDArray[np.float64]) -> None:
    """Validate multivariate returns array.

    Parameters
    ----------
    endog : ndarray
        Returns array.

    Raises
    ------
    ValueError
        If validation fails.
    """
    if endog.ndim != 2:
        msg = f"endog must be 2D (T, k), got {endog.ndim}D"
        raise ValueError(msg)
    if endog.shape[1] < 2:
        msg = f"Need at least 2 series, got {endog.shape[1]}"
        raise ValueError(msg)
    if endog.shape[1] < 20:
        msg = f"Need at least 20 observations, got {endog.shape[0]}"
        raise ValueError(msg)
    if np.any(np.isnan(endog)):
        msg = "endog contains NaN values"
        raise ValueError(msg)
    if np.any(np.isinf(endog)):
        msg = "endog contains Inf values"
        raise ValueError(msg)


def x_validate_multivariate_returns__mutmut_12(endog: NDArray[np.float64]) -> None:
    """Validate multivariate returns array.

    Parameters
    ----------
    endog : ndarray
        Returns array.

    Raises
    ------
    ValueError
        If validation fails.
    """
    if endog.ndim != 2:
        msg = f"endog must be 2D (T, k), got {endog.ndim}D"
        raise ValueError(msg)
    if endog.shape[1] < 2:
        msg = f"Need at least 2 series, got {endog.shape[1]}"
        raise ValueError(msg)
    if endog.shape[0] <= 20:
        msg = f"Need at least 20 observations, got {endog.shape[0]}"
        raise ValueError(msg)
    if np.any(np.isnan(endog)):
        msg = "endog contains NaN values"
        raise ValueError(msg)
    if np.any(np.isinf(endog)):
        msg = "endog contains Inf values"
        raise ValueError(msg)


def x_validate_multivariate_returns__mutmut_13(endog: NDArray[np.float64]) -> None:
    """Validate multivariate returns array.

    Parameters
    ----------
    endog : ndarray
        Returns array.

    Raises
    ------
    ValueError
        If validation fails.
    """
    if endog.ndim != 2:
        msg = f"endog must be 2D (T, k), got {endog.ndim}D"
        raise ValueError(msg)
    if endog.shape[1] < 2:
        msg = f"Need at least 2 series, got {endog.shape[1]}"
        raise ValueError(msg)
    if endog.shape[0] < 21:
        msg = f"Need at least 20 observations, got {endog.shape[0]}"
        raise ValueError(msg)
    if np.any(np.isnan(endog)):
        msg = "endog contains NaN values"
        raise ValueError(msg)
    if np.any(np.isinf(endog)):
        msg = "endog contains Inf values"
        raise ValueError(msg)


def x_validate_multivariate_returns__mutmut_14(endog: NDArray[np.float64]) -> None:
    """Validate multivariate returns array.

    Parameters
    ----------
    endog : ndarray
        Returns array.

    Raises
    ------
    ValueError
        If validation fails.
    """
    if endog.ndim != 2:
        msg = f"endog must be 2D (T, k), got {endog.ndim}D"
        raise ValueError(msg)
    if endog.shape[1] < 2:
        msg = f"Need at least 2 series, got {endog.shape[1]}"
        raise ValueError(msg)
    if endog.shape[0] < 20:
        msg = None
        raise ValueError(msg)
    if np.any(np.isnan(endog)):
        msg = "endog contains NaN values"
        raise ValueError(msg)
    if np.any(np.isinf(endog)):
        msg = "endog contains Inf values"
        raise ValueError(msg)


def x_validate_multivariate_returns__mutmut_15(endog: NDArray[np.float64]) -> None:
    """Validate multivariate returns array.

    Parameters
    ----------
    endog : ndarray
        Returns array.

    Raises
    ------
    ValueError
        If validation fails.
    """
    if endog.ndim != 2:
        msg = f"endog must be 2D (T, k), got {endog.ndim}D"
        raise ValueError(msg)
    if endog.shape[1] < 2:
        msg = f"Need at least 2 series, got {endog.shape[1]}"
        raise ValueError(msg)
    if endog.shape[0] < 20:
        msg = f"Need at least 20 observations, got {endog.shape[1]}"
        raise ValueError(msg)
    if np.any(np.isnan(endog)):
        msg = "endog contains NaN values"
        raise ValueError(msg)
    if np.any(np.isinf(endog)):
        msg = "endog contains Inf values"
        raise ValueError(msg)


def x_validate_multivariate_returns__mutmut_16(endog: NDArray[np.float64]) -> None:
    """Validate multivariate returns array.

    Parameters
    ----------
    endog : ndarray
        Returns array.

    Raises
    ------
    ValueError
        If validation fails.
    """
    if endog.ndim != 2:
        msg = f"endog must be 2D (T, k), got {endog.ndim}D"
        raise ValueError(msg)
    if endog.shape[1] < 2:
        msg = f"Need at least 2 series, got {endog.shape[1]}"
        raise ValueError(msg)
    if endog.shape[0] < 20:
        msg = f"Need at least 20 observations, got {endog.shape[0]}"
        raise ValueError(None)
    if np.any(np.isnan(endog)):
        msg = "endog contains NaN values"
        raise ValueError(msg)
    if np.any(np.isinf(endog)):
        msg = "endog contains Inf values"
        raise ValueError(msg)


def x_validate_multivariate_returns__mutmut_17(endog: NDArray[np.float64]) -> None:
    """Validate multivariate returns array.

    Parameters
    ----------
    endog : ndarray
        Returns array.

    Raises
    ------
    ValueError
        If validation fails.
    """
    if endog.ndim != 2:
        msg = f"endog must be 2D (T, k), got {endog.ndim}D"
        raise ValueError(msg)
    if endog.shape[1] < 2:
        msg = f"Need at least 2 series, got {endog.shape[1]}"
        raise ValueError(msg)
    if endog.shape[0] < 20:
        msg = f"Need at least 20 observations, got {endog.shape[0]}"
        raise ValueError(msg)
    if np.any(None):
        msg = "endog contains NaN values"
        raise ValueError(msg)
    if np.any(np.isinf(endog)):
        msg = "endog contains Inf values"
        raise ValueError(msg)


def x_validate_multivariate_returns__mutmut_18(endog: NDArray[np.float64]) -> None:
    """Validate multivariate returns array.

    Parameters
    ----------
    endog : ndarray
        Returns array.

    Raises
    ------
    ValueError
        If validation fails.
    """
    if endog.ndim != 2:
        msg = f"endog must be 2D (T, k), got {endog.ndim}D"
        raise ValueError(msg)
    if endog.shape[1] < 2:
        msg = f"Need at least 2 series, got {endog.shape[1]}"
        raise ValueError(msg)
    if endog.shape[0] < 20:
        msg = f"Need at least 20 observations, got {endog.shape[0]}"
        raise ValueError(msg)
    if np.any(np.isnan(None)):
        msg = "endog contains NaN values"
        raise ValueError(msg)
    if np.any(np.isinf(endog)):
        msg = "endog contains Inf values"
        raise ValueError(msg)


def x_validate_multivariate_returns__mutmut_19(endog: NDArray[np.float64]) -> None:
    """Validate multivariate returns array.

    Parameters
    ----------
    endog : ndarray
        Returns array.

    Raises
    ------
    ValueError
        If validation fails.
    """
    if endog.ndim != 2:
        msg = f"endog must be 2D (T, k), got {endog.ndim}D"
        raise ValueError(msg)
    if endog.shape[1] < 2:
        msg = f"Need at least 2 series, got {endog.shape[1]}"
        raise ValueError(msg)
    if endog.shape[0] < 20:
        msg = f"Need at least 20 observations, got {endog.shape[0]}"
        raise ValueError(msg)
    if np.any(np.isnan(endog)):
        msg = None
        raise ValueError(msg)
    if np.any(np.isinf(endog)):
        msg = "endog contains Inf values"
        raise ValueError(msg)


def x_validate_multivariate_returns__mutmut_20(endog: NDArray[np.float64]) -> None:
    """Validate multivariate returns array.

    Parameters
    ----------
    endog : ndarray
        Returns array.

    Raises
    ------
    ValueError
        If validation fails.
    """
    if endog.ndim != 2:
        msg = f"endog must be 2D (T, k), got {endog.ndim}D"
        raise ValueError(msg)
    if endog.shape[1] < 2:
        msg = f"Need at least 2 series, got {endog.shape[1]}"
        raise ValueError(msg)
    if endog.shape[0] < 20:
        msg = f"Need at least 20 observations, got {endog.shape[0]}"
        raise ValueError(msg)
    if np.any(np.isnan(endog)):
        msg = "XXendog contains NaN valuesXX"
        raise ValueError(msg)
    if np.any(np.isinf(endog)):
        msg = "endog contains Inf values"
        raise ValueError(msg)


def x_validate_multivariate_returns__mutmut_21(endog: NDArray[np.float64]) -> None:
    """Validate multivariate returns array.

    Parameters
    ----------
    endog : ndarray
        Returns array.

    Raises
    ------
    ValueError
        If validation fails.
    """
    if endog.ndim != 2:
        msg = f"endog must be 2D (T, k), got {endog.ndim}D"
        raise ValueError(msg)
    if endog.shape[1] < 2:
        msg = f"Need at least 2 series, got {endog.shape[1]}"
        raise ValueError(msg)
    if endog.shape[0] < 20:
        msg = f"Need at least 20 observations, got {endog.shape[0]}"
        raise ValueError(msg)
    if np.any(np.isnan(endog)):
        msg = "endog contains nan values"
        raise ValueError(msg)
    if np.any(np.isinf(endog)):
        msg = "endog contains Inf values"
        raise ValueError(msg)


def x_validate_multivariate_returns__mutmut_22(endog: NDArray[np.float64]) -> None:
    """Validate multivariate returns array.

    Parameters
    ----------
    endog : ndarray
        Returns array.

    Raises
    ------
    ValueError
        If validation fails.
    """
    if endog.ndim != 2:
        msg = f"endog must be 2D (T, k), got {endog.ndim}D"
        raise ValueError(msg)
    if endog.shape[1] < 2:
        msg = f"Need at least 2 series, got {endog.shape[1]}"
        raise ValueError(msg)
    if endog.shape[0] < 20:
        msg = f"Need at least 20 observations, got {endog.shape[0]}"
        raise ValueError(msg)
    if np.any(np.isnan(endog)):
        msg = "ENDOG CONTAINS NAN VALUES"
        raise ValueError(msg)
    if np.any(np.isinf(endog)):
        msg = "endog contains Inf values"
        raise ValueError(msg)


def x_validate_multivariate_returns__mutmut_23(endog: NDArray[np.float64]) -> None:
    """Validate multivariate returns array.

    Parameters
    ----------
    endog : ndarray
        Returns array.

    Raises
    ------
    ValueError
        If validation fails.
    """
    if endog.ndim != 2:
        msg = f"endog must be 2D (T, k), got {endog.ndim}D"
        raise ValueError(msg)
    if endog.shape[1] < 2:
        msg = f"Need at least 2 series, got {endog.shape[1]}"
        raise ValueError(msg)
    if endog.shape[0] < 20:
        msg = f"Need at least 20 observations, got {endog.shape[0]}"
        raise ValueError(msg)
    if np.any(np.isnan(endog)):
        msg = "endog contains NaN values"
        raise ValueError(None)
    if np.any(np.isinf(endog)):
        msg = "endog contains Inf values"
        raise ValueError(msg)


def x_validate_multivariate_returns__mutmut_24(endog: NDArray[np.float64]) -> None:
    """Validate multivariate returns array.

    Parameters
    ----------
    endog : ndarray
        Returns array.

    Raises
    ------
    ValueError
        If validation fails.
    """
    if endog.ndim != 2:
        msg = f"endog must be 2D (T, k), got {endog.ndim}D"
        raise ValueError(msg)
    if endog.shape[1] < 2:
        msg = f"Need at least 2 series, got {endog.shape[1]}"
        raise ValueError(msg)
    if endog.shape[0] < 20:
        msg = f"Need at least 20 observations, got {endog.shape[0]}"
        raise ValueError(msg)
    if np.any(np.isnan(endog)):
        msg = "endog contains NaN values"
        raise ValueError(msg)
    if np.any(None):
        msg = "endog contains Inf values"
        raise ValueError(msg)


def x_validate_multivariate_returns__mutmut_25(endog: NDArray[np.float64]) -> None:
    """Validate multivariate returns array.

    Parameters
    ----------
    endog : ndarray
        Returns array.

    Raises
    ------
    ValueError
        If validation fails.
    """
    if endog.ndim != 2:
        msg = f"endog must be 2D (T, k), got {endog.ndim}D"
        raise ValueError(msg)
    if endog.shape[1] < 2:
        msg = f"Need at least 2 series, got {endog.shape[1]}"
        raise ValueError(msg)
    if endog.shape[0] < 20:
        msg = f"Need at least 20 observations, got {endog.shape[0]}"
        raise ValueError(msg)
    if np.any(np.isnan(endog)):
        msg = "endog contains NaN values"
        raise ValueError(msg)
    if np.any(np.isinf(None)):
        msg = "endog contains Inf values"
        raise ValueError(msg)


def x_validate_multivariate_returns__mutmut_26(endog: NDArray[np.float64]) -> None:
    """Validate multivariate returns array.

    Parameters
    ----------
    endog : ndarray
        Returns array.

    Raises
    ------
    ValueError
        If validation fails.
    """
    if endog.ndim != 2:
        msg = f"endog must be 2D (T, k), got {endog.ndim}D"
        raise ValueError(msg)
    if endog.shape[1] < 2:
        msg = f"Need at least 2 series, got {endog.shape[1]}"
        raise ValueError(msg)
    if endog.shape[0] < 20:
        msg = f"Need at least 20 observations, got {endog.shape[0]}"
        raise ValueError(msg)
    if np.any(np.isnan(endog)):
        msg = "endog contains NaN values"
        raise ValueError(msg)
    if np.any(np.isinf(endog)):
        msg = None
        raise ValueError(msg)


def x_validate_multivariate_returns__mutmut_27(endog: NDArray[np.float64]) -> None:
    """Validate multivariate returns array.

    Parameters
    ----------
    endog : ndarray
        Returns array.

    Raises
    ------
    ValueError
        If validation fails.
    """
    if endog.ndim != 2:
        msg = f"endog must be 2D (T, k), got {endog.ndim}D"
        raise ValueError(msg)
    if endog.shape[1] < 2:
        msg = f"Need at least 2 series, got {endog.shape[1]}"
        raise ValueError(msg)
    if endog.shape[0] < 20:
        msg = f"Need at least 20 observations, got {endog.shape[0]}"
        raise ValueError(msg)
    if np.any(np.isnan(endog)):
        msg = "endog contains NaN values"
        raise ValueError(msg)
    if np.any(np.isinf(endog)):
        msg = "XXendog contains Inf valuesXX"
        raise ValueError(msg)


def x_validate_multivariate_returns__mutmut_28(endog: NDArray[np.float64]) -> None:
    """Validate multivariate returns array.

    Parameters
    ----------
    endog : ndarray
        Returns array.

    Raises
    ------
    ValueError
        If validation fails.
    """
    if endog.ndim != 2:
        msg = f"endog must be 2D (T, k), got {endog.ndim}D"
        raise ValueError(msg)
    if endog.shape[1] < 2:
        msg = f"Need at least 2 series, got {endog.shape[1]}"
        raise ValueError(msg)
    if endog.shape[0] < 20:
        msg = f"Need at least 20 observations, got {endog.shape[0]}"
        raise ValueError(msg)
    if np.any(np.isnan(endog)):
        msg = "endog contains NaN values"
        raise ValueError(msg)
    if np.any(np.isinf(endog)):
        msg = "endog contains inf values"
        raise ValueError(msg)


def x_validate_multivariate_returns__mutmut_29(endog: NDArray[np.float64]) -> None:
    """Validate multivariate returns array.

    Parameters
    ----------
    endog : ndarray
        Returns array.

    Raises
    ------
    ValueError
        If validation fails.
    """
    if endog.ndim != 2:
        msg = f"endog must be 2D (T, k), got {endog.ndim}D"
        raise ValueError(msg)
    if endog.shape[1] < 2:
        msg = f"Need at least 2 series, got {endog.shape[1]}"
        raise ValueError(msg)
    if endog.shape[0] < 20:
        msg = f"Need at least 20 observations, got {endog.shape[0]}"
        raise ValueError(msg)
    if np.any(np.isnan(endog)):
        msg = "endog contains NaN values"
        raise ValueError(msg)
    if np.any(np.isinf(endog)):
        msg = "ENDOG CONTAINS INF VALUES"
        raise ValueError(msg)


def x_validate_multivariate_returns__mutmut_30(endog: NDArray[np.float64]) -> None:
    """Validate multivariate returns array.

    Parameters
    ----------
    endog : ndarray
        Returns array.

    Raises
    ------
    ValueError
        If validation fails.
    """
    if endog.ndim != 2:
        msg = f"endog must be 2D (T, k), got {endog.ndim}D"
        raise ValueError(msg)
    if endog.shape[1] < 2:
        msg = f"Need at least 2 series, got {endog.shape[1]}"
        raise ValueError(msg)
    if endog.shape[0] < 20:
        msg = f"Need at least 20 observations, got {endog.shape[0]}"
        raise ValueError(msg)
    if np.any(np.isnan(endog)):
        msg = "endog contains NaN values"
        raise ValueError(msg)
    if np.any(np.isinf(endog)):
        msg = "endog contains Inf values"
        raise ValueError(None)


x_validate_multivariate_returns__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_validate_multivariate_returns__mutmut_1": x_validate_multivariate_returns__mutmut_1,
    "x_validate_multivariate_returns__mutmut_2": x_validate_multivariate_returns__mutmut_2,
    "x_validate_multivariate_returns__mutmut_3": x_validate_multivariate_returns__mutmut_3,
    "x_validate_multivariate_returns__mutmut_4": x_validate_multivariate_returns__mutmut_4,
    "x_validate_multivariate_returns__mutmut_5": x_validate_multivariate_returns__mutmut_5,
    "x_validate_multivariate_returns__mutmut_6": x_validate_multivariate_returns__mutmut_6,
    "x_validate_multivariate_returns__mutmut_7": x_validate_multivariate_returns__mutmut_7,
    "x_validate_multivariate_returns__mutmut_8": x_validate_multivariate_returns__mutmut_8,
    "x_validate_multivariate_returns__mutmut_9": x_validate_multivariate_returns__mutmut_9,
    "x_validate_multivariate_returns__mutmut_10": x_validate_multivariate_returns__mutmut_10,
    "x_validate_multivariate_returns__mutmut_11": x_validate_multivariate_returns__mutmut_11,
    "x_validate_multivariate_returns__mutmut_12": x_validate_multivariate_returns__mutmut_12,
    "x_validate_multivariate_returns__mutmut_13": x_validate_multivariate_returns__mutmut_13,
    "x_validate_multivariate_returns__mutmut_14": x_validate_multivariate_returns__mutmut_14,
    "x_validate_multivariate_returns__mutmut_15": x_validate_multivariate_returns__mutmut_15,
    "x_validate_multivariate_returns__mutmut_16": x_validate_multivariate_returns__mutmut_16,
    "x_validate_multivariate_returns__mutmut_17": x_validate_multivariate_returns__mutmut_17,
    "x_validate_multivariate_returns__mutmut_18": x_validate_multivariate_returns__mutmut_18,
    "x_validate_multivariate_returns__mutmut_19": x_validate_multivariate_returns__mutmut_19,
    "x_validate_multivariate_returns__mutmut_20": x_validate_multivariate_returns__mutmut_20,
    "x_validate_multivariate_returns__mutmut_21": x_validate_multivariate_returns__mutmut_21,
    "x_validate_multivariate_returns__mutmut_22": x_validate_multivariate_returns__mutmut_22,
    "x_validate_multivariate_returns__mutmut_23": x_validate_multivariate_returns__mutmut_23,
    "x_validate_multivariate_returns__mutmut_24": x_validate_multivariate_returns__mutmut_24,
    "x_validate_multivariate_returns__mutmut_25": x_validate_multivariate_returns__mutmut_25,
    "x_validate_multivariate_returns__mutmut_26": x_validate_multivariate_returns__mutmut_26,
    "x_validate_multivariate_returns__mutmut_27": x_validate_multivariate_returns__mutmut_27,
    "x_validate_multivariate_returns__mutmut_28": x_validate_multivariate_returns__mutmut_28,
    "x_validate_multivariate_returns__mutmut_29": x_validate_multivariate_returns__mutmut_29,
    "x_validate_multivariate_returns__mutmut_30": x_validate_multivariate_returns__mutmut_30,
}
x_validate_multivariate_returns__mutmut_orig.__name__ = "x_validate_multivariate_returns"
