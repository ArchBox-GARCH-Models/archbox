"""Tests for portfolio utilities."""

from __future__ import annotations

import numpy as np

from archbox.multivariate.portfolio import (
    marginal_risk_contribution,
    minimum_variance_weights,
    minimum_variance_weights_dynamic,
    portfolio_variance,
    portfolio_volatility,
    risk_contribution,
    risk_decomposition,
)


class TestPortfolioVariance:
    """Test portfolio variance computation."""

    def test_portfolio_variance_basic(self):
        """w' H w should match manual calculation."""
        H = np.array([[0.04, 0.01], [0.01, 0.09]])
        w = np.array([0.6, 0.4])
        H_t = H.reshape(1, 2, 2)

        pv = portfolio_variance(w, H_t)
        expected = w @ H @ w

        np.testing.assert_almost_equal(pv[0], expected, decimal=10)

    def test_portfolio_variance_equal_weight(self):
        """Equal weight portfolio variance check."""
        k = 3
        H = np.eye(k) * 0.01  # Diagonal covariance
        w = np.ones(k) / k
        H_t = H.reshape(1, k, k)

        pv = portfolio_variance(w, H_t)
        expected = 0.01 / k  # For diagonal cov with equal weights

        np.testing.assert_almost_equal(pv[0], expected, decimal=10)

    def test_portfolio_variance_positive(self):
        """Portfolio variance should be non-negative."""
        rng = np.random.default_rng(42)
        k = 4
        A = rng.standard_normal((k, k))
        H = A @ A.T + np.eye(k) * 0.01  # Ensure PD
        w = rng.dirichlet(np.ones(k))
        H_t = np.stack([H] * 100)

        pv = portfolio_variance(w, H_t)
        assert np.all(pv >= 0)

    def test_portfolio_volatility(self):
        """Portfolio volatility = sqrt(variance)."""
        H = np.array([[0.04, 0.01], [0.01, 0.09]])
        w = np.array([0.6, 0.4])
        H_t = H.reshape(1, 2, 2)

        pvar = portfolio_variance(w, H_t)
        pvol = portfolio_volatility(w, H_t)

        np.testing.assert_almost_equal(pvol[0], np.sqrt(pvar[0]), decimal=10)


class TestMinimumVariancePortfolio:
    """Test minimum variance portfolio weights."""

    def test_mv_weights_sum_to_one(self):
        """MV portfolio weights should sum to 1."""
        H = np.array([[0.04, 0.01], [0.01, 0.09]])
        w = minimum_variance_weights(H)
        np.testing.assert_almost_equal(np.sum(w), 1.0, decimal=10)

    def test_mv_weights_minimize_variance(self):
        """MV portfolio should have lower variance than equal weight."""
        H = np.array(
            [
                [0.04, 0.02, 0.01],
                [0.02, 0.09, 0.03],
                [0.01, 0.03, 0.16],
            ]
        )

        w_mv = minimum_variance_weights(H)
        w_eq = np.ones(3) / 3

        var_mv = float(w_mv @ H @ w_mv)
        var_eq = float(w_eq @ H @ w_eq)

        assert (
            var_mv <= var_eq + 1e-10
        ), f"MV variance ({var_mv:.6f}) should be <= equal weight ({var_eq:.6f})"

    def test_mv_weights_dynamic_shape(self):
        """Dynamic MV weights should have correct shape."""
        T, k = 100, 3
        H_t = np.zeros((T, k, k))
        for t in range(T):
            H_t[t] = np.eye(k) * (0.01 + 0.001 * t)

        weights = minimum_variance_weights_dynamic(H_t)
        assert weights.shape == (T, k)

        # Each row should sum to 1
        for t in range(T):
            np.testing.assert_almost_equal(
                np.sum(weights[t]),
                1.0,
                decimal=10,
            )

    def test_mv_diagonal_covariance(self):
        """For diagonal cov, MV weights proportional to 1/variance."""
        variances = np.array([0.04, 0.09, 0.16])
        H = np.diag(variances)

        w = minimum_variance_weights(H)

        # Weights should be proportional to 1/var
        inv_var = 1.0 / variances
        expected = inv_var / np.sum(inv_var)

        np.testing.assert_array_almost_equal(w, expected, decimal=8)


