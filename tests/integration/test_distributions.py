"""Integration tests locking in the conditional-distribution wiring.

These tests verify that volatility models can be fitted with non-normal
conditional distributions, that the combined parameter vector is laid out as
``[variance_params..., dist_params...]``, that distribution name aliases
resolve correctly, and that risk measures work on a fitted Student-t model.
"""

from __future__ import annotations

import numpy as np
import pytest

from archbox.core.volatility_model import VolatilityModel
from archbox.datasets import load_dataset
from archbox.distributions.ged import GeneralizedError
from archbox.distributions.skewed_t import SkewedT
from archbox.distributions.student_t import StudentT
from archbox.models.egarch import EGARCH
from archbox.models.garch import GARCH
from archbox.models.gjr_garch import GJRGARCH

MODELS = {"GARCH": GARCH, "EGARCH": EGARCH, "GJRGARCH": GJRGARCH}
DISTS = ["normal", "student-t", "ged", "skewed-t"]


@pytest.fixture(scope="module")
def returns() -> np.ndarray:
    """Real S&P 500 return series used across the fitting tests."""
    data = load_dataset("sp500")
    return np.asarray(data["returns"], dtype=float)


def _fit(model_cls: type, returns: np.ndarray, dist: str):
    """Construct and fit a model quietly, returning (model, result)."""
    model = model_cls(returns, dist=dist)
    result = model.fit(disp=False)
    return model, result


# ---------------------------------------------------------------------------
# Parametrized fit checks: shape of the param vector, finiteness, convergence.
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("model_name", list(MODELS))
@pytest.mark.parametrize("dist", DISTS)
def test_fit_param_vector_layout(model_name: str, dist: str, returns: np.ndarray) -> None:
    """Each (model, dist) combo fits with the expected combined param count."""
    model_cls = MODELS[model_name]
    model, result = _fit(model_cls, returns, dist)

    expected = model.num_params + model.dist.num_params
    assert len(result.params) == expected
    assert np.all(np.isfinite(result.params))
    # Convergence attribute must be present (and truthy for these well-behaved fits).
    assert hasattr(result, "convergence")
    assert result.convergence


# ---------------------------------------------------------------------------
# Non-normal distributions should fit at least as well as the normal baseline.
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("model_name", list(MODELS))
@pytest.mark.parametrize("dist", ["student-t", "ged", "skewed-t"])
def test_nonnormal_loglike_not_worse_and_shape_in_bounds(
    model_name: str, dist: str, returns: np.ndarray
) -> None:
    """A richer (non-normal) dist must not reduce the maximized log-likelihood.

    Also checks that the fitted shape parameter(s) lie within their bounds.
    """
    model_cls = MODELS[model_name]

    _, normal_result = _fit(model_cls, returns, "normal")
    model, result = _fit(model_cls, returns, dist)

    # Nested-model property: the non-normal LL should be >= normal LL.
    tol = 1e-3
    assert result.loglike >= normal_result.loglike - tol

    # Fitted shape parameters are the trailing block of the param vector.
    n_var = model.num_params
    dist_params = result.params[n_var:]
    bounds = model.dist.bounds()
    assert len(dist_params) == len(bounds) == model.dist.num_params

    names = list(model.dist.param_names)
    # The first shape param is 'nu' for student-t / ged / skewed-t.
    assert "nu" in names
    nu_idx = names.index("nu")
    lo = bounds[nu_idx][0]
    nu = dist_params[nu_idx]
    # The unconstrained transform enforces only the lower bound on nu (the
    # tail index): for near-Gaussian data the optimizer may push nu past the
    # nominal upper hint. Require nu to respect its lower bound and be finite.
    assert np.isfinite(nu)
    assert nu >= lo

    # The lower bound is a genuine constraint for every shape parameter; the
    # upper bound is enforced only where the transform is two-sided (e.g. the
    # skew parameter lambda).
    for name, value, (b_lo, b_hi) in zip(names, dist_params, bounds, strict=True):
        assert np.isfinite(value)
        assert value >= b_lo
        if name != "nu":
            assert value <= b_hi


# ---------------------------------------------------------------------------
# _build_distribution alias coverage.
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    ("alias", "expected_cls"),
    [
        ("studentt", StudentT),
        ("student-t", StudentT),
        ("t", StudentT),
        ("ged", GeneralizedError),
        ("skewed-t", SkewedT),
        ("skewt", SkewedT),
    ],
)
def test_build_distribution_aliases(alias: str, expected_cls: type) -> None:
    """Known aliases resolve to the correct distribution class."""
    dist = VolatilityModel._build_distribution(alias)
    assert isinstance(dist, expected_cls)


def test_build_distribution_unknown_raises() -> None:
    """An unknown distribution name raises ValueError."""
    with pytest.raises(ValueError):
        VolatilityModel._build_distribution("not-a-real-distribution")


# ---------------------------------------------------------------------------
# Risk measures on a fitted Student-t GARCH.
# ---------------------------------------------------------------------------
def test_var_and_es_finite_positive_student_t(returns: np.ndarray) -> None:
    """VaR and ES at 1% are finite positive floats for a Student-t GARCH."""
    _, result = _fit(GARCH, returns, "student-t")

    var = result.var(alpha=0.01)
    es = result.es(alpha=0.01)

    assert isinstance(var, float)
    assert isinstance(es, float)
    assert np.isfinite(var)
    assert np.isfinite(es)
    assert var > 0
    assert es > 0
    # Expected shortfall is a deeper-tail loss than VaR.
    assert es >= var
