"""Tests for full_diagnostics() and DiagnosticReport."""

from __future__ import annotations

from typing import Any

import numpy as np
import pytest

from archbox.diagnostics.diagnostics import DiagnosticReport, full_diagnostics


class MockResults:
    """Mock ArchResults implementing the documented results contract.

    ``resid`` are the RAW residuals (same scale as the returns) and
    ``std_resid`` the standardized residuals eps_t / sigma_t.
    """

    def __init__(
        self,
        resid: np.ndarray,
        sigma: np.ndarray,
        scores: np.ndarray | None = None,
        model: Any = None,
        params: np.ndarray | None = None,
    ):
        self.resid = resid
        self.conditional_volatility = sigma
        self.std_resid = resid / sigma
        self.mu = 0.0
        self.scores = scores
        self._model = model
        self.params = params


def _simulate_garch(rng: np.random.Generator, n: int = 2000) -> tuple[np.ndarray, np.ndarray]:
    """Simulate a GARCH(1,1) on a realistic return scale."""
    omega, alpha, beta = 1e-6, 0.08, 0.91

    sigma2 = np.empty(n)
    returns = np.empty(n)
    sigma2[0] = omega / (1 - alpha - beta)

    for t in range(n):
        if t > 0:
            sigma2[t] = omega + alpha * returns[t - 1] ** 2 + beta * sigma2[t - 1]
        returns[t] = np.sqrt(sigma2[t]) * rng.standard_normal()

    return returns, np.sqrt(sigma2)


@pytest.fixture
def mock_garch_results(rng: np.random.Generator) -> MockResults:
    """Create mock GARCH results with realistic data."""
    returns, sigma = _simulate_garch(rng)
    scores = rng.standard_normal((len(returns), 3))
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

        # Without scores and without a differentiable model, Nyblom is omitted
        # with an explicit reason rather than silently dropped.
        assert report.nyblom is None
        assert "Nyblom" in report.skipped
        assert report.skipped["Nyblom"]


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

    def test_all_statistics_are_finite(self, mock_garch_results: MockResults) -> None:
        """Regression: the report used to be entirely NaN/empty.

        ``full_diagnostics`` looked up ``results.resids``/``results.endog``,
        which do not exist on ArchResults, and swallowed the resulting
        AttributeError with ``contextlib.suppress``.
        """
        report = full_diagnostics(mock_garch_results)

        assert report.arch_lm
        assert report.ljung_box_sq
        for result in report.arch_lm.values():
            assert np.isfinite(result.statistic)
            assert 0.0 <= result.pvalue <= 1.0
        for lb in report.ljung_box_sq.values():
            assert np.isfinite(lb.statistic)
            assert 0.0 <= lb.pvalue <= 1.0
        assert report.sign_bias is not None
        assert np.isfinite(report.sign_bias.joint[0])
        assert report.jarque_bera is not None
        assert all(np.isfinite(v) for v in report.jarque_bera)
        assert report.nyblom is not None
        assert np.isfinite(report.nyblom.joint_statistic)

        assert "nan" not in report.summary().lower()


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

    def test_summary_lists_skipped_tests(self, rng: np.random.Generator) -> None:
        returns = rng.standard_normal(40) * 0.01
        report = full_diagnostics(MockResults(returns, np.full(40, 0.01)))

        summary = report.summary()
        assert "Skipped" in summary
        assert "Nyblom" in summary


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

    def test_lags_argument_is_honoured(self, mock_garch_results: MockResults) -> None:
        """The `lags` argument used to be accepted and then ignored."""
        report = full_diagnostics(mock_garch_results, lags=7)

        assert sorted(report.arch_lm) == [1, 5, 7]
        assert sorted(report.ljung_box_sq) == [5, 7, 14]

    def test_lags_default_reproduces_documented_defaults(
        self, mock_garch_results: MockResults
    ) -> None:
        report = full_diagnostics(mock_garch_results)

        assert sorted(report.arch_lm) == [1, 5, 10]
        assert sorted(report.ljung_box_sq) == [5, 10, 20]

    def test_invalid_lags_raises(self, mock_garch_results: MockResults) -> None:
        with pytest.raises(ValueError, match="lags"):
            full_diagnostics(mock_garch_results, lags=0)


