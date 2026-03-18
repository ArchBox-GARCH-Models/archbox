"""Markdown exporter for archbox reports.

Generates Markdown documents compatible with GitHub, MkDocs,
and Jupyter notebooks.
"""

from __future__ import annotations

from pathlib import Path


class MarkdownExporter:
    """Export reports as Markdown documents.

    Generates .md files with tables and image references,
    compatible with GitHub-flavored Markdown.
    """

    def export(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
    ) -> str:
        """Export rendered content as Markdown.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered Markdown content from TemplateManager.
        output_path : str or Path, optional
            Path to save the .md file.

        Returns
        -------
        str
            Complete Markdown document.
        """
        md = rendered_content

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(md, encoding="utf-8")

        return md

    @staticmethod
    def format_table(headers: list[str], rows: list[list[str]]) -> str:
        """Format a Markdown table.

        Parameters
        ----------
        headers : list of str
            Column headers.
        rows : list of list of str
            Table rows.

        Returns
        -------
        str
            Markdown table.
        """
        lines = []
        lines.append("| " + " | ".join(headers) + " |")
        lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
        for row in rows:
            lines.append("| " + " | ".join(row) + " |")
        return "\n".join(lines)

    @staticmethod
    def format_image(image_path: str, alt_text: str = "", caption: str = "") -> str:
        """Format a Markdown image reference.

        Parameters
        ----------
        image_path : str
            Path to image file.
        alt_text : str
            Alt text for the image.
        caption : str
            Optional caption below image.

        Returns
        -------
        str
            Markdown image reference.
        """
        md = f"![{alt_text}]({image_path})"
        if caption:
            md += f"\n\n*{caption}*"
        return md
