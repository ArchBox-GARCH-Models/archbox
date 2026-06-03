"""Generate synthetic CSV datasets for GARCH univariate examples.

Run this script to (re)generate all datasets in the data/ directory.
Seeds are fixed so output is deterministic.

Usage
-----
    python generate_datasets.py
"""

import os
import sys

# Ensure the utils package is importable when running as a script.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_generator import (
    generate_bitcoin_returns,
    generate_ibovespa_returns,
    generate_sp500_returns,
)

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")


def main() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)

    # S&P 500
    sp500 = generate_sp500_returns(seed=42)
    sp500[["date", "returns"]].to_csv(os.path.join(DATA_DIR, "sp500_returns.csv"), index=False)
    print(f"sp500_returns.csv: {len(sp500)} rows")

    # Ibovespa
    ibov = generate_ibovespa_returns(seed=43)
    ibov[["date", "returns"]].to_csv(os.path.join(DATA_DIR, "ibovespa_returns.csv"), index=False)
    print(f"ibovespa_returns.csv: {len(ibov)} rows")

    # Bitcoin
    btc = generate_bitcoin_returns(seed=44)
    btc[["date", "returns"]].to_csv(os.path.join(DATA_DIR, "bitcoin_returns.csv"), index=False)
    print(f"bitcoin_returns.csv: {len(btc)} rows")

    print("Done. All datasets generated.")


if __name__ == "__main__":
    main()
