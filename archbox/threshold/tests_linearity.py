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

# Relative size of the component of a candidate regressor orthogonal to the
# columns already in the design below which the candidate is treated as a
# duplicate (rank-deficient) column.
_RANK_TOL = 1e-7


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


def _augment(
    base: NDArray[np.float64], candidates: NDArray[np.float64]
) -> tuple[NDArray[np.float64], int]:
    """Append the candidate columns that genuinely add rank to ``base``.

    When the delay satisfies d <= p the transition variable s_t = y_{t-d} is
    itself one of the regressors, so auxiliary terms such as ``1 * s_t`` merely
    duplicate a column already present. Adding them makes the design
    rank-deficient and overstates the number of restrictions. Each candidate is
    therefore kept only if its component orthogonal to the columns already
    selected is non-negligible.

    Parameters
    ----------
    base : ndarray, shape (n, k)
        Columns always kept (assumed to have full column rank).
    candidates : ndarray, shape (n, m)
        Candidate columns, considered in order.

    Returns
    -------
    design : ndarray, shape (n, k + n_added)
        Base columns followed by the retained candidates.
    n_added : int
        Number of retained candidate columns (the numerator degrees of freedom).
    """
    q, _ = np.linalg.qr(base)
    kept: list[NDArray[np.float64]] = []
    for j in range(candidates.shape[1]):
        col = candidates[:, j]
        norm = float(np.linalg.norm(col))
        if norm == 0.0:
            continue
        resid = col - q @ (q.T @ col)
        resid_norm = float(np.linalg.norm(resid))
        if resid_norm / norm > _RANK_TOL:
            kept.append(col)
            q = np.column_stack([q, resid / resid_norm])
    if not kept:
        return base.copy(), 0
    return np.column_stack([base, *kept]), len(kept)


def _f_test(
    resid: NDArray[np.float64],
    base: NDArray[np.float64],
    candidates: NDArray[np.float64],
    rss_restricted: float | None = None,
) -> tuple[float, float, int, int]:
    """F test of the added columns in an auxiliary regression of ``resid``.

    Parameters
    ----------
    resid : ndarray, shape (n,)
        Dependent variable of the auxiliary regression (OLS residuals).
    base : ndarray, shape (n, k)
        Regressors imposed under the null.
    candidates : ndarray, shape (n, m)
        Additional regressors tested for joint significance.
    rss_restricted : float, optional
        RSS under the null. Recomputed from ``base`` when omitted.

    Returns
    -------
    f_stat, p_value, df_num, df_den
        NaN statistics when there are no genuinely added columns or no
        residual degrees of freedom.
    """
    n_obs = len(resid)
    design, n_added = _augment(base, candidates)

    if rss_restricted is None:
        beta_r = np.linalg.lstsq(base, resid, rcond=None)[0]
        rss_restricted = float(np.sum((resid - base @ beta_r) ** 2))

    df_num = n_added
    df_den = n_obs - design.shape[1]
    if df_num == 0 or df_den <= 0:
        return float("nan"), float("nan"), df_num, df_den

    beta_u = np.linalg.lstsq(design, resid, rcond=None)[0]
    rss_unrestricted = float(np.sum((resid - design @ beta_u) ** 2))
    if rss_unrestricted <= 0.0:
        return float("nan"), float("nan"), df_num, df_den

    f_stat = ((rss_restricted - rss_unrestricted) / df_num) / (rss_unrestricted / df_den)
    p_value = float(stats.f.sf(f_stat, df_num, df_den))
    return float(f_stat), p_value, df_num, df_den


def _star_terms(
    x_mat: NDArray[np.float64], s: NDArray[np.float64], power: int
) -> NDArray[np.float64]:
    """Auxiliary regressors x_t * s_t^power."""
    return x_mat * (s**power)[:, np.newaxis]


