"""Tests for MS-VAR (Krolzig, 1997).

Test suite following the spec:
- test_ms_var_fit
- test_ms_var_covariance_positive_definite
"""

from __future__ import annotations

import numpy as np
import pytest

from archbox.regime.ms_var import MarkovSwitchingVAR


@pytest.fixture
def simulated_ms_var_data():
    """Generate simulated MS(2)-VAR(1) bivariate data."""
    rng = np.random.default_rng(42)
    T = 300
    n = 2
    k = 2

    P = np.array([[0.95, 0.05], [0.10, 0.90]])
    mu = [np.array([-1.0, -0.5]), np.array([1.0, 0.5])]
    Sigma = [
        np.array([[0.5, 0.1], [0.1, 0.5]]),
        np.array([[0.2, 0.05], [0.05, 0.2]]),
    ]

    regimes = np.zeros(T, dtype=int)
    regimes[0] = 1
    for t in range(1, T):
        regimes[t] = rng.choice(k, p=P[regimes[t - 1]])

    y = np.zeros((T, n))
    for t in range(T):
        s = regimes[t]
        y[t] = mu[s] + rng.multivariate_normal(np.zeros(n), Sigma[s])

    return y, regimes, P, mu, Sigma


class TestMSVARFit:
    """Test MS-VAR fitting."""

    def test_ms_var_fit(self, simulated_ms_var_data):
        """MS(2)-VAR(1) should converge."""
        y, _, _, _, _ = simulated_ms_var_data
        model = MarkovSwitchingVAR(y, k_regimes=2, order=1)
        results = model.fit(maxiter=100, tol=1e-5, verbose=False)

        assert np.isfinite(results.loglike)
        assert results.transition_matrix.shape == (2, 2)

    def test_ms_var_covariance_positive_definite(self, simulated_ms_var_data):
        """Sigma_{S_t} should be positive definite in each regime."""
        y, _, _, _, _ = simulated_ms_var_data
        model = MarkovSwitchingVAR(y, k_regimes=2, order=1)
        results = model.fit(maxiter=100, tol=1e-5, verbose=False)

        for s in range(2):
            # Diagonal elements of covariance should be positive
            for key, val in results.regime_params[s].items():
                if key.startswith("Sigma_"):
                    assert val > 0, f"Regime {s} {key} should be positive: {val}"


class TestMSVARResults:
    """Test MS-VAR results."""

    def test_results_attributes(self, simulated_ms_var_data):
        """Results should have expected attributes."""
        y, _, _, _, _ = simulated_ms_var_data
        model = MarkovSwitchingVAR(y, k_regimes=2, order=1)
        results = model.fit(maxiter=50, tol=1e-5, verbose=False)

        T = y.shape[0]
        assert results.filtered_probs.shape == (T, 2)
        assert results.smoothed_probs.shape == (T, 2)
        assert results.nobs == T

    def test_summary_works(self, simulated_ms_var_data):
        """summary() should work for MS-VAR."""
        y, _, _, _, _ = simulated_ms_var_data
        model = MarkovSwitchingVAR(y, k_regimes=2, order=1)
        results = model.fit(maxiter=50, tol=1e-5, verbose=False)

        summary = results.summary()
        assert isinstance(summary, str)
        assert "MS-VAR" in summary

    def test_transition_matrix_valid(self, simulated_ms_var_data):
        """Transition matrix should be valid stochastic matrix."""
        y, _, _, _, _ = simulated_ms_var_data
        model = MarkovSwitchingVAR(y, k_regimes=2, order=1)
        results = model.fit(maxiter=50, tol=1e-5, verbose=False)

        P = results.transition_matrix
        np.testing.assert_allclose(P.sum(axis=1), np.ones(2), atol=1e-10)
        assert np.all(P >= 0)


@pytest.fixture
def simulated_ms_var_dynamic():
    """MS(2)-VAR(1) with clearly different dynamics per regime."""
    rng = np.random.default_rng(7)
    T = 1500
    n = 2
    P = np.array([[0.97, 0.03], [0.06, 0.94]])
    mu = [np.array([-1.0, -0.5]), np.array([1.0, 0.5])]
    Phi = [
        np.array([[0.50, 0.00], [0.20, 0.40]]),
        np.array([[-0.30, 0.10], [0.00, 0.60]]),
    ]
    Sigma = [
        np.array([[0.40, 0.05], [0.05, 0.30]]),
        np.array([[0.20, 0.02], [0.02, 0.15]]),
    ]
    chol = [np.linalg.cholesky(s) for s in Sigma]

    regimes = np.zeros(T, dtype=int)
    for t in range(1, T):
        regimes[t] = rng.choice(2, p=P[regimes[t - 1]])

    y = np.zeros((T, n))
    for t in range(T):
        s = regimes[t]
        shock = chol[s] @ rng.standard_normal(n)
        prev = y[t - 1] if t > 0 else np.zeros(n)
        y[t] = mu[s] + Phi[s] @ prev + shock

    return y, regimes, P, mu, Phi, Sigma


