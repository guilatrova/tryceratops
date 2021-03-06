import ast
import pytest
from typing import List, Optional, Tuple
from unittest.mock import MagicMock

from tryceratops.fixers import RaiseWithoutCauseFixer, VerboseReraiseFixer
from tryceratops.fixers.exception_block import LoggerErrorFixer
from tryceratops.violations import RaiseWithoutCauseViolation, VerboseReraiseViolation, codes
from tryceratops.violations.violations import Violation

from .analyzer_helpers import read_sample_lines


def create_violation(code: Tuple[str, str], line: int):
    node_mock = MagicMock(spec=ast.Raise, lineno=line)
    return Violation(code[0], line, 0, code[1], "filename", node_mock)


def create_verbose_reraise_violation(code: Tuple[str, str], line: int):
    node_mock = MagicMock(spec=ast.Raise, lineno=line)
    return VerboseReraiseViolation(code[0], line, 0, "", "", node_mock, "ex")


def assert_ast_is_valid(results: List[str]):
    content = "\n".join(results)
    result = ast.parse(content)
    assert result is not None


def assert_unmodified_lines(initial: List[str], results: List[str], *modified_offsets: int):
    assert len(results) == len(initial)
    for idx, initial_line in enumerate(initial):
        if idx in modified_offsets:
            continue

        assert initial_line == results[idx], f"Line {idx+1} got modified"


def test_verbose_fixer():
    fixer = VerboseReraiseFixer()
    lines = read_sample_lines("except_verbose_reraise")
    expected_modified_line = 20
    expected_modified_offset = expected_modified_line - 1
    violation = create_verbose_reraise_violation(codes.VERBOSE_RERAISE, expected_modified_line)

    results = fixer.perform_fix(lines, violation)

    assert_ast_is_valid(results)
    assert_unmodified_lines(lines, results, expected_modified_offset)
    assert results[expected_modified_offset].endswith("raise  # This is verbose\n")


def test_logger_error_fixer():
    fixer = LoggerErrorFixer()
    lines = read_sample_lines("log_error")
    expected_modified_line = 15
    expected_modified_offset = expected_modified_line - 1
    violation = create_violation(codes.USE_LOGGING_EXCEPTION, expected_modified_line)

    results = fixer.perform_fix(lines, violation)

    assert_ast_is_valid(results)
    assert_unmodified_lines(lines, results, expected_modified_offset)
    assert results[expected_modified_offset].endswith(
        "logger.exception(\"I'm using 'error', but should be using 'exception'\")\n"
    )


class TestReraiseWithoutCauseFixer:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.fixer = RaiseWithoutCauseFixer()

    def create_raise_no_cause_violation(
        self,
        line: int,
        except_line: int = -1,
        exception_name: Optional[str] = None,
        end_lineno: Optional[int] = None,
    ):
        code, _ = codes.RERAISE_NO_CAUSE
        if not end_lineno:
            end_lineno = line

        node_mock = MagicMock(spec=ast.Raise, lineno=line, end_lineno=end_lineno)
        except_node_mock = MagicMock(spec=ast.ExceptHandler, lineno=except_line)
        return RaiseWithoutCauseViolation(
            code, line, 0, "msg", "filename", node_mock, except_node_mock, exception_name
        )

    def test_without_exception_name(self):
        lines = read_sample_lines("except_reraise_no_cause", dir="autofix")
        expected_modified_offsets = {14, 15}
        dependent_offset, offending_offset = expected_modified_offsets
        violation = self.create_raise_no_cause_violation(offending_offset + 1, dependent_offset + 1)

        results = self.fixer.perform_fix(lines, violation)

        assert_ast_is_valid(results)
        assert_unmodified_lines(lines, results, *expected_modified_offsets)
        assert results[dependent_offset].endswith("except Exception as ex:\n")
        assert results[offending_offset].endswith("raise MyException() from ex\n")

    def test_with_exception_name(self):
        lines = read_sample_lines("except_reraise_no_cause", dir="autofix")
        offending_offset = 22
        violation = self.create_raise_no_cause_violation(
            offending_offset + 1, exception_name="error"
        )

        results = self.fixer.perform_fix(lines, violation)

        assert_ast_is_valid(results)
        assert_unmodified_lines(lines, results, offending_offset)
        assert results[offending_offset].endswith("raise MyException() from error\n")

    def test_multiline_raise(self):
        lines = read_sample_lines("except_reraise_no_cause", dir="autofix")
        expected_modified_offsets = (38, 45)
        offending_offset = 40
        dependent_offset, ending_modified_offset = expected_modified_offsets
        violation = self.create_raise_no_cause_violation(
            offending_offset + 1, dependent_offset + 1, end_lineno=ending_modified_offset + 1
        )

        results = self.fixer.perform_fix(lines, violation)

        assert_ast_is_valid(results)
        assert_unmodified_lines(lines, results, *expected_modified_offsets)
        assert results[dependent_offset].endswith("except Exception as ex:\n")
        assert results[ending_modified_offset].endswith(") from ex  # multiline end!\n")
