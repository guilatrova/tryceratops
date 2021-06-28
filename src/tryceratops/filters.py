from dataclasses import dataclass
from typing import Iterable, Optional, Tuple, Type

from tryceratops.analyzers import BaseAnalyzer
from tryceratops.violations import Violation


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
    ignore_violations: Optional[Tuple[str]]
    exclude_dirs: Optional[Tuple[str]]

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
