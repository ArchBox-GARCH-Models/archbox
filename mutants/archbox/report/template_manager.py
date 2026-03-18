"""Template management for archbox reports.

Uses Jinja2 for template loading and rendering with custom filters
and context processors.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

_DEFAULT_TEMPLATE_DIR = Path(__file__).parent / "templates"
from collections.abc import Callable
from typing import Annotated, ClassVar

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


class TemplateManager:
    """Manages Jinja2 templates for report generation.

    Parameters
    ----------
    template_dir : str or Path, optional
        Custom template directory. If None, uses built-in templates.
    """

    def __init__(self, template_dir: str | Path | None = None) -> None:
        args = [template_dir]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁTemplateManagerǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁTemplateManagerǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁTemplateManagerǁ__init____mutmut_orig(
        self, template_dir: str | Path | None = None
    ) -> None:
        """Initialize template manager with optional custom template directory."""
        if template_dir is not None:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = _DEFAULT_TEMPLATE_DIR

        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Register custom filters
        self.env.filters["fmt_number"] = self._fmt_number
        self.env.filters["fmt_pvalue"] = self._fmt_pvalue
        self.env.filters["fmt_percent"] = self._fmt_percent
        self.env.filters["significance_stars"] = self._significance_stars

    def xǁTemplateManagerǁ__init____mutmut_1(self, template_dir: str | Path | None = None) -> None:
        """Initialize template manager with optional custom template directory."""
        if template_dir is None:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = _DEFAULT_TEMPLATE_DIR

        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Register custom filters
        self.env.filters["fmt_number"] = self._fmt_number
        self.env.filters["fmt_pvalue"] = self._fmt_pvalue
        self.env.filters["fmt_percent"] = self._fmt_percent
        self.env.filters["significance_stars"] = self._significance_stars

    def xǁTemplateManagerǁ__init____mutmut_2(self, template_dir: str | Path | None = None) -> None:
        """Initialize template manager with optional custom template directory."""
        if template_dir is not None:
            self.template_dir = None
        else:
            self.template_dir = _DEFAULT_TEMPLATE_DIR

        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Register custom filters
        self.env.filters["fmt_number"] = self._fmt_number
        self.env.filters["fmt_pvalue"] = self._fmt_pvalue
        self.env.filters["fmt_percent"] = self._fmt_percent
        self.env.filters["significance_stars"] = self._significance_stars

    def xǁTemplateManagerǁ__init____mutmut_3(self, template_dir: str | Path | None = None) -> None:
        """Initialize template manager with optional custom template directory."""
        if template_dir is not None:
            self.template_dir = Path(None)
        else:
            self.template_dir = _DEFAULT_TEMPLATE_DIR

        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Register custom filters
        self.env.filters["fmt_number"] = self._fmt_number
        self.env.filters["fmt_pvalue"] = self._fmt_pvalue
        self.env.filters["fmt_percent"] = self._fmt_percent
        self.env.filters["significance_stars"] = self._significance_stars

    def xǁTemplateManagerǁ__init____mutmut_4(self, template_dir: str | Path | None = None) -> None:
        """Initialize template manager with optional custom template directory."""
        if template_dir is not None:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = None

        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Register custom filters
        self.env.filters["fmt_number"] = self._fmt_number
        self.env.filters["fmt_pvalue"] = self._fmt_pvalue
        self.env.filters["fmt_percent"] = self._fmt_percent
        self.env.filters["significance_stars"] = self._significance_stars

    def xǁTemplateManagerǁ__init____mutmut_5(self, template_dir: str | Path | None = None) -> None:
        """Initialize template manager with optional custom template directory."""
        if template_dir is not None:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = _DEFAULT_TEMPLATE_DIR

        self.env = None

        # Register custom filters
        self.env.filters["fmt_number"] = self._fmt_number
        self.env.filters["fmt_pvalue"] = self._fmt_pvalue
        self.env.filters["fmt_percent"] = self._fmt_percent
        self.env.filters["significance_stars"] = self._significance_stars

    def xǁTemplateManagerǁ__init____mutmut_6(self, template_dir: str | Path | None = None) -> None:
        """Initialize template manager with optional custom template directory."""
        if template_dir is not None:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = _DEFAULT_TEMPLATE_DIR

        self.env = Environment(
            loader=None,
            autoescape=select_autoescape(["html"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Register custom filters
        self.env.filters["fmt_number"] = self._fmt_number
        self.env.filters["fmt_pvalue"] = self._fmt_pvalue
        self.env.filters["fmt_percent"] = self._fmt_percent
        self.env.filters["significance_stars"] = self._significance_stars

    def xǁTemplateManagerǁ__init____mutmut_7(self, template_dir: str | Path | None = None) -> None:
        """Initialize template manager with optional custom template directory."""
        if template_dir is not None:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = _DEFAULT_TEMPLATE_DIR

        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=None,
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Register custom filters
        self.env.filters["fmt_number"] = self._fmt_number
        self.env.filters["fmt_pvalue"] = self._fmt_pvalue
        self.env.filters["fmt_percent"] = self._fmt_percent
        self.env.filters["significance_stars"] = self._significance_stars

    def xǁTemplateManagerǁ__init____mutmut_8(self, template_dir: str | Path | None = None) -> None:
        """Initialize template manager with optional custom template directory."""
        if template_dir is not None:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = _DEFAULT_TEMPLATE_DIR

        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html"]),
            trim_blocks=None,
            lstrip_blocks=True,
        )

        # Register custom filters
        self.env.filters["fmt_number"] = self._fmt_number
        self.env.filters["fmt_pvalue"] = self._fmt_pvalue
        self.env.filters["fmt_percent"] = self._fmt_percent
        self.env.filters["significance_stars"] = self._significance_stars

    def xǁTemplateManagerǁ__init____mutmut_9(self, template_dir: str | Path | None = None) -> None:
        """Initialize template manager with optional custom template directory."""
        if template_dir is not None:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = _DEFAULT_TEMPLATE_DIR

        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html"]),
            trim_blocks=True,
            lstrip_blocks=None,
        )

        # Register custom filters
        self.env.filters["fmt_number"] = self._fmt_number
        self.env.filters["fmt_pvalue"] = self._fmt_pvalue
        self.env.filters["fmt_percent"] = self._fmt_percent
        self.env.filters["significance_stars"] = self._significance_stars

    def xǁTemplateManagerǁ__init____mutmut_10(self, template_dir: str | Path | None = None) -> None:
        """Initialize template manager with optional custom template directory."""
        if template_dir is not None:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = _DEFAULT_TEMPLATE_DIR

        self.env = Environment(
            autoescape=select_autoescape(["html"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Register custom filters
        self.env.filters["fmt_number"] = self._fmt_number
        self.env.filters["fmt_pvalue"] = self._fmt_pvalue
        self.env.filters["fmt_percent"] = self._fmt_percent
        self.env.filters["significance_stars"] = self._significance_stars

    def xǁTemplateManagerǁ__init____mutmut_11(self, template_dir: str | Path | None = None) -> None:
        """Initialize template manager with optional custom template directory."""
        if template_dir is not None:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = _DEFAULT_TEMPLATE_DIR

        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Register custom filters
        self.env.filters["fmt_number"] = self._fmt_number
        self.env.filters["fmt_pvalue"] = self._fmt_pvalue
        self.env.filters["fmt_percent"] = self._fmt_percent
        self.env.filters["significance_stars"] = self._significance_stars

    def xǁTemplateManagerǁ__init____mutmut_12(self, template_dir: str | Path | None = None) -> None:
        """Initialize template manager with optional custom template directory."""
        if template_dir is not None:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = _DEFAULT_TEMPLATE_DIR

        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html"]),
            lstrip_blocks=True,
        )

        # Register custom filters
        self.env.filters["fmt_number"] = self._fmt_number
        self.env.filters["fmt_pvalue"] = self._fmt_pvalue
        self.env.filters["fmt_percent"] = self._fmt_percent
        self.env.filters["significance_stars"] = self._significance_stars

    def xǁTemplateManagerǁ__init____mutmut_13(self, template_dir: str | Path | None = None) -> None:
        """Initialize template manager with optional custom template directory."""
        if template_dir is not None:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = _DEFAULT_TEMPLATE_DIR

        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html"]),
            trim_blocks=True,
        )

        # Register custom filters
        self.env.filters["fmt_number"] = self._fmt_number
        self.env.filters["fmt_pvalue"] = self._fmt_pvalue
        self.env.filters["fmt_percent"] = self._fmt_percent
        self.env.filters["significance_stars"] = self._significance_stars

    def xǁTemplateManagerǁ__init____mutmut_14(self, template_dir: str | Path | None = None) -> None:
        """Initialize template manager with optional custom template directory."""
        if template_dir is not None:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = _DEFAULT_TEMPLATE_DIR

        self.env = Environment(
            loader=FileSystemLoader(None),
            autoescape=select_autoescape(["html"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Register custom filters
        self.env.filters["fmt_number"] = self._fmt_number
        self.env.filters["fmt_pvalue"] = self._fmt_pvalue
        self.env.filters["fmt_percent"] = self._fmt_percent
        self.env.filters["significance_stars"] = self._significance_stars

    def xǁTemplateManagerǁ__init____mutmut_15(self, template_dir: str | Path | None = None) -> None:
        """Initialize template manager with optional custom template directory."""
        if template_dir is not None:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = _DEFAULT_TEMPLATE_DIR

        self.env = Environment(
            loader=FileSystemLoader(str(None)),
            autoescape=select_autoescape(["html"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Register custom filters
        self.env.filters["fmt_number"] = self._fmt_number
        self.env.filters["fmt_pvalue"] = self._fmt_pvalue
        self.env.filters["fmt_percent"] = self._fmt_percent
        self.env.filters["significance_stars"] = self._significance_stars

    def xǁTemplateManagerǁ__init____mutmut_16(self, template_dir: str | Path | None = None) -> None:
        """Initialize template manager with optional custom template directory."""
        if template_dir is not None:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = _DEFAULT_TEMPLATE_DIR

        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(None),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Register custom filters
        self.env.filters["fmt_number"] = self._fmt_number
        self.env.filters["fmt_pvalue"] = self._fmt_pvalue
        self.env.filters["fmt_percent"] = self._fmt_percent
        self.env.filters["significance_stars"] = self._significance_stars

    def xǁTemplateManagerǁ__init____mutmut_17(self, template_dir: str | Path | None = None) -> None:
        """Initialize template manager with optional custom template directory."""
        if template_dir is not None:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = _DEFAULT_TEMPLATE_DIR

        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["XXhtmlXX"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Register custom filters
        self.env.filters["fmt_number"] = self._fmt_number
        self.env.filters["fmt_pvalue"] = self._fmt_pvalue
        self.env.filters["fmt_percent"] = self._fmt_percent
        self.env.filters["significance_stars"] = self._significance_stars

    def xǁTemplateManagerǁ__init____mutmut_18(self, template_dir: str | Path | None = None) -> None:
        """Initialize template manager with optional custom template directory."""
        if template_dir is not None:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = _DEFAULT_TEMPLATE_DIR

        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["HTML"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Register custom filters
        self.env.filters["fmt_number"] = self._fmt_number
        self.env.filters["fmt_pvalue"] = self._fmt_pvalue
        self.env.filters["fmt_percent"] = self._fmt_percent
        self.env.filters["significance_stars"] = self._significance_stars

    def xǁTemplateManagerǁ__init____mutmut_19(self, template_dir: str | Path | None = None) -> None:
        """Initialize template manager with optional custom template directory."""
        if template_dir is not None:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = _DEFAULT_TEMPLATE_DIR

        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html"]),
            trim_blocks=False,
            lstrip_blocks=True,
        )

        # Register custom filters
        self.env.filters["fmt_number"] = self._fmt_number
        self.env.filters["fmt_pvalue"] = self._fmt_pvalue
        self.env.filters["fmt_percent"] = self._fmt_percent
        self.env.filters["significance_stars"] = self._significance_stars

    def xǁTemplateManagerǁ__init____mutmut_20(self, template_dir: str | Path | None = None) -> None:
        """Initialize template manager with optional custom template directory."""
        if template_dir is not None:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = _DEFAULT_TEMPLATE_DIR

        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html"]),
            trim_blocks=True,
            lstrip_blocks=False,
        )

        # Register custom filters
        self.env.filters["fmt_number"] = self._fmt_number
        self.env.filters["fmt_pvalue"] = self._fmt_pvalue
        self.env.filters["fmt_percent"] = self._fmt_percent
        self.env.filters["significance_stars"] = self._significance_stars

    def xǁTemplateManagerǁ__init____mutmut_21(self, template_dir: str | Path | None = None) -> None:
        """Initialize template manager with optional custom template directory."""
        if template_dir is not None:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = _DEFAULT_TEMPLATE_DIR

        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Register custom filters
        self.env.filters["fmt_number"] = None
        self.env.filters["fmt_pvalue"] = self._fmt_pvalue
        self.env.filters["fmt_percent"] = self._fmt_percent
        self.env.filters["significance_stars"] = self._significance_stars

    def xǁTemplateManagerǁ__init____mutmut_22(self, template_dir: str | Path | None = None) -> None:
        """Initialize template manager with optional custom template directory."""
        if template_dir is not None:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = _DEFAULT_TEMPLATE_DIR

        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Register custom filters
        self.env.filters["XXfmt_numberXX"] = self._fmt_number
        self.env.filters["fmt_pvalue"] = self._fmt_pvalue
        self.env.filters["fmt_percent"] = self._fmt_percent
        self.env.filters["significance_stars"] = self._significance_stars

    def xǁTemplateManagerǁ__init____mutmut_23(self, template_dir: str | Path | None = None) -> None:
        """Initialize template manager with optional custom template directory."""
        if template_dir is not None:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = _DEFAULT_TEMPLATE_DIR

        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Register custom filters
        self.env.filters["FMT_NUMBER"] = self._fmt_number
        self.env.filters["fmt_pvalue"] = self._fmt_pvalue
        self.env.filters["fmt_percent"] = self._fmt_percent
        self.env.filters["significance_stars"] = self._significance_stars

    def xǁTemplateManagerǁ__init____mutmut_24(self, template_dir: str | Path | None = None) -> None:
        """Initialize template manager with optional custom template directory."""
        if template_dir is not None:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = _DEFAULT_TEMPLATE_DIR

        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Register custom filters
        self.env.filters["fmt_number"] = self._fmt_number
        self.env.filters["fmt_pvalue"] = None
        self.env.filters["fmt_percent"] = self._fmt_percent
        self.env.filters["significance_stars"] = self._significance_stars

    def xǁTemplateManagerǁ__init____mutmut_25(self, template_dir: str | Path | None = None) -> None:
        """Initialize template manager with optional custom template directory."""
        if template_dir is not None:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = _DEFAULT_TEMPLATE_DIR

        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Register custom filters
        self.env.filters["fmt_number"] = self._fmt_number
        self.env.filters["XXfmt_pvalueXX"] = self._fmt_pvalue
        self.env.filters["fmt_percent"] = self._fmt_percent
        self.env.filters["significance_stars"] = self._significance_stars

    def xǁTemplateManagerǁ__init____mutmut_26(self, template_dir: str | Path | None = None) -> None:
        """Initialize template manager with optional custom template directory."""
        if template_dir is not None:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = _DEFAULT_TEMPLATE_DIR

        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Register custom filters
        self.env.filters["fmt_number"] = self._fmt_number
        self.env.filters["FMT_PVALUE"] = self._fmt_pvalue
        self.env.filters["fmt_percent"] = self._fmt_percent
        self.env.filters["significance_stars"] = self._significance_stars

    def xǁTemplateManagerǁ__init____mutmut_27(self, template_dir: str | Path | None = None) -> None:
        """Initialize template manager with optional custom template directory."""
        if template_dir is not None:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = _DEFAULT_TEMPLATE_DIR

        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Register custom filters
        self.env.filters["fmt_number"] = self._fmt_number
        self.env.filters["fmt_pvalue"] = self._fmt_pvalue
        self.env.filters["fmt_percent"] = None
        self.env.filters["significance_stars"] = self._significance_stars

    def xǁTemplateManagerǁ__init____mutmut_28(self, template_dir: str | Path | None = None) -> None:
        """Initialize template manager with optional custom template directory."""
        if template_dir is not None:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = _DEFAULT_TEMPLATE_DIR

        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Register custom filters
        self.env.filters["fmt_number"] = self._fmt_number
        self.env.filters["fmt_pvalue"] = self._fmt_pvalue
        self.env.filters["XXfmt_percentXX"] = self._fmt_percent
        self.env.filters["significance_stars"] = self._significance_stars

    def xǁTemplateManagerǁ__init____mutmut_29(self, template_dir: str | Path | None = None) -> None:
        """Initialize template manager with optional custom template directory."""
        if template_dir is not None:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = _DEFAULT_TEMPLATE_DIR

        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Register custom filters
        self.env.filters["fmt_number"] = self._fmt_number
        self.env.filters["fmt_pvalue"] = self._fmt_pvalue
        self.env.filters["FMT_PERCENT"] = self._fmt_percent
        self.env.filters["significance_stars"] = self._significance_stars

    def xǁTemplateManagerǁ__init____mutmut_30(self, template_dir: str | Path | None = None) -> None:
        """Initialize template manager with optional custom template directory."""
        if template_dir is not None:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = _DEFAULT_TEMPLATE_DIR

        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Register custom filters
        self.env.filters["fmt_number"] = self._fmt_number
        self.env.filters["fmt_pvalue"] = self._fmt_pvalue
        self.env.filters["fmt_percent"] = self._fmt_percent
        self.env.filters["significance_stars"] = None

    def xǁTemplateManagerǁ__init____mutmut_31(self, template_dir: str | Path | None = None) -> None:
        """Initialize template manager with optional custom template directory."""
        if template_dir is not None:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = _DEFAULT_TEMPLATE_DIR

        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Register custom filters
        self.env.filters["fmt_number"] = self._fmt_number
        self.env.filters["fmt_pvalue"] = self._fmt_pvalue
        self.env.filters["fmt_percent"] = self._fmt_percent
        self.env.filters["XXsignificance_starsXX"] = self._significance_stars

    def xǁTemplateManagerǁ__init____mutmut_32(self, template_dir: str | Path | None = None) -> None:
        """Initialize template manager with optional custom template directory."""
        if template_dir is not None:
            self.template_dir = Path(template_dir)
        else:
            self.template_dir = _DEFAULT_TEMPLATE_DIR

        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Register custom filters
        self.env.filters["fmt_number"] = self._fmt_number
        self.env.filters["fmt_pvalue"] = self._fmt_pvalue
        self.env.filters["fmt_percent"] = self._fmt_percent
        self.env.filters["SIGNIFICANCE_STARS"] = self._significance_stars

    xǁTemplateManagerǁ__init____mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁTemplateManagerǁ__init____mutmut_1": xǁTemplateManagerǁ__init____mutmut_1,
        "xǁTemplateManagerǁ__init____mutmut_2": xǁTemplateManagerǁ__init____mutmut_2,
        "xǁTemplateManagerǁ__init____mutmut_3": xǁTemplateManagerǁ__init____mutmut_3,
        "xǁTemplateManagerǁ__init____mutmut_4": xǁTemplateManagerǁ__init____mutmut_4,
        "xǁTemplateManagerǁ__init____mutmut_5": xǁTemplateManagerǁ__init____mutmut_5,
        "xǁTemplateManagerǁ__init____mutmut_6": xǁTemplateManagerǁ__init____mutmut_6,
        "xǁTemplateManagerǁ__init____mutmut_7": xǁTemplateManagerǁ__init____mutmut_7,
        "xǁTemplateManagerǁ__init____mutmut_8": xǁTemplateManagerǁ__init____mutmut_8,
        "xǁTemplateManagerǁ__init____mutmut_9": xǁTemplateManagerǁ__init____mutmut_9,
        "xǁTemplateManagerǁ__init____mutmut_10": xǁTemplateManagerǁ__init____mutmut_10,
        "xǁTemplateManagerǁ__init____mutmut_11": xǁTemplateManagerǁ__init____mutmut_11,
        "xǁTemplateManagerǁ__init____mutmut_12": xǁTemplateManagerǁ__init____mutmut_12,
        "xǁTemplateManagerǁ__init____mutmut_13": xǁTemplateManagerǁ__init____mutmut_13,
        "xǁTemplateManagerǁ__init____mutmut_14": xǁTemplateManagerǁ__init____mutmut_14,
        "xǁTemplateManagerǁ__init____mutmut_15": xǁTemplateManagerǁ__init____mutmut_15,
        "xǁTemplateManagerǁ__init____mutmut_16": xǁTemplateManagerǁ__init____mutmut_16,
        "xǁTemplateManagerǁ__init____mutmut_17": xǁTemplateManagerǁ__init____mutmut_17,
        "xǁTemplateManagerǁ__init____mutmut_18": xǁTemplateManagerǁ__init____mutmut_18,
        "xǁTemplateManagerǁ__init____mutmut_19": xǁTemplateManagerǁ__init____mutmut_19,
        "xǁTemplateManagerǁ__init____mutmut_20": xǁTemplateManagerǁ__init____mutmut_20,
        "xǁTemplateManagerǁ__init____mutmut_21": xǁTemplateManagerǁ__init____mutmut_21,
        "xǁTemplateManagerǁ__init____mutmut_22": xǁTemplateManagerǁ__init____mutmut_22,
        "xǁTemplateManagerǁ__init____mutmut_23": xǁTemplateManagerǁ__init____mutmut_23,
        "xǁTemplateManagerǁ__init____mutmut_24": xǁTemplateManagerǁ__init____mutmut_24,
        "xǁTemplateManagerǁ__init____mutmut_25": xǁTemplateManagerǁ__init____mutmut_25,
        "xǁTemplateManagerǁ__init____mutmut_26": xǁTemplateManagerǁ__init____mutmut_26,
        "xǁTemplateManagerǁ__init____mutmut_27": xǁTemplateManagerǁ__init____mutmut_27,
        "xǁTemplateManagerǁ__init____mutmut_28": xǁTemplateManagerǁ__init____mutmut_28,
        "xǁTemplateManagerǁ__init____mutmut_29": xǁTemplateManagerǁ__init____mutmut_29,
        "xǁTemplateManagerǁ__init____mutmut_30": xǁTemplateManagerǁ__init____mutmut_30,
        "xǁTemplateManagerǁ__init____mutmut_31": xǁTemplateManagerǁ__init____mutmut_31,
        "xǁTemplateManagerǁ__init____mutmut_32": xǁTemplateManagerǁ__init____mutmut_32,
    }
    xǁTemplateManagerǁ__init____mutmut_orig.__name__ = "xǁTemplateManagerǁ__init__"

    def render(self, template_name: str, context: dict[str, Any]) -> str:
        args = [template_name, context]  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁTemplateManagerǁrender__mutmut_orig"),
            object.__getattribute__(self, "xǁTemplateManagerǁrender__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁTemplateManagerǁrender__mutmut_orig(
        self, template_name: str, context: dict[str, Any]
    ) -> str:
        """Render a template with the given context.

        Parameters
        ----------
        template_name : str
            Template file name (e.g. 'garch_report.html').
        context : dict
            Template variables.

        Returns
        -------
        str
            Rendered content.
        """
        template = self.env.get_template(template_name)
        return template.render(**context)

    def xǁTemplateManagerǁrender__mutmut_1(
        self, template_name: str, context: dict[str, Any]
    ) -> str:
        """Render a template with the given context.

        Parameters
        ----------
        template_name : str
            Template file name (e.g. 'garch_report.html').
        context : dict
            Template variables.

        Returns
        -------
        str
            Rendered content.
        """
        template = None
        return template.render(**context)

    def xǁTemplateManagerǁrender__mutmut_2(
        self, template_name: str, context: dict[str, Any]
    ) -> str:
        """Render a template with the given context.

        Parameters
        ----------
        template_name : str
            Template file name (e.g. 'garch_report.html').
        context : dict
            Template variables.

        Returns
        -------
        str
            Rendered content.
        """
        template = self.env.get_template(None)
        return template.render(**context)

    xǁTemplateManagerǁrender__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁTemplateManagerǁrender__mutmut_1": xǁTemplateManagerǁrender__mutmut_1,
        "xǁTemplateManagerǁrender__mutmut_2": xǁTemplateManagerǁrender__mutmut_2,
    }
    xǁTemplateManagerǁrender__mutmut_orig.__name__ = "xǁTemplateManagerǁrender"

    def list_templates(self) -> list[str]:
        args = []  # type: ignore
        kwargs = {}  # type: ignore
        return _mutmut_trampoline(
            object.__getattribute__(self, "xǁTemplateManagerǁlist_templates__mutmut_orig"),
            object.__getattribute__(self, "xǁTemplateManagerǁlist_templates__mutmut_mutants"),
            args,
            kwargs,
            self,
        )

    def xǁTemplateManagerǁlist_templates__mutmut_orig(self) -> list[str]:
        """List available template names."""
        return sorted(self.env.list_templates())

    def xǁTemplateManagerǁlist_templates__mutmut_1(self) -> list[str]:
        """List available template names."""
        return sorted(None)

    xǁTemplateManagerǁlist_templates__mutmut_mutants: ClassVar[MutantDict] = {  # type: ignore
        "xǁTemplateManagerǁlist_templates__mutmut_1": xǁTemplateManagerǁlist_templates__mutmut_1
    }
    xǁTemplateManagerǁlist_templates__mutmut_orig.__name__ = "xǁTemplateManagerǁlist_templates"

    @staticmethod
    def _fmt_number(value: Any, decimals: int = 4) -> str:
        """Format a number with specified decimal places."""
        try:
            return f"{float(value):.{decimals}f}"
        except (TypeError, ValueError):
            return str(value)

    @staticmethod
    def _fmt_pvalue(value: Any) -> str:
        """Format a p-value with appropriate precision."""
        try:
            p = float(value)
            if p < 0.001:
                return "<0.001"
            elif p < 0.01:
                return f"{p:.4f}"
            elif p < 0.1:
                return f"{p:.3f}"
            else:
                return f"{p:.3f}"
        except (TypeError, ValueError):
            return str(value)

    @staticmethod
    def _fmt_percent(value: Any, decimals: int = 2) -> str:
        """Format a value as percentage."""
        try:
            return f"{float(value) * 100:.{decimals}f}%"
        except (TypeError, ValueError):
            return str(value)

    @staticmethod
    def _significance_stars(pvalue: Any) -> str:
        """Return significance stars based on p-value."""
        try:
            p = float(pvalue)
            if p < 0.01:
                return "***"
            elif p < 0.05:
                return "**"
            elif p < 0.10:
                return "*"
            else:
                return ""
        except (TypeError, ValueError):
            return ""
