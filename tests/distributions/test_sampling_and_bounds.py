"""Cross-distribution tests: sampling fidelity, vectorization and bound consistency.

Every distribution here is standardized: draws must have mean 0 and variance 1,
their empirical CDF must agree with the analytic ``cdf``, ``ppf``/``cdf`` must
accept arrays, and ``transform_params`` must land strictly inside the interval
declared by ``bounds()`` (which is also where the likelihood clamps).
"""

from __future__ import annotations

import numpy as np
import pytest

from archbox.distributions.ged import GeneralizedError
from archbox.distributions.mixture_normal import MixtureNormal
from archbox.distributions.normal import Normal
from archbox.distributions.skewed_t import SkewedT
from archbox.distributions.student_t import StudentT

N_DRAWS = 200_000


def _fixed_instances() -> list:
    """Distributions with every shape parameter pinned (so cdf/ppf are usable)."""
    return [
        Normal(),
        StudentT(nu=5.0),
        StudentT(nu=30.0),
        GeneralizedError(nu=1.2),
        GeneralizedError(nu=2.0),
        SkewedT(nu=5.0, lam=-0.5),
        SkewedT(nu=8.0, lam=0.3),
        SkewedT(nu=15.0, lam=0.0),
        MixtureNormal(p=0.5, sigma1=0.5),
        MixtureNormal(p=0.9, sigma1=0.1),
    ]


def _free_instances() -> list:
    """Distributions with free shape parameters."""
    return [StudentT(), GeneralizedError(), SkewedT(), MixtureNormal()]


class TestSimulateMatchesDensity:
    """Draws must follow the very density used by loglikelihood/cdf."""

    @pytest.mark.parametrize("dist", _fixed_instances())
    def test_standardized_moments(self, dist) -> None:
        z = dist.simulate(N_DRAWS, np.random.default_rng(0))
        assert abs(float(np.mean(z))) < 0.03, f"{dist.name}: mean {np.mean(z)}"
        assert abs(float(np.var(z)) - 1.0) < 0.08, f"{dist.name}: var {np.var(z)}"

    @pytest.mark.parametrize("dist", _fixed_instances())
    def test_empirical_cdf_matches_analytic(self, dist) -> None:
        z = dist.simulate(N_DRAWS, np.random.default_rng(1))
        for x in (-1.5, -0.5, 0.0, 0.5, 1.5):
            empirical = float(np.mean(z < x))
            analytic = float(dist.cdf(x))
            msg = f"{dist.name}: CDF({x}) empirical {empirical:.4f} vs analytic {analytic:.4f}"
            assert abs(empirical - analytic) < 0.01, msg

    def test_skewed_t_is_asymmetric_in_the_right_direction(self) -> None:
        """Negative lambda gives a left-skewed sample, positive lambda a right-skewed one.

        The draws are standardized (mean 0, variance 1), so the sign of the
        third moment is the skewness, and a left-skewed law has its median
        above its mean: ``P(Z < 0) < 1/2`` when lambda < 0.
        """
        left = SkewedT(nu=6.0, lam=-0.5).simulate(N_DRAWS, np.random.default_rng(2))
        symmetric = SkewedT(nu=6.0, lam=0.0).simulate(N_DRAWS, np.random.default_rng(2))
        right = SkewedT(nu=6.0, lam=0.5).simulate(N_DRAWS, np.random.default_rng(2))

        assert float(np.mean(left**3)) < -0.5
        assert abs(float(np.mean(symmetric**3))) < 0.1
        assert float(np.mean(right**3)) > 0.5

        assert float(np.mean(left < 0)) < 0.5
        assert float(np.mean(right < 0)) > 0.5
        assert float(np.mean(left < 0)) == pytest.approx(
            float(SkewedT(nu=6.0, lam=-0.5).cdf(0.0)), abs=0.01
        )

    def test_skewed_t_symmetric_case_matches_student_t(self) -> None:
        skew = SkewedT(nu=6.0, lam=0.0)
        student = StudentT(nu=6.0)
        for q in (0.01, 0.1, 0.5, 0.9, 0.99):
            assert skew.ppf(q) == pytest.approx(student.ppf(q), abs=1e-8)


class TestPpfCdfRoundTrip:
    """ppf and cdf are inverses, including deep in the tails."""

    @pytest.mark.parametrize("dist", _fixed_instances())
    @pytest.mark.parametrize("q", [1e-6, 1e-4, 0.01, 0.5, 0.99, 1 - 1e-4, 1 - 1e-6])
    def test_roundtrip(self, dist, q: float) -> None:
        x = dist.ppf(q)
        assert np.isfinite(x)
        assert float(dist.cdf(x)) == pytest.approx(q, rel=1e-4, abs=1e-9)

    def test_skewed_t_small_nu_extreme_quantiles(self) -> None:
        """The old fixed [-50, 50] brentq bracket could not reach these."""
        dist = SkewedT(nu=2.05, lam=-0.9)
        low = dist.ppf(1e-8)
        high = dist.ppf(1 - 1e-8)
        assert np.isfinite(low) and low < -50.0
        assert np.isfinite(high) and high > 0.0

    def test_mixture_normal_extreme_quantiles(self) -> None:
        dist = MixtureNormal(p=0.99, sigma1=0.05)
        low = dist.ppf(1e-8)
        assert np.isfinite(low)
        assert float(dist.cdf(low)) == pytest.approx(1e-8, rel=1e-3)

    def test_mixture_normal_rejects_invalid_quantile(self) -> None:
        with pytest.raises(ValueError, match="q must be in"):
            MixtureNormal(p=0.5, sigma1=0.5).ppf(0.0)


