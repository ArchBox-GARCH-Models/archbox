"""LaTeX exporter for archbox reports.

Generates LaTeX documents with:
- booktabs professional tables
- Figures with PNG/PDF references
- Proper sections and subsections
- Footer with metadata
"""

from __future__ import annotations

from pathlib import Path


class LaTeXExporter:
    """Export reports as LaTeX documents.

    Generates compilable .tex files with booktabs tables,
    figure references, and proper document structure.
    """

    def export(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
    ) -> str:
        """Export rendered content as LaTeX.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered LaTeX content from TemplateManager.
        output_path : str or Path, optional
            Path to save the .tex file.

        Returns
        -------
        str
            Complete LaTeX document.
        """
        latex = rendered_content

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(latex, encoding="utf-8")

        return latex

    @staticmethod
    def format_table(
        headers: list[str],
        rows: list[list[str]],
        caption: str = "",
        label: str = "",
    ) -> str:
        """Format a LaTeX table with booktabs.

        Parameters
        ----------
        headers : list of str
            Column headers.
        rows : list of list of str
            Table rows.
        caption : str
            Table caption.
        label : str
            Table label for cross-references.

        Returns
        -------
        str
            LaTeX table code.
        """
        n_cols = len(headers)
        col_spec = "l" + "r" * (n_cols - 1)

        lines = []
        lines.append("\\begin{table}[htbp]")
        lines.append("\\centering")
        if caption:
            lines.append(f"\\caption{{{caption}}}")
        if label:
            lines.append(f"\\label{{{label}}}")
        lines.append(f"\\begin{{tabular}}{{{col_spec}}}")
        lines.append("\\toprule")
        lines.append(" & ".join(headers) + " \\\\")
        lines.append("\\midrule")
        for row in rows:
            lines.append(" & ".join(row) + " \\\\")
        lines.append("\\bottomrule")
        lines.append("\\end{tabular}")
        lines.append("\\end{table}")

        return "\n".join(lines)

    @staticmethod
    def format_figure(
        image_path: str,
        caption: str = "",
        label: str = "",
        width: str = "0.9\\textwidth",
    ) -> str:
        """Format a LaTeX figure environment.

        Parameters
        ----------
        image_path : str
            Path to the image file.
        caption : str
            Figure caption.
        label : str
            Figure label.
        width : str
            Figure width specification.

        Returns
        -------
        str
            LaTeX figure code.
        """
        lines = []
        lines.append("\\begin{figure}[htbp]")
        lines.append("\\centering")
        lines.append(f"\\includegraphics[width={width}]{{{image_path}}}")
        if caption:
            lines.append(f"\\caption{{{caption}}}")
        if label:
            lines.append(f"\\label{{{label}}}")
        lines.append("\\end{figure}")

        return "\n".join(lines)
