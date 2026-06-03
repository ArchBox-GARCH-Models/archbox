"""Workflow helper functions for complete end-to-end volatility modeling.

Provides pipeline functions that integrate all archbox modules:
univariate models, multivariate models, risk measures, and diagnostics.
"""

import numpy as np
import pandas as pd

from archbox.diagnostics import arch_lm_test, full_diagnostics
from archbox.models import EGARCH, GARCH, GJRGARCH
from archbox.multivariate import CCC, DCC
from archbox.risk import ExpectedShortfall, ValueAtRisk, VaRBacktest

# ---------------------------------------------------------------------------
# Model registry
# ---------------------------------------------------------------------------

UNIVARIATE_MODELS = {
    "GARCH(1,1)": lambda y: GARCH(y, p=1, q=1),
    "GARCH(2,1)": lambda y: GARCH(y, p=2, q=1),
    "EGARCH(1,1)": lambda y: EGARCH(y, p=1, q=1),
    "GJR-GARCH(1,1)": lambda y: GJRGARCH(y, p=1, q=1),
}

MULTIVARIATE_MODELS = {
    "CCC": lambda y: CCC(y),
    "DCC": lambda y: DCC(y),
}


def run_univariate_pipeline(returns, models=None, alpha=0.05):
    """Run the complete univariate volatility modeling pipeline.

    Pipeline steps:
    1. ARCH-LM test for heteroskedasticity
    2. Fit multiple GARCH-family models
    3. Run diagnostics on each fitted model
    4. Compute VaR and ES for each model
    5. Run backtesting on VaR estimates

    Parameters
    ----------
    returns : array-like
        Return series (1-d).
    models : dict or None
        Dictionary mapping model names to callables that accept returns
        and return an unfitted model. If None, uses default model set.
    alpha : float
        Significance level for VaR/ES (default 0.05).

    Returns
    -------
    dict
        Keys: 'arch_lm', 'fitted', 'diagnostics', 'var', 'es', 'backtest'.
    """
    if models is None:
        models = UNIVARIATE_MODELS

    returns_arr = np.asarray(returns).ravel()
    results = {
        "arch_lm": None,
        "fitted": {},
        "diagnostics": {},
        "var": {},
        "es": {},
        "backtest": {},
    }

    # Step 1: Test for ARCH effects
    results["arch_lm"] = arch_lm_test(returns_arr, lags=5)

    # Step 2-3: Fit models and run diagnostics
    for name, model_fn in models.items():
        try:
            model = model_fn(returns_arr)
            fit = model.fit(disp=False)
            results["fitted"][name] = fit

            # Diagnostics
            results["diagnostics"][name] = full_diagnostics(fit)

            # Step 4: VaR and ES
            var_calc = ValueAtRisk(fit, alpha=alpha)
            var_series = var_calc.parametric(dist="normal")
            results["var"][name] = var_series

            es_calc = ExpectedShortfall(fit, alpha=alpha)
            es_series = es_calc.parametric(dist="normal")
            results["es"][name] = es_series

            # Step 5: Backtesting
            bt = VaRBacktest(returns_arr, var_series, alpha=alpha)
            results["backtest"][name] = {
                "kupiec": bt.kupiec_test(),
                "christoffersen": bt.christoffersen_test(),
                "violation_ratio": bt.violation_ratio(),
            }
        except Exception as e:
            results["fitted"][name] = f"Error: {e}"

    return results


def run_multivariate_pipeline(returns_matrix, models=None, alpha=0.05):
    """Run the complete multivariate volatility modeling pipeline.

    Pipeline steps:
    1. Fit multivariate GARCH models (CCC, DCC)
    2. Extract conditional covariance matrices
    3. Compute portfolio risk measures

    Parameters
    ----------
    returns_matrix : array-like
        Multivariate return matrix (T x k).
    models : dict or None
        Dictionary mapping model names to callables. If None, uses defaults.
    alpha : float
        Significance level for risk measures.

    Returns
    -------
    dict
        Keys: 'fitted', 'covariances', 'correlations'.
    """
    if models is None:
        models = MULTIVARIATE_MODELS

    returns_arr = np.asarray(returns_matrix)
    results = {
        "fitted": {},
        "covariances": {},
        "correlations": {},
    }

    for name, model_fn in models.items():
        try:
            model = model_fn(returns_arr)
            fit = model.fit(disp=False)
            results["fitted"][name] = fit

            # Forecast one-step-ahead covariance
            forecast = model.forecast(fit, horizon=1)
            results["covariances"][name] = forecast.get("covariance")
            results["correlations"][name] = forecast.get("correlation")
        except Exception as e:
            results["fitted"][name] = f"Error: {e}"

    return results


def generate_comparison_report(results_dict):
    """Generate a consolidated DataFrame comparing model performance.

    Parameters
    ----------
    results_dict : dict
        Output from ``run_univariate_pipeline``.

    Returns
    -------
    pd.DataFrame
        Comparison table with columns: Model, LogLik, AIC, BIC,
        Persistence, VR (violation ratio), Kupiec_pval, CC_pval.
    """
    rows = []
    fitted = results_dict.get("fitted", {})
    backtest = results_dict.get("backtest", {})

    for name, fit in fitted.items():
        if isinstance(fit, str):
            # Model failed to fit
            rows.append(
                {
                    "Model": name,
                    "LogLik": np.nan,
                    "AIC": np.nan,
                    "BIC": np.nan,
                    "Persistence": np.nan,
                    "VR": np.nan,
                    "Kupiec_pval": np.nan,
                    "CC_pval": np.nan,
                }
            )
            continue

        row = {
            "Model": name,
            "LogLik": fit.loglike,
            "AIC": fit.aic,
            "BIC": fit.bic,
            "Persistence": fit.persistence(),
        }

        bt = backtest.get(name, {})
        if bt:
            row["VR"] = bt.get("violation_ratio", np.nan)
            kupiec = bt.get("kupiec")
            row["Kupiec_pval"] = kupiec.pvalue if kupiec else np.nan
            cc = bt.get("christoffersen")
            row["CC_pval"] = cc.pvalue if cc else np.nan
        else:
            row["VR"] = np.nan
            row["Kupiec_pval"] = np.nan
            row["CC_pval"] = np.nan

        rows.append(row)

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values("AIC").reset_index(drop=True)
    return df


def run_backtesting_suite(returns, var_dict, alpha=0.05):
    """Run backtesting suite on multiple VaR series.

    Parameters
    ----------
    returns : array-like
        Return series.
    var_dict : dict
        Dictionary mapping model names to VaR series.
    alpha : float
        Significance level.

    Returns
    -------
    pd.DataFrame
        Backtesting results with Kupiec and Christoffersen test statistics.
    """
    returns_arr = np.asarray(returns).ravel()
    rows = []

    for name, var_series in var_dict.items():
        bt = VaRBacktest(returns_arr, var_series, alpha=alpha)
        kupiec = bt.kupiec_test()
        cc = bt.christoffersen_test()
        rows.append(
            {
                "Model": name,
                "Violations": int(np.sum(returns_arr < -np.abs(var_series))),
                "VR": bt.violation_ratio(),
                "Kupiec_stat": kupiec.statistic,
                "Kupiec_pval": kupiec.pvalue,
                "CC_stat": cc.statistic,
                "CC_pval": cc.pvalue,
                "Basel_TL": bt.basel_traffic_light(),
            }
        )

    return pd.DataFrame(rows)
