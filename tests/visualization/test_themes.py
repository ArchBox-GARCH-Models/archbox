"""Tests for visualization themes."""

from __future__ import annotations

import pytest

from archbox.visualization.themes import (
    ACADEMIC,
    PRESENTATION,
    PROFESSIONAL,
    Theme,
    get_theme,
    list_themes,
    register_theme,
)


class TestThemes:
    """Test theme system."""

    def test_professional_theme_exists(self):
        theme = get_theme("professional")
        assert theme.name == "professional"
        assert "primary" in theme.colors
        assert "title" in theme.font_sizes

    def test_academic_theme_exists(self):
        theme = get_theme("academic")
        assert theme.name == "academic"
        assert theme.font_family == "serif"

    def test_presentation_theme_exists(self):
        theme = get_theme("presentation")
        assert theme.name == "presentation"
        assert theme.font_sizes["title"] > ACADEMIC.font_sizes["title"]

    def test_risk_theme_exists(self):
        theme = get_theme("risk")
        assert theme.name == "risk"
        assert "zone_green" in theme.colors

    def test_list_themes(self):
        themes = list_themes()
        assert len(themes) == 4
        assert "professional" in themes
        assert "academic" in themes
        assert "presentation" in themes
        assert "risk" in themes

    def test_unknown_theme_raises(self):
        with pytest.raises(ValueError, match="Unknown theme"):
            get_theme("nonexistent")

    def test_to_matplotlib_rcparams(self):
        theme = get_theme("professional")
        params = theme.to_matplotlib_rcparams()
        assert "figure.figsize" in params
        assert "font.family" in params
        assert "axes.grid" in params

    def test_to_plotly_template(self):
        theme = get_theme("professional")
        template = theme.to_plotly_template()
        assert "font" in template
        assert "plot_bgcolor" in template

    def test_register_custom_theme(self):
        custom = Theme(name="custom", colors={"primary": "#000"})
        register_theme("custom", custom)
        assert get_theme("custom").name == "custom"

    def test_theme_dpi(self):
        assert PROFESSIONAL.dpi == 150
        assert ACADEMIC.dpi == 300
        assert PRESENTATION.dpi == 100
