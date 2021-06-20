import ast
import logging
from dataclasses import dataclass
from typing import Iterable, List, Set, Tuple, Type

from tryceratops.violations import Violation

from . import call as call_analyzers
from . import exception_block as except_analyzers
from .base import BaseAnalyzer

logger = logging.getLogger(__name__)


def _get_analyzer_chain() -> Set[BaseAnalyzer]:
    analyzers = {
        call_analyzers.CallTooManyAnalyzer(),
        call_analyzers.CallRaiseVanillaAnalyzer(),
        call_analyzers.CallAvoidCheckingToContinueAnalyzer(),
        except_analyzers.ExceptReraiseWithoutCauseAnalyzer(),
        except_analyzers.ExceptVerboseReraiseAnalyzer(),
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

    def _clear(self):
        self.violations = []
        self.runtime_errors = []

    def analyze(self, trees: Iterable[Tuple[str, ast.AST]]) -> List[Violation]:
        analyzers = _get_analyzer_chain()
        self._clear()
        self.analyzed_files = len(trees)

        for filename, tree in trees:
            for analyzer in analyzers:
                try:
                    self.violations += analyzer.check(tree, filename)
                except Exception as ex:
                    logger.exception(f"Exception raised when running {type(analyzer)}")
                    self.runtime_errors.append(
                        RuntimeError(filename, type(analyzer), ex)
                    )

        return self.violations

    @property
    def had_issues(self) -> bool:
        return len(self.runtime_errors) > 0
