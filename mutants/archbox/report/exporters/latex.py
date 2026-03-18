"""LaTeX exporter for archbox reports.

Generates LaTeX documents with:
- booktabs professional tables
- Figures with PNG/PDF references
- Proper sections and subsections
- Footer with metadata
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
        args = [rendered_content, output_path]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁLaTeXExporterǁexport__mutmut_orig"),
            object.__getattribute__(self, "xǁLaTeXExporterǁexport__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁLaTeXExporterǁexport__mutmut_orig(
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

    def xǁLaTeXExporterǁexport__mutmut_1(
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
        latex = None

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(latex, encoding="utf-8")

        return latex

    def xǁLaTeXExporterǁexport__mutmut_2(
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

        if output_path is None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(latex, encoding="utf-8")

        return latex

    def xǁLaTeXExporterǁexport__mutmut_3(
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
            output_path = None
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(latex, encoding="utf-8")

        return latex

    def xǁLaTeXExporterǁexport__mutmut_4(
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
            output_path = Path(None)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(latex, encoding="utf-8")

        return latex

    def xǁLaTeXExporterǁexport__mutmut_5(
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
            output_path.parent.mkdir(parents=None, exist_ok=True)
            output_path.write_text(latex, encoding="utf-8")

        return latex

    def xǁLaTeXExporterǁexport__mutmut_6(
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
            output_path.parent.mkdir(parents=True, exist_ok=None)
            output_path.write_text(latex, encoding="utf-8")

        return latex

    def xǁLaTeXExporterǁexport__mutmut_7(
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
            output_path.parent.mkdir(exist_ok=True)
            output_path.write_text(latex, encoding="utf-8")

        return latex

    def xǁLaTeXExporterǁexport__mutmut_8(
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
            output_path.parent.mkdir(
                parents=True,
            )
            output_path.write_text(latex, encoding="utf-8")

        return latex

    def xǁLaTeXExporterǁexport__mutmut_9(
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
            output_path.parent.mkdir(parents=False, exist_ok=True)
            output_path.write_text(latex, encoding="utf-8")

        return latex

    def xǁLaTeXExporterǁexport__mutmut_10(
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
            output_path.parent.mkdir(parents=True, exist_ok=False)
            output_path.write_text(latex, encoding="utf-8")

        return latex

    def xǁLaTeXExporterǁexport__mutmut_11(
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
            output_path.write_text(None, encoding="utf-8")

        return latex

    def xǁLaTeXExporterǁexport__mutmut_12(
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
            output_path.write_text(latex, encoding=None)

        return latex

    def xǁLaTeXExporterǁexport__mutmut_13(
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
            output_path.write_text(encoding="utf-8")

        return latex

    def xǁLaTeXExporterǁexport__mutmut_14(
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
            output_path.write_text(
                latex,
            )

        return latex

    def xǁLaTeXExporterǁexport__mutmut_15(
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
            output_path.write_text(latex, encoding="XXutf-8XX")

        return latex

    def xǁLaTeXExporterǁexport__mutmut_16(
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
            output_path.write_text(latex, encoding="UTF-8")

        return latex

    xǁLaTeXExporterǁexport__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁLaTeXExporterǁexport__mutmut_1": xǁLaTeXExporterǁexport__mutmut_1,
        "xǁLaTeXExporterǁexport__mutmut_2": xǁLaTeXExporterǁexport__mutmut_2,
        "xǁLaTeXExporterǁexport__mutmut_3": xǁLaTeXExporterǁexport__mutmut_3,
        "xǁLaTeXExporterǁexport__mutmut_4": xǁLaTeXExporterǁexport__mutmut_4,
        "xǁLaTeXExporterǁexport__mutmut_5": xǁLaTeXExporterǁexport__mutmut_5,
        "xǁLaTeXExporterǁexport__mutmut_6": xǁLaTeXExporterǁexport__mutmut_6,
        "xǁLaTeXExporterǁexport__mutmut_7": xǁLaTeXExporterǁexport__mutmut_7,
        "xǁLaTeXExporterǁexport__mutmut_8": xǁLaTeXExporterǁexport__mutmut_8,
        "xǁLaTeXExporterǁexport__mutmut_9": xǁLaTeXExporterǁexport__mutmut_9,
        "xǁLaTeXExporterǁexport__mutmut_10": xǁLaTeXExporterǁexport__mutmut_10,
        "xǁLaTeXExporterǁexport__mutmut_11": xǁLaTeXExporterǁexport__mutmut_11,
        "xǁLaTeXExporterǁexport__mutmut_12": xǁLaTeXExporterǁexport__mutmut_12,
        "xǁLaTeXExporterǁexport__mutmut_13": xǁLaTeXExporterǁexport__mutmut_13,
        "xǁLaTeXExporterǁexport__mutmut_14": xǁLaTeXExporterǁexport__mutmut_14,
        "xǁLaTeXExporterǁexport__mutmut_15": xǁLaTeXExporterǁexport__mutmut_15,
        "xǁLaTeXExporterǁexport__mutmut_16": xǁLaTeXExporterǁexport__mutmut_16,
    }
    xǁLaTeXExporterǁexport__mutmut_orig.__name__ = "xǁLaTeXExporterǁexport"

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
