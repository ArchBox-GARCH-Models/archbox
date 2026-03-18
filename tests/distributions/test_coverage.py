"""Coverage tests for distributions: ged.py, skewed_t.py, mixture_normal.py."""

from __future__ import annotations

import numpy as np
import pytest
from numpy.typing import NDArray

from archbox.distributions.ged import GeneralizedError
from archbox.distributions.mixture_normal import MixtureNormal
from archbox.distributions.skewed_t import SkewedT


# ============================================================
# Tests for GeneralizedError (GED) - uncovered paths
# ============================================================


class TestGEDCoverage:
    """Tests for GED methods not covered by existing tests."""

    def test_ppf_below_half(self) -> None:
        dist = GeneralizedError(nu=2.0)
        x = dist.ppf(0.1)
        assert np.isfinite(x)
        assert x < 0.0

    def test_ppf_above_half(self) -> None:
        dist = GeneralizedError(nu=2.0)
        x = dist.ppf(0.9)
        assert np.isfinite(x)
        assert x > 0.0

    def test_ppf_at_half(self) -> None:
        dist = GeneralizedError(nu=2.0)
        x = dist.ppf(0.5)
        assert x == 0.0

    def test_cdf_positive(self) -> None:
        dist = GeneralizedError(nu=2.0)
        p = dist.cdf(1.0)
        assert 0.5 < p < 1.0

    def test_cdf_negative(self) -> None:
        dist = GeneralizedError(nu=2.0)
        p = dist.cdf(-1.0)
        assert 0.0 < p < 0.5

    def test_cdf_zero(self) -> None:
        dist = GeneralizedError(nu=2.0)
        p = dist.cdf(0.0)
        assert p == pytest.approx(0.5, abs=1e-6)

    def test_ppf_cdf_roundtrip(self) -> None:
        dist = GeneralizedError(nu=1.5)
        for q in [0.05, 0.25, 0.5, 0.75, 0.95]:
            x = dist.ppf(q)
            q_recovered = dist.cdf(x)
            assert q_recovered == pytest.approx(q, abs=0.01)

    def test_loglikelihood_with_dist_params(self) -> None:
        dist = GeneralizedError()  # nu not fixed
        rng = np.random.default_rng(42)
        resids = rng.standard_normal(50)
        sigma2 = np.ones(50)
        ll = dist.loglikelihood(resids, sigma2, dist_params=np.array([2.0]))
        assert np.all(np.isfinite(ll))

    def test_loglikelihood_no_params_uses_default(self) -> None:
        dist = GeneralizedError()
        rng = np.random.default_rng(42)
        resids = rng.standard_normal(50)
        sigma2 = np.ones(50)
        ll = dist.loglikelihood(resids, sigma2)
        assert np.all(np.isfinite(ll))

    def test_simulate_with_dist_params(self) -> None:
        dist = GeneralizedError()
        rng = np.random.default_rng(42)
        z = dist.simulate(100, rng, dist_params=np.array([1.0]))
        assert len(z) == 100
        assert np.all(np.isfinite(z))

    def test_start_params_unfixed(self) -> None:
        dist = GeneralizedError()
        sp = dist.start_params()
        assert len(sp) == 1

    def test_start_params_fixed(self) -> None:
        dist = GeneralizedError(nu=2.0)
        sp = dist.start_params()
        assert len(sp) == 0

    def test_bounds_unfixed(self) -> None:
        dist = GeneralizedError()
        b = dist.bounds()
        assert len(b) == 1
        assert b[0][0] > 0

    def test_bounds_fixed(self) -> None:
        dist = GeneralizedError(nu=2.0)
        b = dist.bounds()
        assert len(b) == 0

    def test_transform_empty(self) -> None:
        dist = GeneralizedError(nu=2.0)
        result = dist.transform_params(np.array([]))
        assert len(result) == 0

    def test_untransform_empty(self) -> None:
        dist = GeneralizedError(nu=2.0)
        result = dist.untransform_params(np.array([]))
        assert len(result) == 0

    def test_untransform_params(self) -> None:
        dist = GeneralizedError()
        constrained = np.array([1.5])
        unconstrained = dist.untransform_params(constrained)
        assert len(unconstrained) == 1
        assert np.isfinite(unconstrained[0])


