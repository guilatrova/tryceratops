import ast
from abc import ABC
from typing import List, Protocol

from tryceratops.violations import Violation


class BaseAnalyzer(ABC):
    def __init__(self):
        self.violations: List[Violation] = []

    def check(self, tree: ast.AST, filename: str) -> List[Violation]:
        self.filename = filename
        self.violations = []

        self.visit(tree)

        return self.violations


class StmtBodyProtocol(Protocol):
    body: List[ast.stmt]
