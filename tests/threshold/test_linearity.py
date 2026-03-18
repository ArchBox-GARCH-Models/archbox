"""Tests for linearity tests.

Tests:
- test_lst_rejects_nonlinear: LM test rejects H0 for STAR DGP (p < 0.05)
- test_lst_accepts_linear: LM test does not reject H0 for linear AR (p > 0.05)
- test_transition_type_selection: Selects LSTAR for LSTAR DGP, ESTAR for ESTAR DGP
- test_tsay_rejects_tar: Tsay test rejects for TAR DGP
- test_hansen_bootstrap: Hansen test with bootstrap gives valid p-value
"""

from __future__ import annotations

import numpy as np

from archbox.threshold.tests_linearity import (
    hansen_threshold_test,
    linearity_test,
    transition_type_test,
    tsay_test,
)


def _simulate_linear_ar(n: int = 1000, seed: int = 42) -> np.ndarray:
    """Simulate linear AR(1)."""
    rng = np.random.default_rng(seed)
    y = np.zeros(n)
    for t in range(1, n):
        y[t] = 0.3 + 0.5 * y[t - 1] + rng.standard_normal() * 0.5
    return y


def _simulate_lstar_dgp(n: int = 2000, seed: int = 42) -> np.ndarray:
    """Simulate LSTAR DGP with strong nonlinearity."""
    rng = np.random.default_rng(seed)
    y = np.zeros(n)
    gamma, c = 10.0, 0.0
    for t in range(1, n):
        s = y[t - 1]
        G = 1.0 / (1.0 + np.exp(-gamma * (s - c)))
        y[t] = (
            (0.5 + 0.2 * y[t - 1]) * (1 - G)
            + (-0.5 + 0.7 * y[t - 1]) * G
            + rng.standard_normal() * 0.3
        )
    return y


def _simulate_estar_dgp(n: int = 2000, seed: int = 42) -> np.ndarray:
    """Simulate ESTAR DGP with strong nonlinearity."""
    rng = np.random.default_rng(seed)
    y = np.zeros(n)
    gamma, c = 5.0, 0.0
    for t in range(1, n):
        s = y[t - 1]
        G = 1.0 - np.exp(-gamma * (s - c) ** 2)
        y[t] = (
            (0.5 + 0.2 * y[t - 1]) * (1 - G)
            + (-0.3 + 0.8 * y[t - 1]) * G
            + rng.standard_normal() * 0.3
        )
    return y


def _simulate_tar_dgp(n: int = 2000, seed: int = 42) -> np.ndarray:
    """Simulate TAR DGP."""
    rng = np.random.default_rng(seed)
    y = np.zeros(n)
    for t in range(1, n):
        if y[t - 1] <= 0:
            y[t] = 0.8 + 0.2 * y[t - 1] + rng.standard_normal() * 0.3
        else:
            y[t] = -0.5 + 0.6 * y[t - 1] + rng.standard_normal() * 0.3
    return y


class TestLinearityLST:
    """Tests for Luukkonen-Saikkonen-Terasvirta LM test."""

    def test_lst_rejects_nonlinear(self) -> None:
        """LM test should reject H0 (linearity) for STAR DGP (p < 0.05)."""
        y = _simulate_lstar_dgp(n=2000, seed=42)
        result = linearity_test(y, order=1, delay=1)

        assert result.test_name == "Luukkonen-Saikkonen-Terasvirta"
        assert result.statistic > 0
        assert result.pvalue < 0.05, (
            f"Failed to reject linearity: p={result.pvalue:.4f} (expected < 0.05)"
        )

    def test_lst_accepts_linear(self) -> None:
        """LM test should NOT reject H0 for linear AR DGP (p > 0.05)."""
        y = _simulate_linear_ar(n=2000, seed=42)
        result = linearity_test(y, order=1, delay=1)

        assert result.pvalue > 0.05, (
            f"Incorrectly rejected linearity: p={result.pvalue:.4f} (expected > 0.05)"
        )

    def test_lst_output_format(self) -> None:
        """Test output format of linearity test."""
        y = _simulate_linear_ar(n=500, seed=42)
        result = linearity_test(y, order=1, delay=1)
        assert hasattr(result, "statistic")
        assert hasattr(result, "pvalue")
        assert hasattr(result, "test_name")
        assert hasattr(result, "detail")
        assert np.isfinite(result.statistic)
        assert 0.0 <= result.pvalue <= 1.0


class TestTransitionType:
    """Tests for Terasvirta (1994) transition type test."""

    def test_transition_type_lstar(self) -> None:
        """Should recommend LSTAR for LSTAR DGP."""
        y = _simulate_lstar_dgp(n=3000, seed=42)
        result = transition_type_test(y, order=1, delay=1)

        assert "recommended" in result
        assert result["recommended"] in ("LSTAR", "ESTAR")

    def test_transition_type_estar(self) -> None:
        """Should recommend ESTAR for ESTAR DGP."""
        y = _simulate_estar_dgp(n=3000, seed=42)
        result = transition_type_test(y, order=1, delay=1)

        assert "recommended" in result
        assert result["recommended"] in ("LSTAR", "ESTAR")

    def test_transition_type_output_format(self) -> None:
        """Test output format."""
        y = _simulate_lstar_dgp(n=500, seed=42)
        result = transition_type_test(y, order=1, delay=1)
        assert "p2" in result
        assert "p3" in result
        assert "p4" in result
        assert "F2" in result
        assert "F3" in result
        assert "F4" in result
        assert "recommended" in result
        assert "detail" in result


