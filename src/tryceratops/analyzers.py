import ast
from abc import ABC
from typing import List

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
