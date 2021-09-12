import ast
from typing import List, Tuple
from unittest.mock import MagicMock

from tryceratops.fixers import RaiseWithoutCauseFixer, VerboseReraiseFixer
from tryceratops.violations import RaiseWithoutCauseViolation, VerboseReraiseViolation, codes

from .analyzer_helpers import read_sample_lines


def create_verbose_reraise_violation(code: Tuple[str, str], line: int):
    return VerboseReraiseViolation(code[0], line, 0, "", "", None, "ex")


def create_raise_no_cause_violation(line: int, except_line: int):
    code, _ = codes.RERAISE_NO_CAUSE
    node_mock = MagicMock(spec=ast.Raise, lineno=line)
    except_node_mock = MagicMock(spec=ast.ExceptHandler, lineno=except_line)
    return RaiseWithoutCauseViolation(code, line, 0, "", "", node_mock, except_node_mock)


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


def test_raise_without_cause_fixer_without_exception_name():
    fixer = RaiseWithoutCauseFixer()
    lines = read_sample_lines("except_reraise_no_cause")
    expected_modified_offsets = {14, 15}
    dependent_offset, offending_offset = expected_modified_offsets
    violation = create_raise_no_cause_violation(offending_offset + 1, dependent_offset + 1)

    results = fixer.perform_fix(lines, violation)

    assert_ast_is_valid(results)
    assert_unmodified_lines(lines, results, *expected_modified_offsets)
    assert results[dependent_offset].endswith("except Exception as ex:\n")
    assert results[offending_offset].endswith("raise MyException() from ex\n")
