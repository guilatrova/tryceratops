import logging
from dataclasses import dataclass
from typing import List, Set, Type

from tryceratops.filters import GlobalFilter
from tryceratops.types import ParsedFilesType
from tryceratops.violations import Violation

from . import call as call_analyzers
from . import exception_block as except_analyzers
from . import try_block as try_analyzers
from .base import BaseAnalyzer

logger = logging.getLogger(__name__)


ANALYZER_CLASSES = {
    call_analyzers.CallTooManyAnalyzer,
    call_analyzers.CallRaiseVanillaAnalyzer,
    call_analyzers.CallRaiseLongArgsAnalyzer,
    call_analyzers.CallAvoidCheckingToContinueAnalyzer,
    except_analyzers.ExceptReraiseWithoutCauseAnalyzer,
    except_analyzers.ExceptVerboseReraiseAnalyzer,
    except_analyzers.ExceptBroadPassAnalyzer,
    try_analyzers.TryConsiderElseAnalyzer,
    try_analyzers.TryShouldntRaiseAnalyzer,
}


def _get_analyzer_chain(global_filter: GlobalFilter) -> Set[BaseAnalyzer]:
    analyzers = {
        analyzercls()
        for analyzercls in ANALYZER_CLASSES
        if global_filter.should_run_analyzer(analyzercls)
    }
    return analyzers


@dataclass
class RuntimeError:
    filename: str
    analyzer: Type[BaseAnalyzer]
    exception: Exception


class Runner:
    def __init__(self):
        self.runtime_errors: List[RuntimeError] = []
        self.violations: List[Violation] = []
        self.analyzed_files: int = 0
        self.excluded_files: int = 0

    def _clear(self):
        self.violations = []
        self.runtime_errors = []
        self.excluded_files = 0

    def analyze(self, trees: ParsedFilesType, global_filter: GlobalFilter) -> List[Violation]:
        analyzers = _get_analyzer_chain(global_filter)
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

        return self.violations

    @property
    def had_issues(self) -> bool:
        return len(self.runtime_errors) > 0

    @property
    def any_violation(self) -> bool:
        return len(self.violations) > 0
