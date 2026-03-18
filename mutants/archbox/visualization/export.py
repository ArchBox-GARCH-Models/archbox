"""Export utilities for archbox visualizations.

Supports exporting matplotlib figures to PNG, SVG, PDF,
and Plotly figures to interactive HTML.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Annotated, Any, ClassVar

import matplotlib.pyplot as plt

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


def export_png(
    fig: Any,
    filepath: str | Path,
    dpi: int = 150,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    args = [fig, filepath, dpi, transparent, bbox_inches]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_export_png__mutmut_orig, x_export_png__mutmut_mutants, args, kwargs, None
    )


def x_export_png__mutmut_orig(
    fig: Any,
    filepath: str | Path,
    dpi: int = 150,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PNG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    dpi : int
        Resolution in dots per inch.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="png", dpi=dpi, transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_png__mutmut_1(
    fig: Any,
    filepath: str | Path,
    dpi: int = 151,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PNG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    dpi : int
        Resolution in dots per inch.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="png", dpi=dpi, transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_png__mutmut_2(
    fig: Any,
    filepath: str | Path,
    dpi: int = 150,
    transparent: bool = True,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PNG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    dpi : int
        Resolution in dots per inch.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="png", dpi=dpi, transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_png__mutmut_3(
    fig: Any,
    filepath: str | Path,
    dpi: int = 150,
    transparent: bool = False,
    bbox_inches: str = "XXtightXX",
) -> Path:
    """Export a matplotlib figure to PNG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    dpi : int
        Resolution in dots per inch.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="png", dpi=dpi, transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_png__mutmut_4(
    fig: Any,
    filepath: str | Path,
    dpi: int = 150,
    transparent: bool = False,
    bbox_inches: str = "TIGHT",
) -> Path:
    """Export a matplotlib figure to PNG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    dpi : int
        Resolution in dots per inch.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="png", dpi=dpi, transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_png__mutmut_5(
    fig: Any,
    filepath: str | Path,
    dpi: int = 150,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PNG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    dpi : int
        Resolution in dots per inch.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = None
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="png", dpi=dpi, transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_png__mutmut_6(
    fig: Any,
    filepath: str | Path,
    dpi: int = 150,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PNG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    dpi : int
        Resolution in dots per inch.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(None)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="png", dpi=dpi, transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_png__mutmut_7(
    fig: Any,
    filepath: str | Path,
    dpi: int = 150,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PNG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    dpi : int
        Resolution in dots per inch.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=None, exist_ok=True)
    fig.savefig(filepath, format="png", dpi=dpi, transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_png__mutmut_8(
    fig: Any,
    filepath: str | Path,
    dpi: int = 150,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PNG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    dpi : int
        Resolution in dots per inch.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=None)
    fig.savefig(filepath, format="png", dpi=dpi, transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_png__mutmut_9(
    fig: Any,
    filepath: str | Path,
    dpi: int = 150,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PNG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    dpi : int
        Resolution in dots per inch.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(exist_ok=True)
    fig.savefig(filepath, format="png", dpi=dpi, transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_png__mutmut_10(
    fig: Any,
    filepath: str | Path,
    dpi: int = 150,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PNG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    dpi : int
        Resolution in dots per inch.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(
        parents=True,
    )
    fig.savefig(filepath, format="png", dpi=dpi, transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_png__mutmut_11(
    fig: Any,
    filepath: str | Path,
    dpi: int = 150,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PNG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    dpi : int
        Resolution in dots per inch.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=False, exist_ok=True)
    fig.savefig(filepath, format="png", dpi=dpi, transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_png__mutmut_12(
    fig: Any,
    filepath: str | Path,
    dpi: int = 150,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PNG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    dpi : int
        Resolution in dots per inch.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=False)
    fig.savefig(filepath, format="png", dpi=dpi, transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_png__mutmut_13(
    fig: Any,
    filepath: str | Path,
    dpi: int = 150,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PNG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    dpi : int
        Resolution in dots per inch.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(None, format="png", dpi=dpi, transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_png__mutmut_14(
    fig: Any,
    filepath: str | Path,
    dpi: int = 150,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PNG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    dpi : int
        Resolution in dots per inch.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format=None, dpi=dpi, transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_png__mutmut_15(
    fig: Any,
    filepath: str | Path,
    dpi: int = 150,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PNG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    dpi : int
        Resolution in dots per inch.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="png", dpi=None, transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_png__mutmut_16(
    fig: Any,
    filepath: str | Path,
    dpi: int = 150,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PNG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    dpi : int
        Resolution in dots per inch.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="png", dpi=dpi, transparent=None, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_png__mutmut_17(
    fig: Any,
    filepath: str | Path,
    dpi: int = 150,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PNG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    dpi : int
        Resolution in dots per inch.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="png", dpi=dpi, transparent=transparent, bbox_inches=None)
    plt.close(fig)
    return filepath


def x_export_png__mutmut_18(
    fig: Any,
    filepath: str | Path,
    dpi: int = 150,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PNG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    dpi : int
        Resolution in dots per inch.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(format="png", dpi=dpi, transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_png__mutmut_19(
    fig: Any,
    filepath: str | Path,
    dpi: int = 150,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PNG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    dpi : int
        Resolution in dots per inch.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, dpi=dpi, transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_png__mutmut_20(
    fig: Any,
    filepath: str | Path,
    dpi: int = 150,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PNG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    dpi : int
        Resolution in dots per inch.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="png", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_png__mutmut_21(
    fig: Any,
    filepath: str | Path,
    dpi: int = 150,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PNG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    dpi : int
        Resolution in dots per inch.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="png", dpi=dpi, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_png__mutmut_22(
    fig: Any,
    filepath: str | Path,
    dpi: int = 150,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PNG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    dpi : int
        Resolution in dots per inch.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        filepath,
        format="png",
        dpi=dpi,
        transparent=transparent,
    )
    plt.close(fig)
    return filepath


def x_export_png__mutmut_23(
    fig: Any,
    filepath: str | Path,
    dpi: int = 150,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PNG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    dpi : int
        Resolution in dots per inch.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        filepath, format="XXpngXX", dpi=dpi, transparent=transparent, bbox_inches=bbox_inches
    )
    plt.close(fig)
    return filepath


def x_export_png__mutmut_24(
    fig: Any,
    filepath: str | Path,
    dpi: int = 150,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PNG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    dpi : int
        Resolution in dots per inch.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="PNG", dpi=dpi, transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_png__mutmut_25(
    fig: Any,
    filepath: str | Path,
    dpi: int = 150,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PNG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    dpi : int
        Resolution in dots per inch.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="png", dpi=dpi, transparent=transparent, bbox_inches=bbox_inches)
    plt.close(None)
    return filepath


x_export_png__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_export_png__mutmut_1": x_export_png__mutmut_1,
    "x_export_png__mutmut_2": x_export_png__mutmut_2,
    "x_export_png__mutmut_3": x_export_png__mutmut_3,
    "x_export_png__mutmut_4": x_export_png__mutmut_4,
    "x_export_png__mutmut_5": x_export_png__mutmut_5,
    "x_export_png__mutmut_6": x_export_png__mutmut_6,
    "x_export_png__mutmut_7": x_export_png__mutmut_7,
    "x_export_png__mutmut_8": x_export_png__mutmut_8,
    "x_export_png__mutmut_9": x_export_png__mutmut_9,
    "x_export_png__mutmut_10": x_export_png__mutmut_10,
    "x_export_png__mutmut_11": x_export_png__mutmut_11,
    "x_export_png__mutmut_12": x_export_png__mutmut_12,
    "x_export_png__mutmut_13": x_export_png__mutmut_13,
    "x_export_png__mutmut_14": x_export_png__mutmut_14,
    "x_export_png__mutmut_15": x_export_png__mutmut_15,
    "x_export_png__mutmut_16": x_export_png__mutmut_16,
    "x_export_png__mutmut_17": x_export_png__mutmut_17,
    "x_export_png__mutmut_18": x_export_png__mutmut_18,
    "x_export_png__mutmut_19": x_export_png__mutmut_19,
    "x_export_png__mutmut_20": x_export_png__mutmut_20,
    "x_export_png__mutmut_21": x_export_png__mutmut_21,
    "x_export_png__mutmut_22": x_export_png__mutmut_22,
    "x_export_png__mutmut_23": x_export_png__mutmut_23,
    "x_export_png__mutmut_24": x_export_png__mutmut_24,
    "x_export_png__mutmut_25": x_export_png__mutmut_25,
}
x_export_png__mutmut_orig.__name__ = "x_export_png"


def export_svg(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    args = [fig, filepath, transparent, bbox_inches]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_export_svg__mutmut_orig, x_export_svg__mutmut_mutants, args, kwargs, None
    )


def x_export_svg__mutmut_orig(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to SVG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="svg", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_svg__mutmut_1(
    fig: Any,
    filepath: str | Path,
    transparent: bool = True,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to SVG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="svg", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_svg__mutmut_2(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "XXtightXX",
) -> Path:
    """Export a matplotlib figure to SVG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="svg", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_svg__mutmut_3(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "TIGHT",
) -> Path:
    """Export a matplotlib figure to SVG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="svg", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_svg__mutmut_4(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to SVG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = None
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="svg", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_svg__mutmut_5(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to SVG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(None)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="svg", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_svg__mutmut_6(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to SVG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=None, exist_ok=True)
    fig.savefig(filepath, format="svg", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_svg__mutmut_7(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to SVG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=None)
    fig.savefig(filepath, format="svg", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_svg__mutmut_8(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to SVG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(exist_ok=True)
    fig.savefig(filepath, format="svg", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_svg__mutmut_9(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to SVG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(
        parents=True,
    )
    fig.savefig(filepath, format="svg", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_svg__mutmut_10(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to SVG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=False, exist_ok=True)
    fig.savefig(filepath, format="svg", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_svg__mutmut_11(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to SVG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=False)
    fig.savefig(filepath, format="svg", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_svg__mutmut_12(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to SVG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(None, format="svg", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_svg__mutmut_13(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to SVG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format=None, transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_svg__mutmut_14(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to SVG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="svg", transparent=None, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_svg__mutmut_15(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to SVG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="svg", transparent=transparent, bbox_inches=None)
    plt.close(fig)
    return filepath


def x_export_svg__mutmut_16(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to SVG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(format="svg", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_svg__mutmut_17(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to SVG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_svg__mutmut_18(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to SVG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="svg", bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_svg__mutmut_19(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to SVG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        filepath,
        format="svg",
        transparent=transparent,
    )
    plt.close(fig)
    return filepath


def x_export_svg__mutmut_20(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to SVG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="XXsvgXX", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_svg__mutmut_21(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to SVG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="SVG", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_svg__mutmut_22(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to SVG.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="svg", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(None)
    return filepath


x_export_svg__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_export_svg__mutmut_1": x_export_svg__mutmut_1,
    "x_export_svg__mutmut_2": x_export_svg__mutmut_2,
    "x_export_svg__mutmut_3": x_export_svg__mutmut_3,
    "x_export_svg__mutmut_4": x_export_svg__mutmut_4,
    "x_export_svg__mutmut_5": x_export_svg__mutmut_5,
    "x_export_svg__mutmut_6": x_export_svg__mutmut_6,
    "x_export_svg__mutmut_7": x_export_svg__mutmut_7,
    "x_export_svg__mutmut_8": x_export_svg__mutmut_8,
    "x_export_svg__mutmut_9": x_export_svg__mutmut_9,
    "x_export_svg__mutmut_10": x_export_svg__mutmut_10,
    "x_export_svg__mutmut_11": x_export_svg__mutmut_11,
    "x_export_svg__mutmut_12": x_export_svg__mutmut_12,
    "x_export_svg__mutmut_13": x_export_svg__mutmut_13,
    "x_export_svg__mutmut_14": x_export_svg__mutmut_14,
    "x_export_svg__mutmut_15": x_export_svg__mutmut_15,
    "x_export_svg__mutmut_16": x_export_svg__mutmut_16,
    "x_export_svg__mutmut_17": x_export_svg__mutmut_17,
    "x_export_svg__mutmut_18": x_export_svg__mutmut_18,
    "x_export_svg__mutmut_19": x_export_svg__mutmut_19,
    "x_export_svg__mutmut_20": x_export_svg__mutmut_20,
    "x_export_svg__mutmut_21": x_export_svg__mutmut_21,
    "x_export_svg__mutmut_22": x_export_svg__mutmut_22,
}
x_export_svg__mutmut_orig.__name__ = "x_export_svg"


def export_pdf(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    args = [fig, filepath, transparent, bbox_inches]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_export_pdf__mutmut_orig, x_export_pdf__mutmut_mutants, args, kwargs, None
    )


def x_export_pdf__mutmut_orig(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PDF.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="pdf", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_pdf__mutmut_1(
    fig: Any,
    filepath: str | Path,
    transparent: bool = True,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PDF.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="pdf", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_pdf__mutmut_2(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "XXtightXX",
) -> Path:
    """Export a matplotlib figure to PDF.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="pdf", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_pdf__mutmut_3(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "TIGHT",
) -> Path:
    """Export a matplotlib figure to PDF.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="pdf", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_pdf__mutmut_4(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PDF.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = None
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="pdf", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_pdf__mutmut_5(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PDF.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(None)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="pdf", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_pdf__mutmut_6(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PDF.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=None, exist_ok=True)
    fig.savefig(filepath, format="pdf", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_pdf__mutmut_7(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PDF.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=None)
    fig.savefig(filepath, format="pdf", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_pdf__mutmut_8(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PDF.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(exist_ok=True)
    fig.savefig(filepath, format="pdf", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_pdf__mutmut_9(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PDF.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(
        parents=True,
    )
    fig.savefig(filepath, format="pdf", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_pdf__mutmut_10(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PDF.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=False, exist_ok=True)
    fig.savefig(filepath, format="pdf", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_pdf__mutmut_11(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PDF.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=False)
    fig.savefig(filepath, format="pdf", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_pdf__mutmut_12(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PDF.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(None, format="pdf", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_pdf__mutmut_13(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PDF.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format=None, transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_pdf__mutmut_14(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PDF.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="pdf", transparent=None, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_pdf__mutmut_15(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PDF.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="pdf", transparent=transparent, bbox_inches=None)
    plt.close(fig)
    return filepath


def x_export_pdf__mutmut_16(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PDF.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(format="pdf", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_pdf__mutmut_17(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PDF.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_pdf__mutmut_18(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PDF.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="pdf", bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_pdf__mutmut_19(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PDF.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        filepath,
        format="pdf",
        transparent=transparent,
    )
    plt.close(fig)
    return filepath


def x_export_pdf__mutmut_20(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PDF.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="XXpdfXX", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_pdf__mutmut_21(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PDF.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="PDF", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(fig)
    return filepath


def x_export_pdf__mutmut_22(
    fig: Any,
    filepath: str | Path,
    transparent: bool = False,
    bbox_inches: str = "tight",
) -> Path:
    """Export a matplotlib figure to PDF.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to export.
    filepath : str or Path
        Output file path.
    transparent : bool
        If True, use transparent background.
    bbox_inches : str
        Bounding box option.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, format="pdf", transparent=transparent, bbox_inches=bbox_inches)
    plt.close(None)
    return filepath


