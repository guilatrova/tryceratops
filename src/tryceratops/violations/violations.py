import ast
from dataclasses import dataclass
from typing import Tuple


@dataclass
class Violation:
    code: str
    line: int
    col: int
    description: str
    filename: str

    @classmethod
    def build(cls, filename: str, vio_details: Tuple[str, str], stmt: ast.stmt):
        code, msg = vio_details
        return cls(code, stmt.lineno, stmt.col_offset, msg, filename)
