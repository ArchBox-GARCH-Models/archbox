"""End-to-end tests for the risk, backtest and regime CLI subcommands.

Each test drives :func:`archbox.cli.main.main` exactly as a user would from the
shell, on a small simulated CSV, and inspects the JSON artefact the command
writes. They are regression tests for the integration seams between the CLI and
the risk / regime packages (VaR scale, Basel zones, ES/VaR method pairing, the
regime log-likelihood no longer collapsing to the -1e10 sentinel).
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from archbox.cli.main import main


def _simulate_garch(n: int, seed: int) -> np.ndarray:
    """Simulate a GARCH(1,1) return series with omega/alpha/beta = 1e-6/.08/.90."""
    rng = np.random.default_rng(seed)
    omega, alpha, beta = 1e-6, 0.08, 0.90
    sigma2 = omega / (1.0 - alpha - beta)
    returns = np.empty(n, dtype=np.float64)
    for t in range(n):
        eps = math.sqrt(sigma2) * rng.standard_normal()
        returns[t] = eps
        sigma2 = omega + alpha * eps**2 + beta * sigma2
    return returns


@pytest.fixture(scope="module")
def returns_csv(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """A 600-observation single-column CSV of simulated GARCH returns."""
    returns = _simulate_garch(600, seed=20260909)
    path = tmp_path_factory.mktemp("cli_data") / "returns.csv"
    pd.DataFrame({"date": range(returns.size), "returns": returns}).to_csv(path, index=False)
    return path


class TestCLIRiskCommand:
    """`archbox risk` on a real CSV, for every VaR method."""

    @pytest.mark.parametrize("method", ["parametric", "historical", "filtered-hs", "monte-carlo"])
    def test_risk_runs_and_writes_json(self, returns_csv: Path, tmp_path: Path, method: str):
        """Every method exits 0 and writes VaR/ES on the return scale."""
        output = tmp_path / f"risk_{method}.json"
        code = main(
            [
                "risk",
                "--model",
                "garch",
                "--data",
                str(returns_csv),
                "--var-method",
                method,
                "--alpha",
                "0.05",
                "--output",
                str(output),
            ]
        )
        assert code == 0
        payload = json.loads(output.read_text())

        assert payload["model"] == "garch"
        assert payload["method"] == method
        assert payload["alpha"] == 0.05
        assert payload["nobs"] == 600

        var_last = payload["var_last"]
        es_last = payload["es_last"]
        assert math.isfinite(var_last)
        assert math.isfinite(es_last)
        # Signed, on the scale of the returns (daily equity-like returns), not
        # a percentage and not a standardized quantile.
        assert var_last < 0.0
        assert abs(var_last) < 0.2, f"VaR off the return scale: {var_last}"
        # ES is at least as severe as VaR at the same level.
        assert es_last <= var_last + 1e-12

    def test_monte_carlo_pairs_es_with_the_same_horizon(self, returns_csv: Path, tmp_path: Path):
        """--var-method monte-carlo reports a Monte-Carlo ES, not an FHS series.

        ``monte_carlo()`` returns one value per forecast step (horizon 1 by
        default), so the summary statistics must all collapse to that single
        value for both VaR and ES. Pairing the 1-step MC VaR with the full
        in-sample FHS ES series would leave ``es_mean != es_last``.
        """
        output = tmp_path / "risk_mc.json"
        assert (
            main(
                [
                    "risk",
                    "--model",
                    "garch",
                    "--data",
                    str(returns_csv),
                    "--var-method",
                    "monte-carlo",
                    "--output",
                    str(output),
                ]
            )
            == 0
        )
        payload = json.loads(output.read_text())
        assert payload["var_last"] == pytest.approx(payload["var_mean"])
        assert payload["var_min"] == pytest.approx(payload["var_max"])
        assert payload["es_last"] == pytest.approx(payload["es_mean"])
        assert payload["es_last"] <= payload["var_last"] + 1e-12

    def test_risk_reports_failure_for_missing_column(self, returns_csv: Path, tmp_path: Path):
        """A bad --column exits 1 instead of raising."""
        output = tmp_path / "never.json"
        code = main(
            [
                "risk",
                "--model",
                "garch",
                "--data",
                str(returns_csv),
                "--column",
                "not_a_column",
                "--output",
                str(output),
            ]
        )
        assert code == 1
        assert not output.exists()


class TestCLIBacktestCommand:
    """`archbox backtest` on a real CSV."""

    def test_backtest_runs_and_writes_json(self, returns_csv: Path, tmp_path: Path):
        """Backtest exits 0 and reports coherent violation statistics."""
        output = tmp_path / "backtest.json"
        code = main(
            [
                "backtest",
                "--model",
                "garch",
                "--data",
                str(returns_csv),
                "--alpha",
                "0.05",
                "--window",
                "250",
                "--output",
                str(output),
            ]
        )
        assert code == 0
        payload = json.loads(output.read_text())

        assert payload["window"] == 250
        assert payload["expected_violations"] == pytest.approx(12.5)
        assert 0 <= payload["violations"] <= 250
        assert math.isfinite(payload["violation_ratio"])
        for test_name in ("kupiec", "christoffersen"):
            block = payload[test_name]
            assert 0.0 <= block["pvalue"] <= 1.0
            assert math.isfinite(block["statistic"])
            assert isinstance(block["reject"], bool)
        assert payload["traffic_light"] in {"green", "yellow", "red"}

    def test_correctly_specified_var_lands_in_the_green_zone(
        self, returns_csv: Path, tmp_path: Path
    ):
        """A calibrated 5% VaR is green.

        The Basel zone boundaries are computed from the Binomial(n, alpha)
        distribution; with the old hard-coded 250-day/1% table a well-specified
        5% VaR was flagged red.
        """
        output = tmp_path / "backtest_green.json"
        assert (
            main(
                [
                    "backtest",
                    "--model",
                    "garch",
                    "--data",
                    str(returns_csv),
                    "--alpha",
                    "0.05",
                    "--window",
                    "250",
                    "--output",
                    str(output),
                ]
            )
            == 0
        )
        payload = json.loads(output.read_text())
        assert payload["kupiec"]["pvalue"] > 0.05, "simulated GARCH VaR should pass Kupiec"
        assert payload["traffic_light"] == "green"


class TestCLIRegimeCommand:
    """`archbox regime` on a real CSV."""

    @pytest.mark.parametrize("model", ["ms-mean", "ms-ar", "ms-garch"])
    def test_regime_runs_and_writes_json(self, returns_csv: Path, tmp_path: Path, model: str):
        """Every regime model exits 0 with a finite likelihood and a valid chain."""
        output = tmp_path / f"regime_{model}.json"
        code = main(
            [
                "regime",
                "--model",
                model,
                "--data",
                str(returns_csv),
                "--k-regimes",
                "2",
                "--order",
                "1",
                "--output",
                str(output),
            ]
        )
        assert code == 0
        payload = json.loads(output.read_text())

        assert payload["model"] == model
        assert payload["k_regimes"] == 2
        loglike = payload["loglikelihood"]
        assert math.isfinite(loglike)
        # The pre-sample used to be scored with a -1e10 sentinel, which the EM
        # then reported as the fitted log-likelihood.
        assert loglike > -1e6, f"{model} log-likelihood looks like a sentinel: {loglike}"
        assert math.isfinite(payload["aic"])
        assert math.isfinite(payload["bic"])

        transition = np.asarray(payload["transition_matrix"], dtype=np.float64)
        assert transition.shape == (2, 2)
        assert np.all(transition >= 0.0)
        assert np.allclose(transition.sum(axis=1), 1.0)

        regime_params = payload["regime_params"]
        assert len(regime_params) == 2
        for regime in regime_params.values():
            assert isinstance(regime, dict)
            assert regime  # non-empty parameter block per regime
