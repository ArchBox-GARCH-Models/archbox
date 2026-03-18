"""Coverage tests for multivariate module: utils.py and results.py (MultivarResults)."""

from __future__ import annotations

from unittest.mock import MagicMock

import matplotlib
import numpy as np
import pytest

matplotlib.use("Agg")

from archbox.multivariate.utils import (
    corr_to_cov,
    cov_to_corr,
    ensure_positive_definite,
    is_positive_definite,
    validate_multivariate_returns,
)

# ============================================================
# Tests for multivariate/utils.py
# ============================================================


class TestEnsurePositiveDefinite:
    """Tests for ensure_positive_definite."""

    def test_already_pd(self) -> None:
        mat = np.eye(3)
        result = ensure_positive_definite(mat)
        np.testing.assert_allclose(result, mat, atol=1e-7)

    def test_not_pd_becomes_pd(self) -> None:
        mat = np.array([[1.0, 2.0], [2.0, 1.0]])  # not PD
        result = ensure_positive_definite(mat)
        eigvals = np.linalg.eigvalsh(result)
        assert np.all(eigvals > 0)

    def test_custom_epsilon(self) -> None:
        mat = np.array([[1.0, 2.0], [2.0, 1.0]])
        result = ensure_positive_definite(mat, epsilon=0.5)
        eigvals = np.linalg.eigvalsh(result)
        assert np.all(eigvals >= 0.5 - 1e-10)


class TestIsPositiveDefinite:
    """Tests for is_positive_definite."""

    def test_pd_matrix(self) -> None:
        assert is_positive_definite(np.eye(3)) is True

    def test_non_pd_matrix(self) -> None:
        mat = np.array([[1.0, 2.0], [2.0, 1.0]])
        assert is_positive_definite(mat) is False

    def test_singular_matrix(self) -> None:
        mat = np.array([[1.0, 1.0], [1.0, 1.0]])
        assert is_positive_definite(mat) is False


class TestCovCorr:
    """Tests for cov_to_corr and corr_to_cov."""

    def test_cov_to_corr_identity(self) -> None:
        corr = cov_to_corr(np.eye(3))
        np.testing.assert_allclose(corr, np.eye(3), atol=1e-10)

    def test_cov_to_corr_diagonal_ones(self) -> None:
        rng = np.random.default_rng(42)
        A = rng.standard_normal((3, 3))
        cov = A @ A.T + np.eye(3)
        corr = cov_to_corr(cov)
        np.testing.assert_allclose(np.diag(corr), np.ones(3), atol=1e-10)

    def test_cov_to_corr_zero_variance(self) -> None:
        """Zero diagonal should not cause division error."""
        cov = np.array([[0.0, 0.0], [0.0, 1.0]])
        corr = cov_to_corr(cov)
        assert np.all(np.isfinite(corr))

    def test_corr_to_cov(self) -> None:
        corr = np.array([[1.0, 0.5], [0.5, 1.0]])
        vols = np.array([2.0, 3.0])
        cov = corr_to_cov(corr, vols)
        assert cov[0, 0] == pytest.approx(4.0)
        assert cov[1, 1] == pytest.approx(9.0)
        assert cov[0, 1] == pytest.approx(3.0)

    def test_roundtrip_cov_corr_cov(self) -> None:
        rng = np.random.default_rng(42)
        A = rng.standard_normal((3, 3))
        cov_orig = A @ A.T + np.eye(3)
        corr = cov_to_corr(cov_orig)
        vols = np.sqrt(np.diag(cov_orig))
        cov_recovered = corr_to_cov(corr, vols)
        np.testing.assert_allclose(cov_recovered, cov_orig, atol=1e-10)


class TestValidateMultivariateReturns:
    """Tests for validate_multivariate_returns."""

    def test_valid_data(self) -> None:
        rng = np.random.default_rng(42)
        data = rng.standard_normal((50, 3))
        validate_multivariate_returns(data)  # should not raise

    def test_1d_raises(self) -> None:
        with pytest.raises(ValueError, match="must be 2D"):
            validate_multivariate_returns(np.ones(50))

    def test_single_series_raises(self) -> None:
        with pytest.raises(ValueError, match="at least 2 series"):
            validate_multivariate_returns(np.ones((50, 1)))

    def test_too_few_obs_raises(self) -> None:
        with pytest.raises(ValueError, match="at least 20 observations"):
            validate_multivariate_returns(np.ones((10, 2)))

    def test_nan_raises(self) -> None:
        data = np.ones((50, 2))
        data[5, 0] = np.nan
        with pytest.raises(ValueError, match="NaN"):
            validate_multivariate_returns(data)

    def test_inf_raises(self) -> None:
        data = np.ones((50, 2))
        data[5, 0] = np.inf
        with pytest.raises(ValueError, match="Inf"):
            validate_multivariate_returns(data)


# ============================================================
# Tests for MultivarResults (from multivariate/results.py -> base.py)
# ============================================================


class TestMultivarResults:
    """Tests for MultivarResults class."""

    @pytest.fixture()
    def mock_results(self):
        from archbox.multivariate.base import MultivarResults

        T, k = 50, 2
        rng = np.random.default_rng(42)

        # Create mock model
        model = MagicMock()
        model.model_name = "MockDCC"
        model.param_names = ["a", "b"]
        model.k = k

        def _portfolio_variance(weights, cov_t):
            w = np.asarray(weights)
            n_obs = cov_t.shape[0]
            pv = np.zeros(n_obs)
            for t in range(n_obs):
                pv[t] = float(w @ cov_t[t] @ w)
            return pv

        model.portfolio_variance = _portfolio_variance

        # Univariate results mocks
        univ_res = []
        for _ in range(k):
            r = MagicMock()
            r.params = np.array([0.01, 0.05, 0.9])
            univ_res.append(r)

        # Generate synthetic data
        corr = np.zeros((T, k, k))
        cov = np.zeros((T, k, k))
        for t in range(T):
            corr[t] = np.eye(k)
            corr[t, 0, 1] = corr[t, 1, 0] = 0.3
            cov[t] = corr[t] * 0.01

        return MultivarResults(
            model=model,
            univariate_results=univ_res,
            params=np.array([0.05, 0.93]),
            dynamic_correlation=corr,
            dynamic_covariance=cov,
            conditional_volatility=rng.uniform(0.005, 0.02, (T, k)),
            std_resids=rng.standard_normal((T, k)),
            loglike=-500.0,
            aic=1010.0,
            bic=1020.0,
            n_obs=T,
            n_series=k,
        )

    def test_summary(self, mock_results) -> None:
        s = mock_results.summary()
        assert "MockDCC" in s
        assert "Log-likelihood" in s
        assert "AIC" in s
        assert "BIC" in s
        assert "Correlation Model Parameters" in s

    def test_summary_no_corr_params(self, mock_results) -> None:
        mock_results.params = np.array([])
        s = mock_results.summary()
        assert "Correlation Model Parameters" not in s

    def test_plot_correlation(self, mock_results) -> None:
        import matplotlib.pyplot as plt

        mock_results.plot_correlation(0, 1)
        plt.close("all")

    def test_plot_covariance(self, mock_results) -> None:
        import matplotlib.pyplot as plt

        mock_results.plot_covariance(0, 1)
        plt.close("all")

    def test_portfolio_volatility(self, mock_results) -> None:
        weights = np.array([0.5, 0.5])
        port_vol = mock_results.portfolio_volatility(weights)
        assert len(port_vol) == mock_results.n_obs
        assert np.all(port_vol >= 0)
        assert np.all(np.isfinite(port_vol))
