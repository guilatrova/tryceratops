import ast
from typing import Iterable

from ast_selector import AstSelector

from tryceratops.violations import RaiseWithoutCauseViolation, VerboseReraiseViolation, codes

from .base import BaseAnalyzer, visit_error_handler


class ExceptReraiseWithoutCauseAnalyzer(BaseAnalyzer):
    violation_code = codes.RERAISE_NO_CAUSE
    violation_type = RaiseWithoutCauseViolation

    @visit_error_handler
    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        query = AstSelector("Raise[exc is Call][cause is None]", node)
        reraises_no_cause = query.all()

        self._mark_violation(*reraises_no_cause, exception_name=node.name, except_node=node)
        self.generic_visit(node)


class ExceptVerboseReraiseAnalyzer(BaseAnalyzer):
    violation_code = codes.VERBOSE_RERAISE
    violation_type = VerboseReraiseViolation

    @visit_error_handler
    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        # If no name is set, then it's impossible to be verbose
        # since you don't have the object
        if node.name:
            query = AstSelector(f"Raise[exc is Name].exc[id = {node.name}] $Raise", node)
            children = query.all()

            self._mark_violation(*children, exception_name=node.name)

        self.generic_visit(node)


class ExceptBroadPassAnalyzer(BaseAnalyzer):
    violation_code = codes.IGNORING_EXCEPTION

    def _is_vanilla_exception(self, node: ast.expr) -> bool:
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


class LogErrorAnalyzer(BaseAnalyzer):
    violation_code = codes.USE_LOGGING_EXCEPTION

    @visit_error_handler
    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        query = AstSelector("Expr[value is Call].value[func is Attribute].func[attr = error]", node)
        violations = query.all()

        self._mark_violation(*violations)

        self.generic_visit(node)


class LogObjectAnalyzer(BaseAnalyzer):
    violation_code = codes.VERBOSE_LOG_MESSAGE

    def _has_object_reference(self, node: ast.AST) -> bool:
        if isinstance(node, ast.Name):
            if node.id == self.exception_object_name:
                return True

        return False

    def _check_args(self, log_args: Iterable[ast.AST]) -> None:
        for arg in log_args:
            for node in ast.walk(arg):
                if self._has_object_reference(node):
                    self._mark_violation(node)

    def _find_violations(self, node: ast.ExceptHandler) -> None:
        query = AstSelector(
            "Expr[value is Call].value[func is Attribute].func[attr = exception] $Expr.value",
            node,
        )
        log_wraps = query.all()

        for possible_log_wrap in log_wraps:
            self._check_args(possible_log_wrap.args)

    @visit_error_handler
    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        # If no name is set, then it's impossible to be verbose
        # since you don't have the object
        if node.name:
            self.exception_object_name = node.name
            self._find_violations(node)

        self.generic_visit(node)
