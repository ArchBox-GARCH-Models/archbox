"""CLI regime command implementation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


def _build_regime_model(model_name: str, data: np.ndarray, args: argparse.Namespace) -> Any:
    """Build a regime-switching model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Regime model type name.
    data : np.ndarray
        Data array.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    RegimeModel
        Configured model instance.
    """
    k_regimes = args.k_regimes
    order = args.order

    if model_name == "ms-mean":
        from archbox.regime.ms_mean import MarkovSwitchingMean

        return MarkovSwitchingMean(data, k_regimes=k_regimes)
    elif model_name == "ms-ar":
        from archbox.regime.ms_ar import MarkovSwitchingAR

        return MarkovSwitchingAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-var":
        from archbox.regime.ms_var import MarkovSwitchingVAR

        return MarkovSwitchingVAR(data, k_regimes=k_regimes, order=order)
    elif model_name == "ms-garch":
        from archbox.regime.ms_garch import MarkovSwitchingGARCH

        return MarkovSwitchingGARCH(data, k_regimes=k_regimes)
    else:
        msg = f"Unknown regime model: {model_name}"
        raise ValueError(msg)


def run_regime(args: argparse.Namespace) -> None:
    """Execute the regime command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    df = pd.read_csv(args.data)
    column = args.column
    if column not in df.columns:
        msg = f"Column '{column}' not found in {args.data}. Available: {list(df.columns)}"
        raise ValueError(msg)
    data = df[column].dropna().to_numpy(dtype=np.float64)
    print(f"Loaded {len(data)} observations from {args.data}")

    # Build and fit model
    model = _build_regime_model(args.model, data, args)
    print(f"Fitting {args.model.upper()} with {args.k_regimes} regimes, order={args.order}...")
    results = model.fit(method=args.method)

    # Print summary
    print(results.summary())

    # Save results
    output: dict[str, Any] = {
        "model": args.model,
        "k_regimes": args.k_regimes,
        "order": args.order,
        "method": args.method,
        "nobs": int(results.nobs),
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
    }

    # Add regime-specific parameters
    if hasattr(results, "transition_matrix"):
        output["transition_matrix"] = results.transition_matrix.tolist()
    if hasattr(results, "regime_params"):
        output["regime_params"] = {
            k: float(v) if isinstance(v, int | float | np.floating) else v
            for k, v in results.regime_params.items()
        }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nResults saved to {output_path}")
