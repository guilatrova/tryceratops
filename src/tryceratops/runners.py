import logging
from dataclasses import dataclass
from typing import List, Type

from tryceratops.analyzers import BaseAnalyzer, get_analyzer_chain
from tryceratops.filters import GlobalFilter
from tryceratops.fixers import VerboseReraiseFixer
from tryceratops.types import ParsedFilesType
from tryceratops.violations import Violation

logger = logging.getLogger(__name__)


@dataclass
class RuntimeError:
    filename: str
    analyzer: Type[BaseAnalyzer]
    exception: Exception


class Runner:
    def __init__(self):
        self.runtime_errors: List[RuntimeError] = []
        self.violations: List[Violation] = []
        self.analyzed_files = 0
        self.excluded_files = 0
        self.fixes_made = 0

    def _clear(self):
        self.violations = []
        self.runtime_errors = []
        self.excluded_files = 0

    def analyze(self, trees: ParsedFilesType, global_filter: GlobalFilter) -> List[Violation]:
        analyzers = get_analyzer_chain(global_filter)
        self._clear()
        self.analyzed_files = len(trees)

        for filename, tree, filefilter in trees:
            if global_filter.should_skip_file(filename):
                self.analyzed_files -= 1
                self.excluded_files += 1
                continue

            for analyzer in analyzers:
                try:
                    found_violations = analyzer.check(tree, filename)
                    valid_violations = [
                        violation
                        for violation in found_violations
                        if not filefilter.ignores_violation(violation)
                    ]
                    self.violations += valid_violations
                except Exception as ex:
                    logger.exception(
                        f"Exception raised when running {type(analyzer)} on {filename}"
                    )
                    self.runtime_errors.append(RuntimeError(filename, type(analyzer), ex))

            if global_filter.autofix and self.any_violation:
                fixer = VerboseReraiseFixer()
                fixer.fix(self.violations)
                self.fixes_made += 1

        return self.violations

    @property
    def had_issues(self) -> bool:
        return len(self.runtime_errors) > 0

    @property
    def any_violation(self) -> bool:
        return len(self.violations) > 0
