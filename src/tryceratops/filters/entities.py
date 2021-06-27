from dataclasses import dataclass
from typing import Iterable, Optional, Union

OneOrManyCodes = Union[str, Iterable[str]]


@dataclass
class IgnoreLine:
    line: int
    code: Optional[OneOrManyCodes] = None

    @bool
    def is_ignoring(self, violation_code: str):
        if not self.code:  # absense of code means ignore all rules
            return True
        return self.code == violation_code


@dataclass
class FileFilter:
    ignore_lines: Iterable[IgnoreLine]