def linearity_test_from_parts(
    y_dep: NDArray[np.float64],
    x_mat: NDArray[np.float64],
    s: NDArray[np.float64],
) -> TestResult:
    """LST linearity test from pre-built regression matrices.

    Parameters
    ----------
    y_dep : ndarray, shape (n,)
        Dependent variable.
    x_mat : ndarray, shape (n, p+1)
        Design matrix [1, y_{t-1}, ..., y_{t-p}].
    s : ndarray, shape (n,)
        Transition variable.

    Returns
    -------
    TestResult
        F-statistic, p-value, and test name.
    """
    beta_ols = np.linalg.lstsq(x_mat, y_dep, rcond=None)[0]
    resid = y_dep - x_mat @ beta_ols
    rss_restricted = float(np.sum(resid**2))

    candidates = np.hstack([_star_terms(x_mat, s, j) for j in (1, 2, 3)])
    f_stat, p_value, df_num, df_den = _f_test(resid, x_mat, candidates, rss_restricted)

    if not np.isfinite(f_stat):
        return TestResult(
            statistic=float("nan"),
            pvalue=float("nan"),
            test_name="Luukkonen-Saikkonen-Terasvirta",
            detail=f"Test not computable: df_num={df_num}, df_den={df_den}",
        )

    return TestResult(
        statistic=f_stat,
        pvalue=p_value,
        test_name="Luukkonen-Saikkonen-Terasvirta",
        detail=f"F({df_num}, {df_den}) = {f_stat:.4f}, p = {p_value:.4f}",
    )


