"""Generate CSV datasets for risk management examples.

Run this script to create sp500_returns.csv and ibovespa_returns.csv
in the data/ directory.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.data_generator import generate_garch_returns, generate_ibov_returns


def main():
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(data_dir, exist_ok=True)

    # Generate S&P 500 returns
    sp500 = generate_garch_returns(n=2500, seed=42)
    sp500_path = os.path.join(data_dir, "sp500_returns.csv")
    sp500.to_csv(sp500_path, index=False)
    print(f"Generated {sp500_path}: {len(sp500)} observations")
    print(f"  Columns: {list(sp500.columns)}")
    print(f"  Mean return: {sp500['returns'].mean():.6f}")
    print(f"  Std return:  {sp500['returns'].std():.6f}")
    print(f"  Kurtosis:    {sp500['returns'].kurtosis():.4f}")
    print()

    # Generate Ibovespa returns
    ibov = generate_ibov_returns(n=2500, seed=43)
    ibov_path = os.path.join(data_dir, "ibovespa_returns.csv")
    ibov.to_csv(ibov_path, index=False)
    print(f"Generated {ibov_path}: {len(ibov)} observations")
    print(f"  Columns: {list(ibov.columns)}")
    print(f"  Mean return: {ibov['returns'].mean():.6f}")
    print(f"  Std return:  {ibov['returns'].std():.6f}")
    print(f"  Kurtosis:    {ibov['returns'].kurtosis():.4f}")


if __name__ == "__main__":
    main()
