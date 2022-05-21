import ast
from typing import Union

from tryceratops.violations import codes

from .base import BaseAnalyzer

STANDARD_NON_TYPE_ERROR_IDS = (
    "ArithmeticError",
    "AssertionError",
    "AttributeError",
    "BufferError",
    "EOFError",
    "Exception",
    "ImportError",
    "LookupError",
    "MemoryError",
    "NameError",
    "ReferenceError",
    "RuntimeError",
    "SyntaxError",
    "SystemError",
    "ValueError",
)


class PreferTypeErrorAnalyzer(BaseAnalyzer):
    violation_code = codes.PREFER_TYPE_ERROR

    def _is_checking_type(self, node: Union[ast.stmt, ast.expr]) -> bool:
        if isinstance(node, ast.If):
            return self._is_checking_type(node.test) and all(
                [self._is_checking_type(stm) for stm in node.orelse if isinstance(stm, ast.If)]
            )
        if isinstance(node, ast.UnaryOp):
            return self._is_checking_type(node.operand)
        if isinstance(node, ast.BoolOp):
            return all([self._is_checking_type(value) for value in node.values])
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in ("isinstance", "issubclass", "callable"):
                    return True
        return False

    def _check_is_raise_other_than_typeerror(self, node: ast.Raise) -> None:
        if isinstance(node.exc, ast.Call):
            if isinstance(node.exc.func, ast.Name):
                if node.exc.func.id in STANDARD_NON_TYPE_ERROR_IDS:
                    self._mark_violation(node.exc.func)
        elif isinstance(node.exc, ast.Name):
            if node.exc.id in STANDARD_NON_TYPE_ERROR_IDS:
                self._mark_violation(node.exc)

    def _check_for_raises(self, node: ast.stmt) -> None:
        for stm in ast.iter_child_nodes(node):
            if isinstance(stm, ast.Raise):
                self._check_is_raise_other_than_typeerror(stm)
        if isinstance(node, ast.If):
            for stm in node.orelse:
                self._check_for_raises(stm)

    def visit_If(self, node: ast.If) -> None:
        if self._is_checking_type(node):
            self._check_for_raises(node)
