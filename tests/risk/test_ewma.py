"""Tests for EWMA / RiskMetrics implementation."""

from __future__ import annotations

import numpy as np
import pytest

from archbox.risk.ewma import EWMA, EWMAResult


@pytest.fixture
def garch_returns(rng: np.random.Generator) -> np.ndarray:
    """Generate GARCH-like returns for testing."""
    n = 2500
    omega, alpha, beta = 1e-6, 0.08, 0.91

    sigma2 = np.empty(n)
    returns = np.empty(n)
    sigma2[0] = omega / (1 - alpha - beta)

    for t in range(n):
        if t > 0:
            sigma2[t] = omega + alpha * returns[t - 1] ** 2 + beta * sigma2[t - 1]
        z = rng.standard_normal()
        returns[t] = np.sqrt(sigma2[t]) * z

    return returns


class TestEWMALambda094:
    """test_ewma_lambda_094: EWMA(lambda=0.94) produces reasonable volatility."""

    def test_ewma_lambda_094(self, garch_returns: np.ndarray) -> None:
        ewma = EWMA(garch_returns, lam=0.94)
        result = ewma.fit()

        assert isinstance(result, EWMAResult)
        assert len(result.conditional_volatility) == len(garch_returns)

        # Volatility should be positive
        assert np.all(result.conditional_volatility > 0)

        # Volatility should be in reasonable range for financial returns
        mean_vol = result.conditional_volatility.mean()
        assert 0.001 < mean_vol < 0.1, f"Mean vol {mean_vol} out of reasonable range"

    def test_ewma_lambda_097(self, garch_returns: np.ndarray) -> None:
        ewma = EWMA(garch_returns, lam=0.97)
        result = ewma.fit()

        # Higher lambda = smoother volatility
        ewma_094 = EWMA(garch_returns, lam=0.94)
        result_094 = ewma_094.fit()

        vol_std_097 = np.std(np.diff(result.conditional_volatility))
        vol_std_094 = np.std(np.diff(result_094.conditional_volatility))

        assert vol_std_097 < vol_std_094, "Higher lambda should produce smoother volatility"


class TestEWMAEqualsIGARCH:
    """test_ewma_equals_igarch: EWMA == IGARCH(omega=0, alpha=0.06, beta=0.94)."""

    def test_ewma_equals_igarch(self, garch_returns: np.ndarray) -> None:
        lam = 0.94
        ewma = EWMA(garch_returns, lam=lam)
        result = ewma.fit()

        # Manually compute IGARCH(1,1) with omega=0, alpha=1-lambda, beta=lambda
        omega = 0.0
        alpha = 1.0 - lam
        beta = lam

        T = len(garch_returns)
        sigma2_igarch = np.empty(T)
        sigma2_igarch[0] = result.conditional_variance[0]  # same initial value

        for t in range(1, T):
            sigma2_igarch[t] = (
                omega + alpha * garch_returns[t - 1] ** 2 + beta * sigma2_igarch[t - 1]
            )

        np.testing.assert_allclose(
            result.conditional_variance,
            sigma2_igarch,
            rtol=1e-10,
            err_msg="EWMA should be identical to IGARCH(omega=0)",
        )

    def test_ewma_params(self, garch_returns: np.ndarray) -> None:
        lam = 0.94
        ewma = EWMA(garch_returns, lam=lam)
        result = ewma.fit()

        # Check params match IGARCH structure
        np.testing.assert_allclose(result.params[0], 0.0)  # omega=0
        np.testing.assert_allclose(result.params[1], 1.0 - lam)  # alpha
        np.testing.assert_allclose(result.params[2], lam)  # beta


class TestEWMAMultivariate:
    """test_ewma_multivariate: EWMA multivariate H_t positive definite."""

    def test_ewma_multivariate(self, rng: np.random.Generator) -> None:
        # Generate bivariate returns
        n = 500
        k = 3
        cov = (
            np.array(
                [
                    [1.0, 0.5, 0.3],
                    [0.5, 1.0, 0.4],
                    [0.3, 0.4, 1.0],
                ]
            )
            * 1e-4
        )
        returns = rng.multivariate_normal(np.zeros(k), cov, size=n)

        ewma = EWMA(returns[:, 0], lam=0.94)  # univariate for constructor
        H = ewma.covariance(returns)

        assert H.shape == (n, k, k)

        # Check positive definiteness of all covariance matrices
        for t in range(n):
            eigenvalues = np.linalg.eigvalsh(H[t])
            assert np.all(
                eigenvalues > -1e-10
            ), f"H[{t}] is not positive semi-definite: eigenvalues={eigenvalues}"

    def test_ewma_multivariate_symmetry(self, rng: np.random.Generator) -> None:
        n = 200
        k = 2
        returns = rng.standard_normal((n, k)) * 0.01

        ewma = EWMA(returns[:, 0], lam=0.94)
        H = ewma.covariance(returns)

        # All matrices should be symmetric
        for t in range(n):
            np.testing.assert_allclose(
                H[t],
                H[t].T,
                atol=1e-12,
                err_msg=f"H[{t}] is not symmetric",
            )


class TestEWMAEdgeCases:
    """Edge case tests for EWMA."""

    def test_invalid_lambda(self) -> None:
        returns = np.random.randn(100)
        with pytest.raises(ValueError, match="lambda must be in"):
            EWMA(returns, lam=0.0)
        with pytest.raises(ValueError, match="lambda must be in"):
            EWMA(returns, lam=1.0)

    def test_multivariate_wrong_dims(self, rng: np.random.Generator) -> None:
        returns_1d = rng.standard_normal(100)
        ewma = EWMA(returns_1d, lam=0.94)
        with pytest.raises(ValueError, match="2D"):
            ewma.covariance(returns_1d)
