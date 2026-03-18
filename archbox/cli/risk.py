"""CLI risk command implementation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def run_risk(args: argparse.Namespace) -> None:
    """Execute the risk command.

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

    # Compute VaR
    from archbox.risk.var import ValueAtRisk

    var_calculator = ValueAtRisk(results, alpha=args.alpha)

    if args.var_method == "parametric":
        var_series = var_calculator.parametric()
    elif args.var_method == "historical":
        var_series = var_calculator.historical()
    elif args.var_method == "filtered-hs":
        var_series = var_calculator.filtered_historical()
    elif args.var_method == "monte-carlo":
        var_series = var_calculator.monte_carlo()
    else:
        msg = f"Unknown VaR method: {args.var_method}"
        raise ValueError(msg)

    # Compute ES
    from archbox.risk.es import ExpectedShortfall

    es_calculator = ExpectedShortfall(results, alpha=args.alpha)

    if args.var_method == "parametric":
        es_series = es_calculator.parametric()
    elif args.var_method == "historical":
        es_series = es_calculator.historical()
    elif args.var_method in ("filtered-hs", "monte-carlo"):
        es_series = es_calculator.filtered_historical()
    else:
        es_series = es_calculator.parametric()

    # Output
    output = {
        "model": args.model,
        "method": args.var_method,
        "alpha": args.alpha,
        "nobs": len(returns),
        "var_last": float(var_series[-1]),
        "es_last": float(es_series[-1]),
        "var_mean": float(np.mean(var_series)),
        "es_mean": float(np.mean(es_series)),
        "var_min": float(np.min(var_series)),
        "var_max": float(np.max(var_series)),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nVaR({args.alpha}) last: {var_series[-1]:.6f}")
    print(f"ES({args.alpha}) last: {es_series[-1]:.6f}")
    print(f"Results saved to {output_path}")
