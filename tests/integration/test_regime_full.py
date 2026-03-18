"""Integration test: Regime-switching full pipeline.

Workflow: Load US GDP -> Fit MS-AR(2,4) -> Smoothed probs -> Recession detection -> Report
"""

from __future__ import annotations

import numpy as np
import pytest

from archbox.datasets import load_dataset


class TestRegimeFullPipeline:
    """End-to-end test for regime-switching workflow."""

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        """Load GDP data."""
        gdp = load_dataset("us_gdp")
        self.data = gdp["growth"].dropna().to_numpy(dtype=np.float64)

    def test_msar_end_to_end(self) -> None:
        """Full MS-AR pipeline: fit -> smoothed probs -> recession detection -> report."""
        from archbox.regime.ms_ar import MarkovSwitchingAR

        # Step 1: Fit MS-AR(2,4)
        model = MarkovSwitchingAR(self.data, k_regimes=2, order=4)
        results = model.fit(method="em", verbose=False)

        # Verify basic fit
        assert results.params is not None
        assert np.isfinite(results.loglike)
        assert results.aic is not None
        assert results.bic is not None

        # Step 2: Smoothed probabilities (attribute)
        smoothed = results.smoothed_probs
        assert smoothed.shape[0] > 0
        assert smoothed.shape[1] == 2  # 2 regimes
        # Probabilities sum to 1
        prob_sums = np.sum(smoothed, axis=1)
        np.testing.assert_allclose(prob_sums, 1.0, atol=1e-6)

        # Step 3: Transition matrix
        trans_mat = results.transition_matrix
        assert trans_mat.shape == (2, 2)
        # Rows sum to 1
        row_sums = np.sum(trans_mat, axis=1)
        np.testing.assert_allclose(row_sums, 1.0, atol=1e-6)
        # All elements in [0, 1]
        assert np.all(trans_mat >= 0)
        assert np.all(trans_mat <= 1)

        # Step 4: Regime classification
        regimes = results.classify()
        assert len(regimes) > 0
        assert set(np.unique(regimes)).issubset({0, 1})

        # Step 5: Summary
        summary = results.summary()
        assert isinstance(summary, str)
        assert len(summary) > 50

    def test_msar_different_order(self) -> None:
        """MS-AR with different AR order works."""
        from archbox.regime.ms_ar import MarkovSwitchingAR

        model = MarkovSwitchingAR(self.data, k_regimes=2, order=2)
        results = model.fit(method="em", verbose=False)
        assert results.params is not None
