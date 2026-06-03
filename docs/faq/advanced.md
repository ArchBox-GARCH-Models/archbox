---
title: "Advanced FAQ"
description: "Advanced FAQ for ArchBox — optimizer convergence, custom constraints, GPU acceleration, model averaging, DCC scaling, regime selection, and STAR tuning."
---

# Advanced FAQ

Advanced questions about estimation, convergence, scaling, and model configuration.

!!! tip "Looking for basics?"
    - **General questions**: [General FAQ](general.md)
    - **Error messages and debugging**: [Troubleshooting](troubleshooting.md)

---

## Optimization & Convergence

??? question "The optimizer does not converge — what should I do?"

    Non-convergence is the most common issue in GARCH estimation. Here is a systematic approach:

    **1. Rescale your data**

    Returns should be in decimal form (e.g., 0.01 for 1%). Large values cause numerical issues:

    ```python
    # Bad: percentage returns
    returns = prices.pct_change().dropna() * 100  # values like 1.5, -2.3

    # Good: decimal returns
    returns = prices.pct_change().dropna()  # values like 0.015, -0.023
    ```

    **2. Try different starting values**

    ```python
    from archbox.models import GARCH

    model = GARCH(returns, p=1, q=1)

    # Custom starting values: [omega, alpha, beta]
    result = model.fit(starting_values=[1e-5, 0.05, 0.90])
    ```

    **3. Change the optimizer**

    ```python
    # Try different optimization methods
    result = model.fit(method="L-BFGS-B")    # default
    result = model.fit(method="Nelder-Mead")  # gradient-free
    result = model.fit(method="SLSQP")        # constrained
    ```

    **4. Increase iterations**

    ```python
    result = model.fit(maxiter=5000)
    ```

    **5. Simplify the model**

    If EGARCH(2,2) does not converge, try EGARCH(1,1) first, then increase order.

    !!! warning
        If none of these work, the data may not be suitable for GARCH modeling. Check for unit roots, structural breaks, or excessive zeros.

??? question "How do I handle data with many zeros?"

    Zeros in return data (e.g., illiquid assets) can cause estimation problems:

    **Diagnosis:**

    ```python
    import numpy as np

    zero_pct = (returns == 0).mean() * 100
    print(f"Percentage of zeros: {zero_pct:.1f}%")
    ```

    **Solutions by severity:**

    | Zero % | Approach |
    |--------|----------|
    | < 5% | Proceed normally — zeros are unlikely to cause issues |
    | 5–20% | Use **Student-t** distribution (more robust to zero clustering) |
    | 20–50% | Consider filtering or using a mixture distribution |
    | > 50% | Data is too sparse for GARCH — consider alternative approaches |

    ```python
    from archbox.models import GARCH

    # Use robust distribution
    model = GARCH(returns, p=1, q=1, dist="student-t")
    result = model.fit()
    ```

    !!! tip
        For highly illiquid assets, consider aggregating to a lower frequency (weekly or monthly) to reduce the proportion of zeros.

??? question "How do I estimate GARCH with custom constraints?"

    ArchBox uses `scipy.optimize.minimize` with box constraints. You can customize bounds:

    ```python
    from archbox.models import GARCH

    model = GARCH(returns, p=1, q=1)

    # Custom parameter bounds: (lower, upper) for each parameter
    # Parameters: [omega, alpha[1], beta[1]]
    bounds = [
        (1e-8, 1e-2),   # omega: keep small
        (0.01, 0.30),    # alpha: restrict range
        (0.50, 0.99),    # beta: ensure high persistence
    ]

    result = model.fit(bounds=bounds)
    ```

    **Stationarity constraint** ($\alpha + \beta < 1$):

    This is enforced by default. To relax it (e.g., for IGARCH):

    ```python
    from archbox.models import IGARCH

    # IGARCH enforces alpha + beta = 1
    model = IGARCH(returns, p=1, q=1)
    result = model.fit()
    ```

    !!! note
        Custom constraints are useful for ensuring economically meaningful parameters, but overly tight bounds can prevent convergence.

---

## Acceleration & Scaling

??? question "Can I use GPU to accelerate estimation?"

    Currently, ArchBox is **CPU-only** and relies on NumPy/SciPy for numerical computation. GPU acceleration is not natively supported.

    **To maximize CPU performance:**

    1. **Use MKL-backed NumPy** for optimized linear algebra:

        ```bash
        pip install numpy  # pip version uses OpenBLAS by default
        conda install numpy  # conda version often uses MKL
        ```

    2. **Leverage multi-core** for batch estimation:

        ```python
        from concurrent.futures import ProcessPoolExecutor
        from archbox.models import GARCH

        def fit_one(col):
            model = GARCH(data[col], p=1, q=1)
            return model.fit()

        with ProcessPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(fit_one, data.columns))
        ```

    3. **Use ArchExperiment** for systematic model comparison:

        ```python
        from archbox.experiment import ArchExperiment

        exp = ArchExperiment(returns)
        exp.compare_models(["GARCH", "EGARCH", "GJR"], orders=[(1,1), (2,1)])
        ```

    !!! info "Roadmap"
        GPU acceleration via JAX or CuPy is on the long-term roadmap. For now, NumPy with MKL provides excellent single-core performance.

