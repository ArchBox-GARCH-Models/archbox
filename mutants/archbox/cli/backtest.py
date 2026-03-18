"""CLI backtest command implementation."""

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


def run_backtest(args: argparse.Namespace) -> None:
    args = [args]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_run_backtest__mutmut_orig, x_run_backtest__mutmut_mutants, args, kwargs, None
    )


def x_run_backtest__mutmut_orig(args: argparse.Namespace) -> None:
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


def x_run_backtest__mutmut_1(args: argparse.Namespace) -> None:
    """Execute the backtest command.

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


def x_run_backtest__mutmut_2(args: argparse.Namespace) -> None:
    """Execute the backtest command.

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


def x_run_backtest__mutmut_3(args: argparse.Namespace) -> None:
    """Execute the backtest command.

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


def x_run_backtest__mutmut_4(args: argparse.Namespace) -> None:
    """Execute the backtest command.

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


def x_run_backtest__mutmut_5(args: argparse.Namespace) -> None:
    """Execute the backtest command.

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


def x_run_backtest__mutmut_6(args: argparse.Namespace) -> None:
    """Execute the backtest command.

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


def x_run_backtest__mutmut_7(args: argparse.Namespace) -> None:
    """Execute the backtest command.

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


def x_run_backtest__mutmut_8(args: argparse.Namespace) -> None:
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
    model = _build_model(None, returns, args)
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


def x_run_backtest__mutmut_9(args: argparse.Namespace) -> None:
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
    model = _build_model(args.model, None, args)
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


def x_run_backtest__mutmut_10(args: argparse.Namespace) -> None:
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
    model = _build_model(args.model, returns, None)
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


def x_run_backtest__mutmut_11(args: argparse.Namespace) -> None:
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
    model = _build_model(returns, args)
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


def x_run_backtest__mutmut_12(args: argparse.Namespace) -> None:
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
    model = _build_model(args.model, args)
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


def x_run_backtest__mutmut_13(args: argparse.Namespace) -> None:
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
    model = _build_model(
        args.model,
        returns,
    )
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


def x_run_backtest__mutmut_14(args: argparse.Namespace) -> None:
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
    print(None)
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


def x_run_backtest__mutmut_15(args: argparse.Namespace) -> None:
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
    print(f"Fitting {args.model.lower()}({args.p},{args.q}) with {args.dist} distribution...")
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


def x_run_backtest__mutmut_16(args: argparse.Namespace) -> None:
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
    results = None

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


def x_run_backtest__mutmut_17(args: argparse.Namespace) -> None:
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
    results = model.fit(disp=None)

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


def x_run_backtest__mutmut_18(args: argparse.Namespace) -> None:
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
    results = model.fit(disp=True)

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


def x_run_backtest__mutmut_19(args: argparse.Namespace) -> None:
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

    var_calculator = None
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


def x_run_backtest__mutmut_20(args: argparse.Namespace) -> None:
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

    var_calculator = ValueAtRisk(None, alpha=args.alpha)
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


def x_run_backtest__mutmut_21(args: argparse.Namespace) -> None:
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

    var_calculator = ValueAtRisk(results, alpha=None)
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


def x_run_backtest__mutmut_22(args: argparse.Namespace) -> None:
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

    var_calculator = ValueAtRisk(alpha=args.alpha)
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


def x_run_backtest__mutmut_23(args: argparse.Namespace) -> None:
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

    var_calculator = ValueAtRisk(
        results,
    )
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


def x_run_backtest__mutmut_24(args: argparse.Namespace) -> None:
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
    var_series = None

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


def x_run_backtest__mutmut_25(args: argparse.Namespace) -> None:
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

    window = None
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


def x_run_backtest__mutmut_26(args: argparse.Namespace) -> None:
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
    test_returns = None
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


def x_run_backtest__mutmut_27(args: argparse.Namespace) -> None:
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
    test_returns = returns[+window:]
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


def x_run_backtest__mutmut_28(args: argparse.Namespace) -> None:
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
    test_var = None

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


def x_run_backtest__mutmut_29(args: argparse.Namespace) -> None:
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
    test_var = var_series[+window:]

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


def x_run_backtest__mutmut_30(args: argparse.Namespace) -> None:
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

    window = args.window
    test_returns = returns[-window:]
    test_var = var_series[-window:]

    bt = None
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


def x_run_backtest__mutmut_31(args: argparse.Namespace) -> None:
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

    bt = VaRBacktest(None, test_var, alpha=args.alpha)
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


def x_run_backtest__mutmut_32(args: argparse.Namespace) -> None:
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

    bt = VaRBacktest(test_returns, None, alpha=args.alpha)
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


def x_run_backtest__mutmut_33(args: argparse.Namespace) -> None:
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

    bt = VaRBacktest(test_returns, test_var, alpha=None)
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


def x_run_backtest__mutmut_34(args: argparse.Namespace) -> None:
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

    bt = VaRBacktest(test_var, alpha=args.alpha)
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


def x_run_backtest__mutmut_35(args: argparse.Namespace) -> None:
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

    bt = VaRBacktest(test_returns, alpha=args.alpha)
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


def x_run_backtest__mutmut_36(args: argparse.Namespace) -> None:
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

    bt = VaRBacktest(
        test_returns,
        test_var,
    )
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


def x_run_backtest__mutmut_37(args: argparse.Namespace) -> None:
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
    kupiec = None
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


def x_run_backtest__mutmut_38(args: argparse.Namespace) -> None:
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
    christoffersen = None
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


def x_run_backtest__mutmut_39(args: argparse.Namespace) -> None:
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
    traffic_light = None
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


def x_run_backtest__mutmut_40(args: argparse.Namespace) -> None:
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
    violation_ratio = None
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


def x_run_backtest__mutmut_41(args: argparse.Namespace) -> None:
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
    num_violations = None

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


def x_run_backtest__mutmut_42(args: argparse.Namespace) -> None:
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
    num_violations = int(None)

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


def x_run_backtest__mutmut_43(args: argparse.Namespace) -> None:
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
    num_violations = int(np.sum(None))

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


def x_run_backtest__mutmut_44(args: argparse.Namespace) -> None:
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
    output = None

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nViolation ratio: {violation_ratio:.4f}")
    print(f"Kupiec test p-value: {kupiec.pvalue:.4f}")
    print(f"Traffic light: {traffic_light}")
    print(f"Results saved to {output_path}")


def x_run_backtest__mutmut_45(args: argparse.Namespace) -> None:
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
        "XXmodelXX": args.model,
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


def x_run_backtest__mutmut_46(args: argparse.Namespace) -> None:
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
        "MODEL": args.model,
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


def x_run_backtest__mutmut_47(args: argparse.Namespace) -> None:
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
        "XXalphaXX": args.alpha,
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


def x_run_backtest__mutmut_48(args: argparse.Namespace) -> None:
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
        "ALPHA": args.alpha,
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


def x_run_backtest__mutmut_49(args: argparse.Namespace) -> None:
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
        "XXwindowXX": window,
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


def x_run_backtest__mutmut_50(args: argparse.Namespace) -> None:
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
        "WINDOW": window,
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


def x_run_backtest__mutmut_51(args: argparse.Namespace) -> None:
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
        "XXviolationsXX": num_violations,
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


def x_run_backtest__mutmut_52(args: argparse.Namespace) -> None:
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
        "VIOLATIONS": num_violations,
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


def x_run_backtest__mutmut_53(args: argparse.Namespace) -> None:
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
        "XXexpected_violationsXX": float(window * args.alpha),
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


def x_run_backtest__mutmut_54(args: argparse.Namespace) -> None:
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
        "EXPECTED_VIOLATIONS": float(window * args.alpha),
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


def x_run_backtest__mutmut_55(args: argparse.Namespace) -> None:
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
        "expected_violations": float(None),
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


def x_run_backtest__mutmut_56(args: argparse.Namespace) -> None:
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
        "expected_violations": float(window / args.alpha),
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


def x_run_backtest__mutmut_57(args: argparse.Namespace) -> None:
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
        "XXviolation_ratioXX": float(violation_ratio),
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


def x_run_backtest__mutmut_58(args: argparse.Namespace) -> None:
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
        "VIOLATION_RATIO": float(violation_ratio),
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


def x_run_backtest__mutmut_59(args: argparse.Namespace) -> None:
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
        "violation_ratio": float(None),
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


def x_run_backtest__mutmut_60(args: argparse.Namespace) -> None:
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
        "XXkupiecXX": {
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


def x_run_backtest__mutmut_61(args: argparse.Namespace) -> None:
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
        "KUPIEC": {
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


def x_run_backtest__mutmut_62(args: argparse.Namespace) -> None:
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
            "XXstatisticXX": float(kupiec.statistic),
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


def x_run_backtest__mutmut_63(args: argparse.Namespace) -> None:
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
            "STATISTIC": float(kupiec.statistic),
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


def x_run_backtest__mutmut_64(args: argparse.Namespace) -> None:
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
            "statistic": float(None),
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


def x_run_backtest__mutmut_65(args: argparse.Namespace) -> None:
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
            "XXpvalueXX": float(kupiec.pvalue),
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


def x_run_backtest__mutmut_66(args: argparse.Namespace) -> None:
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
            "PVALUE": float(kupiec.pvalue),
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


def x_run_backtest__mutmut_67(args: argparse.Namespace) -> None:
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
            "pvalue": float(None),
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


def x_run_backtest__mutmut_68(args: argparse.Namespace) -> None:
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
            "XXrejectXX": bool(kupiec.pvalue < 0.05),
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


def x_run_backtest__mutmut_69(args: argparse.Namespace) -> None:
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
            "REJECT": bool(kupiec.pvalue < 0.05),
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


def x_run_backtest__mutmut_70(args: argparse.Namespace) -> None:
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
            "reject": bool(None),
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


def x_run_backtest__mutmut_71(args: argparse.Namespace) -> None:
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
            "reject": bool(kupiec.pvalue <= 0.05),
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


def x_run_backtest__mutmut_72(args: argparse.Namespace) -> None:
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
            "reject": bool(kupiec.pvalue < 1.05),
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


def x_run_backtest__mutmut_73(args: argparse.Namespace) -> None:
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
        "XXchristoffersenXX": {
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


def x_run_backtest__mutmut_74(args: argparse.Namespace) -> None:
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
        "CHRISTOFFERSEN": {
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


def x_run_backtest__mutmut_75(args: argparse.Namespace) -> None:
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
            "XXstatisticXX": float(christoffersen.statistic),
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


def x_run_backtest__mutmut_76(args: argparse.Namespace) -> None:
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
            "STATISTIC": float(christoffersen.statistic),
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


def x_run_backtest__mutmut_77(args: argparse.Namespace) -> None:
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
            "statistic": float(None),
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


def x_run_backtest__mutmut_78(args: argparse.Namespace) -> None:
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
            "XXpvalueXX": float(christoffersen.pvalue),
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


def x_run_backtest__mutmut_79(args: argparse.Namespace) -> None:
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
            "PVALUE": float(christoffersen.pvalue),
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


def x_run_backtest__mutmut_80(args: argparse.Namespace) -> None:
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
            "pvalue": float(None),
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


def x_run_backtest__mutmut_81(args: argparse.Namespace) -> None:
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
            "XXrejectXX": bool(christoffersen.pvalue < 0.05),
        },
        "traffic_light": traffic_light,
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nViolation ratio: {violation_ratio:.4f}")
    print(f"Kupiec test p-value: {kupiec.pvalue:.4f}")
    print(f"Traffic light: {traffic_light}")
    print(f"Results saved to {output_path}")


def x_run_backtest__mutmut_82(args: argparse.Namespace) -> None:
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
            "REJECT": bool(christoffersen.pvalue < 0.05),
        },
        "traffic_light": traffic_light,
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nViolation ratio: {violation_ratio:.4f}")
    print(f"Kupiec test p-value: {kupiec.pvalue:.4f}")
    print(f"Traffic light: {traffic_light}")
    print(f"Results saved to {output_path}")


def x_run_backtest__mutmut_83(args: argparse.Namespace) -> None:
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
            "reject": bool(None),
        },
        "traffic_light": traffic_light,
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nViolation ratio: {violation_ratio:.4f}")
    print(f"Kupiec test p-value: {kupiec.pvalue:.4f}")
    print(f"Traffic light: {traffic_light}")
    print(f"Results saved to {output_path}")


def x_run_backtest__mutmut_84(args: argparse.Namespace) -> None:
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
            "reject": bool(christoffersen.pvalue <= 0.05),
        },
        "traffic_light": traffic_light,
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nViolation ratio: {violation_ratio:.4f}")
    print(f"Kupiec test p-value: {kupiec.pvalue:.4f}")
    print(f"Traffic light: {traffic_light}")
    print(f"Results saved to {output_path}")


def x_run_backtest__mutmut_85(args: argparse.Namespace) -> None:
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
            "reject": bool(christoffersen.pvalue < 1.05),
        },
        "traffic_light": traffic_light,
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nViolation ratio: {violation_ratio:.4f}")
    print(f"Kupiec test p-value: {kupiec.pvalue:.4f}")
    print(f"Traffic light: {traffic_light}")
    print(f"Results saved to {output_path}")


def x_run_backtest__mutmut_86(args: argparse.Namespace) -> None:
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
        "XXtraffic_lightXX": traffic_light,
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nViolation ratio: {violation_ratio:.4f}")
    print(f"Kupiec test p-value: {kupiec.pvalue:.4f}")
    print(f"Traffic light: {traffic_light}")
    print(f"Results saved to {output_path}")


def x_run_backtest__mutmut_87(args: argparse.Namespace) -> None:
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
        "TRAFFIC_LIGHT": traffic_light,
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nViolation ratio: {violation_ratio:.4f}")
    print(f"Kupiec test p-value: {kupiec.pvalue:.4f}")
    print(f"Traffic light: {traffic_light}")
    print(f"Results saved to {output_path}")


def x_run_backtest__mutmut_88(args: argparse.Namespace) -> None:
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

    output_path = None
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nViolation ratio: {violation_ratio:.4f}")
    print(f"Kupiec test p-value: {kupiec.pvalue:.4f}")
    print(f"Traffic light: {traffic_light}")
    print(f"Results saved to {output_path}")


def x_run_backtest__mutmut_89(args: argparse.Namespace) -> None:
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

    output_path = Path(None)
    output_path.write_text(json.dumps(output, indent=2))
    print(f"\nViolation ratio: {violation_ratio:.4f}")
    print(f"Kupiec test p-value: {kupiec.pvalue:.4f}")
    print(f"Traffic light: {traffic_light}")
    print(f"Results saved to {output_path}")


def x_run_backtest__mutmut_90(args: argparse.Namespace) -> None:
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
    output_path.write_text(None)
    print(f"\nViolation ratio: {violation_ratio:.4f}")
    print(f"Kupiec test p-value: {kupiec.pvalue:.4f}")
    print(f"Traffic light: {traffic_light}")
    print(f"Results saved to {output_path}")


def x_run_backtest__mutmut_91(args: argparse.Namespace) -> None:
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
    output_path.write_text(json.dumps(None, indent=2))
    print(f"\nViolation ratio: {violation_ratio:.4f}")
    print(f"Kupiec test p-value: {kupiec.pvalue:.4f}")
    print(f"Traffic light: {traffic_light}")
    print(f"Results saved to {output_path}")


def x_run_backtest__mutmut_92(args: argparse.Namespace) -> None:
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
    output_path.write_text(json.dumps(output, indent=None))
    print(f"\nViolation ratio: {violation_ratio:.4f}")
    print(f"Kupiec test p-value: {kupiec.pvalue:.4f}")
    print(f"Traffic light: {traffic_light}")
    print(f"Results saved to {output_path}")


def x_run_backtest__mutmut_93(args: argparse.Namespace) -> None:
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
    output_path.write_text(json.dumps(indent=2))
    print(f"\nViolation ratio: {violation_ratio:.4f}")
    print(f"Kupiec test p-value: {kupiec.pvalue:.4f}")
    print(f"Traffic light: {traffic_light}")
    print(f"Results saved to {output_path}")


def x_run_backtest__mutmut_94(args: argparse.Namespace) -> None:
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
    output_path.write_text(
        json.dumps(
            output,
        )
    )
    print(f"\nViolation ratio: {violation_ratio:.4f}")
    print(f"Kupiec test p-value: {kupiec.pvalue:.4f}")
    print(f"Traffic light: {traffic_light}")
    print(f"Results saved to {output_path}")


def x_run_backtest__mutmut_95(args: argparse.Namespace) -> None:
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
    output_path.write_text(json.dumps(output, indent=3))
    print(f"\nViolation ratio: {violation_ratio:.4f}")
    print(f"Kupiec test p-value: {kupiec.pvalue:.4f}")
    print(f"Traffic light: {traffic_light}")
    print(f"Results saved to {output_path}")


def x_run_backtest__mutmut_96(args: argparse.Namespace) -> None:
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
    print(None)
    print(f"Kupiec test p-value: {kupiec.pvalue:.4f}")
    print(f"Traffic light: {traffic_light}")
    print(f"Results saved to {output_path}")


def x_run_backtest__mutmut_97(args: argparse.Namespace) -> None:
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
    print(None)
    print(f"Traffic light: {traffic_light}")
    print(f"Results saved to {output_path}")


def x_run_backtest__mutmut_98(args: argparse.Namespace) -> None:
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
    print(None)
    print(f"Results saved to {output_path}")


def x_run_backtest__mutmut_99(args: argparse.Namespace) -> None:
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
    print(None)


x_run_backtest__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_run_backtest__mutmut_1": x_run_backtest__mutmut_1,
    "x_run_backtest__mutmut_2": x_run_backtest__mutmut_2,
    "x_run_backtest__mutmut_3": x_run_backtest__mutmut_3,
    "x_run_backtest__mutmut_4": x_run_backtest__mutmut_4,
    "x_run_backtest__mutmut_5": x_run_backtest__mutmut_5,
    "x_run_backtest__mutmut_6": x_run_backtest__mutmut_6,
    "x_run_backtest__mutmut_7": x_run_backtest__mutmut_7,
    "x_run_backtest__mutmut_8": x_run_backtest__mutmut_8,
    "x_run_backtest__mutmut_9": x_run_backtest__mutmut_9,
    "x_run_backtest__mutmut_10": x_run_backtest__mutmut_10,
    "x_run_backtest__mutmut_11": x_run_backtest__mutmut_11,
    "x_run_backtest__mutmut_12": x_run_backtest__mutmut_12,
    "x_run_backtest__mutmut_13": x_run_backtest__mutmut_13,
    "x_run_backtest__mutmut_14": x_run_backtest__mutmut_14,
    "x_run_backtest__mutmut_15": x_run_backtest__mutmut_15,
    "x_run_backtest__mutmut_16": x_run_backtest__mutmut_16,
    "x_run_backtest__mutmut_17": x_run_backtest__mutmut_17,
    "x_run_backtest__mutmut_18": x_run_backtest__mutmut_18,
    "x_run_backtest__mutmut_19": x_run_backtest__mutmut_19,
    "x_run_backtest__mutmut_20": x_run_backtest__mutmut_20,
    "x_run_backtest__mutmut_21": x_run_backtest__mutmut_21,
    "x_run_backtest__mutmut_22": x_run_backtest__mutmut_22,
    "x_run_backtest__mutmut_23": x_run_backtest__mutmut_23,
    "x_run_backtest__mutmut_24": x_run_backtest__mutmut_24,
    "x_run_backtest__mutmut_25": x_run_backtest__mutmut_25,
    "x_run_backtest__mutmut_26": x_run_backtest__mutmut_26,
    "x_run_backtest__mutmut_27": x_run_backtest__mutmut_27,
    "x_run_backtest__mutmut_28": x_run_backtest__mutmut_28,
    "x_run_backtest__mutmut_29": x_run_backtest__mutmut_29,
    "x_run_backtest__mutmut_30": x_run_backtest__mutmut_30,
    "x_run_backtest__mutmut_31": x_run_backtest__mutmut_31,
    "x_run_backtest__mutmut_32": x_run_backtest__mutmut_32,
    "x_run_backtest__mutmut_33": x_run_backtest__mutmut_33,
    "x_run_backtest__mutmut_34": x_run_backtest__mutmut_34,
    "x_run_backtest__mutmut_35": x_run_backtest__mutmut_35,
    "x_run_backtest__mutmut_36": x_run_backtest__mutmut_36,
    "x_run_backtest__mutmut_37": x_run_backtest__mutmut_37,
    "x_run_backtest__mutmut_38": x_run_backtest__mutmut_38,
    "x_run_backtest__mutmut_39": x_run_backtest__mutmut_39,
    "x_run_backtest__mutmut_40": x_run_backtest__mutmut_40,
    "x_run_backtest__mutmut_41": x_run_backtest__mutmut_41,
    "x_run_backtest__mutmut_42": x_run_backtest__mutmut_42,
    "x_run_backtest__mutmut_43": x_run_backtest__mutmut_43,
    "x_run_backtest__mutmut_44": x_run_backtest__mutmut_44,
    "x_run_backtest__mutmut_45": x_run_backtest__mutmut_45,
    "x_run_backtest__mutmut_46": x_run_backtest__mutmut_46,
    "x_run_backtest__mutmut_47": x_run_backtest__mutmut_47,
    "x_run_backtest__mutmut_48": x_run_backtest__mutmut_48,
    "x_run_backtest__mutmut_49": x_run_backtest__mutmut_49,
    "x_run_backtest__mutmut_50": x_run_backtest__mutmut_50,
    "x_run_backtest__mutmut_51": x_run_backtest__mutmut_51,
    "x_run_backtest__mutmut_52": x_run_backtest__mutmut_52,
    "x_run_backtest__mutmut_53": x_run_backtest__mutmut_53,
    "x_run_backtest__mutmut_54": x_run_backtest__mutmut_54,
    "x_run_backtest__mutmut_55": x_run_backtest__mutmut_55,
    "x_run_backtest__mutmut_56": x_run_backtest__mutmut_56,
    "x_run_backtest__mutmut_57": x_run_backtest__mutmut_57,
    "x_run_backtest__mutmut_58": x_run_backtest__mutmut_58,
    "x_run_backtest__mutmut_59": x_run_backtest__mutmut_59,
    "x_run_backtest__mutmut_60": x_run_backtest__mutmut_60,
    "x_run_backtest__mutmut_61": x_run_backtest__mutmut_61,
    "x_run_backtest__mutmut_62": x_run_backtest__mutmut_62,
    "x_run_backtest__mutmut_63": x_run_backtest__mutmut_63,
    "x_run_backtest__mutmut_64": x_run_backtest__mutmut_64,
    "x_run_backtest__mutmut_65": x_run_backtest__mutmut_65,
    "x_run_backtest__mutmut_66": x_run_backtest__mutmut_66,
    "x_run_backtest__mutmut_67": x_run_backtest__mutmut_67,
    "x_run_backtest__mutmut_68": x_run_backtest__mutmut_68,
    "x_run_backtest__mutmut_69": x_run_backtest__mutmut_69,
    "x_run_backtest__mutmut_70": x_run_backtest__mutmut_70,
    "x_run_backtest__mutmut_71": x_run_backtest__mutmut_71,
    "x_run_backtest__mutmut_72": x_run_backtest__mutmut_72,
    "x_run_backtest__mutmut_73": x_run_backtest__mutmut_73,
    "x_run_backtest__mutmut_74": x_run_backtest__mutmut_74,
    "x_run_backtest__mutmut_75": x_run_backtest__mutmut_75,
    "x_run_backtest__mutmut_76": x_run_backtest__mutmut_76,
    "x_run_backtest__mutmut_77": x_run_backtest__mutmut_77,
    "x_run_backtest__mutmut_78": x_run_backtest__mutmut_78,
    "x_run_backtest__mutmut_79": x_run_backtest__mutmut_79,
    "x_run_backtest__mutmut_80": x_run_backtest__mutmut_80,
    "x_run_backtest__mutmut_81": x_run_backtest__mutmut_81,
    "x_run_backtest__mutmut_82": x_run_backtest__mutmut_82,
    "x_run_backtest__mutmut_83": x_run_backtest__mutmut_83,
    "x_run_backtest__mutmut_84": x_run_backtest__mutmut_84,
    "x_run_backtest__mutmut_85": x_run_backtest__mutmut_85,
    "x_run_backtest__mutmut_86": x_run_backtest__mutmut_86,
    "x_run_backtest__mutmut_87": x_run_backtest__mutmut_87,
    "x_run_backtest__mutmut_88": x_run_backtest__mutmut_88,
    "x_run_backtest__mutmut_89": x_run_backtest__mutmut_89,
    "x_run_backtest__mutmut_90": x_run_backtest__mutmut_90,
    "x_run_backtest__mutmut_91": x_run_backtest__mutmut_91,
    "x_run_backtest__mutmut_92": x_run_backtest__mutmut_92,
    "x_run_backtest__mutmut_93": x_run_backtest__mutmut_93,
    "x_run_backtest__mutmut_94": x_run_backtest__mutmut_94,
    "x_run_backtest__mutmut_95": x_run_backtest__mutmut_95,
    "x_run_backtest__mutmut_96": x_run_backtest__mutmut_96,
    "x_run_backtest__mutmut_97": x_run_backtest__mutmut_97,
    "x_run_backtest__mutmut_98": x_run_backtest__mutmut_98,
    "x_run_backtest__mutmut_99": x_run_backtest__mutmut_99,
}
x_run_backtest__mutmut_orig.__name__ = "x_run_backtest"
