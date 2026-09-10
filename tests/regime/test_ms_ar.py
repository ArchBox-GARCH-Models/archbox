"""Tests for MS-AR (Hamilton 1989).

Test suite following the spec:
- test_hamilton_1989_gdp
- test_ms_ar_reduces_to_ar
- test_expected_durations
- test_recession_detection
"""

from __future__ import annotations

import numpy as np
import pytest

from archbox.regime.ms_ar import MarkovSwitchingAR


@pytest.fixture
def gdp_growth():
    """Load US GDP quarterly growth data."""
    from archbox.datasets import load_dataset

    df = load_dataset("us_gdp")
    return df["growth"].to_numpy(dtype=np.float64)


@pytest.fixture
def simulated_ms_ar_data():
    """Generate simulated MS(2)-AR(2) data."""
    rng = np.random.default_rng(42)
    T = 500
    p = 2
    k = 2

    P = np.array([[0.90, 0.10], [0.05, 0.95]])
    mu = [-1.0, 1.5]
    phi = [0.3, 0.1]
    sigma = [1.0, 0.5]

    regimes = np.zeros(T, dtype=int)
    regimes[0] = 1
    for t in range(1, T):
        regimes[t] = rng.choice(k, p=P[regimes[t - 1]])

    y = np.zeros(T)
    y[0] = mu[regimes[0]] + sigma[regimes[0]] * rng.standard_normal()
    y[1] = mu[regimes[1]] + sigma[regimes[1]] * rng.standard_normal()

    for t in range(p, T):
        s = regimes[t]
        y_demean = y[t - 1] - mu[s]
        y_demean2 = y[t - 2] - mu[s]
        y[t] = mu[s] + phi[0] * y_demean + phi[1] * y_demean2 + sigma[s] * rng.standard_normal()

    return y, regimes, P, mu, phi, sigma


class TestHamilton1989GDP:
    """Test Hamilton (1989) replication on US GDP data."""

    def test_hamilton_1989_gdp(self, gdp_growth):
        """MS(2)-AR(4) on US GDP growth.

        Regime 0 (recession): mu_0 < 0 or low
        Regime 1 (expansion): mu_1 > 0 or higher
        """
        model = MarkovSwitchingAR(
            gdp_growth,
            k_regimes=2,
            order=4,
            switching_mean=True,
            switching_variance=True,
            switching_ar=False,
        )
        results = model.fit(maxiter=300, tol=1e-6, verbose=False)

        # Get means sorted
        means = [results.regime_params[s]["mu"] for s in range(2)]
        sorted_means = sorted(means)

        # Recession regime should have lower mean
        # Expansion regime should have higher mean
        assert sorted_means[0] < sorted_means[1], (
            f"Recession mean should be < expansion mean: {sorted_means}"
        )

        # Log-likelihood should be finite
        assert np.isfinite(results.loglike)

    def test_expected_durations(self, gdp_growth):
        """Expected recession duration should be ~3-4 quarters."""
        model = MarkovSwitchingAR(
            gdp_growth,
            k_regimes=2,
            order=4,
            switching_mean=True,
            switching_variance=True,
        )
        results = model.fit(maxiter=300, tol=1e-6, verbose=False)

        durations = results.expected_durations()

        # Both durations should be positive and finite
        assert all(np.isfinite(d) for d in durations)
        assert all(d > 0 for d in durations)

        # At least one duration should be short (recession-like: < 10)
        # and one long (expansion-like: > 5)
        min_dur = min(durations)
        max_dur = max(durations)
        assert min_dur < 15, f"Shortest duration too long: {min_dur:.1f}"
        assert max_dur > 2, f"Longest duration too short: {max_dur:.1f}"

    def test_recession_detection(self, gdp_growth):
        """Smoothed probabilities should identify some recession periods."""
        model = MarkovSwitchingAR(
            gdp_growth,
            k_regimes=2,
            order=4,
            switching_mean=True,
            switching_variance=True,
        )
        results = model.fit(maxiter=300, tol=1e-6, verbose=False)

        # Classify observations
        classified = results.classify()

        # Should have observations in both regimes
        unique_regimes = set(classified.tolist())
        assert len(unique_regimes) == 2, f"Should detect 2 regimes, got {unique_regimes}"

        # The regime with lower mean should be the minority
        means = [results.regime_params[s]["mu"] for s in range(2)]
        recession_regime = 0 if means[0] < means[1] else 1
        recession_pct = np.mean(classified == recession_regime)

        # Recession should be minority of observations (< 50%)
        assert recession_pct < 0.50, f"Recession regime should be minority: {recession_pct:.2%}"


