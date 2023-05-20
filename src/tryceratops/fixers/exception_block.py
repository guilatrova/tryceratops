import ast
import re
import typing as t

from tryceratops.violations import codes
from tryceratops.violations.violations import (
    RaiseWithoutCauseViolation,
    VerboseReraiseViolation,
    Violation,
)

from .base import BaseFixer


class VerboseReraiseFixer(BaseFixer[VerboseReraiseViolation]):
    violation_code = codes.VERBOSE_RERAISE

    def perform_fix(self, lines: t.List[str], violation: VerboseReraiseViolation) -> t.List[str]:
        all_lines = lines[:]

        guilty_line = all_lines[violation.line - 1]
        new_line = re.sub(rf"raise {violation.exception_name}", "raise", guilty_line)
        all_lines[violation.line - 1] = new_line

        return all_lines


class RaiseWithoutCauseFixer(BaseFixer[RaiseWithoutCauseViolation]):
    violation_code = codes.RERAISE_NO_CAUSE
    exception_name_to_create = "ex"

    def _fix_except_handler(
        self, all_lines: t.List[str], offending_node: ast.ExceptHandler
    ) -> None:
        line_offset = offending_node.lineno - 1
        offending_line = all_lines[line_offset]

        new_line = re.sub(
            r"except (.*):", rf"except \1 as {self.exception_name_to_create}:", offending_line
        )

        all_lines[line_offset] = new_line

    def _fix_raise_no_cause(
        self, all_lines: t.List[str], violation: RaiseWithoutCauseViolation, exception_name: str
    ) -> None:
        endline = violation.node.end_lineno or violation.line
        is_singleline = violation.line == endline

        if is_singleline:
            fix_offset = violation.line - 1
            guilty_line = all_lines[fix_offset]
            new_line = re.sub(r"raise (.*)", rf"raise \1 from {exception_name}", guilty_line)
        else:
            fix_offset = endline - 1
            guilty_line = all_lines[fix_offset]
            new_line = re.sub(r"(\))(.*)", rf"\1 from {exception_name}\2", guilty_line)

        all_lines[fix_offset] = new_line

    def perform_fix(self, lines: t.List[str], violation: RaiseWithoutCauseViolation) -> t.List[str]:
        all_lines = lines[:]
        exception_name = violation.exception_name

        if exception_name is None:
            self._fix_except_handler(all_lines, violation.except_node)
            exception_name = self.exception_name_to_create

        self._fix_raise_no_cause(all_lines, violation, exception_name)

        return all_lines


class LoggerErrorFixer(BaseFixer[Violation]):
    violation_code = codes.USE_LOGGING_EXCEPTION

    def perform_fix(self, lines: t.List[str], violation: Violation) -> t.List[str]:
        all_lines = lines[:]

        guilty_line = all_lines[violation.line - 1]
        new_line = guilty_line.replace(".error(", ".exception(")
        all_lines[violation.line - 1] = new_line

        return all_lines
