"""Generate all datasets for the advanced GARCH examples module.

Run this script to regenerate all CSV files in the data/ directory.
All generators use fixed seeds so output is perfectly reproducible.

Usage:
    python -m utils.generate_datasets
    # or
    python utils/generate_datasets.py
"""

import os
import sys

# Ensure the parent directory is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_generator import (
    generate_realized_volatility,
    generate_sp500_returns,
)


def main():
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
    os.makedirs(data_dir, exist_ok=True)

    # S&P 500 returns (same seed=42 as FASE1)
    print("Generating sp500_returns.csv ...")
    sp500 = generate_sp500_returns(n=2500, seed=42)
    sp500.to_csv(os.path.join(data_dir, "sp500_returns.csv"), index=False)
    print(f"  -> {len(sp500)} observations, columns: {list(sp500.columns)}")

    # Realized volatility
    print("Generating realized_volatility.csv ...")
    rv = generate_realized_volatility(n=2500, seed=47)
    rv.to_csv(os.path.join(data_dir, "realized_volatility.csv"), index=False)
    print(f"  -> {len(rv)} observations, columns: {list(rv.columns)}")

    print("\nAll datasets generated successfully.")


if __name__ == "__main__":
    main()
