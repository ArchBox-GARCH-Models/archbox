"""
Script to generate all regime-switching datasets and save to CSV.

Usage:
    python -m utils.generate_datasets
    # or
    python utils/generate_datasets.py
"""

import os
import sys

# Ensure the parent directory is in the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_generator import generate_ms_gdp, generate_ms_returns

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    # Generate US GDP growth (quarterly, MS-AR)
    print("Generating us_gdp_growth.csv ...")
    gdp = generate_ms_gdp(n=250, seed=55)
    gdp_out = gdp[["date", "gdp_growth"]].copy()
    gdp_out["date"] = gdp_out["date"].dt.strftime("%Y-%m-%d")
    gdp_out.to_csv(os.path.join(DATA_DIR, "us_gdp_growth.csv"), index=False)
    print(
        f"  -> {len(gdp_out)} observations, date range: {gdp_out['date'].iloc[0]} to {gdp_out['date'].iloc[-1]}"
    )
    print(
        f"  -> gdp_growth stats: mean={gdp['gdp_growth'].mean():.4f}, std={gdp['gdp_growth'].std():.4f}"
    )

    # Generate S&P 500 returns (daily, MS-GARCH)
    print("Generating sp500_returns.csv ...")
    ret = generate_ms_returns(n=2500, seed=56)
    ret_out = ret[["date", "returns"]].copy()
    ret_out["date"] = ret_out["date"].dt.strftime("%Y-%m-%d")
    ret_out.to_csv(os.path.join(DATA_DIR, "sp500_returns.csv"), index=False)
    print(
        f"  -> {len(ret_out)} observations, date range: {ret_out['date'].iloc[0]} to {ret_out['date'].iloc[-1]}"
    )
    print(f"  -> returns stats: mean={ret['returns'].mean():.6f}, std={ret['returns'].std():.6f}")

    # Print regime info for verification
    print("\n--- Regime Summary ---")
    print(f"GDP regimes: {gdp['true_regime'].value_counts().sort_index().to_dict()}")
    print(f"Returns regimes: {ret['true_regime'].value_counts().sort_index().to_dict()}")

    print("\nAll datasets generated successfully.")


if __name__ == "__main__":
    main()
