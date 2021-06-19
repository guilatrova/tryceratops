import ast
from abc import ABC, abstractmethod
from typing import List

from .violations import TOO_MANY_TRY, Violation


class BaseAnalyzer(ABC):
    @abstractmethod
    def check(self, tree: ast.AST) -> List[Violation]:
        ...


class CallTooManyAnalyzer(BaseAnalyzer, ast.NodeVisitor):
    def __init__(self):
        self.violations: List[Violation] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        try_blocks = [stm for stm in node.body if isinstance(stm, ast.Try)]

        if len(try_blocks) > 1:
            _, *violation_blocks = try_blocks
            code, msg = TOO_MANY_TRY
            violations = [
                Violation(code, block.lineno, block.col_offset, msg)
                for block in violation_blocks
            ]
            self.violations += violations

        self.generic_visit(node)

    def check(self, tree: ast.AST) -> List[Violation]:
        self.visit(tree)
        return self.violations
