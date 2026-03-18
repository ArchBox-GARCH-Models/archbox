"""Tests for GED (Generalized Error Distribution)."""

from __future__ import annotations

import numpy as np

from archbox.distributions.ged import GeneralizedError


class TestGED:
    """Test Generalized Error Distribution."""

    def test_ged_instantiation(self) -> None:
        dist = GeneralizedError()
        assert dist.name == "GED"
        assert dist.num_params == 1
        assert dist.param_names == ["nu"]

    def test_ged_fixed_nu(self) -> None:
        dist = GeneralizedError(nu=2.0)
        assert dist.num_params == 0

    def test_ged_lambda_computation(self) -> None:
        """Lambda should be well-defined for valid nu."""
        for nu in [0.5, 1.0, 1.5, 2.0, 3.0, 5.0]:
            lam = GeneralizedError._lambda_ged(nu)
            assert lam > 0, f"lambda must be > 0 for nu={nu}, got {lam}"
            assert np.isfinite(lam)

    def test_ged_nu2_equals_normal(self) -> None:
        """GED(nu=2) should produce same log-likelihood as Normal."""
        from archbox.distributions.normal import Normal

        rng = np.random.default_rng(42)
        z = rng.standard_normal(500)
        sigma2 = np.ones(500)

        dist_ged = GeneralizedError(nu=2.0)
        dist_normal = Normal()

        ll_ged = dist_ged.loglikelihood(z, sigma2)
        ll_normal = dist_normal.loglikelihood(z, sigma2)

        np.testing.assert_allclose(
            np.sum(ll_ged),
            np.sum(ll_normal),
            rtol=0.01,
            err_msg="GED(nu=2) should match Normal loglikelihood",
        )

    def test_ged_loglike_finite(self) -> None:
        rng = np.random.default_rng(42)
        z = rng.standard_normal(100)
        sigma2 = np.ones(100)
        dist = GeneralizedError(nu=1.5)
        ll = dist.loglikelihood(z, sigma2)
        assert np.all(np.isfinite(ll))

    def test_ged_simulate(self) -> None:
        dist = GeneralizedError(nu=1.5)
        rng = np.random.default_rng(42)
        z = dist.simulate(10000, rng)
        assert len(z) == 10000
        assert np.all(np.isfinite(z))

    def test_ged_transform_roundtrip(self) -> None:
        dist = GeneralizedError()
        params = np.array([1.5])
        constrained = dist.transform_params(params)
        unconstrained = dist.untransform_params(constrained)
        roundtrip = dist.transform_params(unconstrained)
        np.testing.assert_allclose(constrained, roundtrip, rtol=1e-6)

    def test_ged_transform_ensures_positive(self) -> None:
        dist = GeneralizedError()
        for x in [-5.0, -1.0, 0.0, 1.0, 5.0]:
            constrained = dist.transform_params(np.array([x]))
            assert constrained[0] > 0, f"nu must be > 0, got {constrained[0]}"

    def test_ged_heavy_tails(self) -> None:
        """GED with nu < 2 should have heavier tails than Normal."""
        rng = np.random.default_rng(42)
        # Generate heavy-tailed data
        z = rng.standard_t(3, size=1000) / np.sqrt(3.0)
        sigma2 = np.ones(1000)

        dist_ged = GeneralizedError(nu=1.0)  # Laplace - heavy tails
        dist_normal = GeneralizedError(nu=2.0)  # Normal

        ll_ged = np.sum(dist_ged.loglikelihood(z, sigma2))
        ll_normal = np.sum(dist_normal.loglikelihood(z, sigma2))

        assert ll_ged > ll_normal, "GED(nu=1) should fit heavy-tailed data better"
