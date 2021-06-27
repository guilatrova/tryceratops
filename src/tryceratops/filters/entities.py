from dataclasses import dataclass
from typing import Iterable, Optional

ALL_FILE = -1


@dataclass
class IgnoreLine:
    line: int
    code: Optional[Iterable[str]] = None

    def is_ignoring(self, violation_code: str) -> bool:
        if not self.code:  # absense of code means ignore all rules
            return True
        return violation_code in self.code


@dataclass
class FileFilter:
    ignore_lines: Iterable[IgnoreLine]
