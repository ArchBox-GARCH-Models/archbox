"""HTML exporter for archbox reports.

Generates self-contained HTML documents with:
- Plotly interactive charts (inline JS)
- Styled tables with CSS
- Sidebar navigation
- Collapsible sections
- Responsive layout
"""

from __future__ import annotations

from pathlib import Path


class HTMLExporter:
    """Export reports as self-contained HTML files.

    The generated HTML includes all CSS and JavaScript inline,
    making it a single portable file.
    """

    def export(
        self,
        rendered_content: str,
        output_path: str | Path | None = None,
        include_plotly: bool = True,
    ) -> str:
        """Export rendered content as HTML.

        Parameters
        ----------
        rendered_content : str
            Pre-rendered HTML content from TemplateManager.
        output_path : str or Path, optional
            Path to save the file. If None, returns as string.
        include_plotly : bool
            Whether to include Plotly.js CDN link.

        Returns
        -------
        str
            Complete HTML document.
        """
        # The content should already be a complete HTML document
        # from the Jinja2 template, but we can add Plotly if needed
        html = rendered_content

        if include_plotly and "<script" not in html:
            plotly_cdn = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
            html = html.replace("</head>", f"    {plotly_cdn}\n</head>")

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding="utf-8")

        return html

    @staticmethod
    def get_collapsible_script() -> str:
        """Return JavaScript for collapsible sections."""
        return """
<script>
document.querySelectorAll('.collapsible-header').forEach(function(header) {
    header.addEventListener('click', function() {
        this.classList.toggle('active');
        var content = this.nextElementSibling;
        content.classList.toggle('active');
    });
});
</script>
"""

    @staticmethod
    def get_sidebar_script() -> str:
        """Return JavaScript for sidebar navigation highlighting."""
        return """
<script>
document.addEventListener('scroll', function() {
    var sections = document.querySelectorAll('h2[id]');
    var links = document.querySelectorAll('.sidebar a');
    var current = '';
    sections.forEach(function(section) {
        if (window.scrollY >= section.offsetTop - 100) {
            current = section.getAttribute('id');
        }
    });
    links.forEach(function(link) {
        link.style.fontWeight = link.getAttribute('href') === '#' + current ? 'bold' : 'normal';
    });
});
</script>
"""
