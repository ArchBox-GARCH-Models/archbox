"""Tests for Normal distribution."""

from __future__ import annotations

import numpy as np
import pytest
from scipy import stats

from archbox.distributions.normal import Normal


class TestNormal:
    """Test Normal distribution implementation."""

    @pytest.fixture
    def dist(self) -> Normal:
        return Normal()

    def test_name(self, dist: Normal):
        assert dist.name == "Normal"

    def test_num_params(self, dist: Normal):
        assert dist.num_params == 0

    def test_param_names_empty(self, dist: Normal):
        assert dist.param_names == []

    def test_start_params_empty(self, dist: Normal):
        sp = dist.start_params()
        assert len(sp) == 0

    def test_bounds_empty(self, dist: Normal):
        assert dist.bounds() == []

    def test_loglikelihood_matches_scipy(self, dist: Normal, rng):
        """Log-likelihood must match scipy.stats.norm.logpdf."""
        resids = rng.standard_normal(500)
        sigma2 = np.abs(rng.standard_normal(500)) + 0.5

        ll_archbox = dist.loglikelihood(resids, sigma2)
        ll_scipy = stats.norm.logpdf(resids, loc=0, scale=np.sqrt(sigma2))

        np.testing.assert_allclose(ll_archbox, ll_scipy, rtol=1e-10)

    def test_loglikelihood_shape(self, dist: Normal, rng):
        resids = rng.standard_normal(100)
        sigma2 = np.ones(100)
        ll = dist.loglikelihood(resids, sigma2)
        assert ll.shape == (100,)

    def test_loglikelihood_unit_variance(self, dist: Normal, rng):
        """With sigma2=1, should match standard normal logpdf."""
        resids = rng.standard_normal(1000)
        sigma2 = np.ones(1000)
        ll = dist.loglikelihood(resids, sigma2)
        expected = stats.norm.logpdf(resids)
        np.testing.assert_allclose(ll, expected, rtol=1e-10)

    def test_ppf_standard_quantiles(self, dist: Normal):
        """Test well-known quantiles."""
        assert abs(dist.ppf(0.5) - 0.0) < 1e-10
        assert abs(dist.ppf(0.025) - (-1.96)) < 0.01
        assert abs(dist.ppf(0.05) - (-1.645)) < 0.01
        assert abs(dist.ppf(0.975) - 1.96) < 0.01

    def test_cdf_standard_values(self, dist: Normal):
        assert abs(dist.cdf(0.0) - 0.5) < 1e-10
        assert dist.cdf(-10.0) < 1e-10
        assert dist.cdf(10.0) > 1.0 - 1e-10

    def test_cdf_ppf_inverse(self, dist: Normal):
        """CDF and PPF should be inverses."""
        for q in [0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99]:
            x = dist.ppf(q)
            q_back = dist.cdf(x)
            assert abs(q_back - q) < 1e-10

    def test_simulate_shape(self, dist: Normal):
        rng = np.random.default_rng(42)
        z = dist.simulate(1000, rng)
        assert z.shape == (1000,)

    def test_simulate_moments(self, dist: Normal):
        """Simulated values should have mean~0, std~1."""
        rng = np.random.default_rng(42)
        z = dist.simulate(100000, rng)
        assert abs(np.mean(z)) < 0.02
        assert abs(np.std(z) - 1.0) < 0.02
