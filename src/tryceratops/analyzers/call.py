import ast
from typing import Dict, List

from tryceratops.violations import Violation, codes

from .base import BaseAnalyzer, BaseRaiseCallableAnalyzer, StmtBodyProtocol, visit_error_handler


class CallTooManyAnalyzer(BaseAnalyzer, ast.NodeVisitor):
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

    def _scan_assignments(self, node: StmtBodyProtocol):
        def is_assigned_from_call(node: ast.stmt) -> bool:
            if isinstance(node, ast.Assign):
                if isinstance(node.value, ast.Call):
                    return True
                else:
                    if hasattr(node.targets[0], "id"):
                        self.assignments_from_calls.pop(node.targets[0].id, None)
            return False

        raw_assignments = [stm for stm in node.body if is_assigned_from_call(stm)]
        # TODO: What if there's more targets?
        assignments = {
            raw.targets[0].id: raw for raw in raw_assignments if hasattr(raw.targets[0], "id")
        }
        self.assignments_from_calls.update(assignments)

    def _find_violations(self, node: StmtBodyProtocol):
        code, rawmsg = codes.CHECK_TO_CONTINUE

        def is_if_returning(node: ast.stmt) -> bool:
            if isinstance(node, ast.If):
                for child in node.body:
                    if isinstance(child, ast.Return):
                        return True
            return False

        ifs_stmt = [stm for stm in node.body if is_if_returning(stm)]
        if is_if_returning(node):
            ifs_stmt.append(node)

        for if_stmt in ifs_stmt:
            test = if_stmt.test
            if isinstance(test, ast.Name):
                if assignment := self.assignments_from_calls.get(test.id):
                    if hasattr(assignment.value.func, "id"):
                        callable_name = assignment.value.func.id
                        msg = rawmsg.format(callable_name)
                        self.violations.append(
                            Violation(code, if_stmt.lineno, if_stmt.col_offset, msg, self.filename)
                        )
            elif isinstance(test, ast.UnaryOp):
                if isinstance(test.operand, ast.Name):
                    if assignment := self.assignments_from_calls.get(test.operand.id):
                        if hasattr(assignment.value.func, "id"):
                            callable_name = assignment.value.func.id
                            msg = rawmsg.format(callable_name)
                            self.violations.append(
                                Violation(
                                    code,
                                    if_stmt.lineno,
                                    if_stmt.col_offset,
                                    msg,
                                    self.filename,
                                )
                            )

    def _scan_deeper(self, node: StmtBodyProtocol, may_contain_violations: bool):
        self._scan_assignments(node)

        if may_contain_violations:
            self._find_violations(node)
        else:
            if node.body:
                *_, last_stm = node.body
                if isinstance(last_stm, ast.Return):
                    may_contain_violations = True

        for child in node.body:
            if hasattr(child, "body"):
                self._scan_deeper(child, may_contain_violations)

    def check(self, tree: ast.AST, filename: str) -> List[Violation]:
        self.filename = filename
        self.violations = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Module):
                self._scan_deeper(node, False)

        return self.violations
