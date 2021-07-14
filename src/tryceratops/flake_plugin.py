import ast
import importlib.metadata
from typing import Any, Generator, List, Tuple, Type

from tryceratops.analyzers.main import Runner
from tryceratops.filters import FileFilter, GlobalFilter
from tryceratops.violations.violations import Violation

PACKAGE_NAME = "tryceratops"
DUMMY_FILE_FILTER = FileFilter([])
# line, offset, message, class
FLAKE8_VIOLATION_TYPE = Tuple[int, int, str, Type[Any]]


class TryceratopsAdapterPlugin:
    name = PACKAGE_NAME
    version = importlib.metadata.version(PACKAGE_NAME)

    def __init__(self, tree: ast.AST, filename: str = None):
        self._runner = Runner()
        self._global_filter = GlobalFilter(False, ignore_violations=[], exclude_dirs=[])
        self._filename = filename
        self._tree = tree

    def _execute_analyzer(self) -> List[Violation]:
        tryceratops_input = [
            (
                self._filename,
                self._tree,
                DUMMY_FILE_FILTER,
            )
        ]
        return self._runner.analyze(tryceratops_input, self._global_filter)

    def run(self) -> Generator[FLAKE8_VIOLATION_TYPE, None, None]:
        violations = self._execute_analyzer()

        for violation in violations:
            msg = f"{violation.code} {violation.description}"
            yield violation.line, violation.col, msg, type(self)
