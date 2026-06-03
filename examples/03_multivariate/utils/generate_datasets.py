#!/usr/bin/env python3
"""
Generate synthetic datasets for multivariate GARCH examples.

Produces:
- data/fx_majors.csv (2000 obs, 4 FX pairs via DCC simulation)
- data/sector_indices.csv (2000 obs, 5 sector indices)

Usage:
    python generate_datasets.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from data_generator import generate_dcc_returns, generate_sector_returns


def main():
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(data_dir, exist_ok=True)

    # Generate FX majors dataset
    print("Generating fx_majors.csv ...")
    fx = generate_dcc_returns(n=2000, k=4, seed=50)
    fx_path = os.path.join(data_dir, "fx_majors.csv")
    fx.to_csv(fx_path, index=False)
    print(f"  -> {fx.shape[0]} rows, {fx.shape[1]} columns saved to {fx_path}")
    print(f"  Columns: {list(fx.columns)}")
    print(f"  Correlation matrix:\n{fx.drop(columns='date').corr().round(3)}\n")

    # Generate sector indices dataset
    print("Generating sector_indices.csv ...")
    sectors = generate_sector_returns(n=2000, k=5, seed=51)
    sectors_path = os.path.join(data_dir, "sector_indices.csv")
    sectors.to_csv(sectors_path, index=False)
    print(f"  -> {sectors.shape[0]} rows, {sectors.shape[1]} columns saved to {sectors_path}")
    print(f"  Columns: {list(sectors.columns)}")
    print(f"  Correlation matrix:\n{sectors.drop(columns='date').corr().round(3)}\n")

    print("Done! Both datasets generated successfully.")


if __name__ == "__main__":
    main()