x_export_pdf__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_export_pdf__mutmut_1": x_export_pdf__mutmut_1,
    "x_export_pdf__mutmut_2": x_export_pdf__mutmut_2,
    "x_export_pdf__mutmut_3": x_export_pdf__mutmut_3,
    "x_export_pdf__mutmut_4": x_export_pdf__mutmut_4,
    "x_export_pdf__mutmut_5": x_export_pdf__mutmut_5,
    "x_export_pdf__mutmut_6": x_export_pdf__mutmut_6,
    "x_export_pdf__mutmut_7": x_export_pdf__mutmut_7,
    "x_export_pdf__mutmut_8": x_export_pdf__mutmut_8,
    "x_export_pdf__mutmut_9": x_export_pdf__mutmut_9,
    "x_export_pdf__mutmut_10": x_export_pdf__mutmut_10,
    "x_export_pdf__mutmut_11": x_export_pdf__mutmut_11,
    "x_export_pdf__mutmut_12": x_export_pdf__mutmut_12,
    "x_export_pdf__mutmut_13": x_export_pdf__mutmut_13,
    "x_export_pdf__mutmut_14": x_export_pdf__mutmut_14,
    "x_export_pdf__mutmut_15": x_export_pdf__mutmut_15,
    "x_export_pdf__mutmut_16": x_export_pdf__mutmut_16,
    "x_export_pdf__mutmut_17": x_export_pdf__mutmut_17,
    "x_export_pdf__mutmut_18": x_export_pdf__mutmut_18,
    "x_export_pdf__mutmut_19": x_export_pdf__mutmut_19,
    "x_export_pdf__mutmut_20": x_export_pdf__mutmut_20,
    "x_export_pdf__mutmut_21": x_export_pdf__mutmut_21,
    "x_export_pdf__mutmut_22": x_export_pdf__mutmut_22,
}
x_export_pdf__mutmut_orig.__name__ = "x_export_pdf"


