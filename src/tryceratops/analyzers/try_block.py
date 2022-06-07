import ast

from ast_selector import AstSelector

from tryceratops.violations import codes

from .base import BaseAnalyzer, visit_error_handler


class TryConsiderElseAnalyzer(BaseAnalyzer):
    violation_code = codes.CONSIDER_ELSE

    @visit_error_handler
    def visit_Try(self, node: ast.Try) -> None:
        *_, last_child = node.body
        theres_more_children = len(node.body) > 1

        if isinstance(last_child, ast.Return) and theres_more_children:
            self._mark_violation(last_child)

        self.generic_visit(node)


class TryShouldntRaiseAnalyzer(BaseAnalyzer):
    violation_code = codes.RAISE_WITHIN_TRY

    @visit_error_handler
    def visit_Try(self, node: ast.Try) -> None:
        query = AstSelector("Try.body Raise", node)
        raises_within_try = query.all()

        self._mark_violation(*raises_within_try)

        self.generic_visit(node)
