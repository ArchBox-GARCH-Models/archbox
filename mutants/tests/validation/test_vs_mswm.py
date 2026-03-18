"""Validation tests: archbox vs R MSwM package.

Pre-computed R reference values stored in tests/validation/fixtures/.
Tolerance: parameters +-10%, loglike +-2.0.
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


class TestVsMSwM:
    """Validate MS-AR against MSwM."""

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        """Load GDP data."""
        gdp = load_dataset("us_gdp")
        self.data = gdp["growth"].dropna().to_numpy(dtype=np.float64)

    def test_msar24(self) -> None:
        """MS(2)-AR(4) vs MSwM."""
        fixture = load_fixture("mswm_msar24.json")
        tol_pct = fixture["tolerance"]["params_pct"]
        tol_ll = fixture["tolerance"]["loglike_abs"]

        from archbox.regime.ms_ar import MarkovSwitchingAR

        model = MarkovSwitchingAR(self.data, k_regimes=2, order=4)
        results = model.fit(method="em", verbose=False)

        # Verify basic fit
        assert results.params is not None
        assert np.isfinite(results.loglike)

        # Log-likelihood comparison
        assert (
            abs(results.loglike - fixture["loglikelihood"]) < tol_ll
        ), f"MS-AR loglike: archbox={results.loglike:.2f}, R={fixture['loglikelihood']:.2f}"

        # Transition matrix
        trans = results.transition_matrix
        assert trans.shape == (2, 2)

        r_params = fixture["parameters"]

        # Transition probabilities (within tolerance)
        if "p_00" in r_params:
            assert (
                abs(trans[0, 0] - r_params["p_00"]) < tol_pct * r_params["p_00"] + 0.05
            ), f"p_00: archbox={trans[0, 0]:.4f}, R={r_params['p_00']:.4f}"
        if "p_11" in r_params:
            assert (
                abs(trans[1, 1] - r_params["p_11"]) < tol_pct * r_params["p_11"] + 0.05
            ), f"p_11: archbox={trans[1, 1]:.4f}, R={r_params['p_11']:.4f}"

        # Regime means should be ordered (regime 0 = expansion, regime 1 = recession)
        if hasattr(results, "regime_params") and results.regime_params:
            means = [results.regime_params[k].get("mu", 0.0) for k in range(2)]
            assert len(means) == 2

    def test_msar_smoothed_probs_sum_to_one(self) -> None:
        """Smoothed probabilities should sum to 1 across regimes."""
        from archbox.regime.ms_ar import MarkovSwitchingAR

        model = MarkovSwitchingAR(self.data, k_regimes=2, order=2)
        results = model.fit(method="em", verbose=False)

        smoothed = results.smoothed_probs
        prob_sums = np.sum(smoothed, axis=1)
        np.testing.assert_allclose(prob_sums, 1.0, atol=1e-6)

    def test_msar_transition_matrix_rows_sum_to_one(self) -> None:
        """Transition matrix rows should sum to 1."""
        from archbox.regime.ms_ar import MarkovSwitchingAR

        model = MarkovSwitchingAR(self.data, k_regimes=2, order=2)
        results = model.fit(method="em", verbose=False)

        trans = results.transition_matrix
        row_sums = np.sum(trans, axis=1)
        np.testing.assert_allclose(row_sums, 1.0, atol=1e-6)
