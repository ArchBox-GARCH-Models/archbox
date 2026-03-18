"""CLI risk command implementation."""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable
from pathlib import Path
from typing import Annotated, ClassVar

import numpy as np

MutantDict = Annotated[dict[str, Callable], "Mutant"]  # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):  # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os  # type: ignore

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]  # type: ignore
    if mutant_under_test == "fail":  # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException  # type: ignore

        raise MutmutProgrammaticFailException("Failed programmatically")  # type: ignore
    elif mutant_under_test == "stats":  # type: ignore
        from mutmut.__main__ import record_trampoline_hit  # type: ignore

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)  # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs)  # type: ignore
        return result  # type: ignore
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"  # type: ignore
    if not mutant_under_test.startswith(prefix):  # type: ignore
        result = orig(*call_args, **call_kwargs)  # type: ignore
        return result  # type: ignore
    mutant_name = mutant_under_test.rpartition(".")[-1]  # type: ignore
    if self_arg is not None:  # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)  # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)  # type: ignore
    return result  # type: ignore


def run_risk(args: argparse.Namespace) -> None:
    args = [args]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_run_risk__mutmut_orig, x_run_risk__mutmut_mutants, args, kwargs, None
    )


def x_run_risk__mutmut_orig(args: argparse.Namespace) -> None:
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


def x_run_risk__mutmut_1(args: argparse.Namespace) -> None:
    """Execute the risk command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    from archbox.cli.estimate import _build_model

    # Load data
    returns = None
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


def x_run_risk__mutmut_2(args: argparse.Namespace) -> None:
    """Execute the risk command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    from archbox.cli.estimate import _build_model, _load_data

    # Load data
    returns = _load_data(None, args.column)
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


def x_run_risk__mutmut_3(args: argparse.Namespace) -> None:
    """Execute the risk command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    from archbox.cli.estimate import _build_model, _load_data

    # Load data
    returns = _load_data(args.data, None)
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


def x_run_risk__mutmut_4(args: argparse.Namespace) -> None:
    """Execute the risk command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    from archbox.cli.estimate import _build_model, _load_data

    # Load data
    returns = _load_data(args.column)
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


def x_run_risk__mutmut_5(args: argparse.Namespace) -> None:
    """Execute the risk command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    from archbox.cli.estimate import _build_model, _load_data

    # Load data
    returns = _load_data(
        args.data,
    )
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


def x_run_risk__mutmut_6(args: argparse.Namespace) -> None:
    """Execute the risk command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    from archbox.cli.estimate import _build_model, _load_data

    # Load data
    returns = _load_data(args.data, args.column)
    print(None)

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


def x_run_risk__mutmut_7(args: argparse.Namespace) -> None:
    """Execute the risk command.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments.
    """
    from archbox.cli.estimate import _load_data

    # Load data
    returns = _load_data(args.data, args.column)
    print(f"Loaded {len(returns)} observations from {args.data}")

    # Build and fit model
    model = None
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


def x_run_risk__mutmut_8(args: argparse.Namespace) -> None:
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
    model = _build_model(None, returns, args)
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


def x_run_risk__mutmut_9(args: argparse.Namespace) -> None:
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
    model = _build_model(args.model, None, args)
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


def x_run_risk__mutmut_10(args: argparse.Namespace) -> None:
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
    model = _build_model(args.model, returns, None)
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


def x_run_risk__mutmut_11(args: argparse.Namespace) -> None:
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
    model = _build_model(returns, args)
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


def x_run_risk__mutmut_12(args: argparse.Namespace) -> None:
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
    model = _build_model(args.model, args)
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


def x_run_risk__mutmut_13(args: argparse.Namespace) -> None:
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
    model = _build_model(
        args.model,
        returns,
    )
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


def x_run_risk__mutmut_14(args: argparse.Namespace) -> None:
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
    print(None)
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


def x_run_risk__mutmut_15(args: argparse.Namespace) -> None:
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
    print(f"Fitting {args.model.lower()}({args.p},{args.q}) with {args.dist} distribution...")
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


