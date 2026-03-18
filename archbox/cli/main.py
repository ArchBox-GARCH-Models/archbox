"""Main entry point for archbox CLI."""

from __future__ import annotations

import argparse
import sys


def build_parser() -> argparse.ArgumentParser:
    """Build the main argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="archbox",
        description="ArchBox - ARCH/GARCH volatility models for financial time series",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version and exit",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- estimate ---
    est = subparsers.add_parser("estimate", help="Estimate a volatility model")
    est.add_argument(
        "--model",
        required=True,
        choices=[
            "garch",
            "egarch",
            "gjr",
            "aparch",
            "figarch",
            "igarch",
            "garch-m",
            "component",
            "har-rv",
        ],
        help="Model type",
    )
    est.add_argument("--data", required=True, help="Path to CSV data file")
    est.add_argument("--column", default="returns", help="Column name for returns")
    est.add_argument("--p", type=int, default=1, help="GARCH lag order")
    est.add_argument("--q", type=int, default=1, help="ARCH lag order")
    est.add_argument(
        "--dist",
        default="normal",
        choices=["normal", "student-t", "skewed-t", "ged"],
        help="Conditional distribution",
    )
    est.add_argument(
        "--mean",
        default="constant",
        choices=["constant", "zero"],
        help="Mean model",
    )
    est.add_argument("--variance-targeting", action="store_true", help="Use variance targeting")
    est.add_argument("--output", default="results.json", help="Output file path")

    # --- risk ---
    risk = subparsers.add_parser("risk", help="Compute risk measures (VaR, ES)")
    risk.add_argument(
        "--model",
        required=True,
        choices=[
            "garch",
            "egarch",
            "gjr",
            "aparch",
            "figarch",
            "igarch",
            "garch-m",
            "component",
        ],
        help="Model type",
    )
    risk.add_argument("--data", required=True, help="Path to CSV data file")
    risk.add_argument("--column", default="returns", help="Column name for returns")
    risk.add_argument("--p", type=int, default=1, help="GARCH lag order")
    risk.add_argument("--q", type=int, default=1, help="ARCH lag order")
    risk.add_argument(
        "--dist",
        default="normal",
        choices=["normal", "student-t", "skewed-t", "ged"],
        help="Conditional distribution",
    )
    risk.add_argument(
        "--var-method",
        default="parametric",
        choices=["parametric", "historical", "filtered-hs", "monte-carlo"],
        help="VaR computation method",
    )
    risk.add_argument("--alpha", type=float, default=0.05, help="Significance level")
    risk.add_argument("--output", default="risk.json", help="Output file path")

    # --- backtest ---
    bt = subparsers.add_parser("backtest", help="Backtest VaR model")
    bt.add_argument(
        "--model",
        required=True,
        choices=[
            "garch",
            "egarch",
            "gjr",
            "aparch",
            "figarch",
            "igarch",
            "garch-m",
            "component",
        ],
        help="Model type",
    )
    bt.add_argument("--data", required=True, help="Path to CSV data file")
    bt.add_argument("--column", default="returns", help="Column name for returns")
    bt.add_argument("--p", type=int, default=1, help="GARCH lag order")
    bt.add_argument("--q", type=int, default=1, help="ARCH lag order")
    bt.add_argument(
        "--dist",
        default="normal",
        choices=["normal", "student-t", "skewed-t", "ged"],
        help="Conditional distribution",
    )
    bt.add_argument("--alpha", type=float, default=0.05, help="Significance level")
    bt.add_argument("--window", type=int, default=250, help="Rolling window size")
    bt.add_argument("--output", default="backtest.json", help="Output file path")

    # --- regime ---
    reg = subparsers.add_parser("regime", help="Estimate regime-switching model")
    reg.add_argument(
        "--model",
        required=True,
        choices=["ms-mean", "ms-ar", "ms-var", "ms-garch"],
        help="Regime model type",
    )
    reg.add_argument("--data", required=True, help="Path to CSV data file")
    reg.add_argument("--column", default="returns", help="Column name for returns")
    reg.add_argument("--k-regimes", type=int, default=2, help="Number of regimes")
    reg.add_argument("--order", type=int, default=1, help="AR order")
    reg.add_argument(
        "--method",
        default="em",
        choices=["em", "mle"],
        help="Estimation method",
    )
    reg.add_argument("--output", default="regime.json", help="Output file path")

    return parser


def main(argv: list[str] | None = None) -> int:
    """Main entry point for the CLI.

    Parameters
    ----------
    argv : list[str], optional
        Command-line arguments. If None, uses sys.argv.

    Returns
    -------
    int
        Exit code (0 for success, 1 for error).
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.version:
        from archbox.__version__ import __version__

        print(f"archbox {__version__}")
        return 0

    if args.command is None:
        parser.print_help()
        return 0

    try:
        if args.command == "estimate":
            from archbox.cli.estimate import run_estimate

            run_estimate(args)
        elif args.command == "risk":
            from archbox.cli.risk import run_risk

            run_risk(args)
        elif args.command == "backtest":
            from archbox.cli.backtest import run_backtest

            run_backtest(args)
        elif args.command == "regime":
            from archbox.cli.regime import run_regime

            run_regime(args)
        else:
            parser.print_help()
            return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