class TestFullDiagnosticsContract:
    """The results object must expose the documented residual attributes."""

    def test_missing_std_resid_raises(self, rng: np.random.Generator) -> None:
        class NoStdResid:
            resid = rng.standard_normal(200) * 0.01

        with pytest.raises(TypeError, match="std_resid"):
            full_diagnostics(NoStdResid())

    def test_missing_resid_raises(self, rng: np.random.Generator) -> None:
        class NoResid:
            std_resid = rng.standard_normal(200)

        with pytest.raises(TypeError, match="resid"):
            full_diagnostics(NoResid())

    def test_non_finite_residuals_raise(self, rng: np.random.Generator) -> None:
        """Real errors must propagate instead of being suppressed."""
        returns = rng.standard_normal(500) * 0.01
        sigma = np.full(500, 0.01)
        mock = MockResults(returns, sigma)
        mock.std_resid = mock.std_resid.copy()
        mock.std_resid[10] = np.nan

        with pytest.raises(ValueError, match="non-finite"):
            full_diagnostics(mock)

    def test_length_mismatch_raises(self, rng: np.random.Generator) -> None:
        mock = MockResults(rng.standard_normal(500) * 0.01, np.full(500, 0.01))
        mock.std_resid = mock.std_resid[:-1]

        with pytest.raises(ValueError, match="same length"):
            full_diagnostics(mock)


class TestFullDiagnosticsSkips:
    """Inapplicable tests are omitted with an explicit reason."""

    def test_short_sample_skips_long_lags(self, rng: np.random.Generator) -> None:
        n = 12
        returns = rng.standard_normal(n) * 0.01
        report = full_diagnostics(MockResults(returns, np.full(n, 0.01)))

        assert 20 not in report.ljung_box_sq
        assert "Ljung-Box z^2 (20)" in report.skipped
        assert "T=12" in report.skipped["Ljung-Box z^2 (20)"]
        # Short lags still run.
        assert 5 in report.ljung_box_sq

    def test_tiny_sample_skips_sign_bias(self, rng: np.random.Generator) -> None:
        n = 4
        returns = rng.standard_normal(n) * 0.01
        report = full_diagnostics(MockResults(returns, np.full(n, 0.01)))

        assert report.sign_bias is None
        assert "Sign Bias" in report.skipped

    def test_too_many_parameters_skips_nyblom(self, rng: np.random.Generator) -> None:
        n = 500
        returns = rng.standard_normal(n) * 0.01
        scores = rng.standard_normal((n, 21))
        report = full_diagnostics(MockResults(returns, np.full(n, 0.01), scores=scores))

        assert report.nyblom is None
        assert "k=21" in report.skipped["Nyblom"]


class TestNyblomFromFittedModel:
    """Nyblom is wired to the per-observation scores of the fitted model."""

    @pytest.fixture
    def fitted(self, sp500_returns: np.ndarray) -> MockResults:
        from archbox import GARCH

        model = GARCH(sp500_returns)
        res = model.fit(disp=False)
        resid = np.asarray(model.endog, dtype=np.float64)
        sigma = np.asarray(res.conditional_volatility, dtype=np.float64)
        return MockResults(resid, sigma, scores=None, model=model, params=res.params)

    def test_nyblom_uses_loglike_per_obs(self, fitted: MockResults) -> None:
        report = full_diagnostics(fitted)

        assert report.nyblom is not None
        assert "Nyblom" not in report.skipped
        assert fitted.params is not None
        assert report.nyblom.num_params == len(fitted.params)
        assert np.isfinite(report.nyblom.joint_statistic)
        assert report.nyblom.joint_statistic > 0.0
        assert np.all(np.isfinite(report.nyblom.individual_statistics))

    def test_report_on_real_data_has_no_nan(self, fitted: MockResults) -> None:
        report = full_diagnostics(fitted)

        assert "nan" not in report.summary().lower()
        assert report.sign_bias is not None
        assert report.jarque_bera is not None
        assert all(np.isfinite(v) for v in report.jarque_bera)


