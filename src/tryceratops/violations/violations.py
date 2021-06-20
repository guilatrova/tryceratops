import ast
from dataclasses import dataclass
from typing import Tuple


@dataclass
class Violation:
    code: str
    line: int
    col: int
    description: str

    @classmethod
    def build(cls, vio_details: Tuple[str, str], stmt: ast.stmt):
        code, msg = vio_details
        return cls(code, stmt.lineno, stmt.col_offset, msg)

    def __str__(self):
        return f"[{self.code}] {self.description} - ?.py:{self.line}:{self.col}"
