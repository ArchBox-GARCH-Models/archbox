"""Tests for archbox.utils.validation helpers."""

from __future__ import annotations

import numpy as np
import pytest

from archbox import APARCH, EGARCH, GARCH, GARCHM, GJRGARCH
from archbox.utils.validation import (
    validate_positive_integer,
    validate_realized_variance,
    validate_returns,
)


class TestValidatePositiveInteger:
    """validate_positive_integer accepts ints and numpy ints, rejects bools."""

    def test_accepts_python_int(self):
        assert validate_positive_integer(3, "p") == 3

    @pytest.mark.parametrize(
        "value",
        [np.int8(2), np.int16(2), np.int32(2), np.int64(2), np.uint8(2)],
    )
    def test_accepts_numpy_integers(self, value):
        """numpy ints are integers; the old isinstance(val, int) check rejected them."""
        result = validate_positive_integer(value, "q")
        assert result == 2
        assert isinstance(result, int)
        assert not isinstance(result, np.integer)

    @pytest.mark.parametrize("value", [True, False, np.bool_(True)])
    def test_rejects_booleans(self, value):
        """bool subclasses int in Python but is never a valid lag order."""
        with pytest.raises(ValueError, match="positive integer"):
            validate_positive_integer(value, "p")

    @pytest.mark.parametrize("value", [0, -1, np.int64(0), np.int64(-5)])
    def test_rejects_non_positive(self, value):
        with pytest.raises(ValueError, match="positive integer"):
            validate_positive_integer(value, "p")

    @pytest.mark.parametrize("value", [1.5, 2.0, "3", None, np.float64(2.0)])
    def test_rejects_non_integers(self, value):
        with pytest.raises(ValueError, match="positive integer"):
            validate_positive_integer(value, "p")

    def test_error_message_names_the_parameter(self):
        with pytest.raises(ValueError, match="truncation_lag"):
            validate_positive_integer(0, "truncation_lag")


class TestModelConstructorValidation:
    """Every model constructor routes p/q through validate_positive_integer."""

    @pytest.fixture
    def returns(self, rng: np.random.Generator) -> np.ndarray:
        return rng.standard_normal(300) * 0.01

    MODELS = [GARCH, EGARCH, GJRGARCH, APARCH, GARCHM]

    @pytest.mark.parametrize("model_cls", MODELS)
    @pytest.mark.parametrize(("p", "q"), [(0, 1), (1, 0), (-1, 1), (1, -2)])
    def test_rejects_non_positive_orders(self, model_cls, returns, p, q):
        with pytest.raises(ValueError, match="positive integer"):
            model_cls(returns, p=p, q=q)

    @pytest.mark.parametrize("model_cls", MODELS)
    def test_rejects_boolean_orders(self, model_cls, returns):
        with pytest.raises(ValueError, match="positive integer"):
            model_cls(returns, p=True, q=1)

    @pytest.mark.parametrize("model_cls", MODELS)
    def test_rejects_float_orders(self, model_cls, returns):
        with pytest.raises(ValueError, match="positive integer"):
            model_cls(returns, p=1.0, q=1)

    @pytest.mark.parametrize("model_cls", MODELS)
    def test_accepts_numpy_integer_orders(self, model_cls, returns):
        """np.int64 lag orders must work and be normalized to Python ints."""
        model = model_cls(returns, p=np.int64(1), q=np.int64(2))
        assert model.p == 1
        assert model.q == 2
        assert isinstance(model.p, int)
        assert isinstance(model.q, int)
        assert len(model.param_names) == model.num_params

    def test_figarch_truncation_lag_validated(self, returns):
        from archbox import FIGARCH

        with pytest.raises(ValueError, match="truncation_lag"):
            FIGARCH(returns, truncation_lag=0)


class TestValidateReturns:
    """validate_returns rejects malformed return series."""

    def test_rejects_nan(self):
        with pytest.raises(ValueError, match="NaN"):
            validate_returns(np.array([0.1] * 20 + [np.nan]))

    def test_rejects_2d(self):
        with pytest.raises(ValueError, match="1D"):
            validate_returns(np.zeros((20, 2)))


class TestValidateRealizedVariance:
    """Realized variance must be finite and non-negative."""

    def test_accepts_valid_series(self):
        rv = np.linspace(1e-5, 1e-4, 50)
        np.testing.assert_allclose(validate_realized_variance(rv), rv)

    def test_rejects_negative(self):
        rv = np.full(50, 1e-4)
        rv[10] = -1e-4
        with pytest.raises(ValueError, match="non-negative"):
            validate_realized_variance(rv)

    def test_rejects_nan(self):
        rv = np.full(50, 1e-4)
        rv[3] = np.nan
        with pytest.raises(ValueError, match="NaN"):
            validate_realized_variance(rv)

    def test_rejects_inf(self):
        rv = np.full(50, 1e-4)
        rv[3] = np.inf
        with pytest.raises(ValueError, match="Inf"):
            validate_realized_variance(rv)

    def test_rejects_too_short(self):
        with pytest.raises(ValueError, match="at least 10"):
            validate_realized_variance(np.full(5, 1e-4))
