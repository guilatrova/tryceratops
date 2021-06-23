import ast
from typing import List

from tryceratops.violations import Violation, codes

from .base import BaseAnalyzer, visit_error_handler
from .specifications import (
    ChildrenAre,
    ChildrenFilter,
    NodeFirstChildIs,
    NodeFirstChildIsEllipsis,
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

    @visit_error_handler
    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        is_ignoring_exception = NodeFirstChildIs(ast.Pass, "body") | NodeFirstChildIsEllipsis()
        is_vanilla_exception = NodeHasAttr("type", ast.Name) + NodeHasPropEquals("id", "Exception")
        wraps_vanilla = (
            NodeHasAttr("type", ast.Tuple)
            + NodeHasAttr("elts")
            + ChildrenFilter(is_vanilla_exception)
        )
        is_violation = is_vanilla_exception | wraps_vanilla

        print(f"is_ignoring_exception: {is_ignoring_exception.is_satisfied_by(node)}")
        print(f"is_vanilla_exception: {is_vanilla_exception.is_satisfied_by(node)}")
        print(f"wraps_vanilla: {wraps_vanilla.is_satisfied_by(node)}")
        print("-" * 20)

        if is_ignoring_exception.is_satisfied_by(node) and is_violation.is_satisfied_by(node):
            first_child = is_ignoring_exception.result
            violation = Violation.build(self.filename, codes.IGNORING_EXCEPTION, first_child)
            self.violations.append(violation)

        self.generic_visit(node)
