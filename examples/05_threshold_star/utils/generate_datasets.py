"""
Generate CSV datasets for Threshold and STAR model examples.

Produces:
- data/us_gdp_growth.csv: 500 obs from SETAR(2,1,1) process
- data/sp500_returns.csv: 500 obs from LSTAR process

Run from the 05_threshold_star directory:
    python utils/generate_datasets.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_generator import generate_lstar_data, generate_setar_data


def main():
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
    os.makedirs(data_dir, exist_ok=True)

    # US GDP Growth - SETAR process
    gdp = generate_setar_data(n=500, seed=60)
    gdp_path = os.path.join(data_dir, "us_gdp_growth.csv")
    gdp.to_csv(gdp_path, index=False)
    print(f"Generated {gdp_path}: {len(gdp)} observations")
    print(f"  Regime 1 count: {(gdp['true_regime'] == 1).sum()}")
    print(f"  Regime 2 count: {(gdp['true_regime'] == 2).sum()}")

    # SP500 Returns - LSTAR process
    sp500 = generate_lstar_data(n=500, seed=61)
    sp500_path = os.path.join(data_dir, "sp500_returns.csv")
    sp500.to_csv(sp500_path, index=False)
    print(f"Generated {sp500_path}: {len(sp500)} observations")
    print(
        f"  Transition function range: [{sp500['transition_function'].min():.4f}, {sp500['transition_function'].max():.4f}]"
    )


if __name__ == "__main__":
    main()
