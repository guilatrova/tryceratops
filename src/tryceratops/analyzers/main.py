import logging
from dataclasses import dataclass
from typing import List, Set, Type

from tryceratops.types import ParsedFilesType
from tryceratops.violations import Violation

from . import call as call_analyzers
from . import exception_block as except_analyzers
from .base import BaseAnalyzer

logger = logging.getLogger(__name__)


ANALYZER_CLASSES = {
    call_analyzers.CallTooManyAnalyzer,
    call_analyzers.CallRaiseVanillaAnalyzer,
    call_analyzers.CallAvoidCheckingToContinueAnalyzer,
    except_analyzers.ExceptReraiseWithoutCauseAnalyzer,
    except_analyzers.ExceptVerboseReraiseAnalyzer,
    except_analyzers.ExceptBroadPassAnalyzer,
}


def _get_analyzer_chain(include_experimental=False) -> Set[BaseAnalyzer]:
    if include_experimental:
        analyzer_classes = ANALYZER_CLASSES
    else:
        analyzer_classes = {
            analyzercls for analyzercls in ANALYZER_CLASSES if analyzercls.EXPERIMENTAL is False
        }

    analyzers = {analyzercls() for analyzercls in analyzer_classes}
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

    def _clear(self):
        self.violations = []
        self.runtime_errors = []

    def analyze(self, trees: ParsedFilesType, include_experimental: bool) -> List[Violation]:
        analyzers = _get_analyzer_chain(include_experimental)
        self._clear()
        self.analyzed_files = len(trees)

        for filename, tree in trees:
            for analyzer in analyzers:
                try:
                    self.violations += analyzer.check(tree, filename)
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
