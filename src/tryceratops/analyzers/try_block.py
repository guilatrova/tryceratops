import ast
from typing import Generator

from tryceratops.violations import Violation, codes

from .base import BaseAnalyzer, visit_error_handler


class TryConsiderElseAnalyzer(BaseAnalyzer, ast.NodeVisitor):
    @visit_error_handler
    def visit_Try(self, node: ast.Try) -> None:
        *_, last_child = node.body
        if isinstance(last_child, ast.Return):
            violation = Violation.build(self.filename, codes.CONSIDER_ELSE, last_child)
            self.violations.append(violation)

        self.generic_visit(node)


class TryShouldntRaiseAnalyzer(BaseAnalyzer, ast.NodeVisitor):
    def _iter_body(self, node: ast.Try) -> Generator[ast.stmt, None, None]:
        for body_child in node.body:
            yield body_child
            yield from ast.iter_child_nodes(body_child)

    @visit_error_handler
    def visit_Try(self, node: ast.Try) -> None:
        raises_within_try = [
            child for child in self._iter_body(node) if isinstance(child, ast.Raise)
        ]

        self.violations += [
            Violation.build(self.filename, codes.RAISE_WITHIN_TRY, block)
            for block in raises_within_try
        ]

        self.generic_visit(node)