def x_run_risk__mutmut_16(args: argparse.Namespace) -> None:
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
    results = None

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


def x_run_risk__mutmut_17(args: argparse.Namespace) -> None:
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
    results = model.fit(disp=None)

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


def x_run_risk__mutmut_18(args: argparse.Namespace) -> None:
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
    results = model.fit(disp=True)

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


def x_run_risk__mutmut_19(args: argparse.Namespace) -> None:
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

    var_calculator = None

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


def x_run_risk__mutmut_20(args: argparse.Namespace) -> None:
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

    var_calculator = ValueAtRisk(None, alpha=args.alpha)

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


def x_run_risk__mutmut_21(args: argparse.Namespace) -> None:
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

    var_calculator = ValueAtRisk(results, alpha=None)

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


def x_run_risk__mutmut_22(args: argparse.Namespace) -> None:
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

    var_calculator = ValueAtRisk(alpha=args.alpha)

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


def x_run_risk__mutmut_23(args: argparse.Namespace) -> None:
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

    var_calculator = ValueAtRisk(
        results,
    )

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


def x_run_risk__mutmut_24(args: argparse.Namespace) -> None:
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

    if args.var_method != "parametric":
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


def x_run_risk__mutmut_25(args: argparse.Namespace) -> None:
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

    if args.var_method == "XXparametricXX":
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


def x_run_risk__mutmut_26(args: argparse.Namespace) -> None:
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

    if args.var_method == "PARAMETRIC":
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


def x_run_risk__mutmut_27(args: argparse.Namespace) -> None:
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
        var_series = None
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


def x_run_risk__mutmut_28(args: argparse.Namespace) -> None:
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
    elif args.var_method != "historical":
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


def x_run_risk__mutmut_29(args: argparse.Namespace) -> None:
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
    elif args.var_method == "XXhistoricalXX":
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


def x_run_risk__mutmut_30(args: argparse.Namespace) -> None:
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
    elif args.var_method == "HISTORICAL":
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


def x_run_risk__mutmut_31(args: argparse.Namespace) -> None:
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
        var_series = None
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


def x_run_risk__mutmut_32(args: argparse.Namespace) -> None:
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
    elif args.var_method != "filtered-hs":
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


def x_run_risk__mutmut_33(args: argparse.Namespace) -> None:
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
    elif args.var_method == "XXfiltered-hsXX":
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


def x_run_risk__mutmut_34(args: argparse.Namespace) -> None:
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
    elif args.var_method == "FILTERED-HS":
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


def x_run_risk__mutmut_35(args: argparse.Namespace) -> None:
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
        var_series = None
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


def x_run_risk__mutmut_36(args: argparse.Namespace) -> None:
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
    elif args.var_method != "monte-carlo":
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


def x_run_risk__mutmut_37(args: argparse.Namespace) -> None:
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
    elif args.var_method == "XXmonte-carloXX":
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


def x_run_risk__mutmut_38(args: argparse.Namespace) -> None:
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
    elif args.var_method == "MONTE-CARLO":
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


def x_run_risk__mutmut_39(args: argparse.Namespace) -> None:
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
        var_series = None
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


def x_run_risk__mutmut_40(args: argparse.Namespace) -> None:
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
        msg = None
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


def x_run_risk__mutmut_41(args: argparse.Namespace) -> None:
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
        raise ValueError(None)

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


def x_run_risk__mutmut_42(args: argparse.Namespace) -> None:
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

    es_calculator = None

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


def x_run_risk__mutmut_43(args: argparse.Namespace) -> None:
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

    es_calculator = ExpectedShortfall(None, alpha=args.alpha)

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


def x_run_risk__mutmut_44(args: argparse.Namespace) -> None:
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

    es_calculator = ExpectedShortfall(results, alpha=None)

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


def x_run_risk__mutmut_45(args: argparse.Namespace) -> None:
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

    es_calculator = ExpectedShortfall(alpha=args.alpha)

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


