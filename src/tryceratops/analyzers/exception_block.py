import ast

from tryceratops.violations import codes

from .base import BaseAnalyzer, visit_error_handler


class ExceptReraiseWithoutCauseAnalyzer(BaseAnalyzer, ast.NodeVisitor):
    violation_code = codes.RERAISE_NO_CAUSE

    @visit_error_handler
    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        def is_raise_without_cause(node: ast.stmt):
            if isinstance(node, ast.Raise):
                return isinstance(node.exc, ast.Call) and node.cause is None
            return False

        reraises_no_cause = [stm for stm in ast.walk(node) if is_raise_without_cause(stm)]
        self._mark_violation(*reraises_no_cause)

        self.generic_visit(node)


class ExceptVerboseReraiseAnalyzer(BaseAnalyzer, ast.NodeVisitor):
    violation_code = codes.VERBOSE_RERAISE

    @visit_error_handler
    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        def is_raise_with_name(stm: ast.stmt, name: str):
            if isinstance(stm, ast.Raise) and isinstance(stm.exc, ast.Name):
                return stm.exc.id == name
            return False

        # If no name is set, then it's impossible to be verbose
        # since you don't have the object
        if node.name:
            for child in ast.walk(node):
                if is_raise_with_name(child, node.name):
                    self._mark_violation(child)

        self.generic_visit(node)


class ExceptBroadPassAnalyzer(BaseAnalyzer, ast.NodeVisitor):
    violation_code = codes.IGNORING_EXCEPTION

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
            self._mark_violation(first_child)

        self.generic_visit(node)
