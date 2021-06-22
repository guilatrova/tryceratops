import ast

from tryceratops.violations import Violation, codes

from .base import BaseAnalyzer, visit_error_handler
from .specifications import (
    ChildrenAre,
    ChildrenFilter,
    NodeHasAttr,
    NodeHasPropEquals,
    NodeHasPropNone,
)


class ExceptReraiseWithoutCauseAnalyzer(BaseAnalyzer, ast.NodeVisitor):
    @visit_error_handler
    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        bad_reraise = ChildrenAre(ast.Raise) + ChildrenFilter(
            NodeHasAttr("exc", ast.Call) & NodeHasPropNone("cause")
        )

        if bad_reraise.is_satisfied_by(node):
            violations = [
                Violation.build(self.filename, codes.RERAISE_NO_CAUSE, block)
                for block in bad_reraise.result
            ]
            self.violations += violations

        self.generic_visit(node)


class ExceptVerboseReraiseAnalyzer(BaseAnalyzer, ast.NodeVisitor):
    @visit_error_handler
    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        # If no name is set, then it's impossible to be verbose
        # since you don't have the object
        if node.name:
            verbose_reraises = ChildrenAre(ast.Raise, direct_children=False) + ChildrenFilter(
                NodeHasAttr("exc", ast.Name) + NodeHasPropEquals("id", node.name)
            )

            if verbose_reraises.is_satisfied_by(node):
                violations = [
                    Violation.build(self.filename, codes.VERBOSE_RERAISE, child)
                    for child in verbose_reraises.result
                ]
                self.violations += violations

        self.generic_visit(node)


class ExceptBroadPassAnalyzer(BaseAnalyzer, ast.NodeVisitor):
    def _is_vanilla_exception(self, node: ast.stmt) -> bool:
        if isinstance(node, ast.Name):
            return node.id == "Exception"
        return False

    def _wraps_vanilla_exception(self, node: ast.ExceptHandler) -> bool:
        if isinstance(node.type, ast.Name):
            return self._is_vanilla_exception(node.type)

        elif isinstance(node.type, ast.Tuple):
            return any(
                [self._is_vanilla_exception(includedtype) for includedtype in node.type.elts]
            )

        return False

    def _is_ellipsis(self, node: ast.stmt) -> bool:
        if isinstance(node, ast.Expr):
            if isinstance(node.value, ast.Constant):
                return node.value.value == ...

        return False

    @visit_error_handler
    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        first_child = node.body[0]
        is_ignoring_exception = isinstance(first_child, ast.Pass) or self._is_ellipsis(first_child)

        if is_ignoring_exception and self._wraps_vanilla_exception(node):
            violation = Violation.build(self.filename, codes.IGNORING_EXCEPTION, first_child)
            self.violations.append(violation)

        self.generic_visit(node)
