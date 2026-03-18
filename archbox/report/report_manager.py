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


class ReportManager:
    """Orchestrates report generation.

    Parameters
    ----------
    template_dir : str or Path, optional
        Custom template directory. If None, uses built-in templates.
    """

    def __init__(self, template_dir: str | Path | None = None) -> None:
        """Initialize report manager with optional custom template directory."""
        self.template_manager = TemplateManager(template_dir)
        self.css_manager = CSSManager()

    def generate(
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

    def _get_transformer(self, report_type: str) -> Any:
        """Get the appropriate transformer for the report type."""
        if report_type not in _TRANSFORMER_MAP:
            available = ", ".join(sorted(_TRANSFORMER_MAP.keys()))
            msg = f"Unknown report type '{report_type}'. Available: {available}"
            raise ValueError(msg)
        return _TRANSFORMER_MAP[report_type]()

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
