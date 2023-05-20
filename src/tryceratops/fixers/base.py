from __future__ import annotations

from abc import ABC, abstractmethod
from collections import defaultdict
from types import TracebackType
from typing import Dict, Generic, Iterable, List, Optional, Type, TypeVar

from tryceratops.processors import Processor
from tryceratops.violations import Violation

from .exceptions import FixerFixException

ViolationType = TypeVar("ViolationType", bound=Violation)
GroupedViolations = Dict[str, List[ViolationType]]


class FileFixerHandler:
    def __init__(self, filename: str) -> None:
        self.file = open(filename, "r+", encoding="utf-8")

    def __enter__(self) -> FileFixerHandler:
        return self

    def read_lines(self) -> List[str]:
        lines = self.file.readlines()
        self.file.seek(0)
        return lines

    def write_fix(self, new_lines: Iterable[str]) -> None:
        self.file.writelines(new_lines)
        self.file.truncate()
        self.file.seek(0)

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self.file.close()


class BaseFixer(ABC, Processor, Generic[ViolationType]):
    fixes_made = 0

    def _filter_violations_in_scope(self, violations: List[Violation]) -> List[Violation]:
        scope_code, _ = self.violation_code
        relevant = [vio for vio in violations if vio.code == scope_code]
        return relevant

    def _group_violations_by_filename(self, violations: List[Violation]) -> GroupedViolations:
        group: GroupedViolations = defaultdict(list)
        for violation in violations:
            group[violation.filename].append(violation)

        return group

    def _process_group(self, filename: str, violations: List[ViolationType]) -> None:
        with FileFixerHandler(filename) as file:
            for violation in violations:
                try:
                    file_lines = file.read_lines()
                    resulting_lines = self.perform_fix(file_lines, violation)
                    file.write_fix(resulting_lines)
                except Exception as ex:
                    raise FixerFixException(violation, filename) from ex
                else:
                    self.fixes_made += 1

    @abstractmethod
    def perform_fix(self, lines: List[str], violation: ViolationType) -> List[str]:
        pass

    def fix(self, violations: List[Violation]) -> None:
        relevant_violations = self._filter_violations_in_scope(violations)
        grouped = self._group_violations_by_filename(relevant_violations)

        for filename, file_violations in grouped.items():
            self._process_group(filename, file_violations)
