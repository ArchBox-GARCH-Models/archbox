"""Tests for archbox CLI."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from archbox.cli.main import main


class TestCLIHelp:
    """Test --help for all commands."""

    def test_main_help_subprocess(self):
        """archbox --help works via subprocess."""
        result = subprocess.run(
            [sys.executable, "-m", "archbox.cli.main", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "archbox" in result.stdout.lower()

    def test_estimate_help_subprocess(self):
        """archbox estimate --help works via subprocess."""
        result = subprocess.run(
            [sys.executable, "-m", "archbox.cli.main", "estimate", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "--model" in result.stdout

    def test_risk_help_subprocess(self):
        """archbox risk --help works via subprocess."""
        result = subprocess.run(
            [sys.executable, "-m", "archbox.cli.main", "risk", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "--var-method" in result.stdout

    def test_backtest_help_subprocess(self):
        """archbox backtest --help works via subprocess."""
        result = subprocess.run(
            [sys.executable, "-m", "archbox.cli.main", "backtest", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0

    def test_regime_help_subprocess(self):
        """archbox regime --help works via subprocess."""
        result = subprocess.run(
            [sys.executable, "-m", "archbox.cli.main", "regime", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "--k-regimes" in result.stdout


class TestCLIVersion:
    """Test --version flag."""

    def test_version(self, capsys: pytest.CaptureFixture[str]) -> None:
        """--version prints version."""
        result = main(["--version"])
        assert result == 0
        captured = capsys.readouterr()
        assert "archbox" in captured.out


class TestCLIEstimate:
    """Test estimate command with actual data."""

    @pytest.fixture
    def sample_csv(self, tmp_path: Path) -> Path:
        """Create a sample CSV for testing."""
        rng = np.random.default_rng(42)
        n = 500
        returns = rng.standard_normal(n) * 0.01
        df = pd.DataFrame({"date": range(n), "returns": returns})
        csv_path = tmp_path / "test_data.csv"
        df.to_csv(csv_path, index=False)
        return csv_path

    def test_estimate_garch_produces_output(self, sample_csv: Path, tmp_path: Path) -> None:
        """estimate command produces JSON output."""
        output_path = tmp_path / "results.json"
        result = main(
            [
                "estimate",
                "--model",
                "garch",
                "--data",
                str(sample_csv),
                "--p",
                "1",
                "--q",
                "1",
                "--output",
                str(output_path),
            ]
        )
        assert result == 0
        assert output_path.exists()
        data = json.loads(output_path.read_text())
        assert "parameters" in data
        assert "loglikelihood" in data
        assert data["model"] == "garch"


class TestCLINoCommand:
    """Test behavior with no command."""

    def test_no_command_returns_zero(self) -> None:
        """No command prints help and returns 0."""
        result = main([])
        assert result == 0
