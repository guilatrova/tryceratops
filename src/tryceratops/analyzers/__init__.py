from __future__ import annotations

from typing import TYPE_CHECKING, Set, Type

from . import call, classdefs, conditional, exception_block, try_block
from .base import BaseAnalyzer

if TYPE_CHECKING:
    from tryceratops.settings import GlobalSettings


ANALYZER_CLASSES: Set[Type[BaseAnalyzer]] = {
    call.CallTooManyAnalyzer,
    call.CallRaiseVanillaAnalyzer,
    call.CallRaiseLongArgsAnalyzer,
    call.CallAvoidCheckingToContinueAnalyzer,
    conditional.PreferTypeErrorAnalyzer,
    classdefs.NonPickableAnalyzer,
    classdefs.InheritFromBaseAnalyzer,
    exception_block.ExceptReraiseWithoutCauseAnalyzer,
    exception_block.ExceptVerboseReraiseAnalyzer,
    exception_block.ExceptBroadPassAnalyzer,
    exception_block.LogErrorAnalyzer,
    exception_block.LogObjectAnalyzer,
    exception_block.UselessTryExceptAnalyzer,
    try_block.TryConsiderElseAnalyzer,
    try_block.TryShouldntRaiseAnalyzer,
}


def get_analyzer_chain(global_settings: GlobalSettings) -> Set[BaseAnalyzer]:
    analyzers = {
        analyzercls(global_settings)
        for analyzercls in ANALYZER_CLASSES
        if global_settings.should_run_processor(analyzercls)
    }
    return analyzers