def x_run_risk__mutmut_46(args: argparse.Namespace) -> None:
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

    es_calculator = ExpectedShortfall(
        results,
    )

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


def x_run_risk__mutmut_47(args: argparse.Namespace) -> None:
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

    if args.var_method != "parametric":
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


def x_run_risk__mutmut_48(args: argparse.Namespace) -> None:
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

    if args.var_method == "XXparametricXX":
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


def x_run_risk__mutmut_49(args: argparse.Namespace) -> None:
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

    if args.var_method == "PARAMETRIC":
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


def x_run_risk__mutmut_50(args: argparse.Namespace) -> None:
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
        es_series = None
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


def x_run_risk__mutmut_51(args: argparse.Namespace) -> None:
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
    elif args.var_method != "historical":
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


def x_run_risk__mutmut_52(args: argparse.Namespace) -> None:
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
    elif args.var_method == "XXhistoricalXX":
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


def x_run_risk__mutmut_53(args: argparse.Namespace) -> None:
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
    elif args.var_method == "HISTORICAL":
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


def x_run_risk__mutmut_54(args: argparse.Namespace) -> None:
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
        es_series = None
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


def x_run_risk__mutmut_55(args: argparse.Namespace) -> None:
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
    elif args.var_method not in ("filtered-hs", "monte-carlo"):
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


def x_run_risk__mutmut_56(args: argparse.Namespace) -> None:
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
    elif args.var_method in ("XXfiltered-hsXX", "monte-carlo"):
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


def x_run_risk__mutmut_57(args: argparse.Namespace) -> None:
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
    elif args.var_method in ("FILTERED-HS", "monte-carlo"):
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


def x_run_risk__mutmut_58(args: argparse.Namespace) -> None:
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
    elif args.var_method in ("filtered-hs", "XXmonte-carloXX"):
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


def x_run_risk__mutmut_59(args: argparse.Namespace) -> None:
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
    elif args.var_method in ("filtered-hs", "MONTE-CARLO"):
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


def x_run_risk__mutmut_60(args: argparse.Namespace) -> None:
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
        es_series = None
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


def x_run_risk__mutmut_61(args: argparse.Namespace) -> None:
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
        es_series = None

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


def x_run_risk__mutmut_62(args: argparse.Namespace) -> None:
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
    output = None

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nVaR({args.alpha}) last: {var_series[-1]:.6f}")
    print(f"ES({args.alpha}) last: {es_series[-1]:.6f}")
    print(f"Results saved to {output_path}")


def x_run_risk__mutmut_63(args: argparse.Namespace) -> None:
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
        "XXmodelXX": args.model,
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


def x_run_risk__mutmut_64(args: argparse.Namespace) -> None:
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
        "MODEL": args.model,
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


def x_run_risk__mutmut_65(args: argparse.Namespace) -> None:
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
        "XXmethodXX": args.var_method,
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


def x_run_risk__mutmut_66(args: argparse.Namespace) -> None:
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
        "METHOD": args.var_method,
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


def x_run_risk__mutmut_67(args: argparse.Namespace) -> None:
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
        "XXalphaXX": args.alpha,
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


def x_run_risk__mutmut_68(args: argparse.Namespace) -> None:
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
        "ALPHA": args.alpha,
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


def x_run_risk__mutmut_69(args: argparse.Namespace) -> None:
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
        "XXnobsXX": len(returns),
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


def x_run_risk__mutmut_70(args: argparse.Namespace) -> None:
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
        "NOBS": len(returns),
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


def x_run_risk__mutmut_71(args: argparse.Namespace) -> None:
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
        "XXvar_lastXX": float(var_series[-1]),
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


def x_run_risk__mutmut_72(args: argparse.Namespace) -> None:
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
        "VAR_LAST": float(var_series[-1]),
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


def x_run_risk__mutmut_73(args: argparse.Namespace) -> None:
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
        "var_last": float(None),
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


def x_run_risk__mutmut_74(args: argparse.Namespace) -> None:
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
        "var_last": float(var_series[+1]),
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