def linearity_test(
    y: NDArray[np.float64],
    order: int = 1,
    delay: int = 1,
) -> TestResult:
    """Luukkonen-Saikkonen-Terasvirta (1988) LM test for linearity vs STAR.

    Tests H0: AR(p) linear model vs H1: STAR model.

    Procedure:
    1. Estimate AR(p): y_t = x_t' phi + e_t
    2. Auxiliary regression of e_t on x_t and on the cross-products
       x_t * s_t^j, j = 1, 2, 3
    3. F-test that the added cross-products are jointly zero

    When d <= p the transition variable is one of the regressors, so terms
    such as ``1 * s_t`` duplicate an existing column; duplicated columns are
    dropped and the numerator degrees of freedom count only the columns that
    genuinely enter the design.

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
    return linearity_test_from_parts(y_dep, x_mat, s)


def transition_type_test(
    y: NDArray[np.float64],
    order: int = 1,
    delay: int = 1,
) -> dict[str, Any]:
    """Terasvirta (1994) test sequence for transition type: LSTAR vs ESTAR.

    After rejecting linearity, this sequence of nested F-tests on the
    auxiliary regression determines whether the transition function is
    logistic (LSTAR) or exponential (ESTAR):

    - F4: b3 = 0 given b1, b2 free
    - F3: b2 = 0 given b3 = 0
    - F2: b1 = 0 given b2 = b3 = 0

    Decision rule:
    - If p3 < min(p2, p4): ESTAR
    - Otherwise: LSTAR

    As in :func:`linearity_test`, columns duplicating regressors already in the
    design (which happens whenever d <= p) are dropped and the degrees of
    freedom count only the genuinely added columns.

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

    beta_ols = np.linalg.lstsq(x_mat, y_dep, rcond=None)[0]
    resid = y_dep - x_mat @ beta_ols
    rss_restricted = float(np.sum(resid**2))

    z1 = _star_terms(x_mat, s, 1)
    z2 = _star_terms(x_mat, s, 2)
    z3 = _star_terms(x_mat, s, 3)

    # H02: b1 = 0 given b2 = b3 = 0
    f2, p2, _, _ = _f_test(resid, x_mat, z1, rss_restricted)

    # H03: b2 = 0 given b3 = 0
    base3, _ = _augment(x_mat, z1)
    f3, p3, _, _ = _f_test(resid, base3, z2)

    # H04: b3 = 0 given b1, b2 free
    base4, _ = _augment(base3, z2)
    f4, p4, _, _ = _f_test(resid, base4, z3)

    if not (np.isfinite(p2) and np.isfinite(p3) and np.isfinite(p4)):
        recommended = "LSTAR"  # default when the sequence is not computable
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
    start: int | None = None,
) -> TestResult:
    """Tsay (1989) test for threshold nonlinearity.

    Tests H0: linear AR(p) vs H1: TAR, using the arranged autoregression.

    Procedure (Tsay 1989, Section 2):
    1. Sort the AR regression by the threshold variable s_t = y_{t-d}
       ("arranged autoregression").
    2. Run recursive least squares through the arranged data and collect the
       standardized one-step predictive residuals
       ``e_i = (y_i - x_i' b_{i-1}) / sqrt(1 + x_i' P_{i-1} x_i)``.
    3. Regress those predictive residuals on the corresponding regressors
       ``x_i`` and test that all coefficients are zero with an F-test. Under
       linearity the predictive residuals are orthogonal to the regressors;
       under a threshold alternative they are not.

    Parameters
    ----------
    y : ndarray
        Time series.
    order : int
        AR order p.
    delay : int
        Delay d.
    start : int, optional
        Number of arranged observations used to start the recursion.
        Default ``max(p + 2, floor(n / 10) + p + 1)`` as recommended by Tsay.

    Returns
    -------
    TestResult
        F-statistic and p-value.
    """
    y_dep, x_mat, s = _build_ar_matrices(y, order, delay)
    n_obs = len(y_dep)
    k = order + 1

    # Arranged autoregression: order the cases by the threshold variable.
    idx = np.argsort(s, kind="stable")
    y_arr = y_dep[idx]
    x_arr = x_mat[idx]

    m0 = start if start is not None else max(k + 1, int(n_obs // 10) + k)
    m0 = min(max(m0, k + 1), n_obs - k - 1)

    if m0 >= n_obs - k:
        return TestResult(
            statistic=float("nan"),
            pvalue=float("nan"),
            test_name="Tsay",
            detail=f"Insufficient observations for the arranged autoregression (n={n_obs})",
        )

    # Initialise the recursion on the first m0 arranged cases.
    x_init = x_arr[:m0]
    p_mat = np.linalg.pinv(x_init.T @ x_init)
    beta = p_mat @ (x_init.T @ y_arr[:m0])

    pred_resid = np.empty(n_obs - m0)
    for i in range(m0, n_obs):
        x_i = x_arr[i]
        px = p_mat @ x_i
        denom = 1.0 + float(x_i @ px)
        err = float(y_arr[i] - x_i @ beta)
        pred_resid[i - m0] = err / np.sqrt(denom)
        # Recursive least squares update.
        beta = beta + px * (err / denom)
        p_mat = p_mat - np.outer(px, px) / denom

    x_reg = x_arr[m0:]
    rss_restricted = float(np.sum(pred_resid**2))
    beta_reg = np.linalg.lstsq(x_reg, pred_resid, rcond=None)[0]
    rss_unrestricted = float(np.sum((pred_resid - x_reg @ beta_reg) ** 2))

    df_num = k
    df_den = n_obs - m0 - k
    if df_den <= 0 or rss_unrestricted <= 0.0:
        return TestResult(
            statistic=float("nan"),
            pvalue=float("nan"),
            test_name="Tsay",
            detail=f"Insufficient degrees of freedom: df_den={df_den}",
        )

    f_stat = ((rss_restricted - rss_unrestricted) / df_num) / (rss_unrestricted / df_den)
    p_value = float(stats.f.sf(f_stat, df_num, df_den))

    return TestResult(
        statistic=float(f_stat),
        pvalue=p_value,
        test_name="Tsay",
        detail=(
            f"F({df_num}, {df_den}) = {f_stat:.4f}, p = {p_value:.4f} "
            f"(arranged autoregression, startup m0={m0})"
        ),
    )


class _SupF:
    """sup-F statistic for a threshold in all AR coefficients.

    The design matrix and the threshold variable are fixed across bootstrap
    replications, so all quantities that depend only on them are precomputed
    once and each replication costs one pass of cumulative sums.
    """

    def __init__(
        self,
        x_mat: NDArray[np.float64],
        s: NDArray[np.float64],
        trim: float = 0.15,
        max_grid: int = 200,
    ) -> None:
        n_obs, k = x_mat.shape
        self.n_obs = n_obs
        self.k = k
        self.order = np.argsort(s, kind="stable")
        self.x_sorted = x_mat[self.order]

        lo = max(int(np.ceil(trim * n_obs)), k + 1)
        hi = min(int(np.floor((1.0 - trim) * n_obs)), n_obs - k - 1)
        cuts = np.arange(lo, hi + 1) if hi >= lo else np.array([n_obs // 2])
        if len(cuts) > max_grid:
            cuts = np.unique(np.linspace(cuts[0], cuts[-1], max_grid).astype(int))

        outer = self.x_sorted[:, :, None] * self.x_sorted[:, None, :]
        cum_xx = np.cumsum(outer, axis=0)
        self.xx_total = cum_xx[-1]
        xx_low = cum_xx[cuts - 1]
        xx_high = self.xx_total[None] - xx_low

        ok = np.array(
            [
                np.linalg.cond(xx_low[i]) < 1e10 and np.linalg.cond(xx_high[i]) < 1e10
                for i in range(len(cuts))
            ],
            dtype=bool,
        )
        self.cuts = cuts[ok]
        self.xx_low = xx_low[ok]
        self.xx_high = xx_high[ok]
        self.thresholds = np.sort(s)[self.cuts - 1] if len(self.cuts) else np.array([])

    @property
    def usable(self) -> bool:
        """Whether at least one threshold candidate survived the trimming."""
        return len(self.cuts) > 0

    def __call__(self, y: NDArray[np.float64]) -> tuple[float, float]:
        """Return (sup-F, argmax threshold) for the dependent variable y."""
        y_sorted = y[self.order]
        cum_xy = np.cumsum(self.x_sorted * y_sorted[:, None], axis=0)
        cum_yy = np.cumsum(y_sorted**2)

        xy_total = cum_xy[-1]
        yy_total = float(cum_yy[-1])
        rss0 = yy_total - float(xy_total @ np.linalg.solve(self.xx_total, xy_total))

        xy_low = cum_xy[self.cuts - 1]
        xy_high = xy_total[None] - xy_low
        yy_low = cum_yy[self.cuts - 1]
        yy_high = yy_total - yy_low

        sol_low = np.linalg.solve(self.xx_low, xy_low[:, :, None])[:, :, 0]
        sol_high = np.linalg.solve(self.xx_high, xy_high[:, :, None])[:, :, 0]
        rss1 = (yy_low - np.einsum("ij,ij->i", xy_low, sol_low)) + (
            yy_high - np.einsum("ij,ij->i", xy_high, sol_high)
        )
        rss1 = np.maximum(rss1, 1e-300)

        f_vals = (rss0 - rss1) / (rss1 / (self.n_obs - 2 * self.k))
        best = int(np.argmax(f_vals))
        return float(f_vals[best]), float(self.thresholds[best])


def hansen_threshold_test(
    y: NDArray[np.float64],
    order: int = 1,
    delay: int = 1,
    n_bootstrap: int = 1000,
    seed: int | None = None,
    trim: float = 0.15,
) -> TestResult:
    """Hansen (1996) bootstrap threshold test (sup-F).

    Tests H0: no threshold effect in the AR coefficients, i.e.

        y_t = x_t' phi + e_t

    against H1: y_t = x_t' phi_1 I(s_t <= c) + x_t' phi_2 I(s_t > c) + e_t
    where the threshold c is not identified under the null.

    Procedure:
    1. For each candidate threshold c in a trimmed grid, fit the two-regime
       model (a break in *all* AR coefficients, not only the intercept) and
       compute F(c) against the linear fit; the statistic is sup_c F(c).
    2. Wild bootstrap: for each replication draw Rademacher weights v_t,
       build y*_t = x_t' phi_hat + e_hat_t v_t, **re-fit the null linear
       regression** on the bootstrap sample and recompute sup-F on it.
    3. p-value = (1 + #{sup-F* >= sup-F}) / (1 + B).

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
    trim : float
        Fraction of the sample trimmed at each end of the threshold grid.

    Returns
    -------
    TestResult
        sup-F statistic and bootstrap p-value.
    """
    rng = np.random.default_rng(seed)
    y_dep, x_mat, s = _build_ar_matrices(y, order, delay)
    n_obs = len(y_dep)

    sup_f = _SupF(x_mat, s, trim=trim)
    if not sup_f.usable:
        return TestResult(
            statistic=float("nan"),
            pvalue=float("nan"),
            test_name="Hansen Bootstrap Threshold",
            detail=f"No admissible threshold candidates (n={n_obs}, trim={trim})",
        )

    beta_ols = np.linalg.lstsq(x_mat, y_dep, rcond=None)[0]
    fitted = x_mat @ beta_ols
    resid = y_dep - fitted

    stat_obs, c_hat = sup_f(y_dep)

    count_exceed = 0
    for _ in range(n_bootstrap):
        v = rng.choice([-1.0, 1.0], size=n_obs)
        # Bootstrap sample under H0; sup_f re-fits both the null regression
        # and every two-regime regression on it.
        y_boot = fitted + resid * v
        stat_b, _ = sup_f(y_boot)
        if stat_b >= stat_obs:
            count_exceed += 1

    p_value = (1.0 + count_exceed) / (1.0 + n_bootstrap)

    return TestResult(
        statistic=float(stat_obs),
        pvalue=float(p_value),
        test_name="Hansen Bootstrap Threshold",
        detail=(
            f"sup-F = {stat_obs:.4f} at c = {c_hat:.4f}, "
            f"bootstrap p = {p_value:.4f} ({n_bootstrap} reps)"
        ),
    )
