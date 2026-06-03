---
title: "Troubleshooting"
description: "Troubleshooting guide for ArchBox — common error messages, convergence failures, numerical issues, performance problems, and compatibility fixes."
---

# Troubleshooting Guide

Step-by-step solutions for common errors and problems when using ArchBox.

!!! tip "Looking for conceptual answers?"
    - **General questions**: [General FAQ](general.md)
    - **Advanced topics**: [Advanced FAQ](advanced.md)

---

## Convergence Errors

??? question "`Optimization did not converge` — causes and solutions"

    This is the most common error in GARCH estimation. The optimizer failed to find a parameter set that satisfies the convergence criteria.

    **Common causes:**

    1. **Data scale**: returns are in percentages instead of decimals
    2. **Poor starting values**: optimizer starts far from the optimum
    3. **Model too complex**: too many parameters relative to data
    4. **Data issues**: structural breaks, excessive zeros, outliers

    **Solutions (try in order):**

    ```python
    from archbox.models import GARCH

    # 1. Check data scale — returns should be ~0.01, not ~1.0
    print(f"Mean: {returns.mean():.4f}, Std: {returns.std():.4f}")

    # 2. Try different optimizer
    model = GARCH(returns, p=1, q=1)
    result = model.fit(method="Nelder-Mead")

    # 3. Provide starting values
    result = model.fit(starting_values=[1e-5, 0.05, 0.90])

    # 4. Increase max iterations
    result = model.fit(maxiter=5000)

    # 5. Simplify model order
    model = GARCH(returns, p=1, q=1)  # instead of (2,2)
    ```

    !!! warning
        If data has a **structural break** (e.g., COVID-19 crash), consider splitting the sample or using a regime-switching model.

??? question "`Singular Hessian` — what it means and how to fix it"

    A singular Hessian matrix means the optimizer cannot compute standard errors because the information matrix is not invertible. This typically indicates:

    - **Parameters at boundary**: one or more parameters hit their constraint bounds
    - **Flat likelihood**: the likelihood surface is flat in some direction
    - **Near-multicollinearity**: parameters are highly correlated

    **Solutions:**

    ```python
    from archbox.models import GARCH

    model = GARCH(returns, p=1, q=1)

    # 1. Use robust standard errors
    result = model.fit(cov_type="robust")

    # 2. Adjust bounds to avoid boundary solutions
    result = model.fit(bounds=[
        (1e-8, None),    # omega
        (1e-4, 0.50),    # alpha — away from 0
        (0.30, 0.999),   # beta — away from 1
    ])

    # 3. Reduce model complexity
    model = GARCH(returns, p=1, q=1)  # simpler order
    result = model.fit()
    ```

    !!! info
        A singular Hessian does **not** mean the parameter estimates are wrong — only that standard errors cannot be reliably computed. The point estimates may still be useful.

??? question "`Negative variance` — why it happens and how to avoid it"

    The conditional variance $h_t$ should always be positive. Negative values can occur due to:

    - **Numerical overflow**: extremely large or small parameter values
    - **Constraint violation**: optimizer stepped outside the feasible region
    - **Inappropriate model**: GARCH(p,q) with unconstrained parameters

    **Solutions:**

    ```python
    # 1. Use EGARCH — log-variance ensures positivity by construction
    from archbox.models import EGARCH

    model = EGARCH(returns, p=1, q=1)
    result = model.fit()

    # 2. Enforce strict positivity bounds
    from archbox.models import GARCH

    model = GARCH(returns, p=1, q=1)
    result = model.fit(bounds=[
        (1e-8, None),   # omega > 0
        (1e-6, 0.50),   # alpha > 0
        (1e-6, 0.999),  # beta > 0
    ])
    ```

    !!! tip
        EGARCH models the **log** of variance, so $h_t > 0$ is guaranteed. This makes EGARCH numerically more stable than GARCH when positivity is an issue.

---

## Reproducibility

??? question "Results differ between runs — how to set a seed"

    GARCH estimation is deterministic for a given set of starting values. Differences between runs usually come from:

    1. **Random starting values**: the optimizer picks different initial points
    2. **Numerical precision**: floating-point order of operations

    **Fix: set a random seed and explicit starting values:**

    ```python
    import numpy as np
    from archbox.models import GARCH

    np.random.seed(42)

    model = GARCH(returns, p=1, q=1)
    result = model.fit(starting_values=[1e-5, 0.05, 0.90])
    ```

    **For batch estimation:**

    ```python
    np.random.seed(42)

    results = {}
    for col in data.columns:
        model = GARCH(data[col], p=1, q=1)
        results[col] = model.fit(starting_values=[1e-5, 0.05, 0.90])
    ```

    !!! note
        Small differences in the last decimal places (e.g., $10^{-8}$) are normal and arise from floating-point arithmetic. These do not affect inference.

