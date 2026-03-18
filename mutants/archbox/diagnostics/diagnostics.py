"""Full diagnostics suite for GARCH model results.

Runs all available diagnostic tests in a single call and produces
a formatted report.
"""

from __future__ import annotations

import contextlib
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Annotated, ClassVar

import numpy as np
from scipy import stats

from archbox.diagnostics.arch_lm import TestResult, arch_lm_test
from archbox.diagnostics.ljung_box import LjungBoxResult, ljung_box_squared
from archbox.diagnostics.nyblom import NyblomResult, nyblom_test
from archbox.diagnostics.sign_bias import SignBiasResult, sign_bias_test

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
    args = [results, lags, arch_lm_lags, lb_lags]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_full_diagnostics__mutmut_orig, x_full_diagnostics__mutmut_mutants, args, kwargs, None
    )


def x_full_diagnostics__mutmut_orig(
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


def x_full_diagnostics__mutmut_1(
    results: object,
    lags: int = 11,
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


def x_full_diagnostics__mutmut_2(
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
    if arch_lm_lags is not None:
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


def x_full_diagnostics__mutmut_3(
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
        arch_lm_lags = None
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


def x_full_diagnostics__mutmut_4(
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
        arch_lm_lags = [2, 5, 10]
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


def x_full_diagnostics__mutmut_5(
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
        arch_lm_lags = [1, 6, 10]
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


def x_full_diagnostics__mutmut_6(
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
        arch_lm_lags = [1, 5, 11]
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


def x_full_diagnostics__mutmut_7(
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
    if lb_lags is not None:
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


def x_full_diagnostics__mutmut_8(
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
        lb_lags = None

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


def x_full_diagnostics__mutmut_9(
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
        lb_lags = [6, 10, 20]

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


def x_full_diagnostics__mutmut_10(
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
        lb_lags = [5, 11, 20]

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


def x_full_diagnostics__mutmut_11(
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
        lb_lags = [5, 10, 21]

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


def x_full_diagnostics__mutmut_12(
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
    resids = None
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


def x_full_diagnostics__mutmut_13(
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
        None,
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


def x_full_diagnostics__mutmut_14(
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
        dtype=None,
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


def x_full_diagnostics__mutmut_15(
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


def x_full_diagnostics__mutmut_16(
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


def x_full_diagnostics__mutmut_17(
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
        getattr(None, "resids", getattr(results, "endog", None)),
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


def x_full_diagnostics__mutmut_18(
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
        getattr(results, None, getattr(results, "endog", None)),
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


def x_full_diagnostics__mutmut_19(
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
        getattr(results, "resids", None),
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


def x_full_diagnostics__mutmut_20(
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
        getattr("resids", getattr(results, "endog", None)),
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


def x_full_diagnostics__mutmut_21(
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
        getattr(results, getattr(results, "endog", None)),
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


def x_full_diagnostics__mutmut_22(
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
        results.resids,
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


def x_full_diagnostics__mutmut_23(
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
        getattr(results, "XXresidsXX", getattr(results, "endog", None)),
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


def x_full_diagnostics__mutmut_24(
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
        getattr(results, "RESIDS", getattr(results, "endog", None)),
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


def x_full_diagnostics__mutmut_25(
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
        getattr(results, "resids", getattr(None, "endog", None)),
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


def x_full_diagnostics__mutmut_26(
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
        getattr(results, "resids", getattr(results, None, None)),
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


def x_full_diagnostics__mutmut_27(
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
        getattr(results, "resids", getattr("endog", None)),
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


def x_full_diagnostics__mutmut_28(
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
        getattr(results, "resids", getattr(results, None)),
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


def x_full_diagnostics__mutmut_29(
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
        getattr(results, "resids", results.endog),
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


def x_full_diagnostics__mutmut_30(
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
        getattr(results, "resids", getattr(results, "XXendogXX", None)),
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


def x_full_diagnostics__mutmut_31(
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
        getattr(results, "resids", getattr(results, "ENDOG", None)),
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


def x_full_diagnostics__mutmut_32(
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
    sigma = None
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


def x_full_diagnostics__mutmut_33(
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
        None,
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


def x_full_diagnostics__mutmut_34(
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
        dtype=None,
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


def x_full_diagnostics__mutmut_35(
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


def x_full_diagnostics__mutmut_36(
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


def x_full_diagnostics__mutmut_37(
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
        getattr(None, "conditional_volatility", None),
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


def x_full_diagnostics__mutmut_38(
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
        getattr(results, None, None),
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


def x_full_diagnostics__mutmut_39(
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
        getattr("conditional_volatility", None),
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


def x_full_diagnostics__mutmut_40(
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
        getattr(results, None),
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


def x_full_diagnostics__mutmut_41(
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
        results.conditional_volatility,
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


def x_full_diagnostics__mutmut_42(
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
        getattr(results, "XXconditional_volatilityXX", None),
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


def x_full_diagnostics__mutmut_43(
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
        getattr(results, "CONDITIONAL_VOLATILITY", None),
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


def x_full_diagnostics__mutmut_44(
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
    sigma_safe = None
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


def x_full_diagnostics__mutmut_45(
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
    sigma_safe = np.maximum(None, 1e-12)
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


def x_full_diagnostics__mutmut_46(
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
    sigma_safe = np.maximum(sigma, None)
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


def x_full_diagnostics__mutmut_47(
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
    sigma_safe = np.maximum(1e-12)
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


def x_full_diagnostics__mutmut_48(
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
    sigma_safe = np.maximum(
        sigma,
    )
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


def x_full_diagnostics__mutmut_49(
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
    sigma_safe = np.maximum(sigma, 1.000000000001)
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


def x_full_diagnostics__mutmut_50(
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
    std_resids = None

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


def x_full_diagnostics__mutmut_51(
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
    std_resids = resids * sigma_safe

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


def x_full_diagnostics__mutmut_52(
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

    report = None

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


def x_full_diagnostics__mutmut_53(
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
        with contextlib.suppress(None):
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


def x_full_diagnostics__mutmut_54(
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
            report.arch_lm[q] = None

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


def x_full_diagnostics__mutmut_55(
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
            report.arch_lm[q] = arch_lm_test(None, lags=q)

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


def x_full_diagnostics__mutmut_56(
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
            report.arch_lm[q] = arch_lm_test(std_resids, lags=None)

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


def x_full_diagnostics__mutmut_57(
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
            report.arch_lm[q] = arch_lm_test(lags=q)

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


def x_full_diagnostics__mutmut_58(
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
            report.arch_lm[q] = arch_lm_test(
                std_resids,
            )

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


def x_full_diagnostics__mutmut_59(
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
    with contextlib.suppress(None):
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


def x_full_diagnostics__mutmut_60(
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
        report.sign_bias = None

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


def x_full_diagnostics__mutmut_61(
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
        report.sign_bias = sign_bias_test(None, std_resids)

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


def x_full_diagnostics__mutmut_62(
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
        report.sign_bias = sign_bias_test(resids, None)

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


def x_full_diagnostics__mutmut_63(
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
        report.sign_bias = sign_bias_test(std_resids)

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


def x_full_diagnostics__mutmut_64(
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
        report.sign_bias = sign_bias_test(
            resids,
        )

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


def x_full_diagnostics__mutmut_65(
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
        with contextlib.suppress(None):
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


def x_full_diagnostics__mutmut_66(
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
            report.ljung_box_sq[m] = None

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


def x_full_diagnostics__mutmut_67(
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
            report.ljung_box_sq[m] = ljung_box_squared(None, lags=m)

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


def x_full_diagnostics__mutmut_68(
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
            report.ljung_box_sq[m] = ljung_box_squared(std_resids, lags=None)

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


def x_full_diagnostics__mutmut_69(
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
            report.ljung_box_sq[m] = ljung_box_squared(lags=m)

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


def x_full_diagnostics__mutmut_70(
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
            report.ljung_box_sq[m] = ljung_box_squared(
                std_resids,
            )

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


def x_full_diagnostics__mutmut_71(
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
    scores = None
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


def x_full_diagnostics__mutmut_72(
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
    scores = getattr(None, "scores", None)
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


def x_full_diagnostics__mutmut_73(
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
    scores = getattr(results, None, None)
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


def x_full_diagnostics__mutmut_74(
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
    scores = getattr("scores", None)
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


def x_full_diagnostics__mutmut_75(
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
    scores = getattr(results, None)
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


def x_full_diagnostics__mutmut_76(
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
    scores = results.scores
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


def x_full_diagnostics__mutmut_77(
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
    scores = getattr(results, "XXscoresXX", None)
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


def x_full_diagnostics__mutmut_78(
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
    scores = getattr(results, "SCORES", None)
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


def x_full_diagnostics__mutmut_79(
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
    if scores is None:
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


def x_full_diagnostics__mutmut_80(
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
            scores_arr = None
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


def x_full_diagnostics__mutmut_81(
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
            scores_arr = np.asarray(None, dtype=np.float64)
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


def x_full_diagnostics__mutmut_82(
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
            scores_arr = np.asarray(scores, dtype=None)
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


def x_full_diagnostics__mutmut_83(
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
            scores_arr = np.asarray(dtype=np.float64)
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


def x_full_diagnostics__mutmut_84(
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
            scores_arr = np.asarray(
                scores,
            )
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


def x_full_diagnostics__mutmut_85(
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
            report.nyblom = None
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


def x_full_diagnostics__mutmut_86(
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
            report.nyblom = nyblom_test(None)
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


def x_full_diagnostics__mutmut_87(
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
        jb_result = None
        report.jarque_bera = (
            float(jb_result[0]),  # type: ignore[arg-type]
            float(jb_result[1]),  # type: ignore[arg-type]
        )
    except Exception:
        pass

    return report


def x_full_diagnostics__mutmut_88(
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
        jb_result = stats.jarque_bera(None)
        report.jarque_bera = (
            float(jb_result[0]),  # type: ignore[arg-type]
            float(jb_result[1]),  # type: ignore[arg-type]
        )
    except Exception:
        pass

    return report


def x_full_diagnostics__mutmut_89(
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
        report.jarque_bera = None
    except Exception:
        pass

    return report


def x_full_diagnostics__mutmut_90(
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
            float(None),  # type: ignore[arg-type]
            float(jb_result[1]),  # type: ignore[arg-type]
        )
    except Exception:
        pass

    return report


def x_full_diagnostics__mutmut_91(
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
            float(jb_result[1]),  # type: ignore[arg-type]
            float(jb_result[1]),  # type: ignore[arg-type]
        )
    except Exception:
        pass

    return report


def x_full_diagnostics__mutmut_92(
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
            float(None),  # type: ignore[arg-type]
        )
    except Exception:
        pass

    return report


def x_full_diagnostics__mutmut_93(
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
            float(jb_result[2]),  # type: ignore[arg-type]
        )
    except Exception:
        pass

    return report


x_full_diagnostics__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_full_diagnostics__mutmut_1": x_full_diagnostics__mutmut_1,
    "x_full_diagnostics__mutmut_2": x_full_diagnostics__mutmut_2,
    "x_full_diagnostics__mutmut_3": x_full_diagnostics__mutmut_3,
    "x_full_diagnostics__mutmut_4": x_full_diagnostics__mutmut_4,
    "x_full_diagnostics__mutmut_5": x_full_diagnostics__mutmut_5,
    "x_full_diagnostics__mutmut_6": x_full_diagnostics__mutmut_6,
    "x_full_diagnostics__mutmut_7": x_full_diagnostics__mutmut_7,
    "x_full_diagnostics__mutmut_8": x_full_diagnostics__mutmut_8,
    "x_full_diagnostics__mutmut_9": x_full_diagnostics__mutmut_9,
    "x_full_diagnostics__mutmut_10": x_full_diagnostics__mutmut_10,
    "x_full_diagnostics__mutmut_11": x_full_diagnostics__mutmut_11,
    "x_full_diagnostics__mutmut_12": x_full_diagnostics__mutmut_12,
    "x_full_diagnostics__mutmut_13": x_full_diagnostics__mutmut_13,
    "x_full_diagnostics__mutmut_14": x_full_diagnostics__mutmut_14,
    "x_full_diagnostics__mutmut_15": x_full_diagnostics__mutmut_15,
    "x_full_diagnostics__mutmut_16": x_full_diagnostics__mutmut_16,
    "x_full_diagnostics__mutmut_17": x_full_diagnostics__mutmut_17,
    "x_full_diagnostics__mutmut_18": x_full_diagnostics__mutmut_18,
    "x_full_diagnostics__mutmut_19": x_full_diagnostics__mutmut_19,
    "x_full_diagnostics__mutmut_20": x_full_diagnostics__mutmut_20,
    "x_full_diagnostics__mutmut_21": x_full_diagnostics__mutmut_21,
    "x_full_diagnostics__mutmut_22": x_full_diagnostics__mutmut_22,
    "x_full_diagnostics__mutmut_23": x_full_diagnostics__mutmut_23,
    "x_full_diagnostics__mutmut_24": x_full_diagnostics__mutmut_24,
    "x_full_diagnostics__mutmut_25": x_full_diagnostics__mutmut_25,
    "x_full_diagnostics__mutmut_26": x_full_diagnostics__mutmut_26,
    "x_full_diagnostics__mutmut_27": x_full_diagnostics__mutmut_27,
    "x_full_diagnostics__mutmut_28": x_full_diagnostics__mutmut_28,
    "x_full_diagnostics__mutmut_29": x_full_diagnostics__mutmut_29,
    "x_full_diagnostics__mutmut_30": x_full_diagnostics__mutmut_30,
    "x_full_diagnostics__mutmut_31": x_full_diagnostics__mutmut_31,
    "x_full_diagnostics__mutmut_32": x_full_diagnostics__mutmut_32,
    "x_full_diagnostics__mutmut_33": x_full_diagnostics__mutmut_33,
    "x_full_diagnostics__mutmut_34": x_full_diagnostics__mutmut_34,
    "x_full_diagnostics__mutmut_35": x_full_diagnostics__mutmut_35,
    "x_full_diagnostics__mutmut_36": x_full_diagnostics__mutmut_36,
    "x_full_diagnostics__mutmut_37": x_full_diagnostics__mutmut_37,
    "x_full_diagnostics__mutmut_38": x_full_diagnostics__mutmut_38,
    "x_full_diagnostics__mutmut_39": x_full_diagnostics__mutmut_39,
    "x_full_diagnostics__mutmut_40": x_full_diagnostics__mutmut_40,
    "x_full_diagnostics__mutmut_41": x_full_diagnostics__mutmut_41,
    "x_full_diagnostics__mutmut_42": x_full_diagnostics__mutmut_42,
    "x_full_diagnostics__mutmut_43": x_full_diagnostics__mutmut_43,
    "x_full_diagnostics__mutmut_44": x_full_diagnostics__mutmut_44,
    "x_full_diagnostics__mutmut_45": x_full_diagnostics__mutmut_45,
    "x_full_diagnostics__mutmut_46": x_full_diagnostics__mutmut_46,
    "x_full_diagnostics__mutmut_47": x_full_diagnostics__mutmut_47,
    "x_full_diagnostics__mutmut_48": x_full_diagnostics__mutmut_48,
    "x_full_diagnostics__mutmut_49": x_full_diagnostics__mutmut_49,
    "x_full_diagnostics__mutmut_50": x_full_diagnostics__mutmut_50,
    "x_full_diagnostics__mutmut_51": x_full_diagnostics__mutmut_51,
    "x_full_diagnostics__mutmut_52": x_full_diagnostics__mutmut_52,
    "x_full_diagnostics__mutmut_53": x_full_diagnostics__mutmut_53,
    "x_full_diagnostics__mutmut_54": x_full_diagnostics__mutmut_54,
    "x_full_diagnostics__mutmut_55": x_full_diagnostics__mutmut_55,
    "x_full_diagnostics__mutmut_56": x_full_diagnostics__mutmut_56,
    "x_full_diagnostics__mutmut_57": x_full_diagnostics__mutmut_57,
    "x_full_diagnostics__mutmut_58": x_full_diagnostics__mutmut_58,
    "x_full_diagnostics__mutmut_59": x_full_diagnostics__mutmut_59,
    "x_full_diagnostics__mutmut_60": x_full_diagnostics__mutmut_60,
    "x_full_diagnostics__mutmut_61": x_full_diagnostics__mutmut_61,
    "x_full_diagnostics__mutmut_62": x_full_diagnostics__mutmut_62,
    "x_full_diagnostics__mutmut_63": x_full_diagnostics__mutmut_63,
    "x_full_diagnostics__mutmut_64": x_full_diagnostics__mutmut_64,
    "x_full_diagnostics__mutmut_65": x_full_diagnostics__mutmut_65,
    "x_full_diagnostics__mutmut_66": x_full_diagnostics__mutmut_66,
    "x_full_diagnostics__mutmut_67": x_full_diagnostics__mutmut_67,
    "x_full_diagnostics__mutmut_68": x_full_diagnostics__mutmut_68,
    "x_full_diagnostics__mutmut_69": x_full_diagnostics__mutmut_69,
    "x_full_diagnostics__mutmut_70": x_full_diagnostics__mutmut_70,
    "x_full_diagnostics__mutmut_71": x_full_diagnostics__mutmut_71,
    "x_full_diagnostics__mutmut_72": x_full_diagnostics__mutmut_72,
    "x_full_diagnostics__mutmut_73": x_full_diagnostics__mutmut_73,
    "x_full_diagnostics__mutmut_74": x_full_diagnostics__mutmut_74,
    "x_full_diagnostics__mutmut_75": x_full_diagnostics__mutmut_75,
    "x_full_diagnostics__mutmut_76": x_full_diagnostics__mutmut_76,
    "x_full_diagnostics__mutmut_77": x_full_diagnostics__mutmut_77,
    "x_full_diagnostics__mutmut_78": x_full_diagnostics__mutmut_78,
    "x_full_diagnostics__mutmut_79": x_full_diagnostics__mutmut_79,
    "x_full_diagnostics__mutmut_80": x_full_diagnostics__mutmut_80,
    "x_full_diagnostics__mutmut_81": x_full_diagnostics__mutmut_81,
    "x_full_diagnostics__mutmut_82": x_full_diagnostics__mutmut_82,
    "x_full_diagnostics__mutmut_83": x_full_diagnostics__mutmut_83,
    "x_full_diagnostics__mutmut_84": x_full_diagnostics__mutmut_84,
    "x_full_diagnostics__mutmut_85": x_full_diagnostics__mutmut_85,
    "x_full_diagnostics__mutmut_86": x_full_diagnostics__mutmut_86,
    "x_full_diagnostics__mutmut_87": x_full_diagnostics__mutmut_87,
    "x_full_diagnostics__mutmut_88": x_full_diagnostics__mutmut_88,
    "x_full_diagnostics__mutmut_89": x_full_diagnostics__mutmut_89,
    "x_full_diagnostics__mutmut_90": x_full_diagnostics__mutmut_90,
    "x_full_diagnostics__mutmut_91": x_full_diagnostics__mutmut_91,
    "x_full_diagnostics__mutmut_92": x_full_diagnostics__mutmut_92,
    "x_full_diagnostics__mutmut_93": x_full_diagnostics__mutmut_93,
}
x_full_diagnostics__mutmut_orig.__name__ = "x_full_diagnostics"
