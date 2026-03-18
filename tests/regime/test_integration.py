"""Integration tests for Fase 4 - Regime-Switching.

End-to-end tests verifying that all components work together.
"""

from __future__ import annotations

import numpy as np


class TestIntegrationMSMean:
    """Integration test for MS-Mean pipeline."""

    def test_full_pipeline_ms_mean(self) -> None:
        """Full pipeline: create -> fit -> summary -> classify -> plot."""
        from archbox.regime import MarkovSwitchingMean

        rng = np.random.default_rng(42)
        T = 300
        P = np.array([[0.95, 0.05], [0.10, 0.90]])
        mu = [-2.0, 2.0]
        sigma = 0.8

        regimes = np.zeros(T, dtype=int)
        regimes[0] = 1
        for t in range(1, T):
            regimes[t] = rng.choice(2, p=P[regimes[t - 1]])
        y = np.array([mu[s] + sigma * rng.standard_normal() for s in regimes])

        model = MarkovSwitchingMean(y, k_regimes=2)
        results = model.fit(maxiter=200, tol=1e-8, verbose=False)

        # Verify all results
        assert results.converged
        assert np.isfinite(results.loglike)
        assert results.filtered_probs.shape == (T, 2)
        assert results.smoothed_probs.shape == (T, 2)

        # Summary
        summary = results.summary()
        assert len(summary) > 0

        # Classify
        labels = results.classify()
        assert labels.shape == (T,)

        # Durations
        durations = results.expected_durations()
        assert all(d > 0 for d in durations)

        # Ergodic
        ergodic = results.ergodic_probabilities()
        np.testing.assert_allclose(ergodic.sum(), 1.0, atol=1e-10)


class TestIntegrationMSAR:
    """Integration test for MS-AR pipeline."""

    def test_full_pipeline_ms_ar_gdp(self) -> None:
        """Full pipeline with US GDP data."""
        from archbox.datasets import load_dataset
        from archbox.regime import MarkovSwitchingAR

        gdp = load_dataset("us_gdp")
        growth = gdp["growth"].to_numpy(dtype=np.float64)

        model = MarkovSwitchingAR(
            growth,
            k_regimes=2,
            order=4,
            switching_mean=True,
            switching_variance=True,
        )
        results = model.fit(maxiter=200, tol=1e-6, verbose=False)

        assert np.isfinite(results.loglike)
        assert results.transition_matrix.shape == (2, 2)

        summary = results.summary()
        assert "MS-AR" in summary

        durations = results.expected_durations()
        assert all(d > 0 for d in durations)


class TestIntegrationMSGARCH:
    """Integration test for MS-GARCH pipeline."""

    def test_full_pipeline_ms_garch(self) -> None:
        """Full pipeline for MS-GARCH."""
        from archbox.regime import MarkovSwitchingGARCH

        rng = np.random.default_rng(42)
        returns = rng.standard_normal(300) * 0.01

        model = MarkovSwitchingGARCH(returns, k_regimes=2, p=1, q=1)
        results = model.fit(maxiter=50, tol=1e-5, verbose=False)

        assert np.isfinite(results.loglike)
        assert results.transition_matrix.shape == (2, 2)

        for s in range(2):
            assert results.regime_params[s]["omega"] > 0


class TestIntegrationAllImports:
    """Test that all classes are importable from archbox.regime."""

    def test_all_imports(self) -> None:
        """All public classes should be importable."""
        from archbox.regime import (
            EMEstimator,
            HamiltonFilter,
            KimSmoother,
            MarkovSwitchingAR,
            MarkovSwitchingGARCH,
            MarkovSwitchingMean,
            MarkovSwitchingMeanVar,
            MarkovSwitchingModel,
            MarkovSwitchingVAR,
            RegimeResults,
        )

        assert MarkovSwitchingModel is not None
        assert MarkovSwitchingAR is not None
        assert MarkovSwitchingGARCH is not None
        assert MarkovSwitchingMean is not None
        assert MarkovSwitchingMeanVar is not None
        assert MarkovSwitchingVAR is not None
        assert HamiltonFilter is not None
        assert KimSmoother is not None
        assert EMEstimator is not None
        assert RegimeResults is not None
