"""Tests for Student-t distribution."""

from __future__ import annotations

import numpy as np
from scipy.stats import t as scipy_t

from archbox.distributions.student_t import StudentT


class TestStudentT:
    """Test Student-t distribution."""

    def test_student_t_instantiation(self) -> None:
        dist = StudentT()
        assert dist.name == "Student-t"
        assert dist.num_params == 1
        assert dist.param_names == ["nu"]

    def test_student_t_fixed_nu(self) -> None:
        dist = StudentT(nu=5.0)
        assert dist.num_params == 0
        assert dist.param_names == []

    def test_student_t_loglike_matches_scipy(self) -> None:
        """Log-likelihood should match scipy.stats.t."""
        rng = np.random.default_rng(42)
        nu = 5.0
        sigma2 = np.full(100, 1.0)
        z = rng.standard_t(nu, size=100) / np.sqrt(nu / (nu - 2))
        resids = z * np.sqrt(sigma2)

        dist = StudentT(nu=nu)
        ll_archbox = dist.loglikelihood(resids, sigma2)

        # scipy.stats.t logpdf for standardized t (variance = 1)
        scale = np.sqrt((nu - 2) / nu)
        ll_scipy = scipy_t.logpdf(z, df=nu, scale=scale)

        np.testing.assert_allclose(
            ll_archbox,
            ll_scipy,
            atol=0.1,
            err_msg="Student-t loglike should approximately match scipy.stats.t",
        )

    def test_student_t_heavier_tails(self) -> None:
        """Student-t with small nu should give higher loglike for fat-tailed data."""
        rng = np.random.default_rng(42)
        z = rng.standard_t(4, size=1000) / np.sqrt(4 / 2)
        sigma2 = np.ones(1000)

        dist_t = StudentT(nu=4.0)
        dist_normal_approx = StudentT(nu=100.0)

        ll_t = np.sum(dist_t.loglikelihood(z, sigma2))
        ll_normal_approx = np.sum(dist_normal_approx.loglikelihood(z, sigma2))

        assert (
            ll_t > ll_normal_approx
        ), "Student-t(nu=4) should fit fat-tailed data better than near-Normal"

    def test_student_t_simulate(self) -> None:
        dist = StudentT(nu=5.0)
        rng = np.random.default_rng(42)
        z = dist.simulate(10000, rng)
        assert len(z) == 10000
        assert abs(np.mean(z)) < 0.1
        assert abs(np.var(z) - 1.0) < 0.2

    def test_student_t_transform_roundtrip(self) -> None:
        dist = StudentT()
        params = np.array([8.0])
        constrained = dist.transform_params(params)
        unconstrained = dist.untransform_params(constrained)
        roundtrip = dist.transform_params(unconstrained)
        np.testing.assert_allclose(constrained, roundtrip, rtol=1e-6)

    def test_student_t_transform_ensures_nu_gt_2(self) -> None:
        dist = StudentT()
        for x in [-10.0, -1.0, 0.0, 1.0, 10.0]:
            constrained = dist.transform_params(np.array([x]))
            assert constrained[0] > 2.0, f"nu must be > 2, got {constrained[0]}"

    def test_student_t_start_params(self) -> None:
        dist = StudentT()
        sp = dist.start_params()
        assert len(sp) == 1
        assert sp[0] > 2.0