??? question "How do I estimate DCC with more than 50 assets?"

    DCC estimation scales as $O(N^2)$ in the number of assets and can become very slow for large $N$. Strategies for large portfolios:

    **1. Use DECO (Dynamic Equicorrelation)**

    DECO assumes a single dynamic equicorrelation parameter — much faster than full DCC:

    ```python
    from archbox.multivariate import DECO

    # 100 assets — DECO scales linearly
    model = DECO(returns_100, p=1, q=1)
    result = model.fit()
    ```

    **2. Block-diagonal DCC**

    Group assets by sector and estimate DCC within blocks:

    ```python
    from archbox.multivariate import DCC

    # Estimate by sector
    sectors = {"tech": tech_cols, "finance": fin_cols, "energy": energy_cols}
    results = {}
    for name, cols in sectors.items():
        model = DCC(returns[cols], p=1, q=1)
        results[name] = model.fit()
    ```

    **3. Factor-DCC**

    Use principal components to reduce dimensionality:

    ```python
    from sklearn.decomposition import PCA
    from archbox.multivariate import DCC

    pca = PCA(n_components=10)
    factors = pca.fit_transform(returns)

    model = DCC(factors, p=1, q=1)
    result = model.fit()
    ```

    | Method | Max assets | Speed | Accuracy |
    |--------|-----------|-------|----------|
    | Full DCC | ~30 | Slow | Full |
    | DECO | 200+ | Fast | Approximate |
    | Block DCC | 100+ | Medium | Sector-level |
    | Factor DCC | 200+ | Fast | PCA-dependent |

    !!! tip
        For portfolios with > 100 assets, DECO or Factor-DCC are strongly recommended. Full DCC becomes numerically unstable beyond ~50 assets.

---

## Model Configuration

??? question "How do I combine models (model averaging)?"

    Model averaging produces forecasts that are weighted combinations of multiple models, reducing model uncertainty:

    **AIC/BIC-based weights:**

    ```python
    import numpy as np
    from archbox.models import GARCH, EGARCH, GJR

    models = {
        "GARCH": GARCH(returns, p=1, q=1),
        "EGARCH": EGARCH(returns, p=1, q=1),
        "GJR": GJR(returns, p=1, q=1),
    }

    results = {name: m.fit() for name, m in models.items()}

    # AIC-based weights (Burnham & Anderson, 2002)
    aics = np.array([r.aic for r in results.values()])
    delta = aics - aics.min()
    weights = np.exp(-0.5 * delta)
    weights /= weights.sum()

    for name, w in zip(results.keys(), weights):
        print(f"{name}: weight = {w:.3f}")
    ```

    **Averaged volatility forecast:**

    ```python
    # Weighted average of conditional volatility
    avg_vol = sum(
        w * r.conditional_volatility
        for w, r in zip(weights, results.values())
    )
    ```

    !!! tip
        Model averaging is especially useful for risk management, where underestimating tail risk from a single model can be costly.

??? question "MS-GARCH: how do I choose the number of regimes?"

    The number of regimes in Markov-Switching models is a model selection problem. Common approaches:

    **1. Information criteria**

    ```python
    from archbox.regime import MSGARCH

    for k in [2, 3, 4]:
        model = MSGARCH(returns, n_regimes=k, p=1, q=1)
        result = model.fit()
        print(f"K={k}: AIC={result.aic:.2f}, BIC={result.bic:.2f}")
    ```

    !!! warning
        Standard likelihood ratio tests are **not valid** for testing the number of regimes (Davies problem). Use information criteria instead.

    **2. Economic interpretation**

    - **K=2**: Low/high volatility regimes — most common for financial data
    - **K=3**: Low/medium/high — useful for crisis analysis
    - **K=4+**: Rarely needed and prone to overfitting

    **3. Regime stability**

    Check that each regime has a reasonable number of observations:

    ```python
    result = model.fit()

    # Smoothed probabilities
    probs = result.smoothed_probabilities

    # Check regime occupation
    for k in range(n_regimes):
        occupation = (probs[:, k] > 0.5).mean()
        print(f"Regime {k}: {occupation:.1%} of observations")
    ```

    !!! tip
        Start with **K=2** — it is the most robust choice for financial data and captures the essential low/high volatility dynamics. Only add regimes if there is clear economic motivation.

??? question "STAR: gamma is too large or too small — what does it mean?"

    In Smooth Transition (LSTAR/ESTAR) models, the transition parameter $\gamma$ controls the speed of regime switching:

    $$
    G(s_t; \gamma, c) = \frac{1}{1 + \exp(-\gamma(s_t - c))}
    $$

    | $\gamma$ value | Interpretation | Issue |
    |---------------|---------------|-------|
    | Very small ($< 1$) | Almost linear transition | Model collapses to linear |
    | Moderate (1–100) | Smooth nonlinear transition | Ideal range |
    | Very large ($> 1000$) | Sharp threshold (step function) | Equivalent to TAR/SETAR |

    **If $\gamma$ is too small:**

    - The nonlinearity is weak — consider using a linear model instead
    - Run the **linearity test** to confirm nonlinearity exists:

    ```python
    from archbox.threshold import linearity_test

    result = linearity_test(y, d=1)
    print(f"p-value: {result.pvalue:.4f}")
    ```

    **If $\gamma$ is too large:**

    - The transition is effectively a threshold — use **SETAR** instead (simpler, more stable)
    - Try standardizing the transition variable
    - Provide starting values for $\gamma$:

    ```python
    from archbox.threshold import LSTAR

    model = LSTAR(y, p=2, d=1)
    result = model.fit(gamma_start=10.0)
    ```

    !!! info
        Terasvirta (1994) recommends standardizing the transition variable by its standard deviation to keep $\gamma$ in a numerically stable range.