class TestVectorization:
    """cdf/ppf accept scalars and arrays alike."""

    @pytest.mark.parametrize("dist", _fixed_instances())
    def test_cdf_array(self, dist) -> None:
        x = np.array([-2.0, 0.0, 1.0])
        values = dist.cdf(x)
        assert isinstance(values, np.ndarray)
        assert values.shape == x.shape
        for xi, vi in zip(x, values, strict=True):
            assert float(dist.cdf(float(xi))) == pytest.approx(float(vi))

    @pytest.mark.parametrize("dist", _fixed_instances())
    def test_ppf_array(self, dist) -> None:
        q = np.array([0.05, 0.5, 0.95])
        values = dist.ppf(q)
        assert isinstance(values, np.ndarray)
        assert values.shape == q.shape
        for qi, vi in zip(q, values, strict=True):
            assert float(dist.ppf(float(qi))) == pytest.approx(float(vi))

    @pytest.mark.parametrize("dist", _fixed_instances())
    def test_scalar_returns_float(self, dist) -> None:
        assert isinstance(dist.cdf(0.0), float)
        assert isinstance(dist.ppf(0.5), float)

    def test_single_element_array_is_indexable(self) -> None:
        dist = SkewedT(nu=5.0, lam=-0.5)
        assert float(dist.cdf(np.array([0.0]))[0]) == pytest.approx(float(dist.cdf(0.0)))


class TestTransformsRespectBounds:
    """The transform maps onto the interior of the declared bounds."""

    @pytest.mark.parametrize("dist", _free_instances())
    @pytest.mark.parametrize("x", [-1e3, -50.0, -5.0, 0.0, 5.0, 50.0, 1e3])
    def test_transform_inside_bounds(self, dist, x: float) -> None:
        bounds = dist.bounds()
        constrained = dist.transform_params(np.full(len(bounds), x))
        for value, (lo, hi) in zip(constrained, bounds, strict=True):
            assert lo <= value <= hi, f"{dist.name}: {value} outside [{lo}, {hi}]"

    @pytest.mark.parametrize("dist", _free_instances())
    def test_transform_roundtrip(self, dist) -> None:
        start = dist.start_params()
        unconstrained = dist.untransform_params(start)
        np.testing.assert_allclose(dist.transform_params(unconstrained), start, rtol=1e-8)

    def test_student_t_clamp_matches_bounds(self) -> None:
        dist = StudentT()
        (lo, hi) = dist.bounds()[0]
        assert dist._get_nu(np.array([1.0])) == pytest.approx(lo)
        assert dist._get_nu(np.array([1e6])) == pytest.approx(hi)

    def test_ged_clamp_matches_bounds(self) -> None:
        dist = GeneralizedError()
        (lo, hi) = dist.bounds()[0]
        assert dist._get_nu(np.array([0.0])) == pytest.approx(lo)
        assert dist._get_nu(np.array([1e6])) == pytest.approx(hi)

    def test_skewed_t_clamp_matches_bounds(self) -> None:
        dist = SkewedT()
        (nu_lo, nu_hi), (lam_lo, lam_hi) = dist.bounds()
        nu, lam = dist._get_nu_lam(np.array([1.0, -5.0]))
        assert nu == pytest.approx(nu_lo)
        assert lam == pytest.approx(lam_lo)
        nu, lam = dist._get_nu_lam(np.array([1e6, 5.0]))
        assert nu == pytest.approx(nu_hi)
        assert lam == pytest.approx(lam_hi)

    def test_mixture_clamp_matches_bounds(self) -> None:
        dist = MixtureNormal()
        (p_lo, p_hi), (s_lo, s_hi) = dist.bounds()
        p, sigma1 = dist._get_p_sigma1(np.array([0.0, 0.0]))
        assert p == pytest.approx(p_lo)
        assert sigma1 == pytest.approx(s_lo)
        p, sigma1 = dist._get_p_sigma1(np.array([1.0, 100.0]))
        assert p == pytest.approx(p_hi)
        assert sigma1 == pytest.approx(s_hi)


class TestModelsAcceptDistributionInstances:
    """`dist=` takes a name or a ready-made Distribution."""

    def test_instance_is_used_as_is(self) -> None:
        from archbox.models.garch import GARCH

        rng = np.random.default_rng(0)
        returns = rng.standard_normal(400) * 0.01

        fixed = StudentT(nu=5.0)
        model = GARCH(returns, p=1, q=1, dist=fixed)

        assert model.dist is fixed
        assert model.dist.num_params == 0
        assert model.full_param_names() == ["omega", "alpha[1]", "beta[1]"]

        results = model.fit(disp=False)
        assert len(results.params) == 3
        assert np.isfinite(results.loglike)

    def test_string_and_equivalent_instance_agree(self) -> None:
        from archbox.models.garch import GARCH

        rng = np.random.default_rng(1)
        returns = rng.standard_normal(300) * 0.01
        params = np.array([1e-6, 0.08, 0.90, 6.0])

        by_name = GARCH(returns, p=1, q=1, dist="studentt")
        by_instance = GARCH(returns, p=1, q=1, dist=StudentT())
        assert by_name.loglike(params) == pytest.approx(by_instance.loglike(params))

    def test_unknown_name_still_raises(self) -> None:
        from archbox.core.volatility_model import VolatilityModel

        with pytest.raises(ValueError, match="Unknown distribution"):
            VolatilityModel._build_distribution("not-a-distribution")
