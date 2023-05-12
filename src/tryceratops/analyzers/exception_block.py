import ast
from typing import Iterable, Optional

from tryceratops.violations import RaiseWithoutCauseViolation, VerboseReraiseViolation, codes

from .base import BaseAnalyzer, visit_error_handler


class ExceptReraiseWithoutCauseAnalyzer(BaseAnalyzer):
    violation_code = codes.RERAISE_NO_CAUSE
    violation_type = RaiseWithoutCauseViolation

    @visit_error_handler
    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        def is_raise_without_cause(node: ast.AST) -> bool:
            if isinstance(node, ast.Raise):
                return isinstance(node.exc, ast.Call) and node.cause is None
            return False

        reraises_no_cause = [stm for stm in ast.walk(node) if is_raise_without_cause(stm)]
        self._mark_violation(*reraises_no_cause, exception_name=node.name, except_node=node)

        self.generic_visit(node)


class ExceptVerboseReraiseAnalyzer(BaseAnalyzer):
    violation_code = codes.VERBOSE_RERAISE
    violation_type = VerboseReraiseViolation

    @visit_error_handler
    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        def is_raise_with_name(stm: ast.AST, name: str) -> bool:
            if isinstance(stm, ast.Raise) and isinstance(stm.exc, ast.Name):
                return stm.exc.id == name
            return False

        # If no name is set, then it's impossible to be verbose
        # since you don't have the object
        if node.name:
            for child in ast.walk(node):
                if is_raise_with_name(child, node.name):
                    self._mark_violation(child, exception_name=node.name)

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

    def _maybe_get_possible_log_node(self, node: ast.AST) -> Optional[ast.Attribute]:
        if isinstance(node, ast.Expr):
            if isinstance(node.value, ast.Call):
                if isinstance(node.value.func, ast.Attribute):
                    return node.value.func

        return None

    @visit_error_handler
    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        for stm in ast.walk(node):
            if possible_log_node := self._maybe_get_possible_log_node(stm):
                object_method = possible_log_node.attr

                if object_method == "error":
                    self._mark_violation(possible_log_node)

        self.generic_visit(node)


class LogObjectAnalyzer(BaseAnalyzer):
    violation_code = codes.VERBOSE_LOG_MESSAGE

    def _maybe_get_possible_log_wrap(self, node: ast.AST) -> Optional[ast.Call]:
        if isinstance(node, ast.Expr):
            if isinstance(node.value, ast.Call):
                if isinstance(node.value.func, ast.Attribute):
                    return node.value

        return None

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
        for stm in ast.walk(node):
            if possible_log_wrap := self._maybe_get_possible_log_wrap(stm):
                possible_log_node = possible_log_wrap.func

                if isinstance(possible_log_node, ast.Attribute):
                    object_method = possible_log_node.attr

                    if object_method == "exception":
                        self._check_args(possible_log_wrap.args)

    @visit_error_handler
    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        # If no name is set, then it's impossible to be verbose
        # since you don't have the object
        if node.name:
            self.exception_object_name = node.name
            self._find_violations(node)

        self.generic_visit(node)


class UselessTryExceptAnalyzer(BaseAnalyzer):
    violation_code = codes.USELESS_TRY_EXCEPT

    @visit_error_handler
    def visit_Try(self, node: ast.Try) -> None:
        def is_handler_useless(handler: ast.ExceptHandler) -> bool:
            # a handler whose body is just `raise` is considered useless

            if len(handler.body) == 1 and isinstance(handler.body[0], ast.Raise):
                raise_argument = handler.body[0].exc
                return (
                    raise_argument
                    is None
                    # `except ... as e: raise`, no argument
                ) or (
                    isinstance(raise_argument, ast.Name)
                    and raise_argument.id == handler.name
                    # `except ... as e: raise e`
                )
            return False

        if node.handlers and all(is_handler_useless(handler) for handler in node.handlers):
            # the `if node.handlers` is for allowing try-finally cases, without except
            self._mark_violation(node)

        self.generic_visit(node)