def export_html(
    fig: Any,
    filepath: str | Path,
    include_plotlyjs: bool | str = True,
    full_html: bool = True,
) -> Path:
    args = [fig, filepath, include_plotlyjs, full_html]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_export_html__mutmut_orig, x_export_html__mutmut_mutants, args, kwargs, None
    )


def x_export_html__mutmut_orig(
    fig: Any,
    filepath: str | Path,
    include_plotlyjs: bool | str = True,
    full_html: bool = True,
) -> Path:
    """Export a Plotly figure to interactive HTML.

    Parameters
    ----------
    fig : plotly.graph_objects.Figure
        The Plotly figure to export.
    filepath : str or Path
        Output file path.
    include_plotlyjs : bool or str
        Whether to include Plotly.js in the HTML.
        True = inline, 'cdn' = CDN link, False = omit.
    full_html : bool
        If True, generate a full HTML document.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(
        str(filepath),
        include_plotlyjs=include_plotlyjs,
        full_html=full_html,
    )
    return filepath


def x_export_html__mutmut_1(
    fig: Any,
    filepath: str | Path,
    include_plotlyjs: bool | str = False,
    full_html: bool = True,
) -> Path:
    """Export a Plotly figure to interactive HTML.

    Parameters
    ----------
    fig : plotly.graph_objects.Figure
        The Plotly figure to export.
    filepath : str or Path
        Output file path.
    include_plotlyjs : bool or str
        Whether to include Plotly.js in the HTML.
        True = inline, 'cdn' = CDN link, False = omit.
    full_html : bool
        If True, generate a full HTML document.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(
        str(filepath),
        include_plotlyjs=include_plotlyjs,
        full_html=full_html,
    )
    return filepath


