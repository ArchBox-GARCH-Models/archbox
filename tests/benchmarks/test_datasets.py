"""Tests for dataset loading."""

from __future__ import annotations

import pytest

from archbox.datasets import list_datasets, load_dataset


class TestDatasets:
    """Test all built-in datasets load correctly."""

    def test_list_datasets_returns_all(self):
        """list_datasets() returns all expected datasets."""
        datasets = list_datasets()
        expected = [
            "bitcoin",
            "ftse100",
            "fx_majors",
            "ibovespa",
            "industrial_production",
            "realized_vol",
            "sector_indices",
            "sp500",
            "us_gdp",
            "us_unemployment",
            "usdbrl",
        ]
        for name in expected:
            assert name in datasets, f"Missing dataset: {name}"

    @pytest.mark.parametrize(
        "name",
        [
            "sp500",
            "ftse100",
            "bitcoin",
            "fx_majors",
            "sector_indices",
            "realized_vol",
            "us_gdp",
            "us_unemployment",
            "industrial_production",
            "ibovespa",
            "usdbrl",
        ],
    )
    def test_load_dataset(self, name: str):
        """Each dataset loads without error and has data."""
        df = load_dataset(name)
        assert len(df) > 0, f"Dataset '{name}' is empty"
        assert "date" in df.columns, f"Dataset '{name}' missing 'date' column"

    def test_sp500_shape(self):
        """SP500 has expected shape."""
        df = load_dataset("sp500")
        assert len(df) == 2500
        assert "returns" in df.columns

    def test_fx_majors_multivariate(self):
        """FX majors has multiple return series."""
        df = load_dataset("fx_majors")
        numeric_cols = [c for c in df.columns if c != "date"]
        assert len(numeric_cols) >= 2

    def test_sector_indices_multivariate(self):
        """Sector indices has 5 series."""
        df = load_dataset("sector_indices")
        numeric_cols = [c for c in df.columns if c != "date"]
        assert len(numeric_cols) == 5

    def test_unknown_dataset_raises(self):
        """Unknown dataset raises ValueError."""
        with pytest.raises(ValueError, match="Unknown dataset"):
            load_dataset("nonexistent")
