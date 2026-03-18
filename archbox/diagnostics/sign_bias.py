"""Sign Bias Test (Engle & Ng, 1993).

Tests whether positive and negative shocks have different impacts
on conditional volatility.

References
----------
- Engle, R.F. & Ng, V.K. (1993). Measuring and Testing the Impact
  of News on Volatility. Journal of Finance, 48(5), 1749-1778.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import stats


@dataclass
class SignBiasResult:
    """Container for Sign Bias test results.

    Attributes
    ----------
    sign_bias : tuple[float, float]
        (t-statistic, p-value) for the sign bias test.
    neg_sign_bias : tuple[float, float]
        (t-statistic, p-value) for the negative size bias test.
    pos_sign_bias : tuple[float, float]
        (t-statistic, p-value) for the positive size bias test.
    joint : tuple[float, float]
        (F-statistic, p-value) for the joint test.
    """

    sign_bias: tuple[float, float]
    neg_sign_bias: tuple[float, float]
    pos_sign_bias: tuple[float, float]
    joint: tuple[float, float]

    def __repr__(self) -> str:
        """Return string representation of the sign bias test results."""
        lines = [
            "Sign Bias Test (Engle & Ng, 1993)",
            f"  Sign Bias:     t={self.sign_bias[0]:.4f}, p={self.sign_bias[1]:.4f}",
            f"  Neg Size Bias: t={self.neg_sign_bias[0]:.4f}, p={self.neg_sign_bias[1]:.4f}",
            f"  Pos Size Bias: t={self.pos_sign_bias[0]:.4f}, p={self.pos_sign_bias[1]:.4f}",
            f"  Joint Test:    F={self.joint[0]:.4f}, p={self.joint[1]:.4f}",
        ]
        return "\n".join(lines)


def sign_bias_test(resids: object, std_resids: object) -> SignBiasResult:
    """Sign Bias test for asymmetric volatility effects (Engle & Ng, 1993).

    Parameters
    ----------
    resids : array-like
        Raw residuals eps_t from the mean equation.
    std_resids : array-like
        Standardized residuals z_t = eps_t / sigma_t from the GARCH model.

    Returns
    -------
    SignBiasResult
        Results with sign_bias, neg_sign_bias, pos_sign_bias, and joint test.

    Notes
    -----
    Regression:
        z^2_t = c_0 + c_1*S^-_{t-1} + c_2*S^-_{t-1}*eps_{t-1}
                + c_3*S^+_{t-1}*eps_{t-1} + u_t

    Where:
        S^-_{t-1} = 1 if eps_{t-1} < 0, 0 otherwise
        S^+_{t-1} = 1 if eps_{t-1} >= 0, 0 otherwise
    """
    eps = np.asarray(resids, dtype=np.float64).ravel()
    z = np.asarray(std_resids, dtype=np.float64).ravel()

    if len(eps) != len(z):
        msg = f"resids and std_resids must have same length, got {len(eps)} and {len(z)}"
        raise ValueError(msg)

    # Dependent variable: z^2_t for t = 1, ..., T-1
    z2 = z[1:] ** 2
    n = len(z2)

    # Lagged values
    eps_lag = eps[:-1]
    s_neg = (eps_lag < 0).astype(np.float64)
    s_pos = (eps_lag >= 0).astype(np.float64)

    # Build regression matrix: [intercept, S^-, S^-*eps, S^+*eps]
    x_reg = np.column_stack(
        [
            np.ones(n),
            s_neg,
            s_neg * eps_lag,
            s_pos * eps_lag,
        ]
    )

    # OLS regression
    beta = np.linalg.lstsq(x_reg, z2, rcond=None)[0]
    residuals = z2 - x_reg @ beta

    # Variance-covariance matrix of OLS estimates
    sigma2_hat = np.sum(residuals**2) / (n - 4)
    xtx_inv = np.linalg.inv(x_reg.T @ x_reg)
    var_beta = sigma2_hat * xtx_inv

    # t-statistics for individual tests
    se = np.sqrt(np.diag(var_beta))
    t_stats = beta / se

    # Individual p-values (two-sided t-test)
    sign_bias_t = float(t_stats[1])
    sign_bias_p = float(2 * (1 - stats.t.cdf(abs(t_stats[1]), df=n - 4)))

    neg_sign_t = float(t_stats[2])
    neg_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[2]), df=n - 4)))

    pos_sign_t = float(t_stats[3])
    pos_sign_p = float(2 * (1 - stats.t.cdf(abs(t_stats[3]), df=n - 4)))

    # Joint F-test: H0: c_1 = c_2 = c_3 = 0
    r_mat = np.array(
        [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    rb = r_mat @ beta
    middle = r_mat @ xtx_inv @ r_mat.T
    f_stat = float((rb @ np.linalg.inv(middle) @ rb) / (3 * sigma2_hat))
    f_pvalue = float(1 - stats.f.cdf(f_stat, dfn=3, dfd=n - 4))

    return SignBiasResult(
        sign_bias=(sign_bias_t, sign_bias_p),
        neg_sign_bias=(neg_sign_t, neg_sign_p),
        pos_sign_bias=(pos_sign_t, pos_sign_p),
        joint=(f_stat, f_pvalue),
    )
