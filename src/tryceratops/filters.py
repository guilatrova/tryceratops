from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterable, Optional, Type

from tryceratops.analyzers import BaseAnalyzer
from tryceratops.violations import Violation

if TYPE_CHECKING:
    from tryceratops.types import PyprojectConfig


@dataclass
class IgnoreViolation:
    line: int
    code: Optional[Iterable[str]] = None

    @property
    def affects_whole_file(self) -> bool:
        return self.line == 1

    def is_ignoring(self, line: int, violation_code: str) -> bool:
        if not self.affects_whole_file:
            if self.line != line:
                return False

        if not self.code:  # absense of code means ignore all rules
            return True

        return violation_code in self.code


@dataclass
class FileFilter:
    """Represents a filter applied to a single file"""

    ignore_lines: Iterable[IgnoreViolation]

    def ignores_violation(self, violation: Violation):
        for line in self.ignore_lines:
            if line.is_ignoring(violation.line, violation.code):
                return True

        return False


@dataclass
class GlobalFilter:
    """
    Represents a filter applied to the runner
    (i.e. all analyzers and all files).
    """

    include_experimental: bool
    ignore_violations: Optional[Iterable[str]]
    exclude_dirs: Optional[Iterable[str]]

    def _self_check(self):
        self.exclude_dirs = [excluded for excluded in self.exclude_dirs if excluded]

    def __post_init__(self):
        self._self_check()

    @property
    def exclude_experimental(self) -> bool:
        return not self.include_experimental

    def should_run_analyzer(self, analyzer: Type[BaseAnalyzer]) -> bool:
        code, _ = analyzer.violation_code
        if code in self.ignore_violations:
            return False

        if self.exclude_experimental and analyzer.EXPERIMENTAL:
            return False

        return True

    def should_skip_file(self, filename: str) -> bool:
        if any(excluded_filename in filename for excluded_filename in self.exclude_dirs):
            return True

        return False

    @classmethod
    def create_from_config(cls, config: PyprojectConfig) -> GlobalFilter:
        experimental = config.get("experimental", False)
        ignore = config.get("ignore", [])
        exclude = config.get("exclude", [])

        return cls(experimental, ignore, exclude)

    def overwrite_from_cli(
        self,
        include_experimental: bool,
        ignore_violations: Iterable[str],
        exclude_dirs: Iterable[str],
    ):
        """In case any value is set it overwrites the previous value"""
        if include_experimental:
            self.include_experimental = include_experimental

        if ignore_violations:
            self.ignore_violations = ignore_violations

        if exclude_dirs:
            self.exclude_dirs = exclude_dirs

        self._self_check()
