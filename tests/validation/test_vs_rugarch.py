"""Validation tests: archbox vs R rugarch package.

Pre-computed R reference values stored in tests/validation/fixtures/.
Tolerance: parameters +-5%, loglike +-1.0.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from archbox.datasets import load_dataset

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> dict:
    """Load a JSON fixture file."""
    path = FIXTURES_DIR / name
    return json.loads(path.read_text())


def assert_param_close(archbox_val: float, r_val: float, tol_pct: float, name: str) -> None:
    """Assert parameter is within tolerance percentage.

    Parameters
    ----------
    archbox_val : float
        Value from archbox.
    r_val : float
        Reference value from R.
    tol_pct : float
        Tolerance as fraction (e.g., 0.05 = 5%).
    name : str
        Parameter name for error message.
    """
    if abs(r_val) < 1e-10:
        # For near-zero values, use absolute tolerance
        assert abs(archbox_val - r_val) < 0.01, (
            f"{name}: archbox={archbox_val:.6f}, R={r_val:.6f}, "
            f"abs_diff={abs(archbox_val - r_val):.6f}"
        )
    else:
        pct_diff = abs(archbox_val - r_val) / abs(r_val)
        assert pct_diff < tol_pct, (
            f"{name}: archbox={archbox_val:.6f}, R={r_val:.6f}, "
            f"pct_diff={pct_diff:.4f} > tol={tol_pct}"
        )


class TestVsRugarchGARCH:
    """Validate GARCH models against rugarch."""

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        """Load SP500 data."""
        sp500 = load_dataset("sp500")
        self.returns = sp500["returns"].to_numpy(dtype=np.float64)

    def test_garch11_normal(self) -> None:
        """GARCH(1,1) Normal vs rugarch."""
        fixture = load_fixture("rugarch_garch11_normal.json")
        tol_pct = fixture["tolerance"]["params_pct"]
        tol_ll = fixture["tolerance"]["loglike_abs"]

        from archbox.models.garch import GARCH

        model = GARCH(self.returns, p=1, q=1, dist="normal")
        results = model.fit(disp=False)

        # Compare parameters
        r_params = fixture["parameters"]
        ab_params = dict(zip(results.param_names, results.params, strict=False))

        # omega
        if "omega" in ab_params and "omega" in r_params:
            assert_param_close(ab_params["omega"], r_params["omega"], tol_pct, "omega")

        # alpha
        for key in ["alpha1", "alpha"]:
            if key in r_params:
                ab_key = next((k for k in ab_params if "alpha" in k.lower()), None)
                if ab_key:
                    assert_param_close(ab_params[ab_key], r_params[key], tol_pct, key)

        # beta
        for key in ["beta1", "beta"]:
            if key in r_params:
                ab_key = next((k for k in ab_params if "beta" in k.lower()), None)
                if ab_key:
                    assert_param_close(ab_params[ab_key], r_params[key], tol_pct, key)

        # Log-likelihood
        assert abs(results.loglike - fixture["loglikelihood"]) < tol_ll, (
            f"loglike: archbox={results.loglike:.2f}, R={fixture['loglikelihood']:.2f}"
        )

    @pytest.mark.xfail(reason="Student-t distribution not yet implemented")
    def test_garch11_studentt(self) -> None:
        """GARCH(1,1) Student-t vs rugarch."""
        fixture = load_fixture("rugarch_garch11_studentt.json")
        tol_ll = fixture["tolerance"]["loglike_abs"]

        from archbox.models.garch import GARCH

        model = GARCH(self.returns, p=1, q=1, dist="studentt")
        results = model.fit(disp=False)

        assert results.params is not None
        assert abs(results.loglike - fixture["loglikelihood"]) < tol_ll

    def test_egarch11_normal(self) -> None:
        """EGARCH(1,1) Normal vs rugarch."""
        fixture = load_fixture("rugarch_egarch11_normal.json")
        tol_ll = fixture["tolerance"]["loglike_abs"]

        from archbox.models.egarch import EGARCH

        model = EGARCH(self.returns, p=1, q=1, dist="normal")
        results = model.fit(disp=False)

        assert results.params is not None
        assert abs(results.loglike - fixture["loglikelihood"]) < tol_ll, (
            f"loglike: archbox={results.loglike:.2f}, R={fixture['loglikelihood']:.2f}"
        )

    def test_gjr11_normal(self) -> None:
        """GJR-GARCH(1,1) Normal vs rugarch."""
        fixture = load_fixture("rugarch_gjr11_normal.json")
        tol_ll = fixture["tolerance"]["loglike_abs"]

        from archbox.models.gjr_garch import GJRGARCH

        model = GJRGARCH(self.returns, p=1, q=1, dist="normal")
        results = model.fit(disp=False)

        assert results.params is not None
        assert abs(results.loglike - fixture["loglikelihood"]) < tol_ll, (
            f"loglike: archbox={results.loglike:.2f}, R={fixture['loglikelihood']:.2f}"
        )

    def test_aparch11_normal(self) -> None:
        """APARCH(1,1) Normal vs rugarch."""
        fixture = load_fixture("rugarch_aparch11_normal.json")
        tol_ll = fixture["tolerance"]["loglike_abs"]

        from archbox.models.aparch import APARCH

        model = APARCH(self.returns, p=1, q=1, dist="normal")
        results = model.fit(disp=False)

        assert results.params is not None
        assert abs(results.loglike - fixture["loglikelihood"]) < tol_ll, (
            f"loglike: archbox={results.loglike:.2f}, R={fixture['loglikelihood']:.2f}"
        )


class TestParameterConsistency:
    """Test parameter consistency across distributions."""

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        """Load SP500 data."""
        sp500 = load_dataset("sp500")
        self.returns = sp500["returns"].to_numpy(dtype=np.float64)

    @pytest.mark.xfail(reason="Student-t distribution not yet implemented")
    def test_studentt_loglike_better_than_normal(self) -> None:
        """Student-t should have better (higher) loglike than Normal on fat-tailed data."""
        from archbox.models.garch import GARCH

        model_n = GARCH(self.returns, p=1, q=1, dist="normal")
        res_n = model_n.fit(disp=False)

        model_t = GARCH(self.returns, p=1, q=1, dist="studentt")
        res_t = model_t.fit(disp=False)

        # Student-t should fit at least as well (has extra parameter)
        assert res_t.loglike >= res_n.loglike - 1.0
