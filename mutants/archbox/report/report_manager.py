"""Report orchestrator for archbox.

The ReportManager coordinates the full pipeline:
results -> Transformer -> context -> TemplateManager -> rendered -> Exporter -> file
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from archbox.report.css_manager import CSSManager
from archbox.report.template_manager import TemplateManager
from archbox.report.transformers.garch import GARCHTransformer
from archbox.report.transformers.multivariate import MultivariateTransformer
from archbox.report.transformers.regime import RegimeTransformer
from archbox.report.transformers.risk import RiskTransformer

_TRANSFORMER_MAP = {
    "garch": GARCHTransformer,
    "multivariate": MultivariateTransformer,
    "regime": RegimeTransformer,
    "risk": RiskTransformer,
}
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


class ReportManager:
    """Orchestrates report generation.

    Parameters
    ----------
    template_dir : str or Path, optional
        Custom template directory. If None, uses built-in templates.
    """

    def __init__(self, template_dir: str | Path | None = None) -> None:
        args = [template_dir]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁReportManagerǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁReportManagerǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁReportManagerǁ__init____mutmut_orig(self, template_dir: str | Path | None = None) -> None:
        """Initialize report manager with optional custom template directory."""
        self.template_manager = TemplateManager(template_dir)
        self.css_manager = CSSManager()

    def xǁReportManagerǁ__init____mutmut_1(self, template_dir: str | Path | None = None) -> None:
        """Initialize report manager with optional custom template directory."""
        self.template_manager = None
        self.css_manager = CSSManager()

    def xǁReportManagerǁ__init____mutmut_2(self, template_dir: str | Path | None = None) -> None:
        """Initialize report manager with optional custom template directory."""
        self.template_manager = TemplateManager(None)
        self.css_manager = CSSManager()

    def xǁReportManagerǁ__init____mutmut_3(self, template_dir: str | Path | None = None) -> None:
        """Initialize report manager with optional custom template directory."""
        self.template_manager = TemplateManager(template_dir)
        self.css_manager = None

    xǁReportManagerǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁReportManagerǁ__init____mutmut_1": xǁReportManagerǁ__init____mutmut_1,
        "xǁReportManagerǁ__init____mutmut_2": xǁReportManagerǁ__init____mutmut_2,
        "xǁReportManagerǁ__init____mutmut_3": xǁReportManagerǁ__init____mutmut_3,
    }
    xǁReportManagerǁ__init____mutmut_orig.__name__ = "xǁReportManagerǁ__init__"

    def generate(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        args = [results, report_type, fmt, theme, output_path, title]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁReportManagerǁgenerate__mutmut_orig"),
            object.__getattribute__(self, "xǁReportManagerǁgenerate__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁReportManagerǁgenerate__mutmut_orig(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_1(
        self,
        results: Any,
        report_type: str = "XXgarchXX",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_2(
        self,
        results: Any,
        report_type: str = "GARCH",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_3(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "XXhtmlXX",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_4(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "HTML",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_5(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "XXprofessionalXX",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_6(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "PROFESSIONAL",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_7(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = None

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_8(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(None)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_9(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = None
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_10(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(None)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_11(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = None
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_12(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["XXthemeXX"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_13(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["THEME"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_14(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = None
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_15(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["XXreport_typeXX"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_16(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["REPORT_TYPE"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_17(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = None

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_18(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["XXtitleXX"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_19(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["TITLE"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_20(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title and f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_21(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt != "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_22(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "XXhtmlXX":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_23(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "HTML":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_24(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = None

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_25(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["XXcssXX"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_26(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["CSS"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_27(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(None)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_28(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = None
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_29(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(None)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_30(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = None

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_31(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(None, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_32(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, None)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_33(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_34(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(
            template_name,
        )

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_35(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_36(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = None
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_37(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(None)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_38(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=None, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_39(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=None)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_40(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_41(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(
                parents=True,
            )
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_42(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=False, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_43(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=False)
            output_path.write_text(rendered, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_44(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(None, encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_45(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding=None)

        return rendered

    def xǁReportManagerǁgenerate__mutmut_46(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(encoding="utf-8")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_47(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(
                rendered,
            )

        return rendered

    def xǁReportManagerǁgenerate__mutmut_48(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="XXutf-8XX")

        return rendered

    def xǁReportManagerǁgenerate__mutmut_49(
        self,
        results: Any,
        report_type: str = "garch",
        fmt: str = "html",
        theme: str = "professional",
        output_path: str | Path | None = None,
        title: str | None = None,
    ) -> str:
        """Generate a report from model results.

        Parameters
        ----------
        results : Any
            Fitted model results (ArchResults, MultivariateResults, etc.).
        report_type : str
            Type of report: 'garch', 'multivariate', 'regime', 'risk'.
        fmt : str
            Output format: 'html', 'latex', 'markdown'.
        theme : str
            Visual theme for CSS and charts.
        output_path : str or Path, optional
            Path to save the report. If None, returns as string.
        title : str, optional
            Report title.

        Returns
        -------
        str
            Rendered report content.
        """
        # Step 1: Get transformer
        transformer = self._get_transformer(report_type)

        # Step 2: Transform results to template context
        context = transformer.transform(results)
        context["theme"] = theme
        context["report_type"] = report_type
        context["title"] = title or f"archbox {report_type.title()} Report"

        # Step 3: Add CSS if HTML
        if fmt == "html":
            context["css"] = self.css_manager.get_css(theme)

        # Step 4: Load and render template
        template_name = f"{report_type}_report.{self._get_template_ext(fmt)}"
        rendered = self.template_manager.render(template_name, context)

        # Step 5: Save or return
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="UTF-8")

        return rendered

    xǁReportManagerǁgenerate__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁReportManagerǁgenerate__mutmut_1": xǁReportManagerǁgenerate__mutmut_1,
        "xǁReportManagerǁgenerate__mutmut_2": xǁReportManagerǁgenerate__mutmut_2,
        "xǁReportManagerǁgenerate__mutmut_3": xǁReportManagerǁgenerate__mutmut_3,
        "xǁReportManagerǁgenerate__mutmut_4": xǁReportManagerǁgenerate__mutmut_4,
        "xǁReportManagerǁgenerate__mutmut_5": xǁReportManagerǁgenerate__mutmut_5,
        "xǁReportManagerǁgenerate__mutmut_6": xǁReportManagerǁgenerate__mutmut_6,
        "xǁReportManagerǁgenerate__mutmut_7": xǁReportManagerǁgenerate__mutmut_7,
        "xǁReportManagerǁgenerate__mutmut_8": xǁReportManagerǁgenerate__mutmut_8,
        "xǁReportManagerǁgenerate__mutmut_9": xǁReportManagerǁgenerate__mutmut_9,
        "xǁReportManagerǁgenerate__mutmut_10": xǁReportManagerǁgenerate__mutmut_10,
        "xǁReportManagerǁgenerate__mutmut_11": xǁReportManagerǁgenerate__mutmut_11,
        "xǁReportManagerǁgenerate__mutmut_12": xǁReportManagerǁgenerate__mutmut_12,
        "xǁReportManagerǁgenerate__mutmut_13": xǁReportManagerǁgenerate__mutmut_13,
        "xǁReportManagerǁgenerate__mutmut_14": xǁReportManagerǁgenerate__mutmut_14,
        "xǁReportManagerǁgenerate__mutmut_15": xǁReportManagerǁgenerate__mutmut_15,
        "xǁReportManagerǁgenerate__mutmut_16": xǁReportManagerǁgenerate__mutmut_16,
        "xǁReportManagerǁgenerate__mutmut_17": xǁReportManagerǁgenerate__mutmut_17,
        "xǁReportManagerǁgenerate__mutmut_18": xǁReportManagerǁgenerate__mutmut_18,
        "xǁReportManagerǁgenerate__mutmut_19": xǁReportManagerǁgenerate__mutmut_19,
        "xǁReportManagerǁgenerate__mutmut_20": xǁReportManagerǁgenerate__mutmut_20,
        "xǁReportManagerǁgenerate__mutmut_21": xǁReportManagerǁgenerate__mutmut_21,
        "xǁReportManagerǁgenerate__mutmut_22": xǁReportManagerǁgenerate__mutmut_22,
        "xǁReportManagerǁgenerate__mutmut_23": xǁReportManagerǁgenerate__mutmut_23,
        "xǁReportManagerǁgenerate__mutmut_24": xǁReportManagerǁgenerate__mutmut_24,
        "xǁReportManagerǁgenerate__mutmut_25": xǁReportManagerǁgenerate__mutmut_25,
        "xǁReportManagerǁgenerate__mutmut_26": xǁReportManagerǁgenerate__mutmut_26,
        "xǁReportManagerǁgenerate__mutmut_27": xǁReportManagerǁgenerate__mutmut_27,
        "xǁReportManagerǁgenerate__mutmut_28": xǁReportManagerǁgenerate__mutmut_28,
        "xǁReportManagerǁgenerate__mutmut_29": xǁReportManagerǁgenerate__mutmut_29,
        "xǁReportManagerǁgenerate__mutmut_30": xǁReportManagerǁgenerate__mutmut_30,
        "xǁReportManagerǁgenerate__mutmut_31": xǁReportManagerǁgenerate__mutmut_31,
        "xǁReportManagerǁgenerate__mutmut_32": xǁReportManagerǁgenerate__mutmut_32,
        "xǁReportManagerǁgenerate__mutmut_33": xǁReportManagerǁgenerate__mutmut_33,
        "xǁReportManagerǁgenerate__mutmut_34": xǁReportManagerǁgenerate__mutmut_34,
        "xǁReportManagerǁgenerate__mutmut_35": xǁReportManagerǁgenerate__mutmut_35,
        "xǁReportManagerǁgenerate__mutmut_36": xǁReportManagerǁgenerate__mutmut_36,
        "xǁReportManagerǁgenerate__mutmut_37": xǁReportManagerǁgenerate__mutmut_37,
        "xǁReportManagerǁgenerate__mutmut_38": xǁReportManagerǁgenerate__mutmut_38,
        "xǁReportManagerǁgenerate__mutmut_39": xǁReportManagerǁgenerate__mutmut_39,
        "xǁReportManagerǁgenerate__mutmut_40": xǁReportManagerǁgenerate__mutmut_40,
        "xǁReportManagerǁgenerate__mutmut_41": xǁReportManagerǁgenerate__mutmut_41,
        "xǁReportManagerǁgenerate__mutmut_42": xǁReportManagerǁgenerate__mutmut_42,
        "xǁReportManagerǁgenerate__mutmut_43": xǁReportManagerǁgenerate__mutmut_43,
        "xǁReportManagerǁgenerate__mutmut_44": xǁReportManagerǁgenerate__mutmut_44,
        "xǁReportManagerǁgenerate__mutmut_45": xǁReportManagerǁgenerate__mutmut_45,
        "xǁReportManagerǁgenerate__mutmut_46": xǁReportManagerǁgenerate__mutmut_46,
        "xǁReportManagerǁgenerate__mutmut_47": xǁReportManagerǁgenerate__mutmut_47,
        "xǁReportManagerǁgenerate__mutmut_48": xǁReportManagerǁgenerate__mutmut_48,
        "xǁReportManagerǁgenerate__mutmut_49": xǁReportManagerǁgenerate__mutmut_49,
    }
    xǁReportManagerǁgenerate__mutmut_orig.__name__ = "xǁReportManagerǁgenerate"

    def _get_transformer(self, report_type: str) -> Any:
        args = [report_type]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁReportManagerǁ_get_transformer__mutmut_orig"),
            object.__getattribute__(self, "xǁReportManagerǁ_get_transformer__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁReportManagerǁ_get_transformer__mutmut_orig(self, report_type: str) -> Any:
        """Get the appropriate transformer for the report type."""
        if report_type not in _TRANSFORMER_MAP:
            available = ", ".join(sorted(_TRANSFORMER_MAP.keys()))
            msg = f"Unknown report type '{report_type}'. Available: {available}"
            raise ValueError(msg)
        return _TRANSFORMER_MAP[report_type]()

    def xǁReportManagerǁ_get_transformer__mutmut_1(self, report_type: str) -> Any:
        """Get the appropriate transformer for the report type."""
        if report_type in _TRANSFORMER_MAP:
            available = ", ".join(sorted(_TRANSFORMER_MAP.keys()))
            msg = f"Unknown report type '{report_type}'. Available: {available}"
            raise ValueError(msg)
        return _TRANSFORMER_MAP[report_type]()

    def xǁReportManagerǁ_get_transformer__mutmut_2(self, report_type: str) -> Any:
        """Get the appropriate transformer for the report type."""
        if report_type not in _TRANSFORMER_MAP:
            available = None
            msg = f"Unknown report type '{report_type}'. Available: {available}"
            raise ValueError(msg)
        return _TRANSFORMER_MAP[report_type]()

    def xǁReportManagerǁ_get_transformer__mutmut_3(self, report_type: str) -> Any:
        """Get the appropriate transformer for the report type."""
        if report_type not in _TRANSFORMER_MAP:
            available = ", ".join(None)
            msg = f"Unknown report type '{report_type}'. Available: {available}"
            raise ValueError(msg)
        return _TRANSFORMER_MAP[report_type]()

    def xǁReportManagerǁ_get_transformer__mutmut_4(self, report_type: str) -> Any:
        """Get the appropriate transformer for the report type."""
        if report_type not in _TRANSFORMER_MAP:
            available = "XX, XX".join(sorted(_TRANSFORMER_MAP.keys()))
            msg = f"Unknown report type '{report_type}'. Available: {available}"
            raise ValueError(msg)
        return _TRANSFORMER_MAP[report_type]()

    def xǁReportManagerǁ_get_transformer__mutmut_5(self, report_type: str) -> Any:
        """Get the appropriate transformer for the report type."""
        if report_type not in _TRANSFORMER_MAP:
            available = ", ".join(sorted(None))
            msg = f"Unknown report type '{report_type}'. Available: {available}"
            raise ValueError(msg)
        return _TRANSFORMER_MAP[report_type]()

    def xǁReportManagerǁ_get_transformer__mutmut_6(self, report_type: str) -> Any:
        """Get the appropriate transformer for the report type."""
        if report_type not in _TRANSFORMER_MAP:
            available = ", ".join(sorted(_TRANSFORMER_MAP.keys()))
            msg = None
            raise ValueError(msg)
        return _TRANSFORMER_MAP[report_type]()

    def xǁReportManagerǁ_get_transformer__mutmut_7(self, report_type: str) -> Any:
        """Get the appropriate transformer for the report type."""
        if report_type not in _TRANSFORMER_MAP:
            available = ", ".join(sorted(_TRANSFORMER_MAP.keys()))
            msg = f"Unknown report type '{report_type}'. Available: {available}"
            raise ValueError(None)
        return _TRANSFORMER_MAP[report_type]()

    xǁReportManagerǁ_get_transformer__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁReportManagerǁ_get_transformer__mutmut_1": xǁReportManagerǁ_get_transformer__mutmut_1,
        "xǁReportManagerǁ_get_transformer__mutmut_2": xǁReportManagerǁ_get_transformer__mutmut_2,
        "xǁReportManagerǁ_get_transformer__mutmut_3": xǁReportManagerǁ_get_transformer__mutmut_3,
        "xǁReportManagerǁ_get_transformer__mutmut_4": xǁReportManagerǁ_get_transformer__mutmut_4,
        "xǁReportManagerǁ_get_transformer__mutmut_5": xǁReportManagerǁ_get_transformer__mutmut_5,
        "xǁReportManagerǁ_get_transformer__mutmut_6": xǁReportManagerǁ_get_transformer__mutmut_6,
        "xǁReportManagerǁ_get_transformer__mutmut_7": xǁReportManagerǁ_get_transformer__mutmut_7,
    }
    xǁReportManagerǁ_get_transformer__mutmut_orig.__name__ = "xǁReportManagerǁ_get_transformer"

    @staticmethod
    def _get_template_ext(fmt: str) -> str:
        """Map format to template file extension."""
        ext_map = {
            "html": "html",
            "latex": "tex",
            "markdown": "md",
        }
        if fmt not in ext_map:
            available = ", ".join(sorted(ext_map.keys()))
            msg = f"Unknown format '{fmt}'. Available: {available}"
            raise ValueError(msg)
        return ext_map[fmt]

    @staticmethod
    def list_report_types() -> list[str]:
        """List available report types."""
        return sorted(_TRANSFORMER_MAP.keys())

    @staticmethod
    def list_formats() -> list[str]:
        """List available output formats."""
        return ["html", "latex", "markdown"]
