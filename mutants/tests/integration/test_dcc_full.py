"""Integration test: DCC full pipeline.

Workflow: Load FX data -> Fit DCC(2 series) -> Dynamic correlation -> Portfolio variance -> Report
"""

from __future__ import annotations

import numpy as np
import pytest

from archbox.datasets import load_dataset


class TestDCCFullPipeline:
    """End-to-end test for DCC workflow."""

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        """Load FX data."""
        fx = load_dataset("fx_majors")
        # Use first two FX series (exclude date column)
        cols = [c for c in fx.columns if c != "date"][:2]
        self.returns = fx[cols].dropna().to_numpy(dtype=np.float64)

    def test_dcc_end_to_end(self) -> None:
        """Full DCC pipeline: fit -> correlation -> portfolio -> report."""
        from archbox.multivariate.dcc import DCC

        # Step 1: Fit DCC
        model = DCC(self.returns)
        results = model.fit(disp=False)

        # Verify basic fit
        assert results.params is not None
        assert np.isfinite(results.loglike)

        # Step 2: Dynamic correlation (attribute, not method)
        dyn_corr = results.dynamic_correlation
        assert dyn_corr is not None
        assert dyn_corr.shape[0] == self.returns.shape[0]
        # Correlations should be in [-1, 1]
        assert np.all(dyn_corr >= -1.0 - 1e-6)
        assert np.all(dyn_corr <= 1.0 + 1e-6)

        # Step 3: Portfolio volatility
        weights = np.array([0.5, 0.5])
        port_vol = results.portfolio_volatility(weights)
        assert len(port_vol) > 0
        assert np.all(port_vol >= 0)

        # Step 4: Summary
        summary = results.summary()
        assert isinstance(summary, str)
        assert len(summary) > 50

    def test_dcc_different_p_q(self) -> None:
        """DCC with different univariate lag orders works."""
        from archbox.multivariate.dcc import DCC

        model = DCC(self.returns, univariate_order=(1, 1))
        results = model.fit(disp=False)
        assert results.params is not None
