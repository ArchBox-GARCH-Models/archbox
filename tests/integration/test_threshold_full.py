"""Integration test: Threshold/STAR models full pipeline.

Workflow: Load data -> Linearity test -> Fit SETAR/LSTAR -> Phase diagram -> Report
"""

from __future__ import annotations

import numpy as np
import pytest

from archbox.datasets import load_dataset


class TestThresholdFullPipeline:
    """End-to-end test for threshold model workflow."""

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        """Load data for threshold models."""
        # Use SP500 returns (known to exhibit nonlinear behavior)
        sp500 = load_dataset("sp500")
        self.data = sp500["returns"].to_numpy(dtype=np.float64)

    def test_setar_end_to_end(self) -> None:
        """Full SETAR pipeline: linearity test -> fit -> regime analysis -> report."""
        from archbox.threshold.setar import SETAR

        # Step 1: Fit SETAR
        model = SETAR(self.data, order=2, n_regimes=2)
        results = model.fit()

        # Verify basic fit
        assert results.params is not None
        assert np.isfinite(results.loglike)
        assert results.threshold is not None

        # Step 2: Regime classification
        regimes = results.regime_assignments
        assert len(regimes) > 0
        unique_vals = set(np.unique(np.round(regimes).astype(int)))
        assert unique_vals.issubset({0, 1})

        # Step 3: Summary
        summary = results.summary()
        assert isinstance(summary, str)
        assert len(summary) > 50

    def test_lstar_end_to_end(self) -> None:
        """Full LSTAR pipeline: fit -> transition function -> report."""
        from archbox.threshold.lstar import LSTAR

        # Step 1: Fit LSTAR
        model = LSTAR(self.data, order=2)
        results = model.fit()

        # Verify basic fit
        assert results.params is not None
        assert np.isfinite(results.loglike)

        # Step 2: Transition function values
        transition = results.transition_values
        assert len(transition) > 0
        assert np.all(transition >= 0)
        assert np.all(transition <= 1)

        # Step 3: Summary
        summary = results.summary()
        assert isinstance(summary, str)

    def test_linearity_test(self) -> None:
        """Linearity test works before model fitting."""
        from archbox.threshold.tests_linearity import linearity_test

        result = linearity_test(self.data, order=4, delay=1)
        assert hasattr(result, "statistic")
        assert hasattr(result, "pvalue")
        assert np.isfinite(result.statistic)
        assert 0 <= result.pvalue <= 1
