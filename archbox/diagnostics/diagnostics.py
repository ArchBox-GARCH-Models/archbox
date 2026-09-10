"""Full diagnostics suite for GARCH model results.

Runs all available diagnostic tests in a single call and produces
a formatted report.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from numpy.typing import NDArray
from scipy import stats

from archbox.diagnostics.arch_lm import TestResult, arch_lm_test
from archbox.diagnostics.ljung_box import LjungBoxResult, ljung_box_squared
from archbox.diagnostics.nyblom import MAX_NYBLOM_PARAMS, NyblomResult, nyblom_test
from archbox.diagnostics.sign_bias import MIN_SIGN_BIAS_OBS, SignBiasResult, sign_bias_test

#: Relative step used for the central finite differences of loglike_per_obs.
_SCORE_STEP = 1e-5


@dataclass
class DiagnosticReport:
    """Container for all diagnostic test results.

    Attributes
    ----------
    arch_lm : dict[int, TestResult]
        ARCH-LM test results keyed by lag count.
    sign_bias : SignBiasResult | None
        Sign Bias test result.
    ljung_box_sq : dict[int, LjungBoxResult]
        Ljung-Box on z^2 results keyed by lag count.
    nyblom : NyblomResult | None
        Nyblom stability test result.
    jarque_bera : tuple[float, float] | None
        (statistic, pvalue) from Jarque-Bera normality test.
    skipped : dict[str, str]
        Tests that were not applicable, mapped to the reason they were
        omitted. A test is never silently dropped: it either appears above
        with finite numbers, or here with an explanation.
    """

    arch_lm: dict[int, TestResult] = field(default_factory=dict)
    sign_bias: SignBiasResult | None = None
    ljung_box_sq: dict[int, LjungBoxResult] = field(default_factory=dict)
    nyblom: NyblomResult | None = None
    jarque_bera: tuple[float, float] | None = None
    skipped: dict[str, str] = field(default_factory=dict)

    def summary(self, significance: float = 0.05) -> str:
        """Generate formatted summary table of all diagnostic tests.

        Parameters
        ----------
        significance : float
            Significance level for PASS/FAIL decision. Default is 0.05.

        Returns
        -------
        str
            Formatted table.
        """
        lines = [
            "=" * 62,
            "Diagnostic Report",
            "=" * 62,
            f"{'Test':<25} {'Statistic':>10} {'p-value':>10} {'Decision':>10}",
            "-" * 62,
        ]

        # ARCH-LM tests
        for lag in sorted(self.arch_lm.keys()):
            result = self.arch_lm[lag]
            decision = "PASS" if result.pvalue > significance else "FAIL"
            lines.append(
                f"{'ARCH-LM (' + str(lag) + ')':<25} "
                f"{result.statistic:>10.4f} "
                f"{result.pvalue:>10.4f} "
                f"{decision:>10}"
            )

        # Sign Bias
        if self.sign_bias is not None:
            sb = self.sign_bias
            decision = "PASS" if sb.joint[1] > significance else "FAIL"
            lines.append(
                f"{'Sign Bias (joint)':<25} "
                f"{sb.joint[0]:>10.4f} "
                f"{sb.joint[1]:>10.4f} "
                f"{decision:>10}"
            )

        # Ljung-Box
        for lag in sorted(self.ljung_box_sq.keys()):
            result = self.ljung_box_sq[lag]
            decision = "PASS" if result.pvalue > significance else "FAIL"
            lines.append(
                f"{'Ljung-Box z^2 (' + str(lag) + ')':<25} "
                f"{result.statistic:>10.4f} "
                f"{result.pvalue:>10.4f} "
                f"{decision:>10}"
            )

        # Nyblom
        if self.nyblom is not None:
            ny = self.nyblom
            # Use 5% critical value
            cv5 = ny.critical_values_joint[1]
            decision = "PASS" if ny.joint_statistic <= cv5 else "FAIL"
            lines.append(
                f"{'Nyblom (joint)':<25} "
                f"{ny.joint_statistic:>10.4f} "
                f"{'cv5=' + f'{cv5:.3f}':>10} "
                f"{decision:>10}"
            )

        # Jarque-Bera
        if self.jarque_bera is not None:
            jb_stat, jb_pval = self.jarque_bera
            decision = "PASS" if jb_pval > significance else "FAIL"
            lines.append(f"{'Jarque-Bera':<25} {jb_stat:>10.4f} {jb_pval:>10.4f} {decision:>10}")

        lines.append("=" * 62)
        lines.append(f"PASS = do not reject H0 at {significance:.0%}")

        if self.skipped:
            lines.append("-" * 62)
            lines.append("Skipped:")
            for name in sorted(self.skipped):
                lines.append(f"  {name}: {self.skipped[name]}")
            lines.append("=" * 62)

        return "\n".join(lines)

    def __repr__(self) -> str:
        """Return diagnostic report summary."""
        return self.summary()


def _residual_series(results: object, attr: str) -> NDArray[np.float64]:
    """Fetch a residual series from a results object, or fail loudly."""
    value = getattr(results, attr, None)
    if value is None:
        msg = (
            f"{type(results).__name__} has no usable '{attr}' attribute; "
            "full_diagnostics needs the ArchResults API: 'resid' (raw residuals, "
            "same scale as the returns) and 'std_resid' (standardized residuals)"
        )
        raise TypeError(msg)
    array = np.asarray(value, dtype=np.float64).ravel()
    if array.size == 0:
        msg = f"'{attr}' is empty"
        raise ValueError(msg)
    if not np.all(np.isfinite(array)):
        msg = f"'{attr}' contains non-finite values"
        raise ValueError(msg)
    return array


def _numerical_scores(results: object) -> tuple[NDArray[np.float64] | None, str]:
    """Per-observation scores of the fitted model, by central differences.

    Returns
    -------
    tuple
        ``(scores, reason)``. ``scores`` is the (T x k) matrix of
        ``d loglike_t / d theta`` evaluated at the estimated parameters, or
        ``None`` when the model cannot provide them, in which case ``reason``
        explains why.

    Notes
    -----
    The scores are demeaned. At the MLE the first-order condition makes them
    sum to zero exactly; finite differences at a numerically converged optimum
    only satisfy that approximately, and the leftover drift would otherwise be
    read by the Nyblom statistic as parameter instability.
    """
    if getattr(results, "scores", None) is not None:
        supplied = np.asarray(results.scores, dtype=np.float64)  # type: ignore[attr-defined]
        if supplied.ndim == 1:
            supplied = supplied.reshape(-1, 1)
        return supplied - supplied.mean(axis=0, keepdims=True), ""

    model = getattr(results, "_model", None)
    if model is None:
        return None, "results has no fitted model (_model) to differentiate"

    loglike_per_obs = getattr(model, "loglike_per_obs", None)
    if not callable(loglike_per_obs):
        return None, f"{type(model).__name__} does not implement loglike_per_obs"

    raw_params = getattr(results, "params", None)
    if raw_params is None:
        return None, "results has no estimated params"
    params = np.asarray(raw_params, dtype=np.float64).ravel()
    n_params = params.size
    if n_params == 0:
        return None, "results has no estimated params"

    base = np.asarray(loglike_per_obs(params), dtype=np.float64).ravel()
    scores = np.empty((base.size, n_params), dtype=np.float64)
    for j in range(n_params):
        step = _SCORE_STEP * max(abs(float(params[j])), 1e-8)
        up = params.copy()
        up[j] += step
        down = params.copy()
        down[j] -= step
        ll_up = np.asarray(loglike_per_obs(up), dtype=np.float64).ravel()
        ll_down = np.asarray(loglike_per_obs(down), dtype=np.float64).ravel()
        scores[:, j] = (ll_up - ll_down) / (2.0 * step)

    if not np.all(np.isfinite(scores)):
        return None, "numerical scores of loglike_per_obs are not finite"

    return scores - scores.mean(axis=0, keepdims=True), ""


def _jarque_bera(series: NDArray[np.float64]) -> tuple[float, float]:
    """Jarque-Bera normality statistic and its chi2(2) p-value.

    Identical to ``scipy.stats.jarque_bera`` but returns plain floats and
    uses the survival function for the p-value.
    """
    centered = series - series.mean()
    variance = float(np.mean(centered**2))
    if variance < 1e-300:
        return 0.0, 1.0
    skew = float(np.mean(centered**3)) / variance**1.5
    kurt = float(np.mean(centered**4)) / variance**2
    n = series.size
    statistic = n / 6.0 * (skew**2 + (kurt - 3.0) ** 2 / 4.0)
    return float(statistic), float(stats.chi2.sf(statistic, df=2))


def _default_lags(base: list[int], lags: int) -> list[int]:
    """Sorted, de-duplicated lag list built from `lags`."""
    return sorted({value for value in [*base, lags] if value >= 1})


def full_diagnostics(
    results: object,
    lags: int = 10,
    arch_lm_lags: list[int] | None = None,
    lb_lags: list[int] | None = None,
) -> DiagnosticReport:
    """Run all diagnostic tests on fitted model results.

    Parameters
    ----------
    results : ArchResults
        Fitted model results. Must expose:

        - ``resid``: raw residuals (same scale as the returns)
        - ``std_resid``: standardized residuals z_t = eps_t / sigma_t

        Optionally, for the Nyblom stability test, either a ``scores``
        matrix or a ``_model`` implementing ``loglike_per_obs`` together
        with ``params`` (the scores are then obtained by central finite
        differences).
    lags : int
        Primary lag order. When `arch_lm_lags` / `lb_lags` are not given they
        default to ``[1, 5, lags]`` and ``[5, lags, 2 * lags]`` respectively.
        Default is 10.
    arch_lm_lags : list[int], optional
        Lag counts for the ARCH-LM test.
    lb_lags : list[int], optional
        Lag counts for the Ljung-Box test.

    Returns
    -------
    DiagnosticReport
        Report with all applicable diagnostic test results. Tests that cannot
        be run on this sample are listed in ``report.skipped`` with a reason;
        anything else that goes wrong propagates as an exception.

    Raises
    ------
    TypeError
        If `results` does not expose ``resid``/``std_resid``.
    ValueError
        If the residual series are empty, non-finite or of unequal length, or
        if `lags` is not positive.
    """
    if lags < 1:
        msg = f"lags must be >= 1, got {lags}"
        raise ValueError(msg)
    if arch_lm_lags is None:
        arch_lm_lags = _default_lags([1, 5], lags)
    if lb_lags is None:
        lb_lags = _default_lags([5, 2 * lags], lags)

    resid = _residual_series(results, "resid")
    std_resid = _residual_series(results, "std_resid")
    if resid.size != std_resid.size:
        msg = f"resid and std_resid must be the same length, got {resid.size} vs {std_resid.size}"
        raise ValueError(msg)
    nobs = std_resid.size

    report = DiagnosticReport()

    # 1. ARCH-LM tests on the standardized residuals.
    for q in arch_lm_lags:
        if q < 1 or q >= nobs - 1:
            report.skipped[f"ARCH-LM ({q})"] = f"needs 1 <= lags < T-1, T={nobs}"
            continue
        report.arch_lm[q] = arch_lm_test(std_resid, lags=q)

    # 2. Sign Bias test: z_t^2 on the sign/size of the lagged raw residual.
    if nobs < MIN_SIGN_BIAS_OBS:
        report.skipped["Sign Bias"] = f"needs at least {MIN_SIGN_BIAS_OBS} observations, T={nobs}"
    else:
        report.sign_bias = sign_bias_test(resid, std_resid)

    # 3. Ljung-Box on z^2.
    for m in lb_lags:
        if m < 1 or m >= nobs:
            report.skipped[f"Ljung-Box z^2 ({m})"] = f"needs 1 <= lags < T, T={nobs}"
            continue
        report.ljung_box_sq[m] = ljung_box_squared(std_resid, lags=m)

    # 4. Nyblom parameter stability test on the per-observation scores.
    scores, reason = _numerical_scores(results)
    if scores is None:
        report.skipped["Nyblom"] = reason
    elif scores.ndim != 2 or scores.shape[1] < 1:
        report.skipped["Nyblom"] = f"scores must be (T x k), got shape {scores.shape}"
    elif scores.shape[1] > MAX_NYBLOM_PARAMS:
        report.skipped["Nyblom"] = (
            f"no tabulated critical values for k={scores.shape[1]} parameters "
            f"(table stops at k={MAX_NYBLOM_PARAMS})"
        )
    elif scores.shape[0] <= scores.shape[1]:
        report.skipped["Nyblom"] = f"needs T > k, got T={scores.shape[0]} and k={scores.shape[1]}"
    else:
        report.nyblom = nyblom_test(scores)

    # 5. Jarque-Bera normality test on the standardized residuals.
    report.jarque_bera = _jarque_bera(std_resid)

    return report


__all__ = ["DiagnosticReport", "full_diagnostics"]
