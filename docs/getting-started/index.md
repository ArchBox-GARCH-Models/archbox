---
title: Getting Started
description: Learn how to install ArchBox and estimate your first volatility model
---

# Getting Started

Welcome to ArchBox! This section will take you from zero to estimating conditional volatility models in Python. Whether you're an academic researcher, a risk analyst, or a quant developer, these guides will get you productive quickly.

---

## Learning Path

Follow these guides in order for the best experience:

<div class="grid cards" markdown>

-   :material-download: **Installation**

    ---

    Install ArchBox via pip or from source, configure optional dependencies, and verify your setup.

    :material-clock-outline: ~5 minutes

    [:octicons-arrow-right-24: Install ArchBox](installation.md)

-   :material-rocket-launch: **Quick Start**

    ---

    Estimate a GARCH(1,1), run diagnostics, compute VaR/ES, and visualize conditional volatility -- all in one tutorial.

    :material-clock-outline: ~15 minutes

    [:octicons-arrow-right-24: Quick Start Tutorial](quickstart.md)

-   :material-lightbulb-outline: **Core Concepts**

    ---

    Understand the key ideas behind conditional volatility: stylized facts, GARCH intuition, and the ArchBox API design.

    :material-clock-outline: ~10 minutes

    [:octicons-arrow-right-24: Core Concepts](core-concepts.md)

-   :material-compass-outline: **Choosing a Model**

    ---

    Decision guide to pick the right model family for your data: univariate, multivariate, regime-switching, or threshold.

    :material-clock-outline: ~10 minutes

    [:octicons-arrow-right-24: Choosing a Model](choosing-model.md)

</div>

---

## What You'll Learn

By the end of the Getting Started section, you will be able to:

- **Install** ArchBox and verify it works on your system
- **Estimate** a GARCH(1,1) model on financial returns
- **Interpret** parameter estimates, persistence, and half-life
- **Run diagnostics** (ARCH-LM, Ljung-Box) to validate your model
- **Compute risk measures** (Value-at-Risk, Expected Shortfall)
- **Visualize** conditional volatility over time
- **Choose** the appropriate model family for your research question

---

## Prerequisites

ArchBox assumes basic familiarity with:

- **Python** -- NumPy, pandas, and matplotlib basics
- **Statistics** -- mean, variance, standard deviation, hypothesis testing
- **Finance** -- asset returns, volatility, risk measures

!!! tip "New to volatility modeling?"

    If you're new to GARCH models, start with the [Core Concepts](core-concepts.md) page after completing the Quick Start. For the mathematical foundations, see the [Theory](../theory/garch-theory.md) section.

---

## Next Steps

Ready to begin? Start with the [Installation Guide](installation.md).
