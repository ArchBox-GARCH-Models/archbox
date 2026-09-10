"""Tests for Sign Bias test."""

from __future__ import annotations

import numpy as np
import pytest

from archbox.diagnostics.sign_bias import SignBiasResult, sign_bias_test


class TestSignBiasDetectsAsymmetry:
    """test_sign_bias_detects_asymmetry: Joint test rejects for asymmetric DGP."""

    def test_sign_bias_detects_asymmetry(self, rng: np.random.Generator) -> None:
        # Generate EGARCH-like process (asymmetric volatility)
        n = 3000
        omega = -0.1
        alpha = 0.15
        gamma = -0.10  # leverage effect
        beta = 0.98

        log_sigma2 = np.empty(n)
        returns = np.empty(n)
        z = np.empty(n)
        log_sigma2[0] = omega / (1 - beta)

        for t in range(n):
            sigma = np.exp(log_sigma2[t] / 2)
            z[t] = rng.standard_normal()
            returns[t] = sigma * z[t]

            if t < n - 1:
                log_sigma2[t + 1] = (
                    omega
                    + alpha * (abs(z[t]) - np.sqrt(2 / np.pi))
                    + gamma * z[t]
                    + beta * log_sigma2[t]
                )

        # Use symmetric GARCH sigma for standardized residuals
        sigma2_simple = np.empty(n)
        sigma2_simple[0] = np.var(returns[:50])
        for t in range(1, n):
            sigma2_simple[t] = 1e-5 + 0.08 * returns[t - 1] ** 2 + 0.90 * sigma2_simple[t - 1]

        sigma_simple = np.sqrt(sigma2_simple)
        std_resids = returns / sigma_simple

        result = sign_bias_test(returns, std_resids)

        assert isinstance(result, SignBiasResult)
        # Joint test should detect asymmetry (at least marginally)
        assert result.joint[1] < 0.20, (
            f"Joint sign bias should detect asymmetry, p={result.joint[1]:.4f}"
        )


class TestSignBiasSymmetricGARCH:
    """test_sign_bias_symmetric_garch: Joint test does not reject for symmetric GARCH."""

    def test_sign_bias_symmetric_garch(self, rng: np.random.Generator) -> None:
        # Generate symmetric GARCH(1,1)
        n = 3000
        omega, alpha, beta = 1e-5, 0.08, 0.91

        sigma2 = np.empty(n)
        returns = np.empty(n)
        sigma2[0] = omega / (1 - alpha - beta)

        for t in range(n):
            if t > 0:
                sigma2[t] = omega + alpha * returns[t - 1] ** 2 + beta * sigma2[t - 1]
            z = rng.standard_normal()
            returns[t] = np.sqrt(sigma2[t]) * z

        sigma = np.sqrt(sigma2)
        std_resids = returns / sigma

        result = sign_bias_test(returns, std_resids)

        # Joint test should NOT reject for symmetric GARCH
        assert result.joint[1] > 0.05, (
            f"Joint sign bias should not reject for symmetric GARCH, p={result.joint[1]:.4f}"
        )


class TestSignBiasEdgeCases:
    """Edge case tests."""

    def test_mismatched_lengths(self) -> None:
        with pytest.raises(ValueError, match="same length"):
            sign_bias_test(np.random.randn(100), np.random.randn(50))

    def test_output_structure(self, rng: np.random.Generator) -> None:
        n = 500
        resids = rng.standard_normal(n) * 0.01
        std_resids = rng.standard_normal(n)

        result = sign_bias_test(resids, std_resids)

        assert len(result.sign_bias) == 2
        assert len(result.neg_sign_bias) == 2
        assert len(result.pos_sign_bias) == 2
        assert len(result.joint) == 2
