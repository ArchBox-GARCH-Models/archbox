"""Tests for full_diagnostics() and DiagnosticReport."""

from __future__ import annotations

import numpy as np
import pytest

from archbox.diagnostics.diagnostics import DiagnosticReport, full_diagnostics


class MockResults:
    """Mock ArchResults for testing full_diagnostics."""

    def __init__(
        self,
        returns: np.ndarray,
        sigma: np.ndarray,
        scores: np.ndarray | None = None,
    ):
        self.resids = returns
        self.endog = returns
        self.conditional_volatility = sigma
        self.mu = 0.0
        self.scores = scores


@pytest.fixture
def mock_garch_results(rng: np.random.Generator) -> MockResults:
    """Create mock GARCH results with realistic data."""
    n = 2000
    omega, alpha, beta = 1e-6, 0.08, 0.91

    sigma2 = np.empty(n)
    returns = np.empty(n)
    sigma2[0] = omega / (1 - alpha - beta)

    for t in range(n):
        if t > 0:
            sigma2[t] = omega + alpha * returns[t - 1] ** 2 + beta * sigma2[t - 1]
        z = rng.standard_normal()
        returns[t] = np.sqrt(sigma2[t]) * z

    sigma = np.sqrt(sigma2)

    # Generate mock scores (3 parameters)
    scores = rng.standard_normal((n, 3))

    return MockResults(returns, sigma, scores)


class TestFullDiagnosticsRuns:
    """test_full_diagnostics_runs: full_diagnostics runs without error."""

    def test_full_diagnostics_runs(self, mock_garch_results: MockResults) -> None:
        report = full_diagnostics(mock_garch_results)

        assert isinstance(report, DiagnosticReport)

    def test_full_diagnostics_with_scores(self, mock_garch_results: MockResults) -> None:
        report = full_diagnostics(mock_garch_results)

        # With scores, Nyblom should be present
        assert report.nyblom is not None

    def test_full_diagnostics_without_scores(self, rng: np.random.Generator) -> None:
        n = 1000
        returns = rng.standard_normal(n) * 0.01
        sigma = np.full(n, 0.01)
        mock = MockResults(returns, sigma, scores=None)

        report = full_diagnostics(mock)

        # Without scores, Nyblom should be None
        assert report.nyblom is None


class TestFullDiagnosticsContainsAllTests:
    """test_contains_all_results: report contains all test results."""

    def test_contains_all_results(self, mock_garch_results: MockResults) -> None:
        report = full_diagnostics(mock_garch_results)

        # ARCH-LM at lags 1, 5, 10
        assert 1 in report.arch_lm
        assert 5 in report.arch_lm
        assert 10 in report.arch_lm

        # Sign Bias
        assert report.sign_bias is not None

        # Ljung-Box at lags 5, 10, 20
        assert 5 in report.ljung_box_sq
        assert 10 in report.ljung_box_sq
        assert 20 in report.ljung_box_sq

        # Jarque-Bera
        assert report.jarque_bera is not None
        assert len(report.jarque_bera) == 2


class TestDiagnosticReportSummary:
    """Test summary() method of DiagnosticReport."""

    def test_summary_output(self, mock_garch_results: MockResults) -> None:
        report = full_diagnostics(mock_garch_results)
        summary = report.summary()

        assert "Diagnostic Report" in summary
        assert "ARCH-LM" in summary
        assert "Sign Bias" in summary
        assert "Ljung-Box" in summary
        assert "Jarque-Bera" in summary
        assert "PASS" in summary or "FAIL" in summary

    def test_summary_significance(self, mock_garch_results: MockResults) -> None:
        report = full_diagnostics(mock_garch_results)

        # Different significance levels
        summary_005 = report.summary(significance=0.05)
        summary_001 = report.summary(significance=0.01)

        assert "5%" in summary_005
        assert "1%" in summary_001

    def test_repr(self, mock_garch_results: MockResults) -> None:
        report = full_diagnostics(mock_garch_results)
        text = repr(report)
        assert "Diagnostic Report" in text


class TestFullDiagnosticsCustomLags:
    """Test custom lag configurations."""

    def test_custom_arch_lm_lags(self, mock_garch_results: MockResults) -> None:
        report = full_diagnostics(mock_garch_results, arch_lm_lags=[2, 7])

        assert 2 in report.arch_lm
        assert 7 in report.arch_lm
        assert 1 not in report.arch_lm

    def test_custom_lb_lags(self, mock_garch_results: MockResults) -> None:
        report = full_diagnostics(mock_garch_results, lb_lags=[3, 15])

        assert 3 in report.ljung_box_sq
        assert 15 in report.ljung_box_sq
        assert 5 not in report.ljung_box_sq


class TestIntegrationEndToEnd:
    """Full integration test: data -> GARCH -> VaR -> backtest -> diagnostics."""

    def test_full_pipeline(self, rng: np.random.Generator) -> None:
        # Step 1: Generate data
        n = 2000
        omega, alpha, beta = 1e-6, 0.08, 0.91

        sigma2 = np.empty(n)
        returns = np.empty(n)
        sigma2[0] = omega / (1 - alpha - beta)

        for t in range(n):
            if t > 0:
                sigma2[t] = omega + alpha * returns[t - 1] ** 2 + beta * sigma2[t - 1]
            z = rng.standard_normal()
            returns[t] = np.sqrt(sigma2[t]) * z

        sigma = np.sqrt(sigma2)

        # Step 2: Mock "GARCH fit" results
        mock_results = MockResults(returns, sigma, scores=rng.standard_normal((n, 3)))
        mock_results.params = np.array([omega, alpha, beta])
        mock_results.p = 1
        mock_results.q = 1

        # Step 3: VaR
        from archbox.risk.var import ValueAtRisk

        var = ValueAtRisk(mock_results, alpha=0.05)
        var_series = var.parametric(dist="normal")
        assert len(var_series) == n
        assert np.all(np.isfinite(var_series))

        # Step 4: ES
        from archbox.risk.es import ExpectedShortfall

        es = ExpectedShortfall(mock_results, alpha=0.05)
        es_series = es.parametric(dist="normal")
        assert np.all(es_series <= var_series)

        # Step 5: Backtest
        from archbox.risk.backtest import VaRBacktest

        bt = VaRBacktest(returns, var_series, alpha=0.05)
        kupiec = bt.kupiec_test()
        assert kupiec.pvalue > 0.01  # should not strongly reject
        summary = bt.summary()
        assert "Kupiec" in summary

        # Step 6: EWMA
        from archbox.risk.ewma import EWMA

        ewma = EWMA(returns, lam=0.94)
        ewma_result = ewma.fit()
        assert np.all(ewma_result.conditional_volatility > 0)

        # Step 7: Diagnostics
        report = full_diagnostics(mock_results)
        assert isinstance(report, DiagnosticReport)
        diag_summary = report.summary()
        assert "ARCH-LM" in diag_summary
        assert "Sign Bias" in diag_summary
        assert "Ljung-Box" in diag_summary
        assert "Jarque-Bera" in diag_summary

        # Full pipeline completed without errors!