---

## Performance

??? question "Estimation is very slow — optimization tips"

    **Quick wins:**

    | Tip | Impact | How |
    |-----|--------|-----|
    | Rescale data | High | Use decimal returns, not percentages |
    | Provide starting values | High | Reduces iterations |
    | Reduce model order | High | GARCH(1,1) instead of (2,2) |
    | Use L-BFGS-B | Medium | Gradient-based, fast convergence |
    | Upgrade NumPy | Medium | MKL backend is 2-5x faster |

    **For multivariate models:**

    ```python
    # DCC with many assets — use DECO instead
    from archbox.multivariate import DECO

    model = DECO(returns, p=1, q=1)  # O(N) instead of O(N^2)
    result = model.fit()
    ```

    **For batch estimation:**

    ```python
    from concurrent.futures import ProcessPoolExecutor

    def fit_asset(col):
        from archbox.models import GARCH
        model = GARCH(data[col], p=1, q=1)
        return model.fit()

    with ProcessPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(fit_asset, data.columns))
    ```

    !!! tip
        Profile your code with `%%timeit` in Jupyter. The bottleneck is almost always the optimizer, not data loading or post-processing.

??? question "Memory errors with large datasets"

    ArchBox stores the full conditional variance path and residuals in memory. For very large datasets:

    **Estimate memory usage:**

    ```python
    import sys

    n = len(returns)
    # Each float64 = 8 bytes; GARCH stores ~5 arrays of length n
    estimated_mb = n * 8 * 5 / 1e6
    print(f"Estimated memory: {estimated_mb:.1f} MB")
    ```

    | Observations | Approx. Memory (univariate) | Approx. Memory (DCC, 10 assets) |
    |-------------|---------------------------|-------------------------------|
    | 10,000 | < 1 MB | ~10 MB |
    | 100,000 | ~4 MB | ~100 MB |
    | 1,000,000 | ~40 MB | ~1 GB |
    | 10,000,000 | ~400 MB | ~10 GB |

    **Solutions:**

    ```python
    # 1. Subsample the data
    returns_sub = returns.iloc[-5000:]  # last 5000 observations

    # 2. Use float32 for large datasets
    import numpy as np
    returns_32 = returns.astype(np.float32)

    # 3. Process in chunks for batch estimation
    chunk_size = 100
    for i in range(0, len(assets), chunk_size):
        chunk = assets[i:i+chunk_size]
        # estimate and save results
        # free memory between chunks
    ```

    !!! warning
        Multivariate models scale as $O(N^2 \times T)$ in memory. For DCC with 50 assets and 10,000 observations, expect ~2.5 GB of memory usage.

---

## Compatibility

??? question "Version incompatibility issues"

    ArchBox requires specific minimum versions of its dependencies:

    | Dependency | Minimum Version | Recommended |
    |-----------|----------------|-------------|
    | Python | 3.9 | 3.11+ |
    | NumPy | 1.24 | 2.0+ |
    | SciPy | 1.10 | 1.14+ |
    | pandas | 2.0 | 2.2+ |
    | matplotlib | 3.7 | 3.9+ |

    **Check your versions:**

    ```python
    import numpy, scipy, pandas
    print(f"NumPy: {numpy.__version__}")
    print(f"SciPy: {scipy.__version__}")
    print(f"pandas: {pandas.__version__}")
    ```

    **Fix version conflicts:**

    ```bash
    # Upgrade all together
    pip install --upgrade archbox numpy scipy pandas

    # Or create a clean environment
    python -m venv archbox_env
    source archbox_env/bin/activate  # Linux/Mac
    pip install archbox[all]
    ```

    !!! note
        If using conda, ensure you are not mixing pip and conda packages for NumPy/SciPy, as this can cause BLAS conflicts.

??? question "Import errors"

    Common import issues and fixes:

    **`ModuleNotFoundError: No module named 'archbox'`**

    ```bash
    # ArchBox is not installed
    pip install archbox

    # Or not in the active environment
    which python  # verify correct Python
    pip list | grep archbox
    ```

    **`ImportError: cannot import name 'GARCH' from 'archbox'`**

    ```python
    # Wrong import path — use submodules
    # Bad:
    from archbox import GARCH

    # Good:
    from archbox.models import GARCH
    from archbox.multivariate import DCC
    from archbox.regime import MSGARCH
    from archbox.risk import VaR
    ```

    **`ImportError: numpy.core.multiarray failed to import`**

    ```bash
    # NumPy binary incompatibility — rebuild
    pip install --force-reinstall numpy
    ```

    !!! tip
        Always use a **virtual environment** to avoid dependency conflicts between projects:

        ```bash
        python -m venv myenv
        source myenv/bin/activate
        pip install archbox[all]
        ```
