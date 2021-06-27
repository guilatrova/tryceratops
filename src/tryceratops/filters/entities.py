from dataclasses import dataclass
from typing import Iterable, Optional


@dataclass
class IgnoreLine:
    line: int
    code: Optional[Iterable[str]] = None

    @bool
    def is_ignoring(self, violation_code: str):
        if not self.code:  # absense of code means ignore all rules
            return True
        return self.code == violation_code


@dataclass
class FileFilter:
    ignore_lines: Iterable[IgnoreLine]
