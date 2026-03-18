"""Model comparison results."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Annotated, Any

import matplotlib.pyplot as plt
import pandas as pd

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
class ComparisonResult:
    """Container for model comparison results.

    Attributes
    ----------
    model_names : list[str]
        Names of compared models.
    criteria : dict[str, list[float]]
        Dictionary mapping criterion name to list of values per model.
    results : list[Any]
        List of fitted model results (ArchResults).
    """

    model_names: list[str]
    criteria: dict[str, list[float]]
    results: list[Any] = field(default_factory=list, repr=False)

    def ranking(self, criterion: str = "aic") -> pd.DataFrame:
        """Rank models by a given criterion.

        Parameters
        ----------
        criterion : str
            Criterion to rank by (default: 'aic').

        Returns
        -------
        pd.DataFrame
            DataFrame sorted by the criterion.
        """
        if criterion not in self.criteria:
            available = list(self.criteria.keys())
            msg = f"Unknown criterion '{criterion}'. Available: {available}"
            raise ValueError(msg)

        df = pd.DataFrame(self.criteria, index=self.model_names)
        return df.sort_values(criterion, ascending=True)

    def best_model(self, criterion: str = "aic") -> str:
        """Return the name of the best model by a given criterion.

        Parameters
        ----------
        criterion : str
            Criterion to select by (default: 'aic').

        Returns
        -------
        str
            Name of the best model.
        """
        ranked = self.ranking(criterion)
        return str(ranked.index[0])

    def to_dataframe(self) -> pd.DataFrame:
        """Convert comparison to DataFrame.

        Returns
        -------
        pd.DataFrame
            Full comparison table.
        """
        return pd.DataFrame(self.criteria, index=self.model_names)

    def plot_comparison(
        self,
        criterion: str = "aic",
        ax: plt.Axes | None = None,
    ) -> plt.Axes:
        """Plot a bar chart comparing models by criterion.

        Parameters
        ----------
        criterion : str
            Criterion to plot.
        ax : plt.Axes, optional
            Matplotlib axes.

        Returns
        -------
        plt.Axes
            Matplotlib axes with the plot.
        """
        if ax is None:
            _, ax = plt.subplots(figsize=(10, 6))

        ranked = self.ranking(criterion)
        values = ranked[criterion].values
        names = ranked.index.tolist()

        colors = ["#2ecc71" if i == 0 else "#3498db" for i in range(len(names))]
        ax.barh(names, list(values), color=colors)
        ax.set_xlabel(criterion.upper())
        ax.set_title(f"Model Comparison by {criterion.upper()}")
        ax.invert_yaxis()
        plt.tight_layout()
        return ax
