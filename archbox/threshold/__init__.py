"""Threshold and Smooth Transition Autoregressive models.

Models:
- TAR: Threshold Autoregressive (Tong, 1978)
- SETAR: Self-Exciting TAR (Tong & Lim, 1980)
- LSTAR: Logistic Smooth Transition AR (Terasvirta, 1994)
- ESTAR: Exponential Smooth Transition AR (Terasvirta, 1994)

Linearity Tests:
- Luukkonen-Saikkonen-Terasvirta (1988) LM test
- Terasvirta (1994) transition type test
- Tsay (1989) test for TAR
- Hansen (1996) bootstrap threshold test
"""

from archbox.threshold.base import ThresholdModel
from archbox.threshold.estar import ESTAR
from archbox.threshold.lstar import LSTAR
from archbox.threshold.results import TestResult, ThresholdResults
from archbox.threshold.setar import SETAR
from archbox.threshold.tar import TAR
from archbox.threshold.tests_linearity import (
    hansen_threshold_test,
    linearity_test,
    transition_type_test,
    tsay_test,
)
from archbox.threshold.transition import (
    exponential_transition,
    logistic_transition,
    logistic_transition_order2,
    plot_transition,
)

__all__ = [
    "ThresholdModel",
    "ThresholdResults",
    "TestResult",
    "TAR",
    "SETAR",
    "LSTAR",
    "ESTAR",
    "logistic_transition",
    "exponential_transition",
    "logistic_transition_order2",
    "plot_transition",
    "linearity_test",
    "transition_type_test",
    "tsay_test",
    "hansen_threshold_test",
]
