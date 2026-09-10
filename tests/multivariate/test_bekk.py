"""Tests for BEKK-GARCH model."""

from __future__ import annotations

import numpy as np
import pytest

from archbox.multivariate.bekk import BEKK
from archbox.multivariate.utils import is_positive_definite


class TestBEKKGARCH:
    """Test BEKK-GARCH model."""

    @pytest.fixture
    def bekk_returns(self, rng):
        """Generate returns suitable for BEKK (2 series, 300 obs)."""
        n, k = 300, 2
        R = np.array([[1.0, 0.5], [0.5, 1.0]])
        L = np.linalg.cholesky(R)
        z = rng.standard_normal((n, k))
        returns = (z @ L.T) * 0.01
        return returns

    def test_bekk_h_positive_definite(self, bekk_returns):
        """H_t should be positive definite for all t."""
        model = BEKK(bekk_returns, variant="diagonal")
        results = model.fit(disp=False)

        H_t = results.dynamic_covariance
        T = H_t.shape[0]

        for t in range(0, T, 30):
            assert is_positive_definite(H_t[t]), f"H_t not PD at t={t}"

    def test_bekk_covariance_symmetric(self, bekk_returns):
        """H_t should be symmetric for all t."""
        model = BEKK(bekk_returns, variant="diagonal")
        results = model.fit(disp=False)

        H_t = results.dynamic_covariance
        T = H_t.shape[0]

        for t in range(0, T, 30):
            np.testing.assert_array_almost_equal(
                H_t[t],
                H_t[t].T,
                decimal=10,
                err_msg=f"H_t not symmetric at t={t}",
            )

    def test_bekk_diagonal_fewer_params(self):
        """Diagonal BEKK should have fewer params than full BEKK."""
        k = 3
        returns = np.random.randn(200, k) * 0.01

        full_model = BEKK(returns, variant="full")
        diag_model = BEKK(returns, variant="diagonal")

        # Full: k(k+1)/2 + 2*k^2
        expected_full = k * (k + 1) // 2 + 2 * k * k
        # Diagonal: k(k+1)/2 + 2*k
        expected_diag = k * (k + 1) // 2 + 2 * k

        assert full_model.num_params == expected_full, (
            f"Full BEKK k={k}: expected {expected_full}, got {full_model.num_params}"
        )
        assert diag_model.num_params == expected_diag, (
            f"Diag BEKK k={k}: expected {expected_diag}, got {diag_model.num_params}"
        )
        assert diag_model.num_params < full_model.num_params

    def test_bekk_full_params_count(self):
        """Check parameter counts for various k."""
        for k, expected in [(2, 11), (3, 24), (5, 65)]:
            returns = np.random.randn(100, k) * 0.01
            model = BEKK(returns, variant="full")
            assert model.num_params == expected, (
                f"Full BEKK k={k}: expected {expected}, got {model.num_params}"
            )

    def test_bekk_diagonal_params_count(self):
        """Check diagonal parameter counts for various k."""
        for k, expected in [(2, 7), (3, 12), (5, 25)]:
            returns = np.random.randn(100, k) * 0.01
            model = BEKK(returns, variant="diagonal")
            assert model.num_params == expected, (
                f"Diag BEKK k={k}: expected {expected}, got {model.num_params}"
            )

    def test_bekk_loglike_finite(self, bekk_returns):
        """Log-likelihood should be finite."""
        model = BEKK(bekk_returns, variant="diagonal")
        results = model.fit(disp=False)

        assert np.isfinite(results.loglike)

    def test_bekk_summary(self, bekk_returns):
        """summary() should return a non-empty string."""
        model = BEKK(bekk_returns, variant="diagonal")
        results = model.fit(disp=False)
        s = results.summary()
        assert isinstance(s, str)
        assert "BEKK" in s
        assert len(s) > 50

    def test_bekk_forecast(self, bekk_returns):
        """Forecast should return correct shapes and converge."""
        model = BEKK(bekk_returns, variant="diagonal")
        results = model.fit(disp=False)

        fcast = model.forecast(results, horizon=50)
        k = bekk_returns.shape[1]

        assert fcast["covariance"].shape == (50, k, k)
        assert fcast["correlation"].shape == (50, k, k)

        # Check that forecasts are PD
        for h in range(50):
            assert is_positive_definite(fcast["covariance"][h]), f"Forecast not PD at h={h}"

    def test_bekk_forecast_converges(self, bekk_returns):
        """Long-horizon forecast should converge (successive H's become similar)."""
        model = BEKK(bekk_returns, variant="diagonal")
        results = model.fit(disp=False)

        fcast = model.forecast(results, horizon=200)

        # Check convergence: difference between successive forecasts should shrink
        diff_early = np.max(np.abs(fcast["covariance"][1] - fcast["covariance"][0]))
        diff_late = np.max(np.abs(fcast["covariance"][-1] - fcast["covariance"][-2]))

        assert diff_late < diff_early + 1e-10, "Forecast not converging"

    def test_bekk_invalid_variant(self, bekk_returns):
        """Invalid variant should raise ValueError."""
        with pytest.raises(ValueError, match="variant"):
            BEKK(bekk_returns, variant="invalid")

    def test_bekk_correlation_from_covariance(self, bekk_returns):
        """Derived R_t should have diagonal = 1 and elements in [-1, 1]."""
        model = BEKK(bekk_returns, variant="diagonal")
        results = model.fit(disp=False)

        R_t = results.dynamic_correlation
        T, k, _ = R_t.shape

        for t in range(0, T, 30):
            np.testing.assert_array_almost_equal(
                np.diag(R_t[t]),
                np.ones(k),
                decimal=4,
                err_msg=f"R_t diagonal not 1 at t={t}",
            )
            assert np.all(R_t[t] >= -1.0 - 0.01), f"R has elements < -1 at t={t}"
            assert np.all(R_t[t] <= 1.0 + 0.01), f"R has elements > 1 at t={t}"


