import ast
from typing import Generator

from tryceratops.violations import codes

from .base import BaseAnalyzer, visit_error_handler


class TryConsiderElseAnalyzer(BaseAnalyzer, ast.NodeVisitor):
    violation_code = codes.CONSIDER_ELSE

    @visit_error_handler
    def visit_Try(self, node: ast.Try) -> None:
        *_, last_child = node.body
        theres_more_children = len(node.body) > 1

        if isinstance(last_child, ast.Return) and theres_more_children:
            self._mark_violation(last_child)

        self.generic_visit(node)


class TryShouldntRaiseAnalyzer(BaseAnalyzer, ast.NodeVisitor):
    violation_code = codes.RAISE_WITHIN_TRY

    def _iter_body(self, node: ast.Try) -> Generator[ast.stmt, None, None]:
        for body_child in node.body:
            yield body_child
            yield from ast.iter_child_nodes(body_child)

    @visit_error_handler
    def visit_Try(self, node: ast.Try) -> None:
        raises_within_try = [
            child for child in self._iter_body(node) if isinstance(child, ast.Raise)
        ]

        self._mark_violation(*raises_within_try)

        self.generic_visit(node)
