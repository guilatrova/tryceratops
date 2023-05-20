import ast
import os

from tryceratops.files.parser import parse_file
from tryceratops.settings import IgnoreViolation


def get_full_path(filename: str):
    ref_dir = f"{os.path.dirname(__file__)}/samples/ignore_comments/"
    path = f"{ref_dir}{filename}.py"
    return path


def test_parse_ignore_line():
    filename = get_full_path("ignore_line")
    tree, filter = parse_file(filename)
    ignore_lines = filter.ignore_lines

    assert isinstance(tree, ast.AST)
    assert len(ignore_lines) == 3
    assert all([ignore.code is None for ignore in ignore_lines])

    first, second, third = ignore_lines
    assert first.line == 13
    assert second.line == 21
    assert third.line == 30


def test_parse_specific_code_line():
    filename = get_full_path("ignore_line_specific")
    tree, filter = parse_file(filename)
    ignore_lines = filter.ignore_lines

    assert isinstance(tree, ast.AST)
    assert len(ignore_lines) == 3

    first, second, third = ignore_lines
    assert first.line == 13
    assert first.code == ["TRY202"]

    assert second.line == 21
    assert second.code == ["TRY202", "TRY200", "TRY201"]

    assert third.line == 30
    assert third.code == ["TRY101"]


def test_parse_ignore_file():
    filename = get_full_path("ignore_file")
    tree, filter = parse_file(filename)
    ignore_lines = filter.ignore_lines

    assert isinstance(tree, ast.AST)
    assert len(ignore_lines) == 2

    ignore, *_ = ignore_lines
    assert ignore.line == 1
    assert ignore.code is None


def test_entity_ignores_all():
    ignore = IgnoreViolation(10)

    assert ignore.is_ignoring(10, "TRY200") is True
    assert ignore.is_ignoring(10, "TRY100") is True
    assert ignore.is_ignoring(10, "TRY300") is True
    assert ignore.is_ignoring(10, "anything") is True

    assert ignore.is_ignoring(12, "TRY200") is False
    assert ignore.is_ignoring(12, "TRY100") is False
    assert ignore.is_ignoring(12, "TRY300") is False
    assert ignore.is_ignoring(12, "anything") is False


def test_entity_ignores_specific():
    ignore = IgnoreViolation(10, ["TRY200", "TRY101"])

    assert ignore.is_ignoring(10, "TRY200") is True
    assert ignore.is_ignoring(10, "TRY101") is True
    assert ignore.is_ignoring(10, "TRY100") is False
    assert ignore.is_ignoring(10, "TRY300") is False
    assert ignore.is_ignoring(10, "anything") is False


def test_entity_ignore_all_whole_file():
    ignore = IgnoreViolation(1)

    assert ignore.is_ignoring(10, "TRY200") is True
    assert ignore.is_ignoring(10, "TRY100") is True
    assert ignore.is_ignoring(10, "TRY300") is True
    assert ignore.is_ignoring(10, "anything") is True

    # Still true
    assert ignore.is_ignoring(12, "TRY200") is True
    assert ignore.is_ignoring(12, "TRY100") is True
    assert ignore.is_ignoring(12, "TRY300") is True
    assert ignore.is_ignoring(12, "anything") is True


def test_entity_ignore_specific_whole_file():
    ignore = IgnoreViolation(1, ["TRY200", "TRY101"])

    # Any line
    assert ignore.is_ignoring(10, "TRY200") is True
    assert ignore.is_ignoring(10, "TRY101") is True
    assert ignore.is_ignoring(20, "TRY200") is True
    assert ignore.is_ignoring(20, "TRY101") is True
    assert ignore.is_ignoring(30, "TRY200") is True
    assert ignore.is_ignoring(30, "TRY101") is True

    # Any other violation
    assert ignore.is_ignoring(10, "TRY300") is False
    assert ignore.is_ignoring(10, "anything") is False
    assert ignore.is_ignoring(20, "TRY002") is False
    assert ignore.is_ignoring(30, "TRY301") is False
    assert ignore.is_ignoring(30, "anything") is False