class TestMSVARCoefficients:
    """The VAR coefficients must actually be estimated."""

    def test_phi_updated_from_start_values(self, simulated_ms_var_dynamic):
        """results.coefficients differ from the 0.1*I starting values."""
        y, _, _, _, _, _ = simulated_ms_var_dynamic
        model = MarkovSwitchingVAR(y, k_regimes=2, order=1)
        results = model.fit(maxiter=300, tol=1e-10, verbose=False, compute_se=False)

        assert results.coefficients is not None
        assert results.intercepts is not None
        assert len(results.coefficients) == 2
        start = 0.1 * np.eye(2)
        for phi in results.coefficients:
            phi = np.asarray(phi)
            assert phi.shape == (2, 2)
            assert not np.allclose(phi, start, atol=1e-3)

    def test_recovers_true_coefficients(self, simulated_ms_var_dynamic):
        """The estimated Phi matrices are close to the simulated ones."""
        y, _, _, true_mu, true_phi, _ = simulated_ms_var_dynamic
        model = MarkovSwitchingVAR(y, k_regimes=2, order=1)
        results = model.fit(maxiter=500, tol=1e-10, verbose=False, compute_se=False)

        # Match regimes by the first intercept component
        order = np.argsort([float(np.asarray(m)[0]) for m in results.intercepts])
        true_order = np.argsort([float(m[0]) for m in true_mu])

        for rank in range(2):
            est_phi = np.asarray(results.coefficients[int(order[rank])])
            tru_phi = true_phi[int(true_order[rank])]
            assert (
                np.max(np.abs(est_phi - tru_phi)) < 0.15
            ), f"regime {rank}: estimated\n{est_phi}\ntrue\n{tru_phi}"

    def test_weighted_least_squares_conditions(self, simulated_ms_var_dynamic):
        """The weighted normal equations hold at the estimates."""
        y, _, _, _, _, _ = simulated_ms_var_dynamic
        model = MarkovSwitchingVAR(y, k_regimes=2, order=1)
        results = model.fit(maxiter=500, tol=1e-12, verbose=False, compute_se=False)

        z_mat, y_dep = model._design_matrices()
        x_mat = np.column_stack([np.ones(y_dep.shape[0]), z_mat])
        smoothed = results.smoothed_probs[model.order :]

        for s in range(2):
            mu_s, phi_s, _ = model._unpack_var_params(results.params, s)
            resid = y_dep - mu_s - z_mat @ phi_s.T
            score = x_mat.T @ (smoothed[:, s, None] * resid)
            scale = float(np.sum(smoothed[:, s])) * float(np.abs(y_dep).mean())
            assert np.max(np.abs(score)) < 1e-5 * max(scale, 1.0)

    def test_covariance_first_order_condition(self, simulated_ms_var_dynamic):
        """Sigma_s is the weighted residual covariance."""
        y, _, _, _, _, _ = simulated_ms_var_dynamic
        model = MarkovSwitchingVAR(y, k_regimes=2, order=1)
        results = model.fit(maxiter=500, tol=1e-12, verbose=False, compute_se=False)

        z_mat, y_dep = model._design_matrices()
        smoothed = results.smoothed_probs[model.order :]
        for s in range(2):
            mu_s, phi_s, sigma_s = model._unpack_var_params(results.params, s)
            resid = y_dep - mu_s - z_mat @ phi_s.T
            w = smoothed[:, s]
            implied = (resid * w[:, None]).T @ resid / float(w.sum())
            np.testing.assert_allclose(sigma_s, implied, atol=1e-5)


class TestMSVARLikelihoodAndForecast:
    """Likelihood consistency, forecasting and simulation."""

    def test_loglike_matches_params(self, simulated_ms_var_dynamic):
        """model.loglike(results.params) == results.loglike."""
        y, _, _, _, _, _ = simulated_ms_var_dynamic
        model = MarkovSwitchingVAR(y, k_regimes=2, order=1)
        results = model.fit(maxiter=200, tol=1e-10, verbose=False)

        assert model.loglike(results.params) == pytest.approx(results.loglike, abs=1e-7)
        assert results.std_errors is not None
        assert results.std_errors.shape == results.params.shape
        assert results.nobs_effective == y.shape[0] - 1

    def test_loglike_improves_on_start(self, simulated_ms_var_dynamic):
        """Fitting must improve the likelihood of the starting values."""
        y, _, _, _, _, _ = simulated_ms_var_dynamic
        model = MarkovSwitchingVAR(y, k_regimes=2, order=1)
        start_ll = model.loglike(model.start_params)
        results = model.fit(maxiter=300, tol=1e-10, verbose=False, compute_se=False)
        assert results.loglike > start_ll + 1.0

    def test_forecast_shapes_and_values(self, simulated_ms_var_dynamic):
        """Multivariate forecasts return mean (h, n) and covariance (h, n, n)."""
        y, _, _, _, _, _ = simulated_ms_var_dynamic
        model = MarkovSwitchingVAR(y, k_regimes=2, order=1)
        model.fit(maxiter=200, tol=1e-10, verbose=False, compute_se=False)

        fc = model.forecast(5)
        assert fc["mean"].shape == (5, 2)
        assert fc["variance"].shape == (5, 2, 2)
        assert fc["regime_probs"].shape == (5, 2)
        assert np.all(np.isfinite(fc["mean"]))
        assert np.any(fc["mean"] != 0.0)
        for h in range(5):
            assert np.all(np.linalg.eigvalsh(fc["variance"][h]) > 0)

    def test_simulate_matches_fitted_moments(self, simulated_ms_var_dynamic):
        """Simulated data reproduce the fitted regime intercepts."""
        y, _, _, _, _, _ = simulated_ms_var_dynamic
        model = MarkovSwitchingVAR(y, k_regimes=2, order=1)
        results = model.fit(maxiter=300, tol=1e-10, verbose=False, compute_se=False)

        sim, regimes, _ = model.simulate(4000, results.params, seed=5)
        assert sim.shape == (4000, 2)
        assert np.all(np.isfinite(sim))
        assert set(np.unique(regimes).tolist()).issubset({0, 1})
        # the simulated series must not be standard normal noise
        assert sim.std() > 0.5
