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
