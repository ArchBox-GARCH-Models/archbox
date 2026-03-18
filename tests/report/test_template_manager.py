"""Tests for TemplateManager."""

from __future__ import annotations

from archbox.report.template_manager import TemplateManager


class TestTemplateManager:
    """Test TemplateManager."""

    def test_instantiation(self):
        tm = TemplateManager()
        assert tm.template_dir.exists()

    def test_custom_filters(self):
        tm = TemplateManager()
        assert "fmt_number" in tm.env.filters
        assert "fmt_pvalue" in tm.env.filters
        assert "significance_stars" in tm.env.filters

    def test_fmt_number(self):
        assert TemplateManager._fmt_number(3.14159, 2) == "3.14"
        assert TemplateManager._fmt_number(0.001234, 4) == "0.0012"

    def test_fmt_pvalue(self):
        assert TemplateManager._fmt_pvalue(0.0001) == "<0.001"
        assert TemplateManager._fmt_pvalue(0.045) == "0.045"

    def test_significance_stars(self):
        assert TemplateManager._significance_stars(0.001) == "***"
        assert TemplateManager._significance_stars(0.03) == "**"
        assert TemplateManager._significance_stars(0.08) == "*"
        assert TemplateManager._significance_stars(0.15) == ""


class TestCSSManager:
    """Test CSSManager."""

    def test_get_css(self):
        from archbox.report.css_manager import CSSManager

        cm = CSSManager()
        css = cm.get_css("professional")
        assert "Base CSS" in css
        assert "Component CSS" in css
        assert "Professional Theme" in css

    def test_all_themes(self):
        from archbox.report.css_manager import CSSManager

        cm = CSSManager()
        for theme in ["professional", "academic", "presentation", "risk"]:
            css = cm.get_css(theme)
            assert len(css) > 100