def x_export_html__mutmut_2(
    fig: Any,
    filepath: str | Path,
    include_plotlyjs: bool | str = True,
    full_html: bool = False,
) -> Path:
    """Export a Plotly figure to interactive HTML.

    Parameters
    ----------
    fig : plotly.graph_objects.Figure
        The Plotly figure to export.
    filepath : str or Path
        Output file path.
    include_plotlyjs : bool or str
        Whether to include Plotly.js in the HTML.
        True = inline, 'cdn' = CDN link, False = omit.
    full_html : bool
        If True, generate a full HTML document.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(
        str(filepath),
        include_plotlyjs=include_plotlyjs,
        full_html=full_html,
    )
    return filepath


def x_export_html__mutmut_3(
    fig: Any,
    filepath: str | Path,
    include_plotlyjs: bool | str = True,
    full_html: bool = True,
) -> Path:
    """Export a Plotly figure to interactive HTML.

    Parameters
    ----------
    fig : plotly.graph_objects.Figure
        The Plotly figure to export.
    filepath : str or Path
        Output file path.
    include_plotlyjs : bool or str
        Whether to include Plotly.js in the HTML.
        True = inline, 'cdn' = CDN link, False = omit.
    full_html : bool
        If True, generate a full HTML document.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = None
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(
        str(filepath),
        include_plotlyjs=include_plotlyjs,
        full_html=full_html,
    )
    return filepath


