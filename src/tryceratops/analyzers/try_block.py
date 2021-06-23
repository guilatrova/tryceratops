import ast

from tryceratops.violations import Violation, codes

from .base import BaseAnalyzer, visit_error_handler


class TryConsiderElseAnalyzer(BaseAnalyzer, ast.NodeVisitor):
    @visit_error_handler
    def visit_Try(self, node: ast.Try) -> None:
        def is_raise_without_cause(node: ast.stmt):
            if isinstance(node, ast.Raise):
                return isinstance(node.exc, ast.Call) and node.cause is None
            return False

        *_, last_child = node.body
        if isinstance(last_child, ast.Return):
            violation = Violation.build(self.filename, codes.CONSIDER_ELSE, last_child)
            self.violations.append(violation)

        self.generic_visit(node)
