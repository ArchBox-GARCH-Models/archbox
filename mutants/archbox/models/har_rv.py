"""HAR-RV - Heterogeneous Autoregressive Realized Volatility (Corsi, 2009).

RV_t = beta_0 + beta_d * RV_{t-1} + beta_w * RV_w_{t-1} + beta_m * RV_m_{t-1} + eps_t

where:
- RV^{(d)}: daily realized variance
- RV^{(w)} = (1/5) * sum_{i=0}^{4} RV_{t-i}^{(d)}: weekly average
- RV^{(m)} = (1/22) * sum_{i=0}^{21} RV_{t-i}^{(d)}: monthly average
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Annotated, Any, ClassVar

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
class HARRVResults:
    """Results container for HAR-RV model.

    Attributes
    ----------
    params : ndarray
        Estimated coefficients [beta_0, beta_d, beta_w, beta_m].
    param_names : list[str]
        Parameter names.
    std_errors : ndarray
        Standard errors of coefficients.
    t_values : ndarray
        t-statistics.
    r_squared : float
        R-squared of the regression.
    adj_r_squared : float
        Adjusted R-squared.
    residuals : ndarray
        OLS residuals.
    fitted_values : ndarray
        Fitted values.
    nobs : int
        Number of observations used in the regression.
    """

    params: NDArray[np.float64]
    param_names: list[str]
    std_errors: NDArray[np.float64]
    t_values: NDArray[np.float64]
    r_squared: float
    adj_r_squared: float
    residuals: NDArray[np.float64]
    fitted_values: NDArray[np.float64]
    nobs: int

    def summary(self) -> str:
        """Generate summary table."""
        lines: list[str] = []
        lines.append("=" * 60)
        lines.append("HAR-RV Regression Results")
        lines.append("=" * 60)
        lines.append(f"Observations: {self.nobs}")
        lines.append(f"R-squared: {self.r_squared:.6f}")
        lines.append(f"Adj. R-squared: {self.adj_r_squared:.6f}")
        lines.append("-" * 60)
        lines.append(f"{'Parameter':<15} {'Estimate':>12} {'Std.Err':>12} {'t-value':>12}")
        lines.append("-" * 60)
        for name, coef, se, t in zip(
            self.param_names,
            self.params,
            self.std_errors,
            self.t_values,
            strict=True,
        ):
            lines.append(f"{name:<15} {coef:>12.6f} {se:>12.6f} {t:>12.4f}")
        lines.append("=" * 60)
        return "\n".join(lines)

    def forecast(self, horizon: int = 1) -> NDArray[np.float64]:
        """Forecast realized variance.

        Simple iterative forecast using last available RV values.

        Parameters
        ----------
        horizon : int
            Number of steps ahead.

        Returns
        -------
        ndarray
            Forecast values.
        """
        # Use last fitted value as base forecast
        forecasts = np.full(horizon, self.fitted_values[-1])
        return forecasts


class HARRV:
    """Heterogeneous Autoregressive Realized Volatility model.

    Parameters
    ----------
    realized_variance : array-like
        Time series of daily realized variance.
    components : list[str]
        HAR components. Default ['daily', 'weekly', 'monthly'].
    """

    def __init__(
        self,
        realized_variance: Any,
        components: list[str] | None = None,
    ) -> None:
        args = [realized_variance, components]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁHARRVǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁHARRVǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁHARRVǁ__init____mutmut_orig(
        self,
        realized_variance: Any,
        components: list[str] | None = None,
    ) -> None:
        """Initialize HAR-RV model with realized variance and components."""
        self.rv = np.asarray(realized_variance, dtype=np.float64)
        if components is None:
            components = ["daily", "weekly", "monthly"]
        self.components = components
        self._component_lags = {
            "daily": 1,
            "weekly": 5,
            "monthly": 22,
        }

    def xǁHARRVǁ__init____mutmut_1(
        self,
        realized_variance: Any,
        components: list[str] | None = None,
    ) -> None:
        """Initialize HAR-RV model with realized variance and components."""
        self.rv = None
        if components is None:
            components = ["daily", "weekly", "monthly"]
        self.components = components
        self._component_lags = {
            "daily": 1,
            "weekly": 5,
            "monthly": 22,
        }

    def xǁHARRVǁ__init____mutmut_2(
        self,
        realized_variance: Any,
        components: list[str] | None = None,
    ) -> None:
        """Initialize HAR-RV model with realized variance and components."""
        self.rv = np.asarray(None, dtype=np.float64)
        if components is None:
            components = ["daily", "weekly", "monthly"]
        self.components = components
        self._component_lags = {
            "daily": 1,
            "weekly": 5,
            "monthly": 22,
        }

    def xǁHARRVǁ__init____mutmut_3(
        self,
        realized_variance: Any,
        components: list[str] | None = None,
    ) -> None:
        """Initialize HAR-RV model with realized variance and components."""
        self.rv = np.asarray(realized_variance, dtype=None)
        if components is None:
            components = ["daily", "weekly", "monthly"]
        self.components = components
        self._component_lags = {
            "daily": 1,
            "weekly": 5,
            "monthly": 22,
        }

    def xǁHARRVǁ__init____mutmut_4(
        self,
        realized_variance: Any,
        components: list[str] | None = None,
    ) -> None:
        """Initialize HAR-RV model with realized variance and components."""
        self.rv = np.asarray(dtype=np.float64)
        if components is None:
            components = ["daily", "weekly", "monthly"]
        self.components = components
        self._component_lags = {
            "daily": 1,
            "weekly": 5,
            "monthly": 22,
        }

    def xǁHARRVǁ__init____mutmut_5(
        self,
        realized_variance: Any,
        components: list[str] | None = None,
    ) -> None:
        """Initialize HAR-RV model with realized variance and components."""
        self.rv = np.asarray(
            realized_variance,
        )
        if components is None:
            components = ["daily", "weekly", "monthly"]
        self.components = components
        self._component_lags = {
            "daily": 1,
            "weekly": 5,
            "monthly": 22,
        }

    def xǁHARRVǁ__init____mutmut_6(
        self,
        realized_variance: Any,
        components: list[str] | None = None,
    ) -> None:
        """Initialize HAR-RV model with realized variance and components."""
        self.rv = np.asarray(realized_variance, dtype=np.float64)
        if components is not None:
            components = ["daily", "weekly", "monthly"]
        self.components = components
        self._component_lags = {
            "daily": 1,
            "weekly": 5,
            "monthly": 22,
        }

    def xǁHARRVǁ__init____mutmut_7(
        self,
        realized_variance: Any,
        components: list[str] | None = None,
    ) -> None:
        """Initialize HAR-RV model with realized variance and components."""
        self.rv = np.asarray(realized_variance, dtype=np.float64)
        if components is None:
            components = None
        self.components = components
        self._component_lags = {
            "daily": 1,
            "weekly": 5,
            "monthly": 22,
        }

    def xǁHARRVǁ__init____mutmut_8(
        self,
        realized_variance: Any,
        components: list[str] | None = None,
    ) -> None:
        """Initialize HAR-RV model with realized variance and components."""
        self.rv = np.asarray(realized_variance, dtype=np.float64)
        if components is None:
            components = ["XXdailyXX", "weekly", "monthly"]
        self.components = components
        self._component_lags = {
            "daily": 1,
            "weekly": 5,
            "monthly": 22,
        }

    def xǁHARRVǁ__init____mutmut_9(
        self,
        realized_variance: Any,
        components: list[str] | None = None,
    ) -> None:
        """Initialize HAR-RV model with realized variance and components."""
        self.rv = np.asarray(realized_variance, dtype=np.float64)
        if components is None:
            components = ["DAILY", "weekly", "monthly"]
        self.components = components
        self._component_lags = {
            "daily": 1,
            "weekly": 5,
            "monthly": 22,
        }

    def xǁHARRVǁ__init____mutmut_10(
        self,
        realized_variance: Any,
        components: list[str] | None = None,
    ) -> None:
        """Initialize HAR-RV model with realized variance and components."""
        self.rv = np.asarray(realized_variance, dtype=np.float64)
        if components is None:
            components = ["daily", "XXweeklyXX", "monthly"]
        self.components = components
        self._component_lags = {
            "daily": 1,
            "weekly": 5,
            "monthly": 22,
        }

    def xǁHARRVǁ__init____mutmut_11(
        self,
        realized_variance: Any,
        components: list[str] | None = None,
    ) -> None:
        """Initialize HAR-RV model with realized variance and components."""
        self.rv = np.asarray(realized_variance, dtype=np.float64)
        if components is None:
            components = ["daily", "WEEKLY", "monthly"]
        self.components = components
        self._component_lags = {
            "daily": 1,
            "weekly": 5,
            "monthly": 22,
        }

    def xǁHARRVǁ__init____mutmut_12(
        self,
        realized_variance: Any,
        components: list[str] | None = None,
    ) -> None:
        """Initialize HAR-RV model with realized variance and components."""
        self.rv = np.asarray(realized_variance, dtype=np.float64)
        if components is None:
            components = ["daily", "weekly", "XXmonthlyXX"]
        self.components = components
        self._component_lags = {
            "daily": 1,
            "weekly": 5,
            "monthly": 22,
        }

    def xǁHARRVǁ__init____mutmut_13(
        self,
        realized_variance: Any,
        components: list[str] | None = None,
    ) -> None:
        """Initialize HAR-RV model with realized variance and components."""
        self.rv = np.asarray(realized_variance, dtype=np.float64)
        if components is None:
            components = ["daily", "weekly", "MONTHLY"]
        self.components = components
        self._component_lags = {
            "daily": 1,
            "weekly": 5,
            "monthly": 22,
        }

    def xǁHARRVǁ__init____mutmut_14(
        self,
        realized_variance: Any,
        components: list[str] | None = None,
    ) -> None:
        """Initialize HAR-RV model with realized variance and components."""
        self.rv = np.asarray(realized_variance, dtype=np.float64)
        if components is None:
            components = ["daily", "weekly", "monthly"]
        self.components = None
        self._component_lags = {
            "daily": 1,
            "weekly": 5,
            "monthly": 22,
        }

    def xǁHARRVǁ__init____mutmut_15(
        self,
        realized_variance: Any,
        components: list[str] | None = None,
    ) -> None:
        """Initialize HAR-RV model with realized variance and components."""
        self.rv = np.asarray(realized_variance, dtype=np.float64)
        if components is None:
            components = ["daily", "weekly", "monthly"]
        self.components = components
        self._component_lags = None

    def xǁHARRVǁ__init____mutmut_16(
        self,
        realized_variance: Any,
        components: list[str] | None = None,
    ) -> None:
        """Initialize HAR-RV model with realized variance and components."""
        self.rv = np.asarray(realized_variance, dtype=np.float64)
        if components is None:
            components = ["daily", "weekly", "monthly"]
        self.components = components
        self._component_lags = {
            "XXdailyXX": 1,
            "weekly": 5,
            "monthly": 22,
        }

    def xǁHARRVǁ__init____mutmut_17(
        self,
        realized_variance: Any,
        components: list[str] | None = None,
    ) -> None:
        """Initialize HAR-RV model with realized variance and components."""
        self.rv = np.asarray(realized_variance, dtype=np.float64)
        if components is None:
            components = ["daily", "weekly", "monthly"]
        self.components = components
        self._component_lags = {
            "DAILY": 1,
            "weekly": 5,
            "monthly": 22,
        }

    def xǁHARRVǁ__init____mutmut_18(
        self,
        realized_variance: Any,
        components: list[str] | None = None,
    ) -> None:
        """Initialize HAR-RV model with realized variance and components."""
        self.rv = np.asarray(realized_variance, dtype=np.float64)
        if components is None:
            components = ["daily", "weekly", "monthly"]
        self.components = components
        self._component_lags = {
            "daily": 2,
            "weekly": 5,
            "monthly": 22,
        }

    def xǁHARRVǁ__init____mutmut_19(
        self,
        realized_variance: Any,
        components: list[str] | None = None,
    ) -> None:
        """Initialize HAR-RV model with realized variance and components."""
        self.rv = np.asarray(realized_variance, dtype=np.float64)
        if components is None:
            components = ["daily", "weekly", "monthly"]
        self.components = components
        self._component_lags = {
            "daily": 1,
            "XXweeklyXX": 5,
            "monthly": 22,
        }

    def xǁHARRVǁ__init____mutmut_20(
        self,
        realized_variance: Any,
        components: list[str] | None = None,
    ) -> None:
        """Initialize HAR-RV model with realized variance and components."""
        self.rv = np.asarray(realized_variance, dtype=np.float64)
        if components is None:
            components = ["daily", "weekly", "monthly"]
        self.components = components
        self._component_lags = {
            "daily": 1,
            "WEEKLY": 5,
            "monthly": 22,
        }

    def xǁHARRVǁ__init____mutmut_21(
        self,
        realized_variance: Any,
        components: list[str] | None = None,
    ) -> None:
        """Initialize HAR-RV model with realized variance and components."""
        self.rv = np.asarray(realized_variance, dtype=np.float64)
        if components is None:
            components = ["daily", "weekly", "monthly"]
        self.components = components
        self._component_lags = {
            "daily": 1,
            "weekly": 6,
            "monthly": 22,
        }

    def xǁHARRVǁ__init____mutmut_22(
        self,
        realized_variance: Any,
        components: list[str] | None = None,
    ) -> None:
        """Initialize HAR-RV model with realized variance and components."""
        self.rv = np.asarray(realized_variance, dtype=np.float64)
        if components is None:
            components = ["daily", "weekly", "monthly"]
        self.components = components
        self._component_lags = {
            "daily": 1,
            "weekly": 5,
            "XXmonthlyXX": 22,
        }

    def xǁHARRVǁ__init____mutmut_23(
        self,
        realized_variance: Any,
        components: list[str] | None = None,
    ) -> None:
        """Initialize HAR-RV model with realized variance and components."""
        self.rv = np.asarray(realized_variance, dtype=np.float64)
        if components is None:
            components = ["daily", "weekly", "monthly"]
        self.components = components
        self._component_lags = {
            "daily": 1,
            "weekly": 5,
            "MONTHLY": 22,
        }

    def xǁHARRVǁ__init____mutmut_24(
        self,
        realized_variance: Any,
        components: list[str] | None = None,
    ) -> None:
        """Initialize HAR-RV model with realized variance and components."""
        self.rv = np.asarray(realized_variance, dtype=np.float64)
        if components is None:
            components = ["daily", "weekly", "monthly"]
        self.components = components
        self._component_lags = {
            "daily": 1,
            "weekly": 5,
            "monthly": 23,
        }

    xǁHARRVǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁHARRVǁ__init____mutmut_1": xǁHARRVǁ__init____mutmut_1,
        "xǁHARRVǁ__init____mutmut_2": xǁHARRVǁ__init____mutmut_2,
        "xǁHARRVǁ__init____mutmut_3": xǁHARRVǁ__init____mutmut_3,
        "xǁHARRVǁ__init____mutmut_4": xǁHARRVǁ__init____mutmut_4,
        "xǁHARRVǁ__init____mutmut_5": xǁHARRVǁ__init____mutmut_5,
        "xǁHARRVǁ__init____mutmut_6": xǁHARRVǁ__init____mutmut_6,
        "xǁHARRVǁ__init____mutmut_7": xǁHARRVǁ__init____mutmut_7,
        "xǁHARRVǁ__init____mutmut_8": xǁHARRVǁ__init____mutmut_8,
        "xǁHARRVǁ__init____mutmut_9": xǁHARRVǁ__init____mutmut_9,
        "xǁHARRVǁ__init____mutmut_10": xǁHARRVǁ__init____mutmut_10,
        "xǁHARRVǁ__init____mutmut_11": xǁHARRVǁ__init____mutmut_11,
        "xǁHARRVǁ__init____mutmut_12": xǁHARRVǁ__init____mutmut_12,
        "xǁHARRVǁ__init____mutmut_13": xǁHARRVǁ__init____mutmut_13,
        "xǁHARRVǁ__init____mutmut_14": xǁHARRVǁ__init____mutmut_14,
        "xǁHARRVǁ__init____mutmut_15": xǁHARRVǁ__init____mutmut_15,
        "xǁHARRVǁ__init____mutmut_16": xǁHARRVǁ__init____mutmut_16,
        "xǁHARRVǁ__init____mutmut_17": xǁHARRVǁ__init____mutmut_17,
        "xǁHARRVǁ__init____mutmut_18": xǁHARRVǁ__init____mutmut_18,
        "xǁHARRVǁ__init____mutmut_19": xǁHARRVǁ__init____mutmut_19,
        "xǁHARRVǁ__init____mutmut_20": xǁHARRVǁ__init____mutmut_20,
        "xǁHARRVǁ__init____mutmut_21": xǁHARRVǁ__init____mutmut_21,
        "xǁHARRVǁ__init____mutmut_22": xǁHARRVǁ__init____mutmut_22,
        "xǁHARRVǁ__init____mutmut_23": xǁHARRVǁ__init____mutmut_23,
        "xǁHARRVǁ__init____mutmut_24": xǁHARRVǁ__init____mutmut_24,
    }
    xǁHARRVǁ__init____mutmut_orig.__name__ = "xǁHARRVǁ__init__"

    def _build_regressors(self) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁHARRVǁ_build_regressors__mutmut_orig"),
            object.__getattribute__(self, "xǁHARRVǁ_build_regressors__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁHARRVǁ_build_regressors__mutmut_orig(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Build the regression matrix and response vector.

        Returns
        -------
        tuple[ndarray, ndarray]
            (x_mat, y) where x_mat has columns [const, RV_d, RV_w, RV_m].
        """
        max_lag = max(self._component_lags[c] for c in self.components)
        total = len(self.rv)
        n_obs = total - max_lag

        if n_obs < 10:
            msg = f"Not enough observations. Need at least {max_lag + 10}, got {total}."
            raise ValueError(msg)

        y = self.rv[max_lag:]

        # Build regressors
        x_cols: list[NDArray[np.float64]] = [np.ones(n_obs)]  # constant

        for comp in self.components:
            lag = self._component_lags[comp]
            rv_comp = np.empty(n_obs)
            for t in range(n_obs):
                idx = max_lag + t
                rv_comp[t] = np.mean(self.rv[idx - lag : idx])
            x_cols.append(rv_comp)

        x_mat = np.column_stack(x_cols)
        return x_mat, y

    def xǁHARRVǁ_build_regressors__mutmut_1(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Build the regression matrix and response vector.

        Returns
        -------
        tuple[ndarray, ndarray]
            (x_mat, y) where x_mat has columns [const, RV_d, RV_w, RV_m].
        """
        max_lag = None
        total = len(self.rv)
        n_obs = total - max_lag

        if n_obs < 10:
            msg = f"Not enough observations. Need at least {max_lag + 10}, got {total}."
            raise ValueError(msg)

        y = self.rv[max_lag:]

        # Build regressors
        x_cols: list[NDArray[np.float64]] = [np.ones(n_obs)]  # constant

        for comp in self.components:
            lag = self._component_lags[comp]
            rv_comp = np.empty(n_obs)
            for t in range(n_obs):
                idx = max_lag + t
                rv_comp[t] = np.mean(self.rv[idx - lag : idx])
            x_cols.append(rv_comp)

        x_mat = np.column_stack(x_cols)
        return x_mat, y

    def xǁHARRVǁ_build_regressors__mutmut_2(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Build the regression matrix and response vector.

        Returns
        -------
        tuple[ndarray, ndarray]
            (x_mat, y) where x_mat has columns [const, RV_d, RV_w, RV_m].
        """
        max_lag = max(None)
        total = len(self.rv)
        n_obs = total - max_lag

        if n_obs < 10:
            msg = f"Not enough observations. Need at least {max_lag + 10}, got {total}."
            raise ValueError(msg)

        y = self.rv[max_lag:]

        # Build regressors
        x_cols: list[NDArray[np.float64]] = [np.ones(n_obs)]  # constant

        for comp in self.components:
            lag = self._component_lags[comp]
            rv_comp = np.empty(n_obs)
            for t in range(n_obs):
                idx = max_lag + t
                rv_comp[t] = np.mean(self.rv[idx - lag : idx])
            x_cols.append(rv_comp)

        x_mat = np.column_stack(x_cols)
        return x_mat, y

    def xǁHARRVǁ_build_regressors__mutmut_3(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Build the regression matrix and response vector.

        Returns
        -------
        tuple[ndarray, ndarray]
            (x_mat, y) where x_mat has columns [const, RV_d, RV_w, RV_m].
        """
        max_lag = max(self._component_lags[c] for c in self.components)
        total = None
        n_obs = total - max_lag

        if n_obs < 10:
            msg = f"Not enough observations. Need at least {max_lag + 10}, got {total}."
            raise ValueError(msg)

        y = self.rv[max_lag:]

        # Build regressors
        x_cols: list[NDArray[np.float64]] = [np.ones(n_obs)]  # constant

        for comp in self.components:
            lag = self._component_lags[comp]
            rv_comp = np.empty(n_obs)
            for t in range(n_obs):
                idx = max_lag + t
                rv_comp[t] = np.mean(self.rv[idx - lag : idx])
            x_cols.append(rv_comp)

        x_mat = np.column_stack(x_cols)
        return x_mat, y

    def xǁHARRVǁ_build_regressors__mutmut_4(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Build the regression matrix and response vector.

        Returns
        -------
        tuple[ndarray, ndarray]
            (x_mat, y) where x_mat has columns [const, RV_d, RV_w, RV_m].
        """
        max_lag = max(self._component_lags[c] for c in self.components)
        total = len(self.rv)
        n_obs = None

        if n_obs < 10:
            msg = f"Not enough observations. Need at least {max_lag + 10}, got {total}."
            raise ValueError(msg)

        y = self.rv[max_lag:]

        # Build regressors
        x_cols: list[NDArray[np.float64]] = [np.ones(n_obs)]  # constant

        for comp in self.components:
            lag = self._component_lags[comp]
            rv_comp = np.empty(n_obs)
            for t in range(n_obs):
                idx = max_lag + t
                rv_comp[t] = np.mean(self.rv[idx - lag : idx])
            x_cols.append(rv_comp)

        x_mat = np.column_stack(x_cols)
        return x_mat, y

    def xǁHARRVǁ_build_regressors__mutmut_5(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Build the regression matrix and response vector.

        Returns
        -------
        tuple[ndarray, ndarray]
            (x_mat, y) where x_mat has columns [const, RV_d, RV_w, RV_m].
        """
        max_lag = max(self._component_lags[c] for c in self.components)
        total = len(self.rv)
        n_obs = total + max_lag

        if n_obs < 10:
            msg = f"Not enough observations. Need at least {max_lag + 10}, got {total}."
            raise ValueError(msg)

        y = self.rv[max_lag:]

        # Build regressors
        x_cols: list[NDArray[np.float64]] = [np.ones(n_obs)]  # constant

        for comp in self.components:
            lag = self._component_lags[comp]
            rv_comp = np.empty(n_obs)
            for t in range(n_obs):
                idx = max_lag + t
                rv_comp[t] = np.mean(self.rv[idx - lag : idx])
            x_cols.append(rv_comp)

        x_mat = np.column_stack(x_cols)
        return x_mat, y

    def xǁHARRVǁ_build_regressors__mutmut_6(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Build the regression matrix and response vector.

        Returns
        -------
        tuple[ndarray, ndarray]
            (x_mat, y) where x_mat has columns [const, RV_d, RV_w, RV_m].
        """
        max_lag = max(self._component_lags[c] for c in self.components)
        total = len(self.rv)
        n_obs = total - max_lag

        if n_obs <= 10:
            msg = f"Not enough observations. Need at least {max_lag + 10}, got {total}."
            raise ValueError(msg)

        y = self.rv[max_lag:]

        # Build regressors
        x_cols: list[NDArray[np.float64]] = [np.ones(n_obs)]  # constant

        for comp in self.components:
            lag = self._component_lags[comp]
            rv_comp = np.empty(n_obs)
            for t in range(n_obs):
                idx = max_lag + t
                rv_comp[t] = np.mean(self.rv[idx - lag : idx])
            x_cols.append(rv_comp)

        x_mat = np.column_stack(x_cols)
        return x_mat, y

    def xǁHARRVǁ_build_regressors__mutmut_7(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Build the regression matrix and response vector.

        Returns
        -------
        tuple[ndarray, ndarray]
            (x_mat, y) where x_mat has columns [const, RV_d, RV_w, RV_m].
        """
        max_lag = max(self._component_lags[c] for c in self.components)
        total = len(self.rv)
        n_obs = total - max_lag

        if n_obs < 11:
            msg = f"Not enough observations. Need at least {max_lag + 10}, got {total}."
            raise ValueError(msg)

        y = self.rv[max_lag:]

        # Build regressors
        x_cols: list[NDArray[np.float64]] = [np.ones(n_obs)]  # constant

        for comp in self.components:
            lag = self._component_lags[comp]
            rv_comp = np.empty(n_obs)
            for t in range(n_obs):
                idx = max_lag + t
                rv_comp[t] = np.mean(self.rv[idx - lag : idx])
            x_cols.append(rv_comp)

        x_mat = np.column_stack(x_cols)
        return x_mat, y

    def xǁHARRVǁ_build_regressors__mutmut_8(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Build the regression matrix and response vector.

        Returns
        -------
        tuple[ndarray, ndarray]
            (x_mat, y) where x_mat has columns [const, RV_d, RV_w, RV_m].
        """
        max_lag = max(self._component_lags[c] for c in self.components)
        total = len(self.rv)
        n_obs = total - max_lag

        if n_obs < 10:
            msg = None
            raise ValueError(msg)

        y = self.rv[max_lag:]

        # Build regressors
        x_cols: list[NDArray[np.float64]] = [np.ones(n_obs)]  # constant

        for comp in self.components:
            lag = self._component_lags[comp]
            rv_comp = np.empty(n_obs)
            for t in range(n_obs):
                idx = max_lag + t
                rv_comp[t] = np.mean(self.rv[idx - lag : idx])
            x_cols.append(rv_comp)

        x_mat = np.column_stack(x_cols)
        return x_mat, y

    def xǁHARRVǁ_build_regressors__mutmut_9(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Build the regression matrix and response vector.

        Returns
        -------
        tuple[ndarray, ndarray]
            (x_mat, y) where x_mat has columns [const, RV_d, RV_w, RV_m].
        """
        max_lag = max(self._component_lags[c] for c in self.components)
        total = len(self.rv)
        n_obs = total - max_lag

        if n_obs < 10:
            msg = f"Not enough observations. Need at least {max_lag - 10}, got {total}."
            raise ValueError(msg)

        y = self.rv[max_lag:]

        # Build regressors
        x_cols: list[NDArray[np.float64]] = [np.ones(n_obs)]  # constant

        for comp in self.components:
            lag = self._component_lags[comp]
            rv_comp = np.empty(n_obs)
            for t in range(n_obs):
                idx = max_lag + t
                rv_comp[t] = np.mean(self.rv[idx - lag : idx])
            x_cols.append(rv_comp)

        x_mat = np.column_stack(x_cols)
        return x_mat, y

    def xǁHARRVǁ_build_regressors__mutmut_10(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Build the regression matrix and response vector.

        Returns
        -------
        tuple[ndarray, ndarray]
            (x_mat, y) where x_mat has columns [const, RV_d, RV_w, RV_m].
        """
        max_lag = max(self._component_lags[c] for c in self.components)
        total = len(self.rv)
        n_obs = total - max_lag

        if n_obs < 10:
            msg = f"Not enough observations. Need at least {max_lag + 11}, got {total}."
            raise ValueError(msg)

        y = self.rv[max_lag:]

        # Build regressors
        x_cols: list[NDArray[np.float64]] = [np.ones(n_obs)]  # constant

        for comp in self.components:
            lag = self._component_lags[comp]
            rv_comp = np.empty(n_obs)
            for t in range(n_obs):
                idx = max_lag + t
                rv_comp[t] = np.mean(self.rv[idx - lag : idx])
            x_cols.append(rv_comp)

        x_mat = np.column_stack(x_cols)
        return x_mat, y

    def xǁHARRVǁ_build_regressors__mutmut_11(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Build the regression matrix and response vector.

        Returns
        -------
        tuple[ndarray, ndarray]
            (x_mat, y) where x_mat has columns [const, RV_d, RV_w, RV_m].
        """
        max_lag = max(self._component_lags[c] for c in self.components)
        total = len(self.rv)
        n_obs = total - max_lag

        if n_obs < 10:
            msg = f"Not enough observations. Need at least {max_lag + 10}, got {total}."
            raise ValueError(None)

        y = self.rv[max_lag:]

        # Build regressors
        x_cols: list[NDArray[np.float64]] = [np.ones(n_obs)]  # constant

        for comp in self.components:
            lag = self._component_lags[comp]
            rv_comp = np.empty(n_obs)
            for t in range(n_obs):
                idx = max_lag + t
                rv_comp[t] = np.mean(self.rv[idx - lag : idx])
            x_cols.append(rv_comp)

        x_mat = np.column_stack(x_cols)
        return x_mat, y

    def xǁHARRVǁ_build_regressors__mutmut_12(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Build the regression matrix and response vector.

        Returns
        -------
        tuple[ndarray, ndarray]
            (x_mat, y) where x_mat has columns [const, RV_d, RV_w, RV_m].
        """
        max_lag = max(self._component_lags[c] for c in self.components)
        total = len(self.rv)
        n_obs = total - max_lag

        if n_obs < 10:
            msg = f"Not enough observations. Need at least {max_lag + 10}, got {total}."
            raise ValueError(msg)

        y = None

        # Build regressors
        x_cols: list[NDArray[np.float64]] = [np.ones(n_obs)]  # constant

        for comp in self.components:
            lag = self._component_lags[comp]
            rv_comp = np.empty(n_obs)
            for t in range(n_obs):
                idx = max_lag + t
                rv_comp[t] = np.mean(self.rv[idx - lag : idx])
            x_cols.append(rv_comp)

        x_mat = np.column_stack(x_cols)
        return x_mat, y

    def xǁHARRVǁ_build_regressors__mutmut_13(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Build the regression matrix and response vector.

        Returns
        -------
        tuple[ndarray, ndarray]
            (x_mat, y) where x_mat has columns [const, RV_d, RV_w, RV_m].
        """
        max_lag = max(self._component_lags[c] for c in self.components)
        total = len(self.rv)
        n_obs = total - max_lag

        if n_obs < 10:
            msg = f"Not enough observations. Need at least {max_lag + 10}, got {total}."
            raise ValueError(msg)

        y = self.rv[max_lag:]

        # Build regressors
        x_cols: list[NDArray[np.float64]] = None  # constant

        for comp in self.components:
            lag = self._component_lags[comp]
            rv_comp = np.empty(n_obs)
            for t in range(n_obs):
                idx = max_lag + t
                rv_comp[t] = np.mean(self.rv[idx - lag : idx])
            x_cols.append(rv_comp)

        x_mat = np.column_stack(x_cols)
        return x_mat, y

    def xǁHARRVǁ_build_regressors__mutmut_14(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Build the regression matrix and response vector.

        Returns
        -------
        tuple[ndarray, ndarray]
            (x_mat, y) where x_mat has columns [const, RV_d, RV_w, RV_m].
        """
        max_lag = max(self._component_lags[c] for c in self.components)
        total = len(self.rv)
        n_obs = total - max_lag

        if n_obs < 10:
            msg = f"Not enough observations. Need at least {max_lag + 10}, got {total}."
            raise ValueError(msg)

        y = self.rv[max_lag:]

        # Build regressors
        x_cols: list[NDArray[np.float64]] = [np.ones(None)]  # constant

        for comp in self.components:
            lag = self._component_lags[comp]
            rv_comp = np.empty(n_obs)
            for t in range(n_obs):
                idx = max_lag + t
                rv_comp[t] = np.mean(self.rv[idx - lag : idx])
            x_cols.append(rv_comp)

        x_mat = np.column_stack(x_cols)
        return x_mat, y

    def xǁHARRVǁ_build_regressors__mutmut_15(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Build the regression matrix and response vector.

        Returns
        -------
        tuple[ndarray, ndarray]
            (x_mat, y) where x_mat has columns [const, RV_d, RV_w, RV_m].
        """
        max_lag = max(self._component_lags[c] for c in self.components)
        total = len(self.rv)
        n_obs = total - max_lag

        if n_obs < 10:
            msg = f"Not enough observations. Need at least {max_lag + 10}, got {total}."
            raise ValueError(msg)

        y = self.rv[max_lag:]

        # Build regressors
        x_cols: list[NDArray[np.float64]] = [np.ones(n_obs)]  # constant

        for comp in self.components:
            lag = None
            rv_comp = np.empty(n_obs)
            for t in range(n_obs):
                idx = max_lag + t
                rv_comp[t] = np.mean(self.rv[idx - lag : idx])
            x_cols.append(rv_comp)

        x_mat = np.column_stack(x_cols)
        return x_mat, y

    def xǁHARRVǁ_build_regressors__mutmut_16(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Build the regression matrix and response vector.

        Returns
        -------
        tuple[ndarray, ndarray]
            (x_mat, y) where x_mat has columns [const, RV_d, RV_w, RV_m].
        """
        max_lag = max(self._component_lags[c] for c in self.components)
        total = len(self.rv)
        n_obs = total - max_lag

        if n_obs < 10:
            msg = f"Not enough observations. Need at least {max_lag + 10}, got {total}."
            raise ValueError(msg)

        y = self.rv[max_lag:]

        # Build regressors
        x_cols: list[NDArray[np.float64]] = [np.ones(n_obs)]  # constant

        for comp in self.components:
            lag = self._component_lags[comp]
            rv_comp = None
            for t in range(n_obs):
                idx = max_lag + t
                rv_comp[t] = np.mean(self.rv[idx - lag : idx])
            x_cols.append(rv_comp)

        x_mat = np.column_stack(x_cols)
        return x_mat, y

    def xǁHARRVǁ_build_regressors__mutmut_17(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Build the regression matrix and response vector.

        Returns
        -------
        tuple[ndarray, ndarray]
            (x_mat, y) where x_mat has columns [const, RV_d, RV_w, RV_m].
        """
        max_lag = max(self._component_lags[c] for c in self.components)
        total = len(self.rv)
        n_obs = total - max_lag

        if n_obs < 10:
            msg = f"Not enough observations. Need at least {max_lag + 10}, got {total}."
            raise ValueError(msg)

        y = self.rv[max_lag:]

        # Build regressors
        x_cols: list[NDArray[np.float64]] = [np.ones(n_obs)]  # constant

        for comp in self.components:
            lag = self._component_lags[comp]
            rv_comp = np.empty(None)
            for t in range(n_obs):
                idx = max_lag + t
                rv_comp[t] = np.mean(self.rv[idx - lag : idx])
            x_cols.append(rv_comp)

        x_mat = np.column_stack(x_cols)
        return x_mat, y

    def xǁHARRVǁ_build_regressors__mutmut_18(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Build the regression matrix and response vector.

        Returns
        -------
        tuple[ndarray, ndarray]
            (x_mat, y) where x_mat has columns [const, RV_d, RV_w, RV_m].
        """
        max_lag = max(self._component_lags[c] for c in self.components)
        total = len(self.rv)
        n_obs = total - max_lag

        if n_obs < 10:
            msg = f"Not enough observations. Need at least {max_lag + 10}, got {total}."
            raise ValueError(msg)

        y = self.rv[max_lag:]

        # Build regressors
        x_cols: list[NDArray[np.float64]] = [np.ones(n_obs)]  # constant

        for comp in self.components:
            lag = self._component_lags[comp]
            rv_comp = np.empty(n_obs)
            for t in range(None):
                idx = max_lag + t
                rv_comp[t] = np.mean(self.rv[idx - lag : idx])
            x_cols.append(rv_comp)

        x_mat = np.column_stack(x_cols)
        return x_mat, y

    def xǁHARRVǁ_build_regressors__mutmut_19(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Build the regression matrix and response vector.

        Returns
        -------
        tuple[ndarray, ndarray]
            (x_mat, y) where x_mat has columns [const, RV_d, RV_w, RV_m].
        """
        max_lag = max(self._component_lags[c] for c in self.components)
        total = len(self.rv)
        n_obs = total - max_lag

        if n_obs < 10:
            msg = f"Not enough observations. Need at least {max_lag + 10}, got {total}."
            raise ValueError(msg)

        y = self.rv[max_lag:]

        # Build regressors
        x_cols: list[NDArray[np.float64]] = [np.ones(n_obs)]  # constant

        for comp in self.components:
            lag = self._component_lags[comp]
            rv_comp = np.empty(n_obs)
            for t in range(n_obs):
                idx = None
                rv_comp[t] = np.mean(self.rv[idx - lag : idx])
            x_cols.append(rv_comp)

        x_mat = np.column_stack(x_cols)
        return x_mat, y

    def xǁHARRVǁ_build_regressors__mutmut_20(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Build the regression matrix and response vector.

        Returns
        -------
        tuple[ndarray, ndarray]
            (x_mat, y) where x_mat has columns [const, RV_d, RV_w, RV_m].
        """
        max_lag = max(self._component_lags[c] for c in self.components)
        total = len(self.rv)
        n_obs = total - max_lag

        if n_obs < 10:
            msg = f"Not enough observations. Need at least {max_lag + 10}, got {total}."
            raise ValueError(msg)

        y = self.rv[max_lag:]

        # Build regressors
        x_cols: list[NDArray[np.float64]] = [np.ones(n_obs)]  # constant

        for comp in self.components:
            lag = self._component_lags[comp]
            rv_comp = np.empty(n_obs)
            for t in range(n_obs):
                idx = max_lag - t
                rv_comp[t] = np.mean(self.rv[idx - lag : idx])
            x_cols.append(rv_comp)

        x_mat = np.column_stack(x_cols)
        return x_mat, y

    def xǁHARRVǁ_build_regressors__mutmut_21(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Build the regression matrix and response vector.

        Returns
        -------
        tuple[ndarray, ndarray]
            (x_mat, y) where x_mat has columns [const, RV_d, RV_w, RV_m].
        """
        max_lag = max(self._component_lags[c] for c in self.components)
        total = len(self.rv)
        n_obs = total - max_lag

        if n_obs < 10:
            msg = f"Not enough observations. Need at least {max_lag + 10}, got {total}."
            raise ValueError(msg)

        y = self.rv[max_lag:]

        # Build regressors
        x_cols: list[NDArray[np.float64]] = [np.ones(n_obs)]  # constant

        for comp in self.components:
            lag = self._component_lags[comp]
            rv_comp = np.empty(n_obs)
            for t in range(n_obs):
                idx = max_lag + t
                rv_comp[t] = None
            x_cols.append(rv_comp)

        x_mat = np.column_stack(x_cols)
        return x_mat, y

    def xǁHARRVǁ_build_regressors__mutmut_22(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Build the regression matrix and response vector.

        Returns
        -------
        tuple[ndarray, ndarray]
            (x_mat, y) where x_mat has columns [const, RV_d, RV_w, RV_m].
        """
        max_lag = max(self._component_lags[c] for c in self.components)
        total = len(self.rv)
        n_obs = total - max_lag

        if n_obs < 10:
            msg = f"Not enough observations. Need at least {max_lag + 10}, got {total}."
            raise ValueError(msg)

        y = self.rv[max_lag:]

        # Build regressors
        x_cols: list[NDArray[np.float64]] = [np.ones(n_obs)]  # constant

        for comp in self.components:
            lag = self._component_lags[comp]
            rv_comp = np.empty(n_obs)
            for t in range(n_obs):
                idx = max_lag + t
                rv_comp[t] = np.mean(None)
            x_cols.append(rv_comp)

        x_mat = np.column_stack(x_cols)
        return x_mat, y

    def xǁHARRVǁ_build_regressors__mutmut_23(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Build the regression matrix and response vector.

        Returns
        -------
        tuple[ndarray, ndarray]
            (x_mat, y) where x_mat has columns [const, RV_d, RV_w, RV_m].
        """
        max_lag = max(self._component_lags[c] for c in self.components)
        total = len(self.rv)
        n_obs = total - max_lag

        if n_obs < 10:
            msg = f"Not enough observations. Need at least {max_lag + 10}, got {total}."
            raise ValueError(msg)

        y = self.rv[max_lag:]

        # Build regressors
        x_cols: list[NDArray[np.float64]] = [np.ones(n_obs)]  # constant

        for comp in self.components:
            lag = self._component_lags[comp]
            rv_comp = np.empty(n_obs)
            for t in range(n_obs):
                idx = max_lag + t
                rv_comp[t] = np.mean(self.rv[idx + lag : idx])
            x_cols.append(rv_comp)

        x_mat = np.column_stack(x_cols)
        return x_mat, y

    def xǁHARRVǁ_build_regressors__mutmut_24(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Build the regression matrix and response vector.

        Returns
        -------
        tuple[ndarray, ndarray]
            (x_mat, y) where x_mat has columns [const, RV_d, RV_w, RV_m].
        """
        max_lag = max(self._component_lags[c] for c in self.components)
        total = len(self.rv)
        n_obs = total - max_lag

        if n_obs < 10:
            msg = f"Not enough observations. Need at least {max_lag + 10}, got {total}."
            raise ValueError(msg)

        y = self.rv[max_lag:]

        # Build regressors
        x_cols: list[NDArray[np.float64]] = [np.ones(n_obs)]  # constant

        for comp in self.components:
            lag = self._component_lags[comp]
            rv_comp = np.empty(n_obs)
            for t in range(n_obs):
                idx = max_lag + t
                rv_comp[t] = np.mean(self.rv[idx - lag : idx])
            x_cols.append(None)

        x_mat = np.column_stack(x_cols)
        return x_mat, y

    def xǁHARRVǁ_build_regressors__mutmut_25(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Build the regression matrix and response vector.

        Returns
        -------
        tuple[ndarray, ndarray]
            (x_mat, y) where x_mat has columns [const, RV_d, RV_w, RV_m].
        """
        max_lag = max(self._component_lags[c] for c in self.components)
        total = len(self.rv)
        n_obs = total - max_lag

        if n_obs < 10:
            msg = f"Not enough observations. Need at least {max_lag + 10}, got {total}."
            raise ValueError(msg)

        y = self.rv[max_lag:]

        # Build regressors
        x_cols: list[NDArray[np.float64]] = [np.ones(n_obs)]  # constant

        for comp in self.components:
            lag = self._component_lags[comp]
            rv_comp = np.empty(n_obs)
            for t in range(n_obs):
                idx = max_lag + t
                rv_comp[t] = np.mean(self.rv[idx - lag : idx])
            x_cols.append(rv_comp)

        x_mat = None
        return x_mat, y

    def xǁHARRVǁ_build_regressors__mutmut_26(
        self,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Build the regression matrix and response vector.

        Returns
        -------
        tuple[ndarray, ndarray]
            (x_mat, y) where x_mat has columns [const, RV_d, RV_w, RV_m].
        """
        max_lag = max(self._component_lags[c] for c in self.components)
        total = len(self.rv)
        n_obs = total - max_lag

        if n_obs < 10:
            msg = f"Not enough observations. Need at least {max_lag + 10}, got {total}."
            raise ValueError(msg)

        y = self.rv[max_lag:]

        # Build regressors
        x_cols: list[NDArray[np.float64]] = [np.ones(n_obs)]  # constant

        for comp in self.components:
            lag = self._component_lags[comp]
            rv_comp = np.empty(n_obs)
            for t in range(n_obs):
                idx = max_lag + t
                rv_comp[t] = np.mean(self.rv[idx - lag : idx])
            x_cols.append(rv_comp)

        x_mat = np.column_stack(None)
        return x_mat, y

    xǁHARRVǁ_build_regressors__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁHARRVǁ_build_regressors__mutmut_1": xǁHARRVǁ_build_regressors__mutmut_1,
        "xǁHARRVǁ_build_regressors__mutmut_2": xǁHARRVǁ_build_regressors__mutmut_2,
        "xǁHARRVǁ_build_regressors__mutmut_3": xǁHARRVǁ_build_regressors__mutmut_3,
        "xǁHARRVǁ_build_regressors__mutmut_4": xǁHARRVǁ_build_regressors__mutmut_4,
        "xǁHARRVǁ_build_regressors__mutmut_5": xǁHARRVǁ_build_regressors__mutmut_5,
        "xǁHARRVǁ_build_regressors__mutmut_6": xǁHARRVǁ_build_regressors__mutmut_6,
        "xǁHARRVǁ_build_regressors__mutmut_7": xǁHARRVǁ_build_regressors__mutmut_7,
        "xǁHARRVǁ_build_regressors__mutmut_8": xǁHARRVǁ_build_regressors__mutmut_8,
        "xǁHARRVǁ_build_regressors__mutmut_9": xǁHARRVǁ_build_regressors__mutmut_9,
        "xǁHARRVǁ_build_regressors__mutmut_10": xǁHARRVǁ_build_regressors__mutmut_10,
        "xǁHARRVǁ_build_regressors__mutmut_11": xǁHARRVǁ_build_regressors__mutmut_11,
        "xǁHARRVǁ_build_regressors__mutmut_12": xǁHARRVǁ_build_regressors__mutmut_12,
        "xǁHARRVǁ_build_regressors__mutmut_13": xǁHARRVǁ_build_regressors__mutmut_13,
        "xǁHARRVǁ_build_regressors__mutmut_14": xǁHARRVǁ_build_regressors__mutmut_14,
        "xǁHARRVǁ_build_regressors__mutmut_15": xǁHARRVǁ_build_regressors__mutmut_15,
        "xǁHARRVǁ_build_regressors__mutmut_16": xǁHARRVǁ_build_regressors__mutmut_16,
        "xǁHARRVǁ_build_regressors__mutmut_17": xǁHARRVǁ_build_regressors__mutmut_17,
        "xǁHARRVǁ_build_regressors__mutmut_18": xǁHARRVǁ_build_regressors__mutmut_18,
        "xǁHARRVǁ_build_regressors__mutmut_19": xǁHARRVǁ_build_regressors__mutmut_19,
        "xǁHARRVǁ_build_regressors__mutmut_20": xǁHARRVǁ_build_regressors__mutmut_20,
        "xǁHARRVǁ_build_regressors__mutmut_21": xǁHARRVǁ_build_regressors__mutmut_21,
        "xǁHARRVǁ_build_regressors__mutmut_22": xǁHARRVǁ_build_regressors__mutmut_22,
        "xǁHARRVǁ_build_regressors__mutmut_23": xǁHARRVǁ_build_regressors__mutmut_23,
        "xǁHARRVǁ_build_regressors__mutmut_24": xǁHARRVǁ_build_regressors__mutmut_24,
        "xǁHARRVǁ_build_regressors__mutmut_25": xǁHARRVǁ_build_regressors__mutmut_25,
        "xǁHARRVǁ_build_regressors__mutmut_26": xǁHARRVǁ_build_regressors__mutmut_26,
    }
    xǁHARRVǁ_build_regressors__mutmut_orig.__name__ = "xǁHARRVǁ_build_regressors"

    def fit(self, method: str = "ols") -> HARRVResults:
        args = [method]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁHARRVǁfit__mutmut_orig"),
            object.__getattribute__(self, "xǁHARRVǁfit__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁHARRVǁfit__mutmut_orig(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_1(self, method: str = "XXolsXX") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_2(self, method: str = "OLS") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_3(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = None
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_4(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = None

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_5(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method != "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_6(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "XXolsXX":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_7(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "OLS":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_8(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = None
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_9(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = None
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_10(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = None

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_11(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(None, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_12(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, None)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_13(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_14(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(
                xtx,
            )

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_15(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = None
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_16(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = None

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_17(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y + fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_18(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = None
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_19(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) * (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_20(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(None) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_21(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids * 2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_22(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**3) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_23(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n + k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_24(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = None
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_25(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 / np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_26(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(None)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_27(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = None
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_28(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(None)
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_29(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(None))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_30(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = None

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_31(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta * std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_32(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = None
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_33(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(None)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_34(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids * 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_35(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**3)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_36(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = None
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_37(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum(None)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_38(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) * 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_39(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y + np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_40(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(None)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_41(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 3)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_42(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = None
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_43(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(None)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_44(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 + ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_45(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(2.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_46(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res * ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_47(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = None

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_48(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(None)

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_49(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 + (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_50(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(2.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_51(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) * (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_52(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) / (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_53(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 + r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_54(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (2.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_55(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n + 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_56(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 2) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_57(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n + k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_58(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = None
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_59(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(None)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_60(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = None
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_61(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["XXbeta_0XX"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_62(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["BETA_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_63(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(None)

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_64(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[1]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_65(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=None,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_66(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=None,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_67(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=None,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_68(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=None,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_69(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=None,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_70(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=None,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_71(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=None,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_72(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=None,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_73(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=None,
        )

    def xǁHARRVǁfit__mutmut_74(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_75(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_76(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_77(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_78(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_79(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            residuals=resids,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_80(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            fitted_values=fitted,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_81(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            nobs=n,
        )

    def xǁHARRVǁfit__mutmut_82(self, method: str = "ols") -> HARRVResults:
        """Fit the HAR-RV model.

        Parameters
        ----------
        method : str
            Estimation method. 'ols' (default) or 'wls'.

        Returns
        -------
        HARRVResults
            Fitted model results.
        """
        x_mat, y = self._build_regressors()
        n, k = x_mat.shape

        if method == "ols":
            # OLS: beta = (X'X)^{-1} X'y
            xtx = x_mat.T @ x_mat
            xty = x_mat.T @ y
            beta = np.linalg.solve(xtx, xty)

            # Residuals and fitted values
            fitted = x_mat @ beta
            resids = y - fitted

            # Standard errors
            s2 = np.sum(resids**2) / (n - k)
            var_beta = s2 * np.linalg.inv(xtx)
            std_errors = np.sqrt(np.diag(var_beta))
            t_values = beta / std_errors

            # R-squared
            ss_res = np.sum(resids**2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = float(1.0 - ss_res / ss_tot)
            adj_r2 = float(1.0 - (1.0 - r2) * (n - 1) / (n - k))

        else:
            msg = f"Unknown method: {method}. Use 'ols'."
            raise ValueError(msg)

        param_names = ["beta_0"]
        for comp in self.components:
            param_names.append(f"beta_{comp[0]}")

        return HARRVResults(
            params=beta,
            param_names=param_names,
            std_errors=std_errors,
            t_values=t_values,
            r_squared=r2,
            adj_r_squared=adj_r2,
            residuals=resids,
            fitted_values=fitted,
        )

    xǁHARRVǁfit__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁHARRVǁfit__mutmut_1": xǁHARRVǁfit__mutmut_1,
        "xǁHARRVǁfit__mutmut_2": xǁHARRVǁfit__mutmut_2,
        "xǁHARRVǁfit__mutmut_3": xǁHARRVǁfit__mutmut_3,
        "xǁHARRVǁfit__mutmut_4": xǁHARRVǁfit__mutmut_4,
        "xǁHARRVǁfit__mutmut_5": xǁHARRVǁfit__mutmut_5,
        "xǁHARRVǁfit__mutmut_6": xǁHARRVǁfit__mutmut_6,
        "xǁHARRVǁfit__mutmut_7": xǁHARRVǁfit__mutmut_7,
        "xǁHARRVǁfit__mutmut_8": xǁHARRVǁfit__mutmut_8,
        "xǁHARRVǁfit__mutmut_9": xǁHARRVǁfit__mutmut_9,
        "xǁHARRVǁfit__mutmut_10": xǁHARRVǁfit__mutmut_10,
        "xǁHARRVǁfit__mutmut_11": xǁHARRVǁfit__mutmut_11,
        "xǁHARRVǁfit__mutmut_12": xǁHARRVǁfit__mutmut_12,
        "xǁHARRVǁfit__mutmut_13": xǁHARRVǁfit__mutmut_13,
        "xǁHARRVǁfit__mutmut_14": xǁHARRVǁfit__mutmut_14,
        "xǁHARRVǁfit__mutmut_15": xǁHARRVǁfit__mutmut_15,
        "xǁHARRVǁfit__mutmut_16": xǁHARRVǁfit__mutmut_16,
        "xǁHARRVǁfit__mutmut_17": xǁHARRVǁfit__mutmut_17,
        "xǁHARRVǁfit__mutmut_18": xǁHARRVǁfit__mutmut_18,
        "xǁHARRVǁfit__mutmut_19": xǁHARRVǁfit__mutmut_19,
        "xǁHARRVǁfit__mutmut_20": xǁHARRVǁfit__mutmut_20,
        "xǁHARRVǁfit__mutmut_21": xǁHARRVǁfit__mutmut_21,
        "xǁHARRVǁfit__mutmut_22": xǁHARRVǁfit__mutmut_22,
        "xǁHARRVǁfit__mutmut_23": xǁHARRVǁfit__mutmut_23,
        "xǁHARRVǁfit__mutmut_24": xǁHARRVǁfit__mutmut_24,
        "xǁHARRVǁfit__mutmut_25": xǁHARRVǁfit__mutmut_25,
        "xǁHARRVǁfit__mutmut_26": xǁHARRVǁfit__mutmut_26,
        "xǁHARRVǁfit__mutmut_27": xǁHARRVǁfit__mutmut_27,
        "xǁHARRVǁfit__mutmut_28": xǁHARRVǁfit__mutmut_28,
        "xǁHARRVǁfit__mutmut_29": xǁHARRVǁfit__mutmut_29,
        "xǁHARRVǁfit__mutmut_30": xǁHARRVǁfit__mutmut_30,
        "xǁHARRVǁfit__mutmut_31": xǁHARRVǁfit__mutmut_31,
        "xǁHARRVǁfit__mutmut_32": xǁHARRVǁfit__mutmut_32,
        "xǁHARRVǁfit__mutmut_33": xǁHARRVǁfit__mutmut_33,
        "xǁHARRVǁfit__mutmut_34": xǁHARRVǁfit__mutmut_34,
        "xǁHARRVǁfit__mutmut_35": xǁHARRVǁfit__mutmut_35,
        "xǁHARRVǁfit__mutmut_36": xǁHARRVǁfit__mutmut_36,
        "xǁHARRVǁfit__mutmut_37": xǁHARRVǁfit__mutmut_37,
        "xǁHARRVǁfit__mutmut_38": xǁHARRVǁfit__mutmut_38,
        "xǁHARRVǁfit__mutmut_39": xǁHARRVǁfit__mutmut_39,
        "xǁHARRVǁfit__mutmut_40": xǁHARRVǁfit__mutmut_40,
        "xǁHARRVǁfit__mutmut_41": xǁHARRVǁfit__mutmut_41,
        "xǁHARRVǁfit__mutmut_42": xǁHARRVǁfit__mutmut_42,
        "xǁHARRVǁfit__mutmut_43": xǁHARRVǁfit__mutmut_43,
        "xǁHARRVǁfit__mutmut_44": xǁHARRVǁfit__mutmut_44,
        "xǁHARRVǁfit__mutmut_45": xǁHARRVǁfit__mutmut_45,
        "xǁHARRVǁfit__mutmut_46": xǁHARRVǁfit__mutmut_46,
        "xǁHARRVǁfit__mutmut_47": xǁHARRVǁfit__mutmut_47,
        "xǁHARRVǁfit__mutmut_48": xǁHARRVǁfit__mutmut_48,
        "xǁHARRVǁfit__mutmut_49": xǁHARRVǁfit__mutmut_49,
        "xǁHARRVǁfit__mutmut_50": xǁHARRVǁfit__mutmut_50,
        "xǁHARRVǁfit__mutmut_51": xǁHARRVǁfit__mutmut_51,
        "xǁHARRVǁfit__mutmut_52": xǁHARRVǁfit__mutmut_52,
        "xǁHARRVǁfit__mutmut_53": xǁHARRVǁfit__mutmut_53,
        "xǁHARRVǁfit__mutmut_54": xǁHARRVǁfit__mutmut_54,
        "xǁHARRVǁfit__mutmut_55": xǁHARRVǁfit__mutmut_55,
        "xǁHARRVǁfit__mutmut_56": xǁHARRVǁfit__mutmut_56,
        "xǁHARRVǁfit__mutmut_57": xǁHARRVǁfit__mutmut_57,
        "xǁHARRVǁfit__mutmut_58": xǁHARRVǁfit__mutmut_58,
        "xǁHARRVǁfit__mutmut_59": xǁHARRVǁfit__mutmut_59,
        "xǁHARRVǁfit__mutmut_60": xǁHARRVǁfit__mutmut_60,
        "xǁHARRVǁfit__mutmut_61": xǁHARRVǁfit__mutmut_61,
        "xǁHARRVǁfit__mutmut_62": xǁHARRVǁfit__mutmut_62,
        "xǁHARRVǁfit__mutmut_63": xǁHARRVǁfit__mutmut_63,
        "xǁHARRVǁfit__mutmut_64": xǁHARRVǁfit__mutmut_64,
        "xǁHARRVǁfit__mutmut_65": xǁHARRVǁfit__mutmut_65,
        "xǁHARRVǁfit__mutmut_66": xǁHARRVǁfit__mutmut_66,
        "xǁHARRVǁfit__mutmut_67": xǁHARRVǁfit__mutmut_67,
        "xǁHARRVǁfit__mutmut_68": xǁHARRVǁfit__mutmut_68,
        "xǁHARRVǁfit__mutmut_69": xǁHARRVǁfit__mutmut_69,
        "xǁHARRVǁfit__mutmut_70": xǁHARRVǁfit__mutmut_70,
        "xǁHARRVǁfit__mutmut_71": xǁHARRVǁfit__mutmut_71,
        "xǁHARRVǁfit__mutmut_72": xǁHARRVǁfit__mutmut_72,
        "xǁHARRVǁfit__mutmut_73": xǁHARRVǁfit__mutmut_73,
        "xǁHARRVǁfit__mutmut_74": xǁHARRVǁfit__mutmut_74,
        "xǁHARRVǁfit__mutmut_75": xǁHARRVǁfit__mutmut_75,
        "xǁHARRVǁfit__mutmut_76": xǁHARRVǁfit__mutmut_76,
        "xǁHARRVǁfit__mutmut_77": xǁHARRVǁfit__mutmut_77,
        "xǁHARRVǁfit__mutmut_78": xǁHARRVǁfit__mutmut_78,
        "xǁHARRVǁfit__mutmut_79": xǁHARRVǁfit__mutmut_79,
        "xǁHARRVǁfit__mutmut_80": xǁHARRVǁfit__mutmut_80,
        "xǁHARRVǁfit__mutmut_81": xǁHARRVǁfit__mutmut_81,
        "xǁHARRVǁfit__mutmut_82": xǁHARRVǁfit__mutmut_82,
    }
    xǁHARRVǁfit__mutmut_orig.__name__ = "xǁHARRVǁfit"
