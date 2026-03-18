"""Tests for report exporters."""

from __future__ import annotations

from pathlib import Path

from archbox.report.exporters.html import HTMLExporter
from archbox.report.exporters.latex import LaTeXExporter
from archbox.report.exporters.markdown import MarkdownExporter


class TestHTMLExporter:
    """Test HTMLExporter."""

    def test_export_returns_string(self) -> None:
        exporter = HTMLExporter()
        html = exporter.export("<html><head></head><body>Test</body></html>")
        assert isinstance(html, str)
        assert "Test" in html

    def test_adds_plotly_cdn(self) -> None:
        exporter = HTMLExporter()
        html = exporter.export(
            "<html><head></head><body>Test</body></html>",
            include_plotly=True,
        )
        assert "plotly" in html

    def test_export_to_file(self, tmp_path: Path) -> None:
        exporter = HTMLExporter()
        outpath = tmp_path / "report.html"
        exporter.export(
            "<html><head></head><body>Test</body></html>",
            output_path=outpath,
        )
        assert outpath.exists()
        assert outpath.stat().st_size > 0

    def test_collapsible_script(self) -> None:
        script = HTMLExporter.get_collapsible_script()
        assert "collapsible-header" in script


class TestLaTeXExporter:
    """Test LaTeXExporter."""

    def test_export_returns_string(self) -> None:
        exporter = LaTeXExporter()
        latex = exporter.export("\\documentclass{article}\\begin{document}Test\\end{document}")
        assert "Test" in latex

    def test_export_to_file(self, tmp_path: Path) -> None:
        exporter = LaTeXExporter()
        outpath = tmp_path / "report.tex"
        exporter.export("\\documentclass{article}", output_path=outpath)
        assert outpath.exists()

    def test_format_table(self) -> None:
        table = LaTeXExporter.format_table(
            headers=["Param", "Value"],
            rows=[["omega", "1.5e-6"], ["alpha", "0.08"]],
            caption="Parameters",
        )
        assert "\\toprule" in table
        assert "\\midrule" in table
        assert "\\bottomrule" in table
        assert "omega" in table

    def test_format_figure(self) -> None:
        fig = LaTeXExporter.format_figure("vol.png", caption="Volatility")
        assert "\\includegraphics" in fig
        assert "vol.png" in fig


class TestMarkdownExporter:
    """Test MarkdownExporter."""

    def test_export_returns_string(self) -> None:
        exporter = MarkdownExporter()
        md = exporter.export("# Report\n\nContent")
        assert "Content" in md

    def test_export_to_file(self, tmp_path: Path) -> None:
        exporter = MarkdownExporter()
        outpath = tmp_path / "report.md"
        exporter.export("# Report", output_path=outpath)
        assert outpath.exists()

    def test_format_table(self) -> None:
        table = MarkdownExporter.format_table(
            headers=["Param", "Value"],
            rows=[["omega", "1.5e-6"]],
        )
        assert "| Param | Value |" in table
        assert "| omega | 1.5e-6 |" in table

    def test_format_image(self) -> None:
        img = MarkdownExporter.format_image("vol.png", alt_text="Volatility", caption="Fig 1")
        assert "![Volatility](vol.png)" in img
        assert "Fig 1" in img
