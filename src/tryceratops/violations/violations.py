import ast
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class Violation:
    code: str
    line: int
    col: int
    description: str
    filename: str
    node: Optional[ast.AST] = None

    @classmethod
    def build(cls, filename: str, vio_details: Tuple[str, str], node: ast.AST, **kwargs):
        code, msg = vio_details
        return cls(code, node.lineno, node.col_offset, msg, filename, node)


@dataclass
class VerboseReraiseViolation(Violation):
    exception_name: str = ""

    @classmethod
    def build(
        cls,
        filename: str,
        vio_details: Tuple[str, str],
        node: ast.AST,
        exception_name: str = "",
        **kwargs
    ):
        code, msg = vio_details
        return cls(code, node.lineno, node.col_offset, msg, filename, node, exception_name)
