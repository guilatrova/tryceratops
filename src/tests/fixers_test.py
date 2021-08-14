import ast
from typing import List, Tuple

from tryceratops.fixers import VerboseReraiseFixer
from tryceratops.violations import codes
from tryceratops.violations.violations import Violation

from .analyzer_helpers import read_sample_lines


def create_violation(code: Tuple[str, str], line: int):
    return Violation(code[0], line, 0, "", "")


def assert_ast_is_valid(results: List[str]):
    content = "\n".join(results)
    result = ast.parse(content)
    assert result is not None


def assert_unmodified_lines(initial: List[str], results: List[str], modified_offset: int):
    assert len(results) == len(initial)
    assert results[:modified_offset] == initial[:modified_offset]
    assert results[modified_offset + 1 :] == initial[modified_offset + 1 :]


def test_verbose_fixer():
    fixer = VerboseReraiseFixer()
    lines = read_sample_lines("except_verbose_reraise")
    expected_modified_line = 20
    expected_modified_offset = expected_modified_line - 1
    violation = create_violation(codes.VERBOSE_RERAISE, expected_modified_line)

    results = fixer.perform_fix(lines, violation)
    print(f"result: '{results[expected_modified_offset]}'")

    assert_ast_is_valid(results)
    assert_unmodified_lines(lines, results, expected_modified_offset)
    assert results[expected_modified_offset].endswith("raise  # This is verbose\n")
