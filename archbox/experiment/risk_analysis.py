"""Risk analysis results."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray


@dataclass
class RiskAnalysisResult:
    """Container for risk analysis results.

    Attributes
    ----------
    model_name : str
        Name of the model used.
    alpha : float
        Significance level.
    var_series : dict[str, NDArray[np.float64]]
        VaR series by method (e.g., 'parametric', 'historical').
    es_series : dict[str, NDArray[np.float64]]
        Expected shortfall series by method.
    backtest_results : dict[str, Any]
        Backtest results by method.
    """

    model_name: str
    alpha: float
    var_series: dict[str, NDArray[np.float64]] = field(default_factory=dict)
    es_series: dict[str, NDArray[np.float64]] = field(default_factory=dict)
    backtest_results: dict[str, Any] = field(default_factory=dict)

    def backtest_summary(self) -> str:
        """Generate a summary of backtest results.

        Returns
        -------
        str
            Formatted backtest summary.
        """
        lines = [
            f"Risk Analysis Summary - {self.model_name}",
            f"Alpha: {self.alpha}",
            "=" * 60,
        ]
        for method, bt in self.backtest_results.items():
            lines.append(f"\nMethod: {method}")
            if hasattr(bt, "violation_ratio"):
                lines.append(f"  Violation ratio: {bt.violation_ratio():.4f}")
            if hasattr(bt, "kupiec_test"):
                kupiec = bt.kupiec_test()
                lines.append(f"  Kupiec p-value: {kupiec.pvalue:.4f}")
            if hasattr(bt, "basel_traffic_light"):
                lines.append(f"  Traffic light: {bt.basel_traffic_light()}")
        return "\n".join(lines)

    def plot_risk(
        self,
        method: str = "parametric",
        returns: NDArray[np.float64] | None = None,
        ax: plt.Axes | None = None,
    ) -> plt.Axes:
        """Plot VaR and ES series.

        Parameters
        ----------
        method : str
            VaR method to plot.
        returns : ndarray, optional
            Actual returns for overlay.
        ax : plt.Axes, optional
            Matplotlib axes.

        Returns
        -------
        plt.Axes
            Matplotlib axes with the plot.
        """
        if method not in self.var_series:
            msg = f"Method '{method}' not found. Available: {list(self.var_series.keys())}"
            raise ValueError(msg)

        if ax is None:
            _, ax = plt.subplots(figsize=(14, 7))

        var = self.var_series[method]
        t = np.arange(len(var))

        if returns is not None:
            ax.plot(t, returns[-len(var) :], alpha=0.3, color="#95a5a6", label="Returns")

        ax.plot(t, var, color="#e74c3c", linewidth=1.5, label=f"VaR({self.alpha})")

        if method in self.es_series:
            es = self.es_series[method]
            ax.plot(
                t, es, color="#e67e22", linewidth=1.5, linestyle="--", label=f"ES({self.alpha})"
            )

        ax.set_xlabel("Time")
        ax.set_ylabel("Risk Measure")
        ax.set_title(f"{self.model_name} - {method.title()} Risk Measures")
        ax.legend()
        plt.tight_layout()
        return ax