class TestBEKKForecastRecursion:
    """The BEKK h=1 forecast must use eps_T eps_T'."""

    def test_forecast_one_step_uses_last_shock(self, bekk_sim_returns):
        """H_{T+1} = CC' + A' eps_T eps_T' A + B' H_T B."""
        model = BEKK(bekk_sim_returns, variant="diagonal")
        results = model.fit(disp=False)

        c_mat, a_mat, b_mat = model._unpack_params(results.params)
        eps_last = results.extras["resid_last"]
        expected = (
            c_mat @ c_mat.T
            + a_mat.T @ np.outer(eps_last, eps_last) @ a_mat
            + b_mat.T @ results.dynamic_covariance[-1] @ b_mat
        )

        fcast = model.forecast(results, horizon=3)
        np.testing.assert_allclose(fcast["covariance"][0], expected, rtol=1e-12)

    def test_forecast_one_step_differs_from_plain_h_substitution(self, bekk_sim_returns):
        """Substituting H_T for eps_T eps_T' at h=1 is the bug being guarded."""
        model = BEKK(bekk_sim_returns, variant="diagonal")
        results = model.fit(disp=False)

        c_mat, a_mat, b_mat = model._unpack_params(results.params)
        h_last = results.dynamic_covariance[-1]
        wrong = c_mat @ c_mat.T + a_mat.T @ h_last @ a_mat + b_mat.T @ h_last @ b_mat

        fcast = model.forecast(results, horizon=1)
        assert not np.allclose(fcast["covariance"][0], wrong, rtol=1e-6)

    def test_forecast_multistep_substitutes_expectation(self, bekk_sim_returns):
        """For h>1, E[eps eps'] = H_{T+h-1}."""
        model = BEKK(bekk_sim_returns, variant="diagonal")
        results = model.fit(disp=False)

        c_mat, a_mat, b_mat = model._unpack_params(results.params)
        fcast = model.forecast(results, horizon=3)
        h1 = fcast["covariance"][0]
        expected = c_mat @ c_mat.T + a_mat.T @ h1 @ a_mat + b_mat.T @ h1 @ b_mat
        np.testing.assert_allclose(fcast["covariance"][1], expected, rtol=1e-12)