def x_export_html__mutmut_4(
    fig: Any,
    filepath: str | Path,
    include_plotlyjs: bool | str = True,
    full_html: bool = True,
) -> Path:
    """Export a Plotly figure to interactive HTML.

    Parameters
    ----------
    fig : plotly.graph_objects.Figure
        The Plotly figure to export.
    filepath : str or Path
        Output file path.
    include_plotlyjs : bool or str
        Whether to include Plotly.js in the HTML.
        True = inline, 'cdn' = CDN link, False = omit.
    full_html : bool
        If True, generate a full HTML document.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(None)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(
        str(filepath),
        include_plotlyjs=include_plotlyjs,
        full_html=full_html,
    )
    return filepath


def x_export_html__mutmut_5(
    fig: Any,
    filepath: str | Path,
    include_plotlyjs: bool | str = True,
    full_html: bool = True,
) -> Path:
    """Export a Plotly figure to interactive HTML.

    Parameters
    ----------
    fig : plotly.graph_objects.Figure
        The Plotly figure to export.
    filepath : str or Path
        Output file path.
    include_plotlyjs : bool or str
        Whether to include Plotly.js in the HTML.
        True = inline, 'cdn' = CDN link, False = omit.
    full_html : bool
        If True, generate a full HTML document.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=None, exist_ok=True)
    fig.write_html(
        str(filepath),
        include_plotlyjs=include_plotlyjs,
        full_html=full_html,
    )
    return filepath


