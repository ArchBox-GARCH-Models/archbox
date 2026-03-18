"""Tests for Mixture Normal distribution."""

from __future__ import annotations

import numpy as np

from archbox.distributions.mixture_normal import MixtureNormal


class TestMixtureNormal:
    """Test Mixture Normal distribution."""

    def test_mixture_normal_instantiation(self) -> None:
        dist = MixtureNormal()
        assert dist.name == "Mixture Normal"
        assert dist.num_params == 2
        assert dist.param_names == ["p", "sigma1"]

    def test_mixture_normal_fixed_params(self) -> None:
        dist = MixtureNormal(p=0.5, sigma1=0.5)
        assert dist.num_params == 0

    def test_mixture_unit_variance(self) -> None:
        """p * sigma1^2 + (1-p) * sigma2^2 == 1 always."""
        for p in [0.1, 0.3, 0.5, 0.7, 0.9]:
            for sigma1 in [0.3, 0.5, 0.8, 1.0]:
                sigma2 = MixtureNormal._compute_sigma2(p, sigma1)
                if sigma2 > 0:
                    total_var = p * sigma1**2 + (1 - p) * sigma2**2
                    np.testing.assert_allclose(
                        total_var,
                        1.0,
                        rtol=1e-10,
                        err_msg=f"Unit variance violated for p={p}, sigma1={sigma1}",
                    )

    def test_mixture_loglike_finite(self) -> None:
        rng = np.random.default_rng(42)
        z = rng.standard_normal(100)
        sigma2 = np.ones(100)
        dist = MixtureNormal(p=0.5, sigma1=0.5)
        ll = dist.loglikelihood(z, sigma2)
        assert np.all(np.isfinite(ll))

    def test_mixture_simulate(self) -> None:
        dist = MixtureNormal(p=0.5, sigma1=0.5)
        rng = np.random.default_rng(42)
        z = dist.simulate(10000, rng)
        assert len(z) == 10000
        assert np.all(np.isfinite(z))
        # Should have approximately unit variance
        assert abs(np.var(z) - 1.0) < 0.1, f"Variance should be ~1, got {np.var(z)}"

    def test_mixture_simulate_unit_variance(self) -> None:
        """Simulated samples should have unit variance."""
        for p in [0.3, 0.5, 0.7]:
            dist = MixtureNormal(p=p, sigma1=0.5)
            rng = np.random.default_rng(42)
            z = dist.simulate(50000, rng)
            assert abs(np.var(z) - 1.0) < 0.1, (
                f"Simulated variance should be ~1 for p={p}, got {np.var(z)}"
            )

    def test_mixture_transform_roundtrip(self) -> None:
        dist = MixtureNormal()
        params = dist.start_params()
        constrained = dist.transform_params(params)
        unconstrained = dist.untransform_params(constrained)
        roundtrip = dist.transform_params(unconstrained)
        np.testing.assert_allclose(constrained, roundtrip, rtol=1e-6)

    def test_mixture_transform_ensures_bounds(self) -> None:
        dist = MixtureNormal()
        for x1, x2 in [(-5.0, -5.0), (0.0, 0.0), (5.0, 5.0)]:
            constrained = dist.transform_params(np.array([x1, x2]))
            assert 0 < constrained[0] < 1, f"p must be in (0,1), got {constrained[0]}"
            assert constrained[1] > 0, f"sigma1 must be > 0, got {constrained[1]}"

    def test_mixture_sigma2_computation(self) -> None:
        """sigma2 should be computed correctly from constraint."""
        p = 0.3
        sigma1 = 0.5
        sigma2 = MixtureNormal._compute_sigma2(p, sigma1)
        expected = np.sqrt((1 - p * sigma1**2) / (1 - p))
        np.testing.assert_allclose(sigma2, expected, rtol=1e-10)
