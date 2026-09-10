"""Out-of-sample validation results."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:  # pragma: no cover - typing only, keeps matplotlib off the import path
    from matplotlib.axes import Axes


@dataclass
class ValidationResult:
    """Container for out-of-sample validation results.

    Attributes
    ----------
    model_name : str
        Name of the validated model.
    in_sample_size : int
        Number of in-sample observations.
    out_sample_size : int
        Number of out-of-sample observations.
    forecast_volatility : NDArray[np.float64]
        Forecasted volatility for out-of-sample period.
    actual_returns : NDArray[np.float64]
        Actual returns in out-of-sample period.
    actual_squared_returns : NDArray[np.float64]
        Squared returns as proxy for realized variance.
    var_series : NDArray[np.float64] | None
        VaR series if computed.
    alpha : float
        VaR significance level.
    """

    model_name: str
    in_sample_size: int
    out_sample_size: int
    forecast_volatility: NDArray[np.float64]
    actual_returns: NDArray[np.float64]
    actual_squared_returns: NDArray[np.float64]
    var_series: NDArray[np.float64] | None = None
    alpha: float = 0.05

    def rmse_vol(self) -> float:
        """RMSE of the variance forecast against the realized-variance proxy.

        Both series are compared on the *variance* scale: the forecast
        ``sigma^2_t`` against the squared returns.

        Returns
        -------
        float
            Root mean squared error.
        """
        forecast_var = self.forecast_volatility**2
        realized_var = self.actual_squared_returns
        return float(np.sqrt(np.mean((forecast_var - realized_var) ** 2)))

    def mae_vol(self) -> float:
        """MAE of the variance forecast against the realized-variance proxy.

        Both series are compared on the *variance* scale: the forecast
        ``sigma^2_t`` against the squared returns.

        Returns
        -------
        float
            Mean absolute error.
        """
        forecast_var = self.forecast_volatility**2
        realized_var = self.actual_squared_returns
        return float(np.mean(np.abs(forecast_var - realized_var)))

    def var_violation_rate(self) -> float:
        """VaR violation rate.

        The comparison is made on the raw return scale: a violation is
        ``r_t < VaR_t``.

        Returns
        -------
        float
            Fraction of observations where the actual return is below the VaR.

        Raises
        ------
        ValueError
            If no VaR series was computed, or if it does not align with the
            out-of-sample returns.
        """
        if self.var_series is None:
            msg = "VaR series not computed. Run with VaR enabled."
            raise ValueError(msg)

        var = np.asarray(self.var_series, dtype=np.float64).ravel()
        returns = np.asarray(self.actual_returns, dtype=np.float64).ravel()
        if len(var) != len(returns):
            msg = (
                f"var_series and actual_returns must have the same length, "
                f"got {len(var)} and {len(returns)}"
            )
            raise ValueError(msg)

        valid = np.isfinite(var) & np.isfinite(returns)
        if not np.any(valid):
            msg = "no valid (return, VaR) pairs: every observation is NaN or infinite."
            raise ValueError(msg)

        return float(np.mean(returns[valid] < var[valid]))

    def plot_forecast_vs_actual(
        self,
        ax: Axes | None = None,
    ) -> Axes:
        """Plot forecast volatility vs realized returns.

        Parameters
        ----------
        ax : matplotlib.axes.Axes, optional
            Matplotlib axes.

        Returns
        -------
        matplotlib.axes.Axes
            Matplotlib axes with the plot.
        """
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots(figsize=(12, 6))

        t = np.arange(self.out_sample_size)
        ax.plot(t, np.abs(self.actual_returns), alpha=0.3, label="|Returns|", color="#95a5a6")
        ax.plot(t, self.forecast_volatility, label="Forecast Vol", color="#e74c3c", linewidth=1.5)
        ax.set_xlabel("Time")
        ax.set_ylabel("Volatility")
        ax.set_title(f"{self.model_name} - Out-of-Sample Forecast")
        ax.legend()
        plt.tight_layout()
        return ax