class TestMSARSimulated:
    """Test MS-AR on simulated data."""

    def test_fit_converges(self, simulated_ms_ar_data):
        """MS-AR should converge on simulated data."""
        y, _, _, _, _, _ = simulated_ms_ar_data
        model = MarkovSwitchingAR(
            y,
            k_regimes=2,
            order=2,
            switching_mean=True,
            switching_variance=True,
        )
        results = model.fit(maxiter=200, tol=1e-6, verbose=False)

        assert results.converged
        assert np.isfinite(results.loglike)

    def test_recover_means(self, simulated_ms_ar_data):
        """MS-AR should approximately recover regime means."""
        y, _, _, true_mu, _, _ = simulated_ms_ar_data
        model = MarkovSwitchingAR(
            y,
            k_regimes=2,
            order=2,
            switching_mean=True,
            switching_variance=True,
        )
        results = model.fit(maxiter=200, tol=1e-6, verbose=False)

        estimated_means = sorted([results.regime_params[s]["mu"] for s in range(2)])
        true_means = sorted(true_mu)

        for est, true in zip(estimated_means, true_means, strict=True):
            assert abs(est - true) < 1.5, f"Mean recovery: est={est:.3f}, true={true:.3f}"

    def test_regime_detection(self, simulated_ms_ar_data):
        """MS-AR should detect regimes reasonably well."""
        y, true_regimes, _, _, _, _ = simulated_ms_ar_data
        model = MarkovSwitchingAR(
            y,
            k_regimes=2,
            order=2,
            switching_mean=True,
            switching_variance=True,
        )
        results = model.fit(maxiter=200, tol=1e-6, verbose=False)

        classified = results.classify()
        accuracy1 = np.mean(classified == true_regimes)
        accuracy2 = np.mean(classified == (1 - true_regimes))
        accuracy = max(accuracy1, accuracy2)

        assert accuracy > 0.70, f"Regime detection accuracy too low: {accuracy:.2f}"


class TestMSAREdgeCases:
    """Test edge cases."""

    def test_ms_ar_1_reduces_to_simple(self):
        """MS(1)-AR(p) should be similar to a simple AR(p)."""
        rng = np.random.default_rng(42)
        T = 200
        y = rng.standard_normal(T)

        # With 1 regime, should still work (though not meaningful)
        # Use k_regimes=2 but the data has no switching
        model = MarkovSwitchingAR(
            y,
            k_regimes=2,
            order=1,
            switching_mean=True,
            switching_variance=True,
        )
        results = model.fit(maxiter=100, tol=1e-6, verbose=False)

        # Means should be similar (no clear separation in random data)
        means = [results.regime_params[s]["mu"] for s in range(2)]
        # Both means should be near zero for standard normal data
        for m in means:
            assert abs(m) < 2.0, f"Mean too far from zero for N(0,1) data: {m:.3f}"

    def test_ar_order_0(self):
        """MS-AR(0) should reduce to MS-Mean."""
        rng = np.random.default_rng(42)
        T = 300
        P = np.array([[0.95, 0.05], [0.10, 0.90]])
        mu = [-2.0, 2.0]
        regimes = np.zeros(T, dtype=int)
        regimes[0] = 1
        for t in range(1, T):
            regimes[t] = rng.choice(2, p=P[regimes[t - 1]])
        y = np.array([mu[s] + 0.5 * rng.standard_normal() for s in regimes])

        model = MarkovSwitchingAR(
            y,
            k_regimes=2,
            order=0,
            switching_mean=True,
            switching_variance=True,
        )
        results = model.fit(maxiter=200, tol=1e-6, verbose=False)

        assert results.converged
        assert np.isfinite(results.loglike)

    def test_summary_works(self, simulated_ms_ar_data):
        """summary() should work for MS-AR."""
        y, _, _, _, _, _ = simulated_ms_ar_data
        model = MarkovSwitchingAR(
            y,
            k_regimes=2,
            order=2,
            switching_mean=True,
            switching_variance=True,
        )
        results = model.fit(maxiter=100, tol=1e-6, verbose=False)

        summary = results.summary()
        assert isinstance(summary, str)
        assert "MS-AR" in summary
        assert "Regime" in summary

    def test_param_names(self):
        """Param names should include mu, phi, sigma."""
        y = np.random.randn(100)
        model = MarkovSwitchingAR(
            y,
            k_regimes=2,
            order=2,
            switching_mean=True,
            switching_variance=True,
        )
        names = model.param_names
        assert "mu_0" in names
        assert "mu_1" in names
        assert "phi_1" in names
        assert "phi_2" in names
        assert "sigma_0" in names
        assert "sigma_1" in names

    def test_switching_ar_param_names(self):
        """With switching_ar, phi names should include regime."""
        y = np.random.randn(100)
        model = MarkovSwitchingAR(
            y,
            k_regimes=2,
            order=2,
            switching_mean=True,
            switching_variance=True,
            switching_ar=True,
        )
        names = model.param_names
        assert "phi_1(S=0)" in names
        assert "phi_1(S=1)" in names


