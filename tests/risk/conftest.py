"""Shared fixtures for the risk tests.

Every fixture fits a real model on real (0.01-scale) returns, so the tests
exercise the documented ``ArchResults`` contract - raw ``resid``, ``std_resid``,
``mu``, ``conditional_volatility`` - instead of a hand-rolled mock that can
drift away from it.
"""

from __future__ import annotations

import numpy as np
import pytest

from archbox.datasets import load_dataset
from archbox.distributions.student_t import StudentT
from archbox.models.garch import GARCH


@pytest.fixture(scope="session")
def returns() -> np.ndarray:
    """SP500 daily returns (scale ~0.01)."""
    return load_dataset("sp500")["returns"].to_numpy(dtype=np.float64)


@pytest.fixture(scope="session")
def garch_results(returns: np.ndarray):  # noqa: ANN201 - ArchResults
    """GARCH(1,1)-Normal fitted on the SP500 returns."""
    return GARCH(returns, p=1, q=1).fit(disp=False)


@pytest.fixture(scope="session")
def garch_t_results(returns: np.ndarray):  # noqa: ANN201 - ArchResults
    """GARCH(1,1) with a *fixed* Student-t(4) conditional distribution.

    Fixing nu keeps the test independent of the optimizer while still going
    through the "fitted distribution" code path.
    """
    return GARCH(returns, p=1, q=1, dist=StudentT(nu=4.0)).fit(disp=False)


@pytest.fixture(scope="session")
def garch_t_estimated(returns: np.ndarray):  # noqa: ANN201 - ArchResults
    """GARCH(1,1)-Student-t with nu estimated from the data."""
    return GARCH(returns, p=1, q=1, dist="studentt").fit(disp=False)
