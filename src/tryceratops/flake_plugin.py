import ast
import importlib.metadata
from tokenize import TokenInfo
from typing import Any, Generator, Iterable, List, Tuple, Type

from tryceratops.files.discovery import load_config
from tryceratops.files.parser import parse_ignore_tokens
from tryceratops.runners import Runner
from tryceratops.settings import FileFilter, GlobalSettings
from tryceratops.violations.violations import Violation

PACKAGE_NAME = "tryceratops"
GLOBAL_DUMMY_FILTER = GlobalSettings(
    include_experimental=False, ignore_violations=[], exclude_dirs=[], autofix=False
)
FLAKE8_VIOLATION_TYPE = Tuple[int, int, str, Type[Any]]
# line, offset, message, class


class TryceratopsAdapterPlugin:
    name = PACKAGE_NAME
    version = importlib.metadata.version(PACKAGE_NAME)

    def __init__(
        self,
        tree: ast.AST,
        filename: str = "undefined",
        file_tokens: Iterable[TokenInfo] = [],
    ) -> None:
        self._tree = tree
        self._filename = filename
        self._runner = Runner()

        ignore_lines = list(parse_ignore_tokens(file_tokens))
        self._file_filter = FileFilter(ignore_lines)
        self._global_settings = self._create_global_settings(filename)

    def _create_global_settings(self, filename: str) -> GlobalSettings:
        pyproj_config = load_config([filename])
        if pyproj_config:
            filter = GlobalSettings.create_from_config(pyproj_config)
            filter.autofix = False  # Do not allow this option for flake8 to avoid confusion
            return filter

        return GLOBAL_DUMMY_FILTER

    def _execute_analyzer(self) -> List[Violation]:
        tryceratops_input = [
            (
                self._filename,
                self._tree,
                self._file_filter,
            )
        ]
        return self._runner.analyze(tryceratops_input, self._global_settings)

    def run(self) -> Generator[FLAKE8_VIOLATION_TYPE, None, None]:
        violations = self._execute_analyzer()

        for violation in violations:
            msg = f"{violation.code} {violation.description}"
            yield violation.line, violation.col, msg, type(self)