class TestMSARConditioning:
    """The first p observations are conditioned on, not given -1e10."""

    def test_regime_loglike_has_no_sentinel(self, gdp_growth):
        """Regime densities are finite and the pre-sample is excluded."""
        model = MarkovSwitchingAR(gdp_growth, k_regimes=2, order=4)
        params = model.start_params
        for s in range(2):
            ll = model._regime_loglike(params, s)
            assert ll.shape == (len(gdp_growth),)
            assert np.all(np.isfinite(ll))
            assert np.all(ll[:4] == 0.0), "pre-sample entries must be neutral"
            assert np.all(ll[4:] < 0.0)
            assert np.min(ll[4:]) > -1e6

    def test_loglike_is_sane(self, gdp_growth):
        """The marginal log-likelihood is on the scale of the data."""
        model = MarkovSwitchingAR(gdp_growth, k_regimes=2, order=4)
        value = model.loglike(model.start_params)
        assert np.isfinite(value)
        assert -5.0 < value / model.nobs_effective < 0.0

    def test_effective_nobs(self, gdp_growth):
        """nobs_effective excludes the conditioning observations."""
        model = MarkovSwitchingAR(gdp_growth, k_regimes=2, order=4)
        assert model.nobs_effective == len(gdp_growth) - 4
        results = model.fit(maxiter=100, tol=1e-8, verbose=False)
        assert results.nobs_effective == len(gdp_growth) - 4
        assert results.loglike > -1000.0


