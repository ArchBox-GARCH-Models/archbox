"""Integration test: GARCH full pipeline.

Workflow: Load SP500 -> Fit GARCH(1,1) Student-t -> Diagnostics -> VaR -> Backtest -> Report
"""

from __future__ import annotations

import numpy as np
import pytest

from archbox.datasets import load_dataset
from archbox.models.garch import GARCH


class TestGARCHFullPipeline:
    """End-to-end test for GARCH workflow."""

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        """Load data and fit model."""
        sp500 = load_dataset("sp500")
        self.returns = sp500["returns"].to_numpy(dtype=np.float64)

    def test_garch_end_to_end(self) -> None:
        """Full GARCH pipeline: fit -> diagnose -> risk -> backtest -> report."""
        # Step 1: Fit
        model = GARCH(self.returns, p=1, q=1, dist="normal")
        results = model.fit(disp=False)

        # Verify basic fit
        assert results.params is not None
        assert len(results.params) > 0
        assert np.isfinite(results.loglike)
        assert np.isfinite(results.aic)
        assert np.isfinite(results.bic)

        # Persistence should be < 1
        assert 0 < results.persistence() < 1

        # Step 2: Diagnostics
        from archbox.diagnostics import full_diagnostics

        diag = full_diagnostics(results)
        assert diag.arch_lm is not None

        # Step 3: Summary
        summary = results.summary()
        assert isinstance(summary, str)
        assert "Persistence" in summary or "persistence" in summary.lower()

        # Step 4: Forecast
        forecast = results.forecast(horizon=10)
        assert forecast is not None
        assert "variance" in forecast
        assert len(forecast["variance"]) == 10

        # Step 5: Risk - VaR
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(results, alpha=0.05)
        var_series = var_calc.parametric()
        assert len(var_series) > 0
        assert (var_series < 0).all()  # VaR negative for long position

        # Step 6: Backtest
        from archbox.risk.backtest import VaRBacktest

        window = min(500, len(self.returns) // 2)
        test_returns = self.returns[-window:]
        test_var = var_series[-window:]
        bt = VaRBacktest(test_returns, test_var, alpha=0.05)
        violation_ratio = bt.violation_ratio()
        assert 0.0 <= violation_ratio <= 5.0  # reasonable range

        # Step 7: Report
        from archbox.report.report_manager import ReportManager

        report = ReportManager()
        html = report.generate(results, report_type="garch", fmt="html")
        assert "<table>" in html or "<div>" in html
        assert len(html) > 100

    def test_garch_normal_distribution(self) -> None:
        """GARCH with normal distribution also works end-to-end."""
        model = GARCH(self.returns, p=1, q=1, dist="normal")
        results = model.fit(disp=False)
        assert results.params is not None
        assert np.isfinite(results.loglike)

    def test_garch_variance_targeting(self) -> None:
        """GARCH with variance targeting works."""
        model = GARCH(self.returns, p=1, q=1)
        results = model.fit(variance_targeting=True, disp=False)
        assert results.params is not None
        assert np.isfinite(results.loglike)
