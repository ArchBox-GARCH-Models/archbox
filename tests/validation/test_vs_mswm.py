"""Validation tests: archbox MS-AR vs the R package MSwM.

The reference values in ``fixtures/mswm_msar24.json`` are produced by
``fixtures/generate_mswm_msar24.R`` (MSwM 1.5) on the very same data the
tests use; the JSON documents the command and the model.  Both packages
condition on the first ``p`` observations, so the log-likelihoods are
directly comparable.

Two specifications are compared:

* all coefficients switching -- both packages use the same M-step and the
  estimates agree closely;
* common AR coefficients -- MSwM's M-step for the *non-switching*
  coefficients omits the ``1/sigma_s^2`` weighting and is therefore not
  the maximiser of the expected complete-data log-likelihood.  archbox
  attains a strictly higher likelihood there; the test pins that down and
  additionally checks that archbox reproduces MSwM to ~1% once the same
  (suboptimal) weighting is used.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from archbox.datasets import load_dataset
from archbox.regime.ms_ar import MarkovSwitchingAR

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> dict[str, Any]:
    """Load a JSON fixture file."""
    path = FIXTURES_DIR / name
    return json.loads(path.read_text())


def assert_close(
    name: str,
    archbox_value: float,
    r_value: float,
    tol_pct: float,
    tol_abs: float,
) -> None:
    """Assert a parameter matches the R reference within tolerance."""
    tol = tol_pct * abs(r_value) + tol_abs
    assert abs(archbox_value - r_value) <= tol, (
        f"{name}: archbox={archbox_value:.6f}, R={r_value:.6f}, "
        f"|diff|={abs(archbox_value - r_value):.6f} > tol={tol:.6f}"
    )


class MSwMStyleMSAR(MarkovSwitchingAR):
    """MS-AR whose shared-coefficient M-step uses the MSwM weighting.

    MSwM pools the regimes with weights ``P(S_t=s | Y_T)`` only, i.e. it
    ignores the ``1/sigma_s^2`` factor of the expected complete-data
    log-likelihood.  Used to demonstrate that the remaining difference
    between archbox and MSwM is exactly this weighting.
    """

    def _update_mean_ar(
        self,
        new_params: np.ndarray,
        smoothed: np.ndarray,
    ) -> None:
        """Weighted LS ignoring the regime variances (MSwM convention)."""
        k = self.k_regimes
        p = self.order
        x_mat, y_dep = self._design_matrices()
        n_eff = y_dep.size
        z_mat = np.zeros((k * n_eff, k + p))
        weights = np.zeros(k * n_eff)
        target = np.tile(y_dep, k)
        for s in range(k):
            sl = slice(s * n_eff, (s + 1) * n_eff)
            z_mat[sl, s] = 1.0
            z_mat[sl, k:] = x_mat
            weights[sl] = np.maximum(smoothed[:, s], 0.0)
        sqrt_w = np.sqrt(weights)
        beta = np.linalg.lstsq(z_mat * sqrt_w[:, None], target * sqrt_w, rcond=None)[0]
        phi = beta[k:]
        for s in range(k):
            self._set_phi(new_params, s, phi)
            self._set_mu(new_params, s, self._mu_from_intercept(float(beta[s]), phi))


def sorted_regimes(results: Any) -> list[dict[str, Any]]:
    """Regime parameter dicts ordered by increasing mean."""
    regimes = [results.regime_params[s] for s in range(results.k_regimes)]
    order = np.argsort([r["mu"] for r in regimes])
    out: list[dict[str, Any]] = []
    for rank, idx in enumerate(order):
        rp = dict(regimes[int(idx)])
        rp["p_stay"] = float(results.transition_matrix[int(idx), int(idx)])
        rp["rank"] = rank
        out.append(rp)
    return out


class TestVsMSwM:
    """Validate MS-AR against MSwM."""

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        """Load GDP data."""
        gdp = load_dataset("us_gdp")
        self.data = gdp["growth"].dropna().to_numpy(dtype=np.float64)

    def test_msar24_common_ar(self) -> None:
        """MS(2)-AR(4) with common AR coefficients vs MSwM."""
        fixture = load_fixture("mswm_msar24.json")
        tol_pct = fixture["tolerance"]["params_pct"]
        tol_abs = fixture["tolerance"]["params_abs"]
        tol_ll = fixture["tolerance"]["loglike_abs"]
        r_params = fixture["parameters"]
        r_ll = fixture["loglikelihood"]

        model = MarkovSwitchingAR(self.data, k_regimes=2, order=4)
        results = model.fit(method="em", verbose=False)

        assert results.converged
        assert np.isfinite(results.loglike)
        assert results.nobs_effective == fixture["nobs_effective"]

        # The likelihood is the same object in both packages, so archbox
        # must not be worse than MSwM (its M-step is the exact maximiser).
        assert (
            results.loglike >= r_ll - 0.05
        ), f"archbox loglike {results.loglike:.4f} below MSwM {r_ll:.4f}"
        assert (
            abs(results.loglike - r_ll) < tol_ll
        ), f"MS-AR loglike: archbox={results.loglike:.4f}, R={r_ll:.4f}"

        low, high = sorted_regimes(results)
        assert_close("mu_0", low["mu"], r_params["mu_0"], tol_pct, tol_abs)
        assert_close("mu_1", high["mu"], r_params["mu_1"], tol_pct, tol_abs)
        assert_close("sigma_0", low["sigma"], r_params["sigma_0"], tol_pct, tol_abs)
        assert_close("sigma_1", high["sigma"], r_params["sigma_1"], tol_pct, tol_abs)
        assert_close("p_00", low["p_stay"], r_params["p_00"], tol_pct, tol_abs)
        assert_close("p_11", high["p_stay"], r_params["p_11"], tol_pct, tol_abs)
        for lag in range(1, 5):
            assert_close(f"phi_{lag}", low[f"phi_{lag}"], r_params[f"phi_{lag}"], tol_pct, tol_abs)
            # common AR: both regimes share the coefficients
            assert low[f"phi_{lag}"] == pytest.approx(high[f"phi_{lag}"])

    def test_msar24_reproduces_mswm_with_mswm_mstep(self) -> None:
        """With MSwM's M-step weighting, archbox reproduces MSwM to ~1%."""
        fixture = load_fixture("mswm_msar24.json")
        r_params = fixture["parameters"]
        r_ll = fixture["loglikelihood"]

        model = MSwMStyleMSAR(self.data, k_regimes=2, order=4)
        results = model.fit(method="em", maxiter=2000, tol=1e-12, verbose=False)

        assert (
            abs(results.loglike - r_ll) < 0.1
        ), f"loglike: archbox(MSwM M-step)={results.loglike:.4f}, R={r_ll:.4f}"

        low, high = sorted_regimes(results)
        assert_close("mu_0", low["mu"], r_params["mu_0"], 0.02, 0.02)
        assert_close("mu_1", high["mu"], r_params["mu_1"], 0.02, 0.02)
        assert_close("sigma_0", low["sigma"], r_params["sigma_0"], 0.02, 0.02)
        assert_close("sigma_1", high["sigma"], r_params["sigma_1"], 0.02, 0.02)
        assert_close("p_00", low["p_stay"], r_params["p_00"], 0.02, 0.02)
        assert_close("p_11", high["p_stay"], r_params["p_11"], 0.02, 0.02)
        for lag in range(1, 5):
            assert_close(f"phi_{lag}", low[f"phi_{lag}"], r_params[f"phi_{lag}"], 0.02, 0.02)

    def test_msar24_switching_ar(self) -> None:
        """MS(2)-AR(4) with all coefficients switching vs MSwM."""
        fixture = load_fixture("mswm_msar24.json")["switching_ar_model"]
        tol_pct = fixture["tolerance"]["params_pct"]
        tol_abs = fixture["tolerance"]["params_abs"]
        tol_ll = fixture["tolerance"]["loglike_abs"]
        r_params = fixture["parameters"]
        r_ll = fixture["loglikelihood"]

        model = MarkovSwitchingAR(self.data, k_regimes=2, order=4, switching_ar=True)
        results = model.fit(method="em", maxiter=1000, tol=1e-10, verbose=False)

        assert np.isfinite(results.loglike)
        assert (
            abs(results.loglike - r_ll) < tol_ll
        ), f"MS-AR(switching) loglike: archbox={results.loglike:.4f}, R={r_ll:.4f}"

        regimes = sorted_regimes(results)
        for rank, rp in enumerate(regimes):
            assert_close(f"mu_{rank}", rp["mu"], r_params[f"mu_{rank}"], tol_pct, tol_abs)
            assert_close(f"sigma_{rank}", rp["sigma"], r_params[f"sigma_{rank}"], tol_pct, tol_abs)
            assert_close(
                f"p_{rank}{rank}", rp["p_stay"], r_params[f"p_{rank}{rank}"], tol_pct, tol_abs
            )
            for lag in range(1, 5):
                assert_close(
                    f"phi_{lag}_{rank}",
                    rp[f"phi_{lag}"],
                    r_params[f"phi_{lag}_{rank}"],
                    tol_pct,
                    tol_abs,
                )

    def test_loglike_matches_params(self) -> None:
        """model.loglike(results.params) reproduces results.loglike."""
        model = MarkovSwitchingAR(self.data, k_regimes=2, order=4)
        results = model.fit(method="em", verbose=False)

        assert model.loglike(results.params) == pytest.approx(results.loglike, abs=1e-8)

    def test_msar_smoothed_probs_sum_to_one(self) -> None:
        """Smoothed probabilities should sum to 1 across regimes."""
        model = MarkovSwitchingAR(self.data, k_regimes=2, order=2)
        results = model.fit(method="em", verbose=False)

        smoothed = results.smoothed_probs
        assert smoothed.shape == (len(self.data), 2)
        prob_sums = np.sum(smoothed, axis=1)
        np.testing.assert_allclose(prob_sums, 1.0, atol=1e-6)

    def test_msar_transition_matrix_rows_sum_to_one(self) -> None:
        """Transition matrix rows should sum to 1."""
        model = MarkovSwitchingAR(self.data, k_regimes=2, order=2)
        results = model.fit(method="em", verbose=False)

        trans = results.transition_matrix
        row_sums = np.sum(trans, axis=1)
        np.testing.assert_allclose(row_sums, 1.0, atol=1e-6)
