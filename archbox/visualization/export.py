"""Export utilities for archbox visualizations.

Supports exporting matplotlib figures to PNG, SVG, PDF,
and Plotly figures to interactive HTML.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt


def export_png(
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


def export_svg(
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


def export_pdf(
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


def export_html(
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
