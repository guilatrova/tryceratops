import re
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Generic, Iterable, List, Tuple, TypeVar

from tryceratops.violations import Violation, codes
from tryceratops.violations.violations import RaiseWithoutCauseViolation, VerboseReraiseViolation


class FileFixerHandler:
    def __init__(self, filename: str):
        self.file = open(filename, "r+")

    def __enter__(self):
        return self

    def read_lines(self) -> Iterable[str]:
        lines = self.file.readlines()
        self.file.seek(0)
        return lines

    def write_fix(self, new_lines: Iterable[str]):
        self.file.writelines(new_lines)
        self.file.truncate()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.file.close()


ViolationType = TypeVar("ViolationType", bound=Violation)
GroupedViolations = dict[str, List[ViolationType]]


class BaseFixer(Generic[ViolationType], ABC):
    violation_code: Tuple[str, str]
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

    def _process_group(self, filename: str, violations: List[ViolationType]):
        with FileFixerHandler(filename) as file:
            for violation in violations:
                file_lines = file.read_lines()
                resulting_lines = self.perform_fix(file_lines, violation)
                file.write_fix(resulting_lines)

                self.fixes_made += 1

    @abstractmethod
    def perform_fix(self, lines: List[str], violation: ViolationType) -> List[str]:
        pass

    def fix(self, violations: List[Violation]):
        relevant_violations = self._filter_violations_in_scope(violations)
        grouped = self._group_violations_by_filename(relevant_violations)

        for filename, file_violations in grouped.items():
            self._process_group(filename, file_violations)


class VerboseReraiseFixer(BaseFixer[VerboseReraiseViolation]):
    violation_code = codes.VERBOSE_RERAISE

    def perform_fix(self, lines: List[str], violation: VerboseReraiseViolation) -> List[str]:
        all_lines = lines[:]

        guilty_line = all_lines[violation.line - 1]
        new_line = re.sub(rf"raise {violation.exception_name}", "raise", guilty_line)
        all_lines[violation.line - 1] = new_line

        return all_lines


class RaiseWithoutCauseFixer(BaseFixer[RaiseWithoutCauseViolation]):
    violation_code = codes.RERAISE_NO_CAUSE
    exception_name_to_create = "ex"

    def _add_name_to_except_handler(self, line: str) -> str:
        # TODO: refactor function name
        new_line = re.sub(r"except (.*):", rf"except \1 as {self.exception_name_to_create}:", line)
        return new_line

    def perform_fix(self, lines: List[str], violation: RaiseWithoutCauseViolation) -> List[str]:
        all_lines = lines[:]
        exception_name = violation.exception_name

        if violation.except_node and exception_name is None:
            # TODO: refactor: calc line, get line, modify line, write line
            dependent_line_offset = violation.except_node.lineno - 1
            dependent_line = all_lines[dependent_line_offset]
            dependent_fixed_line = self._add_name_to_except_handler(dependent_line)
            all_lines[dependent_line_offset] = dependent_fixed_line
            exception_name = self.exception_name_to_create

        guilty_line = all_lines[violation.line - 1]
        # TODO: What if this raise is multi-line?
        new_line = re.sub(r"raise (.*)", rf"raise \1 from {exception_name}", guilty_line)
        all_lines[violation.line - 1] = new_line

        return all_lines
