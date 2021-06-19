import ast
from abc import ABC
from typing import Dict, List, Protocol

from .violations import Violation, codes


class BaseAnalyzer(ABC):
    def __init__(self):
        self.violations: List[Violation] = []

    def check(self, tree: ast.AST) -> List[Violation]:
        self.visit(tree)
        return self.violations


class CallTooManyAnalyzer(BaseAnalyzer, ast.NodeVisitor):
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        try_blocks = [stm for stm in node.body if isinstance(stm, ast.Try)]

        if len(try_blocks) > 1:
            _, *violation_blocks = try_blocks
            code, msg = codes.TOO_MANY_TRY
            violations = [
                Violation(code, block.lineno, block.col_offset, msg)
                for block in violation_blocks
            ]
            self.violations += violations

        self.generic_visit(node)


class CallRaiseVanillaAnalyzer(BaseAnalyzer, ast.NodeVisitor):
    def visit_Raise(self, node: ast.Raise):
        if exc := node.exc:
            raise_class_id = exc.func.id
            args = exc.args

            if raise_class_id == "Exception":
                code, msg = codes.RAISE_VANILLA_CLASS
                self.violations.append(
                    Violation(code, node.lineno, node.col_offset, msg)
                )

            if len(args):
                first_arg, *_ = args
                is_constant_str = isinstance(first_arg, ast.Constant) and isinstance(
                    first_arg.value, str
                )

                if is_constant_str:
                    code, msg = codes.RAISE_VANILLA_ARGS
                    self.violations.append(
                        Violation(code, node.lineno, node.col_offset, msg)
                    )

        self.generic_visit(node)


class StmtBodyProtocol(Protocol):
    body: List[ast.stmt]


class CallAvoidCheckingToContinueAnalyzer(BaseAnalyzer):
    def __init__(self):
        self.assignments_from_calls: Dict[str, ast.Assign] = {}
        super().__init__()

    def _scan_assignments(self, node: StmtBodyProtocol):
        def is_assigned_from_call(node: ast.stmt) -> bool:
            if isinstance(node, ast.Assign):
                if isinstance(node.value, ast.Call):
                    return True
                else:
                    self.assignments_from_calls.pop(node.targets[0].id, None)
            return False

        raw_assignments = [stm for stm in node.body if is_assigned_from_call(stm)]
        # TODO: What if there's more targets?
        assignments = {raw.targets[0].id: raw for raw in raw_assignments}
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
                    callable_name = assignment.value.func.id
                    msg = rawmsg.format(callable_name)
                    self.violations.append(
                        Violation(code, if_stmt.lineno, if_stmt.col_offset, msg)
                    )
            elif isinstance(test, ast.UnaryOp):
                if isinstance(test.operand, ast.Name):
                    if assignment := self.assignments_from_calls.get(test.operand.id):
                        callable_name = assignment.value.func.id
                        msg = rawmsg.format(callable_name)
                        self.violations.append(
                            Violation(code, if_stmt.lineno, if_stmt.col_offset, msg)
                        )

    def _scan_deeper(self, node: StmtBodyProtocol, may_contain_violations: bool):
        self._scan_assignments(node)

        if may_contain_violations:
            self._find_violations(node)
        else:
            *_, last_stm = node.body
            if isinstance(last_stm, ast.Return):
                may_contain_violations = True

        for child in node.body:
            if hasattr(child, "body"):
                self._scan_deeper(child, may_contain_violations)

    def check(self, tree: ast.AST) -> List[Violation]:
        for node in ast.walk(tree):
            # for child in ast.iter_child_nodes(node):
            if isinstance(node, ast.Module):
                self._scan_deeper(node, False)

        return self.violations
