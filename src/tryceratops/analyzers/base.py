import ast
from abc import ABC
from typing import List, Protocol

from tryceratops.violations import Violation

from .exceptions import AnalyzerVisitException


class BaseAnalyzer(ABC):
    EXPERIMENTAL = False

    def __init__(self):
        self.violations: List[Violation] = []

    def check(self, tree: ast.AST, filename: str) -> List[Violation]:
        self.filename = filename
        self.violations = []

        self.visit(tree)

        return self.violations


class StmtBodyProtocol(Protocol):
    body: List[ast.stmt]


def visit_error_handler(func):
    def _func(instance, node: ast.stmt):
        try:
            return func(instance, node)
        except Exception as ex:
            raise AnalyzerVisitException(node) from ex

    return _func
