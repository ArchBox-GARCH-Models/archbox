"""CLI estimate command implementation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


def _load_data(data_path: str, column: str) -> np.ndarray:
    """Load returns data from CSV file.

    Parameters
    ----------
    data_path : str
        Path to CSV file.
    column : str
        Column name containing returns.

    Returns
    -------
    np.ndarray
        Returns array.
    """
    df = pd.read_csv(data_path)
    if column not in df.columns:
        msg = f"Column '{column}' not found in {data_path}. Available: {list(df.columns)}"
        raise ValueError(msg)
    return df[column].dropna().to_numpy(dtype=np.float64)


def _get_dist_name(dist: str) -> str:
    """Map CLI distribution name to archbox distribution name.

    Parameters
    ----------
    dist : str
        CLI distribution name.

    Returns
    -------
    str
        archbox distribution name.
    """
    mapping = {
        "normal": "normal",
        "student-t": "studentt",
        "skewed-t": "skewt",
        "ged": "ged",
    }
    return mapping.get(dist, dist)


def _build_model(model_name: str, returns: np.ndarray, args: argparse.Namespace) -> Any:
    """Build a volatility model from CLI arguments.

    Parameters
    ----------
    model_name : str
        Model type name.
    returns : np.ndarray
        Returns data.
    args : argparse.Namespace
        Parsed CLI arguments.

    Returns
    -------
    VolatilityModel
        Configured model instance.
    """
    dist = _get_dist_name(args.dist)
    mean = getattr(args, "mean", "constant")

    if model_name == "garch":
        from archbox.models.garch import GARCH

        return GARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "egarch":
        from archbox.models.egarch import EGARCH

        return EGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "gjr":
        from archbox.models.gjr_garch import GJRGARCH

        return GJRGARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "aparch":
        from archbox.models.aparch import APARCH

        return APARCH(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "figarch":
        from archbox.models.figarch import FIGARCH

        return FIGARCH(returns, dist=dist, mean=mean)
    elif model_name == "igarch":
        from archbox.models.igarch import IGARCH

        return IGARCH(returns, dist=dist, mean=mean)
    elif model_name == "garch-m":
        from archbox.models.garch_m import GARCHM

        return GARCHM(returns, p=args.p, q=args.q, dist=dist, mean=mean)
    elif model_name == "component":
        from archbox.models.component_garch import ComponentGARCH

        return ComponentGARCH(returns, dist=dist, mean=mean)
    elif model_name == "har-rv":
        from archbox.models.har_rv import HARRV

        return HARRV(returns)
    else:
        msg = f"Unknown model: {model_name}"
        raise ValueError(msg)


def run_estimate(args: argparse.Namespace) -> None:
    """Execute the estimate command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = _build_model(args.model, returns, args)
    variance_targeting = getattr(args, "variance_targeting", False)

    print(f"Fitting {args.model.upper()}({args.p},{args.q}) with {args.dist} distribution...")
    results = model.fit(variance_targeting=variance_targeting)

    # Print summary
    print(results.summary())

    # Save results
    output = {
        "model": args.model,
        "p": args.p,
        "q": args.q,
        "distribution": args.dist,
        "nobs": int(results.nobs),
        "parameters": {
            name: float(val) for name, val in zip(results.param_names, results.params, strict=False)
        },
        "loglikelihood": float(results.loglike),
        "aic": float(results.aic),
        "bic": float(results.bic),
        "persistence": float(results.persistence()),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {output_path}")
