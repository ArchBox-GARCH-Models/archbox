"""Integration tests for the complete report pipeline.

Tests the full flow: mock results -> Transformer -> Template -> Rendered output
for all report types and formats.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import numpy as np
import pytest

from archbox.report import ReportManager


@pytest.fixture
def mock_garch_results():
    """Create comprehensive mock GARCH results for integration testing."""
    rng = np.random.default_rng(42)
    T = 500

    results = MagicMock()
    results.model_name = "GARCH(1,1)"
    results.nobs = T
    results.params = np.array([1.5e-6, 0.08, 0.91])
    results.param_names = ["omega", "alpha[1]", "beta[1]"]
    results.std_errors = np.array([3e-7, 0.01, 0.01])
    results.tvalues = np.array([5.0, 8.0, 91.0])
    results.pvalues = np.array([0.0001, 0.0001, 0.0001])
    results.persistence = 0.99
    results.unconditional_variance = 1.5e-4
    results.loglikelihood = 4500.0
    results.aic = -8990.0
    results.bic = -8970.0
    results.hqic = -8983.0
    results.conditional_volatility = np.abs(rng.standard_normal(T)) * 0.01 + 0.005
    results.resid = rng.standard_normal(T) * 0.01
    results.std_resid = rng.standard_normal(T)
    results.arch_lm = {"stat": 1.5, "pvalue": 0.22}
    results.ljung_box_z2 = {"stat": 10.2, "pvalue": 0.45}
    results.sign_bias = {"stat": 0.8, "pvalue": 0.42}
    return results


@pytest.fixture
def mock_regime_results():
    """Create mock regime results for integration testing."""
    rng = np.random.default_rng(42)
    T = 500
    K = 2

    smoothed_probs = np.zeros((T, K))
    for t in range(T):
        p = 0.8 if rng.random() > 0.3 else 0.2
        smoothed_probs[t, 0] = p
        smoothed_probs[t, 1] = 1 - p

    results = MagicMock()
    results.model_name = "MS-GARCH(2)"
    results.n_regimes = K
    results.nobs = T
    results.transition_matrix = np.array([[0.97, 0.03], [0.05, 0.95]])
    results.smoothed_probs = smoothed_probs
    results.regime_params = [
        {"omega": 1e-6, "alpha": 0.05, "beta": 0.90},
        {"omega": 5e-6, "alpha": 0.15, "beta": 0.80},
    ]
    results.loglikelihood = 4200.0
    results.aic = -8390.0
    results.bic = -8360.0
    return results


@pytest.fixture
def mock_risk_results():
    """Create mock risk results for integration testing."""
    rng = np.random.default_rng(42)
    T = 500
    returns = rng.standard_normal(T) * 0.01
    var = -np.abs(rng.standard_normal(T) * 0.01) - 0.015
    violations = returns < var

    results = MagicMock()
    results.model_name = "GARCH VaR"
    results.confidence_level = 0.99
    results.returns = returns
    results.var = var
    results.es = var * 1.3
    results.violations = violations
    results.nobs = T
    return results


@pytest.fixture
def report_manager():
    """Create ReportManager instance."""
    return ReportManager()


class TestGARCHReportGeneration:
    """Test GARCH report generation end-to-end."""

    def test_html_generates(self, report_manager, mock_garch_results):
        """HTML report generates without errors."""
        html = report_manager.generate(mock_garch_results, report_type="garch", fmt="html")
        assert isinstance(html, str)
        assert len(html) > 100

    def test_html_contains_params_table(self, report_manager, mock_garch_results):
        """HTML report contains parameter table."""
        html = report_manager.generate(mock_garch_results, report_type="garch", fmt="html")
        assert "omega" in html
        assert "alpha" in html
        assert "beta" in html
        assert "<table" in html

    def test_html_contains_diagnostics(self, report_manager, mock_garch_results):
        """HTML report contains diagnostics section."""
        html = report_manager.generate(mock_garch_results, report_type="garch", fmt="html")
        assert "Diagnostics" in html or "diagnostics" in html
        assert "ARCH-LM" in html

    def test_html_contains_volatility_chart(self, report_manager, mock_garch_results):
        """HTML report contains volatility chart container."""
        html = report_manager.generate(mock_garch_results, report_type="garch", fmt="html")
        assert "volatility" in html.lower()
        assert "chart-container" in html

    def test_html_has_sidebar(self, report_manager, mock_garch_results):
        """HTML report has sidebar navigation."""
        html = report_manager.generate(mock_garch_results, report_type="garch", fmt="html")
        assert "sidebar" in html

    def test_latex_generates(self, report_manager, mock_garch_results):
        """LaTeX report generates without errors."""
        latex = report_manager.generate(mock_garch_results, report_type="garch", fmt="latex")
        assert isinstance(latex, str)
        assert "\\documentclass" in latex
        assert "\\begin{document}" in latex

    def test_latex_has_booktabs(self, report_manager, mock_garch_results):
        """LaTeX report uses booktabs tables."""
        latex = report_manager.generate(mock_garch_results, report_type="garch", fmt="latex")
        assert "\\toprule" in latex
        assert "\\midrule" in latex
        assert "\\bottomrule" in latex

    def test_markdown_generates(self, report_manager, mock_garch_results):
        """Markdown report generates without errors."""
        md = report_manager.generate(mock_garch_results, report_type="garch", fmt="markdown")
        assert isinstance(md, str)
        assert "# " in md or "## " in md

    def test_markdown_has_tables(self, report_manager, mock_garch_results):
        """Markdown report has formatted tables."""
        md = report_manager.generate(mock_garch_results, report_type="garch", fmt="markdown")
        assert "|" in md
        assert "---" in md

    def test_save_to_file(self, report_manager, mock_garch_results, tmp_path):
        """Reports can be saved to file."""
        html_path = tmp_path / "report.html"
        report_manager.generate(
            mock_garch_results,
            report_type="garch",
            fmt="html",
            output_path=html_path,
        )
        assert html_path.exists()
        assert html_path.stat().st_size > 100


class TestRegimeReportGeneration:
    """Test regime report generation."""

    def test_html_generates(self, report_manager, mock_regime_results):
        html = report_manager.generate(mock_regime_results, report_type="regime", fmt="html")
        assert isinstance(html, str)
        assert "Transition Matrix" in html or "transition" in html.lower()

    def test_latex_generates(self, report_manager, mock_regime_results):
        latex = report_manager.generate(mock_regime_results, report_type="regime", fmt="latex")
        assert "\\documentclass" in latex

    def test_markdown_generates(self, report_manager, mock_regime_results):
        md = report_manager.generate(mock_regime_results, report_type="regime", fmt="markdown")
        assert isinstance(md, str)


class TestRiskReportGeneration:
    """Test risk report generation."""

    def test_html_generates(self, report_manager, mock_risk_results):
        html = report_manager.generate(mock_risk_results, report_type="risk", fmt="html")
        assert isinstance(html, str)
        assert "Backtest" in html or "backtest" in html.lower()

    def test_latex_generates(self, report_manager, mock_risk_results):
        latex = report_manager.generate(mock_risk_results, report_type="risk", fmt="latex")
        assert "\\documentclass" in latex

    def test_markdown_generates(self, report_manager, mock_risk_results):
        md = report_manager.generate(mock_risk_results, report_type="risk", fmt="markdown")
        assert isinstance(md, str)


class TestAllReportTypes:
    """Test that all 4 report types generate in all 3 formats."""

    @pytest.mark.parametrize(
        "report_type,fixture_name",
        [
            ("garch", "mock_garch_results"),
            ("regime", "mock_regime_results"),
            ("risk", "mock_risk_results"),
        ],
    )
    @pytest.mark.parametrize("fmt", ["html", "latex", "markdown"])
    def test_generates(self, report_type, fixture_name, fmt, request):
        """All report_type + format combinations generate successfully."""
        results = request.getfixturevalue(fixture_name)
        manager = ReportManager()
        output = manager.generate(results, report_type=report_type, fmt=fmt)
        assert isinstance(output, str)
        assert len(output) > 50


class TestReportManagerAPI:
    """Test ReportManager API."""

    def test_list_report_types(self):
        types = ReportManager.list_report_types()
        assert "garch" in types
        assert "multivariate" in types
        assert "regime" in types
        assert "risk" in types

    def test_list_formats(self):
        fmts = ReportManager.list_formats()
        assert "html" in fmts
        assert "latex" in fmts
        assert "markdown" in fmts

    def test_unknown_report_type_raises(self, mock_garch_results):
        manager = ReportManager()
        with pytest.raises(ValueError, match="Unknown report type"):
            manager.generate(mock_garch_results, report_type="invalid")

    def test_unknown_format_raises(self, mock_garch_results):
        manager = ReportManager()
        with pytest.raises(ValueError, match="Unknown format"):
            manager.generate(mock_garch_results, report_type="garch", fmt="invalid")