def x_run_risk__mutmut_75(args: argparse.Namespace) -> None:
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
        "var_last": float(var_series[-2]),
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


def x_run_risk__mutmut_76(args: argparse.Namespace) -> None:
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
        "XXes_lastXX": float(es_series[-1]),
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


def x_run_risk__mutmut_77(args: argparse.Namespace) -> None:
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
        "ES_LAST": float(es_series[-1]),
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


def x_run_risk__mutmut_78(args: argparse.Namespace) -> None:
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
        "es_last": float(None),
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


def x_run_risk__mutmut_79(args: argparse.Namespace) -> None:
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
        "es_last": float(es_series[+1]),
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


def x_run_risk__mutmut_80(args: argparse.Namespace) -> None:
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
        "es_last": float(es_series[-2]),
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


def x_run_risk__mutmut_81(args: argparse.Namespace) -> None:
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
        "XXvar_meanXX": float(np.mean(var_series)),
        "es_mean": float(np.mean(es_series)),
        "var_min": float(np.min(var_series)),
        "var_max": float(np.max(var_series)),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nVaR({args.alpha}) last: {var_series[-1]:.6f}")
    print(f"ES({args.alpha}) last: {es_series[-1]:.6f}")
    print(f"Results saved to {output_path}")


def x_run_risk__mutmut_82(args: argparse.Namespace) -> None:
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
        "VAR_MEAN": float(np.mean(var_series)),
        "es_mean": float(np.mean(es_series)),
        "var_min": float(np.min(var_series)),
        "var_max": float(np.max(var_series)),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nVaR({args.alpha}) last: {var_series[-1]:.6f}")
    print(f"ES({args.alpha}) last: {es_series[-1]:.6f}")
    print(f"Results saved to {output_path}")


def x_run_risk__mutmut_83(args: argparse.Namespace) -> None:
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
        "var_mean": float(None),
        "es_mean": float(np.mean(es_series)),
        "var_min": float(np.min(var_series)),
        "var_max": float(np.max(var_series)),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nVaR({args.alpha}) last: {var_series[-1]:.6f}")
    print(f"ES({args.alpha}) last: {es_series[-1]:.6f}")
    print(f"Results saved to {output_path}")


def x_run_risk__mutmut_84(args: argparse.Namespace) -> None:
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
        "var_mean": float(np.mean(None)),
        "es_mean": float(np.mean(es_series)),
        "var_min": float(np.min(var_series)),
        "var_max": float(np.max(var_series)),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nVaR({args.alpha}) last: {var_series[-1]:.6f}")
    print(f"ES({args.alpha}) last: {es_series[-1]:.6f}")
    print(f"Results saved to {output_path}")


def x_run_risk__mutmut_85(args: argparse.Namespace) -> None:
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
        "XXes_meanXX": float(np.mean(es_series)),
        "var_min": float(np.min(var_series)),
        "var_max": float(np.max(var_series)),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nVaR({args.alpha}) last: {var_series[-1]:.6f}")
    print(f"ES({args.alpha}) last: {es_series[-1]:.6f}")
    print(f"Results saved to {output_path}")


def x_run_risk__mutmut_86(args: argparse.Namespace) -> None:
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
        "ES_MEAN": float(np.mean(es_series)),
        "var_min": float(np.min(var_series)),
        "var_max": float(np.max(var_series)),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nVaR({args.alpha}) last: {var_series[-1]:.6f}")
    print(f"ES({args.alpha}) last: {es_series[-1]:.6f}")
    print(f"Results saved to {output_path}")


def x_run_risk__mutmut_87(args: argparse.Namespace) -> None:
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
        "es_mean": float(None),
        "var_min": float(np.min(var_series)),
        "var_max": float(np.max(var_series)),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nVaR({args.alpha}) last: {var_series[-1]:.6f}")
    print(f"ES({args.alpha}) last: {es_series[-1]:.6f}")
    print(f"Results saved to {output_path}")


