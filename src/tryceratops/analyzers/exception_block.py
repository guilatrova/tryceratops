import ast

from tryceratops.violations import Violation, codes

from .base import BaseAnalyzer


class ExceptReraiseWithoutCauseAnalyzer(BaseAnalyzer, ast.NodeVisitor):
    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        code, msg = codes.RERAISE_NO_CAUSE

        def is_raise_without_cause(node: ast.stmt):
            if isinstance(node, ast.Raise):
                return node.cause is None
            return False

        reraises_no_cause = [stm for stm in node.body if is_raise_without_cause(stm)]
        violations = [
            Violation(code, block.lineno, block.col_offset, msg)
            for block in reraises_no_cause
        ]
        self.violations += violations

        self.generic_visit(node)