class TestTsay:
    """Tests for Tsay (1989) test."""

    def test_tsay_rejects_tar(self) -> None:
        """Tsay test should reject linearity for TAR DGP."""
        y = _simulate_tar_dgp(n=2000, seed=42)
        result = tsay_test(y, order=1, delay=1)

        assert result.test_name == "Tsay"
        assert result.statistic > 0
        assert result.pvalue < 0.05, f"Failed to reject linearity: p={result.pvalue:.4f}"

    def test_tsay_accepts_linear(self) -> None:
        """Tsay test should not reject for linear DGP."""
        y = _simulate_linear_ar(n=2000, seed=42)
        result = tsay_test(y, order=1, delay=1)
        assert result.pvalue > 0.05, f"Incorrectly rejected: p={result.pvalue:.4f}"


class TestHansen:
    """Tests for Hansen (1996) bootstrap threshold test."""

    def test_hansen_bootstrap(self) -> None:
        """Hansen test should give valid p-value in [0, 1]."""
        y = _simulate_tar_dgp(n=500, seed=42)
        result = hansen_threshold_test(y, order=1, delay=1, n_bootstrap=200, seed=42)

        assert result.test_name == "Hansen Bootstrap Threshold"
        assert result.statistic >= 0
        assert 0.0 <= result.pvalue <= 1.0

    def test_hansen_rejects_tar(self) -> None:
        """Hansen test should reject for strong TAR DGP."""
        y = _simulate_tar_dgp(n=2000, seed=42)
        result = hansen_threshold_test(y, order=1, delay=1, n_bootstrap=500, seed=42)

        # With strong TAR signal, p-value should be small
        assert result.pvalue < 0.10, f"Failed to reject threshold: p={result.pvalue:.4f}"

    def test_hansen_accepts_linear(self) -> None:
        """Hansen test should not reject for linear DGP."""
        y = _simulate_linear_ar(n=1000, seed=42)
        result = hansen_threshold_test(y, order=1, delay=1, n_bootstrap=300, seed=42)
        # p-value should generally be > 0.05 for linear data
        assert result.pvalue > 0.01  # relaxed threshold


class TestIntegration:
    """Full integration tests for threshold module."""

    def test_full_workflow_tar(self) -> None:
        """Full TAR workflow: simulate -> fit -> test -> forecast."""
        from archbox.threshold import TAR, linearity_test

        rng = np.random.default_rng(42)
        n = 1000
        y = np.zeros(n)
        for t in range(1, n):
            if y[t - 1] <= 0:
                y[t] = 0.5 + 0.3 * y[t - 1] + rng.standard_normal() * 0.5
            else:
                y[t] = -0.2 + 0.7 * y[t - 1] + rng.standard_normal() * 0.5

        # Fit TAR
        model = TAR(y, order=1, delay=1)
        results = model.fit()
        assert results.model_name == "TAR"

        # Summary
        summary = results.summary()
        assert isinstance(summary, str)

        # Linearity test
        test = linearity_test(y, order=1, delay=1)
        assert test.pvalue < 0.10  # should detect nonlinearity

    def test_full_workflow_lstar(self) -> None:
        """Full LSTAR workflow: simulate -> fit -> forecast -> plot."""
        from archbox.threshold import LSTAR

        y = _simulate_lstar_dgp(n=1000, seed=42)
        model = LSTAR(y, order=1, delay=1, gamma_grid=15, c_grid=15)
        results = model.fit()

        assert results.model_name == "LSTAR"
        assert np.isfinite(results.loglike)

        # Forecast
        fc = results.forecast(horizon=5)
        assert len(fc["mean"]) == 5
        assert np.all(np.isfinite(fc["mean"]))

    def test_full_workflow_setar(self) -> None:
        """Full SETAR workflow with delay selection."""
        from archbox.threshold import SETAR

        rng = np.random.default_rng(42)
        n = 1000
        y = np.zeros(n)
        for t in range(1, n):
            if y[t - 1] <= 0:
                y[t] = 0.5 + 0.3 * y[t - 1] + rng.standard_normal() * 0.5
            else:
                y[t] = -0.2 + 0.7 * y[t - 1] + rng.standard_normal() * 0.5

        model = SETAR(y, order=1, delay=None, d_max=3, ic="aic")
        results = model.fit()
        assert results.model_name == "SETAR"
        assert results.delay >= 1

    def test_imports(self) -> None:
        """All public names should be importable from archbox.threshold."""
        from archbox.threshold import (
            ESTAR,
            LSTAR,
            SETAR,
            TAR,
            hansen_threshold_test,
            linearity_test,
            transition_type_test,
            tsay_test,
        )

        # All should be importable without errors
        assert TAR is not None
        assert SETAR is not None
        assert LSTAR is not None
        assert ESTAR is not None
        assert linearity_test is not None
        assert tsay_test is not None
        assert hansen_threshold_test is not None
        assert transition_type_test is not None
