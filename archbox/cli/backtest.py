"""CLI backtest command implementation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def run_backtest(args: argparse.Namespace) -> None:
    """Execute the backtest command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    from archbox.cli.estimate import _build_model, _load_data

    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(disp=False)

    # Compute VaR for backtesting
    from archbox.risk.var import ValueAtRisk

    var_calculator = ValueAtRisk(results, alpha=args.alpha)
    var_series = var_calculator.parametric()

    # Run backtest
    from archbox.risk.backtest import VaRBacktest

    window = args.window
    test_returns = returns[-window:]
    test_var = var_series[-window:]

    bt = VaRBacktest(test_returns, test_var, alpha=args.alpha)
    kupiec = bt.kupiec_test()
    christoffersen = bt.christoffersen_test()
    traffic_light = bt.basel_traffic_light()
    violation_ratio = bt.violation_ratio()
    num_violations = int(np.sum(bt.hits))

    # Output
    output = {
        "model": args.model,
        "alpha": args.alpha,
        "window": window,
        "violations": num_violations,
        "expected_violations": float(window * args.alpha),
        "violation_ratio": float(violation_ratio),
        "kupiec": {
            "statistic": float(kupiec.statistic),
            "pvalue": float(kupiec.pvalue),
            "reject": bool(kupiec.pvalue < 0.05),
        },
        "christoffersen": {
            "statistic": float(christoffersen.statistic),
            "pvalue": float(christoffersen.pvalue),
            "reject": bool(christoffersen.pvalue < 0.05),
        },
        "traffic_light": traffic_light,
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nViolation ratio: {violation_ratio:.4f}")
    print(f"Kupiec test p-value: {kupiec.pvalue:.4f}")
    print(f"Traffic light: {traffic_light}")
    print(f"Results saved to {output_path}")
