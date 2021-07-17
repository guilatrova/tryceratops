import ast
import importlib.metadata
from tokenize import TokenInfo
from typing import Any, Generator, Iterable, List, Tuple, Type

from tryceratops.analyzers.main import Runner
from tryceratops.files.discovery import load_config
from tryceratops.files.parser import parse_ignore_tokens
from tryceratops.filters import FileFilter, GlobalFilter
from tryceratops.violations.violations import Violation

PACKAGE_NAME = "tryceratops"
GLOBAL_DUMMY_FILTER = GlobalFilter(False, ignore_violations=[], exclude_dirs=[])
FLAKE8_VIOLATION_TYPE = Tuple[int, int, str, Type[Any]]
# line, offset, message, class


class TryceratopsAdapterPlugin:
    name = PACKAGE_NAME
    version = importlib.metadata.version(PACKAGE_NAME)

    def __init__(
        self,
        tree: ast.AST,
        filename: str = None,
        file_tokens: Iterable[TokenInfo] = None,
    ):
        self._tree = tree
        self._filename = filename
        self._runner = Runner()

        ignore_lines = list(parse_ignore_tokens(file_tokens))
        self._file_filter = FileFilter(ignore_lines)
        self._global_filter = self._create_global_filter(filename)

    def _create_global_filter(self, filename: str) -> GlobalFilter:
        pyproj_config = load_config([filename])
        if pyproj_config:
            return GlobalFilter.create_from_config(pyproj_config)

        return GLOBAL_DUMMY_FILTER

    def _execute_analyzer(self) -> List[Violation]:
        tryceratops_input = [
            (
                self._filename,
                self._tree,
                self._file_filter,
            )
        ]
        return self._runner.analyze(tryceratops_input, self._global_filter)

    def run(self) -> Generator[FLAKE8_VIOLATION_TYPE, None, None]:
        violations = self._execute_analyzer()

        for violation in violations:
            msg = f"{violation.code} {violation.description}"
            yield violation.line, violation.col, msg, type(self)