# ============================================================
# Tests for SkewedT - uncovered paths
# ============================================================


class TestSkewedTCoverage:
    """Tests for SkewedT uncovered methods."""

    def test_cdf_below_threshold(self) -> None:
        dist = SkewedT(nu=8.0, lam=-0.2)
        p = dist.cdf(-5.0)
        assert 0.0 < p < 0.5

    def test_cdf_above_threshold(self) -> None:
        dist = SkewedT(nu=8.0, lam=-0.2)
        p = dist.cdf(5.0)
        assert 0.5 < p < 1.0

    def test_ppf(self) -> None:
        dist = SkewedT(nu=8.0, lam=-0.2)
        x = dist.ppf(0.05)
        assert np.isfinite(x)
        assert x < 0.0

    def test_ppf_cdf_roundtrip(self) -> None:
        dist = SkewedT(nu=8.0, lam=-0.1)
        for q in [0.05, 0.25, 0.5, 0.75, 0.95]:
            x = dist.ppf(q)
            q_recovered = dist.cdf(x)
            assert q_recovered == pytest.approx(q, abs=0.01)

    def test_loglikelihood_both_regimes(self) -> None:
        """Ensure both sides of the threshold are hit."""
        dist = SkewedT(nu=8.0, lam=-0.3)
        rng = np.random.default_rng(42)
        resids = rng.standard_normal(200) * 2  # wide range to cover both sides
        sigma2 = np.ones(200)
        ll = dist.loglikelihood(resids, sigma2)
        assert np.all(np.isfinite(ll))

    def test_get_nu_lam_defaults(self) -> None:
        dist = SkewedT()  # both free
        nu, lam = dist._get_nu_lam()
        assert nu == 8.0
        assert lam == 0.0

    def test_get_nu_lam_from_params(self) -> None:
        dist = SkewedT()
        nu, lam = dist._get_nu_lam(np.array([5.0, -0.3]))
        assert nu == 5.0
        assert lam == pytest.approx(-0.3)

    def test_get_nu_lam_fixed_nu(self) -> None:
        dist = SkewedT(nu=10.0)
        nu, lam = dist._get_nu_lam(np.array([-0.2]))
        assert nu == 10.0
        assert lam == pytest.approx(-0.2)

    def test_get_nu_lam_fixed_lam(self) -> None:
        dist = SkewedT(lam=-0.1)
        nu, lam = dist._get_nu_lam(np.array([6.0]))
        assert nu == 6.0
        assert lam == -0.1

    def test_compute_abc(self) -> None:
        a, b, c = SkewedT._compute_abc(8.0, -0.2)
        assert np.isfinite(a)
        assert b > 0
        assert c > 0

    def test_simulate(self) -> None:
        dist = SkewedT(nu=8.0, lam=-0.2)
        rng = np.random.default_rng(42)
        z = dist.simulate(1000, rng)
        assert len(z) == 1000
        assert np.all(np.isfinite(z))

    def test_simulate_with_params(self) -> None:
        dist = SkewedT()
        rng = np.random.default_rng(42)
        z = dist.simulate(100, rng, dist_params=np.array([6.0, -0.3]))
        assert len(z) == 100

    def test_transform_roundtrip(self) -> None:
        dist = SkewedT()
        params = np.array([8.0, -0.2])
        unconstrained = dist.untransform_params(params)
        recovered = dist.transform_params(unconstrained)
        np.testing.assert_allclose(recovered, params, atol=1e-4)

    def test_transform_empty(self) -> None:
        dist = SkewedT(nu=8.0, lam=-0.2)
        result = dist.transform_params(np.array([]))
        assert len(result) == 0

    def test_untransform_empty(self) -> None:
        dist = SkewedT(nu=8.0, lam=-0.2)
        result = dist.untransform_params(np.array([]))
        assert len(result) == 0

    def test_transform_fixed_nu(self) -> None:
        dist = SkewedT(nu=8.0)
        params = np.array([-0.2])
        unconstrained = dist.untransform_params(params)
        recovered = dist.transform_params(unconstrained)
        np.testing.assert_allclose(recovered, params, atol=1e-4)

    def test_transform_fixed_lam(self) -> None:
        dist = SkewedT(lam=-0.1)
        params = np.array([8.0])
        unconstrained = dist.untransform_params(params)
        recovered = dist.transform_params(unconstrained)
        np.testing.assert_allclose(recovered, params, atol=1e-4)

    def test_bounds(self) -> None:
        dist = SkewedT()
        b = dist.bounds()
        assert len(b) == 2

    def test_bounds_fixed_nu(self) -> None:
        dist = SkewedT(nu=8.0)
        b = dist.bounds()
        assert len(b) == 1

    def test_bounds_both_fixed(self) -> None:
        dist = SkewedT(nu=8.0, lam=-0.1)
        b = dist.bounds()
        assert len(b) == 0

    def test_num_params(self) -> None:
        assert SkewedT().num_params == 2
        assert SkewedT(nu=8.0).num_params == 1
        assert SkewedT(lam=-0.1).num_params == 1
        assert SkewedT(nu=8.0, lam=-0.1).num_params == 0

    def test_param_names(self) -> None:
        assert SkewedT().param_names == ["nu", "lambda"]
        assert SkewedT(nu=8.0).param_names == ["lambda"]
        assert SkewedT(lam=-0.1).param_names == ["nu"]
        assert SkewedT(nu=8.0, lam=-0.1).param_names == []

    def test_start_params(self) -> None:
        sp = SkewedT().start_params()
        assert len(sp) == 2

    def test_start_params_fixed(self) -> None:
        sp = SkewedT(nu=8.0, lam=-0.1).start_params()
        assert len(sp) == 0


