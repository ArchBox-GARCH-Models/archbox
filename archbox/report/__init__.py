"""Report generation module for archbox.

Provides automated report generation for GARCH, multivariate,
regime-switching, and risk analysis results.

Usage:
    from archbox.report import ReportManager

    manager = ReportManager()
    html = manager.generate(results, report_type='garch', fmt='html')
"""

from archbox.report.report_manager import ReportManager

__all__ = ["ReportManager"]
