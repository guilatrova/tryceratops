import ast
from abc import ABC, abstractmethod
from typing import Any, Callable, List, Protocol, Type

from tryceratops.processors import Processor
from tryceratops.violations import Violation

from .exceptions import AnalyzerVisitException


class BaseAnalyzer(ABC, Processor, ast.NodeVisitor):
    violation_type: Type[Violation] = Violation

    def __init__(self):
        self.violations: List[Violation] = []

    def _mark_violation(self, *nodes: ast.AST, **kwargs: Any) -> None:  # noqa: ANN401
        klass = self.violation_type
        for node in nodes:
            violation = klass.build(self.filename, self.violation_code, node, **kwargs)
            self.violations.append(violation)

    def check(self, tree: ast.AST, filename: str) -> List[Violation]:
        self.filename = filename
        self.violations = []

        self.visit(tree)

        return self.violations


class StmtBodyProtocol(Protocol):
    body: List[ast.stmt]


def visit_error_handler(func: Callable[[BaseAnalyzer, Any], Any]):  # noqa: ANN201
    def _func(instance: Any, node: ast.stmt) -> None:  # noqa: ANN401
        try:
            return func(instance, node)
        except Exception as ex:
            raise AnalyzerVisitException(node) from ex

    return _func


class BaseRaiseCallableAnalyzer(BaseAnalyzer, ABC):
    @abstractmethod
    def _check_raise_callable(self, node: ast.Raise, exc: ast.Call, func: ast.Name) -> None:
        pass

    @visit_error_handler
    def visit_Raise(self, node: ast.Raise) -> None:
        if exc := node.exc:
            if isinstance(exc, ast.Call):
                if isinstance(exc.func, ast.Name):
                    self._check_raise_callable(node, exc, exc.func)

        self.generic_visit(node)