class TestIntegrationEndToEnd:
    """Full integration test: data -> GARCH -> VaR -> backtest -> diagnostics."""

    def test_full_pipeline(self, rng: np.random.Generator) -> None:
        # Step 1: Generate data
        n = 2000
        returns, sigma = _simulate_garch(rng, n)

        # Step 2: Mock "GARCH fit" results
        mock_results = MockResults(returns, sigma, scores=rng.standard_normal((n, 3)))
        mock_results.params = np.array([1e-6, 0.08, 0.91])
        mock_results.p = 1  # type: ignore[attr-defined]
        mock_results.q = 1  # type: ignore[attr-defined]

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
        assert "Kupiec" in bt.summary()

        # Step 6: EWMA
        from archbox.risk.ewma import EWMA

        ewma_result = EWMA(returns, lam=0.94).fit()
        assert np.all(ewma_result.conditional_volatility > 0)

        # Step 7: Diagnostics
        report = full_diagnostics(mock_results)
        assert isinstance(report, DiagnosticReport)
        diag_summary = report.summary()
        assert "ARCH-LM" in diag_summary
        assert "Sign Bias" in diag_summary
        assert "Ljung-Box" in diag_summary
        assert "Jarque-Bera" in diag_summary
        assert "nan" not in diag_summary.lower()


class TestJarqueBera:
    """The Jarque-Bera entry must match scipy and use the survival function."""

    def test_matches_scipy(self, mock_garch_results: MockResults) -> None:
        from scipy import stats

        report = full_diagnostics(mock_garch_results)
        assert report.jarque_bera is not None
        expected = stats.jarque_bera(mock_garch_results.std_resid)

        assert report.jarque_bera[0] == pytest.approx(float(expected[0]), rel=1e-10)
        assert report.jarque_bera[1] == pytest.approx(float(expected[1]), rel=1e-10)

    def test_tail_pvalue_is_positive(self, rng: np.random.Generator) -> None:
        from scipy import stats

        n = 800
        heavy = rng.standard_t(5, size=n) * 0.01
        report = full_diagnostics(MockResults(heavy, np.full(n, 0.01)))

        assert report.jarque_bera is not None
        stat, pvalue = report.jarque_bera
        # 1 - chi2.cdf(stat, 2) rounds to exactly 0 well before chi2.sf does.
        assert stat > 100.0
        assert pvalue > 0.0
        assert pvalue == pytest.approx(float(stats.chi2.sf(stat, df=2)), rel=1e-12)


class TestSuppliedScores:
    """A results object may supply its own score matrix."""

    def test_one_dimensional_scores(self, rng: np.random.Generator) -> None:
        n = 600
        returns = rng.standard_normal(n) * 0.01
        scores = rng.standard_normal(n)
        report = full_diagnostics(MockResults(returns, np.full(n, 0.01), scores=scores))

        assert report.nyblom is not None
        assert report.nyblom.num_params == 1

    def test_supplied_scores_are_demeaned(self, rng: np.random.Generator) -> None:
        """A constant drift in the scores is not evidence of instability."""
        n = 600
        returns = rng.standard_normal(n) * 0.01
        stable = rng.standard_normal((n, 2))
        shifted = stable + 5.0

        base = full_diagnostics(MockResults(returns, np.full(n, 0.01), scores=stable))
        drifted = full_diagnostics(MockResults(returns, np.full(n, 0.01), scores=shifted))

        assert base.nyblom is not None
        assert drifted.nyblom is not None
        assert drifted.nyblom.joint_statistic == pytest.approx(
            base.nyblom.joint_statistic, rel=1e-8
        )
