"""Visual themes for archbox charts.

Provides predefined themes for different contexts:
- Professional: reports and internal publications
- Academic: papers and theses
- Presentation: slides and presentations
- Risk: risk management reports
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Annotated, Any, ClassVar

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


@dataclass
class Theme:
    """Visual theme configuration for charts.

    Parameters
    ----------
    name : str
        Theme name.
    colors : dict[str, str]
        Named colors (primary, secondary, accent, background, text, grid, etc.).
    font_family : str
        Primary font family.
    font_sizes : dict[str, int]
        Font sizes for title, label, tick, legend, annotation.
    line_widths : dict[str, float]
        Line widths for primary, secondary, grid, axis.
    figure_size : tuple[float, float]
        Default figure size (width, height) in inches.
    dpi : int
        Default DPI for raster export.
    grid_alpha : float
        Grid transparency (0-1).
    """

    name: str
    colors: dict[str, str] = field(default_factory=dict)
    font_family: str = "Helvetica"
    font_sizes: dict[str, int] = field(default_factory=dict)
    line_widths: dict[str, float] = field(default_factory=dict)
    figure_size: tuple[float, float] = (12, 8)
    dpi: int = 150
    grid_alpha: float = 0.3

    def to_matplotlib_rcparams(self) -> dict[str, Any]:
        """Convert theme to matplotlib rcParams dict."""
        return {
            "figure.figsize": self.figure_size,
            "figure.dpi": self.dpi,
            "font.family": self.font_family,
            "font.size": self.font_sizes.get("tick", 10),
            "axes.titlesize": self.font_sizes.get("title", 14),
            "axes.labelsize": self.font_sizes.get("label", 12),
            "legend.fontsize": self.font_sizes.get("legend", 10),
            "xtick.labelsize": self.font_sizes.get("tick", 10),
            "ytick.labelsize": self.font_sizes.get("tick", 10),
            "axes.grid": True,
            "grid.alpha": self.grid_alpha,
            "axes.facecolor": self.colors.get("background", "white"),
            "figure.facecolor": self.colors.get("background", "white"),
            "axes.edgecolor": self.colors.get("grid", "#cccccc"),
            "grid.color": self.colors.get("grid", "#cccccc"),
            "text.color": self.colors.get("text", "#333333"),
            "axes.labelcolor": self.colors.get("text", "#333333"),
            "xtick.color": self.colors.get("text", "#333333"),
            "ytick.color": self.colors.get("text", "#333333"),
            "lines.linewidth": self.line_widths.get("primary", 1.5),
            "axes.linewidth": self.line_widths.get("axis", 0.8),
        }

    def to_plotly_template(self) -> dict[str, Any]:
        """Convert theme to Plotly layout dict."""
        return {
            "font": {
                "family": self.font_family,
                "size": self.font_sizes.get("tick", 10),
                "color": self.colors.get("text", "#333333"),
            },
            "title": {
                "font": {
                    "size": self.font_sizes.get("title", 14),
                }
            },
            "plot_bgcolor": self.colors.get("background", "white"),
            "paper_bgcolor": self.colors.get("background", "white"),
            "xaxis": {
                "gridcolor": self.colors.get("grid", "#cccccc"),
                "gridwidth": self.line_widths.get("grid", 0.5),
            },
            "yaxis": {
                "gridcolor": self.colors.get("grid", "#cccccc"),
                "gridwidth": self.line_widths.get("grid", 0.5),
            },
        }


# --- Predefined Themes ---

PROFESSIONAL = Theme(
    name="professional",
    colors={
        "primary": "#1f4e79",
        "secondary": "#2e75b6",
        "accent": "#c00000",
        "positive": "#548235",
        "negative": "#c00000",
        "background": "#ffffff",
        "text": "#333333",
        "grid": "#d9d9d9",
        "volatility": "#2e75b6",
        "returns": "#7f7f7f",
        "residuals": "#548235",
        "var_line": "#c00000",
        "es_line": "#c00000",
        "confidence_band": "#2e75b6",
    },
    font_family="Helvetica",
    font_sizes={"title": 14, "label": 12, "tick": 10, "legend": 10, "annotation": 9},
    line_widths={"primary": 1.5, "secondary": 1.0, "grid": 0.5, "axis": 0.8},
    figure_size=(12, 8),
    dpi=150,
    grid_alpha=0.3,
)

ACADEMIC = Theme(
    name="academic",
    colors={
        "primary": "#000000",
        "secondary": "#555555",
        "accent": "#000000",
        "positive": "#333333",
        "negative": "#000000",
        "background": "#ffffff",
        "text": "#000000",
        "grid": "#cccccc",
        "volatility": "#000000",
        "returns": "#999999",
        "residuals": "#555555",
        "var_line": "#000000",
        "es_line": "#666666",
        "confidence_band": "#999999",
    },
    font_family="serif",
    font_sizes={"title": 12, "label": 11, "tick": 10, "legend": 9, "annotation": 8},
    line_widths={"primary": 1.2, "secondary": 0.8, "grid": 0.4, "axis": 0.6},
    figure_size=(10, 7),
    dpi=300,
    grid_alpha=0.2,
)

PRESENTATION = Theme(
    name="presentation",
    colors={
        "primary": "#0066cc",
        "secondary": "#ff6600",
        "accent": "#cc0000",
        "positive": "#00cc66",
        "negative": "#cc0000",
        "background": "#ffffff",
        "text": "#222222",
        "grid": "#e0e0e0",
        "volatility": "#0066cc",
        "returns": "#aaaaaa",
        "residuals": "#00cc66",
        "var_line": "#cc0000",
        "es_line": "#cc0000",
        "confidence_band": "#0066cc",
    },
    font_family="sans-serif",
    font_sizes={"title": 18, "label": 14, "tick": 12, "legend": 12, "annotation": 11},
    line_widths={"primary": 2.5, "secondary": 1.5, "grid": 0.5, "axis": 1.0},
    figure_size=(14, 9),
    dpi=100,
    grid_alpha=0.25,
)

RISK = Theme(
    name="risk",
    colors={
        "primary": "#c00000",
        "secondary": "#ffc000",
        "accent": "#c00000",
        "positive": "#548235",
        "negative": "#c00000",
        "background": "#ffffff",
        "text": "#333333",
        "grid": "#d9d9d9",
        "volatility": "#c00000",
        "returns": "#7f7f7f",
        "residuals": "#548235",
        "var_line": "#c00000",
        "es_line": "#ff6600",
        "confidence_band": "#ffc000",
        "zone_green": "#548235",
        "zone_yellow": "#ffc000",
        "zone_red": "#c00000",
    },
    font_family="Helvetica",
    font_sizes={"title": 14, "label": 12, "tick": 10, "legend": 10, "annotation": 9},
    line_widths={"primary": 1.5, "secondary": 1.0, "grid": 0.5, "axis": 0.8},
    figure_size=(12, 8),
    dpi=150,
    grid_alpha=0.3,
)

# Theme registry
_THEMES: dict[str, Theme] = {
    "professional": PROFESSIONAL,
    "academic": ACADEMIC,
    "presentation": PRESENTATION,
    "risk": RISK,
}


def get_theme(name: str = "professional") -> Theme:
    args = [name]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_get_theme__mutmut_orig, x_get_theme__mutmut_mutants, args, kwargs, None
    )


def x_get_theme__mutmut_orig(name: str = "professional") -> Theme:
    """Get a predefined theme by name.

    Parameters
    ----------
    name : str
        Theme name: 'professional', 'academic', 'presentation', 'risk'.

    Returns
    -------
    Theme
        The requested theme.

    Raises
    ------
    ValueError
        If theme name is not recognized.
    """
    if name not in _THEMES:
        available = ", ".join(sorted(_THEMES.keys()))
        msg = f"Unknown theme '{name}'. Available: {available}"
        raise ValueError(msg)
    return _THEMES[name]


def x_get_theme__mutmut_1(name: str = "XXprofessionalXX") -> Theme:
    """Get a predefined theme by name.

    Parameters
    ----------
    name : str
        Theme name: 'professional', 'academic', 'presentation', 'risk'.

    Returns
    -------
    Theme
        The requested theme.

    Raises
    ------
    ValueError
        If theme name is not recognized.
    """
    if name not in _THEMES:
        available = ", ".join(sorted(_THEMES.keys()))
        msg = f"Unknown theme '{name}'. Available: {available}"
        raise ValueError(msg)
    return _THEMES[name]


def x_get_theme__mutmut_2(name: str = "PROFESSIONAL") -> Theme:
    """Get a predefined theme by name.

    Parameters
    ----------
    name : str
        Theme name: 'professional', 'academic', 'presentation', 'risk'.

    Returns
    -------
    Theme
        The requested theme.

    Raises
    ------
    ValueError
        If theme name is not recognized.
    """
    if name not in _THEMES:
        available = ", ".join(sorted(_THEMES.keys()))
        msg = f"Unknown theme '{name}'. Available: {available}"
        raise ValueError(msg)
    return _THEMES[name]


def x_get_theme__mutmut_3(name: str = "professional") -> Theme:
    """Get a predefined theme by name.

    Parameters
    ----------
    name : str
        Theme name: 'professional', 'academic', 'presentation', 'risk'.

    Returns
    -------
    Theme
        The requested theme.

    Raises
    ------
    ValueError
        If theme name is not recognized.
    """
    if name in _THEMES:
        available = ", ".join(sorted(_THEMES.keys()))
        msg = f"Unknown theme '{name}'. Available: {available}"
        raise ValueError(msg)
    return _THEMES[name]


def x_get_theme__mutmut_4(name: str = "professional") -> Theme:
    """Get a predefined theme by name.

    Parameters
    ----------
    name : str
        Theme name: 'professional', 'academic', 'presentation', 'risk'.

    Returns
    -------
    Theme
        The requested theme.

    Raises
    ------
    ValueError
        If theme name is not recognized.
    """
    if name not in _THEMES:
        available = None
        msg = f"Unknown theme '{name}'. Available: {available}"
        raise ValueError(msg)
    return _THEMES[name]


def x_get_theme__mutmut_5(name: str = "professional") -> Theme:
    """Get a predefined theme by name.

    Parameters
    ----------
    name : str
        Theme name: 'professional', 'academic', 'presentation', 'risk'.

    Returns
    -------
    Theme
        The requested theme.

    Raises
    ------
    ValueError
        If theme name is not recognized.
    """
    if name not in _THEMES:
        available = ", ".join(None)
        msg = f"Unknown theme '{name}'. Available: {available}"
        raise ValueError(msg)
    return _THEMES[name]


def x_get_theme__mutmut_6(name: str = "professional") -> Theme:
    """Get a predefined theme by name.

    Parameters
    ----------
    name : str
        Theme name: 'professional', 'academic', 'presentation', 'risk'.

    Returns
    -------
    Theme
        The requested theme.

    Raises
    ------
    ValueError
        If theme name is not recognized.
    """
    if name not in _THEMES:
        available = "XX, XX".join(sorted(_THEMES.keys()))
        msg = f"Unknown theme '{name}'. Available: {available}"
        raise ValueError(msg)
    return _THEMES[name]


def x_get_theme__mutmut_7(name: str = "professional") -> Theme:
    """Get a predefined theme by name.

    Parameters
    ----------
    name : str
        Theme name: 'professional', 'academic', 'presentation', 'risk'.

    Returns
    -------
    Theme
        The requested theme.

    Raises
    ------
    ValueError
        If theme name is not recognized.
    """
    if name not in _THEMES:
        available = ", ".join(sorted(None))
        msg = f"Unknown theme '{name}'. Available: {available}"
        raise ValueError(msg)
    return _THEMES[name]


def x_get_theme__mutmut_8(name: str = "professional") -> Theme:
    """Get a predefined theme by name.

    Parameters
    ----------
    name : str
        Theme name: 'professional', 'academic', 'presentation', 'risk'.

    Returns
    -------
    Theme
        The requested theme.

    Raises
    ------
    ValueError
        If theme name is not recognized.
    """
    if name not in _THEMES:
        available = ", ".join(sorted(_THEMES.keys()))
        msg = None
        raise ValueError(msg)
    return _THEMES[name]


def x_get_theme__mutmut_9(name: str = "professional") -> Theme:
    """Get a predefined theme by name.

    Parameters
    ----------
    name : str
        Theme name: 'professional', 'academic', 'presentation', 'risk'.

    Returns
    -------
    Theme
        The requested theme.

    Raises
    ------
    ValueError
        If theme name is not recognized.
    """
    if name not in _THEMES:
        available = ", ".join(sorted(_THEMES.keys()))
        msg = f"Unknown theme '{name}'. Available: {available}"
        raise ValueError(None)
    return _THEMES[name]


x_get_theme__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_get_theme__mutmut_1": x_get_theme__mutmut_1,
    "x_get_theme__mutmut_2": x_get_theme__mutmut_2,
    "x_get_theme__mutmut_3": x_get_theme__mutmut_3,
    "x_get_theme__mutmut_4": x_get_theme__mutmut_4,
    "x_get_theme__mutmut_5": x_get_theme__mutmut_5,
    "x_get_theme__mutmut_6": x_get_theme__mutmut_6,
    "x_get_theme__mutmut_7": x_get_theme__mutmut_7,
    "x_get_theme__mutmut_8": x_get_theme__mutmut_8,
    "x_get_theme__mutmut_9": x_get_theme__mutmut_9,
}
x_get_theme__mutmut_orig.__name__ = "x_get_theme"


def list_themes() -> list[str]:
    args = []  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_list_themes__mutmut_orig, x_list_themes__mutmut_mutants, args, kwargs, None
    )


def x_list_themes__mutmut_orig() -> list[str]:
    """List available theme names."""
    return sorted(_THEMES.keys())


def x_list_themes__mutmut_1() -> list[str]:
    """List available theme names."""
    return sorted(None)


x_list_themes__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_list_themes__mutmut_1": x_list_themes__mutmut_1
}
x_list_themes__mutmut_orig.__name__ = "x_list_themes"


def register_theme(name: str, theme: Theme) -> None:
    args = [name, theme]  # type: ignore
    kwargs = {}  # type: ignore
    return _mutmut_trampoline(
        x_register_theme__mutmut_orig, x_register_theme__mutmut_mutants, args, kwargs, None
    )


def x_register_theme__mutmut_orig(name: str, theme: Theme) -> None:
    """Register a custom theme.

    Parameters
    ----------
    name : str
        Theme name.
    theme : Theme
        Theme instance.
    """
    _THEMES[name] = theme


def x_register_theme__mutmut_1(name: str, theme: Theme) -> None:
    """Register a custom theme.

    Parameters
    ----------
    name : str
        Theme name.
    theme : Theme
        Theme instance.
    """
    _THEMES[name] = None


x_register_theme__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
    "x_register_theme__mutmut_1": x_register_theme__mutmut_1
}
x_register_theme__mutmut_orig.__name__ = "x_register_theme"
