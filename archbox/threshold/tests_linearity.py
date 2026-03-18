"""Linearity tests for threshold and STAR models.

This module provides statistical tests for:
1. Linearity vs STAR (Luukkonen-Saikkonen-Terasvirta 1988)
2. Transition type selection: LSTAR vs ESTAR (Terasvirta 1994)
3. Linearity vs TAR (Tsay 1989)
4. Threshold effect test with bootstrap (Hansen 1996)

References
----------
- Luukkonen, R., Saikkonen, P. & Terasvirta, T. (1988). Testing Linearity
  Against Smooth Transition Autoregressive Models. Biometrika, 75(3), 491-499.
- Terasvirta, T. (1994). Specification, Estimation, and Evaluation of
  Smooth Transition Autoregressive Models. JASA, 89(425), 208-218.
- Tsay, R.S. (1989). Testing and Modeling Threshold Autoregressive Processes.
  JASA, 84(405), 231-240.
- Hansen, B.E. (1996). Inference When a Nuisance Parameter Is Not Identified
  Under the Null Hypothesis. Econometrica, 64(2), 413-430.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy import stats

from archbox.threshold.results import TestResult


def _build_ar_matrices(
    y: NDArray[np.float64], order: int, delay: int
) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    """Build dependent variable, regressors, and transition variable.

    Parameters
    ----------
    y : ndarray
        Full time series.
    order : int
        AR order p.
    delay : int
        Delay d for transition variable.

    Returns
    -------
    y_dep : ndarray, shape (t_eff,)
    x_mat : ndarray, shape (t_eff, p+1)
    s : ndarray, shape (t_eff,)
    """
    y = np.asarray(y, dtype=np.float64).ravel()
    p = order
    d = delay
    start = max(p, d)
    t_eff = len(y) - start

    y_dep = y[start:]
    x_mat = np.ones((t_eff, p + 1))
    for lag in range(1, p + 1):
        x_mat[:, lag] = y[start - lag : len(y) - lag]

    s = y[start - d : len(y) - d]
    return y_dep, x_mat, s


def linearity_test(
    y: NDArray[np.float64],
    order: int = 1,
    delay: int = 1,
) -> TestResult:
    """Luukkonen-Saikkonen-Terasvirta (1988) LM test for linearity vs STAR.

    Tests H0: AR(p) linear model vs H1: STAR model.

    Procedure:
    1. Estimate AR(p): y_t = x_t' phi + e_t
    2. Auxiliary regression: e_t = x_t'b0 + x_t'*s_t*b1 + x_t'*s_t^2*b2 + x_t'*s_t^3*b3 + u_t
    3. F-test: H0: b1 = b2 = b3 = 0

    Parameters
    ----------
    y : ndarray
        Time series.
    order : int
        AR order p (default 1).
    delay : int
        Delay d for transition variable s_t = y_{t-d} (default 1).

    Returns
    -------
    TestResult
        Contains F-statistic, p-value, and test name.
    """
    y_dep, x_mat, s = _build_ar_matrices(y, order, delay)
    n_obs = len(y_dep)
    k = order + 1  # number of regressors including constant

    # Step 1: Estimate linear AR(p)
    beta_ols = np.linalg.lstsq(x_mat, y_dep, rcond=None)[0]
    resid = y_dep - x_mat @ beta_ols

    # Step 2: Build auxiliary regression matrix
    # z = [x_mat, x_mat*s, x_mat*s^2, x_mat*s^3]
    z0 = x_mat  # x_t' * beta_0
    z1 = x_mat * s[:, np.newaxis]  # x_t' * s_t * beta_1
    z2 = x_mat * (s**2)[:, np.newaxis]  # x_t' * s_t^2 * beta_2
    z3 = x_mat * (s**3)[:, np.newaxis]  # x_t' * s_t^3 * beta_3
    z_full = np.hstack([z0, z1, z2, z3])

    # Step 3: F-test
    # Restricted model (H0): e_t = z0 * b0 + u_t (which gives SSR0 = RSS from AR)
    rss_restricted = float(np.sum(resid**2))

    # Unrestricted model: e_t = z_full * b + u_t
    beta_aux = np.linalg.lstsq(z_full, resid, rcond=None)[0]
    resid_aux = resid - z_full @ beta_aux
    rss_unrestricted = float(np.sum(resid_aux**2))

    # Degrees of freedom
    df_num = 3 * k  # number of restrictions (beta_1, beta_2, beta_3)
    df_den = n_obs - 4 * k

    if df_den <= 0:
        return TestResult(
            statistic=np.nan,
            pvalue=np.nan,
            test_name="Luukkonen-Saikkonen-Terasvirta",
            detail=f"Insufficient degrees of freedom: df_den={df_den}",
        )

    # F-statistic
    f_stat = ((rss_restricted - rss_unrestricted) / df_num) / (rss_unrestricted / df_den)
    p_value = 1.0 - stats.f.cdf(f_stat, df_num, df_den)

    return TestResult(
        statistic=float(f_stat),
        pvalue=float(p_value),
        test_name="Luukkonen-Saikkonen-Terasvirta",
        detail=f"F({df_num}, {df_den}) = {f_stat:.4f}, p = {p_value:.4f}",
    )


def transition_type_test(
    y: NDArray[np.float64],
    order: int = 1,
    delay: int = 1,
) -> dict[str, Any]:
    """Terasvirta (1994) test for transition type: LSTAR vs ESTAR.

    After rejecting linearity, this test determines whether the transition
    function is logistic (LSTAR) or exponential (ESTAR).

    Decision rule:
    - If p3 < min(p2, p4): ESTAR
    - Otherwise: LSTAR

    Parameters
    ----------
    y : ndarray
        Time series.
    order : int
        AR order p.
    delay : int
        Delay d.

    Returns
    -------
    dict
        Keys: 'recommended' ('LSTAR' or 'ESTAR'), 'p2', 'p3', 'p4',
        'F2', 'F3', 'F4', 'detail'.
    """
    y_dep, x_mat, s = _build_ar_matrices(y, order, delay)
    n_obs = len(y_dep)
    k = order + 1

    # Estimate linear AR
    beta_ols = np.linalg.lstsq(x_mat, y_dep, rcond=None)[0]
    resid = y_dep - x_mat @ beta_ols

    # Build auxiliary matrices
    z0 = x_mat
    z1 = x_mat * s[:, np.newaxis]
    z2 = x_mat * (s**2)[:, np.newaxis]
    z3 = x_mat * (s**3)[:, np.newaxis]

    # H04: beta_3 = 0 (given beta_1, beta_2 free)
    z_unres_4 = np.hstack([z0, z1, z2, z3])
    z_res_4 = np.hstack([z0, z1, z2])

    beta_u4 = np.linalg.lstsq(z_unres_4, resid, rcond=None)[0]
    beta_r4 = np.linalg.lstsq(z_res_4, resid, rcond=None)[0]
    rss_u4 = float(np.sum((resid - z_unres_4 @ beta_u4) ** 2))
    rss_r4 = float(np.sum((resid - z_res_4 @ beta_r4) ** 2))

    df_num_4 = k
    df_den_4 = n_obs - z_unres_4.shape[1]
    if df_den_4 > 0:
        f4 = ((rss_r4 - rss_u4) / df_num_4) / (rss_u4 / df_den_4)
        p4 = 1.0 - stats.f.cdf(f4, df_num_4, df_den_4)
    else:
        f4, p4 = np.nan, np.nan

    # H03: beta_2 = 0 (given beta_3 = 0, beta_1 free)
    z_unres_3 = np.hstack([z0, z1, z2])
    z_res_3 = np.hstack([z0, z1])

    beta_u3 = np.linalg.lstsq(z_unres_3, resid, rcond=None)[0]
    beta_r3 = np.linalg.lstsq(z_res_3, resid, rcond=None)[0]
    rss_u3 = float(np.sum((resid - z_unres_3 @ beta_u3) ** 2))
    rss_r3 = float(np.sum((resid - z_res_3 @ beta_r3) ** 2))

    df_num_3 = k
    df_den_3 = n_obs - z_unres_3.shape[1]
    if df_den_3 > 0:
        f3 = ((rss_r3 - rss_u3) / df_num_3) / (rss_u3 / df_den_3)
        p3 = 1.0 - stats.f.cdf(f3, df_num_3, df_den_3)
    else:
        f3, p3 = np.nan, np.nan

    # H02: beta_1 = 0 (given beta_2 = beta_3 = 0)
    z_unres_2 = np.hstack([z0, z1])
    z_res_2 = z0

    beta_u2 = np.linalg.lstsq(z_unres_2, resid, rcond=None)[0]
    beta_r2 = np.linalg.lstsq(z_res_2, resid, rcond=None)[0]
    rss_u2 = float(np.sum((resid - z_unres_2 @ beta_u2) ** 2))
    rss_r2 = float(np.sum((resid - z_res_2 @ beta_r2) ** 2))

    df_num_2 = k
    df_den_2 = n_obs - z_unres_2.shape[1]
    if df_den_2 > 0:
        f2 = ((rss_r2 - rss_u2) / df_num_2) / (rss_u2 / df_den_2)
        p2 = 1.0 - stats.f.cdf(f2, df_num_2, df_den_2)
    else:
        f2, p2 = np.nan, np.nan

    # Decision rule
    if np.isnan(p2) or np.isnan(p3) or np.isnan(p4):
        recommended = "LSTAR"  # default
    elif p3 < min(p2, p4):
        recommended = "ESTAR"
    else:
        recommended = "LSTAR"

    return {
        "recommended": recommended,
        "p2": float(p2),
        "p3": float(p3),
        "p4": float(p4),
        "F2": float(f2),
        "F3": float(f3),
        "F4": float(f4),
        "detail": f"p2={p2:.4f}, p3={p3:.4f}, p4={p4:.4f} -> {recommended}",
    }


def tsay_test(
    y: NDArray[np.float64],
    order: int = 1,
    delay: int = 1,
) -> TestResult:
    """Tsay (1989) test for threshold nonlinearity.

    Tests H0: linear AR vs H1: TAR using arranged autoregression approach.

    Procedure:
    1. Estimate AR(p): y_t = x_t' phi + e_t
    2. Sort by threshold variable s_t = y_{t-d}
    3. Regress e_t on x_t * e_t (predictive power of nonlinear terms)
    4. F-test for significance

    Parameters
    ----------
    y : ndarray
        Time series.
    order : int
        AR order p.
    delay : int
        Delay d.

    Returns
    -------
    TestResult
        F-statistic and p-value.
    """
    y_dep, x_mat, s = _build_ar_matrices(y, order, delay)
    n_obs = len(y_dep)
    k = order + 1

    # Step 1: Estimate linear AR(p)
    beta_ols = np.linalg.lstsq(x_mat, y_dep, rcond=None)[0]
    resid = y_dep - x_mat @ beta_ols

    # Step 3: Arranged autoregression
    # Regress residuals on cross-products of regressors and threshold variable
    z_cross = x_mat * s[:, np.newaxis]
    z_full = np.hstack([x_mat, z_cross])

    # F-test: restricted (just x_mat) vs unrestricted (x_mat + x_mat*s)
    rss_restricted = float(np.sum(resid**2))

    beta_full = np.linalg.lstsq(z_full, resid, rcond=None)[0]
    resid_full = resid - z_full @ beta_full
    rss_unrestricted = float(np.sum(resid_full**2))

    df_num = k  # additional parameters from x_mat*s
    df_den = n_obs - 2 * k

    if df_den <= 0:
        return TestResult(
            statistic=np.nan,
            pvalue=np.nan,
            test_name="Tsay",
            detail=f"Insufficient degrees of freedom: df_den={df_den}",
        )

    f_stat = ((rss_restricted - rss_unrestricted) / df_num) / (rss_unrestricted / df_den)
    p_value = 1.0 - stats.f.cdf(f_stat, df_num, df_den)

    return TestResult(
        statistic=float(f_stat),
        pvalue=float(p_value),
        test_name="Tsay",
        detail=f"F({df_num}, {df_den}) = {f_stat:.4f}, p = {p_value:.4f}",
    )


def hansen_threshold_test(
    y: NDArray[np.float64],
    order: int = 1,
    delay: int = 1,
    n_bootstrap: int = 1000,
    seed: int | None = None,
) -> TestResult:
    """Hansen (1996) bootstrap threshold test (sup-LM).

    Tests H0: no threshold effect using a bootstrap procedure.

    Procedure:
    1. For each threshold candidate c, compute LM statistic
    2. sup-LM = max_c LM(c)
    3. Bootstrap to obtain null distribution
    4. p-value = proportion of bootstrap sup-LM > observed sup-LM

    Parameters
    ----------
    y : ndarray
        Time series.
    order : int
        AR order p.
    delay : int
        Delay d.
    n_bootstrap : int
        Number of bootstrap replications (default 1000).
    seed : int, optional
        Random seed.

    Returns
    -------
    TestResult
        sup-LM statistic and bootstrap p-value.
    """
    rng = np.random.default_rng(seed)
    y_dep, x_mat, s = _build_ar_matrices(y, order, delay)
    n_obs = len(y_dep)
    k = order + 1

    # Estimate linear AR
    beta_ols = np.linalg.lstsq(x_mat, y_dep, rcond=None)[0]
    resid = y_dep - x_mat @ beta_ols

    # Grid of threshold values (percentiles 15%-85%)
    s_sorted = np.sort(s)
    lo = int(0.15 * n_obs)
    hi = int(0.85 * n_obs)
    if lo >= hi:
        lo = 0
        hi = n_obs - 1
    grid = np.unique(s_sorted[lo:hi])
    if len(grid) > 200:
        grid = np.linspace(float(grid[0]), float(grid[-1]), 200)

    def compute_sup_lm(resid_vec: NDArray[np.float64]) -> float:
        """Compute sup-LM statistic over threshold grid."""
        max_lm = 0.0
        rss_total = float(np.sum(resid_vec**2))

        for c in grid:
            mask1 = s <= c
            mask2 = s > c
            n1, n2 = mask1.sum(), mask2.sum()
            if n1 < k + 1 or n2 < k + 1:
                continue

            # LM stat: compare RSS of restricted vs unrestricted
            rss1 = float(np.sum((resid_vec[mask1] - np.mean(resid_vec[mask1])) ** 2))
            rss2 = float(np.sum((resid_vec[mask2] - np.mean(resid_vec[mask2])) ** 2))
            rss_split = rss1 + rss2
            lm = n_obs * (rss_total - rss_split) / rss_total
            if lm > max_lm:
                max_lm = lm

        return max_lm

    # Observed sup-LM
    sup_lm_obs = compute_sup_lm(resid)

    # Bootstrap
    count_exceed = 0
    for _ in range(n_bootstrap):
        # Wild bootstrap: resid_b = resid * v, v ~ Rademacher
        v = rng.choice([-1.0, 1.0], size=n_obs)
        resid_b = resid * v
        sup_lm_b = compute_sup_lm(resid_b)
        if sup_lm_b >= sup_lm_obs:
            count_exceed += 1

    p_value = count_exceed / n_bootstrap

    return TestResult(
        statistic=float(sup_lm_obs),
        pvalue=float(p_value),
        test_name="Hansen Bootstrap Threshold",
        detail=(f"sup-LM = {sup_lm_obs:.4f}, bootstrap p = {p_value:.4f} ({n_bootstrap} reps)"),
    )
