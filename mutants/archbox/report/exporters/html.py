"""HTML exporter for archbox reports.

Generates self-contained HTML documents with:
- Plotly interactive charts (inline JS)
- Styled tables with CSS
- Sidebar navigation
- Collapsible sections
- Responsive layout
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
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


class HTMLExporter:
    """Export reports as self-contained HTML files.

    The generated HTML includes all CSS and JavaScript inline,
    making it a single portable file.
    """

    def export(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
        include_plotly: bool = True,
    ) -> str:
        args = [rendered_content, output_path, include_plotly]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁHTMLExporterǁexport__mutmut_orig"),
            object.__getattribute__(self, "xǁHTMLExporterǁexport__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁHTMLExporterǁexport__mutmut_orig(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
        include_plotly: bool = True,
    ) -> str:
        """Export rendered content as HTML.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered HTML content from TemplateManager.
        output_path : str or Path, optional
            Path to save the file. If None, returns as string.
        include_plotly : bool
            Whether to include Plotly.js CDN link.

        Returns
        -------
        str
            Complete HTML document.
        """
        # The content should already be a complete HTML document
        # from the Jinja2 template, but we can add Plotly if needed
        html = rendered_content

        if include_plotly and "<script" not in html:
            plotly_cdn = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
            html = html.replace("</head>", f"    {plotly_cdn}\n</head>")

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding="utf-8")

        return html

    def xǁHTMLExporterǁexport__mutmut_1(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
        include_plotly: bool = False,
    ) -> str:
        """Export rendered content as HTML.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered HTML content from TemplateManager.
        output_path : str or Path, optional
            Path to save the file. If None, returns as string.
        include_plotly : bool
            Whether to include Plotly.js CDN link.

        Returns
        -------
        str
            Complete HTML document.
        """
        # The content should already be a complete HTML document
        # from the Jinja2 template, but we can add Plotly if needed
        html = rendered_content

        if include_plotly and "<script" not in html:
            plotly_cdn = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
            html = html.replace("</head>", f"    {plotly_cdn}\n</head>")

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding="utf-8")

        return html

    def xǁHTMLExporterǁexport__mutmut_2(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
        include_plotly: bool = True,
    ) -> str:
        """Export rendered content as HTML.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered HTML content from TemplateManager.
        output_path : str or Path, optional
            Path to save the file. If None, returns as string.
        include_plotly : bool
            Whether to include Plotly.js CDN link.

        Returns
        -------
        str
            Complete HTML document.
        """
        # The content should already be a complete HTML document
        # from the Jinja2 template, but we can add Plotly if needed
        html = None

        if include_plotly and "<script" not in html:
            plotly_cdn = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
            html = html.replace("</head>", f"    {plotly_cdn}\n</head>")

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding="utf-8")

        return html

    def xǁHTMLExporterǁexport__mutmut_3(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
        include_plotly: bool = True,
    ) -> str:
        """Export rendered content as HTML.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered HTML content from TemplateManager.
        output_path : str or Path, optional
            Path to save the file. If None, returns as string.
        include_plotly : bool
            Whether to include Plotly.js CDN link.

        Returns
        -------
        str
            Complete HTML document.
        """
        # The content should already be a complete HTML document
        # from the Jinja2 template, but we can add Plotly if needed
        html = rendered_content

        if include_plotly or "<script" not in html:
            plotly_cdn = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
            html = html.replace("</head>", f"    {plotly_cdn}\n</head>")

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding="utf-8")

        return html

    def xǁHTMLExporterǁexport__mutmut_4(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
        include_plotly: bool = True,
    ) -> str:
        """Export rendered content as HTML.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered HTML content from TemplateManager.
        output_path : str or Path, optional
            Path to save the file. If None, returns as string.
        include_plotly : bool
            Whether to include Plotly.js CDN link.

        Returns
        -------
        str
            Complete HTML document.
        """
        # The content should already be a complete HTML document
        # from the Jinja2 template, but we can add Plotly if needed
        html = rendered_content

        if include_plotly and "XX<scriptXX" not in html:
            plotly_cdn = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
            html = html.replace("</head>", f"    {plotly_cdn}\n</head>")

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding="utf-8")

        return html

    def xǁHTMLExporterǁexport__mutmut_5(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
        include_plotly: bool = True,
    ) -> str:
        """Export rendered content as HTML.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered HTML content from TemplateManager.
        output_path : str or Path, optional
            Path to save the file. If None, returns as string.
        include_plotly : bool
            Whether to include Plotly.js CDN link.

        Returns
        -------
        str
            Complete HTML document.
        """
        # The content should already be a complete HTML document
        # from the Jinja2 template, but we can add Plotly if needed
        html = rendered_content

        if include_plotly and "<SCRIPT" not in html:
            plotly_cdn = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
            html = html.replace("</head>", f"    {plotly_cdn}\n</head>")

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding="utf-8")

        return html

    def xǁHTMLExporterǁexport__mutmut_6(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
        include_plotly: bool = True,
    ) -> str:
        """Export rendered content as HTML.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered HTML content from TemplateManager.
        output_path : str or Path, optional
            Path to save the file. If None, returns as string.
        include_plotly : bool
            Whether to include Plotly.js CDN link.

        Returns
        -------
        str
            Complete HTML document.
        """
        # The content should already be a complete HTML document
        # from the Jinja2 template, but we can add Plotly if needed
        html = rendered_content

        if include_plotly and "<script" in html:
            plotly_cdn = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
            html = html.replace("</head>", f"    {plotly_cdn}\n</head>")

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding="utf-8")

        return html

    def xǁHTMLExporterǁexport__mutmut_7(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
        include_plotly: bool = True,
    ) -> str:
        """Export rendered content as HTML.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered HTML content from TemplateManager.
        output_path : str or Path, optional
            Path to save the file. If None, returns as string.
        include_plotly : bool
            Whether to include Plotly.js CDN link.

        Returns
        -------
        str
            Complete HTML document.
        """
        # The content should already be a complete HTML document
        # from the Jinja2 template, but we can add Plotly if needed
        html = rendered_content

        if include_plotly and "<script" not in html:
            plotly_cdn = None
            html = html.replace("</head>", f"    {plotly_cdn}\n</head>")

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding="utf-8")

        return html

    def xǁHTMLExporterǁexport__mutmut_8(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
        include_plotly: bool = True,
    ) -> str:
        """Export rendered content as HTML.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered HTML content from TemplateManager.
        output_path : str or Path, optional
            Path to save the file. If None, returns as string.
        include_plotly : bool
            Whether to include Plotly.js CDN link.

        Returns
        -------
        str
            Complete HTML document.
        """
        # The content should already be a complete HTML document
        # from the Jinja2 template, but we can add Plotly if needed
        html = rendered_content

        if include_plotly and "<script" not in html:
            plotly_cdn = 'XX<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>XX'
            html = html.replace("</head>", f"    {plotly_cdn}\n</head>")

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding="utf-8")

        return html

    def xǁHTMLExporterǁexport__mutmut_9(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
        include_plotly: bool = True,
    ) -> str:
        """Export rendered content as HTML.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered HTML content from TemplateManager.
        output_path : str or Path, optional
            Path to save the file. If None, returns as string.
        include_plotly : bool
            Whether to include Plotly.js CDN link.

        Returns
        -------
        str
            Complete HTML document.
        """
        # The content should already be a complete HTML document
        # from the Jinja2 template, but we can add Plotly if needed
        html = rendered_content

        if include_plotly and "<script" not in html:
            plotly_cdn = '<SCRIPT SRC="HTTPS://CDN.PLOT.LY/PLOTLY-LATEST.MIN.JS"></SCRIPT>'
            html = html.replace("</head>", f"    {plotly_cdn}\n</head>")

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding="utf-8")

        return html

    def xǁHTMLExporterǁexport__mutmut_10(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
        include_plotly: bool = True,
    ) -> str:
        """Export rendered content as HTML.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered HTML content from TemplateManager.
        output_path : str or Path, optional
            Path to save the file. If None, returns as string.
        include_plotly : bool
            Whether to include Plotly.js CDN link.

        Returns
        -------
        str
            Complete HTML document.
        """
        # The content should already be a complete HTML document
        # from the Jinja2 template, but we can add Plotly if needed
        html = rendered_content

        if include_plotly and "<script" not in html:
            plotly_cdn = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
            html = None

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding="utf-8")

        return html

    def xǁHTMLExporterǁexport__mutmut_11(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
        include_plotly: bool = True,
    ) -> str:
        """Export rendered content as HTML.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered HTML content from TemplateManager.
        output_path : str or Path, optional
            Path to save the file. If None, returns as string.
        include_plotly : bool
            Whether to include Plotly.js CDN link.

        Returns
        -------
        str
            Complete HTML document.
        """
        # The content should already be a complete HTML document
        # from the Jinja2 template, but we can add Plotly if needed
        html = rendered_content

        if include_plotly and "<script" not in html:
            plotly_cdn = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
            html = html.replace(None, f"    {plotly_cdn}\n</head>")

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding="utf-8")

        return html

    def xǁHTMLExporterǁexport__mutmut_12(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
        include_plotly: bool = True,
    ) -> str:
        """Export rendered content as HTML.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered HTML content from TemplateManager.
        output_path : str or Path, optional
            Path to save the file. If None, returns as string.
        include_plotly : bool
            Whether to include Plotly.js CDN link.

        Returns
        -------
        str
            Complete HTML document.
        """
        # The content should already be a complete HTML document
        # from the Jinja2 template, but we can add Plotly if needed
        html = rendered_content

        if include_plotly and "<script" not in html:
            plotly_cdn = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
            html = html.replace("</head>", None)

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding="utf-8")

        return html

    def xǁHTMLExporterǁexport__mutmut_13(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
        include_plotly: bool = True,
    ) -> str:
        """Export rendered content as HTML.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered HTML content from TemplateManager.
        output_path : str or Path, optional
            Path to save the file. If None, returns as string.
        include_plotly : bool
            Whether to include Plotly.js CDN link.

        Returns
        -------
        str
            Complete HTML document.
        """
        # The content should already be a complete HTML document
        # from the Jinja2 template, but we can add Plotly if needed
        html = rendered_content

        if include_plotly and "<script" not in html:
            plotly_cdn = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
            html = html.replace(f"    {plotly_cdn}\n</head>")

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding="utf-8")

        return html

    def xǁHTMLExporterǁexport__mutmut_14(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
        include_plotly: bool = True,
    ) -> str:
        """Export rendered content as HTML.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered HTML content from TemplateManager.
        output_path : str or Path, optional
            Path to save the file. If None, returns as string.
        include_plotly : bool
            Whether to include Plotly.js CDN link.

        Returns
        -------
        str
            Complete HTML document.
        """
        # The content should already be a complete HTML document
        # from the Jinja2 template, but we can add Plotly if needed
        html = rendered_content

        if include_plotly and "<script" not in html:
            plotly_cdn = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
            html = html.replace(
                "</head>",
            )

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding="utf-8")

        return html

    def xǁHTMLExporterǁexport__mutmut_15(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
        include_plotly: bool = True,
    ) -> str:
        """Export rendered content as HTML.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered HTML content from TemplateManager.
        output_path : str or Path, optional
            Path to save the file. If None, returns as string.
        include_plotly : bool
            Whether to include Plotly.js CDN link.

        Returns
        -------
        str
            Complete HTML document.
        """
        # The content should already be a complete HTML document
        # from the Jinja2 template, but we can add Plotly if needed
        html = rendered_content

        if include_plotly and "<script" not in html:
            plotly_cdn = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
            html = html.replace("XX</head>XX", f"    {plotly_cdn}\n</head>")

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding="utf-8")

        return html

    def xǁHTMLExporterǁexport__mutmut_16(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
        include_plotly: bool = True,
    ) -> str:
        """Export rendered content as HTML.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered HTML content from TemplateManager.
        output_path : str or Path, optional
            Path to save the file. If None, returns as string.
        include_plotly : bool
            Whether to include Plotly.js CDN link.

        Returns
        -------
        str
            Complete HTML document.
        """
        # The content should already be a complete HTML document
        # from the Jinja2 template, but we can add Plotly if needed
        html = rendered_content

        if include_plotly and "<script" not in html:
            plotly_cdn = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
            html = html.replace("</HEAD>", f"    {plotly_cdn}\n</head>")

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding="utf-8")

        return html

    def xǁHTMLExporterǁexport__mutmut_17(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
        include_plotly: bool = True,
    ) -> str:
        """Export rendered content as HTML.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered HTML content from TemplateManager.
        output_path : str or Path, optional
            Path to save the file. If None, returns as string.
        include_plotly : bool
            Whether to include Plotly.js CDN link.

        Returns
        -------
        str
            Complete HTML document.
        """
        # The content should already be a complete HTML document
        # from the Jinja2 template, but we can add Plotly if needed
        html = rendered_content

        if include_plotly and "<script" not in html:
            plotly_cdn = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
            html = html.replace("</head>", f"    {plotly_cdn}\n</head>")

        if output_path is None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding="utf-8")

        return html

    def xǁHTMLExporterǁexport__mutmut_18(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
        include_plotly: bool = True,
    ) -> str:
        """Export rendered content as HTML.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered HTML content from TemplateManager.
        output_path : str or Path, optional
            Path to save the file. If None, returns as string.
        include_plotly : bool
            Whether to include Plotly.js CDN link.

        Returns
        -------
        str
            Complete HTML document.
        """
        # The content should already be a complete HTML document
        # from the Jinja2 template, but we can add Plotly if needed
        html = rendered_content

        if include_plotly and "<script" not in html:
            plotly_cdn = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
            html = html.replace("</head>", f"    {plotly_cdn}\n</head>")

        if output_path is not None:
            output_path = None
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding="utf-8")

        return html

    def xǁHTMLExporterǁexport__mutmut_19(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
        include_plotly: bool = True,
    ) -> str:
        """Export rendered content as HTML.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered HTML content from TemplateManager.
        output_path : str or Path, optional
            Path to save the file. If None, returns as string.
        include_plotly : bool
            Whether to include Plotly.js CDN link.

        Returns
        -------
        str
            Complete HTML document.
        """
        # The content should already be a complete HTML document
        # from the Jinja2 template, but we can add Plotly if needed
        html = rendered_content

        if include_plotly and "<script" not in html:
            plotly_cdn = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
            html = html.replace("</head>", f"    {plotly_cdn}\n</head>")

        if output_path is not None:
            output_path = Path(None)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding="utf-8")

        return html

    def xǁHTMLExporterǁexport__mutmut_20(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
        include_plotly: bool = True,
    ) -> str:
        """Export rendered content as HTML.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered HTML content from TemplateManager.
        output_path : str or Path, optional
            Path to save the file. If None, returns as string.
        include_plotly : bool
            Whether to include Plotly.js CDN link.

        Returns
        -------
        str
            Complete HTML document.
        """
        # The content should already be a complete HTML document
        # from the Jinja2 template, but we can add Plotly if needed
        html = rendered_content

        if include_plotly and "<script" not in html:
            plotly_cdn = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
            html = html.replace("</head>", f"    {plotly_cdn}\n</head>")

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=None, exist_ok=True)
            output_path.write_text(html, encoding="utf-8")

        return html

    def xǁHTMLExporterǁexport__mutmut_21(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
        include_plotly: bool = True,
    ) -> str:
        """Export rendered content as HTML.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered HTML content from TemplateManager.
        output_path : str or Path, optional
            Path to save the file. If None, returns as string.
        include_plotly : bool
            Whether to include Plotly.js CDN link.

        Returns
        -------
        str
            Complete HTML document.
        """
        # The content should already be a complete HTML document
        # from the Jinja2 template, but we can add Plotly if needed
        html = rendered_content

        if include_plotly and "<script" not in html:
            plotly_cdn = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
            html = html.replace("</head>", f"    {plotly_cdn}\n</head>")

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=None)
            output_path.write_text(html, encoding="utf-8")

        return html

    def xǁHTMLExporterǁexport__mutmut_22(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
        include_plotly: bool = True,
    ) -> str:
        """Export rendered content as HTML.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered HTML content from TemplateManager.
        output_path : str or Path, optional
            Path to save the file. If None, returns as string.
        include_plotly : bool
            Whether to include Plotly.js CDN link.

        Returns
        -------
        str
            Complete HTML document.
        """
        # The content should already be a complete HTML document
        # from the Jinja2 template, but we can add Plotly if needed
        html = rendered_content

        if include_plotly and "<script" not in html:
            plotly_cdn = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
            html = html.replace("</head>", f"    {plotly_cdn}\n</head>")

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(exist_ok=True)
            output_path.write_text(html, encoding="utf-8")

        return html

    def xǁHTMLExporterǁexport__mutmut_23(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
        include_plotly: bool = True,
    ) -> str:
        """Export rendered content as HTML.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered HTML content from TemplateManager.
        output_path : str or Path, optional
            Path to save the file. If None, returns as string.
        include_plotly : bool
            Whether to include Plotly.js CDN link.

        Returns
        -------
        str
            Complete HTML document.
        """
        # The content should already be a complete HTML document
        # from the Jinja2 template, but we can add Plotly if needed
        html = rendered_content

        if include_plotly and "<script" not in html:
            plotly_cdn = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
            html = html.replace("</head>", f"    {plotly_cdn}\n</head>")

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(
                parents=True,
            )
            output_path.write_text(html, encoding="utf-8")

        return html

    def xǁHTMLExporterǁexport__mutmut_24(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
        include_plotly: bool = True,
    ) -> str:
        """Export rendered content as HTML.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered HTML content from TemplateManager.
        output_path : str or Path, optional
            Path to save the file. If None, returns as string.
        include_plotly : bool
            Whether to include Plotly.js CDN link.

        Returns
        -------
        str
            Complete HTML document.
        """
        # The content should already be a complete HTML document
        # from the Jinja2 template, but we can add Plotly if needed
        html = rendered_content

        if include_plotly and "<script" not in html:
            plotly_cdn = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
            html = html.replace("</head>", f"    {plotly_cdn}\n</head>")

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=False, exist_ok=True)
            output_path.write_text(html, encoding="utf-8")

        return html

    def xǁHTMLExporterǁexport__mutmut_25(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
        include_plotly: bool = True,
    ) -> str:
        """Export rendered content as HTML.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered HTML content from TemplateManager.
        output_path : str or Path, optional
            Path to save the file. If None, returns as string.
        include_plotly : bool
            Whether to include Plotly.js CDN link.

        Returns
        -------
        str
            Complete HTML document.
        """
        # The content should already be a complete HTML document
        # from the Jinja2 template, but we can add Plotly if needed
        html = rendered_content

        if include_plotly and "<script" not in html:
            plotly_cdn = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
            html = html.replace("</head>", f"    {plotly_cdn}\n</head>")

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=False)
            output_path.write_text(html, encoding="utf-8")

        return html

    def xǁHTMLExporterǁexport__mutmut_26(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
        include_plotly: bool = True,
    ) -> str:
        """Export rendered content as HTML.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered HTML content from TemplateManager.
        output_path : str or Path, optional
            Path to save the file. If None, returns as string.
        include_plotly : bool
            Whether to include Plotly.js CDN link.

        Returns
        -------
        str
            Complete HTML document.
        """
        # The content should already be a complete HTML document
        # from the Jinja2 template, but we can add Plotly if needed
        html = rendered_content

        if include_plotly and "<script" not in html:
            plotly_cdn = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
            html = html.replace("</head>", f"    {plotly_cdn}\n</head>")

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(None, encoding="utf-8")

        return html

    def xǁHTMLExporterǁexport__mutmut_27(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
        include_plotly: bool = True,
    ) -> str:
        """Export rendered content as HTML.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered HTML content from TemplateManager.
        output_path : str or Path, optional
            Path to save the file. If None, returns as string.
        include_plotly : bool
            Whether to include Plotly.js CDN link.

        Returns
        -------
        str
            Complete HTML document.
        """
        # The content should already be a complete HTML document
        # from the Jinja2 template, but we can add Plotly if needed
        html = rendered_content

        if include_plotly and "<script" not in html:
            plotly_cdn = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
            html = html.replace("</head>", f"    {plotly_cdn}\n</head>")

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding=None)

        return html

    def xǁHTMLExporterǁexport__mutmut_28(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
        include_plotly: bool = True,
    ) -> str:
        """Export rendered content as HTML.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered HTML content from TemplateManager.
        output_path : str or Path, optional
            Path to save the file. If None, returns as string.
        include_plotly : bool
            Whether to include Plotly.js CDN link.

        Returns
        -------
        str
            Complete HTML document.
        """
        # The content should already be a complete HTML document
        # from the Jinja2 template, but we can add Plotly if needed
        html = rendered_content

        if include_plotly and "<script" not in html:
            plotly_cdn = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
            html = html.replace("</head>", f"    {plotly_cdn}\n</head>")

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(encoding="utf-8")

        return html

    def xǁHTMLExporterǁexport__mutmut_29(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
        include_plotly: bool = True,
    ) -> str:
        """Export rendered content as HTML.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered HTML content from TemplateManager.
        output_path : str or Path, optional
            Path to save the file. If None, returns as string.
        include_plotly : bool
            Whether to include Plotly.js CDN link.

        Returns
        -------
        str
            Complete HTML document.
        """
        # The content should already be a complete HTML document
        # from the Jinja2 template, but we can add Plotly if needed
        html = rendered_content

        if include_plotly and "<script" not in html:
            plotly_cdn = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
            html = html.replace("</head>", f"    {plotly_cdn}\n</head>")

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(
                html,
            )

        return html

    def xǁHTMLExporterǁexport__mutmut_30(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
        include_plotly: bool = True,
    ) -> str:
        """Export rendered content as HTML.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered HTML content from TemplateManager.
        output_path : str or Path, optional
            Path to save the file. If None, returns as string.
        include_plotly : bool
            Whether to include Plotly.js CDN link.

        Returns
        -------
        str
            Complete HTML document.
        """
        # The content should already be a complete HTML document
        # from the Jinja2 template, but we can add Plotly if needed
        html = rendered_content

        if include_plotly and "<script" not in html:
            plotly_cdn = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
            html = html.replace("</head>", f"    {plotly_cdn}\n</head>")

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding="XXutf-8XX")

        return html

    def xǁHTMLExporterǁexport__mutmut_31(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
        include_plotly: bool = True,
    ) -> str:
        """Export rendered content as HTML.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered HTML content from TemplateManager.
        output_path : str or Path, optional
            Path to save the file. If None, returns as string.
        include_plotly : bool
            Whether to include Plotly.js CDN link.

        Returns
        -------
        str
            Complete HTML document.
        """
        # The content should already be a complete HTML document
        # from the Jinja2 template, but we can add Plotly if needed
        html = rendered_content

        if include_plotly and "<script" not in html:
            plotly_cdn = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
            html = html.replace("</head>", f"    {plotly_cdn}\n</head>")

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding="UTF-8")

        return html

    xǁHTMLExporterǁexport__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁHTMLExporterǁexport__mutmut_1": xǁHTMLExporterǁexport__mutmut_1,
        "xǁHTMLExporterǁexport__mutmut_2": xǁHTMLExporterǁexport__mutmut_2,
        "xǁHTMLExporterǁexport__mutmut_3": xǁHTMLExporterǁexport__mutmut_3,
        "xǁHTMLExporterǁexport__mutmut_4": xǁHTMLExporterǁexport__mutmut_4,
        "xǁHTMLExporterǁexport__mutmut_5": xǁHTMLExporterǁexport__mutmut_5,
        "xǁHTMLExporterǁexport__mutmut_6": xǁHTMLExporterǁexport__mutmut_6,
        "xǁHTMLExporterǁexport__mutmut_7": xǁHTMLExporterǁexport__mutmut_7,
        "xǁHTMLExporterǁexport__mutmut_8": xǁHTMLExporterǁexport__mutmut_8,
        "xǁHTMLExporterǁexport__mutmut_9": xǁHTMLExporterǁexport__mutmut_9,
        "xǁHTMLExporterǁexport__mutmut_10": xǁHTMLExporterǁexport__mutmut_10,
        "xǁHTMLExporterǁexport__mutmut_11": xǁHTMLExporterǁexport__mutmut_11,
        "xǁHTMLExporterǁexport__mutmut_12": xǁHTMLExporterǁexport__mutmut_12,
        "xǁHTMLExporterǁexport__mutmut_13": xǁHTMLExporterǁexport__mutmut_13,
        "xǁHTMLExporterǁexport__mutmut_14": xǁHTMLExporterǁexport__mutmut_14,
        "xǁHTMLExporterǁexport__mutmut_15": xǁHTMLExporterǁexport__mutmut_15,
        "xǁHTMLExporterǁexport__mutmut_16": xǁHTMLExporterǁexport__mutmut_16,
        "xǁHTMLExporterǁexport__mutmut_17": xǁHTMLExporterǁexport__mutmut_17,
        "xǁHTMLExporterǁexport__mutmut_18": xǁHTMLExporterǁexport__mutmut_18,
        "xǁHTMLExporterǁexport__mutmut_19": xǁHTMLExporterǁexport__mutmut_19,
        "xǁHTMLExporterǁexport__mutmut_20": xǁHTMLExporterǁexport__mutmut_20,
        "xǁHTMLExporterǁexport__mutmut_21": xǁHTMLExporterǁexport__mutmut_21,
        "xǁHTMLExporterǁexport__mutmut_22": xǁHTMLExporterǁexport__mutmut_22,
        "xǁHTMLExporterǁexport__mutmut_23": xǁHTMLExporterǁexport__mutmut_23,
        "xǁHTMLExporterǁexport__mutmut_24": xǁHTMLExporterǁexport__mutmut_24,
        "xǁHTMLExporterǁexport__mutmut_25": xǁHTMLExporterǁexport__mutmut_25,
        "xǁHTMLExporterǁexport__mutmut_26": xǁHTMLExporterǁexport__mutmut_26,
        "xǁHTMLExporterǁexport__mutmut_27": xǁHTMLExporterǁexport__mutmut_27,
        "xǁHTMLExporterǁexport__mutmut_28": xǁHTMLExporterǁexport__mutmut_28,
        "xǁHTMLExporterǁexport__mutmut_29": xǁHTMLExporterǁexport__mutmut_29,
        "xǁHTMLExporterǁexport__mutmut_30": xǁHTMLExporterǁexport__mutmut_30,
        "xǁHTMLExporterǁexport__mutmut_31": xǁHTMLExporterǁexport__mutmut_31,
    }
    xǁHTMLExporterǁexport__mutmut_orig.__name__ = "xǁHTMLExporterǁexport"

    @staticmethod
    def get_collapsible_script() -> str:
        """Return JavaScript for collapsible sections."""
        return """
<script>
document.querySelectorAll('.collapsible-header').forEach(function(header) {
    header.addEventListener('click', function() {
        this.classList.toggle('active');
        var content = this.nextElementSibling;
        content.classList.toggle('active');
    });
});
</script>
"""

    @staticmethod
    def get_sidebar_script() -> str:
        """Return JavaScript for sidebar navigation highlighting."""
        return """
<script>
document.addEventListener('scroll', function() {
    var sections = document.querySelectorAll('h2[id]');
    var links = document.querySelectorAll('.sidebar a');
    var current = '';
    sections.forEach(function(section) {
        if (window.scrollY >= section.offsetTop - 100) {
            current = section.getAttribute('id');
        }
    });
    links.forEach(function(link) {
        link.style.fontWeight = link.getAttribute('href') === '#' + current ? 'bold' : 'normal';
    });
});
</script>
"""