def x_run_risk__mutmut_88(args: argparse.Namespace) -> None:
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
        "es_mean": float(np.mean(None)),
        "var_min": float(np.min(var_series)),
        "var_max": float(np.max(var_series)),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nVaR({args.alpha}) last: {var_series[-1]:.6f}")
    print(f"ES({args.alpha}) last: {es_series[-1]:.6f}")
    print(f"Results saved to {output_path}")


def x_run_risk__mutmut_89(args: argparse.Namespace) -> None:
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
        "XXvar_minXX": float(np.min(var_series)),
        "var_max": float(np.max(var_series)),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nVaR({args.alpha}) last: {var_series[-1]:.6f}")
    print(f"ES({args.alpha}) last: {es_series[-1]:.6f}")
    print(f"Results saved to {output_path}")


def x_run_risk__mutmut_90(args: argparse.Namespace) -> None:
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
        "VAR_MIN": float(np.min(var_series)),
        "var_max": float(np.max(var_series)),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nVaR({args.alpha}) last: {var_series[-1]:.6f}")
    print(f"ES({args.alpha}) last: {es_series[-1]:.6f}")
    print(f"Results saved to {output_path}")


def x_run_risk__mutmut_91(args: argparse.Namespace) -> None:
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
        "var_min": float(None),
        "var_max": float(np.max(var_series)),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nVaR({args.alpha}) last: {var_series[-1]:.6f}")
    print(f"ES({args.alpha}) last: {es_series[-1]:.6f}")
    print(f"Results saved to {output_path}")


def x_run_risk__mutmut_92(args: argparse.Namespace) -> None:
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
        "var_min": float(np.min(None)),
        "var_max": float(np.max(var_series)),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nVaR({args.alpha}) last: {var_series[-1]:.6f}")
    print(f"ES({args.alpha}) last: {es_series[-1]:.6f}")
    print(f"Results saved to {output_path}")


def x_run_risk__mutmut_93(args: argparse.Namespace) -> None:
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
        "XXvar_maxXX": float(np.max(var_series)),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nVaR({args.alpha}) last: {var_series[-1]:.6f}")
    print(f"ES({args.alpha}) last: {es_series[-1]:.6f}")
    print(f"Results saved to {output_path}")


def x_run_risk__mutmut_94(args: argparse.Namespace) -> None:
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
        "VAR_MAX": float(np.max(var_series)),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nVaR({args.alpha}) last: {var_series[-1]:.6f}")
    print(f"ES({args.alpha}) last: {es_series[-1]:.6f}")
    print(f"Results saved to {output_path}")


def x_run_risk__mutmut_95(args: argparse.Namespace) -> None:
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
        "var_max": float(None),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nVaR({args.alpha}) last: {var_series[-1]:.6f}")
    print(f"ES({args.alpha}) last: {es_series[-1]:.6f}")
    print(f"Results saved to {output_path}")


def x_run_risk__mutmut_96(args: argparse.Namespace) -> None:
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
        "var_max": float(np.max(None)),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nVaR({args.alpha}) last: {var_series[-1]:.6f}")
    print(f"ES({args.alpha}) last: {es_series[-1]:.6f}")
    print(f"Results saved to {output_path}")


def x_run_risk__mutmut_97(args: argparse.Namespace) -> None:
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

    output_path = None
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nVaR({args.alpha}) last: {var_series[-1]:.6f}")
    print(f"ES({args.alpha}) last: {es_series[-1]:.6f}")
    print(f"Results saved to {output_path}")


def x_run_risk__mutmut_98(args: argparse.Namespace) -> None:
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

    output_path = Path(None)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nVaR({args.alpha}) last: {var_series[-1]:.6f}")
    print(f"ES({args.alpha}) last: {es_series[-1]:.6f}")
    print(f"Results saved to {output_path}")


def x_run_risk__mutmut_99(args: argparse.Namespace) -> None:
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
    output_path.write_text(None)
    print(f"\nVaR({args.alpha}) last: {var_series[-1]:.6f}")
    print(f"ES({args.alpha}) last: {es_series[-1]:.6f}")
    print(f"Results saved to {output_path}")


