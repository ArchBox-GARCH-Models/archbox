"""CSS management for archbox HTML reports.

Implements a 3-layer CSS system:
1. Base CSS: layout, reset, typography
2. Component CSS: tables, cards, navigation, collapsible sections
3. Theme CSS: colors, fonts specific to theme (professional, academic, etc.)
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Annotated, ClassVar

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


class CSSManager:
    """Manages CSS for HTML report styling.

    Uses a 3-layer system: base -> component -> theme.
    """

    def get_css(self, theme: str = "professional") -> str:
        args = [theme]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁCSSManagerǁget_css__mutmut_orig"),
            object.__getattribute__(self, "xǁCSSManagerǁget_css__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁCSSManagerǁget_css__mutmut_orig(self, theme: str = "professional") -> str:
        """Get complete CSS for a theme.

        Parameters
        ----------
        theme : str
            Theme name.

        Returns
        -------
        str
            Combined CSS string.
        """
        return "\n".join(
            [
                self._base_css(),
                self._component_css(),
                self._theme_css(theme),
            ]
        )

    def xǁCSSManagerǁget_css__mutmut_1(self, theme: str = "XXprofessionalXX") -> str:
        """Get complete CSS for a theme.

        Parameters
        ----------
        theme : str
            Theme name.

        Returns
        -------
        str
            Combined CSS string.
        """
        return "\n".join(
            [
                self._base_css(),
                self._component_css(),
                self._theme_css(theme),
            ]
        )

    def xǁCSSManagerǁget_css__mutmut_2(self, theme: str = "PROFESSIONAL") -> str:
        """Get complete CSS for a theme.

        Parameters
        ----------
        theme : str
            Theme name.

        Returns
        -------
        str
            Combined CSS string.
        """
        return "\n".join(
            [
                self._base_css(),
                self._component_css(),
                self._theme_css(theme),
            ]
        )

    def xǁCSSManagerǁget_css__mutmut_3(self, theme: str = "professional") -> str:
        """Get complete CSS for a theme.

        Parameters
        ----------
        theme : str
            Theme name.

        Returns
        -------
        str
            Combined CSS string.
        """
        return "\n".join(None)

    def xǁCSSManagerǁget_css__mutmut_4(self, theme: str = "professional") -> str:
        """Get complete CSS for a theme.

        Parameters
        ----------
        theme : str
            Theme name.

        Returns
        -------
        str
            Combined CSS string.
        """
        return "XX\nXX".join(
            [
                self._base_css(),
                self._component_css(),
                self._theme_css(theme),
            ]
        )

    def xǁCSSManagerǁget_css__mutmut_5(self, theme: str = "professional") -> str:
        """Get complete CSS for a theme.

        Parameters
        ----------
        theme : str
            Theme name.

        Returns
        -------
        str
            Combined CSS string.
        """
        return "\n".join(
            [
                self._base_css(),
                self._component_css(),
                self._theme_css(None),
            ]
        )

    xǁCSSManagerǁget_css__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁCSSManagerǁget_css__mutmut_1": xǁCSSManagerǁget_css__mutmut_1,
        "xǁCSSManagerǁget_css__mutmut_2": xǁCSSManagerǁget_css__mutmut_2,
        "xǁCSSManagerǁget_css__mutmut_3": xǁCSSManagerǁget_css__mutmut_3,
        "xǁCSSManagerǁget_css__mutmut_4": xǁCSSManagerǁget_css__mutmut_4,
        "xǁCSSManagerǁget_css__mutmut_5": xǁCSSManagerǁget_css__mutmut_5,
    }
    xǁCSSManagerǁget_css__mutmut_orig.__name__ = "xǁCSSManagerǁget_css"

    @staticmethod
    def _base_css() -> str:
        """Base CSS: reset, layout, typography."""
        return """
