"""Shared estimation machinery for hard-threshold models (TAR and SETAR).

Both TAR and SETAR minimise the conditional sum of squares over a grid of
threshold values, then run OLS regime by regime. The routines here implement
that once for two and three regimes so that the two models cannot drift apart.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

import numpy as np
from numpy.typing import NDArray

from archbox.threshold.base import count_params
from archbox.threshold.results import ThresholdResults
from archbox.threshold.tests_linearity import linearity_test_from_parts

if TYPE_CHECKING:
    from archbox.threshold.base import ThresholdModel


class RegimeFit(NamedTuple):
    """Outcome of fitting a hard-threshold model with known thresholds."""

    betas: list[NDArray[np.float64]]
    resid: NDArray[np.float64]
    sigma2: list[float]
    counts: list[int]
    loglike: float
    rss: float


def _ols_rss(y: NDArray[np.float64], x_mat: NDArray[np.float64]) -> float:
    """Residual sum of squares of an OLS regression of y on x_mat."""
    beta = np.linalg.lstsq(x_mat, y, rcond=None)[0]
    resid = y - x_mat @ beta
    return float(np.sum(resid**2))


def threshold_grid(
    s: NDArray[np.float64], grid_points: int, trim: float = 0.15
) -> NDArray[np.float64]:
    """Candidate thresholds between the ``trim`` and ``1 - trim`` quantiles of s.

    Parameters
    ----------
    s : ndarray
        Transition variable.
    grid_points : int
        Number of candidate values.
    trim : float
        Fraction of the sample trimmed at each end.

    Returns
    -------
    ndarray
        Sorted candidate thresholds.
    """
    s_sorted = np.sort(s)
    n = len(s_sorted)
    lo = int(trim * n)
    hi = int((1.0 - trim) * n)
    if lo >= hi:
        lo, hi = 0, n - 1
    return np.linspace(s_sorted[lo], s_sorted[hi], max(grid_points, 2))


def regime_masks(s: NDArray[np.float64], thresholds: list[float]) -> list[NDArray[np.bool_]]:
    """Boolean regime membership masks for a list of ordered thresholds.

    Parameters
    ----------
    s : ndarray
        Transition variable.
    thresholds : list[float]
        Ordered thresholds (length ``n_regimes - 1``).

    Returns
    -------
    list of ndarray
        One boolean mask per regime.
    """
    edges = [-np.inf, *thresholds, np.inf]
    return [(s > edges[i]) & (s <= edges[i + 1]) for i in range(len(edges) - 1)]


def search_thresholds(
    y: NDArray[np.float64],
    x_mat: NDArray[np.float64],
    s: NDArray[np.float64],
    n_regimes: int,
    grid_points: int,
    min_obs: int,
    trim: float = 0.15,
) -> list[float]:
    """Grid search for the threshold(s) minimising the total RSS.

    Parameters
    ----------
    y : ndarray
        Dependent variable.
    x_mat : ndarray
        Design matrix.
    s : ndarray
        Transition variable.
    n_regimes : int
        2 or 3.
    grid_points : int
        Number of grid points (a coarser grid is used for three regimes,
        where the search is two-dimensional).
    min_obs : int
        Minimum number of observations per regime.
    trim : float
        Quantile trimming for the grid.

    Returns
    -------
    list[float]
        Estimated threshold(s), length ``n_regimes - 1``.
    """
    if n_regimes == 2:
        grid = threshold_grid(s, grid_points, trim)
        best_rss = np.inf
        best = [float(np.median(s))]
        for c in grid:
            mask1 = s <= c
            mask2 = ~mask1
            if mask1.sum() < min_obs or mask2.sum() < min_obs:
                continue
            rss = _ols_rss(y[mask1], x_mat[mask1]) + _ols_rss(y[mask2], x_mat[mask2])
            if rss < best_rss:
                best_rss = rss
                best = [float(c)]
        return best

    grid = threshold_grid(s, min(grid_points, 100), trim)
    best_rss = np.inf
    best = [float(np.percentile(s, 33)), float(np.percentile(s, 67))]
    for i, c1 in enumerate(grid):
        mask1 = s <= c1
        n1 = int(mask1.sum())
        if n1 < min_obs:
            continue
        rss1 = _ols_rss(y[mask1], x_mat[mask1])
        if rss1 >= best_rss:
            continue
        for c2 in grid[i + 1 :]:
            mask2 = (s > c1) & (s <= c2)
            mask3 = s > c2
            if mask2.sum() < min_obs or mask3.sum() < min_obs:
                continue
            rss = rss1 + _ols_rss(y[mask2], x_mat[mask2]) + _ols_rss(y[mask3], x_mat[mask3])
            if rss < best_rss:
                best_rss = rss
                best = [float(c1), float(c2)]
    return best


def fit_given_thresholds(
    y: NDArray[np.float64],
    x_mat: NDArray[np.float64],
    s: NDArray[np.float64],
    thresholds: list[float],
) -> RegimeFit:
    """OLS regime by regime for known thresholds, with the Gaussian log-likelihood.

    Parameters
    ----------
    y : ndarray
        Dependent variable.
    x_mat : ndarray
        Design matrix.
    s : ndarray
        Transition variable.
    thresholds : list[float]
        Ordered thresholds.

    Returns
    -------
    RegimeFit
        Coefficients, residuals, variances, regime counts, log-likelihood, RSS.
    """
    masks = regime_masks(s, thresholds)
    betas: list[NDArray[np.float64]] = []
    sigma2: list[float] = []
    counts: list[int] = []
    resid = np.empty(len(y))
    loglike = 0.0
    rss_total = 0.0

    for mask in masks:
        n_i = int(mask.sum())
        counts.append(n_i)
        if n_i == 0:
            betas.append(np.zeros(x_mat.shape[1]))
            sigma2.append(1e-12)
            continue
        beta = np.linalg.lstsq(x_mat[mask], y[mask], rcond=None)[0].astype(np.float64)
        res_i = y[mask] - x_mat[mask] @ beta
        rss_i = float(np.sum(res_i**2))
        s2_i = max(rss_i / n_i, 1e-12)
        betas.append(beta)
        sigma2.append(s2_i)
        resid[mask] = res_i
        rss_total += rss_i
        loglike += -0.5 * n_i * (np.log(2 * np.pi) + np.log(s2_i)) - rss_i / (2 * s2_i)

    return RegimeFit(
        betas=betas,
        resid=resid,
        sigma2=sigma2,
        counts=counts,
        loglike=float(loglike),
        rss=float(rss_total),
    )


def build_results(
    model: ThresholdModel,
    y: NDArray[np.float64],
    x_mat: NDArray[np.float64],
    s: NDArray[np.float64],
    delay: int,
    grid_points: int | None = None,
    include_delay_param: bool = False,
) -> ThresholdResults:
    """Estimate and package a hard-threshold model (TAR or SETAR).

    Parameters
    ----------
    model : ThresholdModel
        The model instance (used for order, number of regimes and naming).
    y : ndarray
        Dependent variable of the effective sample.
    x_mat : ndarray
        Design matrix of the effective sample.
    s : ndarray
        Transition variable of the effective sample.
    delay : int
        Delay used to build ``s`` (stored on the results).
    grid_points : int, optional
        Number of threshold grid points; defaults to ``model.grid_points``.
    include_delay_param : bool
        Whether the delay was selected from the data and therefore counts as
        an estimated parameter in AIC/BIC.

    Returns
    -------
    ThresholdResults
    """
    n_regimes = model.n_regimes
    if grid_points is None:
        grid_points = int(getattr(model, "grid_points", 300))

    thresholds = search_thresholds(y, x_mat, s, n_regimes, grid_points, min_obs=model.order + 2)
    fit = fit_given_thresholds(y, x_mat, s, thresholds)

    transition_params_array = np.asarray(thresholds, dtype=np.float64)
    g_values = model._transition_function(s, transition_params_array)

    t_eff = len(y)
    # AR coefficients per regime + thresholds + one variance per regime
    # (+ the delay when it was selected from the data).
    n_params = count_params(
        n_regimes,
        model.order,
        n_transition=n_regimes - 1,
        n_variances=n_regimes,
        include_delay=include_delay_param,
    )
    aic = -2.0 * fit.loglike + 2.0 * n_params
    bic = -2.0 * fit.loglike + np.log(t_eff) * n_params

    if n_regimes == 2:
        threshold: float | list[float] = float(thresholds[0])
        transition_params = {"c": float(thresholds[0])}
    else:
        threshold = [float(c) for c in thresholds]
        transition_params = {f"c_{i + 1}": float(c) for i, c in enumerate(thresholds)}

    return ThresholdResults(
        model_name=model.model_name,
        params={f"regime_{i + 1}": beta for i, beta in enumerate(fit.betas)},
        threshold=threshold,
        delay=delay,
        transition_params=transition_params,
        transition_params_array=transition_params_array,
        params_regimes=list(fit.betas),
        regime_assignments=g_values,
        transition_values=g_values,
        resid=fit.resid,
        sigma2={f"regime_{i + 1}": s2 for i, s2 in enumerate(fit.sigma2)},
        loglike=fit.loglike,
        aic=float(aic),
        bic=float(bic),
        nobs=t_eff,
        order=model.order,
        n_regimes=n_regimes,
        endog=model.endog,
        linearity_test=linearity_test_from_parts(y, x_mat, s),
        converged=True,
        param_names=model.param_names,
        _model=model,
    )