def x_run_risk__mutmut_100(args: argparse.Namespace) -> None:
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
    output_path.write_text(json.dumps(None, indent=2))
    print(f"\nVaR({args.alpha}) last: {var_series[-1]:.6f}")
    print(f"ES({args.alpha}) last: {es_series[-1]:.6f}")
    print(f"Results saved to {output_path}")


def x_run_risk__mutmut_101(args: argparse.Namespace) -> None:
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
    output_path.write_text(json.dumps(output, indent=None))
    print(f"\nVaR({args.alpha}) last: {var_series[-1]:.6f}")
    print(f"ES({args.alpha}) last: {es_series[-1]:.6f}")
    print(f"Results saved to {output_path}")


def x_run_risk__mutmut_102(args: argparse.Namespace) -> None:
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
    output_path.write_text(json.dumps(indent=2))
    print(f"\nVaR({args.alpha}) last: {var_series[-1]:.6f}")
    print(f"ES({args.alpha}) last: {es_series[-1]:.6f}")
    print(f"Results saved to {output_path}")


def x_run_risk__mutmut_103(args: argparse.Namespace) -> None:
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
    output_path.write_text(
        json.dumps(
            output,
        )
    )
    print(f"\nVaR({args.alpha}) last: {var_series[-1]:.6f}")
    print(f"ES({args.alpha}) last: {es_series[-1]:.6f}")
    print(f"Results saved to {output_path}")


def x_run_risk__mutmut_104(args: argparse.Namespace) -> None:
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
    output_path.write_text(json.dumps(output, indent=3))
    print(f"\nVaR({args.alpha}) last: {var_series[-1]:.6f}")
    print(f"ES({args.alpha}) last: {es_series[-1]:.6f}")
    print(f"Results saved to {output_path}")


def x_run_risk__mutmut_105(args: argparse.Namespace) -> None:
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
    print(None)
    print(f"ES({args.alpha}) last: {es_series[-1]:.6f}")
    print(f"Results saved to {output_path}")


def x_run_risk__mutmut_106(args: argparse.Namespace) -> None:
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
    print(f"\nVaR({args.alpha}) last: {var_series[+1]:.6f}")
    print(f"ES({args.alpha}) last: {es_series[-1]:.6f}")
    print(f"Results saved to {output_path}")


def x_run_risk__mutmut_107(args: argparse.Namespace) -> None:
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
    print(f"\nVaR({args.alpha}) last: {var_series[-2]:.6f}")
    print(f"ES({args.alpha}) last: {es_series[-1]:.6f}")
    print(f"Results saved to {output_path}")


def x_run_risk__mutmut_108(args: argparse.Namespace) -> None:
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
    print(None)
    print(f"Results saved to {output_path}")


def x_run_risk__mutmut_109(args: argparse.Namespace) -> None:
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
    print(f"ES({args.alpha}) last: {es_series[+1]:.6f}")
    print(f"Results saved to {output_path}")


def x_run_risk__mutmut_110(args: argparse.Namespace) -> None:
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
    print(f"ES({args.alpha}) last: {es_series[-2]:.6f}")
    print(f"Results saved to {output_path}")


def x_run_risk__mutmut_111(args: argparse.Namespace) -> None:
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
    print(None)


