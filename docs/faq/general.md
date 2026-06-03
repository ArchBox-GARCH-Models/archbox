---
title: "General FAQ"
description: "Frequently asked questions about ArchBox — installation, data formats, model selection, distributions, and results interpretation."
---

# General FAQ

Common questions for beginners and intermediate users of ArchBox.

!!! tip "Looking for more?"
    - **Advanced topics** (convergence, GPU, model averaging): [Advanced FAQ](advanced.md)
    - **Error messages and debugging**: [Troubleshooting](troubleshooting.md)

---

## Getting Started

??? question "How do I install ArchBox?"

    Install from PyPI:

    ```bash
    pip install archbox
    ```

    For the full installation with all optional dependencies:

    ```bash
    pip install archbox[all]
    ```

    Verify the installation:

    ```python
    import archbox
    print(archbox.__version__)
    ```

    See the [Installation Guide](../getting-started/installation.md) for detailed instructions, including conda and development installs.

??? question "What data formats are supported?"

    ArchBox accepts three input formats for univariate models:

    === "pandas Series"

        ```python
        import pandas as pd
        from archbox.models import GARCH

        returns = pd.Series([0.01, -0.02, 0.015, ...], name="returns")
        model = GARCH(returns, p=1, q=1)
        result = model.fit()
        ```

    === "pandas DataFrame"

        ```python
        import pandas as pd
        from archbox.models import GARCH

        df = pd.read_csv("data.csv", parse_dates=["date"], index_col="date")
        model = GARCH(df["returns"], p=1, q=1)
        result = model.fit()
        ```

    === "numpy array"

        ```python
        import numpy as np
        from archbox.models import GARCH

        returns = np.random.randn(1000) * 0.01
        model = GARCH(returns, p=1, q=1)
        result = model.fit()
        ```

    For **multivariate models** (DCC, BEKK, etc.), use a pandas DataFrame where each column is an asset:

    ```python
    from archbox.multivariate import DCC

    # DataFrame with columns: ['PETR4', 'VALE3', 'ITUB4']
    model = DCC(returns_df, p=1, q=1)
    result = model.fit()
    ```

    !!! note
        Data should be **returns** (log-returns or simple returns), not prices. ArchBox does not automatically convert prices to returns.

---

## Model Selection

??? question "How do I choose between GARCH and EGARCH?"

    The choice depends on whether you need to capture **leverage effects** (asymmetric response to positive vs. negative shocks):

    | Feature | GARCH(1,1) | EGARCH(1,1) |
    |---------|-----------|-------------|
    | Leverage effects | No | Yes |
    | Positivity constraint | Required ($\alpha, \beta \geq 0$) | Not needed (log variance) |
    | Interpretation | Direct | Through exponential |
    | Speed | Faster | Slightly slower |
    | Best for | Symmetric volatility | Asymmetric volatility |

    **Decision rule:**

    1. Run the **Sign Bias test** on your data
    2. If significant asymmetry: use **EGARCH** or **GJR-GARCH**
    3. If symmetric: use **GARCH** for simplicity

    ```python
    from archbox.diagnostics import sign_bias_test

    result = sign_bias_test(residuals)
    print(result.summary())
    # If p-value < 0.05 → consider asymmetric models
    ```

    !!! tip
        GJR-GARCH is a good middle ground — it captures asymmetry while remaining easy to interpret.

??? question "Which distribution should I use?"

    ArchBox supports several error distributions:

    | Distribution | When to use | Tail behavior |
    |-------------|------------|---------------|
    | **Normal** | Default, symmetric data | Thin tails |
    | **Student-t** | Heavy tails, financial data | Heavy tails (symmetric) |
    | **Skewed Student-t** | Asymmetric heavy tails | Heavy + skewed tails |
    | **GED** | Moderate heavy tails | Flexible kurtosis |
    | **Skewed GED** | Asymmetric moderate tails | Flexible kurtosis + skew |

    **Practical approach:**

    1. Start with **Student-t** — it works well for most financial time series
    2. Use **information criteria** (AIC/BIC) to compare distributions
    3. Use the **Kolmogorov-Smirnov test** to validate the fit

    ```python
    from archbox.models import GARCH

    # Compare distributions
    for dist in ["normal", "student-t", "skewed-t", "ged"]:
        model = GARCH(returns, p=1, q=1, dist=dist)
        result = model.fit()
        print(f"{dist}: AIC={result.aic:.2f}, BIC={result.bic:.2f}")
    ```

    !!! tip
        For risk management applications (VaR/ES), **Student-t** or **Skewed-t** typically provide better tail coverage than Normal.

---

## Using Results