def x_export_html__mutmut_6(
    fig: Any,
    filepath: str | Path,
    include_plotlyjs: bool | str = True,
    full_html: bool = True,
) -> Path:
    """Export a Plotly figure to interactive HTML.

    Parameters
    ----------
    fig : plotly.graph_objects.Figure
        The Plotly figure to export.
    filepath : str or Path
        Output file path.
    include_plotlyjs : bool or str
        Whether to include Plotly.js in the HTML.
        True = inline, 'cdn' = CDN link, False = omit.
    full_html : bool
        If True, generate a full HTML document.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=None)
    fig.write_html(
        str(filepath),
        include_plotlyjs=include_plotlyjs,
        full_html=full_html,
    )
    return filepath


def x_export_html__mutmut_7(
    fig: Any,
    filepath: str | Path,
    include_plotlyjs: bool | str = True,
    full_html: bool = True,
) -> Path:
    """Export a Plotly figure to interactive HTML.

    Parameters
    ----------
    fig : plotly.graph_objects.Figure
        The Plotly figure to export.
    filepath : str or Path
        Output file path.
    include_plotlyjs : bool or str
        Whether to include Plotly.js in the HTML.
        True = inline, 'cdn' = CDN link, False = omit.
    full_html : bool
        If True, generate a full HTML document.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(exist_ok=True)
    fig.write_html(
        str(filepath),
        include_plotlyjs=include_plotlyjs,
        full_html=full_html,
    )
    return filepath


