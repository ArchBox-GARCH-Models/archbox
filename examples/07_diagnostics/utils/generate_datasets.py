"""Generate CSV datasets for diagnostics examples.

Run this script to create sp500_returns.csv in the data/ directory.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.data_generator import (
    generate_misspecified_data,
    generate_sp500_returns,
    generate_structural_break_data,
)


def main():
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(data_dir, exist_ok=True)

    # Generate S&P 500 returns
    sp500 = generate_sp500_returns(seed=42)
    sp500_path = os.path.join(data_dir, "sp500_returns.csv")
    sp500.to_csv(sp500_path, index=False)
    print(f"Generated {sp500_path}: {len(sp500)} observations")
    print(f"  Columns: {list(sp500.columns)}")
    print(f"  Mean return: {sp500['returns'].mean():.6f}")
    print(f"  Std return:  {sp500['returns'].std():.6f}")
    print(f"  Kurtosis:    {sp500['returns'].kurtosis():.4f}")
    print()

    # Generate misspecified (EGARCH) data for sign bias testing
    misspec = generate_misspecified_data(n=2500, seed=70)
    misspec_path = os.path.join(data_dir, "misspecified_returns.csv")
    misspec.to_csv(misspec_path, index=False)
    print(f"Generated {misspec_path}: {len(misspec)} observations")
    print(f"  Columns: {list(misspec.columns)}")
    print(f"  Mean return: {misspec['returns'].mean():.6f}")
    print(f"  Std return:  {misspec['returns'].std():.6f}")
    print(f"  Kurtosis:    {misspec['returns'].kurtosis():.4f}")
    print()

    # Generate structural break data for Nyblom testing
    sb = generate_structural_break_data(n=2500, seed=71)
    sb_path = os.path.join(data_dir, "structural_break_returns.csv")
    sb.to_csv(sb_path, index=False)
    print(f"Generated {sb_path}: {len(sb)} observations")
    print(f"  Columns: {list(sb.columns)}")
    print(f"  Mean return: {sb['returns'].mean():.6f}")
    print(f"  Std return:  {sb['returns'].std():.6f}")
    print(f"  Kurtosis:    {sb['returns'].kurtosis():.4f}")
    print(f"  Regime 1 std: {sb.loc[sb['regime']==1, 'returns'].std():.6f}")
    print(f"  Regime 2 std: {sb.loc[sb['regime']==2, 'returns'].std():.6f}")


if __name__ == "__main__":
    main()