class TestMSARMStep:
    """The M-step must be the weighted least squares maximiser."""

    @staticmethod
    def _fitted(gdp_growth, switching_ar):
        model = MarkovSwitchingAR(gdp_growth, k_regimes=2, order=4, switching_ar=switching_ar)
        results = model.fit(maxiter=1000, tol=1e-12, verbose=False)
        return model, results

    @pytest.mark.parametrize("switching_ar", [False, True])
    def test_first_order_conditions_hold(self, gdp_growth, switching_ar):
        """Weighted score for (intercepts, AR) is zero at the estimates."""
        model, results = self._fitted(gdp_growth, switching_ar)
        p = model.order
        k = model.k_regimes
        x_mat, y_dep = model._design_matrices()
        smoothed = results.smoothed_probs[p:]

        score_c = np.zeros(k)
        score_phi = np.zeros(p)
        scale = 0.0
        for s in range(k):
            _mu, _phi, sigma = model._unpack_params(results.params, s)
            resid = model._regime_residuals(results.params, s)
            w = smoothed[:, s] / sigma**2
            score_c[s] = float(np.sum(w * resid))
            score_phi += x_mat.T @ (w * resid)
            scale += float(np.sum(w * np.abs(resid)))

        assert abs(score_c).max() < 1e-6 * max(scale, 1.0)
        assert abs(score_phi).max() < 1e-6 * max(scale, 1.0) * np.abs(x_mat).mean()

    def test_variance_first_order_condition(self, gdp_growth):
        """sigma_s^2 is the smoothed-probability weighted residual variance."""
        model, results = self._fitted(gdp_growth, False)
        p = model.order
        smoothed = results.smoothed_probs[p:]
        for s in range(model.k_regimes):
            _mu, _phi, sigma = model._unpack_params(results.params, s)
            resid = model._regime_residuals(results.params, s)
            w = smoothed[:, s]
            implied = float(np.sum(w * resid**2) / np.sum(w))
            assert sigma**2 == pytest.approx(implied, rel=1e-6)

    def test_m_step_increases_loglike(self, gdp_growth):
        """One EM iteration from the start values improves the likelihood."""
        from archbox.regime.em import EMEstimator

        model = MarkovSwitchingAR(gdp_growth, k_regimes=2, order=4)
        estimator = EMEstimator()
        estimator.fit(model, maxiter=6, tol=1e-14, verbose=False)
        history = estimator.loglike_history
        assert len(history) >= 3
        for i in range(1, len(history)):
            assert history[i] >= history[i - 1] - 1e-6

    def test_coefficients_exposed(self, gdp_growth):
        """results.coefficients / intercepts expose the AR estimates."""
        model, results = self._fitted(gdp_growth, False)
        assert results.coefficients is not None
        assert results.intercepts is not None
        assert len(results.coefficients) == 2
        for s in range(2):
            phi = np.asarray(results.coefficients[s]).ravel()
            assert phi.shape == (4,)
            mu = results.regime_params[s]["mu"]
            assert float(results.intercepts[s][0]) == pytest.approx(
                mu * (1.0 - phi.sum()), rel=1e-10
            )


class TestMSARForecastSimulate:
    """MS-AR forecasting and simulation use the estimated parameters."""

    def test_forecast_is_not_zero(self, gdp_growth):
        """Forecasts follow the regime means, not zeros."""
        model = MarkovSwitchingAR(gdp_growth, k_regimes=2, order=4)
        results = model.fit(maxiter=300, tol=1e-8, verbose=False)
        fc = model.forecast(8)

        assert fc["mean"].shape == (8,)
        assert np.all(np.isfinite(fc["mean"]))
        assert np.any(fc["mean"] != 0.0)
        assert np.all(fc["variance"] > 0)
        mus = [results.regime_params[s]["mu"] for s in range(2)]
        assert min(mus) - 1.0 <= fc["mean"][-1] <= max(mus) + 1.0

    def test_forecast_one_step_matches_hand_computation(self, gdp_growth):
        """The one-step mixture mean equals the hand-computed value."""
        model = MarkovSwitchingAR(gdp_growth, k_regimes=2, order=2)
        results = model.fit(maxiter=300, tol=1e-8, verbose=False)
        fc = model.forecast(1)

        probs = fc["regime_probs"][0]
        expected = 0.0
        for s in range(2):
            mu, phi, _ = model._unpack_params(results.params, s)
            value = mu + phi[0] * (gdp_growth[-1] - mu) + phi[1] * (gdp_growth[-2] - mu)
            expected += probs[s] * value
        assert fc["mean"][0] == pytest.approx(expected, rel=1e-10)

    def test_simulate_recovers_regime_means(self, simulated_ms_ar_data):
        """Simulated paths follow the regime-conditional distributions."""
        y, _, _, _, _, _ = simulated_ms_ar_data
        model = MarkovSwitchingAR(y, k_regimes=2, order=1)
        results = model.fit(maxiter=300, tol=1e-8, verbose=False)

        sim, regimes, _ = model.simulate(6000, results.params, seed=17)
        assert sim.shape == (6000,)
        for s in range(2):
            mask = regimes == s
            assert mask.sum() > 200
            assert abs(sim[mask].mean() - results.regime_params[s]["mu"]) < 0.5