def x_export_html__mutmut_8(
    fig: Any,
    filepath: str | Path,
    include_plotlyjs: bool | str = True,
    full_html: bool = True,
) -> Path:
    """Export a Plotly figure to interactive HTML.

    Parameters
    ----------
    fig : plotly.graph_objects.Figure
        The Plotly figure to export.
    filepath : str or Path
        Output file path.
    include_plotlyjs : bool or str
        Whether to include Plotly.js in the HTML.
        True = inline, 'cdn' = CDN link, False = omit.
    full_html : bool
        If True, generate a full HTML document.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(
        parents=True,
    )
    fig.write_html(
        str(filepath),
        include_plotlyjs=include_plotlyjs,
        full_html=full_html,
    )
    return filepath


def x_export_html__mutmut_9(
    fig: Any,
    filepath: str | Path,
    include_plotlyjs: bool | str = True,
    full_html: bool = True,
) -> Path:
    """Export a Plotly figure to interactive HTML.

    Parameters
    ----------
    fig : plotly.graph_objects.Figure
        The Plotly figure to export.
    filepath : str or Path
        Output file path.
    include_plotlyjs : bool or str
        Whether to include Plotly.js in the HTML.
        True = inline, 'cdn' = CDN link, False = omit.
    full_html : bool
        If True, generate a full HTML document.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=False, exist_ok=True)
    fig.write_html(
        str(filepath),
        include_plotlyjs=include_plotlyjs,
        full_html=full_html,
    )
    return filepath


def x_export_html__mutmut_10(
    fig: Any,
    filepath: str | Path,
    include_plotlyjs: bool | str = True,
    full_html: bool = True,
) -> Path:
    """Export a Plotly figure to interactive HTML.

    Parameters
    ----------
    fig : plotly.graph_objects.Figure
        The Plotly figure to export.
    filepath : str or Path
        Output file path.
    include_plotlyjs : bool or str
        Whether to include Plotly.js in the HTML.
        True = inline, 'cdn' = CDN link, False = omit.
    full_html : bool
        If True, generate a full HTML document.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=False)
    fig.write_html(
        str(filepath),
        include_plotlyjs=include_plotlyjs,
        full_html=full_html,
    )
    return filepath


def x_export_html__mutmut_11(
    fig: Any,
    filepath: str | Path,
    include_plotlyjs: bool | str = True,
    full_html: bool = True,
) -> Path:
    """Export a Plotly figure to interactive HTML.

    Parameters
    ----------
    fig : plotly.graph_objects.Figure
        The Plotly figure to export.
    filepath : str or Path
        Output file path.
    include_plotlyjs : bool or str
        Whether to include Plotly.js in the HTML.
        True = inline, 'cdn' = CDN link, False = omit.
    full_html : bool
        If True, generate a full HTML document.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(
        None,
        include_plotlyjs=include_plotlyjs,
        full_html=full_html,
    )
    return filepath


def x_export_html__mutmut_12(
    fig: Any,
    filepath: str | Path,
    include_plotlyjs: bool | str = True,
    full_html: bool = True,
) -> Path:
    """Export a Plotly figure to interactive HTML.

    Parameters
    ----------
    fig : plotly.graph_objects.Figure
        The Plotly figure to export.
    filepath : str or Path
        Output file path.
    include_plotlyjs : bool or str
        Whether to include Plotly.js in the HTML.
        True = inline, 'cdn' = CDN link, False = omit.
    full_html : bool
        If True, generate a full HTML document.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(
        str(filepath),
        include_plotlyjs=None,
        full_html=full_html,
    )
    return filepath


def x_export_html__mutmut_13(
    fig: Any,
    filepath: str | Path,
    include_plotlyjs: bool | str = True,
    full_html: bool = True,
) -> Path:
    """Export a Plotly figure to interactive HTML.

    Parameters
    ----------
    fig : plotly.graph_objects.Figure
        The Plotly figure to export.
    filepath : str or Path
        Output file path.
    include_plotlyjs : bool or str
        Whether to include Plotly.js in the HTML.
        True = inline, 'cdn' = CDN link, False = omit.
    full_html : bool
        If True, generate a full HTML document.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(
        str(filepath),
        include_plotlyjs=include_plotlyjs,
        full_html=None,
    )
    return filepath