class TestBEKKParameterCounting:
    """Mean parameters must enter AIC/BIC."""

    def test_information_criteria_count_mean_params(self, bekk_returns):
        """AIC/BIC count k mean parameters on top of the C/A/B block."""
        model = BEKK(bekk_returns, variant="diagonal")
        results = model.fit(disp=False)

        n_params = model.num_params + model.num_mean_params
        assert model.num_mean_params == bekk_returns.shape[1]
        assert results.aic == pytest.approx(-2.0 * results.loglike + 2.0 * n_params)
        assert results.bic == pytest.approx(-2.0 * results.loglike + np.log(model.T) * n_params)

    def test_num_params_excludes_the_mean(self, bekk_returns):
        """``num_params`` stays the covariance-parameter count (public contract)."""
        model = BEKK(bekk_returns, variant="diagonal")
        k = bekk_returns.shape[1]
        assert model.num_params == k * (k + 1) // 2 + 2 * k


class TestBEKKConstraints:
    """Bounds and stationarity constraints."""

    def test_stationarity_measure_diagonal(self):
        """For diagonal BEKK the measure is max_i (a_i^2 + b_i^2)."""
        a = np.diag([0.3, 0.2])
        b = np.diag([0.9, 0.8])
        expected = max(0.3**2 + 0.9**2, 0.2**2 + 0.8**2)
        assert BEKK.stationarity_measure(a, b) == pytest.approx(expected)

    def test_fitted_params_are_stationary(self, bekk_sim_returns):
        """The fitted BEKK must satisfy the stationarity constraint."""
        model = BEKK(bekk_sim_returns, variant="diagonal")
        results = model.fit(disp=False)
        _c, a_mat, b_mat = model._unpack_params(results.params)
        assert BEKK.stationarity_measure(a_mat, b_mat) < 1.0

    def test_c_diagonal_bounded_positive(self, bekk_returns):
        """C's diagonal is bounded strictly positive so C C' stays PD."""
        model = BEKK(bekk_returns, variant="diagonal")
        bounds = model._param_bounds()
        k = bekk_returns.shape[1]
        assert len(bounds) == model.num_params
        idx = 0
        for i in range(k):
            for j in range(i + 1):
                low, high = bounds[idx]
                if i == j:
                    assert low > 0.0, f"C[{i},{i}] lower bound must be positive"
                assert high > low
                idx += 1

    def test_fitted_params_within_bounds(self, bekk_sim_returns):
        """The optimizer must honour the box bounds."""
        model = BEKK(bekk_sim_returns, variant="diagonal")
        results = model.fit(disp=False)
        for value, (low, high) in zip(results.params, model._param_bounds(), strict=True):
            assert low - 1e-9 <= value <= high + 1e-9


class TestBEKKResults:
    """Standard errors and convergence reporting."""

    def test_standard_errors_finite_on_simulated_data(self, bekk_sim_returns):
        """A well-identified BEKK fit reports finite positive standard errors."""
        model = BEKK(bekk_sim_returns, variant="diagonal")
        results = model.fit(disp=False)
        assert results.converged
        assert results.std_errors.shape == results.params.shape
        assert np.all(np.isfinite(results.std_errors))
        assert np.all(results.std_errors > 0)

    def test_recovers_true_parameters(self, bekk_sim_returns):
        """Diagonal BEKK recovers the simulated A and B."""
        model = BEKK(bekk_sim_returns, variant="diagonal")
        results = model.fit(disp=False)
        _c, a_mat, b_mat = model._unpack_params(results.params)
        np.testing.assert_allclose(np.abs(np.diag(a_mat)), 0.25, atol=0.12)
        np.testing.assert_allclose(np.abs(np.diag(b_mat)), 0.90, atol=0.12)

    def test_summary_lists_named_parameters(self, bekk_returns):
        """summary() prints the C/A/B parameter names."""
        model = BEKK(bekk_returns, variant="diagonal")
        results = model.fit(disp=False)
        s = results.summary()
        assert "C[0,0]" in s
        assert "A[0,0]" in s
        assert "B[1,1]" in s
        assert "std err" in s

    def test_rejects_unknown_method(self, bekk_returns):
        """BEKK only supports full MLE."""
        model = BEKK(bekk_returns, variant="diagonal")
        with pytest.raises(ValueError, match="two_step|method"):
            model.fit(method="two_step", disp=False)
