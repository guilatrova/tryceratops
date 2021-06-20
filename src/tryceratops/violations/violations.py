import ast
from dataclasses import dataclass
from typing import Tuple


class COLORS:
    DESCR = "\033[91m"
    CODE = "\033[93m"

    ENDC = "\033[0m"


def wrap_color(msg: str, color: str):
    return f"{color}{msg}{COLORS.ENDC}"


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

    def __str__(self):
        codestr = wrap_color(self.code, COLORS.CODE)
        descstr = wrap_color(self.description, COLORS.DESCR)
        location = f"{self.filename}:{self.line}:{self.col}"

        return f"[{codestr}] {descstr} - {location}"