??? question "How do I interpret the summary output?"

    The `summary()` method displays key estimation results:

    ```python
    result = model.fit()
    print(result.summary())
    ```

    ```
    GARCH(1,1) Model Results
    ========================
    Distribution: Student-t
    Log-Likelihood: -2845.32
    AIC: 5700.64    BIC: 5725.12
    Observations: 2500

    Parameters:
                Estimate  Std.Error  t-stat  p-value
    omega       0.0001    0.00003    3.33    0.0009
    alpha[1]    0.0850    0.0120     7.08    0.0000
    beta[1]     0.9020    0.0130    69.38    0.0000
    nu          6.5400    0.8200     7.98    0.0000
    ```

    **Key elements:**

    - **omega ($\omega$)**: Long-run variance constant. Small positive value expected
    - **alpha ($\alpha$)**: ARCH effect — sensitivity to past shocks. Typically 0.03–0.15
    - **beta ($\beta$)**: GARCH effect — persistence. Typically 0.80–0.95
    - **alpha + beta**: Persistence — closer to 1 means volatility shocks decay slowly
    - **nu ($\nu$)**: Degrees of freedom (Student-t). Lower values = heavier tails
    - **AIC/BIC**: Lower is better for model comparison

    !!! warning
        If $\alpha + \beta \geq 1$, the process is **integrated** (IGARCH) — volatility shocks do not decay. Consider using the IGARCH model explicitly.

??? question "How do I export results?"

    ArchBox provides multiple export options:

    === "DataFrame"

        ```python
        # Parameters as DataFrame
        params_df = result.params_df
        params_df.to_csv("parameters.csv")
        ```

    === "Dictionary"

        ```python
        # All results as dictionary
        results_dict = {
            "params": result.params,
            "log_likelihood": result.loglikelihood,
            "aic": result.aic,
            "bic": result.bic,
            "conditional_volatility": result.conditional_volatility,
        }
        ```

    === "Volatility Series"

        ```python
        # Export conditional volatility
        vol = result.conditional_volatility
        vol.to_csv("volatility.csv")

        # Plot
        vol.plot(title="Conditional Volatility")
        ```

---

## Comparison

??? question "What is the difference between ArchBox and arch (Kevin Sheppard)?"

    Both libraries estimate GARCH-family models, but they differ in scope and focus:

    | Feature | ArchBox | arch |
    |---------|---------|------|
    | **Univariate GARCH** | GARCH, EGARCH, GJR, APARCH, FIGARCH, IGARCH, GARCH-M, Component | GARCH, EGARCH, GJR, APARCH, FIGARCH, HARCH |
    | **Multivariate** | DCC, BEKK, CCC, GO-GARCH, DECO | Not available |
    | **Regime-Switching** | MS-AR, MS-VAR, MS-GARCH | Not available |
    | **Threshold/STAR** | TAR, SETAR, LSTAR, ESTAR | Not available |
    | **Risk Management** | VaR, ES, EWMA, Backtesting | Basic VaR |
    | **HAR-RV** | Full HAR framework | Not available |
    | **Diagnostics** | Comprehensive suite | Basic |
    | **Visualization** | Built-in plots | Not available |
    | **Maturity** | Newer project | Mature, well-tested |
    | **Backend** | NumPy/SciPy | NumPy/SciPy + Cython |

    !!! info
        `arch` by Kevin Sheppard is a mature, well-tested library focused on univariate volatility models. ArchBox extends the scope to multivariate models, regime-switching, threshold models, and integrated risk management.

??? question "Does ArchBox work with intraday data?"

    Yes, ArchBox works with **any frequency** of return data:

    - **Daily returns**: most common use case
    - **Intraday returns**: 1-min, 5-min, hourly — works well with GARCH models
    - **Weekly/monthly returns**: valid but fewer observations for estimation

    ```python
    import pandas as pd
    from archbox.models import GARCH

    # 5-minute returns
    intraday = pd.read_csv("intraday.csv", parse_dates=["timestamp"], index_col="timestamp")
    model = GARCH(intraday["returns"], p=1, q=1)
    result = model.fit()
    ```

    !!! tip "HAR-RV for realized volatility"
        For intraday data, consider using the **HAR-RV** (Heterogeneous Autoregressive Realized Volatility) model, which is specifically designed to work with high-frequency realized measures:

        ```python
        from archbox.models import HARRV

        model = HARRV(realized_variance, lags=[1, 5, 22])
        result = model.fit()
        ```

    !!! warning
        Be mindful of **microstructure noise** in very high-frequency data (< 1 min). Consider using realized kernels or pre-averaging before feeding data to GARCH models.
