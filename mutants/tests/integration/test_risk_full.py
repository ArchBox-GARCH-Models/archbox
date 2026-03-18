"""Integration test: Risk management full pipeline.

Workflow: Load SP500 -> Fit GARCH -> VaR (all methods) -> Backtest (all tests) -> Report
"""

from __future__ import annotations

import numpy as np
import pytest

from archbox.datasets import load_dataset
from archbox.models.garch import GARCH


class TestRiskFullPipeline:
    """End-to-end test for risk management workflow."""

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        """Load data and fit model."""
        sp500 = load_dataset("sp500")
        self.returns = sp500["returns"].to_numpy(dtype=np.float64)
        model = GARCH(self.returns, p=1, q=1)
        self.results = model.fit(disp=False)

    def test_risk_all_methods(self) -> None:
        """All VaR methods work end-to-end."""
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(self.results, alpha=0.05)

        # Parametric
        var_param = var_calc.parametric()
        assert len(var_param) > 0
        assert np.all(np.isfinite(var_param))

        # Historical simulation (first `window` values are NaN by design)
        var_hist = var_calc.historical()
        assert len(var_hist) > 0
        valid_hist = var_hist[~np.isnan(var_hist)]
        assert len(valid_hist) > 0
        assert np.all(np.isfinite(valid_hist))

        # Filtered historical simulation (first `min_obs` values are NaN)
        var_fhs = var_calc.filtered_historical()
        assert len(var_fhs) > 0
        valid_fhs = var_fhs[~np.isnan(var_fhs)]
        assert len(valid_fhs) > 0
        assert np.all(np.isfinite(valid_fhs))

        # Monte Carlo
        var_mc = var_calc.monte_carlo(n_sims=1000)
        assert len(var_mc) > 0
        assert np.all(np.isfinite(var_mc))

    def test_expected_shortfall(self) -> None:
        """Expected shortfall computation works."""
        from archbox.risk.es import ExpectedShortfall

        es_calc = ExpectedShortfall(self.results, alpha=0.05)
        es_param = es_calc.parametric()
        assert len(es_param) > 0
        assert np.all(np.isfinite(es_param))

    def test_backtest_all_tests(self) -> None:
        """All backtest tests work."""
        from archbox.risk.backtest import VaRBacktest
        from archbox.risk.var import ValueAtRisk

        var_calc = ValueAtRisk(self.results, alpha=0.05)
        var_series = var_calc.parametric()

        window = min(500, len(self.returns) // 2)
        bt = VaRBacktest(
            self.returns[-window:],
            var_series[-window:],
            alpha=0.05,
        )

        # Kupiec test
        kupiec = bt.kupiec_test()
        assert hasattr(kupiec, "statistic")
        assert hasattr(kupiec, "pvalue")
        assert np.isfinite(kupiec.statistic)
        assert 0 <= kupiec.pvalue <= 1

        # Christoffersen test
        chris = bt.christoffersen_test()
        assert hasattr(chris, "statistic")
        assert hasattr(chris, "pvalue")

        # Traffic light
        tl = bt.basel_traffic_light()
        assert tl in ("green", "yellow", "red")

        # Violation ratio
        vr = bt.violation_ratio()
        assert vr >= 0

    def test_risk_report(self) -> None:
        """Risk report generation works."""
        from archbox.report.report_manager import ReportManager

        report = ReportManager()
        html = report.generate(self.results, report_type="risk", fmt="html")
        assert isinstance(html, str)
        assert len(html) > 100
