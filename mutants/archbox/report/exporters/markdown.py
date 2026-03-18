"""Markdown exporter for archbox reports.

Generates Markdown documents compatible with GitHub, MkDocs,
and Jupyter notebooks.
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
        args = [rendered_content, output_path]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁMarkdownExporterǁexport__mutmut_orig"),
            object.__getattribute__(self, "xǁMarkdownExporterǁexport__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁMarkdownExporterǁexport__mutmut_orig(
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

    def xǁMarkdownExporterǁexport__mutmut_1(
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
        md = None

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(md, encoding="utf-8")

        return md

    def xǁMarkdownExporterǁexport__mutmut_2(
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

        if output_path is None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(md, encoding="utf-8")

        return md

    def xǁMarkdownExporterǁexport__mutmut_3(
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
            output_path = None
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(md, encoding="utf-8")

        return md

    def xǁMarkdownExporterǁexport__mutmut_4(
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
            output_path = Path(None)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(md, encoding="utf-8")

        return md

    def xǁMarkdownExporterǁexport__mutmut_5(
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
            output_path.parent.mkdir(parents=None, exist_ok=True)
            output_path.write_text(md, encoding="utf-8")

        return md

    def xǁMarkdownExporterǁexport__mutmut_6(
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
            output_path.parent.mkdir(parents=True, exist_ok=None)
            output_path.write_text(md, encoding="utf-8")

        return md

    def xǁMarkdownExporterǁexport__mutmut_7(
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
            output_path.parent.mkdir(exist_ok=True)
            output_path.write_text(md, encoding="utf-8")

        return md

    def xǁMarkdownExporterǁexport__mutmut_8(
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
            output_path.parent.mkdir(
                parents=True,
            )
            output_path.write_text(md, encoding="utf-8")

        return md

    def xǁMarkdownExporterǁexport__mutmut_9(
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
            output_path.parent.mkdir(parents=False, exist_ok=True)
            output_path.write_text(md, encoding="utf-8")

        return md

    def xǁMarkdownExporterǁexport__mutmut_10(
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
            output_path.parent.mkdir(parents=True, exist_ok=False)
            output_path.write_text(md, encoding="utf-8")

        return md

    def xǁMarkdownExporterǁexport__mutmut_11(
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
            output_path.write_text(None, encoding="utf-8")

        return md

    def xǁMarkdownExporterǁexport__mutmut_12(
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
            output_path.write_text(md, encoding=None)

        return md

    def xǁMarkdownExporterǁexport__mutmut_13(
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
            output_path.write_text(encoding="utf-8")

        return md

    def xǁMarkdownExporterǁexport__mutmut_14(
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
            output_path.write_text(
                md,
            )

        return md

    def xǁMarkdownExporterǁexport__mutmut_15(
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
            output_path.write_text(md, encoding="XXutf-8XX")

        return md

    def xǁMarkdownExporterǁexport__mutmut_16(
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
            output_path.write_text(md, encoding="UTF-8")

        return md

    xǁMarkdownExporterǁexport__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁMarkdownExporterǁexport__mutmut_1": xǁMarkdownExporterǁexport__mutmut_1,
        "xǁMarkdownExporterǁexport__mutmut_2": xǁMarkdownExporterǁexport__mutmut_2,
        "xǁMarkdownExporterǁexport__mutmut_3": xǁMarkdownExporterǁexport__mutmut_3,
        "xǁMarkdownExporterǁexport__mutmut_4": xǁMarkdownExporterǁexport__mutmut_4,
        "xǁMarkdownExporterǁexport__mutmut_5": xǁMarkdownExporterǁexport__mutmut_5,
        "xǁMarkdownExporterǁexport__mutmut_6": xǁMarkdownExporterǁexport__mutmut_6,
        "xǁMarkdownExporterǁexport__mutmut_7": xǁMarkdownExporterǁexport__mutmut_7,
        "xǁMarkdownExporterǁexport__mutmut_8": xǁMarkdownExporterǁexport__mutmut_8,
        "xǁMarkdownExporterǁexport__mutmut_9": xǁMarkdownExporterǁexport__mutmut_9,
        "xǁMarkdownExporterǁexport__mutmut_10": xǁMarkdownExporterǁexport__mutmut_10,
        "xǁMarkdownExporterǁexport__mutmut_11": xǁMarkdownExporterǁexport__mutmut_11,
        "xǁMarkdownExporterǁexport__mutmut_12": xǁMarkdownExporterǁexport__mutmut_12,
        "xǁMarkdownExporterǁexport__mutmut_13": xǁMarkdownExporterǁexport__mutmut_13,
        "xǁMarkdownExporterǁexport__mutmut_14": xǁMarkdownExporterǁexport__mutmut_14,
        "xǁMarkdownExporterǁexport__mutmut_15": xǁMarkdownExporterǁexport__mutmut_15,
        "xǁMarkdownExporterǁexport__mutmut_16": xǁMarkdownExporterǁexport__mutmut_16,
    }
    xǁMarkdownExporterǁexport__mutmut_orig.__name__ = "xǁMarkdownExporterǁexport"

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
