"""Template management for archbox reports.

Uses Jinja2 for template loading and rendering with custom filters
and context processors.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

_DEFAULT_TEMPLATE_DIR = Path(__file__).parent / "templates"


class TemplateManager:
    """Manages Jinja2 templates for report generation.

    Parameters
    ----------
    template_dir : str or Path, optional
        Custom template directory. If None, uses built-in templates.
    """

    def __init__(self, template_dir: str | Path | None = None) -> None:
        """Initialize template manager with optional custom template directory."""
        if template_dir is not None:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = _DEFAULT_TEMPLATE_DIR

        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Register custom filters
        self.env.filters["fmt_number"] = self._fmt_number
        self.env.filters["fmt_pvalue"] = self._fmt_pvalue
        self.env.filters["fmt_percent"] = self._fmt_percent
        self.env.filters["significance_stars"] = self._significance_stars

    def render(self, template_name: str, context: dict[str, Any]) -> str:
        """Render a template with the given context.

        Parameters
        ----------
        template_name : str
            Template file name (e.g. 'garch_report.html').
        context : dict
            Template variables.

        Returns
        -------
        str
            Rendered content.
        """
        template = self.env.get_template(template_name)
        return template.render(**context)

    def list_templates(self) -> list[str]:
        """List available template names."""
        return sorted(self.env.list_templates())

    @staticmethod
    def _fmt_number(value: Any, decimals: int = 4) -> str:
        """Format a number with specified decimal places."""
        try:
            return f"{float(value):.{decimals}f}"
        except (TypeError, ValueError):
            return str(value)

    @staticmethod
    def _fmt_pvalue(value: Any) -> str:
        """Format a p-value with appropriate precision."""
        try:
            p = float(value)
            if p < 0.001:
                return "<0.001"
            elif p < 0.01:
                return f"{p:.4f}"
            elif p < 0.1:
                return f"{p:.3f}"
            else:
                return f"{p:.3f}"
        except (TypeError, ValueError):
            return str(value)

    @staticmethod
    def _fmt_percent(value: Any, decimals: int = 2) -> str:
        """Format a value as percentage."""
        try:
            return f"{float(value) * 100:.{decimals}f}%"
        except (TypeError, ValueError):
            return str(value)

    @staticmethod
    def _significance_stars(pvalue: Any) -> str:
        """Return significance stars based on p-value."""
        try:
            p = float(pvalue)
            if p < 0.01:
                return "***"
            elif p < 0.05:
                return "**"
            elif p < 0.10:
                return "*"
            else:
                return ""
        except (TypeError, ValueError):
            return ""
