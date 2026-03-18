"""Out-of-sample validation results."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Annotated

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

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
        """RMSE between forecast volatility and realized volatility proxy.

        Returns
        -------
        float
            Root mean squared error.
        """
        forecast_var = self.forecast_volatility**2
        realized_var = self.actual_squared_returns
        return float(np.sqrt(np.mean((forecast_var - realized_var) ** 2)))

    def mae_vol(self) -> float:
        """MAE between forecast volatility and realized volatility proxy.

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

        Returns
        -------
        float
            Fraction of observations where actual return < VaR.
        """
        if self.var_series is None:
            msg = "VaR series not computed. Run with VaR enabled."
            raise ValueError(msg)
        violations = self.actual_returns < self.var_series
        return float(np.mean(violations))

    def plot_forecast_vs_actual(
        self,
        ax: plt.Axes | None = None,
    ) -> plt.Axes:
        """Plot forecast volatility vs realized returns.

        Parameters
        ----------
        ax : plt.Axes, optional
            Matplotlib axes.

        Returns
        -------
        plt.Axes
            Matplotlib axes with the plot.
        """
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
