from __future__ import annotations

from typing import TYPE_CHECKING, Set

from . import call, conditional, exception_block, try_block
from .base import BaseAnalyzer

if TYPE_CHECKING:
    from tryceratops.filters import GlobalSettings


ANALYZER_CLASSES = {
    call.CallTooManyAnalyzer,  # type: ignore
    call.CallRaiseVanillaAnalyzer,  # type: ignore
    call.CallRaiseLongArgsAnalyzer,  # type: ignore
    call.CallAvoidCheckingToContinueAnalyzer,  # type: ignore
    conditional.PreferTypeErrorAnalyzer,
    exception_block.ExceptReraiseWithoutCauseAnalyzer,
    exception_block.ExceptVerboseReraiseAnalyzer,
    exception_block.ExceptBroadPassAnalyzer,
    exception_block.LogErrorAnalyzer,
    exception_block.LogObjectAnalyzer,
    try_block.TryConsiderElseAnalyzer,
    try_block.TryShouldntRaiseAnalyzer,
}


def get_analyzer_chain(global_settings: GlobalSettings) -> Set[BaseAnalyzer]:
    analyzers = {
        analyzercls()
        for analyzercls in ANALYZER_CLASSES
        if global_settings.should_run_processor(analyzercls)
    }
    return analyzers