# ============================================================
# Tests for MixtureNormal - uncovered paths
# ============================================================


class TestMixtureNormalCoverage:
    """Tests for MixtureNormal uncovered methods."""

    def test_cdf(self) -> None:
        dist = MixtureNormal(p=0.5, sigma1=0.5)
        p = dist.cdf(0.0)
        assert p == pytest.approx(0.5, abs=0.01)

    def test_cdf_tails(self) -> None:
        dist = MixtureNormal(p=0.5, sigma1=0.5)
        assert dist.cdf(-10.0) < 0.01
        assert dist.cdf(10.0) > 0.99

    def test_ppf(self) -> None:
        dist = MixtureNormal(p=0.5, sigma1=0.5)
        x = dist.ppf(0.05)
        assert np.isfinite(x)
        assert x < 0.0

    def test_ppf_cdf_roundtrip(self) -> None:
        dist = MixtureNormal(p=0.5, sigma1=0.5)
        for q in [0.05, 0.25, 0.5, 0.75, 0.95]:
            x = dist.ppf(q)
            q_recovered = dist.cdf(x)
            assert q_recovered == pytest.approx(q, abs=0.01)

    def test_loglikelihood(self) -> None:
        dist = MixtureNormal(p=0.5, sigma1=0.5)
        rng = np.random.default_rng(42)
        resids = rng.standard_normal(100)
        sigma2 = np.ones(100)
        ll = dist.loglikelihood(resids, sigma2)
        assert np.all(np.isfinite(ll))

    def test_loglikelihood_with_dist_params(self) -> None:
        dist = MixtureNormal()
        rng = np.random.default_rng(42)
        resids = rng.standard_normal(100)
        sigma2 = np.ones(100)
        ll = dist.loglikelihood(resids, sigma2, dist_params=np.array([0.5, 0.5]))
        assert np.all(np.isfinite(ll))

    def test_simulate(self) -> None:
        dist = MixtureNormal(p=0.5, sigma1=0.5)
        rng = np.random.default_rng(42)
        z = dist.simulate(1000, rng)
        assert len(z) == 1000
        assert np.all(np.isfinite(z))

    def test_simulate_with_params(self) -> None:
        dist = MixtureNormal()
        rng = np.random.default_rng(42)
        z = dist.simulate(100, rng, dist_params=np.array([0.3, 0.4]))
        assert len(z) == 100

    def test_compute_sigma2_fallback(self) -> None:
        """When numerator <= 0, should return 1.0."""
        sigma2 = MixtureNormal._compute_sigma2(0.5, 2.0)
        assert sigma2 == 1.0

    def test_get_p_sigma1_defaults(self) -> None:
        dist = MixtureNormal()
        p, s1 = dist._get_p_sigma1()
        assert p == 0.5
        assert s1 == 0.5

    def test_get_p_sigma1_from_params(self) -> None:
        dist = MixtureNormal()
        p, s1 = dist._get_p_sigma1(np.array([0.3, 0.7]))
        assert p == pytest.approx(0.3)
        assert s1 == pytest.approx(0.7)

    def test_get_p_sigma1_fixed_p(self) -> None:
        dist = MixtureNormal(p=0.4)
        p, s1 = dist._get_p_sigma1(np.array([0.6]))
        assert p == pytest.approx(0.4)
        assert s1 == pytest.approx(0.6)

    def test_get_p_sigma1_fixed_sigma1(self) -> None:
        dist = MixtureNormal(sigma1=0.3)
        p, s1 = dist._get_p_sigma1(np.array([0.6]))
        assert p == pytest.approx(0.6)
        assert s1 == pytest.approx(0.3)

    def test_transform_roundtrip(self) -> None:
        dist = MixtureNormal()
        params = np.array([0.5, 0.5])
        unconstrained = dist.untransform_params(params)
        recovered = dist.transform_params(unconstrained)
        np.testing.assert_allclose(recovered, params, atol=1e-4)

    def test_transform_empty(self) -> None:
        dist = MixtureNormal(p=0.5, sigma1=0.5)
        result = dist.transform_params(np.array([]))
        assert len(result) == 0

    def test_untransform_empty(self) -> None:
        dist = MixtureNormal(p=0.5, sigma1=0.5)
        result = dist.untransform_params(np.array([]))
        assert len(result) == 0

    def test_transform_fixed_p(self) -> None:
        dist = MixtureNormal(p=0.5)
        params = np.array([0.5])
        unconstrained = dist.untransform_params(params)
        recovered = dist.transform_params(unconstrained)
        np.testing.assert_allclose(recovered, params, atol=1e-4)

    def test_transform_fixed_sigma1(self) -> None:
        dist = MixtureNormal(sigma1=0.5)
        params = np.array([0.5])
        unconstrained = dist.untransform_params(params)
        recovered = dist.transform_params(unconstrained)
        np.testing.assert_allclose(recovered, params, atol=1e-4)

    def test_bounds(self) -> None:
        assert len(MixtureNormal().bounds()) == 2
        assert len(MixtureNormal(p=0.5).bounds()) == 1
        assert len(MixtureNormal(sigma1=0.5).bounds()) == 1
        assert len(MixtureNormal(p=0.5, sigma1=0.5).bounds()) == 0

    def test_num_params(self) -> None:
        assert MixtureNormal().num_params == 2
        assert MixtureNormal(p=0.5).num_params == 1
        assert MixtureNormal(sigma1=0.5).num_params == 1
        assert MixtureNormal(p=0.5, sigma1=0.5).num_params == 0

    def test_param_names(self) -> None:
        assert MixtureNormal().param_names == ["p", "sigma1"]
        assert MixtureNormal(p=0.5).param_names == ["sigma1"]
        assert MixtureNormal(sigma1=0.5).param_names == ["p"]
        assert MixtureNormal(p=0.5, sigma1=0.5).param_names == []

    def test_start_params(self) -> None:
        sp = MixtureNormal().start_params()
        assert len(sp) == 2

    def test_start_params_fixed(self) -> None:
        sp = MixtureNormal(p=0.5, sigma1=0.5).start_params()
        assert len(sp) == 0
