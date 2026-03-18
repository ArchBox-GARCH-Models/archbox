"""Full diagnostics suite for GARCH model results.

Runs all available diagnostic tests in a single call and produces
a formatted report.
"""

from __future__ import annotations

import contextlib
from dataclasses import dataclass, field

import numpy as np
from scipy import stats

from archbox.diagnostics.arch_lm import TestResult, arch_lm_test
from archbox.diagnostics.ljung_box import LjungBoxResult, ljung_box_squared
from archbox.diagnostics.nyblom import NyblomResult, nyblom_test
from archbox.diagnostics.sign_bias import SignBiasResult, sign_bias_test


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
    """

    arch_lm: dict[int, TestResult] = field(default_factory=dict)
    sign_bias: SignBiasResult | None = None
    ljung_box_sq: dict[int, LjungBoxResult] = field(default_factory=dict)
    nyblom: NyblomResult | None = None
    jarque_bera: tuple[float, float] | None = None

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

        return "\n".join(lines)

    def __repr__(self) -> str:
        """Return diagnostic report summary."""
        return self.summary()


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
        Fitted model results. Must have attributes:
        - resids (or endog): raw residuals
        - conditional_volatility: sigma_t series
        Optionally:
        - scores: score matrix for Nyblom test
    lags : int
        Default number of lags. Default is 10.
    arch_lm_lags : list[int], optional
        Lag counts for ARCH-LM test. Default is [1, 5, 10].
    lb_lags : list[int], optional
        Lag counts for Ljung-Box test. Default is [5, 10, 20].

    Returns
    -------
    DiagnosticReport
        Report with all diagnostic test results.
    """
    if arch_lm_lags is None:
        arch_lm_lags = [1, 5, 10]
    if lb_lags is None:
        lb_lags = [5, 10, 20]

    # Extract residuals and volatility
    resids = np.asarray(
        getattr(results, "resids", getattr(results, "endog", None)),
        dtype=np.float64,
    )
    sigma = np.asarray(
        getattr(results, "conditional_volatility", None),
        dtype=np.float64,
    )
    sigma_safe = np.maximum(sigma, 1e-12)
    std_resids = resids / sigma_safe

    report = DiagnosticReport()

    # 1. ARCH-LM tests
    for q in arch_lm_lags:
        with contextlib.suppress(Exception):
            report.arch_lm[q] = arch_lm_test(std_resids, lags=q)

    # 2. Sign Bias test
    with contextlib.suppress(Exception):
        report.sign_bias = sign_bias_test(resids, std_resids)

    # 3. Ljung-Box on z^2
    for m in lb_lags:
        with contextlib.suppress(Exception):
            report.ljung_box_sq[m] = ljung_box_squared(std_resids, lags=m)

    # 4. Nyblom stability test (if scores available)
    scores = getattr(results, "scores", None)
    if scores is not None:
        try:
            scores_arr = np.asarray(scores, dtype=np.float64)
            report.nyblom = nyblom_test(scores_arr)
        except Exception:
            pass

    # 5. Jarque-Bera normality test
    try:
        jb_result = stats.jarque_bera(std_resids)
        report.jarque_bera = (
            float(jb_result[0]),  # type: ignore[arg-type]
            float(jb_result[1]),  # type: ignore[arg-type]
        )
    except Exception:
        pass

    return report
