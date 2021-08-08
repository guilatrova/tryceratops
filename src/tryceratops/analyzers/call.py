# type: ignore
import ast
from typing import Dict, List

from tryceratops.violations import Violation, codes

from .base import BaseAnalyzer, BaseRaiseCallableAnalyzer, visit_error_handler


class CallTooManyAnalyzer(BaseAnalyzer):
    violation_code = codes.TOO_MANY_TRY

    @visit_error_handler
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        try_blocks = [stm for stm in ast.iter_child_nodes(node) if isinstance(stm, ast.Try)]

        if len(try_blocks) > 1:
            _, *violation_blocks = try_blocks
            self._mark_violation(*violation_blocks)

        self.generic_visit(node)


class CallRaiseVanillaAnalyzer(BaseRaiseCallableAnalyzer):
    violation_code = codes.RAISE_VANILLA_CLASS

    def _check_raise_callable(self, node: ast.Raise, exc: ast.Call, func: ast.Name):
        if func.id == "Exception":
            self._mark_violation(node)


class CallRaiseLongArgsAnalyzer(BaseRaiseCallableAnalyzer):
    violation_code = codes.RAISE_VANILLA_ARGS

    def _check_raise_callable(self, node: ast.Raise, exc: ast.Call, func: ast.Name):
        if len(exc.args):
            first_arg, *_ = exc.args
            is_constant_str = isinstance(first_arg, ast.Constant) and isinstance(
                first_arg.value, str
            )

            WHITESPACE = " "
            if is_constant_str and WHITESPACE in first_arg.value:
                self._mark_violation(node)


class CallAvoidCheckingToContinueAnalyzer(BaseAnalyzer):
    EXPERIMENTAL = True
    violation_code = codes.CHECK_TO_CONTINUE

    def __init__(self):
        self.assignments_from_calls: Dict[str, ast.Assign] = {}
        super().__init__()

    def _mark_violation(self, node: ast.AST, callable_name: str):
        code, rawmsg = codes.CHECK_TO_CONTINUE
        msg = rawmsg.format(callable_name)

        violation = Violation(code, node.lineno, node.col_offset, msg, self.filename)
        self.violations.append(violation)

    def _get_callable_name(self, node: ast.Assign) -> str:
        return getattr(node.value.func, "id", "")

    def _scan_if(self, node: ast.If):
        is_checking_a_variable = isinstance(node.test, ast.Name)
        is_unary_checking_a_variable = isinstance(node.test, ast.UnaryOp) and isinstance(
            node.test.operand, ast.Name
        )

        if is_checking_a_variable:
            target_name = node.test.id
        elif is_unary_checking_a_variable:
            target_name = node.test.operand.id

        if target_name:
            if known_assignment := self.assignments_from_calls.get(target_name):
                if callable_name := self._get_callable_name(known_assignment):
                    self._mark_violation(node, callable_name)

    def visit_Assign(self, node: ast.Assign):
        named_targets = [target for target in node.targets if hasattr(target, "id")]

        if isinstance(node.value, ast.Call):
            # check for "assign = call()"
            targets = {target.id: node for target in named_targets}
            self.assignments_from_calls.update(targets)
        else:
            # clear reference for "assign = x"
            for target in named_targets:
                self.assignments_from_calls.pop(target.id, None)

        self.generic_visit(node)

    def visit_If(self, node: ast.If):
        returning_nodes = (isinstance(child, ast.Return) for child in ast.iter_child_nodes(node))
        if any(returning_nodes):
            self._scan_if(node)

        self.generic_visit(node)

    def check(self, tree: ast.AST, filename: str) -> List[Violation]:
        result = super().check(tree, filename)
        self.assignments_from_calls = {}

        return result
