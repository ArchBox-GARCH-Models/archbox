"""Tests for Skewed Student-t distribution."""

from __future__ import annotations

import numpy as np

from archbox.distributions.skewed_t import SkewedT
from archbox.distributions.student_t import StudentT


class TestSkewedT:
    """Test Skewed Student-t distribution."""

    def test_skewed_t_instantiation(self) -> None:
        dist = SkewedT()
        assert dist.name == "Skewed Student-t"
        assert dist.num_params == 2
        assert dist.param_names == ["nu", "lambda"]

    def test_skewed_t_fixed_params(self) -> None:
        dist = SkewedT(nu=5.0, lam=-0.1)
        assert dist.num_params == 0

    def test_skewed_t_abc_computation(self) -> None:
        """Test Hansen's a, b, c constants."""
        nu, lam = 5.0, -0.1
        a, b, c = SkewedT._compute_abc(nu, lam)
        assert np.isfinite(a)
        assert b > 0
        assert c > 0
        # When lambda=0, a should be 0 and b should be 1
        a0, b0, c0 = SkewedT._compute_abc(5.0, 0.0)
        np.testing.assert_allclose(a0, 0.0, atol=1e-10)
        np.testing.assert_allclose(b0, 1.0, atol=1e-10)

    def test_skewed_t_loglike_finite(self) -> None:
        rng = np.random.default_rng(42)
        z = rng.standard_normal(100)
        sigma2 = np.ones(100)
        dist = SkewedT(nu=5.0, lam=-0.1)
        ll = dist.loglikelihood(z, sigma2)
        assert np.all(np.isfinite(ll))

    def test_skewed_t_asymmetry(self) -> None:
        """Lambda != 0 should capture asymmetry."""
        rng = np.random.default_rng(42)
        z = rng.standard_normal(1000)
        z[z < 0] *= 1.5  # make negatives larger
        sigma2 = np.ones(1000)

        dist_skew = SkewedT(nu=8.0, lam=-0.3)
        dist_symm = SkewedT(nu=8.0, lam=0.0)

        ll_skew = np.sum(dist_skew.loglikelihood(z, sigma2))
        ll_symm = np.sum(dist_symm.loglikelihood(z, sigma2))

        assert ll_skew > ll_symm, "Skewed-t should fit skewed data better"

    def test_skewed_t_simulate(self) -> None:
        dist = SkewedT(nu=5.0, lam=-0.1)
        rng = np.random.default_rng(42)
        z = dist.simulate(10000, rng)
        assert len(z) == 10000
        assert np.all(np.isfinite(z))

    def test_skewed_t_transform_roundtrip(self) -> None:
        dist = SkewedT()
        params = dist.start_params()
        constrained = dist.transform_params(params)
        unconstrained = dist.untransform_params(constrained)
        roundtrip = dist.transform_params(unconstrained)
        np.testing.assert_allclose(constrained, roundtrip, rtol=1e-6)

    def test_skewed_t_transform_ensures_bounds(self) -> None:
        dist = SkewedT()
        for x1, x2 in [(-5.0, -5.0), (0.0, 0.0), (5.0, 5.0)]:
            constrained = dist.transform_params(np.array([x1, x2]))
            assert constrained[0] > 2.0, f"nu must be > 2, got {constrained[0]}"
            assert -1.0 < constrained[1] < 1.0, f"lambda must be in (-1,1), got {constrained[1]}"

    def test_skewed_t_reduces_to_symmetric(self) -> None:
        """When lambda=0, Skewed-t should match Student-t loglikelihood."""
        rng = np.random.default_rng(42)
        z = rng.standard_normal(200)
        sigma2 = np.ones(200)
        nu = 8.0

        dist_skew = SkewedT(nu=nu, lam=0.0)
        dist_t = StudentT(nu=nu)

        ll_skew = dist_skew.loglikelihood(z, sigma2)
        ll_t = dist_t.loglikelihood(z, sigma2)

        np.testing.assert_allclose(
            np.sum(ll_skew),
            np.sum(ll_t),
            rtol=0.05,
            err_msg="Skewed-t(lambda=0) should approximate Student-t",
        )