x_run_risk__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_run_risk__mutmut_1": x_run_risk__mutmut_1,
    "x_run_risk__mutmut_2": x_run_risk__mutmut_2,
    "x_run_risk__mutmut_3": x_run_risk__mutmut_3,
    "x_run_risk__mutmut_4": x_run_risk__mutmut_4,
    "x_run_risk__mutmut_5": x_run_risk__mutmut_5,
    "x_run_risk__mutmut_6": x_run_risk__mutmut_6,
    "x_run_risk__mutmut_7": x_run_risk__mutmut_7,
    "x_run_risk__mutmut_8": x_run_risk__mutmut_8,
    "x_run_risk__mutmut_9": x_run_risk__mutmut_9,
    "x_run_risk__mutmut_10": x_run_risk__mutmut_10,
    "x_run_risk__mutmut_11": x_run_risk__mutmut_11,
    "x_run_risk__mutmut_12": x_run_risk__mutmut_12,
    "x_run_risk__mutmut_13": x_run_risk__mutmut_13,
    "x_run_risk__mutmut_14": x_run_risk__mutmut_14,
    "x_run_risk__mutmut_15": x_run_risk__mutmut_15,
    "x_run_risk__mutmut_16": x_run_risk__mutmut_16,
    "x_run_risk__mutmut_17": x_run_risk__mutmut_17,
    "x_run_risk__mutmut_18": x_run_risk__mutmut_18,
    "x_run_risk__mutmut_19": x_run_risk__mutmut_19,
    "x_run_risk__mutmut_20": x_run_risk__mutmut_20,
    "x_run_risk__mutmut_21": x_run_risk__mutmut_21,
    "x_run_risk__mutmut_22": x_run_risk__mutmut_22,
    "x_run_risk__mutmut_23": x_run_risk__mutmut_23,
    "x_run_risk__mutmut_24": x_run_risk__mutmut_24,
    "x_run_risk__mutmut_25": x_run_risk__mutmut_25,
    "x_run_risk__mutmut_26": x_run_risk__mutmut_26,
    "x_run_risk__mutmut_27": x_run_risk__mutmut_27,
    "x_run_risk__mutmut_28": x_run_risk__mutmut_28,
    "x_run_risk__mutmut_29": x_run_risk__mutmut_29,
    "x_run_risk__mutmut_30": x_run_risk__mutmut_30,
    "x_run_risk__mutmut_31": x_run_risk__mutmut_31,
    "x_run_risk__mutmut_32": x_run_risk__mutmut_32,
    "x_run_risk__mutmut_33": x_run_risk__mutmut_33,
    "x_run_risk__mutmut_34": x_run_risk__mutmut_34,
    "x_run_risk__mutmut_35": x_run_risk__mutmut_35,
    "x_run_risk__mutmut_36": x_run_risk__mutmut_36,
    "x_run_risk__mutmut_37": x_run_risk__mutmut_37,
    "x_run_risk__mutmut_38": x_run_risk__mutmut_38,
    "x_run_risk__mutmut_39": x_run_risk__mutmut_39,
    "x_run_risk__mutmut_40": x_run_risk__mutmut_40,
    "x_run_risk__mutmut_41": x_run_risk__mutmut_41,
    "x_run_risk__mutmut_42": x_run_risk__mutmut_42,
    "x_run_risk__mutmut_43": x_run_risk__mutmut_43,
    "x_run_risk__mutmut_44": x_run_risk__mutmut_44,
    "x_run_risk__mutmut_45": x_run_risk__mutmut_45,
    "x_run_risk__mutmut_46": x_run_risk__mutmut_46,
    "x_run_risk__mutmut_47": x_run_risk__mutmut_47,
    "x_run_risk__mutmut_48": x_run_risk__mutmut_48,
    "x_run_risk__mutmut_49": x_run_risk__mutmut_49,
    "x_run_risk__mutmut_50": x_run_risk__mutmut_50,
    "x_run_risk__mutmut_51": x_run_risk__mutmut_51,
    "x_run_risk__mutmut_52": x_run_risk__mutmut_52,
    "x_run_risk__mutmut_53": x_run_risk__mutmut_53,
    "x_run_risk__mutmut_54": x_run_risk__mutmut_54,
    "x_run_risk__mutmut_55": x_run_risk__mutmut_55,
    "x_run_risk__mutmut_56": x_run_risk__mutmut_56,
    "x_run_risk__mutmut_57": x_run_risk__mutmut_57,
    "x_run_risk__mutmut_58": x_run_risk__mutmut_58,
    "x_run_risk__mutmut_59": x_run_risk__mutmut_59,
    "x_run_risk__mutmut_60": x_run_risk__mutmut_60,
    "x_run_risk__mutmut_61": x_run_risk__mutmut_61,
    "x_run_risk__mutmut_62": x_run_risk__mutmut_62,
    "x_run_risk__mutmut_63": x_run_risk__mutmut_63,
    "x_run_risk__mutmut_64": x_run_risk__mutmut_64,
    "x_run_risk__mutmut_65": x_run_risk__mutmut_65,
    "x_run_risk__mutmut_66": x_run_risk__mutmut_66,
    "x_run_risk__mutmut_67": x_run_risk__mutmut_67,
    "x_run_risk__mutmut_68": x_run_risk__mutmut_68,
    "x_run_risk__mutmut_69": x_run_risk__mutmut_69,
    "x_run_risk__mutmut_70": x_run_risk__mutmut_70,
    "x_run_risk__mutmut_71": x_run_risk__mutmut_71,
    "x_run_risk__mutmut_72": x_run_risk__mutmut_72,
    "x_run_risk__mutmut_73": x_run_risk__mutmut_73,
    "x_run_risk__mutmut_74": x_run_risk__mutmut_74,
    "x_run_risk__mutmut_75": x_run_risk__mutmut_75,
    "x_run_risk__mutmut_76": x_run_risk__mutmut_76,
    "x_run_risk__mutmut_77": x_run_risk__mutmut_77,
    "x_run_risk__mutmut_78": x_run_risk__mutmut_78,
    "x_run_risk__mutmut_79": x_run_risk__mutmut_79,
    "x_run_risk__mutmut_80": x_run_risk__mutmut_80,
    "x_run_risk__mutmut_81": x_run_risk__mutmut_81,
    "x_run_risk__mutmut_82": x_run_risk__mutmut_82,
    "x_run_risk__mutmut_83": x_run_risk__mutmut_83,
    "x_run_risk__mutmut_84": x_run_risk__mutmut_84,
    "x_run_risk__mutmut_85": x_run_risk__mutmut_85,
    "x_run_risk__mutmut_86": x_run_risk__mutmut_86,
    "x_run_risk__mutmut_87": x_run_risk__mutmut_87,
    "x_run_risk__mutmut_88": x_run_risk__mutmut_88,
    "x_run_risk__mutmut_89": x_run_risk__mutmut_89,
    "x_run_risk__mutmut_90": x_run_risk__mutmut_90,
    "x_run_risk__mutmut_91": x_run_risk__mutmut_91,
    "x_run_risk__mutmut_92": x_run_risk__mutmut_92,
    "x_run_risk__mutmut_93": x_run_risk__mutmut_93,
    "x_run_risk__mutmut_94": x_run_risk__mutmut_94,
    "x_run_risk__mutmut_95": x_run_risk__mutmut_95,
    "x_run_risk__mutmut_96": x_run_risk__mutmut_96,
    "x_run_risk__mutmut_97": x_run_risk__mutmut_97,
    "x_run_risk__mutmut_98": x_run_risk__mutmut_98,
    "x_run_risk__mutmut_99": x_run_risk__mutmut_99,
    "x_run_risk__mutmut_100": x_run_risk__mutmut_100,
    "x_run_risk__mutmut_101": x_run_risk__mutmut_101,
    "x_run_risk__mutmut_102": x_run_risk__mutmut_102,
    "x_run_risk__mutmut_103": x_run_risk__mutmut_103,
    "x_run_risk__mutmut_104": x_run_risk__mutmut_104,
    "x_run_risk__mutmut_105": x_run_risk__mutmut_105,
    "x_run_risk__mutmut_106": x_run_risk__mutmut_106,
    "x_run_risk__mutmut_107": x_run_risk__mutmut_107,
    "x_run_risk__mutmut_108": x_run_risk__mutmut_108,
    "x_run_risk__mutmut_109": x_run_risk__mutmut_109,
    "x_run_risk__mutmut_110": x_run_risk__mutmut_110,
    "x_run_risk__mutmut_111": x_run_risk__mutmut_111,
}
x_run_risk__mutmut_orig.__name__ = "x_run_risk"
