import ast
from typing import Iterable, List, Set, Tuple

from tryceratops.violations import Violation

from . import call as call_analyzers
from . import exception_block as except_analyzers
from .base import BaseAnalyzer


def _get_analyzer_chain() -> Set[BaseAnalyzer]:
    analyzers = {
        call_analyzers.CallTooManyAnalyzer(),
        call_analyzers.CallRaiseVanillaAnalyzer(),
        call_analyzers.CallAvoidCheckingToContinueAnalyzer(),
        except_analyzers.ExceptReraiseWithoutCauseAnalyzer(),
        except_analyzers.ExceptVerboseReraiseAnalyzer(),
    }

    return analyzers


def analyze(trees: Iterable[Tuple[str, ast.AST]]) -> List[Violation]:
    violations: List[Violation] = []
    analyzers = _get_analyzer_chain()

    for filename, tree in trees:
        for analyzer in analyzers:
            try:
                violations += analyzer.check(tree, filename)
            except Exception as ex:
                print(f"*** Bug when analyzing {filename}: {ex}")

    return violations
