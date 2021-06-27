from dataclasses import dataclass
from typing import Iterable, Optional

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
    ignore_lines: Iterable[IgnoreViolation]

    def ignores_violation(self, violation: Violation):
        for line in self.ignore_lines:
            if line.is_ignoring(violation.line, violation.code):
                return True

        return False