/* === Base CSS === */
* { margin: 0; padding: 0; box-sizing: border-box; }
html { font-size: 14px; line-height: 1.6; }
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    color: #333;
    background: #fff;
    display: flex;
    min-height: 100vh;
}
.report-container {
    display: flex;
    width: 100%;
    max-width: 1400px;
    margin: 0 auto;
}
.sidebar {
    width: 250px;
    min-width: 250px;
    padding: 20px;
    border-right: 1px solid #e0e0e0;
    position: sticky;
    top: 0;
    height: 100vh;
    overflow-y: auto;
}
.sidebar h3 { margin-bottom: 15px; font-size: 1.1rem; }
.sidebar ul { list-style: none; }
.sidebar li { margin-bottom: 8px; }
.sidebar a {
    text-decoration: none;
    color: #555;
    font-size: 0.9rem;
    transition: color 0.2s;
}
.sidebar a:hover { color: #1f4e79; }
.main-content {
    flex: 1;
    padding: 30px 40px;
    max-width: 1100px;
}
h1 { font-size: 1.8rem; margin-bottom: 10px; }
h2 {
    font-size: 1.4rem; margin: 30px 0 15px;
    border-bottom: 2px solid #e0e0e0; padding-bottom: 5px;
}
h3 { font-size: 1.1rem; margin: 20px 0 10px; }
p { margin-bottom: 10px; }
.meta { color: #888; font-size: 0.85rem; margin-bottom: 20px; }
"""

    @staticmethod
    def _component_css() -> str:
        """Component CSS: tables, cards, navigation, collapsible."""
        return """
/* === Component CSS === */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 15px 0;
    font-size: 0.9rem;
}
thead th {
    background: #f5f5f5;
    border-bottom: 2px solid #ddd;
    padding: 10px 12px;
    text-align: left;
    font-weight: 600;
}
tbody td {
    padding: 8px 12px;
    border-bottom: 1px solid #eee;
}
tbody tr:hover { background: #fafafa; }
.numeric { text-align: right; font-family: 'Courier New', monospace; }
.significance { color: #c00000; font-weight: bold; }
.card {
    background: #fff;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.card-header {
    font-weight: 600;
    font-size: 1rem;
    margin-bottom: 10px;
    color: #1f4e79;
}
.chart-container {
    width: 100%;
    margin: 15px 0;
    min-height: 400px;
}
.collapsible-header {
    cursor: pointer;
    display: flex;
    align-items: center;
    padding: 10px 0;
}
.collapsible-header::before {
    content: '\\25B6';
    margin-right: 8px;
    transition: transform 0.2s;
    font-size: 0.7rem;
}
.collapsible-header.active::before {
    transform: rotate(90deg);
}
.collapsible-content {
    display: none;
    padding: 10px 0;
}
.collapsible-content.active { display: block; }
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
    margin: 15px 0;
}
.metric-card {
    background: #f8f9fa;
    border-radius: 4px;
    padding: 15px;
    text-align: center;
}
.metric-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: #1f4e79;
}
.metric-label { font-size: 0.8rem; color: #888; margin-top: 5px; }
.footer {
    margin-top: 40px;
    padding-top: 15px;
    border-top: 1px solid #e0e0e0;
    font-size: 0.8rem;
    color: #999;
}
"""

    @staticmethod
    def _theme_css(theme: str) -> str:
        """Theme-specific CSS."""
        themes = {
            "professional": """
/* === Professional Theme === */
.sidebar { background: #f8f9fa; }
.sidebar a:hover { color: #1f4e79; }
h1, h2, .card-header { color: #1f4e79; }
thead th { background: #1f4e79; color: white; }
.metric-value { color: #1f4e79; }
""",
            "academic": """
/* === Academic Theme === */
body { font-family: 'Times New Roman', Georgia, serif; }
.sidebar { background: #fafafa; border-right: 1px solid #ccc; }
h1, h2 { color: #000; }
thead th { background: #333; color: white; }
table { font-family: 'Times New Roman', serif; }
.metric-value { color: #333; }
""",
            "presentation": """
/* === Presentation Theme === */
html { font-size: 16px; }
body { font-family: 'Arial', 'Helvetica Neue', sans-serif; }
h1, h2, .card-header { color: #0066cc; }
thead th { background: #0066cc; color: white; }
.metric-value { color: #0066cc; font-size: 2rem; }
.card { border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
""",
            "risk": """
/* === Risk Theme === */
h1, h2, .card-header { color: #8b0000; }
thead th { background: #8b0000; color: white; }
.metric-value { color: #c00000; }
.sidebar a:hover { color: #c00000; }
""",
        }
        return themes.get(theme, themes["professional"])