class TestRiskDecomposition:
    """Test risk decomposition."""

    def test_risk_contributions_sum_to_total(self):
        """sum(RC_i) should equal sigma_p (Euler decomposition)."""
        H = np.array(
            [
                [0.04, 0.02, 0.01],
                [0.02, 0.09, 0.03],
                [0.01, 0.03, 0.16],
            ]
        )
        w = np.array([0.4, 0.3, 0.3])

        sigma_p = np.sqrt(float(w @ H @ w))
        rc = risk_contribution(w, H)

        np.testing.assert_almost_equal(
            np.sum(rc),
            sigma_p,
            decimal=10,
            err_msg="Risk contributions don't sum to total risk",
        )

    def test_pct_contributions_sum_to_one(self):
        """Percentage contributions should sum to 1."""
        H = np.array([[0.04, 0.01], [0.01, 0.09]])
        w = np.array([0.6, 0.4])

        decomp = risk_decomposition(w, H)

        np.testing.assert_almost_equal(
            np.sum(decomp["pct_contribution"]),
            1.0,
            decimal=10,
        )

    def test_marginal_contribution_shape(self):
        """Marginal contribution should have shape (k,)."""
        k = 4
        H = np.eye(k) * 0.01
        w = np.ones(k) / k

        mc = marginal_risk_contribution(w, H)
        assert mc.shape == (k,)

    def test_risk_decomposition_keys(self):
        """risk_decomposition should return all expected keys."""
        H = np.eye(3) * 0.01
        w = np.ones(3) / 3

        decomp = risk_decomposition(w, H)

        expected_keys = {
            "weights",
            "portfolio_volatility",
            "marginal_contribution",
            "risk_contribution",
            "pct_contribution",
        }
        assert set(decomp.keys()) == expected_keys


class TestPortfolioIntegration:
    """Integration tests with multivariate models."""

    def test_portfolio_with_ccc(self, synthetic_returns):
        """Portfolio utilities should work with CCC results."""
        from archbox.multivariate.ccc import CCC

        model = CCC(synthetic_returns)
        results = model.fit(disp=False)

        k = synthetic_returns.shape[1]
        w = np.ones(k) / k

        # Portfolio volatility from results
        pvol = results.portfolio_volatility(w)
        assert pvol.shape == (synthetic_returns.shape[0],)
        assert np.all(pvol >= 0)
        assert np.all(np.isfinite(pvol))

        # MV weights from last H_t
        H_last = results.dynamic_covariance[-1]
        w_mv = minimum_variance_weights(H_last)
        np.testing.assert_almost_equal(np.sum(w_mv), 1.0, decimal=10)

        # Risk decomposition
        decomp = risk_decomposition(w, H_last)
        sigma_p = np.sqrt(float(w @ H_last @ w))
        np.testing.assert_almost_equal(
            np.sum(decomp["risk_contribution"]),
            sigma_p,
            decimal=8,
        )

    def test_portfolio_with_dcc(self, synthetic_returns):
        """Portfolio utilities should work with DCC results."""
        from archbox.multivariate.dcc import DCC

        model = DCC(synthetic_returns)
        results = model.fit(disp=False)

        k = synthetic_returns.shape[1]
        w = np.ones(k) / k

        pvol = results.portfolio_volatility(w)
        assert np.all(pvol >= 0)
        assert np.all(np.isfinite(pvol))

    def test_all_models_end_to_end(self, synthetic_returns):
        """All multivariate models should work end-to-end."""
        from archbox.multivariate import CCC, DCC, DECO, GOGARCH

        models = {
            "CCC": CCC(synthetic_returns),
            "DCC": DCC(synthetic_returns),
            "DECO": DECO(synthetic_returns),
            "GOGARCH": GOGARCH(synthetic_returns),
        }

        k = synthetic_returns.shape[1]
        w = np.ones(k) / k

        for name, model in models.items():
            results = model.fit(disp=False)

            # Basic checks
            assert results.dynamic_covariance.shape[1:] == (k, k), f"{name} H_t shape"
            assert results.dynamic_correlation.shape[1:] == (k, k), f"{name} R_t shape"
            assert np.isfinite(results.loglike), f"{name} loglike"

            # Portfolio vol
            pvol = results.portfolio_volatility(w)
            assert np.all(pvol >= 0), f"{name} portfolio vol negative"
            assert np.all(np.isfinite(pvol)), f"{name} portfolio vol not finite"

            # Summary
            s = results.summary()
            assert len(s) > 50, f"{name} summary too short"

            # Forecast
            fcast = model.forecast(results, horizon=5)
            assert fcast["covariance"].shape == (5, k, k), f"{name} forecast shape"

    def test_bekk_end_to_end(self, rng):
        """BEKK should work end-to-end (separate test, needs 2 series)."""
        from archbox.multivariate import BEKK

        n, k = 300, 2
        R = np.array([[1.0, 0.5], [0.5, 1.0]])
        L = np.linalg.cholesky(R)
        returns = (rng.standard_normal((n, k)) @ L.T) * 0.01

        model = BEKK(returns, variant="diagonal")
        results = model.fit(disp=False)

        w = np.ones(k) / k
        pvol = results.portfolio_volatility(w)
        assert np.all(pvol >= 0)
        assert np.isfinite(results.loglike)
