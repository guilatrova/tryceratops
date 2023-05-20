import ast
import logging
from dataclasses import dataclass
from typing import List, Set, Type

from tryceratops.analyzers import BaseAnalyzer, get_analyzer_chain
from tryceratops.filters import FileFilter, GlobalSettings
from tryceratops.fixers import BaseFixer, get_fixers_chain
from tryceratops.processors import Processor
from tryceratops.types import ParsedFilesType
from tryceratops.violations import Violation

logger = logging.getLogger(__name__)


@dataclass
class RuntimeError:
    filename: str
    processor: Type[Processor]
    exception: Exception


class Runner:
    def __init__(self) -> None:
        self.runtime_errors: List[RuntimeError] = []
        self.violations: List[Violation] = []
        self.analyzed_files = 0
        self.excluded_files = 0
        self.fixed_violations = 0

    def _clear(self) -> None:
        self.violations = []
        self.runtime_errors = []
        self.excluded_files = 0

    def _run_analyzers(
        self, analyzers: Set[BaseAnalyzer], filename: str, filefilter: FileFilter, tree: ast.AST
    ) -> None:
        for analyzer in analyzers:
            try:
                found_violations = analyzer.check(tree, filename)
                valid_violations = [
                    violation
                    for violation in found_violations
                    if not filefilter.ignores_violation(violation)
                ]
            except Exception as ex:
                logger.exception(
                    f"Exception raised when running Analyzer: {type(analyzer)} on {filename}"
                )
                self.runtime_errors.append(RuntimeError(filename, type(analyzer), ex))
            else:
                self.violations += valid_violations

    def _run_fixers(self, fixers: Set[BaseFixer]) -> None:
        for fixer in fixers:
            try:
                fixer.fix(self.violations)
            except Exception as ex:
                logger.exception(f"Exception raised when running Fixer: {type(fixer)}")
                self.runtime_errors.append(RuntimeError("unknown", type(fixer), ex))
            else:
                self.fixed_violations += fixer.fixes_made

    def analyze(self, trees: ParsedFilesType, global_settings: GlobalSettings) -> List[Violation]:
        analyzers = get_analyzer_chain(global_settings)
        fixers = get_fixers_chain(global_settings)
        self._clear()
        self.analyzed_files = len(trees)

        for filename, tree, filefilter in trees:
            if global_settings.should_skip_file(filename):
                self.analyzed_files -= 1
                self.excluded_files += 1
                continue

            self._run_analyzers(analyzers, filename, filefilter, tree)

        if global_settings.autofix and self.any_violation:
            self._run_fixers(fixers)

        return self.violations

    @property
    def had_issues(self) -> bool:
        return len(self.runtime_errors) > 0

    @property
    def any_violation(self) -> bool:
        return len(self.violations) > 0