def x_export_html__mutmut_14(
    fig: Any,
    filepath: str | Path,
    include_plotlyjs: bool | str = True,
    full_html: bool = True,
) -> Path:
    """Export a Plotly figure to interactive HTML.

    Parameters
    ----------
    fig : plotly.graph_objects.Figure
        The Plotly figure to export.
    filepath : str or Path
        Output file path.
    include_plotlyjs : bool or str
        Whether to include Plotly.js in the HTML.
        True = inline, 'cdn' = CDN link, False = omit.
    full_html : bool
        If True, generate a full HTML document.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(
        include_plotlyjs=include_plotlyjs,
        full_html=full_html,
    )
    return filepath


def x_export_html__mutmut_15(
    fig: Any,
    filepath: str | Path,
    include_plotlyjs: bool | str = True,
    full_html: bool = True,
) -> Path:
    """Export a Plotly figure to interactive HTML.

    Parameters
    ----------
    fig : plotly.graph_objects.Figure
        The Plotly figure to export.
    filepath : str or Path
        Output file path.
    include_plotlyjs : bool or str
        Whether to include Plotly.js in the HTML.
        True = inline, 'cdn' = CDN link, False = omit.
    full_html : bool
        If True, generate a full HTML document.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(
        str(filepath),
        full_html=full_html,
    )
    return filepath


def x_export_html__mutmut_16(
    fig: Any,
    filepath: str | Path,
    include_plotlyjs: bool | str = True,
    full_html: bool = True,
) -> Path:
    """Export a Plotly figure to interactive HTML.

    Parameters
    ----------
    fig : plotly.graph_objects.Figure
        The Plotly figure to export.
    filepath : str or Path
        Output file path.
    include_plotlyjs : bool or str
        Whether to include Plotly.js in the HTML.
        True = inline, 'cdn' = CDN link, False = omit.
    full_html : bool
        If True, generate a full HTML document.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(
        str(filepath),
        include_plotlyjs=include_plotlyjs,
    )
    return filepath


def x_export_html__mutmut_17(
    fig: Any,
    filepath: str | Path,
    include_plotlyjs: bool | str = True,
    full_html: bool = True,
) -> Path:
    """Export a Plotly figure to interactive HTML.

    Parameters
    ----------
    fig : plotly.graph_objects.Figure
        The Plotly figure to export.
    filepath : str or Path
        Output file path.
    include_plotlyjs : bool or str
        Whether to include Plotly.js in the HTML.
        True = inline, 'cdn' = CDN link, False = omit.
    full_html : bool
        If True, generate a full HTML document.

    Returns
    -------
    Path
        The output file path.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(
        str(None),
        include_plotlyjs=include_plotlyjs,
        full_html=full_html,
    )
    return filepath


x_export_html__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_export_html__mutmut_1": x_export_html__mutmut_1,
    "x_export_html__mutmut_2": x_export_html__mutmut_2,
    "x_export_html__mutmut_3": x_export_html__mutmut_3,
    "x_export_html__mutmut_4": x_export_html__mutmut_4,
    "x_export_html__mutmut_5": x_export_html__mutmut_5,
    "x_export_html__mutmut_6": x_export_html__mutmut_6,
    "x_export_html__mutmut_7": x_export_html__mutmut_7,
    "x_export_html__mutmut_8": x_export_html__mutmut_8,
    "x_export_html__mutmut_9": x_export_html__mutmut_9,
    "x_export_html__mutmut_10": x_export_html__mutmut_10,
    "x_export_html__mutmut_11": x_export_html__mutmut_11,
    "x_export_html__mutmut_12": x_export_html__mutmut_12,
    "x_export_html__mutmut_13": x_export_html__mutmut_13,
    "x_export_html__mutmut_14": x_export_html__mutmut_14,
    "x_export_html__mutmut_15": x_export_html__mutmut_15,
    "x_export_html__mutmut_16": x_export_html__mutmut_16,
    "x_export_html__mutmut_17": x_export_html__mutmut_17,
}
x_export_html__mutmut_orig.__name__ = "x_export_html"
